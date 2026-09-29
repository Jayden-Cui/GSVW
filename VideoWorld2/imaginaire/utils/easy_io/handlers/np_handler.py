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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from io import BytesIO
from io import BytesIO
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import IO, Any
from typing import IO, Any

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.handlers.base import BaseFileHandler
from imaginaire.utils.easy_io.handlers.base import BaseFileHandler


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class NumpyHandler(BaseFileHandler):
class NumpyHandler(BaseFileHandler):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：str_like = False
    str_like = False

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def load_from_fileobj(self, file: IO[bytes], **kwargs) -> Any:
    def load_from_fileobj(self, file: IO[bytes], **kwargs) -> Any:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Load a NumPy array from a file-like object.

        Parameters:
            file (IO[bytes]): The file-like object containing the NumPy array data.
            **kwargs: Additional keyword arguments passed to `np.load`.

        Returns:
            numpy.ndarray: The loaded NumPy array.
        """
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return np.load(file, **kwargs)
        return np.load(file, **kwargs)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def load_from_path(self, filepath: str, **kwargs) -> Any:
    def load_from_path(self, filepath: str, **kwargs) -> Any:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Load a NumPy array from a file path.

        Parameters:
            filepath (str): The path to the file to load.
            **kwargs: Additional keyword arguments passed to `np.load`.

        Returns:
            numpy.ndarray: The loaded NumPy array.
        """
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return super().load_from_path(filepath, mode="rb", **kwargs)
        return super().load_from_path(filepath, mode="rb", **kwargs)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def dump_to_str(self, obj: np.ndarray, **kwargs) -> str:
    def dump_to_str(self, obj: np.ndarray, **kwargs) -> str:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Serialize a NumPy array to a string in binary format.

        Parameters:
            obj (np.ndarray): The NumPy array to serialize.
            **kwargs: Additional keyword arguments passed to `np.save`.

        Returns:
            str: The serialized NumPy array as a string.
        """
        # 中文说明：处理异常、清理资源或管理上下文；代码：with BytesIO() as f:
        with BytesIO() as f:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：np.save(f, obj, **kwargs)
            np.save(f, obj, **kwargs)
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return f.getvalue()
            return f.getvalue()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def dump_to_fileobj(self, obj: np.ndarray, file: IO[bytes], **kwargs):
    def dump_to_fileobj(self, obj: np.ndarray, file: IO[bytes], **kwargs):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Dump a NumPy array to a file-like object.

        Parameters:
            obj (np.ndarray): The NumPy array to dump.
            file (IO[bytes]): The file-like object to which the array is dumped.
            **kwargs: Additional keyword arguments passed to `np.save`.
        """
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：np.save(file, obj, **kwargs)
        np.save(file, obj, **kwargs)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def dump_to_path(self, obj: np.ndarray, filepath: str, **kwargs):
    def dump_to_path(self, obj: np.ndarray, filepath: str, **kwargs):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Dump a NumPy array to a file path.

        Parameters:
            obj (np.ndarray): The NumPy array to dump.
            filepath (str): The file path where the array should be saved.
            **kwargs: Additional keyword arguments passed to `np.save`.
        """
        # 中文说明：处理异常、清理资源或管理上下文；代码：with open(filepath, "wb") as f:
        with open(filepath, "wb") as f:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：np.save(f, obj, **kwargs)
            np.save(f, obj, **kwargs)
