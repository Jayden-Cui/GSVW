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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import inspect
import inspect
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any, Callable, Dict
from typing import Any, Callable, Dict

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.utils.data import Dataset
from torch.utils.data import Dataset

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：MAX_LENGTH = 1 << 15
MAX_LENGTH = 1 << 15


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class LambdaDataset(torch.utils.data.Dataset):
class LambdaDataset(torch.utils.data.Dataset):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    A dataset that generates items by applying a function. This allows for creating
    dynamic datasets where the items are the result of function calls. The function can optionally
    accept an index argument.

    Attributes:
        length (int): The total number of items in the dataset.
        fn (Callable): The function to generate dataset items.
        is_index_in_params (bool): Flag to determine whether 'index' should be passed
                                   to the function `fn`.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, fn: Callable, length: int = MAX_LENGTH) -> None:
    def __init__(self, fn: Callable, length: int = MAX_LENGTH) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Initializes the LambdaDataset with a function and the total length.

        Args:
            fn (Callable): A function that returns a dataset item. It can optionally accept an
                           index argument to generate data items based on their index.
            length (int): The total number of items in the dataset, defaults to MAX_LENGTH.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.length = length
        self.length = length
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.fn = fn
        self.fn = fn

        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Attempt to inspect the function signature to determine if it accepts an 'index' parameter.
            # Attempt to inspect the function signature to determine if it accepts an 'index' parameter.
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：signature = inspect.signature(fn)
            signature = inspect.signature(fn)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.is_index_in_params = "index" in signature.parameters
            self.is_index_in_params = "index" in signature.parameters
        # 中文说明：处理异常、清理资源或管理上下文；代码：except ValueError:
        except ValueError:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# If the function signature is not inspectable, assume 'index' is not a parameter.
            # If the function signature is not inspectable, assume 'index' is not a parameter.
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.is_index_in_params = False
            self.is_index_in_params = False

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __len__(self) -> int:
    def __len__(self) -> int:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Returns the total length of the dataset.

        Returns:
            int: The number of items in the dataset.
        """
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.length
        return self.length

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __getitem__(self, index: int) -> Any:
    def __getitem__(self, index: int) -> Any:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Retrieves an item at a specific index from the dataset by calling the function `fn`.
        Passes the index to `fn` if `fn` is designed to accept an index.

        Args:
            index (int): The index of the item to retrieve.

        Returns:
            Any: The item returned by the function `fn`.
        """
        # 中文说明：根据条件选择执行分支；代码：if self.is_index_in_params:
        if self.is_index_in_params:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.fn(index) # Call fn with index if it accepts an index parameter.
            return self.fn(index)  # Call fn with index if it accepts an index parameter.
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.fn() # Call fn without any parameters if it does not accept the index.
        return self.fn()  # Call fn without any parameters if it does not accept the index.


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class RepeatDataset(torch.utils.data.Dataset):
class RepeatDataset(torch.utils.data.Dataset):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    A dataset wrapper that allows repeating access to items from an underlying dataset.

    This dataset can be used to create an artificial extension of the underlying dataset
    to a specified `length`. Each item from the original dataset can be accessed
    repeatedly up to `num_item` times before it loops back.

    Attributes:
        length (int): The total length of the dataset to be exposed.
        dataset (Dataset): The original dataset.
        num_item (int): Number of times each item is repeated.
        cache_item (dict): Cache to store accessed items to avoid recomputation.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, dataset: Dataset, length: int = MAX_LENGTH, num_item: int = 1) -> None:
    def __init__(self, dataset: Dataset, length: int = MAX_LENGTH, num_item: int = 1) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Initializes the RepeatDataset with a dataset, length, and number of repeats per item.

        Args:
            dataset (Dataset): The dataset to repeat.
            length (int): The total length of the dataset to be exposed. Defaults to MAX_LENGTH.
            num_item (int): The number of times to repeat each item. Defaults to 1.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.length = length
        self.length = length
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dataset = dataset
        self.dataset = dataset
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_item = num_item
        self.num_item = num_item
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.cache_item = {}
        self.cache_item = {}

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __len__(self) -> int:
    def __len__(self) -> int:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.length
        return self.length

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __getitem__(self, index: int) -> Any:
    def __getitem__(self, index: int) -> Any:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：index = index % self.num_item
        index = index % self.num_item
        # 中文说明：根据条件选择执行分支；代码：if index not in self.cache_item:
        if index not in self.cache_item:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.cache_item[index] = self.dataset[index]
            self.cache_item[index] = self.dataset[index]
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.cache_item[index]
        return self.cache_item[index]


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class CombinedDictDataset(torch.utils.data.Dataset):
class CombinedDictDataset(torch.utils.data.Dataset):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    A dataset that wraps multiple PyTorch datasets and returns a dictionary of data items from each dataset for a given index.
    This dataset ensures that all constituent datasets have the same length by setting the length to the minimum length of the datasets provided.

    Parameters:
    -----------
    **datasets : Dict[str, Dataset]
        A dictionary where keys are string identifiers for the datasets and values are the datasets instances themselves.

    Attributes:
    -----------
    datasets : Dict[str, Dataset]
        Stores the input datasets.
    max_length : int
        The minimum length among all provided datasets, determining the length of this combined dataset.

    Examples:
    ---------
    >>> dataset1 = torch.utils.data.TensorDataset(torch.randn(100, 3, 32, 32))
    >>> dataset2 = torch.utils.data.TensorDataset(torch.randn(100, 3, 32, 32))
    >>> combined_dataset = CombinedDictDataset(dataset1=dataset1, dataset2=dataset2)
    >>> print(len(combined_dataset))
    100
    >>> data = combined_dataset[50]
    >>> print(data.keys())
    dict_keys(['dataset1', 'dataset2'])
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, **datasets: Dict[str, Dataset]) -> None:
    def __init__(self, **datasets: Dict[str, Dataset]) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Initializes the CombinedDictDataset with multiple datasets.

        Args:
            **datasets (Dict[str, Dataset]): Key-value pairs where keys are dataset names and values
                                             are dataset instances. Each key-value pair adds a dataset
                                             under the specified key.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.datasets = datasets
        self.datasets = datasets
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.max_length = min([len(dataset) for dataset in datasets.values()])
        self.max_length = min([len(dataset) for dataset in datasets.values()])

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __len__(self) -> int:
    def __len__(self) -> int:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.max_length
        return self.max_length

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __getitem__(self, index: int) -> Dict[str, Any]:
    def __getitem__(self, index: int) -> Dict[str, Any]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Retrieves an item from each dataset at the specified index, combines them into a dictionary,
        and returns the dictionary. Each key in the dictionary corresponds to one of the dataset names provided
        during initialization, and its value is the item from that dataset at the given index.

        Args:
            index (int): The index of the items to retrieve across all datasets.

        Returns:
            Dict[str, Any]: A dictionary containing data items from all datasets for the given index.
                            Each key corresponds to a dataset name, and its value is the data item from that dataset.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data = {}
        data = {}
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key, dataset in self.datasets.items():
        for key, dataset in self.datasets.items():
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data[key] = dataset[index]
            data[key] = dataset[index]
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return data
        return data
