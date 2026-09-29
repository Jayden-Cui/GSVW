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

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import collections
import collections
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import collections.abc
import collections.abc
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import ctypes
import ctypes
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import functools
import functools
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from contextlib import contextmanager
from contextlib import contextmanager
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from datetime import timedelta
from datetime import timedelta
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import TYPE_CHECKING, Any, Callable, Container, Optional
from typing import TYPE_CHECKING, Any, Callable, Container, Optional

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import pynvml
import pynvml
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.distributed as dist
import torch.distributed as dist
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed import get_process_group_ranks
from torch.distributed import get_process_group_ranks

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.device import Device
from imaginaire.utils.device import Device

# 中文说明：根据条件选择执行分支；代码：if dist.is_available():
if dist.is_available():
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed.distributed_c10d import _get_default_group
    from torch.distributed.distributed_c10d import _get_default_group
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed.utils import _sync_module_states, _verify_param_shape_across_processes
    from torch.distributed.utils import _sync_module_states, _verify_param_shape_across_processes

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log

# 中文说明：根据条件选择执行分支；代码：if TYPE_CHECKING:
if TYPE_CHECKING:
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.config import DDPConfig
    from imaginaire.config import DDPConfig

# 中文说明：开始一个可捕获异常的代码块；代码：try:
try:
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from megatron.core import parallel_state
    from megatron.core import parallel_state
