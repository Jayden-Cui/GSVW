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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Optional
from typing import Optional

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import distributed, log
from imaginaire.utils import distributed, log


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class TeroPolyScheduler:
class TeroPolyScheduler:
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：total_Mimg: int,
        total_Mimg: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：batch_size: int,
        batch_size: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ref_Mimg: Optional[int] = None,
        ref_Mimg: Optional[int] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ref_batches: float = 70e3 / 1024,
        ref_batches: float = 70e3 / 1024,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_lr_ratio: Optional[float] = 1.0,
        max_lr_ratio: Optional[float] = 1.0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：min_lr_ratio: Optional[float] = None,
        min_lr_ratio: Optional[float] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rampup_Mimg: float = 0,
        rampup_Mimg: float = 0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rampdown_Mimg: int = 0,
        rampdown_Mimg: int = 0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：verbosity_interval: int = 0,
        verbosity_interval: int = 0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：formula: str = "poly",
        formula: str = "poly",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：poly_exp: float = 0.5,
        poly_exp: float = 0.5,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.total_Mimg = total_Mimg
        self.total_Mimg = total_Mimg
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.batch_size = batch_size * distributed.get_world_size()
        self.batch_size = batch_size * distributed.get_world_size()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.ref_Mimg = ref_Mimg or ref_batches * batch_size / 1e6
        self.ref_Mimg = ref_Mimg or ref_batches * batch_size / 1e6
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.ref_batches = ref_batches
        self.ref_batches = ref_batches
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.max_lr_ratio = max_lr_ratio
        self.max_lr_ratio = max_lr_ratio
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.min_lr_ratio = min_lr_ratio
        self.min_lr_ratio = min_lr_ratio
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.rampup_Mimg = rampup_Mimg
        self.rampup_Mimg = rampup_Mimg
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.rampdown_Mimg = rampdown_Mimg
        self.rampdown_Mimg = rampdown_Mimg
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.verbosity_interval = verbosity_interval
        self.verbosity_interval = verbosity_interval
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.formula = formula
        self.formula = formula
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.poly_exp = poly_exp
        self.poly_exp = poly_exp

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._model = None
        self._model = None

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def model(self):
    def model(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self._model
        return self._model

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@model.setter
    @model.setter
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def model(self, model):
    def model(self, model):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._model = model
        self._model = model

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def schedule(self, n, **kwargs):
    def schedule(self, n, **kwargs):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cur_Mimg = getattr(self.model, "sample_counter", 0) / 1e6
        cur_Mimg = getattr(self.model, "sample_counter", 0) / 1e6

        # 中文说明：根据条件选择执行分支；代码：if self.formula == "constant":
        if self.formula == "constant":
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lr = 1.0
            lr = 1.0
        # 中文说明：根据条件选择执行分支；代码：elif self.formula == "poly":
        elif self.formula == "poly":
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lr = max(cur_Mimg / self.ref_Mimg, 1e-8) ** -self.poly_exp
            lr = max(cur_Mimg / self.ref_Mimg, 1e-8) ** -self.poly_exp
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f'Invalid learning rate formula "{self.formula}"')
            raise ValueError(f'Invalid learning rate formula "{self.formula}"')

        # 中文说明：根据条件选择执行分支；代码：if self.max_lr_ratio is not None:
        if self.max_lr_ratio is not None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lr = min(lr, self.max_lr_ratio)
            lr = min(lr, self.max_lr_ratio)
        # 中文说明：根据条件选择执行分支；代码：if self.min_lr_ratio is not None:
        if self.min_lr_ratio is not None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lr = max(lr, self.min_lr_ratio)
            lr = max(lr, self.min_lr_ratio)

        # 中文说明：根据条件选择执行分支；代码：if self.rampup_Mimg > 0 and cur_Mimg < self.rampup_Mimg:
        if self.rampup_Mimg > 0 and cur_Mimg < self.rampup_Mimg:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lr *= cur_Mimg / self.rampup_Mimg
            lr *= cur_Mimg / self.rampup_Mimg
        # 中文说明：根据条件选择执行分支；代码：if self.rampdown_Mimg > 0 and cur_Mimg > self.total_Mimg - self.rampdown_Mimg:
        if self.rampdown_Mimg > 0 and cur_Mimg > self.total_Mimg - self.rampdown_Mimg:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lr *= (self.total_Mimg - cur_Mimg) / self.rampdown_Mimg
            lr *= (self.total_Mimg - cur_Mimg) / self.rampdown_Mimg

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return lr
        return lr

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, n, **kwargs):
    def __call__(self, n, **kwargs):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.schedule(n, **kwargs)
        return self.schedule(n, **kwargs)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class LambdaWarmUpCosineScheduler:
