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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any, Dict, List, Tuple
from typing import Any, Dict, List, Tuple

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import pandas as pd
import pandas as pd
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import psutil
import psutil
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import pynvml
import pynvml
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.callbacks.every_n import EveryN
from imaginaire.callbacks.every_n import EveryN
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.model import ImaginaireModel
from imaginaire.model import ImaginaireModel
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.trainer import ImaginaireTrainer
from imaginaire.trainer import ImaginaireTrainer
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import distributed, log
from imaginaire.utils import distributed, log


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def log_prof_data(
def log_prof_data(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_list: List[Dict[str, Any]],
    data_list: List[Dict[str, Any]],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：iteration: int,
    iteration: int,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[pd.DataFrame]:
) -> Tuple[pd.DataFrame]:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Create a table to log data with rank information
    # Create a table to log data with rank information
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：columns = ["iteration", "rank"] + list(data_list[0].keys())
    columns = ["iteration", "rank"] + list(data_list[0].keys())
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data = []
    data = []

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Initialize dictionaries to store min and max values for each metric
    # Initialize dictionaries to store min and max values for each metric
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_values = {key: float("inf") for key in columns[2:]}
    min_values = {key: float("inf") for key in columns[2:]}
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_values = {key: float("-inf") for key in columns[2:]}
    max_values = {key: float("-inf") for key in columns[2:]}
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sum_values = {key: 0.0 for key in columns[2:]}
    sum_values = {key: 0.0 for key in columns[2:]}

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：count = 0
    count = 0

    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _rank, prof_data in enumerate(data_list):
    for _rank, prof_data in enumerate(data_list):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：row = [iteration, _rank] + [prof_data[key] for key in columns[2:]]
        row = [iteration, _rank] + [prof_data[key] for key in columns[2:]]
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data.append(row)
        data.append(row)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：count += 1
        count += 1

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Update min, max, and sum values
        # Update min, max, and sum values
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key in columns[2:]:
        for key in columns[2:]:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_values[key] = min(min_values[key], prof_data[key])
            min_values[key] = min(min_values[key], prof_data[key])
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_values[key] = max(max_values[key], prof_data[key])
            max_values[key] = max(max_values[key], prof_data[key])
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sum_values[key] += prof_data[key]
            sum_values[key] += prof_data[key]

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Calculate average values
    # Calculate average values
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：avg_values = {key: sum_values[key] / count for key in columns[2:]}
    avg_values = {key: sum_values[key] / count for key in columns[2:]}

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：df = pd.DataFrame(data, columns=columns)
    df = pd.DataFrame(data, columns=columns)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：summary_df = pd.DataFrame({"Avg": avg_values, "Max": max_values, "Min": min_values})
    summary_df = pd.DataFrame({"Avg": avg_values, "Max": max_values, "Min": min_values})
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return df, summary_df
    return df, summary_df


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class DeviceMonitor(EveryN):
class DeviceMonitor(EveryN):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    A callback to monitor device (CPU/GPU) usage and log it at regular intervals.

    Args:
        every_n (int, optional): The frequency at which the callback is invoked. Defaults to 200.
        step_size (int, optional): The step size for the callback. Defaults to 1.
        log_memory_detail (bool, optional): Whether to log the memory detail. Defaults to True.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：every_n: int = 200,
        every_n: int = 200,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：step_size: int = 1,
        step_size: int = 1,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log_memory_detail: bool = True,
        log_memory_detail: bool = True,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(every_n=every_n, step_size=step_size)
        super().__init__(every_n=every_n, step_size=step_size)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.name = self.__class__.__name__
        self.name = self.__class__.__name__
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.log_memory_detail = log_memory_detail
        self.log_memory_detail = log_memory_detail

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_train_start(self, model, iteration=0):
    def on_train_start(self, model, iteration=0):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.reset_peak_memory_stats()
        torch.cuda.reset_peak_memory_stats()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.world_size = distributed.get_world_size()
        self.world_size = distributed.get_world_size()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.rank = distributed.get_rank()
        self.rank = distributed.get_rank()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config_job = self.config.job
        config_job = self.config.job
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.local_dir = f"{config_job.path_local}/{self.name}"
        self.local_dir = f"{config_job.path_local}/{self.name}"
        # 中文说明：根据条件选择执行分支；代码：if self.rank == 0:
        if self.rank == 0:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.makedirs(self.local_dir, exist_ok=True)
            os.makedirs(self.local_dir, exist_ok=True)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"{self.name} callback: local_dir: {self.local_dir}")
            log.info(f"{self.name} callback: local_dir: {self.local_dir}")

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：local_rank = int(os.getenv("LOCAL_RANK", 0))
        local_rank = int(os.getenv("LOCAL_RANK", 0))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.handle = pynvml.nvmlDeviceGetHandleByIndex(local_rank)
        self.handle = pynvml.nvmlDeviceGetHandleByIndex(local_rank)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def every_n_impl(
    def every_n_impl(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：trainer: ImaginaireTrainer,
        trainer: ImaginaireTrainer,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model: ImaginaireModel,
        model: ImaginaireModel,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_batch: dict[str, torch.Tensor],
        data_batch: dict[str, torch.Tensor],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：output_batch: dict[str, torch.Tensor],
        output_batch: dict[str, torch.Tensor],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：loss: torch.Tensor,
        loss: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：iteration: int,
        iteration: int,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cur_process = psutil.Process(os.getpid())
        cur_process = psutil.Process(os.getpid())
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cpu_memory_usage = sum(p.memory_info().rss for p in [cur_process] + cur_process.children(recu...
        cpu_memory_usage = sum(p.memory_info().rss for p in [cur_process] + cur_process.children(recursive=True))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cpu_mem_gb = cpu_memory_usage / (1024**3)
        cpu_mem_gb = cpu_memory_usage / (1024**3)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：peak_gpu_mem_gb = torch.cuda.max_memory_allocated() / (1024**3)
        peak_gpu_mem_gb = torch.cuda.max_memory_allocated() / (1024**3)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：peak_gpu_mem_reserved_gb = torch.cuda.max_memory_reserved() / (1024**3)
        peak_gpu_mem_reserved_gb = torch.cuda.max_memory_reserved() / (1024**3)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temp = torch.cuda.temperature()
        temp = torch.cuda.temperature()
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：power = torch.cuda.power_draw()
            power = torch.cuda.power_draw()
        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
        except Exception as e:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(f"Failed to get power draw with error {e}")
            log.warning(f"Failed to get power draw with error {e}")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：power = 0
            power = 0
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：util = torch.cuda.utilization()
        util = torch.cuda.utilization()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：clock = torch.cuda.clock_rate()
        clock = torch.cuda.clock_rate()

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：memory_info = pynvml.nvmlDeviceGetMemoryInfo(self.handle)
        memory_info = pynvml.nvmlDeviceGetMemoryInfo(self.handle)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：nvml_used_gpu_mem_gb = memory_info.used / (1024**3)
        nvml_used_gpu_mem_gb = memory_info.used / (1024**3)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：nvml_free_gpu_mem_gb = memory_info.free / (1024**3)
        nvml_free_gpu_mem_gb = memory_info.free / (1024**3)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prof_data = {
        prof_data = {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："cpu_mem_gb": cpu_mem_gb,
            "cpu_mem_gb": cpu_mem_gb,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："peak_gpu_mem_gb": peak_gpu_mem_gb,
            "peak_gpu_mem_gb": peak_gpu_mem_gb,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："peak_gpu_mem_reserved_gb": peak_gpu_mem_reserved_gb,
            "peak_gpu_mem_reserved_gb": peak_gpu_mem_reserved_gb,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："nvml_used_gpu_mem_gb": nvml_used_gpu_mem_gb,
            "nvml_used_gpu_mem_gb": nvml_used_gpu_mem_gb,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："nvml_free_gpu_mem_gb": nvml_free_gpu_mem_gb,
            "nvml_free_gpu_mem_gb": nvml_free_gpu_mem_gb,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："temp": temp,
            "temp": temp,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："power": power,
            "power": power,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："util": util,
            "util": util,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："clock": clock,
            "clock": clock,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_list = [prof_data] * self.world_size
        data_list = [prof_data] * self.world_size
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# this is blocking by default
        # this is blocking by default
        # 中文说明：根据条件选择执行分支；代码：if self.world_size > 1:
        if self.world_size > 1:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.distributed.all_gather_object(data_list, prof_data)
            torch.distributed.all_gather_object(data_list, prof_data)
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.distributed.barrier()
            torch.distributed.barrier()

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：df, summary_df = log_prof_data(data_list, iteration)
        df, summary_df = log_prof_data(data_list, iteration)
        # 中文说明：根据条件选择执行分支；代码：if self.rank == 0:
        if self.rank == 0:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"{self.name} Stats:\n{summary_df.to_string()}")
            log.info(f"{self.name} Stats:\n{summary_df.to_string()}")
            # 中文说明：根据条件选择执行分支；代码：if self.log_memory_detail:
            if self.log_memory_detail:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：memory_stats = torch.cuda.memory_stats()
                memory_stats = torch.cuda.memory_stats()

        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.reset_peak_memory_stats()
        torch.cuda.reset_peak_memory_stats()
