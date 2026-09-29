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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import IO, Any, Dict, Tuple
from typing import IO, Any, Dict, Tuple

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import imageio
import imageio
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import imageio.v3 as iio_v3
import imageio.v3 as iio_v3
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.handlers.base import BaseFileHandler
from imaginaire.utils.easy_io.handlers.base import BaseFileHandler


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ImageioVideoHandler(BaseFileHandler):
class ImageioVideoHandler(BaseFileHandler):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：str_like = False
    str_like = False

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def load_from_fileobj(
    def load_from_fileobj(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, file: IO[bytes], format: str = "mp4", mode: str = "rgb", **kwargs
        self, file: IO[bytes], format: str = "mp4", mode: str = "rgb", **kwargs
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[np.ndarray, Dict[str, Any]]:
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Load video from a file-like object using imageio.v3 with specified format and color mode.

        Parameters:
            file (IO[bytes]): A file-like object containing video data.
            format (str): Format of the video file (default 'mp4').
            mode (str): Color mode of the video, 'rgb' or 'gray' (default 'rgb').

        Returns:
            tuple: A tuple containing an array of video frames and metadata about the video.
        """
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：file.seek(0)
        file.seek(0)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# The plugin argument in v3 replaces the format argument in v2
        # The plugin argument in v3 replaces the format argument in v2
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：plugin = kwargs.pop("plugin", "pyav")
        plugin = kwargs.pop("plugin", "pyav")

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Load all frames at once using v3 API
        # Load all frames at once using v3 API
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_frames = iio_v3.imread(file, plugin=plugin, **kwargs)
        video_frames = iio_v3.imread(file, plugin=plugin, **kwargs)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Handle grayscale conversion if needed
        # Handle grayscale conversion if needed
        # 中文说明：根据条件选择执行分支；代码：if mode == "gray":
        if mode == "gray":
            # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import cv2
            import cv2

            # 中文说明：根据条件选择执行分支；代码：if len(video_frames.shape) == 4: # (frames, height, width, channels)
            if len(video_frames.shape) == 4:  # (frames, height, width, channels)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gray_frames = []
                gray_frames = []
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for frame in video_frames:
                for frame in video_frames:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                    gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gray_frame = np.expand_dims(gray_frame, axis=2) # Keep dimensions consistent
                    gray_frame = np.expand_dims(gray_frame, axis=2)  # Keep dimensions consistent
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：gray_frames.append(gray_frame)
                    gray_frames.append(gray_frame)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_frames = np.array(gray_frames)
                video_frames = np.array(gray_frames)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Extract metadata
        # Extract metadata
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Note: iio_v3.imread doesn't return metadata directly like v2 did
        # Note: iio_v3.imread doesn't return metadata directly like v2 did
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# We need to extract it separately
        # We need to extract it separately
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：file.seek(0)
        file.seek(0)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：metadata = self._extract_metadata(file, plugin=plugin)
        metadata = self._extract_metadata(file, plugin=plugin)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return video_frames, metadata
        return video_frames, metadata

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _extract_metadata(self, file: IO[bytes], plugin: str = "pyav") -> Dict[str, Any]:
    def _extract_metadata(self, file: IO[bytes], plugin: str = "pyav") -> Dict[str, Any]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Extract metadata from a video file.

        Parameters:
            file (IO[bytes]): File-like object containing video data.
            plugin (str): Plugin to use for reading.

        Returns:
            dict: Video metadata.
        """
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Create a generator to read frames and metadata
            # Create a generator to read frames and metadata
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：metadata = iio_v3.immeta(file, plugin=plugin)
            metadata = iio_v3.immeta(file, plugin=plugin)

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Add some standard fields similar to v2 metadata format
            # Add some standard fields similar to v2 metadata format
            # 中文说明：根据条件选择执行分支；代码：if "fps" not in metadata and "duration" in metadata:
            if "fps" not in metadata and "duration" in metadata:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Read the first frame to get shape information
                # Read the first frame to get shape information
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：file.seek(0)
                file.seek(0)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：first_frame = iio_v3.imread(file, plugin=plugin, index=0)
                first_frame = iio_v3.imread(file, plugin=plugin, index=0)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：metadata["size"] = first_frame.shape[1::-1] # (width, height)
                metadata["size"] = first_frame.shape[1::-1]  # (width, height)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：metadata["source_size"] = metadata["size"]
                metadata["source_size"] = metadata["size"]

                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Create a consistent metadata structure with v2
                # Create a consistent metadata structure with v2
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：metadata["plugin"] = plugin
                metadata["plugin"] = plugin
                # 中文说明：根据条件选择执行分支；代码：if "codec" not in metadata:
                if "codec" not in metadata:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：metadata["codec"] = "unknown"
                    metadata["codec"] = "unknown"
                # 中文说明：根据条件选择执行分支；代码：if "pix_fmt" not in metadata:
                if "pix_fmt" not in metadata:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：metadata["pix_fmt"] = "unknown"
                    metadata["pix_fmt"] = "unknown"

                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Calculate nframes if possible
                # Calculate nframes if possible
                # 中文说明：根据条件选择执行分支；代码：if "fps" in metadata and "duration" in metadata:
                if "fps" in metadata and "duration" in metadata:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：metadata["nframes"] = int(metadata["fps"] * metadata["duration"])
                    metadata["nframes"] = int(metadata["fps"] * metadata["duration"])
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：metadata["nframes"] = float("inf")
                    metadata["nframes"] = float("inf")

            # 中文说明：从当前函数返回结果或结束函数执行；代码：return metadata
            return metadata

        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
        except Exception as e:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Fallback to basic metadata
            # Fallback to basic metadata
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return {
            return {
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："plugin": plugin,
                "plugin": plugin,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："nframes": float("inf"),
                "nframes": float("inf"),
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："codec": "unknown",
                "codec": "unknown",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："fps": 30.0, # Default values
                "fps": 30.0,  # Default values
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："duration": 0,
                "duration": 0,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："size": (0, 0),
                "size": (0, 0),
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
            }

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def dump_to_fileobj(
    def dump_to_fileobj(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：obj: np.ndarray | torch.Tensor,
        obj: np.ndarray | torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：file: IO[bytes],
        file: IO[bytes],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：format: str = "mp4", # pylint: disable=redefined-builtin
        format: str = "mp4",  # pylint: disable=redefined-builtin
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：fps: int = 17,
        fps: int = 17,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：quality: int = 7,
        quality: int = 7,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ffmpeg_params=None,
        ffmpeg_params=None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**kwargs,
        **kwargs,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Save an array of video frames to a file-like object using imageio.

        Parameters:
            obj (Union[np.ndarray, torch.Tensor]): An array of frames to be saved as video.
            file (IO[bytes]): A file-like object to which the video data will be written.
            format (str): Format of the video file (default 'mp4').
            fps (int): Frames per second of the output video (default 17).
            quality (int): Quality of the video (0-10, default 5).
            ffmpeg_params (list): Additional parameters to pass to ffmpeg.

        """
        # 中文说明：根据条件选择执行分支；代码：if isinstance(obj, torch.Tensor):
        if isinstance(obj, torch.Tensor):
            # 中文说明：检查运行时假设是否成立；代码：assert obj.dtype == torch.uint8, "Tensor must be of type uint8"
            assert obj.dtype == torch.uint8, "Tensor must be of type uint8"
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：obj = obj.cpu().numpy()
            obj = obj.cpu().numpy()
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：h, w = obj.shape[1:-1]
        h, w = obj.shape[1:-1]

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Default ffmpeg params that ensure width and height are set
        # Default ffmpeg params that ensure width and height are set
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default_ffmpeg_params = ["-s", f"{w}x{h}"]
        default_ffmpeg_params = ["-s", f"{w}x{h}"]

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Use provided ffmpeg_params if any, otherwise use defaults
        # Use provided ffmpeg_params if any, otherwise use defaults
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：final_ffmpeg_params = ffmpeg_params if ffmpeg_params is not None else default_ffmpeg_params
        final_ffmpeg_params = ffmpeg_params if ffmpeg_params is not None else default_ffmpeg_params

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mimsave_kwargs = {
        mimsave_kwargs = {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："fps": fps,
            "fps": fps,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："quality": quality,
            "quality": quality,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："macro_block_size": 1,
            "macro_block_size": 1,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："ffmpeg_params": final_ffmpeg_params,
            "ffmpeg_params": final_ffmpeg_params,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："output_params": ["-f", "mp4"],
            "output_params": ["-f", "mp4"],
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Update with any other kwargs
        # Update with any other kwargs
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：mimsave_kwargs.update(kwargs)
        mimsave_kwargs.update(kwargs)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(f"mimsave_kwargs: {mimsave_kwargs}")
        log.debug(f"mimsave_kwargs: {mimsave_kwargs}")

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：imageio.mimsave(file, obj, format, **mimsave_kwargs)
        imageio.mimsave(file, obj, format, **mimsave_kwargs)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def dump_to_str(self, obj, **kwargs):
    def dump_to_str(self, obj, **kwargs):
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise NotImplementedError
        raise NotImplementedError
