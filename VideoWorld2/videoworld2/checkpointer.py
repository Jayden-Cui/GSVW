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

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import collections
import collections
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import threading
import threading
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import TYPE_CHECKING
from typing import TYPE_CHECKING

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed.checkpoint.state_dict import (
from torch.distributed.checkpoint.state_dict import (
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：StateDictOptions,
    StateDictOptions,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：get_optimizer_state_dict,
    get_optimizer_state_dict,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：set_model_state_dict,
    set_model_state_dict,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：set_optimizer_state_dict,
    set_optimizer_state_dict,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.model import ImaginaireModel
from imaginaire.model import ImaginaireModel
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import callback, distributed, log, misc
from imaginaire.utils import callback, distributed, log, misc

# 中文说明：根据条件选择执行分支；代码：if TYPE_CHECKING:
if TYPE_CHECKING:
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.config import CheckpointConfig, JobConfig
    from imaginaire.config import CheckpointConfig, JobConfig


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Checkpointer:
class Checkpointer:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""The checkpointer class. Supports checkpoint saving/loading to local disk."""
    """The checkpointer class. Supports checkpoint saving/loading to local disk."""

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, config_checkpoint: CheckpointConfig, config_job: JobConfig, callbacks: cal...
    def __init__(self, config_checkpoint: CheckpointConfig, config_job: JobConfig, callbacks: callback.CallBackGroup):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Constructor of the checkpointer.
        """Constructor of the checkpointer.

        Args:
            config_checkpoint (CheckpointConfig): The config object for the checkpointer.
        """
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Set the callback functions.
        # Set the callback functions.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.callbacks = callbacks
        self.callbacks = callbacks
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.checkpoint_dir_local = f"{config_job.path_local}/checkpoints"
        self.checkpoint_dir_local = f"{config_job.path_local}/checkpoints"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.strict_resume = config_checkpoint.strict_resume
        self.strict_resume = config_checkpoint.strict_resume
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.load_path = config_checkpoint.load_path or None
        self.load_path = config_checkpoint.load_path or None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.load_training_state = config_checkpoint.load_training_state
        self.load_training_state = config_checkpoint.load_training_state
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.only_load_scheduler_state = config_checkpoint.only_load_scheduler_state
        self.only_load_scheduler_state = config_checkpoint.only_load_scheduler_state
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.save_thread = None
        self.save_thread = None

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def save(
    def save(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model: ImaginaireModel,
        model: ImaginaireModel,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：optimizer: torch.optim.Optimizer,
        optimizer: torch.optim.Optimizer,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scheduler: torch.optim.lr_scheduler.LRScheduler,
        scheduler: torch.optim.lr_scheduler.LRScheduler,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：grad_scaler: torch.amp.GradScaler,
        grad_scaler: torch.amp.GradScaler,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：iteration: int,
        iteration: int,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Save network weights, optimizer parameters, scheduler parameters to a checkpoint.
        """Save network weights, optimizer parameters, scheduler parameters to a checkpoint.

        Args:
            model (ImaginaireModel): The PyTorch model.
            optimizer (torch.optim.Optimizer): The model optimizer.
            scheduler (torch.optim.lr_scheduler.LRScheduler): The optimization scheduler.
            grad_scaler (torch.amp.GradScaler): The gradient scaler (for mixed precision training).
            iteration (int): Current iteration number.
        """
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_save_checkpoint_start(model, iteration)
        self.callbacks.on_save_checkpoint_start(model, iteration)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint_file = f"iter_{iteration:09}.pt"
        checkpoint_file = f"iter_{iteration:09}.pt"

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Handle optimizer state dict if FSDP is enabled
        # Handle optimizer state dict if FSDP is enabled
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_fsdp = model.config.fsdp_shard_size != 0 and distributed.get_world_size() > 1
        is_fsdp = model.config.fsdp_shard_size != 0 and distributed.get_world_size() > 1
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_fsdp = True
        is_fsdp = True
        # 中文说明：根据条件选择执行分支；代码：if is_fsdp:
        if is_fsdp:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：optimizer_state_dict = get_optimizer_state_dict(
            optimizer_state_dict = get_optimizer_state_dict(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model,
                model,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：optimizer,
                optimizer,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：options=StateDictOptions(
                options=StateDictOptions(
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：full_state_dict=True,
                    full_state_dict=True,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cpu_offload=True,
                    cpu_offload=True,
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
                ),
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：optimizer_state_dict = optimizer.state_dict()
            optimizer_state_dict = optimizer.state_dict()

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Gather all the state dicts to be saved
        # Gather all the state dicts to be saved
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dicts_to_save = {
        state_dicts_to_save = {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："model": model.state_dict(),
            "model": model.state_dict(),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："optim": optimizer_state_dict,
            "optim": optimizer_state_dict,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："scheduler": scheduler.state_dict(),
            "scheduler": scheduler.state_dict(),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："trainer": {
            "trainer": {
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："grad_scaler": grad_scaler.state_dict(),
                "grad_scaler": grad_scaler.state_dict(),
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："iteration": iteration,
                "iteration": iteration,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：},
            },
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }

        # 中文说明：根据条件选择执行分支；代码：if distributed.get_rank() == 0:
        if distributed.get_rank() == 0:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_save_checkpoint(model, state_dict=state_dicts_to_save)
            self.callbacks.on_save_checkpoint(model, state_dict=state_dicts_to_save)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：folders = state_dicts_to_save.keys()
            folders = state_dicts_to_save.keys()
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for folder in folders:
            for folder in folders:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dict = state_dicts_to_save[folder]
                state_dict = state_dicts_to_save[folder]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dict = misc.to(state_dict, device="cpu")
                state_dict = misc.to(state_dict, device="cpu")
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Wait for previous saver thread to end.
                # Wait for previous saver thread to end.
                # 中文说明：根据条件选择执行分支；代码：if self.save_thread:
                if self.save_thread:
                    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.save_thread.join()
                    self.save_thread.join()
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Run the checkpoint saver in a separate thread.
                # Run the checkpoint saver in a separate thread.
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint_path = os.path.join(self.checkpoint_dir_local, folder, checkpoint_file)
                checkpoint_path = os.path.join(self.checkpoint_dir_local, folder, checkpoint_file)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.save_thread = threading.Thread(
                self.save_thread = threading.Thread(
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：target=self._save_worker_local,
                    target=self._save_worker_local,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：daemon=False,
                    daemon=False,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：args=(state_dict, checkpoint_path, distributed.get_rank()),
                    args=(state_dict, checkpoint_path, distributed.get_rank()),
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.save_thread.start()
                self.save_thread.start()

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Note: Checkpoints are saved on a separate thread and this callback is not accurate.
        # Note: Checkpoints are saved on a separate thread and this callback is not accurate.
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Please check logs from on_save_checkpoint_success() for better accuracy
        # Please check logs from on_save_checkpoint_success() for better accuracy
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_save_checkpoint_end(model=None, iteration=iteration)
        self.callbacks.on_save_checkpoint_end(model=None, iteration=iteration)

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@misc.timer("checkpoint saving (local)")
    @misc.timer("checkpoint saving (local)")
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _save_worker_local(self, state_dict: dict[str, torch.Tensor], checkpoint_path: str, rank:...
    def _save_worker_local(self, state_dict: dict[str, torch.Tensor], checkpoint_path: str, rank: int = 0) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Worker to save checkpoint to local disk, spawned with a child thread (runs in parallel wit...
        """Worker to save checkpoint to local disk, spawned with a child thread (runs in parallel with the training).

        Args:
            state_dict (dict[str, torch.Tensor]): The state dict of the model/optimizer/scheduler.
            checkpoint_path (str): The path of the model checkpoint.
            rank (int): GPU device (default: 0).
        """
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.makedirs(os.path.dirname(checkpoint_path), exist_ok=True)
        os.makedirs(os.path.dirname(checkpoint_path), exist_ok=True)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint_file = os.path.basename(checkpoint_path)
        checkpoint_file = os.path.basename(checkpoint_path)
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.save(state_dict, checkpoint_path)
            torch.save(state_dict, checkpoint_path)
            # 中文说明：根据条件选择执行分支；代码：if rank == 0:
            if rank == 0:
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._write_latest_checkpoint_file(checkpoint_file)
                self._write_latest_checkpoint_file(checkpoint_file)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.success(f"Saved checkpoint (local): {checkpoint_path}")
            log.success(f"Saved checkpoint (local): {checkpoint_path}")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iteration = int(checkpoint_file.replace("iter_", "").replace(".pt", ""))
            iteration = int(checkpoint_file.replace("iter_", "").replace(".pt", ""))
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_save_checkpoint_success(iteration=iteration)
            self.callbacks.on_save_checkpoint_success(iteration=iteration)
        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e: # noqa: BLE001
        except Exception as e:  # noqa: BLE001
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.exception(f"Checkpoint failed to save (local): {e}")
            log.exception(f"Checkpoint failed to save (local): {e}")

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@misc.timer("checkpoint loading")
    @misc.timer("checkpoint loading")
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def load(
    def load(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model: ImaginaireModel,
        model: ImaginaireModel,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：optimizer: torch.optim.Optimizer | None = None,
        optimizer: torch.optim.Optimizer | None = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scheduler: torch.optim.lr_scheduler.LRScheduler | None = None,
        scheduler: torch.optim.lr_scheduler.LRScheduler | None = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：grad_scaler: torch.amp.GradScaler | None = None,
        grad_scaler: torch.amp.GradScaler | None = None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> int:
    ) -> int:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Load network weights and optimizer states from a checkpoint in a single process.
        """Load network weights and optimizer states from a checkpoint in a single process.

        The priority of the checkpoint loading logic is:
        1. Attempt to resume training if possible by looking for latest_checkpoint.txt under the same name.
        2. If no latest checkpoint were found, it loads the model weights specified by config_checkpoint.path.
           - This is typically used for inference mode.
           - If config_checkpoint.load_optimizer_state is True, then also load the optimizer and scheduler states.
        3. If none of the above, randomly initialize the model parameters and train from scratch.

        Args:
            model (ImaginaireModel): The PyTorch model.
            optimizer (torch.optim.Optimizer | None): The model optimizer (default: None).
            scheduler (torch.optim.lr_scheduler.LRScheduler | None): The optimization scheduler (default: None).
            grad_scaler (torch.amp.GradScaler | None): The gradient scaler (for mixed precision training).

        Returns:
            iteration (int): the iteration number to start/resume from.
        """
        # 中文说明：检查运行时假设是否成立；代码：assert self.load_path is None, "load_path is not supported yet"
        assert self.load_path is None, "load_path is not supported yet"
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_load_checkpoint_start(model)
        self.callbacks.on_load_checkpoint_start(model)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_fsdp = model.config.fsdp_shard_size != 0 and distributed.get_world_size() > 1
        is_fsdp = model.config.fsdp_shard_size != 0 and distributed.get_world_size() > 1

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：latest_checkpoint_file = self._read_latest_checkpoint_file()
        latest_checkpoint_file = self._read_latest_checkpoint_file()
        # 中文说明：根据条件选择执行分支；代码：if latest_checkpoint_file is not None:
        if latest_checkpoint_file is not None:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 1. Resume training from latest_checkpoint.txt under the same name.
            # 1. Resume training from latest_checkpoint.txt under the same name.
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint_dir = self.checkpoint_dir_local
            checkpoint_dir = self.checkpoint_dir_local
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_checkpoint_path = os.path.join(checkpoint_dir, "model", latest_checkpoint_file)
            model_checkpoint_path = os.path.join(checkpoint_dir, "model", latest_checkpoint_file)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：optimizer_checkpoint_path = os.path.join(checkpoint_dir, "optim", latest_checkpoint_file)
            optimizer_checkpoint_path = os.path.join(checkpoint_dir, "optim", latest_checkpoint_file)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scheduler_checkpoint_path = os.path.join(checkpoint_dir, "scheduler", latest_checkpoint_file)
            scheduler_checkpoint_path = os.path.join(checkpoint_dir, "scheduler", latest_checkpoint_file)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trainer_checkpoint_path = os.path.join(checkpoint_dir, "trainer", latest_checkpoint_file)
            trainer_checkpoint_path = os.path.join(checkpoint_dir, "trainer", latest_checkpoint_file)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resume = True
            resume = True
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：only_resume_scheduler = True
            only_resume_scheduler = True
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_checkpoint_path = None
            model_checkpoint_path = None
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：optimizer_checkpoint_path = None
            optimizer_checkpoint_path = None
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scheduler_checkpoint_path = None
            scheduler_checkpoint_path = None
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trainer_checkpoint_path = None
            trainer_checkpoint_path = None
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resume = False
            resume = False
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：only_resume_scheduler = False
            only_resume_scheduler = False
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Load checkpoint.
        # Load checkpoint.
        # 中文说明：根据条件选择执行分支；代码：if latest_checkpoint_file is not None:
        if latest_checkpoint_file is not None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dicts_paths = {
            state_dicts_paths = {
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："model": model_checkpoint_path,
                "model": model_checkpoint_path,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："optim": optimizer_checkpoint_path,
                "optim": optimizer_checkpoint_path,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："scheduler": scheduler_checkpoint_path,
                "scheduler": scheduler_checkpoint_path,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："trainer": trainer_checkpoint_path,
                "trainer": trainer_checkpoint_path,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
            }
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dicts_to_load = {}
            state_dicts_to_load = {}
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key, checkpoint_path in state_dicts_paths.items():
            for key, checkpoint_path in state_dicts_paths.items():
                # 中文说明：开始一个可捕获异常的代码块；代码：try:
                try:
                    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._check_checkpoint_exists(checkpoint_path)
                    self._check_checkpoint_exists(checkpoint_path)
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Loading checkpoint (local): {checkpoint_path}")
                    log.info(f"Loading checkpoint (local): {checkpoint_path}")
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dicts_to_load[key] = torch.load(checkpoint_path, map_location=lambda storage, loc: stor...
                    state_dicts_to_load[key] = torch.load(checkpoint_path, map_location=lambda storage, loc: storage)
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.success(f"Complete loading checkpoint (local): {checkpoint_path}")
                    log.success(f"Complete loading checkpoint (local): {checkpoint_path}")
                # 中文说明：处理异常、清理资源或管理上下文；代码：except:
                except:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Loading checkpoint (local): {checkpoint_path}, Failed")
                    log.info(f"Loading checkpoint (local): {checkpoint_path}, Failed")

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
            # import pdb;pdb.set_trace()
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_load_checkpoint(model, state_dict=state_dicts_to_load)
            self.callbacks.on_load_checkpoint(model, state_dict=state_dicts_to_load)

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Load the state dicts.
            # Load the state dicts.
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("- Loading the model...")
            log.info("- Loading the model...")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_fsdp = True
            is_fsdp = True
            # 中文说明：根据条件选择执行分支；代码：if is_fsdp:
            if is_fsdp:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# If a model is wrapped with FSDP, its underlying weights will be DTensor.
                # If a model is wrapped with FSDP, its underlying weights will be DTensor.
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# However, Transformer Engine cannot load weights (the useless `extra_state`) into DTensor.
                # However, Transformer Engine cannot load weights (the useless `extra_state`) into DTensor.
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# So we need to first remove the attention operators from Transformer Engine.
                # So we need to first remove the attention operators from Transformer Engine.
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# It will work correctly as long as the attention operators do not have any weights.
                # It will work correctly as long as the attention operators do not have any weights.
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for block in model.pipe.dit.blocks:
                for block in model.pipe.dit.blocks:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block.self_attn.attn = None
                    block.self_attn.attn = None
                
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dicts_to_load_for_dit_ctrl = collections.OrderedDict()
                state_dicts_to_load_for_dit_ctrl = collections.OrderedDict()
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dicts_to_load_for_dit_reg = collections.OrderedDict()
                state_dicts_to_load_for_dit_reg = collections.OrderedDict()
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dicts_to_load_for_dit_ema = collections.OrderedDict()
                state_dicts_to_load_for_dit_ema = collections.OrderedDict()
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dicts_to_load_for_dit_ldm = collections.OrderedDict()
                state_dicts_to_load_for_dit_ldm = collections.OrderedDict()
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key, val in state_dicts_to_load["model"].items():
                for key, val in state_dicts_to_load["model"].items():
                    # 中文说明：根据条件选择执行分支；代码：if key.startswith("net."):
                    if key.startswith("net."):
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dicts_to_load_for_dit_reg[key.replace("net.", "")] = val
                        state_dicts_to_load_for_dit_reg[key.replace("net.", "")] = val
                    # 中文说明：根据条件选择执行分支；代码：elif key.startswith("net_ema."):
                    elif key.startswith("net_ema."):
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dicts_to_load_for_dit_ema[key.replace("net_ema.", "")] = val
                        state_dicts_to_load_for_dit_ema[key.replace("net_ema.", "")] = val
                    # 中文说明：根据条件选择执行分支；代码：elif key.startswith("ldm_net."):
                    elif key.startswith("ldm_net."):
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dicts_to_load_for_dit_ldm[key.replace("ldm_net.", "")] = val
                        state_dicts_to_load_for_dit_ldm[key.replace("ldm_net.", "")] = val
                    # 中文说明：根据条件选择执行分支；代码：elif key.startswith("net_ctrl"):
                    elif key.startswith("net_ctrl"):
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dicts_to_load_for_dit_ctrl[key.replace("net_ctrl.", "")] = val
                        state_dicts_to_load_for_dit_ctrl[key.replace("net_ctrl.", "")] = val
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Load Regular weights.
                # Load Regular weights.
               
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：set_model_state_dict(
                set_model_state_dict(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model.pipe.dit,
                    model.pipe.dit,
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：state_dicts_to_load_for_dit_reg,
                    state_dicts_to_load_for_dit_reg,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：options=StateDictOptions(
                    options=StateDictOptions(
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：full_state_dict=True,
                        full_state_dict=True,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：broadcast_from_rank0=True,
                        broadcast_from_rank0=True,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：strict=False if model.config.train_architecture == "lora" else True,
                        strict=False if model.config.train_architecture == "lora" else True,
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
                    ),
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Load Regular weights.
                # Load Regular weights.
                # 中文说明：开始一个可捕获异常的代码块；代码：try:
                try:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：set_model_state_dict(
                    set_model_state_dict(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model.ldm_net,
                        model.ldm_net,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：state_dicts_to_load_for_dit_ldm,
                        state_dicts_to_load_for_dit_ldm,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：options=StateDictOptions(
                        options=StateDictOptions(
                            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：full_state_dict=True,
                            full_state_dict=True,
                            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：broadcast_from_rank0=True,
                            broadcast_from_rank0=True,
                            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：strict=False,
                            strict=False,
                        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
                        ),
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                # 中文说明：处理异常、清理资源或管理上下文；代码：except:
                except:
                    # 中文说明：执行循环控制或空操作；代码：pass
                    pass

                # 中文说明：开始一个可捕获异常的代码块；代码：try:
                try:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：set_model_state_dict(
                    set_model_state_dict(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model.pipe.dit_ctrl,
                        model.pipe.dit_ctrl,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：state_dicts_to_load_for_dit_ctrl,
                        state_dicts_to_load_for_dit_ctrl,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：options=StateDictOptions(
                        options=StateDictOptions(
                            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：full_state_dict=True,
                            full_state_dict=True,
                            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：broadcast_from_rank0=True,
                            broadcast_from_rank0=True,
                            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：strict=False,
                            strict=False,
                        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
                        ),
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                # 中文说明：处理异常、清理资源或管理上下文；代码：except:
                except:
                    # 中文说明：执行循环控制或空操作；代码：pass
                    pass


                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Load EMA weights.
                # Load EMA weights.
                # 中文说明：根据条件选择执行分支；代码：if model.pipe.config.ema.enabled:
                if model.pipe.config.ema.enabled:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：set_model_state_dict(
                    set_model_state_dict(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model.pipe.dit_ema,
                        model.pipe.dit_ema,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：state_dicts_to_load_for_dit_ema,
                        state_dicts_to_load_for_dit_ema,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：options=StateDictOptions(
                        options=StateDictOptions(
                            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：full_state_dict=True,
                            full_state_dict=True,
                            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：broadcast_from_rank0=True,
                            broadcast_from_rank0=True,
                            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：strict=False if model.config.train_architecture == "lora" else True,
                            strict=False if model.config.train_architecture == "lora" else True,
                        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
                        ),
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )

                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Restore the attention operators.
                # Restore the attention operators.
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model.pipe.apply_cp()
                model.pipe.apply_cp()
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model.load_state_dict(state_dicts_to_load["model"], strict=self.strict_resume)
                model.load_state_dict(state_dicts_to_load["model"], strict=self.strict_resume)
            
            # 中文说明：开始一个可捕获异常的代码块；代码：try:
            try:
                # 中文说明：根据条件选择执行分支；代码：if resume or only_resume_scheduler:
                if resume or only_resume_scheduler:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iteration = state_dicts_to_load["trainer"]["iteration"]
                    iteration = state_dicts_to_load["trainer"]["iteration"]
                    # 中文说明：检查运行时假设是否成立；代码：assert scheduler
                    assert scheduler
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("- Loading the scheduler...")
                    log.info("- Loading the scheduler...")
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scheduler.load_state_dict(state_dicts_to_load["scheduler"])
                    scheduler.load_state_dict(state_dicts_to_load["scheduler"])
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scheduler.last_epoch = iteration
                    scheduler.last_epoch = iteration
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iteration = 0
                    iteration = 0
            # 中文说明：处理异常、清理资源或管理上下文；代码：except:
            except:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iteration = 0
                iteration = 0
            
            # 中文说明：开始一个可捕获异常的代码块；代码：try:
            try:
                # 中文说明：根据条件选择执行分支；代码：if resume:
                if resume:
                    # 中文说明：检查运行时假设是否成立；代码：assert optimizer
                    assert optimizer
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("- Loading the optimizer...")
                    log.info("- Loading the optimizer...")
                    # 中文说明：根据条件选择执行分支；代码：if is_fsdp:
                    if is_fsdp:
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：set_optimizer_state_dict(
                        set_optimizer_state_dict(
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model,
                            model,
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：optimizer,
                            optimizer,
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：state_dicts_to_load["optim"],
                            state_dicts_to_load["optim"],
                            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：options=StateDictOptions(
                            options=StateDictOptions(
                                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：full_state_dict=True,
                                full_state_dict=True,
                                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：broadcast_from_rank0=True,
                                broadcast_from_rank0=True,
                            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
                            ),
                        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                        )
                    # 中文说明：根据条件选择执行分支；代码：else:
                    else:
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：optimizer.load_state_dict(state_dicts_to_load["optim"])
                        optimizer.load_state_dict(state_dicts_to_load["optim"])
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("- Loading the gradient scaler...")
                    log.info("- Loading the gradient scaler...")
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：grad_scaler.load_state_dict(state_dicts_to_load["trainer"]["grad_scaler"])
                    grad_scaler.load_state_dict(state_dicts_to_load["trainer"]["grad_scaler"])
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.success(f"Done with loading the checkpoint (iteration {iteration}).")
                    log.success(f"Done with loading the checkpoint (iteration {iteration}).")
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.success("Done with loading the checkpoint.")
                    log.success("Done with loading the checkpoint.")
            # 中文说明：处理异常、清理资源或管理上下文；代码：except:
            except:
                # 中文说明：执行循环控制或空操作；代码：pass
                pass
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iteration = 0
            iteration = 0
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("Training from scratch.")
            log.info("Training from scratch.")
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.empty_cache()
        torch.cuda.empty_cache()

        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_load_checkpoint_end(model, iteration=iteration, checkpoint_path=model_check...
        self.callbacks.on_load_checkpoint_end(model, iteration=iteration, checkpoint_path=model_checkpoint_path)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return iteration
        return iteration

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _read_latest_checkpoint_file(self) -> str | None:
    def _read_latest_checkpoint_file(self) -> str | None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Get the file name of the latest saved checkpoint. If it doesn't exist, return None.
        """Get the file name of the latest saved checkpoint. If it doesn't exist, return None.

        Returns:
            checkpoint_file (str | None): file name of the latest saved checkpoint.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint_file = None
        checkpoint_file = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：latest_path = os.path.join(self.checkpoint_dir_local, "latest_checkpoint.txt")
        latest_path = os.path.join(self.checkpoint_dir_local, "latest_checkpoint.txt")
        # 中文说明：根据条件选择执行分支；代码：if os.path.isfile(latest_path):
        if os.path.isfile(latest_path):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint_file = open(latest_path).read().strip()
            checkpoint_file = open(latest_path).read().strip()
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return checkpoint_file
        return checkpoint_file

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _write_latest_checkpoint_file(self, checkpoint_file: str) -> None:
    def _write_latest_checkpoint_file(self, checkpoint_file: str) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Track the file name of the latest saved checkpoint.
        """Track the file name of the latest saved checkpoint.

        Args:
            checkpoint_file (str): file name of the latest saved checkpoint.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：content = f"{checkpoint_file}\n"
        content = f"{checkpoint_file}\n"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：latest_path = os.path.join(self.checkpoint_dir_local, "latest_checkpoint.txt")
        latest_path = os.path.join(self.checkpoint_dir_local, "latest_checkpoint.txt")
        # 中文说明：处理异常、清理资源或管理上下文；代码：with open(latest_path, "w") as file:
        with open(latest_path, "w") as file:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：file.write(content)
            file.write(content)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _check_checkpoint_exists(self, checkpoint_path: str) -> None:
    def _check_checkpoint_exists(self, checkpoint_path: str) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""If the file checkpoint_path does not exist, raise an error.
        """If the file checkpoint_path does not exist, raise an error.

        Args:
            checkpoint_path (str): full path to the checkpoint.
        """
        # 中文说明：根据条件选择执行分支；代码：if not os.path.exists(checkpoint_path):
        if not os.path.exists(checkpoint_path):
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise FileNotFoundError(f"File not found (local): {checkpoint_path}")
            raise FileNotFoundError(f"File not found (local): {checkpoint_path}")

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def finalize(self) -> None:
    def finalize(self) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Finalize the checkpointer."""
        """Finalize the checkpointer."""
        # 中文说明：根据条件选择执行分支；代码：if self.save_thread:
        if self.save_thread:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.save_thread.join()
            self.save_thread.join()
