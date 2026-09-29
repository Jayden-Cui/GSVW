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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Callable, Optional
from typing import Callable, Optional

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import omegaconf
import omegaconf
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import webdataset as wds
import webdataset as wds
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from webdataset import filters
from webdataset import filters
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from webdataset.handlers import reraise_exception
from webdataset.handlers import reraise_exception

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.datasets.webdataset.config.schema import DatasetConfig
from imaginaire.datasets.webdataset.config.schema import DatasetConfig
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.datasets.webdataset.utils.iterators import WebDataset
from imaginaire.datasets.webdataset.utils.iterators import WebDataset
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.datasets.webdataset.utils.misc import remove_extensions_from_keys, skip_keys,...
from imaginaire.datasets.webdataset.utils.misc import remove_extensions_from_keys, skip_keys, update_url
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.datasets.webdataset.webdataset import Dataset as BaseDataset
from imaginaire.datasets.webdataset.webdataset import Dataset as BaseDataset
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Dataset(BaseDataset):
class Dataset(BaseDataset):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：config: DatasetConfig,
        config: DatasetConfig,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：handler: Callable = reraise_exception,
        handler: Callable = reraise_exception,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：decoder_handler: Optional[Callable] = None,
        decoder_handler: Optional[Callable] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：detshuffle: bool = False,
        detshuffle: bool = False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Webdataloader class
        r"""Webdataloader class

        Args:
            config: Dataset config
            handler (Callable): Error handler for webdataset class
            decoder_handler (Callable): Error handler during decoding
        """
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(config=config, handler=handler)
        super().__init__(config=config, handler=handler)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.decoder_handler = decoder_handler
        self.decoder_handler = decoder_handler
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.detshuffle = detshuffle
        self.detshuffle = detshuffle

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def build_dataset(self, **kwargs) -> WebDataset:
    def build_dataset(self, **kwargs) -> WebDataset:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""
        r"""
        Build the dataset object.
        The function only diffs from BaseDataset.build_dataset by only adding the decoder_handler to the WebDataset object.
        """
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
        # 中文说明：根据条件选择执行分支；代码：if self.detshuffle:
        if self.detshuffle:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dataset.append(filters.detshuffle(shuffle_buffer_size))
            dataset.append(filters.detshuffle(shuffle_buffer_size))
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
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
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dataset.append(wds.decode(*decoder_functions, handler=self.decoder_handler))
        dataset.append(wds.decode(*decoder_functions, handler=self.decoder_handler))

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
