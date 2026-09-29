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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import contextlib
import contextlib
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import time
import time

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import distributed, log
from imaginaire.utils import distributed, log
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io import easy_io
from imaginaire.utils.easy_io import easy_io

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# the number of warmup steps before the active step in each profiling cycle
# the number of warmup steps before the active step in each profiling cycle
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：TORCH_TRACE_WARMUP = 3
TORCH_TRACE_WARMUP = 3

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# how much memory allocation/free ops to record in memory snapshots
# how much memory allocation/free ops to record in memory snapshots
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：MEMORY_SNAPSHOT_MAX_ENTRIES = 100000
MEMORY_SNAPSHOT_MAX_ENTRIES = 100000


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@contextlib.contextmanager
@contextlib.contextmanager
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def maybe_enable_profiling(config, *, global_step: int = 0):
def maybe_enable_profiling(config, *, global_step: int = 0):
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# get user defined profiler settings
    # get user defined profiler settings
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enable_profiling = config.trainer.profiling.enable_profiling
    enable_profiling = config.trainer.profiling.enable_profiling
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：profile_freq = config.trainer.profiling.profile_freq
    profile_freq = config.trainer.profiling.profile_freq

    # 中文说明：根据条件选择执行分支；代码：if enable_profiling:
    if enable_profiling:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trace_dir = os.path.join(config.job.path_local, "torch_trace")
        trace_dir = os.path.join(config.job.path_local, "torch_trace")
        # 中文说明：根据条件选择执行分支；代码：if distributed.get_rank() == 0:
        if distributed.get_rank() == 0:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.makedirs(trace_dir, exist_ok=True)
            os.makedirs(trace_dir, exist_ok=True)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank = distributed.get_rank()
        rank = distributed.get_rank()

        # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def trace_handler(prof):
        def trace_handler(prof):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_trace_dir_name = "iteration_" + str(prof.step_num)
            curr_trace_dir_name = "iteration_" + str(prof.step_num)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_trace_dir = os.path.join(trace_dir, curr_trace_dir_name)
            curr_trace_dir = os.path.join(trace_dir, curr_trace_dir_name)
            # 中文说明：根据条件选择执行分支；代码：if not os.path.exists(curr_trace_dir):
            if not os.path.exists(curr_trace_dir):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.makedirs(curr_trace_dir, exist_ok=True)
                os.makedirs(curr_trace_dir, exist_ok=True)

            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Dumping traces at step {prof.step_num}")
            log.info(f"Dumping traces at step {prof.step_num}")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：begin = time.monotonic()
            begin = time.monotonic()
            # 中文说明：根据条件选择执行分支；代码：if config.trainer.profiling.first_n_rank < 0 or rank < config.trainer.profiling.first_n_rank:
            if config.trainer.profiling.first_n_rank < 0 or rank < config.trainer.profiling.first_n_rank:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：prof.export_chrome_trace(f"{curr_trace_dir}/rank{rank}_trace.json.gz") # saved as gz to save ...
                prof.export_chrome_trace(f"{curr_trace_dir}/rank{rank}_trace.json.gz")  # saved as gz to save space
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Finished dumping traces in {time.monotonic() - begin:.2f} seconds")
            log.info(f"Finished dumping traces in {time.monotonic() - begin:.2f} seconds")

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Profiling active. Traces will be saved at {trace_dir}")
        log.info(f"Profiling active. Traces will be saved at {trace_dir}")

        # 中文说明：根据条件选择执行分支；代码：if not os.path.exists(trace_dir):
        if not os.path.exists(trace_dir):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.makedirs(trace_dir, exist_ok=True)
            os.makedirs(trace_dir, exist_ok=True)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：warmup, active = TORCH_TRACE_WARMUP, 1
        warmup, active = TORCH_TRACE_WARMUP, 1
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：wait = profile_freq - (active + warmup)
        wait = profile_freq - (active + warmup)
        # 中文说明：检查运行时假设是否成立；代码：assert wait >= 0, "profile_freq must be greater than or equal to warmup + active"
        assert wait >= 0, "profile_freq must be greater than or equal to warmup + active"

        # 中文说明：处理异常、清理资源或管理上下文；代码：with torch.profiler.profile(
        with torch.profiler.profile(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：activities=[
            activities=[
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.profiler.ProfilerActivity.CPU,
                torch.profiler.ProfilerActivity.CPU,
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.profiler.ProfilerActivity.CUDA,
                torch.profiler.ProfilerActivity.CUDA,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：],
            ],
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：schedule=torch.profiler.schedule(wait=wait, warmup=warmup, active=active),
            schedule=torch.profiler.schedule(wait=wait, warmup=warmup, active=active),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：on_trace_ready=trace_handler,
            on_trace_ready=trace_handler,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：record_shapes=config.trainer.profiling.record_shape,
            record_shapes=config.trainer.profiling.record_shape,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：profile_memory=config.trainer.profiling.profile_memory,
            profile_memory=config.trainer.profiling.profile_memory,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：with_stack=config.trainer.profiling.with_stack,
            with_stack=config.trainer.profiling.with_stack,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：with_modules=config.trainer.profiling.with_modules,
            with_modules=config.trainer.profiling.with_modules,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) as torch_profiler:
        ) as torch_profiler:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：torch_profiler.step_num = global_step
            torch_profiler.step_num = global_step
            # 中文说明：从生成器逐步产生本行指定的值；代码：yield torch_profiler
            yield torch_profiler
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：torch_profiler = contextlib.nullcontext()
        torch_profiler = contextlib.nullcontext()
        # 中文说明：从生成器逐步产生本行指定的值；代码：yield None
        yield None


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@contextlib.contextmanager
@contextlib.contextmanager
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def maybe_enable_memory_snapshot(config, *, global_step: int = 0):
def maybe_enable_memory_snapshot(config, *, global_step: int = 0):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enable_snapshot = config.trainer.profiling.enable_memory_snapshot
    enable_snapshot = config.trainer.profiling.enable_memory_snapshot
    # 中文说明：根据条件选择执行分支；代码：if enable_snapshot:
    if enable_snapshot:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：snapshot_dir = os.path.join(config.job.path_local, "memory_snapshot")
        snapshot_dir = os.path.join(config.job.path_local, "memory_snapshot")
        # 中文说明：根据条件选择执行分支；代码：if distributed.get_rank() == 0:
        if distributed.get_rank() == 0:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.makedirs(snapshot_dir, exist_ok=True)
            os.makedirs(snapshot_dir, exist_ok=True)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank = torch.distributed.get_rank()
        rank = torch.distributed.get_rank()

        # 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class MemoryProfiler:
        class MemoryProfiler:
            # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, step_num: int, freq: int):
            def __init__(self, step_num: int, freq: int):
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.memory._record_memory_history(max_entries=MEMORY_SNAPSHOT_MAX_ENTRIES)
                torch.cuda.memory._record_memory_history(max_entries=MEMORY_SNAPSHOT_MAX_ENTRIES)
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# when resume training, we start from the last step
                # when resume training, we start from the last step
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.step_num = step_num
                self.step_num = step_num
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.freq = freq
                self.freq = freq

            # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def step(self, exit_ctx: bool = False):
            def step(self, exit_ctx: bool = False):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.step_num += 1
                self.step_num += 1
                # 中文说明：根据条件选择执行分支；代码：if not exit_ctx and self.step_num % self.freq != 0:
                if not exit_ctx and self.step_num % self.freq != 0:
                    # 中文说明：从当前函数返回结果或结束函数执行；代码：return
                    return
                # 中文说明：根据条件选择执行分支；代码：if not exit_ctx:
                if not exit_ctx:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_step = self.step_num
                    curr_step = self.step_num
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dir_name = f"iteration_{curr_step}"
                    dir_name = f"iteration_{curr_step}"
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# dump as iteration_0_exit if OOM at iter 1
                    # dump as iteration_0_exit if OOM at iter 1
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_step = self.step_num - 1
                    curr_step = self.step_num - 1
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dir_name = f"iteration_{curr_step}_exit"
                    dir_name = f"iteration_{curr_step}_exit"
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_snapshot_dir = os.path.join(snapshot_dir, dir_name)
                curr_snapshot_dir = os.path.join(snapshot_dir, dir_name)
                # 中文说明：根据条件选择执行分支；代码：if not os.path.exists(curr_snapshot_dir):
                if not os.path.exists(curr_snapshot_dir):
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.makedirs(curr_snapshot_dir, exist_ok=True)
                    os.makedirs(curr_snapshot_dir, exist_ok=True)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Dumping memory snapshot at step {curr_step}")
                log.info(f"Dumping memory snapshot at step {curr_step}")
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：begin = time.monotonic()
                begin = time.monotonic()

                # 中文说明：根据条件选择执行分支；代码：if config.trainer.profiling.first_n_rank < 0 or rank < config.trainer.profiling.first_n_rank:
                if config.trainer.profiling.first_n_rank < 0 or rank < config.trainer.profiling.first_n_rank:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：easy_io.dump(
                    easy_io.dump(
                        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.memory._snapshot(),
                        torch.cuda.memory._snapshot(),
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"{curr_snapshot_dir}/rank{rank}_memory_snapshot.pickle",
                        f"{curr_snapshot_dir}/rank{rank}_memory_snapshot.pickle",
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Finished dumping memory snapshot in {time.monotonic() - begin:.2f} seconds")
                log.info(f"Finished dumping memory snapshot in {time.monotonic() - begin:.2f} seconds")

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Memory profiler active. Snapshot will be saved at {snapshot_dir}")
        log.info(f"Memory profiler active. Snapshot will be saved at {snapshot_dir}")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：profiler = MemoryProfiler(global_step, config.trainer.profiling.profile_freq)
        profiler = MemoryProfiler(global_step, config.trainer.profiling.profile_freq)
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：从生成器逐步产生本行指定的值；代码：yield profiler
            yield profiler
        # 中文说明：处理异常、清理资源或管理上下文；代码：except torch.cuda.OutOfMemoryError as e:
        except torch.cuda.OutOfMemoryError as e:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：profiler.step(exit_ctx=True)
            profiler.step(exit_ctx=True)
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：从生成器逐步产生本行指定的值；代码：yield None
        yield None
