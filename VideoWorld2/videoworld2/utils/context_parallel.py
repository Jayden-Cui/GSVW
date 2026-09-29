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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Optional
from typing import Optional

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch import Tensor
from torch import Tensor
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed import ProcessGroup, all_gather, broadcast_object_list, get_process_gr...
from torch.distributed import ProcessGroup, all_gather, broadcast_object_list, get_process_group_ranks, get_world_size
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed.utils import _verify_param_shape_across_processes
from torch.distributed.utils import _verify_param_shape_across_processes

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import distributed
from imaginaire.utils import distributed


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def split_inputs_cp(x: Tensor, seq_dim: int, cp_group: ProcessGroup) -> Tensor:
def split_inputs_cp(x: Tensor, seq_dim: int, cp_group: ProcessGroup) -> Tensor:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Split input tensor along the sequence dimension for checkpoint parallelism.

    This function divides the input tensor into equal parts along the specified
    sequence dimension, based on the number of ranks in the checkpoint parallelism group.
    It then selects the part corresponding to the current rank.

    Args:
        x: Input tensor to be split.
        seq_dim: The dimension along which to split the input (sequence dimension).
        cp_group: The process group for checkpoint parallelism.

    Returns:
        A slice of the input tensor corresponding to the current rank.

    Raises:
        AssertionError: If the sequence dimension is not divisible by the number of ranks.
    """
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Ensure tensor is on CUDA
    # Ensure tensor is on CUDA
    # 中文说明：根据条件选择执行分支；代码：if x.device.type != "cuda":
    if x.device.type != "cuda":
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = x.cuda()
        x = x.cuda()

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cp_ranks = get_process_group_ranks(cp_group)
    cp_ranks = get_process_group_ranks(cp_group)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cp_size = len(cp_ranks)
    cp_size = len(cp_ranks)

    # 中文说明：检查运行时假设是否成立；代码：assert x.shape[seq_dim] % cp_size == 0, f"{x.shape[seq_dim]} cannot divide cp_size {cp_size}"
    assert x.shape[seq_dim] % cp_size == 0, f"{x.shape[seq_dim]} cannot divide cp_size {cp_size}"
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = x.view(*x.shape[:seq_dim], cp_size, x.shape[seq_dim] // cp_size, *x.shape[(seq_dim + 1) :])
    x = x.view(*x.shape[:seq_dim], cp_size, x.shape[seq_dim] // cp_size, *x.shape[(seq_dim + 1) :])
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：seq_idx = torch.tensor([cp_group.rank()], device=x.device)
    seq_idx = torch.tensor([cp_group.rank()], device=x.device)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = x.index_select(seq_dim, seq_idx)
    x = x.index_select(seq_dim, seq_idx)
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Note that the new sequence length is the original sequence length / cp_size
    # Note that the new sequence length is the original sequence length / cp_size
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = x.view(*x.shape[:seq_dim], -1, *x.shape[(seq_dim + 2) :])
    x = x.view(*x.shape[:seq_dim], -1, *x.shape[(seq_dim + 2) :])
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return x
    return x


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def cat_outputs_cp(x: Tensor, seq_dim: int, cp_group: ProcessGroup) -> Tensor:
def cat_outputs_cp(x: Tensor, seq_dim: int, cp_group: ProcessGroup) -> Tensor:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Concatenate outputs from different ranks in the checkpoint parallelism group.

    This function gathers tensors from all ranks in the checkpoint parallelism group
    and concatenates them along the specified sequence dimension.

    Args:
        x: Input tensor to be concatenated.
        seq_dim: The dimension along which to concatenate the tensors (sequence dimension).
        cp_group: The process group for checkpoint parallelism.

    Returns:
        A tensor that is the concatenation of tensors from all ranks in the cp_group.

    Raises:
        RuntimeError: If the gather operation fails.
    """
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Get the world size (number of processes in the group)
    # Get the world size (number of processes in the group)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：world_size = get_world_size(cp_group)
    world_size = get_world_size(cp_group)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Create a list to store tensors from all ranks
    # Create a list to store tensors from all ranks
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gathered_tensors = [torch.zeros_like(x) for _ in range(world_size)]
    gathered_tensors = [torch.zeros_like(x) for _ in range(world_size)]

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Gather tensors from all ranks
    # Gather tensors from all ranks
    # 中文说明：开始一个可捕获异常的代码块；代码：try:
    try:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：all_gather(gathered_tensors, x, group=cp_group)
        all_gather(gathered_tensors, x, group=cp_group)
    # 中文说明：处理异常、清理资源或管理上下文；代码：except RuntimeError as e:
    except RuntimeError as e:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise RuntimeError(f"Failed to gather tensors: {e}")
        raise RuntimeError(f"Failed to gather tensors: {e}")

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Concatenate the gathered tensors along the specified dimension
    # Concatenate the gathered tensors along the specified dimension
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return torch.cat(gathered_tensors, dim=seq_dim)
    return torch.cat(gathered_tensors, dim=seq_dim)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def cat_outputs_cp_with_grad(x: Tensor, seq_dim: int, cp_group: ProcessGroup) -> Tensor:
