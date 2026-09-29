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
# 中文说明：开始一个可捕获异常的代码块；代码：try:
try:
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
    import torch
# 中文说明：处理异常、清理资源或管理上下文；代码：except ImportError:
except ImportError:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：torch = None
    torch = None

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.handlers.base import BaseFileHandler
from imaginaire.utils.easy_io.handlers.base import BaseFileHandler


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class TorchJitHandler(BaseFileHandler):
class TorchJitHandler(BaseFileHandler):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：str_like = False
    str_like = False

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def load_from_fileobj(self, file, **kwargs):
    def load_from_fileobj(self, file, **kwargs):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return torch.jit.load(file, **kwargs)
        return torch.jit.load(file, **kwargs)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def dump_to_fileobj(self, obj, file, **kwargs):
    def dump_to_fileobj(self, obj, file, **kwargs):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.jit.save(obj, file, **kwargs)
        torch.jit.save(obj, file, **kwargs)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def dump_to_str(self, obj, **kwargs):
    def dump_to_str(self, obj, **kwargs):
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise NotImplementedError
        raise NotImplementedError
