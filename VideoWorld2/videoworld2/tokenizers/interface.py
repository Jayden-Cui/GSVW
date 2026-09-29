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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from abc import ABC, abstractmethod
from abc import ABC, abstractmethod
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Optional
from typing import Optional

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class VideoTokenizerInterface(ABC):
class VideoTokenizerInterface(ABC):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self):
    def __init__(self):
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@abstractmethod
    @abstractmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def reset_dtype(self):
    def reset_dtype(self):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Reset the dtype of the model to the dtype its weights were trained with or quantized to.
        """
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@abstractmethod
    @abstractmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def encode(self, state: torch.Tensor) -> torch.Tensor:
    def encode(self, state: torch.Tensor) -> torch.Tensor:
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@abstractmethod
    @abstractmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def decode(self, latent: torch.Tensor) -> torch.Tensor:
    def decode(self, latent: torch.Tensor) -> torch.Tensor:
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@abstractmethod
    @abstractmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_latent_num_frames(self, num_pixel_frames: int) -> int:
    def get_latent_num_frames(self, num_pixel_frames: int) -> int:
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@abstractmethod
    @abstractmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_pixel_num_frames(self, num_latent_frames: int) -> int:
    def get_pixel_num_frames(self, num_latent_frames: int) -> int:
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@abstractmethod
    @abstractmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def spatial_compression_factor(self):
    def spatial_compression_factor(self):
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@abstractmethod
    @abstractmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def temporal_compression_factor(self):
    def temporal_compression_factor(self):
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@abstractmethod
    @abstractmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def spatial_resolution(self):
    def spatial_resolution(self):
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@abstractmethod
    @abstractmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def pixel_chunk_duration(self):
    def pixel_chunk_duration(self):
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@abstractmethod
    @abstractmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def latent_chunk_duration(self):
    def latent_chunk_duration(self):
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@abstractmethod
    @abstractmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def latent_ch(self) -> int:
    def latent_ch(self) -> int:
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_chunk_overlap(self):
    def is_chunk_overlap(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return False
        return False

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_causal(self):
    def is_causal(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return True
        return True
