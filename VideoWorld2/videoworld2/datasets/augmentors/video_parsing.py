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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import random
import random
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Optional
from typing import Optional

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import decord
import decord
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from einops import rearrange
from einops import rearrange
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torchvision.transforms.v2 import UniformTemporalSubsample
from torchvision.transforms.v2 import UniformTemporalSubsample

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.datasets.webdataset.augmentors.augmentor import Augmentor
from imaginaire.datasets.webdataset.augmentors.augmentor import Augmentor
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class VideoParsing(Augmentor):
class VideoParsing(Augmentor):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    This augmentor is used to parse the video bytes and get the video frames.
    the return dict is back-compatible with old datasets, which video decoding happens in the decoder stage.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, input_keys: list, output_keys: Optional[list] = None, args: Optional[dict]...
    def __init__(self, input_keys: list, output_keys: Optional[list] = None, args: Optional[dict] = None) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(input_keys, output_keys, args)
        super().__init__(input_keys, output_keys, args)
        # 中文说明：检查运行时假设是否成立；代码：assert len(input_keys) == 2, "VideoParsing augmentor only supports two input keys"
        assert len(input_keys) == 2, "VideoParsing augmentor only supports two input keys"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.meta_key = input_keys[0]
        self.meta_key = input_keys[0]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.video_key = input_keys[1]
        self.video_key = input_keys[1]

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.key_for_caption = args["key_for_caption"]
        self.key_for_caption = args["key_for_caption"]
        # 中文说明：检查运行时假设是否成立；代码：assert self.key_for_caption in [
        assert self.key_for_caption in [
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："t2w_windows",
            "t2w_windows",
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："i2w_windows_later_frames",
            "i2w_windows_later_frames",
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：], "key_for_caption must be either t2w_windows or i2w_windows_later_frames"
        ], "key_for_caption must be either t2w_windows or i2w_windows_later_frames"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.min_duration = args["min_duration"]
        self.min_duration = args["min_duration"]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.min_fps = args["min_fps"]
        self.min_fps = args["min_fps"]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.max_fps = args["max_fps"]
        self.max_fps = args["max_fps"]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_frames = args["num_video_frames"]
        self.num_frames = args["num_video_frames"]
        # 中文说明：根据条件选择执行分支；代码：if self.num_frames > 0:
        if self.num_frames > 0:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.sampler = UniformTemporalSubsample(self.num_frames)
            self.sampler = UniformTemporalSubsample(self.num_frames)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.video_decode_num_threads = args["video_decode_num_threads"]
        self.video_decode_num_threads = args["video_decode_num_threads"]

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, data_dict: dict) -> dict:
    def __call__(self, data_dict: dict) -> dict:
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：meta_dict = data_dict[self.meta_key]
            meta_dict = data_dict[self.meta_key]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = data_dict[self.video_key]
            video = data_dict[self.video_key]
        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
        except Exception as e:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(
            log.warning(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Cannot find video. url: {data_dict['__url__']}, key: {data_dict['__key__']}", rank0_only=False
                f"Cannot find video. url: {data_dict['__url__']}, key: {data_dict['__key__']}", rank0_only=False
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return None
            return None

        # 中文说明：根据条件选择执行分支；代码：if not isinstance(video, bytes):
        if not isinstance(video, bytes):
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return data_dict
            return data_dict

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_info = {
        video_info = {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："fps": meta_dict["framerate"],
            "fps": meta_dict["framerate"],
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："n_orig_video_frames": meta_dict["nb_frames"],
            "n_orig_video_frames": meta_dict["nb_frames"],
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }

        # 中文说明：根据条件选择执行分支；代码：if video_info["fps"] < self.min_fps:
        if video_info["fps"] < self.min_fps:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(f"Video FPS {video_info['fps']} is less than min_fps {self.min_fps}", rank0_only=...
            log.warning(f"Video FPS {video_info['fps']} is less than min_fps {self.min_fps}", rank0_only=False)
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return None
            return None
        # 中文说明：根据条件选择执行分支；代码：if video_info["fps"] > self.max_fps:
        if video_info["fps"] > self.max_fps:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(f"Video FPS {video_info['fps']} is greater than max_fps {self.max_fps}", rank0_on...
            log.warning(f"Video FPS {video_info['fps']} is greater than max_fps {self.max_fps}", rank0_only=False)
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return None
            return None

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：options: list = list((i, item) for i, item in enumerate(meta_dict[self.key_for_caption]))
        options: list = list((i, item) for i, item in enumerate(meta_dict[self.key_for_caption]))

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Skip the last window if possible.
        # Skip the last window if possible.
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# All windows except the last are 5 seconds long. The last window has a duration in the range...
        # All windows except the last are 5 seconds long. The last window has a duration in the range [2.5s, 7.5), which is less preferred.
        # 中文说明：根据条件选择执行分支；代码：if len(options) > 1:
        if len(options) > 1:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：options = options[:-1]
            options = options[:-1]

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# shuffle options
        # shuffle options
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：random.shuffle(options)
        random.shuffle(options)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_frames = None
        video_frames = None
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for chunk_index, option in options:
        for chunk_index, option in options:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：start_frame = option["start_frame"]
            start_frame = option["start_frame"]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：end_frame = option["end_frame"]
            end_frame = option["end_frame"]
            # 中文说明：根据条件选择执行分支；代码：if (end_frame - start_frame) < self.min_duration * video_info["fps"]:
            if (end_frame - start_frame) < self.min_duration * video_info["fps"]:
                # 中文说明：执行循环控制或空操作；代码：continue
                continue

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_buffer = io.BytesIO(video)
            video_buffer = io.BytesIO(video)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_reader = decord.VideoReader(video_buffer, num_threads=self.video_decode_num_threads)
            video_reader = decord.VideoReader(video_buffer, num_threads=self.video_decode_num_threads)

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_indices = np.arange(start_frame, end_frame).tolist()
            frame_indices = np.arange(start_frame, end_frame).tolist()

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# online hot-fix for alpamayo data. Skip the first 5 frames as there is chance that the first...
            # online hot-fix for alpamayo data. Skip the first 5 frames as there is chance that the first five frames contain black frames.
            # 中文说明：根据条件选择执行分支；代码：if "alpamayo" in data_dict["__url__"].root:
            if "alpamayo" in data_dict["__url__"].root:
                # 中文说明：检查运行时假设是否成立；代码：assert (
                assert (
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：len(frame_indices) >= 5
                    len(frame_indices) >= 5
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), "Getting less than 5 frames for alpamayo videos. There is no way to skip the first five fr...
                ), "Getting less than 5 frames for alpamayo videos. There is no way to skip the first five frames."
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_indices = frame_indices[5:]
                frame_indices = frame_indices[5:]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：start_frame += 5
                start_frame += 5
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_frames = video_reader.get_batch(frame_indices).asnumpy()
            video_frames = video_reader.get_batch(frame_indices).asnumpy()

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_frames = torch.from_numpy(video_frames).permute(3, 0, 1, 2) # (T, H, W, C) -> (C, T, H, W)
            video_frames = torch.from_numpy(video_frames).permute(3, 0, 1, 2)  # (T, H, W, C) -> (C, T, H, W)

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Clean up
            # Clean up
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video_reader.seek(0) # set video reader point back to 0 to clean up cache
            video_reader.seek(0)  # set video reader point back to 0 to clean up cache
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del video_reader # delete the reader to avoid memory leak
            del video_reader  # delete the reader to avoid memory leak
            # 中文说明：执行循环控制或空操作；代码：break
            break

        # 中文说明：根据条件选择执行分支；代码：if video_frames is None:
        if video_frames is None:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(
            log.warning(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"No valid video frames found, return None. url: {data_dict['__url__']}, key: {data_dict['__k...
                f"No valid video frames found, return None. url: {data_dict['__url__']}, key: {data_dict['__key__']}",
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank0_only=False,
                rank0_only=False,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return None
            return None

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_info["chunk_index"] = chunk_index
        video_info["chunk_index"] = chunk_index
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_info["frame_start"] = start_frame
        video_info["frame_start"] = start_frame
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_info["frame_end"] = end_frame
        video_info["frame_end"] = end_frame
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_info["num_frames"] = end_frame - start_frame
        video_info["num_frames"] = end_frame - start_frame
        # 中文说明：根据条件选择执行分支；代码：if self.num_frames > 0:
        if self.num_frames > 0:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_frames = rearrange(self.sampler(rearrange(video_frames, "c t h w -> t c h w")), "t c h ...
            video_frames = rearrange(self.sampler(rearrange(video_frames, "c t h w -> t c h w")), "t c h w -> c t h w")

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_info["video"] = video_frames
        video_info["video"] = video_frames

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# update data_dict, make it back-compatible with old datasets, which video decoding happens i...
        # update data_dict, make it back-compatible with old datasets, which video decoding happens in the decoder stage.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_dict[self.video_key] = video_info
        data_dict[self.video_key] = video_info

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return data_dict
        return data_dict
