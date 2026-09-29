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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import collections.abc as abc
import collections.abc as abc
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import dataclasses
import dataclasses
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any
from typing import Any

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import attrs
import attrs

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config.registry import _convert_target_to_string, locate
from imaginaire.lazy_config.registry import _convert_target_to_string, locate
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：__all__ = ["dump_dataclass", "instantiate"]
__all__ = ["dump_dataclass", "instantiate"]


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_dataclass_or_attrs(target):
def is_dataclass_or_attrs(target):
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return dataclasses.is_dataclass(target) or attrs.has(target)
    return dataclasses.is_dataclass(target) or attrs.has(target)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def dump_dataclass(obj: Any):
def dump_dataclass(obj: Any):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Dump a dataclass recursively into a dict that can be later instantiated.

    Args:
        obj: a dataclass object

    Returns:
        dict
    """
    # 中文说明：检查运行时假设是否成立；代码：assert dataclasses.is_dataclass(obj) and not isinstance(
    assert dataclasses.is_dataclass(obj) and not isinstance(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：obj, type
        obj, type
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), "dump_dataclass() requires an instance of a dataclass."
    ), "dump_dataclass() requires an instance of a dataclass."
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ret = {"_target_": _convert_target_to_string(type(obj))}
    ret = {"_target_": _convert_target_to_string(type(obj))}
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for f in dataclasses.fields(obj):
    for f in dataclasses.fields(obj):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：v = getattr(obj, f.name)
        v = getattr(obj, f.name)
        # 中文说明：根据条件选择执行分支；代码：if dataclasses.is_dataclass(v):
        if dataclasses.is_dataclass(v):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：v = dump_dataclass(v)
            v = dump_dataclass(v)
        # 中文说明：根据条件选择执行分支；代码：if isinstance(v, (list, tuple)):
        if isinstance(v, (list, tuple)):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：v = [dump_dataclass(x) if dataclasses.is_dataclass(x) else x for x in v]
            v = [dump_dataclass(x) if dataclasses.is_dataclass(x) else x for x in v]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ret[f.name] = v
        ret[f.name] = v
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return ret
    return ret


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def instantiate(cfg, *args, **kwargs):
def instantiate(cfg, *args, **kwargs):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Recursively instantiate objects defined in dictionaries by
    "_target_" and arguments.

    Args:
        cfg: a dict-like object with "_target_" that defines the caller, and
            other keys that define the arguments
        args: Optional positional parameters pass-through.
        kwargs: Optional named parameters pass-through.

    Returns:
        object instantiated by cfg
    """
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from omegaconf import DictConfig, ListConfig, OmegaConf
    from omegaconf import DictConfig, ListConfig, OmegaConf

    # 中文说明：根据条件选择执行分支；代码：if isinstance(cfg, ListConfig):
    if isinstance(cfg, ListConfig):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lst = [instantiate(x) for x in cfg]
        lst = [instantiate(x) for x in cfg]
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return ListConfig(lst, flags={"allow_objects": True})
        return ListConfig(lst, flags={"allow_objects": True})
    # 中文说明：根据条件选择执行分支；代码：if isinstance(cfg, list):
    if isinstance(cfg, list):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Specialize for list, because many classes take
        # Specialize for list, because many classes take
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# list[objects] as arguments, such as ResNet, DatasetMapper
        # list[objects] as arguments, such as ResNet, DatasetMapper
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return [instantiate(x) for x in cfg]
        return [instantiate(x) for x in cfg]

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# If input is a DictConfig backed by dataclasses (i.e. omegaconf's structured config),
    # If input is a DictConfig backed by dataclasses (i.e. omegaconf's structured config),
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# instantiate it to the actual dataclass.
    # instantiate it to the actual dataclass.
    # 中文说明：根据条件选择执行分支；代码：if isinstance(cfg, DictConfig) and is_dataclass_or_attrs(cfg._metadata.object_type):
    if isinstance(cfg, DictConfig) and is_dataclass_or_attrs(cfg._metadata.object_type):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return OmegaConf.to_object(cfg)
        return OmegaConf.to_object(cfg)

    # 中文说明：根据条件选择执行分支；代码：if isinstance(cfg, abc.Mapping) and "_target_" in cfg:
    if isinstance(cfg, abc.Mapping) and "_target_" in cfg:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# conceptually equivalent to hydra.utils.instantiate(cfg) with _convert_=all,
        # conceptually equivalent to hydra.utils.instantiate(cfg) with _convert_=all,
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# but faster: https://github.com/facebookresearch/hydra/issues/1200
        # but faster: https://github.com/facebookresearch/hydra/issues/1200
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_recursive = getattr(cfg, "_recursive_", True)
        is_recursive = getattr(cfg, "_recursive_", True)
        # 中文说明：根据条件选择执行分支；代码：if is_recursive:
        if is_recursive:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cfg = {k: instantiate(v) for k, v in cfg.items()}
            cfg = {k: instantiate(v) for k, v in cfg.items()}
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cfg = {k: v for k, v in cfg.items()}
            cfg = {k: v for k, v in cfg.items()}
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# pop the _recursive_ key to avoid passing it as a parameter
        # pop the _recursive_ key to avoid passing it as a parameter
        # 中文说明：根据条件选择执行分支；代码：if "_recursive_" in cfg:
        if "_recursive_" in cfg:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cfg.pop("_recursive_")
            cfg.pop("_recursive_")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cls = cfg.pop("_target_")
        cls = cfg.pop("_target_")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cls = instantiate(cls)
        cls = instantiate(cls)

        # 中文说明：根据条件选择执行分支；代码：if isinstance(cls, str):
        if isinstance(cls, str):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cls_name = cls
            cls_name = cls
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cls = locate(cls_name)
            cls = locate(cls_name)
            # 中文说明：检查运行时假设是否成立；代码：assert cls is not None, cls_name
            assert cls is not None, cls_name
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：开始一个可捕获异常的代码块；代码：try:
            try:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cls_name = cls.__module__ + "." + cls.__qualname__
                cls_name = cls.__module__ + "." + cls.__qualname__
            # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception:
            except Exception:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# target could be anything, so the above could fail
                # target could be anything, so the above could fail
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cls_name = str(cls)
                cls_name = str(cls)
        # 中文说明：检查运行时假设是否成立；代码：assert callable(cls), f"_target_ {cls} does not define a callable object"
        assert callable(cls), f"_target_ {cls} does not define a callable object"
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# override config with kwargs
            # override config with kwargs
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：instantiate_kwargs = {}
            instantiate_kwargs = {}
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：instantiate_kwargs.update(cfg)
            instantiate_kwargs.update(cfg)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：instantiate_kwargs.update(kwargs)
            instantiate_kwargs.update(kwargs)
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return cls(*args, **instantiate_kwargs)
            return cls(*args, **instantiate_kwargs)
        # 中文说明：处理异常、清理资源或管理上下文；代码：except TypeError:
        except TypeError:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.error(f"Error when instantiating {cls_name}!")
            log.error(f"Error when instantiating {cls_name}!")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：raise
            raise
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return cfg # return as-is if don't know what to do
    return cfg  # return as-is if don't know what to do
