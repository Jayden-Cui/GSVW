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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import io
import io
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import re
import re
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from random import randint
from random import randint
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import List, Tuple
from typing import List, Tuple

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import decord
import decord
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from PIL import Image
from PIL import Image

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：Image.MAX_IMAGE_PIXELS = 933120000
Image.MAX_IMAGE_PIXELS = 933120000
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_VIDEO_EXTENSIONS = "mp4 avi webm mov".split()
_VIDEO_EXTENSIONS = "mp4 avi webm mov".split()

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：VIDEO_DECODER_OPTIONS = {}
VIDEO_DECODER_OPTIONS = {}


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def video_decoder_register(key):
def video_decoder_register(key):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def decorator(func):
    def decorator(func):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：VIDEO_DECODER_OPTIONS[key] = func
        VIDEO_DECODER_OPTIONS[key] = func
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return func
        return func

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return decorator
    return decorator


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def basic_check_on_inputs(
def basic_check_on_inputs(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：n_video_frames: int, n_target_frames: int, video_fps: float, min_fps_thres: int, max_fps_thre...
    n_video_frames: int, n_target_frames: int, video_fps: float, min_fps_thres: int, max_fps_thres: int
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> str:
) -> str:
    # 中文说明：根据条件选择执行分支；代码：if n_video_frames <= 0:
    if n_video_frames <= 0:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return "n_video_frames must be positive"
        return "n_video_frames must be positive"
    # 中文说明：根据条件选择执行分支；代码：if min_fps_thres <= 0:
    if min_fps_thres <= 0:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return "min_fps_thres must be positive"
        return "min_fps_thres must be positive"
    # 中文说明：根据条件选择执行分支；代码：if video_fps < 1:
    if video_fps < 1:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return "Video fps lower than 1, skipping"
        return "Video fps lower than 1, skipping"
    # 中文说明：根据条件选择执行分支；代码：if max_fps_thres < min_fps_thres:
    if max_fps_thres < min_fps_thres:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return "max_fps_thres must be greater than or equal to min_fps_thres"
        return "max_fps_thres must be greater than or equal to min_fps_thres"
    # 中文说明：根据条件选择执行分支；代码：if n_target_frames <= 1:
    if n_target_frames <= 1:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return "sequence_length must be greater than 1"
        return "sequence_length must be greater than 1"
    # 中文说明：根据条件选择执行分支；代码：if n_target_frames > n_video_frames:
    if n_target_frames > n_video_frames:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return f"Specified sequence_length {n_target_frames} exceeds num frames in video {n_video_fra...
        return f"Specified sequence_length {n_target_frames} exceeds num frames in video {n_video_frames}."

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return "success"
    return "success"


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def sample_chunk_index_from_chunked_video(
def sample_chunk_index_from_chunked_video(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：n_video_frames: int,
    n_video_frames: int,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：n_target_frames: int,
    n_target_frames: int,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：chunk_size: int,
    chunk_size: int,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[int, int, str]:
) -> Tuple[int, int, str]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Sample a chunk from the chunked videos. Our videos are stored as regular mp4 files but with chunked captions. There is one caption per [chunk_size] frames.
    If the last chunk has frames >= chunk_size / 2, it will be treated as a separate chunk and has its own caption. Otherwise, it will be treated as part of the previous chunk.
    e.g. if chunk_size = 256, possible number of frames in a chunk: [1, 383]

    Args:
      n_video_frames: total number of frames in the video
      n_target_frames: number of requested frames
      chunk_size: number of frames in each chunk. The last chunk will be treated differently

    Returns:
      sampled_chunk_indexs
      n_frames_in_chunk
      message
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_chunks = max(n_video_frames // chunk_size, 1)
    n_chunks = max(n_video_frames // chunk_size, 1)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Check if the last chunk has separate window
    # Check if the last chunk has separate window
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# This happens only if remainder frames >= chunk_size / 2 [data annotation was done this way]
    # This happens only if remainder frames >= chunk_size / 2 [data annotation was done this way]
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Else this is used as a part of previous window.
    # Else this is used as a part of previous window.
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_frames_in_last_chunk = n_video_frames - n_chunks * chunk_size
    n_frames_in_last_chunk = n_video_frames - n_chunks * chunk_size
    # 中文说明：根据条件选择执行分支；代码：if n_frames_in_last_chunk >= int(0.5 * chunk_size):
    if n_frames_in_last_chunk >= int(0.5 * chunk_size):
        # 中文说明：根据条件选择执行分支；代码：if n_frames_in_last_chunk > n_target_frames:
        if n_frames_in_last_chunk > n_target_frames:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_chunks += 1
            n_chunks += 1

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sampled_chunk_index = randint(0, n_chunks - 1)
    sampled_chunk_index = randint(0, n_chunks - 1)
    # 中文说明：根据条件选择执行分支；代码：if sampled_chunk_index == n_chunks - 1:
    if sampled_chunk_index == n_chunks - 1:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# For the last chunk, use all of the remaining frames
        # For the last chunk, use all of the remaining frames
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_frames_in_chunk = n_video_frames - sampled_chunk_index * chunk_size
        n_frames_in_chunk = n_video_frames - sampled_chunk_index * chunk_size
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Else use only the chunk size
        # Else use only the chunk size
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_frames_in_chunk = chunk_size
        n_frames_in_chunk = chunk_size

    # 中文说明：根据条件选择执行分支；代码：if n_target_frames > n_frames_in_chunk:
    if n_target_frames > n_frames_in_chunk:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：error_message = f"Requested sequence_length {n_target_frames} exceeds curr_chunk_size {n_fram...
        error_message = f"Requested sequence_length {n_target_frames} exceeds curr_chunk_size {n_frames_in_chunk}, n_video_frames={n_video_frames}, chunk_size={chunk_size}, sampled_chunk_index={sampled_chunk_index}."
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return -1, 0, error_message
        return -1, 0, error_message

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return sampled_chunk_index, n_frames_in_chunk, "success"
    return sampled_chunk_index, n_frames_in_chunk, "success"


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@video_decoder_register("video_naive_bytes")
@video_decoder_register("video_naive_bytes")
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def video_naive_bytes(*args, **kwargs):
def video_naive_bytes(*args, **kwargs):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    do nothing, just return the video bytes
    """
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del args, kwargs
    del args, kwargs

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def video_decoder(
    def video_decoder(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：key: str,
        key: str,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data: bytes,
        data: bytes,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extension = re.sub(r".*[.]", "", key)
        extension = re.sub(r".*[.]", "", key)
        # 中文说明：根据条件选择执行分支；代码：if extension.lower() not in _VIDEO_EXTENSIONS:
        if extension.lower() not in _VIDEO_EXTENSIONS:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return None
            return None

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return data
        return data

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return video_decoder
    return video_decoder


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@video_decoder_register("chunked_video_decoder")
@video_decoder_register("chunked_video_decoder")
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def chunked_video_decoder(
def chunked_video_decoder(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：chunk_size: int = 0,
    chunk_size: int = 0,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sequence_length: int = 34,
    sequence_length: int = 34,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：min_fps_thres: int = 1,
    min_fps_thres: int = 1,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_fps_thres: int = 9999,
    max_fps_thres: int = 9999,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_threads=4,
    num_threads=4,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Video decoder for videos with chunked captions.
    It first sample a chunk from the video then sample the start frame within the chunk.
    It has a basic check to make sure the video fps falls within the range [min_fps_thres, max_fps_thres]. Otherwise, it will skip the video sample.

    Args:
    - chunk_size (int): How the video is divided into chunks. Only return frames within a chunk. chunk_size=0 means we use full video length. Defaults to 0.
    - sequence_length (int) : Number of frames returned by the function
    - min_fps_thres (int): Minimum fps threshold allowed.
    - max_fps_thres (int): Maximum fps threshold allowed.
    - num_thread (int): Number of threads for decord.

    Returns:
        dict with video frames tensor and additional attributes including
        - fps
        - orig_fps
        - num_frames
        - chunk_index
        - frame_start
        - frame_end
        - n_orig_video_frames
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def video_decoder(
    def video_decoder(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：key: str,
        key: str,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data: bytes,
        data: bytes,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extension = re.sub(r".*[.]", "", key)
        extension = re.sub(r".*[.]", "", key)
        # 中文说明：根据条件选择执行分支；代码：if extension.lower() not in _VIDEO_EXTENSIONS:
        if extension.lower() not in _VIDEO_EXTENSIONS:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return None
            return None

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_buffer = io.BytesIO(data)
        video_buffer = io.BytesIO(data)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_reader = decord.VideoReader(video_buffer, num_threads=num_threads)
        video_reader = decord.VideoReader(video_buffer, num_threads=num_threads)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_target_frames = sequence_length if sequence_length > 0 else len(video_reader)
        n_target_frames = sequence_length if sequence_length > 0 else len(video_reader)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_video_frames = len(video_reader)
        n_video_frames = len(video_reader)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_fps = int(np.round(video_reader.get_avg_fps()))
        video_fps = int(np.round(video_reader.get_avg_fps()))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cur_chunk_size = n_video_frames if chunk_size == 0 else chunk_size
        cur_chunk_size = n_video_frames if chunk_size == 0 else chunk_size

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# basic check
        # basic check
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：message = basic_check_on_inputs(
        message = basic_check_on_inputs(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_video_frames=n_video_frames,
            n_video_frames=n_video_frames,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_target_frames=n_target_frames,
            n_target_frames=n_target_frames,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_fps=video_fps,
            video_fps=video_fps,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_fps_thres=min_fps_thres,
            min_fps_thres=min_fps_thres,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_fps_thres=max_fps_thres,
            max_fps_thres=max_fps_thres,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：根据条件选择执行分支；代码：if message != "success":
        if message != "success":
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(message)
            raise ValueError(message)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# check if video fps is within the specified range
        # check if video fps is within the specified range
        # 中文说明：根据条件选择执行分支；代码：if video_fps < min_fps_thres:
        if video_fps < min_fps_thres:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Video fps {video_fps} lower than {min_fps_thres}, skipping")
            raise ValueError(f"Video fps {video_fps} lower than {min_fps_thres}, skipping")
        # 中文说明：根据条件选择执行分支；代码：if video_fps > max_fps_thres:
        if video_fps > max_fps_thres:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Video fps {video_fps} larger than {max_fps_thres}, skipping")
            raise ValueError(f"Video fps {video_fps} larger than {max_fps_thres}, skipping")

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sampled_chunk_index, n_frames_in_chunk, message = sample_chunk_index_from_chunked_video(
        sampled_chunk_index, n_frames_in_chunk, message = sample_chunk_index_from_chunked_video(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_video_frames=n_video_frames,
            n_video_frames=n_video_frames,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_target_frames=n_target_frames,
            n_target_frames=n_target_frames,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：chunk_size=cur_chunk_size,
            chunk_size=cur_chunk_size,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：根据条件选择执行分支；代码：if sampled_chunk_index == -1:
        if sampled_chunk_index == -1:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(message)
            raise ValueError(message)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：检查运行时假设是否成立；代码：assert message == "success"
            assert message == "success"

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Select the frame start index and frame end index
        # Select the frame start index and frame end index
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：chunk_frame_start = sampled_chunk_index * chunk_size
        chunk_frame_start = sampled_chunk_index * chunk_size
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Start index is randomly selected in the chunk
        # Start index is randomly selected in the chunk
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_start = chunk_frame_start + int(np.random.choice(n_frames_in_chunk - n_target_frames, 1))
        frame_start = chunk_frame_start + int(np.random.choice(n_frames_in_chunk - n_target_frames, 1))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_end = frame_start + n_target_frames
        frame_end = frame_start + n_target_frames

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Subsample the frames
        # Subsample the frames
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_frames = video_reader.get_batch(np.arange(frame_start, frame_end).tolist()).asnumpy()
        video_frames = video_reader.get_batch(np.arange(frame_start, frame_end).tolist()).asnumpy()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_frames = torch.from_numpy(video_frames).permute(3, 0, 1, 2) # (T, H, W, C) -> (C, T, H, W)
        video_frames = torch.from_numpy(video_frames).permute(3, 0, 1, 2)  # (T, H, W, C) -> (C, T, H, W)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Clean up
        # Clean up
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video_reader.seek(0) # set video reader point back to 0 to clean up cache
        video_reader.seek(0)  # set video reader point back to 0 to clean up cache
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del video_reader # delete the reader to avoid memory leak
        del video_reader  # delete the reader to avoid memory leak

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return {
        return {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："video": video_frames,
            "video": video_frames,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："fps": float(video_fps),
            "fps": float(video_fps),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："orig_fps": float(video_fps),
            "orig_fps": float(video_fps),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："num_frames": video_frames.shape[1],
            "num_frames": video_frames.shape[1],
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："chunk_index": sampled_chunk_index,
            "chunk_index": sampled_chunk_index,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："frame_start": frame_start,
            "frame_start": frame_start,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："frame_end": frame_end,
            "frame_end": frame_end,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："n_orig_video_frames": n_video_frames,
            "n_orig_video_frames": n_video_frames,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return video_decoder
    return video_decoder


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_frame_indices_w_lowered_fps(
def get_frame_indices_w_lowered_fps(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：n_video_frames: int,
    n_video_frames: int,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video_fps: int,
    video_fps: int,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：min_fps_thres: int,
    min_fps_thres: int,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_fps_thres: int,
    max_fps_thres: int,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：n_target_frames: int,
    n_target_frames: int,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[List[int], float]:
) -> Tuple[List[int], float]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Generates frame indices for video sampling with FPS control.
    """Generates frame indices for video sampling with FPS control.

    This function determines valid stride lengths for sampling frames from a video,
    preferring lower FPS (larger strides) when multiple options are available.
    It returns both the selected frame indices and the resulting FPS.

    Args:
        n_video_frames: Total number of frames in the original video.
        video_fps: Original video frames per second.
        min_fps_thres: Minimum allowed frames per second.
        max_fps_thres: Maximum allowed frames per second.
        n_target_frames: Number of frames to sample.

    Returns:
        A tuple containing:
            - list[int]: Frame indices to sample from the original video.
            - float: The resulting frames per second after sampling.

    Raises:
        ValueError: If no valid stride options are available given the constraints.
        ValueError: If input parameters are invalid (e.g., negative values).
    """
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Calculate stride range
    # Calculate stride range
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_stride = 1
    min_stride = 1
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_stride = (n_video_frames - 1) // (n_target_frames - 1)
    max_stride = (n_video_frames - 1) // (n_target_frames - 1)

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：valid_strides = []
    valid_strides = []
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for stride in range(min_stride, max_stride + 1):
    for stride in range(min_stride, max_stride + 1):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Check if we can get n_target_frames frames with this stride
        # Check if we can get n_target_frames frames with this stride
        # 中文说明：根据条件选择执行分支；代码：if (n_video_frames - stride * (n_target_frames - 1)) > 0:
        if (n_video_frames - stride * (n_target_frames - 1)) > 0:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：new_fps = video_fps / stride
            new_fps = video_fps / stride
            # 中文说明：根据条件选择执行分支；代码：if min_fps_thres <= new_fps <= max_fps_thres:
            if min_fps_thres <= new_fps <= max_fps_thres:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：valid_strides.append(stride)
                valid_strides.append(stride)

    # 中文说明：根据条件选择执行分支；代码：if not valid_strides:
    if not valid_strides:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(
        raise ValueError(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"No valid stride options available for the given constraints. "
            f"No valid stride options available for the given constraints. "
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"stride range = [{min_stride}, {max_stride}]; "
            f"stride range = [{min_stride}, {max_stride}]; "
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"original FPS = {video_fps}; "
            f"original FPS = {video_fps}; "
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"n_target_frames = {n_target_frames}; "
            f"n_target_frames = {n_target_frames}; "
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"min_fps_thres = {min_fps_thres}; "
            f"min_fps_thres = {min_fps_thres}; "
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"max_fps_thres = {max_fps_thres}; "
            f"max_fps_thres = {max_fps_thres}; "
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"original num_frames = {n_video_frames}"
            f"original num_frames = {n_video_frames}"
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Select stride with weighted probability
    # Select stride with weighted probability
    # 中文说明：根据条件选择执行分支；代码：if len(valid_strides) >= 2:
    if len(valid_strides) >= 2:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：stride_choices = valid_strides[-2:] # Taking last two as they're the largest
        stride_choices = valid_strides[-2:]  # Taking last two as they're the largest
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：weights = [0.01, 0.99] # [smaller_stride, larger_stride]
        weights = [0.01, 0.99]  # [smaller_stride, larger_stride]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：selected_stride = np.random.choice(stride_choices, p=weights)
        selected_stride = np.random.choice(stride_choices, p=weights)
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：selected_stride = valid_strides[0]
        selected_stride = valid_strides[0]

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Calculate the maximum valid start index and random start frame
    # Calculate the maximum valid start index and random start frame
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_start_idx = n_video_frames - (n_target_frames - 1) * selected_stride
    max_start_idx = n_video_frames - (n_target_frames - 1) * selected_stride
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_start = np.random.randint(0, max_start_idx)
    frame_start = np.random.randint(0, max_start_idx)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Generate frame indices
    # Generate frame indices
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_indices = [frame_start + i * selected_stride for i in range(n_target_frames)]
    frame_indices = [frame_start + i * selected_stride for i in range(n_target_frames)]
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return frame_indices, video_fps / selected_stride
    return frame_indices, video_fps / selected_stride


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@video_decoder_register("chunked_video_decoder_w_lower_fps")
@video_decoder_register("chunked_video_decoder_w_lower_fps")
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def chunked_video_decoder_w_lower_fps(
def chunked_video_decoder_w_lower_fps(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：chunk_size: int = 0,
    chunk_size: int = 0,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sequence_length: int = 34,
    sequence_length: int = 34,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：min_fps_thres: int = 4,
    min_fps_thres: int = 4,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_fps_thres: int = 30,
    max_fps_thres: int = 30,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_threads: int = 4,
    num_threads: int = 4,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> dict:
) -> dict:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Video decoder for videos with chunked captions.
    It first sample a chunk from the video then sample the start frame within the chunk.
    It has high probability (>99%) to lower the fps with frame sampling whenever allowed.

    Args:
        - chunk_size (int): How the video is divided into chunks. Only return frames within a chunk. chunk_size=0 means we use full video length. Defaults to 0.
        - sequence_length (int) : Number of frames returned by the function
        - min_fps_thres: Minimum FPS threshold
        - max_fps_thres: Maximum FPS threshold
        - num_threads: Number of threads for decord

    Returns:
        dict with video frames tensor and additional attributes including
        - fps
        - orig_fps
        - num_frames
        - chunk_index
        - frame_start
        - frame_end
        - n_orig_video_frames
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def video_decoder(
    def video_decoder(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：key: str,
        key: str,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data: bytes,
        data: bytes,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> dict[str, torch.Tensor | int]:
    ) -> dict[str, torch.Tensor | int]:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Check video extension
        # Check video extension
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extension = re.sub(r".*[.]", "", key)
        extension = re.sub(r".*[.]", "", key)
        # 中文说明：根据条件选择执行分支；代码：if extension.lower() not in _VIDEO_EXTENSIONS:
        if extension.lower() not in _VIDEO_EXTENSIONS:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return None
            return None

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Read video
        # Read video
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_buffer = io.BytesIO(data)
        video_buffer = io.BytesIO(data)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_reader = decord.VideoReader(video_buffer, num_threads=num_threads)
        video_reader = decord.VideoReader(video_buffer, num_threads=num_threads)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_target_frames = sequence_length if sequence_length > 0 else len(video_reader)
        n_target_frames = sequence_length if sequence_length > 0 else len(video_reader)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_video_frames = len(video_reader)
        n_video_frames = len(video_reader)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_fps = int(np.round(video_reader.get_avg_fps()))
        video_fps = int(np.round(video_reader.get_avg_fps()))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cur_chunk_size = n_video_frames if chunk_size == 0 else chunk_size
        cur_chunk_size = n_video_frames if chunk_size == 0 else chunk_size

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# basic check
        # basic check
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：message = basic_check_on_inputs(
        message = basic_check_on_inputs(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_video_frames=n_video_frames,
            n_video_frames=n_video_frames,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_target_frames=n_target_frames,
            n_target_frames=n_target_frames,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_fps=video_fps,
            video_fps=video_fps,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_fps_thres=min_fps_thres,
            min_fps_thres=min_fps_thres,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_fps_thres=max_fps_thres,
            max_fps_thres=max_fps_thres,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：根据条件选择执行分支；代码：if message != "success":
        if message != "success":
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(message)
            raise ValueError(message)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sampled_chunk_index, n_frames_in_chunk, message = sample_chunk_index_from_chunked_video(
        sampled_chunk_index, n_frames_in_chunk, message = sample_chunk_index_from_chunked_video(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_video_frames=n_video_frames,
            n_video_frames=n_video_frames,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_target_frames=n_target_frames,
            n_target_frames=n_target_frames,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：chunk_size=cur_chunk_size,
            chunk_size=cur_chunk_size,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：根据条件选择执行分支；代码：if sampled_chunk_index == -1:
        if sampled_chunk_index == -1:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(message)
            raise ValueError(message)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：检查运行时假设是否成立；代码：assert message == "success"
            assert message == "success"

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：chunk_frame_start = sampled_chunk_index * cur_chunk_size
        chunk_frame_start = sampled_chunk_index * cur_chunk_size

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：frame_indices, adjusted_fps = get_frame_indices_w_lowered_fps(
        frame_indices, adjusted_fps = get_frame_indices_w_lowered_fps(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_video_frames=n_frames_in_chunk,
            n_video_frames=n_frames_in_chunk,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_fps=video_fps,
            video_fps=video_fps,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_fps_thres=min_fps_thres,
            min_fps_thres=min_fps_thres,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_fps_thres=max_fps_thres,
            max_fps_thres=max_fps_thres,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_target_frames=n_target_frames,
            n_target_frames=n_target_frames,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_indices = [chunk_frame_start + idx for idx in frame_indices]
        frame_indices = [chunk_frame_start + idx for idx in frame_indices]

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Sample frames
        # Sample frames
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_frames = video_reader.get_batch(frame_indices).asnumpy()
        video_frames = video_reader.get_batch(frame_indices).asnumpy()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_frames = torch.from_numpy(video_frames).permute(3, 0, 1, 2) # (T, H, W, C) -> (C, T, H, W)
        video_frames = torch.from_numpy(video_frames).permute(3, 0, 1, 2)  # (T, H, W, C) -> (C, T, H, W)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Clean up
        # Clean up
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video_reader.seek(0)
        video_reader.seek(0)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del video_reader
        del video_reader

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output = {
        output = {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："video": video_frames,
            "video": video_frames,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："fps": float(adjusted_fps),
            "fps": float(adjusted_fps),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："orig_fps": video_fps,
            "orig_fps": video_fps,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："num_frames": video_frames.shape[1],
            "num_frames": video_frames.shape[1],
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："chunk_index": sampled_chunk_index,
            "chunk_index": sampled_chunk_index,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："frame_start": frame_indices[0],
            "frame_start": frame_indices[0],
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："frame_end": frame_indices[-1],
            "frame_end": frame_indices[-1],
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："n_orig_video_frames": n_video_frames,
            "n_orig_video_frames": n_video_frames,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return output
        return output

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return video_decoder
    return video_decoder


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@video_decoder_register("chunked_video_decoder_with_fixed_fps")
@video_decoder_register("chunked_video_decoder_with_fixed_fps")
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def chunked_video_decoder_with_fixed_fps(
def chunked_video_decoder_with_fixed_fps(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：chunk_size: int = 0,
    chunk_size: int = 0,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sequence_length: int = 34,
    sequence_length: int = 34,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：min_fps_thres: int = 4,
    min_fps_thres: int = 4,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_fps_thres: int = 30,
    max_fps_thres: int = 30,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_threads: int = 4,
    num_threads: int = 4,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> dict:
) -> dict:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Video decoder optimized for processing videos with chunked captions.

    unlike other video decoders which return video frames of requested sequence_length.
    The function returns a randomly sampled chunk with duration between 4 seconds and 8 seconds whenever possible.
    The chunk will be provided to modeling code and the frame subsampling happens on the modeling side.
    !!! IMPORTANT: it can only work with batch size 1 otherwise, different length video can not be concatenated.

    This decoder first samples a chunk from the video, then selects frames within that chunk.
    It dynamically adjusts the frame rate with a high probability (>99%) to lower the FPS
    through frame sampling when conditions allow, ensuring efficient processing while
    maintaining video quality.

    The decoder handles variable chunk durations with special processing for chunks that are
    either too short or too long, ensuring consistent output regardless of input video properties.

    Args:
        chunk_size (int): Size of video chunks in frames. If set to 0, the entire video length
                          is used as a single chunk. Defaults to 0.
        sequence_length (int): Number of frames to extract from the video. Defaults to 34.
        min_fps_thres (int): Minimum acceptable frames per second. Videos with lower FPS will
                            raise errors. Defaults to 4.
        max_fps_thres (int): Maximum acceptable frames per second. Higher FPS videos will be
                            downsampled. Defaults to 30.
        num_threads (int): Number of threads to use for video decoding with decord. Defaults to 4.

    Returns:
        dict: A dictionary containing video frames tensor and metadata including:
            - video: Tensor of shape (C, T, H, W) containing the sampled video frames
            - fps: Actual frames per second (float)
            - orig_fps: Original video frame rate (int)
            - num_frames: Number of frames extracted
            - chunk_index: Index of the sampled chunk
            - frame_start: Starting frame index in original video
            - frame_end: Ending frame index in original video
            - n_orig_video_frames: Total number of frames in original video

    Raises:
        ValueError: If video duration is too short, if FPS is outside acceptable range,
                   or if selected chunk has insufficient frames.

    Note:
        - Chunks with duration < 4.0 seconds are skipped with an error.
        - Chunks with duration > 8.0 seconds are capped to 8.0 seconds worth of frames.
        - For best results, ensure videos have FPS between min_fps_thres and max_fps_thres.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def video_decoder(
    def video_decoder(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：key: str,
        key: str,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data: bytes,
        data: bytes,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> dict[str, torch.Tensor | int]:
    ) -> dict[str, torch.Tensor | int]:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Check video extension
        # Check video extension
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extension = re.sub(r".*[.]", "", key)
        extension = re.sub(r".*[.]", "", key)
        # 中文说明：根据条件选择执行分支；代码：if extension.lower() not in _VIDEO_EXTENSIONS:
        if extension.lower() not in _VIDEO_EXTENSIONS:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return None
            return None

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Read video
        # Read video
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_buffer = io.BytesIO(data)
        video_buffer = io.BytesIO(data)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_reader = decord.VideoReader(video_buffer, num_threads=num_threads)
        video_reader = decord.VideoReader(video_buffer, num_threads=num_threads)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_target_frames = sequence_length if sequence_length > 0 else len(video_reader)
        n_target_frames = sequence_length if sequence_length > 0 else len(video_reader)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_video_frames = len(video_reader)
        n_video_frames = len(video_reader)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_fps_float = video_reader.get_avg_fps()
        video_fps_float = video_reader.get_avg_fps()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_fps = int(np.round(video_fps_float))
        video_fps = int(np.round(video_fps_float))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cur_chunk_size = n_video_frames if chunk_size == 0 else chunk_size
        cur_chunk_size = n_video_frames if chunk_size == 0 else chunk_size

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# basic check
        # basic check
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：message = basic_check_on_inputs(
        message = basic_check_on_inputs(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_video_frames=n_video_frames,
            n_video_frames=n_video_frames,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_target_frames=n_target_frames,
            n_target_frames=n_target_frames,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_fps=video_fps,
            video_fps=video_fps,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_fps_thres=min_fps_thres,
            min_fps_thres=min_fps_thres,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_fps_thres=max_fps_thres,
            max_fps_thres=max_fps_thres,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：根据条件选择执行分支；代码：if message != "success":
        if message != "success":
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(message)
            raise ValueError(message)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sampled_chunk_index, n_frames_in_chunk, message = sample_chunk_index_from_chunked_video(
        sampled_chunk_index, n_frames_in_chunk, message = sample_chunk_index_from_chunked_video(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_video_frames=n_video_frames,
            n_video_frames=n_video_frames,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_target_frames=n_target_frames,
            n_target_frames=n_target_frames,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：chunk_size=cur_chunk_size,
            chunk_size=cur_chunk_size,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：根据条件选择执行分支；代码：if sampled_chunk_index == -1:
        if sampled_chunk_index == -1:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(message)
            raise ValueError(message)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：检查运行时假设是否成立；代码：assert message == "success"
            assert message == "success"

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：chunk_frame_start = sampled_chunk_index * cur_chunk_size
        chunk_frame_start = sampled_chunk_index * cur_chunk_size

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：chunk_duration = n_frames_in_chunk / video_fps_float
        chunk_duration = n_frames_in_chunk / video_fps_float
        # 中文说明：根据条件选择执行分支；代码：if chunk_duration < 4.0:
        if chunk_duration < 4.0:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Chunk duration {chunk_duration} is less than 4.0 seconds, skipping")
            raise ValueError(f"Chunk duration {chunk_duration} is less than 4.0 seconds, skipping")

        # 中文说明：根据条件选择执行分支；代码：if chunk_duration > 8.0:
        if chunk_duration > 8.0:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_frames_needed = int(np.ceil(8.0 * video_fps))
            n_frames_needed = int(np.ceil(8.0 * video_fps))
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_frames_needed = n_frames_in_chunk
            n_frames_needed = n_frames_in_chunk

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：chunk_frame_end = chunk_frame_start + n_frames_needed
        chunk_frame_end = chunk_frame_start + n_frames_needed

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_indices = np.arange(chunk_frame_start, chunk_frame_end).tolist()
        frame_indices = np.arange(chunk_frame_start, chunk_frame_end).tolist()

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Sample frames
        # Sample frames
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_frames = video_reader.get_batch(frame_indices).asnumpy()
        video_frames = video_reader.get_batch(frame_indices).asnumpy()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_frames = torch.from_numpy(video_frames).permute(3, 0, 1, 2) # (T, H, W, C) -> (C, T, H, W)
        video_frames = torch.from_numpy(video_frames).permute(3, 0, 1, 2)  # (T, H, W, C) -> (C, T, H, W)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Clean up
        # Clean up
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video_reader.seek(0)
        video_reader.seek(0)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del video_reader
        del video_reader

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output = {
        output = {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："video": video_frames,
            "video": video_frames,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："fps": video_fps_float,
            "fps": video_fps_float,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："orig_fps": video_fps,
            "orig_fps": video_fps,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："num_frames": video_frames.shape[1],
            "num_frames": video_frames.shape[1],
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："chunk_index": sampled_chunk_index,
            "chunk_index": sampled_chunk_index,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："frame_start": frame_indices[0],
            "frame_start": frame_indices[0],
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："frame_end": frame_indices[-1],
            "frame_end": frame_indices[-1],
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："n_orig_video_frames": n_video_frames,
            "n_orig_video_frames": n_video_frames,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return output
        return output

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return video_decoder
    return video_decoder


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def construct_video_decoder(
def construct_video_decoder(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video_decoder_name: str = "chunked_video_decoder",
    video_decoder_name: str = "chunked_video_decoder",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：chunk_size: int = 0,
    chunk_size: int = 0,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sequence_length: int = 34,
    sequence_length: int = 34,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：min_fps_thres: int = 1,
    min_fps_thres: int = 1,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_fps_thres: int = 9999,
    max_fps_thres: int = 9999,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_threads=4,
    num_threads=4,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return VIDEO_DECODER_OPTIONS[video_decoder_name](
    return VIDEO_DECODER_OPTIONS[video_decoder_name](
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：chunk_size=chunk_size,
        chunk_size=chunk_size,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sequence_length=sequence_length,
        sequence_length=sequence_length,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_fps_thres=min_fps_thres,
        min_fps_thres=min_fps_thres,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_fps_thres=max_fps_thres,
        max_fps_thres=max_fps_thres,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_threads=num_threads,
        num_threads=num_threads,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
