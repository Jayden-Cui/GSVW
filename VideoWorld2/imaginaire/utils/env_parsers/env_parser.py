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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import base64
import base64
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import json
import json
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.validator import JsonDict, Validator
from imaginaire.utils.validator import JsonDict, Validator

# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
"""
Base class for parsing environment variables using validators.
Class will go through its list of validators and retrieve values from same named environment variables.
Validators provide:
- default value
- typed parsing
- enforments of mandatory values

Additionally the environment variables can be passed as single base64 encoded string.

we cannot enforce that a component isn't directly using the environment variables.
so evaluation of params should throw error to make sure actual env var is correct.
"""


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class EnvParser:
class EnvParser:
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, b64_str=None):
    def __init__(self, b64_str=None):
        # 中文说明：根据条件选择执行分支；代码：if b64_str:
        if b64_str:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.critical(f"b64_str recieved: {b64_str}")
            log.critical(f"b64_str recieved: {b64_str}")
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.from_b64(b64_str)
            self.from_b64(b64_str)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.from_env()
            self.from_env()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def from_env(self):
    def from_env(self):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：validators = self.get_val_dict()
        validators = self.get_val_dict()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key in validators.keys():
        for key in validators.keys():
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：val = os.getenv(key.upper())
            val = os.getenv(key.upper())
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(f"getting env var {key.upper()}: {val}")
            log.debug(f"getting env var {key.upper()}: {val}")
            # 中文说明：根据条件选择执行分支；代码：if val:
            if val:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：setattr(self, key, val)
                setattr(self, key, val)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.check_mandatory_values()
        self.check_mandatory_values()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def from_json(self, file_name):
    def from_json(self, file_name):
        # 中文说明：处理异常、清理资源或管理上下文；代码：with open(file_name, "r") as f:
        with open(file_name, "r") as f:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Reading env params from {file_name}")
            log.info(f"Reading env params from {file_name}")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dict = json.load(f)
            dict = json.load(f)
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key, value in dict.items():
            for key, value in dict.items():
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：setattr(self, key, value)
                setattr(self, key, value)
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.check_mandatory_values()
            self.check_mandatory_values()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def to_b64(self):
    def to_b64(self):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：json_str = self.to_json()
        json_str = self.to_json()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# create bytes-like object for b64 encoder
        # create bytes-like object for b64 encoder
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：json_str_bytes = json_str.encode()
        json_str_bytes = json_str.encode()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：b64_str = base64.b64encode(json_str_bytes).decode()
        b64_str = base64.b64encode(json_str_bytes).decode()

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(b64_str)
        print(b64_str)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return b64_str
        return b64_str

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def from_b64(self, b64_str):
    def from_b64(self, b64_str):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：json_str = base64.b64decode(b64_str).decode()
        json_str = base64.b64decode(b64_str).decode()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dict = json.loads(json_str)
        dict = json.loads(json_str)
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key, value in dict.items():
        for key, value in dict.items():
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：setattr(self, key, value)
            setattr(self, key, value)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.check_mandatory_values()
        self.check_mandatory_values()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def check_mandatory_values(self):
    def check_mandatory_values(self):
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key, validator in self.get_val_dict().items():
        for key, validator in self.get_val_dict().items():
            # 中文说明：根据条件选择执行分支；代码：if getattr(self, key) is None and validator.default is None:
            if getattr(self, key) is None and validator.default is None:
                # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Missing mandatory env var: {key}")
                raise ValueError(f"Missing mandatory env var: {key}")

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@classmethod
    @classmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_val_dict(cls):
    def get_val_dict(cls):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(f"getting val dict of {cls.__name__}")
        log.debug(f"getting val dict of {cls.__name__}")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：val_dict = {}
        val_dict = {}
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：val_dict.update({key: value for key, value in cls.__dict__.items() if isinstance(value, Valid...
        val_dict.update({key: value for key, value in cls.__dict__.items() if isinstance(value, Validator)})

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return val_dict
        return val_dict

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def dump_validators(self):
    def dump_validators(self):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：validators = self.get_val_dict()
        validators = self.get_val_dict()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key, value in validators.items():
        for key, value in validators.items():
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(f"{key}: {value.__get__(self)}")
            log.debug(f"{key}: {value.__get__(self)}")

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def to_json(self, file_name=None):
    def to_json(self, file_name=None):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dict = {
        dict = {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：key.upper(): value.__get__(self)
            key.upper(): value.__get__(self)
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key, value in EnvParser.__dict__.items()
            for key, value in EnvParser.__dict__.items()
            # 中文说明：根据条件选择执行分支；代码：if isinstance(value, Validator)
            if isinstance(value, Validator)
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：json_str = json.dumps(dict, indent=4)
        json_str = json.dumps(dict, indent=4)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(json_str)
        print(json_str)

        # 中文说明：根据条件选择执行分支；代码：if file_name:
        if file_name:
            # 中文说明：处理异常、清理资源或管理上下文；代码：with open(file_name, "w") as f:
            with open(file_name, "w") as f:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Writing env params to {file_name}")
                log.info(f"Writing env params to {file_name}")
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f.write(json_str)
                f.write(json_str)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return json_str
        return json_str

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def to_string_dict(self):
    def to_string_dict(self):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：result = {}
        result = {}
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key, validator in self.get_val_dict().items():
        for key, validator in self.get_val_dict().items():
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：value = getattr(self, key)
            value = getattr(self, key)
            # 中文说明：根据条件选择执行分支；代码：if value is None:
            if value is None:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：value = validator.default
                value = validator.default
            # 中文说明：根据条件选择执行分支；代码：if isinstance(validator, JsonDict):
            if isinstance(validator, JsonDict):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：value = json.dumps(value)
                value = json.dumps(value)
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：value = str(value)
                value = str(value)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：result[key] = value
            result[key] = value
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return result
        return result

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __str__(self):
    def __str__(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return ", ".join(f"{key}={value}" for key, value in self.__dict__.items())
        return ", ".join(f"{key}={value}" for key, value in self.__dict__.items())
