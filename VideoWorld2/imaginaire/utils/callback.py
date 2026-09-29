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

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import time
import time
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import warnings
import warnings
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import TYPE_CHECKING, Any, Callable, Optional
from typing import TYPE_CHECKING, Any, Callable, Optional

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import omegaconf
import omegaconf
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.distributed as dist
import torch.distributed as dist
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.utils.data
import torch.utils.data
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import tqdm
import tqdm

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import instantiate
from imaginaire.lazy_config import instantiate
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import distributed, log
from imaginaire.utils import distributed, log
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.misc import get_local_tensor_if_DTensor
from imaginaire.utils.misc import get_local_tensor_if_DTensor

# 中文说明：开始一个可捕获异常的代码块；代码：try:
try:
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from megatron.core import parallel_state
    from megatron.core import parallel_state
# 中文说明：处理异常、清理资源或管理上下文；代码：except ImportError:
except ImportError:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：parallel_state = None
    parallel_state = None
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print("Megatron-core is not installed.")
    print("Megatron-core is not installed.")


# 中文说明：根据条件选择执行分支；代码：if TYPE_CHECKING:
if TYPE_CHECKING:
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.config import Config
    from imaginaire.config import Config
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.model import ImaginaireModel
    from imaginaire.model import ImaginaireModel
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.trainer import ImaginaireTrainer
    from imaginaire.trainer import ImaginaireTrainer


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class CallBackGroup:
class CallBackGroup:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""A class for hosting a collection of callback objects.
    """A class for hosting a collection of callback objects.

    It is used to execute callback functions of multiple callback objects with the same method name.
    When callbackgroup.func(args) is executed, internally it loops through the objects in self._callbacks and runs
    self._callbacks[0].func(args), self._callbacks[1].func(args), etc. The method name and arguments should match.

    Attributes:
        _callbacks (list[Callback]): List of callback objects.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, config: Config, trainer: ImaginaireTrainer) -> None:
    def __init__(self, config: Config, trainer: ImaginaireTrainer) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Initializes the list of callback objects.
        """Initializes the list of callback objects.

        Args:
            config (Config): The config object for the Imaginaire codebase.
            trainer (ImaginaireTrainer): The main trainer.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._callbacks = []
        self._callbacks = []
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：callback_configs = config.trainer.callbacks
        callback_configs = config.trainer.callbacks
        # 中文说明：根据条件选择执行分支；代码：if callback_configs:
        if callback_configs:
            # 中文说明：根据条件选择执行分支；代码：if isinstance(callback_configs, list) or isinstance(callback_configs, omegaconf.listconfig.Li...
            if isinstance(callback_configs, list) or isinstance(callback_configs, omegaconf.listconfig.ListConfig):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：warnings.warn(
                warnings.warn(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："The 'config.trainer.callbacks' parameter should be a dict instead of a list. "
                    "The 'config.trainer.callbacks' parameter should be a dict instead of a list. "
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："Please update your code",
                    "Please update your code",
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：DeprecationWarning,
                    DeprecationWarning,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stacklevel=2,
                    stacklevel=2,
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：callback_configs = {f"callback_{i}": v for i, v in enumerate(callback_configs)}
                callback_configs = {f"callback_{i}": v for i, v in enumerate(callback_configs)}
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for callback_name, current_callback_cfg in callback_configs.items():
            for callback_name, current_callback_cfg in callback_configs.items():
                # 中文说明：根据条件选择执行分支；代码：if "_target_" not in current_callback_cfg:
                if "_target_" not in current_callback_cfg:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.critical(
                    log.critical(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Callback {callback_name} is missing the '_target_' field. \n SKip {current_callback_cfg}"
                        f"Callback {callback_name} is missing the '_target_' field. \n SKip {current_callback_cfg}"
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                    # 中文说明：执行循环控制或空操作；代码：continue
                    continue
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.critical(f"Instantiating callback {callback_name}: {current_callback_cfg}")
                log.critical(f"Instantiating callback {callback_name}: {current_callback_cfg}")
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_callback = instantiate(current_callback_cfg)
                _callback = instantiate(current_callback_cfg)
                # 中文说明：检查运行时假设是否成立；代码：assert isinstance(_callback, Callback), f"{current_callback_cfg} is not a valid callback."
                assert isinstance(_callback, Callback), f"{current_callback_cfg} is not a valid callback."
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_callback.config = config
                _callback.config = config
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_callback.trainer = trainer
                _callback.trainer = trainer
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._callbacks.append(_callback)
                self._callbacks.append(_callback)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __getattr__(self, method_name: str) -> Callable:
    def __getattr__(self, method_name: str) -> Callable:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Loops through the callback objects to call the corresponding callback function.
        """Loops through the callback objects to call the corresponding callback function.

        Args:
            method_name (str): Callback method name.
        """

        # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def multi_callback_wrapper(*args, **kwargs) -> None:
        def multi_callback_wrapper(*args, **kwargs) -> None:
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for callback in self._callbacks:
            for callback in self._callbacks:
                # 中文说明：检查运行时假设是否成立；代码：assert hasattr(callback, method_name)
                assert hasattr(callback, method_name)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：method = getattr(callback, method_name)
                method = getattr(callback, method_name)
                # 中文说明：检查运行时假设是否成立；代码：assert callable(method)
                assert callable(method)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_ = method(*args, **kwargs)
                _ = method(*args, **kwargs)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return multi_callback_wrapper
        return multi_callback_wrapper


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Callback:
class Callback:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""The base class for all callbacks.
    """The base class for all callbacks.

    All callbacks should inherit from this class and adhere to the established method names and signatures.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, config: Optional["Config"] = None, trainer: Optional["ImaginaireTrainer"] ...
    def __init__(self, config: Optional["Config"] = None, trainer: Optional["ImaginaireTrainer"] = None):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Initializes a Callback object.
        """Initializes a Callback object.

        Args:
            config (Optional[Config]): The configuration object for the Imaginaire codebase, if available.
            trainer (Optional[ImaginaireTrainer]): The main trainer handling the training loop, if available.

        Notes:
            The config and trainer parameters are optional to maintain backward compatibility.
            In future releases, these parameters will be removed. Upon using these parameters, a deprecation
            warning will be issued.

        """
        # 中文说明：根据条件选择执行分支；代码：if config is not None or trainer is not None:
        if config is not None or trainer is not None:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：warnings.warn(
            warnings.warn(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："The 'config' and 'trainer' parameters are deprecated and will be removed in a future release. "
                "The 'config' and 'trainer' parameters are deprecated and will be removed in a future release. "
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："Please update your code to create Callback instances without these parameters.",
                "Please update your code to create Callback instances without these parameters.",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：DeprecationWarning,
                DeprecationWarning,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stacklevel=2,
                stacklevel=2,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del config, trainer
        del config, trainer

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_train_start(self, model: ImaginaireModel, iteration: int = 0) -> None:
    def on_train_start(self, model: ImaginaireModel, iteration: int = 0) -> None:
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_training_step_start(self, model: ImaginaireModel, data: dict[str, torch.Tensor], itera...
    def on_training_step_start(self, model: ImaginaireModel, data: dict[str, torch.Tensor], iteration: int = 0) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Called before the training step, for each batch. This is paired with on_training_step_end() but note that
        when using gradient accumulation, while on_training_step_end() is only called when the optimizer is updated,
        this function is called for every batch.
        Use on_training_step_batch_start and on_training_step_batch_end if you need callbacks that are called
        for every batch, albeit with the same iteration number.
        """
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_training_step_batch_start(
    def on_training_step_batch_start(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, model: ImaginaireModel, data: dict[str, torch.Tensor], iteration: int = 0
        self, model: ImaginaireModel, data: dict[str, torch.Tensor], iteration: int = 0
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Called before the training step, for each batch, similarly to on_training_step_start(). This function is paired with
        on_training_step_batch_end(), and both functions are called for every batch even when using gradient accumulation.
        Note that the iteration is only updated when the optimizer is updated, and therefore it may be the same for multiple invocations.
        """
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_before_forward(self, iteration: int = 0) -> None:
    def on_before_forward(self, iteration: int = 0) -> None:
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_after_forward(self, iteration: int = 0) -> None:
    def on_after_forward(self, iteration: int = 0) -> None:
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_before_backward(
    def on_before_backward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, model_ddp: distributed.DistributedDataParallel, loss: torch.Tensor, iteration: int = 0
        self, model_ddp: distributed.DistributedDataParallel, loss: torch.Tensor, iteration: int = 0
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_after_backward(self, model_ddp: distributed.DistributedDataParallel, iteration: int = ...
    def on_after_backward(self, model_ddp: distributed.DistributedDataParallel, iteration: int = 0) -> None:
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_before_dataloading(self, iteration: int = 0) -> None:
    def on_before_dataloading(self, iteration: int = 0) -> None:
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_after_dataloading(self, iteration: int = 0) -> None:
    def on_after_dataloading(self, iteration: int = 0) -> None:
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_optimizer_init_start(self) -> None:
    def on_optimizer_init_start(self) -> None:
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_optimizer_init_end(self) -> None:
    def on_optimizer_init_end(self) -> None:
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_before_optimizer_step(
    def on_before_optimizer_step(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model_ddp: distributed.DistributedDataParallel,
        model_ddp: distributed.DistributedDataParallel,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：optimizer: torch.optim.Optimizer,
        optimizer: torch.optim.Optimizer,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scheduler: torch.optim.lr_scheduler.LRScheduler,
        scheduler: torch.optim.lr_scheduler.LRScheduler,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：grad_scaler: torch.amp.GradScaler,
        grad_scaler: torch.amp.GradScaler,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：iteration: int = 0,
        iteration: int = 0,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_before_zero_grad(
    def on_before_zero_grad(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model_ddp: distributed.DistributedDataParallel,
        model_ddp: distributed.DistributedDataParallel,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：optimizer: torch.optim.Optimizer,
        optimizer: torch.optim.Optimizer,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scheduler: torch.optim.lr_scheduler.LRScheduler,
        scheduler: torch.optim.lr_scheduler.LRScheduler,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：iteration: int = 0,
        iteration: int = 0,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_training_step_batch_end(
    def on_training_step_batch_end(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model: ImaginaireModel,
        model: ImaginaireModel,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_batch: dict[str, torch.Tensor],
        data_batch: dict[str, torch.Tensor],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：output_batch: dict[str, torch.Tensor],
        output_batch: dict[str, torch.Tensor],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：loss: torch.Tensor,
        loss: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：iteration: int = 0,
        iteration: int = 0,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Called at the end of a training step for every batch even when using gradient accumulation.
        This is paired with on_training_step_batch_start(). Note that the iteration is only updated when the optimizer is updated,
        and therefore it may be the same for multiple batches.
        """
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_training_step_end(
    def on_training_step_end(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model: ImaginaireModel,
        model: ImaginaireModel,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_batch: dict[str, torch.Tensor],
        data_batch: dict[str, torch.Tensor],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：output_batch: dict[str, torch.Tensor],
        output_batch: dict[str, torch.Tensor],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：loss: torch.Tensor,
        loss: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：iteration: int = 0,
        iteration: int = 0,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Called at the end of a training step, but note that when using gradient accumulation, this is only called
        when the optimizer is updated, and the iteration incremented, whereas on_training_step_start is called every time.
        Use on_training_step_batch_start and on_training_step_batch_end if you need callbacks that are called
        for every batch.
        """
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_validation_start(
    def on_validation_start(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, model: ImaginaireModel, dataloader_val: torch.utils.data.DataLoader, iteration: int = 0
        self, model: ImaginaireModel, dataloader_val: torch.utils.data.DataLoader, iteration: int = 0
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_validation_step_start(
    def on_validation_step_start(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, model: ImaginaireModel, data: dict[str, torch.Tensor], iteration: int = 0
        self, model: ImaginaireModel, data: dict[str, torch.Tensor], iteration: int = 0
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_validation_step_end(
    def on_validation_step_end(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model: ImaginaireModel,
        model: ImaginaireModel,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_batch: dict[str, torch.Tensor],
        data_batch: dict[str, torch.Tensor],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：output_batch: dict[str, torch.Tensor],
        output_batch: dict[str, torch.Tensor],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：loss: torch.Tensor,
        loss: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：iteration: int = 0,
        iteration: int = 0,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_validation_end(self, model: ImaginaireModel, iteration: int = 0) -> None:
    def on_validation_end(self, model: ImaginaireModel, iteration: int = 0) -> None:
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_load_checkpoint_start(self, model: ImaginaireModel) -> None:
    def on_load_checkpoint_start(self, model: ImaginaireModel) -> None:
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_load_checkpoint_end(
    def on_load_checkpoint_end(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, model: ImaginaireModel, iteration: int = 0, checkpoint_path: Optional[str] = None
        self, model: ImaginaireModel, iteration: int = 0, checkpoint_path: Optional[str] = None
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_load_checkpoint(self, model: ImaginaireModel, state_dict: dict[Any]) -> None:
    def on_load_checkpoint(self, model: ImaginaireModel, state_dict: dict[Any]) -> None:
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_save_checkpoint_start(self, model: ImaginaireModel, iteration: int = 0) -> None:
    def on_save_checkpoint_start(self, model: ImaginaireModel, iteration: int = 0) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Called when checkpoint saving is about to start.
        """
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_save_checkpoint_end(self, model: ImaginaireModel, iteration: int = 0) -> None:
    def on_save_checkpoint_end(self, model: ImaginaireModel, iteration: int = 0) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Called when the synchronous part of checkpointing is finished, this function can be used
        along with on_save_checkpoint_start() to measure the exposed (synchronous) checkpoint time.
        Note that for asynchronous checkpoint, the checkpoint may still be ongoing, so this function
        does not mean the checkpoint is finished for the asynchronous case, use on_save_checkpoint_success()
        for that.
        """
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_save_checkpoint_success(self, iteration: int = 0, elapsed_time: float = 0) -> None:
    def on_save_checkpoint_success(self, iteration: int = 0, elapsed_time: float = 0) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Called when checkpoint saving is fully finished, and succeeded. Not called if checkpoint failed.
        For synchronous checkpoint, it is called at the same time as on_save_checkpoint_end(), but for asynchronous
        checkpoint, it is called after the asynchronous part has also finished. For checkpointers with out-of-process
        checkpointing, this function is called as soon as the notification is received from the checkpointer process,
        which may not be immediately after the checkpoint has completed but later on. Therefore, if you need to measure
        the full checkpoint duration for the asynchronous part, use the elapsed_time parameter, do not measure it directly
        as this would be a significant overestimate.
        """
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_save_checkpoint(self, model: ImaginaireModel, state_dict: dict[Any]) -> None:
    def on_save_checkpoint(self, model: ImaginaireModel, state_dict: dict[Any]) -> None:
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_train_end(self, model: ImaginaireModel, iteration: int = 0) -> None:
    def on_train_end(self, model: ImaginaireModel, iteration: int = 0) -> None:
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_app_end(self) -> None:
    def on_app_end(self) -> None:
        # 中文说明：执行循环控制或空操作；代码：pass
        pass


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class EMAModelCallback(Callback):
class EMAModelCallback(Callback):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""The callback class for tracking EMA model weights."""
    """The callback class for tracking EMA model weights."""

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_train_start(self, model: ImaginaireModel, iteration: int = 0) -> None:
    def on_train_start(self, model: ImaginaireModel, iteration: int = 0) -> None:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Set up the EMA model weight tracker.
        # Set up the EMA model weight tracker.
        # 中文说明：根据条件选择执行分支；代码：if model.config.ema.enabled:
        if model.config.ema.enabled:
            # 中文说明：检查运行时假设是否成立；代码：assert hasattr(model, "ema"), "EMA should be initialized from ImaginaireModel"
            assert hasattr(model, "ema"), "EMA should be initialized from ImaginaireModel"
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# EMA model must be kept in FP32 precision.
            # EMA model must be kept in FP32 precision.
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model.ema = model.ema.to(dtype=torch.float32)
            model.ema = model.ema.to(dtype=torch.float32)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：检查运行时假设是否成立；代码：assert not hasattr(model, "ema"), "There should be no EMA initialized."
            assert not hasattr(model, "ema"), "There should be no EMA initialized."

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_training_step_end(
    def on_training_step_end(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model: ImaginaireModel,
        model: ImaginaireModel,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_batch: dict[str, torch.Tensor],
        data_batch: dict[str, torch.Tensor],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：output_batch: dict[str, torch.Tensor],
        output_batch: dict[str, torch.Tensor],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：loss: torch.Tensor,
        loss: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：iteration: int = 0,
        iteration: int = 0,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Update the EMA model with the new regular weights.
        # Update the EMA model with the new regular weights.
        # 中文说明：根据条件选择执行分支；代码：if model.config.ema.enabled:
        if model.config.ema.enabled:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model.ema.update_average(model, iteration)
            model.ema.update_average(model, iteration)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ProgressBarCallback(Callback):
class ProgressBarCallback(Callback):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""The callback class for visualizing the training/validation progress bar in the console."""
    """The callback class for visualizing the training/validation progress bar in the console."""

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@distributed.rank0_only
    @distributed.rank0_only
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_train_start(self, model: ImaginaireModel, iteration: int = 0) -> None:
    def on_train_start(self, model: ImaginaireModel, iteration: int = 0) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.train_pbar = tqdm.trange(self.config.trainer.max_iter, initial=iteration, desc="Training")
        self.train_pbar = tqdm.trange(self.config.trainer.max_iter, initial=iteration, desc="Training")

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@distributed.rank0_only
    @distributed.rank0_only
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_training_step_end(
    def on_training_step_end(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model: ImaginaireModel,
        model: ImaginaireModel,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_batch: dict[str, torch.Tensor],
        data_batch: dict[str, torch.Tensor],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：output_batch: dict[str, torch.Tensor],
        output_batch: dict[str, torch.Tensor],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：loss: torch.Tensor,
        loss: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：iteration: int = 0,
        iteration: int = 0,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.train_pbar.update()
        self.train_pbar.update()

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@distributed.rank0_only
    @distributed.rank0_only
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_validation_start(
    def on_validation_start(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, model: ImaginaireModel, dataloader_val: torch.utils.data.DataLoader, iteration: int = 0
        self, model: ImaginaireModel, dataloader_val: torch.utils.data.DataLoader, iteration: int = 0
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：根据条件选择执行分支；代码：if self.config.trainer.max_val_iter is not None:
        if self.config.trainer.max_val_iter is not None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_iter = self.config.trainer.max_val_iter
            num_iter = self.config.trainer.max_val_iter
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_iter = len(dataloader_val)
            num_iter = len(dataloader_val)
        # 中文说明：检查运行时假设是否成立；代码：assert num_iter is not None and num_iter > 0, f"Invalid number of validation iterations: {num...
        assert num_iter is not None and num_iter > 0, f"Invalid number of validation iterations: {num_iter}"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.val_pbar = tqdm.trange(num_iter, desc="Validating", position=1, leave=False)
        self.val_pbar = tqdm.trange(num_iter, desc="Validating", position=1, leave=False)

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@distributed.rank0_only
    @distributed.rank0_only
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_validation_step_end(
    def on_validation_step_end(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model: ImaginaireModel,
        model: ImaginaireModel,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_batch: dict[str, torch.Tensor],
        data_batch: dict[str, torch.Tensor],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：output_batch: dict[str, torch.Tensor],
        output_batch: dict[str, torch.Tensor],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：loss: torch.Tensor,
        loss: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：iteration: int = 0,
        iteration: int = 0,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.val_pbar.update()
        self.val_pbar.update()

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@distributed.rank0_only
    @distributed.rank0_only
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_validation_end(self, model: ImaginaireModel, iteration: int = 0) -> None:
    def on_validation_end(self, model: ImaginaireModel, iteration: int = 0) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.val_pbar.close()
        self.val_pbar.close()

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@distributed.rank0_only
    @distributed.rank0_only
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_train_end(self, model: ImaginaireModel, iteration: int = 0) -> None:
    def on_train_end(self, model: ImaginaireModel, iteration: int = 0) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.trainer.checkpointer.finalize()
        self.trainer.checkpointer.finalize()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.train_pbar.close()
        self.train_pbar.close()


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class IterationLoggerCallback(Callback):
class IterationLoggerCallback(Callback):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""The callback class for visualizing the training/validation progress bar in the console."""
    """The callback class for visualizing the training/validation progress bar in the console."""

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@distributed.rank0_only
    @distributed.rank0_only
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_train_start(self, model: ImaginaireModel, iteration: int = 0) -> None:
    def on_train_start(self, model: ImaginaireModel, iteration: int = 0) -> None:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self.train_pbar = tqdm.trange(self.config.trainer.max_iter, initial=iteration, desc="Traini...
        # self.train_pbar = tqdm.trange(self.config.trainer.max_iter, initial=iteration, desc="Training")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.start_iteration_time = time.time()
        self.start_iteration_time = time.time()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.elapsed_iteration_time = 0
        self.elapsed_iteration_time = 0

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@distributed.rank0_only
    @distributed.rank0_only
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_training_step_start(self, model: ImaginaireModel, data: dict[str, torch.Tensor], itera...
    def on_training_step_start(self, model: ImaginaireModel, data: dict[str, torch.Tensor], iteration: int = 0) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.start_iteration_time = time.time()
        self.start_iteration_time = time.time()

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@distributed.rank0_only
    @distributed.rank0_only
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_training_step_end(
    def on_training_step_end(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model: ImaginaireModel,
        model: ImaginaireModel,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_batch: dict[str, torch.Tensor],
        data_batch: dict[str, torch.Tensor],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：output_batch: dict[str, torch.Tensor],
        output_batch: dict[str, torch.Tensor],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：loss: torch.Tensor,
        loss: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：iteration: int = 0,
        iteration: int = 0,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.elapsed_iteration_time += time.time() - self.start_iteration_time
        self.elapsed_iteration_time += time.time() - self.start_iteration_time

        # 中文说明：根据条件选择执行分支；代码：if iteration % self.config.trainer.logging_iter == 0:
        if iteration % self.config.trainer.logging_iter == 0:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：avg_time = self.elapsed_iteration_time / self.config.trainer.logging_iter
            avg_time = self.elapsed_iteration_time / self.config.trainer.logging_iter
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Iteration: {iteration}, average iter time: {avg_time:2f}, total loss {loss.item():...
            log.info(f"Iteration: {iteration}, average iter time: {avg_time:2f}, total loss {loss.item():4f}")

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.elapsed_iteration_time = 0
            self.elapsed_iteration_time = 0


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class LowPrecisionCallback(Callback):
class LowPrecisionCallback(Callback):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""The callback class handling low precision training
    """The callback class handling low precision training

    Config with non-primitive type makes it difficult to override the option.
    The callback gets precision from model.precision instead.
    It also auto disabled when using fp32.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, config: Config, trainer: ImaginaireTrainer, update_iter: int):
    def __init__(self, config: Config, trainer: ImaginaireTrainer, update_iter: int):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.update_iter = update_iter
        self.update_iter = update_iter

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_train_start(self, model: ImaginaireModel, iteration: int = 0) -> None:
    def on_train_start(self, model: ImaginaireModel, iteration: int = 0) -> None:
        # 中文说明：检查运行时假设是否成立；代码：assert model.precision in [
        assert model.precision in [
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.bfloat16,
            torch.bfloat16,
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.float16,
            torch.float16,
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.half,
            torch.half,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：], "LowPrecisionCallback must use a low precision dtype."
        ], "LowPrecisionCallback must use a low precision dtype."
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.precision_type = model.precision
        self.precision_type = model.precision

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_training_step_start(self, model: ImaginaireModel, data: dict[str, torch.Tensor], itera...
    def on_training_step_start(self, model: ImaginaireModel, data: dict[str, torch.Tensor], iteration: int = 0) -> None:
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for k, v in data.items():
        for k, v in data.items():
            # 中文说明：根据条件选择执行分支；代码：if isinstance(v, torch.Tensor) and torch.is_floating_point(data[k]):
            if isinstance(v, torch.Tensor) and torch.is_floating_point(data[k]):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data[k] = v.to(dtype=self.precision_type)
                data[k] = v.to(dtype=self.precision_type)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_validation_step_start(
    def on_validation_step_start(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, model: ImaginaireModel, data: dict[str, torch.Tensor], iteration: int = 0
        self, model: ImaginaireModel, data: dict[str, torch.Tensor], iteration: int = 0
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for k, v in data.items():
        for k, v in data.items():
            # 中文说明：根据条件选择执行分支；代码：if isinstance(v, torch.Tensor) and torch.is_floating_point(data[k]):
            if isinstance(v, torch.Tensor) and torch.is_floating_point(data[k]):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data[k] = v.to(dtype=self.precision_type)
                data[k] = v.to(dtype=self.precision_type)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_before_zero_grad(
    def on_before_zero_grad(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model_ddp: distributed.DistributedDataParallel,
        model_ddp: distributed.DistributedDataParallel,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：optimizer: torch.optim.Optimizer,
        optimizer: torch.optim.Optimizer,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scheduler: torch.optim.lr_scheduler.LRScheduler,
        scheduler: torch.optim.lr_scheduler.LRScheduler,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：iteration: int = 0,
        iteration: int = 0,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：根据条件选择执行分支；代码：if iteration % self.update_iter == 0:
        if iteration % self.update_iter == 0:
            # 中文说明：根据条件选择执行分支；代码：if getattr(optimizer, "master_weights", False):
            if getattr(optimizer, "master_weights", False):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：params, master_params = [], []
                params, master_params = [], []
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for group, group_master in zip(optimizer.param_groups, optimizer.param_groups_master):
                for group, group_master in zip(optimizer.param_groups, optimizer.param_groups_master):
                    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for p, p_master in zip(group["params"], group_master["params"]):
                    for p, p_master in zip(group["params"], group_master["params"]):
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：params.append(get_local_tensor_if_DTensor(p.data))
                        params.append(get_local_tensor_if_DTensor(p.data))
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：master_params.append(p_master.data)
                        master_params.append(p_master.data)
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch._foreach_copy_(params, master_params)
                torch._foreach_copy_(params, master_params)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class NVTXCallback(Callback):
class NVTXCallback(Callback):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""The callback for creating NVTX ranges"""
    """The callback for creating NVTX ranges"""

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：synchronize: bool = False,
        synchronize: bool = False,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：config: Optional["Config"] = None,
        config: Optional["Config"] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：trainer: Optional["ImaginaireTrainer"] = None,
        trainer: Optional["ImaginaireTrainer"] = None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(config, trainer)
        super().__init__(config, trainer)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.synchronize = synchronize
        self.synchronize = synchronize

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_before_forward(self, iteration: int = 0) -> None:
    def on_before_forward(self, iteration: int = 0) -> None:
        # 中文说明：根据条件选择执行分支；代码：if self.synchronize:
        if self.synchronize:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.synchronize()
            torch.cuda.synchronize()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.nvtx.range_push("forward")
        torch.cuda.nvtx.range_push("forward")

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_after_forward(self, iteration: int = 0) -> None:
    def on_after_forward(self, iteration: int = 0) -> None:
        # 中文说明：根据条件选择执行分支；代码：if self.synchronize:
        if self.synchronize:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.synchronize()
            torch.cuda.synchronize()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.nvtx.range_pop()
        torch.cuda.nvtx.range_pop()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_before_backward(
    def on_before_backward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, model_ddp: distributed.DistributedDataParallel, loss: torch.Tensor, iteration: int = 0
        self, model_ddp: distributed.DistributedDataParallel, loss: torch.Tensor, iteration: int = 0
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：根据条件选择执行分支；代码：if self.synchronize:
        if self.synchronize:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.synchronize()
            torch.cuda.synchronize()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.nvtx.range_push("backward")
        torch.cuda.nvtx.range_push("backward")

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_after_backward(self, model_ddp: distributed.DistributedDataParallel, iteration: int = ...
    def on_after_backward(self, model_ddp: distributed.DistributedDataParallel, iteration: int = 0) -> None:
        # 中文说明：根据条件选择执行分支；代码：if self.synchronize:
        if self.synchronize:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.synchronize()
            torch.cuda.synchronize()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.nvtx.range_pop()
        torch.cuda.nvtx.range_pop()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_before_optimizer_step(
    def on_before_optimizer_step(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model_ddp: distributed.DistributedDataParallel,
        model_ddp: distributed.DistributedDataParallel,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：optimizer: torch.optim.Optimizer,
        optimizer: torch.optim.Optimizer,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scheduler: torch.optim.lr_scheduler.LRScheduler,
        scheduler: torch.optim.lr_scheduler.LRScheduler,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：grad_scaler: torch.amp.GradScaler,
        grad_scaler: torch.amp.GradScaler,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：iteration: int = 0,
        iteration: int = 0,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：根据条件选择执行分支；代码：if self.synchronize:
        if self.synchronize:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.synchronize()
            torch.cuda.synchronize()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.nvtx.range_push("optimizer_step")
        torch.cuda.nvtx.range_push("optimizer_step")

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_before_zero_grad(
    def on_before_zero_grad(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model_ddp: distributed.DistributedDataParallel,
        model_ddp: distributed.DistributedDataParallel,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：optimizer: torch.optim.Optimizer,
        optimizer: torch.optim.Optimizer,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scheduler: torch.optim.lr_scheduler.LRScheduler,
        scheduler: torch.optim.lr_scheduler.LRScheduler,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：iteration: int = 0,
        iteration: int = 0,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：根据条件选择执行分支；代码：if self.synchronize:
        if self.synchronize:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.synchronize()
            torch.cuda.synchronize()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.nvtx.range_pop()
        torch.cuda.nvtx.range_pop()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_before_dataloading(self, iteration: int = 0) -> None:
    def on_before_dataloading(self, iteration: int = 0) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.nvtx.range_push("dataloading")
        torch.cuda.nvtx.range_push("dataloading")

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_after_dataloading(self, iteration: int = 0) -> None:
    def on_after_dataloading(self, iteration: int = 0) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.nvtx.range_pop()
        torch.cuda.nvtx.range_pop()
