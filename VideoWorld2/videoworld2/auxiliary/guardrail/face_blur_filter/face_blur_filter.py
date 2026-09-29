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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import warnings
import warnings

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from retinaface.data import cfg_re50
from retinaface.data import cfg_re50
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from retinaface.layers.functions.prior_box import PriorBox
from retinaface.layers.functions.prior_box import PriorBox
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from retinaface.models.retinaface import RetinaFace
from retinaface.models.retinaface import RetinaFace
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.utils.data import DataLoader, TensorDataset
from torch.utils.data import DataLoader, TensorDataset
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from tqdm import tqdm
from tqdm import tqdm

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.auxiliary.guardrail.common.core import GuardrailRunner, PostprocessingGuardrail
from videoworld2.auxiliary.guardrail.common.core import GuardrailRunner, PostprocessingGuardrail
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.auxiliary.guardrail.common.io_utils import get_video_filepaths, read_video, ...
from videoworld2.auxiliary.guardrail.common.io_utils import get_video_filepaths, read_video, save_video
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.auxiliary.guardrail.face_blur_filter.blur_utils import pixelate_face
from videoworld2.auxiliary.guardrail.face_blur_filter.blur_utils import pixelate_face
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.auxiliary.guardrail.face_blur_filter.retinaface_utils import (
from videoworld2.auxiliary.guardrail.face_blur_filter.retinaface_utils import (
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：decode_batch,
    decode_batch,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：filter_detected_boxes,
    filter_detected_boxes,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：load_model,
    load_model,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log, misc
from imaginaire.utils import log, misc

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# RetinaFace model constants from https://github.com/biubug6/Pytorch_Retinaface/blob/master/d...
# RetinaFace model constants from https://github.com/biubug6/Pytorch_Retinaface/blob/master/detect.py
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：TOP_K = 5_000
TOP_K = 5_000
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：KEEP_TOP_K = 750
KEEP_TOP_K = 750
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：NMS_THRESHOLD = 0.4
NMS_THRESHOLD = 0.4


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class RetinaFaceFilter(PostprocessingGuardrail):
class RetinaFaceFilter(PostprocessingGuardrail):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：checkpoint_dir: str,
        checkpoint_dir: str,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：batch_size: int = 1,
        batch_size: int = 1,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：confidence_threshold: float = 0.7,
        confidence_threshold: float = 0.7,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：offload_model_to_cpu: bool = True,
        offload_model_to_cpu: bool = True,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Initialize the RetinaFace model for face detection and blurring.

        Args:
            checkpoint: Path to the RetinaFace checkpoint file
            batch_size: Batch size for RetinaFace inference and processing
            confidence_threshold: Minimum confidence score to consider a face detection
            offload_model_to_cpu (bool, optional): Whether to offload the model to CPU. Defaults to True.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.checkpoint = f"{checkpoint_dir}/nvidia/Cosmos-Guardrail1/face_blur_filter/Resnet50_Final...
        self.checkpoint = f"{checkpoint_dir}/nvidia/Cosmos-Guardrail1/face_blur_filter/Resnet50_Final.pth"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.cfg = cfg_re50
        self.cfg = cfg_re50
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.batch_size = batch_size
        self.batch_size = batch_size
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.confidence_threshold = confidence_threshold
        self.confidence_threshold = confidence_threshold
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dtype = torch.float32
        self.dtype = torch.float32
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.offload_model = offload_model_to_cpu
        self.offload_model = offload_model_to_cpu

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Disable loading ResNet pretrained weights
        # Disable loading ResNet pretrained weights
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.cfg["pretrain"] = False
        self.cfg["pretrain"] = False
        # 中文说明：处理异常、清理资源或管理上下文；代码：with warnings.catch_warnings():
        with warnings.catch_warnings():
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：warnings.simplefilter("ignore")
            warnings.simplefilter("ignore")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.net = RetinaFace(cfg=self.cfg, phase="test")
            self.net = RetinaFace(cfg=self.cfg, phase="test")

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Load from RetinaFace pretrained checkpoint
        # Load from RetinaFace pretrained checkpoint
        # 中文说明：根据条件选择执行分支；代码：if not offload_model_to_cpu:
        if not offload_model_to_cpu:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.net = load_model(self.net, self.checkpoint, False)
            self.net = load_model(self.net, self.checkpoint, False)
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.net.to("cuda", dtype=self.dtype).eval()
            self.net.to("cuda", dtype=self.dtype).eval()
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug("Moved face blur filter to GPU")
            log.debug("Moved face blur filter to GPU")
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.net = load_model(self.net, self.checkpoint, True)
            self.net = load_model(self.net, self.checkpoint, True)
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.net.to("cpu", dtype=self.dtype).eval()
            self.net.to("cpu", dtype=self.dtype).eval()
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug("Moved face blur filter to CPU")
            log.debug("Moved face blur filter to CPU")

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def preprocess_frames(self, frames: np.ndarray) -> torch.Tensor:
    def preprocess_frames(self, frames: np.ndarray) -> torch.Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Preprocess a sequence of frames for face detection.
        """Preprocess a sequence of frames for face detection.

        Args:
            frames: Input frames

        Returns:
            Preprocessed frames tensor
        """
        # 中文说明：处理异常、清理资源或管理上下文；代码：with torch.no_grad():
        with torch.no_grad():
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames_tensor = torch.from_numpy(frames).to("cuda", dtype=self.dtype) # Shape: [T, H, W, C]
            frames_tensor = torch.from_numpy(frames).to("cuda", dtype=self.dtype)  # Shape: [T, H, W, C]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames_tensor = frames_tensor.permute(0, 3, 1, 2) # Shape: [T, C, H, W]
            frames_tensor = frames_tensor.permute(0, 3, 1, 2)  # Shape: [T, C, H, W]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames_tensor = frames_tensor[:, [2, 1, 0], :, :] # RGB to BGR to match RetinaFace model input
            frames_tensor = frames_tensor[:, [2, 1, 0], :, :]  # RGB to BGR to match RetinaFace model input
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：means = torch.tensor([104.0, 117.0, 123.0], device="cuda", dtype=self.dtype).view(1, 3, 1, 1)
            means = torch.tensor([104.0, 117.0, 123.0], device="cuda", dtype=self.dtype).view(1, 3, 1, 1)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames_tensor = frames_tensor - means # Subtract mean BGR values for each channel
            frames_tensor = frames_tensor - means  # Subtract mean BGR values for each channel
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return frames_tensor
            return frames_tensor

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def blur_detected_faces(
    def blur_detected_faces(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：frames: np.ndarray,
        frames: np.ndarray,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：batch_loc: torch.Tensor,
        batch_loc: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：batch_conf: torch.Tensor,
        batch_conf: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：prior_data: torch.Tensor,
        prior_data: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scale: torch.Tensor,
        scale: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：min_size: tuple[int] = (20, 20),
        min_size: tuple[int] = (20, 20),
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> list[np.ndarray]:
    ) -> list[np.ndarray]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Blur detected faces in a batch of frames using RetinaFace predictions.
        """Blur detected faces in a batch of frames using RetinaFace predictions.

        Args:
            frames: Input frames
            batch_loc: Batched location predictions
            batch_conf: Batched confidence scores
            prior_data: Prior boxes for the video
            scale: Scale factor for resizing detections
            min_size: Minimum size of a detected face region in pixels

        Returns:
            Processed frames with pixelated faces
        """
        # 中文说明：处理异常、清理资源或管理上下文；代码：with torch.no_grad():
        with torch.no_grad():
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch_boxes = decode_batch(batch_loc, prior_data, self.cfg["variance"])
            batch_boxes = decode_batch(batch_loc, prior_data, self.cfg["variance"])
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch_boxes = batch_boxes * scale
            batch_boxes = batch_boxes * scale

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：blurred_frames = []
        blurred_frames = []
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i, boxes in enumerate(batch_boxes):
        for i, boxes in enumerate(batch_boxes):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：boxes = boxes.detach().cpu().numpy()
            boxes = boxes.detach().cpu().numpy()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scores = batch_conf[i, :, 1].detach().cpu().numpy()
            scores = batch_conf[i, :, 1].detach().cpu().numpy()

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：filtered_boxes = filter_detected_boxes(
            filtered_boxes = filter_detected_boxes(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：boxes,
                boxes,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scores,
                scores,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：confidence_threshold=self.confidence_threshold,
                confidence_threshold=self.confidence_threshold,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：nms_threshold=NMS_THRESHOLD,
                nms_threshold=NMS_THRESHOLD,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：top_k=TOP_K,
                top_k=TOP_K,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：keep_top_k=KEEP_TOP_K,
                keep_top_k=KEEP_TOP_K,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame = frames[i]
            frame = frames[i]
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for box in filtered_boxes:
            for box in filtered_boxes:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x1, y1, x2, y2 = map(int, box)
                x1, y1, x2, y2 = map(int, box)
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Ignore bounding boxes smaller than the minimum size
                # Ignore bounding boxes smaller than the minimum size
                # 中文说明：根据条件选择执行分支；代码：if x2 - x1 < min_size[0] or y2 - y1 < min_size[1]:
                if x2 - x1 < min_size[0] or y2 - y1 < min_size[1]:
                    # 中文说明：执行循环控制或空操作；代码：continue
                    continue
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_h, max_w = frame.shape[:2]
                max_h, max_w = frame.shape[:2]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：face_roi = frame[max(y1, 0) : min(y2, max_h), max(x1, 0) : min(x2, max_w)]
                face_roi = frame[max(y1, 0) : min(y2, max_h), max(x1, 0) : min(x2, max_w)]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：blurred_face = pixelate_face(face_roi)
                blurred_face = pixelate_face(face_roi)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame[max(y1, 0) : min(y2, max_h), max(x1, 0) : min(x2, max_w)] = blurred_face
                frame[max(y1, 0) : min(y2, max_h), max(x1, 0) : min(x2, max_w)] = blurred_face
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：blurred_frames.append(frame)
            blurred_frames.append(frame)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return blurred_frames
        return blurred_frames

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def postprocess(self, frames: np.ndarray) -> np.ndarray:
    def postprocess(self, frames: np.ndarray) -> np.ndarray:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Blur faces in a sequence of frames.
        """Blur faces in a sequence of frames.

        Args:
            frames: Input frames

        Returns:
            Processed frames with pixelated faces
        """
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Create dataset and dataloader
        # Create dataset and dataloader
        # 中文说明：根据条件选择执行分支；代码：if self.offload_model:
        if self.offload_model:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.net = self.net.to("cuda")
            self.net = self.net.to("cuda")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug("Move face blur filter to GPU")
            log.debug("Move face blur filter to GPU")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames_tensor = self.preprocess_frames(frames)
        frames_tensor = self.preprocess_frames(frames)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset = TensorDataset(frames_tensor)
        dataset = TensorDataset(frames_tensor)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataloader = DataLoader(dataset, batch_size=self.batch_size, shuffle=False)
        dataloader = DataLoader(dataset, batch_size=self.batch_size, shuffle=False)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：processed_frames, processed_batches = [], []
        processed_frames, processed_batches = [], []

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：prior_data, scale = None, None
        prior_data, scale = None, None
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i, batch in enumerate(dataloader):
        for i, batch in enumerate(dataloader):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch = batch[0]
            batch = batch[0]
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：h, w = batch.shape[-2:] # Batch shape: [C, H, W]
            h, w = batch.shape[-2:]  # Batch shape: [C, H, W]

            # 中文说明：处理异常、清理资源或管理上下文；代码：with torch.no_grad():
            with torch.no_grad():
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Generate priors for the video
                # Generate priors for the video
                # 中文说明：根据条件选择执行分支；代码：if prior_data is None:
                if prior_data is None:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：priorbox = PriorBox(self.cfg, image_size=(h, w))
                    priorbox = PriorBox(self.cfg, image_size=(h, w))
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：priors = priorbox.forward()
                    priors = priorbox.forward()
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：priors = priors.to("cuda", dtype=self.dtype)
                    priors = priors.to("cuda", dtype=self.dtype)
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prior_data = priors.data
                    prior_data = priors.data

                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Get scale for resizing detections
                # Get scale for resizing detections
                # 中文说明：根据条件选择执行分支；代码：if scale is None:
                if scale is None:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scale = torch.Tensor([w, h, w, h])
                    scale = torch.Tensor([w, h, w, h])
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scale = scale.to("cuda", dtype=self.dtype)
                    scale = scale.to("cuda", dtype=self.dtype)

                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：batch_loc, batch_conf, _ = self.net(batch)
                batch_loc, batch_conf, _ = self.net(batch)

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Blur detected faces in each batch of frames
            # Blur detected faces in each batch of frames
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：start_idx = i * self.batch_size
            start_idx = i * self.batch_size
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：end_idx = min(start_idx + self.batch_size, len(frames))
            end_idx = min(start_idx + self.batch_size, len(frames))
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：processed_batches.append(
            processed_batches.append(
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.blur_detected_faces(frames[start_idx:end_idx], batch_loc, batch_conf, prior_data, scale)
                self.blur_detected_faces(frames[start_idx:end_idx], batch_loc, batch_conf, prior_data, scale)
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：processed_frames = [frame for batch in processed_batches for frame in batch]
        processed_frames = [frame for batch in processed_batches for frame in batch]
        # 中文说明：根据条件选择执行分支；代码：if self.offload_model:
        if self.offload_model:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.net = self.net.to("cpu")
            self.net = self.net.to("cpu")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug("Offload face blur filter to CPU")
            log.debug("Offload face blur filter to CPU")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return np.array(processed_frames)
        return np.array(processed_frames)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def parse_args():
def parse_args():
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser()
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument("--input_dir", type=str, required=True, help="Path containing input videos")
    parser.add_argument("--input_dir", type=str, required=True, help="Path containing input videos")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument("--output_dir", type=str, required=True, help="Path for saving processed ...
    parser.add_argument("--output_dir", type=str, required=True, help="Path for saving processed videos")
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

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：face_blur = RetinaFaceFilter(
    face_blur = RetinaFaceFilter(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint_dir="checkpoints/nvidia/Cosmos-Guardrail1/face_blur_filter/Resnet50_Final.pth"
        checkpoint_dir="checkpoints/nvidia/Cosmos-Guardrail1/face_blur_filter/Resnet50_Final.pth"
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：postprocessing_runner = GuardrailRunner(postprocessors=[face_blur])
    postprocessing_runner = GuardrailRunner(postprocessors=[face_blur])
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(args.output_dir, exist_ok=True)

    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for filepath in tqdm(filepaths):
    for filepath in tqdm(filepaths):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_data = read_video(filepath)
        video_data = read_video(filepath)
        # 中文说明：处理异常、清理资源或管理上下文；代码：with misc.timer("face blur filter"):
        with misc.timer("face blur filter"):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = postprocessing_runner.postprocess(video_data.frames)
            frames = postprocessing_runner.postprocess(video_data.frames)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_path = os.path.join(args.output_dir, os.path.basename(filepath))
        output_path = os.path.join(args.output_dir, os.path.basename(filepath))
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：save_video(output_path, frames, video_data.fps)
        save_video(output_path, frames, video_data.fps)


# 中文说明：根据条件选择执行分支；代码：if __name__ == "__main__":
if __name__ == "__main__":
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：args = parse_args()
    args = parse_args()
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：main(args)
    main(args)
