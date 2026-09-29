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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import io
import io
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import random
import random
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import sys
import sys
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import time
import time
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import IO, Any, BinaryIO, Callable, Dict, Iterable, Iterator, Optional, Tuple, Union
from typing import IO, Any, BinaryIO, Callable, Dict, Iterable, Iterator, Optional, Tuple, Union
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from urllib.parse import urlparse
from urllib.parse import urlparse

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import pandas as pd
import pandas as pd
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import webdataset.gopen as gopen_webdata
import webdataset.gopen as gopen_webdata
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import yaml
import yaml
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from webdataset import cache, filters, shardlists
from webdataset import cache, filters, shardlists
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from webdataset.compat import FluidInterface
from webdataset.compat import FluidInterface
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from webdataset.handlers import reraise_exception
from webdataset.handlers import reraise_exception
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from webdataset.pipeline import DataPipeline
from webdataset.pipeline import DataPipeline
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from webdataset.pytorch import IterableDataset
from webdataset.pytorch import IterableDataset
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from webdataset.tariterators import group_by_keys, tar_file_iterator
from webdataset.tariterators import group_by_keys, tar_file_iterator

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.datasets.webdataset.config.schema import TarSample
from imaginaire.datasets.webdataset.config.schema import TarSample
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def gopen(url: Union[Tuple, str], mode: str = "rb", bufsize: int = 8192, **kw) -> Union[io.By...
def gopen(url: Union[Tuple, str], mode: str = "rb", bufsize: int = 8192, **kw) -> Union[io.BytesIO, BinaryIO, IO]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Open the URL.
    r"""Open the URL.
    This uses the `gopen_schemes` dispatch table to dispatch based
    on scheme.
    Support for the following schemes is built-in: pipe, file,
    http, https, sftp, ftps, scp.
    When no scheme is given the url is treated as a file.
    You can use the OPEN_VERBOSE argument to get info about
    files being opened.
    Args:
        url (list[str]): the source URL
        mode (str): the mode ("rb", "r")
        bufsize (int): the buffer size
    Returns:
        Byte streams
    """
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：global fallback_gopen
    global fallback_gopen
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：verbose = int(os.environ.get("GOPEN_VERBOSE", 0))
    verbose = int(os.environ.get("GOPEN_VERBOSE", 0))
    # 中文说明：根据条件选择执行分支；代码：if verbose:
    if verbose:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("GOPEN", url, gopen_webdata.info, file=sys.stderr)
        log.info("GOPEN", url, gopen_webdata.info, file=sys.stderr)

    # 中文说明：检查运行时假设是否成立；代码：assert mode in ["rb", "wb"], mode
    assert mode in ["rb", "wb"], mode
    # 中文说明：根据条件选择执行分支；代码：if url == "-":
    if url == "-":
        # 中文说明：根据条件选择执行分支；代码：if mode == "rb":
        if mode == "rb":
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return sys.stdin.buffer
            return sys.stdin.buffer
        # 中文说明：根据条件选择执行分支；代码：elif mode == "wb":
        elif mode == "wb":
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return sys.stdout.buffer
            return sys.stdout.buffer
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"unknown mode {mode}")
            raise ValueError(f"unknown mode {mode}")

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# For all other gopen schemes, use the native webdataset gopen functions.
    # For all other gopen schemes, use the native webdataset gopen functions.
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# pr = gopen_webdata.urlparse(url)
    # pr = gopen_webdata.urlparse(url)
    # 中文说明：检查运行时假设是否成立；代码：assert isinstance(url, str)
    assert isinstance(url, str)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pr = urlparse(url)
    pr = urlparse(url)
    # 中文说明：根据条件选择执行分支；代码：if pr.scheme == "":
    if pr.scheme == "":
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：bufsize = int(os.environ.get("GOPEN_BUFFER", -1))
        bufsize = int(os.environ.get("GOPEN_BUFFER", -1))
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return open(url, mode, buffering=bufsize)
        return open(url, mode, buffering=bufsize)
    # 中文说明：根据条件选择执行分支；代码：if pr.scheme == "file":
    if pr.scheme == "file":
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：bufsize = int(os.environ.get("GOPEN_BUFFER", -1))
        bufsize = int(os.environ.get("GOPEN_BUFFER", -1))
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return open(pr.path, mode, buffering=bufsize)
        return open(pr.path, mode, buffering=bufsize)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：handler = gopen_webdata.gopen_schemes["__default__"]
    handler = gopen_webdata.gopen_schemes["__default__"]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：handler = gopen_webdata.gopen_schemes.get(pr.scheme, handler)
    handler = gopen_webdata.gopen_schemes.get(pr.scheme, handler)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return handler(url, mode, bufsize, **kw) # type: ignore
    return handler(url, mode, bufsize, **kw)  # type: ignore


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def url_opener(data: Iterable, handler: Callable = reraise_exception, **kw) -> Iterator[dict]:
def url_opener(data: Iterable, handler: Callable = reraise_exception, **kw) -> Iterator[dict]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Given a stream of url names (packaged in `dict(url=url)`), yield opened streams.
    r"""Given a stream of url names (packaged in `dict(url=url)`), yield opened streams.

    Args:
        data (Iterable): Iterator of dictionaires containing url paths.
        handler (Callable): Exception handler.

    Yields:
      Dictionaries with this structure:
        {"url": ...
         "stream": list[Union[io.BytesIO, RetryingStream]]}
    """
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for sample in data:
    for sample in data:
        # 中文说明：检查运行时假设是否成立；代码：assert isinstance(sample, dict), sample
        assert isinstance(sample, dict), sample
        # 中文说明：检查运行时假设是否成立；代码：assert "url" in sample
        assert "url" in sample
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：url = sample["url"]
        url = sample["url"]
        # 中文说明：检查运行时假设是否成立；代码：assert isinstance(url, TarSample), "URL should be of type TarSample"
        assert isinstance(url, TarSample), "URL should be of type TarSample"
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stream = []
            stream = []
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for data_key in url.keys:
            for data_key in url.keys:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：url_path_full = os.path.join(url.root, data_key, url.path)
                url_path_full = os.path.join(url.root, data_key, url.path)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：url_key = (url_path_full, url.dset_id)
                url_key = (url_path_full, url.dset_id)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：stream.append(gopen(url_key, **kw))
                stream.append(gopen(url_key, **kw))

            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sample.update(stream=stream)
            sample.update(stream=stream)
            # 中文说明：从生成器逐步产生本行指定的值；代码：yield sample
            yield sample
        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as exn:
        except Exception as exn:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Got an exception while opening urls - {exn}", rank0_only=False)
            log.info(f"Got an exception while opening urls - {exn}", rank0_only=False)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：exn.args = exn.args + (url,)
            exn.args = exn.args + (url,)
            # 中文说明：根据条件选择执行分支；代码：if handler(exn):
            if handler(exn):
                # 中文说明：执行循环控制或空操作；代码：continue
                continue
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：执行循环控制或空操作；代码：break
                break


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def process_sample(sample, url, key_idx):
def process_sample(sample, url, key_idx):
    # 中文说明：检查运行时假设是否成立；代码：assert isinstance(sample, dict) and "data" in sample and "fname" in sample
    assert isinstance(sample, dict) and "data" in sample and "fname" in sample
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Edit the url entries
    # Edit the url entries
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sample["__url__"] = url
    sample["__url__"] = url
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# This is the folder name
    # This is the folder name
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_key = url.keys[key_idx]
    data_key = url.keys[key_idx]
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Handle the case where data_key has "/"
    # Handle the case where data_key has "/"
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_key = data_key.replace("/", "_")
    data_key = data_key.replace("/", "_")
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Edit the fname to include the data_key
    # Edit the fname to include the data_key
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：prefix, suffix = sample["fname"].split(".") # {sample_key}.{suffix} e.g. "id_1410095.json"
    prefix, suffix = sample["fname"].split(".")  # {sample_key}.{suffix} e.g. "id_1410095.json"

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# e.g. "id_1410095.caption_ai_from_image.json"
    # e.g. "id_1410095.caption_ai_from_image.json"
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sample["fname"] = f"{prefix}.{data_key}.{suffix}"
    sample["fname"] = f"{prefix}.{data_key}.{suffix}"

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return sample
    return sample


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def tar_file_expander(
def tar_file_expander(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data: Iterable[Dict[str, Any]],
    data: Iterable[Dict[str, Any]],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：handler: Callable[[Exception], bool] = reraise_exception,
    handler: Callable[[Exception], bool] = reraise_exception,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：select_files: Optional[Callable[[str], bool]] = None,
    select_files: Optional[Callable[[str], bool]] = None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rename_files: Optional[Callable[[str], str]] = None,
    rename_files: Optional[Callable[[str], str]] = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Iterator[Dict[str, Any]]:
) -> Iterator[Dict[str, Any]]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Expand tar files.
    """Expand tar files.

    Args:
        data (Iterable[Iterable[Dict[str, Any]]]): iterator over opened tar file streams.
        handler (Callable[[Exception], bool]): exception handler.
        select_files (Optional[Callable[[str], bool]]): select files from tarfiles by name (permits skipping files).
        rename_files (Optional[Callable[[str], bool]]): Renaming tar files.

    Yields:
        a stream of samples.
    """
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for source in data:
    for source in data:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：url = source["url"]
        url = source["url"]
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：检查运行时假设是否成立；代码：assert isinstance(source, dict)
            assert isinstance(source, dict)
            # 中文说明：检查运行时假设是否成立；代码：assert "stream" in source
            assert "stream" in source
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tar_file_iterator_list = []
            tar_file_iterator_list = []
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for stream_id in range(len(source["stream"])):
            for stream_id in range(len(source["stream"])):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：tar_file_iterator_list.append(
                tar_file_iterator_list.append(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：tar_file_iterator(
                    tar_file_iterator(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：source["stream"][stream_id],
                        source["stream"][stream_id],
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：handler=handler,
                        handler=handler,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：select_files=select_files,
                        select_files=select_files,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rename_files=rename_files,
                        rename_files=rename_files,
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
            # 中文说明：根据条件选择执行分支；代码：if url.sample_keys_full_list is None: # Original behavior
            if url.sample_keys_full_list is None:  # Original behavior
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# tar_file_iterator_list is a list of iterator: [tar_file_iterator_0, tar_file_iterator_1, .....
                # tar_file_iterator_list is a list of iterator: [tar_file_iterator_0, tar_file_iterator_1, ... tar_file_iterator_N]
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for sample in zip(*tar_file_iterator_list):
                for sample in zip(*tar_file_iterator_list):
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Merging data from all streams
                    # Merging data from all streams
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# sample is list of dictionaries, each dictionary contains data and fname
                    # sample is list of dictionaries, each dictionary contains data and fname
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# sample [tar_file_iterator_0[0], tar_file_iterator_1[0], ... tar_file_iterator_N[0]], length...
                    # sample [tar_file_iterator_0[0], tar_file_iterator_1[0], ... tar_file_iterator_N[0]], length = num_of_data_key
                    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key_idx, sample_key in enumerate(sample):
                    for key_idx, sample_key in enumerate(sample):
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sample_key = process_sample(sample_key, url, key_idx)
                        sample_key = process_sample(sample_key, url, key_idx)
                        # 中文说明：从生成器逐步产生本行指定的值；代码：yield sample_key
                        yield sample_key
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Provide fallback to standard processing
                # Provide fallback to standard processing
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for sample in zip(*tar_file_iterator_list):
                for sample in zip(*tar_file_iterator_list):
                    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key_idx, sample_key in enumerate(sample):
                    for key_idx, sample_key in enumerate(sample):
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sample_key = process_sample(sample_key, url, key_idx)
                        sample_key = process_sample(sample_key, url, key_idx)
                        # 中文说明：从生成器逐步产生本行指定的值；代码：yield sample_key
                        yield sample_key

        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as exn:
        except Exception as exn:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Got an exception while expanding tars - {exn}", rank0_only=False)
            log.info(f"Got an exception while expanding tars - {exn}", rank0_only=False)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：exn.args = exn.args + (source.get("stream"), source.get("url"))
            exn.args = exn.args + (source.get("stream"), source.get("url"))
            # 中文说明：根据条件选择执行分支；代码：if handler(exn):
            if handler(exn):
                # 中文说明：执行循环控制或空操作；代码：continue
                continue
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：执行循环控制或空操作；代码：break
                break


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def correct_order(sample_list: list[Dict], expected_keys_order: list[str]) -> list[Dict]:
def correct_order(sample_list: list[Dict], expected_keys_order: list[str]) -> list[Dict]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Make sure the order of samples are the same as the url.keys order."""
    """Make sure the order of samples are the same as the url.keys order."""
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_keys_per_sample = [sample["fname"].split(".")[1] for sample in sample_list]
    data_keys_per_sample = [sample["fname"].split(".")[1] for sample in sample_list]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：expected_keys_order = [key.replace("/", "_") for key in expected_keys_order]
    expected_keys_order = [key.replace("/", "_") for key in expected_keys_order]
    # 中文说明：根据条件选择执行分支；代码：if data_keys_per_sample == expected_keys_order: # Correct order
    if data_keys_per_sample == expected_keys_order:  # Correct order
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return sample_list
        return sample_list
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Order the sample_list based on the expected_keys_order
    # Order the sample_list based on the expected_keys_order
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sample_list_ordered = [None] * len(expected_keys_order)
    sample_list_ordered = [None] * len(expected_keys_order)
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for data_key, sample in zip(data_keys_per_sample, sample_list):
    for data_key, sample in zip(data_keys_per_sample, sample_list):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：idx = expected_keys_order.index(data_key)
        idx = expected_keys_order.index(data_key)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sample_list_ordered[idx] = sample
        sample_list_ordered[idx] = sample
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return sample_list_ordered
    return sample_list_ordered


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def load_func_parquet(buffer):
def load_func_parquet(buffer):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_list = pd.read_parquet(buffer).values.tolist()
    data_list = pd.read_parquet(buffer).values.tolist()
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：names = [data[0] for data in data_list]
    names = [data[0] for data in data_list]
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return names
    return names


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def tarfile_samples(
def tarfile_samples(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：src: Iterable,
    src: Iterable,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：handler: Callable = reraise_exception,
    handler: Callable = reraise_exception,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：streaming_download: bool = True,
    streaming_download: bool = True,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Iterator[Dict]:
) -> Iterator[Dict]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""
    r"""
    Given an iterator of filenames, this function opens the URL streams
    and groups data by keys.

    Args:
        src (Iterable): Iterator of TarSample.
        handler (Callable): Exception handler.
        streaming_download(bool): If enabled, performs streaming download.
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：streams = url_opener(
    streams = url_opener(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：src,
        src,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：handler=handler,
        handler=handler,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：streaming_download=streaming_download,
        streaming_download=streaming_download,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：files = tar_file_expander(streams, handler=handler)
    files = tar_file_expander(streams, handler=handler)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：samples = group_by_keys(files, handler=handler)
    samples = group_by_keys(files, handler=handler)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return samples
    return samples


# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tarfile_to_samples = filters.pipelinefilter(tarfile_samples)
tarfile_to_samples = filters.pipelinefilter(tarfile_samples)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class WebDataset(DataPipeline, FluidInterface):
class WebDataset(DataPipeline, FluidInterface):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Webdataset class."""
    r"""Webdataset class."""

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：urls: list[TarSample],
        urls: list[TarSample],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：handler: Callable = reraise_exception,
        handler: Callable = reraise_exception,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：resampled: bool = False,
        resampled: bool = False,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：shardshuffle: Optional[bool] = None,
        shardshuffle: Optional[bool] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cache_size: int = -1,
        cache_size: int = -1,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cache_dir: Optional[str] = None,
        cache_dir: Optional[str] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：detshuffle: bool = False,
        detshuffle: bool = False,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：nodesplitter: Callable = shardlists.single_node_only,
        nodesplitter: Callable = shardlists.single_node_only,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：verbose: bool = False,
        verbose: bool = False,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：streaming_download: bool = True,
        streaming_download: bool = True,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""
        r"""
        Args:
            urls (list[TarSample]): An iterator containing a list of url names.
            handler (Callable): Exception handler.
            resampled (bool): If true, sample shards from shard list with replacement.
            shardshuffle (bool): If true, shuffles the entire shard list.
            cache_size (int): Size of cache.
            cache_dir (str): Path to store cache.
            detshuffle (bool): Whether to use deterministic shuffling when shardshuffle is True.
            nodesplitter (Callable): Function for splitting urls among nodes.
            verbose (bool): If True, prints logs.
            streaming_download (bool): Whether to do streaming download or full object download.
        """
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：根据条件选择执行分支；代码：if isinstance(urls, IterableDataset):
        if isinstance(urls, IterableDataset):
            # 中文说明：检查运行时假设是否成立；代码：assert not resampled
            assert not resampled
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.append(urls)
            self.append(urls)
        # 中文说明：根据条件选择执行分支；代码：elif isinstance(urls, str) and (urls.endswith(".yaml") or urls.endswith(".yml")):
        elif isinstance(urls, str) and (urls.endswith(".yaml") or urls.endswith(".yml")):
            # 中文说明：处理异常、清理资源或管理上下文；代码：with open(urls) as stream:
            with open(urls) as stream:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：spec = yaml.safe_load(stream)
                spec = yaml.safe_load(stream)
            # 中文说明：检查运行时假设是否成立；代码：assert "datasets" in spec
            assert "datasets" in spec
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.append(shardlists.MultiShardSample(spec))
            self.append(shardlists.MultiShardSample(spec))
        # 中文说明：根据条件选择执行分支；代码：elif isinstance(urls, dict):
        elif isinstance(urls, dict):
            # 中文说明：检查运行时假设是否成立；代码：assert "datasets" in urls
            assert "datasets" in urls
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.append(shardlists.MultiShardSample(urls))
            self.append(shardlists.MultiShardSample(urls))
        # 中文说明：根据条件选择执行分支；代码：elif resampled:
        elif resampled:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.append(shardlists.ResampledShards(urls))
            self.append(shardlists.ResampledShards(urls))
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.append(shardlists.SimpleShardList(urls))
            self.append(shardlists.SimpleShardList(urls))
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.append(nodesplitter)
            self.append(nodesplitter)
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.append(shardlists.split_by_worker)
            self.append(shardlists.split_by_worker)
            # 中文说明：根据条件选择执行分支；代码：if shardshuffle is True:
            if shardshuffle is True:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：shardshuffle = 100 # type: ignore
                shardshuffle = 100  # type: ignore
            # 中文说明：根据条件选择执行分支；代码：if shardshuffle is not None:
            if shardshuffle is not None:
                # 中文说明：根据条件选择执行分支；代码：if detshuffle:
                if detshuffle:
                    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.append(filters.detshuffle(shardshuffle))
                    self.append(filters.detshuffle(shardshuffle))
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.append(filters.shuffle(shardshuffle))
                    self.append(filters.shuffle(shardshuffle))
        # 中文说明：根据条件选择执行分支；代码：if cache_dir is None or cache_size == 0:
        if cache_dir is None or cache_size == 0:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.append(
            self.append(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：tarfile_to_samples(
                tarfile_to_samples(
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：handler=handler,
                    handler=handler,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：streaming_download=streaming_download,
                    streaming_download=streaming_download,
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# We dont use cache.
            # We dont use cache.
            # 中文说明：检查运行时假设是否成立；代码：assert cache_size == -1 or cache_size > 0
            assert cache_size == -1 or cache_size > 0
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.append(
            self.append(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cache.cached_tarfile_to_samples(
                cache.cached_tarfile_to_samples(
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：handler=handler,
                    handler=handler,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：verbose=verbose,
                    verbose=verbose,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_size=cache_size,
                    cache_size=cache_size,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_dir=cache_dir,
                    cache_dir=cache_dir,
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
