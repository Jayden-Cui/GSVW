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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from __future__ import annotations
from __future__ import annotations

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import itertools
import itertools
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any
from typing import Any

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.distributed as dist
import torch.distributed as dist
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed import DeviceMesh
from torch.distributed import DeviceMesh
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed.tensor import DTensor
from torch.distributed.tensor import DTensor

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.misc import get_local_tensor_if_DTensor
from imaginaire.utils.misc import get_local_tensor_if_DTensor


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class DTensorFastEmaModelUpdater:
class DTensorFastEmaModelUpdater:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Similar as FastEmaModelUpdater
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self):
    def __init__(self):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Flag to indicate whether the cache is taken or not. Useful to avoid cache overwrite
        # Flag to indicate whether the cache is taken or not. Useful to avoid cache overwrite
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.is_cached = False
        self.is_cached = False

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.no_grad()
    @torch.no_grad()
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def copy_to(self, src_model: torch.nn.Module, tgt_model: torch.nn.Module) -> None:
    def copy_to(self, src_model: torch.nn.Module, tgt_model: torch.nn.Module) -> None:
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for tgt_params, src_params in zip(tgt_model.parameters(), src_model.parameters()):
        for tgt_params, src_params in zip(tgt_model.parameters(), src_model.parameters()):
            # 中文说明：根据条件选择执行分支；代码：if isinstance(tgt_params, DTensor) and isinstance(src_params, DTensor):
            if isinstance(tgt_params, DTensor) and isinstance(src_params, DTensor):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：tgt_params.to_local().data.copy_(src_params.to_local().data)
                tgt_params.to_local().data.copy_(src_params.to_local().data)
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：tgt_params.to_local().data.copy_(src_params.to_local().data)
                tgt_params.to_local().data.copy_(src_params.to_local().data)

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.no_grad()
    @torch.no_grad()
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def update_average(self, src_model: torch.nn.Module, tgt_model: torch.nn.Module, beta: float ...
    def update_average(self, src_model: torch.nn.Module, tgt_model: torch.nn.Module, beta: float = 0.9999) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：target_list = []
        target_list = []
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：source_list = []
        source_list = []
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for tgt_params, src_params in zip(tgt_model.parameters(), src_model.parameters()):
        for tgt_params, src_params in zip(tgt_model.parameters(), src_model.parameters()):
            # 中文说明：检查运行时假设是否成立；代码：assert (
            assert (
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tgt_params.dtype == torch.float32
                tgt_params.dtype == torch.float32
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"EMA model only works in FP32 dtype, got {tgt_params.dtype} instead."
            ), f"EMA model only works in FP32 dtype, got {tgt_params.dtype} instead."
            # 中文说明：根据条件选择执行分支；代码：if isinstance(tgt_params, DTensor) and isinstance(src_params, DTensor):
            if isinstance(tgt_params, DTensor) and isinstance(src_params, DTensor):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：target_list.append(tgt_params.to_local())
                target_list.append(tgt_params.to_local())
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：source_list.append(src_params.to_local().data)
                source_list.append(src_params.to_local().data)
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：target_list.append(tgt_params)
                target_list.append(tgt_params)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：source_list.append(src_params.data)
                source_list.append(src_params.data)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch._foreach_mul_(target_list, beta)
        torch._foreach_mul_(target_list, beta)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch._foreach_add_(target_list, source_list, alpha=1.0 - beta)
        torch._foreach_add_(target_list, source_list, alpha=1.0 - beta)

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.no_grad()
    @torch.no_grad()
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def cache(self, parameters: Any, is_cpu: bool = False) -> None:
    def cache(self, parameters: Any, is_cpu: bool = False) -> None:
        # 中文说明：检查运行时假设是否成立；代码：assert self.is_cached is False, "EMA cache is already taken. Did you forget to restore it?"
        assert self.is_cached is False, "EMA cache is already taken. Did you forget to restore it?"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：device = "cpu" if is_cpu else "cuda"
        device = "cpu" if is_cpu else "cuda"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.collected_params = [param.to_local().clone().to(device) for param in parameters]
        self.collected_params = [param.to_local().clone().to(device) for param in parameters]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.is_cached = True
        self.is_cached = True

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.no_grad()
    @torch.no_grad()
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def restore(self, parameters: Any) -> None:
    def restore(self, parameters: Any) -> None:
        # 中文说明：检查运行时假设是否成立；代码：assert self.is_cached, "EMA cache is not taken yet."
        assert self.is_cached, "EMA cache is not taken yet."
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for c_param, param in zip(self.collected_params, parameters, strict=False):
        for c_param, param in zip(self.collected_params, parameters, strict=False):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：param.to_local().copy_(c_param.data.type_as(param.data))
            param.to_local().copy_(c_param.data.type_as(param.data))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.collected_params = []
        self.collected_params = []
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Release the cache after we call restore
        # Release the cache after we call restore
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.is_cached = False
        self.is_cached = False


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def broadcast_dtensor_model_states(model: torch.nn.Module, mesh: DeviceMesh):
def broadcast_dtensor_model_states(model: torch.nn.Module, mesh: DeviceMesh):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Broadcast model states from replicate mesh's rank 0."""
    """Broadcast model states from replicate mesh's rank 0."""
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：replicate_group = mesh.get_group("replicate")
    replicate_group = mesh.get_group("replicate")
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：all_ranks = dist.get_process_group_ranks(replicate_group)
    all_ranks = dist.get_process_group_ranks(replicate_group)
    # 中文说明：根据条件选择执行分支；代码：if len(all_ranks) == 1:
    if len(all_ranks) == 1:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return
        return

    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _, tensor in itertools.chain(model.named_parameters(), model.named_buffers()):
    for _, tensor in itertools.chain(model.named_parameters(), model.named_buffers()):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Get src rank which is the first rank in each replication group
        # Get src rank which is the first rank in each replication group
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：src_rank = all_ranks[0]
        src_rank = all_ranks[0]
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Broadcast the local tensor
        # Broadcast the local tensor
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：local_tensor = get_local_tensor_if_DTensor(tensor)
        local_tensor = get_local_tensor_if_DTensor(tensor)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dist.broadcast(
        dist.broadcast(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：local_tensor,
            local_tensor,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：src=src_rank,
            src=src_rank,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group=replicate_group,
            group=replicate_group,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
