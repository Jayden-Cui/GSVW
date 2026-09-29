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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os.path as osp
import os.path as osp
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from abc import ABCMeta, abstractmethod
from abc import ABCMeta, abstractmethod


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def mkdir_or_exist(dir_name, mode=0o777):
def mkdir_or_exist(dir_name, mode=0o777):
    # 中文说明：根据条件选择执行分支；代码：if dir_name == "":
    if dir_name == "":
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return
        return
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dir_name = osp.expanduser(dir_name)
    dir_name = osp.expanduser(dir_name)
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.makedirs(dir_name, mode=mode, exist_ok=True)
    os.makedirs(dir_name, mode=mode, exist_ok=True)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def has_method(obj, method):
def has_method(obj, method):
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return hasattr(obj, method) and callable(getattr(obj, method))
    return hasattr(obj, method) and callable(getattr(obj, method))


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class BaseStorageBackend(metaclass=ABCMeta):
class BaseStorageBackend(metaclass=ABCMeta):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Abstract class of storage backends.
    """Abstract class of storage backends.

    All backends need to implement two apis: :meth:`get()` and
    :meth:`get_text()`.

    - :meth:`get()` reads the file as a byte stream.
    - :meth:`get_text()` reads the file as texts.
    """

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# a flag to indicate whether the backend can create a symlink for a file
    # a flag to indicate whether the backend can create a symlink for a file
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# This attribute will be deprecated in future.
    # This attribute will be deprecated in future.
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_allow_symlink = False
    _allow_symlink = False

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def allow_symlink(self):
    def allow_symlink(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self._allow_symlink
        return self._allow_symlink

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def name(self):
    def name(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.__class__.__name__
        return self.__class__.__name__

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@abstractmethod
    @abstractmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get(self, filepath):
    def get(self, filepath):
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@abstractmethod
    @abstractmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_text(self, filepath):
    def get_text(self, filepath):
        # 中文说明：执行循环控制或空操作；代码：pass
        pass
