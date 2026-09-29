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
# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""The loss reduction modes."""
"""The loss reduction modes."""

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from enum import Enum
from enum import Enum

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _mean(recon: torch.Tensor) -> torch.Tensor:
def _mean(recon: torch.Tensor) -> torch.Tensor:
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return torch.mean(recon)
    return torch.mean(recon)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _sum_per_frame(recon: torch.Tensor) -> torch.Tensor:
def _sum_per_frame(recon: torch.Tensor) -> torch.Tensor:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch_size = recon.shape[0] * recon.shape[2] if recon.ndim == 5 else recon.shape[0]
    batch_size = recon.shape[0] * recon.shape[2] if recon.ndim == 5 else recon.shape[0]
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return torch.sum(recon) / batch_size
    return torch.sum(recon) / batch_size


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _sum(recon: torch.Tensor) -> torch.Tensor:
def _sum(recon: torch.Tensor) -> torch.Tensor:
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return torch.sum(recon) / recon.shape[0]
    return torch.sum(recon) / recon.shape[0]


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ReduceMode(Enum):
class ReduceMode(Enum):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：MEAN = "MEAN"
    MEAN = "MEAN"
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：SUM_PER_FRAME = "SUM_PER_FRAME"
    SUM_PER_FRAME = "SUM_PER_FRAME"
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：SUM = "SUM"
    SUM = "SUM"

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def function(self):
    def function(self):
        # 中文说明：根据条件选择执行分支；代码：if self == ReduceMode.MEAN:
        if self == ReduceMode.MEAN:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return _mean
            return _mean
        # 中文说明：根据条件选择执行分支；代码：elif self == ReduceMode.SUM_PER_FRAME:
        elif self == ReduceMode.SUM_PER_FRAME:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return _sum_per_frame
            return _sum_per_frame
        # 中文说明：根据条件选择执行分支；代码：elif self == ReduceMode.SUM:
        elif self == ReduceMode.SUM:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return _sum
            return _sum
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError("Invalid ReduceMode")
            raise ValueError("Invalid ReduceMode")
