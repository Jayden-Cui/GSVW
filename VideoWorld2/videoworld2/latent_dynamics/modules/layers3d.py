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
# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""The model definition for 3D layers
"""The model definition for 3D layers

Adapted from: https://github.com/lucidrains/magvit2-pytorch/blob/
9f49074179c912736e617d61b32be367eb5f993a/magvit2_pytorch/magvit2_pytorch.py#L889

[MIT License Copyright (c) 2023 Phil Wang]
https://github.com/lucidrains/magvit2-pytorch/blob/
9f49074179c912736e617d61b32be367eb5f993a/LICENSE
"""
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import math
import math
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Tuple, Union
from typing import Tuple, Union

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.nn as nn
import torch.nn as nn
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.nn.functional as F
import torch.nn.functional as F
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from loguru import logger as logging
from loguru import logger as logging
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.latent_dynamics.modules.qformer_ldm import QFormerMF, QFormerMFSep, QFormerM...
from videoworld2.latent_dynamics.modules.qformer_ldm import QFormerMF, QFormerMFSep, QFormerMFSingleQ, PositionEmbeddingRandom, QFormerMFAdjacent, QFormerAdjacentFSingleQ
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.latent_dynamics.modules.patching import Patcher, Patcher3D, UnPatcher, UnPat...
from videoworld2.latent_dynamics.modules.patching import Patcher, Patcher3D, UnPatcher, UnPatcher3D
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.latent_dynamics.modules.utils import (
from videoworld2.latent_dynamics.modules.utils import (
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalNormalize,
    CausalNormalize,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：batch2space,
    batch2space,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：batch2time,
    batch2time,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cast_tuple,
    cast_tuple,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：is_odd,
    is_odd,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：nonlinearity,
    nonlinearity,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：replication_pad,
    replication_pad,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：space2batch,
    space2batch,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：time2batch,
    time2batch,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_LEGACY_NUM_GROUPS = 32
_LEGACY_NUM_GROUPS = 32

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：qformer_map = {
qformer_map = {
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：'QFormerMFSep': QFormerMFSep,
    'QFormerMFSep': QFormerMFSep,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：'QFormerMF': QFormerMF,
    'QFormerMF': QFormerMF,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：'QFormerMFSingleQ': QFormerMFSingleQ,
    'QFormerMFSingleQ': QFormerMFSingleQ,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：'QFormerMFAdjacent': QFormerMFAdjacent,
    'QFormerMFAdjacent': QFormerMFAdjacent,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：'QFormerAdjacentFSingleQ': QFormerAdjacentFSingleQ,
    'QFormerAdjacentFSingleQ': QFormerAdjacentFSingleQ,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
}

# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class CausalConv3d(nn.Module):
class CausalConv3d(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：chan_in: int = 1,
        chan_in: int = 1,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：chan_out: int = 1,
        chan_out: int = 1,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：kernel_size: Union[int, Tuple[int, int, int]] = 3,
        kernel_size: Union[int, Tuple[int, int, int]] = 3,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pad_mode: str = "constant",
        pad_mode: str = "constant",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**kwargs,
        **kwargs,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kernel_size = cast_tuple(kernel_size, 3)
        kernel_size = cast_tuple(kernel_size, 3)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：time_kernel_size, height_kernel_size, width_kernel_size = kernel_size
        time_kernel_size, height_kernel_size, width_kernel_size = kernel_size

        # 中文说明：检查运行时假设是否成立；代码：assert is_odd(height_kernel_size) and is_odd(width_kernel_size)
        assert is_odd(height_kernel_size) and is_odd(width_kernel_size)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dilation = kwargs.pop("dilation", 1)
        dilation = kwargs.pop("dilation", 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stride = kwargs.pop("stride", 1)
        stride = kwargs.pop("stride", 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：time_stride = kwargs.pop("time_stride", 1)
        time_stride = kwargs.pop("time_stride", 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：time_dilation = kwargs.pop("time_dilation", 1)
        time_dilation = kwargs.pop("time_dilation", 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding = kwargs.pop("padding", 1)
        padding = kwargs.pop("padding", 1)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.pad_mode = pad_mode
        self.pad_mode = pad_mode
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：time_pad = time_dilation * (time_kernel_size - 1) + (1 - time_stride)
        time_pad = time_dilation * (time_kernel_size - 1) + (1 - time_stride)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.time_pad = time_pad
        self.time_pad = time_pad

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.spatial_pad = (padding, padding, padding, padding)
        self.spatial_pad = (padding, padding, padding, padding)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stride = (time_stride, stride, stride)
        stride = (time_stride, stride, stride)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dilation = (time_dilation, dilation, dilation)
        dilation = (time_dilation, dilation, dilation)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv3d = nn.Conv3d(
        self.conv3d = nn.Conv3d(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：chan_in,
            chan_in,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：chan_out,
            chan_out,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：kernel_size,
            kernel_size,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stride=stride,
            stride=stride,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dilation=dilation,
            dilation=dilation,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**kwargs,
            **kwargs,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _replication_pad(self, x: torch.Tensor) -> torch.Tensor:
    def _replication_pad(self, x: torch.Tensor) -> torch.Tensor:
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_prev = x[:, :, :1, ...].repeat(1, 1, self.time_pad, 1, 1)
            x_prev = x[:, :, :1, ...].repeat(1, 1, self.time_pad, 1, 1)
        # 中文说明：处理异常、清理资源或管理上下文；代码：except:
        except:
            # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import pdb;pdb.set_trace()
            import pdb;pdb.set_trace()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = torch.cat([x_prev, x], dim=2)
        x = torch.cat([x_prev, x], dim=2)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding = self.spatial_pad + (0, 0)
        padding = self.spatial_pad + (0, 0)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return F.pad(x, padding, mode=self.pad_mode, value=0.0)
        return F.pad(x, padding, mode=self.pad_mode, value=0.0)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x: torch.Tensor) -> torch.Tensor:
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self._replication_pad(x)
        x = self._replication_pad(x)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.conv3d(x)
        return self.conv3d(x)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class CausalUpsample3d(nn.Module):
class CausalUpsample3d(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, in_channels: int) -> None:
    def __init__(self, in_channels: int) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv = CausalConv3d(in_channels, in_channels, kernel_size=3, stride=1, padding=1)
        self.conv = CausalConv3d(in_channels, in_channels, kernel_size=3, stride=1, padding=1)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x: torch.Tensor) -> torch.Tensor:
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = x.repeat_interleave(2, dim=3).repeat_interleave(2, dim=4)
        x = x.repeat_interleave(2, dim=3).repeat_interleave(2, dim=4)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：time_factor = 1.0 + 1.0 * (x.shape[2] > 1)
        time_factor = 1.0 + 1.0 * (x.shape[2] > 1)
        # 中文说明：根据条件选择执行分支；代码：if isinstance(time_factor, torch.Tensor):
        if isinstance(time_factor, torch.Tensor):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：time_factor = time_factor.item()
            time_factor = time_factor.item()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = x.repeat_interleave(int(time_factor), dim=2)
        x = x.repeat_interleave(int(time_factor), dim=2)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.conv(x)
        x = self.conv(x)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x[..., int(time_factor - 1) :, :, :]
        return x[..., int(time_factor - 1) :, :, :]


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class CausalDownsample3d(nn.Module):
class CausalDownsample3d(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, in_channels: int) -> None:
    def __init__(self, in_channels: int) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv = CausalConv3d(
        self.conv = CausalConv3d(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：in_channels,
            in_channels,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：in_channels,
            in_channels,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kernel_size=3,
            kernel_size=3,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stride=2,
            stride=2,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：time_stride=2,
            time_stride=2,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding=0,
            padding=0,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x: torch.Tensor) -> torch.Tensor:
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pad = (0, 1, 0, 1, 0, 0)
        pad = (0, 1, 0, 1, 0, 0)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = F.pad(x, pad, mode="constant", value=0)
        x = F.pad(x, pad, mode="constant", value=0)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = replication_pad(x)
        x = replication_pad(x)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.conv(x)
        x = self.conv(x)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x
        return x


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class CausalHybridUpsample3d(nn.Module):
class CausalHybridUpsample3d(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：in_channels: int,
        in_channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：spatial_up: bool = True,
        spatial_up: bool = True,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：temporal_up: bool = True,
        temporal_up: bool = True,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**kwargs,
        **kwargs,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv1 = (
        self.conv1 = (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(in_channels, in_channels, kernel_size=(3, 1, 1), stride=1, time_stride=1, paddin...
            CausalConv3d(in_channels, in_channels, kernel_size=(3, 1, 1), stride=1, time_stride=1, padding=0)
            # 中文说明：根据条件选择执行分支；代码：if temporal_up
            if temporal_up
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：else nn.Identity()
            else nn.Identity()
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv2 = (
        self.conv2 = (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(in_channels, in_channels, kernel_size=(1, 3, 3), stride=1, time_stride=1, paddin...
            CausalConv3d(in_channels, in_channels, kernel_size=(1, 3, 3), stride=1, time_stride=1, padding=1)
            # 中文说明：根据条件选择执行分支；代码：if spatial_up
            if spatial_up
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：else nn.Identity()
            else nn.Identity()
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv3 = (
        self.conv3 = (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(in_channels, in_channels, kernel_size=1, stride=1, time_stride=1, padding=0)
            CausalConv3d(in_channels, in_channels, kernel_size=1, stride=1, time_stride=1, padding=0)
            # 中文说明：根据条件选择执行分支；代码：if spatial_up or temporal_up
            if spatial_up or temporal_up
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：else nn.Identity()
            else nn.Identity()
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.spatial_up = spatial_up
        self.spatial_up = spatial_up
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.temporal_up = temporal_up
        self.temporal_up = temporal_up

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x: torch.Tensor) -> torch.Tensor:
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # 中文说明：根据条件选择执行分支；代码：if not self.spatial_up and not self.temporal_up:
        if not self.spatial_up and not self.temporal_up:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return x
            return x

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# hybrid upsample temporally.
        # hybrid upsample temporally.
        # 中文说明：根据条件选择执行分支；代码：if self.temporal_up:
        if self.temporal_up:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：time_factor = 1.0 + 1.0 * (x.shape[2] > 1)
            time_factor = 1.0 + 1.0 * (x.shape[2] > 1)
            # 中文说明：根据条件选择执行分支；代码：if isinstance(time_factor, torch.Tensor):
            if isinstance(time_factor, torch.Tensor):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：time_factor = time_factor.item()
                time_factor = time_factor.item()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = x.repeat_interleave(int(time_factor), dim=2)
            x = x.repeat_interleave(int(time_factor), dim=2)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = x[..., int(time_factor - 1) :, :, :]
            x = x[..., int(time_factor - 1) :, :, :]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.conv1(x) + x
            x = self.conv1(x) + x

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# hybrid upsample spatially.
        # hybrid upsample spatially.
        # 中文说明：根据条件选择执行分支；代码：if self.spatial_up:
        if self.spatial_up:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = x.repeat_interleave(2, dim=3).repeat_interleave(2, dim=4)
            x = x.repeat_interleave(2, dim=3).repeat_interleave(2, dim=4)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.conv2(x) + x
            x = self.conv2(x) + x

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# final 1x1x1 conv.
        # final 1x1x1 conv.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.conv3(x)
        x = self.conv3(x)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x
        return x


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class CausalHybridDownsample3d(nn.Module):
class CausalHybridDownsample3d(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：in_channels: int,
        in_channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：spatial_down: bool = True,
        spatial_down: bool = True,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：temporal_down: bool = True,
        temporal_down: bool = True,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**kwargs,
        **kwargs,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv1 = (
        self.conv1 = (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(in_channels, in_channels, kernel_size=(1, 3, 3), stride=2, time_stride=1, paddin...
            CausalConv3d(in_channels, in_channels, kernel_size=(1, 3, 3), stride=2, time_stride=1, padding=0)
            # 中文说明：根据条件选择执行分支；代码：if spatial_down
            if spatial_down
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：else nn.Identity()
            else nn.Identity()
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv2 = (
        self.conv2 = (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(in_channels, in_channels, kernel_size=(3, 1, 1), stride=1, time_stride=2, paddin...
            CausalConv3d(in_channels, in_channels, kernel_size=(3, 1, 1), stride=1, time_stride=2, padding=0)
            # 中文说明：根据条件选择执行分支；代码：if temporal_down
            if temporal_down
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：else nn.Identity()
            else nn.Identity()
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv3 = (
        self.conv3 = (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(in_channels, in_channels, kernel_size=1, stride=1, time_stride=1, padding=0)
            CausalConv3d(in_channels, in_channels, kernel_size=1, stride=1, time_stride=1, padding=0)
            # 中文说明：根据条件选择执行分支；代码：if spatial_down or temporal_down
            if spatial_down or temporal_down
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：else nn.Identity()
            else nn.Identity()
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.spatial_down = spatial_down
        self.spatial_down = spatial_down
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.temporal_down = temporal_down
        self.temporal_down = temporal_down

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x: torch.Tensor) -> torch.Tensor:
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # 中文说明：根据条件选择执行分支；代码：if not self.spatial_down and not self.temporal_down:
        if not self.spatial_down and not self.temporal_down:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return x
            return x

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# hybrid downsample spatially.
        # hybrid downsample spatially.
        # 中文说明：根据条件选择执行分支；代码：if self.spatial_down:
        if self.spatial_down:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pad = (0, 1, 0, 1, 0, 0)
            pad = (0, 1, 0, 1, 0, 0)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = F.pad(x, pad, mode="constant", value=0)
            x = F.pad(x, pad, mode="constant", value=0)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x1 = self.conv1(x)
            x1 = self.conv1(x)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x2 = F.avg_pool3d(x, kernel_size=(1, 2, 2), stride=(1, 2, 2))
            x2 = F.avg_pool3d(x, kernel_size=(1, 2, 2), stride=(1, 2, 2))
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = x1 + x2
            x = x1 + x2

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# hybrid downsample temporally.
        # hybrid downsample temporally.
        # 中文说明：根据条件选择执行分支；代码：if self.temporal_down:
        if self.temporal_down:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = replication_pad(x)
            x = replication_pad(x)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x1 = self.conv2(x)
            x1 = self.conv2(x)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x2 = F.avg_pool3d(x, kernel_size=(2, 1, 1), stride=(2, 1, 1))
            x2 = F.avg_pool3d(x, kernel_size=(2, 1, 1), stride=(2, 1, 1))
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = x1 + x2
            x = x1 + x2

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# final 1x1x1 conv.
        # final 1x1x1 conv.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.conv3(x)
        x = self.conv3(x)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x
        return x


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class CausalResnetBlock3d(nn.Module):
class CausalResnetBlock3d(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：*,
        *,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：in_channels: int,
        in_channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out_channels: int = None,
        out_channels: int = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dropout: float,
        dropout: float,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_groups: int,
        num_groups: int,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.in_channels = in_channels
        self.in_channels = in_channels
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels = in_channels if out_channels is None else out_channels
        out_channels = in_channels if out_channels is None else out_channels

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.norm1 = CausalNormalize(in_channels, num_groups=num_groups)
        self.norm1 = CausalNormalize(in_channels, num_groups=num_groups)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv1 = CausalConv3d(in_channels, out_channels, kernel_size=3, stride=1, padding=1)
        self.conv1 = CausalConv3d(in_channels, out_channels, kernel_size=3, stride=1, padding=1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.norm2 = CausalNormalize(out_channels, num_groups=num_groups)
        self.norm2 = CausalNormalize(out_channels, num_groups=num_groups)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dropout = torch.nn.Dropout(dropout)
        self.dropout = torch.nn.Dropout(dropout)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv2 = CausalConv3d(out_channels, out_channels, kernel_size=3, stride=1, padding=1)
        self.conv2 = CausalConv3d(out_channels, out_channels, kernel_size=3, stride=1, padding=1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.nin_shortcut = (
        self.nin_shortcut = (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(in_channels, out_channels, kernel_size=1, stride=1, padding=0)
            CausalConv3d(in_channels, out_channels, kernel_size=1, stride=1, padding=0)
            # 中文说明：根据条件选择执行分支；代码：if in_channels != out_channels
            if in_channels != out_channels
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：else nn.Identity()
            else nn.Identity()
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x: torch.Tensor) -> torch.Tensor:
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = x
        h = x
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.norm1(h)
        h = self.norm1(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = nonlinearity(h)
        h = nonlinearity(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.conv1(h)
        h = self.conv1(h)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.norm2(h)
        h = self.norm2(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = nonlinearity(h)
        h = nonlinearity(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.dropout(h)
        h = self.dropout(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.conv2(h)
        h = self.conv2(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.nin_shortcut(x)
        x = self.nin_shortcut(x)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x + h
        return x + h


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class CausalResnetBlockFactorized3d(nn.Module):
class CausalResnetBlockFactorized3d(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：*,
        *,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：in_channels: int,
        in_channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out_channels: int = None,
        out_channels: int = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dropout: float,
        dropout: float,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_groups: int,
        num_groups: int,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.in_channels = in_channels
        self.in_channels = in_channels
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels = in_channels if out_channels is None else out_channels
        out_channels = in_channels if out_channels is None else out_channels

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.norm1 = CausalNormalize(in_channels, num_groups=1)
        self.norm1 = CausalNormalize(in_channels, num_groups=1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv1 = nn.Sequential(
        self.conv1 = nn.Sequential(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(
            CausalConv3d(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：in_channels,
                in_channels,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out_channels,
                out_channels,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kernel_size=(1, 3, 3),
                kernel_size=(1, 3, 3),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stride=1,
                stride=1,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding=1,
                padding=1,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(
            CausalConv3d(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out_channels,
                out_channels,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out_channels,
                out_channels,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kernel_size=(3, 1, 1),
                kernel_size=(3, 1, 1),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stride=1,
                stride=1,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding=0,
                padding=0,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.norm2 = CausalNormalize(out_channels, num_groups=num_groups)
        self.norm2 = CausalNormalize(out_channels, num_groups=num_groups)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dropout = torch.nn.Dropout(dropout)
        self.dropout = torch.nn.Dropout(dropout)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv2 = nn.Sequential(
        self.conv2 = nn.Sequential(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(
            CausalConv3d(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out_channels,
                out_channels,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out_channels,
                out_channels,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kernel_size=(1, 3, 3),
                kernel_size=(1, 3, 3),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stride=1,
                stride=1,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding=1,
                padding=1,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(
            CausalConv3d(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out_channels,
                out_channels,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out_channels,
                out_channels,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kernel_size=(3, 1, 1),
                kernel_size=(3, 1, 1),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stride=1,
                stride=1,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding=0,
                padding=0,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.nin_shortcut = (
        self.nin_shortcut = (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(in_channels, out_channels, kernel_size=1, stride=1, padding=0)
            CausalConv3d(in_channels, out_channels, kernel_size=1, stride=1, padding=0)
            # 中文说明：根据条件选择执行分支；代码：if in_channels != out_channels
            if in_channels != out_channels
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：else nn.Identity()
            else nn.Identity()
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x: torch.Tensor) -> torch.Tensor:
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = x
        h = x
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.norm1(h)
        h = self.norm1(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = nonlinearity(h)
        h = nonlinearity(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.conv1(h)
        h = self.conv1(h)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.norm2(h)
        h = self.norm2(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = nonlinearity(h)
        h = nonlinearity(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.dropout(h)
        h = self.dropout(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.conv2(h)
        h = self.conv2(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.nin_shortcut(x)
        x = self.nin_shortcut(x)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x + h
        return x + h

# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class CausalCrossAttention(nn.Module):
class CausalCrossAttention(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, in_channels: int, context_dim: int, num_groups: int) -> None:
    def __init__(self, in_channels: int, context_dim: int, num_groups: int) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.norm = CausalNormalize(in_channels, num_groups=num_groups)
        self.norm = CausalNormalize(in_channels, num_groups=num_groups)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.q_proj = CausalConv3d(in_channels, in_channels, kernel_size=1, stride=1, padding=0)
        self.q_proj = CausalConv3d(in_channels, in_channels, kernel_size=1, stride=1, padding=0)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.kv_proj = nn.Linear(context_dim, in_channels * 2)
        self.kv_proj = nn.Linear(context_dim, in_channels * 2)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.proj_out = CausalConv3d(in_channels, in_channels, kernel_size=1, stride=1, padding=0)
        self.proj_out = CausalConv3d(in_channels, in_channels, kernel_size=1, stride=1, padding=0)
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x: torch.Tensor, context: torch.Tensor) -> torch.Tensor:
    def forward(self, x: torch.Tensor, context: torch.Tensor) -> torch.Tensor:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# x: (B, C, T, H, W)
        # x: (B, C, T, H, W)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# context: (B, T_context, D_context) where T_context = n * T
        # context: (B, T_context, D_context) where T_context = n * T
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h_ = x
        h_ = x
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h_ = self.norm(h_)
        h_ = self.norm(h_)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q = self.q_proj(h_) # (B, C, T, H, W)
        q = self.q_proj(h_)  # (B, C, T, H, W)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Get x's T dimension
        # Get x's T dimension
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_T = x.shape[2]
        x_T = x.shape[2]
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Get context's T dimension
        # Get context's T dimension
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：context_T = context.shape[1]
        context_T = context.shape[1]
        
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Ensure context_T is integer multiple of x_T
        # Ensure context_T is integer multiple of x_T
        # 中文说明：检查运行时假设是否成立；代码：assert context_T % x_T == 0, f"context_T ({context_T}) must be integer multiple of x_T ({x_T})"
        assert context_T % x_T == 0, f"context_T ({context_T}) must be integer multiple of x_T ({x_T})"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n = context_T // x_T
        n = context_T // x_T

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Get K, V from context
        # Get K, V from context
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kv = self.kv_proj(context) # (B, T_context, C * 2)
        kv = self.kv_proj(context)  # (B, T_context, C * 2)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k, v = torch.chunk(kv, 2, dim=-1) # k, v: (B, T_context, C)
        k, v = torch.chunk(kv, 2, dim=-1)  # k, v: (B, T_context, C)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Reshape Q for attention
        # Reshape Q for attention
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q, batch_size, height = space2batch(q) # q: (B*H*W, C, T)
        q, batch_size, height = space2batch(q)  # q: (B*H*W, C, T)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：bhw, c, t = q.shape
        bhw, c, t = q.shape
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q = q.permute(0, 2, 1) # q: (B*H*W, T, C)
        q = q.permute(0, 2, 1)  # q: (B*H*W, T, C)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Reshape K, V to match Q
        # Reshape K, V to match Q
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h_w = bhw // batch_size
        h_w = bhw // batch_size
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# For each spatial location, expand k and v
        # For each spatial location, expand k and v
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：k = k.unsqueeze(1).expand(-1, h_w, -1, -1).reshape(bhw, context_T, c) # (bhw, T_context, C)
        k = k.unsqueeze(1).expand(-1, h_w, -1, -1).reshape(bhw, context_T, c)  # (bhw, T_context, C)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：v = v.unsqueeze(1).expand(-1, h_w, -1, -1).reshape(bhw, context_T, c) # (bhw, T_context, C)
        v = v.unsqueeze(1).expand(-1, h_w, -1, -1).reshape(bhw, context_T, c)  # (bhw, T_context, C)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Compute attention with specific interaction pattern
        # Compute attention with specific interaction pattern
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Create mask to enforce first q interacts with first n contexts, second q interacts with fir...
        # Create mask to enforce first q interacts with first n contexts, second q interacts with first 2n contexts, etc.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mask = torch.zeros((bhw, t, context_T), device=q.device)
        mask = torch.zeros((bhw, t, context_T), device=q.device)
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i in range(t):
        for i in range(t):
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# For each query position i, allow attention to first (i+1)*n context positions
            # For each query position i, allow attention to first (i+1)*n context positions
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mask[:, i, :min((i+1)*n, context_T)] = 1.0
            mask[:, i, :min((i+1)*n, context_T)] = 1.0
        
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Compute attention scores
        # Compute attention scores
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：w_ = torch.bmm(q, k.permute(0, 2, 1)) # (bhw, T, T_context)
        w_ = torch.bmm(q, k.permute(0, 2, 1))  # (bhw, T, T_context)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：w_ = w_ * (int(c) ** (-0.5))
        w_ = w_ * (int(c) ** (-0.5))

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Apply mask to restrict attention
        # Apply mask to restrict attention
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：w_ = w_.masked_fill(mask == 0, float("-inf"))
        w_ = w_.masked_fill(mask == 0, float("-inf"))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：w_ = F.softmax(w_, dim=2)
        w_ = F.softmax(w_, dim=2)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Attend to values
        # Attend to values
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h_ = torch.bmm(w_, v) # (bhw, T, C)
        h_ = torch.bmm(w_, v)  # (bhw, T, C)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h_ = h_.permute(0, 2, 1).reshape(bhw, c, t) # (bhw, C, T)
        h_ = h_.permute(0, 2, 1).reshape(bhw, c, t)  # (bhw, C, T)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h_ = batch2space(h_, batch_size, height)
        h_ = batch2space(h_, batch_size, height)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h_ = self.proj_out(h_)
        h_ = self.proj_out(h_)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x + h_
        return x + h_


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class CausalAttnBlock(nn.Module):
class CausalAttnBlock(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, in_channels: int, num_groups: int) -> None:
    def __init__(self, in_channels: int, num_groups: int) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.norm = CausalNormalize(in_channels, num_groups=num_groups)
        self.norm = CausalNormalize(in_channels, num_groups=num_groups)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.q = CausalConv3d(in_channels, in_channels, kernel_size=1, stride=1, padding=0)
        self.q = CausalConv3d(in_channels, in_channels, kernel_size=1, stride=1, padding=0)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.k = CausalConv3d(in_channels, in_channels, kernel_size=1, stride=1, padding=0)
        self.k = CausalConv3d(in_channels, in_channels, kernel_size=1, stride=1, padding=0)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.v = CausalConv3d(in_channels, in_channels, kernel_size=1, stride=1, padding=0)
        self.v = CausalConv3d(in_channels, in_channels, kernel_size=1, stride=1, padding=0)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.proj_out = CausalConv3d(in_channels, in_channels, kernel_size=1, stride=1, padding=0)
        self.proj_out = CausalConv3d(in_channels, in_channels, kernel_size=1, stride=1, padding=0)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x: torch.Tensor, z=None) -> torch.Tensor:
    def forward(self, x: torch.Tensor, z=None) -> torch.Tensor:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h_ = x #1, C, T, H, W
        h_ = x  #1, C, T, H, W
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h_ = self.norm(h_)
        h_ = self.norm(h_)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q = self.q(h_)
        q = self.q(h_)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：k = self.k(h_) # torch.Size([1, 512, 5, 20, 32])
        k = self.k(h_) # torch.Size([1, 512, 5, 20, 32])
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：v = self.v(h_)
        v = self.v(h_)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# compute attention
        # compute attention
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q, batch_size = time2batch(q) #torch.Size([5, 512, 20, 32])
        q, batch_size = time2batch(q) #torch.Size([5, 512, 20, 32])
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k, batch_size = time2batch(k)
        k, batch_size = time2batch(k)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v, batch_size = time2batch(v)
        v, batch_size = time2batch(v)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：b, c, h, w = q.shape
        b, c, h, w = q.shape
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q = q.reshape(b, c, h * w)
        q = q.reshape(b, c, h * w)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q = q.permute(0, 2, 1)
        q = q.permute(0, 2, 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：k = k.reshape(b, c, h * w)
        k = k.reshape(b, c, h * w)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：w_ = torch.bmm(q, k)
        w_ = torch.bmm(q, k)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：w_ = w_ * (int(c) ** (-0.5))
        w_ = w_ * (int(c) ** (-0.5))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：w_ = F.softmax(w_, dim=2)
        w_ = F.softmax(w_, dim=2)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# attend to values
        # attend to values
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：v = v.reshape(b, c, h * w)
        v = v.reshape(b, c, h * w)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：w_ = w_.permute(0, 2, 1)
        w_ = w_.permute(0, 2, 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h_ = torch.bmm(v, w_)
        h_ = torch.bmm(v, w_)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h_ = h_.reshape(b, c, h, w)
        h_ = h_.reshape(b, c, h, w)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h_ = batch2time(h_, batch_size)
        h_ = batch2time(h_, batch_size)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h_ = self.proj_out(h_)
        h_ = self.proj_out(h_)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x + h_
        return x + h_


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class CausalTemporalAttnBlock(nn.Module):
class CausalTemporalAttnBlock(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, in_channels: int, num_groups: int) -> None:
    def __init__(self, in_channels: int, num_groups: int) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.norm = CausalNormalize(in_channels, num_groups=num_groups)
        self.norm = CausalNormalize(in_channels, num_groups=num_groups)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.q = CausalConv3d(in_channels, in_channels, kernel_size=1, stride=1, padding=0)
        self.q = CausalConv3d(in_channels, in_channels, kernel_size=1, stride=1, padding=0)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.k = CausalConv3d(in_channels, in_channels, kernel_size=1, stride=1, padding=0)
        self.k = CausalConv3d(in_channels, in_channels, kernel_size=1, stride=1, padding=0)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.v = CausalConv3d(in_channels, in_channels, kernel_size=1, stride=1, padding=0)
        self.v = CausalConv3d(in_channels, in_channels, kernel_size=1, stride=1, padding=0)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.proj_out = CausalConv3d(in_channels, in_channels, kernel_size=1, stride=1, padding=0)
        self.proj_out = CausalConv3d(in_channels, in_channels, kernel_size=1, stride=1, padding=0)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x: torch.Tensor, z=None) -> torch.Tensor:
    def forward(self, x: torch.Tensor, z=None) -> torch.Tensor:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h_ = x
        h_ = x
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h_ = self.norm(h_)
        h_ = self.norm(h_)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q = self.q(h_)
        q = self.q(h_)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：k = self.k(h_)
        k = self.k(h_)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：v = self.v(h_)
        v = self.v(h_)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# compute attention
        # compute attention
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q, batch_size, height = space2batch(q)
        q, batch_size, height = space2batch(q)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k, _, _ = space2batch(k)
        k, _, _ = space2batch(k)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v, _, _ = space2batch(v)
        v, _, _ = space2batch(v)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：bhw, c, t = q.shape
        bhw, c, t = q.shape
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q = q.permute(0, 2, 1) # (bhw, t, c)
        q = q.permute(0, 2, 1)  # (bhw, t, c)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：k = k.permute(0, 2, 1) # (bhw, t, c)
        k = k.permute(0, 2, 1)  # (bhw, t, c)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：v = v.permute(0, 2, 1) # (bhw, t, c)
        v = v.permute(0, 2, 1)  # (bhw, t, c)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：w_ = torch.bmm(q, k.permute(0, 2, 1)) # (bhw, t, t)
        w_ = torch.bmm(q, k.permute(0, 2, 1))  # (bhw, t, t)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：w_ = w_ * (int(c) ** (-0.5))
        w_ = w_ * (int(c) ** (-0.5))

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Apply causal mask
        # Apply causal mask
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mask = torch.tril(torch.ones_like(w_))
        mask = torch.tril(torch.ones_like(w_))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：w_ = w_.masked_fill(mask == 0, float("-inf"))
        w_ = w_.masked_fill(mask == 0, float("-inf"))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：w_ = F.softmax(w_, dim=2)
        w_ = F.softmax(w_, dim=2)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# attend to values
        # attend to values
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h_ = torch.bmm(w_, v) # (bhw, t, c)
        h_ = torch.bmm(w_, v)  # (bhw, t, c)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h_ = h_.permute(0, 2, 1).reshape(bhw, c, t) # (bhw, c, t)
        h_ = h_.permute(0, 2, 1).reshape(bhw, c, t)  # (bhw, c, t)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h_ = batch2space(h_, batch_size, height)
        h_ = batch2space(h_, batch_size, height)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h_ = self.proj_out(h_)
        h_ = self.proj_out(h_)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x + h_
        return x + h_


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class EncoderBase(nn.Module):
class EncoderBase(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：in_channels: int,
        in_channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：channels: int,
        channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：channels_mult: list[int],
        channels_mult: list[int],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_res_blocks: int,
        num_res_blocks: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：attn_resolutions: list[int],
        attn_resolutions: list[int],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dropout: float,
        dropout: float,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：resolution: int,
        resolution: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：z_channels: int,
        z_channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**ignore_kwargs,
        **ignore_kwargs,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_resolutions = len(channels_mult)
        self.num_resolutions = len(channels_mult)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_res_blocks = num_res_blocks
        self.num_res_blocks = num_res_blocks

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Patcher.
        # Patcher.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：patch_size = ignore_kwargs.get("patch_size", 1)
        patch_size = ignore_kwargs.get("patch_size", 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.patcher = Patcher(patch_size, ignore_kwargs.get("patch_method", "rearrange"))
        self.patcher = Patcher(patch_size, ignore_kwargs.get("patch_method", "rearrange"))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels = in_channels * patch_size * patch_size
        in_channels = in_channels * patch_size * patch_size

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# downsampling
        # downsampling
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv_in = CausalConv3d(in_channels, channels, kernel_size=3, stride=1, padding=1)
        self.conv_in = CausalConv3d(in_channels, channels, kernel_size=3, stride=1, padding=1)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# num of groups for GroupNorm, num_groups=1 for LayerNorm.
        # num of groups for GroupNorm, num_groups=1 for LayerNorm.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups = ignore_kwargs.get("num_groups", _LEGACY_NUM_GROUPS)
        num_groups = ignore_kwargs.get("num_groups", _LEGACY_NUM_GROUPS)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_res = resolution // patch_size
        curr_res = resolution // patch_size
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_ch_mult = (1,) + tuple(channels_mult)
        in_ch_mult = (1,) + tuple(channels_mult)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.in_ch_mult = in_ch_mult
        self.in_ch_mult = in_ch_mult
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.down = nn.ModuleList()
        self.down = nn.ModuleList()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i_level in range(self.num_resolutions):
        for i_level in range(self.num_resolutions):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block = nn.ModuleList()
            block = nn.ModuleList()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn = nn.ModuleList()
            attn = nn.ModuleList()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_in = channels * in_ch_mult[i_level]
            block_in = channels * in_ch_mult[i_level]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_out = channels * channels_mult[i_level]
            block_out = channels * channels_mult[i_level]
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _ in range(self.num_res_blocks):
            for _ in range(self.num_res_blocks):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：block.append(
                block.append(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalResnetBlock3d(
                    CausalResnetBlock3d(
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=block_in,
                        in_channels=block_in,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=block_out,
                        out_channels=block_out,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=dropout,
                        dropout=dropout,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=num_groups,
                        num_groups=num_groups,
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_in = block_out
                block_in = block_out
                # 中文说明：根据条件选择执行分支；代码：if curr_res in attn_resolutions:
                if curr_res in attn_resolutions:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：attn.append(CausalAttnBlock(block_in, num_groups=num_groups))
                    attn.append(CausalAttnBlock(block_in, num_groups=num_groups))
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：down = nn.Module()
            down = nn.Module()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：down.block = block
            down.block = block
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：down.attn = attn
            down.attn = attn
            # 中文说明：根据条件选择执行分支；代码：if i_level != self.num_resolutions - 1:
            if i_level != self.num_resolutions - 1:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：down.downsample = CausalDownsample3d(block_in)
                down.downsample = CausalDownsample3d(block_in)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_res = curr_res // 2
                curr_res = curr_res // 2
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.down.append(down)
            self.down.append(down)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# middle
        # middle
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid = nn.Module()
        self.mid = nn.Module()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid.block_1 = CausalResnetBlock3d(
        self.mid.block_1 = CausalResnetBlock3d(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=block_in,
            in_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=block_in,
            out_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=dropout,
            dropout=dropout,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=num_groups,
            num_groups=num_groups,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid.attn_1 = CausalAttnBlock(block_in, num_groups=num_groups)
        self.mid.attn_1 = CausalAttnBlock(block_in, num_groups=num_groups)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid.block_2 = CausalResnetBlock3d(
        self.mid.block_2 = CausalResnetBlock3d(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=block_in,
            in_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=block_in,
            out_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=dropout,
            dropout=dropout,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=num_groups,
            num_groups=num_groups,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# end
        # end
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.norm_out = CausalNormalize(block_in, num_groups=num_groups)
        self.norm_out = CausalNormalize(block_in, num_groups=num_groups)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv_out = CausalConv3d(block_in, z_channels, kernel_size=3, stride=1, padding=1)
        self.conv_out = CausalConv3d(block_in, z_channels, kernel_size=3, stride=1, padding=1)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def patcher3d(self, x: torch.Tensor) -> torch.Tensor:
    def patcher3d(self, x: torch.Tensor) -> torch.Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x, batch_size = time2batch(x)
        x, batch_size = time2batch(x)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.patcher(x)
        x = self.patcher(x)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = batch2time(x, batch_size)
        x = batch2time(x, batch_size)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x
        return x

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x: torch.Tensor) -> torch.Tensor:
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.patcher3d(x)
        x = self.patcher3d(x)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# downsampling
        # downsampling
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hs = [self.conv_in(x)]
        hs = [self.conv_in(x)]
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i_level in range(self.num_resolutions):
        for i_level in range(self.num_resolutions):
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i_block in range(self.num_res_blocks):
            for i_block in range(self.num_res_blocks):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.down[i_level].block[i_block](hs[-1])
                h = self.down[i_level].block[i_block](hs[-1])
                # 中文说明：根据条件选择执行分支；代码：if len(self.down[i_level].attn) > 0:
                if len(self.down[i_level].attn) > 0:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.down[i_level].attn[i_block](h)
                    h = self.down[i_level].attn[i_block](h)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：hs.append(h)
                hs.append(h)
            # 中文说明：根据条件选择执行分支；代码：if i_level != self.num_resolutions - 1:
            if i_level != self.num_resolutions - 1:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：hs.append(self.down[i_level].downsample(hs[-1]))
                hs.append(self.down[i_level].downsample(hs[-1]))
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# temporal downsample (last level)
                # temporal downsample (last level)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：time_factor = 1 + 1 * (hs[-1].shape[2] > 1)
                time_factor = 1 + 1 * (hs[-1].shape[2] > 1)
                # 中文说明：根据条件选择执行分支；代码：if isinstance(time_factor, torch.Tensor):
                if isinstance(time_factor, torch.Tensor):
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：time_factor = time_factor.item()
                    time_factor = time_factor.item()
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hs[-1] = replication_pad(hs[-1])
                hs[-1] = replication_pad(hs[-1])
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：hs.append(
                hs.append(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：F.avg_pool3d(
                    F.avg_pool3d(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：hs[-1],
                        hs[-1],
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kernel_size=[time_factor, 1, 1],
                        kernel_size=[time_factor, 1, 1],
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stride=[2, 1, 1],
                        stride=[2, 1, 1],
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# middle
        # middle
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = hs[-1]
        h = hs[-1]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.mid.block_1(h)
        h = self.mid.block_1(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.mid.attn_1(h)
        h = self.mid.attn_1(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.mid.block_2(h)
        h = self.mid.block_2(h)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# end
        # end
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.norm_out(h)
        h = self.norm_out(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = nonlinearity(h)
        h = nonlinearity(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.conv_out(h)
        h = self.conv_out(h)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return h
        return h


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class DecoderBase(nn.Module):
class DecoderBase(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out_channels: int,
        out_channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：channels: int,
        channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：channels_mult: list[int],
        channels_mult: list[int],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_res_blocks: int,
        num_res_blocks: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：attn_resolutions: list[int],
        attn_resolutions: list[int],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dropout: float,
        dropout: float,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：resolution: int,
        resolution: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：z_channels: int,
        z_channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**ignore_kwargs,
        **ignore_kwargs,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_resolutions = len(channels_mult)
        self.num_resolutions = len(channels_mult)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_res_blocks = num_res_blocks
        self.num_res_blocks = num_res_blocks

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# UnPatcher.
        # UnPatcher.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：patch_size = ignore_kwargs.get("patch_size", 1)
        patch_size = ignore_kwargs.get("patch_size", 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.unpatcher = UnPatcher(patch_size, ignore_kwargs.get("patch_method", "rearrange"))
        self.unpatcher = UnPatcher(patch_size, ignore_kwargs.get("patch_method", "rearrange"))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_ch = out_channels * patch_size * patch_size
        out_ch = out_channels * patch_size * patch_size

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_in = channels * channels_mult[self.num_resolutions - 1]
        block_in = channels * channels_mult[self.num_resolutions - 1]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_res = (resolution // patch_size) // 2 ** (self.num_resolutions - 1)
        curr_res = (resolution // patch_size) // 2 ** (self.num_resolutions - 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.z_shape = (1, z_channels, curr_res, curr_res)
        self.z_shape = (1, z_channels, curr_res, curr_res)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：logging.info("Working with z of shape {} = {} dimensions.".format(self.z_shape, np.prod(self....
        logging.info("Working with z of shape {} = {} dimensions.".format(self.z_shape, np.prod(self.z_shape)))

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# z to block_in
        # z to block_in
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv_in = CausalConv3d(z_channels, block_in, kernel_size=3, stride=1, padding=1)
        self.conv_in = CausalConv3d(z_channels, block_in, kernel_size=3, stride=1, padding=1)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# num of groups for GroupNorm, num_groups=1 for LayerNorm.
        # num of groups for GroupNorm, num_groups=1 for LayerNorm.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups = ignore_kwargs.get("num_groups", _LEGACY_NUM_GROUPS)
        num_groups = ignore_kwargs.get("num_groups", _LEGACY_NUM_GROUPS)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# middle
        # middle
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid = nn.Module()
        self.mid = nn.Module()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid.block_1 = CausalResnetBlock3d(
        self.mid.block_1 = CausalResnetBlock3d(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=block_in,
            in_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=block_in,
            out_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=dropout,
            dropout=dropout,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=num_groups,
            num_groups=num_groups,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid.attn_1 = CausalAttnBlock(block_in, num_groups=num_groups)
        self.mid.attn_1 = CausalAttnBlock(block_in, num_groups=num_groups)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid.block_2 = CausalResnetBlock3d(
        self.mid.block_2 = CausalResnetBlock3d(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=block_in,
            in_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=block_in,
            out_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=dropout,
            dropout=dropout,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=num_groups,
            num_groups=num_groups,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# upsampling
        # upsampling
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.up = nn.ModuleList()
        self.up = nn.ModuleList()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i_level in reversed(range(self.num_resolutions)):
        for i_level in reversed(range(self.num_resolutions)):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block = nn.ModuleList()
            block = nn.ModuleList()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn = nn.ModuleList()
            attn = nn.ModuleList()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_out = channels * channels_mult[i_level]
            block_out = channels * channels_mult[i_level]
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _ in range(self.num_res_blocks + 1):
            for _ in range(self.num_res_blocks + 1):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：block.append(
                block.append(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalResnetBlock3d(
                    CausalResnetBlock3d(
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=block_in,
                        in_channels=block_in,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=block_out,
                        out_channels=block_out,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=dropout,
                        dropout=dropout,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=num_groups,
                        num_groups=num_groups,
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_in = block_out
                block_in = block_out
                # 中文说明：根据条件选择执行分支；代码：if curr_res in attn_resolutions:
                if curr_res in attn_resolutions:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：attn.append(CausalAttnBlock(block_in, num_groups=num_groups))
                    attn.append(CausalAttnBlock(block_in, num_groups=num_groups))
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：up = nn.Module()
            up = nn.Module()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：up.block = block
            up.block = block
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：up.attn = attn
            up.attn = attn
            # 中文说明：根据条件选择执行分支；代码：if i_level != 0:
            if i_level != 0:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：up.upsample = CausalUpsample3d(block_in)
                up.upsample = CausalUpsample3d(block_in)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_res = curr_res * 2
                curr_res = curr_res * 2
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.up.insert(0, up) # prepend to get consistent order
            self.up.insert(0, up)  # prepend to get consistent order

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# end
        # end
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.norm_out = CausalNormalize(block_in, num_groups=num_groups)
        self.norm_out = CausalNormalize(block_in, num_groups=num_groups)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv_out = CausalConv3d(block_in, out_ch, kernel_size=3, stride=1, padding=1)
        self.conv_out = CausalConv3d(block_in, out_ch, kernel_size=3, stride=1, padding=1)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def unpatcher3d(self, x: torch.Tensor) -> torch.Tensor:
    def unpatcher3d(self, x: torch.Tensor) -> torch.Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x, batch_size = time2batch(x)
        x, batch_size = time2batch(x)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.unpatcher(x)
        x = self.unpatcher(x)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = batch2time(x, batch_size)
        x = batch2time(x, batch_size)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x
        return x

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, z):
    def forward(self, z):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.conv_in(z)
        h = self.conv_in(z)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# middle block.
        # middle block.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.mid.block_1(h)
        h = self.mid.block_1(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.mid.attn_1(h)
        h = self.mid.attn_1(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.mid.block_2(h)
        h = self.mid.block_2(h)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# decoder blocks.
        # decoder blocks.
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i_level in reversed(range(self.num_resolutions)):
        for i_level in reversed(range(self.num_resolutions)):
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i_block in range(self.num_res_blocks + 1):
            for i_block in range(self.num_res_blocks + 1):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.up[i_level].block[i_block](h)
                h = self.up[i_level].block[i_block](h)
                # 中文说明：根据条件选择执行分支；代码：if len(self.up[i_level].attn) > 0:
                if len(self.up[i_level].attn) > 0:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.up[i_level].attn[i_block](h)
                    h = self.up[i_level].attn[i_block](h)
            # 中文说明：根据条件选择执行分支；代码：if i_level != 0:
            if i_level != 0:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.up[i_level].upsample(h)
                h = self.up[i_level].upsample(h)
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# temporal upsample (last level)
                # temporal upsample (last level)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：time_factor = 1.0 + 1.0 * (h.shape[2] > 1)
                time_factor = 1.0 + 1.0 * (h.shape[2] > 1)
                # 中文说明：根据条件选择执行分支；代码：if isinstance(time_factor, torch.Tensor):
                if isinstance(time_factor, torch.Tensor):
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：time_factor = time_factor.item()
                    time_factor = time_factor.item()
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = h.repeat_interleave(int(time_factor), dim=2)
                h = h.repeat_interleave(int(time_factor), dim=2)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = h[..., int(time_factor - 1) :, :, :]
                h = h[..., int(time_factor - 1) :, :, :]

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.norm_out(h)
        h = self.norm_out(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = nonlinearity(h)
        h = nonlinearity(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.conv_out(h)
        h = self.conv_out(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.unpatcher3d(h)
        h = self.unpatcher3d(h)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return h
        return h


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class EncoderFactorized(nn.Module):
class EncoderFactorized(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：in_channels: int,
        in_channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：channels: int,
        channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：channels_mult: list[int],
        channels_mult: list[int],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_res_blocks: int,
        num_res_blocks: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：attn_resolutions: list[int],
        attn_resolutions: list[int],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dropout: float,
        dropout: float,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：resolution: int,
        resolution: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：z_channels: int,
        z_channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：spatial_compression: int = 16,
        spatial_compression: int = 16,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：temporal_compression: int = 8,
        temporal_compression: int = 8,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**ignore_kwargs,
        **ignore_kwargs,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_resolutions = len(channels_mult)
        self.num_resolutions = len(channels_mult)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_res_blocks = num_res_blocks
        self.num_res_blocks = num_res_blocks
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Patcher.
        # Patcher.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：patch_size = ignore_kwargs.get("patch_size", 1)
        patch_size = ignore_kwargs.get("patch_size", 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.patcher3d = Patcher3D(patch_size, ignore_kwargs.get("patch_method", "rearrange"))
        self.patcher3d = Patcher3D(patch_size, ignore_kwargs.get("patch_method", "rearrange"))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels = in_channels * patch_size * patch_size * patch_size
        in_channels = in_channels * patch_size * patch_size * patch_size

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# calculate the number of downsample operations
        # calculate the number of downsample operations
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_spatial_downs = int(math.log2(spatial_compression)) - int(math.log2(patch_size))
        self.num_spatial_downs = int(math.log2(spatial_compression)) - int(math.log2(patch_size))
        # 中文说明：检查运行时假设是否成立；代码：assert (
        assert (
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.num_spatial_downs <= self.num_resolutions
            self.num_spatial_downs <= self.num_resolutions
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"Spatially downsample {self.num_resolutions} times at most"
        ), f"Spatially downsample {self.num_resolutions} times at most"

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_temporal_downs = int(math.log2(temporal_compression)) - int(math.log2(patch_size))
        self.num_temporal_downs = int(math.log2(temporal_compression)) - int(math.log2(patch_size))
        # 中文说明：检查运行时假设是否成立；代码：assert (
        assert (
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.num_temporal_downs <= self.num_resolutions
            self.num_temporal_downs <= self.num_resolutions
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"Temporally downsample {self.num_resolutions} times at most"
        ), f"Temporally downsample {self.num_resolutions} times at most"

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# downsampling
        # downsampling
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv_in = nn.Sequential(
        self.conv_in = nn.Sequential(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(
            CausalConv3d(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：in_channels,
                in_channels,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：channels,
                channels,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kernel_size=(1, 3, 3),
                kernel_size=(1, 3, 3),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stride=1,
                stride=1,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding=1,
                padding=1,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(channels, channels, kernel_size=(3, 1, 1), stride=1, padding=0),
            CausalConv3d(channels, channels, kernel_size=(3, 1, 1), stride=1, padding=0),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_res = resolution // patch_size
        curr_res = resolution // patch_size
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_ch_mult = (1,) + tuple(channels_mult)
        in_ch_mult = (1,) + tuple(channels_mult)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.in_ch_mult = in_ch_mult
        self.in_ch_mult = in_ch_mult
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.down = nn.ModuleList()
        self.down = nn.ModuleList()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i_level in range(self.num_resolutions):
        for i_level in range(self.num_resolutions):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block = nn.ModuleList()
            block = nn.ModuleList()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn = nn.ModuleList()
            attn = nn.ModuleList()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_in = channels * in_ch_mult[i_level]
            block_in = channels * in_ch_mult[i_level]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_out = channels * channels_mult[i_level]
            block_out = channels * channels_mult[i_level]
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _ in range(self.num_res_blocks):
            for _ in range(self.num_res_blocks):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：block.append(
                block.append(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalResnetBlockFactorized3d(
                    CausalResnetBlockFactorized3d(
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=block_in,
                        in_channels=block_in,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=block_out,
                        out_channels=block_out,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=dropout,
                        dropout=dropout,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=1,
                        num_groups=1,
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_in = block_out
                block_in = block_out
                # 中文说明：根据条件选择执行分支；代码：if curr_res in attn_resolutions:
                if curr_res in attn_resolutions:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：attn.append(
                    attn.append(
                        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.Sequential(
                        nn.Sequential(
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalAttnBlock(block_in, num_groups=1),
                            CausalAttnBlock(block_in, num_groups=1),
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalTemporalAttnBlock(block_in, num_groups=1),
                            CausalTemporalAttnBlock(block_in, num_groups=1),
                        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                        )
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：down = nn.Module()
            down = nn.Module()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：down.block = block
            down.block = block
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：down.attn = attn
            down.attn = attn
            # 中文说明：根据条件选择执行分支；代码：if i_level != self.num_resolutions - 1:
            if i_level != self.num_resolutions - 1:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：spatial_down = i_level < self.num_spatial_downs
                spatial_down = i_level < self.num_spatial_downs
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_down = i_level < self.num_temporal_downs
                temporal_down = i_level < self.num_temporal_downs
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：down.downsample = CausalHybridDownsample3d(
                down.downsample = CausalHybridDownsample3d(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：block_in,
                    block_in,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：spatial_down=spatial_down,
                    spatial_down=spatial_down,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_down=temporal_down,
                    temporal_down=temporal_down,
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_res = curr_res // 2
                curr_res = curr_res // 2
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.down.append(down)
            self.down.append(down)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# middle
        # middle
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid = nn.Module()
        self.mid = nn.Module()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid.block_1 = CausalResnetBlockFactorized3d(
        self.mid.block_1 = CausalResnetBlockFactorized3d(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=block_in,
            in_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=block_in,
            out_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=dropout,
            dropout=dropout,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=1,
            num_groups=1,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid.attn_1 = nn.Sequential(
        self.mid.attn_1 = nn.Sequential(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalAttnBlock(block_in, num_groups=1),
            CausalAttnBlock(block_in, num_groups=1),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalTemporalAttnBlock(block_in, num_groups=1),
            CausalTemporalAttnBlock(block_in, num_groups=1),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid.block_2 = CausalResnetBlockFactorized3d(
        self.mid.block_2 = CausalResnetBlockFactorized3d(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=block_in,
            in_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=block_in,
            out_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=dropout,
            dropout=dropout,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=1,
            num_groups=1,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# end
        # end
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.norm_out = CausalNormalize(block_in, num_groups=1)
        self.norm_out = CausalNormalize(block_in, num_groups=1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv_out = nn.Sequential(
        self.conv_out = nn.Sequential(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(block_in, z_channels, kernel_size=(1, 3, 3), stride=1, padding=1),
            CausalConv3d(block_in, z_channels, kernel_size=(1, 3, 3), stride=1, padding=1),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(
            CausalConv3d(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：z_channels,
                z_channels,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：z_channels,
                z_channels,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kernel_size=(3, 1, 1),
                kernel_size=(3, 1, 1),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stride=1,
                stride=1,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding=0,
                padding=0,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x: torch.Tensor) -> torch.Tensor:
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.patcher3d(x)
        x = self.patcher3d(x)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# downsampling
        # downsampling
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hs = [self.conv_in(x)]
        hs = [self.conv_in(x)]
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i_level in range(self.num_resolutions):
        for i_level in range(self.num_resolutions):
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i_block in range(self.num_res_blocks):
            for i_block in range(self.num_res_blocks):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.down[i_level].block[i_block](hs[-1])
                h = self.down[i_level].block[i_block](hs[-1])
                # 中文说明：根据条件选择执行分支；代码：if len(self.down[i_level].attn) > 0:
                if len(self.down[i_level].attn) > 0:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.down[i_level].attn[i_block](h)
                    h = self.down[i_level].attn[i_block](h)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：hs.append(h)
                hs.append(h)
            # 中文说明：根据条件选择执行分支；代码：if i_level != self.num_resolutions - 1:
            if i_level != self.num_resolutions - 1:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：hs.append(self.down[i_level].downsample(hs[-1]))
                hs.append(self.down[i_level].downsample(hs[-1]))

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# middle
        # middle
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = hs[-1]
        h = hs[-1]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.mid.block_1(h)
        h = self.mid.block_1(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.mid.attn_1(h)
        h = self.mid.attn_1(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.mid.block_2(h)
        h = self.mid.block_2(h)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# end
        # end
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.norm_out(h)
        h = self.norm_out(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = nonlinearity(h)
        h = nonlinearity(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.conv_out(h)
        h = self.conv_out(h)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return h
        return h


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class DecoderFactorized(nn.Module):
class DecoderFactorized(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out_channels: int,
        out_channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：channels: int,
        channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：channels_mult: list[int],
        channels_mult: list[int],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_res_blocks: int,
        num_res_blocks: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：attn_resolutions: list[int],
        attn_resolutions: list[int],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dropout: float,
        dropout: float,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：resolution: int,
        resolution: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：z_channels: int,
        z_channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：spatial_compression: int = 16,
        spatial_compression: int = 16,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：temporal_compression: int = 8,
        temporal_compression: int = 8,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**ignore_kwargs,
        **ignore_kwargs,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_resolutions = len(channels_mult)
        self.num_resolutions = len(channels_mult)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_res_blocks = num_res_blocks
        self.num_res_blocks = num_res_blocks

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# UnPatcher.
        # UnPatcher.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：patch_size = ignore_kwargs.get("patch_size", 1)
        patch_size = ignore_kwargs.get("patch_size", 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.unpatcher3d = UnPatcher3D(patch_size, ignore_kwargs.get("patch_method", "rearrange"))
        self.unpatcher3d = UnPatcher3D(patch_size, ignore_kwargs.get("patch_method", "rearrange"))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_ch = out_channels * patch_size * patch_size * patch_size
        out_ch = out_channels * patch_size * patch_size * patch_size

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# calculate the number of upsample operations
        # calculate the number of upsample operations
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_spatial_ups = int(math.log2(spatial_compression)) - int(math.log2(patch_size))
        self.num_spatial_ups = int(math.log2(spatial_compression)) - int(math.log2(patch_size))
        # 中文说明：检查运行时假设是否成立；代码：assert self.num_spatial_ups <= self.num_resolutions, f"Spatially upsample {self.num_resolutio...
        assert self.num_spatial_ups <= self.num_resolutions, f"Spatially upsample {self.num_resolutions} times at most"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_temporal_ups = int(math.log2(temporal_compression)) - int(math.log2(patch_size))
        self.num_temporal_ups = int(math.log2(temporal_compression)) - int(math.log2(patch_size))
        # 中文说明：检查运行时假设是否成立；代码：assert (
        assert (
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.num_temporal_ups <= self.num_resolutions
            self.num_temporal_ups <= self.num_resolutions
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"Temporally upsample {self.num_resolutions} times at most"
        ), f"Temporally upsample {self.num_resolutions} times at most"

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_in = channels * channels_mult[self.num_resolutions - 1]
        block_in = channels * channels_mult[self.num_resolutions - 1]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_res = (resolution // patch_size) // 2 ** (self.num_resolutions - 1)
        curr_res = (resolution // patch_size) // 2 ** (self.num_resolutions - 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.z_shape = (1, z_channels, curr_res, curr_res)
        self.z_shape = (1, z_channels, curr_res, curr_res)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：logging.info("Working with z of shape {} = {} dimensions.".format(self.z_shape, np.prod(self....
        logging.info("Working with z of shape {} = {} dimensions.".format(self.z_shape, np.prod(self.z_shape)))

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# z to block_in
        # z to block_in
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv_in = nn.Sequential(
        self.conv_in = nn.Sequential(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(z_channels, block_in, kernel_size=(1, 3, 3), stride=1, padding=1),
            CausalConv3d(z_channels, block_in, kernel_size=(1, 3, 3), stride=1, padding=1),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(block_in, block_in, kernel_size=(3, 1, 1), stride=1, padding=0),
            CausalConv3d(block_in, block_in, kernel_size=(3, 1, 1), stride=1, padding=0),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# middle
        # middle
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid = nn.Module()
        self.mid = nn.Module()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid.block_1 = CausalResnetBlockFactorized3d(
        self.mid.block_1 = CausalResnetBlockFactorized3d(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=block_in,
            in_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=block_in,
            out_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=dropout,
            dropout=dropout,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=1,
            num_groups=1,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid.attn_1 = nn.Sequential(
        self.mid.attn_1 = nn.Sequential(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalAttnBlock(block_in, num_groups=1),
            CausalAttnBlock(block_in, num_groups=1),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalTemporalAttnBlock(block_in, num_groups=1),
            CausalTemporalAttnBlock(block_in, num_groups=1),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid.block_2 = CausalResnetBlockFactorized3d(
        self.mid.block_2 = CausalResnetBlockFactorized3d(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=block_in,
            in_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=block_in,
            out_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=dropout,
            dropout=dropout,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=1,
            num_groups=1,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：legacy_mode = ignore_kwargs.get("legacy_mode", False)
        legacy_mode = ignore_kwargs.get("legacy_mode", False)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# upsampling
        # upsampling
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.up = nn.ModuleList()
        self.up = nn.ModuleList()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i_level in reversed(range(self.num_resolutions)):
        for i_level in reversed(range(self.num_resolutions)):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block = nn.ModuleList()
            block = nn.ModuleList()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn = nn.ModuleList()
            attn = nn.ModuleList()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_out = channels * channels_mult[i_level]
            block_out = channels * channels_mult[i_level]
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _ in range(self.num_res_blocks + 1):
            for _ in range(self.num_res_blocks + 1):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：block.append(
                block.append(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalResnetBlockFactorized3d(
                    CausalResnetBlockFactorized3d(
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=block_in,
                        in_channels=block_in,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=block_out,
                        out_channels=block_out,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=dropout,
                        dropout=dropout,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=1,
                        num_groups=1,
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_in = block_out
                block_in = block_out
                # 中文说明：根据条件选择执行分支；代码：if curr_res in attn_resolutions:
                if curr_res in attn_resolutions:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：attn.append(
                    attn.append(
                        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.Sequential(
                        nn.Sequential(
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalAttnBlock(block_in, num_groups=1),
                            CausalAttnBlock(block_in, num_groups=1),
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalTemporalAttnBlock(block_in, num_groups=1),
                            CausalTemporalAttnBlock(block_in, num_groups=1),
                        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                        )
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：up = nn.Module()
            up = nn.Module()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：up.block = block
            up.block = block
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：up.attn = attn
            up.attn = attn
            # 中文说明：根据条件选择执行分支；代码：if i_level != 0:
            if i_level != 0:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# The layer index for temporal/spatial downsampling performed
                # The layer index for temporal/spatial downsampling performed
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# in the encoder should correspond to the layer index in
                # in the encoder should correspond to the layer index in
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# reverse order where upsampling is performed in the decoder.
                # reverse order where upsampling is performed in the decoder.
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# If you've a pre-trained model, you can simply finetune.
                # If you've a pre-trained model, you can simply finetune.
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：i_level_reverse = self.num_resolutions - i_level - 1
                i_level_reverse = self.num_resolutions - i_level - 1
                # 中文说明：根据条件选择执行分支；代码：if legacy_mode:
                if legacy_mode:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_up = i_level_reverse < self.num_temporal_ups
                    temporal_up = i_level_reverse < self.num_temporal_ups
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_up = 0 < i_level_reverse < self.num_temporal_ups + 1
                    temporal_up = 0 < i_level_reverse < self.num_temporal_ups + 1
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：spatial_up = temporal_up or (
                spatial_up = temporal_up or (
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：i_level_reverse < self.num_spatial_ups and self.num_spatial_ups > self.num_temporal_ups
                    i_level_reverse < self.num_spatial_ups and self.num_spatial_ups > self.num_temporal_ups
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：up.upsample = CausalHybridUpsample3d(block_in, spatial_up=spatial_up, temporal_up=temporal_up)
                up.upsample = CausalHybridUpsample3d(block_in, spatial_up=spatial_up, temporal_up=temporal_up)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_res = curr_res * 2
                curr_res = curr_res * 2
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.up.insert(0, up) # prepend to get consistent order
            self.up.insert(0, up)  # prepend to get consistent order

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# end
        # end
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.norm_out = CausalNormalize(block_in, num_groups=1)
        self.norm_out = CausalNormalize(block_in, num_groups=1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv_out = nn.Sequential(
        self.conv_out = nn.Sequential(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(block_in, out_ch, kernel_size=(1, 3, 3), stride=1, padding=1),
            CausalConv3d(block_in, out_ch, kernel_size=(1, 3, 3), stride=1, padding=1),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(out_ch, out_ch, kernel_size=(3, 1, 1), stride=1, padding=0),
            CausalConv3d(out_ch, out_ch, kernel_size=(3, 1, 1), stride=1, padding=0),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, z):
    def forward(self, z):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.conv_in(z)
        h = self.conv_in(z)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# middle block.
        # middle block.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.mid.block_1(h)
        h = self.mid.block_1(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.mid.attn_1(h)
        h = self.mid.attn_1(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.mid.block_2(h)
        h = self.mid.block_2(h)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# decoder blocks.
        # decoder blocks.
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i_level in reversed(range(self.num_resolutions)):
        for i_level in reversed(range(self.num_resolutions)):
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i_block in range(self.num_res_blocks + 1):
            for i_block in range(self.num_res_blocks + 1):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.up[i_level].block[i_block](h)
                h = self.up[i_level].block[i_block](h)
                # 中文说明：根据条件选择执行分支；代码：if len(self.up[i_level].attn) > 0:
                if len(self.up[i_level].attn) > 0:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.up[i_level].attn[i_block](h)
                    h = self.up[i_level].attn[i_block](h)
            # 中文说明：根据条件选择执行分支；代码：if i_level != 0:
            if i_level != 0:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.up[i_level].upsample(h)
                h = self.up[i_level].upsample(h)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.norm_out(h)
        h = self.norm_out(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = nonlinearity(h)
        h = nonlinearity(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.conv_out(h)
        h = self.conv_out(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.unpatcher3d(h)
        h = self.unpatcher3d(h)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return h
        return h



# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class LDMEncoderFactorized(nn.Module):
class LDMEncoderFactorized(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：in_channels: int,
        in_channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：channels: int,
        channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：channels_mult: list[int],
        channels_mult: list[int],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_res_blocks: int,
        num_res_blocks: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：attn_resolutions: list[int],
        attn_resolutions: list[int],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dropout: float,
        dropout: float,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：resolution: int,
        resolution: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：z_channels: int,
        z_channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：spatial_compression: int = 16,
        spatial_compression: int = 16,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：temporal_compression: int = 8,
        temporal_compression: int = 8,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：act_embedding_num: int=4,
        act_embedding_num: int=4,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：qformer_type='QFormerMF',
        qformer_type='QFormerMF',
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**ignore_kwargs,
        **ignore_kwargs,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_resolutions = len(channels_mult)
        self.num_resolutions = len(channels_mult)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_res_blocks = num_res_blocks
        self.num_res_blocks = num_res_blocks
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Patcher.
        # Patcher.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：patch_size = ignore_kwargs.get("patch_size", 1)
        patch_size = ignore_kwargs.get("patch_size", 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.patcher3d = Patcher3D(patch_size, ignore_kwargs.get("patch_method", "rearrange"))
        self.patcher3d = Patcher3D(patch_size, ignore_kwargs.get("patch_method", "rearrange"))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels = in_channels * patch_size * patch_size * patch_size
        in_channels = in_channels * patch_size * patch_size * patch_size

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# calculate the number of downsample operations
        # calculate the number of downsample operations
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_spatial_downs = int(math.log2(spatial_compression)) - int(math.log2(patch_size))
        self.num_spatial_downs = int(math.log2(spatial_compression)) - int(math.log2(patch_size))
        # 中文说明：检查运行时假设是否成立；代码：assert (
        assert (
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.num_spatial_downs <= self.num_resolutions
            self.num_spatial_downs <= self.num_resolutions
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"Spatially downsample {self.num_resolutions} times at most"
        ), f"Spatially downsample {self.num_resolutions} times at most"

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_temporal_downs = int(math.log2(temporal_compression)) - int(math.log2(patch_size))
        self.num_temporal_downs = int(math.log2(temporal_compression)) - int(math.log2(patch_size))
        # 中文说明：检查运行时假设是否成立；代码：assert (
        assert (
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.num_temporal_downs <= self.num_resolutions
            self.num_temporal_downs <= self.num_resolutions
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"Temporally downsample {self.num_resolutions} times at most"
        ), f"Temporally downsample {self.num_resolutions} times at most"

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# downsampling
        # downsampling
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv_in = nn.Sequential(
        self.conv_in = nn.Sequential(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(
            CausalConv3d(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：in_channels,
                in_channels,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：channels,
                channels,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kernel_size=(1, 3, 3),
                kernel_size=(1, 3, 3),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stride=1,
                stride=1,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding=1,
                padding=1,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(channels, channels, kernel_size=(3, 1, 1), stride=1, padding=0),
            CausalConv3d(channels, channels, kernel_size=(3, 1, 1), stride=1, padding=0),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_res = resolution // patch_size
        curr_res = resolution // patch_size
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_ch_mult = (1,) + tuple(channels_mult)
        in_ch_mult = (1,) + tuple(channels_mult)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.in_ch_mult = in_ch_mult
        self.in_ch_mult = in_ch_mult
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.down = nn.ModuleList()
        self.down = nn.ModuleList()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i_level in range(self.num_resolutions):
        for i_level in range(self.num_resolutions):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block = nn.ModuleList()
            block = nn.ModuleList()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn = nn.ModuleList()
            attn = nn.ModuleList()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_in = channels * in_ch_mult[i_level]
            block_in = channels * in_ch_mult[i_level]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_out = channels * channels_mult[i_level]
            block_out = channels * channels_mult[i_level]
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _ in range(self.num_res_blocks):
            for _ in range(self.num_res_blocks):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：block.append(
                block.append(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalResnetBlockFactorized3d(
                    CausalResnetBlockFactorized3d(
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=block_in,
                        in_channels=block_in,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=block_out,
                        out_channels=block_out,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=dropout,
                        dropout=dropout,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=1,
                        num_groups=1,
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_in = block_out
                block_in = block_out
                # 中文说明：根据条件选择执行分支；代码：if curr_res in attn_resolutions:
                if curr_res in attn_resolutions:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：attn.append(
                    attn.append(
                        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.Sequential(
                        nn.Sequential(
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalAttnBlock(block_in, num_groups=1),
                            CausalAttnBlock(block_in, num_groups=1),
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalTemporalAttnBlock(block_in, num_groups=1),
                            CausalTemporalAttnBlock(block_in, num_groups=1),
                        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                        )
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：down = nn.Module()
            down = nn.Module()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：down.block = block
            down.block = block
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：down.attn = attn
            down.attn = attn
            # 中文说明：根据条件选择执行分支；代码：if i_level != self.num_resolutions - 1:
            if i_level != self.num_resolutions - 1:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：spatial_down = i_level < self.num_spatial_downs
                spatial_down = i_level < self.num_spatial_downs
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_down = i_level < self.num_temporal_downs
                temporal_down = i_level < self.num_temporal_downs
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：down.downsample = CausalHybridDownsample3d(
                down.downsample = CausalHybridDownsample3d(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：block_in,
                    block_in,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：spatial_down=spatial_down,
                    spatial_down=spatial_down,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_down=temporal_down,
                    temporal_down=temporal_down,
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_res = curr_res // 2
                curr_res = curr_res // 2
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.down.append(down)
            self.down.append(down)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# middle
        # middle
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid = nn.Module()
        self.mid = nn.Module()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid.block_1 = CausalResnetBlockFactorized3d(
        self.mid.block_1 = CausalResnetBlockFactorized3d(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=block_in,
            in_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=block_in,
            out_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=dropout,
            dropout=dropout,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=1,
            num_groups=1,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid.attn_1 = nn.Sequential(
        self.mid.attn_1 = nn.Sequential(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalAttnBlock(block_in, num_groups=1),
            CausalAttnBlock(block_in, num_groups=1),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalTemporalAttnBlock(block_in, num_groups=1),
            CausalTemporalAttnBlock(block_in, num_groups=1),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid.block_2 = CausalResnetBlockFactorized3d(
        self.mid.block_2 = CausalResnetBlockFactorized3d(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=block_in,
            in_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=block_in,
            out_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=dropout,
            dropout=dropout,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=1,
            num_groups=1,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# end
        # end
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.norm_out = CausalNormalize(block_in, num_groups=1)
        self.norm_out = CausalNormalize(block_in, num_groups=1)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self.conv_out = nn.Sequential(
        # self.conv_out = nn.Sequential(
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# CausalConv3d(block_in, z_channels, kernel_size=(1, 3, 3), stride=1, padding=1),
        #     CausalConv3d(block_in, z_channels, kernel_size=(1, 3, 3), stride=1, padding=1),
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# CausalConv3d(
        #     CausalConv3d(
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# z_channels,
        #         z_channels,
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# z_channels,
        #         z_channels,
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# kernel_size=(3, 1, 1),
        #         kernel_size=(3, 1, 1),
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# stride=1,
        #         stride=1,
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# padding=0,
        #         padding=0,
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# ),
        #     ),
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# )
        # )
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：encoder_out_dim = 512
        encoder_out_dim = 512
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# act_embedding_num = 4
        # act_embedding_num = 4
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.pos_embedding = PositionEmbeddingRandom(encoder_out_dim // 2)
        self.pos_embedding = PositionEmbeddingRandom(encoder_out_dim // 2)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.act = nn.Embedding(act_embedding_num, encoder_out_dim)
        self.act = nn.Embedding(act_embedding_num, encoder_out_dim)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.qformer_ldm = qformer_map[qformer_type](2, encoder_out_dim, 4, encoder_out_dim, qformer_...
        self.qformer_ldm = qformer_map[qformer_type](2, encoder_out_dim, 4, encoder_out_dim, qformer_num=act_embedding_num)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self.outproj_ldm = nn.Linear(encoder_out_dim, z_channels)
        # self.outproj_ldm = nn.Linear(encoder_out_dim, z_channels)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.outproj_ldm = CausalConv3d(encoder_out_dim, z_channels, kernel_size=1, padding=0)
        self.outproj_ldm = CausalConv3d(encoder_out_dim, z_channels, kernel_size=1, padding=0)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x: torch.Tensor) -> torch.Tensor:
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.patcher3d(x) #x: torch.Size([1, 3, T, 320, 512]) -> torch.Size([1, 192, 1 + T // 4, ...
        x = self.patcher3d(x) #x: torch.Size([1, 3, T, 320, 512]) -> torch.Size([1, 192, 1 + T // 4, 80, 128])

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# downsampling
        # downsampling
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hs = [self.conv_in(x)]
        hs = [self.conv_in(x)]
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i_level in range(self.num_resolutions):
        for i_level in range(self.num_resolutions):
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i_block in range(self.num_res_blocks):
            for i_block in range(self.num_res_blocks):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.down[i_level].block[i_block](hs[-1])
                h = self.down[i_level].block[i_block](hs[-1])
                # 中文说明：根据条件选择执行分支；代码：if len(self.down[i_level].attn) > 0:
                if len(self.down[i_level].attn) > 0:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.down[i_level].attn[i_block](h)
                    h = self.down[i_level].attn[i_block](h)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：hs.append(h)
                hs.append(h)
            # 中文说明：根据条件选择执行分支；代码：if i_level != self.num_resolutions - 1:
            if i_level != self.num_resolutions - 1:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：hs.append(self.down[i_level].downsample(hs[-1]))
                hs.append(self.down[i_level].downsample(hs[-1]))

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# middle
        # middle
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = hs[-1]
        h = hs[-1]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.mid.block_1(h)
        h = self.mid.block_1(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.mid.attn_1(h)
        h = self.mid.attn_1(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.mid.block_2(h)
        h = self.mid.block_2(h)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# end
        # end
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.norm_out(h)
        h = self.norm_out(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = nonlinearity(h)
        h = nonlinearity(h)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# h = self.conv_out(h)
        # h = self.conv_out(h)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：bz, _, video_length, height, width = h.shape
        bz, _, video_length, height, width = h.shape
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：bz = bz if isinstance(bz, int) else bz.item()
        bz = bz if isinstance(bz, int) else bz.item()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dense_pe = torch.stack([self.pos_embedding((height, width)) for i in range(video_length)]).pe...
        dense_pe = torch.stack([self.pos_embedding((height, width)) for i in range(video_length)]).permute(1, 0, 2, 3)[None]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dense_pe = torch.repeat_interleave(dense_pe, bz, dim=0) # dense_pe: torch.Size([1, 512, 5, 20...
        dense_pe = torch.repeat_interleave(dense_pe, bz, dim=0) # dense_pe: torch.Size([1, 512, 5, 20, 32])
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：query = torch.repeat_interleave(self.act.weight[None], bz, dim=0) # query: torch.Size([1, 1, ...
        query = torch.repeat_interleave(self.act.weight[None], bz, dim=0)  # query: torch.Size([1, 1, 512])

        # 中文说明：根据条件选择执行分支；代码：if h.shape[2] > 1:
        if h.shape[2] > 1:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：query = self.qformer_ldm(h, dense_pe, query)
            query = self.qformer_ldm(h, dense_pe, query) 
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：query = self.outproj_ldm(query.permute(0, 2, 1).unsqueeze(-1).unsqueeze(-1)) #B, 16, T-1, 1, 1
            query = self.outproj_ldm(query.permute(0, 2, 1).unsqueeze(-1).unsqueeze(-1)) #B, 16, T-1, 1, 1
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：query = None
            query = None
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# query = self.quant_conv(query) #B, 16, T-1, 1, 1
        # query = self.quant_conv(query) #B, 16, T-1, 1, 1
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# quant_query = self.quantizer(query)
        # quant_query = self.quantizer(query)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return h, query
        return h, query


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class LDMEncoderFactorizedV2(nn.Module):
class LDMEncoderFactorizedV2(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：in_channels: int,
        in_channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：channels: int,
        channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：channels_mult: list[int],
        channels_mult: list[int],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_res_blocks: int,
        num_res_blocks: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：attn_resolutions: list[int],
        attn_resolutions: list[int],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dropout: float,
        dropout: float,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：resolution: int,
        resolution: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：z_channels: int,
        z_channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：spatial_compression: int = 16,
        spatial_compression: int = 16,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：temporal_compression: int = 8,
        temporal_compression: int = 8,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**ignore_kwargs,
        **ignore_kwargs,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_resolutions = len(channels_mult)
        self.num_resolutions = len(channels_mult)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_res_blocks = num_res_blocks
        self.num_res_blocks = num_res_blocks

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Patcher.
        # Patcher.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：patch_size = ignore_kwargs.get("patch_size", 1)
        patch_size = ignore_kwargs.get("patch_size", 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.patcher3d = Patcher3D(patch_size, ignore_kwargs.get("patch_method", "rearrange"))
        self.patcher3d = Patcher3D(patch_size, ignore_kwargs.get("patch_method", "rearrange"))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels = in_channels * patch_size * patch_size * patch_size
        in_channels = in_channels * patch_size * patch_size * patch_size

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# calculate the number of downsample operations
        # calculate the number of downsample operations
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_spatial_downs = int(math.log2(spatial_compression)) - int(math.log2(patch_size))
        self.num_spatial_downs = int(math.log2(spatial_compression)) - int(math.log2(patch_size))
        # 中文说明：检查运行时假设是否成立；代码：assert (
        assert (
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.num_spatial_downs <= self.num_resolutions
            self.num_spatial_downs <= self.num_resolutions
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"Spatially downsample {self.num_resolutions} times at most"
        ), f"Spatially downsample {self.num_resolutions} times at most"

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_temporal_downs = int(math.log2(temporal_compression)) - int(math.log2(patch_size))
        self.num_temporal_downs = int(math.log2(temporal_compression)) - int(math.log2(patch_size))
        # 中文说明：检查运行时假设是否成立；代码：assert (
        assert (
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.num_temporal_downs <= self.num_resolutions
            self.num_temporal_downs <= self.num_resolutions
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"Temporally downsample {self.num_resolutions} times at most"
        ), f"Temporally downsample {self.num_resolutions} times at most"

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# downsampling
        # downsampling
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv_in = nn.Sequential(
        self.conv_in = nn.Sequential(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(
            CausalConv3d(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：in_channels,
                in_channels,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：channels,
                channels,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kernel_size=(1, 3, 3),
                kernel_size=(1, 3, 3),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stride=1,
                stride=1,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding=1,
                padding=1,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(channels, channels, kernel_size=(3, 1, 1), stride=1, padding=0),
            CausalConv3d(channels, channels, kernel_size=(3, 1, 1), stride=1, padding=0),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_res = resolution // patch_size
        curr_res = resolution // patch_size
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_ch_mult = (1,) + tuple(channels_mult)
        in_ch_mult = (1,) + tuple(channels_mult)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.in_ch_mult = in_ch_mult
        self.in_ch_mult = in_ch_mult
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.down = nn.ModuleList()
        self.down = nn.ModuleList()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i_level in range(self.num_resolutions):
        for i_level in range(self.num_resolutions):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block = nn.ModuleList()
            block = nn.ModuleList()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn = nn.ModuleList()
            attn = nn.ModuleList()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_in = channels * in_ch_mult[i_level]
            block_in = channels * in_ch_mult[i_level]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_out = channels * channels_mult[i_level]
            block_out = channels * channels_mult[i_level]
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _ in range(self.num_res_blocks):
            for _ in range(self.num_res_blocks):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：block.append(
                block.append(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalResnetBlockFactorized3d(
                    CausalResnetBlockFactorized3d(
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=block_in,
                        in_channels=block_in,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=block_out,
                        out_channels=block_out,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=dropout,
                        dropout=dropout,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=1,
                        num_groups=1,
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_in = block_out
                block_in = block_out
                # 中文说明：根据条件选择执行分支；代码：if curr_res in attn_resolutions:
                if curr_res in attn_resolutions:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：attn.append(
                    attn.append(
                        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.Sequential(
                        nn.Sequential(
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalAttnBlock(block_in, num_groups=1),
                            CausalAttnBlock(block_in, num_groups=1),
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalTemporalAttnBlock(block_in, num_groups=1),
                            CausalTemporalAttnBlock(block_in, num_groups=1),
                        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                        )
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：down = nn.Module()
            down = nn.Module()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：down.block = block
            down.block = block
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：down.attn = attn
            down.attn = attn
            # 中文说明：根据条件选择执行分支；代码：if i_level != self.num_resolutions - 1:
            if i_level != self.num_resolutions - 1:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：spatial_down = i_level < self.num_spatial_downs
                spatial_down = i_level < self.num_spatial_downs
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_down = i_level < self.num_temporal_downs
                temporal_down = i_level < self.num_temporal_downs
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：down.downsample = CausalHybridDownsample3d(
                down.downsample = CausalHybridDownsample3d(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：block_in,
                    block_in,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：spatial_down=spatial_down,
                    spatial_down=spatial_down,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_down=temporal_down,
                    temporal_down=temporal_down,
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_res = curr_res // 2
                curr_res = curr_res // 2
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.down.append(down)
            self.down.append(down)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# middle
        # middle
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid = nn.Module()
        self.mid = nn.Module()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid.block_1 = CausalResnetBlockFactorized3d(
        self.mid.block_1 = CausalResnetBlockFactorized3d(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=block_in,
            in_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=block_in,
            out_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=dropout,
            dropout=dropout,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=1,
            num_groups=1,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid.attn_1 = nn.Sequential(
        self.mid.attn_1 = nn.Sequential(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalAttnBlock(block_in, num_groups=1),
            CausalAttnBlock(block_in, num_groups=1),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalTemporalAttnBlock(block_in, num_groups=1),
            CausalTemporalAttnBlock(block_in, num_groups=1),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid.block_2 = CausalResnetBlockFactorized3d(
        self.mid.block_2 = CausalResnetBlockFactorized3d(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=block_in,
            in_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=block_in,
            out_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=dropout,
            dropout=dropout,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=1,
            num_groups=1,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# end
        # end
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.norm_out = CausalNormalize(block_in, num_groups=1)
        self.norm_out = CausalNormalize(block_in, num_groups=1)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self.conv_out = nn.Sequential(
        # self.conv_out = nn.Sequential(
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# CausalConv3d(block_in, z_channels, kernel_size=(1, 3, 3), stride=1, padding=1),
        #     CausalConv3d(block_in, z_channels, kernel_size=(1, 3, 3), stride=1, padding=1),
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# CausalConv3d(
        #     CausalConv3d(
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# z_channels,
        #         z_channels,
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# z_channels,
        #         z_channels,
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# kernel_size=(3, 1, 1),
        #         kernel_size=(3, 1, 1),
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# stride=1,
        #         stride=1,
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# padding=0,
        #         padding=0,
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# ),
        #     ),
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# )
        # )
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：down_out = nn.Module()
        down_out = nn.Module()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：down_out.attn = nn.ModuleList()
        down_out.attn = nn.ModuleList()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：down_out.downsample = nn.ModuleList()
        down_out.downsample = nn.ModuleList()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _ in range(2):
        for _ in range(2):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn = nn.Sequential(
            attn = nn.Sequential(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalAttnBlock(block_in, num_groups=1),
                CausalAttnBlock(block_in, num_groups=1),
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalTemporalAttnBlock(block_in, num_groups=1),
                CausalTemporalAttnBlock(block_in, num_groups=1),
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：down_out.attn.append(attn)
            down_out.attn.append(attn)

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：downsample = CausalHybridDownsample3d(
            downsample = CausalHybridDownsample3d(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：block_in,
                        block_in,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：spatial_down=True,
                        spatial_down=True,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_down=False,
                        temporal_down=False,
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：down_out.downsample.append(downsample)
            down_out.downsample.append(downsample)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.down_out = down_out
        self.down_out = down_out

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# encoder_out_dim = 512
        # encoder_out_dim = 512
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# # act_embedding_num = 4
        # # act_embedding_num = 4
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self.pos_embedding = PositionEmbeddingRandom(encoder_out_dim // 2)
        # self.pos_embedding = PositionEmbeddingRandom(encoder_out_dim // 2)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self.act = nn.Embedding(act_embedding_num, encoder_out_dim)
        # self.act = nn.Embedding(act_embedding_num, encoder_out_dim)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self.qformer_ldm = QFormerMFSep(2, encoder_out_dim, 4, encoder_out_dim, qformer_num=act_emb...
        # self.qformer_ldm = QFormerMFSep(2, encoder_out_dim, 4, encoder_out_dim, qformer_num=act_embedding_num)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# # self.outproj_ldm = nn.Linear(encoder_out_dim, z_channels)
        # # self.outproj_ldm = nn.Linear(encoder_out_dim, z_channels)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self.outproj_ldm = CausalConv3d(encoder_out_dim, z_channels, kernel_size=1, padding=0)
        # self.outproj_ldm = CausalConv3d(encoder_out_dim, z_channels, kernel_size=1, padding=0)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x: torch.Tensor) -> torch.Tensor:
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.patcher3d(x) #x: torch.Size([1, 3, T, 320, 512]) -> torch.Size([1, 192, 1 + T // 4, ...
        x = self.patcher3d(x) #x: torch.Size([1, 3, T, 320, 512]) -> torch.Size([1, 192, 1 + T // 4, 80, 128])

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# downsampling
        # downsampling
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hs = [self.conv_in(x)]
        hs = [self.conv_in(x)]
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i_level in range(self.num_resolutions):
        for i_level in range(self.num_resolutions):
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i_block in range(self.num_res_blocks):
            for i_block in range(self.num_res_blocks):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.down[i_level].block[i_block](hs[-1])
                h = self.down[i_level].block[i_block](hs[-1])
                # 中文说明：根据条件选择执行分支；代码：if len(self.down[i_level].attn) > 0:
                if len(self.down[i_level].attn) > 0:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.down[i_level].attn[i_block](h)
                    h = self.down[i_level].attn[i_block](h)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：hs.append(h)
                hs.append(h)
            # 中文说明：根据条件选择执行分支；代码：if i_level != self.num_resolutions - 1:
            if i_level != self.num_resolutions - 1:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：hs.append(self.down[i_level].downsample(hs[-1]))
                hs.append(self.down[i_level].downsample(hs[-1]))

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# middle
        # middle
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = hs[-1]
        h = hs[-1]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.mid.block_1(h)
        h = self.mid.block_1(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.mid.attn_1(h)
        h = self.mid.attn_1(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.mid.block_2(h)
        h = self.mid.block_2(h)


        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# down for latent code
        # down for latent code  
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for level in range(len(self.down_out.attn)):
        for level in range(len(self.down_out.attn)):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.down_out.attn[level](h)
            h = self.down_out.attn[level](h)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.down_out.downsample[level](h)
            h = self.down_out.downsample[level](h)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# end
        # end
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.norm_out(h)
        h = self.norm_out(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = nonlinearity(h)
        h = nonlinearity(h)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# h = self.conv_out(h)
        # h = self.conv_out(h)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：bz, _, video_length, height, width = h.shape
        bz, _, video_length, height, width = h.shape
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：bz = bz if isinstance(bz, int) else bz.item()
        bz = bz if isinstance(bz, int) else bz.item()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dense_pe = torch.stack([self.pos_embedding((height, width)) for i in range(video_length)]).pe...
        dense_pe = torch.stack([self.pos_embedding((height, width)) for i in range(video_length)]).permute(1, 0, 2, 3)[None]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dense_pe = torch.repeat_interleave(dense_pe, bz, dim=0) # dense_pe: torch.Size([1, 512, 5, 20...
        dense_pe = torch.repeat_interleave(dense_pe, bz, dim=0) # dense_pe: torch.Size([1, 512, 5, 20, 32])
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：query = torch.repeat_interleave(self.act.weight[None], bz, dim=0) # query: torch.Size([1, 1, ...
        query = torch.repeat_interleave(self.act.weight[None], bz, dim=0)  # query: torch.Size([1, 1, 512])

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：query = self.qformer_ldm(h, dense_pe, query)
        query = self.qformer_ldm(h, dense_pe, query)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：query = self.outproj_ldm(query.permute(0, 2, 1).unsqueeze(-1).unsqueeze(-1)) #B, 16, T-1, 1, 1
        query = self.outproj_ldm(query.permute(0, 2, 1).unsqueeze(-1).unsqueeze(-1)) #B, 16, T-1, 1, 1

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# query = self.quant_conv(query) #B, 16, T-1, 1, 1
        # query = self.quant_conv(query) #B, 16, T-1, 1, 1
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# quant_query = self.quantizer(query)
        # quant_query = self.quantizer(query)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return h, query
        return h, query

# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class LDMDecoderFactorized(nn.Module):
class LDMDecoderFactorized(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out_channels: int,
        out_channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：channels: int,
        channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：channels_mult: list[int],
        channels_mult: list[int],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_res_blocks: int,
        num_res_blocks: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：attn_resolutions: list[int],
        attn_resolutions: list[int],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dropout: float,
        dropout: float,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：resolution: int,
        resolution: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：z_channels: int,
        z_channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：spatial_compression: int = 16,
        spatial_compression: int = 16,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：temporal_compression: int = 8,
        temporal_compression: int = 8,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**ignore_kwargs,
        **ignore_kwargs,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_resolutions = len(channels_mult)
        self.num_resolutions = len(channels_mult)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_res_blocks = num_res_blocks
        self.num_res_blocks = num_res_blocks

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# UnPatcher.
        # UnPatcher.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：patch_size = ignore_kwargs.get("patch_size", 1)
        patch_size = ignore_kwargs.get("patch_size", 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.unpatcher3d = UnPatcher3D(patch_size, ignore_kwargs.get("patch_method", "rearrange"))
        self.unpatcher3d = UnPatcher3D(patch_size, ignore_kwargs.get("patch_method", "rearrange"))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_ch = out_channels * patch_size * patch_size * patch_size
        out_ch = out_channels * patch_size * patch_size * patch_size

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# calculate the number of upsample operations
        # calculate the number of upsample operations
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_spatial_ups = int(math.log2(spatial_compression)) - int(math.log2(patch_size))
        self.num_spatial_ups = int(math.log2(spatial_compression)) - int(math.log2(patch_size))
        # 中文说明：检查运行时假设是否成立；代码：assert self.num_spatial_ups <= self.num_resolutions, f"Spatially upsample {self.num_resolutio...
        assert self.num_spatial_ups <= self.num_resolutions, f"Spatially upsample {self.num_resolutions} times at most"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_temporal_ups = int(math.log2(temporal_compression)) - int(math.log2(patch_size))
        self.num_temporal_ups = int(math.log2(temporal_compression)) - int(math.log2(patch_size))
        # 中文说明：检查运行时假设是否成立；代码：assert (
        assert (
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.num_temporal_ups <= self.num_resolutions
            self.num_temporal_ups <= self.num_resolutions
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"Temporally upsample {self.num_resolutions} times at most"
        ), f"Temporally upsample {self.num_resolutions} times at most"

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_in = channels * channels_mult[self.num_resolutions - 1]
        block_in = channels * channels_mult[self.num_resolutions - 1]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_res = (resolution // patch_size) // 2 ** (self.num_resolutions - 1)
        curr_res = (resolution // patch_size) // 2 ** (self.num_resolutions - 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.z_shape = (1, z_channels, curr_res, curr_res)
        self.z_shape = (1, z_channels, curr_res, curr_res)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：logging.info("Working with z of shape {} = {} dimensions.".format(self.z_shape, np.prod(self....
        logging.info("Working with z of shape {} = {} dimensions.".format(self.z_shape, np.prod(self.z_shape)))

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# z to block_in
        # z to block_in
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv_in = nn.Sequential(
        self.conv_in = nn.Sequential(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(z_channels, block_in, kernel_size=(1, 3, 3), stride=1, padding=1),
            CausalConv3d(z_channels, block_in, kernel_size=(1, 3, 3), stride=1, padding=1),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(block_in, block_in, kernel_size=(3, 1, 1), stride=1, padding=0),
            CausalConv3d(block_in, block_in, kernel_size=(3, 1, 1), stride=1, padding=0),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# middle
        # middle
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid = nn.Module()
        self.mid = nn.Module()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid.block_1 = CausalResnetBlockFactorized3d(
        self.mid.block_1 = CausalResnetBlockFactorized3d(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=block_in,
            in_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=block_in,
            out_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=dropout,
            dropout=dropout,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=1,
            num_groups=1,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid.attn_1 = nn.Sequential(
        self.mid.attn_1 = nn.Sequential(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalAttnBlock(block_in, num_groups=1),
            CausalAttnBlock(block_in, num_groups=1),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalTemporalAttnBlock(block_in, num_groups=1),
            CausalTemporalAttnBlock(block_in, num_groups=1),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid.block_2 = CausalResnetBlockFactorized3d(
        self.mid.block_2 = CausalResnetBlockFactorized3d(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=block_in,
            in_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=block_in,
            out_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=dropout,
            dropout=dropout,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=1,
            num_groups=1,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：legacy_mode = ignore_kwargs.get("legacy_mode", False)
        legacy_mode = ignore_kwargs.get("legacy_mode", False)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# upsampling
        # upsampling
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.up = nn.ModuleList()
        self.up = nn.ModuleList()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i_level in reversed(range(self.num_resolutions)):
        for i_level in reversed(range(self.num_resolutions)):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block = nn.ModuleList()
            block = nn.ModuleList()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn = nn.ModuleList()
            attn = nn.ModuleList()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_out = channels * channels_mult[i_level]
            block_out = channels * channels_mult[i_level]
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _ in range(self.num_res_blocks + 1):
            for _ in range(self.num_res_blocks + 1):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：block.append(
                block.append(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalResnetBlockFactorized3d(
                    CausalResnetBlockFactorized3d(
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=block_in,
                        in_channels=block_in,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=block_out,
                        out_channels=block_out,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=dropout,
                        dropout=dropout,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=1,
                        num_groups=1,
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_in = block_out
                block_in = block_out
                # 中文说明：根据条件选择执行分支；代码：if curr_res in attn_resolutions:
                if curr_res in attn_resolutions:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：attn.append(
                    attn.append(
                        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.Sequential(
                        nn.Sequential(
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalAttnBlock(block_in, num_groups=1),
                            CausalAttnBlock(block_in, num_groups=1),
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalTemporalAttnBlock(block_in, num_groups=1),
                            CausalTemporalAttnBlock(block_in, num_groups=1),
                        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                        )
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：up = nn.Module()
            up = nn.Module()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：up.block = block
            up.block = block
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：up.attn = attn
            up.attn = attn
            # 中文说明：根据条件选择执行分支；代码：if i_level != 0:
            if i_level != 0:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# The layer index for temporal/spatial downsampling performed
                # The layer index for temporal/spatial downsampling performed
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# in the encoder should correspond to the layer index in
                # in the encoder should correspond to the layer index in
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# reverse order where upsampling is performed in the decoder.
                # reverse order where upsampling is performed in the decoder.
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# If you've a pre-trained model, you can simply finetune.
                # If you've a pre-trained model, you can simply finetune.
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：i_level_reverse = self.num_resolutions - i_level - 1
                i_level_reverse = self.num_resolutions - i_level - 1
                # 中文说明：根据条件选择执行分支；代码：if legacy_mode:
                if legacy_mode:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_up = i_level_reverse < self.num_temporal_ups
                    temporal_up = i_level_reverse < self.num_temporal_ups
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_up = 0 < i_level_reverse < self.num_temporal_ups + 1
                    temporal_up = 0 < i_level_reverse < self.num_temporal_ups + 1
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：spatial_up = temporal_up or (
                spatial_up = temporal_up or (
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：i_level_reverse < self.num_spatial_ups and self.num_spatial_ups > self.num_temporal_ups
                    i_level_reverse < self.num_spatial_ups and self.num_spatial_ups > self.num_temporal_ups
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：up.upsample = CausalHybridUpsample3d(block_in, spatial_up=spatial_up, temporal_up=temporal_up)
                up.upsample = CausalHybridUpsample3d(block_in, spatial_up=spatial_up, temporal_up=temporal_up)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_res = curr_res * 2
                curr_res = curr_res * 2
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.up.insert(0, up) # prepend to get consistent order
            self.up.insert(0, up)  # prepend to get consistent order

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# end
        # end
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.norm_out = CausalNormalize(block_in, num_groups=1)
        self.norm_out = CausalNormalize(block_in, num_groups=1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv_out = nn.Sequential(
        self.conv_out = nn.Sequential(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(block_in, out_ch, kernel_size=(1, 3, 3), stride=1, padding=1),
            CausalConv3d(block_in, out_ch, kernel_size=(1, 3, 3), stride=1, padding=1),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(out_ch, out_ch, kernel_size=(3, 1, 1), stride=1, padding=0),
            CausalConv3d(out_ch, out_ch, kernel_size=(3, 1, 1), stride=1, padding=0),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, encoded_video, z):
    def forward(self, encoded_video, z):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z = self.conv_in(z)
        z = self.conv_in(z)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z = torch.repeat_interleave(z, int(encoded_video.shape[-2]), dim=-2)
        z = torch.repeat_interleave(z, int(encoded_video.shape[-2]), dim=-2)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z = torch.repeat_interleave(z, int(encoded_video.shape[-1]), dim=-1)
        z = torch.repeat_interleave(z, int(encoded_video.shape[-1]), dim=-1)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = torch.cat((encoded_video[:, :, :1], z), dim=2)
        h = torch.cat((encoded_video[:, :, :1], z), dim=2)
        
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# middle block.
        # middle block.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.mid.block_1(h)
        h = self.mid.block_1(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.mid.attn_1(h)
        h = self.mid.attn_1(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.mid.block_2(h) #[1, 512, T, h, w]
        h = self.mid.block_2(h) #[1, 512, T, h, w]

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# decoder blocks.
        # decoder blocks.
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i_level in reversed(range(self.num_resolutions)):
        for i_level in reversed(range(self.num_resolutions)):
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i_block in range(self.num_res_blocks + 1):
            for i_block in range(self.num_res_blocks + 1):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.up[i_level].block[i_block](h)
                h = self.up[i_level].block[i_block](h)
                # 中文说明：根据条件选择执行分支；代码：if len(self.up[i_level].attn) > 0:
                if len(self.up[i_level].attn) > 0:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.up[i_level].attn[i_block](h)
                    h = self.up[i_level].attn[i_block](h)
            # 中文说明：根据条件选择执行分支；代码：if i_level != 0:
            if i_level != 0:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.up[i_level].upsample(h)
                h = self.up[i_level].upsample(h)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.norm_out(h) #[1, 256, T, h, w]
        h = self.norm_out(h) #[1, 256, T, h, w]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = nonlinearity(h)
        h = nonlinearity(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.conv_out(h)
        h = self.conv_out(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.unpatcher3d(h)
        h = self.unpatcher3d(h)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return h
        return h



# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class LDMDecoderFactorizedV2(nn.Module):
class LDMDecoderFactorizedV2(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out_channels: int,
        out_channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：channels: int,
        channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：channels_mult: list[int],
        channels_mult: list[int],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_res_blocks: int,
        num_res_blocks: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：attn_resolutions: list[int],
        attn_resolutions: list[int],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dropout: float,
        dropout: float,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：resolution: int,
        resolution: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：z_channels: int,
        z_channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：spatial_compression: int = 16,
        spatial_compression: int = 16,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：temporal_compression: int = 8,
        temporal_compression: int = 8,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**ignore_kwargs,
        **ignore_kwargs,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_resolutions = len(channels_mult)
        self.num_resolutions = len(channels_mult)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_res_blocks = num_res_blocks
        self.num_res_blocks = num_res_blocks
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.temporal_compression = temporal_compression
        self.temporal_compression = temporal_compression
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# UnPatcher.
        # UnPatcher.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.act_embedding_num = ignore_kwargs.get("act_embedding_num", 4)
        self.act_embedding_num = ignore_kwargs.get("act_embedding_num", 4)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：patch_size = ignore_kwargs.get("patch_size", 1)
        patch_size = ignore_kwargs.get("patch_size", 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.unpatcher3d = UnPatcher3D(patch_size, ignore_kwargs.get("patch_method", "rearrange"))
        self.unpatcher3d = UnPatcher3D(patch_size, ignore_kwargs.get("patch_method", "rearrange"))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_ch = out_channels * patch_size * patch_size * patch_size
        out_ch = out_channels * patch_size * patch_size * patch_size

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# calculate the number of upsample operations
        # calculate the number of upsample operations
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_spatial_ups = int(math.log2(spatial_compression)) - int(math.log2(patch_size))
        self.num_spatial_ups = int(math.log2(spatial_compression)) - int(math.log2(patch_size))
        # 中文说明：检查运行时假设是否成立；代码：assert self.num_spatial_ups <= self.num_resolutions, f"Spatially upsample {self.num_resolutio...
        assert self.num_spatial_ups <= self.num_resolutions, f"Spatially upsample {self.num_resolutions} times at most"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_temporal_ups = int(math.log2(temporal_compression)) - int(math.log2(patch_size))
        self.num_temporal_ups = int(math.log2(temporal_compression)) - int(math.log2(patch_size))
        # 中文说明：检查运行时假设是否成立；代码：assert (
        assert (
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.num_temporal_ups <= self.num_resolutions
            self.num_temporal_ups <= self.num_resolutions
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"Temporally upsample {self.num_resolutions} times at most"
        ), f"Temporally upsample {self.num_resolutions} times at most"

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_in = channels * channels_mult[self.num_resolutions - 1]
        block_in = channels * channels_mult[self.num_resolutions - 1]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_res = (resolution // patch_size) // 2 ** (self.num_resolutions - 1)
        curr_res = (resolution // patch_size) // 2 ** (self.num_resolutions - 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.z_shape = (1, z_channels, curr_res, curr_res)
        self.z_shape = (1, z_channels, curr_res, curr_res)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：logging.info("Working with z of shape {} = {} dimensions.".format(self.z_shape, np.prod(self....
        logging.info("Working with z of shape {} = {} dimensions.".format(self.z_shape, np.prod(self.z_shape)))

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# z to block_in
        # z to block_in
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv_in = nn.Sequential(
        self.conv_in = nn.Sequential(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(z_channels, block_in, kernel_size=(1, 3, 3), stride=1, padding=1),
            CausalConv3d(z_channels, block_in, kernel_size=(1, 3, 3), stride=1, padding=1),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(block_in, block_in, kernel_size=(3, 1, 1), stride=1, padding=0),
            CausalConv3d(block_in, block_in, kernel_size=(3, 1, 1), stride=1, padding=0),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# middle
        # middle
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid = nn.Module()
        self.mid = nn.Module()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid.block_1 = CausalResnetBlockFactorized3d(
        self.mid.block_1 = CausalResnetBlockFactorized3d(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=block_in,
            in_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=block_in,
            out_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=dropout,
            dropout=dropout,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=1,
            num_groups=1,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid.attn_1 = nn.Sequential(
        self.mid.attn_1 = nn.Sequential(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalCrossAttention(block_in, context_dim=block_in, num_groups=1),
            CausalCrossAttention(block_in, context_dim=block_in, num_groups=1),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalAttnBlock(block_in, num_groups=1),
            CausalAttnBlock(block_in, num_groups=1),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalTemporalAttnBlock(block_in, num_groups=1),
            CausalTemporalAttnBlock(block_in, num_groups=1),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid.block_2 = CausalResnetBlockFactorized3d(
        self.mid.block_2 = CausalResnetBlockFactorized3d(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=block_in,
            in_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=block_in,
            out_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=dropout,
            dropout=dropout,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=1,
            num_groups=1,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：legacy_mode = ignore_kwargs.get("legacy_mode", False)
        legacy_mode = ignore_kwargs.get("legacy_mode", False)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# upsampling
        # upsampling
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn_resolutions = [64]
        attn_resolutions = [64]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.up = nn.ModuleList()
        self.up = nn.ModuleList()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i_level in reversed(range(self.num_resolutions)):
        for i_level in reversed(range(self.num_resolutions)):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block = nn.ModuleList()
            block = nn.ModuleList()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn = nn.ModuleList()
            attn = nn.ModuleList()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_out = channels * channels_mult[i_level]
            block_out = channels * channels_mult[i_level]
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _ in range(self.num_res_blocks + 1):
            for _ in range(self.num_res_blocks + 1):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：block.append(
                block.append(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalResnetBlockFactorized3d(
                    CausalResnetBlockFactorized3d(
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=block_in,
                        in_channels=block_in,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=block_out,
                        out_channels=block_out,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=dropout,
                        dropout=dropout,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=1,
                        num_groups=1,
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_in = block_out
                block_in = block_out
                # 中文说明：根据条件选择执行分支；代码：if curr_res in attn_resolutions:
                if curr_res in attn_resolutions:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：attn.append(
                    attn.append(
                        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.Sequential(
                        nn.Sequential(
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalCrossAttention(block_in, context_dim=block_in, num_groups=1),
                            CausalCrossAttention(block_in, context_dim=block_in, num_groups=1),
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalAttnBlock(block_in, num_groups=1),
                            CausalAttnBlock(block_in, num_groups=1),
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalTemporalAttnBlock(block_in, num_groups=1),
                            CausalTemporalAttnBlock(block_in, num_groups=1),
                        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                        )
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：up = nn.Module()
            up = nn.Module()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：up.block = block
            up.block = block
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：up.attn = attn
            up.attn = attn
            # 中文说明：根据条件选择执行分支；代码：if i_level != 0:
            if i_level != 0:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# The layer index for temporal/spatial downsampling performed
                # The layer index for temporal/spatial downsampling performed
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# in the encoder should correspond to the layer index in
                # in the encoder should correspond to the layer index in
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# reverse order where upsampling is performed in the decoder.
                # reverse order where upsampling is performed in the decoder.
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# If you've a pre-trained model, you can simply finetune.
                # If you've a pre-trained model, you can simply finetune.
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：i_level_reverse = self.num_resolutions - i_level - 1
                i_level_reverse = self.num_resolutions - i_level - 1
                # 中文说明：根据条件选择执行分支；代码：if legacy_mode:
                if legacy_mode:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_up = i_level_reverse < self.num_temporal_ups
                    temporal_up = i_level_reverse < self.num_temporal_ups
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_up = 0 < i_level_reverse < self.num_temporal_ups + 1
                    temporal_up = 0 < i_level_reverse < self.num_temporal_ups + 1
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：spatial_up = temporal_up or (
                spatial_up = temporal_up or (
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：i_level_reverse < self.num_spatial_ups and self.num_spatial_ups > self.num_temporal_ups
                    i_level_reverse < self.num_spatial_ups and self.num_spatial_ups > self.num_temporal_ups
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：up.upsample = CausalHybridUpsample3d(block_in, spatial_up=spatial_up, temporal_up=temporal_up)
                up.upsample = CausalHybridUpsample3d(block_in, spatial_up=spatial_up, temporal_up=temporal_up)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_res = curr_res * 2
                curr_res = curr_res * 2
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.up.insert(0, up) # prepend to get consistent order
            self.up.insert(0, up)  # prepend to get consistent order

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# end
        # end
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.norm_out = CausalNormalize(block_in, num_groups=1)
        self.norm_out = CausalNormalize(block_in, num_groups=1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv_out = nn.Sequential(
        self.conv_out = nn.Sequential(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(block_in, out_ch, kernel_size=(1, 3, 3), stride=1, padding=1),
            CausalConv3d(block_in, out_ch, kernel_size=(1, 3, 3), stride=1, padding=1),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(out_ch, out_ch, kernel_size=(3, 1, 1), stride=1, padding=0),
            CausalConv3d(out_ch, out_ch, kernel_size=(3, 1, 1), stride=1, padding=0),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trainable_params = sum(p.numel() for p in self.parameters() if p.requires_grad)
        trainable_params = sum(p.numel() for p in self.parameters() if p.requires_grad)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"LDM Decoder total parameters: {trainable_params / 1e6:.2f}MB" )
        print(f"LDM Decoder total parameters: {trainable_params / 1e6:.2f}MB" )

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, encoded_video, z):
    def forward(self, encoded_video, z):
        
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z = self.conv_in(z)
        z = self.conv_in(z)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z = z.flatten(2).permute(0, 2, 1)
        z = z.flatten(2).permute(0, 2, 1)
    
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：repeat_num = (z.shape[1] // self.act_embedding_num) + 1
        repeat_num = (z.shape[1] // self.act_embedding_num) + 1
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = encoded_video[:, :, :1].repeat(1, 1, repeat_num, 1, 1)
        h = encoded_video[:, :, :1].repeat(1, 1, repeat_num, 1, 1)
        
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# middle block.
        # middle block.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.mid.block_1(h)
        h = self.mid.block_1(h)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cross_attn, self_attn, temp_attn = self.mid.attn_1
        cross_attn, self_attn, temp_attn = self.mid.attn_1
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：first_h, sub_h = h[:, :, :1], h[:, :, 1:]
        first_h, sub_h = h[:, :, :1], h[:, :, 1:]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sub_h = cross_attn(sub_h, z)
        sub_h = cross_attn(sub_h, z)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = torch.cat([first_h, sub_h], dim=2)
        h = torch.cat([first_h, sub_h], dim=2)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self_attn(h)
        h = self_attn(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = temp_attn(h)
        h = temp_attn(h)
        
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.mid.block_2(h)
        h = self.mid.block_2(h)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# decoder blocks.
        # decoder blocks.
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i_level in reversed(range(self.num_resolutions)):
        for i_level in reversed(range(self.num_resolutions)):
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i_block in range(self.num_res_blocks + 1):
            for i_block in range(self.num_res_blocks + 1):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.up[i_level].block[i_block](h)
                h = self.up[i_level].block[i_block](h)
                # 中文说明：根据条件选择执行分支；代码：if len(self.up[i_level].attn) > 0:
                if len(self.up[i_level].attn) > 0:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cross_attn, self_attn, temp_attn = self.up[i_level].attn[i_block]
                    cross_attn, self_attn, temp_attn = self.up[i_level].attn[i_block]
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：first_h, sub_h = h[:, :, :1], h[:, :, 1:]
                    first_h, sub_h = h[:, :, :1], h[:, :, 1:]
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sub_h = cross_attn(sub_h, z)
                    sub_h = cross_attn(sub_h, z)
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = torch.cat([first_h, sub_h], dim=2)
                    h = torch.cat([first_h, sub_h], dim=2)
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self_attn(h)
                    h = self_attn(h)
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = temp_attn(h)
                    h = temp_attn(h)
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# h = self.up[i_level].attn[i_block](h, z)
                    # h = self.up[i_level].attn[i_block](h, z)
            # 中文说明：根据条件选择执行分支；代码：if i_level != 0:
            if i_level != 0:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.up[i_level].upsample(h)
                h = self.up[i_level].upsample(h)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.norm_out(h)
        h = self.norm_out(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = nonlinearity(h)
        h = nonlinearity(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.conv_out(h)
        h = self.conv_out(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.unpatcher3d(h)
        h = self.unpatcher3d(h)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return h
        return h
    

# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class LDMDecoderFactorizedV3(nn.Module):
class LDMDecoderFactorizedV3(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out_channels: int,
        out_channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：channels: int,
        channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：channels_mult: list[int],
        channels_mult: list[int],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_res_blocks: int,
        num_res_blocks: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：attn_resolutions: list[int],
        attn_resolutions: list[int],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dropout: float,
        dropout: float,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：resolution: int,
        resolution: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：z_channels: int,
        z_channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：spatial_compression: int = 16,
        spatial_compression: int = 16,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：temporal_compression: int = 8,
        temporal_compression: int = 8,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**ignore_kwargs,
        **ignore_kwargs,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_resolutions = len(channels_mult)
        self.num_resolutions = len(channels_mult)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_res_blocks = num_res_blocks
        self.num_res_blocks = num_res_blocks

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# UnPatcher.
        # UnPatcher.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：patch_size = ignore_kwargs.get("patch_size", 1)
        patch_size = ignore_kwargs.get("patch_size", 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.unpatcher3d = UnPatcher3D(patch_size, ignore_kwargs.get("patch_method", "rearrange"))
        self.unpatcher3d = UnPatcher3D(patch_size, ignore_kwargs.get("patch_method", "rearrange"))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_ch = out_channels * patch_size * patch_size * patch_size
        out_ch = out_channels * patch_size * patch_size * patch_size

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# calculate the number of upsample operations
        # calculate the number of upsample operations
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_spatial_ups = int(math.log2(spatial_compression)) - int(math.log2(patch_size))
        self.num_spatial_ups = int(math.log2(spatial_compression)) - int(math.log2(patch_size))
        # 中文说明：检查运行时假设是否成立；代码：assert self.num_spatial_ups <= self.num_resolutions, f"Spatially upsample {self.num_resolutio...
        assert self.num_spatial_ups <= self.num_resolutions, f"Spatially upsample {self.num_resolutions} times at most"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_temporal_ups = int(math.log2(temporal_compression)) - int(math.log2(patch_size))
        self.num_temporal_ups = int(math.log2(temporal_compression)) - int(math.log2(patch_size))
        # 中文说明：检查运行时假设是否成立；代码：assert (
        assert (
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.num_temporal_ups <= self.num_resolutions
            self.num_temporal_ups <= self.num_resolutions
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"Temporally upsample {self.num_resolutions} times at most"
        ), f"Temporally upsample {self.num_resolutions} times at most"

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_in = channels * channels_mult[self.num_resolutions - 1]
        block_in = channels * channels_mult[self.num_resolutions - 1]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_res = (resolution // patch_size) // 2 ** (self.num_resolutions - 1)
        curr_res = (resolution // patch_size) // 2 ** (self.num_resolutions - 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.z_shape = (1, z_channels, curr_res, curr_res)
        self.z_shape = (1, z_channels, curr_res, curr_res)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：logging.info("Working with z of shape {} = {} dimensions.".format(self.z_shape, np.prod(self....
        logging.info("Working with z of shape {} = {} dimensions.".format(self.z_shape, np.prod(self.z_shape)))

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# z to block_in
        # z to block_in
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv_in = nn.Sequential(
        self.conv_in = nn.Sequential(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(z_channels, block_in, kernel_size=(1, 3, 3), stride=1, padding=1),
            CausalConv3d(z_channels, block_in, kernel_size=(1, 3, 3), stride=1, padding=1),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(block_in, block_in, kernel_size=(3, 1, 1), stride=1, padding=0),
            CausalConv3d(block_in, block_in, kernel_size=(3, 1, 1), stride=1, padding=0),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# middle
        # middle
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid = nn.Module()
        self.mid = nn.Module()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid.block_1 = CausalResnetBlockFactorized3d(
        self.mid.block_1 = CausalResnetBlockFactorized3d(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=block_in,
            in_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=block_in,
            out_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=dropout,
            dropout=dropout,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=1,
            num_groups=1,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid.attn_1 = nn.Sequential(
        self.mid.attn_1 = nn.Sequential(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalAttnBlock(block_in, num_groups=1),
            CausalAttnBlock(block_in, num_groups=1),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalTemporalAttnBlock(block_in, num_groups=1),
            CausalTemporalAttnBlock(block_in, num_groups=1),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid.block_2 = CausalResnetBlockFactorized3d(
        self.mid.block_2 = CausalResnetBlockFactorized3d(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=block_in,
            in_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=block_in,
            out_channels=block_in,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=dropout,
            dropout=dropout,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=1,
            num_groups=1,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mid.spatial_up = CausalHybridUpsample3d(block_in, spatial_up=True, temporal_up=False)
        self.mid.spatial_up = CausalHybridUpsample3d(block_in, spatial_up=True, temporal_up=False)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：legacy_mode = ignore_kwargs.get("legacy_mode", False)
        legacy_mode = ignore_kwargs.get("legacy_mode", False)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# upsampling
        # upsampling
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.up = nn.ModuleList()
        self.up = nn.ModuleList()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i_level in reversed(range(self.num_resolutions)):
        for i_level in reversed(range(self.num_resolutions)):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block = nn.ModuleList()
            block = nn.ModuleList()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn = nn.ModuleList()
            attn = nn.ModuleList()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_out = channels * channels_mult[i_level]
            block_out = channels * channels_mult[i_level]
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _ in range(self.num_res_blocks + 1):
            for _ in range(self.num_res_blocks + 1):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：block.append(
                block.append(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalResnetBlockFactorized3d(
                    CausalResnetBlockFactorized3d(
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=block_in,
                        in_channels=block_in,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=block_out,
                        out_channels=block_out,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=dropout,
                        dropout=dropout,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=1,
                        num_groups=1,
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_in = block_out
                block_in = block_out
                # 中文说明：根据条件选择执行分支；代码：if curr_res in attn_resolutions:
                if curr_res in attn_resolutions:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：attn.append(
                    attn.append(
                        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.Sequential(
                        nn.Sequential(
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalAttnBlock(block_in, num_groups=1),
                            CausalAttnBlock(block_in, num_groups=1),
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalTemporalAttnBlock(block_in, num_groups=1),
                            CausalTemporalAttnBlock(block_in, num_groups=1),
                        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                        )
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：up = nn.Module()
            up = nn.Module()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：up.block = block
            up.block = block
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：up.attn = attn
            up.attn = attn
            # 中文说明：根据条件选择执行分支；代码：if i_level != 0:
            if i_level != 0:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# The layer index for temporal/spatial downsampling performed
                # The layer index for temporal/spatial downsampling performed
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# in the encoder should correspond to the layer index in
                # in the encoder should correspond to the layer index in
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# reverse order where upsampling is performed in the decoder.
                # reverse order where upsampling is performed in the decoder.
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# If you've a pre-trained model, you can simply finetune.
                # If you've a pre-trained model, you can simply finetune.
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：i_level_reverse = self.num_resolutions - i_level - 1
                i_level_reverse = self.num_resolutions - i_level - 1
                # 中文说明：根据条件选择执行分支；代码：if legacy_mode:
                if legacy_mode:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_up = i_level_reverse < self.num_temporal_ups
                    temporal_up = i_level_reverse < self.num_temporal_ups
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_up = 0 < i_level_reverse < self.num_temporal_ups + 1
                    temporal_up = 0 < i_level_reverse < self.num_temporal_ups + 1
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：spatial_up = temporal_up or (
                spatial_up = temporal_up or (
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：i_level_reverse < self.num_spatial_ups and self.num_spatial_ups > self.num_temporal_ups
                    i_level_reverse < self.num_spatial_ups and self.num_spatial_ups > self.num_temporal_ups
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：up.upsample = CausalHybridUpsample3d(block_in, spatial_up=spatial_up, temporal_up=temporal_up)
                up.upsample = CausalHybridUpsample3d(block_in, spatial_up=spatial_up, temporal_up=temporal_up)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_res = curr_res * 2
                curr_res = curr_res * 2
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.up.insert(0, up) # prepend to get consistent order
            self.up.insert(0, up)  # prepend to get consistent order

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# end
        # end
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.norm_out = CausalNormalize(block_in, num_groups=1)
        self.norm_out = CausalNormalize(block_in, num_groups=1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv_out = nn.Sequential(
        self.conv_out = nn.Sequential(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(block_in, out_ch, kernel_size=(1, 3, 3), stride=1, padding=1),
            CausalConv3d(block_in, out_ch, kernel_size=(1, 3, 3), stride=1, padding=1),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(out_ch, out_ch, kernel_size=(3, 1, 1), stride=1, padding=0),
            CausalConv3d(out_ch, out_ch, kernel_size=(3, 1, 1), stride=1, padding=0),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, encoded_video, z):
    def forward(self, encoded_video, z):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z = self.conv_in(z)
        z = self.conv_in(z)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z = torch.repeat_interleave(z, int(encoded_video.shape[-2]), dim=-2)
        z = torch.repeat_interleave(z, int(encoded_video.shape[-2]), dim=-2)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z = torch.repeat_interleave(z, int(encoded_video.shape[-1]), dim=-1)
        z = torch.repeat_interleave(z, int(encoded_video.shape[-1]), dim=-1)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = torch.cat((encoded_video[:, :, :1], z), dim=2)
        h = torch.cat((encoded_video[:, :, :1], z), dim=2)
        
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# middle block.
        # middle block.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.mid.block_1(h)
        h = self.mid.block_1(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.mid.attn_1(h)
        h = self.mid.attn_1(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.mid.block_2(h)
        h = self.mid.block_2(h)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mid_h = self.mid.spatial_up(h)
        mid_h = self.mid.spatial_up(h)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# decoder blocks.
        # decoder blocks.
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i_level in reversed(range(self.num_resolutions)):
        for i_level in reversed(range(self.num_resolutions)):
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i_block in range(self.num_res_blocks + 1):
            for i_block in range(self.num_res_blocks + 1):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.up[i_level].block[i_block](h)
                h = self.up[i_level].block[i_block](h)
                # 中文说明：根据条件选择执行分支；代码：if len(self.up[i_level].attn) > 0:
                if len(self.up[i_level].attn) > 0:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.up[i_level].attn[i_block](h)
                    h = self.up[i_level].attn[i_block](h)
            # 中文说明：根据条件选择执行分支；代码：if i_level != 0:
            if i_level != 0:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.up[i_level].upsample(h)
                h = self.up[i_level].upsample(h)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.norm_out(h)
        h = self.norm_out(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = nonlinearity(h)
        h = nonlinearity(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.conv_out(h)
        h = self.conv_out(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.unpatcher3d(h)
        h = self.unpatcher3d(h)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return h, mid_h
        return h, mid_h