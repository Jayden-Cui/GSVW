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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import pdb
import pdb

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import mediapy as mp
import mediapy as mp
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Set TOKENIZERS_PARALLELISM environment variable to avoid deadlocks with multiprocessing
# Set TOKENIZERS_PARALLELISM environment variable to avoid deadlocks with multiprocessing
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from megatron.core import parallel_state
from megatron.core import parallel_state

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.configs.action_conditioned.config_action_conditioned import (
from videoworld2.configs.action_conditioned.config_action_conditioned import (
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ACTION_CONDITIONED_PREDICT2_VIDEO2WORLD_PIPELINE_2B,
    ACTION_CONDITIONED_PREDICT2_VIDEO2WORLD_PIPELINE_2B,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.pipelines.action_video2world import ActionConditionedVideo2WorldPipeline
from videoworld2.pipelines.action_video2world import ActionConditionedVideo2WorldPipeline
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import distributed, log, misc
from imaginaire.utils import distributed, log, misc
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.io import save_image_or_video
from imaginaire.utils.io import save_image_or_video


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_action_sequence(annotation_path):
def get_action_sequence(annotation_path):
    # 中文说明：处理异常、清理资源或管理上下文；代码：with open(annotation_path, "r") as file:
    with open(annotation_path, "r") as file:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data = json.load(file)
        data = json.load(file)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# rescale the action to the original scale
    # rescale the action to the original scale
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：action_ee = np.array(data["action"])[:, :6] * 20
    action_ee = np.array(data["action"])[:, :6] * 20
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gripper = np.array(data["continuous_gripper_state"])[1:, None]
    gripper = np.array(data["continuous_gripper_state"])[1:, None]

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# concatenate the end-effector displacement and gripper width
    # concatenate the end-effector displacement and gripper width
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：action = np.concatenate([action_ee, gripper], axis=1)
    action = np.concatenate([action_ee, gripper], axis=1)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return action
    return action


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def parse_args() -> argparse.Namespace:
def parse_args() -> argparse.Namespace:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：parser = argparse.ArgumentParser(description="Video-to-World Generation with Cosmos Predict2")
    parser = argparse.ArgumentParser(description="Video-to-World Generation with Cosmos Predict2")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--model_size",
        "--model_size",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：choices=["2B"],
        choices=["2B"],
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
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--input_video",
        "--input_video",
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
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--input_annotation",
        "--input_annotation",
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
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--num_conditional_frames",
        "--num_conditional_frames",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type=int,
        type=int,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default=1,
        default=1,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：choices=[1],
        choices=[1],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Number of frames to condition on (1 for single frame, 5 for multi-frame conditioning)",
        help="Number of frames to condition on (1 for single frame, 5 for multi-frame conditioning)",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--chunk_size",
        "--chunk_size",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type=int,
        type=int,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default=12,
        default=12,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Chunk size",
        help="Chunk size",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument("--autoregressive", action="store_true", help="Use autoregressive mode")
    parser.add_argument("--autoregressive", action="store_true", help="Use autoregressive mode")
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
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config = ACTION_CONDITIONED_PREDICT2_VIDEO2WORLD_PIPELINE_2B
        config = ACTION_CONDITIONED_PREDICT2_VIDEO2WORLD_PIPELINE_2B
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path = "checkpoints/nvidia/Cosmos-Predict2-2B-Sample-Action-Conditioned/model-480p-4fps.pth"
        dit_path = "checkpoints/nvidia/Cosmos-Predict2-2B-Sample-Action-Conditioned/model-480p-4fps.pth"
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError("Invalid model size. Choose either '2B' or '14B'.")
        raise ValueError("Invalid model size. Choose either '2B' or '14B'.")
    # 中文说明：根据条件选择执行分支；代码：if hasattr(args, "dit_path") and args.dit_path:
    if hasattr(args, "dit_path") and args.dit_path:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path = args.dit_path
        dit_path = args.dit_path

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# text_encoder_path = "checkpoints/google-t5/t5-11b"
    # text_encoder_path = "checkpoints/google-t5/t5-11b"
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text_encoder_path = ""
    text_encoder_path = ""

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
    # 中文说明：根据条件选择执行分支；代码：if hasattr(args, "num_gpus") and args.num_gpus > 1:
    if hasattr(args, "num_gpus") and args.num_gpus > 1:
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
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe = ActionConditionedVideo2WorldPipeline.from_config(
    pipe = ActionConditionedVideo2WorldPipeline.from_config(
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


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def read_first_frame(video_path):
def read_first_frame(video_path):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = mp.read_video(video_path) # Returns (T, H, W, C) numpy array
    video = mp.read_video(video_path)  # Returns (T, H, W, C) numpy array
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return video[0] # Return first frame as numpy array
    return video[0]  # Return first frame as numpy array


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def process_single_generation(
def process_single_generation(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pipe, input_path, input_annotation, output_path, guidance, seed, chunk_size, autoregressive
    pipe, input_path, input_annotation, output_path, guidance, seed, chunk_size, autoregressive
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：actions = get_action_sequence(input_annotation)
    actions = get_action_sequence(input_annotation)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：first_frame = read_first_frame(input_path)
    first_frame = read_first_frame(input_path)

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Running Video2WorldPipeline\ninput: {input_path}")
    log.info(f"Running Video2WorldPipeline\ninput: {input_path}")

    # 中文说明：根据条件选择执行分支；代码：if autoregressive:
    if autoregressive:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("Using autoregressive mode")
        log.info("Using autoregressive mode")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_chunks = []
        video_chunks = []
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i in range(0, len(actions), chunk_size):
        for i in range(0, len(actions), chunk_size):
            # 中文说明：根据条件选择执行分支；代码：if actions[i : i + chunk_size].shape[0] < chunk_size:
            if actions[i : i + chunk_size].shape[0] < chunk_size:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("Reached end of actions")
                log.info("Reached end of actions")
                # 中文说明：执行循环控制或空操作；代码：break
                break
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = pipe(
            video = pipe(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：first_frame,
                first_frame,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：actions[i : i + chunk_size],
                actions[i : i + chunk_size],
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_conditional_frames=1,
                num_conditional_frames=1,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：guidance=guidance,
                guidance=guidance,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：seed=i,
                seed=i,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：first_frame = ((video[0, :, -1].permute(1, 2, 0).cpu().numpy() / 2 + 0.5).clip(0, 1) * 255).a...
            first_frame = ((video[0, :, -1].permute(1, 2, 0).cpu().numpy() / 2 + 0.5).clip(0, 1) * 255).astype(np.uint8)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video_chunks.append(video)
            video_chunks.append(video)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = torch.cat([video_chunks[0]] + [chunk[:, :, :-1] for chunk in video_chunks[1:]], dim=2)
        video = torch.cat([video_chunks[0]] + [chunk[:, :, :-1] for chunk in video_chunks[1:]], dim=2)
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = pipe(
        video = pipe(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：first_frame,
            first_frame,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：actions[:chunk_size],
            actions[:chunk_size],
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_conditional_frames=1,
            num_conditional_frames=1,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：guidance=guidance,
            guidance=guidance,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：seed=seed,
            seed=seed,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：根据条件选择执行分支；代码：if video is not None:
    if video is not None:
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
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：save_image_or_video(video, output_path, fps=4)
        save_image_or_video(video, output_path, fps=4)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.success(f"Successfully saved video to: {output_path}")
        log.success(f"Successfully saved video to: {output_path}")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return True
        return True
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return False
    return False


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def generate_video(args: argparse.Namespace, pipe: ActionConditionedVideo2WorldPipeline) -> N...
def generate_video(args: argparse.Namespace, pipe: ActionConditionedVideo2WorldPipeline) -> None:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：process_single_generation(
    process_single_generation(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe=pipe,
        pipe=pipe,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_path=args.input_video,
        input_path=args.input_video,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_annotation=args.input_annotation,
        input_annotation=args.input_annotation,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_path=args.save_path,
        output_path=args.save_path,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：guidance=args.guidance,
        guidance=args.guidance,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：seed=args.seed,
        seed=args.seed,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：chunk_size=args.chunk_size,
        chunk_size=args.chunk_size,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：autoregressive=args.autoregressive,
        autoregressive=args.autoregressive,
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
