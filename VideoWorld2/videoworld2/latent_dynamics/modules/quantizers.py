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
# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Quantizers for discrete image and video tokenization."""
"""Quantizers for discrete image and video tokenization."""

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Optional
from typing import Optional

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.nn as nn
import torch.nn as nn
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.nn.functional as F
import torch.nn.functional as F
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from einops import reduce
from einops import reduce
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from loguru import logger as logging
from loguru import logger as logging

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.latent_dynamics.modules.utils import default, entropy, pack_one, rearrange, ...
from videoworld2.latent_dynamics.modules.utils import default, entropy, pack_one, rearrange, round_ste, unpack_one

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_PERSISTENT = True
_PERSISTENT = True


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ResidualFSQuantizer(nn.Module):
class ResidualFSQuantizer(nn.Module):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Residual Finite Scalar Quantization
    """Residual Finite Scalar Quantization

    Follows Algorithm 1. in https://arxiv.org/pdf/2107.03312.pdf
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, levels: list[int], num_quantizers: int, **ignore_kwargs):
    def __init__(self, levels: list[int], num_quantizers: int, **ignore_kwargs):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dtype = ignore_kwargs.get("dtype", torch.float32)
        self.dtype = ignore_kwargs.get("dtype", torch.float32)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.layers = nn.ModuleList([FSQuantizer(levels=levels) for _ in range(num_quantizers)])
        self.layers = nn.ModuleList([FSQuantizer(levels=levels) for _ in range(num_quantizers)])

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x: torch.Tensor) -> torch.Tensor:
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：indices_stack = []
        indices_stack = []
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：residual = x
        residual = x
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quantized_out = 0
        quantized_out = 0
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：loss_out = 0
        loss_out = 0
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i, layer in enumerate(self.layers):
        for i, layer in enumerate(self.layers):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：quant_indices, z, loss = layer(residual)
            quant_indices, z, loss = layer(residual)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：indices_stack.append(quant_indices)
            indices_stack.append(quant_indices)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：residual = residual - z.detach()
            residual = residual - z.detach()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quantized_out = quantized_out + z
            quantized_out = quantized_out + z
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：loss_out = loss_out + loss
            loss_out = loss_out + loss
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.residual = residual
        self.residual = residual
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：indices = torch.stack(indices_stack, dim=1)
        indices = torch.stack(indices_stack, dim=1)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return indices, quantized_out.to(self.dtype), loss_out.to(self.dtype)
        return indices, quantized_out.to(self.dtype), loss_out.to(self.dtype)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def indices_to_codes(self, indices_stack: torch.Tensor) -> torch.Tensor:
    def indices_to_codes(self, indices_stack: torch.Tensor) -> torch.Tensor:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quantized_out = 0
        quantized_out = 0
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for layer, indices in zip(self.layers, indices_stack.transpose(0, 1)):
        for layer, indices in zip(self.layers, indices_stack.transpose(0, 1)):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quantized_out += layer.indices_to_codes(indices)
            quantized_out += layer.indices_to_codes(indices)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return quantized_out
        return quantized_out


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class FSQuantizer(nn.Module):
class FSQuantizer(nn.Module):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Finite Scalar Quantization: VQ-VAE Made Simple - https://arxiv.org/abs/2309.15505
    """Finite Scalar Quantization: VQ-VAE Made Simple - https://arxiv.org/abs/2309.15505

    Code adapted from Jax version in Appendix A.1.

    Adapted from: https://github.com/lucidrains/vector-quantize-pytorch/blob/9502a1f447876d53fd37685b226bf28f250dc4a3/
    vector_quantize_pytorch/finite_scalar_quantization.py
    [Copyright (c) 2020 Phil Wang]
    https://github.com/lucidrains/vector-quantize-pytorch/blob/9502a1f447876d53fd37685b226bf28f250dc4a3/LICENSE
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：levels: list[int],
        levels: list[int],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dim: Optional[int] = None,
        dim: Optional[int] = None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_codebooks=1,
        num_codebooks=1,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：keep_num_codebooks_dim: Optional[bool] = None,
        keep_num_codebooks_dim: Optional[bool] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scale: Optional[float] = None,
        scale: Optional[float] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**ignore_kwargs,
        **ignore_kwargs,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dtype = ignore_kwargs.get("dtype", torch.bfloat16)
        self.dtype = ignore_kwargs.get("dtype", torch.bfloat16)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.persistent = ignore_kwargs.get("persistent_quantizer", _PERSISTENT)
        self.persistent = ignore_kwargs.get("persistent_quantizer", _PERSISTENT)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_levels = torch.tensor(levels, dtype=torch.int32)
        _levels = torch.tensor(levels, dtype=torch.int32)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.register_buffer("_levels", _levels, persistent=self.persistent)
        self.register_buffer("_levels", _levels, persistent=self.persistent)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_basis = torch.cumprod(torch.tensor([1] + levels[:-1]), dim=0, dtype=torch.int32)
        _basis = torch.cumprod(torch.tensor([1] + levels[:-1]), dim=0, dtype=torch.int32)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.register_buffer("_basis", _basis, persistent=self.persistent)
        self.register_buffer("_basis", _basis, persistent=self.persistent)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.scale = scale
        self.scale = scale

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：codebook_dim = len(levels)
        codebook_dim = len(levels)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.codebook_dim = codebook_dim
        self.codebook_dim = codebook_dim

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：effective_codebook_dim = codebook_dim * num_codebooks
        effective_codebook_dim = codebook_dim * num_codebooks
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_codebooks = num_codebooks
        self.num_codebooks = num_codebooks
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.effective_codebook_dim = effective_codebook_dim
        self.effective_codebook_dim = effective_codebook_dim

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：keep_num_codebooks_dim = default(keep_num_codebooks_dim, num_codebooks > 1)
        keep_num_codebooks_dim = default(keep_num_codebooks_dim, num_codebooks > 1)
        # 中文说明：检查运行时假设是否成立；代码：assert not (num_codebooks > 1 and not keep_num_codebooks_dim)
        assert not (num_codebooks > 1 and not keep_num_codebooks_dim)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.keep_num_codebooks_dim = keep_num_codebooks_dim
        self.keep_num_codebooks_dim = keep_num_codebooks_dim

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dim = default(dim, len(_levels) * num_codebooks)
        self.dim = default(dim, len(_levels) * num_codebooks)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：has_projections = self.dim != effective_codebook_dim
        has_projections = self.dim != effective_codebook_dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.project_in = nn.Linear(self.dim, effective_codebook_dim) if has_projections else nn.Iden...
        self.project_in = nn.Linear(self.dim, effective_codebook_dim) if has_projections else nn.Identity()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.project_out = nn.Linear(effective_codebook_dim, self.dim) if has_projections else nn.Ide...
        self.project_out = nn.Linear(effective_codebook_dim, self.dim) if has_projections else nn.Identity()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.has_projections = has_projections
        self.has_projections = has_projections

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.codebook_size = self._levels.prod().item()
        self.codebook_size = self._levels.prod().item()

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：implicit_codebook = self.indices_to_codes(torch.arange(self.codebook_size), project_out=False)
        implicit_codebook = self.indices_to_codes(torch.arange(self.codebook_size), project_out=False)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.register_buffer("implicit_codebook", implicit_codebook, persistent=self.persistent)
        self.register_buffer("implicit_codebook", implicit_codebook, persistent=self.persistent)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def bound(self, z: torch.Tensor, eps: float = 1e-3) -> torch.Tensor:
    def bound(self, z: torch.Tensor, eps: float = 1e-3) -> torch.Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Bound `z`, an array of shape (..., d)."""
        """Bound `z`, an array of shape (..., d)."""
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：half_l = (self._levels - 1) * (1 + eps) / 2
        half_l = (self._levels - 1) * (1 + eps) / 2
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：offset = torch.where(self._levels % 2 == 0, 0.5, 0.0)
        offset = torch.where(self._levels % 2 == 0, 0.5, 0.0)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：shift = (offset / half_l).atanh()
        shift = (offset / half_l).atanh()
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return (z + shift).tanh() * half_l - offset
        return (z + shift).tanh() * half_l - offset

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def quantize(self, z: torch.Tensor) -> torch.Tensor:
    def quantize(self, z: torch.Tensor) -> torch.Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Quantizes z, returns quantized zhat, same shape as z."""
        """Quantizes z, returns quantized zhat, same shape as z."""
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quantized = round_ste(self.bound(z))
        quantized = round_ste(self.bound(z))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：half_width = self._levels // 2 # Renormalize to [-1, 1].
        half_width = self._levels // 2  # Renormalize to [-1, 1].
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return quantized / half_width
        return quantized / half_width

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _scale_and_shift(self, zhat_normalized: torch.Tensor) -> torch.Tensor:
    def _scale_and_shift(self, zhat_normalized: torch.Tensor) -> torch.Tensor:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：half_width = self._levels // 2
        half_width = self._levels // 2
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return (zhat_normalized * half_width) + half_width
        return (zhat_normalized * half_width) + half_width

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _scale_and_shift_inverse(self, zhat: torch.Tensor) -> torch.Tensor:
    def _scale_and_shift_inverse(self, zhat: torch.Tensor) -> torch.Tensor:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：half_width = self._levels // 2
        half_width = self._levels // 2
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return (zhat - half_width) / half_width
        return (zhat - half_width) / half_width

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def codes_to_indices(self, zhat: torch.Tensor) -> torch.Tensor:
    def codes_to_indices(self, zhat: torch.Tensor) -> torch.Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Converts a `code` to an index in the codebook."""
        """Converts a `code` to an index in the codebook."""
        # 中文说明：检查运行时假设是否成立；代码：assert zhat.shape[-1] == self.codebook_dim
        assert zhat.shape[-1] == self.codebook_dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：zhat = self._scale_and_shift(zhat).float()
        zhat = self._scale_and_shift(zhat).float()
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return (zhat * self._basis).sum(dim=-1).to(torch.int32)
        return (zhat * self._basis).sum(dim=-1).to(torch.int32)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def indices_to_codes(self, indices: torch.Tensor, project_out=True) -> torch.Tensor:
    def indices_to_codes(self, indices: torch.Tensor, project_out=True) -> torch.Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Inverse of `codes_to_indices`."""
        """Inverse of `codes_to_indices`."""
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_img_or_video = indices.ndim >= (3 + int(self.keep_num_codebooks_dim))
        is_img_or_video = indices.ndim >= (3 + int(self.keep_num_codebooks_dim))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：indices = rearrange(indices, "... -> ... 1")
        indices = rearrange(indices, "... -> ... 1")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：codes_non_centered = (indices // self._basis) % self._levels
        codes_non_centered = (indices // self._basis) % self._levels
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：codes = self._scale_and_shift_inverse(codes_non_centered)
        codes = self._scale_and_shift_inverse(codes_non_centered)

        # 中文说明：根据条件选择执行分支；代码：if self.keep_num_codebooks_dim:
        if self.keep_num_codebooks_dim:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：codes = rearrange(codes, "... c d -> ... (c d)")
            codes = rearrange(codes, "... c d -> ... (c d)")

        # 中文说明：根据条件选择执行分支；代码：if project_out:
        if project_out:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：codes = self.project_out(codes)
            codes = self.project_out(codes)

        # 中文说明：根据条件选择执行分支；代码：if is_img_or_video:
        if is_img_or_video:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：codes = rearrange(codes, "b ... d -> b d ...")
            codes = rearrange(codes, "b ... d -> b d ...")

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return codes.to(self.dtype)
        return codes.to(self.dtype)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, z: torch.Tensor) -> torch.Tensor:
    def forward(self, z: torch.Tensor) -> torch.Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        einstein notation
        b - batch
        n - sequence (or flattened spatial dimensions)
        d - feature dimension, which is also log2(codebook size)
        c - number of codebook dim
        """
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_img_or_video = z.ndim >= 4
        is_img_or_video = z.ndim >= 4

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# standardize image or video into (batch, seq, dimension)
        # standardize image or video into (batch, seq, dimension)

        # 中文说明：根据条件选择执行分支；代码：if is_img_or_video:
        if is_img_or_video:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z = rearrange(z, "b d ... -> b ... d")
            z = rearrange(z, "b d ... -> b ... d")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：z, ps = pack_one(z, "b * d")
            z, ps = pack_one(z, "b * d")

        # 中文说明：检查运行时假设是否成立；代码：assert z.shape[-1] == self.dim, f"expected dimension of {self.dim} but found dimension of {z....
        assert z.shape[-1] == self.dim, f"expected dimension of {self.dim} but found dimension of {z.shape[-1]}"

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z = self.project_in(z)
        z = self.project_in(z)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z = rearrange(z, "b n (c d) -> b n c d", c=self.num_codebooks)
        z = rearrange(z, "b n (c d) -> b n c d", c=self.num_codebooks)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：codes = self.quantize(z)
        codes = self.quantize(z)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：indices = self.codes_to_indices(codes)
        indices = self.codes_to_indices(codes)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：codes = rearrange(codes, "b n c d -> b n (c d)")
        codes = rearrange(codes, "b n c d -> b n (c d)")

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out = self.project_out(codes)
        out = self.project_out(codes)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# reconstitute image or video dimensions
        # reconstitute image or video dimensions

        # 中文说明：根据条件选择执行分支；代码：if is_img_or_video:
        if is_img_or_video:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out = unpack_one(out, ps, "b * d")
            out = unpack_one(out, ps, "b * d")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out = rearrange(out, "b ... d -> b d ...")
            out = rearrange(out, "b ... d -> b d ...")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：indices = unpack_one(indices, ps, "b * c")
            indices = unpack_one(indices, ps, "b * c")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dummy_loss = torch.zeros_like(out.mean(dim=[1, 2, 3], keepdim=True))
            dummy_loss = torch.zeros_like(out.mean(dim=[1, 2, 3], keepdim=True))
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dummy_loss = torch.zeros_like(out.mean(dim=[1, 2], keepdim=True)).unsqueeze(1)
            dummy_loss = torch.zeros_like(out.mean(dim=[1, 2], keepdim=True)).unsqueeze(1)

        # 中文说明：根据条件选择执行分支；代码：if not self.keep_num_codebooks_dim:
        if not self.keep_num_codebooks_dim:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：indices = rearrange(indices, "... 1 -> ...")
            indices = rearrange(indices, "... 1 -> ...")

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return (indices, out.to(self.dtype), dummy_loss)
        return (indices, out.to(self.dtype), dummy_loss)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class VectorQuantizer(nn.Module):
class VectorQuantizer(nn.Module):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Improved version over VectorQuantizer. Mostly
    """Improved version over VectorQuantizer. Mostly
    avoids costly matrix multiplications and allows for post-hoc remapping of indices.

    Adapted from: https://github.com/CompVis/taming-transformers/blob/3ba01b241669f5ade541ce990f7650a3b8f65318/
    taming/modules/vqvae/quantize.py

    [Copyright (c) 2020 Patrick Esser and Robin Rombach and Björn Ommer]
    https://github.com/CompVis/taming-transformers/blob/3ba01b241669f5ade541ce990f7650a3b8f65318/License.txt
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_embeddings: int,
        num_embeddings: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：embedding_dim: int,
        embedding_dim: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：beta: float = 0.25,
        beta: float = 0.25,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：remap: str = None,
        remap: str = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：unknown_index: str = "random",
        unknown_index: str = "random",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sane_index_shape: bool = False,
        sane_index_shape: bool = False,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：legacy: bool = True,
        legacy: bool = True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_norm=False,
        use_norm=False,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**ignore_kwargs,
        **ignore_kwargs,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.n_e = num_embeddings
        self.n_e = num_embeddings
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.e_dim = embedding_dim
        self.e_dim = embedding_dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.beta = beta
        self.beta = beta
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.legacy = legacy
        self.legacy = legacy
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.norm = lambda x: F.normalize(x, dim=-1) if use_norm else x
        self.norm = lambda x: F.normalize(x, dim=-1) if use_norm else x

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.embedding = nn.Embedding(self.n_e, self.e_dim)
        self.embedding = nn.Embedding(self.n_e, self.e_dim)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.embedding.weight.data.uniform_(-1.0 / self.n_e, 1.0 / self.n_e)
        self.embedding.weight.data.uniform_(-1.0 / self.n_e, 1.0 / self.n_e)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.remap = remap
        self.remap = remap
        # 中文说明：根据条件选择执行分支；代码：if self.remap is not None:
        if self.remap is not None:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.register_buffer("used", torch.tensor(np.load(self.remap)))
            self.register_buffer("used", torch.tensor(np.load(self.remap)))
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.re_embed = self.used.shape[0]
            self.re_embed = self.used.shape[0]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.unknown_index = unknown_index
            self.unknown_index = unknown_index
            # 中文说明：根据条件选择执行分支；代码：if self.unknown_index == "extra":
            if self.unknown_index == "extra":
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.unknown_index = self.re_embed
                self.unknown_index = self.re_embed
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.re_embed = self.re_embed + 1
                self.re_embed = self.re_embed + 1
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(
            print(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Remapping {self.n_e} indices to {self.re_embed} indices. "
                f"Remapping {self.n_e} indices to {self.re_embed} indices. "
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Using {self.unknown_index} for unknown indices."
                f"Using {self.unknown_index} for unknown indices."
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.re_embed = num_embeddings
            self.re_embed = num_embeddings

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.sane_index_shape = sane_index_shape
        self.sane_index_shape = sane_index_shape
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dtype = ignore_kwargs.get("dtype", torch.float32)
        self.dtype = ignore_kwargs.get("dtype", torch.float32)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def remap_to_used(self, inds):
    def remap_to_used(self, inds):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ishape = inds.shape
        ishape = inds.shape
        # 中文说明：检查运行时假设是否成立；代码：assert len(ishape) > 1
        assert len(ishape) > 1
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：inds = inds.reshape(ishape[0], -1)
        inds = inds.reshape(ishape[0], -1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：used = self.used.to(inds)
        used = self.used.to(inds)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：match = (inds[:, :, None] == used[None, None, ...]).long()
        match = (inds[:, :, None] == used[None, None, ...]).long()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：new = match.argmax(-1)
        new = match.argmax(-1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：unknown = match.sum(2) < 1
        unknown = match.sum(2) < 1
        # 中文说明：根据条件选择执行分支；代码：if self.unknown_index == "random":
        if self.unknown_index == "random":
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：new[unknown] = torch.randint(0, self.re_embed, size=new[unknown].shape).to(device=new.device)
            new[unknown] = torch.randint(0, self.re_embed, size=new[unknown].shape).to(device=new.device)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：new[unknown] = self.unknown_index
            new[unknown] = self.unknown_index
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return new.reshape(ishape)
        return new.reshape(ishape)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def unmap_to_all(self, inds):
    def unmap_to_all(self, inds):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ishape = inds.shape
        ishape = inds.shape
        # 中文说明：检查运行时假设是否成立；代码：assert len(ishape) > 1
        assert len(ishape) > 1
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：inds = inds.reshape(ishape[0], -1)
        inds = inds.reshape(ishape[0], -1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：used = self.used.to(inds)
        used = self.used.to(inds)
        # 中文说明：根据条件选择执行分支；代码：if self.re_embed > self.used.shape[0]: # extra token
        if self.re_embed > self.used.shape[0]:  # extra token
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：inds[inds >= self.used.shape[0]] = 0 # simply set to zero
            inds[inds >= self.used.shape[0]] = 0  # simply set to zero
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：back = torch.gather(used[None, :][inds.shape[0] * [0], :], 1, inds)
        back = torch.gather(used[None, :][inds.shape[0] * [0], :], 1, inds)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return back.reshape(ishape)
        return back.reshape(ishape)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, z, temp=None, rescale_logits=False, return_logits=False):
    def forward(self, z, temp=None, rescale_logits=False, return_logits=False):
        # 中文说明：检查运行时假设是否成立；代码：assert temp is None or temp == 1.0, "Only for interface compatible with Gumbel"
        assert temp is None or temp == 1.0, "Only for interface compatible with Gumbel"
        # 中文说明：检查运行时假设是否成立；代码：assert rescale_logits is False, "Only for interface compatible with Gumbel"
        assert rescale_logits is False, "Only for interface compatible with Gumbel"
        # 中文说明：检查运行时假设是否成立；代码：assert return_logits is False, "Only for interface compatible with Gumbel"
        assert return_logits is False, "Only for interface compatible with Gumbel"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z = rearrange(z, "b c h w -> b h w c").contiguous()
        z = rearrange(z, "b c h w -> b h w c").contiguous()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_flattened = z.view(-1, self.e_dim)
        z_flattened = z.view(-1, self.e_dim)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：d = (
        d = (
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.sum(z_flattened**2, dim=1, keepdim=True)
            torch.sum(z_flattened**2, dim=1, keepdim=True)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：+ torch.sum(self.embedding.weight**2, dim=1)
            + torch.sum(self.embedding.weight**2, dim=1)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：- 2
            - 2
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：* torch.einsum(
            * torch.einsum(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："bd,dn->bn",
                "bd,dn->bn",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：z_flattened,
                z_flattened,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rearrange(self.embedding.weight, "n d -> d n"),
                rearrange(self.embedding.weight, "n d -> d n"),
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：encoding_indices = torch.argmin(d, dim=1).unsqueeze(1)
        encoding_indices = torch.argmin(d, dim=1).unsqueeze(1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：encodings = torch.zeros(encoding_indices.shape[0], self.n_e, device=z.device)
        encodings = torch.zeros(encoding_indices.shape[0], self.n_e, device=z.device)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：encodings.scatter_(1, encoding_indices, 1)
        encodings.scatter_(1, encoding_indices, 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_q = torch.matmul(encodings, self.embedding.weight).view(z.shape)
        z_q = torch.matmul(encodings, self.embedding.weight).view(z.shape)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_encodings = None
        min_encodings = None

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：z_q, z = self.norm(z_q), self.norm(z)
        z_q, z = self.norm(z_q), self.norm(z)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# compute loss for embedding
        # compute loss for embedding
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：commit_loss = torch.mean((z_q - z.detach()) ** 2, dim=[1, 2, 3], keepdim=True)
        commit_loss = torch.mean((z_q - z.detach()) ** 2, dim=[1, 2, 3], keepdim=True)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：emb_loss = torch.mean((z_q.detach() - z) ** 2, dim=[1, 2, 3], keepdim=True)
        emb_loss = torch.mean((z_q.detach() - z) ** 2, dim=[1, 2, 3], keepdim=True)
        # 中文说明：根据条件选择执行分支；代码：if not self.legacy:
        if not self.legacy:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：loss = self.beta * emb_loss + commit_loss
            loss = self.beta * emb_loss + commit_loss
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：loss = emb_loss + self.beta * commit_loss
            loss = emb_loss + self.beta * commit_loss

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# preserve gradients
        # preserve gradients
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_q = z + (z_q - z).detach()
        z_q = z + (z_q - z).detach()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：avg_probs = torch.mean(encodings, dim=0)
        avg_probs = torch.mean(encodings, dim=0)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：perplexity = torch.exp(-torch.sum(avg_probs * torch.log(avg_probs + 1e-10)))
        perplexity = torch.exp(-torch.sum(avg_probs * torch.log(avg_probs + 1e-10)))

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# reshape back to match original input shape
        # reshape back to match original input shape
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_q = rearrange(z_q, "b h w c -> b c h w").contiguous()
        z_q = rearrange(z_q, "b h w c -> b c h w").contiguous()

        # 中文说明：根据条件选择执行分支；代码：if self.remap is not None:
        if self.remap is not None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_encoding_indices = encoding_indices.squeeze(1).reshape(z.shape[0], -1) # add batch axis
            min_encoding_indices = encoding_indices.squeeze(1).reshape(z.shape[0], -1)  # add batch axis
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_encoding_indices = self.remap_to_used(encoding_indices.squeeze(1))
            min_encoding_indices = self.remap_to_used(encoding_indices.squeeze(1))
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_encoding_indices = min_encoding_indices.reshape(-1, 1) # flatten
            min_encoding_indices = min_encoding_indices.reshape(-1, 1)  # flatten

        # 中文说明：根据条件选择执行分支；代码：if self.sane_index_shape:
        if self.sane_index_shape:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_encoding_indices = min_encoding_indices.reshape(z_q.shape[0], z_q.shape[2], z_q.shape[3])
            min_encoding_indices = min_encoding_indices.reshape(z_q.shape[0], z_q.shape[2], z_q.shape[3])

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return (
        return (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：z_q,
            z_q,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：loss,
            loss,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：(
            (
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：encoding_indices.squeeze(1),
                encoding_indices.squeeze(1),
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：min_encodings,
                min_encodings,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：commit_loss.mean().detach(),
                commit_loss.mean().detach(),
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.beta * emb_loss.mean().detach(),
                self.beta * emb_loss.mean().detach(),
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：perplexity.mean().detach(),
                perplexity.mean().detach(),
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_codebook_entry(self, indices, shape):
    def get_codebook_entry(self, indices, shape):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# shape specifying (batch, height, width, channel)
        # shape specifying (batch, height, width, channel)
        # 中文说明：根据条件选择执行分支；代码：if self.remap is not None:
        if self.remap is not None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：indices = indices.reshape(shape[0], -1) # add batch axis
            indices = indices.reshape(shape[0], -1)  # add batch axis
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：indices = self.unmap_to_all(indices)
            indices = self.unmap_to_all(indices)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：indices = indices.reshape(-1) # flatten again
            indices = indices.reshape(-1)  # flatten again

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# get quantized latent vectors
        # get quantized latent vectors
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_q = self.embedding(indices)
        z_q = self.embedding(indices)

        # 中文说明：根据条件选择执行分支；代码：if shape is not None:
        if shape is not None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_q = z_q.view(shape)
            z_q = z_q.view(shape)
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# reshape back to match original input shape
            # reshape back to match original input shape
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_q = z_q.permute(0, 3, 1, 2).contiguous()
            z_q = z_q.permute(0, 3, 1, 2).contiguous()

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return z_q
        return z_q


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class LFQuantizer(nn.Module):
class LFQuantizer(nn.Module):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Lookup-Free Quantization
    """Lookup-Free Quantization

    Adapted from: https://github.com/lucidrains/vector-quantize-pytorch/blob/9502a1f447876d53fd37685b226bf28f250dc4a3/
    vector_quantize_pytorch/lookup_free_quantization.py
    [Copyright (c) 2020 Phil Wang]
    https://github.com/lucidrains/vector-quantize-pytorch/blob/9502a1f447876d53fd37685b226bf28f250dc4a3/LICENSE
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：*,
        *,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：codebook_size: int,
        codebook_size: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：codebook_dim: int,
        codebook_dim: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：embed_dim: Optional[int] = None, # if None, use codebook_dim
        embed_dim: Optional[int] = None,  # if None, use codebook_dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：entropy_loss_weight=0.1,
        entropy_loss_weight=0.1,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：commitment_loss_weight=0.25,
        commitment_loss_weight=0.25,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：default_temp: float = 0.01,
        default_temp: float = 0.01,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：entropy_loss: bool = False,
        entropy_loss: bool = False,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**ignore_kwargs,
        **ignore_kwargs,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Lookup-Free Quantization
        """Lookup-Free Quantization

        Args:
            codebook_size (int): The number of entries in the codebook.
            codebook_dim (int): The number of bits in each code.
            embed_dim (Optional[int], optional): The dimension of the input embedding. Defaults to None.
            entropy_loss_weight (float, optional): Whether to use entropy loss. Defaults to 0.1.
            commitment_loss_weight (float, optional): Weight for commitment loss. Defaults to 0.25.
            default_temp (float, optional): The temprature to use. Defaults to 0.01.
            entropy_loss (bool, optional): Flag for entropy loss. Defaults to False.
        """
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.entropy_loss = entropy_loss
        self.entropy_loss = entropy_loss
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.codebook_dim = codebook_dim
        self.codebook_dim = codebook_dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.default_temp = default_temp
        self.default_temp = default_temp
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.entrop_loss_weight = entropy_loss_weight
        self.entrop_loss_weight = entropy_loss_weight
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.commitment_loss_weight = commitment_loss_weight
        self.commitment_loss_weight = commitment_loss_weight
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：embed_dim = embed_dim or codebook_dim
        embed_dim = embed_dim or codebook_dim

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：has_projections = embed_dim != codebook_dim
        has_projections = embed_dim != codebook_dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.project_in = nn.Linear(embed_dim, codebook_dim) if has_projections else nn.Identity()
        self.project_in = nn.Linear(embed_dim, codebook_dim) if has_projections else nn.Identity()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.project_out = nn.Linear(codebook_dim, embed_dim) if has_projections else nn.Identity()
        self.project_out = nn.Linear(codebook_dim, embed_dim) if has_projections else nn.Identity()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：logging.info(f"LFQ: has_projections={has_projections}, dim_in={embed_dim}, codebook_dim={code...
        logging.info(f"LFQ: has_projections={has_projections}, dim_in={embed_dim}, codebook_dim={codebook_dim}")

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dtype = ignore_kwargs.get("dtype", torch.float32)
        self.dtype = ignore_kwargs.get("dtype", torch.float32)

        # 中文说明：根据条件选择执行分支；代码：if entropy_loss:
        if entropy_loss:
            # 中文说明：检查运行时假设是否成立；代码：assert 2**codebook_dim == codebook_size, "codebook size must be 2 ** codebook_dim"
            assert 2**codebook_dim == codebook_size, "codebook size must be 2 ** codebook_dim"
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.codebook_size = codebook_size
            self.codebook_size = codebook_size

            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.register_buffer(
            self.register_buffer(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："mask",
                "mask",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：2 ** torch.arange(codebook_dim - 1, -1, -1),
                2 ** torch.arange(codebook_dim - 1, -1, -1),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：persistent=_PERSISTENT,
                persistent=_PERSISTENT,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.register_buffer("zero", torch.tensor(0.0), persistent=_PERSISTENT)
            self.register_buffer("zero", torch.tensor(0.0), persistent=_PERSISTENT)

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：all_codes = torch.arange(codebook_size)
            all_codes = torch.arange(codebook_size)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：bits = ((all_codes[..., None].int() & self.mask) != 0).float()
            bits = ((all_codes[..., None].int() & self.mask) != 0).float()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：codebook = 2 * bits - 1.0
            codebook = 2 * bits - 1.0

            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.register_buffer("codebook", codebook, persistent=_PERSISTENT) # [codebook_size, codebook...
            self.register_buffer("codebook", codebook, persistent=_PERSISTENT)  # [codebook_size, codebook_dim]

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, z: torch.Tensor, temp: float = None) -> torch.Tensor:
    def forward(self, z: torch.Tensor, temp: float = None) -> torch.Tensor:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temp = temp or self.default_temp
        temp = temp or self.default_temp

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z = rearrange(z, "b d ... -> b ... d")
        z = rearrange(z, "b d ... -> b ... d")
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：z, ps = pack_one(z, "b * d")
        z, ps = pack_one(z, "b * d")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z = self.project_in(z)
        z = self.project_in(z)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# split out number of codebooks
        # split out number of codebooks
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z = rearrange(z, "b n (c d) -> b n c d", c=self.num_codebooks)
        z = rearrange(z, "b n (c d) -> b n c d", c=self.num_codebooks)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# quantization
        # quantization
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：original_input = z
        original_input = z

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：codebook_value = torch.ones_like(z)
        codebook_value = torch.ones_like(z)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_q = torch.where(z > 0, codebook_value, -codebook_value)
        z_q = torch.where(z > 0, codebook_value, -codebook_value)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# preserve gradients
        # preserve gradients
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_q = z + (z_q - z).detach()
        z_q = z + (z_q - z).detach()

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# commit loss
        # commit loss
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：commit_loss = ((original_input - z_q.detach()) ** 2).mean(dim=[1, 2, 3])
        commit_loss = ((original_input - z_q.detach()) ** 2).mean(dim=[1, 2, 3])

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_q = rearrange(z_q, "b n c d -> b n (c d)")
        z_q = rearrange(z_q, "b n c d -> b n (c d)")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_q = self.project_out(z_q)
        z_q = self.project_out(z_q)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# reshape
        # reshape
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_q = unpack_one(z_q, ps, "b * d")
        z_q = unpack_one(z_q, ps, "b * d")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_q = rearrange(z_q, "b ... d -> b d ...")
        z_q = rearrange(z_q, "b ... d -> b d ...")

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：loss = self.commitment_loss_weight * commit_loss
        loss = self.commitment_loss_weight * commit_loss

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# entropy loss (eq-5)
        # entropy loss (eq-5)
        # 中文说明：根据条件选择执行分支；代码：if self.entropy_loss:
        if self.entropy_loss:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# indices
            # indices
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：indices = reduce((z > 0).int() * self.mask.int(), "b n c d -> b n c", "sum")
            indices = reduce((z > 0).int() * self.mask.int(), "b n c d -> b n c", "sum")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：indices = unpack_one(indices, ps, "b * c")
            indices = unpack_one(indices, ps, "b * c")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：indices = rearrange(indices, "... 1 -> ...")
            indices = rearrange(indices, "... 1 -> ...")

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distance = -2 * torch.einsum(
            distance = -2 * torch.einsum(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："... i d, j d -> ... i j",
                "... i d, j d -> ... i j",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：original_input,
                original_input,
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.codebook.to(original_input.dtype),
                self.codebook.to(original_input.dtype),
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prob = (-distance / temp).softmax(dim=-1)
            prob = (-distance / temp).softmax(dim=-1)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：per_sample_entropy = entropy(prob).mean(dim=[1, 2])
            per_sample_entropy = entropy(prob).mean(dim=[1, 2])
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：avg_prob = reduce(prob, "... c d -> c d", "mean")
            avg_prob = reduce(prob, "... c d -> c d", "mean")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：codebook_entropy = entropy(avg_prob).mean()
            codebook_entropy = entropy(avg_prob).mean()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：entropy_aux_loss = per_sample_entropy - codebook_entropy
            entropy_aux_loss = per_sample_entropy - codebook_entropy

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：loss += self.entrop_loss_weight * entropy_aux_loss
            loss += self.entrop_loss_weight * entropy_aux_loss

            # 中文说明：从当前函数返回结果或结束函数执行；代码：return (
            return (
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：z_q,
                z_q,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：loss.unsqueeze(1).unsqueeze(1).unsqueeze(1),
                loss.unsqueeze(1).unsqueeze(1).unsqueeze(1),
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：(
                (
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：indices,
                    indices,
                    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.commitment_loss_weight * commit_loss.mean().detach(),
                    self.commitment_loss_weight * commit_loss.mean().detach(),
                    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.entrop_loss_weight * entropy_aux_loss.mean().detach(),
                    self.entrop_loss_weight * entropy_aux_loss.mean().detach(),
                    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.entrop_loss_weight * per_sample_entropy.mean().detach(),
                    self.entrop_loss_weight * per_sample_entropy.mean().detach(),
                    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.entrop_loss_weight * codebook_entropy.mean().detach(),
                    self.entrop_loss_weight * codebook_entropy.mean().detach(),
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
                ),
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return (
            return (
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：z_q,
                z_q,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：loss.unsqueeze(1).unsqueeze(1).unsqueeze(1),
                loss.unsqueeze(1).unsqueeze(1).unsqueeze(1),
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.commitment_loss_weight * commit_loss.mean().detach(),
                self.commitment_loss_weight * commit_loss.mean().detach(),
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class InvQuantizerJit(nn.Module):
class InvQuantizerJit(nn.Module):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Use for decoder_jit to trace quantizer in discrete tokenizer"""
    """Use for decoder_jit to trace quantizer in discrete tokenizer"""

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, quantizer):
    def __init__(self, quantizer):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.quantizer = quantizer
        self.quantizer = quantizer

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, indices: torch.Tensor):
    def forward(self, indices: torch.Tensor):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：codes = self.quantizer.indices_to_codes(indices)
        codes = self.quantizer.indices_to_codes(indices)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return codes.to(self.quantizer.dtype)
        return codes.to(self.quantizer.dtype)
