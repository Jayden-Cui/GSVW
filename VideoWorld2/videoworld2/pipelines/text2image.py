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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any, List, Tuple, Union
from typing import Any, List, Tuple, Union

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from einops import rearrange
from einops import rearrange
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from megatron.core import parallel_state
from megatron.core import parallel_state
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from tqdm import tqdm
from tqdm import tqdm

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.auxiliary.text_encoder import CosmosT5TextEncoder
from videoworld2.auxiliary.text_encoder import CosmosT5TextEncoder
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.conditioner import DataType, T2VCondition
from videoworld2.conditioner import DataType, T2VCondition
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.datasets.utils import IMAGE_RES_SIZE_INFO
from videoworld2.datasets.utils import IMAGE_RES_SIZE_INFO
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.models.text2image_dit import MiniTrainDIT
from videoworld2.models.text2image_dit import MiniTrainDIT
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.models.utils import init_weights_on_device, load_state_dict
from videoworld2.models.utils import init_weights_on_device, load_state_dict
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.module.denoise_prediction import DenoisePrediction
from videoworld2.module.denoise_prediction import DenoisePrediction
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.module.denoiser_scaling import RectifiedFlowScaling
from videoworld2.module.denoiser_scaling import RectifiedFlowScaling
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.pipelines.base import BasePipeline
from videoworld2.pipelines.base import BasePipeline
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.schedulers.rectified_flow_scheduler import RectifiedFlowAB2Scheduler
from videoworld2.schedulers.rectified_flow_scheduler import RectifiedFlowAB2Scheduler
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.tokenizers.tokenizer import TokenizerInterface
from videoworld2.tokenizers.tokenizer import TokenizerInterface
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import LazyDict, instantiate
from imaginaire.lazy_config import LazyDict, instantiate
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log, misc
from imaginaire.utils import log, misc

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：IS_PREPROCESSED_KEY = "is_preprocessed"
IS_PREPROCESSED_KEY = "is_preprocessed"


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def sample_batch_image(resolution: str = "1024", aspect_ratio: str = "16:9", batch_size: int ...
def sample_batch_image(resolution: str = "1024", aspect_ratio: str = "16:9", batch_size: int = 1) -> dict:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：w, h = IMAGE_RES_SIZE_INFO[resolution][aspect_ratio]
    w, h = IMAGE_RES_SIZE_INFO[resolution][aspect_ratio]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch = {
    data_batch = {
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："dataset_name": "image_data",
        "dataset_name": "image_data",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："images": torch.randn(batch_size, 3, h, w).cuda(),
        "images": torch.randn(batch_size, 3, h, w).cuda(),
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："t5_text_embeddings": torch.randn(batch_size, 512, 1024).cuda(),
        "t5_text_embeddings": torch.randn(batch_size, 512, 1024).cuda(),
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："fps": torch.randint(16, 32, (batch_size,)).cuda(),
        "fps": torch.randint(16, 32, (batch_size,)).cuda(),
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："padding_mask": torch.zeros(batch_size, 1, h, w).cuda(),
        "padding_mask": torch.zeros(batch_size, 1, h, w).cuda(),
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
    }
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return data_batch
    return data_batch


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_sample_batch(
def get_sample_batch(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：resolution: str = "512",
    resolution: str = "512",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：aspect_ratio: str = "16:9",
    aspect_ratio: str = "16:9",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：batch_size: int = 1,
    batch_size: int = 1,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> dict:
) -> dict:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch = sample_batch_image(resolution, aspect_ratio, batch_size)
    data_batch = sample_batch_image(resolution, aspect_ratio, batch_size)

    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for k, v in data_batch.items():
    for k, v in data_batch.items():
        # 中文说明：根据条件选择执行分支；代码：if isinstance(v, torch.Tensor) and torch.is_floating_point(data_batch[k]):
        if isinstance(v, torch.Tensor) and torch.is_floating_point(data_batch[k]):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch[k] = v.cuda().to(dtype=torch.bfloat16)
            data_batch[k] = v.cuda().to(dtype=torch.bfloat16)

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return data_batch
    return data_batch


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Text2ImagePipeline(BasePipeline):
class Text2ImagePipeline(BasePipeline):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, device: str = "cuda", torch_dtype: torch.dtype = torch.bfloat16):
    def __init__(self, device: str = "cuda", torch_dtype: torch.dtype = torch.bfloat16):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(device=device, torch_dtype=torch_dtype)
        super().__init__(device=device, torch_dtype=torch_dtype)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.text_encoder: CosmosT5TextEncoder = None
        self.text_encoder: CosmosT5TextEncoder = None
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.dit: MiniTrainDIT = None
        self.dit: MiniTrainDIT = None
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.tokenizer: TokenizerInterface = None
        self.tokenizer: TokenizerInterface = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conditioner = None
        self.conditioner = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.text_guardrail_runner = None
        self.text_guardrail_runner = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.model_names = ["text_encoder", "dit", "tokenizer"] # , "vae", "image_encoder"]
        self.model_names = ["text_encoder", "dit", "tokenizer"]  # , "vae", "image_encoder"]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.height_division_factor = 16
        self.height_division_factor = 16
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.width_division_factor = 16
        self.width_division_factor = 16
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.use_unified_sequence_parallel = False
        self.use_unified_sequence_parallel = False

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def from_config(
    def from_config(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：config: LazyDict,
        config: LazyDict,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dit_path: str = "checkpoints/nvidia/Cosmos-Predict2-2B-Text2Image/model_ema_reg.pt",
        dit_path: str = "checkpoints/nvidia/Cosmos-Predict2-2B-Text2Image/model_ema_reg.pt",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：text_encoder_path: str = "checkpoints/google-t5/t5-11b",
        text_encoder_path: str = "checkpoints/google-t5/t5-11b",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：device: str = "cuda",
        device: str = "cuda",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：torch_dtype: torch.dtype = torch.bfloat16,
        torch_dtype: torch.dtype = torch.bfloat16,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Any:
    ) -> Any:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Create a pipe
        # Create a pipe
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe = Text2ImagePipeline(device=device, torch_dtype=torch_dtype)
        pipe = Text2ImagePipeline(device=device, torch_dtype=torch_dtype)
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

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 2. setup up diffusion processing and scaling~(pre-condition), sampler
        # 2. setup up diffusion processing and scaling~(pre-condition), sampler
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
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.text_encoder = CosmosT5TextEncoder(device=device, cache_dir=text_encoder_path)
        pipe.text_encoder = CosmosT5TextEncoder(device=device, cache_dir=text_encoder_path)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pipe.text_encoder.to(device)
        pipe.text_encoder.to(device)

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
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.text_guardrail_runner = None
            pipe.text_guardrail_runner = None

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 6. Load DiT
        # 6. Load DiT
        # 中文说明：检查运行时假设是否成立；代码：assert dit_path is not None, "dit_path must be provided to load the model"
        assert dit_path is not None, "dit_path must be provided to load the model"
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Loading DiT from {dit_path}")
        log.info(f"Loading DiT from {dit_path}")
        # 中文说明：处理异常、清理资源或管理上下文；代码：with init_weights_on_device():
        with init_weights_on_device():
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_config = config.net
            dit_config = config.net
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.dit = instantiate(dit_config).eval() # inference
            pipe.dit = instantiate(dit_config).eval()  # inference

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
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# pipe.dit.load_state_dict(state_dict, assign=True)
        # pipe.dit.load_state_dict(state_dict, assign=True)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pipe.dit.load_state_dict(state_dict_dit_compatible, strict=False, assign=True)
        pipe.dit.load_state_dict(state_dict_dit_compatible, strict=False, assign=True)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del state_dict, state_dict_dit_compatible
        del state_dict, state_dict_dit_compatible
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.success(f"Successfully loaded DiT from {dit_path}")
        log.success(f"Successfully loaded DiT from {dit_path}")

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

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def denoising_model(self) -> MiniTrainDIT:
    def denoising_model(self) -> MiniTrainDIT:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.dit
        return self.dit

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def encode_prompt(
    def encode_prompt(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, prompts: Union[str, List[str]], max_length: int = 512, return_mask: bool = False
        self, prompts: Union[str, List[str]], max_length: int = 512, return_mask: bool = False
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor:
    ) -> torch.Tensor:
        # 中文说明：根据条件选择执行分支；代码：if isinstance(prompts, str):
        if isinstance(prompts, str):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prompts = [prompts]
            prompts = [prompts]

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.text_encoder.encode_prompts(prompts, max_length=max_length, return_mask=return_ma...
        return self.text_encoder.encode_prompts(prompts, max_length=max_length, return_mask=return_mask)  # type: ignore

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.no_grad()
    @torch.no_grad()
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def decode(self, latent: torch.Tensor) -> torch.Tensor:
    def decode(self, latent: torch.Tensor) -> torch.Tensor:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.tokenizer.decode(latent / self.sigma_data)
        return self.tokenizer.decode(latent / self.sigma_data)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _augment_image_dim_inplace(self, data_batch: dict, input_key: str = None) -> None:
    def _augment_image_dim_inplace(self, data_batch: dict, input_key: str = None) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_key = "images"
        input_key = "images"
        # 中文说明：根据条件选择执行分支；代码：if input_key in data_batch:
        if input_key in data_batch:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Check if the data has already been augmented and avoid re-augmenting
            # Check if the data has already been augmented and avoid re-augmenting
            # 中文说明：根据条件选择执行分支；代码：if IS_PREPROCESSED_KEY in data_batch and data_batch[IS_PREPROCESSED_KEY] is True:
            if IS_PREPROCESSED_KEY in data_batch and data_batch[IS_PREPROCESSED_KEY] is True:
                # 中文说明：检查运行时假设是否成立；代码：assert (
                assert (
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_batch[input_key].shape[2] == 1
                    data_batch[input_key].shape[2] == 1
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"Image data is claimed be augmented while its shape is {data_batch[input_key].shape}"
                ), f"Image data is claimed be augmented while its shape is {data_batch[input_key].shape}"
                # 中文说明：从当前函数返回结果或结束函数执行；代码：return
                return
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch[input_key] = rearrange(data_batch[input_key], "b c h w -> b c 1 h w").contiguous()
                data_batch[input_key] = rearrange(data_batch[input_key], "b c h w -> b c 1 h w").contiguous()
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch[IS_PREPROCESSED_KEY] = True
                data_batch[IS_PREPROCESSED_KEY] = True

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.no_grad()
    @torch.no_grad()
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def encode(self, state: torch.Tensor) -> torch.Tensor:
    def encode(self, state: torch.Tensor) -> torch.Tensor:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.tokenizer.encode(state) * self.sigma_data
        return self.tokenizer.encode(state) * self.sigma_data

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_context_parallel_group() -> Any | None:
    def get_context_parallel_group() -> Any | None:
        # 中文说明：根据条件选择执行分支；代码：if parallel_state.is_initialized():
        if parallel_state.is_initialized():
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return parallel_state.get_context_parallel_group()
            return parallel_state.get_context_parallel_group()
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return None
        return None

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def broadcast_split_for_model_parallelsim(
    def broadcast_split_for_model_parallelsim(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x0_B_C_T_H_W: torch.Tensor,
        x0_B_C_T_H_W: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：condition: torch.Tensor,
        condition: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：epsilon_B_C_T_H_W: torch.Tensor,
        epsilon_B_C_T_H_W: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sigma_B_T: torch.Tensor,
        sigma_B_T: torch.Tensor,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Broadcast and split the input data and condition for model parallelism.
        Currently, we only support context parallelism, but it's disabled for text2image.
        """
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Always disable context parallelism for text2image
        # Always disable context parallelism for text2image
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.dit.disable_context_parallel()
        self.dit.disable_context_parallel()
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x0_B_C_T_H_W, condition, epsilon_B_C_T_H_W, sigma_B_T
        return x0_B_C_T_H_W, condition, epsilon_B_C_T_H_W, sigma_B_T

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_data_and_condition(
    def get_data_and_condition(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, data_batch: dict[str, torch.Tensor]
        self, data_batch: dict[str, torch.Tensor]
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[torch.Tensor, torch.Tensor, T2VCondition]:
    ) -> Tuple[torch.Tensor, torch.Tensor, T2VCondition]:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._augment_image_dim_inplace(data_batch)
        self._augment_image_dim_inplace(data_batch)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Latent state
        # Latent state
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：raw_state = data_batch["images"]
        raw_state = data_batch["images"]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：latent_state = self.encode(raw_state).contiguous().float()
        latent_state = self.encode(raw_state).contiguous().float()

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Condition
        # Condition
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：condition = self.conditioner(data_batch)
        condition = self.conditioner(data_batch)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：condition = condition.edit_data_type(DataType.IMAGE)
        condition = condition.edit_data_type(DataType.IMAGE)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return raw_state, latent_state, condition
        return raw_state, latent_state, condition

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def denoise(
    def denoise(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, xt_B_C_T_H_W: torch.Tensor, sigma: torch.Tensor, condition: T2VCondition, use_cuda_grap...
        self, xt_B_C_T_H_W: torch.Tensor, sigma: torch.Tensor, condition: T2VCondition, use_cuda_graphs: bool = False
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> DenoisePrediction:
    ) -> DenoisePrediction:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Performs denoising on the input noise data, noise level, and condition

        Args:
            xt (torch.Tensor): The input noise data.
            sigma (torch.Tensor): The noise level.
            condition (T2VCondition): conditional information, generated from self.conditioner
            use_cuda_graphs (bool, optional): Whether to use CUDA Graphs for inference. Defaults to False.

        Returns:
            DenoisePrediction: The denoised prediction, it includes clean data predicton (x0), \
                noise prediction (eps_pred).
        """
        # 中文说明：根据条件选择执行分支；代码：if sigma.ndim == 1:
        if sigma.ndim == 1:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_B_T = rearrange(sigma, "b -> b 1")
            sigma_B_T = rearrange(sigma, "b -> b 1")
        # 中文说明：根据条件选择执行分支；代码：elif sigma.ndim == 2:
        elif sigma.ndim == 2:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_B_T = sigma
            sigma_B_T = sigma
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"sigma shape {sigma.shape} is not supported")
            raise ValueError(f"sigma shape {sigma.shape} is not supported")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_B_1_T_1_1 = rearrange(sigma_B_T, "b t -> b 1 t 1 1")
        sigma_B_1_T_1_1 = rearrange(sigma_B_T, "b t -> b 1 t 1 1")
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# get precondition for the network
        # get precondition for the network
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：c_skip_B_1_T_1_1, c_out_B_1_T_1_1, c_in_B_1_T_1_1, c_noise_B_1_T_1_1 = self.scaling(sigma=sig...
        c_skip_B_1_T_1_1, c_out_B_1_T_1_1, c_in_B_1_T_1_1, c_noise_B_1_T_1_1 = self.scaling(sigma=sigma_B_1_T_1_1)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# forward pass through the network
        # forward pass through the network
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net_output_B_C_T_H_W = self.dit(
        net_output_B_C_T_H_W = self.dit(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_C_T_H_W=(xt_B_C_T_H_W * c_in_B_1_T_1_1).to(
            x_B_C_T_H_W=(xt_B_C_T_H_W * c_in_B_1_T_1_1).to(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**self.tensor_kwargs
                **self.tensor_kwargs
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), # Eq. 7 of https://arxiv.org/pdf/2206.00364.pdf
            ),  # Eq. 7 of https://arxiv.org/pdf/2206.00364.pdf
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：timesteps_B_T=c_noise_B_1_T_1_1.squeeze(dim=[1, 3, 4]).to(
            timesteps_B_T=c_noise_B_1_T_1_1.squeeze(dim=[1, 3, 4]).to(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**self.tensor_kwargs
                **self.tensor_kwargs
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), # Eq. 7 of https://arxiv.org/pdf/2206.00364.pdf
            ),  # Eq. 7 of https://arxiv.org/pdf/2206.00364.pdf
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**condition.to_dict(),
            **condition.to_dict(),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_cuda_graphs=use_cuda_graphs,
            use_cuda_graphs=use_cuda_graphs,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：).float()
        ).float()

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x0_pred_B_C_T_H_W = c_skip_B_1_T_1_1 * xt_B_C_T_H_W + c_out_B_1_T_1_1 * net_output_B_C_T_H_W
        x0_pred_B_C_T_H_W = c_skip_B_1_T_1_1 * xt_B_C_T_H_W + c_out_B_1_T_1_1 * net_output_B_C_T_H_W

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# get noise prediction
        # get noise prediction
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：eps_pred_B_C_T_H_W = (xt_B_C_T_H_W - x0_pred_B_C_T_H_W) / sigma_B_1_T_1_1
        eps_pred_B_C_T_H_W = (xt_B_C_T_H_W - x0_pred_B_C_T_H_W) / sigma_B_1_T_1_1

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return DenoisePrediction(x0_pred_B_C_T_H_W, eps_pred_B_C_T_H_W, None)
        return DenoisePrediction(x0_pred_B_C_T_H_W, eps_pred_B_C_T_H_W, None)

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.no_grad()
    @torch.no_grad()
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(
    def __call__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：prompt: str,
        prompt: str,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：negative_prompt: str = "",
        negative_prompt: str = "",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：aspect_ratio: str = "16:9",
        aspect_ratio: str = "16:9",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：seed: int = 0,
        seed: int = 0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：guidance: float = 4.0,
        guidance: float = 4.0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_sampling_step: int = 35,
        num_sampling_step: int = 35,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：use_cuda_graphs: bool = False,
        use_cuda_graphs: bool = False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor | None:
    ) -> torch.Tensor | None:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Parameter check
        # Parameter check
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：width, height = IMAGE_RES_SIZE_INFO[self.config.resolution][aspect_ratio]
        width, height = IMAGE_RES_SIZE_INFO[self.config.resolution][aspect_ratio]
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：height, width = self.check_resize_height_width(height, width)
        height, width = self.check_resize_height_width(height, width)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Run text guardrail on the prompt
        # Run text guardrail on the prompt
        # 中文说明：根据条件选择执行分支；代码：if self.text_guardrail_runner is not None:
        if self.text_guardrail_runner is not None:
            # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.auxiliary.guardrail.common import presets as guardrail_presets
            from videoworld2.auxiliary.guardrail.common import presets as guardrail_presets

            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("Running guardrail check on prompt...")
            log.info("Running guardrail check on prompt...")
            # 中文说明：根据条件选择执行分支；代码：if not guardrail_presets.run_text_guardrail(prompt, self.text_guardrail_runner):
            if not guardrail_presets.run_text_guardrail(prompt, self.text_guardrail_runner):
                # 中文说明：从当前函数返回结果或结束函数执行；代码：return None
                return None
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.success("Passed guardrail on prompt")
                log.success("Passed guardrail on prompt")

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# get sample batch
        # get sample batch
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch = get_sample_batch(resolution=self.config.resolution, aspect_ratio=aspect_ratio, b...
        data_batch = get_sample_batch(resolution=self.config.resolution, aspect_ratio=aspect_ratio, batch_size=1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch["t5_text_embeddings"] = self.encode_prompt(prompt).to(dtype=self.torch_dtype)
        data_batch["t5_text_embeddings"] = self.encode_prompt(prompt).to(dtype=self.torch_dtype)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch["neg_t5_text_embeddings"] = self.encode_prompt(negative_prompt).to(dtype=self.torc...
        data_batch["neg_t5_text_embeddings"] = self.encode_prompt(negative_prompt).to(dtype=self.torch_dtype)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# preprocess
        # preprocess
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._augment_image_dim_inplace(data_batch)
        self._augment_image_dim_inplace(data_batch)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_key = "images"
        input_key = "images"
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
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Obtains the latent state and condition.
        # Obtains the latent state and condition.
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_, latent_state, _ = self.get_data_and_condition(data_batch)
        _, latent_state, _ = self.get_data_and_condition(data_batch)

        # 中文说明：根据条件选择执行分支；代码：if negative_prompt:
        if negative_prompt:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：condition, uncondition = self.conditioner.get_condition_with_negative_prompt(data_batch)
            condition, uncondition = self.conditioner.get_condition_with_negative_prompt(data_batch)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：condition, uncondition = self.conditioner.get_condition_uncondition(data_batch)
            condition, uncondition = self.conditioner.get_condition_uncondition(data_batch)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Ensures we are conditioning on IMAGE data type.
        # Ensures we are conditioning on IMAGE data type.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：condition = condition.edit_data_type(DataType.IMAGE)
        condition = condition.edit_data_type(DataType.IMAGE)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：uncondition = uncondition.edit_data_type(DataType.IMAGE)
        uncondition = uncondition.edit_data_type(DataType.IMAGE)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Context parallelism is disabled for text2image
        # Context parallelism is disabled for text2image
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_, condition, _, _ = self.broadcast_split_for_model_parallelsim(latent_state, condition, None...
        _, condition, _, _ = self.broadcast_split_for_model_parallelsim(latent_state, condition, None, None)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_, uncondition, _, _ = self.broadcast_split_for_model_parallelsim(latent_state, uncondition, ...
        _, uncondition, _, _ = self.broadcast_split_for_model_parallelsim(latent_state, uncondition, None, None)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("Starting image generation...")
        log.info("Starting image generation...")

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

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i, _ in enumerate(tqdm(scheduler.timesteps, desc="Generating image", leave=False)):
        for i, _ in enumerate(tqdm(scheduler.timesteps, desc="Generating image", leave=False)):
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
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cond_x0 = self.denoise(sample, sigma_in, condition, use_cuda_graphs=use_cuda_graphs).x0
            cond_x0 = self.denoise(sample, sigma_in, condition, use_cuda_graphs=use_cuda_graphs).x0
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：uncond_x0 = self.denoise(sample, sigma_in, uncondition, use_cuda_graphs=use_cuda_graphs).x0
            uncond_x0 = self.denoise(sample, sigma_in, uncondition, use_cuda_graphs=use_cuda_graphs).x0
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x0_pred = cond_x0 + guidance * (cond_x0 - uncond_x0)
            x0_pred = cond_x0 + guidance * (cond_x0 - uncond_x0)

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Scheduler step (handles float64 internally, returns original dtype)
            # Scheduler step (handles float64 internally, returns original dtype)
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

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_min = scheduler.sigmas[-1].to(sample.device, dtype=torch.float32)
        sigma_min = scheduler.sigmas[-1].to(sample.device, dtype=torch.float32)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_in = sigma_min.repeat(sample.shape[0])
        sigma_in = sigma_min.repeat(sample.shape[0])

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Final clean pass.
        # Final clean pass.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cond_x0 = self.denoise(sample, sigma_in, condition, use_cuda_graphs=use_cuda_graphs).x0
        cond_x0 = self.denoise(sample, sigma_in, condition, use_cuda_graphs=use_cuda_graphs).x0
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：uncond_x0 = self.denoise(sample, sigma_in, uncondition, use_cuda_graphs=use_cuda_graphs).x0
        uncond_x0 = self.denoise(sample, sigma_in, uncondition, use_cuda_graphs=use_cuda_graphs).x0
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：samples = cond_x0 + guidance * (cond_x0 - uncond_x0)
        samples = cond_x0 + guidance * (cond_x0 - uncond_x0)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# decode
        # decode
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：image = self.decode(samples)
        image = self.decode(samples)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.success("Image generation completed successfully")
        log.success("Image generation completed successfully")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return image
        return image
