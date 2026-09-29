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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import pickle
import pickle
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from collections.abc import Iterable
from collections.abc import Iterable
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from functools import partial
from functools import partial
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Callable
from typing import Callable

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import omegaconf
import omegaconf
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import webdataset as wds
import webdataset as wds
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from webdataset.handlers import reraise_exception
from webdataset.handlers import reraise_exception

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.datasets.webdataset.config.schema import AugmentorConfig, DatasetConfig, Data...
from imaginaire.datasets.webdataset.config.schema import AugmentorConfig, DatasetConfig, DatasetInfo, TarSample, Wdinfo
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.datasets.webdataset.utils.iterators import WebDataset
from imaginaire.datasets.webdataset.utils.iterators import WebDataset
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.datasets.webdataset.utils.misc import remove_extensions_from_keys, skip_keys,...
from imaginaire.datasets.webdataset.utils.misc import remove_extensions_from_keys, skip_keys, update_url
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import instantiate
from imaginaire.lazy_config import instantiate
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.distributed import get_world_size
from imaginaire.utils.distributed import get_world_size


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def wrap_augmentor_func_as_generator(func: Callable, data: Iterable):
def wrap_augmentor_func_as_generator(func: Callable, data: Iterable):
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for data_dict in data:
    for data_dict in data:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_dict_out = func(data_dict)
        data_dict_out = func(data_dict)
        # 中文说明：根据条件选择执行分支；代码：if data_dict_out is None:
        if data_dict_out is None:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Skip "unhealthy" samples
            # Skip "unhealthy" samples
            # 中文说明：执行循环控制或空操作；代码：continue
            continue
        # 中文说明：从生成器逐步产生本行指定的值；代码：yield data_dict_out
        yield data_dict_out


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Dataset:
class Dataset:
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：config: DatasetConfig,
        config: DatasetConfig,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：handler: Callable = reraise_exception,
        handler: Callable = reraise_exception,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Webdataloader class
        r"""Webdataloader class

        Args:
            config: Dataset config
            world_size: Total number of GPUs
        """
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.config = config
        self.config = config

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.world_size = get_world_size()
        self.world_size = get_world_size()

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset_info = config.dataset_info
        dataset_info = config.dataset_info
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.streaming_download = config.streaming_download
        self.streaming_download = config.streaming_download

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.data_keys = config.keys
        self.data_keys = config.keys

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Parse the metadata
        # Parse the metadata
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.wdinfo = Wdinfo([], 0, 0)
        self.wdinfo = Wdinfo([], 0, 0)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.parse_dataset_info(dataset_info=dataset_info)
        self.parse_dataset_info(dataset_info=dataset_info)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.handler = handler
        self.handler = handler
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.augmentors = dict()
        self.augmentors = dict()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def parse_dataset_info(self, dataset_info: list[DatasetInfo]):
    def parse_dataset_info(self, dataset_info: list[DatasetInfo]):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Parse metadata about the list of tar files.
        r"""Parse metadata about the list of tar files.

        Args:
            dataset_info (list): List of dictionaries containing paths to metadata files.
        """

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for dset_num, dset_info in enumerate(dataset_info):
        for dset_num, dset_info in enumerate(dataset_info):
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# For each dataset, we parse the file paths and store them as a list of TarSample.
            # For each dataset, we parse the file paths and store them as a list of TarSample.
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# TarSample will then be used by each worker to load the data.
            # TarSample will then be used by each worker to load the data.

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dset_id = "dset: {}".format(dset_num)
            dset_id = "dset: {}".format(dset_num)

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Read all wdinfo files and obtain the DataSample list
            # Read all wdinfo files and obtain the DataSample list
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for wdinfo_path in dset_info.wdinfo:
            for wdinfo_path in dset_info.wdinfo:
                # 中文说明：处理异常、清理资源或管理上下文；代码：with open(wdinfo_path, "rb") as fp:
                with open(wdinfo_path, "rb") as fp:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cur_dset_info = pickle.load(fp)
                    cur_dset_info = pickle.load(fp)

                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# No need for sample_keys_full_list since we removed object store functionality
                # No need for sample_keys_full_list since we removed object store functionality
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sample_keys_full_list_per_tar = [None] * len(cur_dset_info["data_list"])
                sample_keys_full_list_per_tar = [None] * len(cur_dset_info["data_list"])

                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_root = cur_dset_info["root"]
                data_root = cur_dset_info["root"]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tar_files_list = cur_dset_info["data_list"]
                tar_files_list = cur_dset_info["data_list"]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tar_files = [
                tar_files = [
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：TarSample(
                    TarSample(
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：path=tar_file,
                        path=tar_file,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：root=data_root,
                        root=data_root,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：keys=dset_info.per_dataset_keys
                        keys=dset_info.per_dataset_keys
                        # 中文说明：根据条件选择执行分支；代码：if dset_info.per_dataset_keys
                        if dset_info.per_dataset_keys
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：else self.data_keys, # use per dataset keys if available
                        else self.data_keys,  # use per dataset keys if available
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：meta=dset_info,
                        meta=dset_info,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dset_id=dset_id,
                        dset_id=dset_id,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sample_keys_full_list=sample_keys_full_list,
                        sample_keys_full_list=sample_keys_full_list,
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for tar_file, sample_keys_full_list in zip(
                    for tar_file, sample_keys_full_list in zip(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：tar_files_list, sample_keys_full_list_per_tar, strict=True
                        tar_files_list, sample_keys_full_list_per_tar, strict=True
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
                ]

                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Update the master winfo
                # Update the master winfo
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.wdinfo.tar_files.extend(tar_files)
                self.wdinfo.tar_files.extend(tar_files)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.wdinfo.total_key_count += cur_dset_info["total_key_count"]
                self.wdinfo.total_key_count += cur_dset_info["total_key_count"]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.wdinfo.chunk_size = cur_dset_info["chunk_size"]
                self.wdinfo.chunk_size = cur_dset_info["chunk_size"]

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# This is the function that calls each augmentor in sequence.
    # This is the function that calls each augmentor in sequence.
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def augmentor_fn(data, augmentations):
    def augmentor_fn(data, augmentations):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Build augmentor chain
        # Build augmentor chain
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for aug_fn in augmentations:
        for aug_fn in augmentations:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Use generator function as augmentor
            # Use generator function as augmentor
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# (recommended, allows skipping or replicating samples inside the augmentor)
            # (recommended, allows skipping or replicating samples inside the augmentor)
            # 中文说明：根据条件选择执行分支；代码：if getattr(aug_fn, "is_generator", False):
            if getattr(aug_fn, "is_generator", False):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data = aug_fn(data)
                data = aug_fn(data)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：else: # Use regular function as augmentor (backward compatibility)
            else:  # Use regular function as augmentor (backward compatibility)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data = wrap_augmentor_func_as_generator(aug_fn, data)
                data = wrap_augmentor_func_as_generator(aug_fn, data)
        # 中文说明：从生成器逐步产生本行指定的值；代码：yield from data
        yield from data

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def build_data_augmentor(self, augmentor_cfg: dict[str, AugmentorConfig]) -> Callable:
    def build_data_augmentor(self, augmentor_cfg: dict[str, AugmentorConfig]) -> Callable:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Function for building data augmentors from augmentor config."""
        r"""Function for building data augmentors from augmentor config."""
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：augmentations = []
        augmentations = []
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for aug in augmentor_cfg.keys():
        for aug in augmentor_cfg.keys():
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：augmentations.append(instantiate(augmentor_cfg[aug]))
            augmentations.append(instantiate(augmentor_cfg[aug]))

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# This is the function that calls each augmentor in sequence.
        # This is the function that calls each augmentor in sequence.
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return partial(Dataset.augmentor_fn, augmentations=augmentations)
        return partial(Dataset.augmentor_fn, augmentations=augmentations)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def build_dataset(self, **kwargs) -> WebDataset:
    def build_dataset(self, **kwargs) -> WebDataset:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tar_list = self.wdinfo.tar_files
        tar_list = self.wdinfo.tar_files
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_tars = len(tar_list)
        num_tars = len(tar_list)
        # 中文说明：检查运行时假设是否成立；代码：assert num_tars > 0, "Did not find any data."
        assert num_tars > 0, "Did not find any data."

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：shuffle_buffer_size = getattr(self.config, "buffer_size", self.wdinfo.chunk_size)
        shuffle_buffer_size = getattr(self.config, "buffer_size", self.wdinfo.chunk_size)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# update distributor urls and chunk size
        # update distributor urls and chunk size
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distributor_fn = self.config.distributor
        distributor_fn = self.config.distributor

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：distributor_fn.set_urls(tar_list)
        distributor_fn.set_urls(tar_list)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：distributor_fn.set_chunk_size(self.wdinfo.chunk_size)
        distributor_fn.set_chunk_size(self.wdinfo.chunk_size)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset = WebDataset(
        dataset = WebDataset(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：distributor_fn,
            distributor_fn,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：streaming_download=self.streaming_download,
            streaming_download=self.streaming_download,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：handler=self.handler,
            handler=self.handler,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Creating a shuffle buffer
        # Creating a shuffle buffer
        # 中文说明：根据条件选择执行分支；代码：if shuffle_buffer_size > 0:
        if shuffle_buffer_size > 0:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dataset.append(wds.shuffle(shuffle_buffer_size))
            dataset.append(wds.shuffle(shuffle_buffer_size))

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Adding decoders
        # Adding decoders
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Decoders are functions that decode the input IO stream
        # Decoders are functions that decode the input IO stream
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：decoder_list = getattr(self.config, "decoders", [])
        decoder_list = getattr(self.config, "decoders", [])
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：decoder_functions = []
        decoder_functions = []
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for decoder in decoder_list:
        for decoder in decoder_list:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# If the specified decoder is a string, use the webdataset decoder
            # If the specified decoder is a string, use the webdataset decoder
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# If its a callable function, use the defined function to decode data
            # If its a callable function, use the defined function to decode data
            # 中文说明：检查运行时假设是否成立；代码：assert isinstance(decoder, str) or callable(decoder), "Decoder should either be callable or a...
            assert isinstance(decoder, str) or callable(decoder), "Decoder should either be callable or a str"
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：decoder_functions.append(decoder)
            decoder_functions.append(decoder)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dataset.append(wds.decode(*decoder_functions))
        dataset.append(wds.decode(*decoder_functions))

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# After the decoders are added, remove extension from the keys
        # After the decoders are added, remove extension from the keys
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Extensions in the data keys are needed for auto-detection of decoders in webdataset.
        # Extensions in the data keys are needed for auto-detection of decoders in webdataset.
        # 中文说明：根据条件选择执行分支；代码：if self.config.remove_extension_from_keys:
        if self.config.remove_extension_from_keys:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dataset.append(remove_extensions_from_keys)
            dataset.append(remove_extensions_from_keys)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Function to skip keys
        # Function to skip keys
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dataset.append(skip_keys)
        dataset.append(skip_keys)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Building augmentors
        # Building augmentors
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：augmentor_cfg = getattr(self.config, "augmentation", None)
        augmentor_cfg = getattr(self.config, "augmentation", None)
        # 中文说明：检查运行时假设是否成立；代码：assert isinstance(
        assert isinstance(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：augmentor_cfg, (dict, omegaconf.dictconfig.DictConfig)
            augmentor_cfg, (dict, omegaconf.dictconfig.DictConfig)
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"getting type: {type(augmentor_cfg)}"
        ), f"getting type: {type(augmentor_cfg)}"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：augmentation_fn = self.build_data_augmentor(augmentor_cfg)
        augmentation_fn = self.build_data_augmentor(augmentor_cfg)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dataset.append(augmentation_fn)
        dataset.append(augmentation_fn)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Updates URL names so that the collate function can handle
        # Updates URL names so that the collate function can handle
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dataset.append(update_url)
        dataset.append(update_url)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset.total_images = self.wdinfo.total_key_count # type: ignore
        dataset.total_images = self.wdinfo.total_key_count  # type: ignore
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("Total number of training shards: %d" % num_tars)
        log.info("Total number of training shards: %d" % num_tars)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("Total training key count: %d" % dataset.total_images) # type: ignore
        log.info("Total training key count: %d" % dataset.total_images)  # type: ignore

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return dataset
        return dataset
