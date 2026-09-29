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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from __future__ import annotations
from __future__ import annotations

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import contextlib
import contextlib
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import threading
import threading
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import time
import time
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from collections.abc import Iterator
from collections.abc import Iterator
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any, Optional, Union
from typing import Any, Optional, Union

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class OperationWatchdog:
class OperationWatchdog:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""A watchdog that monitors operations for hangs and collects performance statistics.
    """A watchdog that monitors operations for hangs and collects performance statistics.

    This class provides a mechanism to detect when operations take longer than expected,
    which can help identify potential deadlocks or performance issues. It also collects
    statistics about operations to help identify bottlenecks.

    Attributes:
        warning_threshold: Time in seconds before warning about potential hangs.
        check_interval: Time in seconds between checks for hung operations.
        verbose_interval: Time in seconds between verbose logging.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：warning_threshold: int = 600,
        warning_threshold: int = 600,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：check_interval: int = 30,
        check_interval: int = 30,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：verbose_interval: int = -1,
        verbose_interval: int = -1,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：name: str = "OperationWatchdog",
        name: str = "OperationWatchdog",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Initialize the watchdog.
        """Initialize the watchdog.

        Args:
            warning_threshold: Time in seconds before warning about potential hangs.
                Defaults to 600 (10 minutes).
            check_interval: Time in seconds between checks. Defaults to 30.
            verbose_interval: Time in seconds between verbose logging. Defaults to -1 (disabled).
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._warning_threshold = warning_threshold
        self._warning_threshold = warning_threshold
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._check_interval = check_interval
        self._check_interval = check_interval
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._verbose_interval = verbose_interval
        self._verbose_interval = verbose_interval
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._name = name
        self._name = name
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._ops: dict[str, dict[str, Any]] = {} # Active operations
        self._ops: dict[str, dict[str, Any]] = {}  # Active operations
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._stats: dict[str, dict[str, Union[int, float]]] = {} # Operation statistics
        self._stats: dict[str, dict[str, Union[int, float]]] = {}  # Operation statistics
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._lock = threading.Lock()
        self._lock = threading.Lock()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._stop_event = threading.Event()
        self._stop_event = threading.Event()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._thread: Optional[threading.Thread] = None
        self._thread: Optional[threading.Thread] = None

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Auto-start the monitoring thread
        # Auto-start the monitoring thread
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.start()
        self.start()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def start(self) -> None:
    def start(self) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Start the watchdog monitoring thread.
        """Start the watchdog monitoring thread.

        If the thread is already running, this method does nothing.
        """
        # 中文说明：根据条件选择执行分支；代码：if self._thread is None or not self._thread.is_alive():
        if self._thread is None or not self._thread.is_alive():
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._stop_event.clear()
            self._stop_event.clear()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._thread = threading.Thread(target=self._monitor_loop, daemon=True, name=f"{self._name}_m...
            self._thread = threading.Thread(target=self._monitor_loop, daemon=True, name=f"{self._name}_monitor_thread")
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._thread.start()
            self._thread.start()
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(f"[{self._name}] Watchdog monitoring thread started")
            log.debug(f"[{self._name}] Watchdog monitoring thread started")

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def stop(self) -> None:
    def stop(self) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Stop the watchdog monitoring thread.
        """Stop the watchdog monitoring thread.

        This method is typically called when shutting down the application.
        """
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._stop_event.set()
        self._stop_event.set()
        # 中文说明：根据条件选择执行分支；代码：if self._thread and self._thread.is_alive():
        if self._thread and self._thread.is_alive():
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._thread.join(timeout=1.0)
            self._thread.join(timeout=1.0)
            # 中文说明：根据条件选择执行分支；代码：if self._thread.is_alive():
            if self._thread.is_alive():
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(f"[{self._name}] Watchdog thread did not terminate within timeout", rank0_only=Fa...
                log.warning(f"[{self._name}] Watchdog thread did not terminate within timeout", rank0_only=False)
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(f"[{self._name}] Watchdog monitoring thread stopped", rank0_only=False)
                log.debug(f"[{self._name}] Watchdog monitoring thread stopped", rank0_only=False)

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@contextlib.contextmanager
    @contextlib.contextmanager
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def watch(self, operation_name: str, description: str = "", verbose_first_n: int = -1) -> Ite...
    def watch(self, operation_name: str, description: str = "", verbose_first_n: int = -1) -> Iterator[None]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Context manager for monitoring an operation.
        """Context manager for monitoring an operation.

        This is the primary interface for using the watchdog. It automatically
        tracks the start and end time of the operation and updates statistics.

        Args:
            operation_name: Name/type of the operation to monitor.
            description: Optional description providing more context.
            verbose_first_n: If positive, print verbose logs for first N operations for operation_name.

        Yields:
            None

        Example:
            with watchdog.watch("data_fetch", "Fetching user data"):
                data = fetch_user_data(user_id)
        """
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Create unique ID for this specific operation instance
        # Create unique ID for this specific operation instance
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：op_id = f"{operation_name}_{int(time.time()*1000)}"
        op_id = f"{operation_name}_{int(time.time()*1000)}"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：start_time = time.time()
        start_time = time.time()

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Register operation
        # Register operation
        # 中文说明：处理异常、清理资源或管理上下文；代码：with self._lock:
        with self._lock:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._ops[op_id] = {
            self._ops[op_id] = {
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："name": operation_name,
                "name": operation_name,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："desc": description or operation_name,
                "desc": description or operation_name,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："start": start_time,
                "start": start_time,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："update": start_time,
                "update": start_time,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："warned": False,
                "warned": False,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
            }

        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Yield control back to the with-block
            # Yield control back to the with-block
            # 中文说明：从生成器逐步产生本行指定的值；代码：yield
            yield
        # 中文说明：处理异常、清理资源或管理上下文；代码：finally:
        finally:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Calculate duration and remove from active operations
            # Calculate duration and remove from active operations
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：duration = time.time() - start_time
            duration = time.time() - start_time
            # 中文说明：根据条件选择执行分支；代码：if duration > self._warning_threshold:
            if duration > self._warning_threshold:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(
                log.warning(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"[{self._name}] Operation id: {op_id}, name: '{operation_name}' took {duration:.2f}s",
                    f"[{self._name}] Operation id: {op_id}, name: '{operation_name}' took {duration:.2f}s",
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank0_only=False,
                    rank0_only=False,
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )

            # 中文说明：处理异常、清理资源或管理上下文；代码：with self._lock:
            with self._lock:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Remove from active operations
                # Remove from active operations
                # 中文说明：根据条件选择执行分支；代码：if op_id in self._ops:
                if op_id in self._ops:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del self._ops[op_id]
                    del self._ops[op_id]

                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Update statistics
                # Update statistics
                # 中文说明：根据条件选择执行分支；代码：if operation_name not in self._stats:
                if operation_name not in self._stats:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._stats[operation_name] = {"count": 0, "total_time": 0.0, "max_time": 0.0, "last_time": 0.0}
                    self._stats[operation_name] = {"count": 0, "total_time": 0.0, "max_time": 0.0, "last_time": 0.0}

                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stats = self._stats[operation_name]
                stats = self._stats[operation_name]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stats["count"] += 1
                stats["count"] += 1
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stats["total_time"] += duration
                stats["total_time"] += duration
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stats["max_time"] = max(stats["max_time"], duration)
                stats["max_time"] = max(stats["max_time"], duration)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stats["last_time"] = duration
                stats["last_time"] = duration

            # 中文说明：根据条件选择执行分支；代码：if verbose_first_n > 0 and stats["count"] <= verbose_first_n:
            if verbose_first_n > 0 and stats["count"] <= verbose_first_n:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：avg_time = stats["total_time"] / stats["count"]
                avg_time = stats["total_time"] / stats["count"]
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(
                log.info(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"[{self._name}] name: '{operation_name}', count {stats['count']} / {verbose_first_n} took {d...
                    f"[{self._name}] name: '{operation_name}', count {stats['count']} / {verbose_first_n} took {duration:.2f}s. avg {avg_time:.2f}s, max {stats['max_time']:.2f}s, last {stats['last_time']:.2f}s",
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank0_only=False,
                    rank0_only=False,
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def heartbeat(self, operation_name: str) -> None:
    def heartbeat(self, operation_name: str) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Send a heartbeat for all operations of a given type.
        """Send a heartbeat for all operations of a given type.

        Use this inside long operations to prevent false warnings.

        Args:
            operation_name: The operation type to update.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：current_time = time.time()
        current_time = time.time()
        # 中文说明：处理异常、清理资源或管理上下文；代码：with self._lock:
        with self._lock:
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _op_id, op in self._ops.items():
            for _op_id, op in self._ops.items():
                # 中文说明：根据条件选择执行分支；代码：if op["name"] == operation_name:
                if op["name"] == operation_name:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：op["update"] = current_time
                    op["update"] = current_time
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：op["warned"] = False
                    op["warned"] = False

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_stats(self, operation_name: Optional[str] = None) -> dict[str, Any]:
    def get_stats(self, operation_name: Optional[str] = None) -> dict[str, Any]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Get statistics for operations.
        """Get statistics for operations.

        Args:
            operation_name: Get stats for specific operation, or None for all.

        Returns:
            Dictionary of operation statistics. For each operation, includes:
            - count: Number of completed operations
            - total_time: Total time spent in this operation type
            - max_time: Maximum time spent in a single operation
            - last_time: Time spent in the most recent operation
            - avg_time: Average time per operation (if count > 0)
        """
        # 中文说明：处理异常、清理资源或管理上下文；代码：with self._lock:
        with self._lock:
            # 中文说明：根据条件选择执行分支；代码：if operation_name:
            if operation_name:
                # 中文说明：根据条件选择执行分支；代码：if operation_name in self._stats:
                if operation_name in self._stats:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stats = self._stats[operation_name].copy()
                    stats = self._stats[operation_name].copy()
                    # 中文说明：根据条件选择执行分支；代码：if stats["count"] > 0:
                    if stats["count"] > 0:
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stats["avg_time"] = stats["total_time"] / stats["count"]
                        stats["avg_time"] = stats["total_time"] / stats["count"]
                    # 中文说明：从当前函数返回结果或结束函数执行；代码：return stats
                    return stats
                # 中文说明：从当前函数返回结果或结束函数执行；代码：return {}
                return {}

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Return all stats
            # Return all stats
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：result = {}
            result = {}
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for name, stats in self._stats.items():
            for name, stats in self._stats.items():
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：result[name] = stats.copy()
                result[name] = stats.copy()
                # 中文说明：根据条件选择执行分支；代码：if stats["count"] > 0:
                if stats["count"] > 0:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：result[name]["avg_time"] = stats["total_time"] / stats["count"]
                    result[name]["avg_time"] = stats["total_time"] / stats["count"]
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return result
            return result

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def print_stats(self) -> None:
    def print_stats(self) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Print statistics for all operations.
        """Print statistics for all operations.

        This is a convenience method that logs statistics at INFO level.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stats = self.get_stats()
        stats = self.get_stats()
        # 中文说明：根据条件选择执行分支；代码：if not stats:
        if not stats:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"[{self._name}] No operation statistics available", rank0_only=False)
            log.info(f"[{self._name}] No operation statistics available", rank0_only=False)
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return
            return

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"[{self._name}] Operation Statistics:", rank0_only=False)
        log.info(f"[{self._name}] Operation Statistics:", rank0_only=False)

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for name, s in stats.items():
        for name, s in stats.items():
            # 中文说明：根据条件选择执行分支；代码：if s["count"] > 0:
            if s["count"] > 0:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：avg = s["total_time"] / s["count"]
                avg = s["total_time"] / s["count"]
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(
                log.info(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"[{self._name}] {name}: count={s['count']}, "
                    f"[{self._name}]  {name}: count={s['count']}, "
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"avg={avg:.2f}s, max={s['max_time']:.2f}s, "
                    f"avg={avg:.2f}s, max={s['max_time']:.2f}s, "
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"last={s['last_time']:.2f}s",
                    f"last={s['last_time']:.2f}s",
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank0_only=False,
                    rank0_only=False,
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def list_active_operations(self) -> dict[str, Any]:
    def list_active_operations(self) -> dict[str, Any]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""List all currently active operations.
        """List all currently active operations.

        Returns:
            Dictionary mapping operation IDs to information about active operations.
        """
        # 中文说明：处理异常、清理资源或管理上下文；代码：with self._lock:
        with self._lock:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：current_time = time.time()
            current_time = time.time()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：result = {}
            result = {}

            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for op_id, op in self._ops.items():
            for op_id, op in self._ops.items():
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：result[op_id] = {
                result[op_id] = {
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："name": op["name"],
                    "name": op["name"],
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："description": op["desc"],
                    "description": op["desc"],
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："running_time": current_time - op["start"],
                    "running_time": current_time - op["start"],
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："time_since_update": current_time - op["update"],
                    "time_since_update": current_time - op["update"],
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
                }

            # 中文说明：从当前函数返回结果或结束函数执行；代码：return result
            return result

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def reset_stats(self) -> None:
    def reset_stats(self) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Reset all operation statistics.
        """Reset all operation statistics.

        This clears all accumulated statistics but does not affect active operations.
        """
        # 中文说明：处理异常、清理资源或管理上下文；代码：with self._lock:
        with self._lock:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._stats.clear()
            self._stats.clear()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _monitor_loop(self) -> None:
    def _monitor_loop(self) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Monitor registered operations for hangs.
        """Monitor registered operations for hangs.

        This is an internal method that runs in a separate thread.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：last_verbose_time = 0
        last_verbose_time = 0
        # 中文说明：在条件成立时重复执行循环体；代码：while not self._stop_event.is_set():
        while not self._stop_event.is_set():
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：now = time.time()
            now = time.time()

            # 中文说明：处理异常、清理资源或管理上下文；代码：with self._lock:
            with self._lock:
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _, op in list(self._ops.items()):
                for _, op in list(self._ops.items()):
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Check if operation is hung
                    # Check if operation is hung
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：elapsed = now - op["update"]
                    elapsed = now - op["update"]
                    # 中文说明：根据条件选择执行分支；代码：if elapsed > self._warning_threshold and not op["warned"]:
                    if elapsed > self._warning_threshold and not op["warned"]:
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：total_time = now - op["start"]
                        total_time = now - op["start"]
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(
                        log.warning(
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"[{self._name}] POTENTIAL HANG: '{op['name']}' ({op['desc']}) "
                            f"[{self._name}] POTENTIAL HANG: '{op['name']}' ({op['desc']}) "
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"has been running for {total_time:.1f}s total, "
                            f"has been running for {total_time:.1f}s total, "
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"with {elapsed:.1f}s since last update",
                            f"with {elapsed:.1f}s since last update",
                            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank0_only=False,
                            rank0_only=False,
                        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                        )
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：op["warned"] = True
                        op["warned"] = True

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Sleep between checks
            # Sleep between checks
            # 中文说明：根据条件选择执行分支；代码：if self._verbose_interval > 0 and now - last_verbose_time > self._verbose_interval:
            if self._verbose_interval > 0 and now - last_verbose_time > self._verbose_interval:
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.print_stats()
                self.print_stats()
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：last_verbose_time = now
                last_verbose_time = now
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._stop_event.wait(self._check_interval)
            self._stop_event.wait(self._check_interval)
