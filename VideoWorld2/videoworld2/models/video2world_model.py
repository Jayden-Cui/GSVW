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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from functools import cache
from functools import cache
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import collections
import collections
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import math
import math
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any, Dict, Mapping, Optional, Tuple
from typing import Any, Dict, Mapping, Optional, Tuple
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import copy
import copy
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import attrs
import attrs
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from einops import rearrange
from einops import rearrange
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from megatron.core import parallel_state
from megatron.core import parallel_state
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed.device_mesh import init_device_mesh
from torch.distributed.device_mesh import init_device_mesh
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed.tensor import DTensor
from torch.distributed.tensor import DTensor
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.nn.modules.module import _IncompatibleKeys
from torch.nn.modules.module import _IncompatibleKeys
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.conditioner import DataType, T2VCondition
from videoworld2.conditioner import DataType, T2VCondition
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.configs.base.config_video2world import PREDICT2_VIDEO2WORLD_PIPELINE_2B, PRE...
from videoworld2.configs.base.config_video2world import PREDICT2_VIDEO2WORLD_PIPELINE_2B, PREDICT2_VIDEO2WORLD_PIPELINE_CTRL_2B, Video2WorldPipelineConfig, Video2WorldWithCtrlPipelineConfig
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.configs.base.config_ldm import LDM_DEFAULT, LatentDynamicModelConfig
from videoworld2.configs.base.config_ldm import LDM_DEFAULT, LatentDynamicModelConfig
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import imageio
import imageio
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.networks.model_weights_stats import WeightTrainingStat
from videoworld2.networks.model_weights_stats import WeightTrainingStat
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.pipelines.video2world import Video2WorldPipeline
from videoworld2.pipelines.video2world import Video2WorldPipeline
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.pipelines.video2world_ctrl import Video2WorldPipelineWithCtrl
from videoworld2.pipelines.video2world_ctrl import Video2WorldPipelineWithCtrl
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.utils.checkpointer import non_strict_load_model
from videoworld2.utils.checkpointer import non_strict_load_model
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.utils.optim_instantiate import get_base_scheduler
from videoworld2.utils.optim_instantiate import get_base_scheduler
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.utils.torch_future import clip_grad_norm_
from videoworld2.utils.torch_future import clip_grad_norm_
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import LazyDict, instantiate
from imaginaire.lazy_config import LazyDict, instantiate
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.model import ImaginaireModel
from imaginaire.model import ImaginaireModel
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.io import save_image_or_video
from imaginaire.utils.io import save_image_or_video
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.models.utils import GeometricAugmentor_K, compute_lpips, compute_psnr, compu...
from videoworld2.models.utils import GeometricAugmentor_K, compute_lpips, compute_psnr, compute_ssim
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed.fsdp import ShardingStrategy
from torch.distributed.fsdp import ShardingStrategy
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from lpips import LPIPS
from lpips import LPIPS
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torchvision.transforms as T
import torchvision.transforms as T
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import glob
import glob
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import random
import random
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：IMAGE_KEY = "images"
IMAGE_KEY = "images"
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：VIDEO_KEY = "video"
VIDEO_KEY = "video"
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：RECON_KEY = "reconstructions"
RECON_KEY = "reconstructions"
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：LATENT_KEY = "latent"
LATENT_KEY = "latent"
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：INPUT_KEY = "INPUT"
INPUT_KEY = "INPUT"
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：MASK_KEY = "loss_mask"
MASK_KEY = "loss_mask"
# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：LDM_H, LDM_W = 240, 416
LDM_H, LDM_W = 240, 416

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from decord import VideoReader, cpu
from decord import VideoReader, cpu
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.utils.data import Dataset as BaseDataset
from torch.utils.data import Dataset as BaseDataset
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torchvision.transforms.v2 import UniformTemporalSubsample
from torchvision.transforms.v2 import UniformTemporalSubsample
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.data.dataset_utils import Resize_Preprocess, ToTensorVideo
from videoworld2.data.dataset_utils import Resize_Preprocess, ToTensorVideo

# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _load_video(video_path):
def _load_video(video_path):
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
    # import pdb;pdb.set_trace()
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：vr = VideoReader(video_path, ctx=cpu(0), num_threads=2)
    vr = VideoReader(video_path, ctx=cpu(0), num_threads=2)
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# frame_ids = np.linspace(0, len(vr) - 1).astype(np.int32)
    # frame_ids = np.linspace(0, len(vr) - 1).astype(np.int32)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_ids = np.arange(0, len(vr) - 1).tolist()
    frame_ids = np.arange(0, len(vr) - 1).tolist()
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：vr.seek(0)
    vr.seek(0)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_data = vr.get_batch(frame_ids).asnumpy()
    frame_data = vr.get_batch(frame_ids).asnumpy()
    # 中文说明：开始一个可捕获异常的代码块；代码：try:
    try:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fps = vr.get_avg_fps()
        fps = vr.get_avg_fps()
    # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception: # failed to read FPS
    except Exception:  # failed to read FPS
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fps = 24
        fps = 24
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return frame_data, fps
    return frame_data, fps

# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _get_frames(video_path):
def _get_frames(video_path):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：preprocess = T.Compose([ToTensorVideo(), Resize_Preprocess((480, 832))])
    preprocess = T.Compose([ToTensorVideo(), Resize_Preprocess((480, 832))])
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：frames, fps = _load_video(video_path)
    frames, fps = _load_video(video_path)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = frames.astype(np.uint8)
    frames = frames.astype(np.uint8)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = torch.from_numpy(frames).permute(0, 3, 1, 2) # (l, c, h, w)
    frames = torch.from_numpy(frames).permute(0, 3, 1, 2)  # (l, c, h, w)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = UniformTemporalSubsample(93)(frames)
    frames = UniformTemporalSubsample(93)(frames)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = preprocess(frames)
    frames = preprocess(frames)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = torch.clamp(frames * 255.0, 0, 255).to(torch.uint8)
    frames = torch.clamp(frames * 255.0, 0, 255).to(torch.uint8)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return frames, fps
    return frames, fps



# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Predict2ModelManagerConfig:
class Predict2ModelManagerConfig:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Local path, use it in fast debug run
    # Local path, use it in fast debug run
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dit_path: str = "checkpoints/Cosmos-Predict2-2B-Video2World/model-720p-16fps.pt"
    dit_path: str = "checkpoints/Cosmos-Predict2-2B-Video2World/model-720p-16fps.pt"
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# For inference
    # For inference
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：text_encoder_path: str = "" # not used in training.
    text_encoder_path: str = ""  # not used in training.


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Predict2Video2WorldModelConfig:
class Predict2Video2WorldModelConfig:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：train_architecture: str = "base"
    train_architecture: str = "base"
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：lora_rank: int = 16
    lora_rank: int = 16
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：lora_alpha: int = 16
    lora_alpha: int = 16
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：lora_target_modules: str = "q_proj,k_proj,v_proj,output_proj,mlp.layer1,mlp.layer2"
    lora_target_modules: str = "q_proj,k_proj,v_proj,output_proj,mlp.layer1,mlp.layer2"
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：init_lora_weights: bool = True
    init_lora_weights: bool = True

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：precision: str = "bfloat16"
    precision: str = "bfloat16"
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：input_data_key: str = "video"
    input_data_key: str = "video"
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：input_image_key: str = "images"
    input_image_key: str = "images"
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：loss_reduce: str = "mean"
    loss_reduce: str = "mean"
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：loss_scale: float = 10.0
    loss_scale: float = 10.0

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：adjust_video_noise: bool = True
    adjust_video_noise: bool = True

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# This is used for the original way to load models
    # This is used for the original way to load models
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model_manager_config: Predict2ModelManagerConfig = Predict2ModelManagerConfig()
    model_manager_config: Predict2ModelManagerConfig = Predict2ModelManagerConfig()
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# This is a new way to load models
    # This is a new way to load models
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pipe_config: Video2WorldPipelineConfig = PREDICT2_VIDEO2WORLD_PIPELINE_2B
    pipe_config: Video2WorldPipelineConfig = PREDICT2_VIDEO2WORLD_PIPELINE_2B
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pipe_type: str = 'Video2WorldPipeline'
    pipe_type: str = 'Video2WorldPipeline'
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# debug flag
    # debug flag
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：debug_without_randomness: bool = False
    debug_without_randomness: bool = False
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：fsdp_shard_size: int = 0 # 0 means not using fsdp, -1 means set to world size
    fsdp_shard_size: int = 0  # 0 means not using fsdp, -1 means set to world size
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# High sigma strategy
    # High sigma strategy
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：high_sigma_ratio: float = 0.0
    high_sigma_ratio: float = 0.0
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ldm_config: LatentDynamicModelConfig = LDM_DEFAULT
    ldm_config: LatentDynamicModelConfig = LDM_DEFAULT
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dldm_warmup: bool = False
    dldm_warmup: bool = False
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：only_dit: bool = False
    only_dit: bool = False
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：geometric_aug_on: bool = False
    geometric_aug_on: bool = False
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ldm_act_embedding: bool = False
    ldm_act_embedding: bool = False
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：use_cross_embedding: bool = False
    use_cross_embedding: bool = False

# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Predict2Video2WorldModelWithCtrlConfig:
class Predict2Video2WorldModelWithCtrlConfig:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：train_architecture: str = "base"
    train_architecture: str = "base"
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：lora_rank: int = 16
    lora_rank: int = 16
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：lora_alpha: int = 16
    lora_alpha: int = 16
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：lora_target_modules: str = "q_proj,k_proj,v_proj,output_proj,mlp.layer1,mlp.layer2"
    lora_target_modules: str = "q_proj,k_proj,v_proj,output_proj,mlp.layer1,mlp.layer2"
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：init_lora_weights: bool = True
    init_lora_weights: bool = True

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：precision: str = "bfloat16"
    precision: str = "bfloat16"
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：input_data_key: str = "video"
    input_data_key: str = "video"
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：input_image_key: str = "images"
    input_image_key: str = "images"
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：loss_reduce: str = "mean"
    loss_reduce: str = "mean"
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：loss_scale: float = 10.0
    loss_scale: float = 10.0

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：adjust_video_noise: bool = True
    adjust_video_noise: bool = True

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# This is used for the original way to load models
    # This is used for the original way to load models
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model_manager_config: Predict2ModelManagerConfig = Predict2ModelManagerConfig()
    model_manager_config: Predict2ModelManagerConfig = Predict2ModelManagerConfig()
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# This is a new way to load models
    # This is a new way to load models
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pipe_config: Video2WorldWithCtrlPipelineConfig = PREDICT2_VIDEO2WORLD_PIPELINE_CTRL_2B
    pipe_config: Video2WorldWithCtrlPipelineConfig = PREDICT2_VIDEO2WORLD_PIPELINE_CTRL_2B
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pipe_type: str = 'Video2WorldPipelineWithCtrl'
    pipe_type: str = 'Video2WorldPipelineWithCtrl'
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# debug flag
    # debug flag
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：debug_without_randomness: bool = False
    debug_without_randomness: bool = False
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：fsdp_shard_size: int = 0 # 0 means not using fsdp, -1 means set to world size
    fsdp_shard_size: int = 0  # 0 means not using fsdp, -1 means set to world size
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# High sigma strategy
    # High sigma strategy
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：high_sigma_ratio: float = 0.0
    high_sigma_ratio: float = 0.0
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ldm_config: LatentDynamicModelConfig = LDM_DEFAULT
    ldm_config: LatentDynamicModelConfig = LDM_DEFAULT
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dldm_warmup: bool = False
    dldm_warmup: bool = False
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：only_dit: bool = False
    only_dit: bool = False
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：geometric_aug_on: bool = False
    geometric_aug_on: bool = False
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ldm_act_embedding: bool = False
    ldm_act_embedding: bool = False
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：use_cross_embedding: bool = True
    use_cross_embedding: bool = True
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：finetune_base_model: bool = False
    finetune_base_model: bool = False
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：control_requires_grad: bool = False
    control_requires_grad: bool = False

# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class TokenizerModel(ImaginaireModel):
class TokenizerModel(ImaginaireModel):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, config):
    def __init__(self, config):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.config = config
        self.config = config
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.init_latent_dynamic_model()
        self.init_latent_dynamic_model()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def init_latent_dynamic_model(self):
    def init_latent_dynamic_model(self):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.network = instantiate(self.config.network).to(dtype=torch.bfloat16).cuda()
        self.network = instantiate(self.config.network).to(dtype=torch.bfloat16).cuda()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.loss = instantiate(self.config.loss).to(dtype=torch.bfloat16).cuda()
        self.loss = instantiate(self.config.loss).to(dtype=torch.bfloat16).cuda()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.metric = instantiate(self.config.metric).to(dtype=torch.bfloat16).cuda()
        self.metric = instantiate(self.config.metric).to(dtype=torch.bfloat16).cuda()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：根据条件选择执行分支；代码：if self.config.ldm_path != "":
        if self.config.ldm_path != "":
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"- Loading the LDM Model, load_path: {self.config.ldm_path}...")
            log.info(f"- Loading the LDM Model, load_path: {self.config.ldm_path}...")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ldm_state_dict = torch.load(self.config.ldm_path, map_location=lambda storage, loc: storage, ...
            ldm_state_dict = torch.load(self.config.ldm_path, map_location=lambda storage, loc: storage, weights_only=False)
            # 中文说明：根据条件选择执行分支；代码：if ldm_state_dict.get('model', None):
            if ldm_state_dict.get('model', None):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(self.load_state_dict(ldm_state_dict['model'], strict=False))
                log.info(self.load_state_dict(ldm_state_dict['model'], strict=False))
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(self.load_state_dict(ldm_state_dict, strict=False))
                log.info(self.load_state_dict(ldm_state_dict, strict=False))



# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Predict2Video2WorldModel(ImaginaireModel):
class Predict2Video2WorldModel(ImaginaireModel):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, config):
    def __init__(self, config):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()

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
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# New way to init pipe
        # New way to init pipe
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_ctrl = (config.pipe_type == 'Video2WorldPipelineWithCtrl')
        use_ctrl = (config.pipe_type == 'Video2WorldPipelineWithCtrl')
        # 中文说明：根据条件选择执行分支；代码：if not use_ctrl:
        if not use_ctrl:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.pipe = Video2WorldPipeline.from_config(
            self.pipe = Video2WorldPipeline.from_config(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：config.pipe_config,
                config.pipe_config,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path=config.model_manager_config.dit_path,
                dit_path=config.model_manager_config.dit_path,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.pipe = Video2WorldPipelineWithCtrl.from_config(
            self.pipe = Video2WorldPipelineWithCtrl.from_config(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：config.pipe_config,
                config.pipe_config,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path=config.model_manager_config.dit_path,
                dit_path=config.model_manager_config.dit_path,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.use_ctrl = use_ctrl
        self.use_ctrl = use_ctrl
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
        # 中文说明：根据条件选择执行分支；代码：if use_ctrl and not self.config.finetune_base_model:
        if use_ctrl and not self.config.finetune_base_model:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.pipe.dit.requires_grad_(False)
            self.pipe.dit.requires_grad_(False)
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.pipe.dit_ctrl.train()
            self.pipe.dit_ctrl.train()
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.pipe.dit_ctrl.requires_grad_(True)
            self.pipe.dit_ctrl.requires_grad_(True)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_ctrl_total_params = sum(p.numel() for p in self.pipe.dit_ctrl.parameters() if p.requires_...
            dit_ctrl_total_params = sum(p.numel() for p in self.pipe.dit_ctrl.parameters() if p.requires_grad)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"DiT CTRL total parameters: {dit_ctrl_total_params / 1e9:.2f}B")
            log.info(f"DiT CTRL total parameters: {dit_ctrl_total_params / 1e9:.2f}B")
        # 中文说明：根据条件选择执行分支；代码：elif use_ctrl and self.config.finetune_base_model:
        elif use_ctrl and self.config.finetune_base_model:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.pipe.dit.requires_grad_(True)
            self.pipe.dit.requires_grad_(True)
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.pipe.dit_ctrl.train()
            self.pipe.dit_ctrl.train()
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.pipe.dit_ctrl.requires_grad_(True)
            self.pipe.dit_ctrl.requires_grad_(True)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_ctrl_total_params = sum(p.numel() for p in self.pipe.dit_ctrl.parameters() if p.requires_...
            dit_ctrl_total_params = sum(p.numel() for p in self.pipe.dit_ctrl.parameters() if p.requires_grad)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_total_params = sum(p.numel() for p in self.pipe.dit.parameters() if p.requires_grad)
            dit_total_params = sum(p.numel() for p in self.pipe.dit.parameters() if p.requires_grad)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"DiT total parameters: {dit_total_params / 1e9:.2f}B")
            log.info(f"DiT total parameters: {dit_total_params / 1e9:.2f}B")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"DiT CTRL total parameters: {dit_ctrl_total_params / 1e9:.2f}B")
            log.info(f"DiT CTRL total parameters: {dit_ctrl_total_params / 1e9:.2f}B")
        
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_total_params = sum(p.numel() for p in self.pipe.dit.parameters())
        dit_total_params = sum(p.numel() for p in self.pipe.dit.parameters())
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frozen_params = sum(p.numel() for p in self.parameters() if not p.requires_grad)
        frozen_params = sum(p.numel() for p in self.parameters() if not p.requires_grad)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trainable_params = sum(p.numel() for p in self.parameters() if p.requires_grad)
        trainable_params = sum(p.numel() for p in self.parameters() if p.requires_grad)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.ldm_net = TokenizerModel(self.config.ldm_config)
        self.ldm_net = TokenizerModel(self.config.ldm_config)
  

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ldm_trainable_params = sum(p.numel() for p in self.ldm_net.parameters() if p.requires_grad)
        ldm_trainable_params = sum(p.numel() for p in self.ldm_net.parameters() if p.requires_grad)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Print the number in billions, or in the format of 1,000,000,000
        # Print the number in billions, or in the format of 1,000,000,000
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"DIT total parameters: {dit_total_params / 1e9:.2f}B, Frozen parameters: {frozen_pa...
        log.info(f"DIT total parameters: {dit_total_params / 1e9:.2f}B, Frozen parameters: {frozen_params / 1e9:.2f}B, DiT Trainable parameters: {trainable_params / 1e9:.2f}B, LDM Trainable parameters: {ldm_trainable_params / 1e9:.2f}B")
        
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
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.ldm_net.network = FSDP(self.ldm_net.network, sharding_strategy=ShardingStrategy.NO_SHARD)
            self.ldm_net.network = FSDP(self.ldm_net.network, sharding_strategy=ShardingStrategy.NO_SHARD)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("FSDP (Fully Sharded Data Parallel) is disabled.")
            log.info("FSDP (Fully Sharded Data Parallel) is disabled.")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.validation_results = []
        self.validation_results = []
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dldm_warmup = config.dldm_warmup
        self.dldm_warmup = config.dldm_warmup
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.only_dit = config.only_dit
        self.only_dit = config.only_dit
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.ldm_act_embedding = False
        self.ldm_act_embedding = False
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.geometric_aug_on = config.geometric_aug_on
        self.geometric_aug_on = config.geometric_aug_on
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.geometric_aug = GeometricAugmentor_K()
        self.geometric_aug = GeometricAugmentor_K()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.color_aug = GeometricAugmentor_K(geo_on=False)
        self.color_aug = GeometricAugmentor_K(geo_on=False)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.grayscale_transform = T.Grayscale(num_output_channels=3)
        self.grayscale_transform = T.Grayscale(num_output_channels=3)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.control_requires_grad = False if not use_ctrl else config.control_requires_grad
        self.control_requires_grad = False if not use_ctrl else config.control_requires_grad
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.use_cross_embedding = config.use_cross_embedding
        self.use_cross_embedding = config.use_cross_embedding
    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def net(self) -> torch.nn.Module:
    def net(self) -> torch.nn.Module:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.pipe.dit
        return self.pipe.dit

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# New function, added for i4 adaption
    # New function, added for i4 adaption
    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def net_ema(self) -> torch.nn.Module:
    def net_ema(self) -> torch.nn.Module:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.pipe.dit_ema
        return self.pipe.dit_ema

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# New function, added for i4 adaption
    # New function, added for i4 adaption
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def init_optimizer_scheduler(
    def init_optimizer_scheduler(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, optimizer_config: LazyDict, scheduler_config: LazyDict
        self, optimizer_config: LazyDict, scheduler_config: LazyDict
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> tuple[torch.optim.Optimizer, torch.optim.lr_scheduler.LRScheduler]:
    ) -> tuple[torch.optim.Optimizer, torch.optim.lr_scheduler.LRScheduler]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Creates the optimizer and scheduler for the model.
        """Creates the optimizer and scheduler for the model.

        Args:
            config_model (ModelConfig): The config object for the model.

        Returns:
            optimizer (torch.optim.Optimizer): The model optimizer.
            scheduler (torch.optim.lr_scheduler.LRScheduler): The optimization scheduler.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：optimizer = instantiate(optimizer_config, model=self)
        optimizer = instantiate(optimizer_config, model=self)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scheduler = get_base_scheduler(optimizer, self, scheduler_config)
        scheduler = get_base_scheduler(optimizer, self, scheduler_config)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return optimizer, scheduler
        return optimizer, scheduler

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# ------------------------ training hooks ------------------------
    # ------------------------ training hooks ------------------------
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_before_zero_grad(
    def on_before_zero_grad(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, optimizer: torch.optim.Optimizer, scheduler: torch.optim.lr_scheduler.LRScheduler, iter...
        self, optimizer: torch.optim.Optimizer, scheduler: torch.optim.lr_scheduler.LRScheduler, iteration: int
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        update the net_ema
        """
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del scheduler, optimizer
        del scheduler, optimizer

        # 中文说明：根据条件选择执行分支；代码：if self.config.pipe_config.ema.enabled:
        if self.config.pipe_config.ema.enabled:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# calculate beta for EMA update
            # calculate beta for EMA update
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ema_beta = self.ema_beta(iteration)
            ema_beta = self.ema_beta(iteration)
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.pipe.dit_ema_worker.update_average(self.net, self.net_ema, beta=ema_beta)
            self.pipe.dit_ema_worker.update_average(self.net, self.net_ema, beta=ema_beta)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# New function, added for i4 adaption
    # New function, added for i4 adaption
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_train_start(self, memory_format: torch.memory_format = torch.preserve_format) -> None:
    def on_train_start(self, memory_format: torch.memory_format = torch.preserve_format) -> None:
        # 中文说明：根据条件选择执行分支；代码：if self.config.pipe_config.ema.enabled:
        if self.config.pipe_config.ema.enabled:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.net_ema.to(dtype=torch.float32)
            self.net_ema.to(dtype=torch.float32)
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for module in [self.net, self.pipe.tokenizer, self.ldm_net]:
        for module in [self.net, self.pipe.tokenizer, self.ldm_net]:
            # 中文说明：根据条件选择执行分支；代码：if module is not None:
            if module is not None:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：module.to(memory_format=memory_format, **self.tensor_kwargs)
                module.to(memory_format=memory_format, **self.tensor_kwargs)


    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def freeze_parameters(self) -> None:
    def freeze_parameters(self) -> None:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Freeze parameters
        # Freeze parameters
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.pipe.requires_grad_(False)
        self.pipe.requires_grad_(False)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.pipe.eval()
        self.pipe.eval()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.pipe.denoising_model().train()
        self.pipe.denoising_model().train()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def add_lora_to_model(
    def add_lora_to_model(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model,
        model,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lora_rank=4,
        lora_rank=4,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lora_alpha=4,
        lora_alpha=4,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lora_target_modules="q_proj,k_proj,v_proj,output_proj,mlp.layer1,mlp.layer2",
        lora_target_modules="q_proj,k_proj,v_proj,output_proj,mlp.layer1,mlp.layer2",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：init_lora_weights=True,
        init_lora_weights=True,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from peft import LoraConfig, inject_adapter_in_model
        from peft import LoraConfig, inject_adapter_in_model

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Add LoRA to UNet
        # Add LoRA to UNet
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.lora_alpha = lora_alpha
        self.lora_alpha = lora_alpha

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lora_config = LoraConfig(
        lora_config = LoraConfig(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：r=lora_rank,
            r=lora_rank,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lora_alpha=lora_alpha,
            lora_alpha=lora_alpha,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：init_lora_weights=init_lora_weights,
            init_lora_weights=init_lora_weights,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：target_modules=lora_target_modules.split(","),
            target_modules=lora_target_modules.split(","),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model = inject_adapter_in_model(lora_config, model)
        model = inject_adapter_in_model(lora_config, model)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# for param in model.parameters():
        # for param in model.parameters():
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# # Upcast LoRA parameters into fp32
        #     # Upcast LoRA parameters into fp32
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# if param.requires_grad:
        #     if param.requires_grad:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# param.data = param.to(torch.float32)
        #         param.data = param.to(torch.float32)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# pth = torch.load("checkpoints/posttraining/video2world/2b_openx_lora_onlydit_f93_fps1to4_al...
        # pth = torch.load("checkpoints/posttraining/video2world/2b_openx_lora_onlydit_f93_fps1to4_all_1014/checkpoints/model/iter_000033000.pt")
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# new_pth = {}
        # new_pth = {}
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# for key, val in pth.items():
        # for key, val in pth.items():
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# if "net." in key:
        #     if "net." in key:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# new_pth[key.replace('net.', '')] = val
        #         new_pth[key.replace('net.', '')] = val
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# peft_model.model.load_state_dict(new_pth, strict=False)
        # peft_model.model.load_state_dict(new_pth, strict=False)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# peft_model = peft_model.merge_and_unload()
        # peft_model = peft_model.merge_and_unload()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# save_pth = {}
        # save_pth = {}
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# for key, val in peft_model.state_dict().items():
        # for key, val in peft_model.state_dict().items():
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# save_pth['net.'+key] = val
        #     save_pth['net.'+key] = val
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# torch.save(save_pth, "checkpoints/posttraining/video2world/2b_openx_lora_onlydit_f93_fps1to...
        # torch.save(save_pth, "checkpoints/posttraining/video2world/2b_openx_lora_onlydit_f93_fps1to4_all_1014/checkpoints/model/iter_000033000_merged.pt")
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def setup_data_key(self) -> None:
    def setup_data_key(self) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.input_data_key = self.config.input_data_key # by default it is video key for Video diffu...
        self.input_data_key = self.config.input_data_key  # by default it is video key for Video diffusion model
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.input_image_key = self.config.input_image_key
        self.input_image_key = self.config.input_image_key

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_image_batch(self, data_batch: dict[str, torch.Tensor]) -> bool:
    def is_image_batch(self, data_batch: dict[str, torch.Tensor]) -> bool:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""We hanlde two types of data_batch. One comes from a joint_dataloader where "dataset_name" ...
        """We hanlde two types of data_batch. One comes from a joint_dataloader where "dataset_name" can be used to differenciate image_batch and video_batch.
        Another comes from a dataloader which we by default assumes as video_data for video model training.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_image = self.input_image_key in data_batch
        is_image = self.input_image_key in data_batch
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_video = self.input_data_key in data_batch
        is_video = self.input_data_key in data_batch
        # 中文说明：检查运行时假设是否成立；代码：assert (
        assert (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：is_image != is_video
            is_image != is_video
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), "Only one of the input_image_key or input_data_key should be present in the data_batch."
        ), "Only one of the input_image_key or input_data_key should be present in the data_batch."
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return is_image
        return is_image

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _update_train_stats(self, data_batch: dict[str, torch.Tensor]) -> None:
    def _update_train_stats(self, data_batch: dict[str, torch.Tensor]) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_image = self.is_image_batch(data_batch)
        is_image = self.is_image_batch(data_batch)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_key = self.input_image_key if is_image else self.input_data_key
        input_key = self.input_image_key if is_image else self.input_data_key
        # 中文说明：根据条件选择执行分支；代码：if isinstance(self.pipe.dit, WeightTrainingStat):
        if isinstance(self.pipe.dit, WeightTrainingStat):
            # 中文说明：根据条件选择执行分支；代码：if is_image:
            if is_image:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.pipe.dit.accum_image_sample_counter += data_batch[input_key].shape[0] * self.data_parall...
                self.pipe.dit.accum_image_sample_counter += data_batch[input_key].shape[0] * self.data_parallel_size
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.pipe.dit.accum_video_sample_counter += data_batch[input_key].shape[0] * self.data_parall...
                self.pipe.dit.accum_video_sample_counter += data_batch[input_key].shape[0] * self.data_parallel_size

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def draw_training_sigma_and_epsilon(self, x0_size: torch.Size, condition: Any) -> Tuple[torch...
    def draw_training_sigma_and_epsilon(self, x0_size: torch.Size, condition: Any) -> Tuple[torch.Tensor, torch.Tensor]:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch_size = x0_size[0]
        batch_size = x0_size[0]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：epsilon = torch.randn(x0_size, device="cuda")
        epsilon = torch.randn(x0_size, device="cuda")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_B = self.pipe.scheduler.sample_sigma(batch_size).to(device="cuda")
        sigma_B = self.pipe.scheduler.sample_sigma(batch_size).to(device="cuda")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_B_1 = rearrange(sigma_B, "b -> b 1") # add a dimension for T, all frames share the same...
        sigma_B_1 = rearrange(sigma_B, "b -> b 1")  # add a dimension for T, all frames share the same sigma
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_video_batch = condition.data_type == DataType.VIDEO
        is_video_batch = condition.data_type == DataType.VIDEO

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：multiplier = self.video_noise_multiplier if is_video_batch else 1
        multiplier = self.video_noise_multiplier if is_video_batch else 1
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_B_1 = sigma_B_1 * multiplier
        sigma_B_1 = sigma_B_1 * multiplier
        # 中文说明：根据条件选择执行分支；代码：if is_video_batch and self.config.high_sigma_ratio > 0:
        if is_video_batch and self.config.high_sigma_ratio > 0:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Implement the high sigma strategy LOGUNIFORM200_100000
            # Implement the high sigma strategy LOGUNIFORM200_100000
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：LOG_200 = math.log(200)
            LOG_200 = math.log(200)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：LOG_100000 = math.log(100000)
            LOG_100000 = math.log(100000)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mask = torch.rand(sigma_B_1.shape, device=sigma_B_1.device) < self.config.high_sigma_ratio
            mask = torch.rand(sigma_B_1.shape, device=sigma_B_1.device) < self.config.high_sigma_ratio
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：log_new_sigma = (
            log_new_sigma = (
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.rand(sigma_B_1.shape, device=sigma_B_1.device).type_as(sigma_B_1) * (LOG_100000 - LOG_200)
                torch.rand(sigma_B_1.shape, device=sigma_B_1.device).type_as(sigma_B_1) * (LOG_100000 - LOG_200)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：+ LOG_200
                + LOG_200
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_B_1 = torch.where(mask, log_new_sigma.exp(), sigma_B_1)
            sigma_B_1 = torch.where(mask, log_new_sigma.exp(), sigma_B_1)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return sigma_B_1, epsilon
        return sigma_B_1, epsilon

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_per_sigma_loss_weights(self, sigma: torch.Tensor) -> torch.Tensor:
    def get_per_sigma_loss_weights(self, sigma: torch.Tensor) -> torch.Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Args:
            sigma (tensor): noise level

        Returns:
            loss weights per sigma noise level
        """
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return (sigma**2 + self.pipe.sigma_data**2) / (sigma * self.pipe.sigma_data) ** 2
        return (sigma**2 + self.pipe.sigma_data**2) / (sigma * self.pipe.sigma_data) ** 2

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def compute_loss_with_epsilon_and_sigma(
    def compute_loss_with_epsilon_and_sigma(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x0_B_C_T_H_W: torch.Tensor,
        x0_B_C_T_H_W: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：condition: T2VCondition,
        condition: T2VCondition,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：epsilon_B_C_T_H_W: torch.Tensor,
        epsilon_B_C_T_H_W: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sigma_B_T: torch.Tensor,
        sigma_B_T: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_batch_idx: int,
        data_batch_idx: int,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[dict, torch.Tensor, torch.Tensor, torch.Tensor]:
    ) -> Tuple[dict, torch.Tensor, torch.Tensor, torch.Tensor]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Compute loss givee epsilon and sigma

        This method is responsible for computing loss give epsilon and sigma. It involves:
        1. Adding noise to the input data.
        2. Passing the noisy data through the network to generate predictions.
        3. Computing the loss based on the difference between the predictions and the original data, \
            considering any configured loss weighting.

        Args:
            data_batch (dict): raw data batch draw from the training data loader.
            x0: image/video latent
            condition: text condition
            epsilon: noise
            sigma: noise level

        Returns:
            tuple: A tuple containing four elements:
                - dict: additional data that used to debug / logging / callbacks
                - Tensor 1: kendall loss,
                - Tensor 2: MSE loss,
                - Tensor 3: EDM loss

        Raises:
            AssertionError: If the class is conditional, \
                but no number of classes is specified in the network configuration.

        Notes:
            - The method handles different types of conditioning
            - The method also supports Kendall's loss
        """
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Get the mean and stand deviation of the marginal probability distribution.
        # Get the mean and stand deviation of the marginal probability distribution.
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：mean_B_C_T_H_W, std_B_T = x0_B_C_T_H_W, sigma_B_T
        mean_B_C_T_H_W, std_B_T = x0_B_C_T_H_W, sigma_B_T
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Generate noisy observations
        # Generate noisy observations
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xt_B_C_T_H_W = mean_B_C_T_H_W + epsilon_B_C_T_H_W * rearrange(std_B_T, "b t -> b 1 t 1 1")
        xt_B_C_T_H_W = mean_B_C_T_H_W + epsilon_B_C_T_H_W * rearrange(std_B_T, "b t -> b 1 t 1 1")
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# make prediction
        # make prediction
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_pred = self.pipe.denoise(xt_B_C_T_H_W, sigma_B_T, condition)
        model_pred = self.pipe.denoise(xt_B_C_T_H_W, sigma_B_T, condition)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# loss weights for different noise levels
        # loss weights for different noise levels
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：weights_per_sigma_B_T = self.get_per_sigma_loss_weights(sigma=sigma_B_T)
        weights_per_sigma_B_T = self.get_per_sigma_loss_weights(sigma=sigma_B_T)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# extra loss mask for each sample, for example, human faces, hands
        # extra loss mask for each sample, for example, human faces, hands
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pred_mse_B_C_T_H_W = (x0_B_C_T_H_W - model_pred.x0) ** 2
        pred_mse_B_C_T_H_W = (x0_B_C_T_H_W - model_pred.x0) ** 2

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：edm_loss_B_C_T_H_W = pred_mse_B_C_T_H_W * rearrange(weights_per_sigma_B_T, "b t -> b 1 t 1 1")
        edm_loss_B_C_T_H_W = pred_mse_B_C_T_H_W * rearrange(weights_per_sigma_B_T, "b t -> b 1 t 1 1")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kendall_loss = edm_loss_B_C_T_H_W
        kendall_loss = edm_loss_B_C_T_H_W
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_batch = {
        output_batch = {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："x0": x0_B_C_T_H_W,
            "x0": x0_B_C_T_H_W,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："xt": xt_B_C_T_H_W,
            "xt": xt_B_C_T_H_W,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："sigma": sigma_B_T,
            "sigma": sigma_B_T,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："weights_per_sigma": weights_per_sigma_B_T,
            "weights_per_sigma": weights_per_sigma_B_T,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："condition": condition,
            "condition": condition,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："model_pred": model_pred,
            "model_pred": model_pred,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："mse_loss": pred_mse_B_C_T_H_W.mean(),
            "mse_loss": pred_mse_B_C_T_H_W.mean(),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："edm_loss": edm_loss_B_C_T_H_W.mean(),
            "edm_loss": edm_loss_B_C_T_H_W.mean(),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："edm_loss_per_frame": torch.mean(edm_loss_B_C_T_H_W, dim=[1, 3, 4]),
            "edm_loss_per_frame": torch.mean(edm_loss_B_C_T_H_W, dim=[1, 3, 4]),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_batch["loss"] = kendall_loss.mean() # check if this is what we want
        output_batch["loss"] = kendall_loss.mean()  # check if this is what we want

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return output_batch, kendall_loss, pred_mse_B_C_T_H_W, edm_loss_B_C_T_H_W
        return output_batch, kendall_loss, pred_mse_B_C_T_H_W, edm_loss_B_C_T_H_W

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def gray_transform(self, video):
    def gray_transform(self, video):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ndim = video.ndim
        ndim = video.ndim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = video[0].permute(1, 0, 2, 3) if ndim == 5 else video.permute(1, 0, 2, 3)
        video = video[0].permute(1, 0, 2, 3) if ndim == 5 else video.permute(1, 0, 2, 3)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_gray = self.grayscale_transform(video)
        video_gray = self.grayscale_transform(video)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return video_gray.permute(1, 0, 2, 3)[None]
        return video_gray.permute(1, 0, 2, 3)[None]

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def geo_transform(self, video, gray_on=False):
    def geo_transform(self, video, gray_on=False):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ndim = video.ndim
        ndim = video.ndim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = video[0].permute(1, 0, 2, 3) if ndim == 5 else video.permute(1, 0, 2, 3)
        video = video[0].permute(1, 0, 2, 3) if ndim == 5 else video.permute(1, 0, 2, 3)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = video.float() / 255 #data_batch['video']: B, 3, T, H, W
        video = video.float() / 255 #data_batch['video']: B, 3, T, H, W
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_aug = (self.geometric_aug(video) * 255).to(torch.uint8)
        video_aug = (self.geometric_aug(video) * 255).to(torch.uint8)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_aug = video_aug.permute(1, 0, 2, 3)[None]
        video_aug = video_aug.permute(1, 0, 2, 3)[None]
        # 中文说明：根据条件选择执行分支；代码：if gray_on and random.random() > 0.5:
        if gray_on and random.random() > 0.5:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_aug = self.gray_transform(video_aug)
            video_aug = self.gray_transform(video_aug)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return video_aug
        return video_aug
    
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def color_transform(self, video):
    def color_transform(self, video):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ndim = video.ndim
        ndim = video.ndim
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = video[0].permute(1, 0, 2, 3) if ndim == 5 else video.permute(1, 0, 2, 3)
        video = video[0].permute(1, 0, 2, 3) if ndim == 5 else video.permute(1, 0, 2, 3)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = video.float() / 255 #data_batch['video']: B, 3, T, H, W
        video = video.float() / 255 #data_batch['video']: B, 3, T, H, W
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_aug = (self.color_aug(video) * 255).to(torch.uint8)
        video_aug = (self.color_aug(video) * 255).to(torch.uint8)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_aug = video_aug.permute(1, 0, 2, 3)[None]
        video_aug = video_aug.permute(1, 0, 2, 3)[None]
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return video_aug
        return video_aug
    
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def training_step(self, data_batch: dict, data_batch_idx: int) -> tuple[dict, torch.Tensor]:
    def training_step(self, data_batch: dict, data_batch_idx: int) -> tuple[dict, torch.Tensor]:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank = torch.distributed.get_rank()
        rank = torch.distributed.get_rank()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_ctrl = self.use_ctrl
        use_ctrl = self.use_ctrl
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._update_train_stats(data_batch)
        self._update_train_stats(data_batch)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：b, _, t, h, w = data_batch['video'].shape
        b, _, t, h, w = data_batch['video'].shape
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hint_key = self.config.pipe_config.hint_key if use_ctrl else "video"
        hint_key = self.config.pipe_config.hint_key if use_ctrl else "video"
       
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# NOTE: Aug Video Color For DiT Ctrl
        # NOTE: Aug Video Color For DiT Ctrl
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# show = data_batch["recon_image"][0].permute(1, 2, 3, 0).cpu().numpy()
        # show = data_batch["recon_image"][0].permute(1, 2, 3, 0).cpu().numpy()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# imageio.mimsave('/opt/tiger/test.mp4', show, fps=30)
        # imageio.mimsave('/opt/tiger/test.mp4', show, fps=30)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch['t5_text_embeddings'] = torch.zeros_like(data_batch['t5_text_embeddings'])
        data_batch['t5_text_embeddings'] = torch.zeros_like(data_batch['t5_text_embeddings'])
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ldm_loss_value = 0
        ldm_loss_value = 0
        # 中文说明：根据条件选择执行分支；代码：if self.dldm_warmup:
        if self.dldm_warmup:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.pipe._normalize_video_databatch_inplace(data_batch)
            self.pipe._normalize_video_databatch_inplace(data_batch)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dldm_data_batch = copy.deepcopy(data_batch)
            dldm_data_batch = copy.deepcopy(data_batch)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dldm_data_batch['video'] = torch.nn.functional.interpolate(dldm_data_batch['video'].permute(0...
            dldm_data_batch['video'] = torch.nn.functional.interpolate(dldm_data_batch['video'].permute(0, 2, 1, 3, 4).flatten(0, 1), size=(LDM_H, LDM_W), mode='bilinear', align_corners=False).view(b, t, 3, LDM_H, LDM_W).permute(0, 2, 1, 3, 4)            
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ldm_output_batch, ldm_recon_loss, crossattn_embed = self.ldm_training_step(dldm_data_batch, d...
            ldm_output_batch, ldm_recon_loss, crossattn_embed = self.ldm_training_step(dldm_data_batch, data_batch_idx)
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return ldm_output_batch, ldm_recon_loss
            return ldm_output_batch, ldm_recon_loss
        # 中文说明：根据条件选择执行分支；代码：elif self.only_dit:
        elif self.only_dit:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：output_batch, kendall_loss = self.pipe_training_step(data_batch, data_batch_idx)
            output_batch, kendall_loss = self.pipe_training_step(data_batch, data_batch_idx)
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return output_batch, kendall_loss
            return output_batch, kendall_loss
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dldm_tensor_batch = torch.nn.functional.interpolate(((data_batch["video"] / 127.5) - 1).permu...
            dldm_tensor_batch = torch.nn.functional.interpolate(((data_batch["video"] / 127.5) - 1).permute(0, 2, 1, 3, 4).flatten(0, 1), size=(LDM_H, LDM_W), mode='bilinear', align_corners=False).view(b, t, 3, LDM_H, LDM_W).permute(0, 2, 1, 3, 4).to(torch.bfloat16)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：encoded_video, _, (quant_codes, _), _ = self.ldm_net.network.encode(dldm_tensor_batch)
            encoded_video, _, (quant_codes, _), _ = self.ldm_net.network.encode(dldm_tensor_batch)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：recon_image = self.ldm_net.network.decode(encoded_video, quant_codes.detach())
            recon_image = self.ldm_net.network.decode(encoded_video, quant_codes.detach()) 
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ori_recon_image = recon_image
            ori_recon_image = recon_image
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：recon_image = torch.nn.functional.interpolate(recon_image[0].permute(1, 0, 2, 3), size=(data_...
            recon_image = torch.nn.functional.interpolate(recon_image[0].permute(1, 0, 2, 3), size=(data_batch['video'].shape[-2], data_batch['video'].shape[-1]), mode='bilinear', align_corners=False).permute(1, 0, 2, 3)[None]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：recon_image = (((recon_image[0] * 0.5) + 0.5).clamp(0, 1)) * 255
            recon_image = (((recon_image[0] * 0.5) + 0.5).clamp(0, 1)) * 255
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：recon_image = recon_image[None] if recon_image.ndim == 4 else recon_image
            recon_image = recon_image[None] if recon_image.ndim == 4 else recon_image
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gray_video = self.gray_transform(recon_image)
            gray_video = self.gray_transform(recon_image)

            # 中文说明：检查运行时假设是否成立；代码：assert self.use_cross_embedding
            assert self.use_cross_embedding
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant = self.ldm_net.network.post_quant_conv(quant_codes)
            quant = self.ldm_net.network.post_quant_conv(quant_codes)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant = self.ldm_net.network.quant_to_dit_dim(quant).flatten(2)
            quant = self.ldm_net.network.quant_to_dit_dim(quant).flatten(2)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant = quant.permute(0, 2, 1)
            quant = quant.permute(0, 2, 1)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：crossattn_embed = torch.cat([quant, torch.zeros((1, 512 - quant.shape[1], 1024)).to(quant)], ...
            crossattn_embed = torch.cat([quant, torch.zeros((1, 512 - quant.shape[1], 1024)).to(quant)], dim=1)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch['t5_text_embeddings'] = crossattn_embed
            data_batch['t5_text_embeddings'] = crossattn_embed

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：inputs = {INPUT_KEY: dldm_tensor_batch, MASK_KEY: data_batch.get("loss_mask", torch.ones_like...
            inputs = {INPUT_KEY: dldm_tensor_batch, MASK_KEY: data_batch.get("loss_mask", torch.ones_like(dldm_tensor_batch))}
    
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_, ldm_loss_value = self.ldm_net.loss(inputs, {"reconstructions": ori_recon_image}, iteration=0)
            _, ldm_loss_value = self.ldm_net.loss(inputs, {"reconstructions": ori_recon_image}, iteration=0)
            
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch['video'] = self.color_transform(data_batch["video"])
            data_batch['video'] = self.color_transform(data_batch["video"])
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gray_video = (gray_video.to(torch.bfloat16) / 127.5) - 1
            gray_video = (gray_video.to(torch.bfloat16) / 127.5) - 1
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gray_video = gray_video.detach()
            gray_video = gray_video.detach()
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.pipe._normalize_video_databatch_inplace(data_batch)
            self.pipe._normalize_video_databatch_inplace(data_batch)

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch['recon_image'] = gray_video
            data_batch['recon_image'] = gray_video
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：output_batch, kendall_loss = self.pipe_training_step(data_batch, data_batch_idx)
            output_batch, kendall_loss = self.pipe_training_step(data_batch, data_batch_idx)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kendall_loss = kendall_loss + ldm_loss_value
            kendall_loss = kendall_loss + ldm_loss_value
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return output_batch, kendall_loss
            return output_batch, kendall_loss      
        

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def ldm_training_step(self, data_batch, data_batch_idx):
    def ldm_training_step(self, data_batch, data_batch_idx):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：根据条件选择执行分支；代码：if data_batch.get('video_aug_0', None) is not None:
        if data_batch.get('video_aug_0', None) is not None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tensor_batch_aug_0 = data_batch['video_aug_0'][:, :, :1]
            tensor_batch_aug_0 = data_batch['video_aug_0'][:, :, :1]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tensor_batch_aug_1 = data_batch['video_aug_1']
            tensor_batch_aug_1 = data_batch['video_aug_1']

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_dict = self.ldm_net.network(tensor_batch_aug_0, tensor_batch_aug_1)
            output_dict = self.ldm_net.network(tensor_batch_aug_0, tensor_batch_aug_1)

        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tensor_batch = data_batch["video"]
            tensor_batch = data_batch["video"]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_dict = self.ldm_net.network(tensor_batch)
            output_dict = self.ldm_net.network(tensor_batch)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：input_images, recon_image, mid_h = data_batch["video"], output_dict["reconstructions"], outpu...
        input_images, recon_image, mid_h = data_batch["video"], output_dict["reconstructions"], output_dict["mid_h"]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：inputs = {INPUT_KEY: input_images, MASK_KEY: data_batch.get("loss_mask", torch.ones_like(inpu...
        inputs = {INPUT_KEY: input_images, MASK_KEY: data_batch.get("loss_mask", torch.ones_like(input_images))}
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：loss_dict, loss_value = self.ldm_net.loss(inputs, output_dict, iteration=0)
        loss_dict, loss_value = self.ldm_net.loss(inputs, output_dict, iteration=0)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant_codes = output_dict['quant_codes']
        quant_codes = output_dict['quant_codes']
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant = self.ldm_net.network.post_quant_conv(quant_codes)
        quant = self.ldm_net.network.post_quant_conv(quant_codes)
        # 中文说明：根据条件选择执行分支；代码：if self.ldm_net.network.connector_type == 'llama':
        if self.ldm_net.network.connector_type == 'llama':
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant = self.ldm_net.network.quant_to_dit_dim(quant)
            quant = self.ldm_net.network.quant_to_dit_dim(quant)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant = self.ldm_net.network.quant_to_dit_dim(quant).flatten(2)
            quant = self.ldm_net.network.quant_to_dit_dim(quant).flatten(2)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant = quant.permute(0, 2, 1)
            quant = quant.permute(0, 2, 1)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return dict({"prediction": recon_image, "mid_h": mid_h, "loss": loss_value}), loss_value, quant
        return dict({"prediction": recon_image, "mid_h": mid_h, "loss": loss_value}), loss_value, quant

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.no_grad()
    @torch.no_grad()
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def validation_step(self, data_batch: dict[str, torch.Tensor], iteration: int) -> tuple[dict[...
    def validation_step(self, data_batch: dict[str, torch.Tensor], iteration: int) -> tuple[dict[str, torch.Tensor], torch.Tensor]:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank = torch.distributed.get_rank()
        rank = torch.distributed.get_rank()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：local_dir = data_batch['local_dir']
        local_dir = data_batch['local_dir']
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：val_iter = data_batch['val_iter']
        val_iter = data_batch['val_iter']
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del data_batch['local_dir']
        del data_batch['local_dir']
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del data_batch['val_iter']
        del data_batch['val_iter']
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for name in data_batch.keys():
        for name in data_batch.keys():
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch[name] = data_batch[name][0] if isinstance(data_batch[name], torch.Tensor) and data...
            data_batch[name] = data_batch[name][0] if isinstance(data_batch[name], torch.Tensor) and data_batch[name].ndim==6 else data_batch[name]

        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.pipe._normalize_video_databatch_inplace(data_batch)
        self.pipe._normalize_video_databatch_inplace(data_batch)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch_size = data_batch['video'].shape[0]
        batch_size = data_batch['video'].shape[0]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_name = '_'.join(data_batch['video_name']['video_path'][0].split('/')[-1].split('_')[:-1])
        video_name = '_'.join(data_batch['video_name']['video_path'][0].split('/')[-1].split('_')[:-1])
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = None
        video = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_video = []
        output_video = []
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant_infos = []
        quant_infos = []

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for bz in range(batch_size):
        for bz in range(batch_size):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_video = data_batch['video'][bz][None]
            input_video = data_batch['video'][bz][None]

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ldm_tensor_batch = input_video
            ldm_tensor_batch = input_video
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ldm_tensor_batch = torch.nn.functional.interpolate(ldm_tensor_batch[0].permute(1, 0, 2, 3), s...
            ldm_tensor_batch = torch.nn.functional.interpolate(ldm_tensor_batch[0].permute(1, 0, 2, 3), size=(LDM_H, LDM_W), mode='bilinear', align_corners=False).permute(1, 0, 2, 3)[None]
            # 中文说明：根据条件选择执行分支；代码：if bz == 0:
            if bz == 0:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：encoded_video, quant_info, (quant_codes, _), _ = self.ldm_net.network.encode(ldm_tensor_batch)
                encoded_video, quant_info, (quant_codes, _), _ = self.ldm_net.network.encode(ldm_tensor_batch)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：recon_image = self.ldm_net.network.decode(encoded_video, quant_codes)
                recon_image = self.ldm_net.network.decode(encoded_video, quant_codes) 

            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：encoded_video_ori, quant_info, (quant_codes, _), _ = self.ldm_net.network.encode(ldm_tensor_b...
                encoded_video_ori, quant_info, (quant_codes, _), _ = self.ldm_net.network.encode(ldm_tensor_batch)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：encoded_video, _ = self.ldm_net.network.encoder(last_frame)
                encoded_video, _ = self.ldm_net.network.encoder(last_frame)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：recon_image = self.ldm_net.network.decode(encoded_video, quant_codes)
                recon_image = self.ldm_net.network.decode(encoded_video, quant_codes) 
                
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# _recon_image = self.ldm_net.network.decode(encoded_video_ori, quant_codes)
                # _recon_image = self.ldm_net.network.decode(encoded_video_ori, quant_codes) 
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# _recon_image = torch.nn.functional.interpolate(_recon_image[0].permute(1, 0, 2, 3), size=(d...
                # _recon_image = torch.nn.functional.interpolate(_recon_image[0].permute(1, 0, 2, 3), size=(data_batch['video'].shape[-2], data_batch['video'].shape[-1]), mode='bilinear', align_corners=False).permute(0, 2, 3, 1)
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# _recon_image = (((_recon_image * 0.5) + 0.5).clamp(0, 1))
                # _recon_image = (((_recon_image * 0.5) + 0.5).clamp(0, 1))
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# _recon_image = (_recon_image * 255).to(torch.uint8).cpu().numpy()
                # _recon_image = (_recon_image * 255).to(torch.uint8).cpu().numpy()
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# imageio.mimsave(os.path.join(local_dir, f"{video_name}_{bz}.mp4"), _recon_image, fps=30)
                # imageio.mimsave(os.path.join(local_dir, f"{video_name}_{bz}.mp4"), _recon_image, fps=30)

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：last_frame = recon_image[:, :, -1:]
            last_frame = recon_image[:, :, -1:]
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：output_video.append(recon_image[:, :, :-1])
            output_video.append(recon_image[:, :, :-1])
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：quant_infos.append(quant_info.flatten().cpu())
            quant_infos.append(quant_info.flatten().cpu())

       
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# all_input_video = data_batch['video'].permute(1, 0, 2, 3, 4).flatten(1, 2)
        # all_input_video = data_batch['video'].permute(1, 0, 2, 3, 4).flatten(1, 2)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# all_input_video = (((all_input_video * 0.5) + 0.5).clamp(0, 1)).permute(1, 2, 3, 0)
        # all_input_video = (((all_input_video * 0.5) + 0.5).clamp(0, 1)).permute(1, 2, 3, 0)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# all_input_video = (all_input_video * 255).to(torch.uint8).cpu().numpy()
        # all_input_video = (all_input_video * 255).to(torch.uint8).cpu().numpy()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# imageio.mimsave(os.path.join(local_dir, f"{video_name}_ori.mp4"), all_input_video, fps=30)
        # imageio.mimsave(os.path.join(local_dir, f"{video_name}_ori.mp4"), all_input_video, fps=30)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_video = torch.cat(output_video, dim=2)
        output_video = torch.cat(output_video, dim=2)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_video = torch.nn.functional.interpolate(output_video[0].permute(1, 0, 2, 3), size=(dat...
        output_video = torch.nn.functional.interpolate(output_video[0].permute(1, 0, 2, 3), size=(data_batch['video'].shape[-2], data_batch['video'].shape[-1]), mode='bilinear', align_corners=False).permute(0, 2, 3, 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_video = (((output_video * 0.5) + 0.5).clamp(0, 1))
        output_video = (((output_video * 0.5) + 0.5).clamp(0, 1))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_video = (output_video * 255).to(torch.uint8).cpu().numpy()
        output_video = (output_video * 255).to(torch.uint8).cpu().numpy()
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：imageio.mimsave(os.path.join(local_dir, f"{video_name}.mp4"), output_video, fps=30)
        imageio.mimsave(os.path.join(local_dir, f"{video_name}.mp4"), output_video, fps=30)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant_infos = torch.stack(quant_infos, dim=0)
        quant_infos = torch.stack(quant_infos, dim=0)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out = {
        out = {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：'global_step': iteration,
            'global_step': iteration,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：'latent_codes': quant_infos,
            'latent_codes': quant_infos,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：'video_path': video_name,
            'video_path': video_name,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：'local_dir': local_dir,
            'local_dir': local_dir,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        } 
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.validation_results.append(out)
        self.validation_results.append(out)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return {"result": recon_image}, torch.tensor([0]).to('cuda').to(torch.bfloat16)
        return {"result": recon_image}, torch.tensor([0]).to('cuda').to(torch.bfloat16)


        


    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def pipe_training_step(self, data_batch: dict, data_batch_idx: int) -> tuple[dict, torch.Tens...
    def pipe_training_step(self, data_batch: dict, data_batch_idx: int) -> tuple[dict, torch.Tensor]:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.pipe.device = self.device
        self.pipe.device = self.device

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Get the input data to noise and denoise~(image, video) and the corresponding conditioner.
        # Get the input data to noise and denoise~(image, video) and the corresponding conditioner.
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_, x0_B_C_T_H_W, condition = self.pipe.get_data_and_condition(data_batch)
        _, x0_B_C_T_H_W, condition = self.pipe.get_data_and_condition(data_batch)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Sample pertubation noise levels and N(0, 1) noises
        # Sample pertubation noise levels and N(0, 1) noises
        

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sigma_B_T, epsilon_B_C_T_H_W = self.draw_training_sigma_and_epsilon(x0_B_C_T_H_W.size(), cond...
        sigma_B_T, epsilon_B_C_T_H_W = self.draw_training_sigma_and_epsilon(x0_B_C_T_H_W.size(), condition)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Broadcast and split the input data and condition for model parallelism
        # Broadcast and split the input data and condition for model parallelism
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x0_B_C_T_H_W, condition, epsilon_B_C_T_H_W, sigma_B_T = self.pipe.broadcast_split_for_model_p...
        x0_B_C_T_H_W, condition, epsilon_B_C_T_H_W, sigma_B_T = self.pipe.broadcast_split_for_model_parallelsim(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x0_B_C_T_H_W, condition, epsilon_B_C_T_H_W, sigma_B_T
            x0_B_C_T_H_W, condition, epsilon_B_C_T_H_W, sigma_B_T
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：output_batch, kendall_loss, _, _ = self.compute_loss_with_epsilon_and_sigma(
        output_batch, kendall_loss, _, _ = self.compute_loss_with_epsilon_and_sigma(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x0_B_C_T_H_W, condition, epsilon_B_C_T_H_W, sigma_B_T, data_batch_idx
            x0_B_C_T_H_W, condition, epsilon_B_C_T_H_W, sigma_B_T, data_batch_idx
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：根据条件选择执行分支；代码：if self.loss_reduce == "mean":
        if self.loss_reduce == "mean":
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kendall_loss = kendall_loss.mean() * self.loss_scale
            kendall_loss = kendall_loss.mean() * self.loss_scale
        # 中文说明：根据条件选择执行分支；代码：elif self.loss_reduce == "sum":
        elif self.loss_reduce == "sum":
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kendall_loss = kendall_loss.sum(dim=1).mean() * self.loss_scale
            kendall_loss = kendall_loss.sum(dim=1).mean() * self.loss_scale
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Invalid loss_reduce: {self.loss_reduce}")
            raise ValueError(f"Invalid loss_reduce: {self.loss_reduce}")

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return output_batch, kendall_loss
        return output_batch, kendall_loss

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# ------------------ Checkpointing ------------------
    # ------------------ Checkpointing ------------------

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def state_dict(self) -> Dict[str, Any]:
    def state_dict(self) -> Dict[str, Any]:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# the checkpoint format should be compatible with traditional imaginaire4
        # the checkpoint format should be compatible with traditional imaginaire4
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# pipeline contains both net and net_ema
        # pipeline contains both net and net_ema
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# checkpoint should be saved/loaded from Model
        # checkpoint should be saved/loaded from Model
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# checkpoint should be loadable from pipeline as well - We don't use Model for inference only...
        # checkpoint should be loadable from pipeline as well - We don't use Model for inference only jobs.

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net_state_dict = self.pipe.dit.state_dict(prefix="net.")
        net_state_dict = self.pipe.dit.state_dict(prefix="net.")
        # 中文说明：根据条件选择执行分支；代码：if self.config.pipe_config.ema.enabled:
        if self.config.pipe_config.ema.enabled:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ema_state_dict = self.pipe.dit_ema.state_dict(prefix="net_ema.")
            ema_state_dict = self.pipe.dit_ema.state_dict(prefix="net_ema.")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：net_state_dict.update(ema_state_dict)
            net_state_dict.update(ema_state_dict)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# convert DTensor to Tensor
        # convert DTensor to Tensor
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key, val in net_state_dict.items():
        for key, val in net_state_dict.items():
            # 中文说明：根据条件选择执行分支；代码：if isinstance(val, DTensor):
            if isinstance(val, DTensor):
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Convert to full tensor
                # Convert to full tensor
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net_state_dict[key] = val.full_tensor().detach().cpu()
                net_state_dict[key] = val.full_tensor().detach().cpu()
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net_state_dict[key] = val.detach().cpu()
                net_state_dict[key] = val.detach().cpu()

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ldm_state_dict = self.ldm_net.state_dict(prefix="ldm_net.")
        ldm_state_dict = self.ldm_net.state_dict(prefix="ldm_net.")
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# convert DTensor to Tensor
        # convert DTensor to Tensor
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key, val in ldm_state_dict.items():
        for key, val in ldm_state_dict.items():
            # 中文说明：根据条件选择执行分支；代码：if 'loss.' in key:
            if 'loss.' in key:
                # 中文说明：执行循环控制或空操作；代码：continue
                continue
            # 中文说明：根据条件选择执行分支；代码：if isinstance(val, DTensor):
            if isinstance(val, DTensor):
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Convert to full tensor
                # Convert to full tensor
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net_state_dict[key] = val.full_tensor().detach().cpu()
                net_state_dict[key] = val.full_tensor().detach().cpu()
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net_state_dict[key] = val.detach().cpu()
                net_state_dict[key] = val.detach().cpu()
        # 中文说明：根据条件选择执行分支；代码：if self.use_ctrl:
        if self.use_ctrl:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net_ctrl_state_dict = self.pipe.dit_ctrl.state_dict(prefix="net_ctrl.")
            net_ctrl_state_dict = self.pipe.dit_ctrl.state_dict(prefix="net_ctrl.")
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# convert DTensor to Tensor
            # convert DTensor to Tensor
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key, val in net_ctrl_state_dict.items():
            for key, val in net_ctrl_state_dict.items():
                # 中文说明：根据条件选择执行分支；代码：if isinstance(val, DTensor):
                if isinstance(val, DTensor):
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Convert to full tensor
                    # Convert to full tensor
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net_state_dict[key] = val.full_tensor().detach().cpu()
                    net_state_dict[key] = val.full_tensor().detach().cpu()
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net_state_dict[key] = val.detach().cpu()
                    net_state_dict[key] = val.detach().cpu()

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return net_state_dict
        return net_state_dict

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def load_state_dict(self, state_dict: Mapping[str, Any], strict: bool = True, assign: bool = ...
    def load_state_dict(self, state_dict: Mapping[str, Any], strict: bool = True, assign: bool = False):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Loads a state dictionary into the model and optionally its EMA counterpart.
        Different from torch strict=False mode, the method will not raise error for unmatched state shape while raise warning.

        Parameters:e
            state_dict (Mapping[str, Any]): A dictionary containing separate state dictionaries for the model and
                                            potentially for an EMA version of the model under the keys 'model' and 'ema', respectively.
            strict (bool, optional): If True, the method will enforce that the keys in the state dict match exactly
                                    those in the model and EMA model (if applicable). Defaults to True.
            assign (bool, optional): If True and in strict mode, will assign the state dictionary directly rather than
                                    matching keys one-by-one. This is typically used when loading parts of state dicts
                                    or using customized loading procedures. Defaults to False.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_reg_state_dict = collections.OrderedDict()
        _reg_state_dict = collections.OrderedDict()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_ema_state_dict = collections.OrderedDict()
        _ema_state_dict = collections.OrderedDict()
        
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for k, v in state_dict.items():
        for k, v in state_dict.items():
            # 中文说明：根据条件选择执行分支；代码：if k.startswith("net."):
            if k.startswith("net."):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_reg_state_dict[k.replace("net.", "")] = v
                _reg_state_dict[k.replace("net.", "")] = v
            # 中文说明：根据条件选择执行分支；代码：elif k.startswith("net_ema."):
            elif k.startswith("net_ema."):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_ema_state_dict[k.replace("net_ema.", "")] = v
                _ema_state_dict[k.replace("net_ema.", "")] = v

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# NOTE: DEBUG
        # NOTE: DEBUG
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# dp_mesh = self.pipe.dit.blocks[0]._checkpoint_wrapped_module.self_attn.k_norm.weight.device...
        # dp_mesh = self.pipe.dit.blocks[0]._checkpoint_wrapped_module.self_attn.k_norm.weight.device_mesh
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# for n, p in self.pipe.dit.named_parameters():
        # for n, p in self.pipe.dit.named_parameters():
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# if isinstance(p, torch.distributed.tensor.DTensor):
        #     if isinstance(p, torch.distributed.tensor.DTensor):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# _reg_state_dict[n] = dist_tensor.DTensor.from_local(v, dp_mesh)
        #         _reg_state_dict[n] = dist_tensor.DTensor.from_local(v, dp_mesh)
        
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dict = _reg_state_dict
        state_dict = _reg_state_dict

        # 中文说明：根据条件选择执行分支；代码：if strict:
        if strict:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：reg_results: _IncompatibleKeys = self.pipe.dit.load_state_dict(
            reg_results: _IncompatibleKeys = self.pipe.dit.load_state_dict(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_reg_state_dict, strict=strict, assign=assign
                _reg_state_dict, strict=strict, assign=assign
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

            # 中文说明：根据条件选择执行分支；代码：if self.config.pipe_config.ema.enabled:
            if self.config.pipe_config.ema.enabled:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ema_results: _IncompatibleKeys = self.pipe.dit_ema.load_state_dict(
                ema_results: _IncompatibleKeys = self.pipe.dit_ema.load_state_dict(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_ema_state_dict, strict=strict, assign=assign
                    _ema_state_dict, strict=strict, assign=assign
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )

            # 中文说明：从当前函数返回结果或结束函数执行；代码：return _IncompatibleKeys(
            return _IncompatibleKeys(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：missing_keys=reg_results.missing_keys
                missing_keys=reg_results.missing_keys
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：+ (ema_results.missing_keys if self.config.pipe_config.ema.enabled else []),
                + (ema_results.missing_keys if self.config.pipe_config.ema.enabled else []),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：unexpected_keys=reg_results.unexpected_keys
                unexpected_keys=reg_results.unexpected_keys
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：+ (ema_results.unexpected_keys if self.config.pipe_config.ema.enabled else []),
                + (ema_results.unexpected_keys if self.config.pipe_config.ema.enabled else []),
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.critical("load model in non-strict mode")
            log.critical("load model in non-strict mode")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.critical(non_strict_load_model(self.pipe.dit, _reg_state_dict), rank0_only=False)
            log.critical(non_strict_load_model(self.pipe.dit, _reg_state_dict), rank0_only=False)
            # 中文说明：根据条件选择执行分支；代码：if self.config.pipe_config.ema.enabled:
            if self.config.pipe_config.ema.enabled:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.critical("load ema model in non-strict mode")
                log.critical("load ema model in non-strict mode")
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.critical(non_strict_load_model(self.pipe.dit_ema, _ema_state_dict), rank0_only=False)
                log.critical(non_strict_load_model(self.pipe.dit_ema, _ema_state_dict), rank0_only=False)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# ------------------ public methods ------------------
    # ------------------ public methods ------------------
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def ema_beta(self, iteration: int) -> float:
    def ema_beta(self, iteration: int) -> float:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Calculate the beta value for EMA update.
        weights = weights * beta + (1 - beta) * new_weights

        Args:
            iteration (int): Current iteration number.

        Returns:
            float: The calculated beta value.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iteration = iteration + self.config.pipe_config.ema.iteration_shift
        iteration = iteration + self.config.pipe_config.ema.iteration_shift
        # 中文说明：根据条件选择执行分支；代码：if iteration < 1:
        if iteration < 1:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return 0.0
            return 0.0
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return (1 - 1 / (iteration + 1)) ** (self.pipe.ema_exp_coefficient + 1)
        return (1 - 1 / (iteration + 1)) ** (self.pipe.ema_exp_coefficient + 1)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def clip_grad_norm_(
    def clip_grad_norm_(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_norm: float,
        max_norm: float,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：norm_type: float = 2.0,
        norm_type: float = 2.0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：error_if_nonfinite: bool = False,
        error_if_nonfinite: bool = False,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：foreach: Optional[bool] = None,
        foreach: Optional[bool] = None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor:
    ) -> torch.Tensor:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return clip_grad_norm_(
        return clip_grad_norm_(
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.net.parameters(),
            self.net.parameters(),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_norm,
            max_norm,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：norm_type=norm_type,
            norm_type=norm_type,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：error_if_nonfinite=error_if_nonfinite,
            error_if_nonfinite=error_if_nonfinite,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：foreach=foreach,
            foreach=foreach,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
    
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Predict2Video2WorldModelWithCtrl(Predict2Video2WorldModel):
class Predict2Video2WorldModelWithCtrl(Predict2Video2WorldModel):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def training_step(self, data_batch: dict, data_batch_idx: int) -> tuple[dict, torch.Tensor]:
    def training_step(self, data_batch: dict, data_batch_idx: int) -> tuple[dict, torch.Tensor]:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch['use_ctrl'] = True
        data_batch['use_ctrl'] = True
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return super().training_step(data_batch, data_batch_idx)
        return super().training_step(data_batch, data_batch_idx)

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.no_grad()
    @torch.no_grad()
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def inference(self, frame, latent_dynamic_codes):
    def inference(self, frame, latent_dynamic_codes):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：#latent_dynamic_codes: [N, L]
        #latent_dynamic_codes: [N, L]
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# frames: [1, 3, 1, H, W]
        # frames: [1, 3, 1, H, W]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：clip_num = latent_dynamic_codes.shape[0]
        clip_num = latent_dynamic_codes.shape[0]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dldm_query_length = 4
        dldm_query_length = 4
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_downsampling = 4
        temporal_downsampling = 4
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：clip_length = (latent_dynamic_codes.shape[1] // dldm_query_length) * temporal_downsampling + 1
        clip_length = (latent_dynamic_codes.shape[1] // dldm_query_length) * temporal_downsampling  + 1
        
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame = ((frame / 127.5) - 1).to(torch.bfloat16) # [1, 3, 1, H, W]
        frame = ((frame / 127.5) - 1).to(torch.bfloat16)  # [1, 3, 1, H, W]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：last_frame = torch.nn.functional.interpolate(frame[0].permute(1, 0, 2, 3), size=(LDM_H, LDM_W...
        last_frame = torch.nn.functional.interpolate(frame[0].permute(1, 0, 2, 3), size=(LDM_H, LDM_W), mode='bilinear', align_corners=False).permute(1, 0, 2, 3)[None]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_input = frame.repeat(1, 1, clip_length, 1, 1)
        dit_input = frame.repeat(1, 1, clip_length, 1, 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dldm_input = last_frame
        dldm_input = last_frame
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：decoder_outputs = []
        decoder_outputs = []
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_outputs = []
        dit_outputs = []
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for ci in range(clip_num):
        for ci in range(clip_num):
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# dLDM Decoder
            # dLDM Decoder
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant_codes = self.ldm_net.network.quantizer.indices_to_codes(latent_dynamic_codes[ci].view(1...
            quant_codes = self.ldm_net.network.quantizer.indices_to_codes(latent_dynamic_codes[ci].view(1, len(latent_dynamic_codes[ci]), 1, 1).to('cuda'))
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：encoded_video, _ = self.ldm_net.network.encoder(dldm_input)
            encoded_video, _ = self.ldm_net.network.encoder(dldm_input)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：decoder_output = self.ldm_net.network.decode(encoded_video, quant_codes)
            decoder_output = self.ldm_net.network.decode(encoded_video, quant_codes) 

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dldm_input = decoder_output[:, :, -1:]
            dldm_input = decoder_output[:, :, -1:]
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：decoder_outputs.append(decoder_output[:, :, :-1])
            decoder_outputs.append(decoder_output[:, :, :-1])
            
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：recon_image = torch.nn.functional.interpolate(decoder_output[0].permute(1, 0, 2, 3), size=(fr...
            recon_image = torch.nn.functional.interpolate(decoder_output[0].permute(1, 0, 2, 3), size=(frame.shape[-2], frame.shape[-1]), mode='bilinear', align_corners=False).permute(1, 0, 2, 3)[None]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：recon_image = (((recon_image[0] * 0.5) + 0.5).clamp(0, 1))
            recon_image = (((recon_image[0] * 0.5) + 0.5).clamp(0, 1))
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：recon_image = recon_image * 255
            recon_image = recon_image * 255

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：#For Visualization
            #For Visualization
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# visualization = recon_image.permute(1, 2, 3, 0).detach().cpu().float().numpy().astype(np.ui...
            # visualization =  recon_image.permute(1, 2, 3, 0).detach().cpu().float().numpy().astype(np.uint8)
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# imageio.mimsave('recon_image.mp4', visualization, fps=30)
            # imageio.mimsave('recon_image.mp4', visualization, fps=30)

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gray_video = self.gray_transform(recon_image)
            gray_video = self.gray_transform(recon_image)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gray_video = (gray_video.to(torch.bfloat16) / 127.5) - 1
            gray_video = (gray_video.to(torch.bfloat16) / 127.5) - 1


            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant = self.ldm_net.network.post_quant_conv(quant_codes)
            quant = self.ldm_net.network.post_quant_conv(quant_codes)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant = self.ldm_net.network.quant_to_dit_dim(quant).flatten(2)
            quant = self.ldm_net.network.quant_to_dit_dim(quant).flatten(2)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant = quant.permute(0, 2, 1)
            quant = quant.permute(0, 2, 1)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：crossattn_embed = torch.cat([quant, torch.zeros((1, 512 - quant.shape[1], 1024)).to(quant)], ...
            crossattn_embed = torch.cat([quant, torch.zeros((1, 512 - quant.shape[1], 1024)).to(quant)], dim=1)
        
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = self.pipe.validation(
            video = self.pipe.validation(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video=dit_input,
                video=dit_input,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prompt_embedding=crossattn_embed,
                prompt_embedding=crossattn_embed,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_conditional_frames=1,
                num_conditional_frames=1,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：guidance=7.0,
                guidance=7.0,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：seed=0,
                seed=0,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_cuda_graphs=False,
                use_cuda_graphs=False,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：actions=None,
                actions=None,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hint=gray_video,
                hint=gray_video,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hint_key='recon_image',
                hint_key='recon_image',
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：initial_noise=None,
                initial_noise=None,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
    
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_input = video[:, :, -1:].repeat(1, 1, video.shape[2], 1, 1)
            dit_input = video[:, :, -1:].repeat(1, 1, video.shape[2], 1, 1)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dit_outputs.append(video[:, :, :-1])
            dit_outputs.append(video[:, :, :-1])
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：save_image_or_video(video, f"infer_output/dit_output_clip_{ci}.mp4", fps=16)
            save_image_or_video(video, f"infer_output/dit_output_clip_{ci}.mp4", fps=16)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_video = torch.cat(dit_outputs, dim=2)
        output_video = torch.cat(dit_outputs, dim=2)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：save_image_or_video(output_video, "infer_output/dit_output_clip.mp4", fps=16)
        save_image_or_video(output_video, "infer_output/dit_output_clip.mp4", fps=16)

        