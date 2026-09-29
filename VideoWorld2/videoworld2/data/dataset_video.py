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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import pickle
import pickle
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import traceback
import traceback
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import warnings
import warnings

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from decord import VideoReader, cpu
from decord import VideoReader, cpu
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.utils.data import Dataset as BaseDataset
from torch.utils.data import Dataset as BaseDataset
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torchvision import transforms as T
from torchvision import transforms as T
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torchvision.transforms.v2 import UniformTemporalSubsample
from torchvision.transforms.v2 import UniformTemporalSubsample
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import random
import random
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.data.dataset_utils import Resize_Preprocess, ToTensorVideo, GeometricAugment...
from videoworld2.data.dataset_utils import Resize_Preprocess, ToTensorVideo, GeometricAugmentor, GeometricAugmentor_K
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from collections import defaultdict
from collections import defaultdict
# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
"""
Test the dataset with the following command:
python -m cosmos_predict2.data.dataset_video
"""


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Dataset(BaseDataset):
class Dataset(BaseDataset):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dataset_dir,
        dataset_dir,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_frames,
        num_frames,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video_size,
        video_size,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctrl_type=None,
        ctrl_type=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extra_video=False, #For LDM
        extra_video=False, #For LDM
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctrl_path="",
        ctrl_path="",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sample_way='uniform',
        sample_way='uniform',
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Dataset class for loading image-text-to-video generation data.
        """Dataset class for loading image-text-to-video generation data.

        Args:
            dataset_dir (str): Base path to the dataset directory
            num_frames (int): Number of frames to load per sequence
            video_size (list): Target size [H,W] for video frames

        Returns dict with:
            - video: RGB frames tensor [T,C,H,W]
            - video_name: Dict with episode/frame metadata
        """

        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dataset_dir = dataset_dir
        self.dataset_dir = dataset_dir
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.sequence_length = num_frames
        self.sequence_length = num_frames
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.sample_way = sample_way
        self.sample_way = sample_way

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_dir = os.path.join(self.dataset_dir, "videos") if 'cosmos_nemo_assets' in dataset_dir e...
        video_dir = os.path.join(self.dataset_dir, "videos") if 'cosmos_nemo_assets' in dataset_dir else self.dataset_dir
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.t5_dir = os.path.join(self.dataset_dir, "t5_xxl")
        self.t5_dir = os.path.join(self.dataset_dir, "t5_xxl")

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.video_paths = [os.path.join(video_dir, f) for f in os.listdir(video_dir) if f.endswith("...
        self.video_paths = [os.path.join(video_dir, f) for f in os.listdir(video_dir) if f.endswith(".mp4")]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.video_paths = sorted(self.video_paths)
        self.video_paths = sorted(self.video_paths)
       
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"{len(self.video_paths)} videos in total")
        log.info(f"{len(self.video_paths)} videos in total")

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.wrong_number = 0
        self.wrong_number = 0
       
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.preprocess = T.Compose([ToTensorVideo(), Resize_Preprocess(tuple(video_size))])
        self.preprocess = T.Compose([ToTensorVideo(), Resize_Preprocess(tuple(video_size))])

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.ctrl_type = ctrl_type
        self.ctrl_type = ctrl_type
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.extra_video = extra_video
        self.extra_video = extra_video
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.ctrl_path = ctrl_path
        self.ctrl_path = ctrl_path
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# if extra_video:
        # if extra_video:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extra_video_dict = defaultdict(list)
        extra_video_dict = defaultdict(list)
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for video_path in os.listdir(video_dir):
        for video_path in os.listdir(video_dir):
            # 中文说明：根据条件选择执行分支；代码：if not video_path.endswith(".mp4"):
            if not video_path.endswith(".mp4"):
                # 中文说明：执行循环控制或空操作；代码：continue
                continue
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_name = video_path.split('/')[-1]
            video_name = video_path.split('/')[-1]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prefix = '_'.join(video_name.split('_')[:3])
            prefix = '_'.join(video_name.split('_')[:3])
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：suffix = video_name.split('_')[-1].replace('.mp4', '')
            suffix = video_name.split('_')[-1].replace('.mp4', '')
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：extra_video_dict[prefix + '_' + suffix].append(os.path.join(video_dir, video_path))
            extra_video_dict[prefix + '_' + suffix].append(os.path.join(video_dir, video_path))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.extra_video_dict = extra_video_dict
        self.extra_video_dict = extra_video_dict
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __str__(self):
    def __str__(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return f"{len(self.video_paths)} samples from {self.dataset_dir}"
        return f"{len(self.video_paths)} samples from {self.dataset_dir}"

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __len__(self):
    def __len__(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return len(self.video_paths)
        return len(self.video_paths)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _load_video(self, video_path):
    def _load_video(self, video_path):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：vr = VideoReader(video_path, ctx=cpu(0), num_threads=2)
        vr = VideoReader(video_path, ctx=cpu(0), num_threads=2)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# frame_ids = np.linspace(0, len(vr) - 1).astype(np.int32)
        # frame_ids = np.linspace(0, len(vr) - 1).astype(np.int32)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_ids = np.arange(0, len(vr)).tolist()
        frame_ids = np.arange(0, len(vr)).tolist()
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：vr.seek(0)
        vr.seek(0)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_data = vr.get_batch(frame_ids).asnumpy()
        frame_data = vr.get_batch(frame_ids).asnumpy()
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fps = vr.get_avg_fps()
            fps = vr.get_avg_fps()
        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception: # failed to read FPS
        except Exception:  # failed to read FPS
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fps = 24
            fps = 24
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return frame_data, fps
        return frame_data, fps

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _get_frames(self, video_path):
    def _get_frames(self, video_path):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：frames, fps = self._load_video(video_path)
        frames, fps = self._load_video(video_path)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = frames.astype(np.uint8)
        frames = frames.astype(np.uint8)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = torch.from_numpy(frames).permute(0, 3, 1, 2) # (l, c, h, w)
        frames = torch.from_numpy(frames).permute(0, 3, 1, 2)  # (l, c, h, w)
        # 中文说明：根据条件选择执行分支；代码：if self.sample_way == 'uniform':
        if self.sample_way == 'uniform':
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = UniformTemporalSubsample(self.sequence_length)(frames)
            frames = UniformTemporalSubsample(self.sequence_length)(frames)
        # 中文说明：根据条件选择执行分支；代码：elif self.sample_way == 'random':
        elif self.sample_way == 'random':
            # 中文说明：根据条件选择执行分支；代码：if len(frames) > self.sequence_length:
            if len(frames) > self.sequence_length:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：start_idx = random.randint(0, len(frames) - self.sequence_length)
                start_idx = random.randint(0, len(frames) - self.sequence_length)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = frames[start_idx:start_idx + self.sequence_length]
                frames = frames[start_idx:start_idx + self.sequence_length]
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = frames[:self.sequence_length]
                frames = frames[:self.sequence_length]
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = frames[:self.sequence_length]
            frames = frames[:self.sequence_length]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = self.preprocess(frames)
        frames = self.preprocess(frames)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = torch.clamp(frames * 255.0, 0, 255).to(torch.uint8)
        frames = torch.clamp(frames * 255.0, 0, 255).to(torch.uint8)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return frames, fps
        return frames, fps


    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _load_control_data(self, sample):
    def _load_control_data(self, sample):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctrl_data, fps = self._load_video(sample['ctrl_path'])
        ctrl_data, fps = self._load_video(sample['ctrl_path'])
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return ctrl_data
        return ctrl_data
        
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __getitem__(self, index):
    def __getitem__(self, index):
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
            # import pdb;pdb.set_trace()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data = dict()
            data = dict()
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video, fps = self._get_frames(self.video_paths[index])
            video, fps = self._get_frames(self.video_paths[index])
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = video.permute(1, 0, 2, 3) # Rearrange from [T, C, H, W] to [C, T, H, W]
            video = video.permute(1, 0, 2, 3)  # Rearrange from [T, C, H, W] to [C, T, H, W]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_path = self.video_paths[index]
            video_path = self.video_paths[index]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_name = video_path.split('/')[-1]
            video_name = video_path.split('/')[-1]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t5_embedding_path = os.path.join(
            t5_embedding_path = os.path.join(
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.t5_dir,
                self.t5_dir,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.path.basename(video_path).replace(".mp4", ".pickle"),
                os.path.basename(video_path).replace(".mp4", ".pickle"),
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["video"] = video
            data["video"] = video
            
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["video_name"] = {
            data["video_name"] = {
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："video_path": video_path,
                "video_path": video_path,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："t5_embedding_path": t5_embedding_path,
                "t5_embedding_path": t5_embedding_path,
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# "start_frame_id": '0',
                # "start_frame_id": '0',
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
            }

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# For LDM, Same dynamic but different apperance
            # For LDM, Same dynamic but different apperance
            # 中文说明：根据条件选择执行分支；代码：if self.extra_video:
            if self.extra_video:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prefix = '_'.join(video_name.split('_')[:3])
                prefix = '_'.join(video_name.split('_')[:3])
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：suffix = video_name.split('_')[-1].replace('.mp4', '')
                suffix = video_name.split('_')[-1].replace('.mp4', '')
                # 中文说明：开始一个可捕获异常的代码块；代码：try:
                try:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extra_video_path = random.choice(self.extra_video_dict[prefix + '_' + suffix])
                    extra_video_path = random.choice(self.extra_video_dict[prefix + '_' + suffix])
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：extra_video, _ = self._get_frames(extra_video_path)
                    extra_video, _ = self._get_frames(extra_video_path)
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extra_video = extra_video.permute(1, 0, 2, 3) # Rearrange from [T, C, H, W] to [C, T, H, W]
                    extra_video = extra_video.permute(1, 0, 2, 3)  # Rearrange from [T, C, H, W] to [C, T, H, W]
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["extra_video"] = extra_video
                    data["extra_video"] = extra_video
                # 中文说明：处理异常、清理资源或管理上下文；代码：except:
                except:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f'extra_video prefix: {prefix}, suffix:{suffix} not found')
                    log.info(f'extra_video prefix: {prefix}, suffix:{suffix} not found')

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Just add these to fit the interface
            # Just add these to fit the interface
            # 中文说明：开始一个可捕获异常的代码块；代码：try:
            try:
                # 中文说明：处理异常、清理资源或管理上下文；代码：with open(t5_embedding_path, "rb") as f:
                with open(t5_embedding_path, "rb") as f:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t5_embedding = pickle.load(f)[0] # [n_tokens, 1024]
                    t5_embedding = pickle.load(f)[0]  # [n_tokens, 1024]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_tokens = t5_embedding.shape[0]
                n_tokens = t5_embedding.shape[0]
                # 中文说明：根据条件选择执行分支；代码：if n_tokens < 512:
                if n_tokens < 512:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t5_embedding = np.concatenate(
                    t5_embedding = np.concatenate(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：[t5_embedding, np.zeros((512 - n_tokens, 1024), dtype=np.float32)], axis=0
                        [t5_embedding, np.zeros((512 - n_tokens, 1024), dtype=np.float32)], axis=0
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
            # 中文说明：处理异常、清理资源或管理上下文；代码：except:
            except:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t5_embedding = np.zeros((512, 1024), dtype=np.float32)
                t5_embedding = np.zeros((512, 1024), dtype=np.float32)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_tokens = 0
                n_tokens = 0
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t5_text_mask = torch.zeros(512, dtype=torch.int64)
            t5_text_mask = torch.zeros(512, dtype=torch.int64)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t5_text_mask[:n_tokens] = 1
            t5_text_mask[:n_tokens] = 1

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["t5_text_embeddings"] = torch.from_numpy(t5_embedding)
            data["t5_text_embeddings"] = torch.from_numpy(t5_embedding)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["t5_text_mask"] = t5_text_mask
            data["t5_text_mask"] = t5_text_mask
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["fps"] = fps
            data["fps"] = fps
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["image_size"] = torch.tensor([704, 1280, 704, 1280])
            data["image_size"] = torch.tensor([704, 1280, 704, 1280])
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["num_frames"] = self.sequence_length
            data["num_frames"] = self.sequence_length
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["padding_mask"] = torch.zeros(1, 704, 1280)
            data["padding_mask"] = torch.zeros(1, 704, 1280)

            # 中文说明：开始一个可捕获异常的代码块；代码：try:
            try:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：noise_path = f"{self.dataset_dir}/noise/" + video_name.replace(".mp4", '.npy')
                noise_path = f"{self.dataset_dir}/noise/" + video_name.replace(".mp4", '.npy')
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_noise = np.load(noise_path) # [n_tokens, 1024]
                video_noise = np.load(noise_path)  # [n_tokens, 1024]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_noise = torch.from_numpy(video_noise).permute(3, 0, 1, 2)
                video_noise = torch.from_numpy(video_noise).permute(3, 0, 1, 2)  
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["video_noise"] = video_noise
                data["video_noise"] = video_noise
            # 中文说明：处理异常、清理资源或管理上下文；代码：except:
            except:
                # 中文说明：执行循环控制或空操作；代码：pass
                pass

            # 中文说明：根据条件选择执行分支；代码：if self.ctrl_type is not None:
            if self.ctrl_type is not None:
                # 中文说明：根据条件选择执行分支；代码：if self.extra_video:
                if self.extra_video:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctrl_data = extra_video
                    ctrl_data = extra_video
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctrl_data, fps = self._get_frames(os.path.join(self.ctrl_path, video_name))
                    ctrl_data, fps = self._get_frames(os.path.join(self.ctrl_path, video_name))
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctrl_data = ctrl_data.permute(1, 0, 2, 3)
                    ctrl_data = ctrl_data.permute(1, 0, 2, 3)
    
                # 中文说明：根据条件选择执行分支；代码：if self.ctrl_type == 'depth':
                if self.ctrl_type == 'depth':
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["control_input_depth"] = ctrl_data
                    data["control_input_depth"] = ctrl_data
                # 中文说明：根据条件选择执行分支；代码：elif self.ctrl_type == 'recon_image':
                elif self.ctrl_type == 'recon_image':
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["recon_image"] = ctrl_data
                    data["recon_image"] = ctrl_data

            # 中文说明：从当前函数返回结果或结束函数执行；代码：return data
            return data
        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception:
        except Exception:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
            # import pdb;pdb.set_trace()
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：warnings.warn(
            warnings.warn(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Invalid data encountered: {self.video_paths[index]}. Skipped "
                f"Invalid data encountered: {self.video_paths[index]}. Skipped "
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
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(self.wrong_number, rank0_only=False)
            log.info(self.wrong_number, rank0_only=False)
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return self[np.random.randint(len(self.samples))]
            return self[np.random.randint(len(self.samples))]

# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class InferDataset(BaseDataset):
class InferDataset(BaseDataset):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dataset_dir,
        dataset_dir,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_frames,
        num_frames,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video_size,
        video_size,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctrl_type=None,
        ctrl_type=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctrl_path=""
        ctrl_path=""
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Dataset class for loading image-text-to-video generation data.
        """Dataset class for loading image-text-to-video generation data.

        Args:
            dataset_dir (str): Base path to the dataset directory
            num_frames (int): Number of frames to load per sequence
            video_size (list): Target size [H,W] for video frames

        Returns dict with:
            - video: RGB frames tensor [T,C,H,W]
            - video_name: Dict with episode/frame metadata
        """
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dataset_dir = dataset_dir
        self.dataset_dir = dataset_dir
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.sequence_length = num_frames
        self.sequence_length = num_frames
       
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_dir = os.path.join(self.dataset_dir, "videos") if 'cosmos_nemo_assets' in dataset_dir e...
        video_dir = os.path.join(self.dataset_dir, "videos") if 'cosmos_nemo_assets' in dataset_dir else self.dataset_dir
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.t5_dir = os.path.join(self.dataset_dir, "t5_xxl")
        self.t5_dir = os.path.join(self.dataset_dir, "t5_xxl")

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_names = defaultdict(list)
        video_names = defaultdict(list)
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for name in os.listdir(video_dir):
        for name in os.listdir(video_dir):
            # 中文说明：根据条件选择执行分支；代码：if not name.endswith(".mp4"):
            if not name.endswith(".mp4"):
                # 中文说明：执行循环控制或空操作；代码：continue
                continue
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# _name = "paper_airplane_"+name.split('_')[2]
            # _name = "paper_airplane_"+name.split('_')[2]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_name = '_'.join(name.split('_')[:-1])
            _name = '_'.join(name.split('_')[:-1])
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video_names[_name].append(os.path.join(video_dir, name))
            video_names[_name].append(os.path.join(video_dir, name))
        
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.video_paths = []
        self.video_paths = []
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for name in video_names:
        for name in video_names:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sorted_videos = sorted(video_names[name], key=lambda x: int(os.path.basename(x).split('_')[-1...
            sorted_videos = sorted(video_names[name], key=lambda x: int(os.path.basename(x).split('_')[-1].replace('.mp4', '')))
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.video_paths.append(sorted_videos)
            self.video_paths.append(sorted_videos)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"{len(self.video_paths)} videos in total")
        log.info(f"{len(self.video_paths)} videos in total")

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.wrong_number = 0
        self.wrong_number = 0
       
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.preprocess = T.Compose([ToTensorVideo(), Resize_Preprocess(tuple(video_size))])
        self.preprocess = T.Compose([ToTensorVideo(), Resize_Preprocess(tuple(video_size))])

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.ctrl_type = ctrl_type
        self.ctrl_type = ctrl_type
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.ctrl_path = ctrl_path
        self.ctrl_path = ctrl_path
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __str__(self):
    def __str__(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return f"{len(self.video_paths)} samples from {self.dataset_dir}"
        return f"{len(self.video_paths)} samples from {self.dataset_dir}"

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __len__(self):
    def __len__(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return len(self.video_paths)
        return len(self.video_paths)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _load_video(self, video_path):
    def _load_video(self, video_path):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：vr = VideoReader(video_path, ctx=cpu(0), num_threads=2)
        vr = VideoReader(video_path, ctx=cpu(0), num_threads=2)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# frame_ids = np.linspace(0, len(vr) - 1).astype(np.int32)
        # frame_ids = np.linspace(0, len(vr) - 1).astype(np.int32)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_ids = np.arange(0, len(vr)).tolist()
        frame_ids = np.arange(0, len(vr)).tolist()
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：vr.seek(0)
        vr.seek(0)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_data = vr.get_batch(frame_ids).asnumpy()
        frame_data = vr.get_batch(frame_ids).asnumpy()
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fps = vr.get_avg_fps()
            fps = vr.get_avg_fps()
        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception: # failed to read FPS
        except Exception:  # failed to read FPS
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fps = 24
            fps = 24
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return frame_data, fps
        return frame_data, fps

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _get_frames(self, video_path):
    def _get_frames(self, video_path):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：frames, fps = self._load_video(video_path)
        frames, fps = self._load_video(video_path)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = frames.astype(np.uint8)
        frames = frames.astype(np.uint8)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = torch.from_numpy(frames).permute(0, 3, 1, 2) # (l, c, h, w)
        frames = torch.from_numpy(frames).permute(0, 3, 1, 2)  # (l, c, h, w)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = UniformTemporalSubsample(self.sequence_length)(frames)
        frames = UniformTemporalSubsample(self.sequence_length)(frames)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = self.preprocess(frames)
        frames = self.preprocess(frames)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = torch.clamp(frames * 255.0, 0, 255).to(torch.uint8)
        frames = torch.clamp(frames * 255.0, 0, 255).to(torch.uint8)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return frames, fps
        return frames, fps


    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _load_control_data(self, sample):
    def _load_control_data(self, sample):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctrl_data, fps = self._load_video(sample['ctrl_path'])
        ctrl_data, fps = self._load_video(sample['ctrl_path'])
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return ctrl_data
        return ctrl_data
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __getitem__(self, index):
    def __getitem__(self, index):
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
            # import pdb;pdb.set_trace()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data = dict()
            data = dict()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_paths = self.video_paths[index]
            video_paths = self.video_paths[index]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：videos = []
            videos = []
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t5_embeddings = []
            t5_embeddings = []
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：control_input = []
            control_input = []
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_noises = []
            video_noises = []
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for video_path in video_paths:
            for video_path in video_paths:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video, fps = self._get_frames(video_path)
                video, fps = self._get_frames(video_path)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = video.permute(1, 0, 2, 3) # Rearrange from [T, C, H, W] to [C, T, H, W]
                video = video.permute(1, 0, 2, 3)  # Rearrange from [T, C, H, W] to [C, T, H, W]
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# video_path = self.video_paths[index]
                # video_path = self.video_paths[index]
            
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_name = video_path.split('/')[-1]
                video_name = video_path.split('/')[-1]
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# clip_index = video_name.split('_')[-2]
                # clip_index = video_name.split('_')[-2]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prefix = '_'.join(video_name.split('_')[:-1])
                prefix = '_'.join(video_name.split('_')[:-1])
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_video_name = f"{prefix}_0.mp4"
                _video_name = f"{prefix}_0.mp4"
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t5_embedding_path = os.path.join(
                t5_embedding_path = os.path.join(
                    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.t5_dir,
                    self.t5_dir,
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# os.path.basename(video_path).replace(".mp4", ".pickle"),
                    # os.path.basename(video_path).replace(".mp4", ".pickle"),
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_video_name.replace(".mp4", ".pickle"),
                    _video_name.replace(".mp4", ".pickle"),
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Just add these to fit the interface
                # Just add these to fit the interface
                # 中文说明：开始一个可捕获异常的代码块；代码：try:
                try:
                    # 中文说明：处理异常、清理资源或管理上下文；代码：with open(t5_embedding_path, "rb") as f:
                    with open(t5_embedding_path, "rb") as f:
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t5_embedding = pickle.load(f)[0] # [n_tokens, 1024]
                        t5_embedding = pickle.load(f)[0]  # [n_tokens, 1024]
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_tokens = t5_embedding.shape[0]
                    n_tokens = t5_embedding.shape[0]
                    # 中文说明：根据条件选择执行分支；代码：if n_tokens < 512:
                    if n_tokens < 512:
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t5_embedding = np.concatenate(
                        t5_embedding = np.concatenate(
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：[t5_embedding, np.zeros((512 - n_tokens, 1024), dtype=np.float32)], axis=0
                            [t5_embedding, np.zeros((512 - n_tokens, 1024), dtype=np.float32)], axis=0
                        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                        )
                # 中文说明：处理异常、清理资源或管理上下文；代码：except:
                except:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t5_embedding = np.zeros((512, 1024), dtype=np.float32)
                    t5_embedding = np.zeros((512, 1024), dtype=np.float32)

                # 中文说明：开始一个可捕获异常的代码块；代码：try:
                try:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：noise_path = f"{self.dataset_dir}/noise/" + video_name.replace(".mp4", '.npy')
                    noise_path = f"{self.dataset_dir}/noise/" + video_name.replace(".mp4", '.npy')
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_noise = np.load(noise_path) # [n_tokens, 1024]
                    video_noise = np.load(noise_path)  # [n_tokens, 1024]
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_noise = torch.from_numpy(video_noise).permute(3, 0, 1, 2)
                    video_noise = torch.from_numpy(video_noise).permute(3, 0, 1, 2)  
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video_noises.append(video_noise)
                    video_noises.append(video_noise)
                # 中文说明：处理异常、清理资源或管理上下文；代码：except:
                except:
                    # 中文说明：执行循环控制或空操作；代码：pass
                    pass

                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t5_embedding = torch.from_numpy(t5_embedding)
                t5_embedding = torch.from_numpy(t5_embedding)
                # 中文说明：根据条件选择执行分支；代码：if self.ctrl_type is not None:
                if self.ctrl_type is not None:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ctrl_data, fps = self._get_frames(os.path.join(self.ctrl_path, video_name))
                    ctrl_data, fps = self._get_frames(os.path.join(self.ctrl_path, video_name))
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctrl_data = ctrl_data.permute(1, 0, 2, 3)
                    ctrl_data = ctrl_data.permute(1, 0, 2, 3)
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：control_input.append(ctrl_data)
                    control_input.append(ctrl_data)

                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：videos.append(video)
                videos.append(video)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：t5_embeddings.append(t5_embedding)
                t5_embeddings.append(t5_embedding)
                

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = torch.stack(videos, dim=0)
            video = torch.stack(videos, dim=0) 
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t5_embedding = torch.stack(t5_embeddings, dim=0)
            t5_embedding = torch.stack(t5_embeddings, dim=0)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["video"] = video
            data["video"] = video
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["video_name"] = {
            data["video_name"] = {
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："video_path": video_path,
                "video_path": video_path,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："t5_embedding_path": t5_embedding_path,
                "t5_embedding_path": t5_embedding_path,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
            }
            # 中文说明：根据条件选择执行分支；代码：if len(video_noises) > 0:
            if len(video_noises) > 0:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["video_noise"] = torch.stack(video_noises, dim=0)
                data["video_noise"] = torch.stack(video_noises, dim=0)
            # 中文说明：根据条件选择执行分支；代码：if len(control_input) > 0:
            if len(control_input) > 0:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：control_input = torch.stack(control_input, dim=0)
                control_input = torch.stack(control_input, dim=0)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["recon_image"] = control_input
                data["recon_image"] = control_input
            
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t5_text_mask = torch.zeros(512, dtype=torch.int64)
            t5_text_mask = torch.zeros(512, dtype=torch.int64)
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# t5_text_mask[:n_tokens] = 1
            # t5_text_mask[:n_tokens] = 1

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["t5_text_embeddings"] = t5_embedding
            data["t5_text_embeddings"] = t5_embedding
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["t5_text_mask"] = t5_text_mask
            data["t5_text_mask"] = t5_text_mask
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["fps"] = fps
            data["fps"] = fps
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["image_size"] = torch.tensor([704, 1280, 704, 1280])
            data["image_size"] = torch.tensor([704, 1280, 704, 1280])
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["num_frames"] = self.sequence_length
            data["num_frames"] = self.sequence_length
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["padding_mask"] = torch.zeros(1, 704, 1280)
            data["padding_mask"] = torch.zeros(1, 704, 1280)            

            # 中文说明：从当前函数返回结果或结束函数执行；代码：return data
            return data
        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception:
        except Exception:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：warnings.warn(
            warnings.warn(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Invalid data encountered: {self.video_paths[index]}. Skipped "
                f"Invalid data encountered: {self.video_paths[index]}. Skipped "
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
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(self.wrong_number, rank0_only=False)
            log.info(self.wrong_number, rank0_only=False)
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return self[np.random.randint(len(self.samples))]
            return self[np.random.randint(len(self.samples))]


# 中文说明：根据条件选择执行分支；代码：if __name__ == "__main__":
if __name__ == "__main__":
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset = InferDataset(
    dataset = InferDataset(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset_dir="/opt/tiger/PointVIS/VideoWorld_Cosmos_Predict/datasets/HowTo100M/task_vid/paper_...
        dataset_dir="/opt/tiger/PointVIS/VideoWorld_Cosmos_Predict/datasets/HowTo100M/task_vid/paper_airplane_allstep/boat_complex_0",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_frames=93,
        num_frames=93,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_size=[480, 832],
        video_size=[480, 832],
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# extra_video=True
        # extra_video=True
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import random
    import random
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：indices = [random.choice(range(len(dataset))) for _ in range(100)]
    indices = [random.choice(range(len(dataset))) for _ in range(100)]
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for idx in indices:
    for idx in indices:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data = dataset[idx]
        data = dataset[idx]
        # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import pdb;pdb.set_trace()
        import pdb;pdb.set_trace()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# log.info(
        # log.info(
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# (
        #     (
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# f"{idx=} "
        #         f"{idx=} "
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# f"{data['video'].sum()=}\n"
        #         f"{data['video'].sum()=}\n"
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# f"{data['video'].shape=}\n"
        #         f"{data['video'].shape=}\n"
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# f"{data['video_name']=}\n"
        #         f"{data['video_name']=}\n"
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# f"{data['t5_text_embeddings'].shape=}\n"
        #         f"{data['t5_text_embeddings'].shape=}\n"
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# "---"
        #         "---"
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# )
        #     )
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# )
        # )