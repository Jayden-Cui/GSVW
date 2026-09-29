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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import math
import math

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from megatron.core import parallel_state
from megatron.core import parallel_state
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed.device_mesh import init_device_mesh
from torch.distributed.device_mesh import init_device_mesh

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.models.video2world_model import Predict2Video2WorldModel, Predict2Video2Worl...
from videoworld2.models.video2world_model import Predict2Video2WorldModel, Predict2Video2WorldModelConfig, TokenizerModel
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.pipelines.action_video2world import ActionConditionedVideo2WorldPipeline
from videoworld2.pipelines.action_video2world import ActionConditionedVideo2WorldPipeline
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.model import ImaginaireModel
from imaginaire.model import ImaginaireModel
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ActionConditionedPredict2Video2WorldModel(Predict2Video2WorldModel):
class ActionConditionedPredict2Video2WorldModel(Predict2Video2WorldModel):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, config: Predict2Video2WorldModelConfig):
    def __init__(self, config: Predict2Video2WorldModelConfig):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super(ImaginaireModel, self).__init__()
        super(ImaginaireModel, self).__init__()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.config = config
        self.config = config

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.precision = {
        self.precision = {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："float32": torch.float32,
            "float32": torch.float32,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："float16": torch.float16,
            "float16": torch.float16,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："bfloat16": torch.bfloat16,
            "bfloat16": torch.bfloat16,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}[config.precision]
        }[config.precision]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.tensor_kwargs = {"device": "cuda", "dtype": self.precision}
        self.tensor_kwargs = {"device": "cuda", "dtype": self.precision}
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.device = torch.device("cuda")
        self.device = torch.device("cuda")

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 1. set data keys and data information
        # 1. set data keys and data information
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.setup_data_key()
        self.setup_data_key()

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 4. Set up loss options, including loss masking, loss reduce and loss scaling
        # 4. Set up loss options, including loss masking, loss reduce and loss scaling
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.loss_reduce = getattr(config, "loss_reduce", "mean")
        self.loss_reduce = getattr(config, "loss_reduce", "mean")
        # 中文说明：检查运行时假设是否成立；代码：assert self.loss_reduce in ["mean", "sum"]
        assert self.loss_reduce in ["mean", "sum"]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.loss_scale = getattr(config, "loss_scale", 1.0)
        self.loss_scale = getattr(config, "loss_scale", 1.0)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.critical(f"Using {self.loss_reduce} loss reduce with loss scale {self.loss_scale}")
        log.critical(f"Using {self.loss_reduce} loss reduce with loss scale {self.loss_scale}")
        # 中文说明：根据条件选择执行分支；代码：if self.config.adjust_video_noise:
        if self.config.adjust_video_noise:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.video_noise_multiplier = math.sqrt(self.config.pipe_config.state_t)
            self.video_noise_multiplier = math.sqrt(self.config.pipe_config.state_t)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.video_noise_multiplier = 1.0
            self.video_noise_multiplier = 1.0

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 7. training states
        # 7. training states
        # 中文说明：根据条件选择执行分支；代码：if parallel_state.is_initialized():
        if parallel_state.is_initialized():
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.data_parallel_size = parallel_state.get_data_parallel_world_size()
            self.data_parallel_size = parallel_state.get_data_parallel_world_size()
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.data_parallel_size = 1
            self.data_parallel_size = 1

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# NOTE: replace the pipeline with action-conditioned setup
        # NOTE: replace the pipeline with action-conditioned setup
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.pipe = ActionConditionedVideo2WorldPipeline.from_config(
        self.pipe = ActionConditionedVideo2WorldPipeline.from_config(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：config.pipe_config,
            config.pipe_config,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path=config.model_manager_config.dit_path,
            dit_path=config.model_manager_config.dit_path,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.freeze_parameters()
        self.freeze_parameters()
        # 中文说明：根据条件选择执行分支；代码：if config.train_architecture == "lora":
        if config.train_architecture == "lora":
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.add_lora_to_model(
            self.add_lora_to_model(
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.pipe.dit,
                self.pipe.dit,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lora_rank=config.lora_rank,
                lora_rank=config.lora_rank,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lora_alpha=config.lora_alpha,
                lora_alpha=config.lora_alpha,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lora_target_modules=config.lora_target_modules,
                lora_target_modules=config.lora_target_modules,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：init_lora_weights=config.init_lora_weights,
                init_lora_weights=config.init_lora_weights,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：根据条件选择执行分支；代码：if self.pipe.dit_ema:
            if self.pipe.dit_ema:
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.add_lora_to_model(
                self.add_lora_to_model(
                    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.pipe.dit_ema,
                    self.pipe.dit_ema,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lora_rank=config.lora_rank,
                    lora_rank=config.lora_rank,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lora_alpha=config.lora_alpha,
                    lora_alpha=config.lora_alpha,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lora_target_modules=config.lora_target_modules,
                    lora_target_modules=config.lora_target_modules,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：init_lora_weights=config.init_lora_weights,
                    init_lora_weights=config.init_lora_weights,
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.pipe.denoising_model().requires_grad_(True)
            self.pipe.denoising_model().requires_grad_(True)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_total_params = sum(p.numel() for p in self.parameters())
        dit_total_params = sum(p.numel() for p in self.parameters())
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frozen_params = sum(p.numel() for p in self.parameters() if not p.requires_grad)
        frozen_params = sum(p.numel() for p in self.parameters() if not p.requires_grad)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trainable_params = sum(p.numel() for p in self.parameters() if p.requires_grad)
        trainable_params = sum(p.numel() for p in self.parameters() if p.requires_grad)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.ldm_net = TokenizerModel(self.config.ldm_config)
        self.ldm_net = TokenizerModel(self.config.ldm_config)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ldm_trainable_params = sum(p.numel() for p in self.ldm_net.parameters() if p.requires_grad)
        ldm_trainable_params = sum(p.numel() for p in self.ldm_net.parameters() if p.requires_grad)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(
        log.info(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"DIT total parameters: {dit_total_params / 1e9:.2f}B, Frozen parameters: {frozen_params:,}, ...
            f"DIT total parameters: {dit_total_params / 1e9:.2f}B, Frozen parameters: {frozen_params:,}, DiT Trainable parameters: {trainable_params:,} LDM Trainable parameters: {ldm_trainable_params / 1e9:.2f}"
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：根据条件选择执行分支；代码：if config.fsdp_shard_size != 0 and torch.distributed.is_initialized():
        if config.fsdp_shard_size != 0 and torch.distributed.is_initialized():
            # 中文说明：根据条件选择执行分支；代码：if config.fsdp_shard_size == -1:
            if config.fsdp_shard_size == -1:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fsdp_shard_size = torch.distributed.get_world_size()
                fsdp_shard_size = torch.distributed.get_world_size()
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：replica_group_size = 1
                replica_group_size = 1
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fsdp_shard_size = min(config.fsdp_shard_size, torch.distributed.get_world_size())
                fsdp_shard_size = min(config.fsdp_shard_size, torch.distributed.get_world_size())
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：replica_group_size = torch.distributed.get_world_size() // fsdp_shard_size
                replica_group_size = torch.distributed.get_world_size() // fsdp_shard_size
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dp_mesh = init_device_mesh(
            dp_mesh = init_device_mesh(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："cuda", (replica_group_size, fsdp_shard_size), mesh_dim_names=("replicate", "shard")
                "cuda", (replica_group_size, fsdp_shard_size), mesh_dim_names=("replicate", "shard")
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Using FSDP with shard size {fsdp_shard_size} | device mesh: {dp_mesh}")
            log.info(f"Using FSDP with shard size {fsdp_shard_size} | device mesh: {dp_mesh}")
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.pipe.apply_fsdp(dp_mesh)
            self.pipe.apply_fsdp(dp_mesh)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("FSDP (Fully Sharded Data Parallel) is disabled.")
            log.info("FSDP (Fully Sharded Data Parallel) is disabled.")

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.only_ldm = config.only_ldm
        self.only_ldm = config.only_ldm
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.only_dit = config.only_dit
        self.only_dit = config.only_dit
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.ldm_act_embedding = True
        self.ldm_act_embedding = True