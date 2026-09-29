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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import io
import io
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os.path as osp
import os.path as osp
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import shutil
import shutil
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from contextlib import contextmanager
from contextlib import contextmanager
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from pathlib import Path
from pathlib import Path
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Generator, Iterator, Optional, Tuple, Union
from typing import Generator, Iterator, Optional, Tuple, Union

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.backends.base_backend import BaseStorageBackend, mkdir_or_exist
from imaginaire.utils.easy_io.backends.base_backend import BaseStorageBackend, mkdir_or_exist


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class LocalBackend(BaseStorageBackend):
class LocalBackend(BaseStorageBackend):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Raw local storage backend."""
    """Raw local storage backend."""

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_allow_symlink = True
    _allow_symlink = True

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get(self, filepath: Union[str, Path]) -> bytes:
    def get(self, filepath: Union[str, Path]) -> bytes:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Read bytes from a given ``filepath`` with 'rb' mode.
        """Read bytes from a given ``filepath`` with 'rb' mode.

        Args:
            filepath (str or Path): Path to read data.

        Returns:
            bytes: Expected bytes object.

        Examples:
            >>> backend = LocalBackend()
            >>> filepath = '/path/of/file'
            >>> backend.get(filepath)
            b'hello world'
        """
        # 中文说明：处理异常、清理资源或管理上下文；代码：with open(filepath, "rb") as f:
        with open(filepath, "rb") as f:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：value = f.read()
            value = f.read()
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return value
        return value

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_text(self, filepath: Union[str, Path], encoding: str = "utf-8") -> str:
    def get_text(self, filepath: Union[str, Path], encoding: str = "utf-8") -> str:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Read text from a given ``filepath`` with 'r' mode.
        """Read text from a given ``filepath`` with 'r' mode.

        Args:
            filepath (str or Path): Path to read data.
            encoding (str): The encoding format used to open the ``filepath``.
                Defaults to 'utf-8'.

        Returns:
            str: Expected text reading from ``filepath``.

        Examples:
            >>> backend = LocalBackend()
            >>> filepath = '/path/of/file'
            >>> backend.get_text(filepath)
            'hello world'
        """
        # 中文说明：处理异常、清理资源或管理上下文；代码：with open(filepath, encoding=encoding) as f:
        with open(filepath, encoding=encoding) as f:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text = f.read()
            text = f.read()
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return text
        return text

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def put(self, obj: Union[bytes, io.BytesIO], filepath: Union[str, Path]) -> None:
    def put(self, obj: Union[bytes, io.BytesIO], filepath: Union[str, Path]) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Write bytes to a given ``filepath`` with 'wb' mode.
        """Write bytes to a given ``filepath`` with 'wb' mode.

        Note:
            ``put`` will create a directory if the directory of
            ``filepath`` does not exist.

        Args:
            obj (bytes): Data to be written.
            filepath (str or Path): Path to write data.

        Examples:
            >>> backend = LocalBackend()
            >>> filepath = '/path/of/file'
            >>> backend.put(b'hello world', filepath)
        """
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：mkdir_or_exist(osp.dirname(filepath))
        mkdir_or_exist(osp.dirname(filepath))
        # 中文说明：根据条件选择执行分支；代码：if isinstance(obj, io.BytesIO):
        if isinstance(obj, io.BytesIO):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：obj.seek(0)
            obj.seek(0)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：obj = obj.getvalue()
            obj = obj.getvalue()
        # 中文说明：处理异常、清理资源或管理上下文；代码：with open(filepath, "wb") as f:
        with open(filepath, "wb") as f:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f.write(obj)
            f.write(obj)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def put_text(self, obj: str, filepath: Union[str, Path], encoding: str = "utf-8") -> None:
    def put_text(self, obj: str, filepath: Union[str, Path], encoding: str = "utf-8") -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Write text to a given ``filepath`` with 'w' mode.
        """Write text to a given ``filepath`` with 'w' mode.

        Note:
            ``put_text`` will create a directory if the directory of
            ``filepath`` does not exist.

        Args:
            obj (str): Data to be written.
            filepath (str or Path): Path to write data.
            encoding (str): The encoding format used to open the ``filepath``.
                Defaults to 'utf-8'.

        Examples:
            >>> backend = LocalBackend()
            >>> filepath = '/path/of/file'
            >>> backend.put_text('hello world', filepath)
        """
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：mkdir_or_exist(osp.dirname(filepath))
        mkdir_or_exist(osp.dirname(filepath))
        # 中文说明：处理异常、清理资源或管理上下文；代码：with open(filepath, "w", encoding=encoding) as f:
        with open(filepath, "w", encoding=encoding) as f:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f.write(obj)
            f.write(obj)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def exists(self, filepath: Union[str, Path]) -> bool:
    def exists(self, filepath: Union[str, Path]) -> bool:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Check whether a file path exists.
        """Check whether a file path exists.

        Args:
            filepath (str or Path): Path to be checked whether exists.

        Returns:
            bool: Return ``True`` if ``filepath`` exists, ``False`` otherwise.

        Examples:
            >>> backend = LocalBackend()
            >>> filepath = '/path/of/file'
            >>> backend.exists(filepath)
            True
        """
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return osp.exists(filepath)
        return osp.exists(filepath)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def isdir(self, filepath: Union[str, Path]) -> bool:
    def isdir(self, filepath: Union[str, Path]) -> bool:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Check whether a file path is a directory.
        """Check whether a file path is a directory.

        Args:
            filepath (str or Path): Path to be checked whether it is a
                directory.

        Returns:
            bool: Return ``True`` if ``filepath`` points to a directory,
            ``False`` otherwise.

        Examples:
            >>> backend = LocalBackend()
            >>> filepath = '/path/of/dir'
            >>> backend.isdir(filepath)
            True
        """
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return osp.isdir(filepath)
        return osp.isdir(filepath)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def isfile(self, filepath: Union[str, Path]) -> bool:
    def isfile(self, filepath: Union[str, Path]) -> bool:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Check whether a file path is a file.
        """Check whether a file path is a file.

        Args:
            filepath (str or Path): Path to be checked whether it is a file.

        Returns:
            bool: Return ``True`` if ``filepath`` points to a file, ``False``
            otherwise.

        Examples:
            >>> backend = LocalBackend()
            >>> filepath = '/path/of/file'
            >>> backend.isfile(filepath)
            True
        """
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return osp.isfile(filepath)
        return osp.isfile(filepath)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def join_path(self, filepath: Union[str, Path], *filepaths: Union[str, Path]) -> str:
    def join_path(self, filepath: Union[str, Path], *filepaths: Union[str, Path]) -> str:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Concatenate all file paths.
        r"""Concatenate all file paths.

        Join one or more filepath components intelligently. The return value
        is the concatenation of filepath and any members of \*filepaths.

        Args:
            filepath (str or Path): Path to be concatenated.

        Returns:
            str: The result of concatenation.

        Examples:
            >>> backend = LocalBackend()
            >>> filepath1 = '/path/of/dir1'
            >>> filepath2 = 'dir2'
            >>> filepath3 = 'path/of/file'
            >>> backend.join_path(filepath1, filepath2, filepath3)
            '/path/of/dir/dir2/path/of/file'
        """
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return osp.join(filepath, *filepaths)
        return osp.join(filepath, *filepaths)

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@contextmanager
    @contextmanager
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_local_path(self, filepath: str) -> Generator[str, None, None]:
    def get_local_path(self, filepath: str) -> Generator[str, None, None]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Download data from filepath to local path with a context manager.
        """Download data from filepath to local path with a context manager.

        If filepath exists in localhost, it just return filepath.
        If filepath doesn't exist in localhost, it will download the data
        to local path, and return the path, then the path will be removed
        after existing from the with statement.

        Args:
            filepath (str): Path to be read data.

        Yields:
            str: Local path.

        Examples:
            >>> with backend.get_local_path('http://example.com/abc.jpg') as path:
            ...     # do something here
        """
        # 中文说明：从生成器逐步产生本行指定的值；代码：yield filepath
        yield filepath

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def copyfile(
    def copyfile(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：src: Union[str, Path],
        src: Union[str, Path],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dst: Union[str, Path],
        dst: Union[str, Path],
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> str:
    ) -> str:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Copy a file src to dst and return the destination file.
        """Copy a file src to dst and return the destination file.

        src and dst should have the same prefix. If dst specifies a directory,
        the file will be copied into dst using the base filename from src. If
        dst specifies a file that already exists, it will be replaced.

        Args:
            src (str or Path): A file to be copied.
            dst (str or Path): Copy file to dst.

        Returns:
            str: The destination file.

        Raises:
            SameFileError: If src and dst are the same file, a SameFileError
                will be raised.

        Examples:
            >>> backend = LocalBackend()
            >>> # dst is a file
            >>> src = '/path/of/file'
            >>> dst = '/path1/of/file1'
            >>> # src will be copied to '/path1/of/file1'
            >>> backend.copyfile(src, dst)
            '/path1/of/file1'

            >>> # dst is a directory
            >>> dst = '/path1/of/dir'
            >>> # src will be copied to '/path1/of/dir/file'
            >>> backend.copyfile(src, dst)
            '/path1/of/dir/file'
        """
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return shutil.copy(src, dst)
        return shutil.copy(src, dst)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def copytree(
    def copytree(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：src: Union[str, Path],
        src: Union[str, Path],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dst: Union[str, Path],
        dst: Union[str, Path],
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> str:
    ) -> str:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Recursively copy an entire directory tree rooted at src to a
        """Recursively copy an entire directory tree rooted at src to a
        directory named dst and return the destination directory.

        src and dst should have the same prefix and dst must not already exist.

        Args:
            src (str or Path): A directory to be copied.
            dst (str or Path): Copy directory to dst.

        Returns:
            str: The destination directory.

        Raises:
            FileExistsError: If dst had already existed, a FileExistsError will
                be raised.

        Examples:
            >>> backend = LocalBackend()
            >>> src = '/path/of/dir1'
            >>> dst = '/path/of/dir2'
            >>> backend.copytree(src, dst)
            '/path/of/dir2'
        """
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return shutil.copytree(src, dst)
        return shutil.copytree(src, dst)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def copyfile_from_local(
    def copyfile_from_local(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：src: Union[str, Path],
        src: Union[str, Path],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dst: Union[str, Path],
        dst: Union[str, Path],
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> str:
    ) -> str:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Copy a local file src to dst and return the destination file. Same
        """Copy a local file src to dst and return the destination file. Same
        as :meth:`copyfile`.

        Args:
            src (str or Path): A local file to be copied.
            dst (str or Path): Copy file to dst.

        Returns:
            str: If dst specifies a directory, the file will be copied into dst
            using the base filename from src.

        Raises:
            SameFileError: If src and dst are the same file, a SameFileError
                will be raised.

        Examples:
            >>> backend = LocalBackend()
            >>> # dst is a file
            >>> src = '/path/of/file'
            >>> dst = '/path1/of/file1'
            >>> # src will be copied to '/path1/of/file1'
            >>> backend.copyfile_from_local(src, dst)
            '/path1/of/file1'

            >>> # dst is a directory
            >>> dst = '/path1/of/dir'
            >>> # src will be copied to
            >>> backend.copyfile_from_local(src, dst)
            '/path1/of/dir/file'
        """
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.copyfile(src, dst)
        return self.copyfile(src, dst)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def copytree_from_local(
    def copytree_from_local(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：src: Union[str, Path],
        src: Union[str, Path],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dst: Union[str, Path],
        dst: Union[str, Path],
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> str:
    ) -> str:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Recursively copy an entire directory tree rooted at src to a
        """Recursively copy an entire directory tree rooted at src to a
        directory named dst and return the destination directory. Same as
        :meth:`copytree`.

        Args:
            src (str or Path): A local directory to be copied.
            dst (str or Path): Copy directory to dst.

        Returns:
            str: The destination directory.

        Examples:
            >>> backend = LocalBackend()
            >>> src = '/path/of/dir1'
            >>> dst = '/path/of/dir2'
            >>> backend.copytree_from_local(src, dst)
            '/path/of/dir2'
        """
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.copytree(src, dst)
        return self.copytree(src, dst)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def copyfile_to_local(
    def copyfile_to_local(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：src: Union[str, Path],
        src: Union[str, Path],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dst: Union[str, Path],
        dst: Union[str, Path],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dst_type: Optional[str] = None,
        dst_type: Optional[str] = None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> str:
    ) -> str:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Copy the file src to local dst and return the destination file. Same
        """Copy the file src to local dst and return the destination file. Same
        as :meth:`copyfile`.

        If dst specifies a directory, the file will be copied into dst using
        the base filename from src. If dst specifies a file that already
        exists, it will be replaced.

        Args:
            src (str or Path): A file to be copied.
            dst (str or Path): Copy file to to local dst.

        Returns:
            str: If dst specifies a directory, the file will be copied into dst
            using the base filename from src.

        Examples:
            >>> backend = LocalBackend()
            >>> # dst is a file
            >>> src = '/path/of/file'
            >>> dst = '/path1/of/file1'
            >>> # src will be copied to '/path1/of/file1'
            >>> backend.copyfile_to_local(src, dst)
            '/path1/of/file1'

            >>> # dst is a directory
            >>> dst = '/path1/of/dir'
            >>> # src will be copied to
            >>> backend.copyfile_to_local(src, dst)
            '/path1/of/dir/file'
        """
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.copyfile(src, dst)
        return self.copyfile(src, dst)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def copytree_to_local(
    def copytree_to_local(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：src: Union[str, Path],
        src: Union[str, Path],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dst: Union[str, Path],
        dst: Union[str, Path],
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> str:
    ) -> str:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Recursively copy an entire directory tree rooted at src to a local
        """Recursively copy an entire directory tree rooted at src to a local
        directory named dst and return the destination directory.

        Args:
            src (str or Path): A directory to be copied.
            dst (str or Path): Copy directory to local dst.
            backend_args (dict, optional): Arguments to instantiate the
                prefix of uri corresponding backend. Defaults to None.

        Returns:
            str: The destination directory.

        Examples:
            >>> backend = LocalBackend()
            >>> src = '/path/of/dir1'
            >>> dst = '/path/of/dir2'
            >>> backend.copytree_from_local(src, dst)
            '/path/of/dir2'
        """
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.copytree(src, dst)
        return self.copytree(src, dst)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def remove(self, filepath: Union[str, Path]) -> None:
    def remove(self, filepath: Union[str, Path]) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Remove a file.
        """Remove a file.

        Args:
            filepath (str or Path): Path to be removed.

        Raises:
            IsADirectoryError: If filepath is a directory, an IsADirectoryError
                will be raised.
            FileNotFoundError: If filepath does not exist, an FileNotFoundError
                will be raised.

        Examples:
            >>> backend = LocalBackend()
            >>> filepath = '/path/of/file'
            >>> backend.remove(filepath)
        """
        # 中文说明：根据条件选择执行分支；代码：if not self.exists(filepath):
        if not self.exists(filepath):
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise FileNotFoundError(f"filepath {filepath} does not exist")
            raise FileNotFoundError(f"filepath {filepath} does not exist")

        # 中文说明：根据条件选择执行分支；代码：if self.isdir(filepath):
        if self.isdir(filepath):
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise IsADirectoryError("filepath should be a file")
            raise IsADirectoryError("filepath should be a file")

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.remove(filepath)
        os.remove(filepath)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def rmtree(self, dir_path: Union[str, Path]) -> None:
    def rmtree(self, dir_path: Union[str, Path]) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Recursively delete a directory tree.
        """Recursively delete a directory tree.

        Args:
            dir_path (str or Path): A directory to be removed.

        Examples:
            >>> dir_path = '/path/of/dir'
            >>> backend.rmtree(dir_path)
        """
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：shutil.rmtree(dir_path)
        shutil.rmtree(dir_path)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def copy_if_symlink_fails(
    def copy_if_symlink_fails(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：src: Union[str, Path],
        src: Union[str, Path],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dst: Union[str, Path],
        dst: Union[str, Path],
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> bool:
    ) -> bool:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Create a symbolic link pointing to src named dst.
        """Create a symbolic link pointing to src named dst.

        If failed to create a symbolic link pointing to src, directly copy src
        to dst instead.

        Args:
            src (str or Path): Create a symbolic link pointing to src.
            dst (str or Path): Create a symbolic link named dst.

        Returns:
            bool: Return True if successfully create a symbolic link pointing
            to src. Otherwise, return False.

        Examples:
            >>> backend = LocalBackend()
            >>> src = '/path/of/file'
            >>> dst = '/path1/of/file1'
            >>> backend.copy_if_symlink_fails(src, dst)
            True
            >>> src = '/path/of/dir'
            >>> dst = '/path1/of/dir1'
            >>> backend.copy_if_symlink_fails(src, dst)
            True
        """
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.symlink(src, dst)
            os.symlink(src, dst)
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return True
            return True
        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception:
        except Exception:
            # 中文说明：根据条件选择执行分支；代码：if self.isfile(src):
            if self.isfile(src):
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.copyfile(src, dst)
                self.copyfile(src, dst)
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.copytree(src, dst)
                self.copytree(src, dst)
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return False
            return False

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def list_dir_or_file(
    def list_dir_or_file(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dir_path: Union[str, Path],
        dir_path: Union[str, Path],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：list_dir: bool = True,
        list_dir: bool = True,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：list_file: bool = True,
        list_file: bool = True,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：suffix: Optional[Union[str, Tuple[str]]] = None,
        suffix: Optional[Union[str, Tuple[str]]] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：recursive: bool = False,
        recursive: bool = False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Iterator[str]:
    ) -> Iterator[str]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Scan a directory to find the interested directories or files in
        """Scan a directory to find the interested directories or files in
        arbitrary order.

        Note:
            :meth:`list_dir_or_file` returns the path relative to ``dir_path``.

        Args:
            dir_path (str or Path): Path of the directory.
            list_dir (bool): List the directories. Defaults to True.
            list_file (bool): List the path of files. Defaults to True.
            suffix (str or tuple[str], optional): File suffix that we are
                interested in. Defaults to None.
            recursive (bool): If set to True, recursively scan the directory.
                Defaults to False.

        Yields:
            Iterable[str]: A relative path to ``dir_path``.

        Examples:
            >>> backend = LocalBackend()
            >>> dir_path = '/path/of/dir'
            >>> # list those files and directories in current directory
            >>> for file_path in backend.list_dir_or_file(dir_path):
            ...     print(file_path)
            >>> # only list files
            >>> for file_path in backend.list_dir_or_file(dir_path, list_dir=False):
            ...     print(file_path)
            >>> # only list directories
            >>> for file_path in backend.list_dir_or_file(dir_path, list_file=False):
            ...     print(file_path)
            >>> # only list files ending with specified suffixes
            >>> for file_path in backend.list_dir_or_file(dir_path, suffix='.txt'):
            ...     print(file_path)
            >>> # list all files and directory recursively
            >>> for file_path in backend.list_dir_or_file(dir_path, recursive=True):
            ...     print(file_path)
        """  # noqa: E501
        # 中文说明：根据条件选择执行分支；代码：if list_dir and suffix is not None:
        if list_dir and suffix is not None:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError("`suffix` should be None when `list_dir` is True")
            raise TypeError("`suffix` should be None when `list_dir` is True")

        # 中文说明：根据条件选择执行分支；代码：if (suffix is not None) and not isinstance(suffix, (str, tuple)):
        if (suffix is not None) and not isinstance(suffix, (str, tuple)):
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError("`suffix` must be a string or tuple of strings")
            raise TypeError("`suffix` must be a string or tuple of strings")

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：root = dir_path
        root = dir_path

        # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _list_dir_or_file(dir_path, list_dir, list_file, suffix, recursive):
        def _list_dir_or_file(dir_path, list_dir, list_file, suffix, recursive):
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for entry in os.scandir(dir_path):
            for entry in os.scandir(dir_path):
                # 中文说明：根据条件选择执行分支；代码：if not entry.name.startswith(".") and entry.is_file():
                if not entry.name.startswith(".") and entry.is_file():
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rel_path = osp.relpath(entry.path, root)
                    rel_path = osp.relpath(entry.path, root)
                    # 中文说明：根据条件选择执行分支；代码：if (suffix is None or rel_path.endswith(suffix)) and list_file:
                    if (suffix is None or rel_path.endswith(suffix)) and list_file:
                        # 中文说明：从生成器逐步产生本行指定的值；代码：yield rel_path
                        yield rel_path
                # 中文说明：根据条件选择执行分支；代码：elif osp.isdir(entry.path):
                elif osp.isdir(entry.path):
                    # 中文说明：根据条件选择执行分支；代码：if list_dir:
                    if list_dir:
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rel_dir = osp.relpath(entry.path, root)
                        rel_dir = osp.relpath(entry.path, root)
                        # 中文说明：从生成器逐步产生本行指定的值；代码：yield rel_dir
                        yield rel_dir
                    # 中文说明：根据条件选择执行分支；代码：if recursive:
                    if recursive:
                        # 中文说明：从生成器逐步产生本行指定的值；代码：yield from _list_dir_or_file(entry.path, list_dir, list_file, suffix, recursive)
                        yield from _list_dir_or_file(entry.path, list_dir, list_file, suffix, recursive)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return _list_dir_or_file(dir_path, list_dir, list_file, suffix, recursive)
        return _list_dir_or_file(dir_path, list_dir, list_file, suffix, recursive)
