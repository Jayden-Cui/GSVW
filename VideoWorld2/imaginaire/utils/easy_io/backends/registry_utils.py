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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import inspect
import inspect
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Optional, Type, Union
from typing import Optional, Type, Union

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.backends.base_backend import BaseStorageBackend
from imaginaire.utils.easy_io.backends.base_backend import BaseStorageBackend
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.backends.http_backend import HTTPBackend
from imaginaire.utils.easy_io.backends.http_backend import HTTPBackend
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.backends.local_backend import LocalBackend
from imaginaire.utils.easy_io.backends.local_backend import LocalBackend

# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backends: dict = {}
backends: dict = {}
# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：prefix_to_backends: dict = {}
prefix_to_backends: dict = {}


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _register_backend(
def _register_backend(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：name: str,
    name: str,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend: Type[BaseStorageBackend],
    backend: Type[BaseStorageBackend],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：force: bool = False,
    force: bool = False,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：prefixes: Union[str, list, tuple, None] = None,
    prefixes: Union[str, list, tuple, None] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Register a backend.
    """Register a backend.

    Args:
        name (str): The name of the registered backend.
        backend (BaseStorageBackend): The backend class to be registered,
            which must be a subclass of :class:`BaseStorageBackend`.
        force (bool): Whether to override the backend if the name has already
            been registered. Defaults to False.
        prefixes (str or list[str] or tuple[str], optional): The prefix
            of the registered storage backend. Defaults to None.
    """
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：global backends, prefix_to_backends
    global backends, prefix_to_backends

    # 中文说明：根据条件选择执行分支；代码：if not isinstance(name, str):
    if not isinstance(name, str):
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError("the backend name should be a string, " f"but got {type(name)}")
        raise TypeError("the backend name should be a string, " f"but got {type(name)}")

    # 中文说明：根据条件选择执行分支；代码：if not inspect.isclass(backend):
    if not inspect.isclass(backend):
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError(f"backend should be a class, but got {type(backend)}")
        raise TypeError(f"backend should be a class, but got {type(backend)}")
    # 中文说明：根据条件选择执行分支；代码：if not issubclass(backend, BaseStorageBackend):
    if not issubclass(backend, BaseStorageBackend):
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError(f"backend {backend} is not a subclass of BaseStorageBackend")
        raise TypeError(f"backend {backend} is not a subclass of BaseStorageBackend")

    # 中文说明：根据条件选择执行分支；代码：if name in backends and not force:
    if name in backends and not force:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(
        raise ValueError(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"{name} is already registered as a storage backend, " 'add "force=True" if you want to overr...
            f"{name} is already registered as a storage backend, " 'add "force=True" if you want to override it'
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backends[name] = backend
    backends[name] = backend

    # 中文说明：根据条件选择执行分支；代码：if prefixes is not None:
    if prefixes is not None:
        # 中文说明：根据条件选择执行分支；代码：if isinstance(prefixes, str):
        if isinstance(prefixes, str):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prefixes = [prefixes]
            prefixes = [prefixes]
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：检查运行时假设是否成立；代码：assert isinstance(prefixes, (list, tuple))
            assert isinstance(prefixes, (list, tuple))

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for prefix in prefixes:
        for prefix in prefixes:
            # 中文说明：根据条件选择执行分支；代码：if prefix in prefix_to_backends and not force:
            if prefix in prefix_to_backends and not force:
                # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(
                raise ValueError(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"{prefix} is already registered as a storage backend,"
                    f"{prefix} is already registered as a storage backend,"
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：' add "force=True" if you want to override it'
                    ' add "force=True" if you want to override it'
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prefix_to_backends[prefix] = backend
            prefix_to_backends[prefix] = backend


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def register_backend(
def register_backend(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：name: str,
    name: str,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend: Optional[Type[BaseStorageBackend]] = None,
    backend: Optional[Type[BaseStorageBackend]] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：force: bool = False,
    force: bool = False,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：prefixes: Union[str, list, tuple, None] = None,
    prefixes: Union[str, list, tuple, None] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Register a backend.
    """Register a backend.

    Args:
        name (str): The name of the registered backend.
        backend (class, optional): The backend class to be registered,
            which must be a subclass of :class:`BaseStorageBackend`.
            When this method is used as a decorator, backend is None.
            Defaults to None.
        force (bool): Whether to override the backend if the name has already
            been registered. Defaults to False.
        prefixes (str or list[str] or tuple[str], optional): The prefix
            of the registered storage backend. Defaults to None.

    This method can be used as a normal method or a decorator.

    Examples:

        >>> class NewBackend(BaseStorageBackend):
        ...     def get(self, filepath):
        ...         return filepath
        ...
        ...     def get_text(self, filepath):
        ...         return filepath
        >>> register_backend('new', NewBackend)

        >>> @register_backend('new')
        ... class NewBackend(BaseStorageBackend):
        ...     def get(self, filepath):
        ...         return filepath
        ...
        ...     def get_text(self, filepath):
        ...         return filepath
    """
    # 中文说明：根据条件选择执行分支；代码：if backend is not None:
    if backend is not None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_register_backend(name, backend, force=force, prefixes=prefixes)
        _register_backend(name, backend, force=force, prefixes=prefixes)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return
        return

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _register(backend_cls):
    def _register(backend_cls):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_register_backend(name, backend_cls, force=force, prefixes=prefixes)
        _register_backend(name, backend_cls, force=force, prefixes=prefixes)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return backend_cls
        return backend_cls

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return _register
    return _register


# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：register_backend("local", LocalBackend, prefixes="")
register_backend("local", LocalBackend, prefixes="")
# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：register_backend("http", HTTPBackend, prefixes=["http", "https"])
register_backend("http", HTTPBackend, prefixes=["http", "https"])
