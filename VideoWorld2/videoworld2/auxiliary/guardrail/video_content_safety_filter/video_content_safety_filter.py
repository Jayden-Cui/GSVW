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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Iterable, Tuple, Union
from typing import Iterable, Tuple, Union

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from PIL import Image
from PIL import Image

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.auxiliary.guardrail.common.core import ContentSafetyGuardrail, GuardrailRunner
from videoworld2.auxiliary.guardrail.common.core import ContentSafetyGuardrail, GuardrailRunner
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.auxiliary.guardrail.common.io_utils import get_video_filepaths, read_video
from videoworld2.auxiliary.guardrail.common.io_utils import get_video_filepaths, read_video
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.auxiliary.guardrail.video_content_safety_filter.model import ModelConfig, Vi...
from videoworld2.auxiliary.guardrail.video_content_safety_filter.model import ModelConfig, VideoSafetyModel
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.auxiliary.guardrail.video_content_safety_filter.vision_encoder import SigLIP...
from videoworld2.auxiliary.guardrail.video_content_safety_filter.vision_encoder import SigLIPEncoder
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log, misc
from imaginaire.utils import log, misc

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Define the class index to class name mapping for multi-class classification
# Define the class index to class name mapping for multi-class classification
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：CLASS_IDX_TO_NAME = {
CLASS_IDX_TO_NAME = {
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：0: "Safe",
    0: "Safe",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：1: "Sexual_Content",
    1: "Sexual_Content",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：2: "Violence",
    2: "Violence",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：3: "Drugs",
    3: "Drugs",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：4: "Child_Abuse",
    4: "Child_Abuse",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：5: "Hate_and_Harassment",
    5: "Hate_and_Harassment",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：6: "Self-Harm",
    6: "Self-Harm",
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
}


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class VideoContentSafetyFilter(ContentSafetyGuardrail):
class VideoContentSafetyFilter(ContentSafetyGuardrail):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：checkpoint_dir: str,
        checkpoint_dir: str,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：offload_model_to_cpu: bool = True,
        offload_model_to_cpu: bool = True,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Video content safety filter model.
        """Video content safety filter model.

        Args:
            checkpoint_dir (str): Path to the checkpoint directory.
            offload_model_to_cpu (bool, optional): Whether to offload the model to CPU. Defaults to True.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.offload_model = offload_model_to_cpu
        self.offload_model = offload_model_to_cpu
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dtype = torch.float32
        self.dtype = torch.float32

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.checkpoint_dir = os.path.join(checkpoint_dir, "nvidia/Cosmos-Guardrail1/video_content_sa...
        self.checkpoint_dir = os.path.join(checkpoint_dir, "nvidia/Cosmos-Guardrail1/video_content_safety_filter")

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Use ModelConfig directly for inference configuration
        # Use ModelConfig directly for inference configuration
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_config = ModelConfig(input_size=1152, num_classes=7)
        model_config = ModelConfig(input_size=1152, num_classes=7)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Load the multi-class classifier and initialize the SigLIP encoder
        # Load the multi-class classifier and initialize the SigLIP encoder
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.model = VideoSafetyModel(model_config)
        self.model = VideoSafetyModel(model_config)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：safety_filter_local_path = os.path.join(self.checkpoint_dir, "safety_filter.pt")
        safety_filter_local_path = os.path.join(self.checkpoint_dir, "safety_filter.pt")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint = torch.load(safety_filter_local_path, map_location=torch.device("cpu"), weights_o...
        checkpoint = torch.load(safety_filter_local_path, map_location=torch.device("cpu"), weights_only=True)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.model.load_state_dict(checkpoint["model"])
        self.model.load_state_dict(checkpoint["model"])
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.encoder = SigLIPEncoder(checkpoint_dir=self.checkpoint_dir, device="cuda", dtype=self.dt...
        self.encoder = SigLIPEncoder(checkpoint_dir=self.checkpoint_dir, device="cuda", dtype=self.dtype)
        # 中文说明：根据条件选择执行分支；代码：if offload_model_to_cpu:
        if offload_model_to_cpu:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.encoder.to("cpu")
            self.encoder.to("cpu")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.model = self.model.to("cpu", dtype=self.dtype).eval()
            self.model = self.model.to("cpu", dtype=self.dtype).eval()
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug("Moved video content safety filter to CPU")
            log.debug("Moved video content safety filter to CPU")
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.encoder.to("cuda")
            self.encoder.to("cuda")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.model = self.model.to("cuda", dtype=self.dtype).eval()
            self.model = self.model.to("cuda", dtype=self.dtype).eval()
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug("Moved video content safety filter to GPU")
            log.debug("Moved video content safety filter to GPU")

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.inference_mode()
    @torch.inference_mode()
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __infer(self, pil_image: Image.Image) -> int:
    def __infer(self, pil_image: Image.Image) -> int:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Infer the class of the image."""
        """Infer the class of the image."""
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：image_embs = self.encoder.encode_image(pil_image)
        image_embs = self.encoder.encode_image(pil_image)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：logits = self.model.network(image_embs)
        logits = self.model.network(image_embs)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：probabilities = torch.nn.functional.softmax(logits, dim=-1)
        probabilities = torch.nn.functional.softmax(logits, dim=-1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：predicted_class = torch.argmax(probabilities, dim=-1).item()
        predicted_class = torch.argmax(probabilities, dim=-1).item()
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return predicted_class
        return predicted_class

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _to_cuda_if_offload(self):
    def _to_cuda_if_offload(self):
        # 中文说明：根据条件选择执行分支；代码：if self.offload_model:
        if self.offload_model:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.encoder = self.encoder.to("cuda")
            self.encoder = self.encoder.to("cuda")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.model = self.model.to("cuda")
            self.model = self.model.to("cuda")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug("Move video content safety filter to GPU")
            log.debug("Move video content safety filter to GPU")

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _to_cpu_if_offload(self):
    def _to_cpu_if_offload(self):
        # 中文说明：根据条件选择执行分支；代码：if self.offload_model:
        if self.offload_model:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.encoder = self.encoder.to("cpu")
            self.encoder = self.encoder.to("cpu")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.model = self.model.to("cpu")
            self.model = self.model.to("cpu")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug("Offload video content safety filter to CPU")
            log.debug("Offload video content safety filter to CPU")

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_safe_file(self, filepath: str) -> bool:
    def is_safe_file(self, filepath: str) -> bool:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Check if the video file is safe."""
        """Check if the video file is safe."""
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_data = read_video(filepath)
        video_data = read_video(filepath)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Sample frames at 2 FPS
        # Sample frames at 2 FPS
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sample_rate = 2 # frames per second
        sample_rate = 2  # frames per second
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_interval = int(video_data.fps / sample_rate)
        frame_interval = int(video_data.fps / sample_rate)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_numbers = list(range(0, int(video_data.fps * video_data.duration), frame_interval))
        frame_numbers = list(range(0, int(video_data.fps * video_data.duration), frame_interval))

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_safe = True
        is_safe = True
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_scores = []
        frame_scores = []

        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._to_cuda_if_offload()
        self._to_cuda_if_offload()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for frame_number in frame_numbers:
        for frame_number in frame_numbers:
            # 中文说明：开始一个可捕获异常的代码块；代码：try:
            try:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame = video_data.frames[frame_number]
                frame = video_data.frames[frame_number]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pil_image = Image.fromarray(frame)
                pil_image = Image.fromarray(frame)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：predicted_class = self.__infer(pil_image)
                predicted_class = self.__infer(pil_image)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：class_name = CLASS_IDX_TO_NAME.get(predicted_class, "Unknown")
                class_name = CLASS_IDX_TO_NAME.get(predicted_class, "Unknown")
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：frame_scores.append({"frame_number": frame_number, "class": class_name})
                frame_scores.append({"frame_number": frame_number, "class": class_name})

                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# If any frame is not "Safe", mark the video as unsafe
                # If any frame is not "Safe", mark the video as unsafe
                # 中文说明：根据条件选择执行分支；代码：if predicted_class != 0:
                if predicted_class != 0:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_safe = False
                    is_safe = False
                    # 中文说明：执行循环控制或空操作；代码：break
                    break

            # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
            except Exception as e:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(f"Warning: Failed to run safety classifier on frame_number {frame_number}. Except...
                log.warning(f"Warning: Failed to run safety classifier on frame_number {frame_number}. Exception: {e}")
                # 中文说明：执行循环控制或空操作；代码：continue
                continue

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Prepare data for JSON
        # Prepare data for JSON
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_data = {
        video_data = {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："filepath": filepath,
            "filepath": filepath,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："is_safe": is_safe,
            "is_safe": is_safe,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："video_length": video_data.duration,
            "video_length": video_data.duration,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："fps": video_data.fps,
            "fps": video_data.fps,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："frame_scores": frame_scores,
            "frame_scores": frame_scores,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._to_cpu_if_offload()
        self._to_cpu_if_offload()
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Video {filepath} is {'SAFE' if is_safe else 'UNSAFE'}.")
        log.info(f"Video {filepath} is {'SAFE' if is_safe else 'UNSAFE'}.")
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(f"Video data: {json.dumps(video_data, indent=4)}")
        log.debug(f"Video data: {json.dumps(video_data, indent=4)}")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return is_safe
        return is_safe

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_safe_frames(self, frames: Iterable) -> bool:
    def is_safe_frames(self, frames: Iterable) -> bool:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Check if the video frames are safe."""
        """Check if the video frames are safe."""
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_safe = True
        is_safe = True
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_scores = []
        frame_scores = []

        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._to_cuda_if_offload()
        self._to_cuda_if_offload()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for frame_number, frame in enumerate(frames):
        for frame_number, frame in enumerate(frames):
            # 中文说明：开始一个可捕获异常的代码块；代码：try:
            try:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pil_image = Image.fromarray(frame)
                pil_image = Image.fromarray(frame)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：predicted_class = self.__infer(pil_image)
                predicted_class = self.__infer(pil_image)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：class_name = CLASS_IDX_TO_NAME.get(predicted_class, "Unknown")
                class_name = CLASS_IDX_TO_NAME.get(predicted_class, "Unknown")
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：frame_scores.append({"frame_number": frame_number, "class": class_name})
                frame_scores.append({"frame_number": frame_number, "class": class_name})

                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# If any frame is not "Safe", mark as not safe
                # If any frame is not "Safe", mark as not safe
                # 中文说明：根据条件选择执行分支；代码：if predicted_class != 0:
                if predicted_class != 0:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_safe = False
                    is_safe = False
                    # 中文说明：执行循环控制或空操作；代码：break
                    break

            # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
            except Exception as e:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(f"Warning: Failed to run safety classifier on frame_number {frame_number}. Except...
                log.warning(f"Warning: Failed to run safety classifier on frame_number {frame_number}. Exception: {e}")
                # 中文说明：执行循环控制或空操作；代码：continue
                continue

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_data = {
        video_data = {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："is_safe": is_safe,
            "is_safe": is_safe,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："frame_scores": frame_scores,
            "frame_scores": frame_scores,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._to_cpu_if_offload()
        self._to_cpu_if_offload()
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(f"Frames data: {json.dumps(video_data, indent=4)}")
        log.debug(f"Frames data: {json.dumps(video_data, indent=4)}")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return is_safe
        return is_safe

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_safe(self, input: Union[str, Iterable]) -> Tuple[bool, str]:
    def is_safe(self, input: Union[str, Iterable]) -> Tuple[bool, str]:
        # 中文说明：根据条件选择执行分支；代码：if isinstance(input, str):
        if isinstance(input, str):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_safe = self.is_safe_file(input)
            is_safe = self.is_safe_file(input)
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return is_safe, "safe video detected" if is_safe else "unsafe video detected"
            return is_safe, "safe video detected" if is_safe else "unsafe video detected"
        # 中文说明：根据条件选择执行分支；代码：elif isinstance(input, Iterable):
        elif isinstance(input, Iterable):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_safe = self.is_safe_frames(input)
            is_safe = self.is_safe_frames(input)
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return is_safe, "safe frames detected" if is_safe else "unsafe frames detected"
            return is_safe, "safe frames detected" if is_safe else "unsafe frames detected"
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Input type {type(input)} not supported.")
            raise ValueError(f"Input type {type(input)} not supported.")


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def parse_args():
def parse_args():
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser()
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument("--input_dir", type=str, required=True, help="Path containing input videos")
    parser.add_argument("--input_dir", type=str, required=True, help="Path containing input videos")
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return parser.parse_args()
    return parser.parse_args()


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def main(args):
def main(args):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：filepaths = get_video_filepaths(args.input_dir)
    filepaths = get_video_filepaths(args.input_dir)
    # 中文说明：根据条件选择执行分支；代码：if not filepaths:
    if not filepaths:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.error(f"No video files found in directory: {args.input_dir}")
        log.error(f"No video files found in directory: {args.input_dir}")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return
        return

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_filter = VideoContentSafetyFilter(
    video_filter = VideoContentSafetyFilter(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint_dir="checkpoints/nvidia/Cosmos-Guardrail1/video_content_safety_filter"
        checkpoint_dir="checkpoints/nvidia/Cosmos-Guardrail1/video_content_safety_filter"
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：runner = GuardrailRunner(safety_models=[video_filter], generic_safe_msg="Video is safe")
    runner = GuardrailRunner(safety_models=[video_filter], generic_safe_msg="Video is safe")

    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for filepath in filepaths:
    for filepath in filepaths:
        # 中文说明：处理异常、清理资源或管理上下文；代码：with misc.timer("video content safety filter"):
        with misc.timer("video content safety filter"):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_ = runner.run_safety_check(filepath)
            _ = runner.run_safety_check(filepath)


# 中文说明：根据条件选择执行分支；代码：if __name__ == "__main__":
if __name__ == "__main__":
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：args = parse_args()
    args = parse_args()
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：main(args)
    main(args)
