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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pathlib
# import pathlib
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from functools import lru_cache
from functools import lru_cache
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any, Optional, Tuple
from typing import Any, Optional, Tuple

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.nn.functional as F
import torch.nn.functional as F

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# from filelock import FileLock
# from filelock import FileLock
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch import nn
from torch import nn

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import distributed, log
from imaginaire.utils import distributed, log
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io import easy_io
from imaginaire.utils.easy_io import easy_io


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def disabled_train(self: Any, mode: bool = True) -> Any:
def disabled_train(self: Any, mode: bool = True) -> Any:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Overwrite model.train with this function to make sure train/eval mode
    """Overwrite model.train with this function to make sure train/eval mode
    does not change anymore."""
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return self
    return self


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def count_params(model: nn.Module, verbose=False) -> int:
def count_params(model: nn.Module, verbose=False) -> int:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    # 中文说明：根据条件选择执行分支；代码：if verbose:
    if verbose:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"{model.__class__.__name__} has {total_params * 1.e-6:.2f} M params.")
        print(f"{model.__class__.__name__} has {total_params * 1.e-6:.2f} M params.")
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return total_params
    return total_params


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def expand_dims_like(x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
def expand_dims_like(x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
    # 中文说明：在条件成立时重复执行循环体；代码：while x.dim() != y.dim():
    while x.dim() != y.dim():
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = x.unsqueeze(-1)
        x = x.unsqueeze(-1)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return x
    return x
