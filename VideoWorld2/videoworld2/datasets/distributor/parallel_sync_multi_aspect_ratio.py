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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import random
import random
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import time
import time
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from copy import deepcopy
from copy import deepcopy

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch

# 中文说明：开始一个可捕获异常的代码块；代码：try:
try:
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from megatron.core import parallel_state
    from megatron.core import parallel_state

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：USE_MEGATRON = True
    USE_MEGATRON = True
# 中文说明：处理异常、清理资源或管理上下文；代码：except ImportError:
except ImportError:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：USE_MEGATRON = False
    USE_MEGATRON = False
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from webdataset.utils import pytorch_worker_info
from webdataset.utils import pytorch_worker_info

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.datasets.webdataset.config.schema import TarSample
from imaginaire.datasets.webdataset.config.schema import TarSample
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.datasets.webdataset.distributors.multi_aspect_ratio import ShardlistMultiAspe...
from imaginaire.datasets.webdataset.distributors.multi_aspect_ratio import ShardlistMultiAspectRatio
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ShardlistMultiAspectRatioParallelSync(ShardlistMultiAspectRatio):
class ShardlistMultiAspectRatioParallelSync(ShardlistMultiAspectRatio):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""
    r"""
    An iterable dataset that parses and yields tar files.
    This distributor is based on ShardlistMultiAspectRatio.
    Additionally, it allows users to synchronize inputs for context/tensor parallelism. This is achieved by specifying the context/tensor parallel group size during initialization.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, **kwargs):
    def __init__(self, **kwargs):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Create a multi-aspect ratio ShardList."""
        r"""Create a multi-aspect ratio ShardList."""
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(**kwargs)
        super().__init__(**kwargs)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.enable_parallel()
        self.enable_parallel()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _obtain_node_worker_url_mapping(
    def _obtain_node_worker_url_mapping(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：url_aspect_split: dict[str, list[TarSample]],
        url_aspect_split: dict[str, list[TarSample]],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_urls_per_worker: int,
        num_urls_per_worker: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group_id: int,
        group_id: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group_num: int,
        group_num: int,
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
            group_id (int): Rank of the current GPU
            group_num (int): Total number of groups
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
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：chunk_mappings = chunk_mappings[group_id::group_num]
        chunk_mappings = chunk_mappings[group_id::group_num]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：chunk_mappings = chunk_mappings[worker_id::num_workers]
        chunk_mappings = chunk_mappings[worker_id::num_workers]

        # 中文说明：检查运行时假设是否成立；代码：assert len(chunk_mappings) == 1, f"Length of chunk_mappings {len(chunk_mappings)} != 1"
        assert len(chunk_mappings) == 1, f"Length of chunk_mappings {len(chunk_mappings)} != 1"
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return chunk_mappings[0][1]
        return chunk_mappings[0][1]

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def enable_parallel(self):
    def enable_parallel(self):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Ranks of the same pp/tp/cp group will have the same dp rank and thus share the same group id.
        # Ranks of the same pp/tp/cp group will have the same dp rank and thus share the same group id.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.group_id = parallel_state.get_data_parallel_rank()
        self.group_id = parallel_state.get_data_parallel_rank()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# The size of the group is how many GPUs we use to process one batch of data.
        # The size of the group is how many GPUs we use to process one batch of data.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.group_size = torch.distributed.get_world_size() // parallel_state.get_data_parallel_worl...
        self.group_size = torch.distributed.get_world_size() // parallel_state.get_data_parallel_world_size()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def obtain_url_list(self):
    def obtain_url_list(self):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Return an iterator over the shards."""
        r"""Return an iterator over the shards."""

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rank, world_size, worker_id, num_workers = pytorch_worker_info()
        rank, world_size, worker_id, num_workers = pytorch_worker_info()

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups = world_size // self.group_size
        num_groups = world_size // self.group_size
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

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：url_aspect_split = deepcopy(self.url_aspect_split)
        url_aspect_split = deepcopy(self.url_aspect_split)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# nworkers_all is no longer world_size * num_workers, since self.group_size workers duplicate
        # nworkers_all is no longer world_size * num_workers, since self.group_size workers duplicate
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：nworkers_all = num_groups * num_workers
        nworkers_all = num_groups * num_workers

        # 中文说明：根据条件选择执行分支；代码：if self.verbose:
        if self.verbose:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Total {nworkers_all} workers are in effect")
            log.info(f"Total {nworkers_all} workers are in effect")

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Perform DDP equalization
        # Perform DDP equalization
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：url_aspect_split, num_urls_per_worker = self._ddp_equalize(url_aspect_split, nworkers_all)
        url_aspect_split, num_urls_per_worker = self._ddp_equalize(url_aspect_split, nworkers_all)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Form a mapping of url_aspect_split to node and workers
        # Form a mapping of url_aspect_split to node and workers
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：urls = self._obtain_node_worker_url_mapping(
        urls = self._obtain_node_worker_url_mapping(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：url_aspect_split, num_urls_per_worker, self.group_id, num_groups, worker_id, num_workers
            url_aspect_split, num_urls_per_worker, self.group_id, num_groups, worker_id, num_workers
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：根据条件选择执行分支；代码：if self.shuffle:
        if self.shuffle:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：random.Random(self.group_id).shuffle(urls)
            random.Random(self.group_id).shuffle(urls)

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
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(
            log.info(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Rank {rank}, group {self.group_id}, worker {worker_id} of {num_workers}, group_size {self.g...
                f"Rank {rank}, group {self.group_id}, worker {worker_id} of {num_workers}, group_size {self.group_size} got {len(urls)} urls, first five are {urls[:5]}"
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

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
