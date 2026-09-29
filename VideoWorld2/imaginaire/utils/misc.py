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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import functools
import functools
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import json
import json
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import random
import random
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import time
import time
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from contextlib import ContextDecorator
from contextlib import ContextDecorator
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from dataclasses import fields
from dataclasses import fields
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any, Callable, List, Tuple, TypeVar, Union
from typing import Any, Callable, List, Tuple, TypeVar, Union

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import termcolor
import termcolor
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed._functional_collectives import AsyncCollectiveTensor
from torch.distributed._functional_collectives import AsyncCollectiveTensor
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed._tensor.api import DTensor
from torch.distributed._tensor.api import DTensor

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import distributed, log
from imaginaire.utils import distributed, log


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def requires_grad(model: torch.nn.Module, value: bool = True) -> None:
def requires_grad(model: torch.nn.Module, value: bool = True) -> None:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Set a model to require gradients or not.
    """Set a model to require gradients or not.

    Args:
        model (torch.nn.Module): Neural network model.
        value (bool): Whether the network requires gradients or not.
    """
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for p in model.parameters():
    for p in model.parameters():
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：p.requires_grad = value
        p.requires_grad = value


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def to(
def to(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data: Any,
    data: Any,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：device: str | torch.device | None = None,
    device: str | torch.device | None = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dtype: torch.dtype | None = None,
    dtype: torch.dtype | None = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：memory_format: torch.memory_format = torch.preserve_format,
    memory_format: torch.memory_format = torch.preserve_format,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Any:
) -> Any:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Recursively cast data into the specified device, dtype, and/or memory_format.
    """Recursively cast data into the specified device, dtype, and/or memory_format.

    The input data can be a tensor, a list of tensors, a dict of tensors.
    See the documentation for torch.Tensor.to() for details.

    Args:
        data (Any): Input data.
        device (str | torch.device): GPU device (default: None).
        dtype (torch.dtype): data type (default: None).
        memory_format (torch.memory_format): memory organization format (default: torch.preserve_format).

    Returns:
        data (Any): Data cast to the specified device, dtype, and/or memory_format.
    """
    # 中文说明：检查运行时假设是否成立；代码：assert (
    assert (
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：device is not None or dtype is not None or memory_format is not None
        device is not None or dtype is not None or memory_format is not None
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), "at least one of device, dtype, memory_format should be specified"
    ), "at least one of device, dtype, memory_format should be specified"
    # 中文说明：根据条件选择执行分支；代码：if isinstance(data, torch.Tensor):
    if isinstance(data, torch.Tensor):
        # 中文说明：根据条件选择执行分支；代码：if (
        if (
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：memory_format == torch.channels_last
            memory_format == torch.channels_last
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：and data.dim() != 4
            and data.dim() != 4
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：or memory_format == torch.channels_last_3d
            or memory_format == torch.channels_last_3d
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：and data.dim() != 5
            and data.dim() != 5
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
        ):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：memory_format = torch.preserve_format # do not change the memory format
            memory_format = torch.preserve_format  # do not change the memory format
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_cpu = (isinstance(device, str) and device == "cpu") or (
        is_cpu = (isinstance(device, str) and device == "cpu") or (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：isinstance(device, torch.device) and device.type == "cpu"
            isinstance(device, torch.device) and device.type == "cpu"
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data = data.to(
        data = data.to(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：device=device,
            device=device,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dtype=dtype,
            dtype=dtype,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：memory_format=memory_format,
            memory_format=memory_format,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：non_blocking=(not is_cpu),
            non_blocking=(not is_cpu),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return data
        return data
    # 中文说明：根据条件选择执行分支；代码：elif isinstance(data, collections.abc.Mapping):
    elif isinstance(data, collections.abc.Mapping):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return type(data)({key: to(data[key], device=device, dtype=dtype, memory_format=memory_format...
        return type(data)({key: to(data[key], device=device, dtype=dtype, memory_format=memory_format) for key in data})
    # 中文说明：根据条件选择执行分支；代码：elif isinstance(data, collections.abc.Sequence) and not isinstance(data, (str, bytes)):
    elif isinstance(data, collections.abc.Sequence) and not isinstance(data, (str, bytes)):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return type(data)([to(elem, device=device, dtype=dtype, memory_format=memory_format) for elem...
        return type(data)([to(elem, device=device, dtype=dtype, memory_format=memory_format) for elem in data])
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return data
        return data


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def serialize(data: Any) -> Any:
def serialize(data: Any) -> Any:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Serialize data by hierarchically traversing through iterables.
    """Serialize data by hierarchically traversing through iterables.

    Args:
        data (Any): Input data.

    Returns:
        data (Any): Serialized data.
    """
    # 中文说明：根据条件选择执行分支；代码：if isinstance(data, collections.abc.Mapping):
    if isinstance(data, collections.abc.Mapping):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return type(data)({key: serialize(data[key]) for key in data})
        return type(data)({key: serialize(data[key]) for key in data})
    # 中文说明：根据条件选择执行分支；代码：elif isinstance(data, collections.abc.Sequence) and not isinstance(data, (str, bytes)):
    elif isinstance(data, collections.abc.Sequence) and not isinstance(data, (str, bytes)):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return type(data)([serialize(elem) for elem in data])
        return type(data)([serialize(elem) for elem in data])
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：json.dumps(data)
            json.dumps(data)
        # 中文说明：处理异常、清理资源或管理上下文；代码：except TypeError:
        except TypeError:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data = str(data)
            data = str(data)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return data
        return data


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def print_environ_variables(env_vars: list[str]) -> None:
def print_environ_variables(env_vars: list[str]) -> None:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Print a specific list of environment variables.
    """Print a specific list of environment variables.

    Args:
        env_vars (list[str]): List of specified environment variables.
    """
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for env_var in env_vars:
    for env_var in env_vars:
        # 中文说明：根据条件选择执行分支；代码：if env_var in os.environ:
        if env_var in os.environ:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Environment variable {Color.green(env_var)}: {Color.yellow(os.environ[env_var])}")
            log.info(f"Environment variable {Color.green(env_var)}: {Color.yellow(os.environ[env_var])}")
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(f"Environment variable {Color.green(env_var)} not set!")
            log.warning(f"Environment variable {Color.green(env_var)} not set!")


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def set_random_seed(seed: int, by_rank: bool = False) -> None:
def set_random_seed(seed: int, by_rank: bool = False) -> None:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Set random seed. This includes random, numpy, Pytorch.
    """Set random seed. This includes random, numpy, Pytorch.

    Args:
        seed (int): Random seed.
        by_rank (bool): if true, each GPU will use a different random seed.
    """
    # 中文说明：根据条件选择执行分支；代码：if by_rank:
    if by_rank:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：seed += distributed.get_rank()
        seed += distributed.get_rank()
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Using random seed {seed}.")
    log.info(f"Using random seed {seed}.")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：random.seed(seed)
    random.seed(seed)
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：np.random.seed(seed)
    np.random.seed(seed)
    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.manual_seed(seed) # sets seed on the current CPU & all GPUs
    torch.manual_seed(seed)  # sets seed on the current CPU & all GPUs


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def arch_invariant_rand(
def arch_invariant_rand(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：shape: List[int] | Tuple[int], dtype: torch.dtype, device: str | torch.device, seed: int | No...
    shape: List[int] | Tuple[int], dtype: torch.dtype, device: str | torch.device, seed: int | None = None
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Produce a GPU-architecture-invariant randomized Torch tensor.
    """Produce a GPU-architecture-invariant randomized Torch tensor.

    Args:
        shape (list or tuple of ints): Output tensor shape.
        dtype (torch.dtype): Output tensor type.
        device (torch.device): Device holding the output.
        seed (int): Optional randomization seed.

    Returns:
        tensor (torch.tensor): Randomly-generated tensor.
    """
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Create a random number generator, optionally seeded
    # Create a random number generator, optionally seeded
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rng = np.random.RandomState(seed)
    rng = np.random.RandomState(seed)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Generate random numbers using the generator
    # Generate random numbers using the generator
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：random_array = rng.standard_normal(shape).astype(np.float32) # Use standard_normal for normal...
    random_array = rng.standard_normal(shape).astype(np.float32)  # Use standard_normal for normal distribution

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Convert to torch tensor and return
    # Convert to torch tensor and return
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return torch.from_numpy(random_array).to(dtype=dtype, device=device)
    return torch.from_numpy(random_array).to(dtype=dtype, device=device)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_data_batch_size(data: dict[str, torch.Tensor] | torch.Tensor) -> int:
def get_data_batch_size(data: dict[str, torch.Tensor] | torch.Tensor) -> int:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Get the batch size from a data batch, a (possibly hierarchical) dictionary of tensors.
    """Get the batch size from a data batch, a (possibly hierarchical) dictionary of tensors.

    Args:
        data (dict[str, torch.Tensor]): Data batch (dictionary of tensors).

    Returns:
        batch_size (int): Data batch size.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _get_batch_size(input_data: Any) -> Union[int, None]:
    def _get_batch_size(input_data: Any) -> Union[int, None]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Helper function that recursively finds a tensor in the input data
        (could be a nested dictionary) and returns its batch size.
        """
        # 中文说明：根据条件选择执行分支；代码：if isinstance(input_data, torch.Tensor):
        if isinstance(input_data, torch.Tensor):
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return len(input_data)
            return len(input_data)
        # 中文说明：根据条件选择执行分支；代码：elif isinstance(input_data, collections.abc.Mapping):
        elif isinstance(input_data, collections.abc.Mapping):
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key, value in input_data.items():
            for key, value in input_data.items():
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch_size = _get_batch_size(value)
                batch_size = _get_batch_size(value)
                # 中文说明：根据条件选择执行分支；代码：if batch_size is not None:
                if batch_size is not None:
                    # 中文说明：从当前函数返回结果或结束函数执行；代码：return batch_size
                    return batch_size
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return None
        return None

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch_size = _get_batch_size(data)
    batch_size = _get_batch_size(data)
    # 中文说明：根据条件选择执行分支；代码：if not isinstance(batch_size, int):
    if not isinstance(batch_size, int):
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Batch size ({batch_size}) obtained from invalid data: {data}")
        raise ValueError(f"Batch size ({batch_size}) obtained from invalid data: {data}")
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return batch_size
    return batch_size


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def parameters_to_buffer(module: torch.nn.Module, persistent: bool = True):
def parameters_to_buffer(module: torch.nn.Module, persistent: bool = True):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Convert parameters in a module to buffers.
    """Convert parameters in a module to buffers.
    Buffers do not have its own gradients and thus not updated by backpropagation.

    Args:
        module (torch.nn.Module): a module to convert parameters
        persistent (bool): If True, buffers are included in state_dict.
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：named_params = dict()
    named_params = dict()

    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for name, param in module.named_parameters():
    for name, param in module.named_parameters():
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：named_params[name] = param
        named_params[name] = param

    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for name, param in named_params.items():
    for name, param in named_params.items():
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：module_hierarchy = name.split(".")
        module_hierarchy = name.split(".")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：submodule_name = ".".join(module_hierarchy[:-1])
        submodule_name = ".".join(module_hierarchy[:-1])
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：submodule = module.get_submodule(submodule_name)
        submodule = module.get_submodule(submodule_name)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：subname = module_hierarchy[-1]
        subname = module_hierarchy[-1]
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：delattr(submodule, subname)
        delattr(submodule, subname)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：submodule.register_buffer(subname, param, persistent=persistent)
        submodule.register_buffer(subname, param, persistent=persistent)

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return
    return


# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：T = TypeVar("T", bound=Callable[..., Any])
T = TypeVar("T", bound=Callable[..., Any])


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class timer(ContextDecorator): # noqa: N801
class timer(ContextDecorator):  # noqa: N801
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Simple timer for timing the execution of code.
    """Simple timer for timing the execution of code.

    It can be used as either a context manager or a function decorator. The timing result will be logged upon exit.

    Example:
        def func_a():
            time.sleep(1)
        with timer("func_a"):
            func_a()

        @timer("func_b)
        def func_b():
            time.sleep(1)
        func_b()
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, context: str, debug: bool = False):
    def __init__(self, context: str, debug: bool = False):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.context = context
        self.context = context
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.debug = debug
        self.debug = debug

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __enter__(self) -> None:
    def __enter__(self) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.tic = time.time()
        self.tic = time.time()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __exit__(self, exc_type, exc_value, traceback) -> None: # noqa: ANN001
    def __exit__(self, exc_type, exc_value, traceback) -> None:  # noqa: ANN001
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：time_spent = time.time() - self.tic
        time_spent = time.time() - self.tic
        # 中文说明：根据条件选择执行分支；代码：if self.debug:
        if self.debug:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(f"Time spent on {self.context}: {time_spent:.4f} seconds")
            log.debug(f"Time spent on {self.context}: {time_spent:.4f} seconds")
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Time spent on {self.context}: {time_spent:.4f} seconds")
            log.info(f"Time spent on {self.context}: {time_spent:.4f} seconds")

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, func: T) -> T:
    def __call__(self, func: T) -> T:
        # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@functools.wraps(func)
        @functools.wraps(func)
        # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def wrapper(*args, **kwargs): # noqa: ANN202
        def wrapper(*args, **kwargs):  # noqa: ANN202
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tic = time.time()
            tic = time.time()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：result = func(*args, **kwargs)
            result = func(*args, **kwargs)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：time_spent = time.time() - tic
            time_spent = time.time() - tic
            # 中文说明：根据条件选择执行分支；代码：if self.debug:
            if self.debug:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(f"Time spent on {self.context}: {time_spent:.4f} seconds")
                log.debug(f"Time spent on {self.context}: {time_spent:.4f} seconds")
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Time spent on {self.context}: {time_spent:.4f} seconds")
                log.info(f"Time spent on {self.context}: {time_spent:.4f} seconds")
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return result
            return result

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return wrapper # type: ignore
        return wrapper  # type: ignore


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class memory_checker(ContextDecorator): # noqa: N801
class memory_checker(ContextDecorator):  # noqa: N801
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Simple memory checker for a given block of code.
    """Simple memory checker for a given block of code.

    It can be used as either a context manager or a function decorator. The memory usage will be logged upon exit.
    Example:
        def func_a():
            torch.rand([int(1024**2)]).float().cuda()
        with memory_checker("func_a"):
            func_a()
        >>> 0.004GB memory used

        @memory_checker("func_b")
        def func_b():
            random_var = torch.rand([int(1024**2)]).cuda()
        func_b()
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, context: str, debug: bool = False):
    def __init__(self, context: str, debug: bool = False):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.context = context
        self.context = context
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.debug = debug
        self.debug = debug

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __enter__(self) -> None:
    def __enter__(self) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.synchronize()
        torch.cuda.synchronize()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.reset_peak_memory_stats()
        torch.cuda.reset_peak_memory_stats()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.initial_memory = torch.cuda.max_memory_allocated()
        self.initial_memory = torch.cuda.max_memory_allocated()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __exit__(self, exc_type, exc_value, traceback) -> None: # noqa: ANN001
    def __exit__(self, exc_type, exc_value, traceback) -> None:  # noqa: ANN001
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.synchronize()
        torch.cuda.synchronize()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：final_memory = torch.cuda.max_memory_allocated()
        final_memory = torch.cuda.max_memory_allocated()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：message = f"Memory used within {self.context}: {(final_memory - self.initial_memory) / 1024**...
        message = f"Memory used within {self.context}: {(final_memory - self.initial_memory) / 1024**3:.4f} GB"
        # 中文说明：根据条件选择执行分支；代码：if self.debug:
        if self.debug:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(message)
            log.debug(message)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(message)
            log.info(message)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, func: T) -> T:
    def __call__(self, func: T) -> T:
        # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@functools.wraps(func)
        @functools.wraps(func)
        # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def wrapper(*args, **kwargs): # noqa: ANN202
        def wrapper(*args, **kwargs):  # noqa: ANN202
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.synchronize()
            torch.cuda.synchronize()
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.reset_peak_memory_stats()
            torch.cuda.reset_peak_memory_stats()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：initial_memory = torch.cuda.max_memory_allocated()
            initial_memory = torch.cuda.max_memory_allocated()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：result = func(*args, **kwargs)
            result = func(*args, **kwargs)
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.synchronize()
            torch.cuda.synchronize()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：final_memory = torch.cuda.max_memory_allocated()
            final_memory = torch.cuda.max_memory_allocated()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：message = f"Memory used within {self.context}: {(final_memory - initial_memory) / 1024**3:.4f...
            message = f"Memory used within {self.context}: {(final_memory - initial_memory) / 1024**3:.4f} GB"
            # 中文说明：根据条件选择执行分支；代码：if self.debug:
            if self.debug:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(message)
                log.debug(message)
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(message)
                log.info(message)
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return result
            return result

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return wrapper # type: ignore
        return wrapper  # type: ignore


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class TrainingTimer:
class TrainingTimer:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Timer for timing the execution of code, aggregating over multiple training iterations.
    """Timer for timing the execution of code, aggregating over multiple training iterations.

    It is used as a context manager to measure the execution time of code and store the timing results
    for each function. The context managers can be nested.

    Attributes:
        results (dict): A dictionary to store timing results for various code.

    Example:
        timer = Timer()
        for i in range(100):
            with timer("func_a"):
                func_a()
        avg_time = sum(timer.results["func_a"]) / len(timer.results["func_a"])
        print(f"func_a() took {avg_time} seconds.")
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self) -> None:
    def __init__(self) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.results = dict()
        self.results = dict()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.average_results = dict()
        self.average_results = dict()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.start_time = []
        self.start_time = []
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.func_stack = []
        self.func_stack = []
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.reset()
        self.reset()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def reset(self) -> None:
    def reset(self) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.results = {key: [] for key in self.results}
        self.results = {key: [] for key in self.results}

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __enter__(self) -> TrainingTimer:
    def __enter__(self) -> TrainingTimer:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.start_time.append(time.time())
        self.start_time.append(time.time())
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self
        return self

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __exit__(self, exc_type, exc_value, traceback) -> None: # noqa: ANN001
    def __exit__(self, exc_type, exc_value, traceback) -> None:  # noqa: ANN001
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：end_time = time.time()
        end_time = time.time()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：result = end_time - self.start_time.pop()
        result = end_time - self.start_time.pop()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：key = self.func_stack.pop()
        key = self.func_stack.pop()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.results.setdefault(key, [])
        self.results.setdefault(key, [])
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.results[key].append(result)
        self.results[key].append(result)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, func_name: str) -> TrainingTimer:
    def __call__(self, func_name: str) -> TrainingTimer:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.func_stack.append(func_name)
        self.func_stack.append(func_name)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self
        return self

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __getattr__(self, func_name: str) -> TrainingTimer:
    def __getattr__(self, func_name: str) -> TrainingTimer:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.__call__(func_name)
        return self.__call__(func_name)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def nested(self, func_name: str) -> TrainingTimer:
    def nested(self, func_name: str) -> TrainingTimer:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.__call__(func_name)
        return self.__call__(func_name)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def compute_average_results(self) -> dict[str, float]:
    def compute_average_results(self) -> dict[str, float]:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：results = dict()
        results = dict()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key, value_list in self.results.items():
        for key, value_list in self.results.items():
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：results[key] = sum(value_list) / len(value_list)
            results[key] = sum(value_list) / len(value_list)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return results
        return results


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def timeout_handler(timeout_period: float, signum: int, frame: int) -> None:
def timeout_handler(timeout_period: float, signum: int, frame: int) -> None:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# What to do when the process gets stuck. For now, we simply end the process.
    # What to do when the process gets stuck. For now, we simply end the process.
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：error_message = f"Timeout error: more than {timeout_period} seconds passed since the last ite...
    error_message = f"Timeout error: more than {timeout_period} seconds passed since the last iteration."
    # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TimeoutError(error_message)
    raise TimeoutError(error_message)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Color:
class Color:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""A convenience class to colorize strings in the console.
    """A convenience class to colorize strings in the console.

    Example:
        import
        print("This is {Color.red('important')}.")
    """

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def red(x: str) -> str:
    def red(x: str) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return termcolor.colored(str(x), color="red")
        return termcolor.colored(str(x), color="red")

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def green(x: str) -> str:
    def green(x: str) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return termcolor.colored(str(x), color="green")
        return termcolor.colored(str(x), color="green")

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def blue(x: str) -> str:
    def blue(x: str) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return termcolor.colored(str(x), color="blue")
        return termcolor.colored(str(x), color="blue")

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def cyan(x: str) -> str:
    def cyan(x: str) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return termcolor.colored(str(x), color="cyan")
        return termcolor.colored(str(x), color="cyan")

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def yellow(x: str) -> str:
    def yellow(x: str) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return termcolor.colored(str(x), color="yellow")
        return termcolor.colored(str(x), color="yellow")

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def magenta(x: str) -> str:
    def magenta(x: str) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return termcolor.colored(str(x), color="magenta")
        return termcolor.colored(str(x), color="magenta")

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def grey(x: str) -> str:
    def grey(x: str) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return termcolor.colored(str(x), color="grey")
        return termcolor.colored(str(x), color="grey")


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class BufferCnt:
class BufferCnt:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Buffer counter which keeps track of the condition when called and returns True when the condition in met "thres"
    amount of times, otherwise returns False.

    Example usage:
        buf = BufferCnt(thres=3)
        for _ in range(5):
            if buf(random.random() > 0.5):
                print("We got lucky 3 times out of 5.")

    Args:
        thres (int): The amount of times the expression needs to be True before returning True.
        reset_over_thres (bool): Whether to reset the buffer after returning True.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, thres=10, reset_over_thres=False):
    def __init__(self, thres=10, reset_over_thres=False):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._cnt = 0
        self._cnt = 0
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.thres = thres
        self.thres = thres
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.reset_over_thres = reset_over_thres
        self.reset_over_thres = reset_over_thres

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, expre, thres=None):
    def __call__(self, expre, thres=None):
        # 中文说明：根据条件选择执行分支；代码：if expre is True:
        if expre is True:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._cnt += 1
            self._cnt += 1
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._cnt = 0
            self._cnt = 0

        # 中文说明：根据条件选择执行分支；代码：if thres is None:
        if thres is None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：thres = self.thres
            thres = self.thres

        # 中文说明：根据条件选择执行分支；代码：if self._cnt >= thres:
        if self._cnt >= thres:
            # 中文说明：根据条件选择执行分支；代码：if self.reset_over_thres:
            if self.reset_over_thres:
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.reset()
                self.reset()
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return True
            return True

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return False
        return False

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def cnt(self):
    def cnt(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self._cnt
        return self._cnt

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def reset(self):
    def reset(self):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._cnt = 0
        self._cnt = 0


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def dataclass_instance_to_dict(dataclass: Any) -> dict:
def dataclass_instance_to_dict(dataclass: Any) -> dict:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Convert a dataclass to a dictionary.
    """Convert a dataclass to a dictionary.

    Args:
        dataclass (Any): Dataclass object.

    Returns:
        dict: Dictionary representation of the dataclass.
    """
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return {f.name: getattr(dataclass, f.name) for f in fields(dataclass)}
    return {f.name: getattr(dataclass, f.name) for f in fields(dataclass)}


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_local_tensor_if_DTensor(tensor: torch.Tensor | DTensor) -> torch.tensor:
def get_local_tensor_if_DTensor(tensor: torch.Tensor | DTensor) -> torch.tensor:
    # 中文说明：根据条件选择执行分支；代码：if isinstance(tensor, DTensor):
    if isinstance(tensor, DTensor):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：local = tensor.to_local()
        local = tensor.to_local()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# As per PyTorch documentation, if the communication is not finished yet, we need to wait for...
        # As per PyTorch documentation, if the communication is not finished yet, we need to wait for it to finish
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# https://pytorch.org/docs/stable/distributed.tensor.html#torch.distributed.tensor.DTensor.to...
        # https://pytorch.org/docs/stable/distributed.tensor.html#torch.distributed.tensor.DTensor.to_local
        # 中文说明：根据条件选择执行分支；代码：if isinstance(local, AsyncCollectiveTensor):
        if isinstance(local, AsyncCollectiveTensor):
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return local.wait()
            return local.wait()
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return local
            return local
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return tensor
    return tensor


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class NVTXRangeContext:
class NVTXRangeContext:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Context manager which inserts NVTX range around the current context and optionally calls torch.cuda.synchronize
    at the start and the end of the context.

    Args:
        name (str): Name of the NVTX range.
        enabled (bool): Whether the context manager is enabled. When disabled, it does nothing. Default: True.
        synchronize (bool): Whether to call torch.cuda.synchronize() at the start and the end of the context. Default: True.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, name: str, enabled: bool = True, synchronize: bool = True):
    def __init__(self, name: str, enabled: bool = True, synchronize: bool = True):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.name = name
        self.name = name
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.enabled = enabled
        self.enabled = enabled
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.synchronize = synchronize
        self.synchronize = synchronize

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __enter__(self):
    def __enter__(self):
        # 中文说明：根据条件选择执行分支；代码：if not self.enabled:
        if not self.enabled:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return
            return
        # 中文说明：根据条件选择执行分支；代码：if self.synchronize:
        if self.synchronize:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.synchronize()
            torch.cuda.synchronize()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.nvtx.range_push(self.name)
        torch.cuda.nvtx.range_push(self.name)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __exit__(self, exc_type, exc_val, exc_tb):
    def __exit__(self, exc_type, exc_val, exc_tb):
        # 中文说明：根据条件选择执行分支；代码：if not self.enabled:
        if not self.enabled:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return
            return
        # 中文说明：根据条件选择执行分支；代码：if self.synchronize:
        if self.synchronize:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.synchronize()
            torch.cuda.synchronize()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.nvtx.range_pop()
        torch.cuda.nvtx.range_pop()
