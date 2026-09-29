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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.auxiliary.guardrail.blocklist.blocklist import Blocklist
from videoworld2.auxiliary.guardrail.blocklist.blocklist import Blocklist
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.auxiliary.guardrail.common.core import GuardrailRunner
from videoworld2.auxiliary.guardrail.common.core import GuardrailRunner
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.auxiliary.guardrail.face_blur_filter.face_blur_filter import RetinaFaceFilter
from videoworld2.auxiliary.guardrail.face_blur_filter.face_blur_filter import RetinaFaceFilter
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.auxiliary.guardrail.llamaGuard3.llamaGuard3 import LlamaGuard3
from videoworld2.auxiliary.guardrail.llamaGuard3.llamaGuard3 import LlamaGuard3
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.auxiliary.guardrail.video_content_safety_filter.video_content_safety_filter ...
from videoworld2.auxiliary.guardrail.video_content_safety_filter.video_content_safety_filter import (
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：VideoContentSafetyFilter,
    VideoContentSafetyFilter,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def create_text_guardrail_runner(checkpoint_dir: str, offload_model_to_cpu: bool) -> Guardrai...
def create_text_guardrail_runner(checkpoint_dir: str, offload_model_to_cpu: bool) -> GuardrailRunner:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Create the text guardrail runner."""
    """Create the text guardrail runner."""
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return GuardrailRunner(
    return GuardrailRunner(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：safety_models=[
        safety_models=[
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：Blocklist(checkpoint_dir=checkpoint_dir),
            Blocklist(checkpoint_dir=checkpoint_dir),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：LlamaGuard3(checkpoint_dir=checkpoint_dir, offload_model_to_cpu=offload_model_to_cpu),
            LlamaGuard3(checkpoint_dir=checkpoint_dir, offload_model_to_cpu=offload_model_to_cpu),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
        ]
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def create_video_guardrail_runner(checkpoint_dir: str, offload_model_to_cpu: bool) -> Guardra...
def create_video_guardrail_runner(checkpoint_dir: str, offload_model_to_cpu: bool) -> GuardrailRunner:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Create the video guardrail runner."""
    """Create the video guardrail runner."""
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return GuardrailRunner(
    return GuardrailRunner(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：safety_models=[
        safety_models=[
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：VideoContentSafetyFilter(checkpoint_dir=checkpoint_dir, offload_model_to_cpu=offload_model_to...
            VideoContentSafetyFilter(checkpoint_dir=checkpoint_dir, offload_model_to_cpu=offload_model_to_cpu)
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：],
        ],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：postprocessors=[RetinaFaceFilter(checkpoint_dir=checkpoint_dir, offload_model_to_cpu=offload_...
        postprocessors=[RetinaFaceFilter(checkpoint_dir=checkpoint_dir, offload_model_to_cpu=offload_model_to_cpu)],
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def run_text_guardrail(prompt: str, guardrail_runner: GuardrailRunner) -> bool:
def run_text_guardrail(prompt: str, guardrail_runner: GuardrailRunner) -> bool:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Run the text guardrail on the prompt, checking for content safety.
    """Run the text guardrail on the prompt, checking for content safety.

    Args:
        prompt: The text prompt.
        guardrail_runner: The text guardrail runner.

    Returns:
        bool: Whether the prompt is safe.
    """
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：is_safe, message = guardrail_runner.run_safety_check(prompt)
    is_safe, message = guardrail_runner.run_safety_check(prompt)
    # 中文说明：根据条件选择执行分支；代码：if not is_safe:
    if not is_safe:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.critical(f"GUARDRAIL BLOCKED: {message}")
        log.critical(f"GUARDRAIL BLOCKED: {message}")
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return is_safe
    return is_safe


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def run_video_guardrail(frames: np.ndarray, guardrail_runner: GuardrailRunner) -> np.ndarray ...
def run_video_guardrail(frames: np.ndarray, guardrail_runner: GuardrailRunner) -> np.ndarray | None:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Run the video guardrail on the frames, checking for content safety and applying face blur.
    """Run the video guardrail on the frames, checking for content safety and applying face blur.

    Args:
        frames: The frames of the generated video.
        guardrail_runner: The video guardrail runner.

    Returns:
        The processed frames if safe, otherwise None.
    """
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：is_safe, message = guardrail_runner.run_safety_check(frames)
    is_safe, message = guardrail_runner.run_safety_check(frames)
    # 中文说明：根据条件选择执行分支；代码：if not is_safe:
    if not is_safe:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.critical(f"GUARDRAIL BLOCKED: {message}")
        log.critical(f"GUARDRAIL BLOCKED: {message}")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return None
        return None

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = guardrail_runner.postprocess(frames)
    frames = guardrail_runner.postprocess(frames)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return frames
    return frames
