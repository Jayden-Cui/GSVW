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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from hydra.core.config_store import ConfigStore
from hydra.core.config_store import ConfigStore


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class EMAConfig:
class EMAConfig:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Config for the EMA.
    """

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：enabled: bool = False # deactivated by default for inference.
    enabled: bool = False  # deactivated by default for inference.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rate: float = 0.1
    rate: float = 0.1
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：iteration_shift: int = 0
    iteration_shift: int = 0


# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：PowerEMAConfig: EMAConfig = EMAConfig(
PowerEMAConfig: EMAConfig = EMAConfig(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enabled=True,
    enabled=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rate=0.10,
    rate=0.10,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iteration_shift=0,
    iteration_shift=0,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：InferenceEMAConfig: EMAConfig = EMAConfig(
InferenceEMAConfig: EMAConfig = EMAConfig(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enabled=False,
    enabled=False,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def register_ema() -> None:
def register_ema() -> None:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cs = ConfigStore.instance()
    cs = ConfigStore.instance()
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(group="ema", package="model.config.ema", name="power", node=PowerEMAConfig)
    cs.store(group="ema", package="model.config.ema", name="power", node=PowerEMAConfig)
