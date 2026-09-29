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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import threading
import threading
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import traceback
import traceback
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Callable, Dict, Iterator, List, Optional
from typing import Callable, Dict, Iterator, List, Optional

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.utils.data import DataLoader
from torch.utils.data import DataLoader

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.datasets.watchdog import OperationWatchdog
from videoworld2.datasets.watchdog import OperationWatchdog


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def concatenate_batches(n: int, data_batches: List[Dict]) -> List[Dict]:
def concatenate_batches(n: int, data_batches: List[Dict]) -> List[Dict]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Smartly concatenate n input data batches into m output data batches.
    Each data batch is a dictionary with values that can be torch tensor, string, or list.

    Args:
        n (int): Number of input batches to process per output batch
        data_batches (list): List of dictionary data batches

    Returns:
        list: List of concatenated data batches
    """
    # 中文说明：根据条件选择执行分支；代码：if n <= 0:
    if n <= 0:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError("n must be a positive integer")
        raise ValueError("n must be a positive integer")

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Calculate m based on the input
    # Calculate m based on the input
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：total_batches = len(data_batches)
    total_batches = len(data_batches)
    # 中文说明：根据条件选择执行分支；代码：if total_batches % n != 0:
    if total_batches % n != 0:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Length of data_batches ({total_batches}) must be divisible by n ({n})")
        raise ValueError(f"Length of data_batches ({total_batches}) must be divisible by n ({n})")

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：m = total_batches // n
    m = total_batches // n

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Initialize output batches
    # Initialize output batches
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_batches = []
    output_batches = []

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Process in groups of n
    # Process in groups of n
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i in range(m):
    for i in range(m):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Get the corresponding batch from each group
        # Get the corresponding batch from each group
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batches_to_concat = []
        batches_to_concat = []
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for j in range(n):
        for j in range(n):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch_idx = j * m + i
            batch_idx = j * m + i
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：batches_to_concat.append(data_batches[batch_idx])
            batches_to_concat.append(data_batches[batch_idx])

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Create a new merged dictionary
        # Create a new merged dictionary
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：merged_batch = {}
        merged_batch = {}

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Get all unique keys from the dictionaries
        # Get all unique keys from the dictionaries
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：all_keys = set()
        all_keys = set()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for batch in batches_to_concat:
        for batch in batches_to_concat:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：all_keys.update(batch.keys())
            all_keys.update(batch.keys())

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Process each key
        # Process each key
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key in all_keys:
        for key in all_keys:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Collect values for this key from all batches
            # Collect values for this key from all batches
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：values = []
            values = []
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for batch in batches_to_concat:
            for batch in batches_to_concat:
                # 中文说明：根据条件选择执行分支；代码：if key in batch:
                if key in batch:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：values.append(batch[key])
                    values.append(batch[key])

            # 中文说明：根据条件选择执行分支；代码：if not values:
            if not values:
                # 中文说明：执行循环控制或空操作；代码：continue
                continue

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Determine the type of the first non-None value
            # Determine the type of the first non-None value
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：first_value = next((v for v in values if v is not None), None)
            first_value = next((v for v in values if v is not None), None)
            # 中文说明：根据条件选择执行分支；代码：if first_value is None:
            if first_value is None:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：merged_batch[key] = None
                merged_batch[key] = None
                # 中文说明：执行循环控制或空操作；代码：continue
                continue

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Handle different types
            # Handle different types
            # 中文说明：根据条件选择执行分支；代码：if isinstance(first_value, torch.Tensor):
            if isinstance(first_value, torch.Tensor):
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Assuming this is a tensor-like object with cat method (e.g., torch.Tensor)
                # Assuming this is a tensor-like object with cat method (e.g., torch.Tensor)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：merged_batch[key] = torch.cat(values, dim=0)
                merged_batch[key] = torch.cat(values, dim=0)
            # 中文说明：根据条件选择执行分支；代码：elif isinstance(first_value, str):
            elif isinstance(first_value, str):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：merged_batch[key] = values[0]
                merged_batch[key] = values[0]
            # 中文说明：根据条件选择执行分支；代码：elif isinstance(first_value, list):
            elif isinstance(first_value, list):
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Extend lists
                # Extend lists
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：merged_list = []
                merged_list = []
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for v in values:
                for v in values:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：merged_list.extend(v)
                    merged_list.extend(v)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：merged_batch[key] = merged_list
                merged_batch[key] = merged_list
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# For other types, just use the list of values
                # For other types, just use the list of values
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：merged_batch[key] = values
                merged_batch[key] = values

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：output_batches.append(merged_batch)
        output_batches.append(merged_batch)

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return output_batches
    return output_batches


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class CachedReplayDataLoader:
class CachedReplayDataLoader:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""A DataLoader wrapper that asynchronously caches and replays data batches to
    """A DataLoader wrapper that asynchronously caches and replays data batches to
    mitigate slow loading issues. Assumes the underlying DataLoader is infinite.

    This class delegates all augmentation logic to an external augmentation function,
    which takes a batch from the data loader and returns multiple augmented versions.
    The class handles caching these augmented batches and optionally concatenating
    them when yielded.

    Attributes:
        data_loader (DataLoader): The underlying infinite DataLoader.
        cache_size (int): Maximum number of augmented batches to store in the cache.
        cache_augmentation_fn (Callable): Function to create multiple augmented versions of each batch.
        concat_size (int): Number of batches to concatenate when yielding from the iterator.
        rng (numpy.random.Generator): Controlled random number generator for deterministic behavior.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_loader: DataLoader,
        data_loader: DataLoader,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cache_size: int,
        cache_size: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cache_augmentation_fn: Callable[[Dict], List[Dict]],
        cache_augmentation_fn: Callable[[Dict], List[Dict]],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：concat_size: int = 1,
        concat_size: int = 1,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：name: str = "cached_replay_dataloader",
        name: str = "cached_replay_dataloader",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Initialize the CachedReplayDataLoader.
        """Initialize the CachedReplayDataLoader.

        Args:
            data_loader (DataLoader): The infinite DataLoader to fetch data batches from.
            cache_size (int): Maximum number of augmented data batches to store in the cache.
            cache_augmentation_fn (Callable[[Dict], List[Dict]]): Function that takes a batch and returns
                a list of augmented batches.
            concat_size (int, optional): Number of batches to concatenate when yielding. Defaults to 1.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.data_loader = data_loader
        self.data_loader = data_loader
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.cache_size = cache_size
        self.cache_size = cache_size
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.cache_augmentation_fn = cache_augmentation_fn
        self.cache_augmentation_fn = cache_augmentation_fn
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.concat_size = concat_size
        self.concat_size = concat_size

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Create controlled random number generator for deterministic behavior
        # Create controlled random number generator for deterministic behavior
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.rng = np.random.default_rng(123)
        self.rng = np.random.default_rng(123)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Create an iterator over the infinite DataLoader.
        # Create an iterator over the infinite DataLoader.
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._data_iter: Iterator = iter(self.data_loader)
        self._data_iter: Iterator = iter(self.data_loader)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Internal cache to store augmented batches.
        # Internal cache to store augmented batches.
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._cache: List[Dict] = []
        self._cache: List[Dict] = []
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Condition variable to manage cache access.
        # Condition variable to manage cache access.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._cache_cond = threading.Condition()
        self._cache_cond = threading.Condition()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Event to signal the background thread to stop.
        # Event to signal the background thread to stop.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._stop_event = threading.Event()
        self._stop_event = threading.Event()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Store exceptions from the background thread
        # Store exceptions from the background thread
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._prefetch_exception = None
        self._prefetch_exception = None

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._watchdog = OperationWatchdog(warning_threshold=100, verbose_interval=600, name=name)
        self._watchdog = OperationWatchdog(warning_threshold=100, verbose_interval=600, name=name)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._prefetch_thread = threading.Thread(
        self._prefetch_thread = threading.Thread(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：target=self._prefetch_loop, daemon=True, name=f"{name}_prefetch_thread"
            target=self._prefetch_loop, daemon=True, name=f"{name}_prefetch_thread"
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._prefetch_thread.start()
        self._prefetch_thread.start()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _prefetch_loop(self) -> None:
    def _prefetch_loop(self) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Continuously fetch batches from the DataLoader, augment them, and store in the cache.
        """Continuously fetch batches from the DataLoader, augment them, and store in the cache.

        If the cache is full (reaches `cache_size`), this loop waits until space is available.
        Catches exceptions and stores them for later propagation to the main thread.
        """
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：在条件成立时重复执行循环体；代码：while not self._stop_event.is_set():
            while not self._stop_event.is_set():
                # 中文说明：开始一个可捕获异常的代码块；代码：try:
                try:
                    # 中文说明：处理异常、清理资源或管理上下文；代码：with self._watchdog.watch("fetch raw batch", verbose_first_n=5):
                    with self._watchdog.watch("fetch raw batch", verbose_first_n=5):
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch = next(self._data_iter)
                        batch = next(self._data_iter)
                # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
                except Exception as e:
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Capture DataLoader errors
                    # Capture DataLoader errors
                    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._set_exception(e, "Error fetching batch from DataLoader")
                    self._set_exception(e, "Error fetching batch from DataLoader")
                    # 中文说明：执行循环控制或空操作；代码：break
                    break

                # 中文说明：开始一个可捕获异常的代码块；代码：try:
                try:
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Apply augmentation function to generate multiple augmented batches
                    # Apply augmentation function to generate multiple augmented batches
                    # 中文说明：处理异常、清理资源或管理上下文；代码：with self._watchdog.watch("augmentation", verbose_first_n=5):
                    with self._watchdog.watch("augmentation", verbose_first_n=5):
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：augmented_batches = self.cache_augmentation_fn(batch)
                        augmented_batches = self.cache_augmentation_fn(batch)
                # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
                except Exception as e:
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Capture augmentation function errors
                    # Capture augmentation function errors
                    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._set_exception(e, "Error in augmentation function")
                    self._set_exception(e, "Error in augmentation function")
                    # 中文说明：执行循环控制或空操作；代码：break
                    break

                # 中文说明：开始一个可捕获异常的代码块；代码：try:
                try:
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Use controlled random generator for shuffling
                    # Use controlled random generator for shuffling
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：permutation = self.rng.permutation(len(augmented_batches))
                    permutation = self.rng.permutation(len(augmented_batches))
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：augmented_batches = [augmented_batches[i] for i in permutation]
                    augmented_batches = [augmented_batches[i] for i in permutation]

                    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for aug_batch in augmented_batches:
                    for aug_batch in augmented_batches:
                        # 中文说明：处理异常、清理资源或管理上下文；代码：with self._cache_cond:
                        with self._cache_cond:
                            # 中文说明：在条件成立时重复执行循环体；代码：while len(self._cache) >= self.cache_size and not self._stop_event.is_set():
                            while len(self._cache) >= self.cache_size and not self._stop_event.is_set():
                                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._cache_cond.wait(timeout=1.0)
                                self._cache_cond.wait(timeout=1.0)
                            # 中文说明：根据条件选择执行分支；代码：if self._stop_event.is_set():
                            if self._stop_event.is_set():
                                # 中文说明：执行循环控制或空操作；代码：break
                                break
                            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._cache.append(aug_batch)
                            self._cache.append(aug_batch)
                            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._cache_cond.notify_all()
                            self._cache_cond.notify_all()
                # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
                except Exception as e:
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Capture other errors during caching
                    # Capture other errors during caching
                    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._set_exception(e, "Error adding batch to cache")
                    self._set_exception(e, "Error adding batch to cache")
                    # 中文说明：执行循环控制或空操作；代码：break
                    break
        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
        except Exception as e:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Catch any other unforeseen errors
            # Catch any other unforeseen errors
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._set_exception(e, "Unexpected error in prefetch thread")
            self._set_exception(e, "Unexpected error in prefetch thread")

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _set_exception(self, exception: Exception, context: str = "") -> None:
    def _set_exception(self, exception: Exception, context: str = "") -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Store an exception from the background thread with context information.
        """Store an exception from the background thread with context information.

        Args:
            exception (Exception): The exception that was raised
            context (str, optional): Additional context about where the error occurred
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：error_info = f"{context}: {str(exception)}\n{traceback.format_exc()}"
        error_info = f"{context}: {str(exception)}\n{traceback.format_exc()}"
        # 中文说明：处理异常、清理资源或管理上下文；代码：with self._cache_cond:
        with self._cache_cond:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._prefetch_exception = RuntimeError(error_info)
            self._prefetch_exception = RuntimeError(error_info)
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._cache_cond.notify_all() # Wake up any waiting threads
            self._cache_cond.notify_all()  # Wake up any waiting threads

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _check_for_errors(self) -> None:
    def _check_for_errors(self) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Check if the background thread has encountered an error and raise it if so."""
        """Check if the background thread has encountered an error and raise it if so."""
        # 中文说明：根据条件选择执行分支；代码：if self._prefetch_exception is not None:
        if self._prefetch_exception is not None:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise self._prefetch_exception
            raise self._prefetch_exception

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __iter__(self) -> Iterator[Dict]:
    def __iter__(self) -> Iterator[Dict]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Yield augmented data batches from the cache, optionally concatenated based on concat_size.
        """Yield augmented data batches from the cache, optionally concatenated based on concat_size.

        This method starts the background prefetch thread if it hasn't been started yet.
        If concat_size > 1, it collects multiple batches and concatenates them.

        Raises:
            RuntimeError: If the background thread encountered an error
        """
        # 中文说明：在条件成立时重复执行循环体；代码：while not self._stop_event.is_set():
        while not self._stop_event.is_set():
            # 中文说明：根据条件选择执行分支；代码：if self.concat_size <= 1:
            if self.concat_size <= 1:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Simple case: yield single batches
                # Simple case: yield single batches
                # 中文说明：处理异常、清理资源或管理上下文；代码：with self._watchdog.watch("main thread fetch single batch", verbose_first_n=5):
                with self._watchdog.watch("main thread fetch single batch", verbose_first_n=5):
                    # 中文说明：处理异常、清理资源或管理上下文；代码：with self._cache_cond:
                    with self._cache_cond:
                        # 中文说明：在条件成立时重复执行循环体；代码：while not self._cache and not self._stop_event.is_set() and self._prefetch_exception is None:
                        while not self._cache and not self._stop_event.is_set() and self._prefetch_exception is None:
                            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._cache_cond.wait(timeout=1.0) # Add timeout to periodically check for errors
                            self._cache_cond.wait(timeout=1.0)  # Add timeout to periodically check for errors

                        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Check for errors before proceeding
                        # Check for errors before proceeding
                        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._check_for_errors()
                        self._check_for_errors()

                        # 中文说明：根据条件选择执行分支；代码：if self._stop_event.is_set():
                        if self._stop_event.is_set():
                            # 中文说明：执行循环控制或空操作；代码：break
                            break

                        # 中文说明：根据条件选择执行分支；代码：if not self._cache: # If cache is still empty after timeout
                        if not self._cache:  # If cache is still empty after timeout
                            # 中文说明：执行循环控制或空操作；代码：continue
                            continue

                        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Use controlled random generator to select batch index
                        # Use controlled random generator to select batch index
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：idx = self.rng.integers(0, len(self._cache))
                        idx = self.rng.integers(0, len(self._cache))
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch = self._cache.pop(idx)
                        batch = self._cache.pop(idx)
                        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._cache_cond.notify_all()
                        self._cache_cond.notify_all()
                # 中文说明：从生成器逐步产生本行指定的值；代码：yield batch
                yield batch
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Collect concat_size batches and concatenate them
                # Collect concat_size batches and concatenate them
                # 中文说明：处理异常、清理资源或管理上下文；代码：with self._watchdog.watch("main thread fetch smaples", verbose_first_n=5):
                with self._watchdog.watch("main thread fetch smaples", verbose_first_n=5):
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：collected_batches = []
                    collected_batches = []
                    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _ in range(self.concat_size):
                    for _ in range(self.concat_size):
                        # 中文说明：处理异常、清理资源或管理上下文；代码：with self._cache_cond:
                        with self._cache_cond:
                            # 中文说明：在条件成立时重复执行循环体；代码：while (
                            while (
                                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：not self._cache and not self._stop_event.is_set() and self._prefetch_exception is None
                                not self._cache and not self._stop_event.is_set() and self._prefetch_exception is None
                            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
                            ):
                                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._cache_cond.wait(timeout=1.0) # Add timeout to periodically check for errors
                                self._cache_cond.wait(timeout=1.0)  # Add timeout to periodically check for errors

                            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Check for errors before proceeding
                            # Check for errors before proceeding
                            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._check_for_errors()
                            self._check_for_errors()

                            # 中文说明：根据条件选择执行分支；代码：if self._stop_event.is_set():
                            if self._stop_event.is_set():
                                # 中文说明：执行循环控制或空操作；代码：break
                                break

                            # 中文说明：根据条件选择执行分支；代码：if not self._cache: # If cache is still empty after timeout
                            if not self._cache:  # If cache is still empty after timeout
                                # 中文说明：执行循环控制或空操作；代码：continue
                                continue

                            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Use controlled random generator to select batch index
                            # Use controlled random generator to select batch index
                            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：idx = self.rng.integers(0, len(self._cache))
                            idx = self.rng.integers(0, len(self._cache))
                            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch = self._cache.pop(idx)
                            batch = self._cache.pop(idx)
                            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._cache_cond.notify_all()
                            self._cache_cond.notify_all()
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：collected_batches.append(batch)
                        collected_batches.append(batch)

                # 中文说明：根据条件选择执行分支；代码：if self._stop_event.is_set():
                if self._stop_event.is_set():
                    # 中文说明：执行循环控制或空操作；代码：break
                    break

                # 中文说明：根据条件选择执行分支；代码：if not collected_batches:
                if not collected_batches:
                    # 中文说明：执行循环控制或空操作；代码：continue
                    continue

                # 中文说明：根据条件选择执行分支；代码：if len(collected_batches) < self.concat_size:
                if len(collected_batches) < self.concat_size:
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Not enough batches collected, just concatenate the ones we have
                    # Not enough batches collected, just concatenate the ones we have
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：concat_batches = concatenate_batches(len(collected_batches), collected_batches)
                    concat_batches = concatenate_batches(len(collected_batches), collected_batches)
                    # 中文说明：从生成器逐步产生本行指定的值；代码：yield concat_batches[0]
                    yield concat_batches[0]
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Concatenate the collected batches
                    # Concatenate the collected batches
                    # 中文说明：开始一个可捕获异常的代码块；代码：try:
                    try:
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：concat_batches = concatenate_batches(self.concat_size, collected_batches)
                        concat_batches = concatenate_batches(self.concat_size, collected_batches)
                        # 中文说明：从生成器逐步产生本行指定的值；代码：yield concat_batches[0]
                        yield concat_batches[0]
                    # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
                    except Exception as e:
                        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Handle errors in batch concatenation
                        # Handle errors in batch concatenation
                        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise RuntimeError(f"Error concatenating batches: {str(e)}") from e
                        raise RuntimeError(f"Error concatenating batches: {str(e)}") from e

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __len__(self) -> int:
    def __len__(self) -> int:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Return the length of the underlying DataLoader."""
        """Return the length of the underlying DataLoader."""
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return len(self.data_loader)
        return len(self.data_loader)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def close(self) -> None:
    def close(self) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Stop the prefetch thread and clear the cache.
        """Stop the prefetch thread and clear the cache.
        Also checks for any errors in the background thread and raises them.
        """
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._stop_event.set()
        self._stop_event.set()
        # 中文说明：处理异常、清理资源或管理上下文；代码：with self._cache_cond:
        with self._cache_cond:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._cache_cond.notify_all()
            self._cache_cond.notify_all()
        # 中文说明：根据条件选择执行分支；代码：if self._prefetch_thread is not None:
        if self._prefetch_thread is not None:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._prefetch_thread.join(timeout=5.0) # Add timeout to avoid hanging on thread join
            self._prefetch_thread.join(timeout=5.0)  # Add timeout to avoid hanging on thread join
        # 中文说明：处理异常、清理资源或管理上下文；代码：with self._cache_cond:
        with self._cache_cond:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._cache.clear()
            self._cache.clear()

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Check and propagate any errors from the background thread
        # Check and propagate any errors from the background thread
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._check_for_errors()
        self._check_for_errors()


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_cached_replay_dataloader(
def get_cached_replay_dataloader(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：use_cache: bool = False,
    use_cache: bool = False,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cache_size: int = 32,
    cache_size: int = 32,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：concat_size: int = 1,
    concat_size: int = 1,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cache_augment_fn: Optional[Callable] = None,
    cache_augment_fn: Optional[Callable] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cache_replay_name: str = "cached_replay_dataloader",
    cache_replay_name: str = "cached_replay_dataloader",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：webdataset: bool = True,
    webdataset: bool = True,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**kwargs,
    **kwargs,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：根据条件选择执行分支；代码：if webdataset:
    if webdataset:
        # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.datasets.webdataset.dataloader import DataLoader as _DataLoader
        from imaginaire.datasets.webdataset.dataloader import DataLoader as _DataLoader
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.utils.data import DataLoader as _DataLoader
        from torch.utils.data import DataLoader as _DataLoader

    # 中文说明：根据条件选择执行分支；代码：if not use_cache:
    if not use_cache:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return _DataLoader(**kwargs)
        return _DataLoader(**kwargs)

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：expected_batch_size = kwargs["batch_size"]
    expected_batch_size = kwargs["batch_size"]
    # 中文说明：检查运行时假设是否成立；代码：assert (
    assert (
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：expected_batch_size % concat_size == 0
        expected_batch_size % concat_size == 0
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"Batch size {expected_batch_size} must be divisible by concat_size {concat_size}"
    ), f"Batch size {expected_batch_size} must be divisible by concat_size {concat_size}"
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["batch_size"] = expected_batch_size // concat_size
    kwargs["batch_size"] = expected_batch_size // concat_size

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataloader = _DataLoader(**kwargs)
    dataloader = _DataLoader(**kwargs)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# wrapper it with cached replay dataloader
    # wrapper it with cached replay dataloader
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return CachedReplayDataLoader(
    return CachedReplayDataLoader(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_loader=dataloader,
        data_loader=dataloader,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_size=cache_size,
        cache_size=cache_size,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：concat_size=concat_size,
        concat_size=concat_size,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_augmentation_fn=cache_augment_fn,
        cache_augmentation_fn=cache_augment_fn,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name=cache_replay_name,
        name=cache_replay_name,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
