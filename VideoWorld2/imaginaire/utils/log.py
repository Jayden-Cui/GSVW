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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import atexit
import atexit
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import sys
import sys
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any, Optional
from typing import Any, Optional

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.distributed as dist
import torch.distributed as dist
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from loguru._logger import Core, Logger
from loguru._logger import Core, Logger

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：RANK0_ONLY = True
RANK0_ONLY = True
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：LEVEL = os.environ.get("LOGURU_LEVEL", "INFO")
LEVEL = os.environ.get("LOGURU_LEVEL", "INFO")

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：logger = Logger(
logger = Logger(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：core=Core(),
    core=Core(),
    # 中文说明：处理异常、清理资源或管理上下文；代码：exception=None,
    exception=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：depth=1,
    depth=1,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：record=False,
    record=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lazy=False,
    lazy=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：colors=False,
    colors=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：raw=False,
    raw=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：capture=True,
    capture=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：patchers=[],
    patchers=[],
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extra={},
    extra={},
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：atexit.register(logger.remove)
atexit.register(logger.remove)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _add_relative_path(record: dict[str, Any]) -> None:
def _add_relative_path(record: dict[str, Any]) -> None:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：start = os.getcwd()
    start = os.getcwd()
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：record["extra"]["relative_path"] = os.path.relpath(record["file"].path, start)
    record["extra"]["relative_path"] = os.path.relpath(record["file"].path, start)


# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：*options, _, extra = logger._options # type: ignore
*options, _, extra = logger._options  # type: ignore
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：logger._options = tuple([*options, [_add_relative_path], extra]) # type: ignore
logger._options = tuple([*options, [_add_relative_path], extra])  # type: ignore


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def init_loguru_stdout() -> None:
def init_loguru_stdout() -> None:
    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：logger.remove()
    logger.remove()
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：machine_format = get_machine_format()
    machine_format = get_machine_format()
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：message_format = get_message_format()
    message_format = get_message_format()
    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：logger.add(
    logger.add(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sys.stdout,
        sys.stdout,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：level=LEVEL,
        level=LEVEL,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：format="[<green>{time:MM-DD HH:mm:ss}</green>|" f"{machine_format}" f"{message_format}",
        format="[<green>{time:MM-DD HH:mm:ss}</green>|" f"{machine_format}" f"{message_format}",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：filter=_rank0_only_filter,
        filter=_rank0_only_filter,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def init_loguru_file(path: str) -> None:
def init_loguru_file(path: str) -> None:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：machine_format = get_machine_format()
    machine_format = get_machine_format()
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：message_format = get_message_format()
    message_format = get_message_format()
    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：logger.add(
    logger.add(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：path,
        path,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：encoding="utf8",
        encoding="utf8",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：level=LEVEL,
        level=LEVEL,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：format="[<green>{time:MM-DD HH:mm:ss}</green>|" f"{machine_format}" f"{message_format}",
        format="[<green>{time:MM-DD HH:mm:ss}</green>|" f"{machine_format}" f"{message_format}",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rotation="100 MB",
        rotation="100 MB",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：filter=lambda result: _rank0_only_filter(result) or not RANK0_ONLY,
        filter=lambda result: _rank0_only_filter(result) or not RANK0_ONLY,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enqueue=True,
        enqueue=True,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_machine_format() -> str:
def get_machine_format() -> str:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：node_id = "0"
    node_id = "0"
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_nodes = 1
    num_nodes = 1
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：machine_format = ""
    machine_format = ""
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank = 0
    rank = 0
    # 中文说明：根据条件选择执行分支；代码：if dist.is_available():
    if dist.is_available():
        # 中文说明：根据条件选择执行分支；代码：if not RANK0_ONLY and dist.is_initialized():
        if not RANK0_ONLY and dist.is_initialized():
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank = dist.get_rank()
            rank = dist.get_rank()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：world_size = dist.get_world_size()
            world_size = dist.get_world_size()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：machine_format = (
            machine_format = (
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"<red>[Node{node_id:<3}/{num_nodes:<3}][RANK{rank:<5}/{world_size:<5}]" + "[{process.name:<8...
                f"<red>[Node{node_id:<3}/{num_nodes:<3}][RANK{rank:<5}/{world_size:<5}]" + "[{process.name:<8}]</red>| "
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return machine_format
    return machine_format


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_message_format() -> str:
def get_message_format() -> str:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：message_format = "<level>{level}</level>|<cyan>{extra[relative_path]}:{line}:{function}</cyan...
    message_format = "<level>{level}</level>|<cyan>{extra[relative_path]}:{line}:{function}</cyan>] {message}"
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return message_format
    return message_format


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _rank0_only_filter(record: Any) -> bool:
def _rank0_only_filter(record: Any) -> bool:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_rank0 = record["extra"].get("rank0_only", True)
    is_rank0 = record["extra"].get("rank0_only", True)
    # 中文说明：根据条件选择执行分支；代码：if _get_rank() == 0 and is_rank0:
    if _get_rank() == 0 and is_rank0:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return True
        return True
    # 中文说明：根据条件选择执行分支；代码：if not is_rank0:
    if not is_rank0:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：record["message"] = f"[RANK{_get_rank()}] " + record["message"]
        record["message"] = f"[RANK{_get_rank()}] " + record["message"]
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return not is_rank0
    return not is_rank0


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def trace(message: str, rank0_only: bool = True) -> None:
def trace(message: str, rank0_only: bool = True) -> None:
    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：logger.opt(depth=1).bind(rank0_only=rank0_only).trace(message)
    logger.opt(depth=1).bind(rank0_only=rank0_only).trace(message)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def debug(message: str, rank0_only: bool = True) -> None:
def debug(message: str, rank0_only: bool = True) -> None:
    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：logger.opt(depth=1).bind(rank0_only=rank0_only).debug(message)
    logger.opt(depth=1).bind(rank0_only=rank0_only).debug(message)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def info(message: str, rank0_only: bool = True) -> None:
def info(message: str, rank0_only: bool = True) -> None:
    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：logger.opt(depth=1).bind(rank0_only=rank0_only).info(message)
    logger.opt(depth=1).bind(rank0_only=rank0_only).info(message)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def success(message: str, rank0_only: bool = True) -> None:
def success(message: str, rank0_only: bool = True) -> None:
    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：logger.opt(depth=1).bind(rank0_only=rank0_only).success(message)
    logger.opt(depth=1).bind(rank0_only=rank0_only).success(message)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def warning(message: str, rank0_only: bool = True) -> None:
def warning(message: str, rank0_only: bool = True) -> None:
    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：logger.opt(depth=1).bind(rank0_only=rank0_only).warning(message)
    logger.opt(depth=1).bind(rank0_only=rank0_only).warning(message)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def error(message: str, rank0_only: bool = True) -> None:
def error(message: str, rank0_only: bool = True) -> None:
    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：logger.opt(depth=1).bind(rank0_only=rank0_only).error(message)
    logger.opt(depth=1).bind(rank0_only=rank0_only).error(message)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def critical(message: str, rank0_only: bool = True) -> None:
def critical(message: str, rank0_only: bool = True) -> None:
    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：logger.opt(depth=1).bind(rank0_only=rank0_only).critical(message)
    logger.opt(depth=1).bind(rank0_only=rank0_only).critical(message)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def exception(message: str, rank0_only: bool = True) -> None:
def exception(message: str, rank0_only: bool = True) -> None:
    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：logger.opt(depth=1).bind(rank0_only=rank0_only).exception(message)
    logger.opt(depth=1).bind(rank0_only=rank0_only).exception(message)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _get_rank(group: Optional[dist.ProcessGroup] = None) -> int:
def _get_rank(group: Optional[dist.ProcessGroup] = None) -> int:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Get the rank (GPU device) of the worker.
    """Get the rank (GPU device) of the worker.

    Returns:
        rank (int): The rank of the worker.
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank = 0
    rank = 0
    # 中文说明：根据条件选择执行分支；代码：if dist.is_available() and dist.is_initialized():
    if dist.is_available() and dist.is_initialized():
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank = dist.get_rank(group)
        rank = dist.get_rank(group)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return rank
    return rank


# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Execute at import time.
# Execute at import time.
# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：init_loguru_stdout()
init_loguru_stdout()
