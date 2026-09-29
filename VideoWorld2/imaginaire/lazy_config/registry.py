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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import pydoc
import pydoc
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any
from typing import Any

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from fvcore.common.registry import Registry # for backward compatibility.
from fvcore.common.registry import Registry  # for backward compatibility.

# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
"""
``Registry`` and `locate` provide ways to map a string (typically found
in config files) to callable objects.
"""

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：__all__ = ["Registry", "locate"]
__all__ = ["Registry", "locate"]


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _convert_target_to_string(t: Any) -> str:
def _convert_target_to_string(t: Any) -> str:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Inverse of ``locate()``.

    Args:
        t: any object with ``__module__`` and ``__qualname__``
    """
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：module, qualname = t.__module__, t.__qualname__
    module, qualname = t.__module__, t.__qualname__

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Compress the path to this object, e.g. ``module.submodule._impl.class``
    # Compress the path to this object, e.g. ``module.submodule._impl.class``
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# may become ``module.submodule.class``, if the later also resolves to the same
    # may become ``module.submodule.class``, if the later also resolves to the same
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# object. This simplifies the string, and also is less affected by moving the
    # object. This simplifies the string, and also is less affected by moving the
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# class implementation.
    # class implementation.
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：module_parts = module.split(".")
    module_parts = module.split(".")
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for k in range(1, len(module_parts)):
    for k in range(1, len(module_parts)):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prefix = ".".join(module_parts[:k])
        prefix = ".".join(module_parts[:k])
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：candidate = f"{prefix}.{qualname}"
        candidate = f"{prefix}.{qualname}"
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：根据条件选择执行分支；代码：if locate(candidate) is t:
            if locate(candidate) is t:
                # 中文说明：从当前函数返回结果或结束函数执行；代码：return candidate
                return candidate
        # 中文说明：处理异常、清理资源或管理上下文；代码：except ImportError:
        except ImportError:
            # 中文说明：执行循环控制或空操作；代码：pass
            pass
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return f"{module}.{qualname}"
    return f"{module}.{qualname}"


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def locate(name: str) -> Any:
def locate(name: str) -> Any:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Locate and return an object ``x`` using an input string ``{x.__module__}.{x.__qualname__}``,
    such as "module.submodule.class_name".

    Raise Exception if it cannot be found.
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：obj = pydoc.locate(name)
    obj = pydoc.locate(name)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Some cases (e.g. torch.optim.sgd.SGD) not handled correctly
    # Some cases (e.g. torch.optim.sgd.SGD) not handled correctly
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# by pydoc.locate. Try a private function from hydra.
    # by pydoc.locate. Try a private function from hydra.
    # 中文说明：根据条件选择执行分支；代码：if obj is None:
    if obj is None:
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# from hydra.utils import get_method - will print many errors
            # from hydra.utils import get_method - will print many errors
            # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from hydra.utils import _locate
            from hydra.utils import _locate
        # 中文说明：处理异常、清理资源或管理上下文；代码：except ImportError as e:
        except ImportError as e:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ImportError(f"Cannot dynamically locate object {name}!") from e
            raise ImportError(f"Cannot dynamically locate object {name}!") from e
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：obj = _locate(name) # it raises if fails
            obj = _locate(name)  # it raises if fails

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return obj
    return obj
