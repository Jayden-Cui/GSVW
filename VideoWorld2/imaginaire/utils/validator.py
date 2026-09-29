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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import base64
import base64
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import itertools
import itertools
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import json
import json
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from abc import ABC, abstractmethod
from abc import ABC, abstractmethod
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from io import BytesIO
from io import BytesIO
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any, List, Union
from typing import Any, List, Union


# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# from https://docs.python.org/3/howto/descriptor.html#validator-class
# from https://docs.python.org/3/howto/descriptor.html#validator-class
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# For usage of hidden flag see the ModelParams class in apis/utils/model_params.py
# For usage of hidden flag see the ModelParams class in apis/utils/model_params.py
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Validator(ABC):
class Validator(ABC):
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# set name is called when the validator is created as class variable
    # set name is called when the validator is created as class variable
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# name is the name of the variable in the owner class, so here we create the name for the bac...
    # name is the name of the variable in the owner class, so here we create the name for the backing variable
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __set_name__(self, owner, name):
    def __set_name__(self, owner, name):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.private_name = "_" + name
        self.private_name = "_" + name

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __get__(self, obj, objtype=None):
    def __get__(self, obj, objtype=None):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return getattr(obj, self.private_name, self.default)
        return getattr(obj, self.private_name, self.default)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __set__(self, obj, value):
    def __set__(self, obj, value):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：value = self.validate(value)
        value = self.validate(value)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：setattr(obj, self.private_name, value)
        setattr(obj, self.private_name, value)

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@abstractmethod
    @abstractmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def validate(self, value):
    def validate(self, value):
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def json(self):
    def json(self):
        # 中文说明：执行循环控制或空操作；代码：pass
        pass


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class MultipleOf(Validator):
class MultipleOf(Validator):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, default: int, multiple_of: int, type_cast=None, hidden=False, tooltip=None):
    def __init__(self, default: int, multiple_of: int, type_cast=None, hidden=False, tooltip=None):
        # 中文说明：根据条件选择执行分支；代码：if type(multiple_of) is not int:
        if type(multiple_of) is not int:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Expected {multiple_of!r} to be an int")
            raise ValueError(f"Expected {multiple_of!r} to be an int")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.multiple_of = multiple_of
        self.multiple_of = multiple_of
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.default = default
        self.default = default
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.type_cast = type_cast
        self.type_cast = type_cast

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# For usage of hidden flag see the ModelParams class in apis/utils/model_params.py
        # For usage of hidden flag see the ModelParams class in apis/utils/model_params.py
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# if a parameter is hidden then probe() can't expose the param
        # if a parameter is hidden then probe() can't expose the param
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# and the param can't be set anymore
        # and the param can't be set anymore
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.hidden = hidden
        self.hidden = hidden
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.tooltip = tooltip
        self.tooltip = tooltip

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def validate(self, value):
    def validate(self, value):
        # 中文说明：根据条件选择执行分支；代码：if self.type_cast:
        if self.type_cast:
            # 中文说明：开始一个可捕获异常的代码块；代码：try:
            try:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：value = self.type_cast(value)
                value = self.type_cast(value)
            # 中文说明：处理异常、清理资源或管理上下文；代码：except ValueError:
            except ValueError:
                # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Expected {value!r} to be castable to {self.type_cast!r}")
                raise ValueError(f"Expected {value!r} to be castable to {self.type_cast!r}")

        # 中文说明：根据条件选择执行分支；代码：if value % self.multiple_of != 0:
        if value % self.multiple_of != 0:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Expected {value!r} to be a multiple of {self.multiple_of!r}")
            raise ValueError(f"Expected {value!r} to be a multiple of {self.multiple_of!r}")

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return value
        return value

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_range_iterator(self):
    def get_range_iterator(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return itertools.count(0, self.multiple_of)
        return itertools.count(0, self.multiple_of)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __repr__(self) -> str:
    def __repr__(self) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return f"MultipleOf({self.private_name=} {self.multiple_of=} {self.hidden=})"
        return f"MultipleOf({self.private_name=} {self.multiple_of=} {self.hidden=})"

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def json(self):
    def json(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return {
        return {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："type": MultipleOf.__name__,
            "type": MultipleOf.__name__,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："default": self.default,
            "default": self.default,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："multiple_of": self.multiple_of,
            "multiple_of": self.multiple_of,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："tooltip": self.tooltip,
            "tooltip": self.tooltip,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class OneOf(Validator):
class OneOf(Validator):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, default, options, type_cast=None, hidden=False, tooltip=None):
    def __init__(self, default, options, type_cast=None, hidden=False, tooltip=None):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.options = set(options)
        self.options = set(options)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.default = default
        self.default = default
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.type_cast = type_cast # Cast the value to this type before checking if it's in options
        self.type_cast = type_cast  # Cast the value to this type before checking if it's in options
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.tooltip = tooltip
        self.tooltip = tooltip
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.hidden = hidden
        self.hidden = hidden

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def validate(self, value):
    def validate(self, value):
        # 中文说明：根据条件选择执行分支；代码：if self.type_cast:
        if self.type_cast:
            # 中文说明：开始一个可捕获异常的代码块；代码：try:
            try:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：value = self.type_cast(value)
                value = self.type_cast(value)
            # 中文说明：处理异常、清理资源或管理上下文；代码：except ValueError:
            except ValueError:
                # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Expected {value!r} to be castable to {self.type_cast!r}")
                raise ValueError(f"Expected {value!r} to be castable to {self.type_cast!r}")

        # 中文说明：根据条件选择执行分支；代码：if value not in self.options:
        if value not in self.options:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Expected {value!r} to be one of {self.options!r}")
            raise ValueError(f"Expected {value!r} to be one of {self.options!r}")

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return value
        return value

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_range_iterator(self):
    def get_range_iterator(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.options
        return self.options

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __repr__(self) -> str:
    def __repr__(self) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return f"OneOf({self.private_name=} {self.options=} {self.hidden=})"
        return f"OneOf({self.private_name=} {self.options=} {self.hidden=})"

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def json(self):
    def json(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return {
        return {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："type": OneOf.__name__,
            "type": OneOf.__name__,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："default": self.default,
            "default": self.default,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："values": list(self.options),
            "values": list(self.options),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："tooltip": self.tooltip,
            "tooltip": self.tooltip,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class HumanAttributes(Validator):
class HumanAttributes(Validator):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, default, hidden=False, tooltip=None):
    def __init__(self, default, hidden=False, tooltip=None):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.default = default
        self.default = default
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.hidden = hidden
        self.hidden = hidden
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.tooltip = tooltip
        self.tooltip = tooltip

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# hard code the options for now
    # hard code the options for now
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# we extend this to init parameter as needed
    # we extend this to init parameter as needed
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：valid_attributes = {
    valid_attributes = {
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："emotion": ["angry", "contemptful", "disgusted", "fearful", "happy", "neutral", "sad", "surpr...
        "emotion": ["angry", "contemptful", "disgusted", "fearful", "happy", "neutral", "sad", "surprised"],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："race": ["asian", "indian", "black", "white", "middle eastern", "latino hispanic"],
        "race": ["asian", "indian", "black", "white", "middle eastern", "latino hispanic"],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："gender": ["male", "female"],
        "gender": ["male", "female"],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："age group": [
        "age group": [
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："young",
            "young",
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："teen",
            "teen",
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："adult early twenties",
            "adult early twenties",
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："adult late twenties",
            "adult late twenties",
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："adult early thirties",
            "adult early thirties",
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："adult late thirties",
            "adult late thirties",
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："adult middle aged",
            "adult middle aged",
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："older adult",
            "older adult",
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：],
        ],
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
    }

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_range_iterator(self):
    def get_range_iterator(self):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# create a list of all possible combinations
        # create a list of all possible combinations
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：l1 = self.valid_attributes["emotion"]
        l1 = self.valid_attributes["emotion"]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：l2 = self.valid_attributes["race"]
        l2 = self.valid_attributes["race"]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：l3 = self.valid_attributes["gender"]
        l3 = self.valid_attributes["gender"]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：l4 = self.valid_attributes["age group"]
        l4 = self.valid_attributes["age group"]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：all_combinations = list(itertools.product(l1, l2, l3, l4))
        all_combinations = list(itertools.product(l1, l2, l3, l4))
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return iter(all_combinations)
        return iter(all_combinations)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def validate(self, value):
    def validate(self, value):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：human_attributes = value.lower()
        human_attributes = value.lower()
        # 中文说明：根据条件选择执行分支；代码：if human_attributes not in ["none", "random"]:
        if human_attributes not in ["none", "random"]:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# In this case, we need for custom attribute string
            # In this case, we need for custom attribute string

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attr_string = human_attributes
            attr_string = human_attributes
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for attr_key in ["emotion", "race", "gender", "age group"]:
            for attr_key in ["emotion", "race", "gender", "age group"]:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attr_detected = False
                attr_detected = False
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for attr_label in self.valid_attributes[attr_key]:
                for attr_label in self.valid_attributes[attr_key]:
                    # 中文说明：根据条件选择执行分支；代码：if attr_string.startswith(attr_label):
                    if attr_string.startswith(attr_label):
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attr_string = attr_string[len(attr_label) + 1 :] # noqa: E203
                        attr_string = attr_string[len(attr_label) + 1 :]  # noqa: E203
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attr_detected = True
                        attr_detected = True
                        # 中文说明：执行循环控制或空操作；代码：break
                        break

                # 中文说明：根据条件选择执行分支；代码：if attr_detected is False:
                if attr_detected is False:
                    # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Expected {value!r} to be one of {self.valid_attributes!r}")
                    raise ValueError(f"Expected {value!r} to be one of {self.valid_attributes!r}")

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return value
        return value

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __repr__(self) -> str:
    def __repr__(self) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return f"HumanAttributes({self.private_name=} {self.hidden=})"
        return f"HumanAttributes({self.private_name=} {self.hidden=})"

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def json(self):
    def json(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return {
        return {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："type": HumanAttributes.__name__,
            "type": HumanAttributes.__name__,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："default": self.default,
            "default": self.default,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："values": self.valid_attributes,
            "values": self.valid_attributes,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："tooltip": self.tooltip,
            "tooltip": self.tooltip,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Bool(Validator):
class Bool(Validator):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, default, hidden=False, tooltip=None):
    def __init__(self, default, hidden=False, tooltip=None):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.default = default
        self.default = default
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.hidden = hidden
        self.hidden = hidden
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.tooltip = tooltip
        self.tooltip = tooltip

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def validate(self, value):
    def validate(self, value):
        # 中文说明：根据条件选择执行分支；代码：if isinstance(value, int):
        if isinstance(value, int):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：value = value != 0
            value = value != 0
        # 中文说明：根据条件选择执行分支；代码：elif isinstance(value, str):
        elif isinstance(value, str):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：value = value.lower()
            value = value.lower()
            # 中文说明：根据条件选择执行分支；代码：if value in ["true", "1"]:
            if value in ["true", "1"]:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：value = True
                value = True
            # 中文说明：根据条件选择执行分支；代码：elif value in ["false", "0"]:
            elif value in ["false", "0"]:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：value = False
                value = False
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Expected {value!r} to be one of ['True', 'False', '1', '0']")
                raise ValueError(f"Expected {value!r} to be one of ['True', 'False', '1', '0']")
        # 中文说明：根据条件选择执行分支；代码：elif not isinstance(value, bool):
        elif not isinstance(value, bool):
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError(f"Expected {value!r} to be an bool")
            raise TypeError(f"Expected {value!r} to be an bool")

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return value
        return value

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_range_iterator(self):
    def get_range_iterator(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return [True, False]
        return [True, False]

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __repr__(self) -> str:
    def __repr__(self) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return f"Bool({self.private_name=} {self.default=} {self.hidden=})"
        return f"Bool({self.private_name=} {self.default=} {self.hidden=})"

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def json(self):
    def json(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return {
        return {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："type": bool.__name__,
            "type": bool.__name__,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："default": self.default,
            "default": self.default,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："tooltip": self.tooltip,
            "tooltip": self.tooltip,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Int(Validator):
class Int(Validator):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, default, min=None, max=None, step=1, hidden=False, tooltip=None):
    def __init__(self, default, min=None, max=None, step=1, hidden=False, tooltip=None):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.min = min
        self.min = min
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.max = max
        self.max = max
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.default = default
        self.default = default
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.step = step
        self.step = step
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.hidden = hidden
        self.hidden = hidden
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.tooltip = tooltip
        self.tooltip = tooltip

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def validate(self, value):
    def validate(self, value):
        # 中文说明：根据条件选择执行分支；代码：if isinstance(value, str):
        if isinstance(value, str):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：value = int(value)
            value = int(value)
        # 中文说明：根据条件选择执行分支；代码：elif not isinstance(value, int):
        elif not isinstance(value, int):
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError(f"Expected {value!r} to be an int")
            raise TypeError(f"Expected {value!r} to be an int")

        # 中文说明：根据条件选择执行分支；代码：if self.min is not None and value < self.min:
        if self.min is not None and value < self.min:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Expected {value!r} to be at least {self.min!r}")
            raise ValueError(f"Expected {value!r} to be at least {self.min!r}")
        # 中文说明：根据条件选择执行分支；代码：if self.max is not None and value > self.max:
        if self.max is not None and value > self.max:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Expected {value!r} to be no more than {self.max!r}")
            raise ValueError(f"Expected {value!r} to be no more than {self.max!r}")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return value
        return value

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_range_iterator(self):
    def get_range_iterator(self):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iter_min = self.min if self.min is not None else self.default
        iter_min = self.min if self.min is not None else self.default
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iter_max = self.max if self.max is not None else self.default
        iter_max = self.max if self.max is not None else self.default
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return itertools.takewhile(lambda x: x <= iter_max, itertools.count(iter_min, self.step))
        return itertools.takewhile(lambda x: x <= iter_max, itertools.count(iter_min, self.step))

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __repr__(self) -> str:
    def __repr__(self) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return f"Int({self.private_name=} {self.default=}, {self.min=}, {self.max=} {self.hidden=})"
        return f"Int({self.private_name=} {self.default=}, {self.min=}, {self.max=} {self.hidden=})"

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def json(self):
    def json(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return {
        return {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："type": int.__name__,
            "type": int.__name__,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："default": self.default,
            "default": self.default,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："min": self.min,
            "min": self.min,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："max": self.max,
            "max": self.max,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："step": self.step,
            "step": self.step,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："tooltip": self.tooltip,
            "tooltip": self.tooltip,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Float(Validator):
class Float(Validator):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, default=0.0, min=None, max=None, step=0.5, hidden=False, tooltip=None):
    def __init__(self, default=0.0, min=None, max=None, step=0.5, hidden=False, tooltip=None):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.min = min
        self.min = min
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.max = max
        self.max = max
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.default = default
        self.default = default
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.step = step
        self.step = step
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.hidden = hidden
        self.hidden = hidden
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.tooltip = tooltip
        self.tooltip = tooltip

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def validate(self, value):
    def validate(self, value):
        # 中文说明：根据条件选择执行分支；代码：if isinstance(value, str) or isinstance(value, int):
        if isinstance(value, str) or isinstance(value, int):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：value = float(value)
            value = float(value)
        # 中文说明：根据条件选择执行分支；代码：elif not isinstance(value, float):
        elif not isinstance(value, float):
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError(f"Expected {value!r} to be float")
            raise TypeError(f"Expected {value!r} to be float")

        # 中文说明：根据条件选择执行分支；代码：if self.min is not None and value < self.min:
        if self.min is not None and value < self.min:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Expected {value!r} to be at least {self.min!r}")
            raise ValueError(f"Expected {value!r} to be at least {self.min!r}")
        # 中文说明：根据条件选择执行分支；代码：if self.max is not None and value > self.max:
        if self.max is not None and value > self.max:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Expected {value!r} to be no more than {self.max!r}")
            raise ValueError(f"Expected {value!r} to be no more than {self.max!r}")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return value
        return value

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_range_iterator(self):
    def get_range_iterator(self):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iter_min = self.min if self.min is not None else self.default
        iter_min = self.min if self.min is not None else self.default
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iter_max = self.max if self.max is not None else self.default
        iter_max = self.max if self.max is not None else self.default
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return itertools.takewhile(lambda x: x <= iter_max, itertools.count(iter_min, self.step))
        return itertools.takewhile(lambda x: x <= iter_max, itertools.count(iter_min, self.step))

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __repr__(self) -> str:
    def __repr__(self) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return f"Float({self.private_name=} {self.default=}, {self.min=}, {self.max=} {self.hidden=})"
        return f"Float({self.private_name=} {self.default=}, {self.min=}, {self.max=} {self.hidden=})"

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def json(self):
    def json(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return {
        return {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："type": float.__name__,
            "type": float.__name__,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："default": self.default,
            "default": self.default,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："min": self.min,
            "min": self.min,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："max": self.max,
            "max": self.max,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："step": self.step,
            "step": self.step,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："tooltip": self.tooltip,
            "tooltip": self.tooltip,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class String(Validator):
class String(Validator):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, default="", min=None, max=None, predicate=None, hidden=False, tooltip=None):
    def __init__(self, default="", min=None, max=None, predicate=None, hidden=False, tooltip=None):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.min = min
        self.min = min
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.max = max
        self.max = max
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.predicate = predicate
        self.predicate = predicate
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.default = default
        self.default = default
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.hidden = hidden
        self.hidden = hidden
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.tooltip = tooltip
        self.tooltip = tooltip

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def validate(self, value):
    def validate(self, value):
        # 中文说明：根据条件选择执行分支；代码：if not isinstance(value, str):
        if not isinstance(value, str):
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError(f"Expected {value!r} to be an str")
            raise TypeError(f"Expected {value!r} to be an str")
        # 中文说明：根据条件选择执行分支；代码：if self.min is not None and len(value) < self.min:
        if self.min is not None and len(value) < self.min:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Expected {value!r} to be no smaller than {self.min!r}")
            raise ValueError(f"Expected {value!r} to be no smaller than {self.min!r}")
        # 中文说明：根据条件选择执行分支；代码：if self.max is not None and len(value) > self.max:
        if self.max is not None and len(value) > self.max:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Expected {value!r} to be no bigger than {self.max!r}")
            raise ValueError(f"Expected {value!r} to be no bigger than {self.max!r}")
        # 中文说明：根据条件选择执行分支；代码：if self.predicate is not None and not self.predicate(value):
        if self.predicate is not None and not self.predicate(value):
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Expected {self.predicate} to be true for {value!r}")
            raise ValueError(f"Expected {self.predicate} to be true for {value!r}")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return value
        return value

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_range_iterator(self):
    def get_range_iterator(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return iter([self.default])
        return iter([self.default])

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __repr__(self) -> str:
    def __repr__(self) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return f"String({self.private_name=} {self.default=}, {self.min=}, {self.max=} {self.hidden=})"
        return f"String({self.private_name=} {self.default=}, {self.min=}, {self.max=} {self.hidden=})"

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def json(self):
    def json(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return {
        return {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："type": str.__name__,
            "type": str.__name__,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："default": self.default,
            "default": self.default,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："tooltip": self.tooltip,
            "tooltip": self.tooltip,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Path(Validator):
class Path(Validator):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, default="", hidden=False, tooltip=None):
    def __init__(self, default="", hidden=False, tooltip=None):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.default = default
        self.default = default
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.hidden = hidden
        self.hidden = hidden
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.tooltip = tooltip
        self.tooltip = tooltip

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def validate(self, value):
    def validate(self, value):
        # 中文说明：根据条件选择执行分支；代码：if not isinstance(value, str):
        if not isinstance(value, str):
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError(f"Expected {value!r} to be an str")
            raise TypeError(f"Expected {value!r} to be an str")
        # 中文说明：根据条件选择执行分支；代码：if not os.path.exists(value):
        if not os.path.exists(value):
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Expected {value!r} to be a valid path")
            raise ValueError(f"Expected {value!r} to be a valid path")

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return value
        return value

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_range_iterator(self):
    def get_range_iterator(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return iter([self.default])
        return iter([self.default])

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __repr__(self) -> str:
    def __repr__(self) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return f"String({self.private_name=} {self.default=}, {self.hidden=})"
        return f"String({self.private_name=} {self.default=}, {self.hidden=})"


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class InputImage(Validator):
class InputImage(Validator):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, default="", hidden=False, tooltip=None):
    def __init__(self, default="", hidden=False, tooltip=None):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.default = default
        self.default = default
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.hidden = hidden
        self.hidden = hidden
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.tooltip = tooltip
        self.tooltip = tooltip

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：valid_formats = {
    valid_formats = {
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："JPEG": ["jpeg", "jpg"],
        "JPEG": ["jpeg", "jpg"],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："JPEG2000": ["jp2"],
        "JPEG2000": ["jp2"],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："PNG": ["png"],
        "PNG": ["png"],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："GIF": ["gif"],
        "GIF": ["gif"],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："BMP": ["bmp"],
        "BMP": ["bmp"],
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
    }

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：valid_extensions = {vi: k for k, v in valid_formats.items() for vi in v}
    valid_extensions = {vi: k for k, v in valid_formats.items() for vi in v}

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def validate(self, value):
    def validate(self, value):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_, ext = os.path.splitext(value).lower()
        _, ext = os.path.splitext(value).lower()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：image_format = InputImage.valid_extensions[ext]
        image_format = InputImage.valid_extensions[ext]

        # 中文说明：根据条件选择执行分支；代码：if not isinstance(value, str):
        if not isinstance(value, str):
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError(f"Expected {value!r} to be an str")
            raise TypeError(f"Expected {value!r} to be an str")
        # 中文说明：根据条件选择执行分支；代码：if not os.path.exists(value):
        if not os.path.exists(value):
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Expected {value!r} to be a valid path")
            raise ValueError(f"Expected {value!r} to be a valid path")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return value
        return value

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_range_iterator(self):
    def get_range_iterator(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return iter([self.default])
        return iter([self.default])

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __repr__(self) -> str:
    def __repr__(self) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return f"String({self.private_name=} {self.default=} {self.hidden=})"
        return f"String({self.private_name=} {self.default=} {self.hidden=})"

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def json(self):
    def json(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return {
        return {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："type": InputImage.__name__,
            "type": InputImage.__name__,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："default": self.default,
            "default": self.default,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："values": self.valid_formats,
            "values": self.valid_formats,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："tooltip": self.tooltip,
            "tooltip": self.tooltip,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class MeshFormat(Validator):
class MeshFormat(Validator):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Validator class for mesh formats. Valid inputs are either:
    - single valid format such as "glb", "obj"
    - or a list of valid formats such as "[obj, ply, usdz]"
    """

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：valid_formats = {"glb", "usdz", "obj", "ply"}
    valid_formats = {"glb", "usdz", "obj", "ply"}

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, default="glb", hidden=False, tooltip=None):
    def __init__(self, default="glb", hidden=False, tooltip=None):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.default = default
        self.default = default
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.hidden = hidden
        self.hidden = hidden
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.tooltip = tooltip
        self.tooltip = tooltip

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def validate(self, value: str) -> Union[str, List[str]]:
    def validate(self, value: str) -> Union[str, List[str]]:
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Attempt to parse the input as a Python list
            # Attempt to parse the input as a Python list
            # 中文说明：根据条件选择执行分支；代码：if value.startswith("[") and value.endswith("]"):
            if value.startswith("[") and value.endswith("]"):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：formats = ast.literal_eval(value)
                formats = ast.literal_eval(value)
                # 中文说明：根据条件选择执行分支；代码：if not all(fmt in MeshFormat.valid_formats for fmt in formats):
                if not all(fmt in MeshFormat.valid_formats for fmt in formats):
                    # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Each item must be one of {MeshFormat.valid_formats}")
                    raise ValueError(f"Each item must be one of {MeshFormat.valid_formats}")
                # 中文说明：从当前函数返回结果或结束函数执行；代码：return formats
                return formats
            # 中文说明：根据条件选择执行分支；代码：elif value in MeshFormat.valid_formats:
            elif value in MeshFormat.valid_formats:
                # 中文说明：从当前函数返回结果或结束函数执行；代码：return value
                return value
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Expected {value!r} to be one of {MeshFormat.valid_formats} or a list of th...
                raise ValueError(f"Expected {value!r} to be one of {MeshFormat.valid_formats} or a list of them")
        # 中文说明：处理异常、清理资源或管理上下文；代码：except (SyntaxError, ValueError) as e:
        except (SyntaxError, ValueError) as e:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Handle case where the input is neither a valid single format nor a list of valid formats
            # Handle case where the input is neither a valid single format nor a list of valid formats
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Invalid format specification: {value}. Error: {str(e)}")
            raise ValueError(f"Invalid format specification: {value}. Error: {str(e)}")

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __repr__(self) -> str:
    def __repr__(self) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return f"MeshFormat(default={self.default}, hidden={self.hidden})"
        return f"MeshFormat(default={self.default}, hidden={self.hidden})"

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def json(self):
    def json(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return {
        return {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："type": MeshFormat.__name__,
            "type": MeshFormat.__name__,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："default": self.default,
            "default": self.default,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："values": self.valid_formats,
            "values": self.valid_formats,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："tooltip": self.tooltip,
            "tooltip": self.tooltip,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class JsonDict(Validator):
class JsonDict(Validator):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    JSON stringified version of a python dict.
    Example: '{"ema_customization_iter.pt": "ema_customization_iter.pt"}'
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, default="", hidden=False):
    def __init__(self, default="", hidden=False):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.default = default
        self.default = default
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.hidden = hidden
        self.hidden = hidden

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def validate(self, value):
    def validate(self, value):
        # 中文说明：根据条件选择执行分支；代码：if not value:
        if not value:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return {}
            return {}
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dict = json.loads(value)
            dict = json.loads(value)
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return dict
            return dict
        # 中文说明：处理异常、清理资源或管理上下文；代码：except json.JSONDecodeError as e:
        except json.JSONDecodeError as e:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Expected {value!r} to be json stringified dict. Error: {str(e)}")
            raise ValueError(f"Expected {value!r} to be json  stringified dict. Error: {str(e)}")

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __repr__(self) -> str:
    def __repr__(self) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return f"Dict({self.default=} {self.hidden=})"
        return f"Dict({self.default=} {self.hidden=})"


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class BytesIOType(Validator):
class BytesIOType(Validator):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Validator class for BytesIO. Valid inputs are either:
    - bytes
    - objects of class BytesIO
    - str which can be successfully  decoded into BytesIO
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, default=None, hidden=False, tooltip=None):
    def __init__(self, default=None, hidden=False, tooltip=None):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.default = default
        self.default = default
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.hidden = hidden
        self.hidden = hidden
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.tooltip = tooltip
        self.tooltip = tooltip

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def validate(self, value: Any) -> BytesIO:
    def validate(self, value: Any) -> BytesIO:
        # 中文说明：根据条件选择执行分支；代码：if isinstance(value, str):
        if isinstance(value, str):
            # 中文说明：开始一个可捕获异常的代码块；代码：try:
            try:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Decode the Base64 string
                # Decode the Base64 string
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：decoded_bytes = base64.b64decode(value)
                decoded_bytes = base64.b64decode(value)
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Create a BytesIO stream from the decoded bytes
                # Create a BytesIO stream from the decoded bytes
                # 中文说明：从当前函数返回结果或结束函数执行；代码：return BytesIO(decoded_bytes)
                return BytesIO(decoded_bytes)
            # 中文说明：处理异常、清理资源或管理上下文；代码：except (base64.binascii.Error, ValueError) as e:
            except (base64.binascii.Error, ValueError) as e:
                # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Invalid Base64 encoded string: {e}")
                raise ValueError(f"Invalid Base64 encoded string: {e}")
        # 中文说明：根据条件选择执行分支；代码：elif isinstance(value, bytes):
        elif isinstance(value, bytes):
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return BytesIO(value)
            return BytesIO(value)
        # 中文说明：根据条件选择执行分支；代码：elif isinstance(value, BytesIO):
        elif isinstance(value, BytesIO):
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return value
            return value
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError(f"Expected {value!r} to be a Base64 encoded string, bytes, or BytesIO")
            raise TypeError(f"Expected {value!r} to be a Base64 encoded string, bytes, or BytesIO")

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __repr__(self) -> str:
    def __repr__(self) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return f"BytesIOValidator({self.default=}, {self.hidden=})"
        return f"BytesIOValidator({self.default=}, {self.hidden=})"

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def json(self):
    def json(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return {
        return {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："type": BytesIO.__name__,
            "type": BytesIO.__name__,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："default": self.default,
            "default": self.default,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："tooltip": self.tooltip,
            "tooltip": self.tooltip,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }
