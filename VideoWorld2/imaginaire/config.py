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
# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Training config system for Imaginare4"""
"""Training config system for Imaginare4"""

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from __future__ import annotations
from __future__ import annotations

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any, Dict, Optional, Type, TypeVar, Union
from typing import Any, Dict, Optional, Type, TypeVar, Union

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import attrs
import attrs
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.utils.data
import torch.utils.data
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.utils.data.distributed
import torch.utils.data.distributed

# 中文说明：开始一个可捕获异常的代码块；代码：try:
try:
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from megatron.core import ModelParallelConfig
    from megatron.core import ModelParallelConfig

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：USE_MEGATRON = True
    USE_MEGATRON = True
# 中文说明：处理异常、清理资源或管理上下文；代码：except ImportError:
except ImportError:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：USE_MEGATRON = False
    USE_MEGATRON = False
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print("Megatron-core is not installed.")
    print("Megatron-core is not installed.")

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import LazyCall as L
from imaginaire.lazy_config import LazyCall as L
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import LazyDict
from imaginaire.lazy_config import LazyDict
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import callback, distributed
from imaginaire.utils import callback, distributed
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.misc import Color
from imaginaire.utils.misc import Color

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：T = TypeVar("T")
T = TypeVar("T")


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _is_attrs_instance(obj: object) -> bool:
def _is_attrs_instance(obj: object) -> bool:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Helper function to check if an object is an instance of an attrs-defined class.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is an instance of an attrs-defined class, False otherwise.
    """
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return hasattr(obj, "__attrs_attrs__")
    return hasattr(obj, "__attrs_attrs__")


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def make_freezable(cls: T) -> T:
def make_freezable(cls: T) -> T:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    A decorator that adds the capability to freeze instances of an attrs-defined class.

    NOTE: This requires the wrapped attrs to be defined with attrs.define(slots=False) because we need
    to hack on a "_is_frozen" attribute.

    This decorator enhances an attrs-defined class with the ability to be "frozen" at runtime.
    Once an instance is frozen, its attributes cannot be changed. It also recursively freezes
    any attrs-defined objects that are attributes of the class.

    Usage:
        @make_freezable
        @attrs.define(slots=False)
        class MyClass:
            attribute1: int
            attribute2: str

        obj = MyClass(1, 'a')
        obj.freeze()  # Freeze the instance
        obj.attribute1 = 2  # Raises AttributeError

    Args:
        cls: The class to be decorated.

    Returns:
        The decorated class with added freezing capability.
    """

    # 中文说明：根据条件选择执行分支；代码：if not hasattr(cls, "__dict__"):
    if not hasattr(cls, "__dict__"):
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError(
        raise TypeError(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："make_freezable cannot be used with classes that do not define __dict__. Make sure that the w...
            "make_freezable cannot be used with classes that do not define __dict__. Make sure that the wrapped "
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："class was defined with `@attrs.define(slots=False)`"
            "class was defined with `@attrs.define(slots=False)`"
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：original_setattr = cls.__setattr__
    original_setattr = cls.__setattr__

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def setattr_override(self, key, value) -> None: # noqa: ANN001
    def setattr_override(self, key, value) -> None:  # noqa: ANN001
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Override __setattr__ to allow modifications during initialization
        and prevent modifications once the instance is frozen.
        """
        # 中文说明：根据条件选择执行分支；代码：if hasattr(self, "_is_frozen") and self._is_frozen and key != "_is_frozen":
        if hasattr(self, "_is_frozen") and self._is_frozen and key != "_is_frozen":
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise AttributeError("Cannot modify frozen instance")
            raise AttributeError("Cannot modify frozen instance")
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：original_setattr(self, key, value) # type: ignore
        original_setattr(self, key, value)  # type: ignore

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cls.__setattr__ = setattr_override # type: ignore
    cls.__setattr__ = setattr_override  # type: ignore

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def freeze(self: object) -> None:
    def freeze(self: object) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Freeze the instance and all its attrs-defined attributes.
        """
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _, value in attrs.asdict(self, recurse=False).items():
        for _, value in attrs.asdict(self, recurse=False).items():
            # 中文说明：根据条件选择执行分支；代码：if _is_attrs_instance(value) and hasattr(value, "freeze"):
            if _is_attrs_instance(value) and hasattr(value, "freeze"):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：value.freeze()
                value.freeze()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._is_frozen = True # type: ignore
        self._is_frozen = True  # type: ignore

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cls.freeze = freeze # type: ignore
    cls.freeze = freeze  # type: ignore

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return cls
    return cls


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _pretty_print_attrs_instance(obj: object, indent: int = 0, use_color: bool = False) -> str:
def _pretty_print_attrs_instance(obj: object, indent: int = 0, use_color: bool = False) -> str:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Recursively pretty prints attrs objects with color.
    """

    # 中文说明：检查运行时假设是否成立；代码：assert attrs.has(obj.__class__)
    assert attrs.has(obj.__class__)

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：lines: list[str] = []
    lines: list[str] = []
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for attribute in attrs.fields(obj.__class__):
    for attribute in attrs.fields(obj.__class__):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：value = getattr(obj, attribute.name)
        value = getattr(obj, attribute.name)
        # 中文说明：根据条件选择执行分支；代码：if attrs.has(value.__class__):
        if attrs.has(value.__class__):
            # 中文说明：根据条件选择执行分支；代码：if use_color:
            if use_color:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：lines.append(" " * indent + Color.cyan("* ") + Color.green(attribute.name) + ":")
                lines.append("   " * indent + Color.cyan("* ") + Color.green(attribute.name) + ":")
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：lines.append(" " * indent + "* " + attribute.name + ":")
                lines.append("   " * indent + "* " + attribute.name + ":")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：lines.append(_pretty_print_attrs_instance(value, indent + 1, use_color))
            lines.append(_pretty_print_attrs_instance(value, indent + 1, use_color))
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：根据条件选择执行分支；代码：if use_color:
            if use_color:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：lines.append(
                lines.append(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：" " * indent + Color.cyan("* ") + Color.green(attribute.name) + ": " + Color.yellow(value)
                    "   " * indent + Color.cyan("* ") + Color.green(attribute.name) + ": " + Color.yellow(value)
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：lines.append(" " * indent + "* " + attribute.name + ": " + str(value))
                lines.append("   " * indent + "* " + attribute.name + ": " + str(value))
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return "\n".join(lines)
    return "\n".join(lines)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def pretty_print_overrides(overrides: Optional[list[str]] = None, use_color: bool = False) ->...
def pretty_print_overrides(overrides: Optional[list[str]] = None, use_color: bool = False) -> str:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Pretty prints overrides.
    """

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：lines: list[str] = []
    lines: list[str] = []
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：lines.append(Color.cyan("* ") + Color.green("overrides") + ": ")
    lines.append(Color.cyan("* ") + Color.green("overrides") + ": ")
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for override in overrides:
    for override in overrides:
        # 中文说明：根据条件选择执行分支；代码：if override == "--":
        if override == "--":
            # 中文说明：执行循环控制或空操作；代码：continue
            continue
        # 中文说明：根据条件选择执行分支；代码：if override.startswith("~"):
        if override.startswith("~"):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attribute_name = override[1:]
            attribute_name = override[1:]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attribute_value = None
            attribute_value = None
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：attribute_name, attribute_value = override.split("=")
            attribute_name, attribute_value = override.split("=")
        # 中文说明：根据条件选择执行分支；代码：if use_color:
        if use_color:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：lines.append(" " + Color.cyan("* ") + Color.green(attribute_name) + ": " + Color.yellow(attri...
            lines.append("   " + Color.cyan("* ") + Color.green(attribute_name) + ": " + Color.yellow(attribute_value))
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：lines.append(" " + "* " + attribute_name + ": " + str(attribute_value))
            lines.append("   " + "* " + attribute_name + ": " + str(attribute_value))

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return "\n".join(lines)
    return "\n".join(lines)


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@make_freezable
@make_freezable
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False) # slots=False is required for make_freezable. See the make_freezab...
@attrs.define(slots=False)  # slots=False is required for make_freezable. See the make_freezable notes for more info.
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ObjectStoreConfig:
class ObjectStoreConfig:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Whether the file I/O is from object store instead of local disk.
    # Whether the file I/O is from object store instead of local disk.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：enabled: bool = False
    enabled: bool = False
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Path to the object store credentials file.
    # Path to the object store credentials file.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：credentials: str = ""
    credentials: str = ""
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Object store bucket to read from / write to the objects.
    # Object store bucket to read from / write to the objects.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：bucket: str = ""
    bucket: str = ""


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@make_freezable
@make_freezable
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class JobConfig:
class JobConfig:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Project name.
    # Project name.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：project: str = ""
    project: str = ""
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Experiment name.
    # Experiment name.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group: str = ""
    group: str = ""
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Run/job name.
    # Run/job name.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：name: str = ""
    name: str = ""

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def path(self) -> str:
    def path(self) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return f"{self.project}/{self.group}/{self.name}"
        return f"{self.project}/{self.group}/{self.name}"

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def path_local(self) -> str:
    def path_local(self) -> str:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：local_root = os.environ.get("IMAGINAIRE_OUTPUT_ROOT", "checkpoints")
        local_root = os.environ.get("IMAGINAIRE_OUTPUT_ROOT", "checkpoints")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return f"{local_root}/{self.path}"
        return f"{local_root}/{self.path}"


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@make_freezable
@make_freezable
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class EMAConfig:
class EMAConfig:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Enable tracking a set of exponential moving average (EMA) weights.
    # Enable tracking a set of exponential moving average (EMA) weights.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：enabled: bool = False
    enabled: bool = False
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# EMA decay rate.
    # EMA decay rate.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：beta: float = 0.9999
    beta: float = 0.9999
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Enable removing "_orig_mod-" from buffer names that is added by torch.compile
    # Enable removing "_orig_mod-" from buffer names that is added by torch.compile
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：torch_compile_buffer_renaming: bool = False
    torch_compile_buffer_renaming: bool = False


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@make_freezable
@make_freezable
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class PowerEMAConfig:
class PowerEMAConfig:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Enable tracking a set of exponential moving average (EMA) weights.
    # Enable tracking a set of exponential moving average (EMA) weights.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：enabled: bool = False
    enabled: bool = False
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# EDM2 paper EMA decay rate.
    # EDM2 paper EMA decay rate.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：s: float = 0.1
    s: float = 0.1
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Enable removing "_orig_mod-" from buffer names that is added by torch.compile
    # Enable removing "_orig_mod-" from buffer names that is added by torch.compile
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：torch_compile_buffer_renaming: bool = False
    torch_compile_buffer_renaming: bool = False


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@make_freezable
@make_freezable
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class DDPConfig:
class DDPConfig:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Traverse the computation graph to find parameters that don't receive gradients.
    # Traverse the computation graph to find parameters that don't receive gradients.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：find_unused_parameters: bool = False
    find_unused_parameters: bool = False
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Set to True if the computation graph does not change during the whole training loop.
    # Set to True if the computation graph does not change during the whole training loop.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：static_graph: bool = True
    static_graph: bool = True
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Set to True if we want to synchronize buffers. Set to False if the sync is going to be hand...
    # Set to True if we want to synchronize buffers. Set to False if the sync is going to be handled elsewhere.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：broadcast_buffers: bool = True
    broadcast_buffers: bool = True


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@make_freezable
@make_freezable
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class CuDNNConfig:
class CuDNNConfig:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Set to True for better reproducibility of the results (only using deterministic cudnn funct...
    # Set to True for better reproducibility of the results (only using deterministic cudnn functions).
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：deterministic: bool = False
    deterministic: bool = False
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# If set to True, cudnn will benchmark several algorithms and pick the fastest one.
    # If set to True, cudnn will benchmark several algorithms and pick the fastest one.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：benchmark: bool = True
    benchmark: bool = True


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@make_freezable
@make_freezable
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class JITConfig:
class JITConfig:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Enable exporting a JIT compiled model.
    # Enable exporting a JIT compiled model.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：enabled: bool = False
    enabled: bool = False
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Input tensor shape, for example input.
    # Input tensor shape, for example input.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：input_shape: Union[list[int], None] = None
    input_shape: Union[list[int], None] = None
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Device to compile onto.
    # Device to compile onto.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：device: str = "cuda"
    device: str = "cuda"
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# # Data type to compile onto.
    # # Data type to compile onto.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dtype: str = "bfloat16"
    dtype: str = "bfloat16"
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Strict mode for PyTorch JIT.
    # Strict mode for PyTorch JIT.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：strict: bool = True
    strict: bool = True


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@make_freezable
@make_freezable
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class CheckpointConfig:
class CheckpointConfig:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# possible checkpoint class
    # possible checkpoint class
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：type: Optional[Dict] = None
    type: Optional[Dict] = None
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# for dcp, whether to use async mode
    # for dcp, whether to use async mode
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dcp_async_mode_enabled: bool = False
    dcp_async_mode_enabled: bool = False
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Save the checkpoint every N iterations.
    # Save the checkpoint every N iterations.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：save_iter: int = 999999999
    save_iter: int = 999999999
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Path of model weights to resume the checkpoint from.
    # Path of model weights to resume the checkpoint from.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：load_path: str = ""
    load_path: str = ""
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Whether to load the training states (optimizer/scheduler/grad-scaler) from the checkpoint p...
    # Whether to load the training states (optimizer/scheduler/grad-scaler) from the checkpoint path.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：load_training_state: bool = False
    load_training_state: bool = False
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Whether to load the scheduler state only from the checkpoint path. If load_training_state i...
    # Whether to load the scheduler state only from the checkpoint path. If load_training_state is True, this will be ignored.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：only_load_scheduler_state: bool = False
    only_load_scheduler_state: bool = False
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Load state_dict to the models in strict mode.
    # Load state_dict to the models in strict mode.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：strict_resume: bool = True
    strict_resume: bool = True
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Configs for JIT compiling EMA model.
    # Configs for JIT compiling EMA model.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：jit: JITConfig = attrs.field(factory=JITConfig)
    jit: JITConfig = attrs.field(factory=JITConfig)
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Print detailed information during checkpoint saving/loading.
    # Print detailed information during checkpoint saving/loading.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：verbose: bool = True
    verbose: bool = True
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# keys not to resume from the checkpoint, choices: ["model", "optim", "scheduler", "trainer"]
    # keys not to resume from the checkpoint, choices: ["model", "optim", "scheduler", "trainer"]
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：keys_not_to_resume: list[str] = []
    keys_not_to_resume: list[str] = []
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Whether to use the local filesystem for broadcasting checkpoint data (used for Tensor Paral...
    # Whether to use the local filesystem for broadcasting checkpoint data (used for Tensor Parallel Checkpointer).
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：broadcast_via_filesystem: bool = False
    broadcast_via_filesystem: bool = False
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：load_ema_to_reg: bool = False
    load_ema_to_reg: bool = False
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# In dcp planner, skip the weight shape check, load weights into the model even weight shape ...
    # In dcp planner, skip the weight shape check, load weights into the model even weight shape is different
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dcp_allow_mismatched_size: bool = False
    dcp_allow_mismatched_size: bool = False


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@make_freezable
@make_freezable
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class NVTXConfig:
class NVTXConfig:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Config for NVTX ranges used in the main training loop.
    """Config for NVTX ranges used in the main training loop.

    See tutorials/nanogpt for more details on how to integrate profiling into your model."""

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Enable the NVTX ranges.
    # Enable the NVTX ranges.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：enabled: bool = False
    enabled: bool = False
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Synchronize everything in each NVTX range.
    # Synchronize everything in each NVTX range.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cuda_synchronize: bool = False
    cuda_synchronize: bool = False


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@make_freezable
@make_freezable
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Profiling:
class Profiling:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：enable_profiling: bool = False
    enable_profiling: bool = False
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：enable_memory_snapshot: bool = False
    enable_memory_snapshot: bool = False
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：profile_freq: int = 1
    profile_freq: int = 1
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：first_n_rank: int = 8 # -1 means all ranks, n means first n ranks dumpy profiling info
    first_n_rank: int = 8  # -1 means all ranks, n means first n ranks dumpy profiling info
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：record_shape: bool = True
    record_shape: bool = True
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：profile_memory: bool = True
    profile_memory: bool = True
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：with_stack: bool = True
    with_stack: bool = True
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：with_modules: bool = True
    with_modules: bool = True


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@make_freezable
@make_freezable
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class TrainerConfig:
class TrainerConfig:
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.trainer import ImaginaireTrainer
    from imaginaire.trainer import ImaginaireTrainer

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：type: Type[ImaginaireTrainer] = ImaginaireTrainer
    type: Type[ImaginaireTrainer] = ImaginaireTrainer
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Set the callback class.
    # Set the callback class.
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Defaults to the callbacks below.
    # Defaults to the callbacks below.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：callbacks: LazyDict = LazyDict(
    callbacks: LazyDict = LazyDict(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dict(
        dict(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ema=L(callback.EMAModelCallback)(),
            ema=L(callback.EMAModelCallback)(),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：progress_bar=L(callback.ProgressBarCallback)(),
            progress_bar=L(callback.ProgressBarCallback)(),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# distributed parallelism strategy
    # distributed parallelism strategy
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：distributed_parallelism: str = "ddp"
    distributed_parallelism: str = "ddp"
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Distributed data parallel configs.
    # Distributed data parallel configs.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ddp: DDPConfig = attrs.field(factory=DDPConfig)
    ddp: DDPConfig = attrs.field(factory=DDPConfig)
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# cuDNN configs.
    # cuDNN configs.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cudnn: CuDNNConfig = attrs.field(factory=CuDNNConfig)
    cudnn: CuDNNConfig = attrs.field(factory=CuDNNConfig)
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Set the random seed.
    # Set the random seed.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：seed: int = 0
    seed: int = 0
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Gradient scaler arguments (for torch.amp.GradScaler).
    # Gradient scaler arguments (for torch.amp.GradScaler).
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：grad_scaler_args: dict = attrs.field(factory=lambda: dict(enabled=False))
    grad_scaler_args: dict = attrs.field(factory=lambda: dict(enabled=False))
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Maximum number of iterations to train the model.
    # Maximum number of iterations to train the model.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_iter: int = 999999999
    max_iter: int = 999999999
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Maximum number of iterations to validate the model. If None, validate on the entire dataset.
    # Maximum number of iterations to validate the model. If None, validate on the entire dataset.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_val_iter: int | None = None
    max_val_iter: int | None = None
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# How often we log the training stats.
    # How often we log the training stats.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：logging_iter: int = 100
    logging_iter: int = 100
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Whether we want to run the validation routines.
    # Whether we want to run the validation routines.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：run_validation: bool = True
    run_validation: bool = True
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# How often we evaluate on the validation set.
    # How often we evaluate on the validation set.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：validation_iter: int = 999999999
    validation_iter: int = 999999999
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Kill the process after N seconds since the last iteration (usually means dead job).
    # Kill the process after N seconds since the last iteration (usually means dead job).
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：timeout_period: int = 999999999
    timeout_period: int = 999999999
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Tensor memory organization format.
    # Tensor memory organization format.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：memory_format: torch.memory_format = torch.preserve_format
    memory_format: torch.memory_format = torch.preserve_format
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Gradient accumulation (update step every N iteration).
    # Gradient accumulation (update step every N iteration).
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：grad_accum_iter: int = 1
    grad_accum_iter: int = 1
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Profiling config
    # Profiling config
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：profiling: Profiling = attrs.field(factory=Profiling)
    profiling: Profiling = attrs.field(factory=Profiling)


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@make_freezable
@make_freezable
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Config:
class Config:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Config for an imaginaire4 job.
    """Config for an imaginaire4 job.

    See /README.md/Configuration System for more info.
    """

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Model configs.
    # Model configs.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model: LazyDict
    model: LazyDict
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Optimizer configs.
    # Optimizer configs.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：optimizer: LazyDict
    optimizer: LazyDict
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Scheduler configs.
    # Scheduler configs.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scheduler: LazyDict
    scheduler: LazyDict
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Training data configs.
    # Training data configs.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dataloader_train: LazyDict
    dataloader_train: LazyDict
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Validation data configs.
    # Validation data configs.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dataloader_val: LazyDict
    dataloader_val: LazyDict

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Training job configs.
    # Training job configs.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：job: JobConfig = attrs.field(factory=JobConfig)
    job: JobConfig = attrs.field(factory=JobConfig)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Trainer configs.
    # Trainer configs.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：trainer: TrainerConfig = attrs.field(factory=TrainerConfig)
    trainer: TrainerConfig = attrs.field(factory=TrainerConfig)

    # 中文说明：根据条件选择执行分支；代码：if USE_MEGATRON:
    if USE_MEGATRON:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Megatron-Core configs
        # Megatron-Core configs
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model_parallel: ModelParallelConfig = attrs.field(factory=ModelParallelConfig)
        model_parallel: ModelParallelConfig = attrs.field(factory=ModelParallelConfig)
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model_parallel: None = None
        model_parallel: None = None

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Checkpointer configs.
    # Checkpointer configs.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：checkpoint: CheckpointConfig = attrs.field(factory=CheckpointConfig)
    checkpoint: CheckpointConfig = attrs.field(factory=CheckpointConfig)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def pretty_print(self, use_color: bool = False) -> str:
    def pretty_print(self, use_color: bool = False) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return _pretty_print_attrs_instance(self, 0, use_color)
        return _pretty_print_attrs_instance(self, 0, use_color)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def to_dict(self) -> dict[str, Any]:
    def to_dict(self) -> dict[str, Any]:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return attrs.asdict(self)
        return attrs.asdict(self)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def validate(self) -> None:
    def validate(self) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Validate that the config has all required fields."""
        """Validate that the config has all required fields."""

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# broadcast job.name across all ranks to make sure it is consistent
        # broadcast job.name across all ranks to make sure it is consistent
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# otherwise, unaligned job names leads unaligned path to save checkpoints
        # otherwise, unaligned job names leads unaligned path to save checkpoints
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：job_name_tensor = torch.ByteTensor(bytearray(self.job.name, "utf-8")).cuda()
        job_name_tensor = torch.ByteTensor(bytearray(self.job.name, "utf-8")).cuda()
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：distributed.broadcast(job_name_tensor, 0)
        distributed.broadcast(job_name_tensor, 0)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.job.name = job_name_tensor.cpu().numpy().tobytes().decode("utf-8")
        self.job.name = job_name_tensor.cpu().numpy().tobytes().decode("utf-8")

        # 中文说明：检查运行时假设是否成立；代码：assert self.job.project != ""
        assert self.job.project != ""
        # 中文说明：检查运行时假设是否成立；代码：assert self.job.group != ""
        assert self.job.group != ""
        # 中文说明：检查运行时假设是否成立；代码：assert self.job.name != ""
        assert self.job.name != ""
