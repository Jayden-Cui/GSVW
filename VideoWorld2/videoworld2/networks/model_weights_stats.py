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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from abc import ABC, abstractmethod
from abc import ABC, abstractmethod
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from dataclasses import dataclass
from dataclasses import dataclass
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any
from typing import Any

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch import nn
from torch import nn


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@dataclass
@dataclass
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class TrainingStats:
class TrainingStats:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Data class to hold training statistics."""
    """Data class to hold training statistics."""

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video_samples: int = 0
    video_samples: int = 0
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：image_samples: int = 0
    image_samples: int = 0
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：iterations: int = 0
    iterations: int = 0
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：training_hours: float = 0.0
    training_hours: float = 0.0


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class WeightTrainingStat(nn.Module, ABC):
class WeightTrainingStat(nn.Module, ABC):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Abstract base class for tracking training statistics."""
    """Abstract base class for tracking training statistics."""

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self) -> None:
    def __init__(self) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._initialize_tracking_buffers()
        self._initialize_tracking_buffers()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _initialize_tracking_buffers(self) -> None:
    def _initialize_tracking_buffers(self) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Initialize tracking buffers with default values."""
        """Initialize tracking buffers with default values."""
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tracking_buffers = {
        tracking_buffers = {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："accum_video_sample_counter": torch.tensor(0, dtype=torch.int64),
            "accum_video_sample_counter": torch.tensor(0, dtype=torch.int64),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："accum_image_sample_counter": torch.tensor(0, dtype=torch.int64),
            "accum_image_sample_counter": torch.tensor(0, dtype=torch.int64),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："accum_iteration": torch.tensor(0, dtype=torch.int64),
            "accum_iteration": torch.tensor(0, dtype=torch.int64),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："accum_train_in_hours": torch.tensor(0.0, dtype=torch.float32),
            "accum_train_in_hours": torch.tensor(0.0, dtype=torch.float32),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for name, tensor in tracking_buffers.items():
        for name, tensor in tracking_buffers.items():
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.register_buffer(name, tensor)
            self.register_buffer(name, tensor)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_training_stats(self) -> TrainingStats:
    def get_training_stats(self) -> TrainingStats:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Return current training statistics."""
        """Return current training statistics."""
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return TrainingStats(
        return TrainingStats(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_samples=self.accum_video_sample_counter.item(),
            video_samples=self.accum_video_sample_counter.item(),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：image_samples=self.accum_image_sample_counter.item(),
            image_samples=self.accum_image_sample_counter.item(),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iterations=self.accum_iteration.item(),
            iterations=self.accum_iteration.item(),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：training_hours=self.accum_train_in_hours.item(),
            training_hours=self.accum_train_in_hours.item(),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@abstractmethod
    @abstractmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, *args, **kwargs) -> Any:
    def forward(self, *args, **kwargs) -> Any:
        # 中文说明：执行循环控制或空操作；代码：pass
        pass
