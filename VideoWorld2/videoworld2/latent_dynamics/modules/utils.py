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
# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Shared utilities for the networks module."""
"""Shared utilities for the networks module."""

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any
from typing import Any

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from einops import pack, rearrange, unpack
from einops import pack, rearrange, unpack


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def time2batch(x: torch.Tensor) -> tuple[torch.Tensor, int]:
def time2batch(x: torch.Tensor) -> tuple[torch.Tensor, int]:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch_size = x.shape[0]
    batch_size = x.shape[0]
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return rearrange(x, "b c t h w -> (b t) c h w"), batch_size
    return rearrange(x, "b c t h w -> (b t) c h w"), batch_size


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def batch2time(x: torch.Tensor, batch_size: int) -> torch.Tensor:
def batch2time(x: torch.Tensor, batch_size: int) -> torch.Tensor:
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return rearrange(x, "(b t) c h w -> b c t h w", b=batch_size)
    return rearrange(x, "(b t) c h w -> b c t h w", b=batch_size)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def space2batch(x: torch.Tensor) -> tuple[torch.Tensor, int]:
def space2batch(x: torch.Tensor) -> tuple[torch.Tensor, int]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：batch_size, height = x.shape[0], x.shape[-2]
    batch_size, height = x.shape[0], x.shape[-2]
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return rearrange(x, "b c t h w -> (b h w) c t"), batch_size, height
    return rearrange(x, "b c t h w -> (b h w) c t"), batch_size, height


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def batch2space(x: torch.Tensor, batch_size: int, height: int) -> torch.Tensor:
def batch2space(x: torch.Tensor, batch_size: int, height: int) -> torch.Tensor:
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return rearrange(x, "(b h w) c t -> b c t h w", b=batch_size, h=height)
    return rearrange(x, "(b h w) c t -> b c t h w", b=batch_size, h=height)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def cast_tuple(t: Any, length: int = 1) -> Any:
def cast_tuple(t: Any, length: int = 1) -> Any:
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return t if isinstance(t, tuple) else ((t,) * length)
    return t if isinstance(t, tuple) else ((t,) * length)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def replication_pad(x):
def replication_pad(x):
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return torch.cat([x[:, :, :1, ...], x], dim=2)
    return torch.cat([x[:, :, :1, ...], x], dim=2)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def divisible_by(num: int, den: int) -> bool:
def divisible_by(num: int, den: int) -> bool:
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return (num % den) == 0
    return (num % den) == 0


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_odd(n: int) -> bool:
def is_odd(n: int) -> bool:
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return not divisible_by(n, 2)
    return not divisible_by(n, 2)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def nonlinearity(x):
def nonlinearity(x):
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return x * torch.sigmoid(x)
    return x * torch.sigmoid(x)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def Normalize(in_channels, num_groups=32):
def Normalize(in_channels, num_groups=32):
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return torch.nn.GroupNorm(num_groups=num_groups, num_channels=in_channels, eps=1e-6, affine=T...
    return torch.nn.GroupNorm(num_groups=num_groups, num_channels=in_channels, eps=1e-6, affine=True)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class CausalNormalize(torch.nn.Module):
class CausalNormalize(torch.nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, in_channels, num_groups=1):
    def __init__(self, in_channels, num_groups=1):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.norm = torch.nn.GroupNorm(
        self.norm = torch.nn.GroupNorm(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=num_groups,
            num_groups=num_groups,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_channels=in_channels,
            num_channels=in_channels,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：eps=1e-6,
            eps=1e-6,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：affine=True,
            affine=True,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_groups = num_groups
        self.num_groups = num_groups

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x):
    def forward(self, x):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# if num_groups !=1, we apply a spatio-temporal groupnorm for backward compatibility purpose.
        # if num_groups !=1, we apply a spatio-temporal groupnorm for backward compatibility purpose.
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# All new models should use num_groups=1, otherwise causality is not guaranteed.
        # All new models should use num_groups=1, otherwise causality is not guaranteed.
        # 中文说明：根据条件选择执行分支；代码：if self.num_groups == 1:
        if self.num_groups == 1:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x, batch_size = time2batch(x)
            x, batch_size = time2batch(x)
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return batch2time(self.norm(x), batch_size)
            return batch2time(self.norm(x), batch_size)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.norm(x)
        return self.norm(x)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def exists(v):
def exists(v):
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return v is not None
    return v is not None


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def default(*args):
def default(*args):
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for arg in args:
    for arg in args:
        # 中文说明：根据条件选择执行分支；代码：if exists(arg):
        if exists(arg):
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return arg
            return arg
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return None
    return None


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def pack_one(t, pattern):
def pack_one(t, pattern):
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return pack([t], pattern)
    return pack([t], pattern)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def unpack_one(t, ps, pattern):
def unpack_one(t, ps, pattern):
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return unpack(t, ps, pattern)[0]
    return unpack(t, ps, pattern)[0]


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def round_ste(z: torch.Tensor) -> torch.Tensor:
def round_ste(z: torch.Tensor) -> torch.Tensor:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Round with straight through gradients."""
    """Round with straight through gradients."""
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：zhat = z.round()
    zhat = z.round()
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return z + (zhat - z).detach()
    return z + (zhat - z).detach()


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def log(t, eps=1e-5):
def log(t, eps=1e-5):
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return t.clamp(min=eps).log()
    return t.clamp(min=eps).log()


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def entropy(prob):
def entropy(prob):
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return (-prob * log(prob)).sum(dim=-1)
    return (-prob * log(prob)).sum(dim=-1)
