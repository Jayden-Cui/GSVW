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

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import time
import time

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from megatron.core import parallel_state
from megatron.core import parallel_state

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.configs.base.config_text2image import (
from videoworld2.configs.base.config_text2image import (
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：PREDICT2_TEXT2IMAGE_PIPELINE_2B,
    PREDICT2_TEXT2IMAGE_PIPELINE_2B,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：PREDICT2_TEXT2IMAGE_PIPELINE_14B,
    PREDICT2_TEXT2IMAGE_PIPELINE_14B,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.pipelines.text2image import Text2ImagePipeline
from videoworld2.pipelines.text2image import Text2ImagePipeline
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import distributed, log, misc
from imaginaire.utils import distributed, log, misc
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.io import save_image_or_video
from imaginaire.utils.io import save_image_or_video

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_DEFAULT_POSITIVE_PROMPT = "A well-worn broom sweeps across a dusty wooden floor, its bristle...
_DEFAULT_POSITIVE_PROMPT = "A well-worn broom sweeps across a dusty wooden floor, its bristles gathering crumbs and flecks of debris in swift, rhythmic strokes. Dust motes dance in the sunbeams filtering through the window, glowing momentarily before settling. The quiet swish of straw brushing wood is interrupted only by the occasional creak of old floorboards. With each pass, the floor grows cleaner, restoring a sense of quiet order to the humble room."


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def parse_args() -> argparse.Namespace:
def parse_args() -> argparse.Namespace:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：parser = argparse.ArgumentParser(description="Text to Image Generation with Cosmos Predict2")
    parser = argparse.ArgumentParser(description="Text to Image Generation with Cosmos Predict2")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--model_size",
        "--model_size",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：choices=["2B", "14B"],
        choices=["2B", "14B"],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default="2B",
        default="2B",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Size of the model to use for text-to-image generation",
        help="Size of the model to use for text-to-image generation",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument("--prompt", type=str, default=_DEFAULT_POSITIVE_PROMPT, help="Text prompt...
    parser.add_argument("--prompt", type=str, default=_DEFAULT_POSITIVE_PROMPT, help="Text prompt for image generation")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--batch_input_json",
        "--batch_input_json",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type=str,
        type=str,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default=None,
        default=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Path to JSON file containing batch inputs. Each entry should have 'prompt' and 'output_...
        help="Path to JSON file containing batch inputs. Each entry should have 'prompt' and 'output_image' fields.",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument("--negative_prompt", type=str, default="", help="Negative text prompt for...
    parser.add_argument("--negative_prompt", type=str, default="", help="Negative text prompt for image generation")
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
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default="output/generated_image.jpg",
        default="output/generated_image.jpg",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Path to save the generated image (include file extension)",
        help="Path to save the generated image (include file extension)",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument("--use_cuda_graphs", action="store_true", help="Use CUDA Graphs for the i...
    parser.add_argument("--use_cuda_graphs", action="store_true", help="Use CUDA Graphs for the inference.")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument("--disable_guardrail", action="store_true", help="Disable guardrail check...
    parser.add_argument("--disable_guardrail", action="store_true", help="Disable guardrail checks on prompts")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument("--offload_guardrail", action="store_true", help="Offload guardrail to CP...
    parser.add_argument("--offload_guardrail", action="store_true", help="Offload guardrail to CPU to save GPU memory")
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
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return parser.parse_args()
    return parser.parse_args()


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def setup_pipeline(args: argparse.Namespace) -> Text2ImagePipeline:
def setup_pipeline(args: argparse.Namespace) -> Text2ImagePipeline:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Using model size: {args.model_size}")
    log.info(f"Using model size: {args.model_size}")
    # 中文说明：根据条件选择执行分支；代码：if args.model_size == "2B":
    if args.model_size == "2B":
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config = PREDICT2_TEXT2IMAGE_PIPELINE_2B
        config = PREDICT2_TEXT2IMAGE_PIPELINE_2B
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path = "checkpoints/nvidia/Cosmos-Predict2-2B-Text2Image/model.pt"
        dit_path = "checkpoints/nvidia/Cosmos-Predict2-2B-Text2Image/model.pt"
    # 中文说明：根据条件选择执行分支；代码：elif args.model_size == "14B":
    elif args.model_size == "14B":
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config = PREDICT2_TEXT2IMAGE_PIPELINE_14B
        config = PREDICT2_TEXT2IMAGE_PIPELINE_14B
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path = "checkpoints/nvidia/Cosmos-Predict2-14B-Text2Image/model.pt"
        dit_path = "checkpoints/nvidia/Cosmos-Predict2-14B-Text2Image/model.pt"
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError("Invalid model size. Choose either '2B' or '14B'.")
        raise ValueError("Invalid model size. Choose either '2B' or '14B'.")

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Disable guardrail if requested
    # Disable guardrail if requested
    # 中文说明：根据条件选择执行分支；代码：if args.disable_guardrail:
    if args.disable_guardrail:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning("Guardrail checks are disabled")
        log.warning("Guardrail checks are disabled")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config.guardrail_config.enabled = False
        config.guardrail_config.enabled = False
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config.guardrail_config.offload_model_to_cpu = args.offload_guardrail
    config.guardrail_config.offload_model_to_cpu = args.offload_guardrail

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

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Check if we're in a distributed environment (called from text2world)
    # Check if we're in a distributed environment (called from text2world)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_distributed = parallel_state.is_initialized() and torch.distributed.is_initialized()
    is_distributed = parallel_state.is_initialized() and torch.distributed.is_initialized()

    # 中文说明：根据条件选择执行分支；代码：if is_distributed:
    if is_distributed:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# We're in a multi-GPU text2world context - only initialize on rank 0
        # We're in a multi-GPU text2world context - only initialize on rank 0
        # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.distributed import get_rank
        from imaginaire.utils.distributed import get_rank

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank = get_rank()
        rank = get_rank()

        # 中文说明：根据条件选择执行分支；代码：if rank == 0:
        if rank == 0:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("Rank 0: Initializing Text2ImagePipeline for text2world")
            log.info("Rank 0: Initializing Text2ImagePipeline for text2world")
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Load models only on rank 0
            # Load models only on rank 0
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Initializing Text2ImagePipeline with model size: {args.model_size}")
            log.info(f"Initializing Text2ImagePipeline with model size: {args.model_size}")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe = Text2ImagePipeline.from_config(
            pipe = Text2ImagePipeline.from_config(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config=config,
                config=config,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path=dit_path,
                dit_path=dit_path,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：device="cuda",
                device="cuda",
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：torch_dtype=torch.bfloat16,
                torch_dtype=torch.bfloat16,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return pipe
            return pipe
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Rank {rank}: Skipping Text2ImagePipeline initialization - will wait for rank 0")
            log.info(f"Rank {rank}: Skipping Text2ImagePipeline initialization - will wait for rank 0")
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return None # Return None for non-rank-0 processes
            return None  # Return None for non-rank-0 processes
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# We're running as standalone text2image script
        # We're running as standalone text2image script
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Only initialize distributed if num_gpus > 1 AND we're running standalone
        # Only initialize distributed if num_gpus > 1 AND we're running standalone
        # 中文说明：根据条件选择执行分支；代码：if hasattr(args, "num_gpus") and args.num_gpus > 1:
        if hasattr(args, "num_gpus") and args.num_gpus > 1:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Initializing distributed environment with {args.num_gpus} GPUs for context paralle...
            log.info(f"Initializing distributed environment with {args.num_gpus} GPUs for context parallelism")

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Check if distributed environment is already initialized
            # Check if distributed environment is already initialized
            # 中文说明：根据条件选择执行分支；代码：if not parallel_state.is_initialized():
            if not parallel_state.is_initialized():
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：distributed.init()
                distributed.init()
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parallel_state.initialize_model_parallel(context_parallel_size=args.num_gpus)
                parallel_state.initialize_model_parallel(context_parallel_size=args.num_gpus)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Context parallel group initialized with {args.num_gpus} GPUs")
                log.info(f"Context parallel group initialized with {args.num_gpus} GPUs")
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("Distributed environment already initialized, skipping initialization")
                log.info("Distributed environment already initialized, skipping initialization")
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Check if we need to reinitialize with different context parallel size
                # Check if we need to reinitialize with different context parallel size
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：current_cp_size = parallel_state.get_context_parallel_world_size()
                current_cp_size = parallel_state.get_context_parallel_world_size()
                # 中文说明：根据条件选择执行分支；代码：if current_cp_size != args.num_gpus:
                if current_cp_size != args.num_gpus:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(f"Context parallel size mismatch: current={current_cp_size}, requested={args.num_...
                    log.warning(f"Context parallel size mismatch: current={current_cp_size}, requested={args.num_gpus}")
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning("Using existing context parallel configuration")
                    log.warning("Using existing context parallel configuration")
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Using existing context parallel group with {current_cp_size} GPUs")
                    log.info(f"Using existing context parallel group with {current_cp_size} GPUs")

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Load models for standalone execution
        # Load models for standalone execution
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Initializing Text2ImagePipeline with model size: {args.model_size}")
        log.info(f"Initializing Text2ImagePipeline with model size: {args.model_size}")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe = Text2ImagePipeline.from_config(
        pipe = Text2ImagePipeline.from_config(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config=config,
            config=config,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path=dit_path,
            dit_path=dit_path,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：device="cuda",
            device="cuda",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：torch_dtype=torch.bfloat16,
            torch_dtype=torch.bfloat16,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return pipe
        return pipe


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def process_single_generation(
def process_single_generation(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pipe: Text2ImagePipeline,
    pipe: Text2ImagePipeline,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：prompt: str,
    prompt: str,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：output_path: str,
    output_path: str,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：negative_prompt: str,
    negative_prompt: str,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：aspect_ratio: str,
    aspect_ratio: str,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：seed: int,
    seed: int,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：use_cuda_graphs: bool,
    use_cuda_graphs: bool,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：benchmark: bool,
    benchmark: bool,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> bool:
) -> bool:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Running Text2ImagePipeline\nprompt: {prompt}")
    log.info(f"Running Text2ImagePipeline\nprompt: {prompt}")

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# When benchmarking, run inference 4 times, exclude the 1st due to warmup and average time.
    # When benchmarking, run inference 4 times, exclude the 1st due to warmup and average time.
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_repeats = 4 if benchmark else 1
    num_repeats = 4 if benchmark else 1
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：time_sum = 0
    time_sum = 0
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i in range(num_repeats):
    for i in range(num_repeats):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Generate image
        # Generate image
        # 中文说明：根据条件选择执行分支；代码：if benchmark and i > 0:
        if benchmark and i > 0:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.synchronize()
            torch.cuda.synchronize()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：start_time = time.time()
            start_time = time.time()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：image = pipe(
        image = pipe(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prompt=prompt,
            prompt=prompt,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：negative_prompt=negative_prompt,
            negative_prompt=negative_prompt,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：aspect_ratio=aspect_ratio,
            aspect_ratio=aspect_ratio,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：seed=seed,
            seed=seed,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_cuda_graphs=use_cuda_graphs,
            use_cuda_graphs=use_cuda_graphs,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：根据条件选择执行分支；代码：if benchmark and i > 0:
        if benchmark and i > 0:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.synchronize()
            torch.cuda.synchronize()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：elapsed = time.time() - start_time
            elapsed = time.time() - start_time
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：time_sum += elapsed
            time_sum += elapsed
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"[iter {i} / {num_repeats - 1}] Generation time: {elapsed:.1f} seconds.")
            log.info(f"[iter {i} / {num_repeats - 1}] Generation time: {elapsed:.1f} seconds.")
    # 中文说明：根据条件选择执行分支；代码：if benchmark:
    if benchmark:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：time_avg = time_sum / (num_repeats - 1)
        time_avg = time_sum / (num_repeats - 1)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.critical(f"The benchmarked generation time for Text2ImagePipeline is {time_avg:.1f} secon...
        log.critical(f"The benchmarked generation time for Text2ImagePipeline is {time_avg:.1f} seconds.")

    # 中文说明：根据条件选择执行分支；代码：if image is not None:
    if image is not None:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# save the generated image
        # save the generated image
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_dir = os.path.dirname(output_path)
        output_dir = os.path.dirname(output_path)
        # 中文说明：根据条件选择执行分支；代码：if output_dir:
        if output_dir:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.makedirs(output_dir, exist_ok=True)
            os.makedirs(output_dir, exist_ok=True)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Saving generated image to: {output_path}")
        log.info(f"Saving generated image to: {output_path}")
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：save_image_or_video(image, output_path)
        save_image_or_video(image, output_path)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.success(f"Successfully saved image to: {output_path}")
        log.success(f"Successfully saved image to: {output_path}")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return True
        return True
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return False
    return False


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def generate_image(args: argparse.Namespace, pipe: Text2ImagePipeline) -> None:
def generate_image(args: argparse.Namespace, pipe: Text2ImagePipeline) -> None:
    # 中文说明：根据条件选择执行分支；代码：if args.benchmark:
    if args.benchmark:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(
        log.warning(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："Running in benchmark mode. Each generation will be rerun a couple of times and the average g...
            "Running in benchmark mode. Each generation will be rerun a couple of times and the average generation time will be shown."
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Text-to-image
    # Text-to-image
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

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for idx, item in enumerate(batch_inputs):
        for idx, item in enumerate(batch_inputs):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Processing batch item {idx + 1}/{len(batch_inputs)}")
            log.info(f"Processing batch item {idx + 1}/{len(batch_inputs)}")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prompt = item.get("prompt", "")
            prompt = item.get("prompt", "")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_image = item.get("output_image", f"output_{idx}.jpg")
            output_image = item.get("output_image", f"output_{idx}.jpg")

            # 中文说明：根据条件选择执行分支；代码：if not prompt:
            if not prompt:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(f"Skipping item {idx}: Missing prompt")
                log.warning(f"Skipping item {idx}: Missing prompt")
                # 中文说明：执行循环控制或空操作；代码：continue
                continue

            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：process_single_generation(
            process_single_generation(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe=pipe,
                pipe=pipe,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prompt=prompt,
                prompt=prompt,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_path=output_image,
                output_path=output_image,
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
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：根据条件选择执行分支；代码：if args.use_cuda_graphs:
        if args.use_cuda_graphs:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(
            log.warning(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："Using CUDA Graphs for a single inference call may not be beneficial because of overhead of G...
                "Using CUDA Graphs for a single inference call may not be beneficial because of overhead of Graphs creation."
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：process_single_generation(
        process_single_generation(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe=pipe,
            pipe=pipe,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prompt=args.prompt,
            prompt=args.prompt,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_path=args.save_path,
            output_path=args.save_path,
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
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：generate_image(args, pipe)
        generate_image(args, pipe)
    # 中文说明：处理异常、清理资源或管理上下文；代码：finally:
    finally:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Make sure to clean up the distributed environment
        # Make sure to clean up the distributed environment
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cleanup_distributed()
        cleanup_distributed()
