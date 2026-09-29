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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import IO, Any, Union
from typing import IO, Any, Union

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from einops import rearrange
from einops import rearrange
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from PIL import Image as PILImage
from PIL import Image as PILImage
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch import Tensor
from torch import Tensor

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io import easy_io
from imaginaire.utils.easy_io import easy_io


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def save_image_or_video(
def save_image_or_video(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：tensor: Tensor, save_path: Union[str, IO[Any]], fps: int = 24, quality=None, ffmpeg_params=None
    tensor: Tensor, save_path: Union[str, IO[Any]], fps: int = 24, quality=None, ffmpeg_params=None
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
) -> None:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Save a tensor as an image or video file based on shape

    Args:
        tensor (Tensor): Input tensor with shape (B, C, T, H, W) or (C, T, H, W) in [-1, 1] or [0, 1] range.
            If in [-1, 1] range, it will be automatically converted to [0, 1] range.
        save_path (Union[str, IO[Any]]): File path (with or without extension) or file-like object.
        fps (int): Frames per second for video. Default is 24.
        quality: Optional quality parameter for images (passed to easy_io).
        ffmpeg_params: Optional ffmpeg parameters for videos (passed to easy_io).
    """
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Handle batch dimension if present
    # Handle batch dimension if present
    # 中文说明：根据条件选择执行分支；代码：if tensor.ndim == 5:
    if tensor.ndim == 5:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tensor = tensor[0] # Take the first item from the batch
        tensor = tensor[0]  # Take the first item from the batch

    # 中文说明：检查运行时假设是否成立；代码：assert tensor.ndim == 4, "Tensor must have shape (C, T, H, W) or (B, C, T, H, W)"
    assert tensor.ndim == 4, "Tensor must have shape (C, T, H, W) or (B, C, T, H, W)"
    # 中文说明：检查运行时假设是否成立；代码：assert isinstance(save_path, str) or hasattr(save_path, "write"), "save_path must be a string...
    assert isinstance(save_path, str) or hasattr(save_path, "write"), "save_path must be a string or file-like object"

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Normalize to [0, 1] range
    # Normalize to [0, 1] range
    # 中文说明：根据条件选择执行分支；代码：if torch.is_floating_point(tensor):
    if torch.is_floating_point(tensor):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Check if tensor is in [-1, 1] range (approximately)
        # Check if tensor is in [-1, 1] range (approximately)
        # 中文说明：根据条件选择执行分支；代码：if tensor.min() < -0.5:
        if tensor.min() < -0.5:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Convert from [-1, 1] to [0, 1]
            # Convert from [-1, 1] to [0, 1]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tensor = (tensor + 1.0) / 2.0
            tensor = (tensor + 1.0) / 2.0
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tensor = tensor.clamp(0, 1)
        tensor = tensor.clamp(0, 1)
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：检查运行时假设是否成立；代码：assert tensor.dtype == torch.uint8, "Only support uint8 tensor"
        assert tensor.dtype == torch.uint8, "Only support uint8 tensor"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tensor = tensor.float().div(255)
        tensor = tensor.float().div(255)

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs = {}
    kwargs = {}
    # 中文说明：根据条件选择执行分支；代码：if quality is not None:
    if quality is not None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["quality"] = quality
        kwargs["quality"] = quality
    # 中文说明：根据条件选择执行分支；代码：if ffmpeg_params is not None:
    if ffmpeg_params is not None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["ffmpeg_params"] = ffmpeg_params
        kwargs["ffmpeg_params"] = ffmpeg_params

    # 中文说明：根据条件选择执行分支；代码：if tensor.shape[1] == 1:
    if tensor.shape[1] == 1:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：save_obj = PILImage.fromarray(
        save_obj = PILImage.fromarray(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：(rearrange((tensor.cpu().float().numpy() * 255), "c 1 h w -> h w c") + 0.5).astype(np.uint8),
            (rearrange((tensor.cpu().float().numpy() * 255), "c 1 h w -> h w c") + 0.5).astype(np.uint8),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mode="RGB",
            mode="RGB",
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：根据条件选择执行分支；代码：if isinstance(save_path, str):
        if isinstance(save_path, str):
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Check if path already has an extension
            # Check if path already has an extension
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：base, ext = os.path.splitext(save_path)
            base, ext = os.path.splitext(save_path)
            # 中文说明：根据条件选择执行分支；代码：if not ext:
            if not ext:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：save_path = f"{base}.jpg"
                save_path = f"{base}.jpg"
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：easy_io.dump(save_obj, save_path, file_format="jpg", format="JPEG", quality=85, **kwargs)
        easy_io.dump(save_obj, save_path, file_format="jpg", format="JPEG", quality=85, **kwargs)
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：save_obj = (rearrange((tensor.cpu().float().numpy() * 255), "c t h w -> t h w c") + 0.5).asty...
        save_obj = (rearrange((tensor.cpu().float().numpy() * 255), "c t h w -> t h w c") + 0.5).astype(np.uint8)
        # 中文说明：根据条件选择执行分支；代码：if isinstance(save_path, str):
        if isinstance(save_path, str):
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Check if path already has an extension
            # Check if path already has an extension
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：base, ext = os.path.splitext(save_path)
            base, ext = os.path.splitext(save_path)
            # 中文说明：根据条件选择执行分支；代码：if not ext:
            if not ext:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：save_path = f"{base}.mp4"
                save_path = f"{base}.mp4"
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：easy_io.dump(save_obj, save_path, file_format="mp4", format="mp4", fps=fps, **kwargs)
        easy_io.dump(save_obj, save_path, file_format="mp4", format="mp4", fps=fps, **kwargs)
