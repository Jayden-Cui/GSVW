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
Impl of multistep methods to solve the ODE in the diffusion model.
"""

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Callable, List, Tuple
from typing import Callable, List, Tuple

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.functional.runge_kutta import reg_x0_euler_step, res_x0_rk2_step
from videoworld2.functional.runge_kutta import reg_x0_euler_step, res_x0_rk2_step


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def order2_fn(
def order2_fn(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_s: torch.Tensor, s: torch.Tensor, t: torch.Tensor, x0_s: torch.Tensor, x0_preds: torch.Tensor
    x_s: torch.Tensor, s: torch.Tensor, t: torch.Tensor, x0_s: torch.Tensor, x0_preds: torch.Tensor
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[torch.Tensor, List[torch.Tensor]]:
) -> Tuple[torch.Tensor, List[torch.Tensor]]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    impl the second order multistep method in https://arxiv.org/pdf/2308.02157
    Adams Bashforth approach!
    """
    # 中文说明：根据条件选择执行分支；代码：if x0_preds:
    if x0_preds:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x0_s1, s1 = x0_preds[0]
        x0_s1, s1 = x0_preds[0]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_t = res_x0_rk2_step(x_s, t, s, x0_s, s1, x0_s1)
        x_t = res_x0_rk2_step(x_s, t, s, x0_s, s1, x0_s1)
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_t = reg_x0_euler_step(x_s, s, t, x0_s)[0]
        x_t = reg_x0_euler_step(x_s, s, t, x0_s)[0]
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return x_t, [(x0_s, s)]
    return x_t, [(x0_s, s)]


# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# key: method name, value: method function
# key: method name, value: method function
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# key: order + algorithm name
# key: order + algorithm name
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：MULTISTEP_FNs = {
MULTISTEP_FNs = {
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："2ab": order2_fn,
    "2ab": order2_fn,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
}


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_multi_step_fn(name: str) -> Callable:
def get_multi_step_fn(name: str) -> Callable:
    # 中文说明：根据条件选择执行分支；代码：if name in MULTISTEP_FNs:
    if name in MULTISTEP_FNs:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return MULTISTEP_FNs[name]
        return MULTISTEP_FNs[name]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：methods = "\n\t".join(MULTISTEP_FNs.keys())
    methods = "\n\t".join(MULTISTEP_FNs.keys())
    # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise RuntimeError("Only support multistep method\n" + methods)
    raise RuntimeError("Only support multistep method\n" + methods)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_multi_step_fn_supported(name: str) -> bool:
def is_multi_step_fn_supported(name: str) -> bool:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Check if the multistep method is supported.
    """
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return name in MULTISTEP_FNs
    return name in MULTISTEP_FNs
