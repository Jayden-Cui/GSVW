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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Dict, Union
from typing import Dict, Union

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import webdataset
import webdataset

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import instantiate
from imaginaire.lazy_config import instantiate


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class IterativeJointDataLoader(webdataset.WebLoader):
class IterativeJointDataLoader(webdataset.WebLoader):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""
    r"""
    A joint dataloader that supports loading both images and videos.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, dataloaders: Dict[str, Dict[str, Union[torch.utils.data.DataLoader, webdataset.WebLoade...
        self, dataloaders: Dict[str, Dict[str, Union[torch.utils.data.DataLoader, webdataset.WebLoader, int]]]
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Initialize the JointDataLoader with multiple datasets.

        Args:
            dataloaders: key - dataset_name; value - {"dataloader": dataloader, "ratio": data_ratio}

        Example:
            joint_loader = IterativeJointDataLoader(
                dataloaders{
                    "image_data": {
                        "dataloader": webdataset.WebLoader(...),
                        "ratio": 4,
                    },
                    "video_data": {
                        "dataloader": torch.utils.data.DataLoader(...),
                        "ratio": 1,
                    },
                }
            )
        """
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.dataloader_list, self.dataset_name_list, self.data_ratios = [], [], []
        self.dataloader_list, self.dataset_name_list, self.data_ratios = [], [], []

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for dataset_name, dataloader_data in dataloaders.items():
        for dataset_name, dataloader_data in dataloaders.items():
            # 中文说明：检查运行时假设是否成立；代码：assert set(dataloader_data.keys()) == {"dataloader", "ratio"}, f"Invalid config: {dataloader_...
            assert set(dataloader_data.keys()) == {"dataloader", "ratio"}, f"Invalid config: {dataloader_data}"
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.dataset_name_list.append(dataset_name)
            self.dataset_name_list.append(dataset_name)
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.dataloader_list.append(instantiate(dataloader_data["dataloader"]))
            self.dataloader_list.append(instantiate(dataloader_data["dataloader"]))
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.data_ratios.append(dataloader_data["ratio"])
            self.data_ratios.append(dataloader_data["ratio"])

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.global_id = 0
        self.global_id = 0
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.ratio_sum = sum(self.data_ratios)
        self.ratio_sum = sum(self.data_ratios)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.data_len = 0
        self.data_len = 0
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dataloaders = [iter(dataloader) for dataloader in self.dataloader_list]
        self.dataloaders = [iter(dataloader) for dataloader in self.dataloader_list]
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for data in self.dataloader_list:
        for data in self.dataloader_list:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.data_len += len(data)
            self.data_len += len(data)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __len__(self) -> int:
    def __len__(self) -> int:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.data_len
        return self.data_len

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __iter__(self):
    def __iter__(self):
        # 中文说明：在条件成立时重复执行循环体；代码：while True:
        while True:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_id = self.global_id % self.ratio_sum
            data_id = self.global_id % self.ratio_sum
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：index_id = self._get_dataloader_index(data_id)
            index_id = self._get_dataloader_index(data_id)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_dataloader = self.dataloaders[index_id]
            curr_dataloader = self.dataloaders[index_id]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output = next(curr_dataloader)
            output = next(curr_dataloader)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output["dataset_name"] = self.dataset_name_list[index_id]
            output["dataset_name"] = self.dataset_name_list[index_id]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.global_id += 1
            self.global_id += 1
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del curr_dataloader
            del curr_dataloader
            # 中文说明：从生成器逐步产生本行指定的值；代码：yield output
            yield output

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _get_dataloader_index(self, data_id):
    def _get_dataloader_index(self, data_id):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Maps global id to the corresponding dataloader index based on ratio."""
        """Maps global id to the corresponding dataloader index based on ratio."""
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i, r in enumerate(self.data_ratios):
        for i, r in enumerate(self.data_ratios):
            # 中文说明：根据条件选择执行分支；代码：if data_id < r:
            if data_id < r:
                # 中文说明：从当前函数返回结果或结束函数执行；代码：return i
                return i
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_id -= r
            data_id -= r
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError("Invalid data_id")
        raise ValueError("Invalid data_id")


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class RandomJointDataLoader(webdataset.WebLoader):
class RandomJointDataLoader(webdataset.WebLoader):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""
    r"""
    A joint dataloader that supports randomly samples batches from multiple datasets.
    """

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# def __init__(self, **kwargs):
    # def __init__(self, **kwargs):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, dataloaders: Dict[str, Dict[str, Union[torch.utils.data.DataLoader, webdataset.WebLoade...
        self, dataloaders: Dict[str, Dict[str, Union[torch.utils.data.DataLoader, webdataset.WebLoader, int]]]
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Initialize the JointDataLoader with multiple datasets.

        Args:
            **kwargs: Arbitrary keyword arguments where each key is a string
                      representing the dataset name, and each value is either
                      a `webdataset.WebLoader` or `torch.utils.data.DataLoader`
                      instance.

        Raises:
            AssertionError: If any value in kwargs is not an instance of
                            `webdataset.WebLoader` or `torch.utils.data.DataLoader`.
            AssertionError: If any key in kwargs is not a string.

        Example:
            joint_loader = JointDataLoader(
                images=webdataset.WebLoader(...),
                videos=torch.utils.data.DataLoader(...)
            )
        """
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.dataloader_list, self.dataset_name_list, self.data_ratios = [], [], []
        self.dataloader_list, self.dataset_name_list, self.data_ratios = [], [], []

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for dataset_name, dataloader_data in dataloaders.items():
        for dataset_name, dataloader_data in dataloaders.items():
            # 中文说明：检查运行时假设是否成立；代码：assert set(dataloader_data.keys()) == {"dataloader", "ratio"}, f"Invalid config: {dataloader_...
            assert set(dataloader_data.keys()) == {"dataloader", "ratio"}, f"Invalid config: {dataloader_data}"
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.dataset_name_list.append(dataset_name)
            self.dataset_name_list.append(dataset_name)
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.dataloader_list.append(instantiate(dataloader_data["dataloader"]))
            self.dataloader_list.append(instantiate(dataloader_data["dataloader"]))
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.data_ratios.append(dataloader_data["ratio"])
            self.data_ratios.append(dataloader_data["ratio"])

        # 中文说明：检查运行时假设是否成立；代码：assert sum(self.data_ratios) == 1.0, "Sum of sample probabilities should be equal to 1."
        assert sum(self.data_ratios) == 1.0, "Sum of sample probabilities should be equal to 1."

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.data_len = 0
        self.data_len = 0
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dataloaders = [iter(dataloader) for dataloader in self.dataloader_list]
        self.dataloaders = [iter(dataloader) for dataloader in self.dataloader_list]
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for data in self.dataloader_list:
        for data in self.dataloader_list:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.data_len += len(data)
            self.data_len += len(data)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __len__(self) -> int:
    def __len__(self) -> int:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.data_len
        return self.data_len

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __iter__(self):
    def __iter__(self):
        # 中文说明：在条件成立时重复执行循环体；代码：while True:
        while True:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Sample a random dataset
            # Sample a random dataset
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_id = int(np.random.choice(len(self.dataloader_list), 1, p=self.data_ratios)[0])
            data_id = int(np.random.choice(len(self.dataloader_list), 1, p=self.data_ratios)[0])
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_dataloader = self.dataloaders[data_id]
            curr_dataloader = self.dataloaders[data_id]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output = next(curr_dataloader)
            output = next(curr_dataloader)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output["dataset_name"] = self.dataset_name_list[data_id]
            output["dataset_name"] = self.dataset_name_list[data_id]
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del curr_dataloader
            del curr_dataloader
            # 中文说明：从生成器逐步产生本行指定的值；代码：yield output
            yield output
