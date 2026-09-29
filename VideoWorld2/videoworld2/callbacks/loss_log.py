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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from dataclasses import dataclass
from dataclasses import dataclass
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Tuple
from typing import Tuple

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.distributed as dist
import torch.distributed as dist

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.model import ImaginaireModel
from imaginaire.model import ImaginaireModel
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import distributed, log
from imaginaire.utils import distributed, log
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.callback import Callback
from imaginaire.utils.callback import Callback


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@dataclass
@dataclass
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class _LossRecord:
class _LossRecord:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：iter_count: int = 0
    iter_count: int = 0
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：loss: float = 0
    loss: float = 0

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def reset(self) -> None:
    def reset(self) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.iter_count = 0
        self.iter_count = 0
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.loss = 0
        self.loss = 0

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_stat(self) -> Tuple[float, float]:
    def get_stat(self) -> Tuple[float, float]:
        # 中文说明：根据条件选择执行分支；代码：if self.iter_count > 0:
        if self.iter_count > 0:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：loss = self.loss / self.iter_count
            loss = self.loss / self.iter_count
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dist.all_reduce(loss, op=dist.ReduceOp.AVG)
            dist.all_reduce(loss, op=dist.ReduceOp.AVG)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：loss = torch.ones(1)
            loss = torch.ones(1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iter_count = self.iter_count
        iter_count = self.iter_count
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.reset()
        self.reset()
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return loss.tolist(), iter_count
        return loss.tolist(), iter_count


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class LossLog(Callback):
class LossLog(Callback):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：logging_iter_multipler: int = 1,
        logging_iter_multipler: int = 1,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.logging_iter_multipler = logging_iter_multipler
        self.logging_iter_multipler = logging_iter_multipler
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.name = self.__class__.__name__
        self.name = self.__class__.__name__

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.train_video_log = _LossRecord()
        self.train_video_log = _LossRecord()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_before_backward(
    def on_before_backward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model: ImaginaireModel,
        model: ImaginaireModel,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：loss: torch.Tensor,
        loss: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：iteration: int = 0,
        iteration: int = 0,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Log this loss for aligning the curve with diffsyncstudio
        # Log this loss for aligning the curve with diffsyncstudio
        # 中文说明：根据条件选择执行分支；代码：if iteration % (self.config.trainer.logging_iter * self.logging_iter_multipler) == 0 and dist...
        if iteration % (self.config.trainer.logging_iter * self.logging_iter_multipler) == 0 and distributed.is_rank0():
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：info = {
            info = {
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："train_loss_step": loss.detach().item(),
                "train_loss_step": loss.detach().item(),
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
            }

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
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：skip_update_due_to_unstable_loss = False
        skip_update_due_to_unstable_loss = False
        # 中文说明：根据条件选择执行分支；代码：if torch.isnan(loss) or torch.isinf(loss):
        if torch.isnan(loss) or torch.isinf(loss):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：skip_update_due_to_unstable_loss = True
            skip_update_due_to_unstable_loss = True
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.critical(
            log.critical(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Unstable loss {loss} at iteration {iteration} with is_image_batch: {model.is_image_batch(da...
                f"Unstable loss {loss} at iteration {iteration} with is_image_batch: {model.is_image_batch(data_batch)}",
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank0_only=False,
                rank0_only=False,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：根据条件选择执行分支；代码：if not skip_update_due_to_unstable_loss:
        if not skip_update_due_to_unstable_loss:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_loss = output_batch["loss"].detach().mean(dim=0)
            _loss = output_batch["loss"].detach().mean(dim=0)

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.train_video_log.iter_count += 1
            self.train_video_log.iter_count += 1
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.train_video_log.loss += _loss
            self.train_video_log.loss += _loss

        # 中文说明：根据条件选择执行分支；代码：if iteration % (self.config.trainer.logging_iter * self.logging_iter_multipler) == 0:
        if iteration % (self.config.trainer.logging_iter * self.logging_iter_multipler) == 0:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：world_size = dist.get_world_size()
            world_size = dist.get_world_size()
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：loss, iter_count = self.train_video_log.get_stat()
            loss, iter_count = self.train_video_log.get_stat()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iter_count *= world_size
            iter_count *= world_size

            # 中文说明：根据条件选择执行分支；代码：if distributed.is_rank0():
            if distributed.is_rank0():
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：info = {}
                info = {}
                # 中文说明：根据条件选择执行分支；代码：if iter_count > 0:
                if iter_count > 0:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：info[f"train@{self.logging_iter_multipler}/loss"] = loss
                    info[f"train@{self.logging_iter_multipler}/loss"] = loss
