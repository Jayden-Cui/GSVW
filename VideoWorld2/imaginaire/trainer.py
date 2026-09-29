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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import functools
import functools
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import inspect
import inspect
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import signal
import signal
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from tqdm import tqdm
from tqdm import tqdm

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.distributed as dist
import torch.distributed as dist
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.utils.data
import torch.utils.data

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.profiling import maybe_enable_memory_snapshot, maybe_enable_profiling
from imaginaire.utils.profiling import maybe_enable_memory_snapshot, maybe_enable_profiling

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
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print("Megatron-core is not installed.")
    print("Megatron-core is not installed.")


# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import LazyConfig, instantiate
from imaginaire.lazy_config import LazyConfig, instantiate
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.model import ImaginaireModel
from imaginaire.model import ImaginaireModel
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import callback, distributed, ema, log, misc
from imaginaire.utils import callback, distributed, ema, log, misc
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.checkpointer import Checkpointer
from imaginaire.utils.checkpointer import Checkpointer


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ImaginaireTrainer:
class ImaginaireTrainer:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""The base trainer class of Imaginaire.
    """The base trainer class of Imaginaire.

    All trainers in Imaginaire should inherit ImaginaireTrainer. It contains the basic functionality for model training
    (particularly suited for large-scale training), including data parallel (DDP/FSDP), model weight average (EMA),
    mixed-precision training (fp16/bf16).

    Attributes:
        checkpointer (Checkpointer): checkpointer object to save/load model weights and optimizer states.
        training_timer (misc.Timer): Timer object to time code blocks and functions.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, config):
    def __init__(self, config):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Constructor of the trainer.
        """Constructor of the trainer.

        Args:
            config (Config): The config object for the Imaginaire codebase.
        """
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.config = config
        self.config = config
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Set up the distributed computing environment.
        # Set up the distributed computing environment.
        # 中文说明：处理异常、清理资源或管理上下文；代码：with misc.timer("init_distributed"):
        with misc.timer("init_distributed"):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：distributed.init()
            distributed.init()
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Set up parallel states.
            # Set up parallel states.
            # 中文说明：根据条件选择执行分支；代码：if hasattr(config.model, "context_parallel_size"):
            if hasattr(config.model, "context_parallel_size"):
                # 中文说明：根据条件选择执行分支；代码：if config.model_parallel.context_parallel_size > 1:
                if config.model_parallel.context_parallel_size > 1:
                    # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(
                    raise ValueError(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："Both config.model.context_parallel_size and config.model_parallel.context_parallel_size are ...
                        "Both config.model.context_parallel_size and config.model_parallel.context_parallel_size are set. "
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："config.model.context_parallel_size is deprecated. Please only set config.model_parallel.cont...
                        "config.model.context_parallel_size is deprecated. Please only set config.model_parallel.context_parallel_size."
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.critical(
                    log.critical(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："Using deprecated config.model.context_parallel_size. Please use config.model_parallel.contex...
                        "Using deprecated config.model.context_parallel_size. Please use config.model_parallel.context_parallel_size instead."
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config.model_parallel.context_parallel_size = config.model.context_parallel_size
                    config.model_parallel.context_parallel_size = config.model.context_parallel_size
            # 中文说明：根据条件选择执行分支；代码：if USE_MEGATRON:
            if USE_MEGATRON:
                # 中文说明：根据条件选择执行分支；代码：if (
                if (
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："create_gloo_process_groups"
                    "create_gloo_process_groups"
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：in inspect.signature(parallel_state.initialize_model_parallel).parameters
                    in inspect.signature(parallel_state.initialize_model_parallel).parameters
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
                ):
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parallel_state.initialize_model_parallel(
                    parallel_state.initialize_model_parallel(
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipeline_model_parallel_size=config.model_parallel.pipeline_model_parallel_size,
                        pipeline_model_parallel_size=config.model_parallel.pipeline_model_parallel_size,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tensor_model_parallel_size=config.model_parallel.tensor_model_parallel_size,
                        tensor_model_parallel_size=config.model_parallel.tensor_model_parallel_size,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：context_parallel_size=config.model_parallel.context_parallel_size,
                        context_parallel_size=config.model_parallel.context_parallel_size,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：create_gloo_process_groups=False,
                        create_gloo_process_groups=False,
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parallel_state.initialize_model_parallel(
                    parallel_state.initialize_model_parallel(
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipeline_model_parallel_size=config.model_parallel.pipeline_model_parallel_size,
                        pipeline_model_parallel_size=config.model_parallel.pipeline_model_parallel_size,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tensor_model_parallel_size=config.model_parallel.tensor_model_parallel_size,
                        tensor_model_parallel_size=config.model_parallel.tensor_model_parallel_size,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：context_parallel_size=config.model_parallel.context_parallel_size,
                        context_parallel_size=config.model_parallel.context_parallel_size,
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# `config.model_parallel.sequence_parallel` is a bool that indicates whether to use sequence ...
                # `config.model_parallel.sequence_parallel` is a bool that indicates whether to use sequence parallelism.
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# It is not part of the original `parallel_state` API, so we need to set it manually.
                # It is not part of the original `parallel_state` API, so we need to set it manually.
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：parallel_state.sequence_parallel = config.model_parallel.sequence_parallel
                parallel_state.sequence_parallel = config.model_parallel.sequence_parallel
                # 中文说明：根据条件选择执行分支；代码：if parallel_state.sequence_parallel:
                if parallel_state.sequence_parallel:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：os.environ["CUDA_DEVICE_MAX_CONNECTIONS"] = "1"
                    os.environ["CUDA_DEVICE_MAX_CONNECTIONS"] = "1"

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Create the local job directory, save the config file, and pipe to a local log.
        # Create the local job directory, save the config file, and pipe to a local log.
        # 中文说明：根据条件选择执行分支；代码：if distributed.is_rank0():
        if distributed.is_rank0():
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.makedirs(config.job.path_local, exist_ok=True)
            os.makedirs(config.job.path_local, exist_ok=True)
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Save the config as .pkl for reproducibility.
            # Save the config as .pkl for reproducibility.
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：LazyConfig.save_pkl(config, f"{config.job.path_local}/config.pkl")
            LazyConfig.save_pkl(config, f"{config.job.path_local}/config.pkl")
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Save the config as .yaml for reading or parsing experiment hyperparameters.
            # Save the config as .yaml for reading or parsing experiment hyperparameters.
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：LazyConfig.save_yaml(config, f"{config.job.path_local}/config.yaml")
            LazyConfig.save_yaml(config, f"{config.job.path_local}/config.yaml")
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dist.barrier()
        dist.barrier()
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.init_loguru_file(f"{config.job.path_local}/stdout.log")
        log.init_loguru_file(f"{config.job.path_local}/stdout.log")
        # 中文说明：根据条件选择执行分支；代码：if distributed.is_rank0():
        if distributed.is_rank0():
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Print important environment variables and the effective config.
            # Print important environment variables and the effective config.
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("Config:\n" + config.pretty_print(use_color=True))
            log.info("Config:\n" + config.pretty_print(use_color=True))
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：misc.print_environ_variables(["TORCH_HOME", "IMAGINAIRE_OUTPUT_ROOT"])
        misc.print_environ_variables(["TORCH_HOME", "IMAGINAIRE_OUTPUT_ROOT"])
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Set the random seed. If multi-GPU, different ranks are set with different seeds.
        # Set the random seed. If multi-GPU, different ranks are set with different seeds.
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：misc.set_random_seed(seed=config.trainer.seed, by_rank=False)
        misc.set_random_seed(seed=config.trainer.seed, by_rank=False)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Initialize cuDNN.
        # Initialize cuDNN.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：torch.backends.cudnn.deterministic = config.trainer.cudnn.deterministic
        torch.backends.cudnn.deterministic = config.trainer.cudnn.deterministic
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：torch.backends.cudnn.benchmark = config.trainer.cudnn.benchmark
        torch.backends.cudnn.benchmark = config.trainer.cudnn.benchmark
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Floating-point precision settings.
        # Floating-point precision settings.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：torch.backends.cudnn.allow_tf32 = torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = torch.backends.cuda.matmul.allow_tf32 = True
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Initialize the callback functions.
        # Initialize the callback functions.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.callbacks = callback.CallBackGroup(config=config, trainer=self)
        self.callbacks = callback.CallBackGroup(config=config, trainer=self)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Initialize the model checkpointer.
        # Initialize the model checkpointer.
        # 中文说明：根据条件选择执行分支；代码：if config.checkpoint.type is None:
        if config.checkpoint.type is None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.checkpointer = Checkpointer(config.checkpoint, config.job, callbacks=self.callbacks)
            self.checkpointer = Checkpointer(config.checkpoint, config.job, callbacks=self.callbacks)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.checkpointer: Checkpointer = instantiate(
            self.checkpointer: Checkpointer = instantiate(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：config.checkpoint.type, config.checkpoint, config.job, callbacks=self.callbacks
                config.checkpoint.type, config.checkpoint, config.job, callbacks=self.callbacks
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Initialize the timer for speed benchmarking.
        # Initialize the timer for speed benchmarking.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.training_timer = misc.TrainingTimer()
        self.training_timer = misc.TrainingTimer()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Send a TimeoutError if a training step takes over timeout_period seconds.
        # Send a TimeoutError if a training step takes over timeout_period seconds.
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：signal.signal(signal.SIGALRM, functools.partial(misc.timeout_handler, config.trainer.timeout_...
        signal.signal(signal.SIGALRM, functools.partial(misc.timeout_handler, config.trainer.timeout_period))  # type: ignore

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def train(
    def train(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model: ImaginaireModel,
        model: ImaginaireModel,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dataloader_train: torch.utils.data.DataLoader,
        dataloader_train: torch.utils.data.DataLoader,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dataloader_val: torch.utils.data.DataLoader,
        dataloader_val: torch.utils.data.DataLoader,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""The training function.
        """The training function.

        Args:
            model (ImaginaireModel): The PyTorch model.
            dataloader_train (torch.utils.data.DataLoader): The training data loader.
            dataloader_val (torch.utils.data.DataLoader): The validation data loader.
        """
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Leaving this for backward compability for now, but we can think about moving this to model....
        # Leaving this for backward compability for now, but we can think about moving this to model.on_train_start for all models.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model = model.to("cuda", memory_format=self.config.trainer.memory_format) # type: ignore
        model = model.to("cuda", memory_format=self.config.trainer.memory_format)  # type: ignore
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model.on_train_start(self.config.trainer.memory_format)
        model.on_train_start(self.config.trainer.memory_format)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# for n, p in model.named_parameters():
        # for n, p in model.named_parameters():
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# print(n, p.requires_grad)
        #     print(n, p.requires_grad)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Initialize the optimizer, scheduler, and grad_scaler.
        # Initialize the optimizer, scheduler, and grad_scaler.
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_optimizer_init_start()
        self.callbacks.on_optimizer_init_start()
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：optimizer, scheduler = model.init_optimizer_scheduler(self.config.optimizer, self.config.sche...
        optimizer, scheduler = model.init_optimizer_scheduler(self.config.optimizer, self.config.scheduler)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：grad_scaler = torch.amp.GradScaler("cuda", **self.config.trainer.grad_scaler_args)
        grad_scaler = torch.amp.GradScaler("cuda", **self.config.trainer.grad_scaler_args)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_optimizer_init_end()
        self.callbacks.on_optimizer_init_end()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Load the model checkpoint and get the starting iteration number.
        # Load the model checkpoint and get the starting iteration number.
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iteration = self.checkpointer.load(model, optimizer, scheduler, grad_scaler)
        iteration = self.checkpointer.load(model, optimizer, scheduler, grad_scaler)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：grad_accum_iter = 0
        grad_accum_iter = 0
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.critical(f"Distributed parallelism mode: {self.config.trainer.distributed_parallelism}")
        log.critical(f"Distributed parallelism mode: {self.config.trainer.distributed_parallelism}")
        # 中文说明：根据条件选择执行分支；代码：if self.config.trainer.distributed_parallelism == "ddp":
        if self.config.trainer.distributed_parallelism == "ddp":
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Create a DDP model wrapper.
            # Create a DDP model wrapper.
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_ddp = distributed.parallel_model_wrapper(self.config.trainer.ddp, model)
            model_ddp = distributed.parallel_model_wrapper(self.config.trainer.ddp, model)
        # 中文说明：根据条件选择执行分支；代码：elif self.config.trainer.distributed_parallelism == "fsdp":
        elif self.config.trainer.distributed_parallelism == "fsdp":
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_ddp = model
            model_ddp = model
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Unknown distributed parallelism mode: {self.config.trainer.distributed_par...
            raise ValueError(f"Unknown distributed parallelism mode: {self.config.trainer.distributed_parallelism}")
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("Starting training...")
        log.info("Starting training...")
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_train_start(model, iteration=iteration)
        self.callbacks.on_train_start(model, iteration=iteration)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Initial validation.
        # Initial validation.
        # 中文说明：根据条件选择执行分支；代码：if self.config.trainer.run_validation:
        if self.config.trainer.run_validation:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.validate(model, dataloader_val, iteration=iteration)
            self.validate(model, dataloader_val, iteration=iteration)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_end_training = False
        _end_training = False
        # 中文说明：处理异常、清理资源或管理上下文；代码：with maybe_enable_profiling(self.config, global_step=iteration) as torch_profiler, maybe_enab...
        with maybe_enable_profiling(self.config, global_step=iteration) as torch_profiler, maybe_enable_memory_snapshot(
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.config, global_step=iteration
            self.config, global_step=iteration
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) as memory_profiler:
        ) as memory_profiler:
            # 中文说明：在条件成立时重复执行循环体；代码：while True:
            while True:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataloader_train_iter = iter(dataloader_train)
                dataloader_train_iter = iter(dataloader_train)
                # 中文说明：在条件成立时重复执行循环体；代码：while True:
                while True:
                    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_before_dataloading(iteration)
                    self.callbacks.on_before_dataloading(iteration)
                    # 中文说明：开始一个可捕获异常的代码块；代码：try:
                    try:
                        # 中文说明：处理异常、清理资源或管理上下文；代码：with self.training_timer("dataloader_train"):
                        with self.training_timer("dataloader_train"):
                            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch = next(dataloader_train_iter)
                            data_batch = next(dataloader_train_iter)
                    # 中文说明：处理异常、清理资源或管理上下文；代码：except StopIteration:
                    except StopIteration:
                        # 中文说明：执行循环控制或空操作；代码：break
                        break
                    # 中文说明：处理异常、清理资源或管理上下文；代码：finally:
                    finally:
                        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_after_dataloading(iteration)
                        self.callbacks.on_after_dataloading(iteration)
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# If max_iter is reached, exit the training loop.
                    # If max_iter is reached, exit the training loop.
                    # 中文说明：根据条件选择执行分支；代码：if iteration >= self.config.trainer.max_iter:
                    if iteration >= self.config.trainer.max_iter:
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_end_training = True
                        _end_training = True
                        # 中文说明：执行循环控制或空操作；代码：break
                        break
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Move all tensors in the data batch to GPU device.
                    # Move all tensors in the data batch to GPU device.
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch = misc.to(data_batch, device="cuda")
                    data_batch = misc.to(data_batch, device="cuda")
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# The actual training step.
                    # The actual training step.
                    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_training_step_start(model, data_batch, iteration=iteration)
                    self.callbacks.on_training_step_start(model, data_batch, iteration=iteration)
                    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_training_step_batch_start(model, data_batch, iteration=iteration)
                    self.callbacks.on_training_step_batch_start(model, data_batch, iteration=iteration)
                    # 中文说明：根据条件选择执行分支；代码：if not model.training:
                    if not model.training:
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model_ddp.train()
                        model_ddp.train()
                    # 中文说明：检查运行时假设是否成立；代码：assert model_ddp.training, "model_ddp is not in training mode."
                    assert model_ddp.training, "model_ddp is not in training mode."
                    # 中文说明：检查运行时假设是否成立；代码：assert model.training, "model is not in training mode."
                    assert model.training, "model is not in training mode."
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：output_batch, loss, grad_accum_iter = self.training_step(
                    output_batch, loss, grad_accum_iter = self.training_step(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model_ddp,
                        model_ddp,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：optimizer,
                        optimizer,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scheduler,
                        scheduler,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：grad_scaler,
                        grad_scaler,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_batch,
                        data_batch,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iteration=iteration,
                        iteration=iteration,
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：grad_accum_iter=grad_accum_iter,
                        grad_accum_iter=grad_accum_iter,
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_training_step_batch_end(
                    self.callbacks.on_training_step_batch_end(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model, data_batch, output_batch, loss, iteration=iteration
                        model, data_batch, output_batch, loss, iteration=iteration
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# If the gradients are still being accumulated, continue to load the next training batch.
                    # If the gradients are still being accumulated, continue to load the next training batch.
                    # 中文说明：根据条件选择执行分支；代码：if grad_accum_iter != 0:
                    if grad_accum_iter != 0:
                        # 中文说明：执行循环控制或空操作；代码：continue
                        continue
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Do the following when an actual optimizer (update) step has been made.
                    # Do the following when an actual optimizer (update) step has been made.
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iteration += 1
                    iteration += 1
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Save checkpoint.
                    # Save checkpoint.
                    # 中文说明：根据条件选择执行分支；代码：if iteration % self.config.checkpoint.save_iter == 0:
                    if iteration % self.config.checkpoint.save_iter == 0:
                        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.checkpointer.save(model, optimizer, scheduler, grad_scaler, iteration=iteration)
                        self.checkpointer.save(model, optimizer, scheduler, grad_scaler, iteration=iteration)
                    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_training_step_end(model, data_batch, output_batch, loss, iteration=iteration)
                    self.callbacks.on_training_step_end(model, data_batch, output_batch, loss, iteration=iteration)
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Validation.
                    # Validation.
                    # 中文说明：根据条件选择执行分支；代码：if self.config.trainer.run_validation and iteration % self.config.trainer.validation_iter == 0:
                    if self.config.trainer.run_validation and iteration % self.config.trainer.validation_iter == 0:
                        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.validate(model, dataloader_val, iteration=iteration)
                        self.validate(model, dataloader_val, iteration=iteration)
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# This iteration is successful; reset the timeout signal.
                    # This iteration is successful; reset the timeout signal.
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：signal.alarm(self.config.trainer.timeout_period)
                    signal.alarm(self.config.trainer.timeout_period)
                    # 中文说明：根据条件选择执行分支；代码：if torch_profiler:
                    if torch_profiler:
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：torch_profiler.step()
                        torch_profiler.step()
                    # 中文说明：根据条件选择执行分支；代码：if memory_profiler:
                    if memory_profiler:
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：memory_profiler.step()
                        memory_profiler.step()
                # 中文说明：根据条件选择执行分支；代码：if _end_training:
                if _end_training:
                    # 中文说明：执行循环控制或空操作；代码：break
                    break
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.success("Done with training.")
        log.success("Done with training.")
        # 中文说明：根据条件选择执行分支；代码：if iteration % self.config.checkpoint.save_iter != 0:
        if iteration % self.config.checkpoint.save_iter != 0:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.checkpointer.save(model, optimizer, scheduler, grad_scaler, iteration=iteration)
            self.checkpointer.save(model, optimizer, scheduler, grad_scaler, iteration=iteration)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_train_end(model, iteration=iteration)
        self.callbacks.on_train_end(model, iteration=iteration)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.checkpointer.finalize()
        self.checkpointer.finalize()
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：distributed.barrier()
        distributed.barrier()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_app_end()
        self.callbacks.on_app_end()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def training_step(
    def training_step(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model_ddp: torch.nn.Module | distributed.DistributedDataParallel,
        model_ddp: torch.nn.Module | distributed.DistributedDataParallel,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：optimizer: torch.optim.Optimizer,
        optimizer: torch.optim.Optimizer,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scheduler: torch.optim.lr_scheduler.LRScheduler,
        scheduler: torch.optim.lr_scheduler.LRScheduler,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：grad_scaler: torch.amp.GradScaler,
        grad_scaler: torch.amp.GradScaler,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data: dict[str, torch.Tensor],
        data: dict[str, torch.Tensor],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：iteration: int = 0,
        iteration: int = 0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：grad_accum_iter: int = 0,
        grad_accum_iter: int = 0,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> tuple[dict[str, torch.Tensor], torch.Tensor, int]:
    ) -> tuple[dict[str, torch.Tensor], torch.Tensor, int]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""The training step.
        """The training step.

        Args:
            model_ddp (torch.nn.Module | distributed.DistributedDataParallel): The model with a DDP wrapper or, the bare
              module, depending on whether distributed training is enabled or not.
            optimizer (torch.optim.Optimizer): The model optimizer.
            scheduler (torch.optim.lr_scheduler.LRScheduler): The optimization scheduler.
            grad_scaler (torch.amp.GradScaler): The gradient scaler (for mixed precision training).
            data (dict[str, torch.Tensor]): Data batch (dictionary of tensors).
            iteration (int): Current iteration number.
            grad_accum_iter (int): Number of gradient accumulation iterations.

        Returns:
            output (dict[str, torch.Tensor]): The model output from the training data batch (dictionary of tensors).
            loss (torch.Tensor): The total loss of the training data batch.
        """
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Only let DDP sync gradient at the last iteration of the gradient accumulation window
        # Only let DDP sync gradient at the last iteration of the gradient accumulation window
        # 中文说明：处理异常、清理资源或管理上下文；代码：with distributed.ddp_sync_grad(model_ddp, grad_accum_iter == self.config.trainer.grad_accum_i...
        with distributed.ddp_sync_grad(model_ddp, grad_accum_iter == self.config.trainer.grad_accum_iter - 1):
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_before_forward(iteration=iteration)
            self.callbacks.on_before_forward(iteration=iteration)
            # 中文说明：处理异常、清理资源或管理上下文；代码：with self.training_timer("forward"):
            with self.training_timer("forward"):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：output_batch, loss = model_ddp.training_step(data, iteration)
                output_batch, loss = model_ddp.training_step(data, iteration)
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_after_forward(iteration=iteration)
            self.callbacks.on_after_forward(iteration=iteration)
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_before_backward(model_ddp, loss, iteration=iteration)
            self.callbacks.on_before_backward(model_ddp, loss, iteration=iteration)
            # 中文说明：处理异常、清理资源或管理上下文；代码：with self.training_timer("backward"):
            with self.training_timer("backward"):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：loss_scaled = grad_scaler.scale(loss / self.config.trainer.grad_accum_iter)
                loss_scaled = grad_scaler.scale(loss / self.config.trainer.grad_accum_iter)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：loss_scaled.backward()
                loss_scaled.backward()
                # 中文说明：根据条件选择执行分支；代码：if self.config.trainer.distributed_parallelism == "ddp":
                if self.config.trainer.distributed_parallelism == "ddp":
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model_ddp.module.on_after_backward()
                    model_ddp.module.on_after_backward()
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model_ddp.on_after_backward()
                    model_ddp.on_after_backward()
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_after_backward(model_ddp, iteration=iteration)
            self.callbacks.on_after_backward(model_ddp, iteration=iteration)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：grad_accum_iter += 1
        grad_accum_iter += 1
        # 中文说明：根据条件选择执行分支；代码：if grad_accum_iter == self.config.trainer.grad_accum_iter:
        if grad_accum_iter == self.config.trainer.grad_accum_iter:
            # 中文说明：处理异常、清理资源或管理上下文；代码：with self.training_timer("optimizer_step"):
            with self.training_timer("optimizer_step"):
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_before_optimizer_step(
                self.callbacks.on_before_optimizer_step(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model_ddp, optimizer, scheduler, grad_scaler, iteration=iteration
                    model_ddp, optimizer, scheduler, grad_scaler, iteration=iteration
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：grad_scaler.step(optimizer)
                grad_scaler.step(optimizer)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：grad_scaler.update()
                grad_scaler.update()
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scheduler.step()
                scheduler.step()
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_before_zero_grad(model_ddp, optimizer, scheduler, iteration=iteration)
                self.callbacks.on_before_zero_grad(model_ddp, optimizer, scheduler, iteration=iteration)
                # 中文说明：根据条件选择执行分支；代码：if self.config.trainer.distributed_parallelism == "ddp":
                if self.config.trainer.distributed_parallelism == "ddp":
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model_ddp.module.on_before_zero_grad(optimizer, scheduler, iteration=iteration)
                    model_ddp.module.on_before_zero_grad(optimizer, scheduler, iteration=iteration)
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model_ddp.on_before_zero_grad(optimizer, scheduler, iteration=iteration)
                    model_ddp.on_before_zero_grad(optimizer, scheduler, iteration=iteration)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：optimizer.zero_grad(set_to_none=True)
                optimizer.zero_grad(set_to_none=True)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：grad_accum_iter = 0
            grad_accum_iter = 0
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return output_batch, loss, grad_accum_iter
        return output_batch, loss, grad_accum_iter

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.no_grad()
    @torch.no_grad()
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def validate(self, model: ImaginaireModel, dataloader_val: torch.utils.data.DataLoader, itera...
    def validate(self, model: ImaginaireModel, dataloader_val: torch.utils.data.DataLoader, iteration: int = 0) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Validate on the full validation dataset.
        """Validate on the full validation dataset.

        Args:
            model (ImaginaireModel): The PyTorch model.
            dataloader_val (torch.utils.data.DataLoader): The validation data loader.
            iteration (int): Current iteration number.
        """
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_validation_start(model, dataloader_val, iteration=iteration)
        self.callbacks.on_validation_start(model, dataloader_val, iteration=iteration)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model.eval()
        model.eval()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：local_dir = os.path.join('checkpoints', self.config.job.project, self.config.job.group, self....
        local_dir = os.path.join('checkpoints', self.config.job.project, self.config.job.group, self.config.job.name, "validation")
        # 中文说明：根据条件选择执行分支；代码：if not os.path.exists(local_dir):
        if not os.path.exists(local_dir):
            # 中文说明：开始一个可捕获异常的代码块；代码：try:
            try:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.makedirs(local_dir)
                os.makedirs(local_dir)
            # 中文说明：处理异常、清理资源或管理上下文；代码：except:
            except:
                # 中文说明：执行循环控制或空操作；代码：pass
                pass
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Evaluate on the full validation set.
        # Evaluate on the full validation set.
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# with ema.ema_scope(model, enabled=model.config.pipe_config.ema.enabled):
        # with ema.ema_scope(model, enabled=model.config.pipe_config.ema.enabled):
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for val_iter, data_batch in tqdm(enumerate(dataloader_val)):
        for val_iter, data_batch in tqdm(enumerate(dataloader_val)):
            # 中文说明：根据条件选择执行分支；代码：if self.config.trainer.max_val_iter is not None and val_iter >= self.config.trainer.max_val_i...
            if self.config.trainer.max_val_iter is not None and val_iter >= self.config.trainer.max_val_iter:
                # 中文说明：执行循环控制或空操作；代码：break
                break
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch = misc.to(data_batch, device="cuda")
            data_batch = misc.to(data_batch, device="cuda")
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_validation_step_start(model, data_batch, iteration=iteration)
            self.callbacks.on_validation_step_start(model, data_batch, iteration=iteration)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_batch['local_dir'], data_batch['val_iter'] = local_dir, val_iter
            data_batch['local_dir'], data_batch['val_iter'] = local_dir, val_iter
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：output_batch, loss = model.validation_step(data_batch, iteration)
            output_batch, loss = model.validation_step(data_batch, iteration)
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_validation_step_end(model, data_batch, output_batch, loss, iteration=iterat...
            self.callbacks.on_validation_step_end(model, data_batch, output_batch, loss, iteration=iteration)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.callbacks.on_validation_end(model, iteration=iteration)
        self.callbacks.on_validation_end(model, iteration=iteration)
