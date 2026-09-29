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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import math
import math
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import random
import random
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import time
import time
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from collections import defaultdict
from collections import defaultdict
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from copy import deepcopy
from copy import deepcopy

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from webdataset.pytorch import IterableDataset
from webdataset.pytorch import IterableDataset
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from webdataset.utils import pytorch_worker_info
from webdataset.utils import pytorch_worker_info

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.datasets.webdataset.config.schema import TarSample
from imaginaire.datasets.webdataset.config.schema import TarSample
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.datasets.webdataset.utils.misc import repeat_list
from imaginaire.datasets.webdataset.utils.misc import repeat_list
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ShardlistMultiAspectRatio(IterableDataset):
class ShardlistMultiAspectRatio(IterableDataset):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""
    r"""
    An iterable dataset that parses and yields tar files.
    This distributor handles the multi-aspect ratio case. For the dataloader to be successful,
    each worker should load only one aspect ratio. Else, there can be a batch where two
    aspect ratios would be present which would raise an error in collate function.
    So, we design data distribution strategy so that each worker sees only one aspect ratio.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：shuffle: bool = True,
        shuffle: bool = True,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：split_by_node: bool = True,
        split_by_node: bool = True,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：split_by_worker: bool = True,
        split_by_worker: bool = True,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：chunk_size: int = 1,
        chunk_size: int = 1,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：resume_flag: bool = True,
        resume_flag: bool = True,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：verbose: bool = False,
        verbose: bool = False,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：is_infinite_loader: bool = False,
        is_infinite_loader: bool = False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Create a multi-aspect ratio ShardList.
        r"""Create a multi-aspect ratio ShardList.
        Args:
            urls (list[TarSample]): a list of tar files along with their metadata
            epoch_shuffle (bool): Shuffles the whole epoch. If disabled, each node will see the same set of urls.
            shuffle (bool): shuffle samples before iterating.
            split_by_node (bool): split shards by node if True
            split_by_worker (bool): split shards by worker if True
            chunk_size (int): chunk size used in webdataset creation
            resume_flag (bool): If enabled, resumes from a specific iteration and epoch number.
            verbose (bool): Prints some logs if true
            is_infinite_loader (bool): If true, creates an infinite dataloader.
                So, the dataset will be only one epoch and will not terminate.
        """
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.verbose = verbose
        self.verbose = verbose
        # 中文说明：根据条件选择执行分支；代码：if self.verbose:
        if self.verbose:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("ShardListWithResumes init")
            log.info("ShardListWithResumes init")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.epoch = 0
        self.epoch = 0
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.start_index = 0
        self.start_index = 0
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.shuffle = shuffle
        self.shuffle = shuffle
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.split_by_node = split_by_node
        self.split_by_node = split_by_node
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.split_by_worker = split_by_worker
        self.split_by_worker = split_by_worker
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.chunk_size = chunk_size
        self.chunk_size = chunk_size
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.resume_flag = resume_flag
        self.resume_flag = resume_flag
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.is_infinite_loader = is_infinite_loader
        self.is_infinite_loader = is_infinite_loader

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def set_urls(self, urls: list[TarSample]):
    def set_urls(self, urls: list[TarSample]):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.urls = urls
        self.urls = urls
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._split_urls_by_aspect_ratio()
        self._split_urls_by_aspect_ratio()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def set_chunk_size(self, chunk_size: int):
    def set_chunk_size(self, chunk_size: int):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Set chunk size
        """Set chunk size

        Args:
            chunk_size (int): chunk size used in webdataset creation
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.chunk_size = chunk_size
        self.chunk_size = chunk_size

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def set_epoch(self, epoch: int, start_index: int):
    def set_epoch(self, epoch: int, start_index: int):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Set the current epoch. Used for per-node shuffling.
        r"""Set the current epoch. Used for per-node shuffling.
        Args:
            epoch (int): Epoch number
            start_index (int): iteraton number
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.epoch = epoch
        self.epoch = epoch
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.start_index = start_index
        self.start_index = start_index

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _split_urls_by_aspect_ratio(self):
    def _split_urls_by_aspect_ratio(self):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Function for splitting urls by aspect ratio.
        r"""Function for splitting urls by aspect ratio.
        We assume that urls are grouped by dataset_id. That is, data belonging to
        one dataset_id should have all data in the same aspect ratio.
        """

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：url_aspect_split = defaultdict(list)
        url_aspect_split = defaultdict(list)

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for url in self.urls:
        for url in self.urls:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dset_info = url.meta
            dset_info = url.meta
            # 中文说明：根据条件选择执行分支；代码：if "aspect_ratio" not in dset_info.opts:
            if "aspect_ratio" not in dset_info.opts:
                # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError("aspect_ratio should be specified in dataset_info when using multi aspect di...
                raise ValueError("aspect_ratio should be specified in dataset_info when using multi aspect distributor")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：aspect_ratio = dset_info.opts["aspect_ratio"]
            aspect_ratio = dset_info.opts["aspect_ratio"]
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：url_aspect_split[aspect_ratio].append(url)
            url_aspect_split[aspect_ratio].append(url)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：aspect_ratio_with_most_elems = -1
        aspect_ratio_with_most_elems = -1
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：aspect_ratio_with_least_elems = -1
        aspect_ratio_with_least_elems = -1
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_aspect_ratio_count = -1
        max_aspect_ratio_count = -1
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_aspect_ratio_count = 1000000000
        min_aspect_ratio_count = 1000000000

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for aspect_ratio in url_aspect_split:
        for aspect_ratio in url_aspect_split:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Sort the url list
            # Sort the url list
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：url_aspect_split[aspect_ratio] = sorted(
            url_aspect_split[aspect_ratio] = sorted(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：url_aspect_split[aspect_ratio], key=lambda tar: (tar.path, tar.root)
                url_aspect_split[aspect_ratio], key=lambda tar: (tar.path, tar.root)
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Finding max and min tar counts per aspect ratio
            # Finding max and min tar counts per aspect ratio
            # 中文说明：根据条件选择执行分支；代码：if len(url_aspect_split[aspect_ratio]) > max_aspect_ratio_count:
            if len(url_aspect_split[aspect_ratio]) > max_aspect_ratio_count:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：aspect_ratio_with_most_elems = aspect_ratio
                aspect_ratio_with_most_elems = aspect_ratio
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_aspect_ratio_count = len(url_aspect_split[aspect_ratio])
                max_aspect_ratio_count = len(url_aspect_split[aspect_ratio])
            # 中文说明：根据条件选择执行分支；代码：if len(url_aspect_split[aspect_ratio]) < min_aspect_ratio_count:
            if len(url_aspect_split[aspect_ratio]) < min_aspect_ratio_count:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：aspect_ratio_with_least_elems = aspect_ratio
                aspect_ratio_with_least_elems = aspect_ratio
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_aspect_ratio_count = len(url_aspect_split[aspect_ratio])
                min_aspect_ratio_count = len(url_aspect_split[aspect_ratio])

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.url_aspect_split = url_aspect_split
        self.url_aspect_split = url_aspect_split
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.aspect_ratio_with_most_elems = aspect_ratio_with_most_elems
        self.aspect_ratio_with_most_elems = aspect_ratio_with_most_elems
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.aspect_ratio_with_least_elems = aspect_ratio_with_least_elems
        self.aspect_ratio_with_least_elems = aspect_ratio_with_least_elems

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _ddp_equalize(
    def _ddp_equalize(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, url_aspect_split: dict[str, list[TarSample]], nworkers_all: int
        self, url_aspect_split: dict[str, list[TarSample]], nworkers_all: int
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> tuple[dict[str, list[TarSample]], int]:
    ) -> tuple[dict[str, list[TarSample]], int]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""This function performs tar file equalization. That is, we repeat the number of tars in ea...
        r"""This function performs tar file equalization. That is, we repeat the number of tars in each aspect
        ratio so that when the tars are split across workers, each worker recieves the same number of tars.
        This function is important for ddp to terminate well at the end of each epoch.

        Args:
            url_aspect_split (dict[list[TarSample]]): TarSample split by aspect ratio
            nworkers_all (int): Total number of dataloader workers

        Returns:
            url_aspect_split (dict[list[TarSample]]): TarSample split after DDP equalization
            num_urls_per_worker (int): Number of tars in each worker
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：betas = []
        betas = []
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_total = sum([len(url_aspect_split[aspect_ratio]) for aspect_ratio in url_aspect_split])
        n_total = sum([len(url_aspect_split[aspect_ratio]) for aspect_ratio in url_aspect_split])

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Initial assignment
        # Initial assignment
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：aspect_ind_with_most_elems = 0
        aspect_ind_with_most_elems = 0
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i, aspect_ratio in enumerate(url_aspect_split):
        for i, aspect_ratio in enumerate(url_aspect_split):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：betas.append(math.ceil((len(url_aspect_split[aspect_ratio]) / n_total) * nworkers_all))
            betas.append(math.ceil((len(url_aspect_split[aspect_ratio]) / n_total) * nworkers_all))
            # 中文说明：根据条件选择执行分支；代码：if aspect_ratio == self.aspect_ratio_with_most_elems:
            if aspect_ratio == self.aspect_ratio_with_most_elems:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：aspect_ind_with_most_elems = i
                aspect_ind_with_most_elems = i

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Constraint that total number of workers is fixed
        # Constraint that total number of workers is fixed
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：betas[aspect_ind_with_most_elems] += nworkers_all - sum(betas)
        betas[aspect_ind_with_most_elems] += nworkers_all - sum(betas)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Rebalance the number of urls
        # Rebalance the number of urls
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_urls_per_worker = math.ceil(n_total / sum(betas))
        num_urls_per_worker = math.ceil(n_total / sum(betas))
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i, aspect_ratio in enumerate(url_aspect_split):
        for i, aspect_ratio in enumerate(url_aspect_split):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：url_aspect_split[aspect_ratio] = repeat_list(url_aspect_split[aspect_ratio], betas[i] * num_u...
            url_aspect_split[aspect_ratio] = repeat_list(url_aspect_split[aspect_ratio], betas[i] * num_urls_per_worker)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return url_aspect_split, num_urls_per_worker
        return url_aspect_split, num_urls_per_worker

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _obtain_node_worker_url_mapping(
    def _obtain_node_worker_url_mapping(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：url_aspect_split: dict[str, list[TarSample]],
        url_aspect_split: dict[str, list[TarSample]],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_urls_per_worker: int,
        num_urls_per_worker: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rank: int,
        rank: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：world_size: int,
        world_size: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：worker_id: int,
        worker_id: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_workers: int,
        num_workers: int,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""This function obtains the worker-URL mapping. It assigns the tar list seen by
        r"""This function obtains the worker-URL mapping. It assigns the tar list seen by
        each workers.

        Args:
            url_aspect_split (dict[list[TarSample]]: TarSample split by aspect ratio
            num_urls_per_worker (int): Number of tar files seen by each worker
            rank (int): Rank of the current GPU
            world_size (int): Total number of GPUs
            worker_id (int): ID for the current worker in the dataloader
            num_workers (int): Total number of workers in the dataloader

        Returns:
            URL list for the current worker
        """
        # 中文说明：检查运行时假设是否成立；代码：assert self.split_by_node is True and self.split_by_worker is True
        assert self.split_by_node is True and self.split_by_worker is True

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# First chunk the tars
        # First chunk the tars
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：chunk_mappings = []
        chunk_mappings = []
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for aspect_ratio in url_aspect_split:
        for aspect_ratio in url_aspect_split:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：samples_asp = url_aspect_split[aspect_ratio]
            samples_asp = url_aspect_split[aspect_ratio]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：nchunks_asp = int(len(samples_asp) / num_urls_per_worker)
            nchunks_asp = int(len(samples_asp) / num_urls_per_worker)
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for chunk_id in range(nchunks_asp):
            for chunk_id in range(nchunks_asp):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：chunk_mappings.append((aspect_ratio, samples_asp[chunk_id::nchunks_asp]))
                chunk_mappings.append((aspect_ratio, samples_asp[chunk_id::nchunks_asp]))

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Split by rank and workers
        # Split by rank and workers
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：chunk_mappings = chunk_mappings[rank::world_size]
        chunk_mappings = chunk_mappings[rank::world_size]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：chunk_mappings = chunk_mappings[worker_id::num_workers]
        chunk_mappings = chunk_mappings[worker_id::num_workers]

        # 中文说明：检查运行时假设是否成立；代码：assert len(chunk_mappings) == 1
        assert len(chunk_mappings) == 1
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return chunk_mappings[0][1]
        return chunk_mappings[0][1]

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def obtain_url_list(self):
    def obtain_url_list(self):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Return an iterator over the shards."""
        r"""Return an iterator over the shards."""

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rank, world_size, worker_id, num_workers = pytorch_worker_info()
        rank, world_size, worker_id, num_workers = pytorch_worker_info()

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Setting epoch and start index
        # Setting epoch and start index
        # 中文说明：根据条件选择执行分支；代码：if self.resume_flag:
        if self.resume_flag:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.epoch = int(os.environ.get("WDS_EPOCH_NUM", 0))
            self.epoch = int(os.environ.get("WDS_EPOCH_NUM", 0))

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# This tells us number of chunks that have been seen by one GPU
            # This tells us number of chunks that have been seen by one GPU
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.start_index = int(os.environ.get("WDS_START_INDEX", 0)) // self.chunk_size
            self.start_index = int(os.environ.get("WDS_START_INDEX", 0)) // self.chunk_size

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：urls = deepcopy(self.urls)
        urls = deepcopy(self.urls)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：url_aspect_split = deepcopy(self.url_aspect_split)
        url_aspect_split = deepcopy(self.url_aspect_split)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Splitting the shards by worker and node
        # Splitting the shards by worker and node
        # 中文说明：根据条件选择执行分支；代码：if self.verbose:
        if self.verbose:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"PytorchShardList rank {rank} of {world_size}")
            log.info(f"PytorchShardList rank {rank} of {world_size}")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"PytorchShardList worker {worker_id} of {num_workers}")
            log.info(f"PytorchShardList worker {worker_id} of {num_workers}")

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：nworkers_all = world_size * num_workers
        nworkers_all = world_size * num_workers

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Perform DDP equalization
        # Perform DDP equalization
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：url_aspect_split, num_urls_per_worker = self._ddp_equalize(url_aspect_split, nworkers_all)
        url_aspect_split, num_urls_per_worker = self._ddp_equalize(url_aspect_split, nworkers_all)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Form a mapping of url_aspect_split to node and workers
        # Form a mapping of url_aspect_split to node and workers
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：urls = self._obtain_node_worker_url_mapping(
        urls = self._obtain_node_worker_url_mapping(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：url_aspect_split, num_urls_per_worker, rank, world_size, worker_id, num_workers
            url_aspect_split, num_urls_per_worker, rank, world_size, worker_id, num_workers
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：根据条件选择执行分支；代码：if self.verbose:
        if self.verbose:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("List of urls (before shuffle)")
            log.info("List of urls (before shuffle)")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(urls[0:10])
            log.info(urls[0:10])

        # 中文说明：根据条件选择执行分支；代码：if self.shuffle:
        if self.shuffle:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：random.Random(rank * world_size + worker_id * num_workers).shuffle(urls)
            random.Random(rank * world_size + worker_id * num_workers).shuffle(urls)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# This tells us the number of chunks seen by one worker.
        # This tells us the number of chunks seen by one worker.
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Do not iterate over the seen chunks.
        # Do not iterate over the seen chunks.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：start_index_per_worker = self.start_index // num_workers
        start_index_per_worker = self.start_index // num_workers
        # 中文说明：根据条件选择执行分支；代码：if not self.is_infinite_loader:
        if not self.is_infinite_loader:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：urls = urls[start_index_per_worker:]
            urls = urls[start_index_per_worker:]

        # 中文说明：根据条件选择执行分支；代码：if self.verbose:
        if self.verbose:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("List of urls (after shuffle)")
            log.info("List of urls (after shuffle)")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(urls[0:10])
            log.info(urls[0:10])
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"PytorchShardList got {len(urls)} urls")
            log.info(f"PytorchShardList got {len(urls)} urls")

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return urls
        return urls

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __iter__(self):
    def __iter__(self):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：url_list = self.obtain_url_list()
        url_list = self.obtain_url_list()

        # 中文说明：根据条件选择执行分支；代码：if self.is_infinite_loader:
        if self.is_infinite_loader:
            # 中文说明：在条件成立时重复执行循环体；代码：while True:
            while True:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cur_time = time.time_ns()
                cur_time = time.time_ns()
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：random.Random(cur_time).shuffle(url_list)
                random.Random(cur_time).shuffle(url_list)
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for url in url_list:
                for url in url_list:
                    # 中文说明：从生成器逐步产生本行指定的值；代码：yield dict(url=url)
                    yield dict(url=url)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for url in url_list:
            for url in url_list:
                # 中文说明：从生成器逐步产生本行指定的值；代码：yield dict(url=url)
                yield dict(url=url)
