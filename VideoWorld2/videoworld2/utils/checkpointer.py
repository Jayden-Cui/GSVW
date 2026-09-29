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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import List, NamedTuple, Tuple
from typing import List, NamedTuple, Tuple

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.model import ImaginaireModel
from imaginaire.model import ImaginaireModel
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import distributed, log, misc
from imaginaire.utils import distributed, log, misc
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.checkpointer import Checkpointer as BaseCheckpointer
from imaginaire.utils.checkpointer import Checkpointer as BaseCheckpointer

# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：TORCH_VERSION: Tuple[int, ...] = tuple(int(x) for x in torch.__version__.split(".")[:2])
TORCH_VERSION: Tuple[int, ...] = tuple(int(x) for x in torch.__version__.split(".")[:2])
# 中文说明：根据条件选择执行分支；代码：if TORCH_VERSION >= (1, 11):
if TORCH_VERSION >= (1, 11):
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.ao import quantization
    from torch.ao import quantization
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.ao.quantization import FakeQuantizeBase, ObserverBase
    from torch.ao.quantization import FakeQuantizeBase, ObserverBase
# 中文说明：根据条件选择执行分支；代码：elif (
elif (
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：TORCH_VERSION >= (1, 8)
    TORCH_VERSION >= (1, 8)
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：and hasattr(torch.quantization, "FakeQuantizeBase")
    and hasattr(torch.quantization, "FakeQuantizeBase")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：and hasattr(torch.quantization, "ObserverBase")
    and hasattr(torch.quantization, "ObserverBase")
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch import quantization
    from torch import quantization
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.quantization import FakeQuantizeBase, ObserverBase
    from torch.quantization import FakeQuantizeBase, ObserverBase


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class _IncompatibleKeys(
class _IncompatibleKeys(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：NamedTuple(
    NamedTuple(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："IncompatibleKeys",
        "IncompatibleKeys",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：[
        [
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：("missing_keys", List[str]),
            ("missing_keys", List[str]),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：("unexpected_keys", List[str]),
            ("unexpected_keys", List[str]),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：("incorrect_shapes", List[Tuple[str, Tuple[int], Tuple[int]]]),
            ("incorrect_shapes", List[Tuple[str, Tuple[int], Tuple[int]]]),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：],
        ],
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：执行循环控制或空操作；代码：pass
    pass


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class MultiRankCheckpointer(BaseCheckpointer):
class MultiRankCheckpointer(BaseCheckpointer):
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
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# checkpoint_file = f"iter_{iteration:09}.pt"
        # checkpoint_file = f"iter_{iteration:09}.pt"
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：postfix, _, total_ema_num = model.get_ckpt_postfix()
        postfix, _, total_ema_num = model.get_ckpt_postfix()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint_file = f"iter_{iteration:09}{postfix}.pt"
        checkpoint_file = f"iter_{iteration:09}{postfix}.pt"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：save_ranks = list(range(total_ema_num))
        save_ranks = list(range(total_ema_num))
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _rank in save_ranks:
        for _rank in save_ranks:
            # 中文说明：根据条件选择执行分支；代码：if distributed.get_rank() == _rank:
            if distributed.get_rank() == _rank:
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
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：latest_checkpoint_file = self._read_latest_checkpoint_file()
        latest_checkpoint_file = self._read_latest_checkpoint_file()
        # 中文说明：根据条件选择执行分支；代码：if latest_checkpoint_file is not None:
        if latest_checkpoint_file is not None:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# different from base checkpointer, this support multi-EMA
            # different from base checkpointer, this support multi-EMA
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：postfix, _, total_ema_num = model.get_ckpt_postfix()
            postfix, _, total_ema_num = model.get_ckpt_postfix()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：latest_checkpoint_file = latest_checkpoint_file.replace(".pt", f"{postfix}.pt")
            latest_checkpoint_file = latest_checkpoint_file.replace(".pt", f"{postfix}.pt")
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 1. Resume training from latest_checkpoint.txt under the same name.
            # 1. Resume training from latest_checkpoint.txt under the same name.
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint_dir = self.checkpoint_dir_local
            checkpoint_dir = self.checkpoint_dir_local
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint_path = os.path.join(checkpoint_dir, latest_checkpoint_file)
            checkpoint_path = os.path.join(checkpoint_dir, latest_checkpoint_file)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resume = True
            resume = True
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：根据条件选择执行分支；代码：if self.load_path:
            if self.load_path:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 2. Load the module weights specified by config_checkpoint.path.
                # 2. Load the module weights specified by config_checkpoint.path.
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint_path = self.load_path
                checkpoint_path = self.load_path
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# different from base checkpointer, this support multi-EMA
                # different from base checkpointer, this support multi-EMA
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：postfix, _, total_ema_num = model.get_ckpt_postfix()
                postfix, _, total_ema_num = model.get_ckpt_postfix()
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint_path = checkpoint_path.replace(".pt", f"{postfix}.pt")
                checkpoint_path = checkpoint_path.replace(".pt", f"{postfix}.pt")
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resume = self.load_training_state
                resume = self.load_training_state
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 3. Randomly initialize the model parameters and train from scratch.
                # 3. Randomly initialize the model parameters and train from scratch.
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint_path = None
                checkpoint_path = None
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resume = False
                resume = False
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
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.critical(model.load_state_dict(state_dict["model"], strict=self.strict_resume))
            log.critical(model.load_state_dict(state_dict["model"], strict=self.strict_resume))
            # 中文说明：根据条件选择执行分支；代码：if resume:
            if resume:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iteration = state_dict["iteration"]
                iteration = state_dict["iteration"]
                # 中文说明：检查运行时假设是否成立；代码：assert optimizer and scheduler
                assert optimizer and scheduler
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("- Loading the optimizer...")
                log.info("- Loading the optimizer...")
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：optimizer.load_state_dict(state_dict["optimizer"])
                optimizer.load_state_dict(state_dict["optimizer"])
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("- Loading the scheduler...")
                log.info("- Loading the scheduler...")
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scheduler.load_state_dict(state_dict["scheduler"])
                scheduler.load_state_dict(state_dict["scheduler"])
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scheduler.last_epoch = iteration
                scheduler.last_epoch = iteration
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("- Loading the gradient scaler...")
                log.info("- Loading the gradient scaler...")
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：grad_scaler.load_state_dict(state_dict["grad_scaler"])
                grad_scaler.load_state_dict(state_dict["grad_scaler"])
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.success(f"Done with loading the checkpoint (iteration {iteration}).")
                log.success(f"Done with loading the checkpoint (iteration {iteration}).")
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iteration = 0
                iteration = 0
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
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return iteration
        return iteration


# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# https://github.com/facebookresearch/fvcore/blob/9d683aae73fb899dd35d6cf6720e5ef567761c57/fv...
# https://github.com/facebookresearch/fvcore/blob/9d683aae73fb899dd35d6cf6720e5ef567761c57/fvcore/common/checkpoint.py
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def non_strict_load_model(model: torch.nn.Module, checkpoint_state_dict: dict) -> _Incompatib...
def non_strict_load_model(model: torch.nn.Module, checkpoint_state_dict: dict) -> _IncompatibleKeys:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# workaround https://github.com/pytorch/pytorch/issues/24139
    # workaround https://github.com/pytorch/pytorch/issues/24139
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_state_dict = model.state_dict()
    model_state_dict = model.state_dict()
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：incorrect_shapes = []
    incorrect_shapes = []
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for k in list(checkpoint_state_dict.keys()):
    for k in list(checkpoint_state_dict.keys()):
        # 中文说明：根据条件选择执行分支；代码：if k in model_state_dict:
        if k in model_state_dict:
            # 中文说明：根据条件选择执行分支；代码：if "_extra_state" in k: # Key introduced by TransformerEngine for FP8
            if "_extra_state" in k:  # Key introduced by TransformerEngine for FP8
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(f"Skipping key {k} introduced by TransformerEngine for FP8 in the checkpoint.")
                log.warning(f"Skipping key {k} introduced by TransformerEngine for FP8 in the checkpoint.")
                # 中文说明：执行循环控制或空操作；代码：continue
                continue
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_param = model_state_dict[k]
            model_param = model_state_dict[k]
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Allow mismatch for uninitialized parameters
            # Allow mismatch for uninitialized parameters
            # 中文说明：根据条件选择执行分支；代码：if TORCH_VERSION >= (1, 8) and isinstance(model_param, torch.nn.parameter.UninitializedParame...
            if TORCH_VERSION >= (1, 8) and isinstance(model_param, torch.nn.parameter.UninitializedParameter):
                # 中文说明：执行循环控制或空操作；代码：continue
                continue
            # 中文说明：根据条件选择执行分支；代码：if not isinstance(model_param, torch.Tensor):
            if not isinstance(model_param, torch.Tensor):
                # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(
                raise ValueError(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Find non-tensor parameter {k} in the model. type: {type(model_param)} {type(checkpoint_stat...
                    f"Find non-tensor parameter {k} in the model. type: {type(model_param)} {type(checkpoint_state_dict[k])}, please check if this key is safe to skip or not."
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：shape_model = tuple(model_param.shape)
            shape_model = tuple(model_param.shape)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：shape_checkpoint = tuple(checkpoint_state_dict[k].shape)
            shape_checkpoint = tuple(checkpoint_state_dict[k].shape)
            # 中文说明：根据条件选择执行分支；代码：if shape_model != shape_checkpoint:
            if shape_model != shape_checkpoint:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：has_observer_base_classes = (
                has_observer_base_classes = (
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：TORCH_VERSION >= (1, 8)
                    TORCH_VERSION >= (1, 8)
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：and hasattr(quantization, "ObserverBase")
                    and hasattr(quantization, "ObserverBase")
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：and hasattr(quantization, "FakeQuantizeBase")
                    and hasattr(quantization, "FakeQuantizeBase")
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：根据条件选择执行分支；代码：if has_observer_base_classes:
                if has_observer_base_classes:
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Handle the special case of quantization per channel observers,
                    # Handle the special case of quantization per channel observers,
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# where buffer shape mismatches are expected.
                    # where buffer shape mismatches are expected.
                    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _get_module_for_key(model: torch.nn.Module, key: str) -> torch.nn.Module:
                    def _get_module_for_key(model: torch.nn.Module, key: str) -> torch.nn.Module:
                        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# foo.bar.param_or_buffer_name -> [foo, bar]
                        # foo.bar.param_or_buffer_name -> [foo, bar]
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：key_parts = key.split(".")[:-1]
                        key_parts = key.split(".")[:-1]
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cur_module = model
                        cur_module = model
                        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key_part in key_parts:
                        for key_part in key_parts:
                            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cur_module = getattr(cur_module, key_part)
                            cur_module = getattr(cur_module, key_part)
                        # 中文说明：从当前函数返回结果或结束函数执行；代码：return cur_module
                        return cur_module

                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cls_to_skip = (
                    cls_to_skip = (
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ObserverBase,
                        ObserverBase,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：FakeQuantizeBase,
                        FakeQuantizeBase,
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：target_module = _get_module_for_key(model, k)
                    target_module = _get_module_for_key(model, k)
                    # 中文说明：根据条件选择执行分支；代码：if isinstance(target_module, cls_to_skip):
                    if isinstance(target_module, cls_to_skip):
                        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Do not remove modules with expected shape mismatches
                        # Do not remove modules with expected shape mismatches
                        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# them from the state_dict loading. They have special logic
                        # them from the state_dict loading. They have special logic
                        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# in _load_from_state_dict to handle the mismatches.
                        # in _load_from_state_dict to handle the mismatches.
                        # 中文说明：执行循环控制或空操作；代码：continue
                        continue

                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：incorrect_shapes.append((k, shape_checkpoint, shape_model))
                incorrect_shapes.append((k, shape_checkpoint, shape_model))
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：checkpoint_state_dict.pop(k)
                checkpoint_state_dict.pop(k)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：incompatible = model.load_state_dict(checkpoint_state_dict, strict=False)
    incompatible = model.load_state_dict(checkpoint_state_dict, strict=False)
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Remove keys with "_extra_state" suffix, which are non-parameter items introduced by Transfo...
    # Remove keys with "_extra_state" suffix, which are non-parameter items introduced by TransformerEngine for FP8 handling
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：missing_keys = [k for k in incompatible.missing_keys if "_extra_state" not in k]
    missing_keys = [k for k in incompatible.missing_keys if "_extra_state" not in k]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：unexpected_keys = [k for k in incompatible.unexpected_keys if "_extra_state" not in k]
    unexpected_keys = [k for k in incompatible.unexpected_keys if "_extra_state" not in k]
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return _IncompatibleKeys(
    return _IncompatibleKeys(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：missing_keys=missing_keys,
        missing_keys=missing_keys,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：unexpected_keys=unexpected_keys,
        unexpected_keys=unexpected_keys,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：incorrect_shapes=incorrect_shapes,
        incorrect_shapes=incorrect_shapes,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
