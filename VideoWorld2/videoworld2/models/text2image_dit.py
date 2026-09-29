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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import collections
import collections
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import math
import math
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from dataclasses import dataclass
from dataclasses import dataclass
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from enum import Enum
from enum import Enum
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any, Callable, List, Optional, Tuple
from typing import Any, Callable, List, Optional, Tuple

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import transformer_engine as te
import transformer_engine as te
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from einops import rearrange, repeat
from einops import rearrange, repeat
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from einops.layers.torch import Rearrange
from einops.layers.torch import Rearrange
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch import nn
from torch import nn
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed import ProcessGroup, get_process_group_ranks
from torch.distributed import ProcessGroup, get_process_group_ranks
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed.algorithms._checkpoint.checkpoint_wrapper import checkpoint_wrapper as...
from torch.distributed.algorithms._checkpoint.checkpoint_wrapper import checkpoint_wrapper as ptd_checkpoint_wrapper
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed.device_mesh import DeviceMesh
from torch.distributed.device_mesh import DeviceMesh
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed.fsdp import fully_shard
from torch.distributed.fsdp import fully_shard
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.utils.checkpoint import CheckpointPolicy, create_selective_checkpoint_contexts
from torch.utils.checkpoint import CheckpointPolicy, create_selective_checkpoint_contexts
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torchvision import transforms
from torchvision import transforms
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from transformer_engine.pytorch.attention import DotProductAttention, apply_rotary_pos_emb
from transformer_engine.pytorch.attention import DotProductAttention, apply_rotary_pos_emb

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.conditioner import DataType
from videoworld2.conditioner import DataType
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.module.a2a_cp import MinimalA2AAttnOp
from videoworld2.module.a2a_cp import MinimalA2AAttnOp
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.networks.model_weights_stats import WeightTrainingStat
from videoworld2.networks.model_weights_stats import WeightTrainingStat
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.networks.selective_activation_checkpoint import SACConfig as _SACConfig
from videoworld2.networks.selective_activation_checkpoint import SACConfig as _SACConfig
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.utils.context_parallel import split_inputs_cp
from videoworld2.utils.context_parallel import split_inputs_cp
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.graph import create_cuda_graph
from imaginaire.utils.graph import create_cuda_graph


# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# selective activation checkpoint; only apply to the minimal v4 model. if there are change in...
# selective activation checkpoint; only apply to the minimal v4 model. if there are change in the networks, some policy will not work as we expect.
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def predict2_2B_720_context_fn():
def predict2_2B_720_context_fn():
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：op_count = collections.defaultdict(int)
    op_count = collections.defaultdict(int)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def policy_fn(ctx, func, *args, **kwargs):
    def policy_fn(ctx, func, *args, **kwargs):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mode = "recompute" if ctx.is_recompute else "forward"
        mode = "recompute" if ctx.is_recompute else "forward"
        # 中文说明：根据条件选择执行分支；代码：if func == torch.ops.aten.mm.default:
        if func == torch.ops.aten.mm.default:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：op_count_key = f"{mode}_mm_count"
            op_count_key = f"{mode}_mm_count"
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# from imaginaire.utils import log
            # from imaginaire.utils import log
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# log.info(f"op_count_key: {op_count_key}, op_count[op_count_key]: {op_count[op_count_key]}, ...
            # log.info(f"op_count_key: {op_count_key}, op_count[op_count_key]: {op_count[op_count_key]}, {args[0].shape}, {args[1].shape}")
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# there are totally 6 + 4 + 4 + 2 = 16 block
            # there are totally 6 + 4 + 4 + 2 = 16 block
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：op_count[op_count_key] = (op_count[op_count_key] + 1) % 16
            op_count[op_count_key] = (op_count[op_count_key] + 1) % 16
            # 中文说明：根据条件选择执行分支；代码：if op_count[op_count_key] > 8: # recompute self attn first 3 linear layers
            if op_count[op_count_key] > 8:  # recompute self attn first 3 linear layers
                # 中文说明：从当前函数返回结果或结束函数执行；代码：return CheckpointPolicy.MUST_SAVE
                return CheckpointPolicy.MUST_SAVE
        # 中文说明：根据条件选择执行分支；代码：if "flash_attn" in str(func):
        if "flash_attn" in str(func):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：op_count_key = f"{mode}_flash_attn_count"
            op_count_key = f"{mode}_flash_attn_count"
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：op_count[op_count_key] = (op_count[op_count_key] + 1) % 2
            op_count[op_count_key] = (op_count[op_count_key] + 1) % 2
            # 中文说明：根据条件选择执行分支；代码：if op_count[op_count_key]:
            if op_count[op_count_key]:
                # 中文说明：从当前函数返回结果或结束函数执行；代码：return CheckpointPolicy.MUST_SAVE
                return CheckpointPolicy.MUST_SAVE
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return CheckpointPolicy.PREFER_RECOMPUTE
        return CheckpointPolicy.PREFER_RECOMPUTE

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return create_selective_checkpoint_contexts(policy_fn)
    return create_selective_checkpoint_contexts(policy_fn)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def predict2_14B_720_context_fn():
def predict2_14B_720_context_fn():
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：op_count = collections.defaultdict(int)
    op_count = collections.defaultdict(int)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def policy_fn(ctx, func, *args, **kwargs):
    def policy_fn(ctx, func, *args, **kwargs):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mode = "recompute" if ctx.is_recompute else "forward"
        mode = "recompute" if ctx.is_recompute else "forward"
        # 中文说明：根据条件选择执行分支；代码：if func == torch.ops.aten.mm.default:
        if func == torch.ops.aten.mm.default:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：op_count_key = f"{mode}_mm_count"
            op_count_key = f"{mode}_mm_count"
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# from imaginaire.utils import log
            # from imaginaire.utils import log
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# log.info(f"op_count_key: {op_count_key}, op_count[op_count_key]: {op_count[op_count_key]}, ...
            # log.info(f"op_count_key: {op_count_key}, op_count[op_count_key]: {op_count[op_count_key]}, {args[0].shape}, {args[1].shape}")
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# there are totally 6 + 4 + 4 + 2 = 16 block
            # there are totally 6 + 4 + 4 + 2 = 16 block
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：op_count[op_count_key] = (op_count[op_count_key] + 1) % 16
            op_count[op_count_key] = (op_count[op_count_key] + 1) % 16
            # 中文说明：根据条件选择执行分支；代码：if op_count[op_count_key] > 8: # recompute self attn first 1 linear layers
            if op_count[op_count_key] > 8:  # recompute self attn first 1 linear layers
                # 中文说明：从当前函数返回结果或结束函数执行；代码：return CheckpointPolicy.MUST_SAVE
                return CheckpointPolicy.MUST_SAVE
        # 中文说明：根据条件选择执行分支；代码：if "flash_attn" in str(func):
        if "flash_attn" in str(func):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：op_count_key = f"{mode}_flash_attn_count"
            op_count_key = f"{mode}_flash_attn_count"
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：op_count[op_count_key] = (op_count[op_count_key] + 1) % 2
            op_count[op_count_key] = (op_count[op_count_key] + 1) % 2
            # 中文说明：根据条件选择执行分支；代码：if op_count[op_count_key]:
            if op_count[op_count_key]:
                # 中文说明：从当前函数返回结果或结束函数执行；代码：return CheckpointPolicy.MUST_SAVE
                return CheckpointPolicy.MUST_SAVE
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return CheckpointPolicy.PREFER_RECOMPUTE
        return CheckpointPolicy.PREFER_RECOMPUTE

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return create_selective_checkpoint_contexts(policy_fn)
    return create_selective_checkpoint_contexts(policy_fn)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def linear_selfattn_context_fn():
def linear_selfattn_context_fn():
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：op_count = collections.defaultdict(int)
    op_count = collections.defaultdict(int)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def policy_fn(ctx, func, *args, **kwargs):
    def policy_fn(ctx, func, *args, **kwargs):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mode = "recompute" if ctx.is_recompute else "forward"
        mode = "recompute" if ctx.is_recompute else "forward"
        # 中文说明：根据条件选择执行分支；代码：if func == torch.ops.aten.mm.default:
        if func == torch.ops.aten.mm.default:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return CheckpointPolicy.MUST_SAVE
            return CheckpointPolicy.MUST_SAVE
        # 中文说明：根据条件选择执行分支；代码：if "flash_attn" in str(func):
        if "flash_attn" in str(func):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：op_count_key = f"{mode}_flash_attn_count"
            op_count_key = f"{mode}_flash_attn_count"
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：op_count[op_count_key] = (op_count[op_count_key] + 1) % 2
            op_count[op_count_key] = (op_count[op_count_key] + 1) % 2
            # 中文说明：根据条件选择执行分支；代码：if op_count[op_count_key]:
            if op_count[op_count_key]:
                # 中文说明：从当前函数返回结果或结束函数执行；代码：return CheckpointPolicy.MUST_SAVE
                return CheckpointPolicy.MUST_SAVE
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return CheckpointPolicy.PREFER_RECOMPUTE
        return CheckpointPolicy.PREFER_RECOMPUTE

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return create_selective_checkpoint_contexts(policy_fn)
    return create_selective_checkpoint_contexts(policy_fn)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class CheckpointMode(str, Enum):
class CheckpointMode(str, Enum):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：NONE = "none"
    NONE = "none"
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：MM_ONLY = "mm_only"
    MM_ONLY = "mm_only"
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：BLOCK_WISE = "block_wise"
    BLOCK_WISE = "block_wise"
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：LINEAR_SELFATTN = "linear_selfattn"
    LINEAR_SELFATTN = "linear_selfattn"
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_2B_720 = "predict2_2b_720"
    PREDICT2_2B_720 = "predict2_2b_720"
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_14B_720 = "predict2_14b_720"
    PREDICT2_14B_720 = "predict2_14b_720"

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __str__(self) -> str:
    def __str__(self) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.value
        return self.value


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@dataclass
@dataclass
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class SACConfig(_SACConfig):
class SACConfig(_SACConfig):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_context_fn(self):
    def get_context_fn(self):
        # 中文说明：根据条件选择执行分支；代码：if self.mode == CheckpointMode.LINEAR_SELFATTN:
        if self.mode == CheckpointMode.LINEAR_SELFATTN:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return linear_selfattn_context_fn
            return linear_selfattn_context_fn
        # 中文说明：根据条件选择执行分支；代码：elif self.mode == CheckpointMode.PREDICT2_2B_720:
        elif self.mode == CheckpointMode.PREDICT2_2B_720:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return predict2_2B_720_context_fn
            return predict2_2B_720_context_fn
        # 中文说明：根据条件选择执行分支；代码：elif self.mode == CheckpointMode.PREDICT2_14B_720:
        elif self.mode == CheckpointMode.PREDICT2_14B_720:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return predict2_14B_720_context_fn
            return predict2_14B_720_context_fn
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Reuse parent class implementation for other modes
            # Reuse parent class implementation for other modes
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return super().get_context_fn()
            return super().get_context_fn()


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class RMSNorm(torch.nn.Module):
class RMSNorm(torch.nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, dim: int, eps: float = 1e-5) -> None:
    def __init__(self, dim: int, eps: float = 1e-5) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.eps = eps
        self.eps = eps
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.weight = nn.Parameter(torch.ones(dim))
        self.weight = nn.Parameter(torch.ones(dim))

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def reset_parameters(self) -> None:
    def reset_parameters(self) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.nn.init.ones_(self.weight)
        torch.nn.init.ones_(self.weight)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _norm(self, x: torch.Tensor) -> torch.Tensor:
    def _norm(self, x: torch.Tensor) -> torch.Tensor:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps)
        return x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x: torch.Tensor) -> torch.Tensor:
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output = self._norm(x.float()).type_as(x)
        output = self._norm(x.float()).type_as(x)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return output * self.weight
        return output * self.weight


# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# ---------------------- Feed Forward Network -----------------------
# ---------------------- Feed Forward Network -----------------------
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class GPT2FeedForward(nn.Module):
class GPT2FeedForward(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, d_model: int, d_ff: int) -> None:
    def __init__(self, d_model: int, d_ff: int) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.activation = nn.GELU()
        self.activation = nn.GELU()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.layer1 = nn.Linear(d_model, d_ff, bias=False)
        self.layer1 = nn.Linear(d_model, d_ff, bias=False)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.layer2 = nn.Linear(d_ff, d_model, bias=False)
        self.layer2 = nn.Linear(d_ff, d_model, bias=False)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._layer_id = None
        self._layer_id = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._dim = d_model
        self._dim = d_model
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._hidden_dim = d_ff
        self._hidden_dim = d_ff
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.init_weights()
        self.init_weights()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def init_weights(self) -> None:
    def init_weights(self) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：std = 1.0 / math.sqrt(self._dim)
        std = 1.0 / math.sqrt(self._dim)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.nn.init.trunc_normal_(self.layer1.weight, std=std, a=-3 * std, b=3 * std)
        torch.nn.init.trunc_normal_(self.layer1.weight, std=std, a=-3 * std, b=3 * std)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# scale init by depth as in https://arxiv.org/abs/1908.11365 -- worked slightly better.
        # scale init by depth as in https://arxiv.org/abs/1908.11365 -- worked slightly better.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：std = 1.0 / math.sqrt(self._hidden_dim)
        std = 1.0 / math.sqrt(self._hidden_dim)
        # 中文说明：根据条件选择执行分支；代码：if self._layer_id is not None:
        if self._layer_id is not None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：std = std / math.sqrt(2 * (self._layer_id + 1))
            std = std / math.sqrt(2 * (self._layer_id + 1))
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.nn.init.trunc_normal_(self.layer2.weight, std=std, a=-3 * std, b=3 * std)
        torch.nn.init.trunc_normal_(self.layer2.weight, std=std, a=-3 * std, b=3 * std)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x: torch.Tensor) -> torch.Tensor:
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.layer1(x)
        x = self.layer1(x)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.activation(x)
        x = self.activation(x)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.layer2(x)
        x = self.layer2(x)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x
        return x


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def torch_attention_op(q_B_S_H_D: torch.Tensor, k_B_S_H_D: torch.Tensor, v_B_S_H_D: torch.Ten...
def torch_attention_op(q_B_S_H_D: torch.Tensor, k_B_S_H_D: torch.Tensor, v_B_S_H_D: torch.Tensor) -> torch.Tensor:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Computes multi-head attention using PyTorch's native implementation.
    """Computes multi-head attention using PyTorch's native implementation.

    This function provides a PyTorch backend alternative to Transformer Engine's attention operation.
    It rearranges the input tensors to match PyTorch's expected format, computes scaled dot-product
    attention, and rearranges the output back to the original format.

    The input tensor names use the following dimension conventions:

    - B: batch size
    - S: sequence length
    - H: number of attention heads
    - D: head dimension

    Args:
        q_B_S_H_D: Query tensor with shape (batch, seq_len, n_heads, head_dim)
        k_B_S_H_D: Key tensor with shape (batch, seq_len, n_heads, head_dim)
        v_B_S_H_D: Value tensor with shape (batch, seq_len, n_heads, head_dim)

    Returns:
        Attention output tensor with shape (batch, seq_len, n_heads * head_dim)
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_q_shape = q_B_S_H_D.shape
    in_q_shape = q_B_S_H_D.shape
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_k_shape = k_B_S_H_D.shape
    in_k_shape = k_B_S_H_D.shape
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q_B_H_S_D = rearrange(q_B_S_H_D, "b ... h k -> b h ... k").view(in_q_shape[0], in_q_shape[-2]...
    q_B_H_S_D = rearrange(q_B_S_H_D, "b ... h k -> b h ... k").view(in_q_shape[0], in_q_shape[-2], -1, in_q_shape[-1])
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：k_B_H_S_D = rearrange(k_B_S_H_D, "b ... h v -> b h ... v").view(in_k_shape[0], in_k_shape[-2]...
    k_B_H_S_D = rearrange(k_B_S_H_D, "b ... h v -> b h ... v").view(in_k_shape[0], in_k_shape[-2], -1, in_k_shape[-1])
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：v_B_H_S_D = rearrange(v_B_S_H_D, "b ... h v -> b h ... v").view(in_k_shape[0], in_k_shape[-2]...
    v_B_H_S_D = rearrange(v_B_S_H_D, "b ... h v -> b h ... v").view(in_k_shape[0], in_k_shape[-2], -1, in_k_shape[-1])
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：result_B_S_HD = rearrange(
    result_B_S_HD = rearrange(
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.nn.functional.scaled_dot_product_attention(q_B_H_S_D, k_B_H_S_D, v_B_H_S_D), "b h ... l...
        torch.nn.functional.scaled_dot_product_attention(q_B_H_S_D, k_B_H_S_D, v_B_H_S_D), "b h ... l -> b ... (h l)"
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return result_B_S_HD
    return result_B_S_HD


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Attention(nn.Module):
class Attention(nn.Module):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    A flexible attention module supporting both self-attention and cross-attention mechanisms.

    This module implements a multi-head attention layer that can operate in either self-attention
    or cross-attention mode. The mode is determined by whether a context dimension is provided.
    The implementation uses scaled dot-product attention and supports optional bias terms and
    dropout regularization.

    Args:
        query_dim (int): The dimensionality of the query vectors.
        context_dim (int, optional): The dimensionality of the context (key/value) vectors.
            If None, the module operates in self-attention mode using query_dim. Default: None
        n_heads (int, optional): Number of attention heads for multi-head attention. Default: 8
        head_dim (int, optional): The dimension of each attention head. Default: 64
        dropout (float, optional): Dropout probability applied to the output. Default: 0.0
        qkv_format (str, optional): Format specification for QKV tensors. Default: "bshd"
        backend (str, optional): Backend to use for the attention operation. Default: "transformer_engine"

    Examples:
        >>> # Self-attention with 512 dimensions and 8 heads
        >>> self_attn = Attention(query_dim=512)
        >>> x = torch.randn(32, 16, 512)  # (batch_size, seq_len, dim)
        >>> out = self_attn(x)  # (32, 16, 512)

        >>> # Cross-attention
        >>> cross_attn = Attention(query_dim=512, context_dim=256)
        >>> query = torch.randn(32, 16, 512)
        >>> context = torch.randn(32, 8, 256)
        >>> out = cross_attn(query, context)  # (32, 16, 512)
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：query_dim: int,
        query_dim: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：context_dim: Optional[int] = None,
        context_dim: Optional[int] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：n_heads: int = 8,
        n_heads: int = 8,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：head_dim: int = 64,
        head_dim: int = 64,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dropout: float = 0.0,
        dropout: float = 0.0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：qkv_format: str = "bshd",
        qkv_format: str = "bshd",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend: str = "transformer_engine",
        backend: str = "transformer_engine",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：attn_mask_type: str = "no_mask",
        attn_mask_type: str = "no_mask",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(
        log.debug(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Setting up {self.__class__.__name__}. Query dim is {query_dim}, context_dim is {context_dim...
            f"Setting up {self.__class__.__name__}. Query dim is {query_dim}, context_dim is {context_dim} and using "
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"{n_heads} heads with a dimension of {head_dim}."
            f"{n_heads} heads with a dimension of {head_dim}."
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.is_selfattn = context_dim is None # self attention
        self.is_selfattn = context_dim is None  # self attention

        # 中文说明：检查运行时假设是否成立；代码：assert backend in ["transformer_engine", "torch", "minimal_a2a"], f"Invalid backend: {backend}"
        assert backend in ["transformer_engine", "torch", "minimal_a2a"], f"Invalid backend: {backend}"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.backend = backend
        self.backend = backend

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：context_dim = query_dim if context_dim is None else context_dim
        context_dim = query_dim if context_dim is None else context_dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：inner_dim = head_dim * n_heads
        inner_dim = head_dim * n_heads

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.n_heads = n_heads
        self.n_heads = n_heads
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.head_dim = head_dim
        self.head_dim = head_dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.qkv_format = qkv_format
        self.qkv_format = qkv_format
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.query_dim = query_dim
        self.query_dim = query_dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.context_dim = context_dim
        self.context_dim = context_dim

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.q_proj = nn.Linear(query_dim, inner_dim, bias=False)
        self.q_proj = nn.Linear(query_dim, inner_dim, bias=False)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.q_norm = te.pytorch.RMSNorm(self.head_dim, eps=1e-6)
        self.q_norm = te.pytorch.RMSNorm(self.head_dim, eps=1e-6)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.k_proj = nn.Linear(context_dim, inner_dim, bias=False)
        self.k_proj = nn.Linear(context_dim, inner_dim, bias=False)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.k_norm = te.pytorch.RMSNorm(self.head_dim, eps=1e-6)
        self.k_norm = te.pytorch.RMSNorm(self.head_dim, eps=1e-6)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.v_proj = nn.Linear(context_dim, inner_dim, bias=False)
        self.v_proj = nn.Linear(context_dim, inner_dim, bias=False)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.v_norm = nn.Identity()
        self.v_norm = nn.Identity()

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.output_proj = nn.Linear(inner_dim, query_dim, bias=False)
        self.output_proj = nn.Linear(inner_dim, query_dim, bias=False)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.output_dropout = nn.Dropout(dropout) if dropout > 1e-4 else nn.Identity()
        self.output_dropout = nn.Dropout(dropout) if dropout > 1e-4 else nn.Identity()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.attn_mask_type = attn_mask_type
        self.attn_mask_type = attn_mask_type
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：根据条件选择执行分支；代码：if self.backend == "transformer_engine":
        if self.backend == "transformer_engine":
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.attn_op = DotProductAttention(
            self.attn_op = DotProductAttention(
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.n_heads,
                self.n_heads,
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.head_dim,
                self.head_dim,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_gqa_groups=self.n_heads,
                num_gqa_groups=self.n_heads,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attention_dropout=0,
                attention_dropout=0,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：qkv_format=qkv_format,
                qkv_format=qkv_format,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn_mask_type=attn_mask_type
                attn_mask_type=attn_mask_type
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：根据条件选择执行分支；代码：elif self.backend == "minimal_a2a":
        elif self.backend == "minimal_a2a":
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.attn_op = MinimalA2AAttnOp(attn_mask_type=attn_mask_type)
            self.attn_op = MinimalA2AAttnOp(attn_mask_type=attn_mask_type)
        # 中文说明：根据条件选择执行分支；代码：elif self.backend == "torch":
        elif self.backend == "torch":
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.attn_op = torch_attention_op
            self.attn_op = torch_attention_op

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._query_dim = query_dim
        self._query_dim = query_dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._context_dim = context_dim
        self._context_dim = context_dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._inner_dim = inner_dim
        self._inner_dim = inner_dim
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.init_weights()
        self.init_weights()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def init_weights(self) -> None:
    def init_weights(self) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：std = 1.0 / math.sqrt(self._query_dim)
        std = 1.0 / math.sqrt(self._query_dim)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.nn.init.trunc_normal_(self.q_proj.weight, std=std, a=-3 * std, b=3 * std)
        torch.nn.init.trunc_normal_(self.q_proj.weight, std=std, a=-3 * std, b=3 * std)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：std = 1.0 / math.sqrt(self._context_dim)
        std = 1.0 / math.sqrt(self._context_dim)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.nn.init.trunc_normal_(self.k_proj.weight, std=std, a=-3 * std, b=3 * std)
        torch.nn.init.trunc_normal_(self.k_proj.weight, std=std, a=-3 * std, b=3 * std)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.nn.init.trunc_normal_(self.v_proj.weight, std=std, a=-3 * std, b=3 * std)
        torch.nn.init.trunc_normal_(self.v_proj.weight, std=std, a=-3 * std, b=3 * std)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：std = 1.0 / math.sqrt(self._inner_dim)
        std = 1.0 / math.sqrt(self._inner_dim)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.nn.init.trunc_normal_(self.output_proj.weight, std=std, a=-3 * std, b=3 * std)
        torch.nn.init.trunc_normal_(self.output_proj.weight, std=std, a=-3 * std, b=3 * std)

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for layer in self.q_norm, self.k_norm, self.v_norm:
        for layer in self.q_norm, self.k_norm, self.v_norm:
            # 中文说明：根据条件选择执行分支；代码：if hasattr(layer, "reset_parameters"):
            if hasattr(layer, "reset_parameters"):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：layer.reset_parameters()
                layer.reset_parameters()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def compute_qkv(
    def compute_qkv(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x: torch.Tensor,
        x: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：context: Optional[torch.Tensor] = None,
        context: Optional[torch.Tensor] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rope_emb: Optional[torch.Tensor] = None,
        rope_emb: Optional[torch.Tensor] = None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q = self.q_proj(x)
        q = self.q_proj(x)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：context = x if context is None else context
        context = x if context is None else context
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：k = self.k_proj(context)
        k = self.k_proj(context)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：v = self.v_proj(context)
        v = self.v_proj(context)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q, k, v = map(
        q, k, v = map(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：lambda t: rearrange(t, "b ... (h d) -> b ... h d", h=self.n_heads, d=self.head_dim),
            lambda t: rearrange(t, "b ... (h d) -> b ... h d", h=self.n_heads, d=self.head_dim),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：(q, k, v),
            (q, k, v),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def apply_norm_and_rotary_pos_emb(
        def apply_norm_and_rotary_pos_emb(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q: torch.Tensor, k: torch.Tensor, v: torch.Tensor, rope_emb: Optional[torch.Tensor]
            q: torch.Tensor, k: torch.Tensor, v: torch.Tensor, rope_emb: Optional[torch.Tensor]
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q = self.q_norm(q)
            q = self.q_norm(q)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：k = self.k_norm(k)
            k = self.k_norm(k)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：v = self.v_norm(v)
            v = self.v_norm(v)
            # 中文说明：根据条件选择执行分支；代码：if self.is_selfattn and rope_emb is not None: # only apply to self-attention!
            if self.is_selfattn and rope_emb is not None:  # only apply to self-attention!
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：q = apply_rotary_pos_emb(q, rope_emb, tensor_format=self.qkv_format, fused=True)
                q = apply_rotary_pos_emb(q, rope_emb, tensor_format=self.qkv_format, fused=True)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：k = apply_rotary_pos_emb(k, rope_emb, tensor_format=self.qkv_format, fused=True)
                k = apply_rotary_pos_emb(k, rope_emb, tensor_format=self.qkv_format, fused=True)
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return q, k, v
            return q, k, v

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q, k, v = apply_norm_and_rotary_pos_emb(q, k, v, rope_emb)
        q, k, v = apply_norm_and_rotary_pos_emb(q, k, v, rope_emb)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return q, k, v
        return q, k, v

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def compute_attention(self, q: torch.Tensor, k: torch.Tensor, v: torch.Tensor, ori_size=None)...
    def compute_attention(self, q: torch.Tensor, k: torch.Tensor, v: torch.Tensor, ori_size=None) -> torch.Tensor:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# if self.attn_mask_type == 'causal':
        # if self.attn_mask_type == 'causal':
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
            # import pdb;pdb.set_trace()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs = {"ori_size": ori_size}
        kwargs = {"ori_size": ori_size}
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：result = self.attn_op(q, k, v, **kwargs) # [B, S, H, D]
        result = self.attn_op(q, k, v, **kwargs)  # [B, S, H, D]
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.output_dropout(self.output_proj(result))
        return self.output_dropout(self.output_proj(result))

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(
    def forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x: torch.Tensor,
        x: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：context: Optional[torch.Tensor] = None,
        context: Optional[torch.Tensor] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rope_emb: Optional[torch.Tensor] = None,
        rope_emb: Optional[torch.Tensor] = None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ori_size = None
        ori_size = None
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor:
    ) -> torch.Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Args:
            x (Tensor): The query tensor of shape [B, Mq, K]
            context (Optional[Tensor]): The key tensor of shape [B, Mk, K] or use x as context [self attention] if None
        """
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q, k, v = self.compute_qkv(x, context, rope_emb=rope_emb)
        q, k, v = self.compute_qkv(x, context, rope_emb=rope_emb)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.compute_attention(q, k, v, ori_size)
        return self.compute_attention(q, k, v, ori_size)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def set_context_parallel_group(
    def set_context_parallel_group(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, process_group: ProcessGroup, ranks: List[int], stream: torch.cuda.Stream
        self, process_group: ProcessGroup, ranks: List[int], stream: torch.cuda.Stream
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.attn_op.set_context_parallel_group(process_group, ranks, stream)
        self.attn_op.set_context_parallel_group(process_group, ranks, stream)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class VideoPositionEmb(nn.Module):
class VideoPositionEmb(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self) -> None:
    def __init__(self) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._cp_group = None
        self._cp_group = None

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def enable_context_parallel(self, process_group: ProcessGroup) -> None:
    def enable_context_parallel(self, process_group: ProcessGroup) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._cp_group = process_group
        self._cp_group = process_group

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def disable_context_parallel(self) -> None:
    def disable_context_parallel(self) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._cp_group = None
        self._cp_group = None

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def seq_dim(self) -> int:
    def seq_dim(self) -> int:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return 1
        return 1

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x_B_T_H_W_C: torch.Tensor, fps: Optional[torch.Tensor]) -> torch.Tensor:
    def forward(self, x_B_T_H_W_C: torch.Tensor, fps: Optional[torch.Tensor]) -> torch.Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        With CP, the function assume that the input tensor is already split.
        It delegates the embedding generation to generate_embeddings function.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：B_T_H_W_C = x_B_T_H_W_C.shape
        B_T_H_W_C = x_B_T_H_W_C.shape
        # 中文说明：根据条件选择执行分支；代码：if self._cp_group is not None:
        if self._cp_group is not None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cp_ranks = get_process_group_ranks(self._cp_group)
            cp_ranks = get_process_group_ranks(self._cp_group)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cp_size = len(cp_ranks)
            cp_size = len(cp_ranks)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：B, T, H, W, C = B_T_H_W_C
            B, T, H, W, C = B_T_H_W_C
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：B_T_H_W_C = torch.Size((B, T * cp_size, H, W, C))
            B_T_H_W_C = torch.Size((B, T * cp_size, H, W, C))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：embeddings = self.generate_embeddings(B_T_H_W_C, fps=fps)
        embeddings = self.generate_embeddings(B_T_H_W_C, fps=fps)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self._split_for_context_parallel(embeddings)
        return self._split_for_context_parallel(embeddings)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def generate_embeddings(self, B_T_H_W_C: torch.Size, fps: Optional[torch.Tensor]) -> Any:
    def generate_embeddings(self, B_T_H_W_C: torch.Size, fps: Optional[torch.Tensor]) -> Any:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise NotImplementedError
        raise NotImplementedError

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _split_for_context_parallel(self, embeddings: torch.Tensor) -> torch.Tensor:
    def _split_for_context_parallel(self, embeddings: torch.Tensor) -> torch.Tensor:
        # 中文说明：根据条件选择执行分支；代码：if self._cp_group is not None:
        if self._cp_group is not None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：embeddings = split_inputs_cp(x=embeddings, seq_dim=self.seq_dim, cp_group=self._cp_group)
            embeddings = split_inputs_cp(x=embeddings, seq_dim=self.seq_dim, cp_group=self._cp_group)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return embeddings
        return embeddings


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class VideoRopePosition3DEmb(VideoPositionEmb):
class VideoRopePosition3DEmb(VideoPositionEmb):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：*, # enforce keyword arguments
        *,  # enforce keyword arguments
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：head_dim: int,
        head_dim: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：len_h: int,
        len_h: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：len_w: int,
        len_w: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：len_t: int,
        len_t: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：base_fps: int = 24,
        base_fps: int = 24,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：h_extrapolation_ratio: float = 1.0,
        h_extrapolation_ratio: float = 1.0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：w_extrapolation_ratio: float = 1.0,
        w_extrapolation_ratio: float = 1.0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：t_extrapolation_ratio: float = 1.0,
        t_extrapolation_ratio: float = 1.0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：enable_fps_modulation: bool = True,
        enable_fps_modulation: bool = True,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**kwargs, # used for compatibility with other positional embeddings; unused in this class
        **kwargs,  # used for compatibility with other positional embeddings; unused in this class
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del kwargs
        del kwargs
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.register_buffer("seq", torch.arange(max(len_h, len_w, len_t), dtype=torch.float))
        self.register_buffer("seq", torch.arange(max(len_h, len_w, len_t), dtype=torch.float))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.base_fps = base_fps
        self.base_fps = base_fps
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.max_h = len_h
        self.max_h = len_h
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.max_w = len_w
        self.max_w = len_w
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.max_t = len_t
        self.max_t = len_t
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.enable_fps_modulation = enable_fps_modulation
        self.enable_fps_modulation = enable_fps_modulation
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dim = head_dim
        dim = head_dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dim_h = dim // 6 * 2
        dim_h = dim // 6 * 2
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dim_w = dim_h
        dim_w = dim_h
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dim_t = dim - 2 * dim_h
        dim_t = dim - 2 * dim_h
        # 中文说明：检查运行时假设是否成立；代码：assert dim == dim_h + dim_w + dim_t, f"bad dim: {dim} != {dim_h} + {dim_w} + {dim_t}"
        assert dim == dim_h + dim_w + dim_t, f"bad dim: {dim} != {dim_h} + {dim_w} + {dim_t}"
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.register_buffer(
        self.register_buffer(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："dim_spatial_range",
            "dim_spatial_range",
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.arange(0, dim_h, 2)[: (dim_h // 2)].float() / dim_h,
            torch.arange(0, dim_h, 2)[: (dim_h // 2)].float() / dim_h,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：persistent=True,
            persistent=True,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.register_buffer(
        self.register_buffer(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："dim_temporal_range",
            "dim_temporal_range",
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.arange(0, dim_t, 2)[: (dim_t // 2)].float() / dim_t,
            torch.arange(0, dim_t, 2)[: (dim_t // 2)].float() / dim_t,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：persistent=True,
            persistent=True,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._dim_h = dim_h
        self._dim_h = dim_h
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._dim_t = dim_t
        self._dim_t = dim_t

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.h_ntk_factor = h_extrapolation_ratio ** (dim_h / (dim_h - 2))
        self.h_ntk_factor = h_extrapolation_ratio ** (dim_h / (dim_h - 2))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.w_ntk_factor = w_extrapolation_ratio ** (dim_w / (dim_w - 2))
        self.w_ntk_factor = w_extrapolation_ratio ** (dim_w / (dim_w - 2))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.t_ntk_factor = t_extrapolation_ratio ** (dim_t / (dim_t - 2))
        self.t_ntk_factor = t_extrapolation_ratio ** (dim_t / (dim_t - 2))
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.reset_parameters()
        self.reset_parameters()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def reset_parameters(self) -> None:
    def reset_parameters(self) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dim_h = self._dim_h
        dim_h = self._dim_h
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dim_t = self._dim_t
        dim_t = self._dim_t

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.seq = torch.arange(max(self.max_h, self.max_w, self.max_t)).float().to(self.dim_spatial_...
        self.seq = torch.arange(max(self.max_h, self.max_w, self.max_t)).float().to(self.dim_spatial_range.device)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dim_spatial_range = (
        self.dim_spatial_range = (
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.arange(0, dim_h, 2)[: (dim_h // 2)].float().to(self.dim_spatial_range.device) / dim_h
            torch.arange(0, dim_h, 2)[: (dim_h // 2)].float().to(self.dim_spatial_range.device) / dim_h
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dim_temporal_range = (
        self.dim_temporal_range = (
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.arange(0, dim_t, 2)[: (dim_t // 2)].float().to(self.dim_spatial_range.device) / dim_t
            torch.arange(0, dim_t, 2)[: (dim_t // 2)].float().to(self.dim_spatial_range.device) / dim_t
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def generate_embeddings(
    def generate_embeddings(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：B_T_H_W_C: torch.Size,
        B_T_H_W_C: torch.Size,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：fps: Optional[torch.Tensor] = None,
        fps: Optional[torch.Tensor] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：h_ntk_factor: Optional[float] = None,
        h_ntk_factor: Optional[float] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：w_ntk_factor: Optional[float] = None,
        w_ntk_factor: Optional[float] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：t_ntk_factor: Optional[float] = None,
        t_ntk_factor: Optional[float] = None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor:
    ) -> torch.Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Generate embeddings for the given input size.

        Args:
            B_T_H_W_C (torch.Size): Input tensor size (Batch, Time, Height, Width, Channels).
            fps (Optional[torch.Tensor], optional): Frames per second. Defaults to None.
            h_ntk_factor (Optional[float], optional): Height NTK factor. If None, uses self.h_ntk_factor.
            w_ntk_factor (Optional[float], optional): Width NTK factor. If None, uses self.w_ntk_factor.
            t_ntk_factor (Optional[float], optional): Time NTK factor. If None, uses self.t_ntk_factor.

        Returns:
            Not specified in the original code snippet.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h_ntk_factor = h_ntk_factor if h_ntk_factor is not None else self.h_ntk_factor
        h_ntk_factor = h_ntk_factor if h_ntk_factor is not None else self.h_ntk_factor
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：w_ntk_factor = w_ntk_factor if w_ntk_factor is not None else self.w_ntk_factor
        w_ntk_factor = w_ntk_factor if w_ntk_factor is not None else self.w_ntk_factor
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t_ntk_factor = t_ntk_factor if t_ntk_factor is not None else self.t_ntk_factor
        t_ntk_factor = t_ntk_factor if t_ntk_factor is not None else self.t_ntk_factor

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h_theta = 10000.0 * h_ntk_factor # type: ignore
        h_theta = 10000.0 * h_ntk_factor  # type: ignore
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：w_theta = 10000.0 * w_ntk_factor # type: ignore
        w_theta = 10000.0 * w_ntk_factor  # type: ignore
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t_theta = 10000.0 * t_ntk_factor # type: ignore
        t_theta = 10000.0 * t_ntk_factor  # type: ignore

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h_spatial_freqs = 1.0 / (h_theta**self.dim_spatial_range)
        h_spatial_freqs = 1.0 / (h_theta**self.dim_spatial_range)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：w_spatial_freqs = 1.0 / (w_theta**self.dim_spatial_range)
        w_spatial_freqs = 1.0 / (w_theta**self.dim_spatial_range)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_freqs = 1.0 / (t_theta**self.dim_temporal_range)
        temporal_freqs = 1.0 / (t_theta**self.dim_temporal_range)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：B, T, H, W, _ = B_T_H_W_C
        B, T, H, W, _ = B_T_H_W_C
        # 中文说明：检查运行时假设是否成立；代码：assert (
        assert (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：H <= self.max_h and W <= self.max_w
            H <= self.max_h and W <= self.max_w
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"Input dimensions (H={H}, W={W}) exceed the maximum dimensions (max_h={self.max_h}, max_w...
        ), f"Input dimensions (H={H}, W={W}) exceed the maximum dimensions (max_h={self.max_h}, max_w={self.max_w})"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：half_emb_h = torch.outer(self.seq[:H], h_spatial_freqs)
        half_emb_h = torch.outer(self.seq[:H], h_spatial_freqs)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：half_emb_w = torch.outer(self.seq[:W], w_spatial_freqs)
        half_emb_w = torch.outer(self.seq[:W], w_spatial_freqs)

        # 中文说明：根据条件选择执行分支；代码：if self.enable_fps_modulation:
        if self.enable_fps_modulation:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：uniform_fps = (fps is None) or (fps.min() == fps.max())
            uniform_fps = (fps is None) or (fps.min() == fps.max())
            # 中文说明：检查运行时假设是否成立；代码：assert (
            assert (
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：uniform_fps or B == 1 or T == 1
                uniform_fps or B == 1 or T == 1
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), "For video batch, batch size should be 1 for non-uniform fps. For image batch, T should be 1"
            ), "For video batch, batch size should be 1 for non-uniform fps. For image batch, T should be 1"

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# apply sequence scaling in temporal dimension
            # apply sequence scaling in temporal dimension
            # 中文说明：根据条件选择执行分支；代码：if fps is None: # image case
            if fps is None:  # image case
                # 中文说明：检查运行时假设是否成立；代码：assert T == 1, "T should be 1 for image batch."
                assert T == 1, "T should be 1 for image batch."
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：half_emb_t = torch.outer(self.seq[:T], temporal_freqs)
                half_emb_t = torch.outer(self.seq[:T], temporal_freqs)
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：half_emb_t = torch.outer(self.seq[:T] / fps[:1] * self.base_fps, temporal_freqs)
                half_emb_t = torch.outer(self.seq[:T] / fps[:1] * self.base_fps, temporal_freqs)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：half_emb_t = torch.outer(self.seq[:T], temporal_freqs)
            half_emb_t = torch.outer(self.seq[:T], temporal_freqs)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：em_T_H_W_D = torch.cat(
        em_T_H_W_D = torch.cat(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：[
            [
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：repeat(half_emb_t, "t d -> t h w d", h=H, w=W),
                repeat(half_emb_t, "t d -> t h w d", h=H, w=W),
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：repeat(half_emb_h, "h d -> t h w d", t=T, w=W),
                repeat(half_emb_h, "h d -> t h w d", t=T, w=W),
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：repeat(half_emb_w, "w d -> t h w d", t=T, h=H),
                repeat(half_emb_w, "w d -> t h w d", t=T, h=H),
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
            ]
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：* 2,
            * 2,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dim=-1,
            dim=-1,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return rearrange(em_T_H_W_D, "t h w d -> (t h w) 1 1 d").float()
        return rearrange(em_T_H_W_D, "t h w d -> (t h w) 1 1 d").float()

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def seq_dim(self) -> int:
    def seq_dim(self) -> int:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return 0
        return 0


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class LearnablePosEmbAxis(VideoPositionEmb):
class LearnablePosEmbAxis(VideoPositionEmb):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：*, # enforce keyword arguments
        *,  # enforce keyword arguments
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：interpolation: str,
        interpolation: str,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model_channels: int,
        model_channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：len_h: int,
        len_h: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：len_w: int,
        len_w: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：len_t: int,
        len_t: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**kwargs,
        **kwargs,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Args:
            interpolation (str): we curretly only support "crop", ideally when we need extrapolation capacity, we should adjust frequency or other more advanced methods. they are not implemented yet.
        """
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del kwargs # unused
        del kwargs  # unused
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.interpolation = interpolation
        self.interpolation = interpolation
        # 中文说明：检查运行时假设是否成立；代码：assert self.interpolation in ["crop"], f"Unknown interpolation method {self.interpolation}"
        assert self.interpolation in ["crop"], f"Unknown interpolation method {self.interpolation}"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.model_channels = model_channels
        self.model_channels = model_channels

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.pos_emb_h = nn.Parameter(torch.zeros(len_h, model_channels))
        self.pos_emb_h = nn.Parameter(torch.zeros(len_h, model_channels))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.pos_emb_w = nn.Parameter(torch.zeros(len_w, model_channels))
        self.pos_emb_w = nn.Parameter(torch.zeros(len_w, model_channels))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.pos_emb_t = nn.Parameter(torch.zeros(len_t, model_channels))
        self.pos_emb_t = nn.Parameter(torch.zeros(len_t, model_channels))

        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.reset_parameters()
        self.reset_parameters()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def reset_parameters(self) -> None:
    def reset_parameters(self) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：std = 1.0 / math.sqrt(self.model_channels)
        std = 1.0 / math.sqrt(self.model_channels)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.nn.init.trunc_normal_(self.pos_emb_h, std=std, a=-3 * std, b=3 * std)
        torch.nn.init.trunc_normal_(self.pos_emb_h, std=std, a=-3 * std, b=3 * std)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.nn.init.trunc_normal_(self.pos_emb_w, std=std, a=-3 * std, b=3 * std)
        torch.nn.init.trunc_normal_(self.pos_emb_w, std=std, a=-3 * std, b=3 * std)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.nn.init.trunc_normal_(self.pos_emb_t, std=std, a=-3 * std, b=3 * std)
        torch.nn.init.trunc_normal_(self.pos_emb_t, std=std, a=-3 * std, b=3 * std)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def generate_embeddings(self, B_T_H_W_C: torch.Size, fps: Optional[torch.Tensor]) -> torch.Te...
    def generate_embeddings(self, B_T_H_W_C: torch.Size, fps: Optional[torch.Tensor]) -> torch.Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：B, T, H, W, _ = B_T_H_W_C
        B, T, H, W, _ = B_T_H_W_C
        # 中文说明：根据条件选择执行分支；代码：if self.interpolation == "crop":
        if self.interpolation == "crop":
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：emb_h_H = self.pos_emb_h[:H]
            emb_h_H = self.pos_emb_h[:H]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：emb_w_W = self.pos_emb_w[:W]
            emb_w_W = self.pos_emb_w[:W]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：emb_t_T = self.pos_emb_t[:T]
            emb_t_T = self.pos_emb_t[:T]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：emb = (
            emb = (
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：repeat(emb_t_T, "t d-> b t h w d", b=B, h=H, w=W)
                repeat(emb_t_T, "t d-> b t h w d", b=B, h=H, w=W)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：+ repeat(emb_h_H, "h d-> b t h w d", b=B, t=T, w=W)
                + repeat(emb_h_H, "h d-> b t h w d", b=B, t=T, w=W)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：+ repeat(emb_w_W, "w d-> b t h w d", b=B, t=T, h=H)
                + repeat(emb_w_W, "w d-> b t h w d", b=B, t=T, h=H)
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：检查运行时假设是否成立；代码：assert list(emb.shape)[:4] == [B, T, H, W], f"bad shape: {list(emb.shape)[:4]} != {B, T, H, W}"
            assert list(emb.shape)[:4] == [B, T, H, W], f"bad shape: {list(emb.shape)[:4]} != {B, T, H, W}"
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Unknown interpolation method {self.interpolation}")
            raise ValueError(f"Unknown interpolation method {self.interpolation}")

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：norm = torch.linalg.vector_norm(emb, dim=-1, keepdim=True, dtype=torch.float32)
        norm = torch.linalg.vector_norm(emb, dim=-1, keepdim=True, dtype=torch.float32)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：norm = torch.add(1e-6, norm, alpha=np.sqrt(norm.numel() / emb.numel()))
        norm = torch.add(1e-6, norm, alpha=np.sqrt(norm.numel() / emb.numel()))
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return emb / norm.to(emb.dtype)
        return emb / norm.to(emb.dtype)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Timesteps(nn.Module):
class Timesteps(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, num_channels: int):
    def __init__(self, num_channels: int):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_channels = num_channels
        self.num_channels = num_channels

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, timesteps_B_T: torch.Tensor) -> torch.Tensor:
    def forward(self, timesteps_B_T: torch.Tensor) -> torch.Tensor:
        # 中文说明：检查运行时假设是否成立；代码：assert timesteps_B_T.ndim == 2, f"Expected 2D input, got {timesteps_B_T.ndim}"
        assert timesteps_B_T.ndim == 2, f"Expected 2D input, got {timesteps_B_T.ndim}"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_dype = timesteps_B_T.dtype
        in_dype = timesteps_B_T.dtype
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：timesteps = timesteps_B_T.flatten().float()
        timesteps = timesteps_B_T.flatten().float()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：half_dim = self.num_channels // 2
        half_dim = self.num_channels // 2
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：exponent = -math.log(10000) * torch.arange(half_dim, dtype=torch.float32, device=timesteps.de...
        exponent = -math.log(10000) * torch.arange(half_dim, dtype=torch.float32, device=timesteps.device)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：exponent = exponent / (half_dim - 0.0)
        exponent = exponent / (half_dim - 0.0)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：emb = torch.exp(exponent)
        emb = torch.exp(exponent)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：emb = timesteps[:, None].float() * emb[None, :]
        emb = timesteps[:, None].float() * emb[None, :]

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sin_emb = torch.sin(emb)
        sin_emb = torch.sin(emb)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cos_emb = torch.cos(emb)
        cos_emb = torch.cos(emb)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：emb = torch.cat([cos_emb, sin_emb], dim=-1)
        emb = torch.cat([cos_emb, sin_emb], dim=-1)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return rearrange(emb.to(dtype=in_dype), "(b t) d -> b t d", b=timesteps_B_T.shape[0], t=times...
        return rearrange(emb.to(dtype=in_dype), "(b t) d -> b t d", b=timesteps_B_T.shape[0], t=timesteps_B_T.shape[1])


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class TimestepEmbedding(nn.Module):
class TimestepEmbedding(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, in_features: int, out_features: int, use_adaln_lora: bool = False):
    def __init__(self, in_features: int, out_features: int, use_adaln_lora: bool = False):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(
        log.debug(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Using AdaLN LoRA Flag: {use_adaln_lora}. We enable bias if no AdaLN LoRA for backward compa...
            f"Using AdaLN LoRA Flag:  {use_adaln_lora}. We enable bias if no AdaLN LoRA for backward compatibility."
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.in_dim = in_features
        self.in_dim = in_features
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.out_dim = out_features
        self.out_dim = out_features
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.linear_1 = nn.Linear(in_features, out_features, bias=not use_adaln_lora)
        self.linear_1 = nn.Linear(in_features, out_features, bias=not use_adaln_lora)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.activation = nn.SiLU()
        self.activation = nn.SiLU()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.use_adaln_lora = use_adaln_lora
        self.use_adaln_lora = use_adaln_lora
        # 中文说明：根据条件选择执行分支；代码：if use_adaln_lora:
        if use_adaln_lora:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.linear_2 = nn.Linear(out_features, 3 * out_features, bias=False)
            self.linear_2 = nn.Linear(out_features, 3 * out_features, bias=False)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.linear_2 = nn.Linear(out_features, out_features, bias=False)
            self.linear_2 = nn.Linear(out_features, out_features, bias=False)

        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.init_weights()
        self.init_weights()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def init_weights(self) -> None:
    def init_weights(self) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：std = 1.0 / math.sqrt(self.in_dim)
        std = 1.0 / math.sqrt(self.in_dim)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.nn.init.trunc_normal_(self.linear_1.weight, std=std, a=-3 * std, b=3 * std)
        torch.nn.init.trunc_normal_(self.linear_1.weight, std=std, a=-3 * std, b=3 * std)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：std = 1.0 / math.sqrt(self.out_dim)
        std = 1.0 / math.sqrt(self.out_dim)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.nn.init.trunc_normal_(self.linear_2.weight, std=std, a=-3 * std, b=3 * std)
        torch.nn.init.trunc_normal_(self.linear_2.weight, std=std, a=-3 * std, b=3 * std)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, sample: torch.Tensor) -> Tuple[torch.Tensor, Optional[torch.Tensor]]:
    def forward(self, sample: torch.Tensor) -> Tuple[torch.Tensor, Optional[torch.Tensor]]:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：emb = self.linear_1(sample)
        emb = self.linear_1(sample)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：emb = self.activation(emb)
        emb = self.activation(emb)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：emb = self.linear_2(emb)
        emb = self.linear_2(emb)

        # 中文说明：根据条件选择执行分支；代码：if self.use_adaln_lora:
        if self.use_adaln_lora:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：adaln_lora_B_T_3D = emb
            adaln_lora_B_T_3D = emb
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：emb_B_T_D = sample
            emb_B_T_D = sample
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：adaln_lora_B_T_3D = None
            adaln_lora_B_T_3D = None
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：emb_B_T_D = emb
            emb_B_T_D = emb

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return emb_B_T_D, adaln_lora_B_T_3D
        return emb_B_T_D, adaln_lora_B_T_3D


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class FourierFeatures(nn.Module):
class FourierFeatures(nn.Module):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Implements a layer that generates Fourier features from input tensors, based on randomly sampled
    frequencies and phases. This can help in learning high-frequency functions in low-dimensional problems.

    [B] -> [B, D]

    Parameters:
        num_channels (int): The number of Fourier features to generate.
        bandwidth (float, optional): The scaling factor for the frequency of the Fourier features. Defaults to 1.
        normalize (bool, optional): If set to True, the outputs are scaled by sqrt(2), usually to normalize
                                    the variance of the features. Defaults to False.

    Example:
        >>> layer = FourierFeatures(num_channels=256, bandwidth=0.5, normalize=True)
        >>> x = torch.randn(10, 256)  # Example input tensor
        >>> output = layer(x)
        >>> print(output.shape)  # Expected shape: (10, 256)
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, num_channels: int, bandwidth: int = 1, normalize: bool = False):
    def __init__(self, num_channels: int, bandwidth: int = 1, normalize: bool = False):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.register_buffer("freqs", 2 * np.pi * bandwidth * torch.randn(num_channels), persistent=T...
        self.register_buffer("freqs", 2 * np.pi * bandwidth * torch.randn(num_channels), persistent=True)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.register_buffer("phases", 2 * np.pi * torch.rand(num_channels), persistent=True)
        self.register_buffer("phases", 2 * np.pi * torch.rand(num_channels), persistent=True)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.gain = np.sqrt(2) if normalize else 1
        self.gain = np.sqrt(2) if normalize else 1
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.bandwidth = bandwidth
        self.bandwidth = bandwidth
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_channels = num_channels
        self.num_channels = num_channels

        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.reset_parameters()
        self.reset_parameters()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def reset_parameters(self) -> None:
    def reset_parameters(self) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：generator = torch.Generator()
        generator = torch.Generator()
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：generator.manual_seed(0)
        generator.manual_seed(0)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.freqs = (
        self.freqs = (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：2 * np.pi * self.bandwidth * torch.randn(self.num_channels, generator=generator).to(self.freq...
            2 * np.pi * self.bandwidth * torch.randn(self.num_channels, generator=generator).to(self.freqs.device)
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.phases = 2 * np.pi * torch.rand(self.num_channels, generator=generator).to(self.freqs.de...
        self.phases = 2 * np.pi * torch.rand(self.num_channels, generator=generator).to(self.freqs.device)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x: torch.Tensor, gain: float = 1.0) -> torch.Tensor:
    def forward(self, x: torch.Tensor, gain: float = 1.0) -> torch.Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Apply the Fourier feature transformation to the input tensor.

        Args:
            x (torch.Tensor): The input tensor.
            gain (float, optional): An additional gain factor applied during the forward pass. Defaults to 1.

        Returns:
            torch.Tensor: The transformed tensor, with Fourier features applied.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_dtype = x.dtype
        in_dtype = x.dtype
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = x.to(torch.float32).ger(self.freqs.to(torch.float32)).add(self.phases.to(torch.float32))
        x = x.to(torch.float32).ger(self.freqs.to(torch.float32)).add(self.phases.to(torch.float32))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = x.cos().mul(self.gain * gain).to(in_dtype)
        x = x.cos().mul(self.gain * gain).to(in_dtype)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x
        return x


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class PatchEmbed(nn.Module):
class PatchEmbed(nn.Module):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    PatchEmbed is a module for embedding patches from an input tensor by applying either 3D or 2D convolutional layers,
    depending on the . This module can process inputs with temporal (video) and spatial (image) dimensions,
    making it suitable for video and image processing tasks. It supports dividing the input into patches
    and embedding each patch into a vector of size `out_channels`.

    Parameters:
    - spatial_patch_size (int): The size of each spatial patch.
    - temporal_patch_size (int): The size of each temporal patch.
    - in_channels (int): Number of input channels. Default: 3.
    - out_channels (int): The dimension of the embedding vector for each patch. Default: 768.
    - bias (bool): If True, adds a learnable bias to the output of the convolutional layers. Default: True.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：spatial_patch_size: int,
        spatial_patch_size: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：temporal_patch_size: int,
        temporal_patch_size: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：in_channels: int = 3,
        in_channels: int = 3,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out_channels: int = 768,
        out_channels: int = 768,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.spatial_patch_size = spatial_patch_size
        self.spatial_patch_size = spatial_patch_size
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.temporal_patch_size = temporal_patch_size
        self.temporal_patch_size = temporal_patch_size

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.proj = nn.Sequential(
        self.proj = nn.Sequential(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：Rearrange(
            Rearrange(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："b c (t r) (h m) (w n) -> b t h w (c r m n)",
                "b c (t r) (h m) (w n) -> b t h w (c r m n)",
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：r=temporal_patch_size,
                r=temporal_patch_size,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：m=spatial_patch_size,
                m=spatial_patch_size,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n=spatial_patch_size,
                n=spatial_patch_size,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.Linear(
            nn.Linear(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：in_channels * spatial_patch_size * spatial_patch_size * temporal_patch_size, out_channels, bi...
                in_channels * spatial_patch_size * spatial_patch_size * temporal_patch_size, out_channels, bias=False
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dim = in_channels * spatial_patch_size * spatial_patch_size * temporal_patch_size
        self.dim = in_channels * spatial_patch_size * spatial_patch_size * temporal_patch_size

        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.init_weights()
        self.init_weights()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def init_weights(self) -> None:
    def init_weights(self) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：std = 1.0 / math.sqrt(self.dim)
        std = 1.0 / math.sqrt(self.dim)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.nn.init.trunc_normal_(self.proj[1].weight, std=std, a=-3 * std, b=3 * std)
        torch.nn.init.trunc_normal_(self.proj[1].weight, std=std, a=-3 * std, b=3 * std)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x: torch.Tensor) -> torch.Tensor:
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Forward pass of the PatchEmbed module.

        Parameters:
        - x (torch.Tensor): The input tensor of shape (B, C, T, H, W) where
            B is the batch size,
            C is the number of channels,
            T is the temporal dimension,
            H is the height, and
            W is the width of the input.

        Returns:
        - torch.Tensor: The embedded patches as a tensor, with shape b t h w c.
        """
        # 中文说明：检查运行时假设是否成立；代码：assert x.dim() == 5
        assert x.dim() == 5
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_, _, T, H, W = x.shape
        _, _, T, H, W = x.shape
        # 中文说明：检查运行时假设是否成立；代码：assert (
        assert (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：H % self.spatial_patch_size == 0 and W % self.spatial_patch_size == 0
            H % self.spatial_patch_size == 0 and W % self.spatial_patch_size == 0
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"H,W {(H, W)} should be divisible by spatial_patch_size {self.spatial_patch_size}"
        ), f"H,W {(H, W)} should be divisible by spatial_patch_size {self.spatial_patch_size}"
        # 中文说明：检查运行时假设是否成立；代码：assert T % self.temporal_patch_size == 0
        assert T % self.temporal_patch_size == 0
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.proj(x)
        x = self.proj(x)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x
        return x


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class FinalLayer(nn.Module):
class FinalLayer(nn.Module):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    The final layer of video DiT.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：hidden_size: int,
        hidden_size: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：spatial_patch_size: int,
        spatial_patch_size: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：temporal_patch_size: int,
        temporal_patch_size: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out_channels: int,
        out_channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：use_adaln_lora: bool = False,
        use_adaln_lora: bool = False,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：adaln_lora_dim: int = 256,
        adaln_lora_dim: int = 256,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.layer_norm = nn.LayerNorm(hidden_size, elementwise_affine=False, eps=1e-6)
        self.layer_norm = nn.LayerNorm(hidden_size, elementwise_affine=False, eps=1e-6)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.linear = nn.Linear(
        self.linear = nn.Linear(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：hidden_size, spatial_patch_size * spatial_patch_size * temporal_patch_size * out_channels, bi...
            hidden_size, spatial_patch_size * spatial_patch_size * temporal_patch_size * out_channels, bias=False
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.hidden_size = hidden_size
        self.hidden_size = hidden_size
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.n_adaln_chunks = 2
        self.n_adaln_chunks = 2
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.use_adaln_lora = use_adaln_lora
        self.use_adaln_lora = use_adaln_lora
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.adaln_lora_dim = adaln_lora_dim
        self.adaln_lora_dim = adaln_lora_dim
        # 中文说明：根据条件选择执行分支；代码：if use_adaln_lora:
        if use_adaln_lora:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.adaln_modulation = nn.Sequential(
            self.adaln_modulation = nn.Sequential(
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.SiLU(),
                nn.SiLU(),
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.Linear(hidden_size, adaln_lora_dim, bias=False),
                nn.Linear(hidden_size, adaln_lora_dim, bias=False),
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.Linear(adaln_lora_dim, self.n_adaln_chunks * hidden_size, bias=False),
                nn.Linear(adaln_lora_dim, self.n_adaln_chunks * hidden_size, bias=False),
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.adaln_modulation = nn.Sequential(
            self.adaln_modulation = nn.Sequential(
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.SiLU(), nn.Linear(hidden_size, self.n_adaln_chunks * hidden_size, bias=False)
                nn.SiLU(), nn.Linear(hidden_size, self.n_adaln_chunks * hidden_size, bias=False)
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.init_weights()
        self.init_weights()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def init_weights(self) -> None:
    def init_weights(self) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：std = 1.0 / math.sqrt(self.hidden_size)
        std = 1.0 / math.sqrt(self.hidden_size)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.nn.init.trunc_normal_(self.linear.weight, std=std, a=-3 * std, b=3 * std)
        torch.nn.init.trunc_normal_(self.linear.weight, std=std, a=-3 * std, b=3 * std)
        # 中文说明：根据条件选择执行分支；代码：if self.use_adaln_lora:
        if self.use_adaln_lora:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.nn.init.trunc_normal_(self.adaln_modulation[1].weight, std=std, a=-3 * std, b=3 * std)
            torch.nn.init.trunc_normal_(self.adaln_modulation[1].weight, std=std, a=-3 * std, b=3 * std)
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.nn.init.zeros_(self.adaln_modulation[2].weight)
            torch.nn.init.zeros_(self.adaln_modulation[2].weight)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.nn.init.zeros_(self.adaln_modulation[1].weight)
            torch.nn.init.zeros_(self.adaln_modulation[1].weight)

        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.layer_norm.reset_parameters()
        self.layer_norm.reset_parameters()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(
    def forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_B_T_H_W_D: torch.Tensor,
        x_B_T_H_W_D: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：emb_B_T_D: torch.Tensor,
        emb_B_T_D: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：adaln_lora_B_T_3D: Optional[torch.Tensor] = None,
        adaln_lora_B_T_3D: Optional[torch.Tensor] = None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：根据条件选择执行分支；代码：if self.use_adaln_lora:
        if self.use_adaln_lora:
            # 中文说明：检查运行时假设是否成立；代码：assert adaln_lora_B_T_3D is not None
            assert adaln_lora_B_T_3D is not None
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：shift_B_T_D, scale_B_T_D = (
            shift_B_T_D, scale_B_T_D = (
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.adaln_modulation(emb_B_T_D) + adaln_lora_B_T_3D[:, :, : 2 * self.hidden_size]
                self.adaln_modulation(emb_B_T_D) + adaln_lora_B_T_3D[:, :, : 2 * self.hidden_size]
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：).chunk(2, dim=-1)
            ).chunk(2, dim=-1)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：shift_B_T_D, scale_B_T_D = self.adaln_modulation(emb_B_T_D).chunk(2, dim=-1)
            shift_B_T_D, scale_B_T_D = self.adaln_modulation(emb_B_T_D).chunk(2, dim=-1)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：shift_B_T_1_1_D, scale_B_T_1_1_D = rearrange(shift_B_T_D, "b t d -> b t 1 1 d"), rearrange(
        shift_B_T_1_1_D, scale_B_T_1_1_D = rearrange(shift_B_T_D, "b t d -> b t 1 1 d"), rearrange(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scale_B_T_D, "b t d -> b t 1 1 d"
            scale_B_T_D, "b t d -> b t 1 1 d"
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _fn(
        def _fn(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_x_B_T_H_W_D: torch.Tensor,
            _x_B_T_H_W_D: torch.Tensor,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_norm_layer: nn.Module,
            _norm_layer: nn.Module,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_scale_B_T_1_1_D: torch.Tensor,
            _scale_B_T_1_1_D: torch.Tensor,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_shift_B_T_1_1_D: torch.Tensor,
            _shift_B_T_1_1_D: torch.Tensor,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor:
        ) -> torch.Tensor:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return _norm_layer(_x_B_T_H_W_D) * (1 + _scale_B_T_1_1_D) + _shift_B_T_1_1_D
            return _norm_layer(_x_B_T_H_W_D) * (1 + _scale_B_T_1_1_D) + _shift_B_T_1_1_D

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_T_H_W_D = _fn(x_B_T_H_W_D, self.layer_norm, scale_B_T_1_1_D, shift_B_T_1_1_D)
        x_B_T_H_W_D = _fn(x_B_T_H_W_D, self.layer_norm, scale_B_T_1_1_D, shift_B_T_1_1_D)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_T_H_W_O = self.linear(x_B_T_H_W_D)
        x_B_T_H_W_O = self.linear(x_B_T_H_W_D)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x_B_T_H_W_O
        return x_B_T_H_W_O


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Block(nn.Module):
class Block(nn.Module):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    A transformer block that combines self-attention, cross-attention and MLP layers with AdaLN modulation.
    Each component (self-attention, cross-attention, MLP) has its own layer normalization and AdaLN modulation.

    Parameters:
        x_dim (int): Dimension of input features
        context_dim (int): Dimension of context features for cross-attention
        num_heads (int): Number of attention heads
        mlp_ratio (float): Multiplier for MLP hidden dimension. Default: 4.0
        use_adaln_lora (bool): Whether to use AdaLN-LoRA modulation. Default: False
        adaln_lora_dim (int): Hidden dimension for AdaLN-LoRA layers. Default: 256

    The block applies the following sequence:
    1. Self-attention with AdaLN modulation
    2. Cross-attention with AdaLN modulation
    3. MLP with AdaLN modulation

    Each component uses skip connections and layer normalization.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_dim: int,
        x_dim: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：context_dim: int,
        context_dim: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_heads: int,
        num_heads: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：mlp_ratio: float = 4.0,
        mlp_ratio: float = 4.0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：use_adaln_lora: bool = False,
        use_adaln_lora: bool = False,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：adaln_lora_dim: int = 256,
        adaln_lora_dim: int = 256,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：backend: str = "transformer_engine",
        backend: str = "transformer_engine",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：causal_cross_attn: bool = False,
        causal_cross_attn: bool = False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.x_dim = x_dim
        self.x_dim = x_dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.layer_norm_self_attn = nn.LayerNorm(x_dim, elementwise_affine=False, eps=1e-6)
        self.layer_norm_self_attn = nn.LayerNorm(x_dim, elementwise_affine=False, eps=1e-6)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.self_attn = Attention(x_dim, None, num_heads, x_dim // num_heads, qkv_format="bshd", bac...
        self.self_attn = Attention(x_dim, None, num_heads, x_dim // num_heads, qkv_format="bshd", backend=backend)
        
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.layer_norm_cross_attn = nn.LayerNorm(x_dim, elementwise_affine=False, eps=1e-6)
        self.layer_norm_cross_attn = nn.LayerNorm(x_dim, elementwise_affine=False, eps=1e-6)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.cross_attn = Attention(
        self.cross_attn = Attention(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_dim,
            x_dim, 
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：context_dim,
            context_dim, 
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_heads,
            num_heads, 
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_dim // num_heads,
            x_dim // num_heads, 
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：qkv_format="bshd",
            qkv_format="bshd", 
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend=backend,
            backend=backend, 
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn_mask_type="causal" if causal_cross_attn else "no_mask",
            attn_mask_type="causal" if causal_cross_attn else "no_mask",
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.layer_norm_mlp = nn.LayerNorm(x_dim, elementwise_affine=False, eps=1e-6)
        self.layer_norm_mlp = nn.LayerNorm(x_dim, elementwise_affine=False, eps=1e-6)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mlp = GPT2FeedForward(x_dim, int(x_dim * mlp_ratio))
        self.mlp = GPT2FeedForward(x_dim, int(x_dim * mlp_ratio))

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.use_adaln_lora = use_adaln_lora
        self.use_adaln_lora = use_adaln_lora
        # 中文说明：根据条件选择执行分支；代码：if self.use_adaln_lora:
        if self.use_adaln_lora:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.adaln_modulation_self_attn = nn.Sequential(
            self.adaln_modulation_self_attn = nn.Sequential(
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.SiLU(),
                nn.SiLU(),
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.Linear(x_dim, adaln_lora_dim, bias=False),
                nn.Linear(x_dim, adaln_lora_dim, bias=False),
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.Linear(adaln_lora_dim, 3 * x_dim, bias=False),
                nn.Linear(adaln_lora_dim, 3 * x_dim, bias=False),
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.adaln_modulation_cross_attn = nn.Sequential(
            self.adaln_modulation_cross_attn = nn.Sequential(
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.SiLU(),
                nn.SiLU(),
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.Linear(x_dim, adaln_lora_dim, bias=False),
                nn.Linear(x_dim, adaln_lora_dim, bias=False),
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.Linear(adaln_lora_dim, 3 * x_dim, bias=False),
                nn.Linear(adaln_lora_dim, 3 * x_dim, bias=False),
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.adaln_modulation_mlp = nn.Sequential(
            self.adaln_modulation_mlp = nn.Sequential(
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.SiLU(),
                nn.SiLU(),
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.Linear(x_dim, adaln_lora_dim, bias=False),
                nn.Linear(x_dim, adaln_lora_dim, bias=False),
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：nn.Linear(adaln_lora_dim, 3 * x_dim, bias=False),
                nn.Linear(adaln_lora_dim, 3 * x_dim, bias=False),
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.adaln_modulation_self_attn = nn.Sequential(nn.SiLU(), nn.Linear(x_dim, 3 * x_dim, bias=F...
            self.adaln_modulation_self_attn = nn.Sequential(nn.SiLU(), nn.Linear(x_dim, 3 * x_dim, bias=False))
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.adaln_modulation_cross_attn = nn.Sequential(nn.SiLU(), nn.Linear(x_dim, 3 * x_dim, bias=...
            self.adaln_modulation_cross_attn = nn.Sequential(nn.SiLU(), nn.Linear(x_dim, 3 * x_dim, bias=False))
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.adaln_modulation_mlp = nn.Sequential(nn.SiLU(), nn.Linear(x_dim, 3 * x_dim, bias=False))
            self.adaln_modulation_mlp = nn.Sequential(nn.SiLU(), nn.Linear(x_dim, 3 * x_dim, bias=False))

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def reset_parameters(self) -> None:
    def reset_parameters(self) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.layer_norm_self_attn.reset_parameters()
        self.layer_norm_self_attn.reset_parameters()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.layer_norm_cross_attn.reset_parameters()
        self.layer_norm_cross_attn.reset_parameters()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.layer_norm_mlp.reset_parameters()
        self.layer_norm_mlp.reset_parameters()

        # 中文说明：根据条件选择执行分支；代码：if self.use_adaln_lora:
        if self.use_adaln_lora:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：std = 1.0 / math.sqrt(self.x_dim)
            std = 1.0 / math.sqrt(self.x_dim)
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.nn.init.trunc_normal_(self.adaln_modulation_self_attn[1].weight, std=std, a=-3 * std, b...
            torch.nn.init.trunc_normal_(self.adaln_modulation_self_attn[1].weight, std=std, a=-3 * std, b=3 * std)
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.nn.init.trunc_normal_(self.adaln_modulation_cross_attn[1].weight, std=std, a=-3 * std, ...
            torch.nn.init.trunc_normal_(self.adaln_modulation_cross_attn[1].weight, std=std, a=-3 * std, b=3 * std)
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.nn.init.trunc_normal_(self.adaln_modulation_mlp[1].weight, std=std, a=-3 * std, b=3 * std)
            torch.nn.init.trunc_normal_(self.adaln_modulation_mlp[1].weight, std=std, a=-3 * std, b=3 * std)
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.nn.init.zeros_(self.adaln_modulation_self_attn[2].weight)
            torch.nn.init.zeros_(self.adaln_modulation_self_attn[2].weight)
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.nn.init.zeros_(self.adaln_modulation_cross_attn[2].weight)
            torch.nn.init.zeros_(self.adaln_modulation_cross_attn[2].weight)
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.nn.init.zeros_(self.adaln_modulation_mlp[2].weight)
            torch.nn.init.zeros_(self.adaln_modulation_mlp[2].weight)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.nn.init.zeros_(self.adaln_modulation_self_attn[1].weight)
            torch.nn.init.zeros_(self.adaln_modulation_self_attn[1].weight)
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.nn.init.zeros_(self.adaln_modulation_cross_attn[1].weight)
            torch.nn.init.zeros_(self.adaln_modulation_cross_attn[1].weight)
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.nn.init.zeros_(self.adaln_modulation_mlp[1].weight)
            torch.nn.init.zeros_(self.adaln_modulation_mlp[1].weight)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def init_weights(self) -> None:
    def init_weights(self) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.reset_parameters()
        self.reset_parameters()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.self_attn.init_weights()
        self.self_attn.init_weights()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.cross_attn.init_weights()
        self.cross_attn.init_weights()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.mlp.init_weights()
        self.mlp.init_weights()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(
    def forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_B_T_H_W_D: torch.Tensor,
        x_B_T_H_W_D: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：emb_B_T_D: torch.Tensor,
        emb_B_T_D: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：crossattn_emb: torch.Tensor,
        crossattn_emb: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rope_emb_L_1_1_D: Optional[torch.Tensor] = None,
        rope_emb_L_1_1_D: Optional[torch.Tensor] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：adaln_lora_B_T_3D: Optional[torch.Tensor] = None,
        adaln_lora_B_T_3D: Optional[torch.Tensor] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：extra_per_block_pos_emb: Optional[torch.Tensor] = None,
        extra_per_block_pos_emb: Optional[torch.Tensor] = None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor:
    ) -> torch.Tensor:
        # 中文说明：根据条件选择执行分支；代码：if extra_per_block_pos_emb is not None:
        if extra_per_block_pos_emb is not None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_T_H_W_D = x_B_T_H_W_D + extra_per_block_pos_emb
            x_B_T_H_W_D = x_B_T_H_W_D + extra_per_block_pos_emb

        # 中文说明：根据条件选择执行分支；代码：if self.use_adaln_lora:
        if self.use_adaln_lora:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：shift_self_attn_B_T_D, scale_self_attn_B_T_D, gate_self_attn_B_T_D = (
            shift_self_attn_B_T_D, scale_self_attn_B_T_D, gate_self_attn_B_T_D = (
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.adaln_modulation_self_attn(emb_B_T_D) + adaln_lora_B_T_3D
                self.adaln_modulation_self_attn(emb_B_T_D) + adaln_lora_B_T_3D
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：).chunk(3, dim=-1)
            ).chunk(3, dim=-1)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：shift_cross_attn_B_T_D, scale_cross_attn_B_T_D, gate_cross_attn_B_T_D = (
            shift_cross_attn_B_T_D, scale_cross_attn_B_T_D, gate_cross_attn_B_T_D = (
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.adaln_modulation_cross_attn(emb_B_T_D) + adaln_lora_B_T_3D
                self.adaln_modulation_cross_attn(emb_B_T_D) + adaln_lora_B_T_3D
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：).chunk(3, dim=-1)
            ).chunk(3, dim=-1)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：shift_mlp_B_T_D, scale_mlp_B_T_D, gate_mlp_B_T_D = (
            shift_mlp_B_T_D, scale_mlp_B_T_D, gate_mlp_B_T_D = (
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.adaln_modulation_mlp(emb_B_T_D) + adaln_lora_B_T_3D
                self.adaln_modulation_mlp(emb_B_T_D) + adaln_lora_B_T_3D
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：).chunk(3, dim=-1)
            ).chunk(3, dim=-1)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：shift_self_attn_B_T_D, scale_self_attn_B_T_D, gate_self_attn_B_T_D = self.adaln_modulation_se...
            shift_self_attn_B_T_D, scale_self_attn_B_T_D, gate_self_attn_B_T_D = self.adaln_modulation_self_attn(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：emb_B_T_D
                emb_B_T_D
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：).chunk(3, dim=-1)
            ).chunk(3, dim=-1)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：shift_cross_attn_B_T_D, scale_cross_attn_B_T_D, gate_cross_attn_B_T_D = self.adaln_modulation...
            shift_cross_attn_B_T_D, scale_cross_attn_B_T_D, gate_cross_attn_B_T_D = self.adaln_modulation_cross_attn(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：emb_B_T_D
                emb_B_T_D
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：).chunk(3, dim=-1)
            ).chunk(3, dim=-1)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：shift_mlp_B_T_D, scale_mlp_B_T_D, gate_mlp_B_T_D = self.adaln_modulation_mlp(emb_B_T_D).chunk...
            shift_mlp_B_T_D, scale_mlp_B_T_D, gate_mlp_B_T_D = self.adaln_modulation_mlp(emb_B_T_D).chunk(3, dim=-1)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Reshape tensors from (B, T, D) to (B, T, 1, 1, D) for broadcasting
        # Reshape tensors from (B, T, D) to (B, T, 1, 1, D) for broadcasting
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：shift_self_attn_B_T_1_1_D = rearrange(shift_self_attn_B_T_D, "b t d -> b t 1 1 d")
        shift_self_attn_B_T_1_1_D = rearrange(shift_self_attn_B_T_D, "b t d -> b t 1 1 d")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scale_self_attn_B_T_1_1_D = rearrange(scale_self_attn_B_T_D, "b t d -> b t 1 1 d")
        scale_self_attn_B_T_1_1_D = rearrange(scale_self_attn_B_T_D, "b t d -> b t 1 1 d")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gate_self_attn_B_T_1_1_D = rearrange(gate_self_attn_B_T_D, "b t d -> b t 1 1 d")
        gate_self_attn_B_T_1_1_D = rearrange(gate_self_attn_B_T_D, "b t d -> b t 1 1 d")

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：shift_cross_attn_B_T_1_1_D = rearrange(shift_cross_attn_B_T_D, "b t d -> b t 1 1 d")
        shift_cross_attn_B_T_1_1_D = rearrange(shift_cross_attn_B_T_D, "b t d -> b t 1 1 d")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scale_cross_attn_B_T_1_1_D = rearrange(scale_cross_attn_B_T_D, "b t d -> b t 1 1 d")
        scale_cross_attn_B_T_1_1_D = rearrange(scale_cross_attn_B_T_D, "b t d -> b t 1 1 d")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gate_cross_attn_B_T_1_1_D = rearrange(gate_cross_attn_B_T_D, "b t d -> b t 1 1 d")
        gate_cross_attn_B_T_1_1_D = rearrange(gate_cross_attn_B_T_D, "b t d -> b t 1 1 d")

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：shift_mlp_B_T_1_1_D = rearrange(shift_mlp_B_T_D, "b t d -> b t 1 1 d")
        shift_mlp_B_T_1_1_D = rearrange(shift_mlp_B_T_D, "b t d -> b t 1 1 d")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scale_mlp_B_T_1_1_D = rearrange(scale_mlp_B_T_D, "b t d -> b t 1 1 d")
        scale_mlp_B_T_1_1_D = rearrange(scale_mlp_B_T_D, "b t d -> b t 1 1 d")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gate_mlp_B_T_1_1_D = rearrange(gate_mlp_B_T_D, "b t d -> b t 1 1 d")
        gate_mlp_B_T_1_1_D = rearrange(gate_mlp_B_T_D, "b t d -> b t 1 1 d")

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：B, T, H, W, D = x_B_T_H_W_D.shape
        B, T, H, W, D = x_B_T_H_W_D.shape

        # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _fn(_x_B_T_H_W_D, _norm_layer, _scale_B_T_1_1_D, _shift_B_T_1_1_D):
        def _fn(_x_B_T_H_W_D, _norm_layer, _scale_B_T_1_1_D, _shift_B_T_1_1_D):
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return _norm_layer(_x_B_T_H_W_D) * (1 + _scale_B_T_1_1_D) + _shift_B_T_1_1_D
            return _norm_layer(_x_B_T_H_W_D) * (1 + _scale_B_T_1_1_D) + _shift_B_T_1_1_D

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：normalized_x_B_T_H_W_D = _fn(
        normalized_x_B_T_H_W_D = _fn(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_B_T_H_W_D,
            x_B_T_H_W_D,
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.layer_norm_self_attn,
            self.layer_norm_self_attn,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scale_self_attn_B_T_1_1_D,
            scale_self_attn_B_T_1_1_D,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：shift_self_attn_B_T_1_1_D,
            shift_self_attn_B_T_1_1_D,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：result_B_T_H_W_D = rearrange(
        result_B_T_H_W_D = rearrange(
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.self_attn(
            self.self_attn(
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# normalized_x_B_T_HW_D,
                # normalized_x_B_T_HW_D,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rearrange(normalized_x_B_T_H_W_D, "b t h w d -> b (t h w) d"),
                rearrange(normalized_x_B_T_H_W_D, "b t h w d -> b (t h w) d"),
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None,
                None,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rope_emb=rope_emb_L_1_1_D,
                rope_emb=rope_emb_L_1_1_D,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："b (t h w) d -> b t h w d",
            "b (t h w) d -> b t h w d",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t=T,
            t=T,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h=H,
            h=H,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：w=W,
            w=W,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_T_H_W_D = x_B_T_H_W_D + gate_self_attn_B_T_1_1_D * result_B_T_H_W_D
        x_B_T_H_W_D = x_B_T_H_W_D + gate_self_attn_B_T_1_1_D * result_B_T_H_W_D

        # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _x_fn(
        def _x_fn(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_x_B_T_H_W_D: torch.Tensor,
            _x_B_T_H_W_D: torch.Tensor,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：layer_norm_cross_attn: Callable,
            layer_norm_cross_attn: Callable,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_scale_cross_attn_B_T_1_1_D: torch.Tensor,
            _scale_cross_attn_B_T_1_1_D: torch.Tensor,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_shift_cross_attn_B_T_1_1_D: torch.Tensor,
            _shift_cross_attn_B_T_1_1_D: torch.Tensor,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor:
        ) -> torch.Tensor:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_normalized_x_B_T_H_W_D = _fn(
            _normalized_x_B_T_H_W_D = _fn(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_x_B_T_H_W_D, layer_norm_cross_attn, _scale_cross_attn_B_T_1_1_D, _shift_cross_attn_B_T_1_1_D
                _x_B_T_H_W_D, layer_norm_cross_attn, _scale_cross_attn_B_T_1_1_D, _shift_cross_attn_B_T_1_1_D
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_result_B_T_H_W_D = rearrange(
            _result_B_T_H_W_D = rearrange(
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.cross_attn(
                self.cross_attn(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rearrange(_normalized_x_B_T_H_W_D, "b t h w d -> b (t h w) d"),
                    rearrange(_normalized_x_B_T_H_W_D, "b t h w d -> b (t h w) d"),
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：crossattn_emb,
                    crossattn_emb,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rope_emb=rope_emb_L_1_1_D,
                    rope_emb=rope_emb_L_1_1_D,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ori_size=[B, T, H, W]
                    ori_size=[B, T, H, W]
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
                ),
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："b (t h w) d -> b t h w d",
                "b (t h w) d -> b t h w d",
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t=T,
                t=T,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h=H,
                h=H,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：w=W,
                w=W,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return _result_B_T_H_W_D
            return _result_B_T_H_W_D

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：result_B_T_H_W_D = _x_fn(
        result_B_T_H_W_D = _x_fn(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_B_T_H_W_D,
            x_B_T_H_W_D,
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.layer_norm_cross_attn,
            self.layer_norm_cross_attn,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scale_cross_attn_B_T_1_1_D,
            scale_cross_attn_B_T_1_1_D,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：shift_cross_attn_B_T_1_1_D,
            shift_cross_attn_B_T_1_1_D,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_T_H_W_D = result_B_T_H_W_D * gate_cross_attn_B_T_1_1_D + x_B_T_H_W_D
        x_B_T_H_W_D = result_B_T_H_W_D * gate_cross_attn_B_T_1_1_D + x_B_T_H_W_D

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：normalized_x_B_T_H_W_D = _fn(
        normalized_x_B_T_H_W_D = _fn(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_B_T_H_W_D,
            x_B_T_H_W_D,
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.layer_norm_mlp,
            self.layer_norm_mlp,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scale_mlp_B_T_1_1_D,
            scale_mlp_B_T_1_1_D,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：shift_mlp_B_T_1_1_D,
            shift_mlp_B_T_1_1_D,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：result_B_T_H_W_D = self.mlp(normalized_x_B_T_H_W_D)
        result_B_T_H_W_D = self.mlp(normalized_x_B_T_H_W_D)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_T_H_W_D = x_B_T_H_W_D + gate_mlp_B_T_1_1_D * result_B_T_H_W_D
        x_B_T_H_W_D = x_B_T_H_W_D + gate_mlp_B_T_1_1_D * result_B_T_H_W_D
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x_B_T_H_W_D
        return x_B_T_H_W_D


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class MiniTrainDIT(WeightTrainingStat):
class MiniTrainDIT(WeightTrainingStat):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    A clean impl of DIT that can load and  reproduce the training results of the original DIT model in~(cosmos 1)
    A general implementation of adaln-modulated VIT-like~(DiT) transformer for video processing.

    Args:
        max_img_h (int): Maximum height of the input images.
        max_img_w (int): Maximum width of the input images.
        max_frames (int): Maximum number of frames in the video sequence.
        in_channels (int): Number of input channels (e.g., RGB channels for color images).
        out_channels (int): Number of output channels.
        patch_spatial (tuple): Spatial resolution of patches for input processing.
        patch_temporal (int): Temporal resolution of patches for input processing.
        concat_padding_mask (bool): If True, includes a mask channel in the input to handle padding.
        model_channels (int): Base number of channels used throughout the model.
        num_blocks (int): Number of transformer blocks.
        num_heads (int): Number of heads in the multi-head attention layers.
        mlp_ratio (float): Expansion ratio for MLP blocks.
        crossattn_emb_channels (int): Number of embedding channels for cross-attention.
        pos_emb_cls (str): Type of positional embeddings.
        pos_emb_learnable (bool): Whether positional embeddings are learnable.
        pos_emb_interpolation (str): Method for interpolating positional embeddings.
        min_fps (int): Minimum frames per second.
        max_fps (int): Maximum frames per second.
        use_adaln_lora (bool): Whether to use AdaLN-LoRA.
        adaln_lora_dim (int): Dimension for AdaLN-LoRA.
        rope_h_extrapolation_ratio (float): Height extrapolation ratio for RoPE.
        rope_w_extrapolation_ratio (float): Width extrapolation ratio for RoPE.
        rope_t_extrapolation_ratio (float): Temporal extrapolation ratio for RoPE.
        extra_per_block_abs_pos_emb (bool): Whether to use extra per-block absolute positional embeddings.
        extra_h_extrapolation_ratio (float): Height extrapolation ratio for extra embeddings.
        extra_w_extrapolation_ratio (float): Width extrapolation ratio for extra embeddings.
        extra_t_extrapolation_ratio (float): Temporal extrapolation ratio for extra embeddings.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_img_h: int,
        max_img_h: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_img_w: int,
        max_img_w: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_frames: int,
        max_frames: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：in_channels: int,
        in_channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out_channels: int,
        out_channels: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：patch_spatial: int, # tuple,
        patch_spatial: int,  # tuple,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：patch_temporal: int,
        patch_temporal: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：concat_padding_mask: bool = True,
        concat_padding_mask: bool = True,
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# attention settings
        # attention settings
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model_channels: int = 768,
        model_channels: int = 768,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_blocks: int = 10,
        num_blocks: int = 10,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_heads: int = 16,
        num_heads: int = 16,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：mlp_ratio: float = 4.0,
        mlp_ratio: float = 4.0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：atten_backend: str = "transformer_engine",
        atten_backend: str = "transformer_engine",
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# cross attention settings
        # cross attention settings
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：crossattn_emb_channels: int = 1024,
        crossattn_emb_channels: int = 1024,
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# positional embedding settings
        # positional embedding settings
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pos_emb_cls: str = "sincos",
        pos_emb_cls: str = "sincos",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pos_emb_learnable: bool = False,
        pos_emb_learnable: bool = False,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pos_emb_interpolation: str = "crop",
        pos_emb_interpolation: str = "crop",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：min_fps: int = 1,
        min_fps: int = 1,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_fps: int = 30,
        max_fps: int = 30,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：use_adaln_lora: bool = False,
        use_adaln_lora: bool = False,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：adaln_lora_dim: int = 256,
        adaln_lora_dim: int = 256,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rope_h_extrapolation_ratio: float = 1.0,
        rope_h_extrapolation_ratio: float = 1.0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rope_w_extrapolation_ratio: float = 1.0,
        rope_w_extrapolation_ratio: float = 1.0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rope_t_extrapolation_ratio: float = 1.0,
        rope_t_extrapolation_ratio: float = 1.0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：extra_per_block_abs_pos_emb: bool = False,
        extra_per_block_abs_pos_emb: bool = False,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：extra_h_extrapolation_ratio: float = 1.0,
        extra_h_extrapolation_ratio: float = 1.0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：extra_w_extrapolation_ratio: float = 1.0,
        extra_w_extrapolation_ratio: float = 1.0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：extra_t_extrapolation_ratio: float = 1.0,
        extra_t_extrapolation_ratio: float = 1.0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rope_enable_fps_modulation: bool = True,
        rope_enable_fps_modulation: bool = True,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sac_config: SACConfig = SACConfig(),
        sac_config: SACConfig = SACConfig(),
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：causal_cross_attn: bool = False,
        causal_cross_attn: bool = False,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**kwargs,
        **kwargs,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.max_img_h = max_img_h
        self.max_img_h = max_img_h
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.max_img_w = max_img_w
        self.max_img_w = max_img_w
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.max_frames = max_frames
        self.max_frames = max_frames
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.in_channels = in_channels
        self.in_channels = in_channels
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.out_channels = out_channels
        self.out_channels = out_channels
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.patch_spatial = patch_spatial
        self.patch_spatial = patch_spatial
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.patch_temporal = patch_temporal
        self.patch_temporal = patch_temporal
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_heads = num_heads
        self.num_heads = num_heads
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_blocks = num_blocks
        self.num_blocks = num_blocks
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.model_channels = model_channels
        self.model_channels = model_channels
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.concat_padding_mask = concat_padding_mask
        self.concat_padding_mask = concat_padding_mask
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.atten_backend = atten_backend
        self.atten_backend = atten_backend
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# positional embedding settings
        # positional embedding settings
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.pos_emb_cls = pos_emb_cls
        self.pos_emb_cls = pos_emb_cls
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.pos_emb_learnable = pos_emb_learnable
        self.pos_emb_learnable = pos_emb_learnable
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.pos_emb_interpolation = pos_emb_interpolation
        self.pos_emb_interpolation = pos_emb_interpolation
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.min_fps = min_fps
        self.min_fps = min_fps
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.max_fps = max_fps
        self.max_fps = max_fps
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.rope_h_extrapolation_ratio = rope_h_extrapolation_ratio
        self.rope_h_extrapolation_ratio = rope_h_extrapolation_ratio
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.rope_w_extrapolation_ratio = rope_w_extrapolation_ratio
        self.rope_w_extrapolation_ratio = rope_w_extrapolation_ratio
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.rope_t_extrapolation_ratio = rope_t_extrapolation_ratio
        self.rope_t_extrapolation_ratio = rope_t_extrapolation_ratio
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.extra_per_block_abs_pos_emb = extra_per_block_abs_pos_emb
        self.extra_per_block_abs_pos_emb = extra_per_block_abs_pos_emb
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.extra_h_extrapolation_ratio = extra_h_extrapolation_ratio
        self.extra_h_extrapolation_ratio = extra_h_extrapolation_ratio
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.extra_w_extrapolation_ratio = extra_w_extrapolation_ratio
        self.extra_w_extrapolation_ratio = extra_w_extrapolation_ratio
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.extra_t_extrapolation_ratio = extra_t_extrapolation_ratio
        self.extra_t_extrapolation_ratio = extra_t_extrapolation_ratio
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.rope_enable_fps_modulation = rope_enable_fps_modulation
        self.rope_enable_fps_modulation = rope_enable_fps_modulation
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.cuda_graphs = {}
        self.cuda_graphs = {}
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.causal_cross_attn = causal_cross_attn
        self.causal_cross_attn = causal_cross_attn

        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.build_patch_embed()
        self.build_patch_embed()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.build_pos_embed()
        self.build_pos_embed()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.use_adaln_lora = use_adaln_lora
        self.use_adaln_lora = use_adaln_lora
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.adaln_lora_dim = adaln_lora_dim
        self.adaln_lora_dim = adaln_lora_dim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.t_embedder = nn.Sequential(
        self.t_embedder = nn.Sequential(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：Timesteps(model_channels),
            Timesteps(model_channels),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：TimestepEmbedding(model_channels, model_channels, use_adaln_lora=use_adaln_lora),
            TimestepEmbedding(model_channels, model_channels, use_adaln_lora=use_adaln_lora),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：layer_mask = kwargs.get("layer_mask", None)
        layer_mask = kwargs.get("layer_mask", None)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：layer_mask = [False] * num_blocks if layer_mask is None else layer_mask
        layer_mask = [False] * num_blocks if layer_mask is None else layer_mask
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.blocks = nn.ModuleList(
        self.blocks = nn.ModuleList(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：[
            [
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：Block(
                Block(
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_dim=model_channels,
                    x_dim=model_channels,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：context_dim=crossattn_emb_channels,
                    context_dim=crossattn_emb_channels,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_heads=num_heads,
                    num_heads=num_heads,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mlp_ratio=mlp_ratio,
                    mlp_ratio=mlp_ratio,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_adaln_lora=use_adaln_lora,
                    use_adaln_lora=use_adaln_lora,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：adaln_lora_dim=adaln_lora_dim,
                    adaln_lora_dim=adaln_lora_dim,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend=atten_backend,
                    backend=atten_backend,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：causal_cross_attn=causal_cross_attn,
                    causal_cross_attn=causal_cross_attn,
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for idx in range(num_blocks) if not layer_mask[idx]
                for idx in range(num_blocks) if not layer_mask[idx]
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
            ]
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.final_layer = FinalLayer(
        self.final_layer = FinalLayer(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hidden_size=self.model_channels,
            hidden_size=self.model_channels,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：spatial_patch_size=self.patch_spatial,
            spatial_patch_size=self.patch_spatial,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_patch_size=self.patch_temporal,
            temporal_patch_size=self.patch_temporal,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=self.out_channels,
            out_channels=self.out_channels,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_adaln_lora=self.use_adaln_lora,
            use_adaln_lora=self.use_adaln_lora,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：adaln_lora_dim=self.adaln_lora_dim,
            adaln_lora_dim=self.adaln_lora_dim,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.t_embedding_norm = te.pytorch.RMSNorm(model_channels, eps=1e-6)
        self.t_embedding_norm = te.pytorch.RMSNorm(model_channels, eps=1e-6)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.init_weights()
        self.init_weights()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.enable_selective_checkpoint(sac_config)
        self.enable_selective_checkpoint(sac_config)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._is_context_parallel_enabled = False
        self._is_context_parallel_enabled = False

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def init_weights(self) -> None:
    def init_weights(self) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.x_embedder.init_weights()
        self.x_embedder.init_weights()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.pos_embedder.reset_parameters()
        self.pos_embedder.reset_parameters()
        # 中文说明：根据条件选择执行分支；代码：if self.extra_per_block_abs_pos_emb:
        if self.extra_per_block_abs_pos_emb:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.extra_pos_embedder.reset_parameters()
            self.extra_pos_embedder.reset_parameters()

        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.t_embedder[1].init_weights()
        self.t_embedder[1].init_weights()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for block in self.blocks:
        for block in self.blocks:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：block.init_weights()
            block.init_weights()

        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.final_layer.init_weights()
        self.final_layer.init_weights()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.t_embedding_norm.reset_parameters()
        self.t_embedding_norm.reset_parameters()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def build_patch_embed(self) -> None:
    def build_patch_embed(self) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：(
        (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：concat_padding_mask,
            concat_padding_mask,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：in_channels,
            in_channels,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：patch_spatial,
            patch_spatial,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：patch_temporal,
            patch_temporal,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model_channels,
            model_channels,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) = (
        ) = (
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.concat_padding_mask,
            self.concat_padding_mask,
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.in_channels,
            self.in_channels,
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.patch_spatial,
            self.patch_spatial,
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.patch_temporal,
            self.patch_temporal,
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.model_channels,
            self.model_channels,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels = in_channels + 1 if concat_padding_mask else in_channels
        in_channels = in_channels + 1 if concat_padding_mask else in_channels
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.x_embedder = PatchEmbed(
        self.x_embedder = PatchEmbed(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：spatial_patch_size=patch_spatial,
            spatial_patch_size=patch_spatial,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_patch_size=patch_temporal,
            temporal_patch_size=patch_temporal,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=in_channels,
            in_channels=in_channels,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=model_channels,
            out_channels=model_channels,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def build_pos_embed(self) -> None:
    def build_pos_embed(self) -> None:
        # 中文说明：根据条件选择执行分支；代码：if self.pos_emb_cls == "rope3d":
        if self.pos_emb_cls == "rope3d":
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cls_type = VideoRopePosition3DEmb
            cls_type = VideoRopePosition3DEmb
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Unknown pos_emb_cls {self.pos_emb_cls}")
            raise ValueError(f"Unknown pos_emb_cls {self.pos_emb_cls}")

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(f"Building positional embedding with {self.pos_emb_cls} class, impl {cls_type}")
        log.debug(f"Building positional embedding with {self.pos_emb_cls} class, impl {cls_type}")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs = dict(
        kwargs = dict(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_channels=self.model_channels,
            model_channels=self.model_channels,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：len_h=self.max_img_h // self.patch_spatial,
            len_h=self.max_img_h // self.patch_spatial,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：len_w=self.max_img_w // self.patch_spatial,
            len_w=self.max_img_w // self.patch_spatial,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：len_t=self.max_frames // self.patch_temporal,
            len_t=self.max_frames // self.patch_temporal,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_fps=self.max_fps,
            max_fps=self.max_fps,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_fps=self.min_fps,
            min_fps=self.min_fps,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_learnable=self.pos_emb_learnable,
            is_learnable=self.pos_emb_learnable,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：interpolation=self.pos_emb_interpolation,
            interpolation=self.pos_emb_interpolation,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：head_dim=self.model_channels // self.num_heads,
            head_dim=self.model_channels // self.num_heads,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h_extrapolation_ratio=self.rope_h_extrapolation_ratio,
            h_extrapolation_ratio=self.rope_h_extrapolation_ratio,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：w_extrapolation_ratio=self.rope_w_extrapolation_ratio,
            w_extrapolation_ratio=self.rope_w_extrapolation_ratio,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t_extrapolation_ratio=self.rope_t_extrapolation_ratio,
            t_extrapolation_ratio=self.rope_t_extrapolation_ratio,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enable_fps_modulation=self.rope_enable_fps_modulation,
            enable_fps_modulation=self.rope_enable_fps_modulation,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.pos_embedder = cls_type(
        self.pos_embedder = cls_type(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**kwargs, # type: ignore
            **kwargs,  # type: ignore
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：根据条件选择执行分支；代码：if self.extra_per_block_abs_pos_emb:
        if self.extra_per_block_abs_pos_emb:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["h_extrapolation_ratio"] = self.extra_h_extrapolation_ratio
            kwargs["h_extrapolation_ratio"] = self.extra_h_extrapolation_ratio
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["w_extrapolation_ratio"] = self.extra_w_extrapolation_ratio
            kwargs["w_extrapolation_ratio"] = self.extra_w_extrapolation_ratio
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["t_extrapolation_ratio"] = self.extra_t_extrapolation_ratio
            kwargs["t_extrapolation_ratio"] = self.extra_t_extrapolation_ratio
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.extra_pos_embedder = LearnablePosEmbAxis(
            self.extra_pos_embedder = LearnablePosEmbAxis(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**kwargs, # type: ignore
                **kwargs,  # type: ignore
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def prepare_embedded_sequence(
    def prepare_embedded_sequence(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_B_C_T_H_W: torch.Tensor,
        x_B_C_T_H_W: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：fps: Optional[torch.Tensor] = None,
        fps: Optional[torch.Tensor] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：padding_mask: Optional[torch.Tensor] = None,
        padding_mask: Optional[torch.Tensor] = None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[torch.Tensor, Optional[torch.Tensor], Optional[torch.Tensor]]:
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor], Optional[torch.Tensor]]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Prepares an embedded sequence tensor by applying positional embeddings and handling padding masks.

        Args:
            x_B_C_T_H_W (torch.Tensor): video
            fps (Optional[torch.Tensor]): Frames per second tensor to be used for positional embedding when required.
                                    If None, a default value (`self.base_fps`) will be used.
            padding_mask (Optional[torch.Tensor]): current it is not used

        Returns:
            Tuple[torch.Tensor, Optional[torch.Tensor]]:
                - A tensor of shape (B, T, H, W, D) with the embedded sequence.
                - An optional positional embedding tensor, returned only if the positional embedding class
                (`self.pos_emb_cls`) includes 'rope'. Otherwise, None.

        Notes:
            - If `self.concat_padding_mask` is True, a padding mask channel is concatenated to the input tensor.
            - The method of applying positional embeddings depends on the value of `self.pos_emb_cls`.
            - If 'rope' is in `self.pos_emb_cls` (case insensitive), the positional embeddings are generated using
                the `self.pos_embedder` with the shape [T, H, W].
            - If "fps_aware" is in `self.pos_emb_cls`, the positional embeddings are generated using the
            `self.pos_embedder` with the fps tensor.
            - Otherwise, the positional embeddings are generated without considering fps.
        """
        # 中文说明：根据条件选择执行分支；代码：if self.concat_padding_mask:
        if self.concat_padding_mask:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding_mask = transforms.functional.resize(
            padding_mask = transforms.functional.resize(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：padding_mask, list(x_B_C_T_H_W.shape[-2:]), interpolation=transforms.InterpolationMode.NEAREST
                padding_mask, list(x_B_C_T_H_W.shape[-2:]), interpolation=transforms.InterpolationMode.NEAREST
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_C_T_H_W = torch.cat(
            x_B_C_T_H_W = torch.cat(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：[x_B_C_T_H_W, padding_mask.unsqueeze(1).repeat(1, 1, x_B_C_T_H_W.shape[2], 1, 1)], dim=1
                [x_B_C_T_H_W, padding_mask.unsqueeze(1).repeat(1, 1, x_B_C_T_H_W.shape[2], 1, 1)], dim=1
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_T_H_W_D = self.x_embedder(x_B_C_T_H_W)
        x_B_T_H_W_D = self.x_embedder(x_B_C_T_H_W)

        # 中文说明：根据条件选择执行分支；代码：if self.extra_per_block_abs_pos_emb:
        if self.extra_per_block_abs_pos_emb:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extra_pos_emb = self.extra_pos_embedder(x_B_T_H_W_D, fps=fps)
            extra_pos_emb = self.extra_pos_embedder(x_B_T_H_W_D, fps=fps)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extra_pos_emb = None
            extra_pos_emb = None

        # 中文说明：根据条件选择执行分支；代码：if "rope" in self.pos_emb_cls.lower():
        if "rope" in self.pos_emb_cls.lower():
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return x_B_T_H_W_D, self.pos_embedder(x_B_T_H_W_D, fps=fps), extra_pos_emb
            return x_B_T_H_W_D, self.pos_embedder(x_B_T_H_W_D, fps=fps), extra_pos_emb
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_T_H_W_D = x_B_T_H_W_D + self.pos_embedder(x_B_T_H_W_D) # [B, T, H, W, D]
        x_B_T_H_W_D = x_B_T_H_W_D + self.pos_embedder(x_B_T_H_W_D)  # [B, T, H, W, D]

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x_B_T_H_W_D, None, extra_pos_emb
        return x_B_T_H_W_D, None, extra_pos_emb

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def unpatchify(self, x_B_T_H_W_M: torch.Tensor) -> torch.Tensor:
    def unpatchify(self, x_B_T_H_W_M: torch.Tensor) -> torch.Tensor:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_C_Tt_Hp_Wp = rearrange(
        x_B_C_Tt_Hp_Wp = rearrange(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_B_T_H_W_M,
            x_B_T_H_W_M,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："B T H W (p1 p2 t C) -> B C (T t) (H p1) (W p2)",
            "B T H W (p1 p2 t C) -> B C (T t) (H p1) (W p2)",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：p1=self.patch_spatial,
            p1=self.patch_spatial,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：p2=self.patch_spatial,
            p2=self.patch_spatial,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t=self.patch_temporal,
            t=self.patch_temporal,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x_B_C_Tt_Hp_Wp
        return x_B_C_Tt_Hp_Wp

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(
    def forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_B_C_T_H_W: torch.Tensor,
        x_B_C_T_H_W: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：timesteps_B_T: torch.Tensor,
        timesteps_B_T: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：crossattn_emb: torch.Tensor,
        crossattn_emb: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：fps: Optional[torch.Tensor] = None,
        fps: Optional[torch.Tensor] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：padding_mask: Optional[torch.Tensor] = None,
        padding_mask: Optional[torch.Tensor] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_type: Optional[DataType] = DataType.VIDEO,
        data_type: Optional[DataType] = DataType.VIDEO,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：use_cuda_graphs: bool = False,
        use_cuda_graphs: bool = False,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_ctrl: Optional[dict] = None,
        x_ctrl: Optional[dict] = None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor | List[torch.Tensor] | Tuple[torch.Tensor, List[torch.Tensor]]:
    ) -> torch.Tensor | List[torch.Tensor] | Tuple[torch.Tensor, List[torch.Tensor]]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Args:
            x: (B, C, T, H, W) tensor of spatial-temp inputs
            timesteps: (B, ) tensor of timesteps
            crossattn_emb: (B, N, D) tensor of cross-attention embeddings
        """
        # 中文说明：检查运行时假设是否成立；代码：assert isinstance(
        assert isinstance(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_type, DataType
            data_type, DataType
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"Expected DataType, got {type(data_type)}. We need discuss this flag later."
        ), f"Expected DataType, got {type(data_type)}. We need discuss this flag later."
        # 中文说明：检查运行时假设是否成立；代码：assert not (self.training and use_cuda_graphs), "CUDA Graphs are supported only for inference"
        assert not (self.training and use_cuda_graphs), "CUDA Graphs are supported only for inference"
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_B_T_H_W_D, rope_emb_L_1_1_D, extra_pos_emb_B_T_H_W_D_or_T_H_W_B_D = self.prepare_embedded_s...
        x_B_T_H_W_D, rope_emb_L_1_1_D, extra_pos_emb_B_T_H_W_D_or_T_H_W_B_D = self.prepare_embedded_sequence(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_B_C_T_H_W,
            x_B_C_T_H_W,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fps=fps,
            fps=fps,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding_mask=padding_mask,
            padding_mask=padding_mask,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：根据条件选择执行分支；代码：if timesteps_B_T.ndim == 1:
        if timesteps_B_T.ndim == 1:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：timesteps_B_T = timesteps_B_T.unsqueeze(1)
            timesteps_B_T = timesteps_B_T.unsqueeze(1)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：t_embedding_B_T_D, adaln_lora_B_T_3D = self.t_embedder(timesteps_B_T)
        t_embedding_B_T_D, adaln_lora_B_T_3D = self.t_embedder(timesteps_B_T)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t_embedding_B_T_D = self.t_embedding_norm(t_embedding_B_T_D)
        t_embedding_B_T_D = self.t_embedding_norm(t_embedding_B_T_D)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# for logging purpose
        # for logging purpose
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：affline_scale_log_info = {}
        affline_scale_log_info = {}
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：affline_scale_log_info["t_embedding_B_T_D"] = t_embedding_B_T_D.detach()
        affline_scale_log_info["t_embedding_B_T_D"] = t_embedding_B_T_D.detach()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.affline_scale_log_info = affline_scale_log_info
        self.affline_scale_log_info = affline_scale_log_info
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.affline_emb = t_embedding_B_T_D
        self.affline_emb = t_embedding_B_T_D
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.crossattn_emb = crossattn_emb
        self.crossattn_emb = crossattn_emb

        # 中文说明：根据条件选择执行分支；代码：if extra_pos_emb_B_T_H_W_D_or_T_H_W_B_D is not None:
        if extra_pos_emb_B_T_H_W_D_or_T_H_W_B_D is not None:
            # 中文说明：检查运行时假设是否成立；代码：assert (
            assert (
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_T_H_W_D.shape == extra_pos_emb_B_T_H_W_D_or_T_H_W_B_D.shape
                x_B_T_H_W_D.shape == extra_pos_emb_B_T_H_W_D_or_T_H_W_B_D.shape
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"{x_B_T_H_W_D.shape} != {extra_pos_emb_B_T_H_W_D_or_T_H_W_B_D.shape}"
            ), f"{x_B_T_H_W_D.shape} != {extra_pos_emb_B_T_H_W_D_or_T_H_W_B_D.shape}"

        # 中文说明：根据条件选择执行分支；代码：if use_cuda_graphs:
        if use_cuda_graphs:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：shapes_key = create_cuda_graph(
            shapes_key = create_cuda_graph(
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.cuda_graphs,
                self.cuda_graphs,
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.blocks,
                self.blocks,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_B_T_H_W_D,
                x_B_T_H_W_D,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：t_embedding_B_T_D,
                t_embedding_B_T_D,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：crossattn_emb,
                crossattn_emb,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rope_emb_L_1_1_D,
                rope_emb_L_1_1_D,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：adaln_lora_B_T_3D,
                adaln_lora_B_T_3D,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：extra_pos_emb_B_T_H_W_D_or_T_H_W_B_D,
                extra_pos_emb_B_T_H_W_D_or_T_H_W_B_D,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：blocks = self.cuda_graphs[shapes_key]
            blocks = self.cuda_graphs[shapes_key]
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：blocks = self.blocks
            blocks = self.blocks

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_kwargs = {
        block_kwargs = {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："rope_emb_L_1_1_D": rope_emb_L_1_1_D,
            "rope_emb_L_1_1_D": rope_emb_L_1_1_D,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："adaln_lora_B_T_3D": adaln_lora_B_T_3D,
            "adaln_lora_B_T_3D": adaln_lora_B_T_3D,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："extra_per_block_pos_emb": extra_pos_emb_B_T_H_W_D_or_T_H_W_B_D,
            "extra_per_block_pos_emb": extra_pos_emb_B_T_H_W_D_or_T_H_W_B_D,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for idx, block in enumerate(blocks):
        for idx, block in enumerate(blocks):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_T_H_W_D = block(
            x_B_T_H_W_D = block(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_B_T_H_W_D,
                x_B_T_H_W_D,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：t_embedding_B_T_D,
                t_embedding_B_T_D,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：crossattn_emb,
                crossattn_emb,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**block_kwargs,
                **block_kwargs,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name = f"block{idx}"
            name = f"block{idx}"
            # 中文说明：根据条件选择执行分支；代码：if x_ctrl is not None and name in x_ctrl:
            if x_ctrl is not None and name in x_ctrl:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_T_H_W_D = x_B_T_H_W_D + x_ctrl[name]
                x_B_T_H_W_D = x_B_T_H_W_D + x_ctrl[name]

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_T_H_W_O = self.final_layer(x_B_T_H_W_D, t_embedding_B_T_D, adaln_lora_B_T_3D=adaln_lora_B...
        x_B_T_H_W_O = self.final_layer(x_B_T_H_W_D, t_embedding_B_T_D, adaln_lora_B_T_3D=adaln_lora_B_T_3D)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_C_Tt_Hp_Wp = self.unpatchify(x_B_T_H_W_O)
        x_B_C_Tt_Hp_Wp = self.unpatchify(x_B_T_H_W_O)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x_B_C_Tt_Hp_Wp
        return x_B_C_Tt_Hp_Wp

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def enable_selective_checkpoint(self, sac_config: SACConfig):
    def enable_selective_checkpoint(self, sac_config: SACConfig):
        # 中文说明：根据条件选择执行分支；代码：if sac_config.mode == CheckpointMode.NONE:
        if sac_config.mode == CheckpointMode.NONE:
            # 中文说明：执行循环控制或空操作；代码：pass
            pass
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(
            log.debug(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Enable selective checkpoint with {sac_config.mode}, for every {sac_config.every_n_blocks} b...
                f"Enable selective checkpoint with {sac_config.mode}, for every {sac_config.every_n_blocks} blocks. Total blocks: {len(self.blocks)}"
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_context_fn = sac_config.get_context_fn()
            _context_fn = sac_config.get_context_fn()
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for block_id, block in self.blocks.named_children():
            for block_id, block in self.blocks.named_children():
                # 中文说明：根据条件选择执行分支；代码：if int(block_id) % sac_config.every_n_blocks == 0:
                if int(block_id) % sac_config.every_n_blocks == 0:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(f"Enable selective checkpoint for block {block_id}")
                    log.debug(f"Enable selective checkpoint for block {block_id}")
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block = ptd_checkpoint_wrapper(
                    block = ptd_checkpoint_wrapper(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：block,
                        block,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：context_fn=_context_fn,
                        context_fn=_context_fn,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：preserve_rng_state=False,
                        preserve_rng_state=False,
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.blocks.register_module(block_id, block)
                    self.blocks.register_module(block_id, block)
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.register_module(
            self.register_module(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："final_layer",
                "final_layer",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ptd_checkpoint_wrapper(
                ptd_checkpoint_wrapper(
                    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.final_layer,
                    self.final_layer,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：context_fn=_context_fn,
                    context_fn=_context_fn,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：preserve_rng_state=False,
                    preserve_rng_state=False,
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
                ),
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self
        return self

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def fully_shard(self, mesh: DeviceMesh) -> None:
    def fully_shard(self, mesh: DeviceMesh) -> None:
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i, block in enumerate(self.blocks):
        for i, block in enumerate(self.blocks):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：reshard_after_forward = i < len(self.blocks) - 1
            reshard_after_forward = i < len(self.blocks) - 1
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：fully_shard(block, mesh=mesh, reshard_after_forward=reshard_after_forward)
            fully_shard(block, mesh=mesh, reshard_after_forward=reshard_after_forward)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：fully_shard(self.final_layer, mesh=mesh, reshard_after_forward=True)
        fully_shard(self.final_layer, mesh=mesh, reshard_after_forward=True)
        # 中文说明：根据条件选择执行分支；代码：if self.extra_per_block_abs_pos_emb:
        if self.extra_per_block_abs_pos_emb:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：fully_shard(self.extra_pos_embedder, mesh=mesh, reshard_after_forward=True)
            fully_shard(self.extra_pos_embedder, mesh=mesh, reshard_after_forward=True)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：fully_shard(self.t_embedder, mesh=mesh, reshard_after_forward=True)
        fully_shard(self.t_embedder, mesh=mesh, reshard_after_forward=True)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def disable_context_parallel(self) -> None:
    def disable_context_parallel(self) -> None:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# pos_embedder
        # pos_embedder
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.pos_embedder.disable_context_parallel()
        self.pos_embedder.disable_context_parallel()
        # 中文说明：根据条件选择执行分支；代码：if self.extra_per_block_abs_pos_emb:
        if self.extra_per_block_abs_pos_emb:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.extra_pos_embedder.disable_context_parallel()
            self.extra_pos_embedder.disable_context_parallel()

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# attention
        # attention
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for block in self.blocks:
        for block in self.blocks:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：block.self_attn.set_context_parallel_group(
            block.self_attn.set_context_parallel_group(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：process_group=None,
                process_group=None,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ranks=None,
                ranks=None,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stream=torch.cuda.Stream(),
                stream=torch.cuda.Stream(),
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._is_context_parallel_enabled = False
        self._is_context_parallel_enabled = False

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def enable_context_parallel(self, process_group: Optional[ProcessGroup] = None) -> None:
    def enable_context_parallel(self, process_group: Optional[ProcessGroup] = None) -> None:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# pos_embedder
        # pos_embedder
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.pos_embedder.enable_context_parallel(process_group=process_group)
        self.pos_embedder.enable_context_parallel(process_group=process_group)
        # 中文说明：根据条件选择执行分支；代码：if self.extra_per_block_abs_pos_emb:
        if self.extra_per_block_abs_pos_emb:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.extra_pos_embedder.enable_context_parallel(process_group=process_group)
            self.extra_pos_embedder.enable_context_parallel(process_group=process_group)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# attention
        # attention
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cp_ranks = get_process_group_ranks(process_group)
        cp_ranks = get_process_group_ranks(process_group)
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for block in self.blocks:
        for block in self.blocks:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：block.self_attn.set_context_parallel_group(
            block.self_attn.set_context_parallel_group(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：process_group=process_group,
                process_group=process_group,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ranks=cp_ranks,
                ranks=cp_ranks,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stream=torch.cuda.Stream(),
                stream=torch.cuda.Stream(),
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._is_context_parallel_enabled = True
        self._is_context_parallel_enabled = True

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_context_parallel_enabled(self) -> bool:
    def is_context_parallel_enabled(self) -> bool:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self._is_context_parallel_enabled
        return self._is_context_parallel_enabled
