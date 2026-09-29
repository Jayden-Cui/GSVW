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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from collections.abc import Iterable
from collections.abc import Iterable
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any, Generator, Optional
from typing import Any, Generator, Optional


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Augmentor:
class Augmentor:
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, input_keys: list, output_keys: Optional[list] = None, args: Optional[dict]...
    def __init__(self, input_keys: list, output_keys: Optional[list] = None, args: Optional[dict] = None) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Base augmentor class
        r"""Base augmentor class

        Args:
            input_keys (list): List of input keys
            output_keys (list): List of output keys
            args (dict): Arguments associated with the augmentation
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.input_keys = input_keys
        self.input_keys = input_keys
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.output_keys = output_keys
        self.output_keys = output_keys
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.args = args
        self.args = args

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, *args: Any, **kwds: Any) -> Any:
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError("Augmentor not implemented")
        raise ValueError("Augmentor not implemented")


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class IterableAugmentor:
class IterableAugmentor:
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, input_keys: list, output_keys: Optional[list] = None, args: Optional[dict]...
    def __init__(self, input_keys: list, output_keys: Optional[list] = None, args: Optional[dict] = None) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Base augmentor class
        r"""Base augmentor class

        Args:
            input_keys (list): List of input keys
            output_keys (list): List of output keys
            args (dict): Arguments associated with the augmentation
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.input_keys = input_keys
        self.input_keys = input_keys
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.output_keys = output_keys
        self.output_keys = output_keys
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.args = args
        self.args = args
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.is_generator = True
        self.is_generator = True

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, data: Iterable) -> Generator:
    def __call__(self, data: Iterable) -> Generator:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Example usage:
        r"""Example usage:

        for data_dict in data:
            # Do something to data_dict
            data_dict["input"] = data_dict["raw_sequence"][:, :-1]
            data_dict["target"] = data_dict["raw_sequence"][:, 1:]
            # Skip sample if needed
            if data_dict["input"].shape[1] < 64:
                continue
            # Construct a generator
            yield data_dict
        """
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError("Augmentor not implemented")
        raise ValueError("Augmentor not implemented")
