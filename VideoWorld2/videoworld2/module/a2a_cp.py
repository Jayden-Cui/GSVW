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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any, Callable, List, Tuple, Union
from typing import Any, Callable, List, Tuple, Union

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.distributed as dist
import torch.distributed as dist
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from einops import rearrange
from einops import rearrange
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch import Tensor
from torch import Tensor
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed import ProcessGroup
from torch.distributed import ProcessGroup
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.nn import Module
from torch.nn import Module

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.module.attention import attention
from videoworld2.module.attention import attention
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.module.neighborhood_attn import NeighborhoodAttention
from videoworld2.module.neighborhood_attn import NeighborhoodAttention


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def post_all2all(local_seq_2_local_head, seq_world_size):
def post_all2all(local_seq_2_local_head, seq_world_size):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def post_func(input):
    def post_func(input):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# b, s, n, h
        # b, s, n, h
        # 中文说明：根据条件选择执行分支；代码：if local_seq_2_local_head:
        if local_seq_2_local_head:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output = rearrange(input, "w bs seq h d -> bs (w seq) h d")
            output = rearrange(input, "w bs seq h d -> bs (w seq) h d")
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output = rearrange(input, "w bs s h d -> bs s (w h) d", w=seq_world_size)
            output = rearrange(input, "w bs s h d -> bs s (w h) d", w=seq_world_size)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return output
        return output

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return post_func
    return post_func


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def single_all_to_all(input, local_seq_2_local_head, group, async_op=False):
def single_all_to_all(input, local_seq_2_local_head, group, async_op=False):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：seq_world_size = dist.get_world_size(group)
    seq_world_size = dist.get_world_size(group)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# b, s, n, h
    # b, s, n, h
    # 中文说明：根据条件选择执行分支；代码：if local_seq_2_local_head:
    if local_seq_2_local_head:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：bs, local_seq_len, num_total_head, head_dim = input.shape
        bs, local_seq_len, num_total_head, head_dim = input.shape
        # 中文说明：检查运行时假设是否成立；代码：assert (
        assert (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_total_head % seq_world_size == 0
            num_total_head % seq_world_size == 0
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"Number of heads ({num_total_head}) must be divisible by the sequence parallel size ({seq...
        ), f"Number of heads ({num_total_head}) must be divisible by the sequence parallel size ({seq_world_size})!"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_t = rearrange(
        input_t = rearrange(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：input, "bs seq_len (w h) d -> w bs seq_len h d", w=seq_world_size, h=num_total_head // seq_wo...
            input, "bs seq_len (w h) d -> w bs seq_len h d", w=seq_world_size, h=num_total_head // seq_world_size
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：).contiguous()
        ).contiguous()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：post_all2all_fun = post_all2all(local_seq_2_local_head, seq_world_size)
        post_all2all_fun = post_all2all(local_seq_2_local_head, seq_world_size)
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：bs, global_seq_len, num_local_head, head_dim = input.shape
        bs, global_seq_len, num_local_head, head_dim = input.shape
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_t = rearrange(
        input_t = rearrange(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：input, "bs (w s) h d -> w bs s h d", w=seq_world_size, s=global_seq_len // seq_world_size
            input, "bs (w s) h d -> w bs s h d", w=seq_world_size, s=global_seq_len // seq_world_size
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：).contiguous()
        ).contiguous()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：post_all2all_fun = post_all2all(local_seq_2_local_head, seq_world_size)
        post_all2all_fun = post_all2all(local_seq_2_local_head, seq_world_size)

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output = torch.empty_like(input_t)
    output = torch.empty_like(input_t)
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dist.all_to_all_single(output, input_t, group=group, async_op=async_op)
    dist.all_to_all_single(output, input_t, group=group, async_op=async_op)

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：res = post_all2all_fun(output)
    res = post_all2all_fun(output)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return res
    return res


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def async_a2a_communicate(
def async_a2a_communicate(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：a2a_inputs: Union[torch.Tensor, List[torch.Tensor]],
    a2a_inputs: Union[torch.Tensor, List[torch.Tensor]],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cp_size: int,
    cp_size: int,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cp_group: ProcessGroup,
    cp_group: ProcessGroup,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cp_stream: torch.cuda.Stream,
    cp_stream: torch.cuda.Stream,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：local_seq_2_local_head: bool,
    local_seq_2_local_head: bool,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Union[torch.Tensor, List[torch.Tensor]]:
) -> Union[torch.Tensor, List[torch.Tensor]]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    A2A communication for context parallelism. best used in communicate qkv
    Modified from Nvidia Transformer Engine.
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：a2a_inputs = [a2a_inputs] if not isinstance(a2a_inputs, list) else a2a_inputs
    a2a_inputs = [a2a_inputs] if not isinstance(a2a_inputs, list) else a2a_inputs
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：a2a_outputs, a2a_reqs = [None] * len(a2a_inputs), [None] * len(a2a_inputs)
    a2a_outputs, a2a_reqs = [None] * len(a2a_inputs), [None] * len(a2a_inputs)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：a2a_post_fns = [None] * len(a2a_inputs)
    a2a_post_fns = [None] * len(a2a_inputs)
    # 中文说明：根据条件选择执行分支；代码：if local_seq_2_local_head:
    if local_seq_2_local_head:
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i in range(len(a2a_inputs) + 2):
        for i in range(len(a2a_inputs) + 2):
            # 中文说明：根据条件选择执行分支；代码：if 0 < i < len(a2a_inputs) + 1:
            if 0 < i < len(a2a_inputs) + 1:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：a2a_outputs[i - 1] = torch.empty_like(a2a_inputs[i - 1])
                a2a_outputs[i - 1] = torch.empty_like(a2a_inputs[i - 1])
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：a2a_reqs[i - 1] = torch.distributed.all_to_all_single(
                a2a_reqs[i - 1] = torch.distributed.all_to_all_single(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：a2a_outputs[i - 1], a2a_inputs[i - 1], group=cp_group, async_op=True
                    a2a_outputs[i - 1], a2a_inputs[i - 1], group=cp_group, async_op=True
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：a2a_post_fns[i - 1] = post_all2all(local_seq_2_local_head, cp_size)
                a2a_post_fns[i - 1] = post_all2all(local_seq_2_local_head, cp_size)
            # 中文说明：根据条件选择执行分支；代码：if i > 1:
            if i > 1:
                # 中文说明：处理异常、清理资源或管理上下文；代码：with torch.cuda.stream(cp_stream):
                with torch.cuda.stream(cp_stream):
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：a2a_reqs[i - 2].wait()
                    a2a_reqs[i - 2].wait()
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：a2a_outputs[i - 2] = a2a_post_fns[i - 2](a2a_outputs[i - 2])
                    a2a_outputs[i - 2] = a2a_post_fns[i - 2](a2a_outputs[i - 2])
            # 中文说明：根据条件选择执行分支；代码：if i < len(a2a_inputs):
            if i < len(a2a_inputs):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：a2a_inputs[i] = rearrange(
                a2a_inputs[i] = rearrange(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：a2a_inputs[i], "bs seq_len (w h) d -> w bs seq_len h d", w=cp_size
                    a2a_inputs[i], "bs seq_len (w h) d -> w bs seq_len h d", w=cp_size
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：).contiguous()
                ).contiguous()
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i in range(len(a2a_inputs) + 2):
        for i in range(len(a2a_inputs) + 2):
            # 中文说明：根据条件选择执行分支；代码：if 0 < i < len(a2a_inputs) + 1:
            if 0 < i < len(a2a_inputs) + 1:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：a2a_outputs[i - 1] = torch.empty_like(a2a_inputs[i - 1])
                a2a_outputs[i - 1] = torch.empty_like(a2a_inputs[i - 1])
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：a2a_reqs[i - 1] = torch.distributed.all_to_all_single(
                a2a_reqs[i - 1] = torch.distributed.all_to_all_single(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：a2a_outputs[i - 1], a2a_inputs[i - 1], group=cp_group, async_op=True
                    a2a_outputs[i - 1], a2a_inputs[i - 1], group=cp_group, async_op=True
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：a2a_post_fns[i - 1] = post_all2all(local_seq_2_local_head, cp_size)
                a2a_post_fns[i - 1] = post_all2all(local_seq_2_local_head, cp_size)
            # 中文说明：根据条件选择执行分支；代码：if i < len(a2a_inputs):
            if i < len(a2a_inputs):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：a2a_inputs[i] = rearrange(a2a_inputs[i], "bs (w s) h d -> w bs s h d", w=cp_size).contiguous()
                a2a_inputs[i] = rearrange(a2a_inputs[i], "bs (w s) h d -> w bs s h d", w=cp_size).contiguous()
            # 中文说明：根据条件选择执行分支；代码：if i > 1:
            if i > 1:
                # 中文说明：处理异常、清理资源或管理上下文；代码：with torch.cuda.stream(cp_stream):
                with torch.cuda.stream(cp_stream):
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：a2a_reqs[i - 2].wait()
                    a2a_reqs[i - 2].wait()
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：a2a_outputs[i - 2] = a2a_post_fns[i - 2](a2a_outputs[i - 2])
                    a2a_outputs[i - 2] = a2a_post_fns[i - 2](a2a_outputs[i - 2])
    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.current_stream().wait_stream(cp_stream)
    torch.cuda.current_stream().wait_stream(cp_stream)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return a2a_outputs[0] if len(a2a_inputs) == 1 else a2a_outputs
    return a2a_outputs[0] if len(a2a_inputs) == 1 else a2a_outputs


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class _SeqAllToAll(torch.autograd.Function):
class _SeqAllToAll(torch.autograd.Function):
    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(ctx: Any, group: dist.ProcessGroup, input: Tensor, local_seq_2_local_head: bool) ...
    def forward(ctx: Any, group: dist.ProcessGroup, input: Tensor, local_seq_2_local_head: bool) -> Tensor:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctx.group = group
        ctx.group = group
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：res = single_all_to_all(input, local_seq_2_local_head, group, False)
        res = single_all_to_all(input, local_seq_2_local_head, group, False)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctx.local_seq_2_local_head = local_seq_2_local_head
        ctx.local_seq_2_local_head = local_seq_2_local_head
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return res
        return res

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def backward(ctx: Any, *grad_output: Tensor) -> Tuple[None, Tensor, None]:
    def backward(ctx: Any, *grad_output: Tensor) -> Tuple[None, Tensor, None]:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return (None, _SeqAllToAll.apply(ctx.group, *grad_output, not ctx.local_seq_2_local_head), None)
        return (None, _SeqAllToAll.apply(ctx.group, *grad_output, not ctx.local_seq_2_local_head), None)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class _SeqAllToAllQKV(torch.autograd.Function):
class _SeqAllToAllQKV(torch.autograd.Function):
    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(
    def forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx: Any,
        ctx: Any,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group: dist.ProcessGroup,
        group: dist.ProcessGroup,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q: Tensor,
        q: Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k: Tensor,
        k: Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v: Tensor,
        v: Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cp_size: int,
        cp_size: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cp_stream: torch.cuda.Stream,
        cp_stream: torch.cuda.Stream,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：local_seq_2_local_head: bool,
        local_seq_2_local_head: bool,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[Tensor, Tensor, Tensor]:
    ) -> Tuple[Tensor, Tensor, Tensor]:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctx.group = group
        ctx.group = group
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctx.cp_size = cp_size
        ctx.cp_size = cp_size
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctx.cp_stream = cp_stream
        ctx.cp_stream = cp_stream
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctx.local_seq_2_local_head = local_seq_2_local_head
        ctx.local_seq_2_local_head = local_seq_2_local_head
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q, k, v = async_a2a_communicate([q, k, v], cp_size, group, cp_stream, local_seq_2_local_head)
        q, k, v = async_a2a_communicate([q, k, v], cp_size, group, cp_stream, local_seq_2_local_head)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return q, k, v
        return q, k, v

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def backward(ctx: Any, *grad_output: Tensor) -> Tuple[None, Tensor, Tensor, Tensor, None, Non...
    def backward(ctx: Any, *grad_output: Tensor) -> Tuple[None, Tensor, Tensor, Tensor, None, None, None]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：q_grad, k_grad, v_grad = _SeqAllToAllQKV.apply(
        q_grad, k_grad, v_grad = _SeqAllToAllQKV.apply(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctx.group, *grad_output, ctx.cp_size, ctx.cp_stream, not ctx.local_seq_2_local_head
            ctx.group, *grad_output, ctx.cp_size, ctx.cp_stream, not ctx.local_seq_2_local_head
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return (None, q_grad, k_grad, v_grad, None, None, None)
        return (None, q_grad, k_grad, v_grad, None, None, None)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class DistributedAttention(torch.nn.Module):
class DistributedAttention(torch.nn.Module):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Initialization.
    """Initialization.

    Arguments:
        local_attention (Module): local attention with q,k,v
        sequence_process_group (ProcessGroup): sequence parallel process group
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：local_attention: Union[Module, Callable],
        local_attention: Union[Module, Callable],
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super(DistributedAttention, self).__init__()
        super(DistributedAttention, self).__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.local_attn = local_attention
        self.local_attn = local_attention
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.pg = None
        self.pg = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.stream = None
        self.stream = None

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, query: Tensor, key: Tensor, value: Tensor, *args: Any, **kwargs) -> Tensor:
    def forward(self, query: Tensor, key: Tensor, value: Tensor, *args: Any, **kwargs) -> Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""forward
        """forward

        Arguments:
            query (Tensor): query input to the layer
            key (Tensor): key input to the layer
            value (Tensor): value input to the layer
            args: other args

        Returns:
            * output (Tensor): context output
        """
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs['causal'] = (self.attn_mask_type == "causal")
        kwargs['causal'] = (self.attn_mask_type == "causal")
        # 中文说明：根据条件选择执行分支；代码：if self.pg is None:
        if self.pg is None:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.local_attn(query, key, value, *args, **kwargs)
            return self.local_attn(query, key, value, *args, **kwargs)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pg_size = dist.get_world_size(self.pg)
        pg_size = dist.get_world_size(self.pg)
        # 中文说明：根据条件选择执行分支；代码：if pg_size < 2:
        if pg_size < 2:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.local_attn(query, key, value, *args, **kwargs)
            return self.local_attn(query, key, value, *args, **kwargs)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：query_layer, key_layer, value_layer = _SeqAllToAllQKV.apply(
        query_layer, key_layer, value_layer = _SeqAllToAllQKV.apply(
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.pg, query, key, value, pg_size, self.stream, True
            self.pg, query, key, value, pg_size, self.stream, True
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：context_layer = self.local_attn(query_layer, key_layer, value_layer, *args, **kwargs)
        context_layer = self.local_attn(query_layer, key_layer, value_layer, *args, **kwargs)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output = _SeqAllToAll.apply(self.pg, context_layer, False)
        output = _SeqAllToAll.apply(self.pg, context_layer, False)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return output
        return output

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def set_context_parallel_group(self, group, stream):
    def set_context_parallel_group(self, group, stream):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.pg = group
        self.pg = group
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.stream = stream
        self.stream = stream


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class MinimalA2AAttnOp(DistributedAttention):
class MinimalA2AAttnOp(DistributedAttention):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, *args, **kwargs):
    def __init__(self, *args, **kwargs):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.attn_mask_type = kwargs.get("attn_mask_type", "no_mask")
        self.attn_mask_type = kwargs.get("attn_mask_type", "no_mask")
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del args, kwargs
        del args, kwargs
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super(MinimalA2AAttnOp, self).__init__(attention)
        super(MinimalA2AAttnOp, self).__init__(attention)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def set_context_parallel_group(self, process_group, ranks, stream):
    def set_context_parallel_group(self, process_group, ranks, stream):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del ranks
        del ranks
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().set_context_parallel_group(process_group, stream)
        super().set_context_parallel_group(process_group, stream)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, query: Tensor, key: Tensor, value: Tensor, *args: Any, **kwargs) -> Tensor:
    def forward(self, query: Tensor, key: Tensor, value: Tensor, *args: Any, **kwargs) -> Tensor:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：results = super().forward(query, key, value, *args, **kwargs)
        results = super().forward(query, key, value, *args, **kwargs)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return rearrange(results, "b ... h l -> b ... (h l)")
        return rearrange(results, "b ... h l -> b ... (h l)")


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class NattenA2AAttnOp(MinimalA2AAttnOp):
class NattenA2AAttnOp(MinimalA2AAttnOp):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, *args, **kwargs):
    def __init__(self, *args, **kwargs):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super(NattenA2AAttnOp, self).__init__(None)
        super(NattenA2AAttnOp, self).__init__(None)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.natten_op = NeighborhoodAttention(*args, **kwargs, base_attn_op=attention)
        self.natten_op = NeighborhoodAttention(*args, **kwargs, base_attn_op=attention)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.local_attn = self.natten_op
        self.local_attn = self.natten_op
