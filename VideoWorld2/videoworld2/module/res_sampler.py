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
# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
"""
A general framework for various sampling algorithm from a diffusion model.
Impl based on
* Refined Exponential Solver (RES) in https://arxiv.org/pdf/2308.02157
* also clude other impl, DDIM, DEIS, DPM-Solver, EDM sampler.
Most of sampling algorihtm, Runge-Kutta, Multi-step, etc, can be impl in this framework by \
    adding new step function in get_runge_kutta_fn or get_multi_step_fn.
"""

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import math
import math
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any, Callable, List, Literal, Optional, Tuple, Union
from typing import Any, Callable, List, Literal, Optional, Tuple, Union

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import attrs
import attrs
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.functional.multi_step import get_multi_step_fn, is_multi_step_fn_supported
from videoworld2.functional.multi_step import get_multi_step_fn, is_multi_step_fn_supported
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.functional.runge_kutta import get_runge_kutta_fn, is_runge_kutta_fn_supported
from videoworld2.functional.runge_kutta import get_runge_kutta_fn, is_runge_kutta_fn_supported
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.config import make_freezable
from imaginaire.config import make_freezable

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：COMMON_SOLVER_OPTIONS = Literal["2ab", "2mid", "1euler"]
COMMON_SOLVER_OPTIONS = Literal["2ab", "2mid", "1euler"]


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@make_freezable
@make_freezable
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class SolverConfig:
class SolverConfig:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：is_multi: bool = False
    is_multi: bool = False
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rk: str = "2mid"
    rk: str = "2mid"
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：multistep: str = "2ab"
    multistep: str = "2ab"
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# following parameters control stochasticity, see EDM paper
    # following parameters control stochasticity, see EDM paper
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# BY default, we use deterministic with no stochasticity
    # BY default, we use deterministic with no stochasticity
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：s_churn: float = 0.0
    s_churn: float = 0.0
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：s_t_max: float = float("inf")
    s_t_max: float = float("inf")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：s_t_min: float = 0.05
    s_t_min: float = 0.05
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：s_noise: float = 1.0
    s_noise: float = 1.0


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@make_freezable
@make_freezable
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class SolverTimestampConfig:
class SolverTimestampConfig:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：nfe: int = 50
    nfe: int = 50
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：t_min: float = 0.002
    t_min: float = 0.002
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：t_max: float = 80.0
    t_max: float = 80.0
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：order: float = 7.0
    order: float = 7.0
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：is_forward: bool = False # whether generate forward or backward timestamps
    is_forward: bool = False  # whether generate forward or backward timestamps


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@make_freezable
@make_freezable
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class SamplerConfig:
class SamplerConfig:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：solver: SolverConfig = attrs.field(factory=SolverConfig)
    solver: SolverConfig = attrs.field(factory=SolverConfig)
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：timestamps: SolverTimestampConfig = attrs.field(factory=SolverTimestampConfig)
    timestamps: SolverTimestampConfig = attrs.field(factory=SolverTimestampConfig)
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sample_clean: bool = True # whether run one last step to generate clean image
    sample_clean: bool = True  # whether run one last step to generate clean image


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_rev_ts(
def get_rev_ts(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：t_min: float, t_max: float, num_steps: int, ts_order: Union[int, float], is_forward: bool = F...
    t_min: float, t_max: float, num_steps: int, ts_order: Union[int, float], is_forward: bool = False
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor:
) -> torch.Tensor:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Generate a sequence of reverse time steps.

    Args:
        t_min (float): The minimum time value.
        t_max (float): The maximum time value.
        num_steps (int): The number of time steps to generate.
        ts_order (Union[int, float]): The order of the time step progression.
        is_forward (bool, optional): If True, returns the sequence in forward order. Defaults to False.

    Returns:
        torch.Tensor: A tensor containing the generated time steps in reverse or forward order.

    Raises:
        ValueError: If `t_min` is not less than `t_max`.
        TypeError: If `ts_order` is not an integer or float.
    """
    # 中文说明：根据条件选择执行分支；代码：if t_min >= t_max:
    if t_min >= t_max:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError("t_min must be less than t_max")
        raise ValueError("t_min must be less than t_max")

    # 中文说明：根据条件选择执行分支；代码：if not isinstance(ts_order, (int, float)):
    if not isinstance(ts_order, (int, float)):
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError("ts_order must be an integer or float")
        raise TypeError("ts_order must be an integer or float")

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：step_indices = torch.arange(num_steps + 1, dtype=torch.float64)
    step_indices = torch.arange(num_steps + 1, dtype=torch.float64)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：time_steps = (
    time_steps = (
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：t_max ** (1 / ts_order) + step_indices / num_steps * (t_min ** (1 / ts_order) - t_max ** (1 /...
        t_max ** (1 / ts_order) + step_indices / num_steps * (t_min ** (1 / ts_order) - t_max ** (1 / ts_order))
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) ** ts_order
    ) ** ts_order

    # 中文说明：根据条件选择执行分支；代码：if is_forward:
    if is_forward:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return time_steps.flip(dims=(0,))
        return time_steps.flip(dims=(0,))

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return time_steps
    return time_steps


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Sampler(torch.nn.Module):
class Sampler(torch.nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, cfg: Optional[SamplerConfig] = None):
    def __init__(self, cfg: Optional[SamplerConfig] = None):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：根据条件选择执行分支；代码：if cfg is None:
        if cfg is None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cfg = SamplerConfig()
            cfg = SamplerConfig()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.cfg = cfg
        self.cfg = cfg

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.no_grad()
    @torch.no_grad()
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(
    def forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x0_fn: Callable,
        x0_fn: Callable,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_sigma_max: torch.Tensor,
        x_sigma_max: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_steps: int = 35,
        num_steps: int = 35,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sigma_min: float = 0.002,
        sigma_min: float = 0.002,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sigma_max: float = 80,
        sigma_max: float = 80,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rho: float = 7,
        rho: float = 7,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：S_churn: float = 0,
        S_churn: float = 0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：S_min: float = 0,
        S_min: float = 0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：S_max: float = float("inf"),
        S_max: float = float("inf"),
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：S_noise: float = 1,
        S_noise: float = 1,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：solver_option: str = "2ab",
        solver_option: str = "2ab",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor:
    ) -> torch.Tensor:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_dtype = x_sigma_max.dtype
        in_dtype = x_sigma_max.dtype

        # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def float64_x0_fn(x_B_StateShape: torch.Tensor, t_B: torch.Tensor) -> torch.Tensor:
        def float64_x0_fn(x_B_StateShape: torch.Tensor, t_B: torch.Tensor) -> torch.Tensor:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return x0_fn(x_B_StateShape.to(in_dtype), t_B.to(in_dtype)).to(torch.float64)
            return x0_fn(x_B_StateShape.to(in_dtype), t_B.to(in_dtype)).to(torch.float64)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_multistep = is_multi_step_fn_supported(solver_option)
        is_multistep = is_multi_step_fn_supported(solver_option)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_rk = is_runge_kutta_fn_supported(solver_option)
        is_rk = is_runge_kutta_fn_supported(solver_option)
        # 中文说明：检查运行时假设是否成立；代码：assert is_multistep or is_rk, f"Only support multistep or Runge-Kutta method, got {solver_opt...
        assert is_multistep or is_rk, f"Only support multistep or Runge-Kutta method, got {solver_option}"

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：solver_cfg = SolverConfig(
        solver_cfg = SolverConfig(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：s_churn=S_churn,
            s_churn=S_churn,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：s_t_max=S_max,
            s_t_max=S_max,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：s_t_min=S_min,
            s_t_min=S_min,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：s_noise=S_noise,
            s_noise=S_noise,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_multi=is_multistep,
            is_multi=is_multistep,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rk=solver_option,
            rk=solver_option,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：multistep=solver_option,
            multistep=solver_option,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：timestamps_cfg = SolverTimestampConfig(nfe=num_steps, t_min=sigma_min, t_max=sigma_max, order...
        timestamps_cfg = SolverTimestampConfig(nfe=num_steps, t_min=sigma_min, t_max=sigma_max, order=rho)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sampler_cfg = SamplerConfig(solver=solver_cfg, timestamps=timestamps_cfg, sample_clean=True)
        sampler_cfg = SamplerConfig(solver=solver_cfg, timestamps=timestamps_cfg, sample_clean=True)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self._forward_impl(float64_x0_fn, x_sigma_max, sampler_cfg).to(in_dtype)
        return self._forward_impl(float64_x0_fn, x_sigma_max, sampler_cfg).to(in_dtype)

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.no_grad()
    @torch.no_grad()
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _forward_impl(
    def _forward_impl(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：denoiser_fn: Callable[[torch.Tensor, torch.Tensor], torch.Tensor],
        denoiser_fn: Callable[[torch.Tensor, torch.Tensor], torch.Tensor],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：noisy_input_B_StateShape: torch.Tensor,
        noisy_input_B_StateShape: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sampler_cfg: Optional[SamplerConfig] = None,
        sampler_cfg: Optional[SamplerConfig] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：callback_fns: Optional[List[Callable]] = None,
        callback_fns: Optional[List[Callable]] = None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor:
    ) -> torch.Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Internal implementation of the forward pass.

        Args:
            denoiser_fn: Function to denoise the input.
            noisy_input_B_StateShape: Input tensor with noise.
            sampler_cfg: Configuration for the sampler.
            callback_fns: List of callback functions to be called during sampling.

        Returns:
            torch.Tensor: Denoised output tensor.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sampler_cfg = self.cfg if sampler_cfg is None else sampler_cfg
        sampler_cfg = self.cfg if sampler_cfg is None else sampler_cfg
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：solver_order = 1 if sampler_cfg.solver.is_multi else int(sampler_cfg.solver.rk[0])
        solver_order = 1 if sampler_cfg.solver.is_multi else int(sampler_cfg.solver.rk[0])
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_timestamps = sampler_cfg.timestamps.nfe // solver_order
        num_timestamps = sampler_cfg.timestamps.nfe // solver_order

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigmas_L = get_rev_ts(
        sigmas_L = get_rev_ts(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sampler_cfg.timestamps.t_min, sampler_cfg.timestamps.t_max, num_timestamps, sampler_cfg.times...
            sampler_cfg.timestamps.t_min, sampler_cfg.timestamps.t_max, num_timestamps, sampler_cfg.timestamps.order
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：).to(noisy_input_B_StateShape.device)
        ).to(noisy_input_B_StateShape.device)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：denoised_output = differential_equation_solver(
        denoised_output = differential_equation_solver(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：denoiser_fn, sigmas_L, sampler_cfg.solver, callback_fns=callback_fns
            denoiser_fn, sigmas_L, sampler_cfg.solver, callback_fns=callback_fns
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)(noisy_input_B_StateShape)
        )(noisy_input_B_StateShape)

        # 中文说明：根据条件选择执行分支；代码：if sampler_cfg.sample_clean:
        if sampler_cfg.sample_clean:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Override denoised_output with fully denoised version
            # Override denoised_output with fully denoised version
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ones = torch.ones(denoised_output.size(0), device=denoised_output.device, dtype=denoised_outp...
            ones = torch.ones(denoised_output.size(0), device=denoised_output.device, dtype=denoised_output.dtype)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：denoised_output = denoiser_fn(denoised_output, sigmas_L[-1] * ones)
            denoised_output = denoiser_fn(denoised_output, sigmas_L[-1] * ones)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return denoised_output
        return denoised_output


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def fori_loop(lower: int, upper: int, body_fun: Callable[[int, Any], Any], init_val: Any) -> ...
def fori_loop(lower: int, upper: int, body_fun: Callable[[int, Any], Any], init_val: Any) -> Any:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Implements a for loop with a function.

    Args:
        lower: Lower bound of the loop (inclusive).
        upper: Upper bound of the loop (exclusive).
        body_fun: Function to be applied in each iteration.
        init_val: Initial value for the loop.

    Returns:
        The final result after all iterations.
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：val = init_val
    val = init_val
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i in range(lower, upper):
    for i in range(lower, upper):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：val = body_fun(i, val)
        val = body_fun(i, val)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return val
    return val


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def differential_equation_solver(
def differential_equation_solver(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x0_fn: Callable[[torch.Tensor, torch.Tensor], torch.Tensor],
    x0_fn: Callable[[torch.Tensor, torch.Tensor], torch.Tensor],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sigmas_L: torch.Tensor,
    sigmas_L: torch.Tensor,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：solver_cfg: SolverConfig,
    solver_cfg: SolverConfig,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：callback_fns: Optional[List[Callable]] = None,
    callback_fns: Optional[List[Callable]] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Callable[[torch.Tensor], torch.Tensor]:
) -> Callable[[torch.Tensor], torch.Tensor]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Creates a differential equation solver function.

    Args:
        x0_fn: Function to compute x0 prediction.
        sigmas_L: Tensor of sigma values with shape [L,].
        solver_cfg: Configuration for the solver.
        callback_fns: Optional list of callback functions.

    Returns:
        A function that solves the differential equation.
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_step = len(sigmas_L) - 1
    num_step = len(sigmas_L) - 1

    # 中文说明：根据条件选择执行分支；代码：if solver_cfg.is_multi:
    if solver_cfg.is_multi:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：update_step_fn = get_multi_step_fn(solver_cfg.multistep)
        update_step_fn = get_multi_step_fn(solver_cfg.multistep)
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：update_step_fn = get_runge_kutta_fn(solver_cfg.rk)
        update_step_fn = get_runge_kutta_fn(solver_cfg.rk)

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：eta = min(solver_cfg.s_churn / (num_step + 1), math.sqrt(1.2) - 1)
    eta = min(solver_cfg.s_churn / (num_step + 1), math.sqrt(1.2) - 1)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def sample_fn(input_xT_B_StateShape: torch.Tensor) -> torch.Tensor:
    def sample_fn(input_xT_B_StateShape: torch.Tensor) -> torch.Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Samples from the differential equation.

        Args:
            input_xT_B_StateShape: Input tensor with shape [B, StateShape].

        Returns:
            Output tensor with shape [B, StateShape].
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ones_B = torch.ones(input_xT_B_StateShape.size(0), device=input_xT_B_StateShape.device, dtype...
        ones_B = torch.ones(input_xT_B_StateShape.size(0), device=input_xT_B_StateShape.device, dtype=torch.float64)

        # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def step_fn(
        def step_fn(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：i_th: int, state: Tuple[torch.Tensor, Optional[List[torch.Tensor]]]
            i_th: int, state: Tuple[torch.Tensor, Optional[List[torch.Tensor]]]
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[torch.Tensor, Optional[List[torch.Tensor]]]:
        ) -> Tuple[torch.Tensor, Optional[List[torch.Tensor]]]:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：input_x_B_StateShape, x0_preds = state
            input_x_B_StateShape, x0_preds = state
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sigma_cur_0, sigma_next_0 = sigmas_L[i_th], sigmas_L[i_th + 1]
            sigma_cur_0, sigma_next_0 = sigmas_L[i_th], sigmas_L[i_th + 1]

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# algorithm 2: line 4-6
            # algorithm 2: line 4-6
            # 中文说明：根据条件选择执行分支；代码：if solver_cfg.s_t_min < sigma_cur_0 < solver_cfg.s_t_max:
            if solver_cfg.s_t_min < sigma_cur_0 < solver_cfg.s_t_max:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hat_sigma_cur_0 = sigma_cur_0 + eta * sigma_cur_0
                hat_sigma_cur_0 = sigma_cur_0 + eta * sigma_cur_0
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_x_B_StateShape = input_x_B_StateShape + (
                input_x_B_StateShape = input_x_B_StateShape + (
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：hat_sigma_cur_0**2 - sigma_cur_0**2
                    hat_sigma_cur_0**2 - sigma_cur_0**2
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：).sqrt() * solver_cfg.s_noise * torch.randn_like(input_x_B_StateShape)
                ).sqrt() * solver_cfg.s_noise * torch.randn_like(input_x_B_StateShape)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_cur_0 = hat_sigma_cur_0
                sigma_cur_0 = hat_sigma_cur_0

            # 中文说明：根据条件选择执行分支；代码：if solver_cfg.is_multi:
            if solver_cfg.is_multi:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x0_pred_B_StateShape = x0_fn(input_x_B_StateShape, sigma_cur_0 * ones_B)
                x0_pred_B_StateShape = x0_fn(input_x_B_StateShape, sigma_cur_0 * ones_B)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：output_x_B_StateShape, x0_preds = update_step_fn(
                output_x_B_StateShape, x0_preds = update_step_fn(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：input_x_B_StateShape, sigma_cur_0 * ones_B, sigma_next_0 * ones_B, x0_pred_B_StateShape, x0_p...
                    input_x_B_StateShape, sigma_cur_0 * ones_B, sigma_next_0 * ones_B, x0_pred_B_StateShape, x0_preds
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：output_x_B_StateShape, x0_preds = update_step_fn(
                output_x_B_StateShape, x0_preds = update_step_fn(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：input_x_B_StateShape, sigma_cur_0 * ones_B, sigma_next_0 * ones_B, x0_fn
                    input_x_B_StateShape, sigma_cur_0 * ones_B, sigma_next_0 * ones_B, x0_fn
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )

            # 中文说明：根据条件选择执行分支；代码：if callback_fns:
            if callback_fns:
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for callback_fn in callback_fns:
                for callback_fn in callback_fns:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：callback_fn(**locals())
                    callback_fn(**locals())

            # 中文说明：从当前函数返回结果或结束函数执行；代码：return output_x_B_StateShape, x0_preds
            return output_x_B_StateShape, x0_preds

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_at_eps, _ = fori_loop(0, num_step, step_fn, [input_xT_B_StateShape, None])
        x_at_eps, _ = fori_loop(0, num_step, step_fn, [input_xT_B_StateShape, None])
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x_at_eps
        return x_at_eps

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return sample_fn
    return sample_fn
