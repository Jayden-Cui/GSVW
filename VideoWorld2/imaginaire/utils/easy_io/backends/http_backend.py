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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import tempfile
import tempfile
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from contextlib import contextmanager
from contextlib import contextmanager
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from pathlib import Path
from pathlib import Path
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Generator, Union
from typing import Generator, Union
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from urllib.request import urlopen
from urllib.request import urlopen

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.backends.base_backend import BaseStorageBackend
from imaginaire.utils.easy_io.backends.base_backend import BaseStorageBackend


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class HTTPBackend(BaseStorageBackend):
class HTTPBackend(BaseStorageBackend):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""HTTP and HTTPS storage bachend."""
    """HTTP and HTTPS storage bachend."""

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get(self, filepath: str) -> bytes:
    def get(self, filepath: str) -> bytes:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Read bytes from a given ``filepath``.
        """Read bytes from a given ``filepath``.

        Args:
            filepath (str): Path to read data.

        Returns:
            bytes: Expected bytes object.

        Examples:
            >>> backend = HTTPBackend()
            >>> backend.get('http://path/of/file')
            b'hello world'
        """
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return urlopen(filepath).read()
        return urlopen(filepath).read()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_text(self, filepath, encoding="utf-8") -> str:
    def get_text(self, filepath, encoding="utf-8") -> str:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Read text from a given ``filepath``.
        """Read text from a given ``filepath``.

        Args:
            filepath (str): Path to read data.
            encoding (str): The encoding format used to open the ``filepath``.
                Defaults to 'utf-8'.

        Returns:
            str: Expected text reading from ``filepath``.

        Examples:
            >>> backend = HTTPBackend()
            >>> backend.get_text('http://path/of/file')
            'hello world'
        """
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return urlopen(filepath).read().decode(encoding)
        return urlopen(filepath).read().decode(encoding)

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@contextmanager
    @contextmanager
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_local_path(self, filepath: str) -> Generator[Union[str, Path], None, None]:
    def get_local_path(self, filepath: str) -> Generator[Union[str, Path], None, None]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Download a file from ``filepath`` to a local temporary directory,
        """Download a file from ``filepath`` to a local temporary directory,
        and return the temporary path.

        ``get_local_path`` is decorated by :meth:`contxtlib.contextmanager`. It
        can be called with ``with`` statement, and when exists from the
        ``with`` statement, the temporary path will be released.

        Args:
            filepath (str): Download a file from ``filepath``.

        Yields:
            Iterable[str]: Only yield one temporary path.

        Examples:
            >>> backend = HTTPBackend()
            >>> # After existing from the ``with`` clause,
            >>> # the path will be removed
            >>> with backend.get_local_path('http://path/of/file') as path:
            ...     # do something here
        """
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：f = tempfile.NamedTemporaryFile(delete=False)
            f = tempfile.NamedTemporaryFile(delete=False)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f.write(self.get(filepath))
            f.write(self.get(filepath))
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f.close()
            f.close()
            # 中文说明：从生成器逐步产生本行指定的值；代码：yield f.name
            yield f.name
        # 中文说明：处理异常、清理资源或管理上下文；代码：finally:
        finally:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.remove(f.name)
            os.remove(f.name)
