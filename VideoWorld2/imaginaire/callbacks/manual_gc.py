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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import gc
import gc

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.callbacks.every_n import EveryN
from imaginaire.callbacks.every_n import EveryN
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ManualGarbageCollection(EveryN):
class ManualGarbageCollection(EveryN):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Disable auto gc and manually trigger garbage collection every N iterations
    It is super useful for large scale training to reduce gpu sync time!
    Can reach 50% speedup.

    It is important to note that this callback only disables gc in main process and have auto gc enabled in subprocesses.

    We start disable gc after warm_up iterations to avoid disabling gc in subprocesses, such as dataloader, which can cause OOM
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, *args, warm_up: int = 5, **kwargs):
    def __init__(self, *args, warm_up: int = 5, **kwargs):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["barrier_after_run"] = False
        kwargs["barrier_after_run"] = False
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.counter = 0
        self.counter = 0
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.warm = warm_up
        self.warm = warm_up

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def every_n_impl(self, trainer, model, data_batch, output_batch, loss, iteration):
    def every_n_impl(self, trainer, model, data_batch, output_batch, loss, iteration):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del trainer, model, data_batch, output_batch, loss
        del trainer, model, data_batch, output_batch, loss
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.counter += 1
        self.counter += 1
        # 中文说明：根据条件选择执行分支；代码：if self.counter < self.warm:
        if self.counter < self.warm:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return
            return
        # 中文说明：根据条件选择执行分支；代码：if self.counter == self.warm:
        if self.counter == self.warm:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：gc.disable()
            gc.disable()
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.critical("Garbage collection disabled")
            log.critical("Garbage collection disabled")

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：gc.collect(1)
        gc.collect(1)
