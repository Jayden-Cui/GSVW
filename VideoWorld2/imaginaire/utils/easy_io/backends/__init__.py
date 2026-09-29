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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.backends.base_backend import BaseStorageBackend
from imaginaire.utils.easy_io.backends.base_backend import BaseStorageBackend
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.backends.http_backend import HTTPBackend
from imaginaire.utils.easy_io.backends.http_backend import HTTPBackend
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.backends.local_backend import LocalBackend
from imaginaire.utils.easy_io.backends.local_backend import LocalBackend
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.backends.registry_utils import backends, prefix_to_backends, re...
from imaginaire.utils.easy_io.backends.registry_utils import backends, prefix_to_backends, register_backend

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：__all__ = [
__all__ = [
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："BaseStorageBackend",
    "BaseStorageBackend",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："LocalBackend",
    "LocalBackend",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："HTTPBackend",
    "HTTPBackend",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："register_backend",
    "register_backend",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："backends",
    "backends",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："prefix_to_backends",
    "prefix_to_backends",
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
]
