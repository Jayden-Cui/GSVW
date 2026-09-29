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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import attrs
import attrs
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.nn as nn
import torch.nn as nn

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.config import make_freezable
from imaginaire.config import make_freezable


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@make_freezable
@make_freezable
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ModelConfig:
class ModelConfig:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：input_size: int = 1152
    input_size: int = 1152
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_classes: int = 7
    num_classes: int = 7


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class SafetyClassifier(nn.Module):
class SafetyClassifier(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, input_size: int = 1024, num_classes: int = 2):
    def __init__(self, input_size: int = 1024, num_classes: int = 2):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.input_size = input_size
        self.input_size = input_size
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_classes = num_classes
        self.num_classes = num_classes
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.layers = nn.Sequential(
        self.layers = nn.Sequential(
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.Linear(self.input_size, 512),
            nn.Linear(self.input_size, 512),
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.BatchNorm1d(512),
            nn.BatchNorm1d(512),
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.ReLU(),
            nn.ReLU(),
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.Linear(512, 256),
            nn.Linear(512, 256),
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.BatchNorm1d(256),
            nn.BatchNorm1d(256),
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.ReLU(),
            nn.ReLU(),
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.Linear(256, self.num_classes),
            nn.Linear(256, self.num_classes),
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Note: No activation function here; CrossEntropyLoss expects raw logits
            # Note: No activation function here; CrossEntropyLoss expects raw logits
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x):
    def forward(self, x):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.layers(x)
        return self.layers(x)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class VideoSafetyModel(nn.Module):
class VideoSafetyModel(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, config: ModelConfig) -> None:
    def __init__(self, config: ModelConfig) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.config = config
        self.config = config
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_classes = config.num_classes
        self.num_classes = config.num_classes
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.network = SafetyClassifier(input_size=config.input_size, num_classes=self.num_classes)
        self.network = SafetyClassifier(input_size=config.input_size, num_classes=self.num_classes)

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.inference_mode()
    @torch.inference_mode()
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, data_batch: dict[str, torch.Tensor]) -> dict[str, torch.Tensor]:
    def forward(self, data_batch: dict[str, torch.Tensor]) -> dict[str, torch.Tensor]:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：logits = self.network(data_batch["data"].cuda())
        logits = self.network(data_batch["data"].cuda())
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return {"logits": logits}
        return {"logits": logits}
