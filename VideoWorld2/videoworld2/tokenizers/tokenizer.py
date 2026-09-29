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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from contextlib import nullcontext
from contextlib import nullcontext

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.nn as nn
import torch.nn as nn
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.nn.functional as F
import torch.nn.functional as F
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from einops import rearrange
from einops import rearrange

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.tokenizers.interface import VideoTokenizerInterface
from videoworld2.tokenizers.interface import VideoTokenizerInterface
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.distributed import broadcast, get_rank, sync_model_states
from imaginaire.utils.distributed import broadcast, get_rank, sync_model_states
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io import easy_io
from imaginaire.utils.easy_io import easy_io

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：__all__ = [
__all__ = [
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："VAE",
    "VAE",
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
]

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：CACHE_T = 2
CACHE_T = 2


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class CausalConv3d(nn.Conv3d):
class CausalConv3d(nn.Conv3d):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Causal 3d convolusion.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, *args, **kwargs):
    def __init__(self, *args, **kwargs):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._padding = (self.padding[2], self.padding[2], self.padding[1], self.padding[1], 2 * self...
        self._padding = (self.padding[2], self.padding[2], self.padding[1], self.padding[1], 2 * self.padding[0], 0)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.padding = (0, 0, 0)
        self.padding = (0, 0, 0)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x, cache_x=None):
    def forward(self, x, cache_x=None):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding = list(self._padding)
        padding = list(self._padding)
        # 中文说明：根据条件选择执行分支；代码：if cache_x is not None and self._padding[4] > 0:
        if cache_x is not None and self._padding[4] > 0:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_x = cache_x.to(x.device)
            cache_x = cache_x.to(x.device)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = torch.cat([cache_x, x], dim=2)
            x = torch.cat([cache_x, x], dim=2)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding[4] -= cache_x.shape[2]
            padding[4] -= cache_x.shape[2]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = F.pad(x, padding)
        x = F.pad(x, padding)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return super().forward(x)
        return super().forward(x)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class RMS_norm(nn.Module):
