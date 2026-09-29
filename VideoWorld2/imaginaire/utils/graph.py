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
# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""A rework of make_graphed_callabled function from TransformerEngine so that it works with i...
"""A rework of make_graphed_callabled function from TransformerEngine so that it works with inference-only."""
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any, Callable, Dict, Optional, Tuple, TypeVar, Union
from typing import Any, Callable, Dict, Optional, Tuple, TypeVar, Union

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch._C import _graph_pool_handle
from torch._C import _graph_pool_handle
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.utils._pytree import tree_flatten as _tree_flatten
from torch.utils._pytree import tree_flatten as _tree_flatten
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.utils._pytree import tree_unflatten as _tree_unflatten
from torch.utils._pytree import tree_unflatten as _tree_unflatten
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from transformer_engine.pytorch.distributed import get_all_rng_states, graph_safe_rng_available
from transformer_engine.pytorch.distributed import get_all_rng_states, graph_safe_rng_available
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from transformer_engine.pytorch.module.base import TransformerEngineBaseModule
from transformer_engine.pytorch.module.base import TransformerEngineBaseModule

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：__all__ = ["create_cuda_graph"]
__all__ = ["create_cuda_graph"]


# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_IS_GRAPH_CAPTURING = False
_IS_GRAPH_CAPTURING = False

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_T = TypeVar("_T")
_T = TypeVar("_T")
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：SingleOrTuple = Union[_T, Tuple[_T, ...]]
SingleOrTuple = Union[_T, Tuple[_T, ...]]


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def set_capture_start() -> None:
def set_capture_start() -> None:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Record beginning of `make_graphed_callables`."""
    """Record beginning of `make_graphed_callables`."""
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：global _IS_GRAPH_CAPTURING
    global _IS_GRAPH_CAPTURING
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_IS_GRAPH_CAPTURING = True
    _IS_GRAPH_CAPTURING = True


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def set_capture_end() -> None:
def set_capture_end() -> None:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Record end of `make_graphed_callables`."""
    """Record end of `make_graphed_callables`."""
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：global _IS_GRAPH_CAPTURING
    global _IS_GRAPH_CAPTURING
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_IS_GRAPH_CAPTURING = False
    _IS_GRAPH_CAPTURING = False


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_graph_capturing() -> None:
def is_graph_capturing() -> None:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Return whether within `make_graphed_callables`."""
    """Return whether within `make_graphed_callables`."""
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return _IS_GRAPH_CAPTURING
    return _IS_GRAPH_CAPTURING


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def graph_pool_handle():
def graph_pool_handle():
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Returns an opaque token representing the id of a graph memory pool.
    """
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return _graph_pool_handle()
    return _graph_pool_handle()


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _make_graphed_callables(
def _make_graphed_callables(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：callables: SingleOrTuple[Callable],
    callables: SingleOrTuple[Callable],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sample_args: SingleOrTuple[Tuple[torch.Tensor, ...]],
    sample_args: SingleOrTuple[Tuple[torch.Tensor, ...]],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_warmup_iters: int = 3,
    num_warmup_iters: int = 3,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sample_kwargs: Optional[SingleOrTuple[Dict[str, Any]]] = None,
    sample_kwargs: Optional[SingleOrTuple[Dict[str, Any]]] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pool: Optional[Tuple[int, ...]] = None,
    pool: Optional[Tuple[int, ...]] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> SingleOrTuple[Callable]:
) -> SingleOrTuple[Callable]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Helper method for `make_graphed_callables`
    """

    # 中文说明：根据条件选择执行分支；代码：if torch.is_autocast_enabled() and torch.is_autocast_cache_enabled():
    if torch.is_autocast_enabled() and torch.is_autocast_cache_enabled():
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise RuntimeError(
        raise RuntimeError(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："make_graphed_callables does not support the autocast " "caching. Please set `cache_enabled=F...
            "make_graphed_callables does not support the autocast " "caching. Please set `cache_enabled=False`."
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Default is to pass no kwargs to callables
    # Default is to pass no kwargs to callables
    # 中文说明：根据条件选择执行分支；代码：if sample_kwargs is None:
    if sample_kwargs is None:
        # 中文说明：根据条件选择执行分支；代码：if isinstance(callables, tuple):
        if isinstance(callables, tuple):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sample_kwargs = tuple({} for _ in range(len(sample_args)))
            sample_kwargs = tuple({} for _ in range(len(sample_args)))
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sample_kwargs = {}
            sample_kwargs = {}

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Canonicalize args as tuples
    # Canonicalize args as tuples
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：just_one_callable = False
    just_one_callable = False
    # 中文说明：根据条件选择执行分支；代码：if not isinstance(callables, tuple):
    if not isinstance(callables, tuple):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：just_one_callable = True
        just_one_callable = True
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：callables = (callables,)
        callables = (callables,)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sample_args = (sample_args,)
        sample_args = (sample_args,)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sample_kwargs = (sample_kwargs,)
        sample_kwargs = (sample_kwargs,)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Check sizes of args
    # Check sizes of args
    # 中文说明：检查运行时假设是否成立；代码：assert len(sample_args) == len(callables)
    assert len(sample_args) == len(callables)
    # 中文说明：检查运行时假设是否成立；代码：assert len(sample_kwargs) == len(callables)
    assert len(sample_kwargs) == len(callables)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Check callables
    # Check callables
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for c in callables:
    for c in callables:
        # 中文说明：根据条件选择执行分支；代码：if isinstance(c, torch.nn.Module):
        if isinstance(c, torch.nn.Module):
            # 中文说明：检查运行时假设是否成立；代码：assert len(c._backward_hooks) == 0 and len(c._forward_hooks) == 0 and len(c._forward_pre_hook...
            assert len(c._backward_hooks) == 0 and len(c._forward_hooks) == 0 and len(c._forward_pre_hooks) == 0, (
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："Modules must not have hooks registered at the time they are passed. "
                "Modules must not have hooks registered at the time they are passed. "
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：+ "However, registering hooks on modules after passing them "
                + "However, registering hooks on modules after passing them "
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：+ "through make_graphed_callables is allowed."
                + "through make_graphed_callables is allowed."
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：检查运行时假设是否成立；代码：assert all(b.requires_grad is False for b in c.buffers()), (
            assert all(b.requires_grad is False for b in c.buffers()), (
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："In any :class:`~torch.nn.Module` passed to "
                "In any :class:`~torch.nn.Module` passed to "
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：+ ":func:`~make_graphed_callables`, only parameters may be trainable. "
                + ":func:`~make_graphed_callables`, only parameters may be trainable. "
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：+ "All buffers must have ``requires_grad=False``."
                + "All buffers must have ``requires_grad=False``."
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Flatten callable arguments
    # Flatten callable arguments
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：per_callable_kwargs_keys = [list(kwargs.keys()) for kwargs in sample_kwargs]
    per_callable_kwargs_keys = [list(kwargs.keys()) for kwargs in sample_kwargs]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：flatten_sample_args = []
    flatten_sample_args = []
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for args, kwargs, kwargs_keys in zip(sample_args, sample_kwargs, per_callable_kwargs_keys):
    for args, kwargs, kwargs_keys in zip(sample_args, sample_kwargs, per_callable_kwargs_keys):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：flatten_arg, _ = _tree_flatten(args)
        flatten_arg, _ = _tree_flatten(args)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：flatten_kwarg, _ = _tree_flatten([kwargs[key] for key in kwargs_keys])
        flatten_kwarg, _ = _tree_flatten([kwargs[key] for key in kwargs_keys])
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：flatten_sample_args.append(tuple(flatten_arg + flatten_kwarg))
        flatten_sample_args.append(tuple(flatten_arg + flatten_kwarg))
        # 中文说明：检查运行时假设是否成立；代码：assert all(isinstance(arg, torch.Tensor) for arg in flatten_arg), (
        assert all(isinstance(arg, torch.Tensor) for arg in flatten_arg), (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："In the beta API, sample_args "
            "In the beta API, sample_args "
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：+ "for each callable must contain only Tensors. Other types are not allowed."
            + "for each callable must contain only Tensors. Other types are not allowed."
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# If a callable is an nn.Module, its graph's full input surface is the args the user explicitly
    # If a callable is an nn.Module, its graph's full input surface is the args the user explicitly
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# passes to forward (ie, its sample_args) AND the module's parameter attributes.
    # passes to forward (ie, its sample_args) AND the module's parameter attributes.
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：per_callable_len_user_args = [len(args) for args in flatten_sample_args]
    per_callable_len_user_args = [len(args) for args in flatten_sample_args]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：per_callable_module_params = [tuple(c.parameters()) if isinstance(c, torch.nn.Module) else ()...
    per_callable_module_params = [tuple(c.parameters()) if isinstance(c, torch.nn.Module) else () for c in callables]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：per_callable_static_input_surfaces = [
    per_callable_static_input_surfaces = [
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：flatten_sample_args[i] + per_callable_module_params[i] for i in range(len(callables))
        flatten_sample_args[i] + per_callable_module_params[i] for i in range(len(callables))
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
    ]

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fwd_graphs = [torch.cuda.CUDAGraph() for _ in range(len(flatten_sample_args))]
    fwd_graphs = [torch.cuda.CUDAGraph() for _ in range(len(flatten_sample_args))]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：graph_callables = [None for _ in range(len(flatten_sample_args))]
    graph_callables = [None for _ in range(len(flatten_sample_args))]

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# For cases with multiple active RNG states, e.g. TP.
    # For cases with multiple active RNG states, e.g. TP.
    # 中文说明：根据条件选择执行分支；代码：if graph_safe_rng_available():
    if graph_safe_rng_available():
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _, state in get_all_rng_states().items():
        for _, state in get_all_rng_states().items():
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for fwd_graph in fwd_graphs:
            for fwd_graph in fwd_graphs:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：fwd_graph.register_generator_state(state)
                fwd_graph.register_generator_state(state)

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mempool = graph_pool_handle() if pool is None else pool
    mempool = graph_pool_handle() if pool is None else pool

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Warmup
    # Warmup
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Hopefully prevents cudnn benchmarking and other lazy-initialization cuda work
    # Hopefully prevents cudnn benchmarking and other lazy-initialization cuda work
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# from ending up in any captures.
    # from ending up in any captures.
    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.synchronize()
    torch.cuda.synchronize()

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Get warmup func and func_idx.
    # Get warmup func and func_idx.
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：warmup_func_idx = []
    warmup_func_idx = []
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：warmup_func = []
    warmup_func = []
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for func_idx, func in enumerate(callables):
    for func_idx, func in enumerate(callables):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：warmup_func_idx.append(func_idx)
        warmup_func_idx.append(func_idx)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：warmup_func.append(func)
        warmup_func.append(func)
    # 中文说明：检查运行时假设是否成立；代码：assert len(warmup_func) == len(sample_args), f"Warmup runs {len(warmup_func)} don't match arg...
    assert len(warmup_func) == len(sample_args), f"Warmup runs {len(warmup_func)} don't match args {len(sample_args)}."
    # 中文说明：检查运行时假设是否成立；代码：assert len(warmup_func_idx) == len(
    assert len(warmup_func_idx) == len(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：set(warmup_func_idx)
        set(warmup_func_idx)
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"Warmup runs {len(warmup_func)} but only {len(set(warmup_func_idx))} are unique."
    ), f"Warmup runs {len(warmup_func)} but only {len(set(warmup_func_idx))} are unique."

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Filter the TE modules that cudagraph can access.
    # Filter the TE modules that cudagraph can access.
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：visited_te_modules = set()
    visited_te_modules = set()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def hook_fn(module, inputs, outputs): # pylint: disable=unused-argument
    def hook_fn(module, inputs, outputs):  # pylint: disable=unused-argument
        # 中文说明：根据条件选择执行分支；代码：if isinstance(module, TransformerEngineBaseModule):
        if isinstance(module, TransformerEngineBaseModule):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：visited_te_modules.add(module)
            visited_te_modules.add(module)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Run warmup and do the above filtering.
    # Run warmup and do the above filtering.
    # 中文说明：处理异常、清理资源或管理上下文；代码：with torch.cuda.stream(torch.cuda.Stream()):
    with torch.cuda.stream(torch.cuda.Stream()):
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for func_idx, func in zip(warmup_func_idx, warmup_func):
        for func_idx, func in zip(warmup_func_idx, warmup_func):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：args = sample_args[func_idx]
            args = sample_args[func_idx]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs = sample_kwargs[func_idx]
            kwargs = sample_kwargs[func_idx]
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _ in range(num_warmup_iters):
            for _ in range(num_warmup_iters):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hooks = []
                hooks = []
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for module in func.modules():
                for module in func.modules():
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hook = module.register_forward_hook(hook_fn)
                    hook = module.register_forward_hook(hook_fn)
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：hooks.append(hook)
                    hooks.append(hook)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：outputs, _ = _tree_flatten(func(*args, **kwargs))
                outputs, _ = _tree_flatten(func(*args, **kwargs))
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for hook in hooks:
                for hook in hooks:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：hook.remove()
                    hook.remove()
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del outputs
                del outputs
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# The following code is added specifically for MCore's special requirements,
            # The following code is added specifically for MCore's special requirements,
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# aimed at preventing warmup from altering the control flow.
            # aimed at preventing warmup from altering the control flow.
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for module in func.modules():
            for module in func.modules():
                # 中文说明：根据条件选择执行分支；代码：if hasattr(module, "is_first_microbatch"):
                if hasattr(module, "is_first_microbatch"):
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：module.is_first_microbatch = True
                    module.is_first_microbatch = True
    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.synchronize()
    torch.cuda.synchronize()

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# All captures here share a mempool. To avoid replays corrupting each other's memory,
    # All captures here share a mempool. To avoid replays corrupting each other's memory,
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# the safest approach is to capture all passes in the same order they'll run:
    # the safest approach is to capture all passes in the same order they'll run:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Capture forward graphs
    # Capture forward graphs
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：per_callable_static_outputs = []
    per_callable_static_outputs = []
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：per_callable_output_unflatten_spec = []
    per_callable_output_unflatten_spec = []
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：graph_id = 0
    graph_id = 0
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for func, args, kwargs, fwd_graph in zip(callables, sample_args, sample_kwargs, fwd_graphs):
    for func, args, kwargs, fwd_graph in zip(callables, sample_args, sample_kwargs, fwd_graphs):
        # 中文说明：处理异常、清理资源或管理上下文；代码：with torch.cuda.graph(fwd_graph, pool=mempool):
        with torch.cuda.graph(fwd_graph, pool=mempool):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：outputs = func(*args, **kwargs)
            outputs = func(*args, **kwargs)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：graph_callables[graph_id] = func
        graph_callables[graph_id] = func
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：graph_id += 1
        graph_id += 1

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：flatten_outputs, spec = _tree_flatten(outputs)
        flatten_outputs, spec = _tree_flatten(outputs)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：per_callable_static_outputs.append(tuple(flatten_outputs))
        per_callable_static_outputs.append(tuple(flatten_outputs))
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：per_callable_output_unflatten_spec.append(spec)
        per_callable_output_unflatten_spec.append(spec)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def make_graphed_autograd_function(
    def make_graphed_autograd_function(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：fwd_graph,
        fwd_graph,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：module_params,
        module_params,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：kwargs_keys,
        kwargs_keys,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：len_user_args,
        len_user_args,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：output_unflatten_spec,
        output_unflatten_spec,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：static_input_surface,
        static_input_surface,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：static_outputs,
        static_outputs,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Graphed(torch.autograd.Function):
        class Graphed(torch.autograd.Function):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Autograd function for graph replay."""
            """Autograd function for graph replay."""

            # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
            @staticmethod
            # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(ctx, *inputs):
            def forward(ctx, *inputs):
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# pylint: disable=missing-function-docstring
                # pylint: disable=missing-function-docstring

                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Copy values from new tensors into static tensors
                # Copy values from new tensors into static tensors
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i in range(len_user_args):
                for i in range(len_user_args):
                    # 中文说明：根据条件选择执行分支；代码：if static_input_surface[i].data_ptr() != inputs[i].data_ptr():
                    if static_input_surface[i].data_ptr() != inputs[i].data_ptr():
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：static_input_surface[i].copy_(inputs[i])
                        static_input_surface[i].copy_(inputs[i])

                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Replay forward graph
                # Replay forward graph
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：fwd_graph.replay()
                fwd_graph.replay()
                # 中文说明：检查运行时假设是否成立；代码：assert isinstance(static_outputs, tuple)
                assert isinstance(static_outputs, tuple)
                # 中文说明：从当前函数返回结果或结束函数执行；代码：return tuple(o.detach() for o in static_outputs)
                return tuple(o.detach() for o in static_outputs)

        # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def functionalized(*user_args, **user_kwargs):
        def functionalized(*user_args, **user_kwargs):
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Check that required kwargs are provided
            # Check that required kwargs are provided
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key in kwargs_keys:
            for key in kwargs_keys:
                # 中文说明：根据条件选择执行分支；代码：if key not in user_kwargs:
                if key not in user_kwargs:
                    # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError(
                    raise TypeError(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Graphed callable was initialized with kwarg {key} ," "but it was not provided in graph replay"
                        f"Graphed callable was initialized with kwarg {key} ," "but it was not provided in graph replay"
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Runs the autograd function with inputs == all inputs to
            # Runs the autograd function with inputs == all inputs to
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# the graph that might require grad (explicit user args +
            # the graph that might require grad (explicit user args +
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# module parameters)
            # module parameters)
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Assumes module params didn't change since capture.
            # Assumes module params didn't change since capture.
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：flatten_user_args, _ = _tree_flatten(user_args)
            flatten_user_args, _ = _tree_flatten(user_args)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：flatten_user_kwargs, _ = _tree_flatten([user_kwargs[key] for key in kwargs_keys])
            flatten_user_kwargs, _ = _tree_flatten([user_kwargs[key] for key in kwargs_keys])
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：func_args = tuple(flatten_user_args) + tuple(flatten_user_kwargs) + module_params
            func_args = tuple(flatten_user_args) + tuple(flatten_user_kwargs) + module_params
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out = Graphed.apply(*func_args)
            out = Graphed.apply(*func_args)
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return _tree_unflatten(out, output_unflatten_spec)
            return _tree_unflatten(out, output_unflatten_spec)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return functionalized
        return functionalized

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Put together the final graphed callables
    # Put together the final graphed callables
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ret = []
    ret = []
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i in range(len(sample_args)):
    for i in range(len(sample_args)):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：graphed = make_graphed_autograd_function(
        graphed = make_graphed_autograd_function(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：fwd_graphs[i],
            fwd_graphs[i],
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：per_callable_module_params[i],
            per_callable_module_params[i],
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：per_callable_kwargs_keys[i],
            per_callable_kwargs_keys[i],
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：per_callable_len_user_args[i],
            per_callable_len_user_args[i],
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：per_callable_output_unflatten_spec[i],
            per_callable_output_unflatten_spec[i],
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：per_callable_static_input_surfaces[i],
            per_callable_static_input_surfaces[i],
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：per_callable_static_outputs[i],
            per_callable_static_outputs[i],
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：func = graph_callables[i]
        func = graph_callables[i]
        # 中文说明：根据条件选择执行分支；代码：if isinstance(func, torch.nn.Module):
        if isinstance(func, torch.nn.Module):

            # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def make_graphed_forward(func, graph_training_state, graphed, orig_fwd):
            def make_graphed_forward(func, graph_training_state, graphed, orig_fwd):
                # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def new_fwd(*user_args, **user_kwargs):
                def new_fwd(*user_args, **user_kwargs):
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# If the module's training-or-eval state matches what we graphed,
                    # If the module's training-or-eval state matches what we graphed,
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# run the graph, otherwise run the original forward method
                    # run the graph, otherwise run the original forward method
                    # 中文说明：根据条件选择执行分支；代码：if func.training == graph_training_state:
                    if func.training == graph_training_state:
                        # 中文说明：从当前函数返回结果或结束函数执行；代码：return graphed(*user_args, **user_kwargs)
                        return graphed(*user_args, **user_kwargs)
                    # 中文说明：从当前函数返回结果或结束函数执行；代码：return orig_fwd(*user_args, **user_kwargs)
                    return orig_fwd(*user_args, **user_kwargs)

                # 中文说明：从当前函数返回结果或结束函数执行；代码：return new_fwd
                return new_fwd

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：forward = make_graphed_forward(func, func.training, graphed, func.forward)
            forward = make_graphed_forward(func, func.training, graphed, func.forward)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ret.append(forward)
            ret.append(forward)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ret.append(graphed)
            ret.append(graphed)

    # 中文说明：根据条件选择执行分支；代码：if just_one_callable:
    if just_one_callable:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return ret[0]
        return ret[0]

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return tuple(ret)
    return tuple(ret)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def make_graphed_callables_forward(
def make_graphed_callables_forward(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：modules: SingleOrTuple[Callable],
    modules: SingleOrTuple[Callable],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sample_args: SingleOrTuple[Tuple[torch.Tensor, ...]],
    sample_args: SingleOrTuple[Tuple[torch.Tensor, ...]],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_warmup_iters: int = 3,
    num_warmup_iters: int = 3,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sample_kwargs: Optional[SingleOrTuple[Dict[str, Any]]] = None,
    sample_kwargs: Optional[SingleOrTuple[Dict[str, Any]]] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pool: Optional[Tuple[int, ...]] = None,
    pool: Optional[Tuple[int, ...]] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Union[Callable, Tuple[Callable, ...]]:
) -> Union[Callable, Tuple[Callable, ...]]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Make CUDA graph version of Transformer Engine modules
    A variation of PyTorch's `make_graphed_callables` utility function.
    `original PyTorch implementation <https://pytorch.org/docs/stable/generated/torch.cuda.make_graphed_callables.html>`_
    for more documentation.
    Graphing parameters
    -------------------
    modules: (tuple of) callable
             Callable or callables to graph.
    sample_args: (tuple of) tuple of torch.Tensor
                 Positional arguments to callable(s).
    num_warmup_iters: int, default = 3
                      Number of warmup iterations.
    sample_kwargs: (tuple of) dict, optional
                   Keyword arguments to callable(s)
    pool: (tuple of) int, default = `None`, optional
          An instance returned from function `torch.cuda.graph_pool_handle` that hints
          this graph may share memory with the indicated pool.
    """
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：set_capture_start()
    set_capture_start()

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Handle single module.
    # Handle single module.
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：just_one_callable = False
    just_one_callable = False
    # 中文说明：根据条件选择执行分支；代码：if not isinstance(modules, tuple):
    if not isinstance(modules, tuple):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：just_one_callable = True
        just_one_callable = True
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：modules = (modules,)
        modules = (modules,)

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：forward_funcs = []
    forward_funcs = []
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for module in modules:
    for module in modules:
        # 中文说明：检查运行时假设是否成立；代码：assert isinstance(module, torch.nn.Module), f"Graphing for {type(module)} is not supported."
        assert isinstance(module, torch.nn.Module), f"Graphing for {type(module)} is not supported."
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：forward_funcs.append(module)
        forward_funcs.append(module)

    # 中文说明：根据条件选择执行分支；代码：if just_one_callable:
    if just_one_callable:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：forward_funcs = forward_funcs[0]
        forward_funcs = forward_funcs[0]
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：forward_funcs = tuple(forward_funcs)
        forward_funcs = tuple(forward_funcs)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Save RNG state.
    # Save RNG state.
    # 中文说明：根据条件选择执行分支；代码：if graph_safe_rng_available():
    if graph_safe_rng_available():
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：generators = [
        generators = [
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.default_generators[torch.cuda.current_device()],
            torch.cuda.default_generators[torch.cuda.current_device()],
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：*get_all_rng_states().values(),
            *get_all_rng_states().values(),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
        ]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：original_rng_states = [state.get_state() for state in generators]
        original_rng_states = [state.get_state() for state in generators]
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：original_rng_states = torch.cuda.get_rng_state()
        original_rng_states = torch.cuda.get_rng_state()

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：graphed_callables = _make_graphed_callables(
    graphed_callables = _make_graphed_callables(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：forward_funcs,
        forward_funcs,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sample_args,
        sample_args,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_warmup_iters=num_warmup_iters,
        num_warmup_iters=num_warmup_iters,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sample_kwargs=sample_kwargs,
        sample_kwargs=sample_kwargs,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pool=pool,
        pool=pool,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Ensures warmup does not affect numerics for ops such as dropout.
    # Ensures warmup does not affect numerics for ops such as dropout.
    # 中文说明：根据条件选择执行分支；代码：if graph_safe_rng_available():
    if graph_safe_rng_available():
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for gen, state in zip(generators, original_rng_states):
        for gen, state in zip(generators, original_rng_states):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：gen.set_state(state)
            gen.set_state(state)
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.set_rng_state(original_rng_states)
        torch.cuda.set_rng_state(original_rng_states)
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：set_capture_end()
    set_capture_end()
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return graphed_callables
    return graphed_callables


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def create_cuda_graph(
def create_cuda_graph(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cuda_graphs_storage: dict,
    cuda_graphs_storage: dict,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：blocks: torch.nn.ModuleList,
    blocks: torch.nn.ModuleList,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x: torch.Tensor,
    x: torch.Tensor,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：affline_emb_B_D: torch.Tensor,
    affline_emb_B_D: torch.Tensor,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：crossattn_emb: torch.Tensor,
    crossattn_emb: torch.Tensor,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rope_emb_L_1_1_D: torch.Tensor,
    rope_emb_L_1_1_D: torch.Tensor,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：adaln_lora_B_3D: torch.Tensor,
    adaln_lora_B_3D: torch.Tensor,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：extra_per_block_pos_emb: torch.Tensor,
    extra_per_block_pos_emb: torch.Tensor,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> str:
) -> str:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：real_args = [arg for arg in [x, affline_emb_B_D, crossattn_emb] if arg is not None]
    real_args = [arg for arg in [x, affline_emb_B_D, crossattn_emb] if arg is not None]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：real_kwargs = {
    real_kwargs = {
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k: v
        k: v
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for k, v in {
        for k, v in {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："rope_emb_L_1_1_D": rope_emb_L_1_1_D,
            "rope_emb_L_1_1_D": rope_emb_L_1_1_D,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："adaln_lora_B_T_3D": adaln_lora_B_3D,
            "adaln_lora_B_T_3D": adaln_lora_B_3D,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："extra_per_block_pos_emb": extra_per_block_pos_emb,
            "extra_per_block_pos_emb": extra_per_block_pos_emb,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}.items()
        }.items()
        # 中文说明：根据条件选择执行分支；代码：if v is not None
        if v is not None
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
    }
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：shapes_key = "_".join(
    shapes_key = "_".join(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：[
        [
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：str(shape_component)
            str(shape_component)
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for shape in [x.shape for x in real_args + list(real_kwargs.values())]
            for shape in [x.shape for x in real_args + list(real_kwargs.values())]
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for shape_component in shape
            for shape_component in shape
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
        ]
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：根据条件选择执行分支；代码：if shapes_key not in cuda_graphs_storage:
    if shapes_key not in cuda_graphs_storage:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：callables = []
        callables = []
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sample_args = []
        sample_args = []
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sample_kwargs = []
        sample_kwargs = []
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for block in blocks:
        for block in blocks:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：callables.append(block)
            callables.append(block)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：args = []
            args = []
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs = {}
            kwargs = {}
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for arg in real_args:
            for arg in real_args:
                # 中文说明：根据条件选择执行分支；代码：if arg.dtype == torch.int64:
                if arg.dtype == torch.int64:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dummy_arg = torch.randint(arg.min(), arg.max() + 1, arg.shape).type_as(arg)
                    dummy_arg = torch.randint(arg.min(), arg.max() + 1, arg.shape).type_as(arg)
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dummy_arg = torch.randn(arg.shape).type_as(arg)
                    dummy_arg = torch.randn(arg.shape).type_as(arg)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dummy_arg.requires_grad = arg.requires_grad
                dummy_arg.requires_grad = arg.requires_grad
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：args.append(dummy_arg)
                args.append(dummy_arg)
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for name, kwarg in real_kwargs.items():
            for name, kwarg in real_kwargs.items():
                # 中文说明：根据条件选择执行分支；代码：if kwarg.dtype == torch.int64:
                if kwarg.dtype == torch.int64:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dummy_kwarg = torch.randint(kwarg.min(), kwarg.max() + 1, kwarg.shape).type_as(kwarg)
                    dummy_kwarg = torch.randint(kwarg.min(), kwarg.max() + 1, kwarg.shape).type_as(kwarg)
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dummy_kwarg = torch.randn(kwarg.shape).type_as(kwarg)
                    dummy_kwarg = torch.randn(kwarg.shape).type_as(kwarg)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dummy_kwarg.requires_grad = kwarg.requires_grad
                dummy_kwarg.requires_grad = kwarg.requires_grad
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs[name] = dummy_kwarg
                kwargs[name] = dummy_kwarg
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sample_args.append(args)
            sample_args.append(args)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sample_kwargs.append(kwargs)
            sample_kwargs.append(kwargs)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.critical(f"Creating graph for shape {shapes_key}")
        log.critical(f"Creating graph for shape {shapes_key}")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cuda_graphs_storage[shapes_key] = make_graphed_callables_forward(
        cuda_graphs_storage[shapes_key] = make_graphed_callables_forward(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：tuple(callables),
            tuple(callables),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：tuple(sample_args),
            tuple(sample_args),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sample_kwargs=tuple(sample_kwargs),
            sample_kwargs=tuple(sample_kwargs),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_warmup_iters=11,
            num_warmup_iters=11,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.critical(f"Created graph for shape {shapes_key}")
        log.critical(f"Created graph for shape {shapes_key}")
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return shapes_key
    return shapes_key
