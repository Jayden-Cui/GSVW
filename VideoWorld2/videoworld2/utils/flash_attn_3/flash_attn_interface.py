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
Copied from flash-attention repository, with necessary modifications to register FA3 as PyTorch operation.
It's requires to use FA3 with Selective Activation Checkpointing.
Original source: https://github.com/Dao-AILab/flash-attention/blob/27f501dbe011f4371bff938fe7e09311ab3002fa/hopper/flash_attn_interface.py
Used to build docker images with FA3 support.
Refer to projects.cosmos.diffusion.v2.docker.README.md for details.
"""

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Optional, Tuple, Union
from typing import Optional, Tuple, Union

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# isort: off
# isort: off
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# We need to import the CUDA kernels after importing torch
# We need to import the CUDA kernels after importing torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import flash_attn_3_cuda
import flash_attn_3_cuda

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# isort: on
# isort: on


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def maybe_contiguous(x):
def maybe_contiguous(x):
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return x.contiguous() if x is not None and x.stride(-1) != 1 else x
    return x.contiguous() if x is not None and x.stride(-1) != 1 else x


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.library.custom_op("flash_attn_3::_flash_attn_forward", mutates_args=(), device_types="...
@torch.library.custom_op("flash_attn_3::_flash_attn_forward", mutates_args=(), device_types="cuda")
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _flash_attn_forward(
def _flash_attn_forward(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q: torch.Tensor,
    q: torch.Tensor,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k: torch.Tensor,
    k: torch.Tensor,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v: torch.Tensor,
    v: torch.Tensor,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k_new: Optional[torch.Tensor],
    k_new: Optional[torch.Tensor],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v_new: Optional[torch.Tensor],
    v_new: Optional[torch.Tensor],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：qv: Optional[torch.Tensor],
    qv: Optional[torch.Tensor],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out: Optional[torch.Tensor],
    out: Optional[torch.Tensor],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cu_seqlens_q: Optional[torch.Tensor],
    cu_seqlens_q: Optional[torch.Tensor],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cu_seqlens_k: Optional[torch.Tensor],
    cu_seqlens_k: Optional[torch.Tensor],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cu_seqlens_k_new: Optional[torch.Tensor],
    cu_seqlens_k_new: Optional[torch.Tensor],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：seqused_q: Optional[torch.Tensor],
    seqused_q: Optional[torch.Tensor],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：seqused_k: Optional[torch.Tensor],
    seqused_k: Optional[torch.Tensor],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_seqlen_q: Optional[int],
    max_seqlen_q: Optional[int],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_seqlen_k: Optional[int],
    max_seqlen_k: Optional[int],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：page_table: Optional[torch.Tensor],
    page_table: Optional[torch.Tensor],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：kv_batch_idx: Optional[torch.Tensor],
    kv_batch_idx: Optional[torch.Tensor],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：leftpad_k: Optional[torch.Tensor],
    leftpad_k: Optional[torch.Tensor],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rotary_cos: Optional[torch.Tensor],
    rotary_cos: Optional[torch.Tensor],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rotary_sin: Optional[torch.Tensor],
    rotary_sin: Optional[torch.Tensor],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q_descale: Optional[torch.Tensor],
    q_descale: Optional[torch.Tensor],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k_descale: Optional[torch.Tensor],
    k_descale: Optional[torch.Tensor],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v_descale: Optional[torch.Tensor],
    v_descale: Optional[torch.Tensor],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：softmax_scale: Optional[float],
    softmax_scale: Optional[float],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：causal: bool,
    causal: bool,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：window_size_left: int,
    window_size_left: int,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：window_size_right: int,
    window_size_right: int,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：softcap: float = 0.0,
    softcap: float = 0.0,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rotary_interleaved: bool = True,
    rotary_interleaved: bool = True,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scheduler_metadata: Optional[torch.Tensor] = None,
    scheduler_metadata: Optional[torch.Tensor] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_splits: int = 1,
    num_splits: int = 1,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pack_gqa: Optional[bool] = None,
    pack_gqa: Optional[bool] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sm_margin: int = 0,
    sm_margin: int = 0,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q, k, k_new, v_new = [maybe_contiguous(x) for x in (q, k, k_new, v_new)]
    q, k, k_new, v_new = [maybe_contiguous(x) for x in (q, k, k_new, v_new)]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：v = v.contiguous() if v.stride(-1) != 1 and v.stride(-3) != 1 else v
    v = v.contiguous() if v.stride(-1) != 1 and v.stride(-3) != 1 else v
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cu_seqlens_q, cu_seqlens_k, cu_seqlens_k_new = [
    cu_seqlens_q, cu_seqlens_k, cu_seqlens_k_new = [
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：maybe_contiguous(x) for x in (cu_seqlens_q, cu_seqlens_k, cu_seqlens_k_new)
        maybe_contiguous(x) for x in (cu_seqlens_q, cu_seqlens_k, cu_seqlens_k_new)
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
    ]
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：seqused_q, seqused_k = [maybe_contiguous(x) for x in (seqused_q, seqused_k)]
    seqused_q, seqused_k = [maybe_contiguous(x) for x in (seqused_q, seqused_k)]
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：page_table, kv_batch_idx, leftpad_k = [maybe_contiguous(x) for x in (page_table, kv_batch_idx...
    page_table, kv_batch_idx, leftpad_k = [maybe_contiguous(x) for x in (page_table, kv_batch_idx, leftpad_k)]
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rotary_cos, rotary_sin = [maybe_contiguous(x) for x in (rotary_cos, rotary_sin)]
    rotary_cos, rotary_sin = [maybe_contiguous(x) for x in (rotary_cos, rotary_sin)]
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out, softmax_lse, *rest = flash_attn_3_cuda.fwd(
    out, softmax_lse, *rest = flash_attn_3_cuda.fwd(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q,
        q,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k,
        k,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v,
        v,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k_new,
        k_new,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v_new,
        v_new,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：qv,
        qv,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out,
        out,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cu_seqlens_q,
        cu_seqlens_q,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cu_seqlens_k,
        cu_seqlens_k,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cu_seqlens_k_new,
        cu_seqlens_k_new,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：seqused_q,
        seqused_q,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：seqused_k,
        seqused_k,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_seqlen_q,
        max_seqlen_q,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_seqlen_k,
        max_seqlen_k,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：page_table,
        page_table,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：kv_batch_idx,
        kv_batch_idx,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：leftpad_k,
        leftpad_k,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rotary_cos,
        rotary_cos,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rotary_sin,
        rotary_sin,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q_descale,
        q_descale,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k_descale,
        k_descale,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v_descale,
        v_descale,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：softmax_scale,
        softmax_scale,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：causal,
        causal,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：window_size_left,
        window_size_left,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：window_size_right,
        window_size_right,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：softcap,
        softcap,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rotary_interleaved,
        rotary_interleaved,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scheduler_metadata,
        scheduler_metadata,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_splits,
        num_splits,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pack_gqa,
        pack_gqa,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sm_margin,
        sm_margin,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return out, softmax_lse, *rest
    return out, softmax_lse, *rest


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _flash_attn_backward(
def _flash_attn_backward(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dout,
    dout,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q,
    q,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k,
    k,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v,
    v,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out,
    out,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：softmax_lse,
    softmax_lse,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cu_seqlens_q,
    cu_seqlens_q,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cu_seqlens_k,
    cu_seqlens_k,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sequed_q,
    sequed_q,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sequed_k,
    sequed_k,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_seqlen_q,
    max_seqlen_q,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_seqlen_k,
    max_seqlen_k,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dq,
    dq,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dk,
    dk,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dv,
    dv,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：softmax_scale,
    softmax_scale,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：causal,
    causal,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：window_size_left,
    window_size_left,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：window_size_right,
    window_size_right,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：softcap=0.0,
    softcap=0.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：deterministic=False,
    deterministic=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sm_margin=0,
    sm_margin=0,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# dq, dk, dv are allocated by us so they should already be contiguous
    # dq, dk, dv are allocated by us so they should already be contiguous
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dout, q, k, v, out = [maybe_contiguous(x) for x in (dout, q, k, v, out)]
    dout, q, k, v, out = [maybe_contiguous(x) for x in (dout, q, k, v, out)]
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dq, dk, dv, softmax_d, *rest = flash_attn_3_cuda.bwd(
    dq, dk, dv, softmax_d, *rest = flash_attn_3_cuda.bwd(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dout,
        dout,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q,
        q,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k,
        k,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v,
        v,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out,
        out,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：softmax_lse,
        softmax_lse,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dq,
        dq,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dk,
        dk,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dv,
        dv,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cu_seqlens_q,
        cu_seqlens_q,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cu_seqlens_k,
        cu_seqlens_k,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sequed_q,
        sequed_q,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sequed_k,
        sequed_k,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_seqlen_q,
        max_seqlen_q,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_seqlen_k,
        max_seqlen_k,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：softmax_scale,
        softmax_scale,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：causal,
        causal,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：window_size_left,
        window_size_left,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：window_size_right,
        window_size_right,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：softcap,
        softcap,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：deterministic,
        deterministic,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sm_margin,
        sm_margin,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return dq, dk, dv, softmax_d
    return dq, dk, dv, softmax_d


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class FlashAttnQKVPackedFunc(torch.autograd.Function):
class FlashAttnQKVPackedFunc(torch.autograd.Function):
    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(
    def forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx,
        ctx,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：qkv,
        qkv,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：softmax_scale,
        softmax_scale,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：causal,
        causal,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q_descale=None,
        q_descale=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：k_descale=None,
        k_descale=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：v_descale=None,
        v_descale=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：window_size=(-1, -1),
        window_size=(-1, -1),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：softcap=0.0,
        softcap=0.0,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：deterministic=False,
        deterministic=False,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_heads_q=None,
        num_heads_q=None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：根据条件选择执行分支；代码：if softmax_scale is None:
        if softmax_scale is None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：softmax_scale = qkv.shape[-1] ** (-0.5)
            softmax_scale = qkv.shape[-1] ** (-0.5)
        # 中文说明：根据条件选择执行分支；代码：if qkv.dim() == 5:
        if qkv.dim() == 5:
            # 中文说明：检查运行时假设是否成立；代码：assert qkv.shape[-3] == 3
            assert qkv.shape[-3] == 3
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q, k, v = qkv.unbind(dim=-3)
            q, k, v = qkv.unbind(dim=-3)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：检查运行时假设是否成立；代码：assert qkv.dim() == 4
            assert qkv.dim() == 4
            # 中文说明：检查运行时假设是否成立；代码：assert num_heads_q is not None
            assert num_heads_q is not None
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_heads_k = (qkv.shape[2] - num_heads_q) // 2
            num_heads_k = (qkv.shape[2] - num_heads_q) // 2
            # 中文说明：检查运行时假设是否成立；代码：assert num_heads_k * 2 + num_heads_q == qkv.shape[2]
            assert num_heads_k * 2 + num_heads_q == qkv.shape[2]
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q, k, v = qkv.split([num_heads_q, num_heads_k, num_heads_k], dim=-2)
            q, k, v = qkv.split([num_heads_q, num_heads_k, num_heads_k], dim=-2)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out, q, k, v, out_padded, softmax_lse = _flash_attn_forward(
        out, q, k, v, out_padded, softmax_lse = _flash_attn_forward(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q,
            q,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k,
            k,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v,
            v,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：softmax_scale,
            softmax_scale,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：causal=causal,
            causal=causal,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q_descale=q_descale,
            q_descale=q_descale,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：k_descale=k_descale,
            k_descale=k_descale,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：v_descale=v_descale,
            v_descale=v_descale,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：window_size_left=window_size[0],
            window_size_left=window_size[0],
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：window_size_right=window_size[1],
            window_size_right=window_size[1],
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：softcap=softcap,
            softcap=softcap,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx.save_for_backward(q, k, v, out_padded, softmax_lse)
        ctx.save_for_backward(q, k, v, out_padded, softmax_lse)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctx.softmax_scale = softmax_scale
        ctx.softmax_scale = softmax_scale
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctx.causal = causal
        ctx.causal = causal
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctx.window_size = window_size
        ctx.window_size = window_size
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctx.softcap = softcap
        ctx.softcap = softcap
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctx.deterministic = deterministic
        ctx.deterministic = deterministic
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctx.ndim = qkv.dim()
        ctx.ndim = qkv.dim()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# return out, softmax_lse
        # return out, softmax_lse
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return out
        return out

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def backward(ctx, dout, *args):
    def backward(ctx, dout, *args):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q, k, v, out, softmax_lse = ctx.saved_tensors
        q, k, v, out, softmax_lse = ctx.saved_tensors
        # 中文说明：根据条件选择执行分支；代码：if ctx.ndim == 5:
        if ctx.ndim == 5:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：qkv_shape = q.shape[:-2] + (3, *q.shape[-2:])
            qkv_shape = q.shape[:-2] + (3, *q.shape[-2:])
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dqkv = torch.empty(qkv_shape, dtype=q.dtype, device=q.device)
            dqkv = torch.empty(qkv_shape, dtype=q.dtype, device=q.device)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dq, dk, dv = dqkv.unbind(dim=-3)
            dq, dk, dv = dqkv.unbind(dim=-3)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_heads_q = q.shape[2]
            num_heads_q = q.shape[2]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_heads_k = k.shape[2]
            num_heads_k = k.shape[2]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：qkv_shape = q.shape[:-2] + (num_heads_q + num_heads_k * 2, *q.shape[-1:])
            qkv_shape = q.shape[:-2] + (num_heads_q + num_heads_k * 2, *q.shape[-1:])
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dqkv = torch.empty(qkv_shape, dtype=q.dtype, device=q.device)
            dqkv = torch.empty(qkv_shape, dtype=q.dtype, device=q.device)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dq, dk, dv = dqkv.split([num_heads_q, num_heads_k, num_heads_k], dim=-2)
            dq, dk, dv = dqkv.split([num_heads_q, num_heads_k, num_heads_k], dim=-2)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_flash_attn_backward(
        _flash_attn_backward(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dout,
            dout,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q,
            q,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k,
            k,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v,
            v,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out,
            out,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：softmax_lse,
            softmax_lse,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dq,
            dq,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dk,
            dk,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dv,
            dv,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx.softmax_scale,
            ctx.softmax_scale,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx.causal,
            ctx.causal,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx.window_size[0],
            ctx.window_size[0],
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx.window_size[1],
            ctx.window_size[1],
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx.softcap,
            ctx.softcap,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx.deterministic,
            ctx.deterministic,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dqkv = dqkv[..., : dout.shape[-1]] # We could have padded the head dimension
        dqkv = dqkv[..., : dout.shape[-1]]  # We could have padded the head dimension
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return dqkv, None, None, None, None, None, None, None, None, None, None
        return dqkv, None, None, None, None, None, None, None, None, None, None


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class FlashAttnFunc(torch.autograd.Function):
class FlashAttnFunc(torch.autograd.Function):
    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(
    def forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx,
        ctx,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q,
        q,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k,
        k,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v,
        v,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：softmax_scale,
        softmax_scale,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：causal,
        causal,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：qv=None,
        qv=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q_descale=None,
        q_descale=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：k_descale=None,
        k_descale=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：v_descale=None,
        v_descale=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：window_size=(-1, -1),
        window_size=(-1, -1),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：softcap=0.0,
        softcap=0.0,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_splits=1,
        num_splits=1,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pack_gqa=None,
        pack_gqa=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：deterministic=False,
        deterministic=False,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sm_margin=0,
        sm_margin=0,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：根据条件选择执行分支；代码：if softmax_scale is None:
        if softmax_scale is None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：softmax_scale = (q.shape[-1] + (qv.shape[-1] if qv is not None else 0)) ** (-0.5)
            softmax_scale = (q.shape[-1] + (qv.shape[-1] if qv is not None else 0)) ** (-0.5)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# out, q, k, v, out_padded, softmax_lse = _flash_attn_forward(
        # out, q, k, v, out_padded, softmax_lse = _flash_attn_forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out, softmax_lse, *rest = _flash_attn_forward(
        out, softmax_lse, *rest = _flash_attn_forward(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q,
            q,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k,
            k,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v,
            v,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None, # k_new, v_new
            None,  # k_new, v_new
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：qv, # qv
            qv,  # qv
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None, # out
            None,  # out
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None, # cu_seqlens_q/k/k_new
            None,  # cu_seqlens_q/k/k_new
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None, # seqused_q/k
            None,  # seqused_q/k
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None, # max_seqlen_q/k
            None,  # max_seqlen_q/k
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None, # page_table, kv_batch_idx, leftpad_k,
            None,  # page_table, kv_batch_idx, leftpad_k,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None, # rotary_cos/sin
            None,  # rotary_cos/sin
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q_descale,
            q_descale,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k_descale,
            k_descale,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v_descale,
            v_descale,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：softmax_scale,
            softmax_scale,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：causal=causal,
            causal=causal,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：window_size_left=window_size[0],
            window_size_left=window_size[0],
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：window_size_right=window_size[1],
            window_size_right=window_size[1],
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：softcap=softcap,
            softcap=softcap,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_splits=num_splits,
            num_splits=num_splits,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pack_gqa=pack_gqa,
            pack_gqa=pack_gqa,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sm_margin=sm_margin,
            sm_margin=sm_margin,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# ctx.save_for_backward(q, k, v, out_padded, softmax_lse)
        # ctx.save_for_backward(q, k, v, out_padded, softmax_lse)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx.save_for_backward(q, k, v, out, softmax_lse)
        ctx.save_for_backward(q, k, v, out, softmax_lse)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctx.softmax_scale = softmax_scale
        ctx.softmax_scale = softmax_scale
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctx.causal = causal
        ctx.causal = causal
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctx.window_size = window_size
        ctx.window_size = window_size
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctx.softcap = softcap
        ctx.softcap = softcap
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctx.deterministic = deterministic
        ctx.deterministic = deterministic
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctx.sm_margin = sm_margin
        ctx.sm_margin = sm_margin
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return out, softmax_lse
        return out, softmax_lse

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def backward(ctx, dout, *args):
    def backward(ctx, dout, *args):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q, k, v, out, softmax_lse = ctx.saved_tensors
        q, k, v, out, softmax_lse = ctx.saved_tensors
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dq, dk, dv = torch.empty_like(q), torch.empty_like(k), torch.empty_like(v)
        dq, dk, dv = torch.empty_like(q), torch.empty_like(k), torch.empty_like(v)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_flash_attn_backward(
        _flash_attn_backward(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dout,
            dout,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q,
            q,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k,
            k,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v,
            v,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out,
            out,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：softmax_lse,
            softmax_lse,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None, # cu_seqlens_q, cu_seqlens_k,
            None,  # cu_seqlens_q, cu_seqlens_k,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None, # sequed_q, sequed_k,
            None,  # sequed_q, sequed_k,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None, # max_seqlen_q, max_seqlen_k,
            None,  # max_seqlen_q, max_seqlen_k,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dq,
            dq,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dk,
            dk,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dv,
            dv,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx.softmax_scale,
            ctx.softmax_scale,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx.causal,
            ctx.causal,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx.window_size[0],
            ctx.window_size[0],
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx.window_size[1],
            ctx.window_size[1],
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx.softcap,
            ctx.softcap,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx.deterministic,
            ctx.deterministic,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx.sm_margin,
            ctx.sm_margin,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dq = dq[..., : dout.shape[-1]] # We could have padded the head dimension
        dq = dq[..., : dout.shape[-1]]  # We could have padded the head dimension
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dk = dk[..., : dout.shape[-1]]
        dk = dk[..., : dout.shape[-1]]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dv = dv[..., : dout.shape[-1]]
        dv = dv[..., : dout.shape[-1]]
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return dq, dk, dv, None, None, None, None, None, None, None, None, None, None, None, None, None
        return dq, dk, dv, None, None, None, None, None, None, None, None, None, None, None, None, None


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class FlashAttnVarlenFunc(torch.autograd.Function):
class FlashAttnVarlenFunc(torch.autograd.Function):
    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(
    def forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx,
        ctx,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q,
        q,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k,
        k,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v,
        v,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cu_seqlens_q,
        cu_seqlens_q,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cu_seqlens_k,
        cu_seqlens_k,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：seqused_q,
        seqused_q,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：seqused_k,
        seqused_k,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_seqlen_q,
        max_seqlen_q,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_seqlen_k,
        max_seqlen_k,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：softmax_scale,
        softmax_scale,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：causal,
        causal,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：qv=None,
        qv=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q_descale=None,
        q_descale=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：k_descale=None,
        k_descale=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：v_descale=None,
        v_descale=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：window_size=(-1, -1),
        window_size=(-1, -1),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：softcap=0.0,
        softcap=0.0,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_splits=1,
        num_splits=1,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pack_gqa=None,
        pack_gqa=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：deterministic=False,
        deterministic=False,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sm_margin=0,
        sm_margin=0,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：根据条件选择执行分支；代码：if softmax_scale is None:
        if softmax_scale is None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：softmax_scale = (q.shape[-1] + (qv.shape[-1] if qv is not None else 0)) ** (-0.5)
            softmax_scale = (q.shape[-1] + (qv.shape[-1] if qv is not None else 0)) ** (-0.5)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# out, q, k, v, out_padded, softmax_lse = _flash_attn_varlen_forward(
        # out, q, k, v, out_padded, softmax_lse = _flash_attn_varlen_forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out, softmax_lse, *rest = _flash_attn_forward(
        out, softmax_lse, *rest = _flash_attn_forward(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q,
            q,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k,
            k,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v,
            v,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None, # k_new, v_new
            None,  # k_new, v_new
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：qv, # qv
            qv,  # qv
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None, # out
            None,  # out
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cu_seqlens_q,
            cu_seqlens_q,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cu_seqlens_k,
            cu_seqlens_k,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None, # cu_seqlens_k_new
            None,  # cu_seqlens_k_new
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：seqused_q,
            seqused_q,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：seqused_k,
            seqused_k,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_seqlen_q,
            max_seqlen_q,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_seqlen_k,
            max_seqlen_k,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None, # page_table, kv_batch_idx, leftpad_k,
            None,  # page_table, kv_batch_idx, leftpad_k,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None, # rotary_cos/sin
            None,  # rotary_cos/sin
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q_descale,
            q_descale,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k_descale,
            k_descale,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v_descale,
            v_descale,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：softmax_scale,
            softmax_scale,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：causal=causal,
            causal=causal,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：window_size_left=window_size[0],
            window_size_left=window_size[0],
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：window_size_right=window_size[1],
            window_size_right=window_size[1],
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：softcap=softcap,
            softcap=softcap,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_splits=num_splits,
            num_splits=num_splits,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pack_gqa=pack_gqa,
            pack_gqa=pack_gqa,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sm_margin=sm_margin,
            sm_margin=sm_margin,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# ctx.save_for_backward(q, k, v, out_padded, softmax_lse, cu_seqlens_q, cu_seqlens_k, seqused...
        # ctx.save_for_backward(q, k, v, out_padded, softmax_lse, cu_seqlens_q, cu_seqlens_k, seqused_q, seqused_k)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx.save_for_backward(q, k, v, out, softmax_lse, cu_seqlens_q, cu_seqlens_k, seqused_q, sequs...
        ctx.save_for_backward(q, k, v, out, softmax_lse, cu_seqlens_q, cu_seqlens_k, seqused_q, seqused_k)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctx.max_seqlen_q = max_seqlen_q
        ctx.max_seqlen_q = max_seqlen_q
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctx.max_seqlen_k = max_seqlen_k
        ctx.max_seqlen_k = max_seqlen_k
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctx.softmax_scale = softmax_scale
        ctx.softmax_scale = softmax_scale
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctx.causal = causal
        ctx.causal = causal
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctx.window_size = window_size
        ctx.window_size = window_size
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctx.softcap = softcap
        ctx.softcap = softcap
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctx.deterministic = deterministic
        ctx.deterministic = deterministic
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctx.sm_margin = sm_margin
        ctx.sm_margin = sm_margin
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return out, softmax_lse
        return out, softmax_lse

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def backward(ctx, dout, *args):
    def backward(ctx, dout, *args):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q, k, v, out, softmax_lse, cu_seqlens_q, cu_seqlens_k, seqused_q, seqused_k = ctx.saved_tensors
        q, k, v, out, softmax_lse, cu_seqlens_q, cu_seqlens_k, seqused_q, seqused_k = ctx.saved_tensors
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dq, dk, dv = torch.empty_like(q), torch.empty_like(k), torch.empty_like(v)
        dq, dk, dv = torch.empty_like(q), torch.empty_like(k), torch.empty_like(v)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_flash_attn_backward(
        _flash_attn_backward(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dout,
            dout,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q,
            q,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k,
            k,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v,
            v,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out,
            out,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：softmax_lse,
            softmax_lse,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cu_seqlens_q,
            cu_seqlens_q,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cu_seqlens_k,
            cu_seqlens_k,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：seqused_q,
            seqused_q,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：seqused_k,
            seqused_k,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx.max_seqlen_q,
            ctx.max_seqlen_q,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx.max_seqlen_k,
            ctx.max_seqlen_k,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dq,
            dq,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dk,
            dk,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dv,
            dv,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx.softmax_scale,
            ctx.softmax_scale,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx.causal,
            ctx.causal,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx.window_size[0],
            ctx.window_size[0],
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx.window_size[1],
            ctx.window_size[1],
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx.softcap,
            ctx.softcap,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx.deterministic,
            ctx.deterministic,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx.sm_margin,
            ctx.sm_margin,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dq = dq[..., : dout.shape[-1]] # We could have padded the head dimension
        dq = dq[..., : dout.shape[-1]]  # We could have padded the head dimension
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dk = dk[..., : dout.shape[-1]]
        dk = dk[..., : dout.shape[-1]]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dv = dv[..., : dout.shape[-1]]
        dv = dv[..., : dout.shape[-1]]
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return (
        return (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dq,
            dq,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dk,
            dk,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dv,
            dv,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
            None,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def flash_attn_qkvpacked_func(
def flash_attn_qkvpacked_func(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：qkv,
    qkv,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：softmax_scale=None,
    softmax_scale=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：causal=False,
    causal=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q_descale=None,
    q_descale=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：k_descale=None,
    k_descale=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：v_descale=None,
    v_descale=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：window_size=(-1, -1),
    window_size=(-1, -1),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：softcap=0.0,
    softcap=0.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：deterministic=False,
    deterministic=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_heads_q=None,
    num_heads_q=None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""dropout_p should be set to 0.0 during evaluation
    """dropout_p should be set to 0.0 during evaluation
    If Q, K, V are already stacked into 1 tensor, this function will be faster than
    calling flash_attn_func on Q, K, V since the backward pass avoids explicit concatenation
    of the gradients of Q, K, V.
    For multi-query and grouped-query attention (MQA/GQA), please see
    flash_attn_kvpacked_func and flash_attn_func.

    If window_size != (-1, -1), implements sliding window local attention. Query at position i
    will only attend to keys between [i - window_size[0], i + window_size[1]] inclusive.

    Arguments:
        qkv: (batch_size, seqlen, 3, nheads, headdim)
        dropout_p: float. Dropout probability.
        softmax_scale: float. The scaling of QK^T before applying softmax.
            Default to 1 / sqrt(headdim).
        causal: bool. Whether to apply causal attention mask (e.g., for auto-regressive modeling).
        window_size: (left, right). If not (-1, -1), implements sliding window local attention.
        softcap: float. Anything > 0 activates softcapping attention.
        alibi_slopes: (nheads,) or (batch_size, nheads), fp32. A bias of (-alibi_slope * |i - j|) is added to
            the attention score of query i and key j.
        deterministic: bool. Whether to use the deterministic implementation of the backward pass,
            which is slightly slower and uses more memory. The forward pass is always deterministic.
        return_attn_probs: bool. Whether to return the attention probabilities. This option is for
           testing only. The returned probabilities are not guaranteed to be correct
           (they might not have the right scaling).
    Return:
        out: (batch_size, seqlen, nheads, headdim).
        softmax_lse [optional, if return_attn_probs=True]: (batch_size, nheads, seqlen). The
            logsumexp of each row of the matrix QK^T * scaling (e.g., log of the softmax
            normalization factor).
        S_dmask [optional, if return_attn_probs=True]: (batch_size, nheads, seqlen, seqlen).
            The output of softmax (possibly with different scaling). It also encodes the dropout
            pattern (negative means that location was dropped, nonnegative means it was kept).
    """
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return FlashAttnQKVPackedFunc.apply(
    return FlashAttnQKVPackedFunc.apply(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：qkv,
        qkv,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：softmax_scale,
        softmax_scale,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：causal,
        causal,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q_descale,
        q_descale,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k_descale,
        k_descale,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v_descale,
        v_descale,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：window_size,
        window_size,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：softcap,
        softcap,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：deterministic,
        deterministic,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_heads_q,
        num_heads_q,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def flash_attn_func(
def flash_attn_func(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q,
    q,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k,
    k,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v,
    v,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：softmax_scale=None,
    softmax_scale=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：causal=False,
    causal=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：qv=None,
    qv=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q_descale=None,
    q_descale=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：k_descale=None,
    k_descale=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：v_descale=None,
    v_descale=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：window_size=(-1, -1),
    window_size=(-1, -1),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：softcap=0.0,
    softcap=0.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_splits=1,
    num_splits=1,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pack_gqa=None,
    pack_gqa=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：deterministic=False,
    deterministic=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sm_margin=0,
    sm_margin=0,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""dropout_p should be set to 0.0 during evaluation
    """dropout_p should be set to 0.0 during evaluation
    Supports multi-query and grouped-query attention (MQA/GQA) by passing in KV with fewer heads
    than Q. Note that the number of heads in Q must be divisible by the number of heads in KV.
    For example, if Q has 6 heads and K, V have 2 heads, head 0, 1, 2 of Q will attention to head
    0 of K, V, and head 3, 4, 5 of Q will attention to head 1 of K, V.

    If causal=True, the causal mask is aligned to the bottom right corner of the attention matrix.
    For example, if seqlen_q = 2 and seqlen_k = 5, the causal mask (1 = keep, 0 = masked out) is:
        1 1 1 1 0
        1 1 1 1 1
    If seqlen_q = 5 and seqlen_k = 2, the causal mask is:
        0 0
        0 0
        0 0
        1 0
        1 1
    If the row of the mask is all zero, the output will be zero.

    If window_size != (-1, -1), implements sliding window local attention. Query at position i
    will only attend to keys between
    [i + seqlen_k - seqlen_q - window_size[0], i + seqlen_k - seqlen_q + window_size[1]] inclusive.

    Arguments:
        q: (batch_size, seqlen, nheads, headdim)
        k: (batch_size, seqlen, nheads_k, headdim)
        v: (batch_size, seqlen, nheads_k, headdim)
        dropout_p: float. Dropout probability.
        softmax_scale: float. The scaling of QK^T before applying softmax.
            Default to 1 / sqrt(headdim).
        causal: bool. Whether to apply causal attention mask (e.g., for auto-regressive modeling).
        window_size: (left, right). If not (-1, -1), implements sliding window local attention.
        alibi_slopes: (nheads,) or (batch_size, nheads), fp32. A bias of
            (-alibi_slope * |i + seqlen_k - seqlen_q - j|)
            is added to the attention score of query i and key j.
        deterministic: bool. Whether to use the deterministic implementation of the backward pass,
            which is slightly slower and uses more memory. The forward pass is always deterministic.
        return_attn_probs: bool. Whether to return the attention probabilities. This option is for
           testing only. The returned probabilities are not guaranteed to be correct
           (they might not have the right scaling).
    Return:
        out: (batch_size, seqlen, nheads, headdim).
        softmax_lse [optional, if return_attn_probs=True]: (batch_size, nheads, seqlen). The
            logsumexp of each row of the matrix QK^T * scaling (e.g., log of the softmax
            normalization factor).
    """
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return FlashAttnFunc.apply(
    return FlashAttnFunc.apply(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q,
        q,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k,
        k,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v,
        v,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：softmax_scale,
        softmax_scale,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：causal,
        causal,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：qv,
        qv,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q_descale,
        q_descale,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k_descale,
        k_descale,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v_descale,
        v_descale,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：window_size,
        window_size,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：softcap,
        softcap,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_splits,
        num_splits,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pack_gqa,
        pack_gqa,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：deterministic,
        deterministic,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sm_margin,
        sm_margin,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def flash_attn_varlen_func(
def flash_attn_varlen_func(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q,
    q,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k,
    k,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v,
    v,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cu_seqlens_q,
    cu_seqlens_q,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cu_seqlens_k,
    cu_seqlens_k,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_seqlen_q,
    max_seqlen_q,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_seqlen_k,
    max_seqlen_k,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：seqused_q=None,
    seqused_q=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：seqused_k=None,
    seqused_k=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：softmax_scale=None,
    softmax_scale=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：causal=False,
    causal=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：qv=None,
    qv=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q_descale=None,
    q_descale=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：k_descale=None,
    k_descale=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：v_descale=None,
    v_descale=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：window_size=(-1, -1),
    window_size=(-1, -1),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：softcap=0.0,
    softcap=0.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_splits=1,
    num_splits=1,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pack_gqa=None,
    pack_gqa=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：deterministic=False,
    deterministic=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sm_margin=0,
    sm_margin=0,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return FlashAttnVarlenFunc.apply(
    return FlashAttnVarlenFunc.apply(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q,
        q,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k,
        k,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v,
        v,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cu_seqlens_q,
        cu_seqlens_q,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cu_seqlens_k,
        cu_seqlens_k,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：seqused_q,
        seqused_q,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：seqused_k,
        seqused_k,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_seqlen_q,
        max_seqlen_q,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_seqlen_k,
        max_seqlen_k,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：softmax_scale,
        softmax_scale,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：causal,
        causal,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：qv,
        qv,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q_descale,
        q_descale,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k_descale,
        k_descale,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v_descale,
        v_descale,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：window_size,
        window_size,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：softcap,
        softcap,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_splits,
        num_splits,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pack_gqa,
        pack_gqa,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：deterministic,
        deterministic,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sm_margin,
        sm_margin,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def flash_attn_combine(out_partial, lse_partial, out=None, out_dtype=None):
def flash_attn_combine(out_partial, lse_partial, out=None, out_dtype=None):
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return flash_attn_3_cuda.fwd_combine(out_partial, lse_partial, out, out_dtype)
    return flash_attn_3_cuda.fwd_combine(out_partial, lse_partial, out, out_dtype)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def flash_attn_with_kvcache(
def flash_attn_with_kvcache(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q,
    q,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k_cache,
    k_cache,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v_cache,
    v_cache,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：k=None,
    k=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：v=None,
    v=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：qv=None,
    qv=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rotary_cos=None,
    rotary_cos=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rotary_sin=None,
    rotary_sin=None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cache_seqlens: Optional[Union[(int, torch.Tensor)]] = None,
    cache_seqlens: Optional[Union[(int, torch.Tensor)]] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cache_batch_idx: Optional[torch.Tensor] = None,
    cache_batch_idx: Optional[torch.Tensor] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cache_leftpad: Optional[torch.Tensor] = None,
    cache_leftpad: Optional[torch.Tensor] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：page_table: Optional[torch.Tensor] = None,
    page_table: Optional[torch.Tensor] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cu_seqlens_q: Optional[torch.Tensor] = None,
    cu_seqlens_q: Optional[torch.Tensor] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cu_seqlens_k_new: Optional[torch.Tensor] = None,
    cu_seqlens_k_new: Optional[torch.Tensor] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_seqlen_q: Optional[int] = None,
    max_seqlen_q: Optional[int] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q_descale: Optional[torch.Tensor] = None,
    q_descale: Optional[torch.Tensor] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k_descale: Optional[torch.Tensor] = None,
    k_descale: Optional[torch.Tensor] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v_descale: Optional[torch.Tensor] = None,
    v_descale: Optional[torch.Tensor] = None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：softmax_scale=None,
    softmax_scale=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：causal=False,
    causal=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：window_size=(-1, -1), # -1 means infinite context window
    window_size=(-1, -1),  # -1 means infinite context window
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：softcap=0.0, # 0.0 means deactivated
    softcap=0.0,  # 0.0 means deactivated
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rotary_interleaved=True,
    rotary_interleaved=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scheduler_metadata=None,
    scheduler_metadata=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_splits=0, # Can be tuned for speed
    num_splits=0,  # Can be tuned for speed
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pack_gqa=None, # Can be tuned for speed
    pack_gqa=None,  # Can be tuned for speed
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sm_margin=0, # Can be tuned if some SMs are used for communication
    sm_margin=0,  # Can be tuned if some SMs are used for communication
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return_softmax_lse=False,
    return_softmax_lse=False,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    If k and v are not None, k_cache and v_cache will be updated *inplace* with the new values from
    k and v. This is useful for incremental decoding: you can pass in the cached keys/values from
    the previous step, and update them with the new keys/values from the current step, and do
    attention with the updated cache, all in 1 kernel.

    If you pass in k / v, you must make sure that the cache is large enough to hold the new values.
    For example, the KV cache could be pre-allocated with the max sequence length, and you can use
    cache_seqlens to keep track of the current sequence lengths of each sequence in the batch.

    Also apply rotary embedding if rotary_cos and rotary_sin are passed in. The key @k will be
    rotated by rotary_cos and rotary_sin at indices cache_seqlens, cache_seqlens + 1, etc.
    If causal or local (i.e., window_size != (-1, -1)), the query @q will be rotated by rotary_cos
    and rotary_sin at indices cache_seqlens, cache_seqlens + 1, etc.
    If not causal and not local, the query @q will be rotated by rotary_cos and rotary_sin at
    indices cache_seqlens only (i.e. we consider all tokens in @q to be at position cache_seqlens).

    See tests/test_flash_attn.py::test_flash_attn_kvcache for examples of how to use this function.

    Supports multi-query and grouped-query attention (MQA/GQA) by passing in KV with fewer heads
    than Q. Note that the number of heads in Q must be divisible by the number of heads in KV.
    For example, if Q has 6 heads and K, V have 2 heads, head 0, 1, 2 of Q will attention to head
    0 of K, V, and head 3, 4, 5 of Q will attention to head 1 of K, V.

    If causal=True, the causal mask is aligned to the bottom right corner of the attention matrix.
    For example, if seqlen_q = 2 and seqlen_k = 5, the causal mask (1 = keep, 0 = masked out) is:
        1 1 1 1 0
        1 1 1 1 1
    If seqlen_q = 5 and seqlen_k = 2, the causal mask is:
        0 0
        0 0
        0 0
        1 0
        1 1
    If the row of the mask is all zero, the output will be zero.

    If window_size != (-1, -1), implements sliding window local attention. Query at position i
    will only attend to keys between
    [i + seqlen_k - seqlen_q - window_size[0], i + seqlen_k - seqlen_q + window_size[1]] inclusive.

    Note: Does not support backward pass.

    Arguments:
        q: (batch_size, seqlen, nheads, headdim)
        k_cache: (batch_size_cache, seqlen_cache, nheads_k, headdim) if there's no page_table,
            or (num_blocks, page_block_size, nheads_k, headdim) if there's a page_table (i.e. paged KV cache)
            page_block_size must be a multiple of 256.
        v_cache: (batch_size_cache, seqlen_cache, nheads_k, headdim_v) if there's no page_table,
            or (num_blocks, page_block_size, nheads_k, headdim_v) if there's a page_table (i.e. paged KV cache)
        k [optional]: (batch_size, seqlen_new, nheads_k, headdim). If not None, we concatenate
            k with k_cache, starting at the indices specified by cache_seqlens.
        v [optional]: (batch_size, seqlen_new, nheads_k, headdim_v). Similar to k.
        qv [optional]: (batch_size, seqlen, nheads, headdim_v)
        rotary_cos [optional]: (seqlen_ro, rotary_dim / 2). If not None, we apply rotary embedding
            to k and q. Only applicable if k and v are passed in. rotary_dim must be divisible by 16.
        rotary_sin [optional]: (seqlen_ro, rotary_dim / 2). Similar to rotary_cos.
        cache_seqlens: int, or (batch_size,), dtype torch.int32. The sequence lengths of the
            KV cache.
        cache_batch_idx: (batch_size,), dtype torch.int32. The indices used to index into the KV cache.
            If None, we assume that the batch indices are [0, 1, 2, ..., batch_size - 1].
            If the indices are not distinct, and k and v are provided, the values updated in the cache
                 might come from any of the duplicate indices.
        cache_leftpad: (batch_size,), dtype torch.int32. The index that the KV cache starts. If None, assume 0.
        page_table [optional]: (batch_size, max_num_blocks_per_seq), dtype torch.int32.
        softmax_scale: float. The scaling of QK^T before applying softmax.
            Default to 1 / sqrt(headdim).
        causal: bool. Whether to apply causal attention mask (e.g., for auto-regressive modeling).
        window_size: (left, right). If not (-1, -1), implements sliding window local attention.
        softcap: float. Anything > 0 activates softcapping attention.
        rotary_interleaved: bool. Only applicable if rotary_cos and rotary_sin are passed in.
            If True, rotary embedding will combine dimensions 0 & 1, 2 & 3, etc. If False,
            rotary embedding will combine dimensions 0 & rotary_dim / 2, 1 & rotary_dim / 2 + 1
            (i.e. GPT-NeoX style).
        num_splits: int. If > 1, split the key/value into this many chunks along the sequence.
           If num_splits == 1, we don't split the key/value. If num_splits == 0, we use a heuristic
           to automatically determine the number of splits.
           Don't change this unless you know what you are doing.
        return_softmax_lse: bool. Whether to return the logsumexp of the attention scores.

    Return:
        out: (batch_size, seqlen, nheads, headdim).
        softmax_lse [optional, if return_softmax_lse=True]: (batch_size, nheads, seqlen). The
            logsumexp of each row of the matrix QK^T * scaling (e.g., log of the softmax
            normalization factor).
    """
    # 中文说明：检查运行时假设是否成立；代码：assert k_cache.stride(-1) == 1, "k_cache must have contiguous last dimension"
    assert k_cache.stride(-1) == 1, "k_cache must have contiguous last dimension"
    # 中文说明：检查运行时假设是否成立；代码：assert v_cache.stride(-1) == 1, "v_cache must have contiguous last dimension"
    assert v_cache.stride(-1) == 1, "v_cache must have contiguous last dimension"
    # 中文说明：根据条件选择执行分支；代码：if softmax_scale is None:
    if softmax_scale is None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：softmax_scale = (q.shape[-1] + (qv.shape[-1] if qv is not None else 0)) ** (-0.5)
        softmax_scale = (q.shape[-1] + (qv.shape[-1] if qv is not None else 0)) ** (-0.5)
    # 中文说明：根据条件选择执行分支；代码：if cache_seqlens is not None and isinstance(cache_seqlens, int):
    if cache_seqlens is not None and isinstance(cache_seqlens, int):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_seqlens = torch.full((k_cache.shape[0],), cache_seqlens, dtype=torch.int32, device=k_ca...
        cache_seqlens = torch.full((k_cache.shape[0],), cache_seqlens, dtype=torch.int32, device=k_cache.device)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_seqlens = maybe_contiguous(cache_seqlens)
        cache_seqlens = maybe_contiguous(cache_seqlens)
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out, softmax_lse, *rest = _flash_attn_forward(
    out, softmax_lse, *rest = _flash_attn_forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q,
        q,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k_cache,
        k_cache,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v_cache,
        v_cache,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k,
        k,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v,
        v,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：qv,
        qv,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None, # out
        None,  # out
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cu_seqlens_q,
        cu_seqlens_q,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None, # cu_seqlens_k
        None,  # cu_seqlens_k
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cu_seqlens_k_new,
        cu_seqlens_k_new,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None, # seqused_q
        None,  # seqused_q
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cache_seqlens,
        cache_seqlens,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_seqlen_q,
        max_seqlen_q,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None, # max_seqlen_k
        None,  # max_seqlen_k
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：page_table,
        page_table,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cache_batch_idx,
        cache_batch_idx,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cache_leftpad,
        cache_leftpad,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rotary_cos,
        rotary_cos,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rotary_sin,
        rotary_sin,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q_descale,
        q_descale,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k_descale,
        k_descale,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v_descale,
        v_descale,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：softmax_scale,
        softmax_scale,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：causal=causal,
        causal=causal,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：window_size_left=window_size[0],
        window_size_left=window_size[0],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：window_size_right=window_size[1],
        window_size_right=window_size[1],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：softcap=softcap,
        softcap=softcap,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rotary_interleaved=rotary_interleaved,
        rotary_interleaved=rotary_interleaved,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scheduler_metadata=scheduler_metadata,
        scheduler_metadata=scheduler_metadata,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_splits=num_splits,
        num_splits=num_splits,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pack_gqa=pack_gqa,
        pack_gqa=pack_gqa,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sm_margin=sm_margin,
        sm_margin=sm_margin,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# return (out, softmax_lse) if return_softmax_lse else out
    # return (out, softmax_lse) if return_softmax_lse else out
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return (out, softmax_lse, *rest) if return_softmax_lse else out
    return (out, softmax_lse, *rest) if return_softmax_lse else out


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_scheduler_metadata(
def get_scheduler_metadata(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：batch_size,
    batch_size,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_seqlen_q,
    max_seqlen_q,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_seqlen_k,
    max_seqlen_k,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_heads_q,
    num_heads_q,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_heads_kv,
    num_heads_kv,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：headdim,
    headdim,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cache_seqlens: torch.Tensor,
    cache_seqlens: torch.Tensor,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：qkv_dtype=torch.bfloat16,
    qkv_dtype=torch.bfloat16,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：headdim_v=None,
    headdim_v=None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cu_seqlens_q: Optional[torch.Tensor] = None,
    cu_seqlens_q: Optional[torch.Tensor] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cu_seqlens_k_new: Optional[torch.Tensor] = None,
    cu_seqlens_k_new: Optional[torch.Tensor] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cache_leftpad: Optional[torch.Tensor] = None,
    cache_leftpad: Optional[torch.Tensor] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：page_size: Optional[int] = None,
    page_size: Optional[int] = None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_seqlen_k_new=0,
    max_seqlen_k_new=0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：causal=False,
    causal=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：window_size=(-1, -1), # -1 means infinite context window
    window_size=(-1, -1),  # -1 means infinite context window
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：has_softcap=False,
    has_softcap=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_splits=0, # Can be tuned for speed
    num_splits=0,  # Can be tuned for speed
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pack_gqa=None, # Can be tuned for speed
    pack_gqa=None,  # Can be tuned for speed
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sm_margin=0, # Can be tuned if some SMs are used for communication
    sm_margin=0,  # Can be tuned if some SMs are used for communication
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_seqlens = maybe_contiguous(cache_seqlens)
    cache_seqlens = maybe_contiguous(cache_seqlens)
    # 中文说明：根据条件选择执行分支；代码：if headdim_v is None:
    if headdim_v is None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：headdim_v = headdim
        headdim_v = headdim
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scheduler_metadata = flash_attn_3_cuda.get_scheduler_metadata(
    scheduler_metadata = flash_attn_3_cuda.get_scheduler_metadata(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：batch_size,
        batch_size,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_seqlen_q,
        max_seqlen_q,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_seqlen_k,
        max_seqlen_k,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_heads_q,
        num_heads_q,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_heads_kv,
        num_heads_kv,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：headdim,
        headdim,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：headdim_v,
        headdim_v,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：qkv_dtype,
        qkv_dtype,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cache_seqlens,
        cache_seqlens,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cu_seqlens_q,
        cu_seqlens_q,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None, # cu_seqlens_k
        None,  # cu_seqlens_k
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cu_seqlens_k_new,
        cu_seqlens_k_new,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None, # seqused_q
        None,  # seqused_q
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cache_leftpad,
        cache_leftpad,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：page_size,
        page_size,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_seqlen_k_new,
        max_seqlen_k_new,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：causal,
        causal,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：window_size[0],
        window_size[0],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：window_size[1],
        window_size[1],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：has_softcap,
        has_softcap,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_splits,
        num_splits,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pack_gqa,
        pack_gqa,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sm_margin,
        sm_margin,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return scheduler_metadata
    return scheduler_metadata
