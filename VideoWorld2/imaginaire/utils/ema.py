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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import TYPE_CHECKING, Any, Generator, List, Optional, Union
from typing import TYPE_CHECKING, Any, Generator, List, Optional, Union

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch

# 中文说明：开始一个可捕获异常的代码块；代码：try:
try:
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from megatron.core import parallel_state
    from megatron.core import parallel_state

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：USE_MEGATRON = True
    USE_MEGATRON = True
# 中文说明：处理异常、清理资源或管理上下文；代码：except ImportError:
except ImportError:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：USE_MEGATRON = False
    USE_MEGATRON = False

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import distributed, log
from imaginaire.utils import distributed, log

# 中文说明：根据条件选择执行分支；代码：if TYPE_CHECKING:
if TYPE_CHECKING:
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.model import ImaginaireModel
    from imaginaire.model import ImaginaireModel


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class FastEmaModelUpdater:
class FastEmaModelUpdater:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    This class is used to update target model~(EMA) given source model~(regular model) and beta.
    The method interaface mimic :class:`EMAModelTracker` and :class:`PowerEMATracker`.
    Different from two classes, this class does not maintain the EMA model weights as buffers. It expects the user to have two module with same architecture and weights shape.
    The class is proposed to work with FSDP model where above two classes are not working as expected. Besides, it is strange to claim model weights as buffers and do unnecessary name changing in :class:`EMAModelTracker` and :class:`PowerEMATracker`. Moeving forward, we should use this class instead of above two classes.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self):
    def __init__(self):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Flag to indicate whether the cache is taken or not. Useful to avoid cache overwrite
        # Flag to indicate whether the cache is taken or not. Useful to avoid cache overwrite
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.is_cached = False
        self.is_cached = False

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.no_grad()
    @torch.no_grad()
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def copy_to(self, src_model: torch.nn.Module, tgt_model: torch.nn.Module) -> None:
    def copy_to(self, src_model: torch.nn.Module, tgt_model: torch.nn.Module) -> None:
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for tgt_params, src_params in zip(tgt_model.parameters(), src_model.parameters()):
        for tgt_params, src_params in zip(tgt_model.parameters(), src_model.parameters()):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：tgt_params.data.copy_(src_params.data)
            tgt_params.data.copy_(src_params.data)

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.no_grad()
    @torch.no_grad()
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def update_average(self, src_model: torch.nn.Module, tgt_model: torch.nn.Module, beta: float ...
    def update_average(self, src_model: torch.nn.Module, tgt_model: torch.nn.Module, beta: float = 0.9999) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：target_list = []
        target_list = []
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：source_list = []
        source_list = []
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for tgt_params, src_params in zip(tgt_model.parameters(), src_model.parameters()):
        for tgt_params, src_params in zip(tgt_model.parameters(), src_model.parameters()):
            # 中文说明：检查运行时假设是否成立；代码：assert (
            assert (
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tgt_params.dtype == torch.float32
                tgt_params.dtype == torch.float32
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"EMA model only works in FP32 dtype, got {tgt_params.dtype} instead."
            ), f"EMA model only works in FP32 dtype, got {tgt_params.dtype} instead."
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：target_list.append(tgt_params)
            target_list.append(tgt_params)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：source_list.append(src_params.data)
            source_list.append(src_params.data)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch._foreach_mul_(target_list, beta)
        torch._foreach_mul_(target_list, beta)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch._foreach_add_(target_list, source_list, alpha=1.0 - beta)
        torch._foreach_add_(target_list, source_list, alpha=1.0 - beta)

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.no_grad()
    @torch.no_grad()
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def cache(self, parameters: Any, is_cpu: bool = False) -> None:
    def cache(self, parameters: Any, is_cpu: bool = False) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Save the current parameters for restoring later.
        """Save the current parameters for restoring later.

        Args:
            parameters (iterable): Iterable of torch.nn.Parameter to be temporarily stored.
        """
        # 中文说明：检查运行时假设是否成立；代码：assert self.is_cached is False, "EMA cache is already taken. Did you forget to restore it?"
        assert self.is_cached is False, "EMA cache is already taken. Did you forget to restore it?"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：device = "cpu" if is_cpu else "cuda"
        device = "cpu" if is_cpu else "cuda"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.collected_params = [param.clone().to(device) for param in parameters]
        self.collected_params = [param.clone().to(device) for param in parameters]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.is_cached = True
        self.is_cached = True

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.no_grad()
    @torch.no_grad()
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def restore(self, parameters: Any) -> None:
    def restore(self, parameters: Any) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Restore the parameters in self.collected_params.
        """Restore the parameters in self.collected_params.

        Useful to validate the model with EMA parameters without affecting the
        original optimization process. Store the parameters before copy_to().
        After validation (or model saving), use this to restore the former parameters.

        Args:
            parameters (iterable): Iterable of torch.nn.Parameter to be updated with the stored parameters.
        """
        # 中文说明：检查运行时假设是否成立；代码：assert self.is_cached, "EMA cache is not taken yet."
        assert self.is_cached, "EMA cache is not taken yet."
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for c_param, param in zip(self.collected_params, parameters, strict=False):
        for c_param, param in zip(self.collected_params, parameters, strict=False):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：param.data.copy_(c_param.data.type_as(param.data))
            param.data.copy_(c_param.data.type_as(param.data))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.collected_params = []
        self.collected_params = []
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Release the cache after we call restore
        # Release the cache after we call restore
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.is_cached = False
        self.is_cached = False


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_buffer_name(param_name: str, torch_compile_buffer_renaming: bool = False) -> str:
def get_buffer_name(param_name: str, torch_compile_buffer_renaming: bool = False) -> str:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    This function creates buffer name used by EMA from parameter's name

    Args:
        param_name (str): Model's parameter name
    Returns:
        buffer_name (str): buffer name to be used for given parameter name
    """

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：buffer_name = param_name.replace(".", "-")
    buffer_name = param_name.replace(".", "-")

    # 中文说明：根据条件选择执行分支；代码：if torch_compile_buffer_renaming:
    if torch_compile_buffer_renaming:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# torch.compile() adds _orig_mod to state dict names, this way we get original name
        # torch.compile() adds _orig_mod to state dict names, this way we get original name
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：buffer_name = buffer_name.replace("_orig_mod-", "")
        buffer_name = buffer_name.replace("_orig_mod-", "")

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return buffer_name
    return buffer_name


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class EMAModelTracker(torch.nn.Module):
class EMAModelTracker(torch.nn.Module):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""This is a class to track the EMA model weights.
    """This is a class to track the EMA model weights.

    The EMA weights are registered as buffers, which are extractable as state dicts. The names follow those of the
    regular weights, except all "." are replaced with "-" (limitation of register_buffer()). This is similar to SDXL's
    implementation of EMA. There are no optimizable parameters.

    Attributes:
        collected_params (list): temporarily stores the regular weights while in EMA mode.
        beta (float): EMA decay rate. (default: 0.9999).
        torch_compile_buffer_renaming (bool): whether to remove '_orig_mod-' from buffer names when torch.compile is used
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, model: ImaginaireModel, beta: float = 0.9999, torch_compile_buffer_renamin...
    def __init__(self, model: ImaginaireModel, beta: float = 0.9999, torch_compile_buffer_renaming: bool = False):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Constructor of the EMA model weight tracker.
        """Constructor of the EMA model weight tracker.

        Args:
            model (ImaginaireModel): The PyTorch model.
            beta (float): EMA decay rate. (default: 0.9999).
        """
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.torch_compile_buffer_renaming: bool = torch_compile_buffer_renaming
        self.torch_compile_buffer_renaming: bool = torch_compile_buffer_renaming
        # 中文说明：根据条件选择执行分支；代码：if not 0.0 <= beta <= 1.0:
        if not 0.0 <= beta <= 1.0:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError("Decay must be between 0 and 1")
            raise ValueError("Decay must be between 0 and 1")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.beta = beta
        self.beta = beta
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for name, param in model.named_parameters():
        for name, param in model.named_parameters():
            # 中文说明：根据条件选择执行分支；代码：if param.requires_grad:
            if param.requires_grad:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：buffer_name = get_buffer_name(name, self.torch_compile_buffer_renaming)
                buffer_name = get_buffer_name(name, self.torch_compile_buffer_renaming)
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.register_buffer(buffer_name, param.clone().detach().data)
                self.register_buffer(buffer_name, param.clone().detach().data)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.collected_params = []
        self.collected_params = []
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Flag to indicate whether the cache is taken or not. Useful to avoid cache overwrite
        # Flag to indicate whether the cache is taken or not. Useful to avoid cache overwrite
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.is_cached = False
        self.is_cached = False

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.no_grad()
    @torch.no_grad()
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def update_average(self, model: ImaginaireModel, iteration: Optional[int] = None) -> None:
    def update_average(self, model: ImaginaireModel, iteration: Optional[int] = None) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del iteration
        del iteration
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：target_list = []
        target_list = []
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：source_list = []
        source_list = []
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ema_buffers = self.state_dict()
        ema_buffers = self.state_dict()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for name, param in model.named_parameters():
        for name, param in model.named_parameters():
            # 中文说明：根据条件选择执行分支；代码：if param.requires_grad:
            if param.requires_grad:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：buffer_name = get_buffer_name(name, self.torch_compile_buffer_renaming)
                buffer_name = get_buffer_name(name, self.torch_compile_buffer_renaming)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：buffer = ema_buffers[buffer_name]
                buffer = ema_buffers[buffer_name]
                # 中文说明：检查运行时假设是否成立；代码：assert buffer.dtype == torch.float32, f"EMA model only works in FP32 dtype, got {buffer.dtype...
                assert buffer.dtype == torch.float32, f"EMA model only works in FP32 dtype, got {buffer.dtype} instead."
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：target_list.append(buffer)
                target_list.append(buffer)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：source_list.append(param.data)
                source_list.append(param.data)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch._foreach_mul_(target_list, self.beta)
        torch._foreach_mul_(target_list, self.beta)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch._foreach_add_(target_list, source_list, alpha=1.0 - self.beta)
        torch._foreach_add_(target_list, source_list, alpha=1.0 - self.beta)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def copy_to(self, model: ImaginaireModel) -> None:
    def copy_to(self, model: ImaginaireModel) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ema_buffers = self.state_dict()
        ema_buffers = self.state_dict()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for name, param in model.named_parameters():
        for name, param in model.named_parameters():
            # 中文说明：根据条件选择执行分支；代码：if param.requires_grad:
            if param.requires_grad:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：buffer_name = get_buffer_name(name, self.torch_compile_buffer_renaming)
                buffer_name = get_buffer_name(name, self.torch_compile_buffer_renaming)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：buffer = ema_buffers[buffer_name]
                buffer = ema_buffers[buffer_name]
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：param.data.copy_(buffer.data)
                param.data.copy_(buffer.data)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def cache(self, parameters: Any, is_cpu: bool = False) -> None:
    def cache(self, parameters: Any, is_cpu: bool = False) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Save the current parameters for restoring later.
        """Save the current parameters for restoring later.

        Args:
            parameters (iterable): Iterable of torch.nn.Parameter to be temporarily stored.
        """
        # 中文说明：检查运行时假设是否成立；代码：assert self.is_cached is False, "EMA cache is already taken. Did you forget to restore it?"
        assert self.is_cached is False, "EMA cache is already taken. Did you forget to restore it?"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：device = "cpu" if is_cpu else "cuda"
        device = "cpu" if is_cpu else "cuda"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.collected_params = [param.clone().to(device) for param in parameters]
        self.collected_params = [param.clone().to(device) for param in parameters]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.is_cached = True
        self.is_cached = True

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def restore(self, parameters: Any) -> None:
    def restore(self, parameters: Any) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Restore the parameters in self.collected_params.
        """Restore the parameters in self.collected_params.

        Useful to validate the model with EMA parameters without affecting the
        original optimization process. Store the parameters before copy_to().
        After validation (or model saving), use this to restore the former parameters.

        Args:
            parameters (iterable): Iterable of torch.nn.Parameter to be updated with the stored parameters.
        """
        # 中文说明：检查运行时假设是否成立；代码：assert self.is_cached, "EMA cache is not taken yet."
        assert self.is_cached, "EMA cache is not taken yet."
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for c_param, param in zip(self.collected_params, parameters, strict=False):
        for c_param, param in zip(self.collected_params, parameters, strict=False):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：param.data.copy_(c_param.data.type_as(param.data))
            param.data.copy_(c_param.data.type_as(param.data))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.collected_params = []
        self.collected_params = []
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Release the cache after we call restore
        # Release the cache after we call restore
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.is_cached = False
        self.is_cached = False

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@classmethod
    @classmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def initialize_multi_rank_ema(
    def initialize_multi_rank_ema(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cls, model: torch.nn.Module, rate: Union[float, List[float]], num: int = 1, enabled: bool = True
        cls, model: torch.nn.Module, rate: Union[float, List[float]], num: int = 1, enabled: bool = True
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Optional[EMAModelTracker]:
    ) -> Optional[EMAModelTracker]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Class method to initialize per rank EMA Model Tracker with different rate.
        Each rank will have a different rate based on the given configuration, resulting in different EMA weights.

        Args:
            model (torch.nn.Module): The neural network model to be tracked.
            rate (Union[float, List[float]]): The decay rate(s) for the EMA. If a list is provided,
                                              it corresponds to rates for different ranks.
            num (int, optional): The number of leading ranks to consider for different rates.
                                 Defaults to 1.
            enabled (bool, optional): Flag to enable or disable the creation of the tracker.
                                      If False, returns None. Defaults to True.

        Returns:
            Optional[EMAModelTracker]: An instance of EMAModelTracker if enabled, otherwise None.

        Example:
            >>> model = torch.nn.Linear(10, 2)
            >>> tracker = EMAModelTracker.initialize_ema_from_settings(model, rate=[0.1, 0.2], num=2)
            >>> print(tracker)

        Notes:
            If `rate` is a list and the current rank is less than `num`, the rate for the current rank
            is used. If the current rank exceeds `num`, the first rate in the list is used by default.
        """
        # 中文说明：根据条件选择执行分支；代码：if not enabled:
        if not enabled:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return None
            return None
        # 中文说明：根据条件选择执行分支；代码：if USE_MEGATRON and parallel_state.is_initialized():
        if USE_MEGATRON and parallel_state.is_initialized():
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cur_dp_rank = parallel_state.get_data_parallel_rank(with_context_parallel=True)
            cur_dp_rank = parallel_state.get_data_parallel_rank(with_context_parallel=True)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.critical(f"using MCore parallel_state for EMA initialization. DP RANK: {cur_dp_rank}", ra...
            log.critical(f"using MCore parallel_state for EMA initialization. DP RANK: {cur_dp_rank}", rank0_only=False)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning("It should not used together with FSDP!")
            log.warning("It should not used together with FSDP!")
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cur_dp_rank = distributed.get_rank()
            cur_dp_rank = distributed.get_rank()
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.critical(f"using torch.distributed for EMA initialization. DP RANK: {cur_dp_rank}", rank0...
            log.critical(f"using torch.distributed for EMA initialization. DP RANK: {cur_dp_rank}", rank0_only=False)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rate = rate if isinstance(rate, list) else [rate]
        rate = rate if isinstance(rate, list) else [rate]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num = min(num, len(rate))
        num = min(num, len(rate))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rate = rate[cur_dp_rank] if cur_dp_rank < num else rate[0]
        rate = rate[cur_dp_rank] if cur_dp_rank < num else rate[0]
        # 中文说明：根据条件选择执行分支；代码：if cur_dp_rank < num:
        if cur_dp_rank < num:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"EMAModelTracker: rank {cur_dp_rank}, rate {rate}")
            print(f"EMAModelTracker: rank {cur_dp_rank}, rate {rate}")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return cls(model, rate)
        return cls(model, rate)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class PowerEMATracker(EMAModelTracker):
class PowerEMATracker(EMAModelTracker):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, model: ImaginaireModel, s: float = 0.1, torch_compile_buffer_renaming: boo...
    def __init__(self, model: ImaginaireModel, s: float = 0.1, torch_compile_buffer_renaming: bool = False):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Constructor of the EMA model weight tracker.
        """Constructor of the EMA model weight tracker.

        Args:
            model (ImaginaireModel): The PyTorch model.
            s (float): EMA decay rate. See EDM2 paper
            torch_compile_buffer_renaming (bool): whether to remove '_orig_mod-' from buffer names when torch.compile is used
        """
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(model=model, beta=0.0, torch_compile_buffer_renaming=torch_compile_buffer_re...
        super().__init__(model=model, beta=0.0, torch_compile_buffer_renaming=torch_compile_buffer_renaming)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.exp = np.roots([1, 7, 16 - s**-2, 12 - s**-2]).real.max()
        self.exp = np.roots([1, 7, 16 - s**-2, 12 - s**-2]).real.max()

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.no_grad()
    @torch.no_grad()
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def update_average(self, model: ImaginaireModel, iteration: Optional[int] = None) -> None:
    def update_average(self, model: ImaginaireModel, iteration: Optional[int] = None) -> None:
        # 中文说明：根据条件选择执行分支；代码：if iteration == 0:
        if iteration == 0:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：beta = 0.0
            beta = 0.0
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：i = iteration + 1
            i = iteration + 1
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：beta = (1 - 1 / i) ** (self.exp + 1)
            beta = (1 - 1 / i) ** (self.exp + 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.beta = beta
        self.beta = beta

        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().update_average(model, iteration)
        super().update_average(model, iteration)

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@classmethod
    @classmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def initialize_multi_rank_ema(
    def initialize_multi_rank_ema(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cls, model: torch.nn.Module, rate: float, num: int, enabled: bool = True
        cls, model: torch.nn.Module, rate: float, num: int, enabled: bool = True
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Optional[PowerEMATracker]:
    ) -> Optional[PowerEMATracker]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Class method to initialize per rank EMA Model Tracker with different rate.
        Each rank will have a different rate based on the given configuration, resulting in different EMA weights.

        Args:
            model (torch.nn.Module): The neural network model for which the EMA tracker is being set up.
            num (int): The number of ranks for which the rate adjustment is applied. Beyond this, the rate remains unchanged.
            rate (float): The base decay rate for the EMA calculation.
            enabled (bool, optional): Flag to enable or disable the initialization of the tracker. If False, returns None.
                                      Defaults to True.

        Returns:
            Optional[PowerEMATracker]: An instance of PowerEMATracker with adjusted rate if enabled, otherwise None.

        Raises:
            None

        Example:
            >>> model = torch.nn.Linear(10, 2)
            >>> tracker = PowerEMATracker.initialize_multi_rank_ema(model, num=3, rate=0.99)
            >>> print(tracker)

        Notes:
            The decay rate is modified by dividing it by 2 raised to the power of the rank for each rank less than `num`.
            If the rank is greater than or equal to `num`, the base rate is used without modification. This approach
            allows higher ranked processes to have a less aggressive decay, potentially reflecting their delayed synchronization
            in a distributed training scenario.
        """
        # 中文说明：根据条件选择执行分支；代码：if not enabled:
        if not enabled:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return None
            return None
        # 中文说明：根据条件选择执行分支；代码：if USE_MEGATRON and parallel_state.is_initialized():
        if USE_MEGATRON and parallel_state.is_initialized():
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cur_dp_rank = parallel_state.get_data_parallel_rank(with_context_parallel=True)
            cur_dp_rank = parallel_state.get_data_parallel_rank(with_context_parallel=True)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.critical(f"using MCore parallel_state for EMA initialization. DP RANK: {cur_dp_rank}", ra...
            log.critical(f"using MCore parallel_state for EMA initialization. DP RANK: {cur_dp_rank}", rank0_only=False)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning("It should not used together with FSDP!")
            log.warning("It should not used together with FSDP!")
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cur_dp_rank = distributed.get_rank()
            cur_dp_rank = distributed.get_rank()
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.critical(f"using torch.distributed for EMA initialization. DP RANK: {cur_dp_rank}", rank0...
            log.critical(f"using torch.distributed for EMA initialization. DP RANK: {cur_dp_rank}", rank0_only=False)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：divider = 2**cur_dp_rank if cur_dp_rank < num else 1
        divider = 2**cur_dp_rank if cur_dp_rank < num else 1
        # 中文说明：根据条件选择执行分支；代码：if cur_dp_rank < num:
        if cur_dp_rank < num:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"PowerEMATracker: rank {cur_dp_rank}, rate {rate / divider}")
            print(f"PowerEMATracker: rank {cur_dp_rank}, rate {rate / divider}")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return cls(model, rate / divider)
        return cls(model, rate / divider)


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@contextmanager
@contextmanager
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def ema_scope(model: ImaginaireModel, enabled: bool = False) -> Generator[None, None, None]:
def ema_scope(model: ImaginaireModel, enabled: bool = False) -> Generator[None, None, None]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Context manager for switching between regular and EMA model weights.
    """Context manager for switching between regular and EMA model weights.

    Args:
        model (ImaginaireModel): The PyTorch model.
        enabled (bool): Whether switching to EMA weights is enabled (default: False).
    """
    # 中文说明：根据条件选择执行分支；代码：if enabled:
    if enabled:
        # 中文说明：检查运行时假设是否成立；代码：assert hasattr(model, "ema") and isinstance(model.ema, (FastEmaModelUpdater, EMAModelTracker,...
        assert hasattr(model, "ema") and isinstance(model.ema, (FastEmaModelUpdater, EMAModelTracker, PowerEMATracker))
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model.ema.cache(model.parameters())
        model.ema.cache(model.parameters())
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model.ema.copy_to(model)
        model.ema.copy_to(model)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("EMA: switched to EMA weights.")
        log.info("EMA: switched to EMA weights.")
    # 中文说明：开始一个可捕获异常的代码块；代码：try:
    try:
        # 中文说明：从生成器逐步产生本行指定的值；代码：yield None
        yield None
    # 中文说明：处理异常、清理资源或管理上下文；代码：finally:
    finally:
        # 中文说明：根据条件选择执行分支；代码：if enabled:
        if enabled:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model.ema.restore(model.parameters())
            model.ema.restore(model.parameters())
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("EMA: restored regular weights.")
            log.info("EMA: restored regular weights.")
