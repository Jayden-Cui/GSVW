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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from collections.abc import Mapping, Sized
from collections.abc import Mapping, Sized
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Optional
from typing import Optional

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch import nn
from torch import nn

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# from imaginaire.utils import log
# from imaginaire.utils import log

# 中文说明：开始一个可捕获异常的代码块；代码：try:
try:
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import natten
    import natten
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from natten.functional import neighborhood_attention_generic
    from natten.functional import neighborhood_attention_generic

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：natten.use_kv_parallelism_in_fused_na(True)
    natten.use_kv_parallelism_in_fused_na(True)
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：natten.set_memory_usage_preference("unrestricted")
    natten.set_memory_usage_preference("unrestricted")

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：HAS_NATTEN = True
    HAS_NATTEN = True

# 中文说明：处理异常、清理资源或管理上下文；代码：except ImportError:
except ImportError:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：HAS_NATTEN = False
    HAS_NATTEN = False

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def neighborhood_attention_generic(*args, **kwargs):
    def neighborhood_attention_generic(*args, **kwargs):
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise RuntimeError("You attempted to run neighborhood attention, but you don't have NATTEN in...
        raise RuntimeError("You attempted to run neighborhood attention, but you don't have NATTEN installed.")


# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from collections import namedtuple
from collections import namedtuple

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：VideoSize = namedtuple("VideoSize", ["T", "H", "W"])
VideoSize = namedtuple("VideoSize", ["T", "H", "W"])


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class NeighborhoodAttention(nn.Module):
class NeighborhoodAttention(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, gna_parameters, base_attn_op):
    def __init__(self, gna_parameters, base_attn_op):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super(NeighborhoodAttention, self).__init__()
        super(NeighborhoodAttention, self).__init__()

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.base_attn_op = base_attn_op
        self.base_attn_op = base_attn_op

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.gna_parameters = gna_parameters
        self.gna_parameters = gna_parameters
        # 中文说明：根据条件选择执行分支；代码：if (
        if (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：not isinstance(gna_parameters, Mapping)
            not isinstance(gna_parameters, Mapping)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：or "window_size" not in gna_parameters
            or "window_size" not in gna_parameters
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：or "stride" not in gna_parameters
            or "stride" not in gna_parameters
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
        ):
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(
            raise ValueError(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："Expected `gna_parameters` to be a dict with keys window_size " f"and stride, got {gna_parame...
                "Expected `gna_parameters` to be a dict with keys window_size " f"and stride, got {gna_parameters=}."
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.natten_window_size = gna_parameters["window_size"]
        self.natten_window_size = gna_parameters["window_size"]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.natten_stride = gna_parameters["stride"]
        self.natten_stride = gna_parameters["stride"]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.natten_base_size = None if "base_size" not in gna_parameters else gna_parameters["base_s...
        self.natten_base_size = None if "base_size" not in gna_parameters else gna_parameters["base_size"]

        # 中文说明：根据条件选择执行分支；代码：if not isinstance(self.natten_window_size, Sized) or len(self.natten_window_size) != 3:
        if not isinstance(self.natten_window_size, Sized) or len(self.natten_window_size) != 3:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(
            raise ValueError(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："Invalid window_size value. Expected an iterable of length 3, got " f"{self.natten_window_siz...
                "Invalid window_size value. Expected an iterable of length 3, got " f"{self.natten_window_size}."
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：根据条件选择执行分支；代码：if (not isinstance(self.natten_stride, Sized) or len(self.natten_stride) != 3) and not isinst...
        if (not isinstance(self.natten_stride, Sized) or len(self.natten_stride) != 3) and not isinstance(
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.natten_stride, int
            self.natten_stride, int
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
        ):
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(
            raise ValueError(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："Invalid stride value. Expected an iterable of length 3, or integer, got " f"{self.natten_str...
                "Invalid stride value. Expected an iterable of length 3, or integer, got " f"{self.natten_stride}."
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：根据条件选择执行分支；代码：if self.natten_base_size is not None and (
        if self.natten_base_size is not None and (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：not isinstance(self.natten_base_size, Sized) or len(self.natten_base_size) != 3
            not isinstance(self.natten_base_size, Sized) or len(self.natten_base_size) != 3
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
        ):
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(
            raise ValueError(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："Invalid base feature map size. Expected an iterable of length 3, or None, got "
                "Invalid base feature map size. Expected an iterable of length 3, or None, got "
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"{self.natten_base_size}."
                f"{self.natten_base_size}."
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Flex can be faster with multi-dim tiling, but it's buggy...
        # Flex can be faster with multi-dim tiling, but it's buggy...
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.backend = "fna" # Choices (as of natten v0.20.0.dev0): fna, fna-blackwell, flex
        self.backend = "fna"  # Choices (as of natten v0.20.0.dev0): fna, fna-blackwell, flex

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Kernel configurations
        # Kernel configurations

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.q_tile_shape = None
        self.q_tile_shape = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.kv_tile_shape = None
        self.kv_tile_shape = None
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self.q_tile_shape = (4, 4, 4)
        # self.q_tile_shape = (4, 4, 4)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self.kv_tile_shape = (4, 4, 4)
        # self.kv_tile_shape = (4, 4, 4)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.backward_q_tile_shape = None # fna only
        self.backward_q_tile_shape = None  # fna only
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.backward_kv_tile_shape = None # fna only
        self.backward_kv_tile_shape = None  # fna only
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.backward_kv_splits = None # fna only
        self.backward_kv_splits = None  # fna only
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.backward_use_pt_reduction = False # fna only
        self.backward_use_pt_reduction = False  # fna only

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.run_persistent_kernel = True # blackwell-fna only
        self.run_persistent_kernel = True  # blackwell-fna only

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(
    def forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q_B_L_H_D: torch.Tensor,
        q_B_L_H_D: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k_B_L_H_D: torch.Tensor,
        k_B_L_H_D: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v_B_L_H_D: torch.Tensor,
        v_B_L_H_D: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video_size: Optional[VideoSize] = None,
        video_size: Optional[VideoSize] = None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：根据条件选择执行分支；代码：if not (q_B_L_H_D.shape == k_B_L_H_D.shape == v_B_L_H_D.shape):
        if not (q_B_L_H_D.shape == k_B_L_H_D.shape == v_B_L_H_D.shape):
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(
            raise ValueError(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："NATTEN requires QKV shapes to match, got "
                "NATTEN requires QKV shapes to match, got "
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"{q_B_L_H_D.shape=}, {k_B_L_H_D.shape=}, {v_B_L_H_D.shape=}."
                f"{q_B_L_H_D.shape=}, {k_B_L_H_D.shape=}, {v_B_L_H_D.shape=}."
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：batch, seqlen, heads, head_dim = q_B_L_H_D.shape
        batch, seqlen, heads, head_dim = q_B_L_H_D.shape
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：T, H, W = video_size
        T, H, W = video_size

        # 中文说明：根据条件选择执行分支；代码：if seqlen != T * H * W:
        if seqlen != T * H * W:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError("Mismatch between seqlen and video_size dimensions; got " f"{video_size=}, {...
            raise ValueError("Mismatch between seqlen and video_size dimensions; got " f"{video_size=}, {seqlen=}.")

        # 中文说明：根据条件选择执行分支；代码：if T > 1:
        if T > 1:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# assert T in [20, 24]
            # assert T in [20, 24]

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_shape = (T, H, W)
            input_shape = (T, H, W)

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 720p
            # 720p
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# window_size = (T, 12, 24)
            # window_size = (T, 12, 24)
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# stride = (1, 4, 8)
            # stride = (1, 4, 8)

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 480p
            # 480p
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# window_size = (T, 12, 16)
            # window_size = (T, 12, 16)
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# stride = (1, 4, 16)
            # stride = (1, 4, 16)

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：window_size = tuple(w if w > 1 else x for x, w in zip(input_shape, self.natten_window_size))
            window_size = tuple(w if w > 1 else x for x, w in zip(input_shape, self.natten_window_size))
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stride = (
            stride = (
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：tuple(self.natten_stride for _ in range(3))
                tuple(self.natten_stride for _ in range(3))
                # 中文说明：根据条件选择执行分支；代码：if isinstance(self.natten_stride, int)
                if isinstance(self.natten_stride, int)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：else tuple(x for x in self.natten_stride)
                else tuple(x for x in self.natten_stride)
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Scale window size and stride according to some base input size
            # Scale window size and stride according to some base input size
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# For example, if window size is (8, 8, 8), stride is (1, 2, 2), for a base
            # For example, if window size is (8, 8, 8), stride is (1, 2, 2), for a base
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# input/feature map size of (16, 16, 16); then if the input feat map in this iteration
            # input/feature map size of (16, 16, 16); then if the input feat map in this iteration
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# has shape (8, 8, 8), we should use window size (4, 4, 4), and stride (1, 1, 1).
            # has shape (8, 8, 8), we should use window size (4, 4, 4), and stride (1, 1, 1).
            # 中文说明：根据条件选择执行分支；代码：if self.natten_base_size is not None:
            if self.natten_base_size is not None:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：base_shape = tuple(b if b > 0 else x for x, b in zip(input_shape, self.natten_base_size))
                base_shape = tuple(b if b > 0 else x for x, b in zip(input_shape, self.natten_base_size))

                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scale = tuple(x / b for x, b in zip(input_shape, base_shape))
                scale = tuple(x / b for x, b in zip(input_shape, base_shape))

                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scaled_window_size = tuple(
                scaled_window_size = tuple(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：min(max(2, round(w * s)), x) for w, s, x in zip(window_size, scale, input_shape)
                    min(max(2, round(w * s)), x) for w, s, x in zip(window_size, scale, input_shape)
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scaled_stride = tuple(
                scaled_stride = tuple(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：min(max(1, round(st * s)), w) for w, s, st in zip(scaled_window_size, scale, stride)
                    min(max(1, round(st * s)), w) for w, s, st in zip(scaled_window_size, scale, stride)
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )

                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：window_size = scaled_window_size
                window_size = scaled_window_size
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stride = scaled_stride
                stride = scaled_stride

            # 中文说明：检查运行时假设是否成立；代码：assert all(x >= w for x, w in zip(input_shape, window_size))
            assert all(x >= w for x, w in zip(input_shape, window_size))
            # 中文说明：检查运行时假设是否成立；代码：assert all(w >= s for w, s in zip(window_size, stride))
            assert all(w >= s for w, s in zip(window_size, stride))

        # 中文说明：根据条件选择执行分支；代码：elif T == 1:
        elif T == 1:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Do self attention for image model
            # Do self attention for image model
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.base_attn_op(q_B_L_H_D, k_B_L_H_D, v_B_L_H_D)
            return self.base_attn_op(q_B_L_H_D, k_B_L_H_D, v_B_L_H_D)

        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Invalid dimension {T=}.")
            raise ValueError(f"Invalid dimension {T=}.")

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dilation = 1 # = (1, 1, 1)
        dilation = 1  # = (1, 1, 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：causal = False # = (False, False, False)
        causal = False  # = (False, False, False)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q = q_B_L_H_D.view(batch, *input_shape, heads, head_dim)
        q = q_B_L_H_D.view(batch, *input_shape, heads, head_dim)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：k = k_B_L_H_D.view(batch, *input_shape, heads, head_dim)
        k = k_B_L_H_D.view(batch, *input_shape, heads, head_dim)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：v = v_B_L_H_D.view(batch, *input_shape, heads, head_dim)
        v = v_B_L_H_D.view(batch, *input_shape, heads, head_dim)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# log.debug(
        # log.debug(
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# f"Running neighborhood attention on qkv.shape={q.shape} ({input_shape=}), "
        #     f"Running neighborhood attention on qkv.shape={q.shape} ({input_shape=}), "
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# f"{window_size=}, {stride=}, {dilation=}, {causal=}, "
        #     f"{window_size=}, {stride=}, {dilation=}, {causal=}, "
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# f"q_tile_shape={self.q_tile_shape}, kv_tile_shape={self.kv_tile_shape}, backend={self.backe...
        #     f"q_tile_shape={self.q_tile_shape}, kv_tile_shape={self.kv_tile_shape}, backend={self.backend}."
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# )
        # )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out = neighborhood_attention_generic(
        out = neighborhood_attention_generic(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：query=q,
            query=q,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：key=k,
            key=k,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：value=v,
            value=v,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kernel_size=window_size,
            kernel_size=window_size,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stride=stride,
            stride=stride,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dilation=dilation,
            dilation=dilation,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_causal=causal,
            is_causal=causal,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend=self.backend,
            backend=self.backend,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q_tile_shape=self.q_tile_shape,
            q_tile_shape=self.q_tile_shape,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kv_tile_shape=self.kv_tile_shape,
            kv_tile_shape=self.kv_tile_shape,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backward_q_tile_shape=self.backward_q_tile_shape,
            backward_q_tile_shape=self.backward_q_tile_shape,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backward_kv_tile_shape=self.backward_kv_tile_shape,
            backward_kv_tile_shape=self.backward_kv_tile_shape,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backward_kv_splits=self.backward_kv_splits,
            backward_kv_splits=self.backward_kv_splits,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backward_use_pt_reduction=self.backward_use_pt_reduction,
            backward_use_pt_reduction=self.backward_use_pt_reduction,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：run_persistent_kernel=self.run_persistent_kernel,
            run_persistent_kernel=self.run_persistent_kernel,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return out.view(batch, seqlen, heads, head_dim)
        return out.view(batch, seqlen, heads, head_dim)
