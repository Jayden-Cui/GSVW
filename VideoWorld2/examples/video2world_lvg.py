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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import argparse
import argparse
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import json
import json
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Set TOKENIZERS_PARALLELISM environment variable to avoid deadlocks with multiprocessing
# Set TOKENIZERS_PARALLELISM environment variable to avoid deadlocks with multiprocessing
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import tempfile
import tempfile

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from megatron.core import parallel_state
from megatron.core import parallel_state
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from tqdm import tqdm
from tqdm import tqdm

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.configs.base.config_video2world import (
from videoworld2.configs.base.config_video2world import (
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：PREDICT2_VIDEO2WORLD_PIPELINE_2B,
    PREDICT2_VIDEO2WORLD_PIPELINE_2B,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：PREDICT2_VIDEO2WORLD_PIPELINE_14B,
    PREDICT2_VIDEO2WORLD_PIPELINE_14B,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.pipelines.video2world import _IMAGE_EXTENSIONS, _VIDEO_EXTENSIONS, Video2Wor...
from videoworld2.pipelines.video2world import _IMAGE_EXTENSIONS, _VIDEO_EXTENSIONS, Video2WorldPipeline
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import distributed, log, misc
from imaginaire.utils import distributed, log, misc
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.io import save_image_or_video
from imaginaire.utils.io import save_image_or_video

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_DEFAULT_NEGATIVE_PROMPT = "The video captures a series of frames showing ugly scenes, static...
_DEFAULT_NEGATIVE_PROMPT = "The video captures a series of frames showing ugly scenes, static with no motion, motion blur, over-saturation, shaky footage, low resolution, grainy texture, pixelated images, poorly lit areas, underexposed and overexposed scenes, poor color balance, washed out colors, choppy sequences, jerky movements, low frame rate, artifacting, color banding, unnatural transitions, outdated special effects, fake elements, unconvincing visuals, poorly edited content, jump cuts, visual noise, and flickering. Overall, the video is of poor quality."


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def validate_input_file(input_path: str, num_conditional_frames: int) -> bool:
def validate_input_file(input_path: str, num_conditional_frames: int) -> bool:
    # 中文说明：根据条件选择执行分支；代码：if not os.path.exists(input_path):
    if not os.path.exists(input_path):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(f"Input file does not exist, skipping: {input_path}")
        log.warning(f"Input file does not exist, skipping: {input_path}")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return False
        return False

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ext = os.path.splitext(input_path)[1].lower()
    ext = os.path.splitext(input_path)[1].lower()

    # 中文说明：根据条件选择执行分支；代码：if num_conditional_frames == 1:
    if num_conditional_frames == 1:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Single frame conditioning: accept both images and videos
        # Single frame conditioning: accept both images and videos
        # 中文说明：根据条件选择执行分支；代码：if ext not in _IMAGE_EXTENSIONS and ext not in _VIDEO_EXTENSIONS:
        if ext not in _IMAGE_EXTENSIONS and ext not in _VIDEO_EXTENSIONS:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(
            log.warning(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Skipping file with unsupported extension for single frame conditioning: {input_path} "
                f"Skipping file with unsupported extension for single frame conditioning: {input_path} "
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"(expected: {_IMAGE_EXTENSIONS + _VIDEO_EXTENSIONS})"
                f"(expected: {_IMAGE_EXTENSIONS + _VIDEO_EXTENSIONS})"
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return False
            return False
    # 中文说明：根据条件选择执行分支；代码：elif num_conditional_frames == 5:
    elif num_conditional_frames == 5:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Multi-frame conditioning: only accept videos
        # Multi-frame conditioning: only accept videos
        # 中文说明：根据条件选择执行分支；代码：if ext not in _VIDEO_EXTENSIONS:
        if ext not in _VIDEO_EXTENSIONS:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(
            log.warning(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Skipping file for multi-frame conditioning (requires video): {input_path} "
                f"Skipping file for multi-frame conditioning (requires video): {input_path} "
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"(expected: {_VIDEO_EXTENSIONS}, got: {ext})"
                f"(expected: {_VIDEO_EXTENSIONS}, got: {ext})"
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return False
            return False
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.error(f"Invalid num_conditional_frames: {num_conditional_frames} (must be 1 or 5)")
        log.error(f"Invalid num_conditional_frames: {num_conditional_frames} (must be 1 or 5)")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return False
        return False

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return True
    return True


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def parse_args() -> argparse.Namespace:
def parse_args() -> argparse.Namespace:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：parser = argparse.ArgumentParser(description="Video-to-World Generation with Cosmos Predict2")
    parser = argparse.ArgumentParser(description="Video-to-World Generation with Cosmos Predict2")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--model_size",
        "--model_size",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：choices=["2B", "14B"],
        choices=["2B", "14B"],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default="2B",
        default="2B",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Size of the model to use for video-to-world generation",
        help="Size of the model to use for video-to-world generation",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--dit_path",
        "--dit_path",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type=str,
        type=str,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default="",
        default="",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Custom path to the DiT model checkpoint for post-trained models.",
        help="Custom path to the DiT model checkpoint for post-trained models.",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--prompt",
        "--prompt",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type=str,
        type=str,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default="",
        default="",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Text prompt for video generation",
        help="Text prompt for video generation",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--input_path",
        "--input_path",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type=str,
        type=str,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default="assets/video2world/input0.jpg",
        default="assets/video2world/input0.jpg",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Path to input image or video for conditioning (include file extension)",
        help="Path to input image or video for conditioning (include file extension)",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--negative_prompt",
        "--negative_prompt",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type=str,
        type=str,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default=_DEFAULT_NEGATIVE_PROMPT,
        default=_DEFAULT_NEGATIVE_PROMPT,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Negative text prompt for video-to-world generation",
        help="Negative text prompt for video-to-world generation",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--aspect_ratio",
        "--aspect_ratio",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：choices=["1:1", "4:3", "3:4", "16:9", "9:16"],
        choices=["1:1", "4:3", "3:4", "16:9", "9:16"],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default="16:9",
        default="16:9",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type=str,
        type=str,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Aspect ratio of the generated output (width:height)",
        help="Aspect ratio of the generated output (width:height)",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--num_conditional_frames",
        "--num_conditional_frames",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type=int,
        type=int,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default=1,
        default=1,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：choices=[1, 5],
        choices=[1, 5],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Number of frames to condition on (1 for single frame, 5 for multi-frame conditioning)",
        help="Number of frames to condition on (1 for single frame, 5 for multi-frame conditioning)",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--num_chunks",
        "--num_chunks",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type=int,
        type=int,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default=6,
        default=6,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Number of chunks to be generated for long video generation",
        help="Number of chunks to be generated for long video generation",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--batch_input_json",
        "--batch_input_json",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type=str,
        type=str,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default=None,
        default=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Path to JSON file containing batch inputs. Each entry should have 'input_video', 'promp...
        help="Path to JSON file containing batch inputs. Each entry should have 'input_video', 'prompt', and 'output_video' fields.",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument("--guidance", type=float, default=7, help="Guidance value")
    parser.add_argument("--guidance", type=float, default=7, help="Guidance value")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument("--seed", type=int, default=0, help="Random seed for reproducibility")
    parser.add_argument("--seed", type=int, default=0, help="Random seed for reproducibility")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--save_path",
        "--save_path",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type=str,
        type=str,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default="output/generated_video.mp4",
        default="output/generated_video.mp4",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Path to save the generated video (include file extension)",
        help="Path to save the generated video (include file extension)",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--num_gpus",
        "--num_gpus",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type=int,
        type=int,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default=1,
        default=1,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Number of GPUs to use for context parallel inference (should be a divisor of the total ...
        help="Number of GPUs to use for context parallel inference (should be a divisor of the total frames)",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument("--disable_guardrail", action="store_true", help="Disable guardrail check...
    parser.add_argument("--disable_guardrail", action="store_true", help="Disable guardrail checks on prompts")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--disable_prompt_refiner", action="store_true", help="Disable prompt refiner that enhances s...
        "--disable_prompt_refiner", action="store_true", help="Disable prompt refiner that enhances short prompts"
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return parser.parse_args()
    return parser.parse_args()


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def setup_pipeline(args: argparse.Namespace):
def setup_pipeline(args: argparse.Namespace):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Using model size: {args.model_size}")
    log.info(f"Using model size: {args.model_size}")
    # 中文说明：根据条件选择执行分支；代码：if args.model_size == "2B":
    if args.model_size == "2B":
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config = PREDICT2_VIDEO2WORLD_PIPELINE_2B
        config = PREDICT2_VIDEO2WORLD_PIPELINE_2B
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path = "checkpoints/nvidia/Cosmos-Predict2-2B-Video2World/model-720p-16fps.pt"
        dit_path = "checkpoints/nvidia/Cosmos-Predict2-2B-Video2World/model-720p-16fps.pt"
    # 中文说明：根据条件选择执行分支；代码：elif args.model_size == "14B":
    elif args.model_size == "14B":
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config = PREDICT2_VIDEO2WORLD_PIPELINE_14B
        config = PREDICT2_VIDEO2WORLD_PIPELINE_14B
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path = "checkpoints/nvidia/Cosmos-Predict2-14B-Video2World/model-720p-16fps.pt"
        dit_path = "checkpoints/nvidia/Cosmos-Predict2-14B-Video2World/model-720p-16fps.pt"
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError("Invalid model size. Choose either '2B' or '14B'.")
        raise ValueError("Invalid model size. Choose either '2B' or '14B'.")
    # 中文说明：根据条件选择执行分支；代码：if args.dit_path:
    if args.dit_path:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path = args.dit_path
        dit_path = args.dit_path

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text_encoder_path = "checkpoints/google-t5/t5-11b"
    text_encoder_path = "checkpoints/google-t5/t5-11b"

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：misc.set_random_seed(seed=args.seed, by_rank=True)
    misc.set_random_seed(seed=args.seed, by_rank=True)
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Initialize cuDNN.
    # Initialize cuDNN.
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：torch.backends.cudnn.deterministic = False
    torch.backends.cudnn.deterministic = False
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：torch.backends.cudnn.benchmark = True
    torch.backends.cudnn.benchmark = True
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Floating-point precision settings.
    # Floating-point precision settings.
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：torch.backends.cudnn.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cuda.matmul.allow_tf32 = True

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Initialize distributed environment for multi-GPU inference
    # Initialize distributed environment for multi-GPU inference
    # 中文说明：根据条件选择执行分支；代码：if args.num_gpus > 1:
    if args.num_gpus > 1:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Initializing distributed environment with {args.num_gpus} GPUs for context paralle...
        log.info(f"Initializing distributed environment with {args.num_gpus} GPUs for context parallelism")
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：distributed.init()
        distributed.init()
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parallel_state.initialize_model_parallel(context_parallel_size=args.num_gpus)
        parallel_state.initialize_model_parallel(context_parallel_size=args.num_gpus)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Context parallel group initialized with {args.num_gpus} GPUs")
        log.info(f"Context parallel group initialized with {args.num_gpus} GPUs")

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Disable guardrail if requested
    # Disable guardrail if requested
    # 中文说明：根据条件选择执行分支；代码：if args.disable_guardrail:
    if args.disable_guardrail:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning("Guardrail checks are disabled")
        log.warning("Guardrail checks are disabled")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config.guardrail_config.enabled = False
        config.guardrail_config.enabled = False

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Disable prompt refiner if requested
    # Disable prompt refiner if requested
    # 中文说明：根据条件选择执行分支；代码：if args.disable_prompt_refiner:
    if args.disable_prompt_refiner:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning("Prompt refiner is disabled")
        log.warning("Prompt refiner is disabled")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config.prompt_refiner_config.enabled = False
        config.prompt_refiner_config.enabled = False

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Load models
    # Load models
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Initializing Video2WorldPipeline with model size: {args.model_size}")
    log.info(f"Initializing Video2WorldPipeline with model size: {args.model_size}")
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe = Video2WorldPipeline.from_config(
    pipe = Video2WorldPipeline.from_config(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config=config,
        config=config,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path=dit_path,
        dit_path=dit_path,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text_encoder_path=text_encoder_path,
        text_encoder_path=text_encoder_path,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：device="cuda",
        device="cuda",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：torch_dtype=torch.bfloat16,
        torch_dtype=torch.bfloat16,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：load_prompt_refiner=True,
        load_prompt_refiner=True,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return pipe
    return pipe


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def process_single_generation(
def process_single_generation(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pipe: Video2WorldPipeline,
    pipe: Video2WorldPipeline,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：input_path: str,
    input_path: str,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：prompt: str,
    prompt: str,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：output_path: str,
    output_path: str,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：negative_prompt: str,
    negative_prompt: str,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：aspect_ratio: str,
    aspect_ratio: str,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_conditional_frames: int,
    num_conditional_frames: int,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_chunks: int,
    num_chunks: int,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：guidance: float,
    guidance: float,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：seed: int,
    seed: int,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> bool:
) -> bool:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Validate input file
    # Validate input file
    # 中文说明：根据条件选择执行分支；代码：if not validate_input_file(input_path, num_conditional_frames):
    if not validate_input_file(input_path, num_conditional_frames):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(f"Input file validation failed: {input_path}")
        log.warning(f"Input file validation failed: {input_path}")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return False
        return False

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Running Video2WorldPipeline\ninput: {input_path}\nprompt: {prompt}")
    log.info(f"Running Video2WorldPipeline\ninput: {input_path}\nprompt: {prompt}")

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：all_chunks = []
    all_chunks = []
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：current_input_path = input_path
    current_input_path = input_path

    # 中文说明：处理异常、清理资源或管理上下文；代码：with tempfile.TemporaryDirectory() as tmpdir:
    with tempfile.TemporaryDirectory() as tmpdir:
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for chunk_id in tqdm(range(num_chunks)):
        for chunk_id in tqdm(range(num_chunks)):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Generating chunk {chunk_id + 1}/{num_chunks}...")
            log.info(f"Generating chunk {chunk_id + 1}/{num_chunks}...")

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = pipe(
            video = pipe(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prompt=prompt,
                prompt=prompt,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：negative_prompt=negative_prompt,
                negative_prompt=negative_prompt,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：aspect_ratio=aspect_ratio,
                aspect_ratio=aspect_ratio,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_path=current_input_path,
                input_path=current_input_path,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_conditional_frames=num_conditional_frames,
                num_conditional_frames=num_conditional_frames,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：guidance=guidance,
                guidance=guidance,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：seed=seed + chunk_id, # change random seed to avoid repeat
                seed=seed + chunk_id,  # change random seed to avoid repeat
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# for the first chunk, we save the whole clip
            # for the first chunk, we save the whole clip
            # 中文说明：根据条件选择执行分支；代码：if chunk_id == 0:
            if chunk_id == 0:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：chunk = video
                chunk = video
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：chunk = video[:, :, num_conditional_frames:, :, :]
                chunk = video[:, :, num_conditional_frames:, :, :]
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：all_chunks.append(chunk.cpu())
            all_chunks.append(chunk.cpu())

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Prepare for next chunk: use last `num_conditional_frames` frames as new condition
            # Prepare for next chunk: use last `num_conditional_frames` frames as new condition
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：last_frames = video[:, :, -num_conditional_frames:, :, :] # (1, C, num_conditional_frames, H, W)
            last_frames = video[:, :, -num_conditional_frames:, :, :]  # (1, C, num_conditional_frames, H, W)
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# if num_conditional_frames is 1, save as image temp file
            # if num_conditional_frames is 1, save as image temp file
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# otherwise, save as video temp file
            # otherwise, save as video temp file
            # 中文说明：根据条件选择执行分支；代码：if num_conditional_frames == 1:
            if num_conditional_frames == 1:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：last_frames_path = os.path.join(tmpdir, f"chunk{chunk_id}_overlap.png")
                last_frames_path = os.path.join(tmpdir, f"chunk{chunk_id}_overlap.png")
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：last_frames_path = os.path.join(tmpdir, f"chunk{chunk_id}_overlap.mp4")
                last_frames_path = os.path.join(tmpdir, f"chunk{chunk_id}_overlap.mp4")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：save_image_or_video(last_frames, last_frames_path, fps=16)
            save_image_or_video(last_frames, last_frames_path, fps=16)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：current_input_path = last_frames_path
            current_input_path = last_frames_path

    # 中文说明：根据条件选择执行分支；代码：if len(all_chunks) > 0:
    if len(all_chunks) > 0:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Concatenate all chunks along time
        # Concatenate all chunks along time
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = torch.cat(all_chunks, dim=2)
        video = torch.cat(all_chunks, dim=2)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# save the generated video
        # save the generated video
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_dir = os.path.dirname(output_path)
        output_dir = os.path.dirname(output_path)
        # 中文说明：根据条件选择执行分支；代码：if output_dir:
        if output_dir:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.makedirs(output_dir, exist_ok=True)
            os.makedirs(output_dir, exist_ok=True)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Saving generated video to: {output_path}")
        log.info(f"Saving generated video to: {output_path}")
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：save_image_or_video(video, output_path, fps=16)
        save_image_or_video(video, output_path, fps=16)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.success(f"Successfully saved video to: {output_path}")
        log.success(f"Successfully saved video to: {output_path}")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return True
        return True
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return False
    return False


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def generate_video(args: argparse.Namespace, pipe: Video2WorldPipeline) -> None:
def generate_video(args: argparse.Namespace, pipe: Video2WorldPipeline) -> None:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Video-to-World
    # Video-to-World
    # 中文说明：根据条件选择执行分支；代码：if args.batch_input_json is not None:
    if args.batch_input_json is not None:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Process batch inputs from JSON file
        # Process batch inputs from JSON file
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Loading batch inputs from JSON file: {args.batch_input_json}")
        log.info(f"Loading batch inputs from JSON file: {args.batch_input_json}")
        # 中文说明：处理异常、清理资源或管理上下文；代码：with open(args.batch_input_json, "r") as f:
        with open(args.batch_input_json, "r") as f:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch_inputs = json.load(f)
            batch_inputs = json.load(f)

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for idx, item in enumerate(tqdm(batch_inputs)):
        for idx, item in enumerate(tqdm(batch_inputs)):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_video = item.get("input_video", "")
            input_video = item.get("input_video", "")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prompt = item.get("prompt", "")
            prompt = item.get("prompt", "")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_video = item.get("output_video", f"output_{idx}.mp4")
            output_video = item.get("output_video", f"output_{idx}.mp4")

            # 中文说明：根据条件选择执行分支；代码：if not input_video or not prompt:
            if not input_video or not prompt:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(f"Skipping item {idx}: Missing input_video or prompt")
                log.warning(f"Skipping item {idx}: Missing input_video or prompt")
                # 中文说明：执行循环控制或空操作；代码：continue
                continue

            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：process_single_generation(
            process_single_generation(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe=pipe,
                pipe=pipe,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_path=input_video,
                input_path=input_video,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prompt=prompt,
                prompt=prompt,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_path=output_video,
                output_path=output_video,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：negative_prompt=args.negative_prompt,
                negative_prompt=args.negative_prompt,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：aspect_ratio=args.aspect_ratio,
                aspect_ratio=args.aspect_ratio,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_conditional_frames=args.num_conditional_frames,
                num_conditional_frames=args.num_conditional_frames,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_chunks=args.num_chunks,
                num_chunks=args.num_chunks,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：guidance=args.guidance,
                guidance=args.guidance,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：seed=args.seed,
                seed=args.seed,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：process_single_generation(
        process_single_generation(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe=pipe,
            pipe=pipe,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_path=args.input_path,
            input_path=args.input_path,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prompt=args.prompt,
            prompt=args.prompt,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_path=args.save_path,
            output_path=args.save_path,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：negative_prompt=args.negative_prompt,
            negative_prompt=args.negative_prompt,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：aspect_ratio=args.aspect_ratio,
            aspect_ratio=args.aspect_ratio,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_conditional_frames=args.num_conditional_frames,
            num_conditional_frames=args.num_conditional_frames,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_chunks=args.num_chunks,
            num_chunks=args.num_chunks,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：guidance=args.guidance,
            guidance=args.guidance,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：seed=args.seed,
            seed=args.seed,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return
    return


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def cleanup_distributed():
def cleanup_distributed():
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Clean up the distributed environment if initialized."""
    """Clean up the distributed environment if initialized."""
    # 中文说明：根据条件选择执行分支；代码：if parallel_state.is_initialized():
    if parallel_state.is_initialized():
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parallel_state.destroy_model_parallel()
        parallel_state.destroy_model_parallel()
        # 中文说明：根据条件选择执行分支；代码：if torch.distributed.is_initialized():
        if torch.distributed.is_initialized():
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.distributed.destroy_process_group()
            torch.distributed.destroy_process_group()


# 中文说明：根据条件选择执行分支；代码：if __name__ == "__main__":
if __name__ == "__main__":
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：args = parse_args()
    args = parse_args()
    # 中文说明：开始一个可捕获异常的代码块；代码：try:
    try:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe = setup_pipeline(args)
        pipe = setup_pipeline(args)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：generate_video(args, pipe)
        generate_video(args, pipe)
    # 中文说明：处理异常、清理资源或管理上下文；代码：finally:
    finally:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Make sure to clean up the distributed environment
        # Make sure to clean up the distributed environment
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cleanup_distributed()
        cleanup_distributed()
