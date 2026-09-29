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

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.functional.lr_scheduler import LambdaLinearScheduler
from videoworld2.functional.lr_scheduler import LambdaLinearScheduler
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import LazyCall as L
from imaginaire.lazy_config import LazyCall as L
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import LazyDict
from imaginaire.lazy_config import LazyDict

# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：LambdaLinearSchedulerConfig: LazyDict = L(LambdaLinearScheduler)(
LambdaLinearSchedulerConfig: LazyDict = L(LambdaLinearScheduler)(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：warm_up_steps=[1000],
    warm_up_steps=[1000],
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cycle_lengths=[10000000000000],
    cycle_lengths=[10000000000000],
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：f_start=[1.0e-6],
    f_start=[1.0e-6],
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：f_max=[1.0],
    f_max=[1.0],
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：f_min=[1.0],
    f_min=[1.0],
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ConstantScheduler:
class ConstantScheduler:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Linear instead of cosine decay for the main part of the cycle.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, n, **kwargs):
    def __call__(self, n, **kwargs):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return 1.0
        return 1.0

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def schedule(self, n, **kwargs):
    def schedule(self, n, **kwargs):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return 1.0
        return 1.0


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def register_scheduler():
def register_scheduler():
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cs = ConfigStore.instance()
    cs = ConfigStore.instance()
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(group="scheduler", package="scheduler", name="lambdalinear", node=LambdaLinearSchedu...
    cs.store(group="scheduler", package="scheduler", name="lambdalinear", node=LambdaLinearSchedulerConfig)
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(group="scheduler", package="scheduler", name="constant", node=L(ConstantScheduler)())
    cs.store(group="scheduler", package="scheduler", name="constant", node=L(ConstantScheduler)())
