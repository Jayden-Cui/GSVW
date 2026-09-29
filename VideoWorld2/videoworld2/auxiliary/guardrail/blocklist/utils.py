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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import re
import re

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def read_keyword_list_from_dir(folder_path: str) -> list[str]:
def read_keyword_list_from_dir(folder_path: str) -> list[str]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Read keyword list from all files in a folder."""
    """Read keyword list from all files in a folder."""
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_list = []
    output_list = []
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：file_list = []
    file_list = []
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Get list of files in the folder
    # Get list of files in the folder
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for file in os.listdir(folder_path):
    for file in os.listdir(folder_path):
        # 中文说明：根据条件选择执行分支；代码：if os.path.isfile(os.path.join(folder_path, file)):
        if os.path.isfile(os.path.join(folder_path, file)):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：file_list.append(file)
            file_list.append(file)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Process each file
    # Process each file
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for file in file_list:
    for file in file_list:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：file_path = os.path.join(folder_path, file)
        file_path = os.path.join(folder_path, file)
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：处理异常、清理资源或管理上下文；代码：with open(file_path, "r") as f:
            with open(file_path, "r") as f:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：output_list.extend([line.strip() for line in f.readlines()])
                output_list.extend([line.strip() for line in f.readlines()])
        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
        except Exception as e:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.error(f"Error reading file {file}: {str(e)}")
            log.error(f"Error reading file {file}: {str(e)}")

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return output_list
    return output_list


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def to_ascii(prompt: str) -> str:
def to_ascii(prompt: str) -> str:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Convert prompt to ASCII."""
    """Convert prompt to ASCII."""
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return re.sub(r"[^\x00-\x7F]+", " ", prompt)
    return re.sub(r"[^\x00-\x7F]+", " ", prompt)
