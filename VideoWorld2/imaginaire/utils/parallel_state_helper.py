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
# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
"""
This module contains various helper functions designed to extend the functionality of parallel states within the MCore library.

MCore is a third-party library that is infrequently updated and may introduce backward compatibility issues in our codebase, such as changes in function signatures or missing / new functions in new versions.

To mitigate these issues, this module provides stable functions that ensure the imaginaire codebase remains compatible with different versions of MCore.
"""


# 中文说明：开始一个可捕获异常的代码块；代码：try:
try:
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from megatron.core import parallel_state
    from megatron.core import parallel_state
# 中文说明：处理异常、清理资源或管理上下文；代码：except ImportError:
except ImportError:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print("Megatron is not installed, is_tp_cp_pp_rank0 functions will not work.")
    print("Megatron is not installed, is_tp_cp_pp_rank0 functions will not work.")


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_tp_cp_pp_rank0():
def is_tp_cp_pp_rank0():
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return (
    return (
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parallel_state.get_tensor_model_parallel_rank() == 0
        parallel_state.get_tensor_model_parallel_rank() == 0
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：and parallel_state.get_pipeline_model_parallel_rank() == 0
        and parallel_state.get_pipeline_model_parallel_rank() == 0
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：and parallel_state.get_context_parallel_rank() == 0
        and parallel_state.get_context_parallel_rank() == 0
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
