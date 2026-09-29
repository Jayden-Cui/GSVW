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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import math
import math
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import pynvml
import pynvml
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from loguru import logger as logging
from loguru import logger as logging


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Device:
class Device:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_nvml_affinity_elements = math.ceil(os.cpu_count() / 64) # type: ignore
    _nvml_affinity_elements = math.ceil(os.cpu_count() / 64)  # type: ignore

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, device_idx: int):
    def __init__(self, device_idx: int):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.handle = pynvml.nvmlDeviceGetHandleByIndex(device_idx)
        self.handle = pynvml.nvmlDeviceGetHandleByIndex(device_idx)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_name(self) -> str:
    def get_name(self) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return pynvml.nvmlDeviceGetName(self.handle)
        return pynvml.nvmlDeviceGetName(self.handle)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_cpu_affinity(self) -> list[int]:
    def get_cpu_affinity(self) -> list[int]:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：affinity_string = ""
        affinity_string = ""
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for j in pynvml.nvmlDeviceGetCpuAffinity(self.handle, Device._nvml_affinity_elements):
        for j in pynvml.nvmlDeviceGetCpuAffinity(self.handle, Device._nvml_affinity_elements):
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# assume nvml returns list of 64 bit ints
            # assume nvml returns list of 64 bit ints
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：affinity_string = "{:064b}".format(j) + affinity_string
            affinity_string = "{:064b}".format(j) + affinity_string
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：affinity_list = [int(x) for x in affinity_string]
        affinity_list = [int(x) for x in affinity_string]
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：affinity_list.reverse() # so core 0 is in 0th element of list
        affinity_list.reverse()  # so core 0 is in 0th element of list
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return [i for i, e in enumerate(affinity_list) if e != 0]
        return [i for i, e in enumerate(affinity_list) if e != 0]
