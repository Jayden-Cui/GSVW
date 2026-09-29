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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch import nn, einsum, Tensor
from torch import nn, einsum, Tensor
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Union, Tuple, Optional, List
from typing import  Union, Tuple, Optional, List
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import math
import math

# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class PositionEmbeddingRandom(nn.Module):
class PositionEmbeddingRandom(nn.Module):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Positional encoding using random spatial frequencies.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, num_pos_feats: int = 64, scale: Optional[float] = None) -> None:
    def __init__(self, num_pos_feats: int = 64, scale: Optional[float] = None) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：根据条件选择执行分支；代码：if scale is None or scale <= 0.0:
        if scale is None or scale <= 0.0:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scale = 1.0
            scale = 1.0
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.register_buffer(
        self.register_buffer(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："positional_encoding_gaussian_matrix",
            "positional_encoding_gaussian_matrix",
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scale * torch.randn((2, num_pos_feats)),
            scale * torch.randn((2, num_pos_feats)),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _pe_encoding(self, coords: torch.Tensor) -> torch.Tensor:
    def _pe_encoding(self, coords: torch.Tensor) -> torch.Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Positionally encode points that are normalized to [0,1]."""
        """Positionally encode points that are normalized to [0,1]."""
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# assuming coords are in [0, 1]^2 square and have d_1 x ... x d_n x 2 shape
        # assuming coords are in [0, 1]^2 square and have d_1 x ... x d_n x 2 shape
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：coords = 2 * coords - 1
        coords = 2 * coords - 1

        # 中文说明：根据条件选择执行分支；代码：if coords.dtype != self.positional_encoding_gaussian_matrix.dtype:
        if coords.dtype != self.positional_encoding_gaussian_matrix.dtype:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：coords = coords.to(self.positional_encoding_gaussian_matrix.dtype)
            coords = coords.to(self.positional_encoding_gaussian_matrix.dtype)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：coords = coords @ self.positional_encoding_gaussian_matrix
        coords = coords @ self.positional_encoding_gaussian_matrix
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：coords = 2 * np.pi * coords
        coords = 2 * np.pi * coords
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# outputs d_1 x ... x d_n x C shape
        # outputs d_1 x ... x d_n x C shape
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return torch.cat([torch.sin(coords), torch.cos(coords)], dim=-1)
        return torch.cat([torch.sin(coords), torch.cos(coords)], dim=-1)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, size: Tuple[int, int]) -> torch.Tensor:
    def forward(self, size: Tuple[int, int]) -> torch.Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Generate positional encoding for a grid of the specified size."""
        """Generate positional encoding for a grid of the specified size."""
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：h, w = size
        h, w = size
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：device = self.positional_encoding_gaussian_matrix.device
        device = self.positional_encoding_gaussian_matrix.device
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：grid = torch.ones(
        grid = torch.ones(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：(h, w), device=device, dtype=self.positional_encoding_gaussian_matrix.dtype
            (h, w), device=device, dtype=self.positional_encoding_gaussian_matrix.dtype
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：y_embed = grid.cumsum(dim=0) - 0.5
        y_embed = grid.cumsum(dim=0) - 0.5
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_embed = grid.cumsum(dim=1) - 0.5
        x_embed = grid.cumsum(dim=1) - 0.5
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：y_embed = y_embed / h
        y_embed = y_embed / h
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_embed = x_embed / w
        x_embed = x_embed / w

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pe = self._pe_encoding(torch.stack([x_embed, y_embed], dim=-1))
        pe = self._pe_encoding(torch.stack([x_embed, y_embed], dim=-1))
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return pe.permute(2, 0, 1) # C x H x W
        return pe.permute(2, 0, 1)  # C x H x W

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward_with_coords(
    def forward_with_coords(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, coords_input: torch.Tensor, image_size: Tuple[int, int]
        self, coords_input: torch.Tensor, image_size: Tuple[int, int]
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor:
    ) -> torch.Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Positionally encode points that are not normalized to [0,1]."""
        """Positionally encode points that are not normalized to [0,1]."""
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：coords = coords_input.clone()
        coords = coords_input.clone()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：coords[:, :, 0] = coords[:, :, 0] / image_size[1]
        coords[:, :, 0] = coords[:, :, 0] / image_size[1]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：coords[:, :, 1] = coords[:, :, 1] / image_size[0]
        coords[:, :, 1] = coords[:, :, 1] / image_size[0]
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self._pe_encoding(coords.to(torch.float)) # B x N x C
        return self._pe_encoding(coords.to(torch.float))  # B x N x C


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Attention(nn.Module):
class Attention(nn.Module):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    An attention layer that allows for downscaling the size of the embedding
    after projection to queries, keys, and values.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：embedding_dim: int,
        embedding_dim: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_heads: int,
        num_heads: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：downsample_rate: int = 1,
        downsample_rate: int = 1,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.embedding_dim = embedding_dim
        self.embedding_dim = embedding_dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.internal_dim = embedding_dim // downsample_rate
        self.internal_dim = embedding_dim // downsample_rate
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_heads = num_heads
        self.num_heads = num_heads
        # 中文说明：检查运行时假设是否成立；代码：assert (
        assert (
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.internal_dim % num_heads == 0
            self.internal_dim % num_heads == 0
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), "num_heads must divide embedding_dim."
        ), "num_heads must divide embedding_dim."

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.q_proj = nn.Linear(embedding_dim, self.internal_dim)
        self.q_proj = nn.Linear(embedding_dim, self.internal_dim)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.k_proj = nn.Linear(embedding_dim, self.internal_dim)
        self.k_proj = nn.Linear(embedding_dim, self.internal_dim)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.v_proj = nn.Linear(embedding_dim, self.internal_dim)
        self.v_proj = nn.Linear(embedding_dim, self.internal_dim)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.out_proj = nn.Linear(self.internal_dim, embedding_dim)
        self.out_proj = nn.Linear(self.internal_dim, embedding_dim)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _separate_heads(self, x: Tensor, num_heads: int) -> Tensor:
    def _separate_heads(self, x: Tensor, num_heads: int) -> Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：b, n, c = x.shape
        b, n, c = x.shape
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = x.reshape(b, n, num_heads, c // num_heads)
        x = x.reshape(b, n, num_heads, c // num_heads)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x.transpose(1, 2) # B x N_heads x N_tokens x C_per_head
        return x.transpose(1, 2)  # B x N_heads x N_tokens x C_per_head

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _recombine_heads(self, x: Tensor) -> Tensor:
    def _recombine_heads(self, x: Tensor) -> Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：b, n_heads, n_tokens, c_per_head = x.shape
        b, n_heads, n_tokens, c_per_head = x.shape
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = x.transpose(1, 2)
        x = x.transpose(1, 2)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x.reshape(b, n_tokens, n_heads * c_per_head) # B x N_tokens x C
        return x.reshape(b, n_tokens, n_heads * c_per_head)  # B x N_tokens x C

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, q: Tensor, k: Tensor, v: Tensor) -> Tensor:
    def forward(self, q: Tensor, k: Tensor, v: Tensor) -> Tensor:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Input projections
        # Input projections
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q = self.q_proj(q)
        q = self.q_proj(q)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：k = self.k_proj(k)
        k = self.k_proj(k)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：v = self.v_proj(v)
        v = self.v_proj(v)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Separate into heads
        # Separate into heads
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q = self._separate_heads(q, self.num_heads)
        q = self._separate_heads(q, self.num_heads)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：k = self._separate_heads(k, self.num_heads)
        k = self._separate_heads(k, self.num_heads)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：v = self._separate_heads(v, self.num_heads)
        v = self._separate_heads(v, self.num_heads)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Attention
        # Attention
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_, _, _, c_per_head = q.shape
        _, _, _, c_per_head = q.shape
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn = q @ k.permute(0, 1, 3, 2) # B x N_heads x N_tokens x N_tokens
        attn = q @ k.permute(0, 1, 3, 2)  # B x N_heads x N_tokens x N_tokens
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn = attn / math.sqrt(c_per_head)
        attn = attn / math.sqrt(c_per_head)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn = torch.softmax(attn, dim=-1)
        attn = torch.softmax(attn, dim=-1)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Get output
        # Get output
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out = attn @ v
        out = attn @ v
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out = self._recombine_heads(out)
        out = self._recombine_heads(out)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out = self.out_proj(out)
        out = self.out_proj(out)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return out
        return out

# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class MLPBlock(nn.Module):
class MLPBlock(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：embedding_dim: int,
        embedding_dim: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：mlp_dim: int,
        mlp_dim: int,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：act = nn.GELU,
        act  = nn.GELU,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.lin1 = nn.Linear(embedding_dim, mlp_dim)
        self.lin1 = nn.Linear(embedding_dim, mlp_dim)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.lin2 = nn.Linear(mlp_dim, embedding_dim)
        self.lin2 = nn.Linear(mlp_dim, embedding_dim)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.act = act()
        self.act = act()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x: torch.Tensor) -> torch.Tensor:
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.lin2(self.act(self.lin1(x)))
        return self.lin2(self.act(self.lin1(x)))


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class AttentionBlock(nn.Module):
class AttentionBlock(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：embedding_dim: int,
        embedding_dim: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_heads: int,
        num_heads: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：mlp_dim: int = 2048,
        mlp_dim: int = 2048,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：activation = nn.ReLU,
        activation = nn.ReLU,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：attention_downsample_rate: int = 2,
        attention_downsample_rate: int = 2,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：skip_first_layer_pe: bool = False,
        skip_first_layer_pe: bool = False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self.norm1 = nn.LayerNorm(embedding_dim)
        # self.norm1 = nn.LayerNorm(embedding_dim)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.cross_attn_token_to_image = Attention(
        self.cross_attn_token_to_image = Attention(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：embedding_dim, num_heads, downsample_rate=attention_downsample_rate
                embedding_dim, num_heads, downsample_rate=attention_downsample_rate
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.norm2 = nn.LayerNorm(embedding_dim)
        self.norm2 = nn.LayerNorm(embedding_dim)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mlp = MLPBlock(embedding_dim, mlp_dim, activation)
        self.mlp = MLPBlock(embedding_dim, mlp_dim, activation)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.norm3 = nn.LayerNorm(embedding_dim)
        self.norm3 = nn.LayerNorm(embedding_dim)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, queries: Tensor, keys: Tensor, key_pe: Tensor):
    def forward(self, queries: Tensor, keys: Tensor, key_pe: Tensor):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：k = keys + key_pe
        k = keys + key_pe
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q = queries
        q = queries
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn_out = self.cross_attn_token_to_image(q=q, k=k, v=keys)
        attn_out = self.cross_attn_token_to_image(q=q, k=k, v=keys)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：queries = queries + attn_out
        queries = queries + attn_out
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：queries = self.norm2(queries)
        queries = self.norm2(queries)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mlp_out = self.mlp(queries)
        mlp_out = self.mlp(queries)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：queries = queries + mlp_out
        queries = queries + mlp_out
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：queries = self.norm3(queries)
        queries = self.norm3(queries)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return queries, keys
        return queries, keys
        

# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class QFormer(nn.Module):
class QFormer(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, depth: int,
    def __init__(self, depth: int,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：embedding_dim: int,
                embedding_dim: int,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_heads: int,
                num_heads: int,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：mlp_dim: int,
                mlp_dim: int,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：activation = nn.ReLU,
                activation = nn.ReLU,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：attention_downsample_rate: int = 2,
                attention_downsample_rate: int = 2,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
            ):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.depth = depth
        self.depth = depth
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.embedding_dim = embedding_dim
        self.embedding_dim = embedding_dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_heads = num_heads
        self.num_heads = num_heads
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mlp_dim = mlp_dim
        self.mlp_dim = mlp_dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.layers = nn.ModuleList()
        self.layers = nn.ModuleList()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i in range(depth):
        for i in range(depth):
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.layers.append(
            self.layers.append(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：AttentionBlock(
                AttentionBlock(
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：embedding_dim=embedding_dim,
                    embedding_dim=embedding_dim,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_heads=num_heads,
                    num_heads=num_heads,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mlp_dim=mlp_dim,
                    mlp_dim=mlp_dim,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：activation=activation,
                    activation=activation,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attention_downsample_rate=attention_downsample_rate,
                    attention_downsample_rate=attention_downsample_rate,
                    
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.final_attn_token_to_image = Attention(
        self.final_attn_token_to_image = Attention(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：embedding_dim, num_heads, downsample_rate=attention_downsample_rate
            embedding_dim, num_heads, downsample_rate=attention_downsample_rate
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.norm_final_attn = nn.LayerNorm(embedding_dim)
        self.norm_final_attn = nn.LayerNorm(embedding_dim)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(
    def forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：image_embedding: Tensor,
        image_embedding: Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：image_pe: Tensor,
        image_pe: Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：queries: Tensor,
        queries: Tensor,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[Tensor, Tensor]:
    ) -> Tuple[Tensor, Tensor]:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# BxCxHxW -> BxHWxC == B x N_image_tokens x C
        # BxCxHxW -> BxHWxC == B x N_image_tokens x C
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：bs, c, t, h, w = image_embedding.shape
        bs, c, t, h, w = image_embedding.shape
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：image_embedding = image_embedding.flatten(2).permute(0, 2, 1)
        image_embedding = image_embedding.flatten(2).permute(0, 2, 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：image_pe = image_pe.flatten(2).permute(0, 2, 1)
        image_pe = image_pe.flatten(2).permute(0, 2, 1)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Prepare queries
        # Prepare queries
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：keys = image_embedding
        keys = image_embedding

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Apply transformer blocks and final layernorm
        # Apply transformer blocks and final layernorm
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for layer in self.layers:
        for layer in self.layers:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：queries, keys = layer(
            queries, keys = layer(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：queries=queries,
                queries=queries,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：keys=keys,
                keys=keys,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：key_pe=image_pe,
                key_pe=image_pe,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Apply the final attention layer from the points to the image
        # Apply the final attention layer from the points to the image
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q = queries + queries
        q = queries + queries
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：k = keys + image_pe
        k = keys + image_pe
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn_out = self.final_attn_token_to_image(q=q, k=k, v=keys)
        attn_out = self.final_attn_token_to_image(q=q, k=k, v=keys)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：queries = queries + attn_out
        queries = queries + attn_out
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：queries = self.norm_final_attn(queries)
        queries = self.norm_final_attn(queries)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return queries, keys
        return queries, keys


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class QFormerMF(nn.Module):
class QFormerMF(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self,
    def __init__(self, 
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：depth: int,
                depth: int,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：embedding_dim: int,
                embedding_dim: int,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_heads: int,
                num_heads: int,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：mlp_dim: int,
                mlp_dim: int,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：activation = nn.ReLU,
                activation = nn.ReLU,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：qformer_num=1,
                qformer_num=1,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：attention_downsample_rate: int = 2,
                attention_downsample_rate: int = 2,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
            ):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.depth = depth
        self.depth = depth
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.embedding_dim = embedding_dim
        self.embedding_dim = embedding_dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_heads = num_heads
        self.num_heads = num_heads
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mlp_dim = mlp_dim
        self.mlp_dim = mlp_dim
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self.qformer_num = qformer_num
        # self.qformer_num = qformer_num
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self.qformers = nn.ModuleList()
        # self.qformers = nn.ModuleList()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# for _ in range(qformer_num):
        # for _ in range(qformer_num):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.qformer = QFormer(depth, embedding_dim, num_heads, mlp_dim)
        self.qformer = QFormer(depth, embedding_dim, num_heads, mlp_dim)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self.qformers.append(qformer)
        # self.qformers.append(qformer)
     
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(
    def forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：image_embedding: Tensor,
        image_embedding: Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：image_pe: Tensor,
        image_pe: Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：queries: Tensor,
        queries: Tensor,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[Tensor, Tensor]:
    ) -> Tuple[Tensor, Tensor]:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# BxCxHxW -> BxHWxC == B x N_image_tokens x C
        # BxCxHxW -> BxHWxC == B x N_image_tokens x C
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：bs, c, t, h, w = image_embedding.shape
        bs, c, t, h, w = image_embedding.shape
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：act_num = queries.shape[1]
        act_num = queries.shape[1]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_interval = t // act_num
        frame_interval = t // act_num
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：new_queries = []
        new_queries = []
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i in range(act_num):
        for i in range(act_num):
            # 中文说明：根据条件选择执行分支；代码：if t - act_num == 1:
            if t - act_num == 1:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t_num = i + 2
                t_num = i + 2
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t_num = frame_interval * (i + 1)
                t_num = frame_interval * (i + 1) 
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_image_embedding = image_embedding[:, :, :t_num]
            _image_embedding = image_embedding[:, :, :t_num]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_image_pe = image_pe[:, :, :t_num]
            _image_pe = image_pe[:, :, :t_num]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_queries = queries[:, i][:, None]
            _queries = queries[:, i][:, None]
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_queries, _ = self.qformer(_image_embedding, _image_pe, _queries)
            _queries, _ = self.qformer(_image_embedding, _image_pe, _queries)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：new_queries.append(_queries)
            new_queries.append(_queries)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：new_queries = torch.cat(new_queries, dim=1)
        new_queries = torch.cat(new_queries, dim=1)
        
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return new_queries
        return new_queries
    
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class QFormerMFAdjacent(nn.Module):
class QFormerMFAdjacent(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self,
    def __init__(self, 
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：depth: int,
                depth: int,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：embedding_dim: int,
                embedding_dim: int,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_heads: int,
                num_heads: int,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：mlp_dim: int,
                mlp_dim: int,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：activation = nn.ReLU,
                activation = nn.ReLU,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：qformer_num=1,
                qformer_num=1,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：attention_downsample_rate: int = 2,
                attention_downsample_rate: int = 2,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
            ):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.depth = depth
        self.depth = depth
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.embedding_dim = embedding_dim
        self.embedding_dim = embedding_dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_heads = num_heads
        self.num_heads = num_heads
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mlp_dim = mlp_dim
        self.mlp_dim = mlp_dim
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self.qformer_num = qformer_num
        # self.qformer_num = qformer_num
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self.qformers = nn.ModuleList()
        # self.qformers = nn.ModuleList()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# for _ in range(qformer_num):
        # for _ in range(qformer_num):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.qformer = QFormer(depth, embedding_dim, num_heads, mlp_dim)
        self.qformer = QFormer(depth, embedding_dim, num_heads, mlp_dim)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self.qformers.append(qformer)
        # self.qformers.append(qformer)
     
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(
    def forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：image_embedding: Tensor,
        image_embedding: Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：image_pe: Tensor,
        image_pe: Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：queries: Tensor,
        queries: Tensor,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[Tensor, Tensor]:
    ) -> Tuple[Tensor, Tensor]:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# BxCxHxW -> BxHWxC == B x N_image_tokens x C
        # BxCxHxW -> BxHWxC == B x N_image_tokens x C
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：bs, c, t, h, w = image_embedding.shape
        bs, c, t, h, w = image_embedding.shape
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：act_num = queries.shape[1]
        act_num = queries.shape[1]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_interval = t // act_num
        frame_interval = t // act_num
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：new_queries = []
        new_queries = []
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i in range(act_num):
        for i in range(act_num):
            # 中文说明：根据条件选择执行分支；代码：if t - act_num == 1:
            if t - act_num == 1:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t_num = i + 2
                t_num = i + 2
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t_num = frame_interval * (i + 1)
                t_num = frame_interval * (i + 1) 
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_image_embedding = image_embedding[:, :, (t_num-1):t_num]
            _image_embedding = image_embedding[:, :, (t_num-1):t_num]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_image_pe = image_pe[:, :, (t_num-1):t_num]
            _image_pe = image_pe[:, :, (t_num-1):t_num]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_queries = queries[:, i][:, None]
            _queries = queries[:, i][:, None]
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_queries, _ = self.qformer(_image_embedding, _image_pe, _queries)
            _queries, _ = self.qformer(_image_embedding, _image_pe, _queries)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：new_queries.append(_queries)
            new_queries.append(_queries)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：new_queries = torch.cat(new_queries, dim=1)
        new_queries = torch.cat(new_queries, dim=1)
        
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return new_queries
        return new_queries


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class QFormerMFSep(nn.Module):
class QFormerMFSep(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, depth: int,
    def __init__(self, depth: int,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：embedding_dim: int,
                embedding_dim: int,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_heads: int,
                num_heads: int,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：mlp_dim: int,
                mlp_dim: int,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：activation = nn.ReLU,
                activation = nn.ReLU,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：attention_downsample_rate: int = 2,
                attention_downsample_rate: int = 2,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：qformer_num=2,
                qformer_num=2,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
            ):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.depth = depth
        self.depth = depth
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.embedding_dim = embedding_dim
        self.embedding_dim = embedding_dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_heads = num_heads
        self.num_heads = num_heads
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mlp_dim = mlp_dim
        self.mlp_dim = mlp_dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.qformer_num = qformer_num
        self.qformer_num = qformer_num
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.qformers = nn.ModuleList()
        self.qformers = nn.ModuleList()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _ in range(qformer_num):
        for _ in range(qformer_num):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：qformer = QFormer(depth, embedding_dim, num_heads, mlp_dim)
            qformer = QFormer(depth, embedding_dim, num_heads, mlp_dim)
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.qformers.append(qformer)
            self.qformers.append(qformer)
        
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(
    def forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：image_embedding: Tensor,
        image_embedding: Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：image_pe: Tensor,
        image_pe: Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：queries: Tensor,
        queries: Tensor,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[Tensor, Tensor]:
    ) -> Tuple[Tensor, Tensor]:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# BxCxHxW -> BxHWxC == B x N_image_tokens x C
        # BxCxHxW -> BxHWxC == B x N_image_tokens x C
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：bs, c, t, h, w = image_embedding.shape
        bs, c, t, h, w = image_embedding.shape
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：act_num = queries.shape[1]
        act_num = queries.shape[1]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_interval = t // act_num
        frame_interval = t // act_num
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：new_queries = []
        new_queries = []
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i in range(act_num):
        for i in range(act_num):
            # 中文说明：根据条件选择执行分支；代码：if t - act_num == 1:
            if t - act_num == 1:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t_num = i + 2
                t_num = i + 2
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t_num = frame_interval * (i + 1)
                t_num = frame_interval * (i + 1) 
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_image_embedding = image_embedding[:, :, :t_num]
            _image_embedding = image_embedding[:, :, :t_num]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_image_pe = image_pe[:, :, :t_num]
            _image_pe = image_pe[:, :, :t_num]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_queries = queries[:, i][:, None]
            _queries = queries[:, i][:, None]
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_queries, _ = self.qformers[i](_image_embedding, _image_pe, _queries)
            _queries, _ = self.qformers[i](_image_embedding, _image_pe, _queries)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：new_queries.append(_queries)
            new_queries.append(_queries)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：new_queries = torch.cat(new_queries, dim=1)
        new_queries = torch.cat(new_queries, dim=1)
        
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return new_queries
        return new_queries


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class QFormerMFSingleQ(nn.Module):
class QFormerMFSingleQ(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self,
    def __init__(self, 
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：depth: int,
                depth: int,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：embedding_dim: int,
                embedding_dim: int,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_heads: int,
                num_heads: int,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：mlp_dim: int,
                mlp_dim: int,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：activation = nn.ReLU,
                activation = nn.ReLU,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：attention_downsample_rate: int = 2,
                attention_downsample_rate: int = 2,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：act_embedding_num=1,
                act_embedding_num=1,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：qformer_num=1,
                qformer_num=1,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
            ):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.depth = depth
        self.depth = depth
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.embedding_dim = embedding_dim
        self.embedding_dim = embedding_dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_heads = num_heads
        self.num_heads = num_heads
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mlp_dim = mlp_dim
        self.mlp_dim = mlp_dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.qformer = QFormer(depth, embedding_dim, num_heads, mlp_dim)
        self.qformer = QFormer(depth, embedding_dim, num_heads, mlp_dim)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self.qformers = nn.ModuleList()
        # self.qformers = nn.ModuleList()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# for _ in range(qformer_num):
        # for _ in range(qformer_num):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# qformer = QFormer(depth, embedding_dim, num_heads, mlp_dim)
        #     qformer = QFormer(depth, embedding_dim, num_heads, mlp_dim)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self.qformers.append(qformer)
        #     self.qformers.append(qformer)
        
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(
    def forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：image_embedding: Tensor,
        image_embedding: Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：image_pe: Tensor,
        image_pe: Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：queries: Tensor,
        queries: Tensor,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[Tensor, Tensor]:
    ) -> Tuple[Tensor, Tensor]:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# BxCxHxW -> BxHWxC == B x N_image_tokens x C
        # BxCxHxW -> BxHWxC == B x N_image_tokens x C
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：bs, c, t, h, w = image_embedding.shape
        bs, c, t, h, w = image_embedding.shape
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：new_queries = []
        new_queries = []
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i in range(t-1):
        for i in range(t-1):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t_num = i + 2
            t_num = i + 2
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_image_embedding = image_embedding[:, :, :t_num]
            _image_embedding = image_embedding[:, :, :t_num]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_image_pe = image_pe[:, :, :t_num]
            _image_pe = image_pe[:, :, :t_num]
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_queries, _ = self.qformer(_image_embedding, _image_pe, queries)
            _queries, _ = self.qformer(_image_embedding, _image_pe, queries)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：new_queries.append(_queries)
            new_queries.append(_queries)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：new_queries = torch.cat(new_queries, dim=1)
        new_queries = torch.cat(new_queries, dim=1)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return new_queries
        return new_queries
        
        
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class QFormerAdjacentFSingleQ(nn.Module):
class QFormerAdjacentFSingleQ(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self,
    def __init__(self, 
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：depth: int,
                depth: int,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：embedding_dim: int,
                embedding_dim: int,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_heads: int,
                num_heads: int,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：mlp_dim: int,
                mlp_dim: int,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：activation = nn.ReLU,
                activation = nn.ReLU,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：attention_downsample_rate: int = 2,
                attention_downsample_rate: int = 2,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：qformer_num=1
                qformer_num=1
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
            ):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.depth = depth
        self.depth = depth
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.embedding_dim = embedding_dim
        self.embedding_dim = embedding_dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_heads = num_heads
        self.num_heads = num_heads
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mlp_dim = mlp_dim
        self.mlp_dim = mlp_dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.qformer = QFormer(depth, embedding_dim, num_heads, mlp_dim)
        self.qformer = QFormer(depth, embedding_dim, num_heads, mlp_dim)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self.qformers = nn.ModuleList()
        # self.qformers = nn.ModuleList()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# for _ in range(qformer_num):
        # for _ in range(qformer_num):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# qformer = QFormer(depth, embedding_dim, num_heads, mlp_dim)
        #     qformer = QFormer(depth, embedding_dim, num_heads, mlp_dim)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self.qformers.append(qformer)
        #     self.qformers.append(qformer)
        
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(
    def forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：image_embedding: Tensor,
        image_embedding: Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：image_pe: Tensor,
        image_pe: Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：queries: Tensor,
        queries: Tensor,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[Tensor, Tensor]:
    ) -> Tuple[Tensor, Tensor]:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# BxCxHxW -> BxHWxC == B x N_image_tokens x C
        # BxCxHxW -> BxHWxC == B x N_image_tokens x C
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：bs, c, t, h, w = image_embedding.shape
        bs, c, t, h, w = image_embedding.shape
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：new_queries = []
        new_queries = []
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i in range(t-1):
        for i in range(t-1):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t_num = i + 2
            t_num = i + 2
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_image_embedding = image_embedding[:, :, t_num-2:t_num]
            _image_embedding = image_embedding[:, :, t_num-2:t_num]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_image_pe = image_pe[:, :, t_num-2:t_num]
            _image_pe = image_pe[:, :, t_num-2:t_num]
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_queries, _ = self.qformer(_image_embedding, _image_pe, queries)
            _queries, _ = self.qformer(_image_embedding, _image_pe, queries)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：new_queries.append(_queries)
            new_queries.append(_queries)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：new_queries = torch.cat(new_queries, dim=1)
        new_queries = torch.cat(new_queries, dim=1)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return new_queries
        return new_queries