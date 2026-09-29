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


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ShardlistBasic(IterableDataset):
class ShardlistBasic(IterableDataset):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""
    r"""
    An iterable dataset that parses and yields tar files.
    The dataset restored from an iteration number and index number.
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
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：resume_flag: bool = True,
        resume_flag: bool = True,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：verbose: bool = False,
        verbose: bool = False,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：is_infinite_loader: bool = False,
        is_infinite_loader: bool = False,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_epochs: int = 100000,
        max_epochs: int = 100000,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：repeat_url: bool = True,
        repeat_url: bool = True,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Create a ShardList.
        r"""Create a ShardList.
        Args:
            shuffle (bool): shuffle samples before iterating.
            split_by_node (bool): split shards by node if True
            split_by_worker (bool): split shards by worker if True
            resume_flag (bool): If enabled, resumes from a specific iteration and epoch number.
            verbose (bool): Prints some logs if true
            is_infinite_loader (bool): If true, creates an infinite dataloader.
                So, the dataset will be only one epoch and will not terminate.
            max_epochs (int): Infinite dataloader is created with max_epochs number of epochs.
                Should be a very large number.
            repeat_url (bool): If true, each worker will receive the same number of batches by repeating urls.
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
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.resume_flag = resume_flag
        self.resume_flag = resume_flag
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.is_infinite_loader = is_infinite_loader
        self.is_infinite_loader = is_infinite_loader
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.max_epochs = max_epochs
        self.max_epochs = max_epochs
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.repeat_url = repeat_url
        self.repeat_url = repeat_url

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def set_urls(self, urls: list[TarSample]):
    def set_urls(self, urls: list[TarSample]):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Set urls
        """Set urls

        Args:
            urls (list[TarSample]): a list of tar files along with their metadata
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.urls = urls
        self.urls = urls

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

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：urls = self.urls
        urls = self.urls
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_urls = len(urls)
        num_urls = len(urls)

        # 中文说明：根据条件选择执行分支；代码：if self.repeat_url:
        if self.repeat_url:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Extending urls so that each workers receive the same number of batches.
            # Extending urls so that each workers receive the same number of batches.
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# This serves the job of ddp_equalize.
            # This serves the job of ddp_equalize.
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：nworkers_all = world_size * num_workers
            nworkers_all = world_size * num_workers
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_urls_per_process = (num_urls + nworkers_all - 1) // nworkers_all
            num_urls_per_process = (num_urls + nworkers_all - 1) // nworkers_all
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extended_url_list_size = num_urls_per_process * nworkers_all
            extended_url_list_size = num_urls_per_process * nworkers_all
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：urls = repeat_list(urls, extended_url_list_size)
            urls = repeat_list(urls, extended_url_list_size)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Splits the urls by node and worker id. This ensures each worker sees different urls.
        # Splits the urls by node and worker id. This ensures each worker sees different urls.
        # 中文说明：根据条件选择执行分支；代码：if self.split_by_node:
        if self.split_by_node:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：urls = urls[rank::world_size]
            urls = urls[rank::world_size]
        # 中文说明：根据条件选择执行分支；代码：if self.split_by_worker:
        if self.split_by_worker:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：urls = urls[worker_id::num_workers]
            urls = urls[worker_id::num_workers]

        # 中文说明：根据条件选择执行分支；代码：if self.verbose:
        if self.verbose:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("List of urls (before shuffle)")
            log.info("List of urls (before shuffle)")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(urls[0:10])
            log.info(urls[0:10])

        # 中文说明：根据条件选择执行分支；代码：if self.shuffle:
        if self.shuffle:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Shuffle based on the world worker id.
            # Shuffle based on the world worker id.
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
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _ in range(self.max_epochs):
            for _ in range(self.max_epochs):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cur_time = int(time.time())
                cur_time = int(time.time())
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
