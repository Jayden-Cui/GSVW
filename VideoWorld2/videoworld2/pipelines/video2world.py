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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any, Callable, Dict, List, Tuple, Union
from typing import Any, Callable, Dict, List, Tuple, Union

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torchvision
import torchvision
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from einops import rearrange
from einops import rearrange
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from megatron.core import parallel_state
from megatron.core import parallel_state
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from tqdm import tqdm
from tqdm import tqdm
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from PIL import Image
from PIL import Image
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed.device_mesh import DeviceMesh
from torch.distributed.device_mesh import DeviceMesh
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed.fsdp import fully_shard
from torch.distributed.fsdp import fully_shard


# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.auxiliary.text_encoder import CosmosT5TextEncoder
from videoworld2.auxiliary.text_encoder import CosmosT5TextEncoder
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.conditioner import DataType, T2VCondition
from videoworld2.conditioner import DataType, T2VCondition
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.configs.base.config_video2world import ConditioningStrategy, Video2WorldPipe...
from videoworld2.configs.base.config_video2world import ConditioningStrategy, Video2WorldPipelineConfig, Video2WorldWithCtrlPipelineConfig
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.datasets.utils import VIDEO_RES_SIZE_INFO
from videoworld2.datasets.utils import VIDEO_RES_SIZE_INFO
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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.utils.context_parallel import broadcast, broadcast_split_tensor, cat_outputs...
from videoworld2.utils.context_parallel import broadcast, broadcast_split_tensor, cat_outputs_cp, split_inputs_cp
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.utils.dtensor_helper import DTensorFastEmaModelUpdater, broadcast_dtensor_mo...
from videoworld2.utils.dtensor_helper import DTensorFastEmaModelUpdater, broadcast_dtensor_model_states
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import instantiate
from imaginaire.lazy_config import instantiate
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log, misc
from imaginaire.utils import log, misc
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io import easy_io
from imaginaire.utils.easy_io import easy_io
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.ema import FastEmaModelUpdater
from imaginaire.utils.ema import FastEmaModelUpdater
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import pickle
import pickle
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：IS_PREPROCESSED_KEY = "is_preprocessed"
IS_PREPROCESSED_KEY = "is_preprocessed"
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg", "webp"]
_IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg", "webp"]
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_VIDEO_EXTENSIONS = [".mp4"]
_VIDEO_EXTENSIONS = [".mp4"]
# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：NUM_CONDITIONAL_FRAMES_KEY: str = "num_conditional_frames"
NUM_CONDITIONAL_FRAMES_KEY: str = "num_conditional_frames"


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def resize_input(video: torch.Tensor, resolution: list[int]) -> torch.Tensor:
def resize_input(video: torch.Tensor, resolution: list[int]) -> torch.Tensor:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""
    r"""
    Resizes and crops the input video tensor while preserving aspect ratio.

    The video is first resized so that the smaller dimension matches the target resolution,
    preserving the aspect ratio. Then, it's center-cropped to the target resolution.

    Args:
        video (torch.Tensor): Input video tensor of shape (T, C, H, W).
        resolution (list[int]): Target resolution [H, W].

    Returns:
        torch.Tensor: Resized and cropped video tensor of shape (T, C, target_H, target_W).
    """

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：orig_h, orig_w = video.shape[2], video.shape[3]
    orig_h, orig_w = video.shape[2], video.shape[3]
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：target_h, target_w = resolution
    target_h, target_w = resolution

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scaling_ratio = max((target_w / orig_w), (target_h / orig_h))
    scaling_ratio = max((target_w / orig_w), (target_h / orig_h))
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resizing_shape = (int(math.ceil(scaling_ratio * orig_h)), int(math.ceil(scaling_ratio * orig_...
    resizing_shape = (int(math.ceil(scaling_ratio * orig_h)), int(math.ceil(scaling_ratio * orig_w)))
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_resized = torchvision.transforms.functional.resize(video, resizing_shape)
    video_resized = torchvision.transforms.functional.resize(video, resizing_shape)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_cropped = torchvision.transforms.functional.center_crop(video_resized, resolution)
    video_cropped = torchvision.transforms.functional.center_crop(video_resized, resolution)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return video_cropped
    return video_cropped


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def read_and_process_image(
def read_and_process_image(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：img_path: str, resolution: list[int], num_video_frames: int, resize: bool = True
    img_path: str, resolution: list[int], num_video_frames: int, resize: bool = True
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor:
) -> torch.Tensor:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Reads an image, converts it to a video tensor, and processes it for model input.

    The image is loaded, converted to a tensor, and replicated to match the
    `num_video_frames`. It's then optionally resized and permuted to the
    standard video format (B, C, T, H, W).

    Args:
        img_path (str): Path to the input image file.
        resolution (list[int]): Target resolution [H, W] for resizing.
        num_video_frames (int): The number of frames the output video tensor should have.
        resize (bool, optional): Whether to resize the image to the target resolution. Defaults to True.

    Returns:
        torch.Tensor: Processed video tensor of shape (1, C, T, H, W).

    Raises:
        ValueError: If the image extension is not one of the supported types.
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ext = os.path.splitext(img_path)[1]
    ext = os.path.splitext(img_path)[1]
    # 中文说明：根据条件选择执行分支；代码：if ext not in _IMAGE_EXTENSIONS:
    if ext not in _IMAGE_EXTENSIONS:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Invalid image extension: {ext}")
        raise ValueError(f"Invalid image extension: {ext}")

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Read the image and convert to tensor
    # Read the image and convert to tensor
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：img = Image.open(img_path)
    img = Image.open(img_path)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：img = torchvision.transforms.functional.to_tensor(img)
    img = torchvision.transforms.functional.to_tensor(img)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Resize the single image first if needed (more efficient than resizing full tensor later)
    # Resize the single image first if needed (more efficient than resizing full tensor later)
    # 中文说明：根据条件选择执行分支；代码：if resize:
    if resize:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：orig_h, orig_w = img.shape[1], img.shape[2]
        orig_h, orig_w = img.shape[1], img.shape[2]
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：target_h, target_w = resolution
        target_h, target_w = resolution

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Calculate scaling based on aspect ratio
        # Calculate scaling based on aspect ratio
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scaling_ratio = max((target_w / orig_w), (target_h / orig_h))
        scaling_ratio = max((target_w / orig_w), (target_h / orig_h))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resizing_shape = (int(math.ceil(scaling_ratio * orig_h)), int(math.ceil(scaling_ratio * orig_...
        resizing_shape = (int(math.ceil(scaling_ratio * orig_h)), int(math.ceil(scaling_ratio * orig_w)))

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Resize and crop the single image
        # Resize and crop the single image
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：img_resized = torchvision.transforms.functional.resize(img.unsqueeze(0), resizing_shape).sque...
        img_resized = torchvision.transforms.functional.resize(img.unsqueeze(0), resizing_shape).squeeze(0)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：img = torchvision.transforms.functional.center_crop(img_resized, resolution)
        img = torchvision.transforms.functional.center_crop(img_resized, resolution)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Get final dimensions
    # Get final dimensions
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：C, H, W = img.shape
    C, H, W = img.shape

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Pre-allocate tensor with target dimensions and directly in uint8 format
    # Pre-allocate tensor with target dimensions and directly in uint8 format
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# This avoids allocating a large float tensor that would be converted later
    # This avoids allocating a large float tensor that would be converted later
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：vid_input = torch.zeros((num_video_frames, C, H, W), dtype=torch.uint8, device=img.device)
    vid_input = torch.zeros((num_video_frames, C, H, W), dtype=torch.uint8, device=img.device)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Set first frame and convert to uint8 (only the first frame needs conversion)
    # Set first frame and convert to uint8 (only the first frame needs conversion)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：vid_input[0] = (img * 255.0).to(torch.uint8)
    vid_input[0] = (img * 255.0).to(torch.uint8)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Add batch dimension and permute in one step
    # Add batch dimension and permute in one step
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# [T, C, H, W] -> [1, C, T, H, W]
    # [T, C, H, W] -> [1, C, T, H, W]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：vid_input = vid_input.unsqueeze(0).permute(0, 2, 1, 3, 4)
    vid_input = vid_input.unsqueeze(0).permute(0, 2, 1, 3, 4)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return vid_input
    return vid_input


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def read_and_process_video(
def read_and_process_video(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video_path: str,
    video_path: str,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：resolution: list[int],
    resolution: list[int],
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_video_frames: int,
    num_video_frames: int,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_latent_conditional_frames: int = 2,
    num_latent_conditional_frames: int = 2,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：resize: bool = True,
    resize: bool = True,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Reads a video, processes it for model input.

    The video is loaded using easy_io, and uses the last 4x(num_latent_conditional_frames - 1) + 1 from the video.
    If the video is shorter than num_video_frames, it pads with the last frame repeated.
    The first num_latent_conditional_frames are marked as conditioning frames.

    Args:
        video_path (str): Path to the input video file.
        resolution (list[int]): Target resolution [H, W] for resizing.
        num_video_frames (int): Number of frames needed by the model (should equal model.tokenizer.get_pixel_num_frames(model.config.state_t)).
        num_latent_conditional_frames (int): Number of latent conditional frames from the input video (1 or 2).
        resize (bool, optional): Whether to resize the video to the target resolution. Defaults to True.

    Returns:
        torch.Tensor: Processed video tensor of shape (1, C, T, H, W) where T equals num_video_frames.

    Raises:
        ValueError: If the video extension is not supported or other validation errors.

    Note:
        Uses the last 4x(num_latent_conditional_frames - 1) + 1 frames from the video. If video is shorter, pads with last frame repeated.
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ext = os.path.splitext(video_path)[1]
    ext = os.path.splitext(video_path)[1]
    # 中文说明：根据条件选择执行分支；代码：if ext.lower() not in _VIDEO_EXTENSIONS:
    if ext.lower() not in _VIDEO_EXTENSIONS:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Invalid video extension: {ext}")
        raise ValueError(f"Invalid video extension: {ext}")

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Load video using easy_io
    # Load video using easy_io
    # 中文说明：开始一个可捕获异常的代码块；代码：try:
    try:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video_frames, video_metadata = easy_io.load(video_path) # Returns (T, H, W, C) numpy array
        video_frames, video_metadata = easy_io.load(video_path)  # Returns (T, H, W, C) numpy array
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Loaded video with shape {video_frames.shape}, metadata: {video_metadata}")
        log.info(f"Loaded video with shape {video_frames.shape}, metadata: {video_metadata}")
    # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
    except Exception as e:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Failed to load video {video_path}: {e}")
        raise ValueError(f"Failed to load video {video_path}: {e}")

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Convert numpy array to tensor and rearrange dimensions
    # Convert numpy array to tensor and rearrange dimensions
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_tensor = torch.from_numpy(video_frames).float() / 255.0 # Convert to [0, 1] range
    video_tensor = torch.from_numpy(video_frames).float() / 255.0  # Convert to [0, 1] range
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_tensor = video_tensor.permute(3, 0, 1, 2) # (T, H, W, C) -> (C, T, H, W)
    video_tensor = video_tensor.permute(3, 0, 1, 2)  # (T, H, W, C) -> (C, T, H, W)

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：available_frames = video_tensor.shape[1]
    available_frames = video_tensor.shape[1]

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Calculate how many frames to extract from input video
    # Calculate how many frames to extract from input video
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames_to_extract = 4 * (num_latent_conditional_frames - 1) + 1
    frames_to_extract = 4 * (num_latent_conditional_frames - 1) + 1
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Will extract the last {frames_to_extract} frames from input video and pad to {num_...
    log.info(f"Will extract the last {frames_to_extract} frames from input video and pad to {num_video_frames}")

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Validate num_latent_conditional_frames
    # Validate num_latent_conditional_frames
    # 中文说明：根据条件选择执行分支；代码：if num_latent_conditional_frames not in [1, 2]:
    if num_latent_conditional_frames not in [1, 2]:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"num_latent_conditional_frames must be 1 or 2, but got {num_latent_conditio...
        raise ValueError(f"num_latent_conditional_frames must be 1 or 2, but got {num_latent_conditional_frames}")

    # 中文说明：根据条件选择执行分支；代码：if available_frames < frames_to_extract:
    if available_frames < frames_to_extract:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(
        raise ValueError(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Video has only {available_frames} frames but needs at least {frames_to_extract} frames for ...
            f"Video has only {available_frames} frames but needs at least {frames_to_extract} frames for num_latent_conditional_frames={num_latent_conditional_frames}"
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Extract the last frames_to_extract from input video
    # Extract the last frames_to_extract from input video
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：start_idx = available_frames - frames_to_extract
    start_idx = available_frames - frames_to_extract
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
    # import pdb;pdb.set_trace()
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# extracted_frames = video_tensor[:, start_idx:, :, :] # (C, frames_to_extract, H, W)
    # extracted_frames = video_tensor[:, start_idx:, :, :]  # (C, frames_to_extract, H, W)

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extracted_frames = video_tensor[:, :1, :, :] # (C, frames_to_extract, H, W)
    extracted_frames = video_tensor[:, :1, :, :]  # (C, frames_to_extract, H, W)
    

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Convert to (frames_to_extract, C, H, W) for resize
    # Convert to (frames_to_extract, C, H, W) for resize
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extracted_frames = extracted_frames.permute(1, 0, 2, 3) # (frames_to_extract, C, H, W)
    extracted_frames = extracted_frames.permute(1, 0, 2, 3)  # (frames_to_extract, C, H, W)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Get last frame for padding
    # Get last frame for padding
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：last_frame = extracted_frames[-1] # (C, H, W)
    last_frame = extracted_frames[-1]  # (C, H, W)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Resize the extracted frames if needed (more efficient than resizing full tensor later)
    # Resize the extracted frames if needed (more efficient than resizing full tensor later)
    # 中文说明：根据条件选择执行分支；代码：if resize:
    if resize:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：C, H, W = extracted_frames.shape[1], extracted_frames.shape[2], extracted_frames.shape[3]
        C, H, W = extracted_frames.shape[1], extracted_frames.shape[2], extracted_frames.shape[3]
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：target_h, target_w = resolution
        target_h, target_w = resolution

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Calculate scaling based on aspect ratio
        # Calculate scaling based on aspect ratio
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scaling_ratio = max((target_w / W), (target_h / H))
        scaling_ratio = max((target_w / W), (target_h / H))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resizing_shape = (int(math.ceil(scaling_ratio * H)), int(math.ceil(scaling_ratio * W)))
        resizing_shape = (int(math.ceil(scaling_ratio * H)), int(math.ceil(scaling_ratio * W)))

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Resize and crop the extracted frames
        # Resize and crop the extracted frames
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extracted_frames = torchvision.transforms.functional.resize(extracted_frames, resizing_shape)
        extracted_frames = torchvision.transforms.functional.resize(extracted_frames, resizing_shape)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extracted_frames = torchvision.transforms.functional.center_crop(extracted_frames, resolution)
        extracted_frames = torchvision.transforms.functional.center_crop(extracted_frames, resolution)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Resize and crop the last frame separately (for padding)
        # Resize and crop the last frame separately (for padding)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：last_frame = last_frame.unsqueeze(0) # Add batch dim for resize
        last_frame = last_frame.unsqueeze(0)  # Add batch dim for resize
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：last_frame = torchvision.transforms.functional.resize(last_frame, resizing_shape)
        last_frame = torchvision.transforms.functional.resize(last_frame, resizing_shape)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：last_frame = torchvision.transforms.functional.center_crop(last_frame, resolution)
        last_frame = torchvision.transforms.functional.center_crop(last_frame, resolution)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：last_frame = last_frame.squeeze(0) # Remove batch dim
        last_frame = last_frame.squeeze(0)  # Remove batch dim

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Get final dimensions
    # Get final dimensions
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：C, H, W = extracted_frames.shape[1], extracted_frames.shape[2], extracted_frames.shape[3]
    C, H, W = extracted_frames.shape[1], extracted_frames.shape[2], extracted_frames.shape[3]

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Pre-allocate tensor with target dimensions and directly in uint8 format
    # Pre-allocate tensor with target dimensions and directly in uint8 format
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# This avoids allocating a large float tensor that would be converted later
    # This avoids allocating a large float tensor that would be converted later
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：full_video = torch.zeros((num_video_frames, C, H, W), dtype=torch.uint8, device=extracted_fra...
    full_video = torch.zeros((num_video_frames, C, H, W), dtype=torch.uint8, device=extracted_frames.device)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Set extracted frames and convert to uint8
    # Set extracted frames and convert to uint8
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：full_video[:frames_to_extract] = (extracted_frames * 255.0).to(torch.uint8)
    full_video[:frames_to_extract] = (extracted_frames * 255.0).to(torch.uint8)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Pad remaining frames with the last frame (already resized if needed)
    # Pad remaining frames with the last frame (already resized if needed)
    # 中文说明：根据条件选择执行分支；代码：if frames_to_extract < num_video_frames:
    if frames_to_extract < num_video_frames:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：last_frame_uint8 = (last_frame * 255.0).to(torch.uint8)
        last_frame_uint8 = (last_frame * 255.0).to(torch.uint8)
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i in range(num_video_frames - frames_to_extract):
        for i in range(num_video_frames - frames_to_extract):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：full_video[frames_to_extract + i] = last_frame_uint8
            full_video[frames_to_extract + i] = last_frame_uint8

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Add batch dimension and permute in one operation to final format
    # Add batch dimension and permute in one operation to final format
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# [T, C, H, W] -> [1, C, T, H, W]
    # [T, C, H, W] -> [1, C, T, H, W]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：full_video = full_video.unsqueeze(0).permute(0, 2, 1, 3, 4)
    full_video = full_video.unsqueeze(0).permute(0, 2, 1, 3, 4)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return full_video
    return full_video


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Video2WorldPipeline(BasePipeline):
class Video2WorldPipeline(BasePipeline):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, device: str = "cuda", torch_dtype: torch.dtype = torch.bfloat16):
    def __init__(self, device: str = "cuda", torch_dtype: torch.dtype = torch.bfloat16):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(device=device, torch_dtype=torch_dtype)
        super().__init__(device=device, torch_dtype=torch_dtype)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.text_encoder: CosmosT5TextEncoder = None
        self.text_encoder: CosmosT5TextEncoder = None
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.dit: torch.nn.Module = None
        self.dit: torch.nn.Module = None
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.dit_ema: torch.nn.Module = None
        self.dit_ema: torch.nn.Module = None
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.tokenizer: TokenizerInterface = None
        self.tokenizer: TokenizerInterface = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conditioner = None
        self.conditioner = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.prompt_refiner = None
        self.prompt_refiner = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.text_guardrail_runner = None
        self.text_guardrail_runner = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.video_guardrail_runner = None
        self.video_guardrail_runner = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.model_names = ["text_encoder", "dit", "tokenizer"]
        self.model_names = ["text_encoder", "dit", "tokenizer"]
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
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe = Video2WorldPipeline(device=device, torch_dtype=torch_dtype)
        pipe = Video2WorldPipeline(device=device, torch_dtype=torch_dtype)
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

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# if load_prompt_refiner:
        # if load_prompt_refiner:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# pipe.prompt_refiner = CosmosReason1(
        #     pipe.prompt_refiner = CosmosReason1(
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# checkpoint_dir=config.prompt_refiner_config.checkpoint_dir,
        #         checkpoint_dir=config.prompt_refiner_config.checkpoint_dir,
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# offload_model_to_cpu=config.prompt_refiner_config.offload_model_to_cpu,
        #         offload_model_to_cpu=config.prompt_refiner_config.offload_model_to_cpu,
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# enabled=config.prompt_refiner_config.enabled,
        #         enabled=config.prompt_refiner_config.enabled,
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# )
        #     )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# if config.guardrail_config.enabled:
        # if config.guardrail_config.enabled:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# from videoworld2.auxiliary.guardrail.common import presets as guardrail_presets
        #     from videoworld2.auxiliary.guardrail.common import presets as guardrail_presets

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# pipe.text_guardrail_runner = guardrail_presets.create_text_guardrail_runner(
        #     pipe.text_guardrail_runner = guardrail_presets.create_text_guardrail_runner(
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# config.guardrail_config.checkpoint_dir, config.guardrail_config.offload_model_to_cpu
        #         config.guardrail_config.checkpoint_dir, config.guardrail_config.offload_model_to_cpu
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# )
        #     )
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# pipe.video_guardrail_runner = guardrail_presets.create_video_guardrail_runner(
        #     pipe.video_guardrail_runner = guardrail_presets.create_video_guardrail_runner(
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# config.guardrail_config.checkpoint_dir, config.guardrail_config.offload_model_to_cpu
        #         config.guardrail_config.checkpoint_dir, config.guardrail_config.offload_model_to_cpu
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# )
        #     )
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# else:
        # else:
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
        # 中文说明：处理异常、清理资源或管理上下文；代码：with init_weights_on_device():
        with init_weights_on_device():
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
            # 中文说明：根据条件选择执行分支；代码：if 'ldm_net' in k:
            if 'ldm_net' in k:
                # 中文说明：执行循环控制或空操作；代码：continue
                continue
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

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# for n, p in pipe.dit.named_parameters():
        # for n, p in pipe.dit.named_parameters():
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# print(n, p.device)
        #     print(n, p.device)
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

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def setup_data_key(self) -> None:
    def setup_data_key(self) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.input_data_key = self.config.input_data_key # by default it is video key for Video diffu...
        self.input_data_key = self.config.input_data_key  # by default it is video key for Video diffusion model
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.input_image_key = self.config.input_image_key
        self.input_image_key = self.config.input_image_key

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def apply_fsdp(self, dp_mesh: DeviceMesh) -> None:
    def apply_fsdp(self, dp_mesh: DeviceMesh) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.dit.fully_shard(mesh=dp_mesh)
        self.dit.fully_shard(mesh=dp_mesh)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dit = fully_shard(self.dit, mesh=dp_mesh, reshard_after_forward=True)
        self.dit = fully_shard(self.dit, mesh=dp_mesh, reshard_after_forward=True)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：broadcast_dtensor_model_states(self.dit, dp_mesh)
        broadcast_dtensor_model_states(self.dit, dp_mesh)
        # 中文说明：根据条件选择执行分支；代码：if self.dit_ema:
        if self.dit_ema:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.dit_ema.fully_shard(mesh=dp_mesh)
            self.dit_ema.fully_shard(mesh=dp_mesh)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dit_ema = fully_shard(self.dit_ema, mesh=dp_mesh, reshard_after_forward=True)
            self.dit_ema = fully_shard(self.dit_ema, mesh=dp_mesh, reshard_after_forward=True)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：broadcast_dtensor_model_states(self.dit_ema, dp_mesh)
            broadcast_dtensor_model_states(self.dit_ema, dp_mesh)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dit_ema_worker = DTensorFastEmaModelUpdater()
            self.dit_ema_worker = DTensorFastEmaModelUpdater()
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# No need to copy weights to EMA when applying FSDP, it is already copied before applying FSDP.
            # No need to copy weights to EMA when applying FSDP, it is already copied before applying FSDP.

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def apply_cp(self) -> None:
    def apply_cp(self) -> None:
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _get_data_batch_input(
    def _get_data_batch_input(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, video: torch.Tensor, prompt: str, negative_prompt: str = "", num_latent_conditional_fra...
        self, video: torch.Tensor, prompt: str, negative_prompt: str = "", num_latent_conditional_frames: int = 1
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
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："t5_text_embeddings": self.encode_prompt(prompt).to(dtype=self.torch_dtype),
            "t5_text_embeddings": self.encode_prompt(prompt).to(dtype=self.torch_dtype),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："fps": torch.randint(16, 32, (self.batch_size,)), # Random FPS (might be used by model)
            "fps": torch.randint(16, 32, (self.batch_size,)),  # Random FPS (might be used by model)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："padding_mask": torch.zeros(self.batch_size, 1, H, W), # Padding mask (assumed no padding here)
            "padding_mask": torch.zeros(self.batch_size, 1, H, W),  # Padding mask (assumed no padding here)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："num_conditional_frames": num_latent_conditional_frames, # Specify number of conditional frames
            "num_conditional_frames": num_latent_conditional_frames,  # Specify number of conditional frames
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

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def denoising_model(self) -> torch.nn.Module:
    def denoising_model(self) -> torch.nn.Module:
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

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _normalize_video_databatch_inplace(self, data_batch: dict[str, torch.Tensor]) -> None:
    def _normalize_video_databatch_inplace(self, data_batch: dict[str, torch.Tensor]) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Normalizes video data in-place on a CUDA device to reduce data loading overhead.

        This function modifies the video data tensor within the provided data_batch dictionary
        in-place, scaling the uint8 data from the range [0, 255] to the normalized range [-1, 1].

        Warning:
            A warning is issued if the data has not been previously normalized.

        Args:
            data_batch (dict[str, Tensor]): A dictionary containing the video data under a specific key.
                This tensor is expected to be on a CUDA device and have dtype of torch.uint8.

        Side Effects:
            Modifies the 'input_data_key' tensor within the 'data_batch' dictionary in-place.

        Note:
            This operation is performed directly on the CUDA device to avoid the overhead associated
            with moving data to/from the GPU. Ensure that the tensor is already on the appropriate device
            and has the correct dtype (torch.uint8) to avoid unexpected behaviors.
        """
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# input_key = self.input_data_key if input_key is None else input_key
        # input_key = self.input_data_key if input_key is None else input_key
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_keys = ['video', 'video_aug_0', 'video_aug_1', 'control_input_depth', 'extra_video']
        input_keys = ['video', 'video_aug_0', 'video_aug_1', 'control_input_depth', 'extra_video'] 
        # 中文说明：根据条件选择执行分支；代码：if data_batch.get('use_ctrl', False):
        if data_batch.get('use_ctrl', False):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：input_keys.append(self.config.hint_key)
            input_keys.append(self.config.hint_key)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_keys = list(set(input_keys))
        input_keys = list(set(input_keys))
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# only handle video batch
        # only handle video batch
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for input_key in input_keys:
        for input_key in input_keys:
            # 中文说明：根据条件选择执行分支；代码：if input_key in data_batch:
            if input_key in data_batch:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Check if the data has already been normalized and avoid re-normalizing
                # Check if the data has already been normalized and avoid re-normalizing
                # 中文说明：根据条件选择执行分支；代码：if IS_PREPROCESSED_KEY in data_batch and data_batch[IS_PREPROCESSED_KEY] is True:
                if IS_PREPROCESSED_KEY in data_batch and data_batch[IS_PREPROCESSED_KEY] is True:
                    # 中文说明：检查运行时假设是否成立；代码：assert torch.is_floating_point(data_batch[input_key]), "Video data is not in float format."
                    assert torch.is_floating_point(data_batch[input_key]), "Video data is not in float format."
                    # 中文说明：检查运行时假设是否成立；代码：assert torch.all(
                    assert torch.all(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：(data_batch[input_key] >= -1.0001) & (data_batch[input_key] <= 1.0001)
                        (data_batch[input_key] >= -1.0001) & (data_batch[input_key] <= 1.0001)
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"Video data is not in the range [-1, 1]. get data range [{data_batch[input_key].min()}, {...
                    ), f"Video data is not in the range [-1, 1]. get data range [{data_batch[input_key].min()}, {data_batch[input_key].max()}]"
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：检查运行时假设是否成立；代码：assert data_batch[input_key].dtype == torch.uint8, "Video data is not in uint8 format."
                    assert data_batch[input_key].dtype == torch.uint8, "Video data is not in uint8 format."
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch[input_key] = data_batch[input_key].to(**self.tensor_kwargs) / 127.5 - 1.0
                    data_batch[input_key] = data_batch[input_key].to(**self.tensor_kwargs) / 127.5 - 1.0

                # 中文说明：根据条件选择执行分支；代码：if self.config.resize_online:
                if self.config.resize_online:
                    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torchvision.transforms.v2 import UniformTemporalSubsample
                    from torchvision.transforms.v2 import UniformTemporalSubsample

                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：expected_length = self.tokenizer.get_pixel_num_frames(self.config.state_t)
                    expected_length = self.tokenizer.get_pixel_num_frames(self.config.state_t)
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：original_length = data_batch[input_key].shape[2]
                    original_length = data_batch[input_key].shape[2]
                    # 中文说明：根据条件选择执行分支；代码：if original_length != expected_length:
                    if original_length != expected_length:
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = rearrange(data_batch[input_key], "b c t h w -> b t c h w")
                        video = rearrange(data_batch[input_key], "b c t h w -> b t c h w")
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = UniformTemporalSubsample(expected_length)(video)
                        video = UniformTemporalSubsample(expected_length)(video)
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch[input_key] = rearrange(video, "b t c h w -> b c t h w")
                        data_batch[input_key] = rearrange(video, "b t c h w -> b c t h w")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch[IS_PREPROCESSED_KEY] = True
        data_batch[IS_PREPROCESSED_KEY] = True

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _augment_image_dim_inplace(self, data_batch: dict[str, torch.Tensor], input_key: str = No...
    def _augment_image_dim_inplace(self, data_batch: dict[str, torch.Tensor], input_key: str = None) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_key = self.input_image_key if input_key is None else input_key
        input_key = self.input_image_key if input_key is None else input_key
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
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
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
        Currently, we only support context parallelism.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cp_group = self.get_context_parallel_group()
        cp_group = self.get_context_parallel_group()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cp_size = 1 if cp_group is None else cp_group.size()
        cp_size = 1 if cp_group is None else cp_group.size()
        # 中文说明：根据条件选择执行分支；代码：if condition.is_video and cp_size > 1:
        if condition.is_video and cp_size > 1:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x0_B_C_T_H_W = broadcast_split_tensor(x0_B_C_T_H_W, seq_dim=2, process_group=cp_group)
            x0_B_C_T_H_W = broadcast_split_tensor(x0_B_C_T_H_W, seq_dim=2, process_group=cp_group)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：epsilon_B_C_T_H_W = broadcast_split_tensor(epsilon_B_C_T_H_W, seq_dim=2, process_group=cp_group)
            epsilon_B_C_T_H_W = broadcast_split_tensor(epsilon_B_C_T_H_W, seq_dim=2, process_group=cp_group)
            # 中文说明：根据条件选择执行分支；代码：if sigma_B_T is not None:
            if sigma_B_T is not None:
                # 中文说明：检查运行时假设是否成立；代码：assert sigma_B_T.ndim == 2, "sigma_B_T should be 2D tensor"
                assert sigma_B_T.ndim == 2, "sigma_B_T should be 2D tensor"
                # 中文说明：根据条件选择执行分支；代码：if sigma_B_T.shape[-1] == 1: # single sigma is shared across all frames
                if sigma_B_T.shape[-1] == 1:  # single sigma is shared across all frames
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_B_T = broadcast(sigma_B_T, cp_group)
                    sigma_B_T = broadcast(sigma_B_T, cp_group)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：else: # different sigma for each frame
                else:  # different sigma for each frame
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_B_T = broadcast_split_tensor(sigma_B_T, seq_dim=1, process_group=cp_group)
                    sigma_B_T = broadcast_split_tensor(sigma_B_T, seq_dim=1, process_group=cp_group)
            # 中文说明：根据条件选择执行分支；代码：if condition is not None:
            if condition is not None:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：condition = condition.broadcast(cp_group)
                condition = condition.broadcast(cp_group)
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.dit.enable_context_parallel(cp_group)
            self.dit.enable_context_parallel(cp_group)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
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
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self._normalize_video_databatch_inplace(data_batch) # Remove to training_step
        # self._normalize_video_databatch_inplace(data_batch) # Remove to training_step 
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._augment_image_dim_inplace(data_batch)
        self._augment_image_dim_inplace(data_batch)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_image_batch = self.is_image_batch(data_batch)
        is_image_batch = self.is_image_batch(data_batch)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Latent state
        # Latent state
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：raw_state = data_batch[self.input_image_key if is_image_batch else self.input_data_key]
        raw_state = data_batch[self.input_image_key if is_image_batch else self.input_data_key]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：latent_state = self.encode(raw_state).contiguous().float()
        latent_state = self.encode(raw_state).contiguous().float()

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Condition
        # Condition
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：condition = self.conditioner(data_batch)
        condition = self.conditioner(data_batch)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：condition = condition.edit_data_type(DataType.IMAGE if is_image_batch else DataType.VIDEO)
        condition = condition.edit_data_type(DataType.IMAGE if is_image_batch else DataType.VIDEO)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extra_condition = {}
        extra_condition = {}
        # 中文说明：根据条件选择执行分支；代码：if data_batch.get('use_ctrl', False):
        if data_batch.get('use_ctrl', False):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch["hint_key"] = self.config.hint_key
            data_batch["hint_key"] = self.config.hint_key
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：latent_hint = self.encode(data_batch[self.config.hint_key]) if self.config.hint_key != 'decod...
            latent_hint = self.encode(data_batch[self.config.hint_key]) if self.config.hint_key != 'decoder_feature' else data_batch[self.config.hint_key]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extra_condition[self.config.hint_key] = latent_hint
            extra_condition[self.config.hint_key] = latent_hint
            
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：condition = condition.set_video_condition(
        condition = condition.set_video_condition(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gt_frames=latent_state.to(**self.tensor_kwargs),
            gt_frames=latent_state.to(**self.tensor_kwargs),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：random_min_num_conditional_frames=self.config.min_num_conditional_frames,
            random_min_num_conditional_frames=self.config.min_num_conditional_frames,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：random_max_num_conditional_frames=self.config.max_num_conditional_frames,
            random_max_num_conditional_frames=self.config.max_num_conditional_frames,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_conditional_frames=data_batch.get(NUM_CONDITIONAL_FRAMES_KEY, None),
            num_conditional_frames=data_batch.get(NUM_CONDITIONAL_FRAMES_KEY, None),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**extra_condition,
            **extra_condition,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# print(condition.condition_video_input_mask_B_C_T_H_W[0][0][0].sum(), condition.condition_vi...
        # print(condition.condition_video_input_mask_B_C_T_H_W[0][0][0].sum(), condition.condition_video_input_mask_B_C_T_H_W[0][0][1].sum(), condition.condition_video_input_mask_B_C_T_H_W[0][0][2].sum())
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return raw_state, latent_state, condition
        return raw_state, latent_state, condition

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

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def blend_noise(self, noise_background, noise_foreground, alpha):
    def blend_noise(self, noise_background, noise_foreground, alpha):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return (noise_foreground * alpha + noise_background * (1-alpha))/(alpha ** 2 + (1-alpha) ** 2...
        return (noise_foreground * alpha + noise_background * (1-alpha))/(alpha ** 2 + (1-alpha) ** 2)**.5
    
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def visualize_noise(self, noise):
    def visualize_noise(self, noise):
        # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import imageio
        import imageio
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：noise = noise[0, :3]/5 + 0.5
        noise = noise[0, :3]/5 + 0.5
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：noise = noise.clamp(0, 1)
        noise = noise.clamp(0, 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：noise = noise.permute(1, 2, 3, 0)
        noise = noise.permute(1, 2, 3, 0)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：noise = (noise * 255).to(torch.uint8).cpu().numpy()
        noise = (noise * 255).to(torch.uint8).cpu().numpy() 
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：imageio.mimsave("/opt/tiger/noise.mp4", noise, fps=30 )
        imageio.mimsave("/opt/tiger/noise.mp4", noise, fps=30 )

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
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
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

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net_state_in_B_C_T_H_W = xt_B_C_T_H_W * c_in_B_1_T_1_1
        net_state_in_B_C_T_H_W = xt_B_C_T_H_W * c_in_B_1_T_1_1
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# if step_idx == 0 and initial_noise is not None:
        # if step_idx == 0 and initial_noise is not None:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# net_state_in_B_C_T_H_W = self.blend_noise(initial_noise, net_state_in_B_C_T_H_W, 0.3)
        #     net_state_in_B_C_T_H_W = self.blend_noise(initial_noise, net_state_in_B_C_T_H_W, 0.3)
        # 中文说明：根据条件选择执行分支；代码：if condition.is_video:
        if condition.is_video:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：condition_state_in_B_C_T_H_W = condition.gt_frames.type_as(net_state_in_B_C_T_H_W) / self.con...
            condition_state_in_B_C_T_H_W = condition.gt_frames.type_as(net_state_in_B_C_T_H_W) / self.config.sigma_data
            # 中文说明：根据条件选择执行分支；代码：if not condition.use_video_condition:
            if not condition.use_video_condition:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# When using random dropout, we zero out the ground truth frames
                # When using random dropout, we zero out the ground truth frames
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：condition_state_in_B_C_T_H_W = condition_state_in_B_C_T_H_W * 0
                condition_state_in_B_C_T_H_W = condition_state_in_B_C_T_H_W * 0

            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_, C, _, _, _ = xt_B_C_T_H_W.shape
            _, C, _, _, _ = xt_B_C_T_H_W.shape
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：condition_video_mask = condition.condition_video_input_mask_B_C_T_H_W.repeat(1, C, 1, 1, 1).t...
            condition_video_mask = condition.condition_video_input_mask_B_C_T_H_W.repeat(1, C, 1, 1, 1).type_as(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：net_state_in_B_C_T_H_W
                net_state_in_B_C_T_H_W
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

            # 中文说明：根据条件选择执行分支；代码：if self.config.conditioning_strategy == str(ConditioningStrategy.FRAME_REPLACE):
            if self.config.conditioning_strategy == str(ConditioningStrategy.FRAME_REPLACE):
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# In case of frame replacement strategy, replace the first few frames of the video with the c...
                # In case of frame replacement strategy, replace the first few frames of the video with the conditional frames
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Update the c_noise as the conditional frames are clean and have very low noise
                # Update the c_noise as the conditional frames are clean and have very low noise

                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Make the first few frames of x_t be the ground truth frames
                # Make the first few frames of x_t be the ground truth frames
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net_state_in_B_C_T_H_W = (
                net_state_in_B_C_T_H_W = (
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：condition_state_in_B_C_T_H_W * condition_video_mask
                    condition_state_in_B_C_T_H_W * condition_video_mask
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：+ net_state_in_B_C_T_H_W * (1 - condition_video_mask)
                    + net_state_in_B_C_T_H_W * (1 - condition_video_mask)
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )

                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Adjust c_noise for the conditional frames
                # Adjust c_noise for the conditional frames
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_cond_B_1_T_1_1 = torch.ones_like(sigma_B_1_T_1_1) * self.config.sigma_conditional
                sigma_cond_B_1_T_1_1 = torch.ones_like(sigma_B_1_T_1_1) * self.config.sigma_conditional
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_, _, _, c_noise_cond_B_1_T_1_1 = self.scaling(sigma=sigma_cond_B_1_T_1_1)
                _, _, _, c_noise_cond_B_1_T_1_1 = self.scaling(sigma=sigma_cond_B_1_T_1_1)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：condition_video_mask_B_1_T_1_1 = condition_video_mask.mean(dim=[1, 3, 4], keepdim=True)
                condition_video_mask_B_1_T_1_1 = condition_video_mask.mean(dim=[1, 3, 4], keepdim=True)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：c_noise_B_1_T_1_1 = c_noise_cond_B_1_T_1_1 * condition_video_mask_B_1_T_1_1 + c_noise_B_1_T_1...
                c_noise_B_1_T_1_1 = c_noise_cond_B_1_T_1_1 * condition_video_mask_B_1_T_1_1 + c_noise_B_1_T_1_1 * (
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：1 - condition_video_mask_B_1_T_1_1
                    1 - condition_video_mask_B_1_T_1_1
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
            # 中文说明：根据条件选择执行分支；代码：elif self.config.conditioning_strategy == str(ConditioningStrategy.CHANNEL_CONCAT):
            elif self.config.conditioning_strategy == str(ConditioningStrategy.CHANNEL_CONCAT):
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# In case of channel concatenation strategy, concatenate the conditional frames in the channe...
                # In case of channel concatenation strategy, concatenate the conditional frames in the channel dimension
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：condition_state_in_masked_B_C_T_H_W = condition_state_in_B_C_T_H_W * condition_video_mask
                condition_state_in_masked_B_C_T_H_W = condition_state_in_B_C_T_H_W * condition_video_mask
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net_state_in_B_C_T_H_W = torch.cat([net_state_in_B_C_T_H_W, condition_state_in_masked_B_C_T_H...
                net_state_in_B_C_T_H_W = torch.cat([net_state_in_B_C_T_H_W, condition_state_in_masked_B_C_T_H_W], dim=1)

        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# In case of image batch, simply concatenate the 0 frames when channel concat strategy is used
            # In case of image batch, simply concatenate the 0 frames when channel concat strategy is used
            # 中文说明：根据条件选择执行分支；代码：if self.config.conditioning_strategy == str(ConditioningStrategy.CHANNEL_CONCAT):
            if self.config.conditioning_strategy == str(ConditioningStrategy.CHANNEL_CONCAT):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net_state_in_B_C_T_H_W = torch.cat(
                net_state_in_B_C_T_H_W = torch.cat(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：[net_state_in_B_C_T_H_W, torch.zeros_like(net_state_in_B_C_T_H_W)], dim=1
                    [net_state_in_B_C_T_H_W, torch.zeros_like(net_state_in_B_C_T_H_W)], dim=1
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# forward pass through the network
        # forward pass through the network
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net_output_B_C_T_H_W = self.dit(
        net_output_B_C_T_H_W = self.dit(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_C_T_H_W=net_state_in_B_C_T_H_W.to(**self.tensor_kwargs),
            x_B_C_T_H_W=net_state_in_B_C_T_H_W.to(**self.tensor_kwargs),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：timesteps_B_T=c_noise_B_1_T_1_1.squeeze(dim=[1, 3, 4]).to(**self.tensor_kwargs),
            timesteps_B_T=c_noise_B_1_T_1_1.squeeze(dim=[1, 3, 4]).to(**self.tensor_kwargs),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**condition.to_dict(),
            **condition.to_dict(),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_cuda_graphs=use_cuda_graphs,
            use_cuda_graphs=use_cuda_graphs,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：).float()
        ).float()

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x0_pred_B_C_T_H_W = c_skip_B_1_T_1_1 * xt_B_C_T_H_W + c_out_B_1_T_1_1 * net_output_B_C_T_H_W
        x0_pred_B_C_T_H_W = c_skip_B_1_T_1_1 * xt_B_C_T_H_W + c_out_B_1_T_1_1 * net_output_B_C_T_H_W
        # 中文说明：根据条件选择执行分支；代码：if condition.is_video:
        if condition.is_video:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Set the first few frames to the ground truth frames. This will ensure that the loss is not ...
            # Set the first few frames to the ground truth frames. This will ensure that the loss is not computed for the first few frames.
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x0_pred_B_C_T_H_W = condition.gt_frames.type_as(
            x0_pred_B_C_T_H_W = condition.gt_frames.type_as(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x0_pred_B_C_T_H_W
                x0_pred_B_C_T_H_W
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) * condition_video_mask + x0_pred_B_C_T_H_W * (1 - condition_video_mask)
            ) * condition_video_mask + x0_pred_B_C_T_H_W * (1 - condition_video_mask)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# get noise prediction
        # get noise prediction
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：eps_pred_B_C_T_H_W = (xt_B_C_T_H_W - x0_pred_B_C_T_H_W) / sigma_B_1_T_1_1
        eps_pred_B_C_T_H_W = (xt_B_C_T_H_W - x0_pred_B_C_T_H_W) / sigma_B_1_T_1_1

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return DenoisePrediction(x0_pred_B_C_T_H_W, eps_pred_B_C_T_H_W, None)
        return DenoisePrediction(x0_pred_B_C_T_H_W, eps_pred_B_C_T_H_W, None)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_x0_fn_from_batch(
    def get_x0_fn_from_batch(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_batch: Dict,
        data_batch: Dict,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：guidance: float = 1.5,
        guidance: float = 1.5,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：is_negative_prompt: bool = False,
        is_negative_prompt: bool = False,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：use_cuda_graphs: bool = False,
        use_cuda_graphs: bool = False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Callable:
    ) -> Callable:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Generates a callable function `x0_fn` based on the provided data batch and guidance factor.

        This function first processes the input data batch through a conditioning workflow (`conditioner`) to obtain conditioned and unconditioned states. It then defines a nested function `x0_fn` which applies a denoising operation on an input `noise_x` at a given noise level `sigma` using both the conditioned and unconditioned states.

        Args:
        - data_batch (Dict): A batch of data used for conditioning. The format and content of this dictionary should align with the expectations of the `self.conditioner`
        - guidance (float, optional): A scalar value that modulates the influence of the conditioned state relative to the unconditioned state in the output. Defaults to 1.5.
        - is_negative_prompt (bool): use negative prompt t5 in uncondition if true

        Returns:
        - Callable: A function `x0_fn(noise_x, sigma)` that takes two arguments, `noise_x` and `sigma`, and return x0 predictoin

        The returned function is suitable for use in scenarios where a denoised state is required based on both conditioned and unconditioned inputs, with an adjustable level of guidance influence.
        """
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：根据条件选择执行分支；代码：if NUM_CONDITIONAL_FRAMES_KEY in data_batch:
        if NUM_CONDITIONAL_FRAMES_KEY in data_batch:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_conditional_frames = data_batch[NUM_CONDITIONAL_FRAMES_KEY]
            num_conditional_frames = data_batch[NUM_CONDITIONAL_FRAMES_KEY]
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_conditional_frames = 1
            num_conditional_frames = 1

        # 中文说明：根据条件选择执行分支；代码：if is_negative_prompt:
        if is_negative_prompt:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：condition, uncondition = self.conditioner.get_condition_with_negative_prompt(data_batch)
            condition, uncondition = self.conditioner.get_condition_with_negative_prompt(data_batch)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：condition, uncondition = self.conditioner.get_condition_uncondition(data_batch)
            condition, uncondition = self.conditioner.get_condition_uncondition(data_batch)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_image_batch = self.is_image_batch(data_batch)
        is_image_batch = self.is_image_batch(data_batch)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：condition = condition.edit_data_type(DataType.IMAGE if is_image_batch else DataType.VIDEO)
        condition = condition.edit_data_type(DataType.IMAGE if is_image_batch else DataType.VIDEO)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：uncondition = uncondition.edit_data_type(DataType.IMAGE if is_image_batch else DataType.VIDEO)
        uncondition = uncondition.edit_data_type(DataType.IMAGE if is_image_batch else DataType.VIDEO)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_, x0, _ = self.get_data_and_condition(data_batch)
        _, x0, _ = self.get_data_and_condition(data_batch)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# override condition with inference mode; num_conditional_frames used Here!
        # override condition with inference mode; num_conditional_frames used Here!
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extra_condition = {}
        extra_condition = {}
        # 中文说明：根据条件选择执行分支；代码：if data_batch.get('hint_key', None) is not None:
        if data_batch.get('hint_key', None) is not None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hint_key = data_batch['hint_key']
            hint_key = data_batch['hint_key']
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：latent_hint = self.encode(data_batch[hint_key]) if hint_key!= 'decoder_feature' else data_bat...
            latent_hint = self.encode(data_batch[hint_key]) if hint_key!= 'decoder_feature' else data_batch[hint_key]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extra_condition[hint_key] = latent_hint
            extra_condition[hint_key] = latent_hint

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：condition = condition.set_video_condition(
        condition = condition.set_video_condition(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gt_frames=x0,
            gt_frames=x0,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：random_min_num_conditional_frames=self.config.min_num_conditional_frames,
            random_min_num_conditional_frames=self.config.min_num_conditional_frames,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：random_max_num_conditional_frames=self.config.max_num_conditional_frames,
            random_max_num_conditional_frames=self.config.max_num_conditional_frames,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_conditional_frames=num_conditional_frames,
            num_conditional_frames=num_conditional_frames,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**extra_condition
            **extra_condition
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：uncondition = uncondition.set_video_condition(
        uncondition = uncondition.set_video_condition(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gt_frames=x0,
            gt_frames=x0,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：random_min_num_conditional_frames=self.config.min_num_conditional_frames,
            random_min_num_conditional_frames=self.config.min_num_conditional_frames,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：random_max_num_conditional_frames=self.config.max_num_conditional_frames,
            random_max_num_conditional_frames=self.config.max_num_conditional_frames,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_conditional_frames=num_conditional_frames,
            num_conditional_frames=num_conditional_frames,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**extra_condition
            **extra_condition
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：condition = condition.edit_for_inference(is_cfg_conditional=True, num_conditional_frames=num_...
        condition = condition.edit_for_inference(is_cfg_conditional=True, num_conditional_frames=num_conditional_frames)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：uncondition = uncondition.edit_for_inference(
        uncondition = uncondition.edit_for_inference(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_cfg_conditional=False, num_conditional_frames=num_conditional_frames
            is_cfg_conditional=False, num_conditional_frames=num_conditional_frames
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_, condition, _, _ = self.broadcast_split_for_model_parallelsim(x0, condition, None, None)
        _, condition, _, _ = self.broadcast_split_for_model_parallelsim(x0, condition, None, None)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_, uncondition, _, _ = self.broadcast_split_for_model_parallelsim(x0, uncondition, None, None)
        _, uncondition, _, _ = self.broadcast_split_for_model_parallelsim(x0, uncondition, None, None)

        # 中文说明：根据条件选择执行分支；代码：if not parallel_state.is_initialized():
        if not parallel_state.is_initialized():
            # 中文说明：检查运行时假设是否成立；代码：assert (
            assert (
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：not self.dit.is_context_parallel_enabled
                not self.dit.is_context_parallel_enabled
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), "parallel_state is not initialized, context parallel should be turned off."
            ), "parallel_state is not initialized, context parallel should be turned off."

        # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def x0_fn(noise_x: torch.Tensor, sigma: torch.Tensor) -> torch.Tensor:
        def x0_fn(noise_x: torch.Tensor, sigma: torch.Tensor) -> torch.Tensor:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cond_x0 = self.denoise(noise_x, sigma, condition, use_cuda_graphs=use_cuda_graphs).x0
            cond_x0 = self.denoise(noise_x, sigma, condition, use_cuda_graphs=use_cuda_graphs).x0
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：uncond_x0 = self.denoise(noise_x, sigma, uncondition, use_cuda_graphs=use_cuda_graphs).x0
            uncond_x0 = self.denoise(noise_x, sigma, uncondition, use_cuda_graphs=use_cuda_graphs).x0
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：raw_x0 = cond_x0 + guidance * (cond_x0 - uncond_x0)
            raw_x0 = cond_x0 + guidance * (cond_x0 - uncond_x0)
            # 中文说明：根据条件选择执行分支；代码：if "guided_image" in data_batch:
            if "guided_image" in data_batch:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# replacement trick that enables inpainting with base model
                # replacement trick that enables inpainting with base model
                # 中文说明：检查运行时假设是否成立；代码：assert "guided_mask" in data_batch, "guided_mask should be in data_batch if guided_image is p...
                assert "guided_mask" in data_batch, "guided_mask should be in data_batch if guided_image is present"
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：guide_image = data_batch["guided_image"]
                guide_image = data_batch["guided_image"]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：guide_mask = data_batch["guided_mask"]
                guide_mask = data_batch["guided_mask"]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：raw_x0 = guide_mask * guide_image + (1 - guide_mask) * raw_x0
                raw_x0 = guide_mask * guide_image + (1 - guide_mask) * raw_x0
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return raw_x0
            return raw_x0

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x0_fn
        return x0_fn

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.no_grad()
    @torch.no_grad()
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(
    def __call__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：input_path: str,
        input_path: str,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：prompt: str,
        prompt: str,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：negative_prompt: str = "",
        negative_prompt: str = "",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：aspect_ratio: str = "16:9",
        aspect_ratio: str = "16:9",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_conditional_frames: int = 1,
        num_conditional_frames: int = 1,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：guidance: float = 7.0,
        guidance: float = 7.0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_sampling_step: int = 35,
        num_sampling_step: int = 35,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：seed: int = 0,
        seed: int = 0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：use_cuda_graphs: bool = False,
        use_cuda_graphs: bool = False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor | None:
    ) -> torch.Tensor | None:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Parameter check
        # Parameter check
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：width, height = VIDEO_RES_SIZE_INFO[self.config.resolution][aspect_ratio]
        width, height = VIDEO_RES_SIZE_INFO[self.config.resolution][aspect_ratio]
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：height, width = self.check_resize_height_width(height, width)
        height, width = self.check_resize_height_width(height, width)
        # 中文说明：检查运行时假设是否成立；代码：assert num_conditional_frames in [1, 5], "num_conditional_frames must be 1 or 5"
        assert num_conditional_frames in [1, 5], "num_conditional_frames must be 1 or 5"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_latent_conditional_frames = self.tokenizer.get_latent_num_frames(num_conditional_frames)
        num_latent_conditional_frames = self.tokenizer.get_latent_num_frames(num_conditional_frames)

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
        # 中文说明：根据条件选择执行分支；代码：elif self.text_guardrail_runner is None:
        elif self.text_guardrail_runner is None:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning("Guardrail checks on prompt are disabled")
            log.warning("Guardrail checks on prompt are disabled")

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# refine prompt only if prompt refiner is enabled
        # refine prompt only if prompt refiner is enabled
        # 中文说明：根据条件选择执行分支；代码：if (
        if (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：hasattr(self, "prompt_refiner")
            hasattr(self, "prompt_refiner")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：and self.prompt_refiner is not None
            and self.prompt_refiner is not None
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：and getattr(self.config, "prompt_refiner_config", None)
            and getattr(self.config, "prompt_refiner_config", None)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：and getattr(self.config.prompt_refiner_config, "enabled", False)
            and getattr(self.config.prompt_refiner_config, "enabled", False)
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
        ):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("Starting prompt refinement...")
            log.info("Starting prompt refinement...")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prompt = self.prompt_refiner.refine_prompt(input_path, prompt)
            prompt = self.prompt_refiner.refine_prompt(input_path, prompt)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("Finished prompt refinement")
            log.info("Finished prompt refinement")

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Run text guardrail on the refined prompt
            # Run text guardrail on the refined prompt
            # 中文说明：根据条件选择执行分支；代码：if self.text_guardrail_runner is not None:
            if self.text_guardrail_runner is not None:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("Running guardrail check on refined prompt...")
                log.info("Running guardrail check on refined prompt...")
                # 中文说明：根据条件选择执行分支；代码：if not guardrail_presets.run_text_guardrail(prompt, self.text_guardrail_runner):
                if not guardrail_presets.run_text_guardrail(prompt, self.text_guardrail_runner):
                    # 中文说明：从当前函数返回结果或结束函数执行；代码：return None
                    return None
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.success("Passed guardrail on refined prompt")
                    log.success("Passed guardrail on refined prompt")
            # 中文说明：根据条件选择执行分支；代码：elif self.text_guardrail_runner is None:
            elif self.text_guardrail_runner is None:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning("Guardrail checks on refined prompt are disabled")
                log.warning("Guardrail checks on refined prompt are disabled")
        # 中文说明：根据条件选择执行分支；代码：elif (
        elif (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：hasattr(self, "config")
            hasattr(self, "config")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：and hasattr(self.config, "prompt_refiner_config")
            and hasattr(self.config, "prompt_refiner_config")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：and not self.config.prompt_refiner_config.enabled
            and not self.config.prompt_refiner_config.enabled
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
        ):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning("Prompt refinement is disabled")
            log.warning("Prompt refinement is disabled")

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_video_frames = self.tokenizer.get_pixel_num_frames(self.config.state_t)
        num_video_frames = self.tokenizer.get_pixel_num_frames(self.config.state_t)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Detect file extension to determine appropriate reading function
        # Detect file extension to determine appropriate reading function
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ext = os.path.splitext(input_path)[1].lower()
        ext = os.path.splitext(input_path)[1].lower()
        # 中文说明：根据条件选择执行分支；代码：if ext in _VIDEO_EXTENSIONS:
        if ext in _VIDEO_EXTENSIONS:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Always use video reading for video files, regardless of num_latent_conditional_frames
            # Always use video reading for video files, regardless of num_latent_conditional_frames
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：vid_input = read_and_process_video(
            vid_input = read_and_process_video(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：input_path, [height, width], num_video_frames, num_latent_conditional_frames, resize=True
                input_path, [height, width], num_video_frames, num_latent_conditional_frames, resize=True
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：根据条件选择执行分支；代码：elif ext in _IMAGE_EXTENSIONS:
        elif ext in _IMAGE_EXTENSIONS:
            # 中文说明：根据条件选择执行分支；代码：if num_latent_conditional_frames == 1:
            if num_latent_conditional_frames == 1:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Use image reading for single frame conditioning with image files
                # Use image reading for single frame conditioning with image files
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：vid_input = read_and_process_image(input_path, [height, width], num_video_frames, resize=True)
                vid_input = read_and_process_image(input_path, [height, width], num_video_frames, resize=True)
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(
                raise ValueError(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Cannot use multi-frame conditioning (num_conditional_frames={num_conditional_frames}) with ...
                    f"Cannot use multi-frame conditioning (num_conditional_frames={num_conditional_frames}) with image input. Please provide a video file."
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(
            raise ValueError(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Unsupported file extension: {ext}. Supported extensions are {_IMAGE_EXTENSIONS + _VIDEO_EXT...
                f"Unsupported file extension: {ext}. Supported extensions are {_IMAGE_EXTENSIONS + _VIDEO_EXTENSIONS}"
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Prepare the data batch with text embeddings
        # Prepare the data batch with text embeddings
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch = self._get_data_batch_input(
        data_batch = self._get_data_batch_input(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：vid_input, prompt, negative_prompt, num_latent_conditional_frames=num_latent_conditional_frames
            vid_input, prompt, negative_prompt, num_latent_conditional_frames=num_latent_conditional_frames
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

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x0_fn = self.get_x0_fn_from_batch(
        x0_fn = self.get_x0_fn_from_batch(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_batch, guidance, is_negative_prompt=True, use_cuda_graphs=use_cuda_graphs
            data_batch, guidance, is_negative_prompt=True, use_cuda_graphs=use_cuda_graphs
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

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

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i, _ in enumerate(tqdm(scheduler.timesteps, desc="Generating world", leave=False)):
        for i, _ in enumerate(tqdm(scheduler.timesteps, desc="Generating world", leave=False)):
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
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video,
        video,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：prompt_embedding,
        prompt_embedding,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_conditional_frames: int = 1,
        num_conditional_frames: int = 1,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：guidance: float = 7.0,
        guidance: float = 7.0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_sampling_step: int = 35,
        num_sampling_step: int = 35,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：seed: int = 0,
        seed: int = 0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：use_cuda_graphs: bool = False,
        use_cuda_graphs: bool = False,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：actions=None,
        actions=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hint=None,
        hint=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hint_key=None,
        hint_key=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：initial_noise=None,
        initial_noise=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：initial_noise_level=0.3
        initial_noise_level=0.3
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor | None:
    ) -> torch.Tensor | None:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Parameter check
        # Parameter check
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# width, height = VIDEO_RES_SIZE_INFO[self.config.resolution][aspect_ratio]
        # width, height = VIDEO_RES_SIZE_INFO[self.config.resolution][aspect_ratio]
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# height, width = self.check_resize_height_width(height, width)
        # height, width = self.check_resize_height_width(height, width)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# _DEFAULT_NEGATIVE_PROMPT = "The video captures a series of frames showing ugly scenes, stat...
        # _DEFAULT_NEGATIVE_PROMPT = "The video captures a series of frames showing ugly scenes, static with no motion, motion blur, over-saturation, shaky footage, low resolution, grainy texture, pixelated images, poorly lit areas, underexposed and overexposed scenes, poor color balance, washed out colors, choppy sequences, jerky movements, low frame rate, artifacting, color banding, unnatural transitions, outdated special effects, fake elements, unconvincing visuals, poorly edited content, jump cuts, visual noise, and flickering. Overall, the video is of poor quality."
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：处理异常、清理资源或管理上下文；代码：with open("checkpoints/VideoWorld2_dLDM_2B/default_neg.pickle", "rb") as fp:
        with open("checkpoints/VideoWorld2_dLDM_2B/default_neg.pickle", "rb") as fp:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：neg_t5_text_embeddings = pickle.load(fp)
            neg_t5_text_embeddings = pickle.load(fp)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：neg_t5_text_embeddings = torch.from_numpy(neg_t5_text_embeddings[0])[None].to(dtype=self.torc...
        neg_t5_text_embeddings = torch.from_numpy(neg_t5_text_embeddings[0])[None].to(dtype=self.torch_dtype)
        # 中文说明：根据条件选择执行分支；代码：if neg_t5_text_embeddings.shape[1] < prompt_embedding.shape[1]:
        if neg_t5_text_embeddings.shape[1] < prompt_embedding.shape[1]:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：neg_t5_text_embeddings = torch.cat([neg_t5_text_embeddings.to(prompt_embedding), torch.zeros(...
            neg_t5_text_embeddings = torch.cat([neg_t5_text_embeddings.to(prompt_embedding), torch.zeros(1, prompt_embedding.shape[1]-neg_t5_text_embeddings.shape[1], prompt_embedding.shape[2]).to(prompt_embedding)], dim=1)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# width, height = VIDEO_RES_SIZE_INFO[self.config.resolution]["16:9"]
        # width, height = VIDEO_RES_SIZE_INFO[self.config.resolution]["16:9"]
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# height, width = self.check_resize_height_width(height, width)
        # height, width = self.check_resize_height_width(height, width)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# video = torch.nn.functional.interpolate(video[0].permute(1, 0, 2, 3), (height, width)).perm...
        # video = torch.nn.functional.interpolate(video[0].permute(1, 0, 2, 3), (height, width)).permute(1, 0, 2, 3)[None]
        # 中文说明：检查运行时假设是否成立；代码：assert num_conditional_frames in [1, 5], "num_conditional_frames must be 1 or 5"
        assert num_conditional_frames in [1, 5], "num_conditional_frames must be 1 or 5"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_latent_conditional_frames = self.tokenizer.get_latent_num_frames(num_conditional_frames)
        num_latent_conditional_frames = self.tokenizer.get_latent_num_frames(num_conditional_frames)
        
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：H, W = video.shape[-2:]
        H, W = video.shape[-2:]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch = {
        data_batch = {
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："dataset_name": "video_data",
                "dataset_name": "video_data",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："video": video,
                "video": video,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："t5_text_embeddings": prompt_embedding,
                "t5_text_embeddings": prompt_embedding,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："neg_t5_text_embeddings": neg_t5_text_embeddings,
                "neg_t5_text_embeddings": neg_t5_text_embeddings,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："fps": torch.ones((1,)) * 16, # Random FPS (might be used by model)
                "fps": torch.ones((1,)) * 16,  # Random FPS (might be used by model)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："padding_mask": torch.zeros(1, 1, H, W), # Padding mask (assumed no padding here)
                "padding_mask": torch.zeros(1, 1, H, W),  # Padding mask (assumed no padding here)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："num_conditional_frames": num_latent_conditional_frames, # Specify number of conditional frames
                "num_conditional_frames": num_latent_conditional_frames,  # Specify number of conditional frames
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
            }
        # 中文说明：根据条件选择执行分支；代码：if hint is not None:
        if hint is not None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch[hint_key] = hint
            data_batch[hint_key] = hint
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch['hint_key'] = hint_key
            data_batch['hint_key'] = hint_key

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for k, v in data_batch.items():
        for k, v in data_batch.items():
            # 中文说明：根据条件选择执行分支；代码：if isinstance(v, torch.Tensor) and torch.is_floating_point(data_batch[k]):
            if isinstance(v, torch.Tensor) and torch.is_floating_point(data_batch[k]):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch[k] = v.cuda().to(dtype=torch.bfloat16)
                data_batch[k] = v.cuda().to(dtype=torch.bfloat16)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Prepare the data batch with text embeddings
        # Prepare the data batch with text embeddings
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# data_batch = self._get_data_batch_input(
        # data_batch = self._get_data_batch_input(
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# vid_input, prompt, negative_prompt, num_latent_conditional_frames=num_latent_conditional_fr...
        #     vid_input, prompt, negative_prompt, num_latent_conditional_frames=num_latent_conditional_frames
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# )
        # )
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# preprocess
        # preprocess
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self._normalize_video_databatch_inplace(data_batch) # Move to video2world_model.py
        # self._normalize_video_databatch_inplace(data_batch) # Move to video2world_model.py
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

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x0_fn = self.get_x0_fn_from_batch(
        x0_fn = self.get_x0_fn_from_batch(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_batch, guidance, is_negative_prompt=True, use_cuda_graphs=use_cuda_graphs
            data_batch, guidance, is_negative_prompt=True, use_cuda_graphs=use_cuda_graphs
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

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

        # 中文说明：根据条件选择执行分支；代码：if initial_noise is not None:
        if initial_noise is not None:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：B, C, T, H, W = initial_noise.shape
            B, C, T, H, W = initial_noise.shape
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：N = (T - 1) // (x_sigma_max.shape[2] - 1)
            N = (T - 1) // (x_sigma_max.shape[2] - 1)
            # 中文说明：根据条件选择执行分支；代码：if N > 1:
            if N > 1:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：first_noise_bg, later_noise_bg = initial_noise[:, :, :1], initial_noise[:, :, 1:]
                first_noise_bg, later_noise_bg = initial_noise[:, :, :1], initial_noise[:, :, 1:]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：later_noise_bg = later_noise_bg.reshape(B, C, (T - 1)//N, N, H, W)
                later_noise_bg = later_noise_bg.reshape(B, C, (T - 1)//N, N, H, W)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：later_noise_bg = later_noise_bg[:, :, :, 0, :, :]
                later_noise_bg = later_noise_bg[:, :, :, 0, :, :]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：initial_noise = torch.cat([first_noise_bg, later_noise_bg], dim=2)
                initial_noise = torch.cat([first_noise_bg, later_noise_bg], dim=2)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：initial_noise = initial_noise * self.scheduler.config.sigma_max
            initial_noise = initial_noise * self.scheduler.config.sigma_max
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_sigma_max = self.blend_noise(initial_noise, x_sigma_max, initial_noise_level)
            x_sigma_max = self.blend_noise(initial_noise, x_sigma_max, initial_noise_level)
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# initial_noise = split_inputs_cp(x=initial_noise, seq_dim=2, cp_group=self.get_context_paral...
            # initial_noise = split_inputs_cp(x=initial_noise, seq_dim=2, cp_group=self.get_context_parallel_group())
    
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

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i, _ in enumerate(tqdm(scheduler.timesteps, desc="Generating world", leave=False)):
        for i, _ in enumerate(tqdm(scheduler.timesteps, desc="Generating world", leave=False)):
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
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# x0_pred = x0_fn(sample, sigma_in, initial_noise=initial_noise, step_idx=i)
            # x0_pred = x0_fn(sample, sigma_in, initial_noise=initial_noise, step_idx=i)
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
