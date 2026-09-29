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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from functools import partial
from functools import partial

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.nn.attention import SDPBackend, sdpa_kernel
from torch.nn.attention import SDPBackend, sdpa_kernel
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from einops import rearrange, repeat
from einops import rearrange, repeat
# 中文说明：开始一个可捕获异常的代码块；代码：try:
try:
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from flash_attn_3.flash_attn_interface import flash_attn_func
    from flash_attn_3.flash_attn_interface import flash_attn_func

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：FLASH_ATTN_3_AVAILABLE = True
    FLASH_ATTN_3_AVAILABLE = True
# 中文说明：处理异常、清理资源或管理上下文；代码：except ModuleNotFoundError:
except ModuleNotFoundError:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：FLASH_ATTN_3_AVAILABLE = False
    FLASH_ATTN_3_AVAILABLE = False


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_device_cc(device) -> int:
def get_device_cc(device) -> int:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Returns the compute capability of a given torch device if it's a CUDA device, otherwise returns 0.

    Args:
        device: torch device.

    Returns:
        device_cc (int): compute capability in the SmXXX format (i.e. 90 for Hopper).
    """
    # 中文说明：根据条件选择执行分支；代码：if torch.cuda.is_available() and torch.version.cuda and device.type == "cuda":
    if torch.cuda.is_available() and torch.version.cuda and device.type == "cuda":
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：major, minor = torch.cuda.get_device_capability(device)
        major, minor = torch.cuda.get_device_capability(device)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return major * 10 + minor
        return major * 10 + minor
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return 0
    return 0


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def attention(
def attention(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q,
    q,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k,
    k,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v,
    v,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q_lens=None,
    q_lens=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：k_lens=None,
    k_lens=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout_p=0.0,
    dropout_p=0.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：softmax_scale=None,
    softmax_scale=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q_scale=None,
    q_scale=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：causal=False,
    causal=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：deterministic=False,
    deterministic=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dtype=torch.bfloat16,
    dtype=torch.bfloat16,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ori_size=None
    ori_size=None
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：supported_dtypes = [torch.bfloat16, torch.float16, torch.float32]
    supported_dtypes = [torch.bfloat16, torch.float16, torch.float32]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_half = dtype in [torch.bfloat16, torch.float16]
    is_half = dtype in [torch.bfloat16, torch.float16]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：compute_cap = get_device_cc(q.device)
    compute_cap = get_device_cc(q.device)

    # 中文说明：根据条件选择执行分支；代码：if dtype not in supported_dtypes:
    if dtype not in supported_dtypes:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise NotImplementedError(f"{dtype=} is not supported.")
        raise NotImplementedError(f"{dtype=} is not supported.")

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q = q.to(dtype)
    q = q.to(dtype)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：k = k.to(dtype)
    k = k.to(dtype)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：v = v.to(dtype)
    v = v.to(dtype)

    # 中文说明：根据条件选择执行分支；代码：if q_scale is not None:
    if q_scale is not None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q = q * q_scale
        q = q * q_scale
    # 中文说明：根据条件选择执行分支；代码：if causal:
    if causal:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：检查运行时假设是否成立；代码：assert ori_size is not None
        assert ori_size is not None
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：B, T, H, W = ori_size
        B, T, H, W = ori_size
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# attn_mask = torch.ones((B*H*W, T, T), dtype=torch.bool, device=q.device)
        # attn_mask = torch.ones((B*H*W, T, T), dtype=torch.bool, device=q.device)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# attn_mask = torch.tril(attn_mask)
        # attn_mask = torch.tril(attn_mask)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# attn_mask = rearrange(attn_mask, "(b h w) t d -> b (t h w) d", b=B, h=H, w=W, t=T, d=T)
        # attn_mask = rearrange(attn_mask, "(b h w) t d -> b (t h w) d", b=B, h=H, w=W, t=T, d=T)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# k = k[:, :T]
        # k = k[:, :T]
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# v = v[:, :T]
        # v = v[:, :T]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q_len = q.shape[1]
        q_len = q.shape[1]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q_indices = torch.arange(q_len, device=q.device)
        q_indices = torch.arange(q_len, device=q.device)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：k_indices = torch.arange(T, device=q.device)
        k_indices = torch.arange(T, device=q.device)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q_frame_indices = q_indices // (H * W)
        q_frame_indices = q_indices // (H * W)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn_mask = k_indices.view(1, T) <= q_frame_indices.view(q_len, 1)
        attn_mask = k_indices.view(1, T) <= q_frame_indices.view(q_len, 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding_attn_mask = torch.ones((B*H*W*T, 512-T), dtype=torch.bool, device=q.device)
        padding_attn_mask = torch.ones((B*H*W*T, 512-T), dtype=torch.bool, device=q.device)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn_mask = torch.cat((attn_mask, padding_attn_mask), dim=1)
        attn_mask = torch.cat((attn_mask, padding_attn_mask), dim=1)

    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn_mask = None
        attn_mask = None
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# If Flash Attention 3 is installed, and the user's running on a Hopper GPU (compute capability
    # If Flash Attention 3 is installed, and the user's running on a Hopper GPU (compute capability
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 9.0, or SM90), use Flash Attention 3.
    # 9.0, or SM90), use Flash Attention 3.
    # 中文说明：根据条件选择执行分支；代码：if compute_cap == 90 and FLASH_ATTN_3_AVAILABLE and is_half:
    if compute_cap == 90 and FLASH_ATTN_3_AVAILABLE and is_half:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return flash_attn_func(
        return flash_attn_func(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q=q,
            q=q,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：k=k,
            k=k,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：v=v,
            v=v,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn_mask=attn_mask,
            attn_mask=attn_mask,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：softmax_scale=softmax_scale,
            softmax_scale=softmax_scale,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：causal=causal,
            causal=causal,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：deterministic=deterministic,
            deterministic=deterministic,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)[0]
        )[0]
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# If Blackwell or Hopper (SM100 or SM90), cuDNN has native FMHA kernels. The Hopper one is
        # If Blackwell or Hopper (SM100 or SM90), cuDNN has native FMHA kernels. The Hopper one is
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# not always as fast as Flash Attention 3, but when Flash Attention is unavailable, it's
        # not always as fast as Flash Attention 3, but when Flash Attention is unavailable, it's
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# still a far better choice than Flash Attention 2 (Ampere).
        # still a far better choice than Flash Attention 2 (Ampere).
        # 中文说明：根据条件选择执行分支；代码：if compute_cap in [90, 100] and is_half:
        if compute_cap in [90, 100] and is_half:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：SDPA_BACKENDS = [
            SDPA_BACKENDS = [
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：SDPBackend.CUDNN_ATTENTION,
                SDPBackend.CUDNN_ATTENTION,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：SDPBackend.FLASH_ATTENTION,
                SDPBackend.FLASH_ATTENTION,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：SDPBackend.EFFICIENT_ATTENTION,
                SDPBackend.EFFICIENT_ATTENTION,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
            ]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：BEST_SDPA_BACKEND = SDPBackend.CUDNN_ATTENTION
            BEST_SDPA_BACKEND = SDPBackend.CUDNN_ATTENTION
        # 中文说明：根据条件选择执行分支；代码：elif is_half:
        elif is_half:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：SDPA_BACKENDS = [
            SDPA_BACKENDS = [
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：SDPBackend.FLASH_ATTENTION,
                SDPBackend.FLASH_ATTENTION,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：SDPBackend.CUDNN_ATTENTION,
                SDPBackend.CUDNN_ATTENTION,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：SDPBackend.EFFICIENT_ATTENTION,
                SDPBackend.EFFICIENT_ATTENTION,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
            ]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：BEST_SDPA_BACKEND = SDPBackend.FLASH_ATTENTION if compute_cap >= 80 else SDPBackend.EFFICIENT...
            BEST_SDPA_BACKEND = SDPBackend.FLASH_ATTENTION if compute_cap >= 80 else SDPBackend.EFFICIENT_ATTENTION
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：检查运行时假设是否成立；代码：assert dtype == torch.float32, f"Unrecognized {dtype=}."
            assert dtype == torch.float32, f"Unrecognized {dtype=}."
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：SDPA_BACKENDS = [SDPBackend.EFFICIENT_ATTENTION]
            SDPA_BACKENDS = [SDPBackend.EFFICIENT_ATTENTION]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：BEST_SDPA_BACKEND = SDPBackend.EFFICIENT_ATTENTION
            BEST_SDPA_BACKEND = SDPBackend.EFFICIENT_ATTENTION

        # 中文说明：根据条件选择执行分支；代码：if deterministic:
        if deterministic:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise NotImplementedError(
            raise NotImplementedError(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："Deterministic mode in attention is only supported when Flash Attention 3 is available."
                "Deterministic mode in attention is only supported when Flash Attention 3 is available."
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Torch 2.6 and later allows priorities for backends, but for older versions
        # Torch 2.6 and later allows priorities for backends, but for older versions
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# we can only run with a specific backend. As long as we pick ones we're certain
        # we can only run with a specific backend. As long as we pick ones we're certain
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# will work on that device, it should be fine.
        # will work on that device, it should be fine.
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sdpa_kernel(backends=SDPA_BACKENDS, set_priority_order=True)
            sdpa_kernel(backends=SDPA_BACKENDS, set_priority_order=True)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sdpa_kernel_ = partial(sdpa_kernel, set_priority_order=True)
            sdpa_kernel_ = partial(sdpa_kernel, set_priority_order=True)
        # 中文说明：处理异常、清理资源或管理上下文；代码：except TypeError:
        except TypeError:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sdpa_kernel_ = sdpa_kernel
            sdpa_kernel_ = sdpa_kernel
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：SDPA_BACKENDS = [BEST_SDPA_BACKEND]
            SDPA_BACKENDS = [BEST_SDPA_BACKEND]
        
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q = q.transpose(1, 2)
        q = q.transpose(1, 2)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：k = k.transpose(1, 2)
        k = k.transpose(1, 2)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：v = v.transpose(1, 2)
        v = v.transpose(1, 2)

        # 中文说明：根据条件选择执行分支；代码：if attn_mask is not None:
        if attn_mask is not None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：SDPA_BACKENDS = [SDPBackend.EFFICIENT_ATTENTION]
            SDPA_BACKENDS = [SDPBackend.EFFICIENT_ATTENTION]
        # 中文说明：处理异常、清理资源或管理上下文；代码：with sdpa_kernel_(backends=SDPA_BACKENDS):
        with sdpa_kernel_(backends=SDPA_BACKENDS):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out = torch.nn.functional.scaled_dot_product_attention(
            out = torch.nn.functional.scaled_dot_product_attention(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q,
                q,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k,
                k,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v,
                v,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn_mask=attn_mask,
                attn_mask=attn_mask,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_causal=False,
                is_causal=False,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout_p=dropout_p,
                dropout_p=dropout_p,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scale=softmax_scale,
                scale=softmax_scale,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out = out.transpose(1, 2).contiguous()
        out = out.transpose(1, 2).contiguous()
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return out
        return out
