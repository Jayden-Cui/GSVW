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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import random
import random
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import time
import time
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from collections import defaultdict
from collections import defaultdict

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from webdataset.pytorch import IterableDataset
from webdataset.pytorch import IterableDataset
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from webdataset.utils import pytorch_worker_info
from webdataset.utils import pytorch_worker_info

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.datasets.webdataset.config.schema import TarSample
from imaginaire.datasets.webdataset.config.schema import TarSample
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ShardlistMultiAspectRatioInfinite(IterableDataset):
class ShardlistMultiAspectRatioInfinite(IterableDataset):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""
    r"""
    An iterable dataset that parses and yields tar files.
    This distributor handles the multi-aspect ratio case. For the dataloader to be successful,
    each worker should load only one aspect ratio. Else, there can be a batch where two
    aspect ratios would be present which would raise an error in collate function.
    So, we design data distribution strategy so that each worker sees only one aspect ratio.

    This version only supports infinite loader mode. This enables a simpler code that is faster to initialize
    and produces samples better matching the dataset distribution.
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
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：is_infinite_loader: bool = True,
        is_infinite_loader: bool = True,
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
            chunk_size (int): Ignored
            resume_flag (bool): Ignored
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
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("ShardlistMultiAspectRatioInfinite init")
            log.info("ShardlistMultiAspectRatioInfinite init")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.shuffle = shuffle
        self.shuffle = shuffle
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.split_by_node = split_by_node
        self.split_by_node = split_by_node
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.split_by_worker = split_by_worker
        self.split_by_worker = split_by_worker
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.chunk_size = chunk_size # Ignored
        self.chunk_size = chunk_size  # Ignored
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.resume_flag = resume_flag # Ignored
        self.resume_flag = resume_flag  # Ignored
        # 中文说明：检查运行时假设是否成立；代码：assert is_infinite_loader is True
        assert is_infinite_loader is True

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def set_urls(self, urls: list[TarSample]):
    def set_urls(self, urls: list[TarSample]):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.url_aspect_split = self._split_urls_by_aspect_ratio(urls)
        self.url_aspect_split = self._split_urls_by_aspect_ratio(urls)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def set_chunk_size(self, chunk_size: int):
    def set_chunk_size(self, chunk_size: int):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Set chunk size
        """Set chunk size
        For backward compatibility. Ignored.

        Args:
            chunk_size (int): chunk size used in webdataset creation
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.chunk_size = chunk_size
        self.chunk_size = chunk_size

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def set_epoch(self, epoch: int, start_index: int):
    def set_epoch(self, epoch: int, start_index: int):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Set the current epoch. Used for per-node shuffling.
        r"""Set the current epoch. Used for per-node shuffling.
        For backward compatibility. Ignored.

        Args:
            epoch (int): Epoch number
            start_index (int): iteraton number
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.epoch = epoch
        self.epoch = epoch
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.start_index = start_index
        self.start_index = start_index

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _split_urls_by_aspect_ratio(self, urls):
    def _split_urls_by_aspect_ratio(self, urls):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Function for splitting urls by aspect ratio.
        r"""Function for splitting urls by aspect ratio.
        We assume that urls are grouped by dataset_id. That is, data belonging to
        one dataset_id should have all data in the same aspect ratio.
        """

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：url_aspect_split = defaultdict(list)
        url_aspect_split = defaultdict(list)

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for url in urls:
        for url in urls:
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

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return url_aspect_split
        return url_aspect_split

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _allocate_workers_to_aspects(
    def _allocate_workers_to_aspects(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, url_aspect_split: dict[str, list[TarSample]], num_workers_all: int
        self, url_aspect_split: dict[str, list[TarSample]], num_workers_all: int
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> list[tuple[str, int]]:
    ) -> list[tuple[str, int]]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Allocate workers to each aspect ratio so that:
        r"""Allocate workers to each aspect ratio so that:
        1. Each aspect ratio has at least one worker
        2. All the workers have jobs to do

        Args:
            url_aspect_split (dict[list[TarSample]]): TarSample split by aspect ratio
            num_workers_all (int): Total number of dataloader workers

        Returns:
            aspect_worker_allocation (list): List of tuple containing (aspect_key, num_workers)
        """
        # 中文说明：根据条件选择执行分支；代码：if self.verbose:
        if self.verbose:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(
            log.info(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"#URLs for each aspect ratio: {[len(url_aspect_split[aspect_ratio]) for aspect_ratio in url_...
                f"#URLs for each aspect ratio: {[len(url_aspect_split[aspect_ratio]) for aspect_ratio in url_aspect_split]}"
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Must have more global workers than the number of aspect ratios, as each global worker can o...
        # Must have more global workers than the number of aspect ratios, as each global worker can only load a single
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# aspect ratio.
        # aspect ratio.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_aspects = len(url_aspect_split)
        num_aspects = len(url_aspect_split)
        # 中文说明：检查运行时假设是否成立；代码：assert num_workers_all >= num_aspects
        assert num_workers_all >= num_aspects

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：aspect_keys = list(url_aspect_split.keys())
        aspect_keys = list(url_aspect_split.keys())
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Allocate at least one worker per aspect ratios
        # Allocate at least one worker per aspect ratios
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：target_ratio = np.array([len(url_aspect_split[key]) for key in aspect_keys])
        target_ratio = np.array([len(url_aspect_split[key]) for key in aspect_keys])
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：target_ratio = target_ratio / target_ratio.sum()
        target_ratio = target_ratio / target_ratio.sum()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：aspect_worker_allocation = np.ones([num_aspects], dtype=np.int64)
        aspect_worker_allocation = np.ones([num_aspects], dtype=np.int64)
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _i in range(num_workers_all - num_aspects):
        for _i in range(num_workers_all - num_aspects):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：current_ratio = aspect_worker_allocation / aspect_worker_allocation.sum()
            current_ratio = aspect_worker_allocation / aspect_worker_allocation.sum()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：aspect_worker_allocation[np.argmin(current_ratio - target_ratio)] += 1
            aspect_worker_allocation[np.argmin(current_ratio - target_ratio)] += 1

        # 中文说明：根据条件选择执行分支；代码：if self.verbose:
        if self.verbose:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Aspects: {aspect_keys}")
            log.info(f"Aspects: {aspect_keys}")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Target ratio: {target_ratio}")
            log.info(f"Target ratio: {target_ratio}")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Worker allocation: {aspect_worker_allocation}")
            log.info(f"Worker allocation: {aspect_worker_allocation}")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Discrepancy: {aspect_worker_allocation / aspect_worker_allocation.sum() / target_r...
            log.info(f"Discrepancy: {aspect_worker_allocation / aspect_worker_allocation.sum() / target_ratio}")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return [(k, v) for k, v in zip(aspect_keys, aspect_worker_allocation.tolist())]
        return [(k, v) for k, v in zip(aspect_keys, aspect_worker_allocation.tolist())]

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _obtain_node_worker_url_mapping(
    def _obtain_node_worker_url_mapping(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：url_aspect_split: dict[str, list[TarSample]],
        url_aspect_split: dict[str, list[TarSample]],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：aspect_worker_allocation: list[tuple[str, int]],
        aspect_worker_allocation: list[tuple[str, int]],
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
            aspect_worker_allocation (dict): Number of workers allocated to each aspect ratio
            rank (int): Rank of the current GPU
            world_size (int): Total number of GPUs
            worker_id (int): ID for the current worker in the dataloader
            num_workers (int): Total number of workers in the dataloader

        Returns:
            URL list for the current worker
        """
        # 中文说明：检查运行时假设是否成立；代码：assert self.split_by_node is True and self.split_by_worker is True
        assert self.split_by_node is True and self.split_by_worker is True

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# First determine the aspect ratio for the current worker
        # First determine the aspect ratio for the current worker
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：global_worker_id = rank * num_workers + worker_id
        global_worker_id = rank * num_workers + worker_id

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cumulative = 0
        cumulative = 0
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for aspect_key, worker_count in aspect_worker_allocation:
        for aspect_key, worker_count in aspect_worker_allocation:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cumulative += worker_count
            cumulative += worker_count
            # 中文说明：根据条件选择执行分支；代码：if global_worker_id < cumulative:
            if global_worker_id < cumulative:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：chunk_id = global_worker_id - cumulative + worker_count
                chunk_id = global_worker_id - cumulative + worker_count
                # 中文说明：执行循环控制或空操作；代码：break
                break

        # 中文说明：根据条件选择执行分支；代码：if self.verbose:
        if self.verbose:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"GID={global_worker_id}, aspect_key={aspect_key}, chunk_id={chunk_id}")
            log.info(f"GID={global_worker_id}, aspect_key={aspect_key}, chunk_id={chunk_id}")
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# chunk the urls for the target aspect ratio
        # chunk the urls for the target aspect ratio
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：urls_asp = url_aspect_split[aspect_key]
        urls_asp = url_aspect_split[aspect_key]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：url_chunk = urls_asp[chunk_id::worker_count]
        url_chunk = urls_asp[chunk_id::worker_count]

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return url_chunk
        return url_chunk

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def obtain_url_list(self):
    def obtain_url_list(self):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Return an iterator over the shards."""
        r"""Return an iterator over the shards."""

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rank, world_size, worker_id, num_workers = pytorch_worker_info()
        rank, world_size, worker_id, num_workers = pytorch_worker_info()

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

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Assigning workers to process each aspect ratio
        # Assigning workers to process each aspect ratio
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：aspect_worker_allocation = self._allocate_workers_to_aspects(self.url_aspect_split, nworkers_...
        aspect_worker_allocation = self._allocate_workers_to_aspects(self.url_aspect_split, nworkers_all)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Form a mapping of url_aspect_split to node and workers
        # Form a mapping of url_aspect_split to node and workers
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：urls = self._obtain_node_worker_url_mapping(
        urls = self._obtain_node_worker_url_mapping(
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.url_aspect_split, aspect_worker_allocation, rank, world_size, worker_id, num_workers
            self.url_aspect_split, aspect_worker_allocation, rank, world_size, worker_id, num_workers
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
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：global_worker_id = rank * num_workers + worker_id
            global_worker_id = rank * num_workers + worker_id
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：random.Random(global_worker_id).shuffle(urls)
            random.Random(global_worker_id).shuffle(urls)

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
