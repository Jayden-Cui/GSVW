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

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import webdataset
import webdataset

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import imaginaire.datasets.webdataset.webdataset
import imaginaire.datasets.webdataset.webdataset
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.distributed import get_world_size
from imaginaire.utils.distributed import get_world_size


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Sampler:
class Sampler:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""
    r"""
    A sampler function for setting the epoch number and iteration number.
    In webdataset, information is propagated using environment flags.
    In our case,
        WDS_EPOCH_NUM: Epoch number
        WDS_START_INDEX: Start index in this epoch.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, mode: str):
    def __init__(self, mode: str):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mode = mode
        self.mode = mode
        # 中文说明：检查运行时假设是否成立；代码：assert self.mode in ["train", "val"]
        assert self.mode in ["train", "val"]

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def set_epoch(self, epoch: int):
    def set_epoch(self, epoch: int):
        # 中文说明：根据条件选择执行分支；代码：if self.mode == "train":
        if self.mode == "train":
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：os.environ["WDS_EPOCH_NUM"] = str(epoch)
            os.environ["WDS_EPOCH_NUM"] = str(epoch)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行循环控制或空操作；代码：pass
            pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def set_iteration(self, start_index: int):
    def set_iteration(self, start_index: int):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# start_index should be iters * batch_size
        # start_index should be iters * batch_size
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# It is the number of samples that have been seen by one GPU
        # It is the number of samples that have been seen by one GPU
        # 中文说明：根据条件选择执行分支；代码：if self.mode == "train":
        if self.mode == "train":
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：os.environ["WDS_START_INDEX"] = str(start_index)
            os.environ["WDS_START_INDEX"] = str(start_index)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行循环控制或空操作；代码：pass
            pass


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class DataLoader(webdataset.WebLoader):
class DataLoader(webdataset.WebLoader):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""
    r"""
    This class is a wrapper on webloader class with a len attribute.
    len function is needed in Imaginaire dataloaders.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, dataset: imaginaire.datasets.webdataset.webdataset.Dataset, batch_size: in...
    def __init__(self, dataset: imaginaire.datasets.webdataset.webdataset.Dataset, batch_size: int = 1, *args, **kw):  # type: ignore
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Setting data length. Webdataset is an iterable dataset, so it does not have data_len attr.
        # Setting data length. Webdataset is an iterable dataset, so it does not have data_len attr.
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# So, we compute it from dataset and set it.
        # So, we compute it from dataset and set it.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset_obj = dataset.build_dataset()
        dataset_obj = dataset.build_dataset()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：world_size = get_world_size()
        world_size = get_world_size()
        # 中文说明：根据条件选择执行分支；代码：if dataset_obj.total_images < world_size * batch_size: # type: ignore
        if dataset_obj.total_images < world_size * batch_size:  # type: ignore
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_length = 1
            data_length = 1
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_length = dataset_obj.total_images // (world_size * batch_size) # type: ignore
            data_length = dataset_obj.total_images // (world_size * batch_size)  # type: ignore
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.data_len = data_length
        self.data_len = data_length

        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(dataset_obj, batch_size, *args, **kw)
        super().__init__(dataset_obj, batch_size, *args, **kw)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __len__(self) -> int:
    def __len__(self) -> int:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.data_len
        return self.data_len
