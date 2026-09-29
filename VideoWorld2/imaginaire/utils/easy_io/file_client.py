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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from contextlib import contextmanager
from contextlib import contextmanager
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from pathlib import Path
from pathlib import Path
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any, Generator, Iterator, Optional, Tuple, Union
from typing import Any, Generator, Iterator, Optional, Tuple, Union

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.backends import BaseStorageBackend, HTTPBackend, LocalBackend
from imaginaire.utils.easy_io.backends import BaseStorageBackend, HTTPBackend, LocalBackend


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_filepath(filepath):
def is_filepath(filepath):
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return isinstance(filepath, (str, Path))
    return isinstance(filepath, (str, Path))


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class HardDiskBackend(LocalBackend):
class HardDiskBackend(LocalBackend):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Raw hard disks storage backend."""
    """Raw hard disks storage backend."""

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def name(self):
    def name(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.__class__.__name__
        return self.__class__.__name__


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class FileClient:
class FileClient:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""A general file client to access files in different backends.
    """A general file client to access files in different backends.

    The client loads a file or text in a specified backend from its path
    and returns it as a binary or text file. There are two ways to choose a
    backend, the name of backend and the prefix of path. Although both of them
    can be used to choose a storage backend, ``backend`` has a higher priority
    that is if they are all set, the storage backend will be chosen by the
    backend argument. If they are all `None`, the disk backend will be chosen.
    Note that It can also register other backend accessor with a given name,
    prefixes, and backend class. In addition, We use the singleton pattern to
    avoid repeated object creation. If the arguments are the same, the same
    object will be returned.

    Warning:
        `FileClient` will be deprecated in future. Please use io functions
        in https://mmengine.readthedocs.io/en/latest/api/fileio.html#file-io

    Args:
        backend (str, optional): The storage backend type. Options are "disk",
            "memcached", "lmdb" and "http". Defaults to None.
        prefix (str, optional): The prefix of the registered storage backend.
            Options are "http", "https". Defaults to None.

    Examples:
        >>> # only set backend
        >>> file_client = FileClient(backend='disk')
        >>> # only set prefix
        >>> file_client = FileClient(prefix='http')
        >>> # set both backend and prefix but use backend to choose client
        >>> file_client = FileClient(backend='http', prefix='http')
        >>> # if the arguments are the same, the same object is returned
        >>> file_client1 = FileClient(backend='disk')
        >>> file_client1 is file_client
        True

    Attributes:
        client (:obj:`BaseStorageBackend`): The backend object.
    """

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_backends = {
    _backends = {
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："disk": HardDiskBackend,
        "disk": HardDiskBackend,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："http": HTTPBackend,
        "http": HTTPBackend,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
    }

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_prefix_to_backends: dict = {
    _prefix_to_backends: dict = {
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："http": HTTPBackend,
        "http": HTTPBackend,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："https": HTTPBackend,
        "https": HTTPBackend,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
    }

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_instances: dict = {}
    _instances: dict = {}

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：client: Any
    client: Any

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __new__(cls, backend=None, prefix=None, **kwargs):
    def __new__(cls, backend=None, prefix=None, **kwargs):
        # 中文说明：根据条件选择执行分支；代码：if backend is None and prefix is None:
        if backend is None and prefix is None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend = "disk"
            backend = "disk"
        # 中文说明：根据条件选择执行分支；代码：if backend is not None and backend not in cls._backends:
        if backend is not None and backend not in cls._backends:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(
            raise ValueError(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Backend {backend} is not supported. Currently supported ones" f" are {list(cls._backends.ke...
                f"Backend {backend} is not supported. Currently supported ones" f" are {list(cls._backends.keys())}"
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：根据条件选择执行分支；代码：if prefix is not None and prefix not in cls._prefix_to_backends:
        if prefix is not None and prefix not in cls._prefix_to_backends:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(
            raise ValueError(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"prefix {prefix} is not supported. Currently supported ones "
                f"prefix {prefix} is not supported. Currently supported ones "
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"are {list(cls._prefix_to_backends.keys())}"
                f"are {list(cls._prefix_to_backends.keys())}"
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# concatenate the arguments to a unique key for determining whether
        # concatenate the arguments to a unique key for determining whether
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# objects with the same arguments were created
        # objects with the same arguments were created
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：arg_key = f"{backend}:{prefix}"
        arg_key = f"{backend}:{prefix}"
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key, value in kwargs.items():
        for key, value in kwargs.items():
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：arg_key += f":{key}:{value}"
            arg_key += f":{key}:{value}"

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# if a backend was overridden, it will create a new object
        # if a backend was overridden, it will create a new object
        # 中文说明：根据条件选择执行分支；代码：if arg_key in cls._instances:
        if arg_key in cls._instances:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_instance = cls._instances[arg_key]
            _instance = cls._instances[arg_key]
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# create a new object and put it to _instance
            # create a new object and put it to _instance
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_instance = super().__new__(cls)
            _instance = super().__new__(cls)
            # 中文说明：根据条件选择执行分支；代码：if backend is not None:
            if backend is not None:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_instance.client = cls._backends[backend](**kwargs)
                _instance.client = cls._backends[backend](**kwargs)
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_instance.client = cls._prefix_to_backends[prefix](**kwargs)
                _instance.client = cls._prefix_to_backends[prefix](**kwargs)

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cls._instances[arg_key] = _instance
            cls._instances[arg_key] = _instance

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return _instance
        return _instance

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def name(self):
    def name(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.client.name
        return self.client.name

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def allow_symlink(self):
    def allow_symlink(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.client.allow_symlink
        return self.client.allow_symlink

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def parse_uri_prefix(uri: Union[str, Path]) -> Optional[str]:
    def parse_uri_prefix(uri: Union[str, Path]) -> Optional[str]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Parse the prefix of a uri.
        """Parse the prefix of a uri.

        Args:
            uri (str | Path): Uri to be parsed that contains the file prefix.

        Examples:
            >>> FileClient.parse_uri_prefix('http://path/of/your/file')
            'http'

        Returns:
            str | None: Return the prefix of uri if the uri contains '://' else
            ``None``.
        """
        # 中文说明：检查运行时假设是否成立；代码：assert is_filepath(uri)
        assert is_filepath(uri)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：uri = str(uri)
        uri = str(uri)
        # 中文说明：根据条件选择执行分支；代码：if "://" not in uri:
        if "://" not in uri:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return None
            return None
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：prefix, _ = uri.split("://")
            prefix, _ = uri.split("://")
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return prefix
            return prefix

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@classmethod
    @classmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def infer_client(
    def infer_client(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cls,
        cls,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：file_client_args: Optional[dict] = None,
        file_client_args: Optional[dict] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：uri: Optional[Union[str, Path]] = None,
        uri: Optional[Union[str, Path]] = None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> "FileClient":
    ) -> "FileClient":
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Infer a suitable file client based on the URI and arguments.
        """Infer a suitable file client based on the URI and arguments.

        Args:
            file_client_args (dict, optional): Arguments to instantiate a
                FileClient. Defaults to None.
            uri (str | Path, optional): Uri to be parsed that contains the file
                prefix. Defaults to None.

        Examples:
            >>> uri = 'http://path/of/your/file'
            >>> file_client = FileClient.infer_client(uri=uri)
            >>> file_client_args = {'backend': 'disk'}
            >>> file_client = FileClient.infer_client(file_client_args)

        Returns:
            FileClient: Instantiated FileClient object.
        """
        # 中文说明：检查运行时假设是否成立；代码：assert file_client_args is not None or uri is not None
        assert file_client_args is not None or uri is not None
        # 中文说明：根据条件选择执行分支；代码：if file_client_args is None:
        if file_client_args is None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：file_prefix = cls.parse_uri_prefix(uri) # type: ignore
            file_prefix = cls.parse_uri_prefix(uri)  # type: ignore
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return cls(prefix=file_prefix)
            return cls(prefix=file_prefix)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return cls(**file_client_args)
            return cls(**file_client_args)

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@classmethod
    @classmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _register_backend(cls, name, backend, force=False, prefixes=None):
    def _register_backend(cls, name, backend, force=False, prefixes=None):
        # 中文说明：根据条件选择执行分支；代码：if not isinstance(name, str):
        if not isinstance(name, str):
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError("the backend name should be a string, " f"but got {type(name)}")
            raise TypeError("the backend name should be a string, " f"but got {type(name)}")
        # 中文说明：根据条件选择执行分支；代码：if not inspect.isclass(backend):
        if not inspect.isclass(backend):
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError(f"backend should be a class but got {type(backend)}")
            raise TypeError(f"backend should be a class but got {type(backend)}")
        # 中文说明：根据条件选择执行分支；代码：if not issubclass(backend, BaseStorageBackend):
        if not issubclass(backend, BaseStorageBackend):
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError(f"backend {backend} is not a subclass of BaseStorageBackend")
            raise TypeError(f"backend {backend} is not a subclass of BaseStorageBackend")
        # 中文说明：根据条件选择执行分支；代码：if not force and name in cls._backends:
        if not force and name in cls._backends:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise KeyError(
            raise KeyError(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"{name} is already registered as a storage backend, " 'add "force=True" if you want to overr...
                f"{name} is already registered as a storage backend, " 'add "force=True" if you want to override it'
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：根据条件选择执行分支；代码：if name in cls._backends and force:
        if name in cls._backends and force:
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for arg_key, instance in list(cls._instances.items()):
            for arg_key, instance in list(cls._instances.items()):
                # 中文说明：根据条件选择执行分支；代码：if isinstance(instance.client, cls._backends[name]):
                if isinstance(instance.client, cls._backends[name]):
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cls._instances.pop(arg_key)
                    cls._instances.pop(arg_key)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cls._backends[name] = backend
        cls._backends[name] = backend

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
                # 中文说明：根据条件选择执行分支；代码：if prefix not in cls._prefix_to_backends:
                if prefix not in cls._prefix_to_backends:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cls._prefix_to_backends[prefix] = backend
                    cls._prefix_to_backends[prefix] = backend
                # 中文说明：根据条件选择执行分支；代码：elif (prefix in cls._prefix_to_backends) and force:
                elif (prefix in cls._prefix_to_backends) and force:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：overridden_backend = cls._prefix_to_backends[prefix]
                    overridden_backend = cls._prefix_to_backends[prefix]
                    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for arg_key, instance in list(cls._instances.items()):
                    for arg_key, instance in list(cls._instances.items()):
                        # 中文说明：根据条件选择执行分支；代码：if isinstance(instance.client, overridden_backend):
                        if isinstance(instance.client, overridden_backend):
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cls._instances.pop(arg_key)
                            cls._instances.pop(arg_key)
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise KeyError(
                    raise KeyError(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"{prefix} is already registered as a storage backend,"
                        f"{prefix} is already registered as a storage backend,"
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：' add "force=True" if you want to override it'
                        ' add "force=True" if you want to override it'
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@classmethod
    @classmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def register_backend(cls, name, backend=None, force=False, prefixes=None):
    def register_backend(cls, name, backend=None, force=False, prefixes=None):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Register a backend to FileClient.
        """Register a backend to FileClient.

        This method can be used as a normal class method or a decorator.

        .. code-block:: python

            class NewBackend(BaseStorageBackend):

                def get(self, filepath):
                    return filepath

                def get_text(self, filepath):
                    return filepath

            FileClient.register_backend('new', NewBackend)

        or

        .. code-block:: python

            @FileClient.register_backend('new')
            class NewBackend(BaseStorageBackend):

                def get(self, filepath):
                    return filepath

                def get_text(self, filepath):
                    return filepath

        Args:
            name (str): The name of the registered backend.
            backend (class, optional): The backend class to be registered,
                which must be a subclass of :class:`BaseStorageBackend`.
                When this method is used as a decorator, backend is None.
                Defaults to None.
            force (bool, optional): Whether to override the backend if the name
                has already been registered. Defaults to False.
            prefixes (str or list[str] or tuple[str], optional): The prefixes
                of the registered storage backend. Defaults to None.
                `New in version 1.3.15.`
        """
        # 中文说明：根据条件选择执行分支；代码：if backend is not None:
        if backend is not None:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cls._register_backend(name, backend, force=force, prefixes=prefixes)
            cls._register_backend(name, backend, force=force, prefixes=prefixes)
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return
            return

        # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _register(backend_cls):
        def _register(backend_cls):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cls._register_backend(name, backend_cls, force=force, prefixes=prefixes)
            cls._register_backend(name, backend_cls, force=force, prefixes=prefixes)
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return backend_cls
            return backend_cls

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return _register
        return _register

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get(self, filepath: Union[str, Path]) -> Union[bytes, memoryview]:
    def get(self, filepath: Union[str, Path]) -> Union[bytes, memoryview]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Read data from a given ``filepath`` with 'rb' mode.
        """Read data from a given ``filepath`` with 'rb' mode.

        Note:
            There are two types of return values for ``get``, one is ``bytes``
            and the other is ``memoryview``. The advantage of using memoryview
            is that you can avoid copying, and if you want to convert it to
            ``bytes``, you can use ``.tobytes()``.

        Args:
            filepath (str or Path): Path to read data.

        Returns:
            bytes | memoryview: Expected bytes object or a memory view of the
            bytes object.
        """
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.client.get(filepath)
        return self.client.get(filepath)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_text(self, filepath: Union[str, Path], encoding="utf-8") -> str:
    def get_text(self, filepath: Union[str, Path], encoding="utf-8") -> str:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Read data from a given ``filepath`` with 'r' mode.
        """Read data from a given ``filepath`` with 'r' mode.

        Args:
            filepath (str or Path): Path to read data.
            encoding (str): The encoding format used to open the ``filepath``.
                Defaults to 'utf-8'.

        Returns:
            str: Expected text reading from ``filepath``.
        """
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.client.get_text(filepath, encoding)
        return self.client.get_text(filepath, encoding)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def put(self, obj: bytes, filepath: Union[str, Path]) -> None:
    def put(self, obj: bytes, filepath: Union[str, Path]) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Write data to a given ``filepath`` with 'wb' mode.
        """Write data to a given ``filepath`` with 'wb' mode.

        Note:
            ``put`` should create a directory if the directory of ``filepath``
            does not exist.

        Args:
            obj (bytes): Data to be written.
            filepath (str or Path): Path to write data.
        """
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.client.put(obj, filepath)
        self.client.put(obj, filepath)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def put_text(self, obj: str, filepath: Union[str, Path]) -> None:
    def put_text(self, obj: str, filepath: Union[str, Path]) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Write data to a given ``filepath`` with 'w' mode.
        """Write data to a given ``filepath`` with 'w' mode.

        Note:
            ``put_text`` should create a directory if the directory of
            ``filepath`` does not exist.

        Args:
            obj (str): Data to be written.
            filepath (str or Path): Path to write data.
            encoding (str, optional): The encoding format used to open the
                `filepath`. Defaults to 'utf-8'.
        """
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.client.put_text(obj, filepath)
        self.client.put_text(obj, filepath)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def remove(self, filepath: Union[str, Path]) -> None:
    def remove(self, filepath: Union[str, Path]) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Remove a file.
        """Remove a file.

        Args:
            filepath (str, Path): Path to be removed.
        """
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.client.remove(filepath)
        self.client.remove(filepath)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def exists(self, filepath: Union[str, Path]) -> bool:
    def exists(self, filepath: Union[str, Path]) -> bool:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Check whether a file path exists.
        """Check whether a file path exists.

        Args:
            filepath (str or Path): Path to be checked whether exists.

        Returns:
            bool: Return ``True`` if ``filepath`` exists, ``False`` otherwise.
        """
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.client.exists(filepath)
        return self.client.exists(filepath)

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
        """
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.client.isdir(filepath)
        return self.client.isdir(filepath)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def isfile(self, filepath: Union[str, Path]) -> bool:
    def isfile(self, filepath: Union[str, Path]) -> bool:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Check whether a file path is a file.
        """Check whether a file path is a file.

        Args:
            filepath (str or Path): Path to be checked whether it is a file.

        Returns:
            bool: Return ``True`` if ``filepath`` points to a file, ``False``
            otherwise.
        """
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.client.isfile(filepath)
        return self.client.isfile(filepath)

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
        """
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.client.join_path(filepath, *filepaths)
        return self.client.join_path(filepath, *filepaths)

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@contextmanager
    @contextmanager
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_local_path(self, filepath: Union[str, Path]) -> Generator[Union[str, Path], None, None]:
    def get_local_path(self, filepath: Union[str, Path]) -> Generator[Union[str, Path], None, None]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Download data from ``filepath`` and write the data to local path.
        """Download data from ``filepath`` and write the data to local path.

        ``get_local_path`` is decorated by :meth:`contxtlib.contextmanager`. It
        can be called with ``with`` statement, and when exists from the
        ``with`` statement, the temporary path will be released.

        Note:
            If the ``filepath`` is a local path, just return itself.

        .. warning::
            ``get_local_path`` is an experimental interface that may change in
            the future.

        Args:
            filepath (str or Path): Path to be read data.

        Examples:
            >>> file_client = FileClient(prefix='http')
            >>> with file_client.get_local_path('http://example.com/abc.jpg') as path:
            ...     # do something here

        Yields:
            Iterable[str]: Only yield one path.
        """
        # 中文说明：处理异常、清理资源或管理上下文；代码：with self.client.get_local_path(str(filepath)) as local_path:
        with self.client.get_local_path(str(filepath)) as local_path:
            # 中文说明：从生成器逐步产生本行指定的值；代码：yield local_path
            yield local_path

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def list_dir_or_file( # pylint: disable=too-many-arguments
    def list_dir_or_file(  # pylint: disable=too-many-arguments
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
            dir_path (str | Path): Path of the directory.
            list_dir (bool): List the directories. Defaults to True.
            list_file (bool): List the path of files. Defaults to True.
            suffix (str or tuple[str], optional):  File suffix
                that we are interested in. Defaults to None.
            recursive (bool): If set to True, recursively scan the
                directory. Defaults to False.

        Yields:
            Iterable[str]: A relative path to ``dir_path``.
        """
        # 中文说明：从生成器逐步产生本行指定的值；代码：yield from self.client.list_dir_or_file(dir_path, list_dir, list_file, suffix, recursive)
        yield from self.client.list_dir_or_file(dir_path, list_dir, list_file, suffix, recursive)