class LambdaWarmUpCosineScheduler:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    A learning rate scheduler that combines warm-up with a cosine decay schedule for multiple cycles.
    It supports different configurations for each cycle, including the number of warm-up steps, minimum
    and maximum scaling factors for the learning rate.

    The scheduler is intended to be used with a base learning rate of 1.0, where the actual learning
    rate at any step is the base learning rate multiplied by the scaling factor computed by the scheduler.

    Parameters:
        warm_up_steps (list[int]): List of integers where each element represents the number of warm-up
                                   steps for the corresponding cycle.
        f_min (list[float]): List of the minimum scaling factors for each cycle after warm-up.
        f_max (list[float]): List of the maximum scaling factors at the start and end of each cosine cycle.
        f_start (list[float]): List of starting scaling factors for each warm-up phase.
        cycle_lengths (list[int]): List of the total lengths of each cycle, including warm-up steps.
        verbosity_interval (int, optional): Interval of training steps at which to print current step and
                                            scaling factor information. Set to 0 by default to disable verbosity.

    Examples:
        >>> scheduler = LambdaWarmUpCosineScheduler2(
                warm_up_steps=[10, 10],
                f_min=[0.1, 0.1],
                f_max=[1.0, 1.0],
                f_start=[0.01, 0.01],
                cycle_lengths=[50, 50],
                verbosity_interval=10)
        >>> for step in range(100):
        >>>     lr_multiplier = scheduler(step)
        >>>     print(f"Step {step}: LR Multiplier = {lr_multiplier}")
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, warm_up_steps, f_min, f_max, f_start, cycle_lengths, verbosity_interval=0):
    def __init__(self, warm_up_steps, f_min, f_max, f_start, cycle_lengths, verbosity_interval=0):
        # 中文说明：检查运行时假设是否成立；代码：assert len(warm_up_steps) == len(f_min) == len(f_max) == len(f_start) == len(cycle_lengths)
        assert len(warm_up_steps) == len(f_min) == len(f_max) == len(f_start) == len(cycle_lengths)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.lr_warm_up_steps = warm_up_steps
        self.lr_warm_up_steps = warm_up_steps
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.f_start = f_start
        self.f_start = f_start
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.f_min = f_min
        self.f_min = f_min
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.f_max = f_max
        self.f_max = f_max
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.cycle_lengths = cycle_lengths
        self.cycle_lengths = cycle_lengths
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.cum_cycles = np.cumsum([0] + list(self.cycle_lengths))
        self.cum_cycles = np.cumsum([0] + list(self.cycle_lengths))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.last_f = 0.0
        self.last_f = 0.0
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.verbosity_interval = verbosity_interval
        self.verbosity_interval = verbosity_interval

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def find_in_interval(self, n):
    def find_in_interval(self, n):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：interval = 0
        interval = 0
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for cl in self.cum_cycles[1:]:
        for cl in self.cum_cycles[1:]:
            # 中文说明：根据条件选择执行分支；代码：if n <= cl:
            if n <= cl:
                # 中文说明：从当前函数返回结果或结束函数执行；代码：return interval
                return interval
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：interval += 1
            interval += 1

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def schedule(self, n, **kwargs):
    def schedule(self, n, **kwargs):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cycle = self.find_in_interval(n)
        cycle = self.find_in_interval(n)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n = n - self.cum_cycles[cycle]
        n = n - self.cum_cycles[cycle]
        # 中文说明：根据条件选择执行分支；代码：if self.verbosity_interval > 0:
        if self.verbosity_interval > 0:
            # 中文说明：根据条件选择执行分支；代码：if n % self.verbosity_interval == 0:
            if n % self.verbosity_interval == 0:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"current step: {n}, recent lr-multiplier: {self.last_f}, " f"current cycle {cycle}")
                log.info(f"current step: {n}, recent lr-multiplier: {self.last_f}, " f"current cycle {cycle}")
        # 中文说明：根据条件选择执行分支；代码：if n < self.lr_warm_up_steps[cycle]:
        if n < self.lr_warm_up_steps[cycle]:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：f = (self.f_max[cycle] - self.f_start[cycle]) / self.lr_warm_up_steps[cycle] * n + self.f_sta...
            f = (self.f_max[cycle] - self.f_start[cycle]) / self.lr_warm_up_steps[cycle] * n + self.f_start[cycle]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.last_f = f
            self.last_f = f
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return f
            return f
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t = (n - self.lr_warm_up_steps[cycle]) / (self.cycle_lengths[cycle] - self.lr_warm_up_steps[c...
            t = (n - self.lr_warm_up_steps[cycle]) / (self.cycle_lengths[cycle] - self.lr_warm_up_steps[cycle])
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t = min(t, 1.0)
            t = min(t, 1.0)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：f = self.f_min[cycle] + 0.5 * (self.f_max[cycle] - self.f_min[cycle]) * (1 + np.cos(t * np.pi))
            f = self.f_min[cycle] + 0.5 * (self.f_max[cycle] - self.f_min[cycle]) * (1 + np.cos(t * np.pi))
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.last_f = f
            self.last_f = f
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return f
            return f

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, n, **kwargs):
    def __call__(self, n, **kwargs):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.schedule(n, **kwargs)
        return self.schedule(n, **kwargs)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class LambdaLinearScheduler(LambdaWarmUpCosineScheduler):
class LambdaLinearScheduler(LambdaWarmUpCosineScheduler):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Linear instead of cosine decay for the main part of the cycle.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def schedule(self, n, **kwargs):
    def schedule(self, n, **kwargs):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cycle = self.find_in_interval(n)
        cycle = self.find_in_interval(n)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n = n - self.cum_cycles[cycle]
        n = n - self.cum_cycles[cycle]
        # 中文说明：根据条件选择执行分支；代码：if self.verbosity_interval > 0:
        if self.verbosity_interval > 0:
            # 中文说明：根据条件选择执行分支；代码：if n % self.verbosity_interval == 0:
            if n % self.verbosity_interval == 0:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"current step: {n}, recent lr-multiplier: {self.last_f}, " f"current cycle {cycle}")
                log.info(f"current step: {n}, recent lr-multiplier: {self.last_f}, " f"current cycle {cycle}")

        # 中文说明：根据条件选择执行分支；代码：if n < self.lr_warm_up_steps[cycle]:
        if n < self.lr_warm_up_steps[cycle]:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：f = (self.f_max[cycle] - self.f_start[cycle]) / self.lr_warm_up_steps[cycle] * n + self.f_sta...
            f = (self.f_max[cycle] - self.f_start[cycle]) / self.lr_warm_up_steps[cycle] * n + self.f_start[cycle]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.last_f = f
            self.last_f = f
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return f
            return f
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：f = self.f_min[cycle] + (self.f_max[cycle] - self.f_min[cycle]) * (self.cycle_lengths[cycle] ...
            f = self.f_min[cycle] + (self.f_max[cycle] - self.f_min[cycle]) * (self.cycle_lengths[cycle] - n) / (
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.cycle_lengths[cycle] - self.lr_warm_up_steps[cycle]
                self.cycle_lengths[cycle] - self.lr_warm_up_steps[cycle]
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.last_f = f
            self.last_f = f
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return f
            return f