def cat_outputs_cp_with_grad(x: Tensor, seq_dim: int, cp_group: ProcessGroup) -> Tensor:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Concatenate outputs from different ranks in the context parallelism group.

    This function gathers tensors from all ranks in the checkpoint parallelism group
    and concatenates them along the specified sequence dimension.

    It retains computational graph locally for each rank by replacing the portion of the tensor with original output.

    Args:
        x: Input tensor to be concatenated.
        seq_dim: The dimension along which to concatenate the tensors (sequence dimension).
        cp_group: The process group for checkpoint parallelism.

    Returns:
        A tensor that is the concatenation of tensors from all ranks in the cp_group.

    Raises:
        RuntimeError: If the gather operation fails.
    """
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Get the world size (number of processes in the group)
    # Get the world size (number of processes in the group)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cp_size = cp_group.size()
    cp_size = cp_group.size()
    # 中文说明：检查运行时假设是否成立；代码：assert cp_size > 0, "cp_size should be greater than 0"
    assert cp_size > 0, "cp_size should be greater than 0"

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Create a list to store tensors from all ranks
    # Create a list to store tensors from all ranks
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gathered_tensors = [torch.zeros_like(x) for _ in range(cp_size)]
    gathered_tensors = [torch.zeros_like(x) for _ in range(cp_size)]

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Gather tensors from all ranks
    # Gather tensors from all ranks
    # 中文说明：开始一个可捕获异常的代码块；代码：try:
    try:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：all_gather(gathered_tensors, x, group=cp_group)
        all_gather(gathered_tensors, x, group=cp_group)
    # 中文说明：处理异常、清理资源或管理上下文；代码：except RuntimeError as e:
    except RuntimeError as e:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise RuntimeError(f"Failed to gather tensors: {e}")
        raise RuntimeError(f"Failed to gather tensors: {e}")

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank = cp_group.rank()
    rank = cp_group.rank()
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gathered_tensors[rank] = x
    gathered_tensors[rank] = x
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Concatenate the gathered tensors along the specified dimension
    # Concatenate the gathered tensors along the specified dimension
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return torch.cat(gathered_tensors, dim=seq_dim)
    return torch.cat(gathered_tensors, dim=seq_dim)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def robust_broadcast(tensor: torch.Tensor, src: int, pg: ProcessGroup, is_check_shape: bool =...
def robust_broadcast(tensor: torch.Tensor, src: int, pg: ProcessGroup, is_check_shape: bool = False) -> torch.Tensor:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Perform a robust broadcast operation that works regardless of tensor shapes on different ranks.

    Args:
        tensor (torch.Tensor): The tensor to broadcast (on src rank) or receive (on other ranks).
        src (int): The source rank for the broadcast. Defaults to 0.

    Returns:
        torch.Tensor: The broadcasted tensor on all ranks.
    """
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Ensure tensor is on CUDA
    # Ensure tensor is on CUDA
    # 中文说明：根据条件选择执行分支；代码：if tensor.device.type != "cuda":
    if tensor.device.type != "cuda":
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tensor = tensor.cuda()
        tensor = tensor.cuda()

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# First, broadcast the shape of the tensor
    # First, broadcast the shape of the tensor
    # 中文说明：根据条件选择执行分支；代码：if distributed.get_rank() == src:
    if distributed.get_rank() == src:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：shape = torch.tensor(tensor.shape).cuda()
        shape = torch.tensor(tensor.shape).cuda()
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：shape = torch.empty(tensor.dim(), dtype=torch.long).cuda()
        shape = torch.empty(tensor.dim(), dtype=torch.long).cuda()
    # 中文说明：根据条件选择执行分支；代码：if is_check_shape:
    if is_check_shape:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_verify_param_shape_across_processes(pg, [shape])
        _verify_param_shape_across_processes(pg, [shape])
    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.distributed.broadcast(shape, src, group=pg)
    torch.distributed.broadcast(shape, src, group=pg)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Resize the tensor on non-src ranks if necessary
    # Resize the tensor on non-src ranks if necessary
    # 中文说明：根据条件选择执行分支；代码：if distributed.get_rank() != src:
    if distributed.get_rank() != src:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tensor = tensor.new_empty(shape.tolist()).type_as(tensor)
        tensor = tensor.new_empty(shape.tolist()).type_as(tensor)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Now broadcast the tensor data
    # Now broadcast the tensor data
    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.distributed.broadcast(tensor, src, group=pg)
    torch.distributed.broadcast(tensor, src, group=pg)

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return tensor
    return tensor


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def broadcast(
def broadcast(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：item: torch.Tensor | str | None, process_group: Optional[ProcessGroup] = None
    item: torch.Tensor | str | None, process_group: Optional[ProcessGroup] = None
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor | str | None:
) -> torch.Tensor | str | None:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Broadcast the item from the minimum rank in the specified group(s).
    """
    # 中文说明：根据条件选择执行分支；代码：if process_group is None:
    if process_group is None:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return item
        return item

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_rank = min(get_process_group_ranks(process_group))
    min_rank = min(get_process_group_ranks(process_group))
    # 中文说明：根据条件选择执行分支；代码：if isinstance(item, torch.Tensor):
    if isinstance(item, torch.Tensor):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Ensure tensor is on CUDA before broadcasting
        # Ensure tensor is on CUDA before broadcasting
        # 中文说明：根据条件选择执行分支；代码：if item.device.type != "cuda":
        if item.device.type != "cuda":
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：item = item.cuda()
            item = item.cuda()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：item = robust_broadcast(item, min_rank, process_group)
        item = robust_broadcast(item, min_rank, process_group)
    # 中文说明：根据条件选择执行分支；代码：elif item is not None:
    elif item is not None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：broadcastable_list = [item]
        broadcastable_list = [item]
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：broadcast_object_list(broadcastable_list, min_rank, group=process_group)
        broadcast_object_list(broadcastable_list, min_rank, group=process_group)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：item = broadcastable_list[0]
        item = broadcastable_list[0]
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return item
    return item


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def broadcast_split_tensor(
def broadcast_split_tensor(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：tensor: torch.Tensor,
    tensor: torch.Tensor,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：seq_dim: int,
    seq_dim: int,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：process_group: Optional[ProcessGroup] = None,
    process_group: Optional[ProcessGroup] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor:
) -> torch.Tensor:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Broadcast the tensor from the minimum rank in the specified group(s).
    """
    # 中文说明：根据条件选择执行分支；代码：if tensor is None:
    if tensor is None:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return tensor
        return tensor

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Ensure tensor is on CUDA before broadcasting
    # Ensure tensor is on CUDA before broadcasting
    # 中文说明：根据条件选择执行分支；代码：if tensor.device.type != "cuda":
    if tensor.device.type != "cuda":
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tensor = tensor.cuda()
        tensor = tensor.cuda()

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_rank = min(get_process_group_ranks(process_group))
    min_rank = min(get_process_group_ranks(process_group))
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tensor = robust_broadcast(tensor, min_rank, process_group)
    tensor = robust_broadcast(tensor, min_rank, process_group)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return split_inputs_cp(tensor, seq_dim, process_group)
    return split_inputs_cp(tensor, seq_dim, process_group)
