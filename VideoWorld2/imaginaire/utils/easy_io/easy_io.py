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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import warnings
import warnings
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from contextlib import contextmanager
from contextlib import contextmanager
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from io import BytesIO, StringIO
from io import BytesIO, StringIO
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from pathlib import Path
from pathlib import Path
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import IO, Any, Generator, Iterator, Optional, Tuple, Union
from typing import IO, Any, Generator, Iterator, Optional, Tuple, Union

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.backends import backends, prefix_to_backends
from imaginaire.utils.easy_io.backends import backends, prefix_to_backends
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.file_client import FileClient
from imaginaire.utils.easy_io.file_client import FileClient
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.handlers import file_handlers
from imaginaire.utils.easy_io.handlers import file_handlers

# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_instances: dict = {}
backend_instances: dict = {}


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_filepath(filepath):
def is_filepath(filepath):
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return isinstance(filepath, (str, Path))
    return isinstance(filepath, (str, Path))


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _parse_uri_prefix(uri: Union[str, Path]) -> str:
def _parse_uri_prefix(uri: Union[str, Path]) -> str:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Parse the prefix of uri.
    """Parse the prefix of uri.

    Args:
        uri (str or Path): Uri to be parsed that contains the file prefix.

    Examples:
        >>> _parse_uri_prefix('/home/path/of/your/file')
        ''
        >>> _parse_uri_prefix('http://path/of/your/file')
        'http'

    Returns:
        str: Return the prefix of uri if the uri contains '://'. Otherwise,
        return ''.
    """
    # 中文说明：检查运行时假设是否成立；代码：assert is_filepath(uri)
    assert is_filepath(uri)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：uri = str(uri)
    uri = str(uri)
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# if uri does not contains '://', the uri will be handled by
    # if uri does not contains '://', the uri will be handled by
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# LocalBackend by default
    # LocalBackend by default
    # 中文说明：根据条件选择执行分支；代码：if "://" not in uri:
    if "://" not in uri:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return ""
        return ""
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：prefix, _ = uri.split("://")
        prefix, _ = uri.split("://")
        # 中文说明：根据条件选择执行分支；代码：if ":" in prefix:
        if ":" in prefix:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_, prefix = prefix.split(":")
            _, prefix = prefix.split(":")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return prefix
        return prefix


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _get_file_backend(prefix: str, backend_args: dict):
def _get_file_backend(prefix: str, backend_args: dict):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Return a file backend based on the prefix or backend_args.
    """Return a file backend based on the prefix or backend_args.

    Args:
        prefix (str): Prefix of uri.
        backend_args (dict): Arguments to instantiate the corresponding
            backend.
    """
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# backend name has a higher priority
    # backend name has a higher priority
    # 中文说明：根据条件选择执行分支；代码：if "backend" in backend_args:
    if "backend" in backend_args:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# backend_args should not be modified
        # backend_args should not be modified
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_args_bak = backend_args.copy()
        backend_args_bak = backend_args.copy()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_name = backend_args_bak.pop("backend")
        backend_name = backend_args_bak.pop("backend")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend = backends[backend_name](**backend_args_bak)
        backend = backends[backend_name](**backend_args_bak)
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend = prefix_to_backends[prefix](**backend_args)
        backend = prefix_to_backends[prefix](**backend_args)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return backend
    return backend


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_file_backend(
def get_file_backend(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：uri: Union[str, Path, None] = None,
    uri: Union[str, Path, None] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：*,
    *,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_args: Optional[dict] = None,
    backend_args: Optional[dict] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：enable_singleton: bool = False,
    enable_singleton: bool = False,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_key: Optional[str] = None,
    backend_key: Optional[str] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Return a file backend based on the prefix of uri or backend_args.
    """Return a file backend based on the prefix of uri or backend_args.

    Args:
        uri (str or Path): Uri to be parsed that contains the file prefix.
        backend_args (dict, optional): Arguments to instantiate the
            corresponding backend. Defaults to None.
        enable_singleton (bool): Whether to enable the singleton pattern.
            If it is True, the backend created will be reused if the
            signature is same with the previous one. Defaults to False.
        backend_key: str: The key to register the backend. Defaults to None.

    Returns:
        BaseStorageBackend: Instantiated Backend object.

    Examples:
        >>> # get file backend based on the prefix of uri
        >>> uri = 'http://path/of/your/file'
        >>> backend = get_file_backend(uri)
        >>> # get file backend based on the backend_args
        >>> backend = get_file_backend(backend_args={'backend': 'http'})
        >>> # backend name has a higher priority if 'backend' in backend_args
        >>> backend = get_file_backend(uri, backend_args={'backend': 'http'})
    """
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：global backend_instances
    global backend_instances
    # 中文说明：根据条件选择执行分支；代码：if backend_key is not None:
    if backend_key is not None:
        # 中文说明：根据条件选择执行分支；代码：if backend_key in backend_instances:
        if backend_key in backend_instances:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return backend_instances[backend_key]
            return backend_instances[backend_key]

    # 中文说明：根据条件选择执行分支；代码：if backend_args is None:
    if backend_args is None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_args = {}
        backend_args = {}

    # 中文说明：根据条件选择执行分支；代码：if uri is None and "backend" not in backend_args and backend_key is None:
    if uri is None and "backend" not in backend_args and backend_key is None:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(
        raise ValueError(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：'uri should not be None when "backend" does not exist in ' "backend_args and backend_key is N...
            'uri should not be None when "backend" does not exist in ' "backend_args and backend_key is None"
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：根据条件选择执行分支；代码：if uri is not None:
    if uri is not None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prefix = _parse_uri_prefix(uri)
        prefix = _parse_uri_prefix(uri)
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prefix = ""
        prefix = ""

    # 中文说明：根据条件选择执行分支；代码：if enable_singleton:
    if enable_singleton:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：unique_key = f"{prefix}:{json.dumps(backend_args)}"
        unique_key = f"{prefix}:{json.dumps(backend_args)}"
        # 中文说明：根据条件选择执行分支；代码：if unique_key in backend_instances:
        if unique_key in backend_instances:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return backend_instances[unique_key]
            return backend_instances[unique_key]

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend = _get_file_backend(prefix, backend_args)
        backend = _get_file_backend(prefix, backend_args)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_instances[unique_key] = backend
        backend_instances[unique_key] = backend
        # 中文说明：根据条件选择执行分支；代码：if backend_key is not None:
        if backend_key is not None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_instances[backend_key] = backend
            backend_instances[backend_key] = backend
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return backend
        return backend
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend = _get_file_backend(prefix, backend_args)
        backend = _get_file_backend(prefix, backend_args)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return backend
        return backend


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get(
def get(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：filepath: Union[str, Path],
    filepath: Union[str, Path],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_args: Optional[dict] = None,
    backend_args: Optional[dict] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_key: Optional[str] = None,
    backend_key: Optional[str] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> bytes:
) -> bytes:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Read bytes from a given ``filepath`` with 'rb' mode.
    """Read bytes from a given ``filepath`` with 'rb' mode.

    Args:
        filepath (str or Path): Path to read data.
        backend_args (dict, optional): Arguments to instantiate the
            corresponding backend. Defaults to None.
        backend_key (str, optional): The key to get the backend from register.

    Returns:
        bytes: Expected bytes object.

    Examples:
        >>> filepath = '/path/of/file'
        >>> get(filepath)
        b'hello world'
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend = get_file_backend(
    backend = get_file_backend(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：filepath,
        filepath,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_args=backend_args,
        backend_args=backend_args,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enable_singleton=True,
        enable_singleton=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_key=backend_key,
        backend_key=backend_key,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return backend.get(filepath)
    return backend.get(filepath)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_text(
def get_text(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：filepath: Union[str, Path],
    filepath: Union[str, Path],
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：encoding="utf-8",
    encoding="utf-8",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_args: Optional[dict] = None,
    backend_args: Optional[dict] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_key: Optional[str] = None,
    backend_key: Optional[str] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> str:
) -> str:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Read text from a given ``filepath`` with 'r' mode.
    """Read text from a given ``filepath`` with 'r' mode.

    Args:
        filepath (str or Path): Path to read data.
        encoding (str): The encoding format used to open the ``filepath``.
            Defaults to 'utf-8'.
        backend_args (dict, optional): Arguments to instantiate the
            corresponding backend. Defaults to None.
        backend_key (str, optional): The key to get the backend from register.

    Returns:
        str: Expected text reading from ``filepath``.

    Examples:
        >>> filepath = '/path/of/file'
        >>> get_text(filepath)
        'hello world'
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend = get_file_backend(
    backend = get_file_backend(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：filepath,
        filepath,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_args=backend_args,
        backend_args=backend_args,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enable_singleton=True,
        enable_singleton=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_key=backend_key,
        backend_key=backend_key,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return backend.get_text(filepath, encoding)
    return backend.get_text(filepath, encoding)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def put(
def put(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：obj: bytes,
    obj: bytes,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：filepath: Union[str, Path],
    filepath: Union[str, Path],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_args: Optional[dict] = None,
    backend_args: Optional[dict] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_key: Optional[str] = None,
    backend_key: Optional[str] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
) -> None:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Write bytes to a given ``filepath`` with 'wb' mode.
    """Write bytes to a given ``filepath`` with 'wb' mode.

    Note:
        ``put`` should create a directory if the directory of
        ``filepath`` does not exist.

    Args:
        obj (bytes): Data to be written.
        filepath (str or Path): Path to write data.
        backend_args (dict, optional): Arguments to instantiate the
            corresponding backend. Defaults to None.
        backend_key (str, optional): The key to get the backend from register.

    Examples:
        >>> filepath = '/path/of/file'
        >>> put(b'hello world', filepath)
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend = get_file_backend(
    backend = get_file_backend(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：filepath,
        filepath,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_args=backend_args,
        backend_args=backend_args,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enable_singleton=True,
        enable_singleton=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_key=backend_key,
        backend_key=backend_key,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend.put(obj, filepath)
    backend.put(obj, filepath)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def put_text(
def put_text(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：obj: str,
    obj: str,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：filepath: Union[str, Path],
    filepath: Union[str, Path],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_args: Optional[dict] = None,
    backend_args: Optional[dict] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_key: Optional[str] = None,
    backend_key: Optional[str] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
) -> None:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Write text to a given ``filepath`` with 'w' mode.
    """Write text to a given ``filepath`` with 'w' mode.

    Note:
        ``put_text`` should create a directory if the directory of
        ``filepath`` does not exist.

    Args:
        obj (str): Data to be written.
        filepath (str or Path): Path to write data.
        encoding (str, optional): The encoding format used to open the
            ``filepath``. Defaults to 'utf-8'.
        backend_args (dict, optional): Arguments to instantiate the
            corresponding backend. Defaults to None.
        backend_key (str, optional): The key to get the backend from register.

    Examples:
        >>> filepath = '/path/of/file'
        >>> put_text('hello world', filepath)
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend = get_file_backend(
    backend = get_file_backend(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：filepath,
        filepath,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_args=backend_args,
        backend_args=backend_args,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enable_singleton=True,
        enable_singleton=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_key=backend_key,
        backend_key=backend_key,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend.put_text(obj, filepath)
    backend.put_text(obj, filepath)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def exists(
def exists(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：filepath: Union[str, Path],
    filepath: Union[str, Path],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_args: Optional[dict] = None,
    backend_args: Optional[dict] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_key: Optional[str] = None,
    backend_key: Optional[str] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> bool:
) -> bool:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Check whether a file path exists.
    """Check whether a file path exists.

    Args:
        filepath (str or Path): Path to be checked whether exists.
        backend_args (dict, optional): Arguments to instantiate the
            corresponding backend. Defaults to None.
        backend_key (str, optional): The key to get the backend from register.

    Returns:
        bool: Return ``True`` if ``filepath`` exists, ``False`` otherwise.

    Examples:
        >>> filepath = '/path/of/file'
        >>> exists(filepath)
        True
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend = get_file_backend(
    backend = get_file_backend(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：filepath,
        filepath,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_args=backend_args,
        backend_args=backend_args,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enable_singleton=True,
        enable_singleton=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_key=backend_key,
        backend_key=backend_key,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return backend.exists(filepath)
    return backend.exists(filepath)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def isdir(
def isdir(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：filepath: Union[str, Path],
    filepath: Union[str, Path],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_args: Optional[dict] = None,
    backend_args: Optional[dict] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_key: Optional[str] = None,
    backend_key: Optional[str] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> bool:
) -> bool:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Check whether a file path is a directory.
    """Check whether a file path is a directory.

    Args:
        filepath (str or Path): Path to be checked whether it is a
            directory.
        backend_args (dict, optional): Arguments to instantiate the
            corresponding backend. Defaults to None.
        backend_key (str, optional): The key to get the backend from register.

    Returns:
        bool: Return ``True`` if ``filepath`` points to a directory,
        ``False`` otherwise.

    Examples:
        >>> filepath = '/path/of/dir'
        >>> isdir(filepath)
        True
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend = get_file_backend(
    backend = get_file_backend(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：filepath,
        filepath,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_args=backend_args,
        backend_args=backend_args,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enable_singleton=True,
        enable_singleton=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_key=backend_key,
        backend_key=backend_key,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return backend.isdir(filepath)
    return backend.isdir(filepath)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def isfile(
def isfile(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：filepath: Union[str, Path],
    filepath: Union[str, Path],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_args: Optional[dict] = None,
    backend_args: Optional[dict] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_key: Optional[str] = None,
    backend_key: Optional[str] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> bool:
) -> bool:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Check whether a file path is a file.
    """Check whether a file path is a file.

    Args:
        filepath (str or Path): Path to be checked whether it is a file.
        backend_args (dict, optional): Arguments to instantiate the
            corresponding backend. Defaults to None.
        backend_key (str, optional): The key to get the backend from register.

    Returns:
        bool: Return ``True`` if ``filepath`` points to a file, ``False``
        otherwise.

    Examples:
        >>> filepath = '/path/of/file'
        >>> isfile(filepath)
        True
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend = get_file_backend(
    backend = get_file_backend(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：filepath,
        filepath,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_args=backend_args,
        backend_args=backend_args,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enable_singleton=True,
        enable_singleton=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_key=backend_key,
        backend_key=backend_key,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return backend.isfile(filepath)
    return backend.isfile(filepath)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def join_path(
def join_path(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：filepath: Union[str, Path],
    filepath: Union[str, Path],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：*filepaths: Union[str, Path],
    *filepaths: Union[str, Path],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_args: Optional[dict] = None,
    backend_args: Optional[dict] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_key: Optional[str] = None,
    backend_key: Optional[str] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Union[str, Path]:
) -> Union[str, Path]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Concatenate all file paths.
    r"""Concatenate all file paths.

    Join one or more filepath components intelligently. The return value
    is the concatenation of filepath and any members of \*filepaths.

    Args:
        filepath (str or Path): Path to be concatenated.
        *filepaths (str or Path): Other paths to be concatenated.
        backend_args (dict, optional): Arguments to instantiate the
            corresponding backend. Defaults to None.
        backend_key (str, optional): The key to get the backend from register.

    Returns:
        str: The result of concatenation.

    Examples:
        >>> filepath1 = '/path/of/dir1'
        >>> filepath2 = 'dir2'
        >>> filepath3 = 'path/of/file'
        >>> join_path(filepath1, filepath2, filepath3)
        '/path/of/dir/dir2/path/of/file'
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend = get_file_backend(
    backend = get_file_backend(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：filepath,
        filepath,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_args=backend_args,
        backend_args=backend_args,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enable_singleton=True,
        enable_singleton=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_key=backend_key,
        backend_key=backend_key,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return backend.join_path(filepath, *filepaths)
    return backend.join_path(filepath, *filepaths)


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@contextmanager
@contextmanager
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_local_path(
def get_local_path(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：filepath: Union[str, Path],
    filepath: Union[str, Path],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_args: Optional[dict] = None,
    backend_args: Optional[dict] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_key: Optional[str] = None,
    backend_key: Optional[str] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Generator[Union[str, Path], None, None]:
) -> Generator[Union[str, Path], None, None]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Download data from ``filepath`` and write the data to local path.
    """Download data from ``filepath`` and write the data to local path.

    ``get_local_path`` is decorated by :meth:`contxtlib.contextmanager`. It
    can be called with ``with`` statement, and when exists from the
    ``with`` statement, the temporary path will be released.

    Note:
        If the ``filepath`` is a local path, just return itself and it will
        not be released (removed).

    Args:
        filepath (str or Path): Path to be read data.
        backend_args (dict, optional): Arguments to instantiate the
            corresponding backend. Defaults to None.

    Yields:
        Iterable[str]: Only yield one path.

    Examples:
        >>> with get_local_path('http://example.com/file.jpg') as path:
        ...     # do something here
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend = get_file_backend(
    backend = get_file_backend(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：filepath,
        filepath,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_args=backend_args,
        backend_args=backend_args,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enable_singleton=True,
        enable_singleton=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_key=backend_key,
        backend_key=backend_key,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：处理异常、清理资源或管理上下文；代码：with backend.get_local_path(str(filepath)) as local_path:
    with backend.get_local_path(str(filepath)) as local_path:
        # 中文说明：从生成器逐步产生本行指定的值；代码：yield local_path
        yield local_path


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def copyfile(
def copyfile(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：src: Union[str, Path],
    src: Union[str, Path],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dst: Union[str, Path],
    dst: Union[str, Path],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_args: Optional[dict] = None,
    backend_args: Optional[dict] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_key: Optional[str] = None,
    backend_key: Optional[str] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Union[str, Path]:
) -> Union[str, Path]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Copy a file src to dst and return the destination file.
    """Copy a file src to dst and return the destination file.

    src and dst should have the same prefix. If dst specifies a directory,
    the file will be copied into dst using the base filename from src. If
    dst specifies a file that already exists, it will be replaced.

    Args:
        src (str or Path): A file to be copied.
        dst (str or Path): Copy file to dst.
        backend_args (dict, optional): Arguments to instantiate the
            corresponding backend. Defaults to None.

    Returns:
        str: The destination file.

    Raises:
        SameFileError: If src and dst are the same file, a SameFileError will
            be raised.

    Examples:
        >>> # dst is a file
        >>> src = '/path/of/file'
        >>> dst = '/path1/of/file1'
        >>> # src will be copied to '/path1/of/file1'
        >>> copyfile(src, dst)
        '/path1/of/file1'

        >>> # dst is a directory
        >>> dst = '/path1/of/dir'
        >>> # src will be copied to '/path1/of/dir/file'
        >>> copyfile(src, dst)
        '/path1/of/dir/file'
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend = get_file_backend(src, backend_args=backend_args, enable_singleton=True, backend_key...
    backend = get_file_backend(src, backend_args=backend_args, enable_singleton=True, backend_key=backend_key)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return backend.copyfile(src, dst)
    return backend.copyfile(src, dst)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def copytree(
def copytree(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：src: Union[str, Path],
    src: Union[str, Path],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dst: Union[str, Path],
    dst: Union[str, Path],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_args: Optional[dict] = None,
    backend_args: Optional[dict] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_key: Optional[str] = None,
    backend_key: Optional[str] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Union[str, Path]:
) -> Union[str, Path]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Recursively copy an entire directory tree rooted at src to a directory
    """Recursively copy an entire directory tree rooted at src to a directory
    named dst and return the destination directory.

    src and dst should have the same prefix and dst must not already exist.

    Args:
        src (str or Path): A directory to be copied.
        dst (str or Path): Copy directory to dst.
        backend_args (dict, optional): Arguments to instantiate the
            corresponding backend. Defaults to None.
        backend_key (str, optional): The key to get the backend from register.

    Returns:
        str: The destination directory.

    Raises:
        FileExistsError: If dst had already existed, a FileExistsError will be
            raised.

    Examples:
        >>> src = '/path/of/dir1'
        >>> dst = '/path/of/dir2'
        >>> copytree(src, dst)
        '/path/of/dir2'
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend = get_file_backend(src, backend_args=backend_args, enable_singleton=True, backend_key...
    backend = get_file_backend(src, backend_args=backend_args, enable_singleton=True, backend_key=backend_key)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return backend.copytree(src, dst)
    return backend.copytree(src, dst)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def copyfile_from_local(
def copyfile_from_local(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：src: Union[str, Path],
    src: Union[str, Path],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dst: Union[str, Path],
    dst: Union[str, Path],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_args: Optional[dict] = None,
    backend_args: Optional[dict] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_key: Optional[str] = None,
    backend_key: Optional[str] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Union[str, Path]:
) -> Union[str, Path]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Copy a local file src to dst and return the destination file.
    """Copy a local file src to dst and return the destination file.

    Note:
        If the backend is the instance of LocalBackend, it does the same
        thing with :func:`copyfile`.

    Args:
        src (str or Path): A local file to be copied.
        dst (str or Path): Copy file to dst.
        backend_args (dict, optional): Arguments to instantiate the
            corresponding backend. Defaults to None.

    Returns:
        str: If dst specifies a directory, the file will be copied into dst
        using the base filename from src.

    Examples:
        >>> # dst is a file
        >>> src = '/path/of/file'
        >>> dst = 'http://example.com/file1'
        >>> # src will be copied to 'http://example.com/file1'
        >>> copyfile_from_local(src, dst)
        http://example.com/file1

        >>> # dst is a directory
        >>> dst = 'http://example.com/dir'
        >>> # src will be copied to 'http://example.com/dir/file''
        >>> copyfile_from_local(src, dst)
        'http://example.com/dir/file'
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend = get_file_backend(dst, backend_args=backend_args, enable_singleton=True, backend_key...
    backend = get_file_backend(dst, backend_args=backend_args, enable_singleton=True, backend_key=backend_key)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return backend.copyfile_from_local(src, dst)
    return backend.copyfile_from_local(src, dst)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def copytree_from_local(
def copytree_from_local(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：src: Union[str, Path],
    src: Union[str, Path],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dst: Union[str, Path],
    dst: Union[str, Path],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_args: Optional[dict] = None,
    backend_args: Optional[dict] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_key: Optional[str] = None,
    backend_key: Optional[str] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Union[str, Path]:
) -> Union[str, Path]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Recursively copy an entire directory tree rooted at src to a directory
    """Recursively copy an entire directory tree rooted at src to a directory
    named dst and return the destination directory.

    Note:
        If the backend is the instance of LocalBackend, it does the same
        thing with :func:`copytree`.

    Args:
        src (str or Path): A local directory to be copied.
        dst (str or Path): Copy directory to dst.
        backend_args (dict, optional): Arguments to instantiate the
            corresponding backend. Defaults to None.

    Returns:
        str: The destination directory.

    Examples:
        >>> src = '/path/of/dir'
        >>> dst = 'http://example.com/dir'
        >>> copyfile_from_local(src, dst)
        'http://example.com/dir'
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend = get_file_backend(dst, backend_args=backend_args, enable_singleton=True, backend_key...
    backend = get_file_backend(dst, backend_args=backend_args, enable_singleton=True, backend_key=backend_key)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return backend.copytree_from_local(src, dst)
    return backend.copytree_from_local(src, dst)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def copyfile_to_local(
def copyfile_to_local(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：src: Union[str, Path],
    src: Union[str, Path],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dst: Union[str, Path],
    dst: Union[str, Path],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dst_type: str, # Choose from ["file", "dir"]
    dst_type: str,  # Choose from ["file", "dir"]
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_args: Optional[dict] = None,
    backend_args: Optional[dict] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_key: Optional[str] = None,
    backend_key: Optional[str] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Union[str, Path]:
) -> Union[str, Path]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Copy the file src to local dst and return the destination file.
    """Copy the file src to local dst and return the destination file.

    If dst specifies a directory, the file will be copied into dst using
    the base filename from src. If dst specifies a file that already
    exists, it will be replaced.

    Note:
        If the backend is the instance of LocalBackend, it does the same
        thing with :func:`copyfile`.

    Args:
        src (str or Path): A file to be copied.
        dst (str or Path): Copy file to to local dst.
        backend_args (dict, optional): Arguments to instantiate the
            corresponding backend. Defaults to None.

    Returns:
        str: If dst specifies a directory, the file will be copied into dst
        using the base filename from src.

    Examples:
        >>> # dst is a file
        >>> src = 'http://example.com/file'
        >>> dst = '/path/of/file'
        >>> # src will be copied to '/path/of/file'
        >>> copyfile_to_local(src, dst)
        '/path/of/file'

        >>> # dst is a directory
        >>> dst = '/path/of/dir'
        >>> # src will be copied to '/path/of/dir/file'
        >>> copyfile_to_local(src, dst)
        '/path/of/dir/file'
    """
    # 中文说明：检查运行时假设是否成立；代码：assert dst_type in ["file", "dir"]
    assert dst_type in ["file", "dir"]
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：Path(dst).parent.mkdir(parents=True, exist_ok=True)
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend = get_file_backend(src, backend_args=backend_args, enable_singleton=True, backend_key...
    backend = get_file_backend(src, backend_args=backend_args, enable_singleton=True, backend_key=backend_key)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return backend.copyfile_to_local(src, dst, dst_type=dst_type)
    return backend.copyfile_to_local(src, dst, dst_type=dst_type)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def copytree_to_local(
def copytree_to_local(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：src: Union[str, Path],
    src: Union[str, Path],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dst: Union[str, Path],
    dst: Union[str, Path],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_args: Optional[dict] = None,
    backend_args: Optional[dict] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_key: Optional[str] = None,
    backend_key: Optional[str] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Union[str, Path]:
) -> Union[str, Path]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Recursively copy an entire directory tree rooted at src to a local
    """Recursively copy an entire directory tree rooted at src to a local
    directory named dst and return the destination directory.

    Note:
        If the backend is the instance of LocalBackend, it does the same
        thing with :func:`copytree`.

    Args:
        src (str or Path): A directory to be copied.
        dst (str or Path): Copy directory to local dst.
        backend_args (dict, optional): Arguments to instantiate the
            corresponding backend. Defaults to None.

    Returns:
        str: The destination directory.

    Examples:
        >>> src = 'http://example.com/dir'
        >>> dst = '/path/of/dir'
        >>> copytree_to_local(src, dst)
        '/path/of/dir'
    """
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：Path(dst).parent.mkdir(parents=True, exist_ok=True)
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend = get_file_backend(dst, backend_args=backend_args, enable_singleton=True, backend_key...
    backend = get_file_backend(dst, backend_args=backend_args, enable_singleton=True, backend_key=backend_key)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return backend.copytree_to_local(src, dst)
    return backend.copytree_to_local(src, dst)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def remove(
def remove(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：filepath: Union[str, Path],
    filepath: Union[str, Path],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_args: Optional[dict] = None,
    backend_args: Optional[dict] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_key: Optional[str] = None,
    backend_key: Optional[str] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
) -> None:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Remove a file.
    """Remove a file.

    Args:
        filepath (str, Path): Path to be removed.
        backend_args (dict, optional): Arguments to instantiate the
            corresponding backend. Defaults to None.

    Raises:
        FileNotFoundError: If filepath does not exist, an FileNotFoundError
            will be raised.
        IsADirectoryError: If filepath is a directory, an IsADirectoryError
            will be raised.

    Examples:
        >>> filepath = '/path/of/file'
        >>> remove(filepath)
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend = get_file_backend(
    backend = get_file_backend(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：filepath,
        filepath,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_args=backend_args,
        backend_args=backend_args,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enable_singleton=True,
        enable_singleton=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_key=backend_key,
        backend_key=backend_key,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend.remove(filepath)
    backend.remove(filepath)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def rmtree(
def rmtree(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dir_path: Union[str, Path],
    dir_path: Union[str, Path],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_args: Optional[dict] = None,
    backend_args: Optional[dict] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_key: Optional[str] = None,
    backend_key: Optional[str] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
) -> None:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Recursively delete a directory tree.
    """Recursively delete a directory tree.

    Args:
        dir_path (str or Path): A directory to be removed.
        backend_args (dict, optional): Arguments to instantiate the
            corresponding backend. Defaults to None.

    Examples:
        >>> dir_path = '/path/of/dir'
        >>> rmtree(dir_path)
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend = get_file_backend(
    backend = get_file_backend(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dir_path,
        dir_path,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_args=backend_args,
        backend_args=backend_args,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enable_singleton=True,
        enable_singleton=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_key=backend_key,
        backend_key=backend_key,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend.rmtree(dir_path)
    backend.rmtree(dir_path)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def copy_if_symlink_fails(
def copy_if_symlink_fails(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：src: Union[str, Path],
    src: Union[str, Path],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dst: Union[str, Path],
    dst: Union[str, Path],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_args: Optional[dict] = None,
    backend_args: Optional[dict] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_key: Optional[str] = None,
    backend_key: Optional[str] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> bool:
) -> bool:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Create a symbolic link pointing to src named dst.
    """Create a symbolic link pointing to src named dst.

    If failed to create a symbolic link pointing to src, directory copy src to
    dst instead.

    Args:
        src (str or Path): Create a symbolic link pointing to src.
        dst (str or Path): Create a symbolic link named dst.
        backend_args (dict, optional): Arguments to instantiate the
            corresponding backend. Defaults to None.

    Returns:
        bool: Return True if successfully create a symbolic link pointing to
        src. Otherwise, return False.

    Examples:
        >>> src = '/path/of/file'
        >>> dst = '/path1/of/file1'
        >>> copy_if_symlink_fails(src, dst)
        True
        >>> src = '/path/of/dir'
        >>> dst = '/path1/of/dir1'
        >>> copy_if_symlink_fails(src, dst)
        True
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend = get_file_backend(src, backend_args=backend_args, enable_singleton=True, backend_key...
    backend = get_file_backend(src, backend_args=backend_args, enable_singleton=True, backend_key=backend_key)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return backend.copy_if_symlink_fails(src, dst)
    return backend.copy_if_symlink_fails(src, dst)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def list_dir(
def list_dir(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dir_path: Union[str, Path],
    dir_path: Union[str, Path],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_args: Optional[dict] = None,
    backend_args: Optional[dict] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_key: Optional[str] = None,
    backend_key: Optional[str] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""List all folders in a directory with a given path.
    """List all folders in a directory with a given path.

    Args:
        dir_path (str | Path): Path of the directory.

    Examples:
        >>> dir_path = '/path/of/dir'
        >>> for file_path in list_dir(dir_path):
        ...     print(file_path)
    """
    # 中文说明：根据条件选择执行分支；代码：if not dir_path.endswith("/"):
    if not dir_path.endswith("/"):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dir_path += "/"
        dir_path += "/"
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend = get_file_backend(
    backend = get_file_backend(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dir_path,
        dir_path,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_args=backend_args,
        backend_args=backend_args,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enable_singleton=True,
        enable_singleton=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_key=backend_key,
        backend_key=backend_key,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return backend.list_dir(dir_path)
    return backend.list_dir(dir_path)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def list_dir_or_file(
def list_dir_or_file(
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
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_args: Optional[dict] = None,
    backend_args: Optional[dict] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_key: Optional[str] = None,
    backend_key: Optional[str] = None,
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
        backend_args (dict, optional): Arguments to instantiate the
            corresponding backend. Defaults to None.

    Yields:
        Iterable[str]: A relative path to ``dir_path``.

    Examples:
        >>> dir_path = '/path/of/dir'
        >>> for file_path in list_dir_or_file(dir_path):
        ...     print(file_path)
        >>> # list those files and directories in current directory
        >>> for file_path in list_dir_or_file(dir_path):
        ...     print(file_path)
        >>> # only list files
        >>> for file_path in list_dir_or_file(dir_path, list_dir=False):
        ...     print(file_path)
        >>> # only list directories
        >>> for file_path in list_dir_or_file(dir_path, list_file=False):
        ...     print(file_path)
        >>> # only list files ending with specified suffixes
        >>> for file_path in list_dir_or_file(dir_path, suffix='.txt'):
        ...     print(file_path)
        >>> # list all files and directory recursively
        >>> for file_path in list_dir_or_file(dir_path, recursive=True):
        ...     print(file_path)
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend = get_file_backend(
    backend = get_file_backend(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dir_path,
        dir_path,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_args=backend_args,
        backend_args=backend_args,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enable_singleton=True,
        enable_singleton=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_key=backend_key,
        backend_key=backend_key,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：从生成器逐步产生本行指定的值；代码：yield from backend.list_dir_or_file(dir_path, list_dir, list_file, suffix, recursive)
    yield from backend.list_dir_or_file(dir_path, list_dir, list_file, suffix, recursive)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def load(
def load(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：file: Union[str, Path, IO[Any]],
    file: Union[str, Path, IO[Any]],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：file_format: Optional[str] = None,
    file_format: Optional[str] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：file_client_args: Optional[dict] = None,
    file_client_args: Optional[dict] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：fast_backend: bool = False,
    fast_backend: bool = False,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_args: Optional[dict] = None,
    backend_args: Optional[dict] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_key: Optional[str] = None,
    backend_key: Optional[str] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**kwargs,
    **kwargs,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Load data from json/yaml/pickle files.
    """Load data from json/yaml/pickle files.

    This method provides a unified api for loading data from serialized files.

    ``load`` supports loading data from serialized files those can be storaged
    in different backends.

    Args:
        file (str or :obj:`Path` or file-like object): Filename or a file-like
            object.
        file_format (str, optional): If not specified, the file format will be
            inferred from the file extension, otherwise use the specified one.
            Currently supported formats include "json", "yaml/yml" and
            "pickle/pkl".
        file_client_args (dict, optional): Arguments to instantiate a
            FileClient. See :class:`mmengine.fileio.FileClient` for details.
            Defaults to None. It will be deprecated in future. Please use
            ``backend_args`` instead.
        fast_backend: bool: Whether to use multiprocess. Defaults to False.
        backend_args (dict, optional): Arguments to instantiate the
            prefix of uri corresponding backend. Defaults to None.
            New in v0.2.0.

    Examples:
        >>> load('/path/of/your/file')  # file is storaged in disk
        >>> load('https://path/of/your/file')  # file is storaged in Internet

    Returns:
        The content from the file.
    """
    # 中文说明：根据条件选择执行分支；代码：if isinstance(file, Path):
    if isinstance(file, Path):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：file = str(file)
        file = str(file)
    # 中文说明：根据条件选择执行分支；代码：if file_format is None and isinstance(file, str):
    if file_format is None and isinstance(file, str):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：file_format = file.split(".")[-1]
        file_format = file.split(".")[-1]
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# convert file_format to lower case
    # convert file_format to lower case
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：file_format = file_format.lower()
    file_format = file_format.lower()
    # 中文说明：根据条件选择执行分支；代码：if file_format not in file_handlers:
    if file_format not in file_handlers:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError(f"Unsupported format: {file_format}")
        raise TypeError(f"Unsupported format: {file_format}")

    # 中文说明：根据条件选择执行分支；代码：if file_client_args is not None:
    if file_client_args is not None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：warnings.warn(
        warnings.warn(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：'"file_client_args" will be deprecated in future. ' 'Please use "backend_args" instead',
            '"file_client_args" will be deprecated in future. ' 'Please use "backend_args" instead',
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：DeprecationWarning,
            DeprecationWarning,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：根据条件选择执行分支；代码：if backend_args is not None:
        if backend_args is not None:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError('"file_client_args and "backend_args" cannot be set at the ' "same time.")
            raise ValueError('"file_client_args and "backend_args" cannot be set at the ' "same time.")

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：handler = file_handlers[file_format]
    handler = file_handlers[file_format]
    # 中文说明：根据条件选择执行分支；代码：if isinstance(file, str):
    if isinstance(file, str):
        # 中文说明：根据条件选择执行分支；代码：if file_client_args is not None:
        if file_client_args is not None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：file_client = FileClient.infer_client(file_client_args, file)
            file_client = FileClient.infer_client(file_client_args, file)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：file_backend = file_client
            file_backend = file_client
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：file_backend = get_file_backend(
            file_backend = get_file_backend(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：file,
                file,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_args=backend_args,
                backend_args=backend_args,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_key=backend_key,
                backend_key=backend_key,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enable_singleton=True,
                enable_singleton=True,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：根据条件选择执行分支；代码：if handler.str_like:
        if handler.str_like:
            # 中文说明：处理异常、清理资源或管理上下文；代码：with StringIO(file_backend.get_text(file)) as f:
            with StringIO(file_backend.get_text(file)) as f:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：obj = handler.load_from_fileobj(f, **kwargs)
                obj = handler.load_from_fileobj(f, **kwargs)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：根据条件选择执行分支；代码：if fast_backend:
            if fast_backend:
                # 中文说明：根据条件选择执行分支；代码：if hasattr(file_backend, "fast_get"):
                if hasattr(file_backend, "fast_get"):
                    # 中文说明：处理异常、清理资源或管理上下文；代码：with BytesIO(file_backend.fast_get(file)) as f:
                    with BytesIO(file_backend.fast_get(file)) as f:
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：obj = handler.load_from_fileobj(f, **kwargs)
                        obj = handler.load_from_fileobj(f, **kwargs)
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：warnings.warn(
                    warnings.warn(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"fast_backend is not supported by the backend, type {type(file_backend)} fallback to normal ...
                        f"fast_backend is not supported by the backend, type {type(file_backend)} fallback to normal get"
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                    # 中文说明：处理异常、清理资源或管理上下文；代码：with BytesIO(file_backend.get(file)) as f:
                    with BytesIO(file_backend.get(file)) as f:
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：obj = handler.load_from_fileobj(f, **kwargs)
                        obj = handler.load_from_fileobj(f, **kwargs)
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：处理异常、清理资源或管理上下文；代码：with BytesIO(file_backend.get(file)) as f:
                with BytesIO(file_backend.get(file)) as f:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：obj = handler.load_from_fileobj(f, **kwargs)
                    obj = handler.load_from_fileobj(f, **kwargs)
    # 中文说明：根据条件选择执行分支；代码：elif hasattr(file, "read"):
    elif hasattr(file, "read"):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：obj = handler.load_from_fileobj(file, **kwargs)
        obj = handler.load_from_fileobj(file, **kwargs)
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError('"file" must be a filepath str or a file-object')
        raise TypeError('"file" must be a filepath str or a file-object')
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return obj
    return obj


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def dump(
def dump(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：obj: Any,
    obj: Any,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：file: Union[str, Path, IO[Any], None] = None,
    file: Union[str, Path, IO[Any], None] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：file_format: Optional[str] = None,
    file_format: Optional[str] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：file_client_args: Optional[dict] = None,
    file_client_args: Optional[dict] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：fast_backend: bool = False,
    fast_backend: bool = False,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_args: Optional[dict] = None,
    backend_args: Optional[dict] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend_key: Optional[str] = None,
    backend_key: Optional[str] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**kwargs,
    **kwargs,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Dump data to json/yaml/pickle strings or files.
    """Dump data to json/yaml/pickle strings or files.

    This method provides a unified api for dumping data as strings or to files,
    and also supports custom arguments for each file format.

    ``dump`` supports dumping data as strings or to files which is saved to
    different backends.

    Args:
        obj (any): The python object to be dumped.
        file (str or :obj:`Path` or file-like object, optional): If not
            specified, then the object is dumped to a str, otherwise to a file
            specified by the filename or file-like object.
        file_format (str, optional): Same as :func:`load`.
        file_client_args (dict, optional): Arguments to instantiate a
            FileClient. See :class:`mmengine.fileio.FileClient` for details.
            Defaults to None. It will be deprecated in future. Please use
            ``backend_args`` instead.
        fast_backend: bool: Whether to use multiprocess. Defaults to False.
        backend_args (dict, optional): Arguments to instantiate the
            prefix of uri corresponding backend. Defaults to None.
            New in v0.2.0.
        backend_key: str: The key to register the backend. Defaults to None.

    Examples:
        >>> dump('hello world', '/path/of/your/file')  # disk
        >>> dump('hello world', 'http://path/of/your/file')  # http

    Returns:
        bool: True for success, False otherwise.
    """
    # 中文说明：根据条件选择执行分支；代码：if isinstance(file, Path):
    if isinstance(file, Path):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：file = str(file)
        file = str(file)
    # 中文说明：根据条件选择执行分支；代码：if file_format is None:
    if file_format is None:
        # 中文说明：根据条件选择执行分支；代码：if isinstance(file, str):
        if isinstance(file, str):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：file_format = file.split(".")[-1]
            file_format = file.split(".")[-1]
        # 中文说明：根据条件选择执行分支；代码：elif file is None:
        elif file is None:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError("file_format must be specified since file is None")
            raise ValueError("file_format must be specified since file is None")
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# convert file_format to lower case
    # convert file_format to lower case
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：file_format = file_format.lower()
    file_format = file_format.lower()
    # 中文说明：根据条件选择执行分支；代码：if file_format not in file_handlers:
    if file_format not in file_handlers:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError(f"Unsupported format: {file_format}")
        raise TypeError(f"Unsupported format: {file_format}")

    # 中文说明：根据条件选择执行分支；代码：if file_client_args is not None:
    if file_client_args is not None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：warnings.warn(
        warnings.warn(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：'"file_client_args" will be deprecated in future. ' 'Please use "backend_args" instead',
            '"file_client_args" will be deprecated in future. ' 'Please use "backend_args" instead',
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：DeprecationWarning,
            DeprecationWarning,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：根据条件选择执行分支；代码：if backend_args is not None:
        if backend_args is not None:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError('"file_client_args" and "backend_args" cannot be set at the ' "same time.")
            raise ValueError('"file_client_args" and "backend_args" cannot be set at the ' "same time.")

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：handler = file_handlers[file_format]
    handler = file_handlers[file_format]
    # 中文说明：根据条件选择执行分支；代码：if file is None:
    if file is None:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return handler.dump_to_str(obj, **kwargs)
        return handler.dump_to_str(obj, **kwargs)
    # 中文说明：根据条件选择执行分支；代码：elif isinstance(file, str):
    elif isinstance(file, str):
        # 中文说明：根据条件选择执行分支；代码：if file_client_args is not None:
        if file_client_args is not None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：file_client = FileClient.infer_client(file_client_args, file)
            file_client = FileClient.infer_client(file_client_args, file)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：file_backend = file_client
            file_backend = file_client
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：file_backend = get_file_backend(
            file_backend = get_file_backend(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：file,
                file,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_args=backend_args,
                backend_args=backend_args,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_key=backend_key,
                backend_key=backend_key,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enable_singleton=True,
                enable_singleton=True,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：根据条件选择执行分支；代码：if handler.str_like:
        if handler.str_like:
            # 中文说明：处理异常、清理资源或管理上下文；代码：with StringIO() as f:
            with StringIO() as f:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：handler.dump_to_fileobj(obj, f, **kwargs)
                handler.dump_to_fileobj(obj, f, **kwargs)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：file_backend.put_text(f.getvalue(), file)
                file_backend.put_text(f.getvalue(), file)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：处理异常、清理资源或管理上下文；代码：with BytesIO() as f:
            with BytesIO() as f:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：handler.dump_to_fileobj(obj, f, **kwargs)
                handler.dump_to_fileobj(obj, f, **kwargs)
                # 中文说明：根据条件选择执行分支；代码：if fast_backend:
                if fast_backend:
                    # 中文说明：根据条件选择执行分支；代码：if hasattr(file_backend, "fast_put"):
                    if hasattr(file_backend, "fast_put"):
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：file_backend.fast_put(f, file)
                        file_backend.fast_put(f, file)
                    # 中文说明：根据条件选择执行分支；代码：else:
                    else:
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：warnings.warn("fast_backend is not supported by the backend, fallback to normal put")
                        warnings.warn("fast_backend is not supported by the backend, fallback to normal put")
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：file_backend.put(f, file)
                        file_backend.put(f, file)
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：file_backend.put(f, file)
                    file_backend.put(f, file)
    # 中文说明：根据条件选择执行分支；代码：elif hasattr(file, "write"):
    elif hasattr(file, "write"):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：handler.dump_to_fileobj(obj, file, **kwargs)
        handler.dump_to_fileobj(obj, file, **kwargs)
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError('"file" must be a filename str or a file-object')
        raise TypeError('"file" must be a filename str or a file-object')
