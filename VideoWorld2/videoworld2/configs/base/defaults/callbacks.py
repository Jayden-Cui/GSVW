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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from hydra.core.config_store import ConfigStore
from hydra.core.config_store import ConfigStore

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.callbacks.device_monitor import DeviceMonitor
from videoworld2.callbacks.device_monitor import DeviceMonitor
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.callbacks.grad_clip import GradClip
from videoworld2.callbacks.grad_clip import GradClip
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.callbacks.iter_speed import IterSpeed
from videoworld2.callbacks.iter_speed import IterSpeed
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.callbacks.ldm_callback import LDMCallback
from videoworld2.callbacks.ldm_callback import LDMCallback
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.callbacks.loss_log import LossLog
from videoworld2.callbacks.loss_log import LossLog
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.callbacks.manual_gc import ManualGarbageCollection
from imaginaire.callbacks.manual_gc import ManualGarbageCollection
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import PLACEHOLDER
from imaginaire.lazy_config import PLACEHOLDER
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import LazyCall as L
from imaginaire.lazy_config import LazyCall as L
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.callback import LowPrecisionCallback
from imaginaire.utils.callback import LowPrecisionCallback

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：BASIC_CALLBACKS = dict(
BASIC_CALLBACKS = dict(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：low_prec=L(LowPrecisionCallback)(config=PLACEHOLDER, trainer=PLACEHOLDER, update_iter=1),
    low_prec=L(LowPrecisionCallback)(config=PLACEHOLDER, trainer=PLACEHOLDER, update_iter=1),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iter_speed=L(IterSpeed)(
    iter_speed=L(IterSpeed)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：every_n="${trainer.logging_iter}",
        every_n="${trainer.logging_iter}",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：device_monitor=L(DeviceMonitor)(
    device_monitor=L(DeviceMonitor)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：every_n="${trainer.logging_iter}",
        every_n="${trainer.logging_iter}",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：manual_gc=L(ManualGarbageCollection)(every_n=5),
    manual_gc=L(ManualGarbageCollection)(every_n=5),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：loss_log=L(LossLog)(),
    loss_log=L(LossLog)(),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：grad_clip=L(GradClip)(clip_norm=1.0),
    grad_clip=L(GradClip)(clip_norm=1.0),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ldm_callback=L(LDMCallback)(every_n="${trainer.logging_iter}"),
    ldm_callback=L(LDMCallback)(every_n="${trainer.logging_iter}"),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def register_callbacks():
def register_callbacks():
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cs = ConfigStore.instance()
    cs = ConfigStore.instance()
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(group="callbacks", package="trainer.callbacks", name="basic", node=BASIC_CALLBACKS)
    cs.store(group="callbacks", package="trainer.callbacks", name="basic", node=BASIC_CALLBACKS)
