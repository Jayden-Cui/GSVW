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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from abc import abstractmethod
from abc import abstractmethod
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Optional
from typing import Optional

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.model import ImaginaireModel
from imaginaire.model import ImaginaireModel
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.trainer import ImaginaireTrainer
from imaginaire.trainer import ImaginaireTrainer
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import distributed, log
from imaginaire.utils import distributed, log
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.callback import Callback
from imaginaire.utils.callback import Callback


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class EveryN(Callback):
class EveryN(Callback):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：every_n: Optional[int] = None,
        every_n: Optional[int] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：step_size: int = 1,
        step_size: int = 1,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：barrier_after_run: bool = True,
        barrier_after_run: bool = True,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：run_at_start: bool = False,
        run_at_start: bool = False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Constructor for `EveryN`.
        """Constructor for `EveryN`.

        Args:
            every_n (int): Frequency with which callback is run during training.
            step_size (int): Size of iteration step count. Default 1.
            barrier_after_run (bool): Whether to have a distributed barrier after each execution. Default True, to avoid timeouts.
            run_at_start (bool): Whether to run at the beginning of training. Default False.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.every_n = every_n
        self.every_n = every_n
        # 中文说明：根据条件选择执行分支；代码：if self.every_n == 0:
        if self.every_n == 0:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(
            log.warning(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"every_n is set to 0. Callback {self.__class__.__name__} will be invoked only once in the be...
                f"every_n is set to 0. Callback {self.__class__.__name__} will be invoked only once in the beginning of the training. Calls happens on_training_step_end will be skipped."
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.step_size = step_size
        self.step_size = step_size
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.barrier_after_run = barrier_after_run
        self.barrier_after_run = barrier_after_run
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.run_at_start = run_at_start
        self.run_at_start = run_at_start

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
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# every_n = 0 is a special case which means every_n_impl will be called only once in the begi...
        # every_n = 0 is a special case which means every_n_impl will be called only once in the beginning of the training
        # 中文说明：根据条件选择执行分支；代码：if self.every_n != 0:
        if self.every_n != 0:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trainer = self.trainer
            trainer = self.trainer
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：global_step = iteration // self.step_size
            global_step = iteration // self.step_size
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：should_run = (iteration == 1 and self.run_at_start) or (
            should_run = (iteration == 1 and self.run_at_start) or (
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：global_step % self.every_n == 0
                global_step % self.every_n == 0
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) # (self.every_n - 1)
            )  # (self.every_n - 1)
            # 中文说明：根据条件选择执行分支；代码：if should_run:
            if should_run:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(f"Callback {self.__class__.__name__} fired on train_batch_end step {global_step}")
                log.debug(f"Callback {self.__class__.__name__} fired on train_batch_end step {global_step}")
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.every_n_impl(trainer, model, data_batch, output_batch, loss, iteration)
                self.every_n_impl(trainer, model, data_batch, output_batch, loss, iteration)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(f"Callback {self.__class__.__name__} finished on train_batch_end step {global_step}")
                log.debug(f"Callback {self.__class__.__name__} finished on train_batch_end step {global_step}")
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# add necessary barrier to avoid timeout
                # add necessary barrier to avoid timeout
                # 中文说明：根据条件选择执行分支；代码：if self.barrier_after_run:
                if self.barrier_after_run:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：distributed.barrier()
                    distributed.barrier()

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@abstractmethod
    @abstractmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def every_n_impl(
    def every_n_impl(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：trainer: ImaginaireTrainer,
        trainer: ImaginaireTrainer,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model: ImaginaireModel,
        model: ImaginaireModel,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_batch: dict[str, torch.Tensor],
        data_batch: dict[str, torch.Tensor],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：output_batch: dict[str, torch.Tensor],
        output_batch: dict[str, torch.Tensor],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：loss: torch.Tensor,
        loss: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：iteration: int,
        iteration: int,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：...
        ...
