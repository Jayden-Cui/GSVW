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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from __future__ import annotations
from __future__ import annotations

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from contextlib import contextmanager
from contextlib import contextmanager
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from functools import partial
from functools import partial

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed.algorithms._checkpoint.checkpoint_wrapper import (
from torch.distributed.algorithms._checkpoint.checkpoint_wrapper import (
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CheckpointImpl,
    CheckpointImpl,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：apply_activation_checkpointing,
    apply_activation_checkpointing,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：checkpoint_wrapper,
    checkpoint_wrapper,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed.device_mesh import init_device_mesh
from torch.distributed.device_mesh import init_device_mesh
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed.fsdp._runtime_utils import (
from torch.distributed.fsdp._runtime_utils import (
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_post_forward,
    _post_forward,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_post_forward_reshard,
    _post_forward_reshard,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_pre_forward,
    _pre_forward,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_pre_forward_unshard,
    _pre_forward_unshard,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_root_pre_forward,
    _root_pre_forward,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed.utils import _p_assert
from torch.distributed.utils import _p_assert

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import distributed, log
from imaginaire.utils import distributed, log


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def apply_fsdp_checkpointing(model, list_block_cls):
def apply_fsdp_checkpointing(model, list_block_cls):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""apply activation checkpointing to model
    """apply activation checkpointing to model
    returns None as model is updated directly
    """
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.critical("--> applying fdsp activation checkpointing...")
    log.critical("--> applying fdsp activation checkpointing...")
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：non_reentrant_wrapper = partial(
    non_reentrant_wrapper = partial(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：checkpoint_wrapper,
        checkpoint_wrapper,
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# offload_to_cpu=False,
        # offload_to_cpu=False,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint_impl=CheckpointImpl.NO_REENTRANT,
        checkpoint_impl=CheckpointImpl.NO_REENTRANT,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def check_fn(submodule):
    def check_fn(submodule):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：result = False
        result = False
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for block_cls in list_block_cls:
        for block_cls in list_block_cls:
            # 中文说明：根据条件选择执行分支；代码：if isinstance(submodule, block_cls):
            if isinstance(submodule, block_cls):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：result = True
                result = True
                # 中文说明：执行循环控制或空操作；代码：break
                break
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return result
        return result

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：apply_activation_checkpointing(model, checkpoint_wrapper_fn=non_reentrant_wrapper, check_fn=c...
    apply_activation_checkpointing(model, checkpoint_wrapper_fn=non_reentrant_wrapper, check_fn=check_fn)


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@contextmanager
@contextmanager
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def possible_fsdp_scope(
def possible_fsdp_scope(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model: torch.nn.Module,
    model: torch.nn.Module,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enabled = isinstance(model, FSDP)
    enabled = isinstance(model, FSDP)
    # 中文说明：根据条件选择执行分支；代码：if enabled:
    if enabled:
        # 中文说明：检查运行时假设是否成立；代码：assert not torch.is_grad_enabled(), "FSDP context should be entered with grad disabled"
        assert not torch.is_grad_enabled(), "FSDP context should be entered with grad disabled"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：handle = model._handle
        handle = model._handle
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：args, kwargs = [0], dict(dummy=0)
        args, kwargs = [0], dict(dummy=0)
        # 中文说明：处理异常、清理资源或管理上下文；代码：with torch.autograd.profiler.record_function("FullyShardedDataParallel.possible_fsdp_scope"):
        with torch.autograd.profiler.record_function("FullyShardedDataParallel.possible_fsdp_scope"):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：args, kwargs = _root_pre_forward(model, model, args, kwargs)
            args, kwargs = _root_pre_forward(model, model, args, kwargs)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：unused = None
            unused = None
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：args, kwargs = _pre_forward(
            args, kwargs = _pre_forward(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model,
                model,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：handle,
                handle,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_pre_forward_unshard,
                _pre_forward_unshard,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model._fsdp_wrapped_module,
                model._fsdp_wrapped_module,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：args,
                args,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：kwargs,
                kwargs,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：根据条件选择执行分支；代码：if handle:
            if handle:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_p_assert(
                _p_assert(
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：handle.flat_param.device == model.compute_device,
                    handle.flat_param.device == model.compute_device,
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："Expected `FlatParameter` to be on the compute device "
                    "Expected `FlatParameter` to be on the compute device "
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"{model.compute_device} but got {handle.flat_param.device}",
                    f"{model.compute_device} but got {handle.flat_param.device}",
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
    # 中文说明：开始一个可捕获异常的代码块；代码：try:
    try:
        # 中文说明：从生成器逐步产生本行指定的值；代码：yield None
        yield None
    # 中文说明：处理异常、清理资源或管理上下文；代码：finally:
    finally:
        # 中文说明：根据条件选择执行分支；代码：if enabled:
        if enabled:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output = {"output": 1}
            output = {"output": 1}
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_post_forward(model, handle, _post_forward_reshard, model, unused, output)
            _post_forward(model, handle, _post_forward_reshard, model, unused, output)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def hsdp_device_mesh(replica_group_size=None, sharding_group_size=None, device=None):
def hsdp_device_mesh(replica_group_size=None, sharding_group_size=None, device=None):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
     Initializes a device mesh for use with Hybrid Sharding strategy in FSDP (HSDP) training.

    This function requires explicit sizes for replica and sharding groups to accommodate models
    whose GPU fit is unknown, providing flexibility in distributed training setups.

    Args:
        replica_group_size (int): The size of each replica group. Must be provided to ensure
            the model fits within the available resources.
        sharding_group_size (int): The size of each sharding group that the model can fit. Must be provided to
            ensure the correct distribution of model parameters.
        device (str, optional): The device to use (e.g., "cuda:0"). If None, defaults to "cuda"
            with the local rank as the device index.

    Returns:
        A device mesh object compatible with FSDP.

    Raises:
        ValueError: If replica_group_size or sharding_group_size are not provided, or if the
            world size is not evenly divisible by the sharding group size.
        RuntimeError: If a valid device mesh cannot be created.

    Usage:
        If your model fits on 4 GPUS, and you have 3 nodes of 8 GPUs, then:
        Sharding_Group_Size = 4
        Replica_Groups_Size = (24 total gpus, 4 per sharding group) = 6 Replica Groups
        >>> device_mesh = initialize_device_mesh(replica_group_size, sharding_group_size)
        >>> sharded_model = FSDP(model, device_mesh=device_mesh, ...)
    """

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# world_size = int(os.getenv("WORLD_SIZE", "1"))
    # world_size = int(os.getenv("WORLD_SIZE", "1"))
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：world_size = distributed.get_world_size()
    world_size = distributed.get_world_size()
    # 中文说明：根据条件选择执行分支；代码：if sharding_group_size is None:
    if sharding_group_size is None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sharding_group_size = min(world_size, 8)
        sharding_group_size = min(world_size, 8)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sharding_group_size = min(sharding_group_size, world_size)
    sharding_group_size = min(sharding_group_size, world_size)
    # 中文说明：根据条件选择执行分支；代码：if replica_group_size is None:
    if replica_group_size is None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：replica_group_size = world_size // sharding_group_size
        replica_group_size = world_size // sharding_group_size

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：device = device or "cuda"
    device = device or "cuda"

    # 中文说明：根据条件选择执行分支；代码：if world_size % sharding_group_size != 0:
    if world_size % sharding_group_size != 0:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(
        raise ValueError(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"World size {world_size} is not evenly divisible by " f"sharding group size {sharding_group_...
            f"World size {world_size} is not evenly divisible by " f"sharding group size {sharding_group_size}."
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：根据条件选择执行分支；代码：if (world_size // sharding_group_size) % replica_group_size != 0:
    if (world_size // sharding_group_size) % replica_group_size != 0:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(
        raise ValueError(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"The calculated number of replica groups is not evenly divisible by "
            f"The calculated number of replica groups is not evenly divisible by "
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"replica_group_size {replica_group_size}."
            f"replica_group_size {replica_group_size}."
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：device_mesh = init_device_mesh(
    device_mesh = init_device_mesh(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：device, (replica_group_size, sharding_group_size), mesh_dim_names=("replicate", "shard")
        device, (replica_group_size, sharding_group_size), mesh_dim_names=("replicate", "shard")
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：根据条件选择执行分支；代码：if device_mesh is None:
    if device_mesh is None:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise RuntimeError("Failed to create a valid device mesh.")
        raise RuntimeError("Failed to create a valid device mesh.")

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.critical(
    log.critical(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Device mesh initialized with replica group size {replica_group_size} and sharding group siz...
        f"Device mesh initialized with replica group size {replica_group_size} and sharding group size {sharding_group_size}"
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return device_mesh
    return device_mesh
