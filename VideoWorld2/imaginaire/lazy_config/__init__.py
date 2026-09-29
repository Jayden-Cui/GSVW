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

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from omegaconf import DictConfig, OmegaConf
from omegaconf import DictConfig, OmegaConf

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config.instantiate import instantiate
from imaginaire.lazy_config.instantiate import instantiate
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config.lazy import LazyCall, LazyConfig
from imaginaire.lazy_config.lazy import LazyCall, LazyConfig
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config.omegaconf_patch import to_object
from imaginaire.lazy_config.omegaconf_patch import to_object

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：OmegaConf.to_object = to_object
OmegaConf.to_object = to_object

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PLACEHOLDER = None
PLACEHOLDER = None
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：LazyDict = DictConfig
LazyDict = DictConfig

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：__all__ = ["instantiate", "LazyCall", "LazyConfig", "PLACEHOLDER", "LazyDict"]
__all__ = ["instantiate", "LazyCall", "LazyConfig", "PLACEHOLDER", "LazyDict"]


# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：DOC_BUILDING = os.getenv("_DOC_BUILDING", False) # set in docs/conf.py
DOC_BUILDING = os.getenv("_DOC_BUILDING", False)  # set in docs/conf.py


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def fixup_module_metadata(module_name, namespace, keys=None):
def fixup_module_metadata(module_name, namespace, keys=None):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Fix the __qualname__ of module members to be their exported api name, so
    when they are referenced in docs, sphinx can find them. Reference:
    https://github.com/python-trio/trio/blob/6754c74eacfad9cc5c92d5c24727a2f3b620624e/trio/_util.py#L216-L241
    """
    # 中文说明：根据条件选择执行分支；代码：if not DOC_BUILDING:
    if not DOC_BUILDING:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return
        return
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：seen_ids = set()
    seen_ids = set()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def fix_one(qualname, name, obj):
    def fix_one(qualname, name, obj):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# avoid infinite recursion (relevant when using
        # avoid infinite recursion (relevant when using
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# typing.Generic, for example)
        # typing.Generic, for example)
        # 中文说明：根据条件选择执行分支；代码：if id(obj) in seen_ids:
        if id(obj) in seen_ids:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return
            return
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：seen_ids.add(id(obj))
        seen_ids.add(id(obj))

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mod = getattr(obj, "__module__", None)
        mod = getattr(obj, "__module__", None)
        # 中文说明：根据条件选择执行分支；代码：if mod is not None and (mod.startswith(module_name) or mod.startswith("fvcore.")):
        if mod is not None and (mod.startswith(module_name) or mod.startswith("fvcore.")):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：obj.__module__ = module_name
            obj.__module__ = module_name
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Modules, unlike everything else in Python, put fully-qualitied
            # Modules, unlike everything else in Python, put fully-qualitied
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# names into their __name__ attribute. We check for "." to avoid
            # names into their __name__ attribute. We check for "." to avoid
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# rewriting these.
            # rewriting these.
            # 中文说明：根据条件选择执行分支；代码：if hasattr(obj, "__name__") and "." not in obj.__name__:
            if hasattr(obj, "__name__") and "." not in obj.__name__:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：obj.__name__ = name
                obj.__name__ = name
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：obj.__qualname__ = qualname
                obj.__qualname__ = qualname
            # 中文说明：根据条件选择执行分支；代码：if isinstance(obj, type):
            if isinstance(obj, type):
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for attr_name, attr_value in obj.__dict__.items():
                for attr_name, attr_value in obj.__dict__.items():
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：fix_one(objname + "." + attr_name, attr_name, attr_value)
                    fix_one(objname + "." + attr_name, attr_name, attr_value)

    # 中文说明：根据条件选择执行分支；代码：if keys is None:
    if keys is None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：keys = namespace.keys()
        keys = namespace.keys()
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for objname in keys:
    for objname in keys:
        # 中文说明：根据条件选择执行分支；代码：if not objname.startswith("_"):
        if not objname.startswith("_"):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：obj = namespace[objname]
            obj = namespace[objname]
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：fix_one(objname, objname, obj)
            fix_one(objname, objname, obj)


# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：fixup_module_metadata(__name__, globals(), __all__)
fixup_module_metadata(__name__, globals(), __all__)
# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del fixup_module_metadata
del fixup_module_metadata
