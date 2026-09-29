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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Tuple
from typing import Tuple

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class EDMScaling:
class EDMScaling:
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, sigma_data: float = 0.5):
    def __init__(self, sigma_data: float = 0.5):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.sigma_data = sigma_data
        self.sigma_data = sigma_data

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, sigma: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, to...
    def __call__(self, sigma: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：c_skip = self.sigma_data**2 / (sigma**2 + self.sigma_data**2)
        c_skip = self.sigma_data**2 / (sigma**2 + self.sigma_data**2)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：c_out = sigma * self.sigma_data / (sigma**2 + self.sigma_data**2) ** 0.5
        c_out = sigma * self.sigma_data / (sigma**2 + self.sigma_data**2) ** 0.5
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：c_in = 1 / (sigma**2 + self.sigma_data**2) ** 0.5
        c_in = 1 / (sigma**2 + self.sigma_data**2) ** 0.5
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：c_noise = 0.25 * sigma.log()
        c_noise = 0.25 * sigma.log()
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return c_skip, c_out, c_in, c_noise
        return c_skip, c_out, c_in, c_noise

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def sigma_loss_weights(self, sigma: torch.Tensor) -> torch.Tensor:
    def sigma_loss_weights(self, sigma: torch.Tensor) -> torch.Tensor:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return (sigma**2 + self.sigma_data**2) / (sigma * self.sigma_data) ** 2
        return (sigma**2 + self.sigma_data**2) / (sigma * self.sigma_data) ** 2


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class RectifiedFlowScaling:
class RectifiedFlowScaling:
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, sigma_data: float = 1.0, t_scaling_factor: float = 1.0):
    def __init__(self, sigma_data: float = 1.0, t_scaling_factor: float = 1.0):
        # 中文说明：检查运行时假设是否成立；代码：assert abs(sigma_data - 1.0) < 1e-6, "sigma_data must be 1.0 for RectifiedFlowScaling"
        assert abs(sigma_data - 1.0) < 1e-6, "sigma_data must be 1.0 for RectifiedFlowScaling"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.t_scaling_factor = t_scaling_factor
        self.t_scaling_factor = t_scaling_factor

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, sigma: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, to...
    def __call__(self, sigma: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t = sigma / (sigma + 1)
        t = sigma / (sigma + 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：c_skip = 1.0 - t
        c_skip = 1.0 - t
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：c_out = -t
        c_out = -t
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：c_in = 1.0 - t
        c_in = 1.0 - t
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：c_noise = t * self.t_scaling_factor
        c_noise = t * self.t_scaling_factor
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return c_skip, c_out, c_in, c_noise
        return c_skip, c_out, c_in, c_noise

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def sigma_loss_weights(self, sigma: torch.Tensor) -> torch.Tensor:
    def sigma_loss_weights(self, sigma: torch.Tensor) -> torch.Tensor:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return 1.0 / sigma**2
        return 1.0 / sigma**2
