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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Iterator
from typing import Iterator


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def repeat_list(x: list, n: int) -> list:
def repeat_list(x: list, n: int) -> list:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Function to repeat the list to a fixed shape.
    r"""Function to repeat the list to a fixed shape.
    n is the desired length of the extended list.
    Args:
        x (list): Input list
        n (int): Desired length
    Returns:
        Extended list
    """
    # 中文说明：根据条件选择执行分支；代码：if n == 0:
    if n == 0:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return []
        return []
    # 中文说明：检查运行时假设是否成立；代码：assert len(x) > 0
    assert len(x) > 0

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_extended = []
    x_extended = []
    # 中文说明：在条件成立时重复执行循环体；代码：while len(x_extended) < n:
    while len(x_extended) < n:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_extended = x_extended + x
        x_extended = x_extended + x
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_extended = x_extended[0:n]
    x_extended = x_extended[0:n]

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return x_extended
    return x_extended


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def remove_extensions_from_keys(data: Iterator[dict]) -> Iterator[dict]:
def remove_extensions_from_keys(data: Iterator[dict]) -> Iterator[dict]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Function to remove extension from keys
    r"""Function to remove extension from keys
    Args:
        data (dict): Input data dict
    Returns:
        data dict with keys removed
    """

    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for data_dict in data:
    for data_dict in data:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_dict_remapped = dict()
        data_dict_remapped = dict()

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key in data_dict:
        for key in data_dict:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：key_split = key.split(".")
            key_split = key.split(".")
            # 中文说明：根据条件选择执行分支；代码：if len(key_split) > 1:
            if len(key_split) > 1:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：key_new = ".".join(key_split[:-1])
                key_new = ".".join(key_split[:-1])
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：key_new = key
                key_new = key
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_dict_remapped[key_new] = data_dict[key]
            data_dict_remapped[key_new] = data_dict[key]

        # 中文说明：从生成器逐步产生本行指定的值；代码：yield data_dict_remapped
        yield data_dict_remapped


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def update_url(data: Iterator[dict]) -> Iterator[dict]:
def update_url(data: Iterator[dict]) -> Iterator[dict]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Function to update the URLs so that the TarSample is removed from data.
    r"""Function to update the URLs so that the TarSample is removed from data.
    Instead, we replace the URL with a string.
    Args:
        data (dict): Input data dict
    Returns:
        data dict with URL replaced with a string
    """
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for data_dict in data:
    for data_dict in data:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_dict["__url__"] = os.path.join(data_dict["__url__"].root, data_dict["__url__"].path)
        data_dict["__url__"] = os.path.join(data_dict["__url__"].root, data_dict["__url__"].path)
        # 中文说明：从生成器逐步产生本行指定的值；代码：yield data_dict
        yield data_dict


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def skip_keys(data: Iterator[dict]) -> Iterator[dict]:
def skip_keys(data: Iterator[dict]) -> Iterator[dict]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""
    r"""
    Function to skip keys
    Args:
        data (dict): Input data dict
    Returns:
        data_dict with keys skipped
    """

    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for data_dict in data:
    for data_dict in data:
        # 中文说明：根据条件选择执行分支；代码：if ("keys_to_skip" in data_dict) and (int(data_dict["keys_to_skip"]) == 1):
        if ("keys_to_skip" in data_dict) and (int(data_dict["keys_to_skip"]) == 1):
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Skip this key if data_dict["skip_key"] is True
            # Skip this key if data_dict["skip_key"] is True
            # 中文说明：执行循环控制或空操作；代码：continue
            continue
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：从生成器逐步产生本行指定的值；代码：yield data_dict
            yield data_dict
