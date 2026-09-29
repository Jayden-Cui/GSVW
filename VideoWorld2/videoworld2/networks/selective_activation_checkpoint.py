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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from dataclasses import dataclass
from dataclasses import dataclass
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from enum import Enum
from enum import Enum

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch

# 中文说明：开始一个可捕获异常的代码块；代码：try:
try:
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.utils.checkpoint import CheckpointPolicy, create_selective_checkpoint_contexts
    from torch.utils.checkpoint import CheckpointPolicy, create_selective_checkpoint_contexts
# 中文说明：处理异常、清理资源或管理上下文；代码：except ImportError:
except ImportError:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：CheckpointPolicy = None
    CheckpointPolicy = None

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mm_only_save_list = {
mm_only_save_list = {
    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.ops.aten.mm.default,
    torch.ops.aten.mm.default,
    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.ops.aten._scaled_dot_product_efficient_attention.default,
    torch.ops.aten._scaled_dot_product_efficient_attention.default,
    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.ops.aten._scaled_dot_product_flash_attention.default,
    torch.ops.aten._scaled_dot_product_flash_attention.default,
    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.ops.aten.addmm.default,
    torch.ops.aten.addmm.default,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
}


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class CheckpointMode(str, Enum):
class CheckpointMode(str, Enum):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Enum for the different checkpoint modes.
    """

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：NONE = "none"
    NONE = "none"
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：MM_ONLY = "mm_only"
    MM_ONLY = "mm_only"
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：BLOCK_WISE = "block_wise"
    BLOCK_WISE = "block_wise"

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __str__(self) -> str:
    def __str__(self) -> str:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Optional: makes print() show just the value
        # Optional: makes print() show just the value
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.value
        return self.value


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def mm_only_policy(ctx, func, *args, **kwargs):
def mm_only_policy(ctx, func, *args, **kwargs):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    In newer flash-attn and TE versions, FA2 shows up in the list of ops with the name of 'flash_attn._flash_attn_forward'.
    However, FA2 is much slower (2-3x) than FA3 or cuDNN kernel. Registering cuDNN kernel would require heavy changes in TE code.
    That's why the best option is to use FA3 with small modifications to flash_attn_interface.py to register FA3 as PyTorch op.
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：to_save = func in mm_only_save_list or "flash_attn" in str(func)
    to_save = func in mm_only_save_list or "flash_attn" in str(func)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return CheckpointPolicy.MUST_SAVE if to_save else CheckpointPolicy.PREFER_RECOMPUTE
    return CheckpointPolicy.MUST_SAVE if to_save else CheckpointPolicy.PREFER_RECOMPUTE


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def mm_only_context_fn():
def mm_only_context_fn():
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return create_selective_checkpoint_contexts(mm_only_policy)
    return create_selective_checkpoint_contexts(mm_only_policy)


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@dataclass
@dataclass
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class SACConfig:
class SACConfig:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：mode: str = "mm_only"
    mode: str = "mm_only"
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：every_n_blocks: int = 1
    every_n_blocks: int = 1

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_context_fn(self):
    def get_context_fn(self):
        # 中文说明：根据条件选择执行分支；代码：if self.mode == CheckpointMode.MM_ONLY:
        if self.mode == CheckpointMode.MM_ONLY:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return mm_only_context_fn
            return mm_only_context_fn
        # 中文说明：根据条件选择执行分支；代码：elif self.mode == CheckpointMode.BLOCK_WISE:
        elif self.mode == CheckpointMode.BLOCK_WISE:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return None
            return None
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Invalid mode: {self.mode}")
            raise ValueError(f"Invalid mode: {self.mode}")
