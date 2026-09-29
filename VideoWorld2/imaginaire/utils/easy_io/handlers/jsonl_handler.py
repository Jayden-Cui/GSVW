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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import json
import json
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import IO
from typing import IO

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.handlers.base import BaseFileHandler
from imaginaire.utils.easy_io.handlers.base import BaseFileHandler


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def set_default(obj):
def set_default(obj):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Set default json values for non-serializable values.
    """Set default json values for non-serializable values.

    It helps convert ``set``, ``range`` and ``np.ndarray`` data types to list.
    It also converts ``np.generic`` (including ``np.int32``, ``np.float32``,
    etc.) into plain numbers of plain python built-in types.
    """
    # 中文说明：根据条件选择执行分支；代码：if isinstance(obj, (set, range)):
    if isinstance(obj, (set, range)):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return list(obj)
        return list(obj)
    # 中文说明：根据条件选择执行分支；代码：elif isinstance(obj, np.ndarray):
    elif isinstance(obj, np.ndarray):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return obj.tolist()
        return obj.tolist()
    # 中文说明：根据条件选择执行分支；代码：elif isinstance(obj, np.generic):
    elif isinstance(obj, np.generic):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return obj.item()
        return obj.item()
    # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError(f"{type(obj)} is unsupported for json dump")
    raise TypeError(f"{type(obj)} is unsupported for json dump")


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class JsonlHandler(BaseFileHandler):
class JsonlHandler(BaseFileHandler):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Handler for JSON lines (JSONL) files."""
    """Handler for JSON lines (JSONL) files."""

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def load_from_fileobj(self, file: IO[bytes]):
    def load_from_fileobj(self, file: IO[bytes]):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Load JSON objects from a newline-delimited JSON (JSONL) file object.
        """Load JSON objects from a newline-delimited JSON (JSONL) file object.

        Returns:
            A list of Python objects loaded from each JSON line.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data = []
        data = []
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for line in file:
        for line in file:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：line = line.strip()
            line = line.strip()
            # 中文说明：根据条件选择执行分支；代码：if not line:
            if not line:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：continue # skip empty lines if any
                continue  # skip empty lines if any
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data.append(json.loads(line))
            data.append(json.loads(line))
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return data
        return data

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def dump_to_fileobj(self, obj: IO[bytes], file, **kwargs):
    def dump_to_fileobj(self, obj: IO[bytes], file, **kwargs):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Dump a list of objects to a newline-delimited JSON (JSONL) file object.
        """Dump a list of objects to a newline-delimited JSON (JSONL) file object.

        Args:
            obj: A list (or iterable) of objects to dump line by line.
        """
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：kwargs.setdefault("default", set_default)
        kwargs.setdefault("default", set_default)
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for item in obj:
        for item in obj:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：file.write(json.dumps(item, **kwargs) + "\n")
            file.write(json.dumps(item, **kwargs) + "\n")

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def dump_to_str(self, obj, **kwargs):
    def dump_to_str(self, obj, **kwargs):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Dump a list of objects to a newline-delimited JSON (JSONL) string."""
        """Dump a list of objects to a newline-delimited JSON (JSONL) string."""
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：kwargs.setdefault("default", set_default)
        kwargs.setdefault("default", set_default)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lines = [json.dumps(item, **kwargs) for item in obj]
        lines = [json.dumps(item, **kwargs) for item in obj]
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return "\n".join(lines)
        return "\n".join(lines)


# 中文说明：根据条件选择执行分支；代码：if __name__ == "__main__":
if __name__ == "__main__":
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io import easy_io
    from imaginaire.utils.easy_io import easy_io

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：easy_io.dump([1, 2, 3], "test.jsonl", file_format="jsonl")
    easy_io.dump([1, 2, 3], "test.jsonl", file_format="jsonl")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(easy_io.load("test.jsonl"))
    print(easy_io.load("test.jsonl"))
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：easy_io.dump([{"key1": 1, "key2": 2}, {"key1": 3, "key2": 4}], "test.jsonl", file_format="jso...
    easy_io.dump([{"key1": 1, "key2": 2}, {"key1": 3, "key2": 4}], "test.jsonl", file_format="jsonl")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(easy_io.load("test.jsonl"))
    print(easy_io.load("test.jsonl"))
