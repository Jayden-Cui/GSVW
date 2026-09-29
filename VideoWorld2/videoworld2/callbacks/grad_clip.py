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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import List, Tuple
from typing import List, Tuple

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import wandb
import wandb

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.model import ImaginaireModel
from imaginaire.model import ImaginaireModel
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import distributed
from imaginaire.utils import distributed
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.callback import Callback
from imaginaire.utils.callback import Callback


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.jit.script
@torch.jit.script
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _fused_nan_to_num(params: List[torch.Tensor]):
def _fused_nan_to_num(params: List[torch.Tensor]):
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for param in params:
    for param in params:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.nan_to_num(param, nan=0.0, posinf=0.0, neginf=0.0, out=param)
        torch.nan_to_num(param, nan=0.0, posinf=0.0, neginf=0.0, out=param)


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@dataclass
@dataclass
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class _MagnitudeRecord:
class _MagnitudeRecord:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：state: float = 0
    state: float = 0
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：iter_count: int = 0
    iter_count: int = 0

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def reset(self) -> None:
    def reset(self) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.state = 0
        self.state = 0
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.iter_count = 0
        self.iter_count = 0

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def update(self, cur_state: torch.Tensor) -> None:
    def update(self, cur_state: torch.Tensor) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.state += cur_state
        self.state += cur_state
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.iter_count += 1
        self.iter_count += 1

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_stat(self) -> Tuple[float, float]:
    def get_stat(self) -> Tuple[float, float]:
        # 中文说明：根据条件选择执行分支；代码：if self.iter_count > 0:
        if self.iter_count > 0:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：avg_state = self.state / self.iter_count
            avg_state = self.state / self.iter_count
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：avg_state = avg_state.item()
            avg_state = avg_state.item()
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：avg_state = 0
            avg_state = 0
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.reset()
        self.reset()
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return avg_state
        return avg_state


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class GradClip(Callback):
class GradClip(Callback):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, clip_norm=1.0, force_finite: bool = True):
    def __init__(self, clip_norm=1.0, force_finite: bool = True):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.clip_norm = clip_norm
        self.clip_norm = clip_norm
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.force_finite = force_finite
        self.force_finite = force_finite

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.img_mag_log = _MagnitudeRecord()
        self.img_mag_log = _MagnitudeRecord()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.video_mag_log = _MagnitudeRecord()
        self.video_mag_log = _MagnitudeRecord()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._cur_state = None
        self._cur_state = None

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_training_step_start(
    def on_training_step_start(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, model: ImaginaireModel, data_batch: dict[str, torch.Tensor], iteration: int = 0
        self, model: ImaginaireModel, data_batch: dict[str, torch.Tensor], iteration: int = 0
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：根据条件选择执行分支；代码：if model.is_image_batch(data_batch):
        if model.is_image_batch(data_batch):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._cur_state = self.img_mag_log
            self._cur_state = self.img_mag_log
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._cur_state = self.video_mag_log
            self._cur_state = self.video_mag_log

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
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del optimizer, scheduler
        del optimizer, scheduler
        # 中文说明：根据条件选择执行分支；代码：if isinstance(model_ddp, distributed.DistributedDataParallel):
        if isinstance(model_ddp, distributed.DistributedDataParallel):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model = model_ddp.module
            model = model_ddp.module
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model = model_ddp
            model = model_ddp
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：params = []
        params = []
        # 中文说明：根据条件选择执行分支；代码：if self.force_finite:
        if self.force_finite:
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for param in model.parameters():
            for param in model.parameters():
                # 中文说明：根据条件选择执行分支；代码：if param.grad is not None:
                if param.grad is not None:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：params.append(param.grad)
                    params.append(param.grad)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_fused_nan_to_num(params)
            _fused_nan_to_num(params)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：total_norm = model.clip_grad_norm_(self.clip_norm)
        total_norm = model.clip_grad_norm_(self.clip_norm)

        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._cur_state.update(total_norm)
        self._cur_state.update(total_norm)
        # 中文说明：根据条件选择执行分支；代码：if iteration % self.config.trainer.logging_iter == 0:
        if iteration % self.config.trainer.logging_iter == 0:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：avg_img_mag, avg_video_mag = self.img_mag_log.get_stat(), self.video_mag_log.get_stat()
            avg_img_mag, avg_video_mag = self.img_mag_log.get_stat(), self.video_mag_log.get_stat()
            # 中文说明：根据条件选择执行分支；代码：if wandb.run:
            if wandb.run:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：wandb.log(
                wandb.log(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{
                    {
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："clip_grad_norm/image": avg_img_mag,
                        "clip_grad_norm/image": avg_img_mag,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："clip_grad_norm/video": avg_video_mag,
                        "clip_grad_norm/video": avg_video_mag,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："iteration": iteration,
                        "iteration": iteration,
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：},
                    },
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：step=iteration,
                    step=iteration,
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
