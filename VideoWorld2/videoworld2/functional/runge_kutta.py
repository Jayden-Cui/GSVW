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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Callable, Tuple
from typing import Callable, Tuple

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.functional.batch_ops import batch_mul
from videoworld2.functional.batch_ops import batch_mul


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def phi1(t: torch.Tensor) -> torch.Tensor:
def phi1(t: torch.Tensor) -> torch.Tensor:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Compute the first order phi function: (exp(t) - 1) / t.

    Args:
        t: Input tensor.

    Returns:
        Tensor: Result of phi1 function.
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_dtype = t.dtype
    input_dtype = t.dtype
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t = t.to(dtype=torch.float64)
    t = t.to(dtype=torch.float64)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return (torch.expm1(t) / t).to(dtype=input_dtype)
    return (torch.expm1(t) / t).to(dtype=input_dtype)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def phi2(t: torch.Tensor) -> torch.Tensor:
def phi2(t: torch.Tensor) -> torch.Tensor:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Compute the second order phi function: (phi1(t) - 1) / t.

    Args:
        t: Input tensor.

    Returns:
        Tensor: Result of phi2 function.
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_dtype = t.dtype
    input_dtype = t.dtype
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t = t.to(dtype=torch.float64)
    t = t.to(dtype=torch.float64)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return ((phi1(t) - 1.0) / t).to(dtype=input_dtype)
    return ((phi1(t) - 1.0) / t).to(dtype=input_dtype)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def res_x0_rk2_step(
def res_x0_rk2_step(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_s: torch.Tensor,
    x_s: torch.Tensor,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：t: torch.Tensor,
    t: torch.Tensor,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：s: torch.Tensor,
    s: torch.Tensor,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x0_s: torch.Tensor,
    x0_s: torch.Tensor,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：s1: torch.Tensor,
    s1: torch.Tensor,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x0_s1: torch.Tensor,
    x0_s1: torch.Tensor,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor:
) -> torch.Tensor:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Perform a residual-based 2nd order Runge-Kutta step.

    Args:
        x_s: Current state tensor.
        t: Target time tensor.
        s: Current time tensor.
        x0_s: Prediction at current time.
        s1: Intermediate time tensor.
        x0_s1: Prediction at intermediate time.

    Returns:
        Tensor: Updated state tensor.

    Raises:
        AssertionError: If step size is too small.
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：s = -torch.log(s)
    s = -torch.log(s)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t = -torch.log(t)
    t = -torch.log(t)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：m = -torch.log(s1)
    m = -torch.log(s1)

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dt = t - s
    dt = t - s
    # 中文说明：检查运行时假设是否成立；代码：assert not torch.any(torch.isclose(dt, torch.zeros_like(dt), atol=1e-6)), "Step size is too s...
    assert not torch.any(torch.isclose(dt, torch.zeros_like(dt), atol=1e-6)), "Step size is too small"
    # 中文说明：检查运行时假设是否成立；代码：assert not torch.any(torch.isclose(m - s, torch.zeros_like(dt), atol=1e-6)), "Step size is to...
    assert not torch.any(torch.isclose(m - s, torch.zeros_like(dt), atol=1e-6)), "Step size is too small"

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：c2 = (m - s) / dt
    c2 = (m - s) / dt
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：phi1_val, phi2_val = phi1(-dt), phi2(-dt)
    phi1_val, phi2_val = phi1(-dt), phi2(-dt)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Handle edge case where t = s = m
    # Handle edge case where t = s = m
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：b1 = torch.nan_to_num(phi1_val - 1.0 / c2 * phi2_val, nan=0.0)
    b1 = torch.nan_to_num(phi1_val - 1.0 / c2 * phi2_val, nan=0.0)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：b2 = torch.nan_to_num(1.0 / c2 * phi2_val, nan=0.0)
    b2 = torch.nan_to_num(1.0 / c2 * phi2_val, nan=0.0)

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return batch_mul(torch.exp(-dt), x_s) + batch_mul(dt, batch_mul(b1, x0_s) + batch_mul(b2, x0_...
    return batch_mul(torch.exp(-dt), x_s) + batch_mul(dt, batch_mul(b1, x0_s) + batch_mul(b2, x0_s1))


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def reg_x0_euler_step(
def reg_x0_euler_step(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_s: torch.Tensor,
    x_s: torch.Tensor,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：s: torch.Tensor,
    s: torch.Tensor,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：t: torch.Tensor,
    t: torch.Tensor,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x0_s: torch.Tensor,
    x0_s: torch.Tensor,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[torch.Tensor, torch.Tensor]:
) -> Tuple[torch.Tensor, torch.Tensor]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Perform a regularized Euler step based on x0 prediction.

    Args:
        x_s: Current state tensor.
        s: Current time tensor.
        t: Target time tensor.
        x0_s: Prediction at current time.

    Returns:
        Tuple[Tensor, Tensor]: Updated state tensor and current prediction.
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：coef_x0 = (s - t) / s
    coef_x0 = (s - t) / s
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：coef_xs = t / s
    coef_xs = t / s
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return batch_mul(coef_x0, x0_s) + batch_mul(coef_xs, x_s), x0_s
    return batch_mul(coef_x0, x0_s) + batch_mul(coef_xs, x_s), x0_s


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def reg_eps_euler_step(
def reg_eps_euler_step(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_s: torch.Tensor, s: torch.Tensor, t: torch.Tensor, eps_s: torch.Tensor
    x_s: torch.Tensor, s: torch.Tensor, t: torch.Tensor, eps_s: torch.Tensor
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[torch.Tensor, torch.Tensor]:
) -> Tuple[torch.Tensor, torch.Tensor]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Perform a regularized Euler step based on epsilon prediction.

    Args:
        x_s: Current state tensor.
        s: Current time tensor.
        t: Target time tensor.
        eps_s: Epsilon prediction at current time.

    Returns:
        Tuple[Tensor, Tensor]: Updated state tensor and current x0 prediction.
    """
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return x_s + batch_mul(eps_s, t - s), x_s + batch_mul(eps_s, 0 - s)
    return x_s + batch_mul(eps_s, t - s), x_s + batch_mul(eps_s, 0 - s)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def rk1_euler(
def rk1_euler(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_s: torch.Tensor, s: torch.Tensor, t: torch.Tensor, x0_fn: Callable
    x_s: torch.Tensor, s: torch.Tensor, t: torch.Tensor, x0_fn: Callable
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[torch.Tensor, torch.Tensor]:
) -> Tuple[torch.Tensor, torch.Tensor]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Perform a first-order Runge-Kutta (Euler) step.

    Recommended for diffusion models with guidance or model undertrained
    Usually more stable at the cost of a bit slower convergence.

    Args:
        x_s: Current state tensor.
        s: Current time tensor.
        t: Target time tensor.
        x0_fn: Function to compute x0 prediction.

    Returns:
        Tuple[Tensor, Tensor]: Updated state tensor and x0 prediction.
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x0_s = x0_fn(x_s, s)
    x0_s = x0_fn(x_s, s)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return reg_x0_euler_step(x_s, s, t, x0_s)
    return reg_x0_euler_step(x_s, s, t, x0_s)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def rk2_mid_stable(
def rk2_mid_stable(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_s: torch.Tensor, s: torch.Tensor, t: torch.Tensor, x0_fn: Callable
    x_s: torch.Tensor, s: torch.Tensor, t: torch.Tensor, x0_fn: Callable
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[torch.Tensor, torch.Tensor]:
) -> Tuple[torch.Tensor, torch.Tensor]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Perform a stable second-order Runge-Kutta (midpoint) step.

    Args:
        x_s: Current state tensor.
        s: Current time tensor.
        t: Target time tensor.
        x0_fn: Function to compute x0 prediction.

    Returns:
        Tuple[Tensor, Tensor]: Updated state tensor and x0 prediction.
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：s1 = torch.sqrt(s * t)
    s1 = torch.sqrt(s * t)
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_s1, _ = rk1_euler(x_s, s, s1, x0_fn)
    x_s1, _ = rk1_euler(x_s, s, s1, x0_fn)

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x0_s1 = x0_fn(x_s1, s1)
    x0_s1 = x0_fn(x_s1, s1)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return reg_x0_euler_step(x_s, s, t, x0_s1)
    return reg_x0_euler_step(x_s, s, t, x0_s1)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def rk2_mid(x_s: torch.Tensor, s: torch.Tensor, t: torch.Tensor, x0_fn: Callable) -> Tuple[to...
def rk2_mid(x_s: torch.Tensor, s: torch.Tensor, t: torch.Tensor, x0_fn: Callable) -> Tuple[torch.Tensor, torch.Tensor]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Perform a second-order Runge-Kutta (midpoint) step.

    Args:
        x_s: Current state tensor.
        s: Current time tensor.
        t: Target time tensor.
        x0_fn: Function to compute x0 prediction.

    Returns:
        Tuple[Tensor, Tensor]: Updated state tensor and x0 prediction.
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：s1 = torch.sqrt(s * t)
    s1 = torch.sqrt(s * t)
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_s1, x0_s = rk1_euler(x_s, s, s1, x0_fn)
    x_s1, x0_s = rk1_euler(x_s, s, s1, x0_fn)

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x0_s1 = x0_fn(x_s1, s1)
    x0_s1 = x0_fn(x_s1, s1)

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return res_x0_rk2_step(x_s, t, s, x0_s, s1, x0_s1), x0_s1
    return res_x0_rk2_step(x_s, t, s, x0_s, s1, x0_s1), x0_s1


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def rk_2heun_naive(
def rk_2heun_naive(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_s: torch.Tensor, s: torch.Tensor, t: torch.Tensor, x0_fn: Callable
    x_s: torch.Tensor, s: torch.Tensor, t: torch.Tensor, x0_fn: Callable
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[torch.Tensor, torch.Tensor]:
) -> Tuple[torch.Tensor, torch.Tensor]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Perform a naive second-order Runge-Kutta (Heun's method) step.
    Impl based on rho-rk-deis solvers, https://github.com/qsh-zh/deis
    Recommended for diffusion models without guidance and relative large NFE

    Args:
        x_s: Current state tensor.
        s: Current time tensor.
        t: Target time tensor.
        x0_fn: Function to compute x0 prediction.

    Returns:
        Tuple[Tensor, Tensor]: Updated state tensor and current state.
    """
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_t, x0_s = rk1_euler(x_s, s, t, x0_fn)
    x_t, x0_s = rk1_euler(x_s, s, t, x0_fn)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：eps_s = batch_mul(1.0 / s, x_t - x0_s)
    eps_s = batch_mul(1.0 / s, x_t - x0_s)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x0_t = x0_fn(x_t, t)
    x0_t = x0_fn(x_t, t)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：eps_t = batch_mul(1.0 / t, x_t - x0_t)
    eps_t = batch_mul(1.0 / t, x_t - x0_t)

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：avg_eps = (eps_s + eps_t) / 2
    avg_eps = (eps_s + eps_t) / 2

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return reg_eps_euler_step(x_s, s, t, avg_eps)
    return reg_eps_euler_step(x_s, s, t, avg_eps)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def rk_2heun_edm(
def rk_2heun_edm(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_s: torch.Tensor, s: torch.Tensor, t: torch.Tensor, x0_fn: Callable
    x_s: torch.Tensor, s: torch.Tensor, t: torch.Tensor, x0_fn: Callable
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[torch.Tensor, torch.Tensor]:
) -> Tuple[torch.Tensor, torch.Tensor]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Perform a naive second-order Runge-Kutta (Heun's method) step.
    Impl based no EDM second order Heun method

    Args:
        x_s: Current state tensor.
        s: Current time tensor.
        t: Target time tensor.
        x0_fn: Function to compute x0 prediction.

    Returns:
        Tuple[Tensor, Tensor]: Updated state tensor and current state.
    """
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_t, x0_s = rk1_euler(x_s, s, t, x0_fn)
    x_t, x0_s = rk1_euler(x_s, s, t, x0_fn)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x0_t = x0_fn(x_t, t)
    x0_t = x0_fn(x_t, t)

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：avg_x0 = (x0_s + x0_t) / 2
    avg_x0 = (x0_s + x0_t) / 2

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return reg_x0_euler_step(x_s, s, t, avg_x0)
    return reg_x0_euler_step(x_s, s, t, avg_x0)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def rk_3kutta_naive(
def rk_3kutta_naive(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_s: torch.Tensor, s: torch.Tensor, t: torch.Tensor, x0_fn: Callable
    x_s: torch.Tensor, s: torch.Tensor, t: torch.Tensor, x0_fn: Callable
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[torch.Tensor, torch.Tensor]:
) -> Tuple[torch.Tensor, torch.Tensor]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Perform a naive third-order Runge-Kutta step.
    Impl based on rho-rk-deis solvers, https://github.com/qsh-zh/deis
    Recommended for diffusion models without guidance and relative large NFE

    Args:
        x_s: Current state tensor.
        s: Current time tensor.
        t: Target time tensor.
        x0_fn: Function to compute x0 prediction.

    Returns:
        Tuple[Tensor, Tensor]: Updated state tensor and current state.
    """
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：c2, c3 = 0.5, 1.0
    c2, c3 = 0.5, 1.0
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：a31, a32 = -1.0, 2.0
    a31, a32 = -1.0, 2.0
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：b1, b2, b3 = 1.0 / 6, 4.0 / 6, 1.0 / 6
    b1, b2, b3 = 1.0 / 6, 4.0 / 6, 1.0 / 6

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：delta = t - s
    delta = t - s

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：s1 = c2 * delta + s
    s1 = c2 * delta + s
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：s2 = c3 * delta + s
    s2 = c3 * delta + s
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_s1, x0_s = rk1_euler(x_s, s, s1, x0_fn)
    x_s1, x0_s = rk1_euler(x_s, s, s1, x0_fn)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：eps_s = batch_mul(1.0 / s, x_s - x0_s)
    eps_s = batch_mul(1.0 / s, x_s - x0_s)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x0_s1 = x0_fn(x_s1, s1)
    x0_s1 = x0_fn(x_s1, s1)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：eps_s1 = batch_mul(1.0 / s1, x_s1 - x0_s1)
    eps_s1 = batch_mul(1.0 / s1, x_s1 - x0_s1)

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_eps = a31 * eps_s + a32 * eps_s1
    _eps = a31 * eps_s + a32 * eps_s1
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_s2, _ = reg_eps_euler_step(x_s, s, s2, _eps)
    x_s2, _ = reg_eps_euler_step(x_s, s, s2, _eps)

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x0_s2 = x0_fn(x_s2, s2)
    x0_s2 = x0_fn(x_s2, s2)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：eps_s2 = batch_mul(1.0 / s2, x_s2 - x0_s2)
    eps_s2 = batch_mul(1.0 / s2, x_s2 - x0_s2)

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：avg_eps = b1 * eps_s + b2 * eps_s1 + b3 * eps_s2
    avg_eps = b1 * eps_s + b2 * eps_s1 + b3 * eps_s2
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return reg_eps_euler_step(x_s, s, t, avg_eps)
    return reg_eps_euler_step(x_s, s, t, avg_eps)


# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# key : order + name
# key : order + name
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：RK_FNs = {
RK_FNs = {
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："1euler": rk1_euler,
    "1euler": rk1_euler,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："2mid": rk2_mid,
    "2mid": rk2_mid,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："2mid_stable": rk2_mid_stable,
    "2mid_stable": rk2_mid_stable,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："2heun_edm": rk_2heun_edm,
    "2heun_edm": rk_2heun_edm,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："2heun_naive": rk_2heun_naive,
    "2heun_naive": rk_2heun_naive,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："3kutta_naive": rk_3kutta_naive,
    "3kutta_naive": rk_3kutta_naive,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
}


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_runge_kutta_fn(name: str) -> Callable:
def get_runge_kutta_fn(name: str) -> Callable:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Get the specified Runge-Kutta function.

    Args:
        name: Name of the Runge-Kutta method.

    Returns:
        Callable: The specified Runge-Kutta function.

    Raises:
        RuntimeError: If the specified method is not supported.
    """
    # 中文说明：根据条件选择执行分支；代码：if name in RK_FNs:
    if name in RK_FNs:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return RK_FNs[name]
        return RK_FNs[name]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：methods = "\n\t".join(RK_FNs.keys())
    methods = "\n\t".join(RK_FNs.keys())
    # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise RuntimeError(f"Only support the following Runge-Kutta methods:\n\t{methods}")
    raise RuntimeError(f"Only support the following Runge-Kutta methods:\n\t{methods}")


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_runge_kutta_fn_supported(name: str) -> bool:
def is_runge_kutta_fn_supported(name: str) -> bool:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Check if the specified Runge-Kutta function is supported.

    Args:
        name: Name of the Runge-Kutta method.

    Returns:
        bool: True if the method is supported, False otherwise.
    """
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return name in RK_FNs
    return name in RK_FNs
