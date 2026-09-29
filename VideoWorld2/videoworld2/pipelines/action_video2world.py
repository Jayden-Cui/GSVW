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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any
from typing import Any

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from megatron.core import parallel_state
from megatron.core import parallel_state
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import pickle
import pickle
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.auxiliary.cosmos_reason1 import CosmosReason1
from videoworld2.auxiliary.cosmos_reason1 import CosmosReason1
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.auxiliary.text_encoder import CosmosT5TextEncoder
from videoworld2.auxiliary.text_encoder import CosmosT5TextEncoder
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.configs.base.config_video2world import Video2WorldPipelineConfig
from videoworld2.configs.base.config_video2world import Video2WorldPipelineConfig
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.models.utils import load_state_dict
from videoworld2.models.utils import load_state_dict
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.module.denoiser_scaling import RectifiedFlowScaling
from videoworld2.module.denoiser_scaling import RectifiedFlowScaling
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.pipelines.video2world import Video2WorldPipeline
from videoworld2.pipelines.video2world import Video2WorldPipeline
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.schedulers.rectified_flow_scheduler import RectifiedFlowAB2Scheduler
from videoworld2.schedulers.rectified_flow_scheduler import RectifiedFlowAB2Scheduler
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.utils.context_parallel import cat_outputs_cp, split_inputs_cp
from videoworld2.utils.context_parallel import cat_outputs_cp, split_inputs_cp
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import instantiate
from imaginaire.lazy_config import instantiate
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log, misc
from imaginaire.utils import log, misc
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.ema import FastEmaModelUpdater
from imaginaire.utils.ema import FastEmaModelUpdater

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：IS_PREPROCESSED_KEY = "is_preprocessed"
IS_PREPROCESSED_KEY = "is_preprocessed"
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg", "webp"]
_IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg", "webp"]
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_VIDEO_EXTENSIONS = [".mp4"]
_VIDEO_EXTENSIONS = [".mp4"]
# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：NUM_CONDITIONAL_FRAMES_KEY: str = "num_conditional_frames"
NUM_CONDITIONAL_FRAMES_KEY: str = "num_conditional_frames"


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ActionConditionedVideo2WorldPipeline(Video2WorldPipeline):
class ActionConditionedVideo2WorldPipeline(Video2WorldPipeline):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, device: str = "cuda", torch_dtype: torch.dtype = torch.bfloat16):
    def __init__(self, device: str = "cuda", torch_dtype: torch.dtype = torch.bfloat16):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(device=device, torch_dtype=torch_dtype)
        super().__init__(device=device, torch_dtype=torch_dtype)

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def from_config(
    def from_config(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：config: Video2WorldPipelineConfig,
        config: Video2WorldPipelineConfig,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dit_path: str = "",
        dit_path: str = "",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：text_encoder_path: str = "",
        text_encoder_path: str = "",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：device: str = "cuda",
        device: str = "cuda",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：torch_dtype: torch.dtype = torch.bfloat16,
        torch_dtype: torch.dtype = torch.bfloat16,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：load_prompt_refiner: bool = False,
        load_prompt_refiner: bool = False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Any:
    ) -> Any:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Create a pipe
        # Create a pipe
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe = ActionConditionedVideo2WorldPipeline(device=device, torch_dtype=torch_dtype)
        pipe = ActionConditionedVideo2WorldPipeline(device=device, torch_dtype=torch_dtype)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.config = config
        pipe.config = config
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.precision = {
        pipe.precision = {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："float32": torch.float32,
            "float32": torch.float32,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："float16": torch.float16,
            "float16": torch.float16,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："bfloat16": torch.bfloat16,
            "bfloat16": torch.bfloat16,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}[config.precision]
        }[config.precision]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.tensor_kwargs = {"device": "cuda", "dtype": pipe.precision}
        pipe.tensor_kwargs = {"device": "cuda", "dtype": pipe.precision}
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(f"precision {pipe.precision}")
        log.warning(f"precision {pipe.precision}")

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 1. set data keys and data information
        # 1. set data keys and data information
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.sigma_data = config.sigma_data
        pipe.sigma_data = config.sigma_data
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pipe.setup_data_key()
        pipe.setup_data_key()

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 2. setup up diffusion processing and scaling~(pre-condition)
        # 2. setup up diffusion processing and scaling~(pre-condition)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.scheduler = RectifiedFlowAB2Scheduler(
        pipe.scheduler = RectifiedFlowAB2Scheduler(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_min=config.timestamps.t_min,
            sigma_min=config.timestamps.t_min,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_max=config.timestamps.t_max,
            sigma_max=config.timestamps.t_max,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：order=config.timestamps.order,
            order=config.timestamps.order,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t_scaling_factor=config.rectified_flow_t_scaling_factor,
            t_scaling_factor=config.rectified_flow_t_scaling_factor,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.scaling = RectifiedFlowScaling(pipe.sigma_data, config.rectified_flow_t_scaling_factor)
        pipe.scaling = RectifiedFlowScaling(pipe.sigma_data, config.rectified_flow_t_scaling_factor)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 3. Set up tokenizer
        # 3. Set up tokenizer
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.tokenizer = instantiate(config.tokenizer)
        pipe.tokenizer = instantiate(config.tokenizer)
        # 中文说明：检查运行时假设是否成立；代码：assert (
        assert (
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.tokenizer.latent_ch == pipe.config.state_ch
            pipe.tokenizer.latent_ch == pipe.config.state_ch
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"latent_ch {pipe.tokenizer.latent_ch} != state_shape {pipe.config.state_ch}"
        ), f"latent_ch {pipe.tokenizer.latent_ch} != state_shape {pipe.config.state_ch}"

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 4. Load text encoder
        # 4. Load text encoder
        # 中文说明：根据条件选择执行分支；代码：if text_encoder_path:
        if text_encoder_path:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# inference
            # inference
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.text_encoder = CosmosT5TextEncoder(device=device, cache_dir=text_encoder_path)
            pipe.text_encoder = CosmosT5TextEncoder(device=device, cache_dir=text_encoder_path)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pipe.text_encoder.to(device)
            pipe.text_encoder.to(device)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# training
            # training
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.text_encoder = None
            pipe.text_encoder = None

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 5. Initialize conditioner
        # 5. Initialize conditioner
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.conditioner = instantiate(config.conditioner)
        pipe.conditioner = instantiate(config.conditioner)
        # 中文说明：检查运行时假设是否成立；代码：assert (
        assert (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sum(p.numel() for p in pipe.conditioner.parameters() if p.requires_grad) == 0
            sum(p.numel() for p in pipe.conditioner.parameters() if p.requires_grad) == 0
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), "conditioner should not have learnable parameters"
        ), "conditioner should not have learnable parameters"

        # 中文说明：根据条件选择执行分支；代码：if load_prompt_refiner:
        if load_prompt_refiner:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.prompt_refiner = CosmosReason1(
            pipe.prompt_refiner = CosmosReason1(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint_dir=config.prompt_refiner_config.checkpoint_dir,
                checkpoint_dir=config.prompt_refiner_config.checkpoint_dir,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：offload_model_to_cpu=config.prompt_refiner_config.offload_model_to_cpu,
                offload_model_to_cpu=config.prompt_refiner_config.offload_model_to_cpu,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enabled=config.prompt_refiner_config.enabled,
                enabled=config.prompt_refiner_config.enabled,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：根据条件选择执行分支；代码：if config.guardrail_config.enabled:
        if config.guardrail_config.enabled:
            # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.auxiliary.guardrail.common import presets as guardrail_presets
            from videoworld2.auxiliary.guardrail.common import presets as guardrail_presets

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.text_guardrail_runner = guardrail_presets.create_text_guardrail_runner(
            pipe.text_guardrail_runner = guardrail_presets.create_text_guardrail_runner(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：config.guardrail_config.checkpoint_dir, config.guardrail_config.offload_model_to_cpu
                config.guardrail_config.checkpoint_dir, config.guardrail_config.offload_model_to_cpu
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.video_guardrail_runner = guardrail_presets.create_video_guardrail_runner(
            pipe.video_guardrail_runner = guardrail_presets.create_video_guardrail_runner(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：config.guardrail_config.checkpoint_dir, config.guardrail_config.offload_model_to_cpu
                config.guardrail_config.checkpoint_dir, config.guardrail_config.offload_model_to_cpu
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.text_guardrail_runner = None
            pipe.text_guardrail_runner = None
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.video_guardrail_runner = None
            pipe.video_guardrail_runner = None

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 6. Set up DiT
        # 6. Set up DiT
        # 中文说明：根据条件选择执行分支；代码：if dit_path:
        if dit_path:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Loading DiT from {dit_path}")
            log.info(f"Loading DiT from {dit_path}")
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning("dit_path not provided, initializing DiT with random weights")
            log.warning("dit_path not provided, initializing DiT with random weights")
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# with init_weights_on_device():
        # with init_weights_on_device():
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# NOTE: we don't load checkpoint on meta device since we have additional action encoder
        # NOTE: we don't load checkpoint on meta device since we have additional action encoder
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_config = config.net
        dit_config = config.net
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.dit = instantiate(dit_config).eval() # inference
        pipe.dit = instantiate(dit_config).eval()  # inference

        # 中文说明：根据条件选择执行分支；代码：if dit_path:
        if dit_path:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dict = load_state_dict(dit_path)
            state_dict = load_state_dict(dit_path)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# drop net. prefix
        # drop net. prefix
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dict_dit_compatible = dict()
        state_dict_dit_compatible = dict()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for k, v in state_dict.items():
        for k, v in state_dict.items():
            # 中文说明：根据条件选择执行分支；代码：if k.startswith("net."):
            if k.startswith("net."):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：state_dict_dit_compatible[k[4:]] = v
                state_dict_dit_compatible[k[4:]] = v
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dict_dit_compatible[k] = v
                state_dict_dit_compatible[k] = v
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pipe.dit.load_state_dict(state_dict_dit_compatible, strict=False, assign=True)
        pipe.dit.load_state_dict(state_dict_dit_compatible, strict=False, assign=True)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del state_dict, state_dict_dit_compatible
        del state_dict, state_dict_dit_compatible
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.success(f"Successfully loaded DiT from {dit_path}")
        log.success(f"Successfully loaded DiT from {dit_path}")

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 6-2. Handle EMA
        # 6-2. Handle EMA
        # 中文说明：根据条件选择执行分支；代码：if config.ema.enabled:
        if config.ema.enabled:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.dit_ema = instantiate(dit_config).eval()
            pipe.dit_ema = instantiate(dit_config).eval()
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pipe.dit_ema.requires_grad_(False)
            pipe.dit_ema.requires_grad_(False)

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.dit_ema_worker = FastEmaModelUpdater() # default when not using FSDP
            pipe.dit_ema_worker = FastEmaModelUpdater()  # default when not using FSDP

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：s = config.ema.rate
            s = config.ema.rate
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.ema_exp_coefficient = np.roots([1, 7, 16 - s**-2, 12 - s**-2]).real.max()
            pipe.ema_exp_coefficient = np.roots([1, 7, 16 - s**-2, 12 - s**-2]).real.max()
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# copying is only necessary when starting the training at iteration 0.
            # copying is only necessary when starting the training at iteration 0.
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Actual state_dict should be loaded after the pipe is created.
            # Actual state_dict should be loaded after the pipe is created.
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pipe.dit_ema_worker.copy_to(src_model=pipe.dit, tgt_model=pipe.dit_ema)
            pipe.dit_ema_worker.copy_to(src_model=pipe.dit, tgt_model=pipe.dit_ema)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.dit = pipe.dit.to(device=device, dtype=torch_dtype)
        pipe.dit = pipe.dit.to(device=device, dtype=torch_dtype)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.empty_cache()
        torch.cuda.empty_cache()

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 7. training states
        # 7. training states
        # 中文说明：根据条件选择执行分支；代码：if parallel_state.is_initialized():
        if parallel_state.is_initialized():
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.data_parallel_size = parallel_state.get_data_parallel_world_size()
            pipe.data_parallel_size = parallel_state.get_data_parallel_world_size()
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.data_parallel_size = 1
            pipe.data_parallel_size = 1

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return pipe
        return pipe

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _get_data_batch_input(
    def _get_data_batch_input(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video: torch.Tensor,
        video: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：actions: np.ndarray,
        actions: np.ndarray,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：prompt: str,
        prompt: str,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：negative_prompt: str = "",
        negative_prompt: str = "",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_latent_conditional_frames: int = 1,
        num_latent_conditional_frames: int = 1,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Prepares the input data batch for the diffusion model.

        Constructs a dictionary containing the video tensor, text embeddings,
        and other necessary metadata required by the model's forward pass.
        Optionally includes negative text embeddings.

        Args:
            video (torch.Tensor): The input video tensor (B, C, T, H, W).
            prompt (str): The text prompt for conditioning.
            negative_prompt (str): Negative prompt.
            num_latent_conditional_frames (int, optional): The number of latent conditional frames. Defaults to 1.

        Returns:
            dict: A dictionary containing the prepared data batch, moved to the correct device and dtype.
        """
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：B, C, T, H, W = video.shape
        B, C, T, H, W = video.shape

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.batch_size = 1
        self.batch_size = 1
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch = {
        data_batch = {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："dataset_name": "video_data",
            "dataset_name": "video_data",
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："video": video,
            "video": video,
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# NOTE: we don't use text embeddings for action conditional video2world
            # NOTE: we don't use text embeddings for action conditional video2world
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："t5_text_embeddings": torch.zeros(self.batch_size, 512, 1024, dtype=torch.bfloat16).cuda(),
            "t5_text_embeddings": torch.zeros(self.batch_size, 512, 1024, dtype=torch.bfloat16).cuda(),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："fps": torch.randint(16, 32, (self.batch_size,)), # Random FPS (might be used by model)
            "fps": torch.randint(16, 32, (self.batch_size,)),  # Random FPS (might be used by model)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："padding_mask": torch.zeros(self.batch_size, 1, H, W), # Padding mask (assumed no padding here)
            "padding_mask": torch.zeros(self.batch_size, 1, H, W),  # Padding mask (assumed no padding here)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："num_conditional_frames": num_latent_conditional_frames, # Specify number of conditional frames
            "num_conditional_frames": num_latent_conditional_frames,  # Specify number of conditional frames
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："action": actions,
            "action": actions,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Handle negative prompts for classifier-free guidance
        # Handle negative prompts for classifier-free guidance
        # 中文说明：根据条件选择执行分支；代码：if negative_prompt:
        if negative_prompt:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch["neg_t5_text_embeddings"] = self.encode_prompt(negative_prompt).to(dtype=self.torc...
            data_batch["neg_t5_text_embeddings"] = self.encode_prompt(negative_prompt).to(dtype=self.torch_dtype)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Move tensors to GPU and convert to bfloat16 if they are floating point
        # Move tensors to GPU and convert to bfloat16 if they are floating point
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for k, v in data_batch.items():
        for k, v in data_batch.items():
            # 中文说明：根据条件选择执行分支；代码：if isinstance(v, torch.Tensor) and torch.is_floating_point(data_batch[k]):
            if isinstance(v, torch.Tensor) and torch.is_floating_point(data_batch[k]):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch[k] = v.cuda().to(dtype=torch.bfloat16)
                data_batch[k] = v.cuda().to(dtype=torch.bfloat16)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return data_batch
        return data_batch

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.no_grad()
    @torch.no_grad()
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(
    def __call__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：first_frame: np.ndarray,
        first_frame: np.ndarray,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：actions: np.ndarray,
        actions: np.ndarray,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：prompt: str = "",
        prompt: str = "",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：negative_prompt: str = "",
        negative_prompt: str = "",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_conditional_frames: int = 1,
        num_conditional_frames: int = 1,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：guidance: float = 7.0,
        guidance: float = 7.0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_sampling_step: int = 35,
        num_sampling_step: int = 35,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：seed: int = 0,
        seed: int = 0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：solver_option: str = "2ab",
        solver_option: str = "2ab",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor | None:
    ) -> torch.Tensor | None:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Parameter check
        # Parameter check
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# width, height = VIDEO_RES_SIZE_INFO[self.config.resolution]["16:9"] # type: ignore
        # width, height = VIDEO_RES_SIZE_INFO[self.config.resolution]["16:9"]  # type: ignore
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# height, width = self.check_resize_height_width(height, width)
        # height, width = self.check_resize_height_width(height, width)
        # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import pdb;pdb.set_trace()
        import pdb;pdb.set_trace()
        # 中文说明：检查运行时假设是否成立；代码：assert num_conditional_frames in [1, 5], "num_conditional_frames must be 1 or 5"
        assert num_conditional_frames in [1, 5], "num_conditional_frames must be 1 or 5"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_latent_conditional_frames = self.tokenizer.get_latent_num_frames(num_conditional_frames)
        num_latent_conditional_frames = self.tokenizer.get_latent_num_frames(num_conditional_frames)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# num_video_frames = self.tokenizer.get_pixel_num_frames(self.config.state_t)
        # num_video_frames = self.tokenizer.get_pixel_num_frames(self.config.state_t)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# transform first frame and actions to tensor
        # transform first frame and actions to tensor
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：vid_input = torch.from_numpy(first_frame).permute(2, 0, 1)[None, :, None, ...]
        vid_input = torch.from_numpy(first_frame).permute(2, 0, 1)[None, :, None, ...]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：actions_tensor = torch.from_numpy(actions).to(dtype=torch.bfloat16)[None, ...]
        actions_tensor = torch.from_numpy(actions).to(dtype=torch.bfloat16)[None, ...]

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Prepare the data batch with text embeddings
        # Prepare the data batch with text embeddings
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch = self._get_data_batch_input(
        data_batch = self._get_data_batch_input(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：vid_input,
            vid_input,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：actions_tensor,
            actions_tensor,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：prompt,
            prompt,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：negative_prompt,
            negative_prompt,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_latent_conditional_frames=num_latent_conditional_frames,
            num_latent_conditional_frames=num_latent_conditional_frames,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# preprocess
        # preprocess
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._normalize_video_databatch_inplace(data_batch)
        self._normalize_video_databatch_inplace(data_batch)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._augment_image_dim_inplace(data_batch)
        self._augment_image_dim_inplace(data_batch)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_image_batch = self.is_image_batch(data_batch)
        is_image_batch = self.is_image_batch(data_batch)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_key = self.input_image_key if is_image_batch else self.input_data_key
        input_key = self.input_image_key if is_image_batch else self.input_data_key
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_sample = data_batch[input_key].shape[0]
        n_sample = data_batch[input_key].shape[0]
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_T, _H, _W = data_batch[input_key].shape[-3:]
        _T, _H, _W = data_batch[input_key].shape[-3:]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_shape = [
        state_shape = [
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.config.state_ch,
            self.config.state_ch,
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.tokenizer.get_latent_num_frames(_T),
            self.tokenizer.get_latent_num_frames(_T),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_H // self.tokenizer.spatial_compression_factor,
            _H // self.tokenizer.spatial_compression_factor,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_W // self.tokenizer.spatial_compression_factor,
            _W // self.tokenizer.spatial_compression_factor,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
        ]

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x0_fn = self.get_x0_fn_from_batch(data_batch, guidance, is_negative_prompt=True)
        x0_fn = self.get_x0_fn_from_batch(data_batch, guidance, is_negative_prompt=True)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("Starting video generation...")
        log.info("Starting video generation...")

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_sigma_max = (
        x_sigma_max = (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：misc.arch_invariant_rand(
            misc.arch_invariant_rand(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：(n_sample,) + tuple(state_shape),
                (n_sample,) + tuple(state_shape),
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.float32,
                torch.float32,
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.tensor_kwargs["device"],
                self.tensor_kwargs["device"],
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：seed,
                seed,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：* self.scheduler.config.sigma_max
            * self.scheduler.config.sigma_max
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Split the input data and condition for model parallelism, if context parallelism is enabled.
        # Split the input data and condition for model parallelism, if context parallelism is enabled.
        # 中文说明：根据条件选择执行分支；代码：if self.dit.is_context_parallel_enabled:
        if self.dit.is_context_parallel_enabled:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_sigma_max = split_inputs_cp(x=x_sigma_max, seq_dim=2, cp_group=self.get_context_parallel_gr...
            x_sigma_max = split_inputs_cp(x=x_sigma_max, seq_dim=2, cp_group=self.get_context_parallel_group())

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# ------------------------------------------------------------------ #
        # ------------------------------------------------------------------ #
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Sampling loop driven by `RectifiedFlowAB2Scheduler`
        # Sampling loop driven by `RectifiedFlowAB2Scheduler`
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# ------------------------------------------------------------------ #
        # ------------------------------------------------------------------ #
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scheduler = self.scheduler
        scheduler = self.scheduler

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Construct sigma schedule (L + 1 entries including simga_min) and timesteps
        # Construct sigma schedule (L + 1 entries including simga_min) and timesteps
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scheduler.set_timesteps(num_sampling_step, device=x_sigma_max.device)
        scheduler.set_timesteps(num_sampling_step, device=x_sigma_max.device)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Bring the initial latent into the precision expected by the scheduler
        # Bring the initial latent into the precision expected by the scheduler
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sample = x_sigma_max.to(dtype=torch.float32)
        sample = x_sigma_max.to(dtype=torch.float32)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x0_prev: torch.Tensor | None = None
        x0_prev: torch.Tensor | None = None

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i, _ in enumerate(scheduler.timesteps):
        for i, _ in enumerate(scheduler.timesteps):
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Current noise level (sigma_t).
            # Current noise level (sigma_t).
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_t = scheduler.sigmas[i].to(sample.device, dtype=torch.float32)
            sigma_t = scheduler.sigmas[i].to(sample.device, dtype=torch.float32)

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# `x0_fn` expects `sigma` as a tensor of shape [B] or [B, T]. We
            # `x0_fn` expects `sigma` as a tensor of shape [B] or [B, T]. We
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# pass a 1-D tensor broadcastable to any later shape handling.
            # pass a 1-D tensor broadcastable to any later shape handling.
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_in = sigma_t.repeat(sample.shape[0])
            sigma_in = sigma_t.repeat(sample.shape[0])

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# x0 prediction with conditional and unconditional branches
            # x0 prediction with conditional and unconditional branches
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x0_pred = x0_fn(sample, sigma_in)
            x0_pred = x0_fn(sample, sigma_in)

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Scheduler step updates the noisy sample and returns the cached x0.
            # Scheduler step updates the noisy sample and returns the cached x0.
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sample, x0_prev = scheduler.step(
            sample, x0_prev = scheduler.step(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x0_pred=x0_pred,
                x0_pred=x0_pred,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：i=i,
                i=i,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sample=sample,
                sample=sample,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x0_prev=x0_prev,
                x0_prev=x0_prev,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Final clean pass at sigma_min.
        # Final clean pass at sigma_min.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_min = scheduler.sigmas[-1].to(sample.device, dtype=torch.float32)
        sigma_min = scheduler.sigmas[-1].to(sample.device, dtype=torch.float32)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_in = sigma_min.repeat(sample.shape[0])
        sigma_in = sigma_min.repeat(sample.shape[0])
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：samples = x0_fn(sample, sigma_in)
        samples = x0_fn(sample, sigma_in)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Merge context-parallel chunks back together if needed.
        # Merge context-parallel chunks back together if needed.
        # 中文说明：根据条件选择执行分支；代码：if self.dit.is_context_parallel_enabled:
        if self.dit.is_context_parallel_enabled:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：samples = cat_outputs_cp(samples, seq_dim=2, cp_group=self.get_context_parallel_group())
            samples = cat_outputs_cp(samples, seq_dim=2, cp_group=self.get_context_parallel_group())

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Decode
        # Decode
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = self.decode(samples) # shape: (B, C, T, H, W), possibly out of [-1, 1]
        video = self.decode(samples)  # shape: (B, C, T, H, W), possibly out of [-1, 1]

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Run video guardrail on the generated video and apply postprocessing
        # Run video guardrail on the generated video and apply postprocessing
        # 中文说明：根据条件选择执行分支；代码：if self.video_guardrail_runner is not None:
        if self.video_guardrail_runner is not None:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Clamp to safe range before normalization
            # Clamp to safe range before normalization
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = video.clamp(-1.0, 1.0)
            video = video.clamp(-1.0, 1.0)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_normalized = (video + 1) / 2 # [0, 1]
            video_normalized = (video + 1) / 2  # [0, 1]

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Convert tensor to NumPy frames for guardrail processing
            # Convert tensor to NumPy frames for guardrail processing
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_squeezed = video_normalized.squeeze(0) # (C, T, H, W)
            video_squeezed = video_normalized.squeeze(0)  # (C, T, H, W)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = (video_squeezed * 255).clamp(0, 255).to(torch.uint8)
            frames = (video_squeezed * 255).clamp(0, 255).to(torch.uint8)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = frames.permute(1, 2, 3, 0).cpu().numpy() # (T, H, W, C)
            frames = frames.permute(1, 2, 3, 0).cpu().numpy()  # (T, H, W, C)

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Run guardrail
            # Run guardrail
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：processed_frames = guardrail_presets.run_video_guardrail(frames, self.video_guardrail_runner)
            processed_frames = guardrail_presets.run_video_guardrail(frames, self.video_guardrail_runner)
            # 中文说明：根据条件选择执行分支；代码：if processed_frames is None:
            if processed_frames is None:
                # 中文说明：从当前函数返回结果或结束函数执行；代码：return None
                return None
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.success("Passed guardrail on generated video")
                log.success("Passed guardrail on generated video")

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Convert processed frames back to tensor format
            # Convert processed frames back to tensor format
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：processed_video = torch.from_numpy(processed_frames).float().permute(3, 0, 1, 2) / 255.0
            processed_video = torch.from_numpy(processed_frames).float().permute(3, 0, 1, 2) / 255.0
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：processed_video = processed_video * 2 - 1 # back to [-1, 1]
            processed_video = processed_video * 2 - 1  # back to [-1, 1]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：processed_video = processed_video.unsqueeze(0)
            processed_video = processed_video.unsqueeze(0)

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = processed_video.to(video.device, dtype=video.dtype)
            video = processed_video.to(video.device, dtype=video.dtype)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.success("Video generation completed successfully")
        log.success("Video generation completed successfully")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return video
        return video

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.no_grad()
    @torch.no_grad()
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def validation(
    def validation(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video: np.ndarray,
        video: np.ndarray,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：actions: np.ndarray,
        actions: np.ndarray,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_conditional_frames: int = 1,
        num_conditional_frames: int = 1,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：guidance: float = 7.0,
        guidance: float = 7.0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_sampling_step: int = 35,
        num_sampling_step: int = 35,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：seed: int = 0,
        seed: int = 0,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prompt_embedding=None,
        prompt_embedding=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_cuda_graphs=False
        use_cuda_graphs=False
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor | None:
    ) -> torch.Tensor | None:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Parameter check
        # Parameter check
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# width, height = VIDEO_RES_SIZE_INFO[self.config.resolution]["16:9"] # type: ignore
        # width, height = VIDEO_RES_SIZE_INFO[self.config.resolution]["16:9"]  # type: ignore
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# height, width = self.check_resize_height_width(height, width)
        # height, width = self.check_resize_height_width(height, width)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：处理异常、清理资源或管理上下文；代码：with open("datasets/cosmos_nemo_assets/default_neg.pickle", "rb") as fp:
        with open("datasets/cosmos_nemo_assets/default_neg.pickle", "rb") as fp:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：neg_t5_text_embeddings = pickle.load(fp)
            neg_t5_text_embeddings = pickle.load(fp)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：neg_t5_text_embeddings = torch.from_numpy(neg_t5_text_embeddings[0])[None].to(dtype=self.torc...
        neg_t5_text_embeddings = torch.from_numpy(neg_t5_text_embeddings[0])[None].to(dtype=self.torch_dtype)
        # 中文说明：根据条件选择执行分支；代码：if neg_t5_text_embeddings.shape[1] < 512:
        if neg_t5_text_embeddings.shape[1] < 512:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：neg_t5_text_embeddings = torch.cat([neg_t5_text_embeddings.to(torch.bfloat16).cuda(), torch.z...
            neg_t5_text_embeddings = torch.cat([neg_t5_text_embeddings.to(torch.bfloat16).cuda(), torch.zeros(1, 512-neg_t5_text_embeddings.shape[1], 1024).to(torch.bfloat16).cuda()], dim=1)

        # 中文说明：检查运行时假设是否成立；代码：assert num_conditional_frames in [1, 5], "num_conditional_frames must be 1 or 5"
        assert num_conditional_frames in [1, 5], "num_conditional_frames must be 1 or 5"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_latent_conditional_frames = self.tokenizer.get_latent_num_frames(num_conditional_frames)
        num_latent_conditional_frames = self.tokenizer.get_latent_num_frames(num_conditional_frames)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Prepare the data batch with text embeddings
        # Prepare the data batch with text embeddings
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：H, W = video.shape[-2:]
        H, W = video.shape[-2:]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch = {
        data_batch = {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："dataset_name": "video_data",
            "dataset_name": "video_data",
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："video": video,
            "video": video,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："t5_text_embeddings": torch.zeros(video.shape[0], 512, 1024, dtype=torch.bfloat16).cuda(),
            "t5_text_embeddings": torch.zeros(video.shape[0], 512, 1024, dtype=torch.bfloat16).cuda(),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："neg_t5_text_embeddings": neg_t5_text_embeddings,
            "neg_t5_text_embeddings": neg_t5_text_embeddings,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："fps": torch.ones((1,)) * 16, # Random FPS (might be used by model)
            "fps": torch.ones((1,)) * 16,  # Random FPS (might be used by model)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："padding_mask": torch.zeros(1, 1, H, W), # Padding mask (assumed no padding here)
            "padding_mask": torch.zeros(1, 1, H, W),  # Padding mask (assumed no padding here)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："num_conditional_frames": num_latent_conditional_frames, # Specify number of conditional frames
            "num_conditional_frames": num_latent_conditional_frames,  # Specify number of conditional frames
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："action": actions.contiguous(),
            "action": actions.contiguous(),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for k, v in data_batch.items():
        for k, v in data_batch.items():
            # 中文说明：根据条件选择执行分支；代码：if isinstance(v, torch.Tensor) and torch.is_floating_point(data_batch[k]):
            if isinstance(v, torch.Tensor) and torch.is_floating_point(data_batch[k]):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch[k] = v.cuda().to(dtype=torch.bfloat16)
                data_batch[k] = v.cuda().to(dtype=torch.bfloat16)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# preprocess
        # preprocess
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self._normalize_video_databatch_inplace(data_batch)
        # self._normalize_video_databatch_inplace(data_batch)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._augment_image_dim_inplace(data_batch)
        self._augment_image_dim_inplace(data_batch)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_image_batch = self.is_image_batch(data_batch)
        is_image_batch = self.is_image_batch(data_batch)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_key = self.input_image_key if is_image_batch else self.input_data_key
        input_key = self.input_image_key if is_image_batch else self.input_data_key
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_sample = data_batch[input_key].shape[0]
        n_sample = data_batch[input_key].shape[0]
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_T, _H, _W = data_batch[input_key].shape[-3:]
        _T, _H, _W = data_batch[input_key].shape[-3:]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_shape = [
        state_shape = [
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.config.state_ch,
            self.config.state_ch,
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.tokenizer.get_latent_num_frames(_T),
            self.tokenizer.get_latent_num_frames(_T),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_H // self.tokenizer.spatial_compression_factor,
            _H // self.tokenizer.spatial_compression_factor,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_W // self.tokenizer.spatial_compression_factor,
            _W // self.tokenizer.spatial_compression_factor,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
        ]

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x0_fn = self.get_x0_fn_from_batch(data_batch, guidance, is_negative_prompt=True)
        x0_fn = self.get_x0_fn_from_batch(data_batch, guidance, is_negative_prompt=True)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("Starting video generation...")
        log.info("Starting video generation...")

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_sigma_max = (
        x_sigma_max = (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：misc.arch_invariant_rand(
            misc.arch_invariant_rand(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：(n_sample,) + tuple(state_shape),
                (n_sample,) + tuple(state_shape),
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.float32,
                torch.float32,
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.tensor_kwargs["device"],
                self.tensor_kwargs["device"],
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：seed,
                seed,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：* self.scheduler.config.sigma_max
            * self.scheduler.config.sigma_max
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Split the input data and condition for model parallelism, if context parallelism is enabled.
        # Split the input data and condition for model parallelism, if context parallelism is enabled.
        # 中文说明：根据条件选择执行分支；代码：if self.dit.is_context_parallel_enabled:
        if self.dit.is_context_parallel_enabled:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_sigma_max = split_inputs_cp(x=x_sigma_max, seq_dim=2, cp_group=self.get_context_parallel_gr...
            x_sigma_max = split_inputs_cp(x=x_sigma_max, seq_dim=2, cp_group=self.get_context_parallel_group())

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# ------------------------------------------------------------------ #
        # ------------------------------------------------------------------ #
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Sampling loop driven by `RectifiedFlowAB2Scheduler`
        # Sampling loop driven by `RectifiedFlowAB2Scheduler`
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# ------------------------------------------------------------------ #
        # ------------------------------------------------------------------ #
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scheduler = self.scheduler
        scheduler = self.scheduler

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Construct sigma schedule (L + 1 entries including simga_min) and timesteps
        # Construct sigma schedule (L + 1 entries including simga_min) and timesteps
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scheduler.set_timesteps(num_sampling_step, device=x_sigma_max.device)
        scheduler.set_timesteps(num_sampling_step, device=x_sigma_max.device)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Bring the initial latent into the precision expected by the scheduler
        # Bring the initial latent into the precision expected by the scheduler
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sample = x_sigma_max.to(dtype=torch.float32)
        sample = x_sigma_max.to(dtype=torch.float32)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x0_prev: torch.Tensor | None = None
        x0_prev: torch.Tensor | None = None

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i, _ in enumerate(scheduler.timesteps):
        for i, _ in enumerate(scheduler.timesteps):
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Current noise level (sigma_t).
            # Current noise level (sigma_t).
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_t = scheduler.sigmas[i].to(sample.device, dtype=torch.float32)
            sigma_t = scheduler.sigmas[i].to(sample.device, dtype=torch.float32)

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# `x0_fn` expects `sigma` as a tensor of shape [B] or [B, T]. We
            # `x0_fn` expects `sigma` as a tensor of shape [B] or [B, T]. We
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# pass a 1-D tensor broadcastable to any later shape handling.
            # pass a 1-D tensor broadcastable to any later shape handling.
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_in = sigma_t.repeat(sample.shape[0])
            sigma_in = sigma_t.repeat(sample.shape[0])

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# x0 prediction with conditional and unconditional branches
            # x0 prediction with conditional and unconditional branches
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x0_pred = x0_fn(sample, sigma_in)
            x0_pred = x0_fn(sample, sigma_in)

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Scheduler step updates the noisy sample and returns the cached x0.
            # Scheduler step updates the noisy sample and returns the cached x0.
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sample, x0_prev = scheduler.step(
            sample, x0_prev = scheduler.step(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x0_pred=x0_pred,
                x0_pred=x0_pred,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：i=i,
                i=i,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sample=sample,
                sample=sample,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x0_prev=x0_prev,
                x0_prev=x0_prev,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Final clean pass at sigma_min.
        # Final clean pass at sigma_min.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_min = scheduler.sigmas[-1].to(sample.device, dtype=torch.float32)
        sigma_min = scheduler.sigmas[-1].to(sample.device, dtype=torch.float32)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_in = sigma_min.repeat(sample.shape[0])
        sigma_in = sigma_min.repeat(sample.shape[0])
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：samples = x0_fn(sample, sigma_in)
        samples = x0_fn(sample, sigma_in)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Merge context-parallel chunks back together if needed.
        # Merge context-parallel chunks back together if needed.
        # 中文说明：根据条件选择执行分支；代码：if self.dit.is_context_parallel_enabled:
        if self.dit.is_context_parallel_enabled:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：samples = cat_outputs_cp(samples, seq_dim=2, cp_group=self.get_context_parallel_group())
            samples = cat_outputs_cp(samples, seq_dim=2, cp_group=self.get_context_parallel_group())

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Decode
        # Decode
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = self.decode(samples) # shape: (B, C, T, H, W), possibly out of [-1, 1]
        video = self.decode(samples)  # shape: (B, C, T, H, W), possibly out of [-1, 1]

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Run video guardrail on the generated video and apply postprocessing
        # Run video guardrail on the generated video and apply postprocessing


        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.success("Video generation completed successfully")
        log.success("Video generation completed successfully")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return video
        return video