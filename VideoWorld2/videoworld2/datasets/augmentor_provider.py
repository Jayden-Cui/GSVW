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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import cosmos_predict2.datasets.augmentors.append_fps_frames_for_image as append_fps_frames_f...
import cosmos_predict2.datasets.augmentors.append_fps_frames_for_image as append_fps_frames_for_image
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import cosmos_predict2.datasets.augmentors.merge_datadict as merge_datadict
import cosmos_predict2.datasets.augmentors.merge_datadict as merge_datadict
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import cosmos_predict2.datasets.augmentors.text_transforms_for_image as text_transforms_for_i...
import cosmos_predict2.datasets.augmentors.text_transforms_for_image as text_transforms_for_image
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import cosmos_predict2.datasets.augmentors.text_transforms_for_video as text_transforms_for_v...
import cosmos_predict2.datasets.augmentors.text_transforms_for_video as text_transforms_for_video
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import cosmos_predict2.datasets.augmentors.video_parsing as video_parsing
import cosmos_predict2.datasets.augmentors.video_parsing as video_parsing
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import imaginaire.datasets.webdataset.augmentors.image.normalize as normalize
import imaginaire.datasets.webdataset.augmentors.image.normalize as normalize
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import imaginaire.datasets.webdataset.augmentors.image.padding as padding
import imaginaire.datasets.webdataset.augmentors.image.padding as padding
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import imaginaire.datasets.webdataset.augmentors.image.resize as resize
import imaginaire.datasets.webdataset.augmentors.image.resize as resize
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.datasets.utils import IMAGE_RES_SIZE_INFO, VIDEO_RES_SIZE_INFO
from videoworld2.datasets.utils import IMAGE_RES_SIZE_INFO, VIDEO_RES_SIZE_INFO
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import LazyCall as L
from imaginaire.lazy_config import LazyCall as L
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：AUGMENTOR_OPTIONS = {}
AUGMENTOR_OPTIONS = {}


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def augmentor_register(key):
def augmentor_register(key):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"registering {key}...")
    log.info(f"registering {key}...")

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def decorator(func):
    def decorator(func):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：AUGMENTOR_OPTIONS[key] = func
        AUGMENTOR_OPTIONS[key] = func
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return func
        return func

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return decorator
    return decorator


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_video_text_transform(
def get_video_text_transform(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：caption_type: str,
    caption_type: str,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：embedding_type: str,
    embedding_type: str,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：long_caption_ratio: int = 7,
    long_caption_ratio: int = 7,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：medium_caption_ratio: int = 2,
    medium_caption_ratio: int = 2,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：short_caption_ratio: int = 1,
    short_caption_ratio: int = 1,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：user_caption_ratio: int = 90,
    user_caption_ratio: int = 90,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_video_frames: int = -1,
    num_video_frames: int = -1,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del num_video_frames
    del num_video_frames
    # 中文说明：根据条件选择执行分支；代码：if caption_type == "t2w_qwen2p5_7b":
    if caption_type == "t2w_qwen2p5_7b":
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(
        log.info(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"caption_type: {caption_type}, long_caption_ratio: {long_caption_ratio}, medium_caption_rati...
            f"caption_type: {caption_type}, long_caption_ratio: {long_caption_ratio}, medium_caption_ratio: {medium_caption_ratio}, short_caption_ratio: {short_caption_ratio}, user_caption_ratio: {user_caption_ratio}"
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_text_transform = L(text_transforms_for_video.TextTransformForVideo)(
        video_text_transform = L(text_transforms_for_video.TextTransformForVideo)(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_keys=[],
            input_keys=[],
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：args={
            args={
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："captions_key": "metas",
                "captions_key": "metas",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："embeddings_key": embedding_type,
                "embeddings_key": embedding_type,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："caption_windows_key": "t2w_windows",
                "caption_windows_key": "t2w_windows",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："caption_type": "qwen2p5_7b_caption",
                "caption_type": "qwen2p5_7b_caption",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："embedding_caption_type": "t2w_qwen2p5_7b",
                "embedding_caption_type": "t2w_qwen2p5_7b",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："t5_tokens": {"num": 512},
                "t5_tokens": {"num": 512},
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："is_mask_all_ones": True,
                "is_mask_all_ones": True,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："caption_probs": {
                "caption_probs": {
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："long": long_caption_ratio,
                    "long": long_caption_ratio,
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："medium": medium_caption_ratio,
                    "medium": medium_caption_ratio,
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："short": short_caption_ratio,
                    "short": short_caption_ratio,
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："user": user_caption_ratio,
                    "user": user_caption_ratio,
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：},
                },
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：},
            },
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
    # 中文说明：根据条件选择执行分支；代码：elif caption_type == "i2w_qwen2p5_7b_later_frames":
    elif caption_type == "i2w_qwen2p5_7b_later_frames":
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_text_transform = L(text_transforms_for_video.TextTransformForVideo)(
        video_text_transform = L(text_transforms_for_video.TextTransformForVideo)(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_keys=[],
            input_keys=[],
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：args={
            args={
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："captions_key": "metas",
                "captions_key": "metas",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："embeddings_key": embedding_type,
                "embeddings_key": embedding_type,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："caption_windows_key": "i2w_windows_later_frames",
                "caption_windows_key": "i2w_windows_later_frames",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："caption_type": "qwen2p5_7b_caption",
                "caption_type": "qwen2p5_7b_caption",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："embedding_caption_type": "i2w_qwen2p5_7b_later_frames",
                "embedding_caption_type": "i2w_qwen2p5_7b_later_frames",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："t5_tokens": {"num": 512},
                "t5_tokens": {"num": 512},
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："is_mask_all_ones": True,
                "is_mask_all_ones": True,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："caption_probs": {
                "caption_probs": {
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："long": long_caption_ratio,
                    "long": long_caption_ratio,
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："medium": medium_caption_ratio,
                    "medium": medium_caption_ratio,
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："short": short_caption_ratio,
                    "short": short_caption_ratio,
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："user": user_caption_ratio,
                    "user": user_caption_ratio,
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：},
                },
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：},
            },
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Unsupported caption type ({caption_type}) for video data")
        raise ValueError(f"Unsupported caption type ({caption_type}) for video data")

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return video_text_transform
    return video_text_transform


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@augmentor_register("video_basic_augmentor_v2")
@augmentor_register("video_basic_augmentor_v2")
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_video_augmentor_v2(
def get_video_augmentor_v2(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：resolution: str,
    resolution: str,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：caption_type: str = "t2w_qwen2p5_7b",
    caption_type: str = "t2w_qwen2p5_7b",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：embedding_type: str = "t5_xxl",
    embedding_type: str = "t5_xxl",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：min_fps: int = 10,
    min_fps: int = 10,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_fps: int = 60,
    max_fps: int = 60,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：long_caption_ratio: int = 7,
    long_caption_ratio: int = 7,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：medium_caption_ratio: int = 2,
    medium_caption_ratio: int = 2,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：short_caption_ratio: int = 1,
    short_caption_ratio: int = 1,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：user_caption_ratio: int = 90,
    user_caption_ratio: int = 90,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_video_frames: int = -1,
    num_video_frames: int = -1,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    num_video_frames: -1 means use all frames, otherwise use the number of frames specified.

    Video augmentor V2. It works with a naive video decoder ("video_naive_bytes") that does nothing.
    Augmentors here include:
    - a basic video decoder that fetches frames within a window and delegates further subsampling or duplication to the modeling code to produce videos with the required number of frames.
    - resize the video
    - add reflection padding
    - extract captions and embeddings.

    Supported caption_type include t2w_qwen2p5_7b and i2w_qwen2p5_7b_later_frames.
    Supported embedding_type include t5_xxl and umt5_xxl.
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_text_transform = get_video_text_transform(
    video_text_transform = get_video_text_transform(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：caption_type=caption_type,
        caption_type=caption_type,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：embedding_type=embedding_type,
        embedding_type=embedding_type,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：long_caption_ratio=long_caption_ratio,
        long_caption_ratio=long_caption_ratio,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：medium_caption_ratio=medium_caption_ratio,
        medium_caption_ratio=medium_caption_ratio,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：short_caption_ratio=short_caption_ratio,
        short_caption_ratio=short_caption_ratio,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：user_caption_ratio=user_caption_ratio,
        user_caption_ratio=user_caption_ratio,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：根据条件选择执行分支；代码：if caption_type == "t2w_qwen2p5_7b":
    if caption_type == "t2w_qwen2p5_7b":
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：key_for_caption = "t2w_windows"
        key_for_caption = "t2w_windows"
    # 中文说明：根据条件选择执行分支；代码：elif caption_type == "i2w_qwen2p5_7b_later_frames":
    elif caption_type == "i2w_qwen2p5_7b_later_frames":
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：key_for_caption = "i2w_windows_later_frames"
        key_for_caption = "i2w_windows_later_frames"
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Unsupported caption type ({caption_type}) for video data"
        f"Unsupported caption type ({caption_type}) for video data"
    # 中文说明：检查运行时假设是否成立；代码：assert embedding_type in ("t5_xxl", "umt5_xxl"), f"Unsupported embeddings type ({embedding_ty...
    assert embedding_type in ("t5_xxl", "umt5_xxl"), f"Unsupported embeddings type ({embedding_type}) for video data"

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return {
    return {
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："video_parsing": L(video_parsing.VideoParsing)(
        "video_parsing": L(video_parsing.VideoParsing)(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_keys=["metas", "video"],
            input_keys=["metas", "video"],
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：args={
            args={
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："key_for_caption": key_for_caption,
                "key_for_caption": key_for_caption,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："min_duration": 4.0,
                "min_duration": 4.0,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："min_fps": min_fps,
                "min_fps": min_fps,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："max_fps": max_fps,
                "max_fps": max_fps,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："video_decode_num_threads": 4,
                "video_decode_num_threads": 4,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："num_video_frames": num_video_frames,
                "num_video_frames": num_video_frames,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：},
            },
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："merge_datadict": L(merge_datadict.DataDictMerger)(
        "merge_datadict": L(merge_datadict.DataDictMerger)(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_keys=["video"],
            input_keys=["video"],
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_keys=[
            output_keys=[
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："video",
                "video",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："fps",
                "fps",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："num_frames",
                "num_frames",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："chunk_index",
                "chunk_index",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："frame_start",
                "frame_start",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："frame_end",
                "frame_end",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："n_orig_video_frames",
                "n_orig_video_frames",
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：],
            ],
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："resize_largest_side_aspect_ratio_preserving": L(resize.ResizeLargestSideAspectPreserving)(
        "resize_largest_side_aspect_ratio_preserving": L(resize.ResizeLargestSideAspectPreserving)(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_keys=["video"],
            input_keys=["video"],
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：args={"size": VIDEO_RES_SIZE_INFO[resolution]},
            args={"size": VIDEO_RES_SIZE_INFO[resolution]},
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："reflection_padding": L(padding.ReflectionPadding)(
        "reflection_padding": L(padding.ReflectionPadding)(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_keys=["video"],
            input_keys=["video"],
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：args={"size": VIDEO_RES_SIZE_INFO[resolution]},
            args={"size": VIDEO_RES_SIZE_INFO[resolution]},
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："text_transform": video_text_transform,
        "text_transform": video_text_transform,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
    }


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@augmentor_register("image_basic_augmentor")
@augmentor_register("image_basic_augmentor")
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_image_augmentor(
def get_image_augmentor(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：resolution: str,
    resolution: str,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：caption_type: str = "ai_v3p1",
    caption_type: str = "ai_v3p1",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：embedding_type: str = "t5_xxl",
    embedding_type: str = "t5_xxl",
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：augmentation = {
    augmentation = {
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："resize_largest_side_aspect_ratio_preserving": L(resize.ResizeLargestSideAspectPreserving)(
        "resize_largest_side_aspect_ratio_preserving": L(resize.ResizeLargestSideAspectPreserving)(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_keys=["images"],
            input_keys=["images"],
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：args={"size": IMAGE_RES_SIZE_INFO[resolution]},
            args={"size": IMAGE_RES_SIZE_INFO[resolution]},
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："reflection_padding": L(padding.ReflectionPadding)(
        "reflection_padding": L(padding.ReflectionPadding)(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_keys=["images"],
            input_keys=["images"],
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：args={"size": IMAGE_RES_SIZE_INFO[resolution]},
            args={"size": IMAGE_RES_SIZE_INFO[resolution]},
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："normalize": L(normalize.Normalize)(
        "normalize": L(normalize.Normalize)(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_keys=["images"],
            input_keys=["images"],
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：args={"mean": 0.5, "std": 0.5},
            args={"mean": 0.5, "std": 0.5},
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："text_transform": L(text_transforms_for_image.TextTransformForImage)(
        "text_transform": L(text_transforms_for_image.TextTransformForImage)(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_keys=[],
            input_keys=[],
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：args={
            args={
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："caption_type": caption_type,
                "caption_type": caption_type,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："embedding_type": embedding_type,
                "embedding_type": embedding_type,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："weight_captions_gt": 0.05,
                "weight_captions_gt": 0.05,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："caption_probs": {"ground_truth": 1},
                "caption_probs": {"ground_truth": 1},
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："t5_tokens": {"num": 512, "dim": 1024},
                "t5_tokens": {"num": 512, "dim": 1024},
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："is_mask_all_ones": True,
                "is_mask_all_ones": True,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：},
            },
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："append_fps_frames": L(append_fps_frames_for_image.AppendFPSFramesForImage)(),
        "append_fps_frames": L(append_fps_frames_for_image.AppendFPSFramesForImage)(),
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
    }

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return augmentation
    return augmentation


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@augmentor_register("video_basic_augmentor_v2_with_edge_control")
@augmentor_register("video_basic_augmentor_v2_with_edge_control")
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_video_augmentor_v2_with_edge_control(
def get_video_augmentor_v2_with_edge_control(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：resolution: str,
    resolution: str,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：caption_type: str = "t2w_qwen2p5_7b",
    caption_type: str = "t2w_qwen2p5_7b",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：embedding_type: str = "t5_xxl",
    embedding_type: str = "t5_xxl",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：min_fps: int = 10,
    min_fps: int = 10,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_fps: int = 60,
    max_fps: int = 60,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：long_caption_ratio: int = 7,
    long_caption_ratio: int = 7,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：medium_caption_ratio: int = 2,
    medium_caption_ratio: int = 2,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：short_caption_ratio: int = 1,
    short_caption_ratio: int = 1,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：user_caption_ratio: int = 90,
    user_caption_ratio: int = 90,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_video_frames: int = -1,
    num_video_frames: int = -1,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**kwargs,
    **kwargs,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Video augmentor V2. It works with a naive video decoder ("video_naive_bytes") that does no...
    """Video augmentor V2. It works with a naive video decoder ("video_naive_bytes") that does nothing.
    Augmentors here include:
    - a basic video decoder that fetches frames within a window and delegates further subsampling or duplication to the modeling code to produce videos with the required number of frames.
    - resize the video
    - add reflection padding
    - extract captions and embeddings.

    Supported caption_type include t2w_qwen2p5_7b and i2w_qwen2p5_7b_later_frames.
    Supported embedding_type include t5_xxl and umt5_xxl.
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_text_transform = get_video_text_transform(caption_type=caption_type, embedding_type=emb...
    video_text_transform = get_video_text_transform(caption_type=caption_type, embedding_type=embedding_type)
    # 中文说明：根据条件选择执行分支；代码：if caption_type == "t2w_qwen2p5_7b":
    if caption_type == "t2w_qwen2p5_7b":
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：key_for_caption = "t2w_windows"
        key_for_caption = "t2w_windows"
    # 中文说明：根据条件选择执行分支；代码：elif caption_type == "i2w_qwen2p5_7b_later_frames":
    elif caption_type == "i2w_qwen2p5_7b_later_frames":
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：key_for_caption = "i2w_windows_later_frames"
        key_for_caption = "i2w_windows_later_frames"
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Unsupported caption type ({caption_type}) for video data"
        f"Unsupported caption type ({caption_type}) for video data"
    # 中文说明：检查运行时假设是否成立；代码：assert embedding_type in ("t5_xxl", "umt5_xxl"), f"Unsupported embeddings type ({embedding_ty...
    assert embedding_type in ("t5_xxl", "umt5_xxl"), f"Unsupported embeddings type ({embedding_type}) for video data"

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return {
    return {
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："video_parsing": L(video_parsing.VideoParsing)(
        "video_parsing": L(video_parsing.VideoParsing)(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_keys=["metas", "video"],
            input_keys=["metas", "video"],
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：args={
            args={
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："key_for_caption": key_for_caption,
                "key_for_caption": key_for_caption,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："min_duration": 4.0,
                "min_duration": 4.0,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："min_fps": min_fps,
                "min_fps": min_fps,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："max_fps": max_fps,
                "max_fps": max_fps,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："video_decode_num_threads": 4,
                "video_decode_num_threads": 4,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："num_video_frames": num_video_frames,
                "num_video_frames": num_video_frames,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：},
            },
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："merge_datadict": L(merge_datadict.DataDictMerger)(
        "merge_datadict": L(merge_datadict.DataDictMerger)(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_keys=["video"],
            input_keys=["video"],
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_keys=[
            output_keys=[
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："video",
                "video",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："fps",
                "fps",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："num_frames",
                "num_frames",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："chunk_index",
                "chunk_index",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："frame_start",
                "frame_start",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："frame_end",
                "frame_end",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："n_orig_video_frames",
                "n_orig_video_frames",
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：],
            ],
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："resize_largest_side_aspect_ratio_preserving": L(resize.ResizeLargestSideAspectPreserving)(
        "resize_largest_side_aspect_ratio_preserving": L(resize.ResizeLargestSideAspectPreserving)(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_keys=["video"],
            input_keys=["video"],
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：args={"size": VIDEO_RES_SIZE_INFO[resolution]},
            args={"size": VIDEO_RES_SIZE_INFO[resolution]},
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："reflection_padding": L(padding.ReflectionPadding)(
        "reflection_padding": L(padding.ReflectionPadding)(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_keys=["video"],
            input_keys=["video"],
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：args={"size": VIDEO_RES_SIZE_INFO[resolution]},
            args={"size": VIDEO_RES_SIZE_INFO[resolution]},
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："text_transform": video_text_transform,
        "text_transform": video_text_transform,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
    }
