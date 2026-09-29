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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import glob
import glob
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from dataclasses import dataclass
from dataclasses import dataclass

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import imageio
import imageio
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@dataclass
@dataclass
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class VideoData:
class VideoData:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：frames: np.ndarray # Shape: [B, H, W, C]
    frames: np.ndarray  # Shape: [B, H, W, C]
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：fps: int
    fps: int
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：duration: int # in seconds
    duration: int  # in seconds


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_video_filepaths(input_dir: str) -> list[str]:
def get_video_filepaths(input_dir: str) -> list[str]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Get a list of filepaths for all videos in the input directory."""
    """Get a list of filepaths for all videos in the input directory."""
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：paths = glob.glob(f"{input_dir}/**/*.mp4", recursive=True)
    paths = glob.glob(f"{input_dir}/**/*.mp4", recursive=True)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：paths += glob.glob(f"{input_dir}/**/*.avi", recursive=True)
    paths += glob.glob(f"{input_dir}/**/*.avi", recursive=True)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：paths += glob.glob(f"{input_dir}/**/*.mov", recursive=True)
    paths += glob.glob(f"{input_dir}/**/*.mov", recursive=True)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：paths = sorted(paths)
    paths = sorted(paths)
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(f"Found {len(paths)} videos")
    log.debug(f"Found {len(paths)} videos")
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return paths
    return paths


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def read_video(filepath: str) -> VideoData:
def read_video(filepath: str) -> VideoData:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Read a video file and extract its frames and metadata."""
    """Read a video file and extract its frames and metadata."""
    # 中文说明：开始一个可捕获异常的代码块；代码：try:
    try:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：reader = imageio.get_reader(filepath, "ffmpeg")
        reader = imageio.get_reader(filepath, "ffmpeg")
    # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
    except Exception as e:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Failed to read video file: {filepath}") from e
        raise ValueError(f"Failed to read video file: {filepath}") from e

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Extract metadata from the video file
    # Extract metadata from the video file
    # 中文说明：开始一个可捕获异常的代码块；代码：try:
    try:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：metadata = reader.get_meta_data()
        metadata = reader.get_meta_data()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fps = metadata.get("fps")
        fps = metadata.get("fps")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：duration = metadata.get("duration")
        duration = metadata.get("duration")
    # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
    except Exception as e:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：reader.close()
        reader.close()
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Failed to extract metadata from video file: {filepath}") from e
        raise ValueError(f"Failed to extract metadata from video file: {filepath}") from e

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Extract frames from the video file
    # Extract frames from the video file
    # 中文说明：开始一个可捕获异常的代码块；代码：try:
    try:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = np.array([frame for frame in reader])
        frames = np.array([frame for frame in reader])
    # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
    except Exception as e:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Failed to extract frames from video file: {filepath}") from e
        raise ValueError(f"Failed to extract frames from video file: {filepath}") from e
    # 中文说明：处理异常、清理资源或管理上下文；代码：finally:
    finally:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：reader.close()
        reader.close()

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return VideoData(frames=frames, fps=fps, duration=duration)
    return VideoData(frames=frames, fps=fps, duration=duration)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def save_video(filepath: str, frames: np.ndarray, fps: int) -> None:
def save_video(filepath: str, frames: np.ndarray, fps: int) -> None:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Save a video file from a sequence of frames."""
    """Save a video file from a sequence of frames."""
    # 中文说明：开始一个可捕获异常的代码块；代码：try:
    try:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：writer = imageio.get_writer(filepath, fps=fps, macro_block_size=1)
        writer = imageio.get_writer(filepath, fps=fps, macro_block_size=1)
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for frame in frames:
        for frame in frames:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：writer.append_data(frame)
            writer.append_data(frame)
    # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
    except Exception as e:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Failed to save video file to {filepath}") from e
        raise ValueError(f"Failed to save video file to {filepath}") from e
    # 中文说明：处理异常、清理资源或管理上下文；代码：finally:
    finally:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：writer.close()
        writer.close()
