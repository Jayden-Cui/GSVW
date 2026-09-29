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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import math
import math
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Dict, Iterable, List, Optional, Tuple, Union
from typing import Dict, Iterable, List, Optional, Tuple, Union

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.distributed as dist
import torch.distributed as dist
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch import Tensor
from torch import Tensor
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed import DeviceMesh
from torch.distributed import DeviceMesh
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed._tensor.api import DTensor
from torch.distributed._tensor.api import DTensor
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.nn.utils.clip_grad import (
from torch.nn.utils.clip_grad import (
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_device_has_foreach_support,
    _device_has_foreach_support,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_group_tensors_by_device_and_dtype,
    _group_tensors_by_device_and_dtype,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_has_foreach_support,
    _has_foreach_support,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_no_grad,
    _no_grad,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_tensor_or_tensors,
    _tensor_or_tensors,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)


# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# https://github.com/pytorch/torchtitan/blob/d4c86e3758a84cf23e2e879ab3c995cba9d5e410/torchti...
# https://github.com/pytorch/torchtitan/blob/d4c86e3758a84cf23e2e879ab3c995cba9d5e410/torchtitan/utils.py#L354
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.no_grad()
@torch.no_grad()
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def clip_grad_norm_(
def clip_grad_norm_(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parameters: Union[torch.Tensor, Iterable[torch.Tensor]],
    parameters: Union[torch.Tensor, Iterable[torch.Tensor]],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_norm: float,
    max_norm: float,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：norm_type: float = 2.0,
    norm_type: float = 2.0,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：error_if_nonfinite: bool = False,
    error_if_nonfinite: bool = False,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：foreach: Optional[bool] = None,
    foreach: Optional[bool] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pp_mesh: Optional[DeviceMesh] = None,
    pp_mesh: Optional[DeviceMesh] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor:
) -> torch.Tensor:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Clip the gradient norm of an iterable of parameters.

    Gradient norm clipping requires computing the gradient norm over the entire model.
    `torch.nn.utils.clip_grad_norm_` only computes gradient norm along DP/FSDP/TP dimensions.
    We need to manually reduce the gradient norm across PP stages.
    See https://github.com/pytorch/torchtitan/issues/596 for details.

    Args:
        parameters: an iterable of Tensors or a single Tensor that will have gradients normalized
        max_norm (float): max norm of the gradients
        norm_type (float): type of the used p-norm. Can be ``'inf'`` for
            infinity norm.
        error_if_nonfinite (bool): if True, an error is thrown if the total
            norm of the gradients from :attr:`parameters` is ``nan``,
            ``inf``, or ``-inf``. Default: False (will switch to True in the future)
        foreach (bool): use the faster foreach-based implementation.
            If ``None``, use the foreach implementation for CUDA and CPU native tensors and silently
            fall back to the slow implementation for other device types.
            Default: ``None``
        pp_mesh: pipeline parallel device mesh. If not None, will reduce gradient norm across PP stages.

    Returns:
        Total norm of the parameter gradients (viewed as a single vector).

    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：grads = [p.grad for p in parameters if p.grad is not None]
    grads = [p.grad for p in parameters if p.grad is not None]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：total_norm = get_total_norm(grads, norm_type, error_if_nonfinite, foreach)
    total_norm = get_total_norm(grads, norm_type, error_if_nonfinite, foreach)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# If total_norm is a DTensor, the placements must be `torch.distributed._tensor.ops.math_ops....
    # If total_norm is a DTensor, the placements must be `torch.distributed._tensor.ops.math_ops._NormPartial`.
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# We can simply reduce the DTensor to get the total norm in this tensor's process group
    # We can simply reduce the DTensor to get the total norm in this tensor's process group
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# and then convert it to a local tensor.
    # and then convert it to a local tensor.
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# NOTE: It has two purposes:
    # NOTE: It has two purposes:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 1. to make sure the total norm is computed correctly when PP is used (see below)
    #       1. to make sure the total norm is computed correctly when PP is used (see below)
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 2. to return a reduced total_norm tensor whose .item() would return the correct value
    #       2. to return a reduced total_norm tensor whose .item() would return the correct value
    # 中文说明：根据条件选择执行分支；代码：if isinstance(total_norm, DTensor):
    if isinstance(total_norm, DTensor):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Will reach here if any non-PP parallelism is used.
        # Will reach here if any non-PP parallelism is used.
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# If only using PP, total_norm will be a local tensor.
        # If only using PP, total_norm will be a local tensor.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：total_norm = total_norm.full_tensor()
        total_norm = total_norm.full_tensor()

    # 中文说明：根据条件选择执行分支；代码：if pp_mesh is not None:
    if pp_mesh is not None:
        # 中文说明：根据条件选择执行分支；代码：if math.isinf(norm_type):
        if math.isinf(norm_type):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dist.all_reduce(total_norm, op=dist.ReduceOp.MAX, group=pp_mesh.get_group())
            dist.all_reduce(total_norm, op=dist.ReduceOp.MAX, group=pp_mesh.get_group())
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：total_norm **= norm_type
            total_norm **= norm_type
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dist.all_reduce(total_norm, op=dist.ReduceOp.SUM, group=pp_mesh.get_group())
            dist.all_reduce(total_norm, op=dist.ReduceOp.SUM, group=pp_mesh.get_group())
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：total_norm **= 1.0 / norm_type
            total_norm **= 1.0 / norm_type

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：clip_grads_with_norm_(parameters, max_norm, total_norm, foreach)
    clip_grads_with_norm_(parameters, max_norm, total_norm, foreach)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return total_norm
    return total_norm


# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# from: pytorch/pytorch/torch/nn/utils/clip_grad.py
# from: pytorch/pytorch/torch/nn/utils/clip_grad.py
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@_no_grad
@_no_grad
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _get_total_norm(
def _get_total_norm(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：tensors: _tensor_or_tensors,
    tensors: _tensor_or_tensors,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：norm_type: float = 2.0,
    norm_type: float = 2.0,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：error_if_nonfinite: bool = False,
    error_if_nonfinite: bool = False,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：foreach: Optional[bool] = None,
    foreach: Optional[bool] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor:
) -> torch.Tensor:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Compute the norm of an iterable of tensors.
    r"""Compute the norm of an iterable of tensors.

    The norm is computed over the norms of the individual tensors, as if the norms of
    the individual tensors were concatenated into a single vector.

    Args:
        tensors (Iterable[Tensor] or Tensor): an iterable of Tensors or a
            single Tensor that will be normalized
        norm_type (float): type of the used p-norm. Can be ``'inf'`` for
            infinity norm.
        error_if_nonfinite (bool): if True, an error is thrown if the total
            norm of :attr:`tensors` is ``nan``, ``inf``, or ``-inf``.
            Default: ``False``
        foreach (bool): use the faster foreach-based implementation.
            If ``None``, use the foreach implementation for CUDA and CPU native tensors and silently
            fall back to the slow implementation for other device types.
            Default: ``None``

    Returns:
        Total norm of the tensors (viewed as a single vector).
    """
    # 中文说明：根据条件选择执行分支；代码：if isinstance(tensors, torch.Tensor):
    if isinstance(tensors, torch.Tensor):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tensors = [tensors]
        tensors = [tensors]
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tensors = list(tensors)
        tensors = list(tensors)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：norm_type = float(norm_type)
    norm_type = float(norm_type)
    # 中文说明：根据条件选择执行分支；代码：if len(tensors) == 0:
    if len(tensors) == 0:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return torch.tensor(0.0)
        return torch.tensor(0.0)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：first_device = tensors[0].device
    first_device = tensors[0].device
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：grouped_tensors: Dict[
    grouped_tensors: Dict[
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：Tuple[torch.device, torch.dtype], Tuple[List[List[Tensor]], List[int]]
        Tuple[torch.device, torch.dtype], Tuple[List[List[Tensor]], List[int]]
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：] = _group_tensors_by_device_and_dtype([tensors])
    ] = _group_tensors_by_device_and_dtype([tensors])

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：norms: List[Tensor] = []
    norms: List[Tensor] = []
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for (device, _), ([device_tensors], _) in grouped_tensors.items():
    for (device, _), ([device_tensors], _) in grouped_tensors.items():
        # 中文说明：根据条件选择执行分支；代码：if (foreach is None and _has_foreach_support(device_tensors, device)) or (
        if (foreach is None and _has_foreach_support(device_tensors, device)) or (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：foreach and _device_has_foreach_support(device)
            foreach and _device_has_foreach_support(device)
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
        ):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：norms.extend(torch._foreach_norm(device_tensors, norm_type))
            norms.extend(torch._foreach_norm(device_tensors, norm_type))
        # 中文说明：根据条件选择执行分支；代码：elif foreach:
        elif foreach:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise RuntimeError(f"foreach=True was passed, but can't use the foreach API on {device.type} ...
            raise RuntimeError(f"foreach=True was passed, but can't use the foreach API on {device.type} tensors")
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：norms.extend([torch.linalg.vector_norm(g, norm_type) for g in device_tensors])
            norms.extend([torch.linalg.vector_norm(g, norm_type) for g in device_tensors])

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：total_norm = torch.linalg.vector_norm(torch.stack([norm.to(first_device) for norm in norms]),...
    total_norm = torch.linalg.vector_norm(torch.stack([norm.to(first_device) for norm in norms]), norm_type)

    # 中文说明：根据条件选择执行分支；代码：if error_if_nonfinite and torch.logical_or(total_norm.isnan(), total_norm.isinf()):
    if error_if_nonfinite and torch.logical_or(total_norm.isnan(), total_norm.isinf()):
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise RuntimeError(
        raise RuntimeError(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"The total norm of order {norm_type} for gradients from "
            f"The total norm of order {norm_type} for gradients from "
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："`parameters` is non-finite, so it cannot be clipped. To disable "
            "`parameters` is non-finite, so it cannot be clipped. To disable "
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："this error and scale the gradients by the non-finite norm anyway, "
            "this error and scale the gradients by the non-finite norm anyway, "
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："set `error_if_nonfinite=False`"
            "set `error_if_nonfinite=False`"
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return total_norm
    return total_norm


# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：get_total_norm = _get_total_norm
get_total_norm = _get_total_norm


# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# from: pytorch/pytorch/torch/nn/utils/clip_grad.py
# from: pytorch/pytorch/torch/nn/utils/clip_grad.py
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@_no_grad
@_no_grad
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _clip_grads_with_norm_(
def _clip_grads_with_norm_(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parameters: _tensor_or_tensors,
    parameters: _tensor_or_tensors,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_norm: float,
    max_norm: float,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：total_norm: torch.Tensor,
    total_norm: torch.Tensor,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：foreach: Optional[bool] = None,
    foreach: Optional[bool] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
) -> None:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Scale the gradients of an iterable of parameters given a pre-calculated total norm and de...
    r"""Scale the gradients of an iterable of parameters given a pre-calculated total norm and desired max norm.

    The gradients will be scaled by the following calculation

    .. math::
        grad = grad * \frac{max\_norm}{total\_norm + 1e-6}

    Gradients are modified in-place.

    This function is equivalent to :func:`torch.nn.utils.clip_grad_norm_` with a pre-calculated
    total norm.

    Args:
        parameters (Iterable[Tensor] or Tensor): an iterable of Tensors or a
            single Tensor that will have gradients normalized
        max_norm (float): max norm of the gradients
        total_norm (Tensor): total norm of the gradients to use for clipping
        foreach (bool): use the faster foreach-based implementation.
            If ``None``, use the foreach implementation for CUDA and CPU native tensors and silently
            fall back to the slow implementation for other device types.
            Default: ``None``

    Returns:
        None
    """
    # 中文说明：根据条件选择执行分支；代码：if isinstance(parameters, torch.Tensor):
    if isinstance(parameters, torch.Tensor):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：parameters = [parameters]
        parameters = [parameters]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：grads = [p.grad for p in parameters if p.grad is not None]
    grads = [p.grad for p in parameters if p.grad is not None]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_norm = float(max_norm)
    max_norm = float(max_norm)
    # 中文说明：根据条件选择执行分支；代码：if len(grads) == 0:
    if len(grads) == 0:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return
        return
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：grouped_grads: Dict[
    grouped_grads: Dict[
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：Tuple[torch.device, torch.dtype], Tuple[List[List[Tensor]], List[int]]
        Tuple[torch.device, torch.dtype], Tuple[List[List[Tensor]], List[int]]
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：] = _group_tensors_by_device_and_dtype([grads])
    ] = _group_tensors_by_device_and_dtype([grads])

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：clip_coef = max_norm / (total_norm + 1e-6)
    clip_coef = max_norm / (total_norm + 1e-6)
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Note: multiplying by the clamped coef is redundant when the coef is clamped to 1, but doing so
    # Note: multiplying by the clamped coef is redundant when the coef is clamped to 1, but doing so
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# avoids a `if clip_coef < 1:` conditional which can require a CPU <=> device synchronization
    # avoids a `if clip_coef < 1:` conditional which can require a CPU <=> device synchronization
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# when the gradients do not reside in CPU memory.
    # when the gradients do not reside in CPU memory.
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：clip_coef_clamped = torch.clamp(clip_coef, max=1.0)
    clip_coef_clamped = torch.clamp(clip_coef, max=1.0)
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for (device, _), ([device_grads], _) in grouped_grads.items():
    for (device, _), ([device_grads], _) in grouped_grads.items():
        # 中文说明：根据条件选择执行分支；代码：if (foreach is None and _has_foreach_support(device_grads, device)) or (
        if (foreach is None and _has_foreach_support(device_grads, device)) or (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：foreach and _device_has_foreach_support(device)
            foreach and _device_has_foreach_support(device)
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
        ):
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch._foreach_mul_(device_grads, clip_coef_clamped.to(device))
            torch._foreach_mul_(device_grads, clip_coef_clamped.to(device))
        # 中文说明：根据条件选择执行分支；代码：elif foreach:
        elif foreach:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise RuntimeError(f"foreach=True was passed, but can't use the foreach API on {device.type} ...
            raise RuntimeError(f"foreach=True was passed, but can't use the foreach API on {device.type} tensors")
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：clip_coef_clamped_device = clip_coef_clamped.to(device)
            clip_coef_clamped_device = clip_coef_clamped.to(device)
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for g in device_grads:
            for g in device_grads:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：g.mul_(clip_coef_clamped_device)
                g.mul_(clip_coef_clamped_device)


# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：clip_grads_with_norm_ = _clip_grads_with_norm_
clip_grads_with_norm_ = _clip_grads_with_norm_
