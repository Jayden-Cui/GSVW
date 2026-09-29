# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights rese...
# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# SPDX-License-Identifier: Apache-2.0
# SPDX-License-Identifier: Apache-2.0
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
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# http://www.apache.org/licenses/LICENSE-2.0
# http://www.apache.org/licenses/LICENSE-2.0
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

# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
"""
Adapted from:
https://github.com/bytedance/IRASim/blob/main/dataset/dataset_3D.py
"""

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import json
import json
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import random
import random
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import traceback
import traceback
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import warnings
import warnings
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from concurrent.futures import ThreadPoolExecutor, as_completed
from concurrent.futures import ThreadPoolExecutor, as_completed

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import imageio
import imageio
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from einops import rearrange
from einops import rearrange
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.utils.data import Dataset
from torch.utils.data import Dataset
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torchvision import transforms as T
from torchvision import transforms as T
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from tqdm import tqdm
from tqdm import tqdm

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.data.action_conditioned.dataset_utils import (
from videoworld2.data.action_conditioned.dataset_utils import (
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：Resize_Preprocess,
    Resize_Preprocess,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ToTensorVideo,
    ToTensorVideo,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：euler2rotm,
    euler2rotm,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rotm2euler,
    rotm2euler,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ActionConditionedDataset(Dataset):
class ActionConditionedDataset(Dataset):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：train_annotation_path,
        train_annotation_path,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：val_annotation_path,
        val_annotation_path,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：test_annotation_path,
        test_annotation_path,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video_path,
        video_path,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sequence_interval,
        sequence_interval,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_frames,
        num_frames,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cam_ids,
        cam_ids,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：accumulate_action,
        accumulate_action,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video_size,
        video_size,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：val_start_frame_interval,
        val_start_frame_interval,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：debug=False,
        debug=False,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：normalize=False,
        normalize=False,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pre_encode=False,
        pre_encode=False,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：do_evaluate=False,
        do_evaluate=False,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：load_t5_embeddings=False,
        load_t5_embeddings=False,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：load_action=True,
        load_action=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mode="train",
        mode="train",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Dataset class for loading 3D robot action-conditioned data.
        """Dataset class for loading 3D robot action-conditioned data.

        This dataset loads robot trajectories consisting of RGB video frames, robot states (arm positions and gripper states),
        and computes relative actions between consecutive frames.

        Args:
            train_annotation_path (str): Path to training annotation files
            val_annotation_path (str): Path to validation annotation files
            test_annotation_path (str): Path to test annotation files
            video_path (str): Base path to video files
            sequence_interval (int): Interval between sampled frames in a sequence
            num_frames (int): Number of frames to load per sequence
            cam_ids (list): List of camera IDs to sample from
            accumulate_action (bool): Whether to accumulate actions relative to first frame
            video_size (list): Target size [H,W] for video frames
            val_start_frame_interval (int): Frame sampling interval for validation/test
            debug (bool, optional): If True, only loads subset of data. Defaults to False.
            normalize (bool, optional): Whether to normalize video frames. Defaults to False.
            pre_encode (bool, optional): Whether to pre-encode video frames. Defaults to False.
            do_evaluate (bool, optional): Whether in evaluation mode. Defaults to False.
            load_t5_embeddings (bool, optional): Whether to load T5 embeddings. Defaults to False.
            load_action (bool, optional): Whether to load actions. Defaults to True.
            mode (str, optional): Dataset mode - 'train', 'val' or 'test'. Defaults to 'train'.

        The dataset loads robot trajectories and computes:
        - RGB video frames from specified camera views
        - Robot arm states (xyz position + euler angles)
        - Gripper states (binary open/closed)
        - Relative actions between consecutive frames

        Actions are computed as relative transforms between frames:
        - Translation: xyz offset in previous frame's coordinate frame
        - Rotation: euler angles of relative rotation
        - Gripper: binary gripper state

        Returns dict with:
            - video: RGB frames tensor [T,C,H,W]
            - action: Action tensor [T-1,7]
            - video_name: Dict with episode/frame metadata
            - latent: Pre-encoded video features if pre_encode=True
        """

        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：根据条件选择执行分支；代码：if mode == "train":
        if mode == "train":
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.data_path = train_annotation_path
            self.data_path = train_annotation_path
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.start_frame_interval = 1
            self.start_frame_interval = 1
        # 中文说明：根据条件选择执行分支；代码：elif mode == "val":
        elif mode == "val":
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.data_path = val_annotation_path
            self.data_path = val_annotation_path
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.start_frame_interval = val_start_frame_interval
            self.start_frame_interval = val_start_frame_interval
        # 中文说明：根据条件选择执行分支；代码：elif mode == "test":
        elif mode == "test":
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.data_path = test_annotation_path
            self.data_path = test_annotation_path
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.start_frame_interval = val_start_frame_interval
            self.start_frame_interval = val_start_frame_interval
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.video_path = video_path
        self.video_path = video_path
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.sequence_interval = sequence_interval
        self.sequence_interval = sequence_interval
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.mode = mode
        self.mode = mode
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.sequence_length = num_frames
        self.sequence_length = num_frames
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.normalize = normalize
        self.normalize = normalize
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.pre_encode = pre_encode
        self.pre_encode = pre_encode
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.load_t5_embeddings = load_t5_embeddings
        self.load_t5_embeddings = load_t5_embeddings
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.load_action = load_action
        self.load_action = load_action

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.cam_ids = cam_ids
        self.cam_ids = cam_ids
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.accumulate_action = accumulate_action
        self.accumulate_action = accumulate_action

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.action_dim = 7 # ee xyz (3) + ee euler (3) + gripper(1)
        self.action_dim = 7  # ee xyz (3) + ee euler (3) + gripper(1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.c_act_scaler = [20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 1.0]
        self.c_act_scaler = [20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 1.0]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.c_act_scaler = np.array(self.c_act_scaler, dtype=float)
        self.c_act_scaler = np.array(self.c_act_scaler, dtype=float)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.ann_files = self._init_anns(self.data_path)
        self.ann_files = self._init_anns(self.data_path)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"{len(self.ann_files)} trajectories in total")
        print(f"{len(self.ann_files)} trajectories in total")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.samples = self._init_sequences(self.ann_files)
        self.samples = self._init_sequences(self.ann_files)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.samples = sorted(self.samples, key=lambda x: (x["ann_file"], x["frame_ids"][0]))
        self.samples = sorted(self.samples, key=lambda x: (x["ann_file"], x["frame_ids"][0]))
        # 中文说明：根据条件选择执行分支；代码：if debug and not do_evaluate:
        if debug and not do_evaluate:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.samples = self.samples[0:10]
            self.samples = self.samples[0:10]
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"{len(self.ann_files)} trajectories in total")
        print(f"{len(self.ann_files)} trajectories in total")
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"{len(self.samples)} samples in total")
        print(f"{len(self.samples)} samples in total")
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# with open('./samples_16.pkl','wb') as file:
        # with open('./samples_16.pkl','wb') as file:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# pickle.dump(self.samples,file)
        #     pickle.dump(self.samples,file)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.wrong_number = 0
        self.wrong_number = 0
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.transform = T.Compose([T.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5], inplace=Tr...
        self.transform = T.Compose([T.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5], inplace=True)])
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.training = False
        self.training = False
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.preprocess = T.Compose(
        self.preprocess = T.Compose(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：[
            [
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ToTensorVideo(),
                ToTensorVideo(),
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：Resize_Preprocess(tuple(video_size)), # 288 512
                Resize_Preprocess(tuple(video_size)),  # 288 512
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：T.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5], inplace=True),
                T.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5], inplace=True),
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
            ]
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.not_norm_preprocess = T.Compose([ToTensorVideo(), Resize_Preprocess(tuple(video_size))])
        self.not_norm_preprocess = T.Compose([ToTensorVideo(), Resize_Preprocess(tuple(video_size))])

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __str__(self):
    def __str__(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return f"{len(self.ann_files)} samples from {self.data_path}"
        return f"{len(self.ann_files)} samples from {self.data_path}"

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _init_anns(self, data_dir):
    def _init_anns(self, data_dir):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ann_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(".json")]
        ann_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(".json")]
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return ann_files
        return ann_files

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _init_sequences(self, ann_files):
    def _init_sequences(self, ann_files):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：samples = []
        samples = []
        # 中文说明：处理异常、清理资源或管理上下文；代码：with ThreadPoolExecutor(32) as executor:
        with ThreadPoolExecutor(32) as executor:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：future_to_ann_file = {
            future_to_ann_file = {
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：executor.submit(self._load_and_process_ann_file, ann_file): ann_file for ann_file in ann_files
                executor.submit(self._load_and_process_ann_file, ann_file): ann_file for ann_file in ann_files
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
            }
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for future in tqdm(as_completed(future_to_ann_file), total=len(ann_files)):
            for future in tqdm(as_completed(future_to_ann_file), total=len(ann_files)):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：samples.extend(future.result())
                samples.extend(future.result())
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return samples
        return samples

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _load_and_process_ann_file(self, ann_file):
    def _load_and_process_ann_file(self, ann_file):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：samples = []
        samples = []
        # 中文说明：处理异常、清理资源或管理上下文；代码：with open(ann_file, "r") as f:
        with open(ann_file, "r") as f:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ann = json.load(f)
            ann = json.load(f)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_frames = len(ann["state"])
        n_frames = len(ann["state"])
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for frame_i in range(0, n_frames, self.start_frame_interval):
        for frame_i in range(0, n_frames, self.start_frame_interval):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sample = dict()
            sample = dict()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sample["ann_file"] = ann_file
            sample["ann_file"] = ann_file
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sample["frame_ids"] = []
            sample["frame_ids"] = []
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_frame_i = frame_i
            curr_frame_i = frame_i
            # 中文说明：在条件成立时重复执行循环体；代码：while True:
            while True:
                # 中文说明：根据条件选择执行分支；代码：if curr_frame_i > (n_frames - 1):
                if curr_frame_i > (n_frames - 1):
                    # 中文说明：执行循环控制或空操作；代码：break
                    break
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sample["frame_ids"].append(curr_frame_i)
                sample["frame_ids"].append(curr_frame_i)
                # 中文说明：根据条件选择执行分支；代码：if len(sample["frame_ids"]) == self.sequence_length:
                if len(sample["frame_ids"]) == self.sequence_length:
                    # 中文说明：执行循环控制或空操作；代码：break
                    break
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_frame_i += self.sequence_interval
                curr_frame_i += self.sequence_interval
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# make sure there are sequence_length number of frames
            # make sure there are sequence_length number of frames
            # 中文说明：根据条件选择执行分支；代码：if len(sample["frame_ids"]) == self.sequence_length:
            if len(sample["frame_ids"]) == self.sequence_length:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：samples.append(sample)
                samples.append(sample)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return samples
        return samples

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __len__(self):
    def __len__(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return len(self.samples)
        return len(self.samples)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _load_video(self, video_path, frame_ids):
    def _load_video(self, video_path, frame_ids):
        # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from decord import VideoReader, cpu # Importing here due to malloc errors on ARM when importi...
        from decord import VideoReader, cpu # Importing here due to malloc errors on ARM when importing on top level
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：vr = VideoReader(video_path, ctx=cpu(0), num_threads=2)
        vr = VideoReader(video_path, ctx=cpu(0), num_threads=2)
        # 中文说明：检查运行时假设是否成立；代码：assert (np.array(frame_ids) < len(vr)).all()
        assert (np.array(frame_ids) < len(vr)).all()
        # 中文说明：检查运行时假设是否成立；代码：assert (np.array(frame_ids) >= 0).all()
        assert (np.array(frame_ids) >= 0).all()
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：vr.seek(0)
        vr.seek(0)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_data = vr.get_batch(frame_ids).asnumpy()
        frame_data = vr.get_batch(frame_ids).asnumpy()
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return frame_data
        return frame_data

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _get_frames(self, label, frame_ids, cam_id, pre_encode):
    def _get_frames(self, label, frame_ids, cam_id, pre_encode):
        # 中文说明：根据条件选择执行分支；代码：if pre_encode:
        if pre_encode:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise NotImplementedError("Pre-encoded videos are not supported for this dataset.")
            raise NotImplementedError("Pre-encoded videos are not supported for this dataset.")
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_path = label["videos"][cam_id]["video_path"]
            video_path = label["videos"][cam_id]["video_path"]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_path = os.path.join(self.video_path, video_path)
            video_path = os.path.join(self.video_path, video_path)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = self._load_video(video_path, frame_ids)
            frames = self._load_video(video_path, frame_ids)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = frames.astype(np.uint8)
            frames = frames.astype(np.uint8)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = torch.from_numpy(frames).permute(0, 3, 1, 2) # (l, c, h, w)
            frames = torch.from_numpy(frames).permute(0, 3, 1, 2)  # (l, c, h, w)

            # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def printvideo(videos, filename):
            def printvideo(videos, filename):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t_videos = rearrange(videos, "f c h w -> f h w c")
                t_videos = rearrange(videos, "f c h w -> f h w c")
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t_videos = (
                t_videos = (
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：((t_videos / 2.0 + 0.5).clamp(0, 1) * 255).detach().to(dtype=torch.uint8).cpu().contiguous()....
                    ((t_videos / 2.0 + 0.5).clamp(0, 1) * 255).detach().to(dtype=torch.uint8).cpu().contiguous().numpy()
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(t_videos.shape)
                print(t_videos.shape)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：writer = imageio.get_writer(filename, fps=4) # fps 是帧率
                writer = imageio.get_writer(filename, fps=4)  # 中文说明：fps 是帧率
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for frame in t_videos:
                for frame in t_videos:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：writer.append_data(frame) # 1 4 13 23 # fp16 24 76 456 688
                    writer.append_data(frame)  # 1 4 13 23 # fp16 24 76 456 688

            # 中文说明：根据条件选择执行分支；代码：if self.normalize:
            if self.normalize:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = self.preprocess(frames)
                frames = self.preprocess(frames)
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = self.not_norm_preprocess(frames)
                frames = self.not_norm_preprocess(frames)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = torch.clamp(frames * 255.0, 0, 255).to(torch.uint8)
                frames = torch.clamp(frames * 255.0, 0, 255).to(torch.uint8)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return frames
        return frames

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _get_obs(self, label, frame_ids, cam_id, pre_encode):
    def _get_obs(self, label, frame_ids, cam_id, pre_encode):
        # 中文说明：根据条件选择执行分支；代码：if cam_id is None:
        if cam_id is None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temp_cam_id = random.choice(self.cam_ids)
            temp_cam_id = random.choice(self.cam_ids)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temp_cam_id = cam_id
            temp_cam_id = cam_id
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = self._get_frames(label, frame_ids, cam_id=temp_cam_id, pre_encode=pre_encode)
        frames = self._get_frames(label, frame_ids, cam_id=temp_cam_id, pre_encode=pre_encode)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return frames, temp_cam_id
        return frames, temp_cam_id

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _get_robot_states(self, label, frame_ids):
    def _get_robot_states(self, label, frame_ids):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：all_states = np.array(label["state"])
        all_states = np.array(label["state"])
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：all_cont_gripper_states = np.array(label["continuous_gripper_state"])
        all_cont_gripper_states = np.array(label["continuous_gripper_state"])
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：states = all_states[frame_ids]
        states = all_states[frame_ids]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cont_gripper_states = all_cont_gripper_states[frame_ids]
        cont_gripper_states = all_cont_gripper_states[frame_ids]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：arm_states = states[:, :6]
        arm_states = states[:, :6]
        # 中文说明：检查运行时假设是否成立；代码：assert arm_states.shape[0] == self.sequence_length
        assert arm_states.shape[0] == self.sequence_length
        # 中文说明：检查运行时假设是否成立；代码：assert cont_gripper_states.shape[0] == self.sequence_length
        assert cont_gripper_states.shape[0] == self.sequence_length
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return arm_states, cont_gripper_states
        return arm_states, cont_gripper_states

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _get_all_robot_states(self, label, frame_ids):
    def _get_all_robot_states(self, label, frame_ids):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：all_states = np.array(label["state"])
        all_states = np.array(label["state"])
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：all_cont_gripper_states = np.array(label["continuous_gripper_state"])
        all_cont_gripper_states = np.array(label["continuous_gripper_state"])
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：states = all_states[frame_ids]
        states = all_states[frame_ids]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cont_gripper_states = all_cont_gripper_states[frame_ids]
        cont_gripper_states = all_cont_gripper_states[frame_ids]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：arm_states = states[:, :6]
        arm_states = states[:, :6]
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return arm_states, cont_gripper_states
        return arm_states, cont_gripper_states

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _get_all_actions(self, arm_states, gripper_states, accumulate_action):
    def _get_all_actions(self, arm_states, gripper_states, accumulate_action):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：action_num = arm_states.shape[0] - 1
        action_num = arm_states.shape[0] - 1
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：action = np.zeros((action_num, self.action_dim))
        action = np.zeros((action_num, self.action_dim))
        # 中文说明：根据条件选择执行分支；代码：if accumulate_action:
        if accumulate_action:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：first_xyz = arm_states[0, 0:3]
            first_xyz = arm_states[0, 0:3]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：first_rpy = arm_states[0, 3:6]
            first_rpy = arm_states[0, 3:6]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：first_rotm = euler2rotm(first_rpy)
            first_rotm = euler2rotm(first_rpy)
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for k in range(1, action_num + 1):
            for k in range(1, action_num + 1):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_xyz = arm_states[k, 0:3]
                curr_xyz = arm_states[k, 0:3]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_rpy = arm_states[k, 3:6]
                curr_rpy = arm_states[k, 3:6]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_gripper = gripper_states[k]
                curr_gripper = gripper_states[k]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_rotm = euler2rotm(curr_rpy)
                curr_rotm = euler2rotm(curr_rpy)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rel_xyz = np.dot(first_rotm.T, curr_xyz - first_xyz)
                rel_xyz = np.dot(first_rotm.T, curr_xyz - first_xyz)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rel_rotm = first_rotm.T @ curr_rotm
                rel_rotm = first_rotm.T @ curr_rotm
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rel_rpy = rotm2euler(rel_rotm)
                rel_rpy = rotm2euler(rel_rotm)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：action[k - 1, 0:3] = rel_xyz
                action[k - 1, 0:3] = rel_xyz
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：action[k - 1, 3:6] = rel_rpy
                action[k - 1, 3:6] = rel_rpy
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：action[k - 1, 6] = curr_gripper
                action[k - 1, 6] = curr_gripper
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for k in range(1, action_num + 1):
            for k in range(1, action_num + 1):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prev_xyz = arm_states[k - 1, 0:3]
                prev_xyz = arm_states[k - 1, 0:3]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prev_rpy = arm_states[k - 1, 3:6]
                prev_rpy = arm_states[k - 1, 3:6]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prev_rotm = euler2rotm(prev_rpy)
                prev_rotm = euler2rotm(prev_rpy)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_xyz = arm_states[k, 0:3]
                curr_xyz = arm_states[k, 0:3]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_rpy = arm_states[k, 3:6]
                curr_rpy = arm_states[k, 3:6]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_gripper = gripper_states[k]
                curr_gripper = gripper_states[k]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_rotm = euler2rotm(curr_rpy)
                curr_rotm = euler2rotm(curr_rpy)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rel_xyz = np.dot(prev_rotm.T, curr_xyz - prev_xyz)
                rel_xyz = np.dot(prev_rotm.T, curr_xyz - prev_xyz)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rel_rotm = prev_rotm.T @ curr_rotm
                rel_rotm = prev_rotm.T @ curr_rotm
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rel_rpy = rotm2euler(rel_rotm)
                rel_rpy = rotm2euler(rel_rotm)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：action[k - 1, 0:3] = rel_xyz
                action[k - 1, 0:3] = rel_xyz
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：action[k - 1, 3:6] = rel_rpy
                action[k - 1, 3:6] = rel_rpy
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：action[k - 1, 6] = curr_gripper
                action[k - 1, 6] = curr_gripper
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return torch.from_numpy(action) # (l - 1, act_dim)
        return torch.from_numpy(action)  # (l - 1, act_dim)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _get_actions(self, arm_states, gripper_states, accumulate_action):
    def _get_actions(self, arm_states, gripper_states, accumulate_action):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：action = np.zeros((self.sequence_length - 1, self.action_dim))
        action = np.zeros((self.sequence_length - 1, self.action_dim))
        # 中文说明：根据条件选择执行分支；代码：if accumulate_action:
        if accumulate_action:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：first_xyz = arm_states[0, 0:3]
            first_xyz = arm_states[0, 0:3]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：first_rpy = arm_states[0, 3:6]
            first_rpy = arm_states[0, 3:6]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：first_rotm = euler2rotm(first_rpy)
            first_rotm = euler2rotm(first_rpy)
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for k in range(1, self.sequence_length):
            for k in range(1, self.sequence_length):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_xyz = arm_states[k, 0:3]
                curr_xyz = arm_states[k, 0:3]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_rpy = arm_states[k, 3:6]
                curr_rpy = arm_states[k, 3:6]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_gripper = gripper_states[k]
                curr_gripper = gripper_states[k]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_rotm = euler2rotm(curr_rpy)
                curr_rotm = euler2rotm(curr_rpy)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rel_xyz = np.dot(first_rotm.T, curr_xyz - first_xyz)
                rel_xyz = np.dot(first_rotm.T, curr_xyz - first_xyz)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rel_rotm = first_rotm.T @ curr_rotm
                rel_rotm = first_rotm.T @ curr_rotm
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rel_rpy = rotm2euler(rel_rotm)
                rel_rpy = rotm2euler(rel_rotm)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：action[k - 1, 0:3] = rel_xyz
                action[k - 1, 0:3] = rel_xyz
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：action[k - 1, 3:6] = rel_rpy
                action[k - 1, 3:6] = rel_rpy
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：action[k - 1, 6] = curr_gripper
                action[k - 1, 6] = curr_gripper
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for k in range(1, self.sequence_length):
            for k in range(1, self.sequence_length):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prev_xyz = arm_states[k - 1, 0:3]
                prev_xyz = arm_states[k - 1, 0:3]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prev_rpy = arm_states[k - 1, 3:6]
                prev_rpy = arm_states[k - 1, 3:6]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prev_rotm = euler2rotm(prev_rpy)
                prev_rotm = euler2rotm(prev_rpy)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_xyz = arm_states[k, 0:3]
                curr_xyz = arm_states[k, 0:3]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_rpy = arm_states[k, 3:6]
                curr_rpy = arm_states[k, 3:6]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_gripper = gripper_states[k]
                curr_gripper = gripper_states[k]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_rotm = euler2rotm(curr_rpy)
                curr_rotm = euler2rotm(curr_rpy)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rel_xyz = np.dot(prev_rotm.T, curr_xyz - prev_xyz)
                rel_xyz = np.dot(prev_rotm.T, curr_xyz - prev_xyz)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rel_rotm = prev_rotm.T @ curr_rotm
                rel_rotm = prev_rotm.T @ curr_rotm
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rel_rpy = rotm2euler(rel_rotm)
                rel_rpy = rotm2euler(rel_rotm)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：action[k - 1, 0:3] = rel_xyz
                action[k - 1, 0:3] = rel_xyz
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：action[k - 1, 3:6] = rel_rpy
                action[k - 1, 3:6] = rel_rpy
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：action[k - 1, 6] = curr_gripper
                action[k - 1, 6] = curr_gripper
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return torch.from_numpy(action) # (l - 1, act_dim)
        return torch.from_numpy(action)  # (l - 1, act_dim)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __getitem__(self, index, cam_id=None, return_video=False):
    def __getitem__(self, index, cam_id=None, return_video=False):
        # 中文说明：根据条件选择执行分支；代码：if self.mode != "train":
        if self.mode != "train":
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：np.random.seed(index)
            np.random.seed(index)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：random.seed(index)
            random.seed(index)

        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sample = self.samples[index]
            sample = self.samples[index]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ann_file = sample["ann_file"]
            ann_file = sample["ann_file"]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_ids = sample["frame_ids"]
            frame_ids = sample["frame_ids"]
            # 中文说明：处理异常、清理资源或管理上下文；代码：with open(ann_file, "r") as f:
            with open(ann_file, "r") as f:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：label = json.load(f)
                label = json.load(f)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：arm_states, gripper_states = self._get_robot_states(label, frame_ids)
            arm_states, gripper_states = self._get_robot_states(label, frame_ids)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：actions = self._get_actions(arm_states, gripper_states, self.accumulate_action)
            actions = self._get_actions(arm_states, gripper_states, self.accumulate_action)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：actions *= self.c_act_scaler
            actions *= self.c_act_scaler

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data = dict()
            data = dict()
            # 中文说明：根据条件选择执行分支；代码：if self.load_action:
            if self.load_action:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["action"] = actions.float()
                data["action"] = actions.float()

            # 中文说明：根据条件选择执行分支；代码：if self.pre_encode:
            if self.pre_encode:
                # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise NotImplementedError("Pre-encoded videos are not supported for this dataset.")
                raise NotImplementedError("Pre-encoded videos are not supported for this dataset.")
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video, cam_id = self._get_obs(label, frame_ids, cam_id, pre_encode=False)
                video, cam_id = self._get_obs(label, frame_ids, cam_id, pre_encode=False)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = video.permute(1, 0, 2, 3) # Rearrange from [T, C, H, W] to [C, T, H, W]
                video = video.permute(1, 0, 2, 3)  # Rearrange from [T, C, H, W] to [C, T, H, W]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["video"] = video.to(dtype=torch.uint8)
                data["video"] = video.to(dtype=torch.uint8)

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["annotation_file"] = ann_file
            data["annotation_file"] = ann_file

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# NOTE: __key__ is used to uniquely identify the sample, required for callback functions
            # NOTE: __key__ is used to uniquely identify the sample, required for callback functions
            # 中文说明：根据条件选择执行分支；代码：if "episode_id" in label:
            if "episode_id" in label:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["__key__"] = label["episode_id"]
                data["__key__"] = label["episode_id"]
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["__key__"] = label["original_path"]
                data["__key__"] = label["original_path"]

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Just add these to fit the interface
            # Just add these to fit the interface
            # 中文说明：根据条件选择执行分支；代码：if self.load_t5_embeddings:
            if self.load_t5_embeddings:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t5_embeddings = np.squeeze(np.load(ann_file.replace(".json", ".npy")))
                t5_embeddings = np.squeeze(np.load(ann_file.replace(".json", ".npy")))
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["t5_text_embeddings"] = torch.from_numpy(t5_embeddings).cuda()
                data["t5_text_embeddings"] = torch.from_numpy(t5_embeddings).cuda()
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["t5_text_embeddings"] = torch.zeros(512, 1024, dtype=torch.bfloat16).cuda()
                data["t5_text_embeddings"] = torch.zeros(512, 1024, dtype=torch.bfloat16).cuda()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["t5_text_mask"] = torch.ones(512, dtype=torch.int64).cuda()
            data["t5_text_mask"] = torch.ones(512, dtype=torch.int64).cuda()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["fps"] = 4
            data["fps"] = 4
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["image_size"] = 256 * torch.ones(4).cuda() # TODO: Does this matter?
            data["image_size"] = 256 * torch.ones(4).cuda()  # TODO: Does this matter?
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["num_frames"] = self.sequence_length
            data["num_frames"] = self.sequence_length
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["padding_mask"] = torch.zeros(1, 256, 256).cuda()
            data["padding_mask"] = torch.zeros(1, 256, 256).cuda()

            # 中文说明：从当前函数返回结果或结束函数执行；代码：return data
            return data
        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception:
        except Exception:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：warnings.warn(
            warnings.warn(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Invalid data encountered: {self.samples[index]['ann_file']}. Skipped "
                f"Invalid data encountered: {self.samples[index]['ann_file']}. Skipped "
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"(by randomly sampling another sample in the same dataset)."
                f"(by randomly sampling another sample in the same dataset)."
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：warnings.warn("FULL TRACEBACK:")
            warnings.warn("FULL TRACEBACK:")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：warnings.warn(traceback.format_exc())
            warnings.warn(traceback.format_exc())
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.wrong_number += 1
            self.wrong_number += 1
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(self.wrong_number)
            print(self.wrong_number)
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return self[np.random.randint(len(self.samples))]
            return self[np.random.randint(len(self.samples))]