class RMS_norm(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, dim, channel_first=True, images=True, bias=False):
    def __init__(self, dim, channel_first=True, images=True, bias=False):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：broadcastable_dims = (1, 1, 1) if not images else (1, 1)
        broadcastable_dims = (1, 1, 1) if not images else (1, 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：shape = (dim, *broadcastable_dims) if channel_first else (dim,)
        shape = (dim, *broadcastable_dims) if channel_first else (dim,)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.channel_first = channel_first
        self.channel_first = channel_first
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.scale = dim**0.5
        self.scale = dim**0.5
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.gamma = nn.Parameter(torch.ones(shape))
        self.gamma = nn.Parameter(torch.ones(shape))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.bias = nn.Parameter(torch.zeros(shape)) if bias else 0.0
        self.bias = nn.Parameter(torch.zeros(shape)) if bias else 0.0

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x):
    def forward(self, x):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return F.normalize(x, dim=(1 if self.channel_first else -1)) * self.scale * self.gamma + self...
        return F.normalize(x, dim=(1 if self.channel_first else -1)) * self.scale * self.gamma + self.bias


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Upsample(nn.Upsample):
class Upsample(nn.Upsample):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x):
    def forward(self, x):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Fix bfloat16 support for nearest neighbor interpolation.
        """
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return super().forward(x.float()).type_as(x)
        return super().forward(x.float()).type_as(x)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Resample(nn.Module):
class Resample(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, dim, mode):
    def __init__(self, dim, mode):
        # 中文说明：检查运行时假设是否成立；代码：assert mode in ("none", "upsample2d", "upsample3d", "downsample2d", "downsample3d")
        assert mode in ("none", "upsample2d", "upsample3d", "downsample2d", "downsample3d")
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dim = dim
        self.dim = dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mode = mode
        self.mode = mode

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# layers
        # layers
        # 中文说明：根据条件选择执行分支；代码：if mode == "upsample2d":
        if mode == "upsample2d":
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.resample = nn.Sequential(
            self.resample = nn.Sequential(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：Upsample(scale_factor=(2.0, 2.0), mode="nearest-exact"), nn.Conv2d(dim, dim // 2, 3, padding=1)
                Upsample(scale_factor=(2.0, 2.0), mode="nearest-exact"), nn.Conv2d(dim, dim // 2, 3, padding=1)
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：根据条件选择执行分支；代码：elif mode == "upsample3d":
        elif mode == "upsample3d":
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.resample = nn.Sequential(
            self.resample = nn.Sequential(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：Upsample(scale_factor=(2.0, 2.0), mode="nearest-exact"), nn.Conv2d(dim, dim // 2, 3, padding=1)
                Upsample(scale_factor=(2.0, 2.0), mode="nearest-exact"), nn.Conv2d(dim, dim // 2, 3, padding=1)
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.time_conv = CausalConv3d(dim, dim * 2, (3, 1, 1), padding=(1, 0, 0))
            self.time_conv = CausalConv3d(dim, dim * 2, (3, 1, 1), padding=(1, 0, 0))

        # 中文说明：根据条件选择执行分支；代码：elif mode == "downsample2d":
        elif mode == "downsample2d":
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.resample = nn.Sequential(nn.ZeroPad2d((0, 1, 0, 1)), nn.Conv2d(dim, dim, 3, stride=(2, 2)))
            self.resample = nn.Sequential(nn.ZeroPad2d((0, 1, 0, 1)), nn.Conv2d(dim, dim, 3, stride=(2, 2)))
        # 中文说明：根据条件选择执行分支；代码：elif mode == "downsample3d":
        elif mode == "downsample3d":
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.resample = nn.Sequential(nn.ZeroPad2d((0, 1, 0, 1)), nn.Conv2d(dim, dim, 3, stride=(2, 2)))
            self.resample = nn.Sequential(nn.ZeroPad2d((0, 1, 0, 1)), nn.Conv2d(dim, dim, 3, stride=(2, 2)))
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.time_conv = CausalConv3d(dim, dim, (3, 1, 1), stride=(2, 1, 1), padding=(0, 0, 0))
            self.time_conv = CausalConv3d(dim, dim, (3, 1, 1), stride=(2, 1, 1), padding=(0, 0, 0))

        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.resample = nn.Identity()
            self.resample = nn.Identity()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x, feat_cache=None, feat_idx=[0]):
    def forward(self, x, feat_cache=None, feat_idx=[0]):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：b, c, t, h, w = x.size()
        b, c, t, h, w = x.size()
        # 中文说明：根据条件选择执行分支；代码：if self.mode == "upsample3d":
        if self.mode == "upsample3d":
            # 中文说明：根据条件选择执行分支；代码：if feat_cache is not None:
            if feat_cache is not None:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：idx = feat_idx[0]
                idx = feat_idx[0]
                # 中文说明：根据条件选择执行分支；代码：if feat_cache[idx] is None:
                if feat_cache[idx] is None:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：feat_cache[idx] = "Rep"
                    feat_cache[idx] = "Rep"
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：feat_idx[0] += 1
                    feat_idx[0] += 1
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_x = x[:, :, -CACHE_T:, :, :].clone()
                    cache_x = x[:, :, -CACHE_T:, :, :].clone()
                    # 中文说明：根据条件选择执行分支；代码：if cache_x.shape[2] < 2 and feat_cache[idx] is not None and feat_cache[idx] != "Rep":
                    if cache_x.shape[2] < 2 and feat_cache[idx] is not None and feat_cache[idx] != "Rep":
                        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# cache last frame of last two chunk
                        # cache last frame of last two chunk
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_x = torch.cat(
                        cache_x = torch.cat(
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：[feat_cache[idx][:, :, -1, :, :].unsqueeze(2).to(cache_x.device), cache_x], dim=2
                            [feat_cache[idx][:, :, -1, :, :].unsqueeze(2).to(cache_x.device), cache_x], dim=2
                        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                        )
                    # 中文说明：根据条件选择执行分支；代码：if cache_x.shape[2] < 2 and feat_cache[idx] is not None and feat_cache[idx] == "Rep":
                    if cache_x.shape[2] < 2 and feat_cache[idx] is not None and feat_cache[idx] == "Rep":
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_x = torch.cat([torch.zeros_like(cache_x).to(cache_x.device), cache_x], dim=2)
                        cache_x = torch.cat([torch.zeros_like(cache_x).to(cache_x.device), cache_x], dim=2)
                    # 中文说明：根据条件选择执行分支；代码：if feat_cache[idx] == "Rep":
                    if feat_cache[idx] == "Rep":
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.time_conv(x)
                        x = self.time_conv(x)
                    # 中文说明：根据条件选择执行分支；代码：else:
                    else:
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.time_conv(x, feat_cache[idx])
                        x = self.time_conv(x, feat_cache[idx])
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：feat_cache[idx] = cache_x
                    feat_cache[idx] = cache_x
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：feat_idx[0] += 1
                    feat_idx[0] += 1

                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = x.reshape(b, 2, c, t, h, w)
                    x = x.reshape(b, 2, c, t, h, w)
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = torch.stack((x[:, 0, :, :, :, :], x[:, 1, :, :, :, :]), 3)
                    x = torch.stack((x[:, 0, :, :, :, :], x[:, 1, :, :, :, :]), 3)
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = x.reshape(b, c, t * 2, h, w)
                    x = x.reshape(b, c, t * 2, h, w)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t = x.shape[2]
        t = x.shape[2]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = rearrange(x, "b c t h w -> (b t) c h w")
        x = rearrange(x, "b c t h w -> (b t) c h w")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.resample(x)
        x = self.resample(x)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = rearrange(x, "(b t) c h w -> b c t h w", t=t)
        x = rearrange(x, "(b t) c h w -> b c t h w", t=t)

        # 中文说明：根据条件选择执行分支；代码：if self.mode == "downsample3d":
        if self.mode == "downsample3d":
            # 中文说明：根据条件选择执行分支；代码：if feat_cache is not None:
            if feat_cache is not None:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：idx = feat_idx[0]
                idx = feat_idx[0]
                # 中文说明：根据条件选择执行分支；代码：if feat_cache[idx] is None:
                if feat_cache[idx] is None:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：feat_cache[idx] = x.clone()
                    feat_cache[idx] = x.clone()
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：feat_idx[0] += 1
                    feat_idx[0] += 1
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_x = x[:, :, -1:, :, :].clone()
                    cache_x = x[:, :, -1:, :, :].clone()
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# if cache_x.shape[2] < 2 and feat_cache[idx] is not None and feat_cache[idx]!='Rep':
                    # if cache_x.shape[2] < 2 and feat_cache[idx] is not None and feat_cache[idx]!='Rep':
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# # cache last frame of last two chunk
                    #     # cache last frame of last two chunk
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# cache_x = torch.cat([feat_cache[idx][:, :, -1, :, :].unsqueeze(2).to(cache_x.device), cache...
                    #     cache_x = torch.cat([feat_cache[idx][:, :, -1, :, :].unsqueeze(2).to(cache_x.device), cache_x], dim=2)

                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.time_conv(torch.cat([feat_cache[idx][:, :, -1:, :, :], x], 2))
                    x = self.time_conv(torch.cat([feat_cache[idx][:, :, -1:, :, :], x], 2))
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：feat_cache[idx] = cache_x
                    feat_cache[idx] = cache_x
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：feat_idx[0] += 1
                    feat_idx[0] += 1
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x
        return x


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ResidualBlock(nn.Module):
class ResidualBlock(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, in_dim, out_dim, dropout=0.0):
    def __init__(self, in_dim, out_dim, dropout=0.0):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.in_dim = in_dim
        self.in_dim = in_dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.out_dim = out_dim
        self.out_dim = out_dim

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# layers
        # layers
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.residual = nn.Sequential(
        self.residual = nn.Sequential(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：RMS_norm(in_dim, images=False),
            RMS_norm(in_dim, images=False),
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.SiLU(),
            nn.SiLU(),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(in_dim, out_dim, 3, padding=1),
            CausalConv3d(in_dim, out_dim, 3, padding=1),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：RMS_norm(out_dim, images=False),
            RMS_norm(out_dim, images=False),
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.SiLU(),
            nn.SiLU(),
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.Dropout(dropout),
            nn.Dropout(dropout),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CausalConv3d(out_dim, out_dim, 3, padding=1),
            CausalConv3d(out_dim, out_dim, 3, padding=1),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.shortcut = CausalConv3d(in_dim, out_dim, 1) if in_dim != out_dim else nn.Identity()
        self.shortcut = CausalConv3d(in_dim, out_dim, 1) if in_dim != out_dim else nn.Identity()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x, feat_cache=None, feat_idx=[0]):
    def forward(self, x, feat_cache=None, feat_idx=[0]):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.shortcut(x)
        h = self.shortcut(x)
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for layer in self.residual:
        for layer in self.residual:
            # 中文说明：根据条件选择执行分支；代码：if isinstance(layer, CausalConv3d) and feat_cache is not None:
            if isinstance(layer, CausalConv3d) and feat_cache is not None:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：idx = feat_idx[0]
                idx = feat_idx[0]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_x = x[:, :, -CACHE_T:, :, :].clone()
                cache_x = x[:, :, -CACHE_T:, :, :].clone()
                # 中文说明：根据条件选择执行分支；代码：if cache_x.shape[2] < 2 and feat_cache[idx] is not None:
                if cache_x.shape[2] < 2 and feat_cache[idx] is not None:
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# cache last frame of last two chunk
                    # cache last frame of last two chunk
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_x = torch.cat(
                    cache_x = torch.cat(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：[feat_cache[idx][:, :, -1, :, :].unsqueeze(2).to(cache_x.device), cache_x], dim=2
                        [feat_cache[idx][:, :, -1, :, :].unsqueeze(2).to(cache_x.device), cache_x], dim=2
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = layer(x, feat_cache[idx])
                x = layer(x, feat_cache[idx])
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：feat_cache[idx] = cache_x
                feat_cache[idx] = cache_x
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：feat_idx[0] += 1
                feat_idx[0] += 1
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = layer(x)
                x = layer(x)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x + h
        return x + h


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class AttentionBlock(nn.Module):
class AttentionBlock(nn.Module):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Causal self-attention with a single head.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, dim):
    def __init__(self, dim):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dim = dim
        self.dim = dim

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# layers
        # layers
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.norm = RMS_norm(dim)
        self.norm = RMS_norm(dim)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.to_qkv = nn.Conv2d(dim, dim * 3, 1)
        self.to_qkv = nn.Conv2d(dim, dim * 3, 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.proj = nn.Conv2d(dim, dim, 1)
        self.proj = nn.Conv2d(dim, dim, 1)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# zero out the last layer params
        # zero out the last layer params
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.init.zeros_(self.proj.weight)
        nn.init.zeros_(self.proj.weight)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x):
    def forward(self, x):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：identity = x
        identity = x
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：b, c, t, h, w = x.size()
        b, c, t, h, w = x.size()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = rearrange(x, "b c t h w -> (b t) c h w")
        x = rearrange(x, "b c t h w -> (b t) c h w")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.norm(x)
        x = self.norm(x)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# compute query, key, value
        # compute query, key, value
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q, k, v = self.to_qkv(x).reshape(b * t, 1, c * 3, -1).permute(0, 1, 3, 2).contiguous().chunk(...
        q, k, v = self.to_qkv(x).reshape(b * t, 1, c * 3, -1).permute(0, 1, 3, 2).contiguous().chunk(3, dim=-1)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# apply attention
        # apply attention
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = F.scaled_dot_product_attention(
        x = F.scaled_dot_product_attention(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q,
            q,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k,
            k,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v,
            v,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = x.squeeze(1).permute(0, 2, 1).reshape(b * t, c, h, w)
        x = x.squeeze(1).permute(0, 2, 1).reshape(b * t, c, h, w)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# output
        # output
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.proj(x)
        x = self.proj(x)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = rearrange(x, "(b t) c h w-> b c t h w", t=t)
        x = rearrange(x, "(b t) c h w-> b c t h w", t=t)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x + identity
        return x + identity


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Encoder3d(nn.Module):
class Encoder3d(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dim=128,
        dim=128,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_dim=4,
        z_dim=4,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dim_mult=[1, 2, 4, 4],
        dim_mult=[1, 2, 4, 4],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_res_blocks=2,
        num_res_blocks=2,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn_scales=[],
        attn_scales=[],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temperal_downsample=[True, True, False],
        temperal_downsample=[True, True, False],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=0.0,
        dropout=0.0,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dim = dim
        self.dim = dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.z_dim = z_dim
        self.z_dim = z_dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dim_mult = dim_mult
        self.dim_mult = dim_mult
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_res_blocks = num_res_blocks
        self.num_res_blocks = num_res_blocks
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.attn_scales = attn_scales
        self.attn_scales = attn_scales
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.temperal_downsample = temperal_downsample
        self.temperal_downsample = temperal_downsample

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# dimensions
        # dimensions
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dims = [dim * u for u in [1] + dim_mult]
        dims = [dim * u for u in [1] + dim_mult]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scale = 1.0
        scale = 1.0

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# init block
        # init block
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv1 = CausalConv3d(3, dims[0], 3, padding=1)
        self.conv1 = CausalConv3d(3, dims[0], 3, padding=1)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# downsample blocks
        # downsample blocks
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：downsamples = []
        downsamples = []
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i, (in_dim, out_dim) in enumerate(zip(dims[:-1], dims[1:])):
        for i, (in_dim, out_dim) in enumerate(zip(dims[:-1], dims[1:])):
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# residual (+attention) blocks
            # residual (+attention) blocks
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _ in range(num_res_blocks):
            for _ in range(num_res_blocks):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：downsamples.append(ResidualBlock(in_dim, out_dim, dropout))
                downsamples.append(ResidualBlock(in_dim, out_dim, dropout))
                # 中文说明：根据条件选择执行分支；代码：if scale in attn_scales:
                if scale in attn_scales:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：downsamples.append(AttentionBlock(out_dim))
                    downsamples.append(AttentionBlock(out_dim))
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_dim = out_dim
                in_dim = out_dim

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# downsample block
            # downsample block
            # 中文说明：根据条件选择执行分支；代码：if i != len(dim_mult) - 1:
            if i != len(dim_mult) - 1:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mode = "downsample3d" if temperal_downsample[i] else "downsample2d"
                mode = "downsample3d" if temperal_downsample[i] else "downsample2d"
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：downsamples.append(Resample(out_dim, mode=mode))
                downsamples.append(Resample(out_dim, mode=mode))
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scale /= 2.0
                scale /= 2.0
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.downsamples = nn.Sequential(*downsamples)
        self.downsamples = nn.Sequential(*downsamples)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# middle blocks
        # middle blocks
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.middle = nn.Sequential(
        self.middle = nn.Sequential(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ResidualBlock(out_dim, out_dim, dropout), AttentionBlock(out_dim), ResidualBlock(out_dim, out...
            ResidualBlock(out_dim, out_dim, dropout), AttentionBlock(out_dim), ResidualBlock(out_dim, out_dim, dropout)
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# output blocks
        # output blocks
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.head = nn.Sequential(
        self.head = nn.Sequential(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：RMS_norm(out_dim, images=False), nn.SiLU(), CausalConv3d(out_dim, z_dim, 3, padding=1)
            RMS_norm(out_dim, images=False), nn.SiLU(), CausalConv3d(out_dim, z_dim, 3, padding=1)
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x, feat_cache=None, feat_idx=[0]):
    def forward(self, x, feat_cache=None, feat_idx=[0]):
        # 中文说明：根据条件选择执行分支；代码：if feat_cache is not None:
        if feat_cache is not None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：idx = feat_idx[0]
            idx = feat_idx[0]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_x = x[:, :, -CACHE_T:, :, :].clone()
            cache_x = x[:, :, -CACHE_T:, :, :].clone()
            # 中文说明：根据条件选择执行分支；代码：if cache_x.shape[2] < 2 and feat_cache[idx] is not None:
            if cache_x.shape[2] < 2 and feat_cache[idx] is not None:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# cache last frame of last two chunk
                # cache last frame of last two chunk
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_x = torch.cat([feat_cache[idx][:, :, -1, :, :].unsqueeze(2).to(cache_x.device), cache_x...
                cache_x = torch.cat([feat_cache[idx][:, :, -1, :, :].unsqueeze(2).to(cache_x.device), cache_x], dim=2)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.conv1(x, feat_cache[idx])
            x = self.conv1(x, feat_cache[idx])
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：feat_cache[idx] = cache_x
            feat_cache[idx] = cache_x
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：feat_idx[0] += 1
            feat_idx[0] += 1
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.conv1(x)
            x = self.conv1(x)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# downsamples
        # downsamples
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for layer in self.downsamples:
        for layer in self.downsamples:
            # 中文说明：根据条件选择执行分支；代码：if feat_cache is not None:
            if feat_cache is not None:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = layer(x, feat_cache, feat_idx)
                x = layer(x, feat_cache, feat_idx)
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = layer(x)
                x = layer(x)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# middle
        # middle
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for layer in self.middle:
        for layer in self.middle:
            # 中文说明：根据条件选择执行分支；代码：if isinstance(layer, ResidualBlock) and feat_cache is not None:
            if isinstance(layer, ResidualBlock) and feat_cache is not None:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = layer(x, feat_cache, feat_idx)
                x = layer(x, feat_cache, feat_idx)
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = layer(x)
                x = layer(x)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# head
        # head
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for layer in self.head:
        for layer in self.head:
            # 中文说明：根据条件选择执行分支；代码：if isinstance(layer, CausalConv3d) and feat_cache is not None:
            if isinstance(layer, CausalConv3d) and feat_cache is not None:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：idx = feat_idx[0]
                idx = feat_idx[0]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_x = x[:, :, -CACHE_T:, :, :].clone()
                cache_x = x[:, :, -CACHE_T:, :, :].clone()
                # 中文说明：根据条件选择执行分支；代码：if cache_x.shape[2] < 2 and feat_cache[idx] is not None:
                if cache_x.shape[2] < 2 and feat_cache[idx] is not None:
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# cache last frame of last two chunk
                    # cache last frame of last two chunk
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_x = torch.cat(
                    cache_x = torch.cat(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：[feat_cache[idx][:, :, -1, :, :].unsqueeze(2).to(cache_x.device), cache_x], dim=2
                        [feat_cache[idx][:, :, -1, :, :].unsqueeze(2).to(cache_x.device), cache_x], dim=2
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = layer(x, feat_cache[idx])
                x = layer(x, feat_cache[idx])
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：feat_cache[idx] = cache_x
                feat_cache[idx] = cache_x
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：feat_idx[0] += 1
                feat_idx[0] += 1
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = layer(x)
                x = layer(x)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x
        return x


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Decoder3d(nn.Module):
class Decoder3d(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dim=128,
        dim=128,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_dim=4,
        z_dim=4,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dim_mult=[1, 2, 4, 4],
        dim_mult=[1, 2, 4, 4],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_res_blocks=2,
        num_res_blocks=2,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn_scales=[],
        attn_scales=[],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temperal_upsample=[False, True, True],
        temperal_upsample=[False, True, True],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=0.0,
        dropout=0.0,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dim = dim
        self.dim = dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.z_dim = z_dim
        self.z_dim = z_dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dim_mult = dim_mult
        self.dim_mult = dim_mult
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_res_blocks = num_res_blocks
        self.num_res_blocks = num_res_blocks
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.attn_scales = attn_scales
        self.attn_scales = attn_scales
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.temperal_upsample = temperal_upsample
        self.temperal_upsample = temperal_upsample

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# dimensions
        # dimensions
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dims = [dim * u for u in [dim_mult[-1]] + dim_mult[::-1]]
        dims = [dim * u for u in [dim_mult[-1]] + dim_mult[::-1]]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scale = 1.0 / 2 ** (len(dim_mult) - 2)
        scale = 1.0 / 2 ** (len(dim_mult) - 2)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# init block
        # init block
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv1 = CausalConv3d(z_dim, dims[0], 3, padding=1)
        self.conv1 = CausalConv3d(z_dim, dims[0], 3, padding=1)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# middle blocks
        # middle blocks
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.middle = nn.Sequential(
        self.middle = nn.Sequential(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ResidualBlock(dims[0], dims[0], dropout), AttentionBlock(dims[0]), ResidualBlock(dims[0], dim...
            ResidualBlock(dims[0], dims[0], dropout), AttentionBlock(dims[0]), ResidualBlock(dims[0], dims[0], dropout)
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# upsample blocks
        # upsample blocks
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：upsamples = []
        upsamples = []
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i, (in_dim, out_dim) in enumerate(zip(dims[:-1], dims[1:])):
        for i, (in_dim, out_dim) in enumerate(zip(dims[:-1], dims[1:])):
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# residual (+attention) blocks
            # residual (+attention) blocks
            # 中文说明：根据条件选择执行分支；代码：if i == 1 or i == 2 or i == 3:
            if i == 1 or i == 2 or i == 3:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_dim = in_dim // 2
                in_dim = in_dim // 2
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _ in range(num_res_blocks + 1):
            for _ in range(num_res_blocks + 1):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：upsamples.append(ResidualBlock(in_dim, out_dim, dropout))
                upsamples.append(ResidualBlock(in_dim, out_dim, dropout))
                # 中文说明：根据条件选择执行分支；代码：if scale in attn_scales:
                if scale in attn_scales:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：upsamples.append(AttentionBlock(out_dim))
                    upsamples.append(AttentionBlock(out_dim))
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_dim = out_dim
                in_dim = out_dim

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# upsample block
            # upsample block
            # 中文说明：根据条件选择执行分支；代码：if i != len(dim_mult) - 1:
            if i != len(dim_mult) - 1:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mode = "upsample3d" if temperal_upsample[i] else "upsample2d"
                mode = "upsample3d" if temperal_upsample[i] else "upsample2d"
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：upsamples.append(Resample(out_dim, mode=mode))
                upsamples.append(Resample(out_dim, mode=mode))
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scale *= 2.0
                scale *= 2.0
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.upsamples = nn.Sequential(*upsamples)
        self.upsamples = nn.Sequential(*upsamples)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# output blocks
        # output blocks
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.head = nn.Sequential(RMS_norm(out_dim, images=False), nn.SiLU(), CausalConv3d(out_dim, 3...
        self.head = nn.Sequential(RMS_norm(out_dim, images=False), nn.SiLU(), CausalConv3d(out_dim, 3, 3, padding=1))

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x, feat_cache=None, feat_idx=[0]):
    def forward(self, x, feat_cache=None, feat_idx=[0]):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# conv1
        # conv1
        # 中文说明：根据条件选择执行分支；代码：if feat_cache is not None:
        if feat_cache is not None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：idx = feat_idx[0]
            idx = feat_idx[0]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_x = x[:, :, -CACHE_T:, :, :].clone()
            cache_x = x[:, :, -CACHE_T:, :, :].clone()
            # 中文说明：根据条件选择执行分支；代码：if cache_x.shape[2] < 2 and feat_cache[idx] is not None:
            if cache_x.shape[2] < 2 and feat_cache[idx] is not None:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# cache last frame of last two chunk
                # cache last frame of last two chunk
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_x = torch.cat([feat_cache[idx][:, :, -1, :, :].unsqueeze(2).to(cache_x.device), cache_x...
                cache_x = torch.cat([feat_cache[idx][:, :, -1, :, :].unsqueeze(2).to(cache_x.device), cache_x], dim=2)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.conv1(x, feat_cache[idx])
            x = self.conv1(x, feat_cache[idx])
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：feat_cache[idx] = cache_x
            feat_cache[idx] = cache_x
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：feat_idx[0] += 1
            feat_idx[0] += 1
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.conv1(x)
            x = self.conv1(x)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# middle
        # middle
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for layer in self.middle:
        for layer in self.middle:
            # 中文说明：根据条件选择执行分支；代码：if isinstance(layer, ResidualBlock) and feat_cache is not None:
            if isinstance(layer, ResidualBlock) and feat_cache is not None:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = layer(x, feat_cache, feat_idx)
                x = layer(x, feat_cache, feat_idx)
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = layer(x)
                x = layer(x)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# upsamples
        # upsamples
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for layer in self.upsamples:
        for layer in self.upsamples:
            # 中文说明：根据条件选择执行分支；代码：if feat_cache is not None:
            if feat_cache is not None:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = layer(x, feat_cache, feat_idx)
                x = layer(x, feat_cache, feat_idx)
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = layer(x)
                x = layer(x)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# head
        # head
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for layer in self.head:
        for layer in self.head:
            # 中文说明：根据条件选择执行分支；代码：if isinstance(layer, CausalConv3d) and feat_cache is not None:
            if isinstance(layer, CausalConv3d) and feat_cache is not None:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：idx = feat_idx[0]
                idx = feat_idx[0]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_x = x[:, :, -CACHE_T:, :, :].clone()
                cache_x = x[:, :, -CACHE_T:, :, :].clone()
                # 中文说明：根据条件选择执行分支；代码：if cache_x.shape[2] < 2 and feat_cache[idx] is not None:
                if cache_x.shape[2] < 2 and feat_cache[idx] is not None:
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# cache last frame of last two chunk
                    # cache last frame of last two chunk
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_x = torch.cat(
                    cache_x = torch.cat(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：[feat_cache[idx][:, :, -1, :, :].unsqueeze(2).to(cache_x.device), cache_x], dim=2
                        [feat_cache[idx][:, :, -1, :, :].unsqueeze(2).to(cache_x.device), cache_x], dim=2
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = layer(x, feat_cache[idx])
                x = layer(x, feat_cache[idx])
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：feat_cache[idx] = cache_x
                feat_cache[idx] = cache_x
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：feat_idx[0] += 1
                feat_idx[0] += 1
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = layer(x)
                x = layer(x)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x
        return x


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def count_conv3d(model):
def count_conv3d(model):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：count = 0
    count = 0
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for m in model.modules():
    for m in model.modules():
        # 中文说明：根据条件选择执行分支；代码：if isinstance(m, CausalConv3d):
        if isinstance(m, CausalConv3d):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：count += 1
            count += 1
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return count
    return count


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class VAE_(nn.Module):
class VAE_(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dim=128,
        dim=128,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_dim=4,
        z_dim=4,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dim_mult=[1, 2, 4, 4],
        dim_mult=[1, 2, 4, 4],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_res_blocks=2,
        num_res_blocks=2,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn_scales=[],
        attn_scales=[],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temperal_downsample=[True, True, False],
        temperal_downsample=[True, True, False],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=0.0,
        dropout=0.0,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_window=4,
        temporal_window=4,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dim = dim
        self.dim = dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.z_dim = z_dim
        self.z_dim = z_dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dim_mult = dim_mult
        self.dim_mult = dim_mult
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_res_blocks = num_res_blocks
        self.num_res_blocks = num_res_blocks
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.attn_scales = attn_scales
        self.attn_scales = attn_scales
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.temperal_downsample = temperal_downsample
        self.temperal_downsample = temperal_downsample
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.temperal_upsample = temperal_downsample[::-1]
        self.temperal_upsample = temperal_downsample[::-1]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.temporal_window = temporal_window
        self.temporal_window = temporal_window
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# modules
        # modules
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.encoder = Encoder3d(
        self.encoder = Encoder3d(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dim, z_dim * 2, dim_mult, num_res_blocks, attn_scales, self.temperal_downsample, dropout
            dim, z_dim * 2, dim_mult, num_res_blocks, attn_scales, self.temperal_downsample, dropout
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv1 = CausalConv3d(z_dim * 2, z_dim * 2, 1)
        self.conv1 = CausalConv3d(z_dim * 2, z_dim * 2, 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conv2 = CausalConv3d(z_dim, z_dim, 1)
        self.conv2 = CausalConv3d(z_dim, z_dim, 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.decoder = Decoder3d(dim, z_dim, dim_mult, num_res_blocks, attn_scales, self.temperal_ups...
        self.decoder = Decoder3d(dim, z_dim, dim_mult, num_res_blocks, attn_scales, self.temperal_upsample, dropout)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x):
    def forward(self, x):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：mu, log_var = self.encode(x)
        mu, log_var = self.encode(x)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z = self.reparameterize(mu, log_var)
        z = self.reparameterize(mu, log_var)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_recon = self.decode(z)
        x_recon = self.decode(z)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x_recon, mu, log_var
        return x_recon, mu, log_var

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def encode(self, x, scale):
    def encode(self, x, scale):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.clear_cache()
        self.clear_cache()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# cache
        # cache
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t = x.shape[2]
        t = x.shape[2]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iter_ = 1 + (t - 1) // self.temporal_window
        iter_ = 1 + (t - 1) // self.temporal_window
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i in range(iter_):
        for i in range(iter_):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._enc_conv_idx = [0]
            self._enc_conv_idx = [0]
            # 中文说明：根据条件选择执行分支；代码：if i == 0:
            if i == 0:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out = self.encoder(x[:, :, :1, :, :], feat_cache=self._enc_feat_map, feat_idx=self._enc_conv_...
                out = self.encoder(x[:, :, :1, :, :], feat_cache=self._enc_feat_map, feat_idx=self._enc_conv_idx)
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_ = self.encoder(
                out_ = self.encoder(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x[:, :, 1 + self.temporal_window * (i - 1) : 1 + self.temporal_window * i, :, :],
                    x[:, :, 1 + self.temporal_window * (i - 1) : 1 + self.temporal_window * i, :, :],
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：feat_cache=self._enc_feat_map,
                    feat_cache=self._enc_feat_map,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：feat_idx=self._enc_conv_idx,
                    feat_idx=self._enc_conv_idx,
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out = torch.cat([out, out_], 2)
                out = torch.cat([out, out_], 2)
        # 中文说明：根据条件选择执行分支；代码：if (t - 1) % self.temporal_window:
        if (t - 1) % self.temporal_window:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._enc_conv_idx = [0]
            self._enc_conv_idx = [0]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_ = self.encoder(
            out_ = self.encoder(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x[:, :, 1 + self.temporal_window * (iter_ - 1) :, :, :],
                x[:, :, 1 + self.temporal_window * (iter_ - 1) :, :, :],
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：feat_cache=self._enc_feat_map,
                feat_cache=self._enc_feat_map,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：feat_idx=self._enc_conv_idx,
                feat_idx=self._enc_conv_idx,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out = torch.cat([out, out_], 2)
            out = torch.cat([out, out_], 2)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：mu, log_var = self.conv1(out).chunk(2, dim=1)
        mu, log_var = self.conv1(out).chunk(2, dim=1)
        # 中文说明：根据条件选择执行分支；代码：if isinstance(scale[0], torch.Tensor):
        if isinstance(scale[0], torch.Tensor):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mu = (mu - scale[0].view(1, self.z_dim, 1, 1, 1)) * scale[1].view(1, self.z_dim, 1, 1, 1)
            mu = (mu - scale[0].view(1, self.z_dim, 1, 1, 1)) * scale[1].view(1, self.z_dim, 1, 1, 1)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mu = (mu - scale[0]) * scale[1]
            mu = (mu - scale[0]) * scale[1]
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.clear_cache()
        self.clear_cache()
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return mu
        return mu

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def decode(self, z, scale):
    def decode(self, z, scale):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.clear_cache()
        self.clear_cache()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# z: [b,c,t,h,w]
        # z: [b,c,t,h,w]
        # 中文说明：根据条件选择执行分支；代码：if isinstance(scale[0], torch.Tensor):
        if isinstance(scale[0], torch.Tensor):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z = z / scale[1].view(1, self.z_dim, 1, 1, 1) + scale[0].view(1, self.z_dim, 1, 1, 1)
            z = z / scale[1].view(1, self.z_dim, 1, 1, 1) + scale[0].view(1, self.z_dim, 1, 1, 1)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z = z / scale[1] + scale[0]
            z = z / scale[1] + scale[0]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iter_ = z.shape[2]
        iter_ = z.shape[2]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.conv2(z)
        x = self.conv2(z)
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i in range(iter_):
        for i in range(iter_):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._conv_idx = [0]
            self._conv_idx = [0]
            # 中文说明：根据条件选择执行分支；代码：if i == 0:
            if i == 0:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out = self.decoder(x[:, :, i : i + 1, :, :], feat_cache=self._feat_map, feat_idx=self._conv_idx)
                out = self.decoder(x[:, :, i : i + 1, :, :], feat_cache=self._feat_map, feat_idx=self._conv_idx)
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_ = self.decoder(x[:, :, i : i + 1, :, :], feat_cache=self._feat_map, feat_idx=self._conv_...
                out_ = self.decoder(x[:, :, i : i + 1, :, :], feat_cache=self._feat_map, feat_idx=self._conv_idx)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out = torch.cat([out, out_], 2)
                out = torch.cat([out, out_], 2)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.clear_cache()
        self.clear_cache()
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return out
        return out

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def reparameterize(self, mu, log_var):
    def reparameterize(self, mu, log_var):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：std = torch.exp(0.5 * log_var)
        std = torch.exp(0.5 * log_var)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：eps = torch.randn_like(std)
        eps = torch.randn_like(std)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return eps * std + mu
        return eps * std + mu

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def sample(self, imgs, deterministic=False):
    def sample(self, imgs, deterministic=False):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：mu, log_var = self.encode(imgs)
        mu, log_var = self.encode(imgs)
        # 中文说明：根据条件选择执行分支；代码：if deterministic:
        if deterministic:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return mu
            return mu
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：std = torch.exp(0.5 * log_var.clamp(-30.0, 20.0))
        std = torch.exp(0.5 * log_var.clamp(-30.0, 20.0))
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return mu + std * torch.randn_like(std)
        return mu + std * torch.randn_like(std)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def clear_cache(self):
    def clear_cache(self):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._conv_num = count_conv3d(self.decoder)
        self._conv_num = count_conv3d(self.decoder)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._conv_idx = [0]
        self._conv_idx = [0]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._feat_map = [None] * self._conv_num
        self._feat_map = [None] * self._conv_num
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# cache encode
        # cache encode
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._enc_conv_num = count_conv3d(self.encoder)
        self._enc_conv_num = count_conv3d(self.encoder)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._enc_conv_idx = [0]
        self._enc_conv_idx = [0]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._enc_feat_map = [None] * self._enc_conv_num
        self._enc_feat_map = [None] * self._enc_conv_num


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _video_vae(
def _video_vae(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pretrained_path=None,
    pretrained_path=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_dim=None,
    z_dim=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：device="cpu",
    device="cpu",
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：load_mean_std=False,
    load_mean_std=False,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：mean_std_path: str = "",
    mean_std_path: str = "",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**kwargs,
    **kwargs,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Autoencoder3d adapted from Stable Diffusion 1.x, 2.x and XL.
    """
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# params
    # params
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cfg = dict(
    cfg = dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dim=96,
        dim=96,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_dim=z_dim,
        z_dim=z_dim,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dim_mult=[1, 2, 4, 4],
        dim_mult=[1, 2, 4, 4],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_res_blocks=2,
        num_res_blocks=2,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn_scales=[],
        attn_scales=[],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temperal_downsample=[False, True, True],
        temperal_downsample=[False, True, True],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=0.0,
        dropout=0.0,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cfg.update(**kwargs)
    cfg.update(**kwargs)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# init model
    # init model
    # 中文说明：处理异常、清理资源或管理上下文；代码：with torch.device("meta"):
    with torch.device("meta"):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model = VAE_(**cfg)
        model = VAE_(**cfg)

    # 中文说明：根据条件选择执行分支；代码：if pretrained_path is None:
    if pretrained_path is None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model.to_empty(device=device)
        model.to_empty(device=device)
        # 中文说明：根据条件选择执行分支；代码：if load_mean_std:
        if load_mean_std:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：img_mean, img_std = torch.randn(1, 16, 1, 1, 1, device=device), torch.randn(1, 16, 1, 1, 1, d...
            img_mean, img_std = torch.randn(1, 16, 1, 1, 1, device=device), torch.randn(1, 16, 1, 1, 1, device=device)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video_mean, video_std = torch.randn(1, 16, 32, 1, 1, device=device), torch.randn(
            video_mean, video_std = torch.randn(1, 16, 32, 1, 1, device=device), torch.randn(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：1, 16, 32, 1, 1, device=device
                1, 16, 32, 1, 1, device=device
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：根据条件选择执行分支；代码：if get_rank() == 0:
        if get_rank() == 0:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ckpt = easy_io.load(
            ckpt = easy_io.load(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pretrained_path,
                pretrained_path,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_key=None,
                backend_key=None,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：map_location=device,
                map_location=device,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：根据条件选择执行分支；代码：if load_mean_std:
            if load_mean_std:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：img_mean_std = mean_std_path.replace("mean_std.pt", "images_mean_std.pt")
                img_mean_std = mean_std_path.replace("mean_std.pt", "images_mean_std.pt")
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_mean_std = mean_std_path.replace("mean_std.pt", "video_mean_std.pt")
                video_mean_std = mean_std_path.replace("mean_std.pt", "video_mean_std.pt")
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：img_mean, img_std = easy_io.load(img_mean_std, backend_key=backend_key, map_location=device)
                img_mean, img_std = easy_io.load(img_mean_std, backend_key=backend_key, map_location=device)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video_mean, video_std = easy_io.load(video_mean_std, backend_key=backend_key, map_location=de...
                video_mean, video_std = easy_io.load(video_mean_std, backend_key=backend_key, map_location=device)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：img_mean = img_mean.reshape(1, 16, 1, 1, 1)
                img_mean = img_mean.reshape(1, 16, 1, 1, 1)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：img_std = img_std.reshape(1, 16, 1, 1, 1)
                img_std = img_std.reshape(1, 16, 1, 1, 1)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_mean = video_mean.reshape(1, 16, 32, 1, 1)
                video_mean = video_mean.reshape(1, 16, 32, 1, 1)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_std = video_std.reshape(1, 16, 32, 1, 1)
                video_std = video_std.reshape(1, 16, 32, 1, 1)

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# load checkpoint
            # load checkpoint
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Loading {pretrained_path}")
            log.info(f"Loading {pretrained_path}")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model.load_state_dict(ckpt, assign=True)
            model.load_state_dict(ckpt, assign=True)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.success(f"Successfully loaded {pretrained_path}")
            log.success(f"Successfully loaded {pretrained_path}")
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model.to_empty(device=device)
            model.to_empty(device=device)
            # 中文说明：根据条件选择执行分支；代码：if load_mean_std:
            if load_mean_std:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：img_mean, img_std = torch.randn(1, 16, 1, 1, 1, device=device), torch.randn(
                img_mean, img_std = torch.randn(1, 16, 1, 1, 1, device=device), torch.randn(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：1, 16, 1, 1, 1, device=device
                    1, 16, 1, 1, 1, device=device
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video_mean, video_std = torch.randn(1, 16, 32, 1, 1, device=device), torch.randn(
                video_mean, video_std = torch.randn(1, 16, 32, 1, 1, device=device), torch.randn(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：1, 16, 32, 1, 1, device=device
                    1, 16, 32, 1, 1, device=device
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sync_model_states(model)
    sync_model_states(model)

    # 中文说明：根据条件选择执行分支；代码：if load_mean_std:
    if load_mean_std:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("broadcast mean and std")
        log.info("broadcast mean and std")
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：broadcast(img_mean, 0)
        broadcast(img_mean, 0)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：broadcast(img_std, 0)
        broadcast(img_std, 0)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：broadcast(video_mean, 0)
        broadcast(video_mean, 0)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：broadcast(video_std, 0)
        broadcast(video_std, 0)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return model, img_mean, img_std, video_mean, video_std
        return model, img_mean, img_std, video_mean, video_std

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return (
    return (
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model,
        model,
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.zeros(1, 1, 1, 1, 1, device=device),
        torch.zeros(1, 1, 1, 1, 1, device=device),
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.ones(1, 1, 1, 1, 1, device=device),
        torch.ones(1, 1, 1, 1, 1, device=device),
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.zeros(1, 1, 50, 1, 1, device=device),
        torch.zeros(1, 1, 50, 1, 1, device=device),
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.ones(1, 1, 50, 1, 1, device=device),
        torch.ones(1, 1, 50, 1, 1, device=device),
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class VAE:
class VAE:
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_dim=16,
        z_dim=16,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：vae_pth="",
        vae_pth="",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：load_mean_std=False,
        load_mean_std=False,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：mean_std_path: str = "",
        mean_std_path: str = "",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dtype=torch.float,
        dtype=torch.float,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：device="cuda",
        device="cuda",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_amp=True,
        is_amp=True,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：temporal_window: int = 4,
        temporal_window: int = 4,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dtype = dtype
        self.dtype = dtype
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.device = device
        self.device = device
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.temporal_window = temporal_window
        self.temporal_window = temporal_window

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mean = [
        mean = [
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：-0.7571,
            -0.7571,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：-0.7089,
            -0.7089,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：-0.9113,
            -0.9113,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：0.1075,
            0.1075,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：-0.1745,
            -0.1745,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：0.9653,
            0.9653,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：-0.1517,
            -0.1517,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：1.5508,
            1.5508,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：0.4134,
            0.4134,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：-0.0715,
            -0.0715,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：0.5517,
            0.5517,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：-0.3632,
            -0.3632,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：-0.1922,
            -0.1922,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：-0.9497,
            -0.9497,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：0.2503,
            0.2503,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：-0.2921,
            -0.2921,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
        ]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：std = [
        std = [
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：2.8184,
            2.8184,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：1.4541,
            1.4541,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：2.3275,
            2.3275,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：2.6558,
            2.6558,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：1.2196,
            1.2196,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：1.7708,
            1.7708,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：2.6052,
            2.6052,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：2.0743,
            2.0743,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：3.2687,
            3.2687,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：2.1526,
            2.1526,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：2.8652,
            2.8652,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：1.5579,
            1.5579,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：1.6382,
            1.6382,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：1.1253,
            1.1253,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：2.8251,
            2.8251,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：1.9160,
            1.9160,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
        ]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mean = torch.tensor(mean, dtype=dtype, device=device)
        self.mean = torch.tensor(mean, dtype=dtype, device=device)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.std = torch.tensor(std, dtype=dtype, device=device)
        self.std = torch.tensor(std, dtype=dtype, device=device)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.scale = [self.mean, 1.0 / self.std]
        self.scale = [self.mean, 1.0 / self.std]

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# init model
        # init model
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.model, self.img_mean, self.img_std, self.video_mean, self.video_std = _video_vae(
        self.model, self.img_mean, self.img_std, self.video_mean, self.video_std = _video_vae(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pretrained_path=vae_pth,
            pretrained_path=vae_pth,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_dim=z_dim,
            z_dim=z_dim,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：load_mean_std=load_mean_std,
            load_mean_std=load_mean_std,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mean_std_path=mean_std_path,
            mean_std_path=mean_std_path,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：device=device,
            device=device,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_window=temporal_window,
            temporal_window=temporal_window,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.model = self.model.eval().requires_grad_(False)
        self.model = self.model.eval().requires_grad_(False)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.is_amp = is_amp
        self.is_amp = is_amp
        # 中文说明：根据条件选择执行分支；代码：if not is_amp:
        if not is_amp:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.model = self.model.to(dtype=dtype)
            self.model = self.model.to(dtype=dtype)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.context = nullcontext()
            self.context = nullcontext()
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.context = torch.amp.autocast("cuda", dtype=dtype)
            self.context = torch.amp.autocast("cuda", dtype=dtype)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def count_param(self):
    def count_param(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return sum(p.numel() for p in self.model.parameters())
        return sum(p.numel() for p in self.model.parameters())

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.no_grad()
    @torch.no_grad()
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def encode(self, videos):
    def encode(self, videos):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        videos: A list of videos each with shape [C, T, H, W].
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_dtype = videos.dtype
        in_dtype = videos.dtype
        # 中文说明：处理异常、清理资源或管理上下文；代码：with self.context:
        with self.context:
            # 中文说明：根据条件选择执行分支；代码：if not self.is_amp:
            if not self.is_amp:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：videos = videos.to(self.dtype)
                videos = videos.to(self.dtype)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：latent = self.model.encode(videos, self.scale)
            latent = self.model.encode(videos, self.scale)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：latent = latent.to(in_dtype)
        latent = latent.to(in_dtype)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return latent
        return latent

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.no_grad()
    @torch.no_grad()
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def decode(self, zs):
    def decode(self, zs):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_dtype = zs.dtype
        in_dtype = zs.dtype
        # 中文说明：处理异常、清理资源或管理上下文；代码：with self.context:
        with self.context:
            # 中文说明：根据条件选择执行分支；代码：if not self.is_amp:
            if not self.is_amp:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：zs = zs.to(self.dtype)
                zs = zs.to(self.dtype)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_recon = self.model.decode(zs, self.scale)
            video_recon = self.model.decode(zs, self.scale)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_recon = video_recon.to(in_dtype)
        video_recon = video_recon.to(in_dtype)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return video_recon
        return video_recon


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class TokenizerInterface(VideoTokenizerInterface):
class TokenizerInterface(VideoTokenizerInterface):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, chunk_duration: int = 81, load_mean_std=False, **kwargs):
    def __init__(self, chunk_duration: int = 81, load_mean_std=False, **kwargs):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.model = VAE(
        self.model = VAE(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dtype=torch.bfloat16,
            dtype=torch.bfloat16,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_amp=False,
            is_amp=False,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：load_mean_std=load_mean_std,
            load_mean_std=load_mean_std,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：vae_pth=kwargs.get(
            vae_pth=kwargs.get(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："vae_pth",
                "vae_pth",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："",
                "",
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_window=kwargs.get("temporal_window", 4),
            temporal_window=kwargs.get("temporal_window", 4),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del kwargs
        del kwargs
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.chunk_duration = chunk_duration
        self.chunk_duration = chunk_duration

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def dtype(self):
    def dtype(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.model.dtype
        return self.model.dtype

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def to(self, **kwargs) -> VAE_:
    def to(self, **kwargs) -> VAE_:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.model.model.to(**kwargs)
        return self.model.model.to(**kwargs)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def reset_dtype(self):
    def reset_dtype(self):
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# @torch.compile(dynamic=False); it will significantly slow down the training job
    # @torch.compile(dynamic=False); it will significantly slow down the training job
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def encode(self, state: torch.Tensor) -> torch.Tensor:
    def encode(self, state: torch.Tensor) -> torch.Tensor:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：latents = self.model.encode(state)
        latents = self.model.encode(state)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_frames = latents.shape[2]
        num_frames = latents.shape[2]
        # 中文说明：根据条件选择执行分支；代码：if num_frames == 1:
        if num_frames == 1:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return (latents - self.model.img_mean.type_as(latents)) / self.model.img_std.type_as(latents)
            return (latents - self.model.img_mean.type_as(latents)) / self.model.img_std.type_as(latents)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return (latents - self.model.video_mean[:, :, :num_frames].type_as(latents)) / self.model.vid...
            return (latents - self.model.video_mean[:, :, :num_frames].type_as(latents)) / self.model.video_std[
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：:, :, :num_frames
                :, :, :num_frames
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：].type_as(latents)
            ].type_as(latents)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def decode(self, latent: torch.Tensor) -> torch.Tensor:
    def decode(self, latent: torch.Tensor) -> torch.Tensor:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_frames = latent.shape[2]
        num_frames = latent.shape[2]
        # 中文说明：根据条件选择执行分支；代码：if num_frames == 1:
        if num_frames == 1:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.model.decode(
            return self.model.decode(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：(latent * self.model.img_std.type_as(latent)) + self.model.img_mean.type_as(latent)
                (latent * self.model.img_std.type_as(latent)) + self.model.img_mean.type_as(latent)
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.model.decode(
            return self.model.decode(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：(latent * self.model.video_std[:, :, :num_frames].type_as(latent))
                (latent * self.model.video_std[:, :, :num_frames].type_as(latent))
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：+ self.model.video_mean[:, :, :num_frames].type_as(latent)
                + self.model.video_mean[:, :, :num_frames].type_as(latent)
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_latent_num_frames(self, num_pixel_frames: int) -> int:
    def get_latent_num_frames(self, num_pixel_frames: int) -> int:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return 1 + (num_pixel_frames - 1) // 4
        return 1 + (num_pixel_frames - 1) // 4

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_pixel_num_frames(self, num_latent_frames: int) -> int:
    def get_pixel_num_frames(self, num_latent_frames: int) -> int:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return (num_latent_frames - 1) * 4 + 1
        return (num_latent_frames - 1) * 4 + 1

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def spatial_compression_factor(self):
    def spatial_compression_factor(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return 8
        return 8

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def temporal_compression_factor(self):
    def temporal_compression_factor(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return 4
        return 4

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def pixel_chunk_duration(self):
    def pixel_chunk_duration(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.chunk_duration
        return self.chunk_duration

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def latent_chunk_duration(self):
    def latent_chunk_duration(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.get_latent_num_frames(self.chunk_duration)
        return self.get_latent_num_frames(self.chunk_duration)

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def latent_ch(self):
    def latent_ch(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return 16
        return 16

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def spatial_resolution(self):
    def spatial_resolution(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return 512
        return 512

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def name(self):
    def name(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return "tokenizer"
        return "tokenizer"
