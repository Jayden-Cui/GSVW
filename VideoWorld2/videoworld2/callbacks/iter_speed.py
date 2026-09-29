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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import time
import time

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch import Tensor
from torch import Tensor

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.callbacks.every_n import EveryN
from imaginaire.callbacks.every_n import EveryN
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.model import ImaginaireModel
from imaginaire.model import ImaginaireModel
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.trainer import ImaginaireTrainer
from imaginaire.trainer import ImaginaireTrainer
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.distributed import rank0_only
from imaginaire.utils.distributed import rank0_only
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io import easy_io
from imaginaire.utils.easy_io import easy_io


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class IterSpeed(EveryN):
class IterSpeed(EveryN):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Args:
        hit_thres (int): Number of iterations to wait before logging.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, *args, hit_thres: int = 5, **kwargs):
    def __init__(self, *args, hit_thres: int = 5, **kwargs):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.time = None
        self.time = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.hit_counter = 0
        self.hit_counter = 0
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.hit_thres = hit_thres
        self.hit_thres = hit_thres
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.name = self.__class__.__name__
        self.name = self.__class__.__name__
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.last_hit_time = time.time()
        self.last_hit_time = time.time()

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
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：根据条件选择执行分支；代码：if self.hit_counter < self.hit_thres:
        if self.hit_counter < self.hit_thres:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：recon_loss = output_batch.get('recon_loss', torch.tensor([0])).item()
            recon_loss = output_batch.get('recon_loss', torch.tensor([0])).item()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kendall_loss = output_batch.get('kendall_loss', torch.tensor([0])).item()
            kendall_loss = output_batch.get('kendall_loss', torch.tensor([0])).item()
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(
            log.info(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Iteration {iteration}: "
                f"Iteration {iteration}: "
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Hit counter: {self.hit_counter + 1}/{self.hit_thres} | "
                f"Hit counter: {self.hit_counter + 1}/{self.hit_thres} | "
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Loss: {loss.item():.4f} | "
                f"Loss: {loss.item():.4f} | "
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Recon loss: {recon_loss:.4f} | "
                f"Recon loss: {recon_loss:.4f} | "
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Kendall loss: {kendall_loss:.4f} | "
                f"Kendall loss: {kendall_loss:.4f} | "
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Time: {time.time() - self.last_hit_time:.2f}s"
                f"Time: {time.time() - self.last_hit_time:.2f}s"
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.hit_counter += 1
            self.hit_counter += 1
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.last_hit_time = time.time()
            self.last_hit_time = time.time()
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：#! useful for large scale training and avoid oom crash in the first two iterations!!!
            #! useful for large scale training and avoid oom crash in the first two iterations!!!
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.synchronize()
            torch.cuda.synchronize()
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return
            return
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().on_training_step_end(model, data_batch, output_batch, loss, iteration)
        super().on_training_step_end(model, data_batch, output_batch, loss, iteration)

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@rank0_only
    @rank0_only
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def every_n_impl(
    def every_n_impl(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：trainer: ImaginaireTrainer,
        trainer: ImaginaireTrainer,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model: ImaginaireModel,
        model: ImaginaireModel,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_batch: dict[str, Tensor],
        data_batch: dict[str, Tensor],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：output_batch: dict[str, Tensor],
        output_batch: dict[str, Tensor],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：loss: Tensor,
        loss: Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：iteration: int,
        iteration: int,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：根据条件选择执行分支；代码：if self.time is None:
        if self.time is None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.time = time.time()
            self.time = time.time()
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return
            return
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cur_time = time.time()
        cur_time = time.time()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iter_speed = (cur_time - self.time) / self.every_n / self.step_size
        iter_speed = (cur_time - self.time) / self.every_n / self.step_size

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"{iteration} : iter_speed {iter_speed:.2f} seconds per iteration | Loss: {loss.item...
        log.info(f"{iteration} : iter_speed {iter_speed:.2f} seconds per iteration | Loss: {loss.item():.4f}")

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.time = cur_time
        self.time = cur_time
