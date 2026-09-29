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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any
from typing import Any

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import LazyDict, instantiate
from imaginaire.lazy_config import LazyDict, instantiate


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ImaginaireModel(torch.nn.Module):
class ImaginaireModel(torch.nn.Module):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""The base model class of Imaginaire. It is inherited from torch.nn.Module.
    """The base model class of Imaginaire. It is inherited from torch.nn.Module.

    All models in Imaginaire should inherit ImaginaireModel. It should include the implementions for all the
    computation graphs. All inheriting child classes should implement the following methods:
    - training_step(): The training step of the model, including the loss computation.
    - validation_step(): The validation step of the model, including the loss computation.
    - forward(): The computation graph for model inference.
    The following methods have default implementations in ImaginaireModel:
    - init_optimizer_scheduler(): Creates the optimizer and scheduler for the model.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self) -> None:
    def __init__(self) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def init_optimizer_scheduler(
    def init_optimizer_scheduler(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, optimizer_config: LazyDict, scheduler_config: LazyDict
        self, optimizer_config: LazyDict, scheduler_config: LazyDict
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> tuple[torch.optim.Optimizer, torch.optim.lr_scheduler.LRScheduler]:
    ) -> tuple[torch.optim.Optimizer, torch.optim.lr_scheduler.LRScheduler]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Creates the optimizer and scheduler for the model.
        """Creates the optimizer and scheduler for the model.

        Args:
            config_model (ModelConfig): The config object for the model.

        Returns:
            optimizer (torch.optim.Optimizer): The model optimizer.
            scheduler (torch.optim.lr_scheduler.LRScheduler): The optimization scheduler.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：optimizer_config.params = self.parameters()
        optimizer_config.params = self.parameters()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：optimizer = instantiate(optimizer_config)
        optimizer = instantiate(optimizer_config)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scheduler_config.optimizer = optimizer
        scheduler_config.optimizer = optimizer
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scheduler = instantiate(scheduler_config)
        scheduler = instantiate(scheduler_config)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return optimizer, scheduler
        return optimizer, scheduler

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def training_step(
    def training_step(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, data_batch: dict[str, torch.Tensor], iteration: int
        self, data_batch: dict[str, torch.Tensor], iteration: int
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> tuple[dict[str, torch.Tensor], torch.Tensor]:
    ) -> tuple[dict[str, torch.Tensor], torch.Tensor]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""The training step of the model, including the loss computation.
        """The training step of the model, including the loss computation.

        Args:
            data (dict[str, torch.Tensor]): Data batch (dictionary of tensors).
            iteration (int): Current iteration number.

        Returns:
            output_batch (dict[str, torch.Tensor]): Auxiliary model output from the training batch.
            loss (torch.Tensor): The total loss for backprop (weighted sum of various losses).
        """
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise NotImplementedError
        raise NotImplementedError

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.no_grad()
    @torch.no_grad()
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def validation_step(
    def validation_step(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, data_batch: dict[str, torch.Tensor], iteration: int
        self, data_batch: dict[str, torch.Tensor], iteration: int
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> tuple[dict[str, torch.Tensor], torch.Tensor]:
    ) -> tuple[dict[str, torch.Tensor], torch.Tensor]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""The validation step of the model, including the loss computation.
        """The validation step of the model, including the loss computation.

        Args:
            data (dict[str, torch.Tensor]): Data batch (dictionary of tensors).
            iteration (int): Current iteration number.

        Returns:
            output_batch (dict[str, torch.Tensor]): Auxiliary model output from the validation batch.
            loss (torch.Tensor): The total loss (weighted sum of various losses).
        """
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise NotImplementedError
        raise NotImplementedError

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.inference_mode()
    @torch.inference_mode()
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, *args: Any, **kwargs: Any) -> Any:
    def forward(self, *args: Any, **kwargs: Any) -> Any:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""The computation graph for model inference.
        """The computation graph for model inference.

        Args:
            *args: Whatever you decide to pass into the forward method.
            **kwargs: Keyword arguments are also possible.

        Return:
            Your model's output.
        """
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise NotImplementedError
        raise NotImplementedError

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_model_init_start(self, set_barrier=False) -> None:
    def on_model_init_start(self, set_barrier=False) -> None:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return
        return

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_model_init_end(self, set_barrier=False) -> None:
    def on_model_init_end(self, set_barrier=False) -> None:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return
        return

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_train_start(self, memory_format: torch.memory_format = torch.preserve_format) -> None:
    def on_train_start(self, memory_format: torch.memory_format = torch.preserve_format) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""The model preparation before the training is launched
        """The model preparation before the training is launched

        Args:
            memory_format (torch.memory_format): Memory format of the model.
        """
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_before_zero_grad(
    def on_before_zero_grad(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, optimizer: torch.optim.Optimizer, scheduler: torch.optim.lr_scheduler.LRScheduler, iter...
        self, optimizer: torch.optim.Optimizer, scheduler: torch.optim.lr_scheduler.LRScheduler, iteration: int
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Hook before zero_grad() is called.
        """Hook before zero_grad() is called.

        Args:
            optimizer (torch.optim.Optimizer): The model optimizer.
            scheduler (torch.optim.lr_scheduler.LRScheduler): The optimization scheduler.
            iteration (int): Current iteration number.
        """
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_after_backward(self, iteration: int = 0) -> None:
    def on_after_backward(self, iteration: int = 0) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Hook after loss.backward() is called.
        """Hook after loss.backward() is called.

        This method is called immediately after the backward pass, allowing for custom operations
        or modifications to be performed on the gradients before the optimizer step.

        Args:
            iteration (int): Current iteration number.
        """
        # 中文说明：执行循环控制或空操作；代码：pass
        pass