# 中文说明：处理异常、清理资源或管理上下文；代码：except ImportError:
except ImportError:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print("Megatron-core is not installed.")
    print("Megatron-core is not installed.")


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def init() -> int | None:
def init() -> int | None:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Initialize distributed training."""
    """Initialize distributed training."""
    # 中文说明：根据条件选择执行分支；代码：if dist.is_initialized():
    if dist.is_initialized():
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return torch.cuda.current_device()
        return torch.cuda.current_device()

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Set GPU affinity.
    # Set GPU affinity.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pynvml.nvmlInit()
    pynvml.nvmlInit()
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：local_rank = int(os.getenv("LOCAL_RANK", 0))
    local_rank = int(os.getenv("LOCAL_RANK", 0))
    # 中文说明：开始一个可捕获异常的代码块；代码：try:
    try:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：device = Device(local_rank)
        device = Device(local_rank)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.sched_setaffinity(0, device.get_cpu_affinity())
        os.sched_setaffinity(0, device.get_cpu_affinity())
    # 中文说明：处理异常、清理资源或管理上下文；代码：except pynvml.NVMLError as e:
    except pynvml.NVMLError as e:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(f"Failed to set device affinity: {e}")
        log.warning(f"Failed to set device affinity: {e}")
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Set up NCCL communication.
    # Set up NCCL communication.
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：os.environ["TORCH_NCCL_BLOCKING_WAIT"] = "0"
    os.environ["TORCH_NCCL_BLOCKING_WAIT"] = "0"
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：os.environ["TORCH_NCCL_ASYNC_ERROR_HANDLING"] = "1"
    os.environ["TORCH_NCCL_ASYNC_ERROR_HANDLING"] = "1"
    # 中文说明：根据条件选择执行分支；代码：if dist.is_available():
    if dist.is_available():
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.set_device(local_rank)
        torch.cuda.set_device(local_rank)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Get the timeout value from environment variable
        # Get the timeout value from environment variable
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：timeout_seconds = os.getenv("TORCH_NCCL_HEARTBEAT_TIMEOUT_SEC", 1800)
        timeout_seconds = os.getenv("TORCH_NCCL_HEARTBEAT_TIMEOUT_SEC", 1800)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Convert the timeout to an integer (if it isn't already) and then to a timedelta
        # Convert the timeout to an integer (if it isn't already) and then to a timedelta
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：timeout_timedelta = timedelta(seconds=int(timeout_seconds))
        timeout_timedelta = timedelta(seconds=int(timeout_seconds))
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dist.init_process_group(backend="nccl", init_method="env://", timeout=timeout_timedelta)
        dist.init_process_group(backend="nccl", init_method="env://", timeout=timeout_timedelta)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(
        log.info(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Initialized distributed training with local rank {local_rank} with timeout {timeout_seconds}",
            f"Initialized distributed training with local rank {local_rank} with timeout {timeout_seconds}",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank0_only=False,
            rank0_only=False,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Increase the L2 fetch granularity for faster speed.
    # Increase the L2 fetch granularity for faster speed.
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_libcudart = ctypes.CDLL("libcudart.so")
    _libcudart = ctypes.CDLL("libcudart.so")
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Set device limit on the current device.
    # Set device limit on the current device.
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：p_value = ctypes.cast((ctypes.c_int * 1)(), ctypes.POINTER(ctypes.c_int))
    p_value = ctypes.cast((ctypes.c_int * 1)(), ctypes.POINTER(ctypes.c_int))
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_libcudart.cudaDeviceSetLimit(ctypes.c_int(0x05), ctypes.c_int(128))
    _libcudart.cudaDeviceSetLimit(ctypes.c_int(0x05), ctypes.c_int(128))
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_libcudart.cudaDeviceGetLimit(p_value, ctypes.c_int(0x05))
    _libcudart.cudaDeviceGetLimit(p_value, ctypes.c_int(0x05))
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Training with {get_world_size()} GPUs.")
    log.info(f"Training with {get_world_size()} GPUs.")


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_rank(group: Optional[dist.ProcessGroup] = None) -> int:
def get_rank(group: Optional[dist.ProcessGroup] = None) -> int:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Get the rank (GPU device) of the worker.
    """Get the rank (GPU device) of the worker.

    Returns:
        rank (int): The rank of the worker.
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank = 0
    rank = 0
    # 中文说明：根据条件选择执行分支；代码：if dist.is_available() and dist.is_initialized():
    if dist.is_available() and dist.is_initialized():
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank = dist.get_rank(group)
        rank = dist.get_rank(group)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return rank
    return rank


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_world_size(group: Optional[dist.ProcessGroup] = None) -> int:
def get_world_size(group: Optional[dist.ProcessGroup] = None) -> int:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Get world size. How many GPUs are available in this job.
    """Get world size. How many GPUs are available in this job.

    Returns:
        world_size (int): The total number of GPUs available in this job.
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：world_size = 1
    world_size = 1
    # 中文说明：根据条件选择执行分支；代码：if dist.is_available() and dist.is_initialized():
    if dist.is_available() and dist.is_initialized():
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：world_size = dist.get_world_size(group)
        world_size = dist.get_world_size(group)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return world_size
    return world_size


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_rank0() -> bool:
def is_rank0() -> bool:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Check if current process is the master GPU.
    """Check if current process is the master GPU.

    Returns:
        (bool): True if this function is called from the master GPU, else False.
    """
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return get_rank() == 0
    return get_rank() == 0


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_local_rank0() -> bool:
def is_local_rank0() -> bool:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Check if current process is the local master GPU in the current node.
    """Check if current process is the local master GPU in the current node.

    Returns:
        (bool): True if this function is called from the local master GPU, else False.
    """
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return torch.cuda.current_device() == 0
    return torch.cuda.current_device() == 0


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def rank0_only(func: Callable) -> Callable:
def rank0_only(func: Callable) -> Callable:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Apply this function only to the master GPU.
    """Apply this function only to the master GPU.

    Example usage:
        @rank0_only
        def func(x):
            return x + 3

    Args:
        func (Callable): a function.

    Returns:
        (Callable): A function wrapper executing the function only on the master GPU.
    """

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@functools.wraps(func)
    @functools.wraps(func)
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def wrapper(*args, **kwargs): # noqa: ANN202
    def wrapper(*args, **kwargs):  # noqa: ANN202
        # 中文说明：根据条件选择执行分支；代码：if is_rank0():
        if is_rank0():
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return func(*args, **kwargs)
            return func(*args, **kwargs)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return None
            return None

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return wrapper
    return wrapper


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def barrier() -> None:
def barrier() -> None:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Barrier for all GPUs."""
    """Barrier for all GPUs."""
    # 中文说明：根据条件选择执行分支；代码：if dist.is_available() and dist.is_initialized():
    if dist.is_available() and dist.is_initialized():
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dist.barrier()
        dist.barrier()


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def rank0_first(func: Callable) -> Callable:
def rank0_first(func: Callable) -> Callable:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""run the function on rank 0 first, then on other ranks."""
    """run the function on rank 0 first, then on other ranks."""

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@functools.wraps(func)
    @functools.wraps(func)
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def wrapper(*args, **kwargs): # noqa: ANN202
    def wrapper(*args, **kwargs):  # noqa: ANN202
        # 中文说明：根据条件选择执行分支；代码：if is_rank0():
        if is_rank0():
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：result = func(*args, **kwargs)
            result = func(*args, **kwargs)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：barrier()
        barrier()
        # 中文说明：根据条件选择执行分支；代码：if not is_rank0():
        if not is_rank0():
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：result = func(*args, **kwargs)
            result = func(*args, **kwargs)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return result
        return result

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return wrapper
    return wrapper


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def parallel_model_wrapper(config_ddp: DDPConfig, model: torch.nn.Module) -> torch.nn.Module ...
def parallel_model_wrapper(config_ddp: DDPConfig, model: torch.nn.Module) -> torch.nn.Module | DistributedDataParallel:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Wraps the model to enable data parallalism for training across multiple GPU devices.
    """Wraps the model to enable data parallalism for training across multiple GPU devices.

    Args:
        config_ddp (DDPConfig): The data parallel config.
        model (torch.nn.Module): The PyTorch module.

    Returns:
        model (torch.nn.Module | DistributedDataParallel): The data parallel model wrapper
            if distributed environment is available, otherwise return the original model.
    """
    # 中文说明：根据条件选择执行分支；代码：if dist.is_available() and dist.is_initialized():
    if dist.is_available() and dist.is_initialized():
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：local_rank = int(os.getenv("LOCAL_RANK", 0))
        local_rank = int(os.getenv("LOCAL_RANK", 0))
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ddp_group = parallel_state.get_data_parallel_group(with_context_parallel=True)
            ddp_group = parallel_state.get_data_parallel_group(with_context_parallel=True)
        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
        except Exception as e:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(e)
            log.info(e)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("parallel_state not initialized, treating all GPUs equally for DDP")
            log.info("parallel_state not initialized, treating all GPUs equally for DDP")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ddp_group = None
            ddp_group = None

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model = DistributedDataParallel(
        model = DistributedDataParallel(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model,
            model,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：device_ids=[local_rank],
            device_ids=[local_rank],
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_device=local_rank,
            output_device=local_rank,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：find_unused_parameters=config_ddp.find_unused_parameters,
            find_unused_parameters=config_ddp.find_unused_parameters,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：static_graph=config_ddp.static_graph,
            static_graph=config_ddp.static_graph,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：broadcast_buffers=config_ddp.broadcast_buffers,
            broadcast_buffers=config_ddp.broadcast_buffers,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：process_group=ddp_group,
            process_group=ddp_group,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return model
    return model


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class DistributedDataParallel(torch.nn.parallel.DistributedDataParallel):
class DistributedDataParallel(torch.nn.parallel.DistributedDataParallel):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""This extends torch.nn.parallel.DistributedDataParallel with .training_step().
    """This extends torch.nn.parallel.DistributedDataParallel with .training_step().

    This borrows the concept of `forward-redirection` from Pytorch lightning. It wraps an ImaginaireModel such that
    model.training_step() would be executed when calling self.training_step(), while preserving the behavior of calling
    model() for Pytorch modules. Internally, this is a double rerouting mechanism (training_step -> forward ->
    training_step), allowing us to preserve the function names and signatures.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, model: torch.nn.Module, *args, **kwargs):
    def __init__(self, model: torch.nn.Module, *args, **kwargs):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(model, *args, **kwargs)
        super().__init__(model, *args, **kwargs)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.show_sync_grad_static_graph_warning = True
        self.show_sync_grad_static_graph_warning = True

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def training_step(self, *args, **kwargs) -> Any:
    def training_step(self, *args, **kwargs) -> Any:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Cache the original model.forward() method.
        # Cache the original model.forward() method.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：original_forward = self.module.forward
        original_forward = self.module.forward

        # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def wrapped_training_step(*_args, **_kwargs): # noqa: ANN202
        def wrapped_training_step(*_args, **_kwargs):  # noqa: ANN202
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Unpatch immediately before calling training_step() because itself may want to call the real...
            # Unpatch immediately before calling training_step() because itself may want to call the real forward.
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.module.forward = original_forward
            self.module.forward = original_forward
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# The actual .training_step().
            # The actual .training_step().
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.module.training_step(*_args, **_kwargs)
            return self.module.training_step(*_args, **_kwargs)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Patch the original_module's forward so we can redirect the arguments back to the real method.
        # Patch the original_module's forward so we can redirect the arguments back to the real method.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.module.forward = wrapped_training_step
        self.module.forward = wrapped_training_step
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Call self, which implicitly calls self.forward() --> model.forward(), which is now model.tr...
        # Call self, which implicitly calls self.forward() --> model.forward(), which is now model.training_step().
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Without calling self.forward() or model.forward() explciitly, implicit hooks are also execu...
        # Without calling self.forward() or model.forward() explciitly, implicit hooks are also executed.
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self(*args, **kwargs)
        return self(*args, **kwargs)


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@contextmanager
@contextmanager
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def ddp_sync_grad(model, enabled):
def ddp_sync_grad(model, enabled):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""
    r"""
    Context manager to enable/disable gradient synchronizations across DDP processes for DDP model.
    Modified from:
    https://pytorch.org/docs/stable/_modules/torch/nn/parallel/distributed.html#DistributedDataParallel.no_sync
    Note that this is incompatible with static_graph=True and will be an no-op if static_graph=True.

    Within this context, gradients will be accumulated on module
    variables, which will later be synchronized in the first
    forward-backward pass exiting the context.

    .. warning::
        The forward pass should be included inside the context manager, or
        else gradients will still be synchronized.
    """
    # 中文说明：检查运行时假设是否成立；代码：assert isinstance(model, torch.nn.Module)
    assert isinstance(model, torch.nn.Module)
    # 中文说明：根据条件选择执行分支；代码：if isinstance(model, DistributedDataParallel):
    if isinstance(model, DistributedDataParallel):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：old_require_backward_grad_sync = model.require_backward_grad_sync
        old_require_backward_grad_sync = model.require_backward_grad_sync
        # 中文说明：根据条件选择执行分支；代码：if model.static_graph and model.require_backward_grad_sync != enabled:
        if model.static_graph and model.require_backward_grad_sync != enabled:
            # 中文说明：根据条件选择执行分支；代码：if model.show_sync_grad_static_graph_warning:
            if model.show_sync_grad_static_graph_warning:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning("DDP static_graph=True is incompatible with sync_grad(). Performance will be redu...
                log.warning("DDP static_graph=True is incompatible with sync_grad(). Performance will be reduced.")
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model.show_sync_grad_static_graph_warning = False
                model.show_sync_grad_static_graph_warning = False
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model.require_backward_grad_sync = enabled
            model.require_backward_grad_sync = enabled
    # 中文说明：开始一个可捕获异常的代码块；代码：try:
    try:
        # 中文说明：从生成器逐步产生本行指定的值；代码：yield
        yield
    # 中文说明：处理异常、清理资源或管理上下文；代码：finally:
    finally:
        # 中文说明：根据条件选择执行分支；代码：if isinstance(model, DistributedDataParallel):
        if isinstance(model, DistributedDataParallel):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model.require_backward_grad_sync = old_require_backward_grad_sync
            model.require_backward_grad_sync = old_require_backward_grad_sync


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def collate_batches(data_batches: list[dict[str, torch.Tensor]]) -> torch.Tensor | dict[str, ...
def collate_batches(data_batches: list[dict[str, torch.Tensor]]) -> torch.Tensor | dict[str, torch.Tensor]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Aggregate the list of data batches from all devices and process the results.
    """Aggregate the list of data batches from all devices and process the results.

    This is used for gathering validation data batches with imaginaire.utils.dataloader.DistributedEvalSampler.
    It will return the data/output of the entire validation set in its original index order. The sizes of data_batches
    in different ranks may differ by 1 (if dataset size is not evenly divisible), in which case a dummy sample will be
    created before calling dis.all_gather().

    Args:
        data_batches (list[dict[str, torch.Tensor]]): List of tensors or (hierarchical) dictionary where
            leaf entries are tensors.

    Returns:
        data_gather (torch.Tensor | dict[str, torch.Tensor]): tensors or (hierarchical) dictionary where
            leaf entries are concatenated tensors.
    """
    # 中文说明：根据条件选择执行分支；代码：if isinstance(data_batches[0], torch.Tensor):
    if isinstance(data_batches[0], torch.Tensor):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Concatenate the local data batches.
        # Concatenate the local data batches.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_concat = torch.cat(data_batches, dim=0) # type: ignore
        data_concat = torch.cat(data_batches, dim=0)  # type: ignore
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Get the largest number of local samples from all ranks to determine whether to dummy-pad on...
        # Get the largest number of local samples from all ranks to determine whether to dummy-pad on this rank.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_num_local_samples = torch.tensor(len(data_concat), device="cuda")
        max_num_local_samples = torch.tensor(len(data_concat), device="cuda")
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dist.all_reduce(max_num_local_samples, op=dist.ReduceOp.MAX)
        dist.all_reduce(max_num_local_samples, op=dist.ReduceOp.MAX)
        # 中文说明：根据条件选择执行分支；代码：if len(data_concat) < max_num_local_samples:
        if len(data_concat) < max_num_local_samples:
            # 中文说明：检查运行时假设是否成立；代码：assert len(data_concat) + 1 == max_num_local_samples
            assert len(data_concat) + 1 == max_num_local_samples
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dummy = torch.empty_like(data_concat[:1])
            dummy = torch.empty_like(data_concat[:1])
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_concat = torch.cat([data_concat, dummy], dim=0)
            data_concat = torch.cat([data_concat, dummy], dim=0)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dummy_count = torch.tensor(1, device="cuda")
            dummy_count = torch.tensor(1, device="cuda")
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dummy_count = torch.tensor(0, device="cuda")
            dummy_count = torch.tensor(0, device="cuda")
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Get all concatenated batches from all ranks and concatenate again.
        # Get all concatenated batches from all ranks and concatenate again.
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dist.all_reduce(dummy_count, op=dist.ReduceOp.SUM)
        dist.all_reduce(dummy_count, op=dist.ReduceOp.SUM)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_concat = all_gather_tensor(data_concat.contiguous())
        data_concat = all_gather_tensor(data_concat.contiguous())
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_collate = torch.stack(data_concat, dim=1).flatten(start_dim=0, end_dim=1)
        data_collate = torch.stack(data_concat, dim=1).flatten(start_dim=0, end_dim=1)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Remove the dummy samples.
        # Remove the dummy samples.
        # 中文说明：根据条件选择执行分支；代码：if dummy_count > 0:
        if dummy_count > 0:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_collate = data_collate[:-dummy_count]
            data_collate = data_collate[:-dummy_count]
    # 中文说明：根据条件选择执行分支；代码：elif isinstance(data_batches[0], collections.abc.Mapping):
    elif isinstance(data_batches[0], collections.abc.Mapping):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_collate = dict()
        data_collate = dict()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key in data_batches[0].keys():
        for key in data_batches[0].keys():
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_collate[key] = collate_batches([data[key] for data in data_batches]) # type: ignore
            data_collate[key] = collate_batches([data[key] for data in data_batches])  # type: ignore
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError
        raise TypeError
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return data_collate
    return data_collate


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.no_grad()
@torch.no_grad()
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def all_gather_tensor(tensor: torch.Tensor) -> list[torch.Tensor]:
def all_gather_tensor(tensor: torch.Tensor) -> list[torch.Tensor]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Gather the corresponding tensor from all GPU devices to a list.
    """Gather the corresponding tensor from all GPU devices to a list.

    Args:
        tensor (torch.Tensor): Pytorch tensor.

    Returns:
        tensor_list (list[torch.Tensor]): A list of Pytorch tensors gathered from all GPU devices.
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tensor_list = [torch.zeros_like(tensor) for _ in range(get_world_size())]
    tensor_list = [torch.zeros_like(tensor) for _ in range(get_world_size())]
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dist.all_gather(tensor_list, tensor)
    dist.all_gather(tensor_list, tensor)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return tensor_list
    return tensor_list


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def broadcast(tensor, src, group=None, async_op=False):
def broadcast(tensor, src, group=None, async_op=False):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：world_size = get_world_size()
    world_size = get_world_size()
    # 中文说明：根据条件选择执行分支；代码：if world_size < 2:
    if world_size < 2:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return tensor
        return tensor
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dist.broadcast(tensor, src=src, group=group, async_op=async_op)
    dist.broadcast(tensor, src=src, group=group, async_op=async_op)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def dist_reduce_tensor(tensor, rank=0, reduce="mean"):
def dist_reduce_tensor(tensor, rank=0, reduce="mean"):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Reduce to rank 0"""
    r"""Reduce to rank 0"""
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：world_size = get_world_size()
    world_size = get_world_size()
    # 中文说明：根据条件选择执行分支；代码：if world_size < 2:
    if world_size < 2:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return tensor
        return tensor
    # 中文说明：处理异常、清理资源或管理上下文；代码：with torch.no_grad():
    with torch.no_grad():
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dist.reduce(tensor, dst=rank)
        dist.reduce(tensor, dst=rank)
        # 中文说明：根据条件选择执行分支；代码：if get_rank() == rank:
        if get_rank() == rank:
            # 中文说明：根据条件选择执行分支；代码：if reduce == "mean":
            if reduce == "mean":
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tensor /= world_size
                tensor /= world_size
            # 中文说明：根据条件选择执行分支；代码：elif reduce == "sum":
            elif reduce == "sum":
                # 中文说明：执行循环控制或空操作；代码：pass
                pass
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise NotImplementedError
                raise NotImplementedError
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return tensor
    return tensor


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def sync_model_states(
def sync_model_states(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model: torch.nn.Module,
    model: torch.nn.Module,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：process_group: Optional[dist.ProcessGroup] = None,
    process_group: Optional[dist.ProcessGroup] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：src: int = 0,
    src: int = 0,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：params_and_buffers_to_ignore: Optional[Container[str]] = None,
    params_and_buffers_to_ignore: Optional[Container[str]] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：broadcast_buffers: bool = True,
    broadcast_buffers: bool = True,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Modify based on DDP source code
    Synchronizes the parameters and buffers of a model across different processes in a distributed setting.

    This function ensures that all processes in the specified process group have the same initial parameters and
    buffers from the source rank, typically rank 0. It is useful when different processes start with different model
    states and a synchronization is required to ensure consistency across all ranks.

    Args:
        model (nn.Module): The model whose parameters and buffers are to be synchronized.
        process_group (dist.ProcessGroup, optional): The process group for communication. If None,
            the default group is used. Defaults to None.
        src (int, optional): The source rank from which parameters and buffers will be broadcasted.
            Defaults to 0.
        params_and_buffers_to_ignore (Optional[Container[str]], optional): A container of parameter and buffer
            names to exclude from synchronization. Defaults to None, which means all parameters and buffers are
            included.
        broadcast_buffers (bool, optional): Whether to broadcast buffers or not. Defaults to True.

    Side Effects:
        This function modifies the state of the model in-place to synchronize it with the source rank's model state.

    Raises:
        RuntimeError: If the shapes of parameters across processes do not match, a runtime error will be raised.

    Examples:
        >>> # downloading duplicated model weights from s3 in each rank and save network bandwidth
        >>> # useful and save our time when model weights are huge
        >>> if dist.get_rank == 0:
        >>>     model.load_state_dict(network_bound_weights_download_fn(s3_weights_path))
        >>> dist.barrir()
        >>> sync_model_states(model) # sync rank0 weights to other ranks
    """
    # 中文说明：根据条件选择执行分支；代码：if not dist.is_available() or not dist.is_initialized():
    if not dist.is_available() or not dist.is_initialized():
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return
        return
    # 中文说明：根据条件选择执行分支；代码：if process_group is None:
    if process_group is None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：process_group = _get_default_group()
        process_group = _get_default_group()
    # 中文说明：根据条件选择执行分支；代码：if not params_and_buffers_to_ignore:
    if not params_and_buffers_to_ignore:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：params_and_buffers_to_ignore = set()
        params_and_buffers_to_ignore = set()

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(
    log.info(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Synchronizing model states from rank {src} to all ranks in process group {get_process_group...
        f"Synchronizing model states from rank {src} to all ranks in process group {get_process_group_ranks(process_group)}."
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Build tuple of (module, parameter) for all parameters that require grads.
    # Build tuple of (module, parameter) for all parameters that require grads.
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：modules_and_parameters = [
    modules_and_parameters = [
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：(module, parameter)
        (module, parameter)
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for module_name, module in model.named_modules()
        for module_name, module in model.named_modules()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for parameter in [
        for parameter in [
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：param
            param
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Note that we access module.named_parameters instead of
            # Note that we access module.named_parameters instead of
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# parameters(module). parameters(module) is only needed in the
            # parameters(module). parameters(module) is only needed in the
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# single-process multi device case, where it accesses replicated
            # single-process multi device case, where it accesses replicated
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# parameters through _former_parameters.
            # parameters through _former_parameters.
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for param_name, param in module.named_parameters(recurse=False)
            for param_name, param in module.named_parameters(recurse=False)
            # 中文说明：根据条件选择执行分支；代码：if f"{module_name}.{param_name}" not in params_and_buffers_to_ignore
            if f"{module_name}.{param_name}" not in params_and_buffers_to_ignore
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# if param.requires_grad
            # if param.requires_grad
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# and f"{module_name}.{param_name}" not in params_and_buffers_to_ignore
            # and f"{module_name}.{param_name}" not in params_and_buffers_to_ignore
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
        ]
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
    ]

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Deduplicate any parameters that might be shared across child modules.
    # Deduplicate any parameters that might be shared across child modules.
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：memo = set()
    memo = set()
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：modules_and_parameters = [
    modules_and_parameters = [
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# "p not in memo" is the deduplication check.
        # "p not in memo" is the deduplication check.
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# "not memo.add(p)" is always True, and it's only there to cause "add(p)" if needed.
        # "not memo.add(p)" is always True, and it's only there to cause "add(p)" if needed.
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：(m, p)
        (m, p)
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for m, p in modules_and_parameters
        for m, p in modules_and_parameters
        # 中文说明：根据条件选择执行分支；代码：if p not in memo and not memo.add(p) # type: ignore[func-returns-value]
        if p not in memo and not memo.add(p)  # type: ignore[func-returns-value]
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
    ]

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Build list of parameters.
    # Build list of parameters.
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：parameters = [parameter for _, parameter in modules_and_parameters]
    parameters = [parameter for _, parameter in modules_and_parameters]
    # 中文说明：根据条件选择执行分支；代码：if len(parameters) == 0:
    if len(parameters) == 0:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return
        return

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_verify_param_shape_across_processes(process_group, parameters)
    _verify_param_shape_across_processes(process_group, parameters)

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_sync_module_states(
    _sync_module_states(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：module=model,
        module=model,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：process_group=process_group,
        process_group=process_group,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：broadcast_bucket_size=int(250 * 1024 * 1024),
        broadcast_bucket_size=int(250 * 1024 * 1024),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：src=src,
        src=src,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：params_and_buffers_to_ignore=params_and_buffers_to_ignore,
        params_and_buffers_to_ignore=params_and_buffers_to_ignore,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：broadcast_buffers=broadcast_buffers,
        broadcast_buffers=broadcast_buffers,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
