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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import ast
import ast
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import builtins
import builtins
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import collections.abc as abc
import collections.abc as abc
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import importlib
import importlib
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import inspect
import inspect
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import logging
import logging
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import pickle
import pickle
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import uuid
import uuid
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from collections import OrderedDict
from collections import OrderedDict
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from contextlib import contextmanager
from contextlib import contextmanager
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from copy import deepcopy
from copy import deepcopy
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from dataclasses import is_dataclass
from dataclasses import is_dataclass
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any, Dict, List, Tuple, Union
from typing import Any, Dict, List, Tuple, Union

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import attrs
import attrs
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import yaml
import yaml
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from omegaconf import DictConfig, ListConfig, OmegaConf
from omegaconf import DictConfig, ListConfig, OmegaConf

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log

# 中文说明：开始一个可捕获异常的代码块；代码：try:
try:
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import dill as dill_pickle
    import dill as dill_pickle
# 中文说明：处理异常、清理资源或管理上下文；代码：except ImportError:
except ImportError:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dill_pickle = None
    dill_pickle = None

# 中文说明：开始一个可捕获异常的代码块；代码：try:
try:
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import cloudpickle
    import cloudpickle
# 中文说明：处理异常、清理资源或管理上下文；代码：except ImportError:
except ImportError:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cloudpickle = None
    cloudpickle = None

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config.file_io import PathManager
from imaginaire.lazy_config.file_io import PathManager
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config.registry import _convert_target_to_string
from imaginaire.lazy_config.registry import _convert_target_to_string

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：__all__ = ["LazyCall", "LazyConfig"]
__all__ = ["LazyCall", "LazyConfig"]


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def sort_dict(d: Dict[str, Any]) -> OrderedDict[str, Any]:
def sort_dict(d: Dict[str, Any]) -> OrderedDict[str, Any]:
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return OrderedDict(sorted(d.items(), key=lambda x: x[0]))
    return OrderedDict(sorted(d.items(), key=lambda x: x[0]))


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def dict_representer(dumper: yaml.Dumper, data: OrderedDict[str, Any]) -> yaml.nodes.MappingN...
def dict_representer(dumper: yaml.Dumper, data: OrderedDict[str, Any]) -> yaml.nodes.MappingNode:
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return dumper.represent_mapping("tag:yaml.org,2002:map", data.items())
    return dumper.represent_mapping("tag:yaml.org,2002:map", data.items())


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def sort_recursive(obj: Union[Dict[str, Any], List[Any], Any]) -> Union[OrderedDict[str, Any]...
def sort_recursive(obj: Union[Dict[str, Any], List[Any], Any]) -> Union[OrderedDict[str, Any], List[Any], Any]:
    # 中文说明：根据条件选择执行分支；代码：if isinstance(obj, dict):
    if isinstance(obj, dict):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return sort_dict({k: sort_recursive(v) for k, v in obj.items()})
        return sort_dict({k: sort_recursive(v) for k, v in obj.items()})
    # 中文说明：根据条件选择执行分支；代码：elif isinstance(obj, list):
    elif isinstance(obj, list):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return [sort_recursive(item) for item in obj]
        return [sort_recursive(item) for item in obj]
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return obj
    return obj


# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：yaml.add_representer(OrderedDict, dict_representer)
yaml.add_representer(OrderedDict, dict_representer)

# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：OmegaConf.register_new_resolver("add", lambda *vals: sum(vals))
OmegaConf.register_new_resolver("add", lambda *vals: sum(vals))
# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：OmegaConf.register_new_resolver("subtract", lambda *vals: vals[0] - sum(vals[1:]))
OmegaConf.register_new_resolver("subtract", lambda *vals: vals[0] - sum(vals[1:]))


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_default_params(cls_or_func):
def get_default_params(cls_or_func):
    # 中文说明：根据条件选择执行分支；代码：if callable(cls_or_func):
    if callable(cls_or_func):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# inspect signature for function
        # inspect signature for function
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：signature = inspect.signature(cls_or_func)
        signature = inspect.signature(cls_or_func)
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# inspect signature for class
        # inspect signature for class
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：signature = inspect.signature(cls_or_func.__init__)
        signature = inspect.signature(cls_or_func.__init__)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：params = signature.parameters
    params = signature.parameters
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default_params = {
    default_params = {
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：name: param.default for name, param in params.items() if param.default is not inspect.Paramet...
        name: param.default for name, param in params.items() if param.default is not inspect.Parameter.empty
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
    }
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return default_params
    return default_params


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class LazyCall:
class LazyCall:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Wrap a callable so that when it's called, the call will not be executed,
    but returns a dict that describes the call.

    LazyCall object has to be called with only keyword arguments. Positional
    arguments are not yet supported.

    Examples:
    ::
        from detectron2.config import instantiate, LazyCall

        layer_cfg = LazyCall(nn.Conv2d)(in_channels=32, out_channels=32)
        layer_cfg.out_channels = 64   # can edit it afterwards
        layer = instantiate(layer_cfg)
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, target):
    def __init__(self, target):
        # 中文说明：根据条件选择执行分支；代码：if not (callable(target) or isinstance(target, (str, abc.Mapping))):
        if not (callable(target) or isinstance(target, (str, abc.Mapping))):
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError(f"target of LazyCall must be a callable or defines a callable! Got {target}")
            raise TypeError(f"target of LazyCall must be a callable or defines a callable! Got {target}")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._target = target
        self._target = target

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, **kwargs):
    def __call__(self, **kwargs):
        # 中文说明：根据条件选择执行分支；代码：if is_dataclass(self._target) or attrs.has(self._target):
        if is_dataclass(self._target) or attrs.has(self._target):
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# omegaconf object cannot hold dataclass type
            # omegaconf object cannot hold dataclass type
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# https://github.com/omry/omegaconf/issues/784
            # https://github.com/omry/omegaconf/issues/784
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：target = _convert_target_to_string(self._target)
            target = _convert_target_to_string(self._target)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：target = self._target
            target = self._target
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["_target_"] = target
        kwargs["_target_"] = target

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_final_params = get_default_params(self._target)
        _final_params = get_default_params(self._target)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_final_params.update(kwargs)
        _final_params.update(kwargs)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return DictConfig(content=_final_params, flags={"allow_objects": True})
        return DictConfig(content=_final_params, flags={"allow_objects": True})


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _visit_dict_config(cfg, func):
def _visit_dict_config(cfg, func):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Apply func recursively to all DictConfig in cfg.
    """
    # 中文说明：根据条件选择执行分支；代码：if isinstance(cfg, DictConfig):
    if isinstance(cfg, DictConfig):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：func(cfg)
        func(cfg)
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for v in cfg.values():
        for v in cfg.values():
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_visit_dict_config(v, func)
            _visit_dict_config(v, func)
    # 中文说明：根据条件选择执行分支；代码：elif isinstance(cfg, ListConfig):
    elif isinstance(cfg, ListConfig):
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for v in cfg:
        for v in cfg:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_visit_dict_config(v, func)
            _visit_dict_config(v, func)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _validate_py_syntax(filename):
def _validate_py_syntax(filename):
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# see also https://github.com/open-mmlab/mmcv/blob/master/mmcv/utils/config.py
    # see also https://github.com/open-mmlab/mmcv/blob/master/mmcv/utils/config.py
    # 中文说明：处理异常、清理资源或管理上下文；代码：with PathManager.open(filename, "r") as f:
    with PathManager.open(filename, "r") as f:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：content = f.read()
        content = f.read()
    # 中文说明：开始一个可捕获异常的代码块；代码：try:
    try:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ast.parse(content)
        ast.parse(content)
    # 中文说明：处理异常、清理资源或管理上下文；代码：except SyntaxError as e:
    except SyntaxError as e:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise SyntaxError(f"Config file {filename} has syntax error!") from e
        raise SyntaxError(f"Config file {filename} has syntax error!") from e


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _cast_to_config(obj):
def _cast_to_config(obj):
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# if given a dict, return DictConfig instead
    # if given a dict, return DictConfig instead
    # 中文说明：根据条件选择执行分支；代码：if isinstance(obj, dict):
    if isinstance(obj, dict):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return DictConfig(obj, flags={"allow_objects": True})
        return DictConfig(obj, flags={"allow_objects": True})
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return obj
    return obj


# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_CFG_PACKAGE_NAME = "detectron2._cfg_loader"
_CFG_PACKAGE_NAME = "detectron2._cfg_loader"
# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
"""
A namespace to put all imported config into.
"""


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _random_package_name(filename):
def _random_package_name(filename):
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# generate a random package name when loading config files
    # generate a random package name when loading config files
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return _CFG_PACKAGE_NAME + str(uuid.uuid4())[:4] + "." + os.path.basename(filename)
    return _CFG_PACKAGE_NAME + str(uuid.uuid4())[:4] + "." + os.path.basename(filename)


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@contextmanager
@contextmanager
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _patch_import():
def _patch_import():
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Enhance relative import statements in config files, so that they:
    1. locate files purely based on relative location, regardless of packages.
       e.g. you can import file without having __init__
    2. do not cache modules globally; modifications of module states has no side effect
    3. support other storage system through PathManager, so config files can be in the cloud
    4. imported dict are turned into omegaconf.DictConfig automatically
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：old_import = builtins.__import__
    old_import = builtins.__import__

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def find_relative_file(original_file, relative_import_path, level):
    def find_relative_file(original_file, relative_import_path, level):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# NOTE: "from . import x" is not handled. Because then it's unclear
        # NOTE: "from . import x" is not handled. Because then it's unclear
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# if such import should produce `x` as a python module or DictConfig.
        # if such import should produce `x` as a python module or DictConfig.
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# This can be discussed further if needed.
        # This can be discussed further if needed.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：relative_import_err = """
        relative_import_err = """
Relative import of directories is not allowed within config files.
Within a config file, relative import can only import other config files.
""".replace(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："\n", " "
            "\n", " "
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：根据条件选择执行分支；代码：if not len(relative_import_path):
        if not len(relative_import_path):
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ImportError(relative_import_err)
            raise ImportError(relative_import_err)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cur_file = os.path.dirname(original_file)
        cur_file = os.path.dirname(original_file)
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _ in range(level - 1):
        for _ in range(level - 1):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cur_file = os.path.dirname(cur_file)
            cur_file = os.path.dirname(cur_file)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cur_name = relative_import_path.lstrip(".")
        cur_name = relative_import_path.lstrip(".")
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for part in cur_name.split("."):
        for part in cur_name.split("."):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cur_file = os.path.join(cur_file, part)
            cur_file = os.path.join(cur_file, part)
        # 中文说明：根据条件选择执行分支；代码：if not cur_file.endswith(".py"):
        if not cur_file.endswith(".py"):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cur_file += ".py"
            cur_file += ".py"
        # 中文说明：根据条件选择执行分支；代码：if not PathManager.isfile(cur_file):
        if not PathManager.isfile(cur_file):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cur_file_no_suffix = cur_file[: -len(".py")]
            cur_file_no_suffix = cur_file[: -len(".py")]
            # 中文说明：根据条件选择执行分支；代码：if PathManager.isdir(cur_file_no_suffix):
            if PathManager.isdir(cur_file_no_suffix):
                # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ImportError(f"Cannot import from {cur_file_no_suffix}." + relative_import_err)
                raise ImportError(f"Cannot import from {cur_file_no_suffix}." + relative_import_err)
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ImportError(
                raise ImportError(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Cannot import name {relative_import_path} from " f"{original_file}: {cur_file} does not exi...
                    f"Cannot import name {relative_import_path} from " f"{original_file}: {cur_file} does not exist."
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return cur_file
        return cur_file

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def new_import(name, globals=None, locals=None, fromlist=(), level=0):
    def new_import(name, globals=None, locals=None, fromlist=(), level=0):
        # 中文说明：根据条件选择执行分支；代码：if (
        if (
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Only deal with relative imports inside config files
            # Only deal with relative imports inside config files
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：level != 0
            level != 0
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：and globals is not None
            and globals is not None
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：and (globals.get("__package__", "") or "").startswith(_CFG_PACKAGE_NAME)
            and (globals.get("__package__", "") or "").startswith(_CFG_PACKAGE_NAME)
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
        ):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cur_file = find_relative_file(globals["__file__"], name, level)
            cur_file = find_relative_file(globals["__file__"], name, level)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_validate_py_syntax(cur_file)
            _validate_py_syntax(cur_file)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：spec = importlib.machinery.ModuleSpec(_random_package_name(cur_file), None, origin=cur_file)
            spec = importlib.machinery.ModuleSpec(_random_package_name(cur_file), None, origin=cur_file)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：module = importlib.util.module_from_spec(spec)
            module = importlib.util.module_from_spec(spec)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：module.__file__ = cur_file
            module.__file__ = cur_file
            # 中文说明：处理异常、清理资源或管理上下文；代码：with PathManager.open(cur_file) as f:
            with PathManager.open(cur_file) as f:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：content = f.read()
                content = f.read()
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：exec(compile(content, cur_file, "exec"), module.__dict__)
            exec(compile(content, cur_file, "exec"), module.__dict__)
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for name in fromlist: # turn imported dict into DictConfig automatically
            for name in fromlist:  # turn imported dict into DictConfig automatically
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：val = _cast_to_config(module.__dict__[name])
                val = _cast_to_config(module.__dict__[name])
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：module.__dict__[name] = val
                module.__dict__[name] = val
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return module
            return module
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return old_import(name, globals, locals, fromlist=fromlist, level=level)
        return old_import(name, globals, locals, fromlist=fromlist, level=level)

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：builtins.__import__ = new_import
    builtins.__import__ = new_import
    # 中文说明：从生成器逐步产生本行指定的值；代码：yield new_import
    yield new_import
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：builtins.__import__ = old_import
    builtins.__import__ = old_import


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class LazyConfig:
class LazyConfig:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Provide methods to save, load, and overrides an omegaconf config object
    which may contain definition of lazily-constructed objects.
    """

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def load_rel(filename: str, keys: Union[None, str, Tuple[str, ...]] = None):
    def load_rel(filename: str, keys: Union[None, str, Tuple[str, ...]] = None):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Similar to :meth:`load()`, but load path relative to the caller's
        source file.

        This has the same functionality as a relative import, except that this method
        accepts filename as a string, so more characters are allowed in the filename.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：caller_frame = inspect.stack()[1]
        caller_frame = inspect.stack()[1]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：caller_fname = caller_frame[0].f_code.co_filename
        caller_fname = caller_frame[0].f_code.co_filename
        # 中文说明：检查运行时假设是否成立；代码：assert caller_fname != "<string>", "load_rel Unable to find caller"
        assert caller_fname != "<string>", "load_rel Unable to find caller"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：caller_dir = os.path.dirname(caller_fname)
        caller_dir = os.path.dirname(caller_fname)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：filename = os.path.join(caller_dir, filename)
        filename = os.path.join(caller_dir, filename)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return LazyConfig.load(filename, keys)
        return LazyConfig.load(filename, keys)

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def load(filename: str, keys: Union[None, str, Tuple[str, ...]] = None):
    def load(filename: str, keys: Union[None, str, Tuple[str, ...]] = None):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Load a config file.

        Args:
            filename: absolute path or relative path w.r.t. the current working directory
            keys: keys to load and return. If not given, return all keys
                (whose values are config objects) in a dict.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：has_keys = keys is not None
        has_keys = keys is not None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：filename = filename.replace("/./", "/") # redundant
        filename = filename.replace("/./", "/")  # redundant
        # 中文说明：根据条件选择执行分支；代码：if os.path.splitext(filename)[1] not in [".py", ".yaml", ".yml"]:
        if os.path.splitext(filename)[1] not in [".py", ".yaml", ".yml"]:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Config file {filename} has to be a python or yaml file.")
            raise ValueError(f"Config file {filename} has to be a python or yaml file.")
        # 中文说明：根据条件选择执行分支；代码：if filename.endswith(".py"):
        if filename.endswith(".py"):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_validate_py_syntax(filename)
            _validate_py_syntax(filename)

            # 中文说明：处理异常、清理资源或管理上下文；代码：with _patch_import():
            with _patch_import():
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Record the filename
                # Record the filename
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：module_namespace = {
                module_namespace = {
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："__file__": filename,
                    "__file__": filename,
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："__package__": _random_package_name(filename),
                    "__package__": _random_package_name(filename),
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
                }
                # 中文说明：处理异常、清理资源或管理上下文；代码：with PathManager.open(filename) as f:
                with PathManager.open(filename) as f:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：content = f.read()
                    content = f.read()
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Compile first with filename to:
                # Compile first with filename to:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 1. make filename appears in stacktrace
                # 1. make filename appears in stacktrace
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 2. make load_rel able to find its parent's (possibly remote) location
                # 2. make load_rel able to find its parent's (possibly remote) location
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：exec(compile(content, filename, "exec"), module_namespace)
                exec(compile(content, filename, "exec"), module_namespace)

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ret = module_namespace
            ret = module_namespace
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：处理异常、清理资源或管理上下文；代码：with PathManager.open(filename) as f:
            with PathManager.open(filename) as f:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：obj = yaml.unsafe_load(f)
                obj = yaml.unsafe_load(f)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ret = OmegaConf.create(obj, flags={"allow_objects": True})
            ret = OmegaConf.create(obj, flags={"allow_objects": True})

        # 中文说明：根据条件选择执行分支；代码：if has_keys:
        if has_keys:
            # 中文说明：根据条件选择执行分支；代码：if isinstance(keys, str):
            if isinstance(keys, str):
                # 中文说明：从当前函数返回结果或结束函数执行；代码：return _cast_to_config(ret[keys])
                return _cast_to_config(ret[keys])
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：从当前函数返回结果或结束函数执行；代码：return tuple(_cast_to_config(ret[a]) for a in keys)
                return tuple(_cast_to_config(ret[a]) for a in keys)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：根据条件选择执行分支；代码：if filename.endswith(".py"):
            if filename.endswith(".py"):
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# when not specified, only load those that are config objects
                # when not specified, only load those that are config objects
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ret = DictConfig(
                ret = DictConfig(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{
                    {
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：name: _cast_to_config(value)
                        name: _cast_to_config(value)
                        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for name, value in ret.items()
                        for name, value in ret.items()
                        # 中文说明：根据条件选择执行分支；代码：if isinstance(value, (DictConfig, ListConfig, dict)) and not name.startswith("_")
                        if isinstance(value, (DictConfig, ListConfig, dict)) and not name.startswith("_")
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：},
                    },
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：flags={"allow_objects": True},
                    flags={"allow_objects": True},
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return ret
            return ret

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def save_pkl(cfg, filename: str) -> str:
    def save_pkl(cfg, filename: str) -> str:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Saves a Config object to a file using pickle serialization. This method is typically used
        when the configuration object contains complex objects, such as lambdas, that are not supported by
        simpler serialization methods like YAML. The function attempts to create a deep copy of the configuration
        object before serialization to ensure that the original object remains unmodified.

        Args:
            cfg: A Config object to be serialized and saved.
            filename: The path and name of the file where the configuration should be saved. The function
                      assumes the file extension indicates a pickle format (e.g., .pkl).

        Returns:
            str: The filename to which the configuration was saved. This can be used to verify the file location
                 or log the outcome.

        Notes:
            - The function logs a warning if the configuration is successfully saved using pickle.
            - If saving fails, an error is logged with the exception details.
        """
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cfg = deepcopy(cfg)
            cfg = deepcopy(cfg)
        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception:
        except Exception:
            # 中文说明：执行循环控制或空操作；代码：pass
            pass

        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：处理异常、清理资源或管理上下文；代码：with PathManager.open(filename, "wb") as f:
            with PathManager.open(filename, "wb") as f:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pickle.dump(cfg, f)
                pickle.dump(cfg, f)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(f"Config is saved using pickle at {filename}.")
            log.warning(f"Config is saved using pickle at {filename}.")
        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
        except Exception as e:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.error(f"Failed to save config to {filename}: {e}. Trying dill or cloudpickle instead")
            log.error(f"Failed to save config to {filename}: {e}. Trying dill or cloudpickle instead")
            # 中文说明：根据条件选择执行分支；代码：if dill_pickle:
            if dill_pickle:
                # 中文说明：开始一个可捕获异常的代码块；代码：try:
                try:
                    # 中文说明：处理异常、清理资源或管理上下文；代码：with PathManager.open(filename, "wb") as f:
                    with PathManager.open(filename, "wb") as f:
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pickle.dump(dill_pickle.dumps(cfg, recurse=True), f)
                        pickle.dump(dill_pickle.dumps(cfg, recurse=True), f)
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(f"Config is saved using dill at {filename}.")
                        log.warning(f"Config is saved using dill at {filename}.")
                # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
                except Exception as e:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.error(f"Failed to save config to {filename}: {e}.")
                    log.error(f"Failed to save config to {filename}: {e}.")
                    # 中文说明：根据条件选择执行分支；代码：if cloudpickle:
                    if cloudpickle:
                        # 中文说明：开始一个可捕获异常的代码块；代码：try:
                        try:
                            # 中文说明：处理异常、清理资源或管理上下文；代码：with PathManager.open(filename, "wb") as f:
                            with PathManager.open(filename, "wb") as f:
                                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pickle.dump(cloudpickle.dumps(cfg), f)
                                pickle.dump(cloudpickle.dumps(cfg), f)
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(f"Config is saved using cloudpickle at {filename}.")
                            log.warning(f"Config is saved using cloudpickle at {filename}.")
                        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
                        except Exception as e:
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.error(f"Failed to save config to {filename}: {e}.")
                            log.error(f"Failed to save config to {filename}: {e}.")
                    # 中文说明：根据条件选择执行分支；代码：else:
                    else:
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.error("cloudpickle is not available. Cannot save the config.")
                        log.error("cloudpickle is not available. Cannot save the config.")
                        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise e
                        raise e

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return filename
        return filename

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def save_yaml(cfg, filename: str) -> str:
    def save_yaml(cfg, filename: str) -> str:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Saves a Config object to a file using YAML serialization. This method is beneficial when the configuration object's content needs to be human-readable and easily editable. YAML is suitable for configurations that do not contain complex types like lambdas, which must be handled differently. The function converts unserializable items to strings before saving to ensure compatibility with YAML serialization.

        Args:
            cfg: A Config object to be serialized and saved. It handles both DictConfig and ListConfig types.
            filename: The path and name of the file where the configuration should be saved. The function does not require a specific file extension but typically uses '.yaml'.

        Returns:
            str: The filename to which the configuration was saved. This can be used to verify the file location or log the outcome.

        Notes:
            - The function logs a warning if the configuration is successfully saved using YAML.
            - If saving fails, an error is logged with the exception details.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：logger = logging.getLogger(__name__)
        logger = logging.getLogger(__name__)
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cfg = deepcopy(cfg)
            cfg = deepcopy(cfg)
        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception:
        except Exception:
            # 中文说明：执行循环控制或空操作；代码：pass
            pass

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Define a function to check if an item is serializable to YAML
        # Define a function to check if an item is serializable to YAML
        # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_serializable(item):
        def is_serializable(item):
            # 中文说明：开始一个可捕获异常的代码块；代码：try:
            try:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：OmegaConf.to_yaml(item)
                OmegaConf.to_yaml(item)
                # 中文说明：从当前函数返回结果或结束函数执行；代码：return True
                return True
            # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
            except Exception as e:
                # 中文说明：从当前函数返回结果或结束函数执行；代码：return False
                return False

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Function to convert unserializable items to strings
        # Function to convert unserializable items to strings
        # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def serialize_config(config):
        def serialize_config(config):
            # 中文说明：根据条件选择执行分支；代码：if isinstance(config, DictConfig):
            if isinstance(config, DictConfig):
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key, value in config.items():
                for key, value in config.items():
                    # 中文说明：根据条件选择执行分支；代码：if isinstance(value, (DictConfig, ListConfig)):
                    if isinstance(value, (DictConfig, ListConfig)):
                        # 中文说明：开始一个可捕获异常的代码块；代码：try:
                        try:
                            # 中文说明：根据条件选择执行分支；代码：if "_target_" in value:
                            if "_target_" in value:
                                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default_params = get_default_params(value["_target_"])
                                default_params = get_default_params(value["_target_"])
                                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for default_key, default_v in default_params.items():
                                for default_key, default_v in default_params.items():
                                    # 中文说明：根据条件选择执行分支；代码：if default_key not in value:
                                    if default_key not in value:
                                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：value[default_key] = default_v
                                        value[default_key] = default_v
                        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
                        except Exception as e:
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.error(f"Failed to add default argument values: {e}")
                            log.error(f"Failed to add default argument values: {e}")

                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：serialize_config(value)
                        serialize_config(value)
                    # 中文说明：根据条件选择执行分支；代码：else:
                    else:
                        # 中文说明：根据条件选择执行分支；代码：if not is_serializable(value) and value is not None:
                        if not is_serializable(value) and value is not None:
                            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config[key] = str(value)
                            config[key] = str(value)
            # 中文说明：根据条件选择执行分支；代码：elif isinstance(config, ListConfig):
            elif isinstance(config, ListConfig):
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i, item in enumerate(config):
                for i, item in enumerate(config):
                    # 中文说明：根据条件选择执行分支；代码：if isinstance(item, (DictConfig, ListConfig)):
                    if isinstance(item, (DictConfig, ListConfig)):
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：serialize_config(item)
                        serialize_config(item)
                    # 中文说明：根据条件选择执行分支；代码：else:
                    else:
                        # 中文说明：根据条件选择执行分支；代码：if not is_serializable(item) and item is not None:
                        if not is_serializable(item) and item is not None:
                            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config[i] = str(item)
                            config[i] = str(item)
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise NotImplementedError("Input config must be a DictConfig or ListConfig.")
                raise NotImplementedError("Input config must be a DictConfig or ListConfig.")
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return config
            return config

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Convert Config object to a DictConfig object.
        # Convert Config object to a DictConfig object.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config_dict = attrs.asdict(cfg)
        config_dict = attrs.asdict(cfg)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config_omegaconf = DictConfig(content=config_dict, flags={"allow_objects": True})
        config_omegaconf = DictConfig(content=config_dict, flags={"allow_objects": True})

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Serialize the DictConfig object by converting non-serializable objects to strings.
        # Serialize the DictConfig object by converting non-serializable objects to strings.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config_omegaconf = serialize_config(config_omegaconf)
        config_omegaconf = serialize_config(config_omegaconf)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：config_dict: Dict[str, Any] = OmegaConf.to_container(config_omegaconf, resolve=True)
        config_dict: Dict[str, Any] = OmegaConf.to_container(config_omegaconf, resolve=True)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sorted_config: OrderedDict[str, Any] = sort_recursive(config_dict)
        sorted_config: OrderedDict[str, Any] = sort_recursive(config_dict)
        # 中文说明：处理异常、清理资源或管理上下文；代码：with open(filename, "w") as f:
        with open(filename, "w") as f:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：yaml.dump(sorted_config, f, default_flow_style=False)
            yaml.dump(sorted_config, f, default_flow_style=False)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(f"Config is saved using omegaconf at {filename}.")
        log.warning(f"Config is saved using omegaconf at {filename}.")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return filename
        return filename
