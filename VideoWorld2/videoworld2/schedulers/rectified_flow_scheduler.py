# Copyright (c) 2025 ByteDance Ltd. and/or its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 阅读：采样调度；首步 Euler，后续结合上一预测做二步更新。
from statistics import NormalDist

import numpy as np
import torch
from diffusers.configuration_utils import register_to_config
from diffusers.schedulers import KDPM2DiscreteScheduler

from videoworld2.functional.runge_kutta import reg_x0_euler_step, res_x0_rk2_step


class RectifiedFlowAB2Scheduler(KDPM2DiscreteScheduler):
    @register_to_config
    def __init__(
        self,
        sigma_min: float = 0.002,
        sigma_max: float = 80.0,
        order: float = 7.0,
        t_scaling_factor: float = 1.0,
        use_double_precision: bool = True,
        **kpm2_kwargs,
    ):
        super().__init__(
            prediction_type="epsilon",  # placeholder, not used
            num_train_timesteps=1000,  # dummy, not used at inference
            **kpm2_kwargs,
        )
        self.gaussian_dist = NormalDist(mu=0.0, sigma=1.0)

    def sample_sigma(self, batch_size: int) -> torch.Tensor:
        cdf_vals = np.random.uniform(size=(batch_size))
        samples_interval_gaussian = [self.gaussian_dist.inv_cdf(cdf_val) for cdf_val in cdf_vals]
        log_sigma = torch.tensor(samples_interval_gaussian, device="cuda")
        # 对正态变量取指数，得到训练使用的对数正态噪声强度。
        return torch.exp(log_sigma)

    def set_timesteps(self, num_inference_steps, device=None, num_train_timesteps: int | None = None):
        """Create Karras-like sigma schedule matching Rectified-Flow's paper."""

        device = device or torch.device("cpu")

        # Create (L + 1) sigma values following Karras et al. (Eq. 5)
        # 采样步数之外再留一个终点，方便每步读取 sigma[i+1]。
        n_sigma = num_inference_steps + 1
        i = torch.arange(
            n_sigma, device=device, dtype=torch.float64 if self.config.use_double_precision else torch.float32
        )

        # Extract values from config to ensure consistency
        sigma_min = self.config.sigma_min
        sigma_max = self.config.sigma_max
        order = self.config.order

        # 在 sigma 的 1/order 次幂空间插值，再恢复 sigma。
        ramp = (sigma_max ** (1 / order)) + i / (n_sigma - 1) * (sigma_min ** (1 / order) - sigma_max ** (1 / order))
        sigmas = ramp**order  # shape (n_sigma,)

        self.sigmas = sigmas.to(dtype=torch.float64 if self.config.use_double_precision else torch.float32)
        self.timesteps = torch.arange(num_inference_steps, device=device, dtype=torch.long)
        self.num_inference_steps = num_inference_steps

        return self.timesteps

    def step(
        self,
        x0_pred: torch.Tensor,
        i: int,
        sample: torch.Tensor,
        x0_prev: torch.Tensor | None = None,
        generator: torch.Generator | None = None,
    ):
        """Two step Adams-Bashforth (2-AB) evaluation in Rectified Flow form.

        Parameters
        ----------
        x0_pred : torch.Tensor
            Prediction of the clean sample at current sigma (sigma_t).
        i : int
            Index in `self.timesteps` (NOT the actual timestep value).
        sample : torch.Tensor
            Current noisy sample x_t.
        x0_prev : torch.Tensor | None
            Cached x0 from the previous step.  `None` on the first call.
        generator : torch.Generator | None
            Unused.  Present for signature compatibility only.
        """

        dtype_target = sample.dtype
        # 可选 float64 做数值更新，返回时恢复 sample 的原精度。
        dtype_work = torch.float64 if self.config.use_double_precision else sample.dtype

        x_t = sample.to(dtype_work)
        x0_t = x0_pred.to(dtype_work)

        sigma_t = self.sigmas[i]
        sigma_s = self.sigmas[i + 1]

        # Optional stochastic augment (churn) could be added here (currently not handled)

        ones = torch.ones(x_t.shape[0], device=x_t.device, dtype=dtype_work)

        # 首步没有历史预测，使用 Euler；后续利用上一轮 x0 做二步更新。
        if x0_prev is None:
            # First step – Euler in x0-formulation.
            x_next, _ = reg_x0_euler_step(
                x_t,
                sigma_t * ones,
                sigma_s * ones,
                x0_t,
            )
        else:
            # Subsequent steps – 2-AB using residual formulation.
            x_next = res_x0_rk2_step(
                x_t,
                sigma_s * ones,
                sigma_t * ones,
                x0_t,
                self.sigmas[i - 1] * ones,  # previous sigma
                x0_prev,
            )

        # 返回下一状态与当前 x0，调用者负责缓存到下一轮。
        return x_next.to(dtype_target), x0_t.to(dtype_target)
