# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Copyright (c) 2025 ByteDance Ltd. and/or its affiliates
# Copyright (c) 2025 ByteDance Ltd. and/or its affiliates
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：#
#
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Licensed under the Apache License, Version 2.0 (the "License");
# Licensed under the Apache License, Version 2.0 (the "License");
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# you may not use this file except in compliance with the License.
# you may not use this file except in compliance with the License.
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# You may obtain a copy of the License at
# You may obtain a copy of the License at
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：#
#
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# http:#www.apache.org/licenses/LICENSE-2.0
#     http:#www.apache.org/licenses/LICENSE-2.0
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：#
#
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Unless required by applicable law or agreed to in writing, software
# Unless required by applicable law or agreed to in writing, software
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# distributed under the License is distributed on an "AS IS" BASIS,
# distributed under the License is distributed on an "AS IS" BASIS,
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# See the License for the specific language governing permissions and
# See the License for the specific language governing permissions and
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# limitations under the License.
# limitations under the License.
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from statistics import NormalDist
from statistics import NormalDist

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from diffusers.configuration_utils import register_to_config
from diffusers.configuration_utils import register_to_config
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from diffusers.schedulers import KDPM2DiscreteScheduler
from diffusers.schedulers import KDPM2DiscreteScheduler

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.functional.runge_kutta import reg_x0_euler_step, res_x0_rk2_step
from videoworld2.functional.runge_kutta import reg_x0_euler_step, res_x0_rk2_step


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class RectifiedFlowAB2Scheduler(KDPM2DiscreteScheduler):
class RectifiedFlowAB2Scheduler(KDPM2DiscreteScheduler):
    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@register_to_config
    @register_to_config
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sigma_min: float = 0.002,
        sigma_min: float = 0.002,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sigma_max: float = 80.0,
        sigma_max: float = 80.0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：order: float = 7.0,
        order: float = 7.0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：t_scaling_factor: float = 1.0,
        t_scaling_factor: float = 1.0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：use_double_precision: bool = True,
        use_double_precision: bool = True,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**kpm2_kwargs,
        **kpm2_kwargs,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(
        super().__init__(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prediction_type="epsilon", # placeholder, not used
            prediction_type="epsilon",  # placeholder, not used
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_train_timesteps=1000, # dummy, not used at inference
            num_train_timesteps=1000,  # dummy, not used at inference
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**kpm2_kwargs,
            **kpm2_kwargs,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.gaussian_dist = NormalDist(mu=0.0, sigma=1.0)
        self.gaussian_dist = NormalDist(mu=0.0, sigma=1.0)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def sample_sigma(self, batch_size: int) -> torch.Tensor:
    def sample_sigma(self, batch_size: int) -> torch.Tensor:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cdf_vals = np.random.uniform(size=(batch_size))
        cdf_vals = np.random.uniform(size=(batch_size))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：samples_interval_gaussian = [self.gaussian_dist.inv_cdf(cdf_val) for cdf_val in cdf_vals]
        samples_interval_gaussian = [self.gaussian_dist.inv_cdf(cdf_val) for cdf_val in cdf_vals]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：log_sigma = torch.tensor(samples_interval_gaussian, device="cuda")
        log_sigma = torch.tensor(samples_interval_gaussian, device="cuda")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return torch.exp(log_sigma)
        return torch.exp(log_sigma)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def set_timesteps(self, num_inference_steps, device=None, num_train_timesteps: int | None = N...
    def set_timesteps(self, num_inference_steps, device=None, num_train_timesteps: int | None = None):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Create Karras-like sigma schedule matching Rectified-Flow's paper."""
        """Create Karras-like sigma schedule matching Rectified-Flow's paper."""

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：device = device or torch.device("cpu")
        device = device or torch.device("cpu")

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Create (L + 1) sigma values following Karras et al. (Eq. 5)
        # Create (L + 1) sigma values following Karras et al. (Eq. 5)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_sigma = num_inference_steps + 1
        n_sigma = num_inference_steps + 1
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：i = torch.arange(
        i = torch.arange(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：n_sigma, device=device, dtype=torch.float64 if self.config.use_double_precision else torch.fl...
            n_sigma, device=device, dtype=torch.float64 if self.config.use_double_precision else torch.float32
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Extract values from config to ensure consistency
        # Extract values from config to ensure consistency
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_min = self.config.sigma_min
        sigma_min = self.config.sigma_min
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_max = self.config.sigma_max
        sigma_max = self.config.sigma_max
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：order = self.config.order
        order = self.config.order

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ramp = (sigma_max ** (1 / order)) + i / (n_sigma - 1) * (sigma_min ** (1 / order) - sigma_max...
        ramp = (sigma_max ** (1 / order)) + i / (n_sigma - 1) * (sigma_min ** (1 / order) - sigma_max ** (1 / order))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigmas = ramp**order # shape (n_sigma,)
        sigmas = ramp**order  # shape (n_sigma,)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.sigmas = sigmas.to(dtype=torch.float64 if self.config.use_double_precision else torch.fl...
        self.sigmas = sigmas.to(dtype=torch.float64 if self.config.use_double_precision else torch.float32)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.timesteps = torch.arange(num_inference_steps, device=device, dtype=torch.long)
        self.timesteps = torch.arange(num_inference_steps, device=device, dtype=torch.long)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_inference_steps = num_inference_steps
        self.num_inference_steps = num_inference_steps

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.timesteps
        return self.timesteps

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def step(
    def step(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x0_pred: torch.Tensor,
        x0_pred: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：i: int,
        i: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sample: torch.Tensor,
        sample: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x0_prev: torch.Tensor | None = None,
        x0_prev: torch.Tensor | None = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：generator: torch.Generator | None = None,
        generator: torch.Generator | None = None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Two step Adams-Bashforth (2-AB) evaluation in Rectified Flow form.
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

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dtype_target = sample.dtype
        dtype_target = sample.dtype
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dtype_work = torch.float64 if self.config.use_double_precision else sample.dtype
        dtype_work = torch.float64 if self.config.use_double_precision else sample.dtype

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_t = sample.to(dtype_work)
        x_t = sample.to(dtype_work)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x0_t = x0_pred.to(dtype_work)
        x0_t = x0_pred.to(dtype_work)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_t = self.sigmas[i]
        sigma_t = self.sigmas[i]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_s = self.sigmas[i + 1]
        sigma_s = self.sigmas[i + 1]

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Optional stochastic augment (churn) could be added here (currently not handled)
        # Optional stochastic augment (churn) could be added here (currently not handled)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ones = torch.ones(x_t.shape[0], device=x_t.device, dtype=dtype_work)
        ones = torch.ones(x_t.shape[0], device=x_t.device, dtype=dtype_work)

        # 中文说明：根据条件选择执行分支；代码：if x0_prev is None:
        if x0_prev is None:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# First step – Euler in x0-formulation.
            # 中文说明：First step – Euler in x0-formulation.
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_next, _ = reg_x0_euler_step(
            x_next, _ = reg_x0_euler_step(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_t,
                x_t,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sigma_t * ones,
                sigma_t * ones,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sigma_s * ones,
                sigma_s * ones,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x0_t,
                x0_t,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Subsequent steps – 2-AB using residual formulation.
            # 中文说明：Subsequent steps – 2-AB using residual formulation.
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_next = res_x0_rk2_step(
            x_next = res_x0_rk2_step(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_t,
                x_t,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sigma_s * ones,
                sigma_s * ones,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sigma_t * ones,
                sigma_t * ones,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x0_t,
                x0_t,
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.sigmas[i - 1] * ones, # previous sigma
                self.sigmas[i - 1] * ones,  # previous sigma
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x0_prev,
                x0_prev,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x_next.to(dtype_target), x0_t.to(dtype_target)
        return x_next.to(dtype_target), x0_t.to(dtype_target)
