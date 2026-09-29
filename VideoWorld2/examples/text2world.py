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

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.distributed
import torch.distributed

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.pipelines.text2image import Text2ImagePipeline
from videoworld2.pipelines.text2image import Text2ImagePipeline
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.pipelines.video2world import Video2WorldPipeline
from videoworld2.pipelines.video2world import Video2WorldPipeline

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Import functionality from other example scripts
# Import functionality from other example scripts
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from examples.text2image import process_single_generation as process_single_image_generation
from examples.text2image import process_single_generation as process_single_image_generation
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from examples.text2image import setup_pipeline as setup_text2image_pipeline
from examples.text2image import setup_pipeline as setup_text2image_pipeline
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from examples.video2world import _DEFAULT_NEGATIVE_PROMPT, cleanup_distributed
from examples.video2world import _DEFAULT_NEGATIVE_PROMPT, cleanup_distributed
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from examples.video2world import process_single_generation as process_single_video_generation
from examples.video2world import process_single_generation as process_single_video_generation
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from examples.video2world import setup_pipeline as setup_video2world_pipeline
from examples.video2world import setup_pipeline as setup_video2world_pipeline
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_DEFAULT_POSITIVE_PROMPT = "An autonomous welding robot arm operating inside a modern automot...
_DEFAULT_POSITIVE_PROMPT = "An autonomous welding robot arm operating inside a modern automotive factory, sparks flying as it welds a car frame with precision under bright overhead lights."


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def parse_args() -> argparse.Namespace:
def parse_args() -> argparse.Namespace:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：parser = argparse.ArgumentParser(description="Text to World Generation with Cosmos Predict2")
    parser = argparse.ArgumentParser(description="Text to World Generation with Cosmos Predict2")
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Common arguments between text2image and video2world
    # Common arguments between text2image and video2world
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--model_size",
        "--model_size",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：choices=["2B", "14B"],
        choices=["2B", "14B"],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default="2B",
        default="2B",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Size of the model to use for text2world generation",
        help="Size of the model to use for text2world generation",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument("--prompt", type=str, default=_DEFAULT_POSITIVE_PROMPT, help="Text prompt...
    parser.add_argument("--prompt", type=str, default=_DEFAULT_POSITIVE_PROMPT, help="Text prompt for generation")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--batch_input_json",
        "--batch_input_json",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type=str,
        type=str,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default=None,
        default=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Path to JSON file containing batch inputs. Each entry should have 'prompt' and 'output_...
        help="Path to JSON file containing batch inputs. Each entry should have 'prompt' and 'output_video' fields.",
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
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Negative text prompt for video2world generation",
        help="Negative text prompt for video2world generation",
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
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument("--disable_guardrail", action="store_true", help="Disable guardrail check...
    parser.add_argument("--disable_guardrail", action="store_true", help="Disable guardrail checks on prompts")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--num_gpus",
        "--num_gpus",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type=int,
        type=int,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default=1,
        default=1,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Number of GPUs to use for context parallel inference for both text2image and video2worl...
        help="Number of GPUs to use for context parallel inference for both text2image and video2world parts",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--benchmark",
        "--benchmark",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：action="store_true",
        action="store_true",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Run the generation in benchmark mode. It means that generation will be rerun a few time...
        help="Run the generation in benchmark mode. It means that generation will be rerun a few times and the average generation time will be shown.",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Text2image specific arguments
    # Text2image specific arguments
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument("--use_cuda_graphs", action="store_true", help="Use CUDA Graphs for the t...
    parser.add_argument("--use_cuda_graphs", action="store_true", help="Use CUDA Graphs for the text2image inference.")

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Video2world specific arguments
    # Video2world specific arguments
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--resolution",
        "--resolution",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：choices=["480", "720"],
        choices=["480", "720"],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default="720",
        default="720",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type=str,
        type=str,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Resolution of the model to use for video-to-world generation",
        help="Resolution of the model to use for video-to-world generation",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--fps",
        "--fps",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：choices=[10, 16],
        choices=[10, 16],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default=16,
        default=16,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type=int,
        type=int,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="FPS of the model to use for video-to-world generation",
        help="FPS of the model to use for video-to-world generation",
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
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument("--guidance", type=float, default=7, help="Guidance value for video gener...
    parser.add_argument("--guidance", type=float, default=7, help="Guidance value for video generation")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument("--offload_guardrail", action="store_true", help="Offload guardrail to CP...
    parser.add_argument("--offload_guardrail", action="store_true", help="Offload guardrail to CPU to save GPU memory")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--disable_prompt_refiner", action="store_true", help="Disable prompt refiner that enhances s...
        "--disable_prompt_refiner", action="store_true", help="Disable prompt refiner that enhances short prompts"
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--offload_prompt_refiner", action="store_true", help="Offload prompt refiner to CPU to save ...
        "--offload_prompt_refiner", action="store_true", help="Offload prompt refiner to CPU to save GPU memory"
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return parser.parse_args()
    return parser.parse_args()


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def generate_first_frames(text2image_pipe: Text2ImagePipeline, args: argparse.Namespace) -> l...
def generate_first_frames(text2image_pipe: Text2ImagePipeline, args: argparse.Namespace) -> list:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Generate first frames using the text2image pipeline.
    Returns a list of batch items containing prompt, output video path, and temp image path.
    """
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from megatron.core import parallel_state
    from megatron.core import parallel_state

    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.distributed import barrier, get_rank
    from imaginaire.utils.distributed import barrier, get_rank

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch_items = []
    batch_items = []

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Check if we're in a multi-GPU distributed environment
    # Check if we're in a multi-GPU distributed environment
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_distributed = parallel_state.is_initialized() and torch.distributed.is_initialized()
    is_distributed = parallel_state.is_initialized() and torch.distributed.is_initialized()
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank = get_rank() if is_distributed else 0
    rank = get_rank() if is_distributed else 0

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Only rank 0 should run text2image generation to avoid OOM when CP is disabled
    # Only rank 0 should run text2image generation to avoid OOM when CP is disabled
    # 中文说明：根据条件选择执行分支；代码：if rank == 0 and text2image_pipe is not None:
    if rank == 0 and text2image_pipe is not None:
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

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Generate all the first frames first
            # Generate all the first frames first
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for idx, item in enumerate(batch_inputs):
            for idx, item in enumerate(batch_inputs):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Generating first frame {idx + 1}/{len(batch_inputs)}")
                log.info(f"Generating first frame {idx + 1}/{len(batch_inputs)}")
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prompt = item.get("prompt", "")
                prompt = item.get("prompt", "")
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_video = item.get("output_video", f"output_{idx}.mp4")
                output_video = item.get("output_video", f"output_{idx}.mp4")

                # 中文说明：根据条件选择执行分支；代码：if not prompt:
                if not prompt:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(f"Skipping item {idx}: Missing prompt")
                    log.warning(f"Skipping item {idx}: Missing prompt")
                    # 中文说明：执行循环控制或空操作；代码：continue
                    continue

                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Save the generated first frame with a temporary name based on the output video path
                # Save the generated first frame with a temporary name based on the output video path
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temp_image_name = os.path.splitext(output_video)[0] + "_temp.jpg"
                temp_image_name = os.path.splitext(output_video)[0] + "_temp.jpg"

                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Use the imported process_single_image_generation function
                # Use the imported process_single_image_generation function
                # 中文说明：根据条件选择执行分支；代码：if process_single_image_generation(
                if process_single_image_generation(
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe=text2image_pipe,
                    pipe=text2image_pipe,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prompt=prompt,
                    prompt=prompt,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_path=temp_image_name,
                    output_path=temp_image_name,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：negative_prompt=args.negative_prompt,
                    negative_prompt=args.negative_prompt,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：aspect_ratio=args.aspect_ratio,
                    aspect_ratio=args.aspect_ratio,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：seed=args.seed,
                    seed=args.seed,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_cuda_graphs=args.use_cuda_graphs,
                    use_cuda_graphs=args.use_cuda_graphs,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：benchmark=args.benchmark,
                    benchmark=args.benchmark,
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
                ):
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Save the item for the second stage
                    # Save the item for the second stage
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：batch_items.append(
                    batch_items.append(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"prompt": prompt, "output_video": output_video, "temp_image_path": temp_image_name}
                        {"prompt": prompt, "output_video": output_video, "temp_image_path": temp_image_name}
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Single item processing
            # Single item processing
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temp_image_path = os.path.splitext(args.save_path)[0] + "_temp.jpg"
            temp_image_path = os.path.splitext(args.save_path)[0] + "_temp.jpg"

            # 中文说明：根据条件选择执行分支；代码：if args.use_cuda_graphs:
            if args.use_cuda_graphs:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(
                log.warning(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："Using CUDA Graphs for a single inference call may not be beneficial because of overhead of G...
                    "Using CUDA Graphs for a single inference call may not be beneficial because of overhead of Graphs creation."
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Use the imported process_single_image_generation function
            # Use the imported process_single_image_generation function
            # 中文说明：根据条件选择执行分支；代码：if process_single_image_generation(
            if process_single_image_generation(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe=text2image_pipe,
                pipe=text2image_pipe,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prompt=args.prompt,
                prompt=args.prompt,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_path=temp_image_path,
                output_path=temp_image_path,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：negative_prompt=args.negative_prompt,
                negative_prompt=args.negative_prompt,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：aspect_ratio=args.aspect_ratio,
                aspect_ratio=args.aspect_ratio,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：seed=args.seed,
                seed=args.seed,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_cuda_graphs=args.use_cuda_graphs,
                use_cuda_graphs=args.use_cuda_graphs,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：benchmark=args.benchmark,
                benchmark=args.benchmark,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
            ):
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Add single item to batch_items for consistent processing
                # Add single item to batch_items for consistent processing
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：batch_items.append(
                batch_items.append(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"prompt": args.prompt, "output_video": args.save_path, "temp_image_path": temp_image_path}
                    {"prompt": args.prompt, "output_video": args.save_path, "temp_image_path": temp_image_path}
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Rank 0: Generated {len(batch_items)} first frames")
        log.info(f"Rank 0: Generated {len(batch_items)} first frames")
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Non-rank-0 processes: just wait for broadcast
        # Non-rank-0 processes: just wait for broadcast
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Rank {rank}: Waiting for batch_items from rank 0")
        log.info(f"Rank {rank}: Waiting for batch_items from rank 0")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch_items = [] # Initialize empty list for non-rank-0 processes
        batch_items = []  # Initialize empty list for non-rank-0 processes

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Broadcast batch_items from rank 0 to all other ranks using PyTorch's broadcast_object_list
    # Broadcast batch_items from rank 0 to all other ranks using PyTorch's broadcast_object_list
    # 中文说明：根据条件选择执行分支；代码：if is_distributed:
    if is_distributed:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch_items_list = [batch_items] # Wrap in list for broadcast_object_list
        batch_items_list = [batch_items]  # Wrap in list for broadcast_object_list
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.distributed.broadcast_object_list(batch_items_list, src=0)
        torch.distributed.broadcast_object_list(batch_items_list, src=0)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch_items = batch_items_list[0] # Extract the broadcasted list
        batch_items = batch_items_list[0]  # Extract the broadcasted list

        # 中文说明：根据条件选择执行分支；代码：if rank != 0:
        if rank != 0:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Rank {rank}: Received {len(batch_items)} batch items from rank 0")
            log.info(f"Rank {rank}: Received {len(batch_items)} batch items from rank 0")

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：barrier()
        barrier()
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Rank {rank}: Synchronized after batch_items broadcast")
        log.info(f"Rank {rank}: Synchronized after batch_items broadcast")

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return batch_items
    return batch_items


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def generate_videos(video2world_pipe: Video2WorldPipeline, batch_items: list, args: argparse....
def generate_videos(video2world_pipe: Video2WorldPipeline, batch_items: list, args: argparse.Namespace) -> None:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Generate videos from first frames using the video2world pipeline.
    """
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Process all items for video generation
    # Process all items for video generation
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for idx, item in enumerate(batch_items):
    for idx, item in enumerate(batch_items):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Generating video from first frame {idx + 1}/{len(batch_items)}")
        log.info(f"Generating video from first frame {idx + 1}/{len(batch_items)}")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prompt = item["prompt"]
        prompt = item["prompt"]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_video = item["output_video"]
        output_video = item["output_video"]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temp_image_path = item["temp_image_path"]
        temp_image_path = item["temp_image_path"]

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Use the imported process_single_video_generation function
        # Use the imported process_single_video_generation function
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：process_single_video_generation(
        process_single_video_generation(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe=video2world_pipe,
            pipe=video2world_pipe,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_path=temp_image_path,
            input_path=temp_image_path,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prompt=prompt,
            prompt=prompt,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_path=output_video,
            output_path=output_video,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：negative_prompt=args.negative_prompt,
            negative_prompt=args.negative_prompt,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：aspect_ratio=args.aspect_ratio,
            aspect_ratio=args.aspect_ratio,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_conditional_frames=1, # Always use 1 frame for text2world
            num_conditional_frames=1,  # Always use 1 frame for text2world
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：guidance=args.guidance,
            guidance=args.guidance,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：seed=args.seed,
            seed=args.seed,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：benchmark=args.benchmark,
            benchmark=args.benchmark,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_cuda_graphs=args.use_cuda_graphs,
            use_cuda_graphs=args.use_cuda_graphs,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Clean up the temporary image file
        # Clean up the temporary image file
        # 中文说明：根据条件选择执行分支；代码：if os.path.exists(temp_image_path):
        if os.path.exists(temp_image_path):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.remove(temp_image_path)
            os.remove(temp_image_path)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.success(f"Cleaned up temporary image: {temp_image_path}")
            log.success(f"Cleaned up temporary image: {temp_image_path}")


# 中文说明：根据条件选择执行分支；代码：if __name__ == "__main__":
if __name__ == "__main__":
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：args = parse_args()
    args = parse_args()
    # 中文说明：开始一个可捕获异常的代码块；代码：try:
    try:
        # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from megatron.core import parallel_state
        from megatron.core import parallel_state

        # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.distributed import get_rank
        from imaginaire.utils.distributed import get_rank

        # 中文说明：根据条件选择执行分支；代码：if args.benchmark:
        if args.benchmark:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(
            log.warning(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："Running in benchmark mode. Each generation will be rerun a couple of times and the average g...
                "Running in benchmark mode. Each generation will be rerun a couple of times and the average generation time will be shown."
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Check if we're in a multi-GPU distributed environment
        # Check if we're in a multi-GPU distributed environment
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_distributed = parallel_state.is_initialized() and torch.distributed.is_initialized()
        is_distributed = parallel_state.is_initialized() and torch.distributed.is_initialized()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank = get_rank() if is_distributed else 0
        rank = get_rank() if is_distributed else 0

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Step 1: Initialize text2image pipeline and generate all first frames
        # Step 1: Initialize text2image pipeline and generate all first frames
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Only rank 0 initializes the text2image pipeline to avoid OOM
        # Only rank 0 initializes the text2image pipeline to avoid OOM
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text2image_pipe = None
        text2image_pipe = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text_encoder = None
        text_encoder = None

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("Step 1: Initializing text2image pipeline...")
        log.info("Step 1: Initializing text2image pipeline...")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text2image_pipe = setup_text2image_pipeline(args)
        text2image_pipe = setup_text2image_pipeline(args)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Handle the case where setup_text2image_pipeline returns None for non-rank-0 processes
        # Handle the case where setup_text2image_pipeline returns None for non-rank-0 processes
        # 中文说明：根据条件选择执行分支；代码：if text2image_pipe is not None:
        if text2image_pipe is not None:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Store text encoder for later use (only on rank 0)
            # Store text encoder for later use (only on rank 0)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text_encoder = text2image_pipe.text_encoder
            text_encoder = text2image_pipe.text_encoder
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("Rank 0: Text2image pipeline initialized successfully")
            log.info("Rank 0: Text2image pipeline initialized successfully")
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Non-rank-0 processes get None
            # Non-rank-0 processes get None
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text_encoder = None
            text_encoder = None
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Rank {rank}: Text2image pipeline setup returned None (expected for non-rank-0)")
            log.info(f"Rank {rank}: Text2image pipeline setup returned None (expected for non-rank-0)")

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Generate first frames (only rank 0 does actual generation)
        # Generate first frames (only rank 0 does actual generation)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("Step 1: Generating first frames...")
        log.info("Step 1: Generating first frames...")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch_items = generate_first_frames(text2image_pipe, args)
        batch_items = generate_first_frames(text2image_pipe, args)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Clean up text2image pipeline on rank 0
        # Clean up text2image pipeline on rank 0
        # 中文说明：根据条件选择执行分支；代码：if text2image_pipe is not None:
        if text2image_pipe is not None:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("Step 1 complete. Cleaning up text2image pipeline to free memory...")
            log.info("Step 1 complete. Cleaning up text2image pipeline to free memory...")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del text2image_pipe
            del text2image_pipe
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.empty_cache()
            torch.cuda.empty_cache()

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Step 2: Initialize video2world pipeline and generate videos
        # Step 2: Initialize video2world pipeline and generate videos
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("Step 2: Initializing video2world pipeline...")
        log.info("Step 2: Initializing video2world pipeline...")

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# For non-rank-0 processes, let video2world create its own text encoder
        # For non-rank-0 processes, let video2world create its own text encoder
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# This avoids the complexity of broadcasting the text encoder object across ranks
        # This avoids the complexity of broadcasting the text encoder object across ranks
        # 中文说明：根据条件选择执行分支；代码：if is_distributed and rank != 0:
        if is_distributed and rank != 0:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text_encoder = None
            text_encoder = None
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Rank {rank}: Will create new text encoder for video2world pipeline")
            log.info(f"Rank {rank}: Will create new text encoder for video2world pipeline")

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Pass all video2world relevant arguments and the text encoder
        # Pass all video2world relevant arguments and the text encoder
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video2world_pipe = setup_video2world_pipeline(args, text_encoder=text_encoder)
        video2world_pipe = setup_video2world_pipeline(args, text_encoder=text_encoder)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Generate videos
        # Generate videos
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("Step 2: Generating videos from first frames...")
        log.info("Step 2: Generating videos from first frames...")
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：generate_videos(video2world_pipe, batch_items, args)
        generate_videos(video2world_pipe, batch_items, args)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Clean up video2world pipeline
        # Clean up video2world pipeline
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("All done. Cleaning up video2world pipeline...")
        log.info("All done. Cleaning up video2world pipeline...")
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del video2world_pipe
        del video2world_pipe
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.empty_cache()
        torch.cuda.empty_cache()

    # 中文说明：处理异常、清理资源或管理上下文；代码：finally:
    finally:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Make sure to clean up the distributed environment
        # Make sure to clean up the distributed environment
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cleanup_distributed()
        cleanup_distributed()
