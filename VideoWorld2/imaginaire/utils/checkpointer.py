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

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import threading
import threading
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import TYPE_CHECKING
from typing import TYPE_CHECKING

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch

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

        # 中文说明：根据条件选择执行分支；代码：if distributed.get_rank() == 0:
        if distributed.get_rank() == 0:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dict = dict(
            state_dict = dict(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model=model.state_dict(),
                model=model.state_dict(),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：optimizer=optimizer.state_dict(),
                optimizer=optimizer.state_dict(),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scheduler=scheduler.state_dict(),
                scheduler=scheduler.state_dict(),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：grad_scaler=grad_scaler.state_dict(),
                grad_scaler=grad_scaler.state_dict(),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iteration=iteration,
                iteration=iteration,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dict = misc.to(state_dict, device="cpu")
            state_dict = misc.to(state_dict, device="cpu")
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_save_checkpoint(model, state_dict=state_dict)
            self.callbacks.on_save_checkpoint(model, state_dict=state_dict)
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Wait for previous saver thread to end.
            # Wait for previous saver thread to end.
            # 中文说明：根据条件选择执行分支；代码：if self.save_thread:
            if self.save_thread:
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.save_thread.join()
                self.save_thread.join()
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Run the checkpoint saver in a separate thread.
            # Run the checkpoint saver in a separate thread.
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.save_thread = threading.Thread(
            self.save_thread = threading.Thread(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：target=self._save_worker_local,
                target=self._save_worker_local,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：daemon=False,
                daemon=False,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：args=(state_dict, checkpoint_file, distributed.get_rank()),
                args=(state_dict, checkpoint_file, distributed.get_rank()),
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
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _save_worker_local(self, state_dict: dict[str, torch.Tensor], checkpoint_file: str, rank:...
    def _save_worker_local(self, state_dict: dict[str, torch.Tensor], checkpoint_file: str, rank: int = 0) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Worker to save checkpoint to local disk, spawned with a child thread (runs in parallel wit...
        """Worker to save checkpoint to local disk, spawned with a child thread (runs in parallel with the training).

        Args:
            state_dict (dict[str, torch.Tensor]): The state dict of the model/optimizer/scheduler.
            checkpoint_file (str): The file name of the model checkpoint.
            rank (int): GPU device (default: 0).
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint_path = os.path.join(self.checkpoint_dir_local, checkpoint_file)
        checkpoint_path = os.path.join(self.checkpoint_dir_local, checkpoint_file)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.makedirs(self.checkpoint_dir_local, exist_ok=True)
        os.makedirs(self.checkpoint_dir_local, exist_ok=True)
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
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_load_checkpoint_start(model)
        self.callbacks.on_load_checkpoint_start(model)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：latest_checkpoint_file = self._read_latest_checkpoint_file()
        latest_checkpoint_file = self._read_latest_checkpoint_file()
        # 中文说明：根据条件选择执行分支；代码：if latest_checkpoint_file is not None:
        if latest_checkpoint_file is not None:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 1. Resume training from latest_checkpoint.txt under the same name.
            # 1. Resume training from latest_checkpoint.txt under the same name.
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint_dir = self.checkpoint_dir_local
            checkpoint_dir = self.checkpoint_dir_local
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint_path = os.path.join(checkpoint_dir, latest_checkpoint_file)
            checkpoint_path = os.path.join(checkpoint_dir, latest_checkpoint_file)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resume = True
            resume = True
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：only_resume_scheduler = True
            only_resume_scheduler = True
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：根据条件选择执行分支；代码：if self.load_path:
            if self.load_path:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 2. Load the module weights specified by config_checkpoint.path.
                # 2. Load the module weights specified by config_checkpoint.path.
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint_path = self.load_path
                checkpoint_path = self.load_path
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resume = self.load_training_state
                resume = self.load_training_state
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：only_resume_scheduler = self.only_load_scheduler_state
                only_resume_scheduler = self.only_load_scheduler_state
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 3. Randomly initialize the model parameters and train from scratch.
                # 3. Randomly initialize the model parameters and train from scratch.
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint_path = None
                checkpoint_path = None
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resume = False
                resume = False
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：only_resume_scheduler = False
                only_resume_scheduler = False
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Load checkpoint.
        # Load checkpoint.
        # 中文说明：根据条件选择执行分支；代码：if checkpoint_path is not None:
        if checkpoint_path is not None:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._check_checkpoint_exists(checkpoint_path)
            self._check_checkpoint_exists(checkpoint_path)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Loading checkpoint (local): {checkpoint_path}")
            log.info(f"Loading checkpoint (local): {checkpoint_path}")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dict = torch.load(checkpoint_path, map_location=lambda storage, loc: storage)
            state_dict = torch.load(checkpoint_path, map_location=lambda storage, loc: storage)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.success(f"Complete loading checkpoint (local): {checkpoint_path}")
            log.success(f"Complete loading checkpoint (local): {checkpoint_path}")
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_load_checkpoint(model, state_dict=state_dict)
            self.callbacks.on_load_checkpoint(model, state_dict=state_dict)
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Load the state dicts.
            # Load the state dicts.
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("- Loading the model...")
            log.info("- Loading the model...")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model.load_state_dict(state_dict["model"], strict=self.strict_resume)
            model.load_state_dict(state_dict["model"], strict=self.strict_resume)
            # 中文说明：根据条件选择执行分支；代码：if resume or only_resume_scheduler:
            if resume or only_resume_scheduler:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iteration = state_dict["iteration"]
                iteration = state_dict["iteration"]
                # 中文说明：检查运行时假设是否成立；代码：assert scheduler
                assert scheduler
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("- Loading the scheduler...")
                log.info("- Loading the scheduler...")
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scheduler.load_state_dict(state_dict["scheduler"])
                scheduler.load_state_dict(state_dict["scheduler"])
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scheduler.last_epoch = iteration
                scheduler.last_epoch = iteration
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iteration = 0
                iteration = 0
            # 中文说明：根据条件选择执行分支；代码：if resume:
            if resume:
                # 中文说明：检查运行时假设是否成立；代码：assert optimizer
                assert optimizer
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("- Loading the optimizer...")
                log.info("- Loading the optimizer...")
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：optimizer.load_state_dict(state_dict["optimizer"])
                optimizer.load_state_dict(state_dict["optimizer"])
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("- Loading the gradient scaler...")
                log.info("- Loading the gradient scaler...")
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：grad_scaler.load_state_dict(state_dict["grad_scaler"])
                grad_scaler.load_state_dict(state_dict["grad_scaler"])
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.success(f"Done with loading the checkpoint (iteration {iteration}).")
                log.success(f"Done with loading the checkpoint (iteration {iteration}).")
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.success("Done with loading the checkpoint.")
                log.success("Done with loading the checkpoint.")
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Checkpoint not found and not specified. We will train everything from scratch.
            # Checkpoint not found and not specified. We will train everything from scratch.
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iteration = 0
            iteration = 0
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("Training from scratch.")
            log.info("Training from scratch.")
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.empty_cache()
        torch.cuda.empty_cache()

        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_load_checkpoint_end(model, iteration=iteration, checkpoint_path=checkpoint_...
        self.callbacks.on_load_checkpoint_end(model, iteration=iteration, checkpoint_path=checkpoint_path)

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
