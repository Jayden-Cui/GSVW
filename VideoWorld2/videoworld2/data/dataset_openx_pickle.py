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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.utils.data import Dataset
from torch.utils.data import Dataset
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torchvision import transforms as T
from torchvision import transforms as T
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torchvision.transforms.v2 import UniformTemporalSubsample
from torchvision.transforms.v2 import UniformTemporalSubsample
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import warnings
import warnings
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import traceback
import traceback
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from PIL import Image
from PIL import Image
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import random
import random
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import io
import io
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import json
import json
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from tqdm import tqdm
from tqdm import tqdm
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import cv2
import cv2
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from decord import VideoReader, cpu
from decord import VideoReader, cpu

# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class PreserveAspectRatioResize:
class PreserveAspectRatioResize:
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, size, antialias=True):
    def __init__(self, size, antialias=True):
       
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.size = size
        self.size = size
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.antialias = antialias
        self.antialias = antialias
    
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, img):
    def __call__(self, img):

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_, h, w = img.shape
        _, h, w = img.shape
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：target_h, target_w = self.size
        target_h, target_w = self.size
        

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scale = min(target_h / h, target_w / w)
        scale = min(target_h / h, target_w / w)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：new_h, new_w = int(h * scale), int(w * scale)
        new_h, new_w = int(h * scale), int(w * scale)
        

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resized = T.Resize((new_h, new_w), antialias=self.antialias)(img)
        resized = T.Resize((new_h, new_w), antialias=self.antialias)(img)
        
       
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：result = torch.zeros((3, target_h, target_w), dtype=img.dtype)
        result = torch.zeros((3, target_h, target_w), dtype=img.dtype)
        

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：y_start = (target_h - new_h) // 2
        y_start = (target_h - new_h) // 2
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_start = (target_w - new_w) // 2
        x_start = (target_w - new_w) // 2
        

        # 中文说明：根据条件选择执行分支；代码：if new_h <= target_h and new_w <= target_w:
        if new_h <= target_h and new_w <= target_w:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：result[:, y_start:y_start+new_h, x_start:x_start+new_w] = resized
            result[:, y_start:y_start+new_h, x_start:x_start+new_w] = resized

        # 中文说明：根据条件选择执行分支；代码：else:
        else:
 
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：y_crop_start = (new_h - target_h) // 2
            y_crop_start = (new_h - target_h) // 2
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_crop_start = (new_w - target_w) // 2
            x_crop_start = (new_w - target_w) // 2
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cropped = resized[:, y_crop_start:y_crop_start+target_h, x_crop_start:x_crop_start+target_w]
            cropped = resized[:, y_crop_start:y_crop_start+target_h, x_crop_start:x_crop_start+target_w]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：result = cropped
            result = cropped
        
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return result
        return result

# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class RandomResizeStrategy:
class RandomResizeStrategy:
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, size, antialias=True, aspect_ratio_prob=0.5):
    def __init__(self, size, antialias=True, aspect_ratio_prob=0.5):

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.size = size
        self.size = size
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.antialias = antialias
        self.antialias = antialias
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.aspect_ratio_prob = aspect_ratio_prob
        self.aspect_ratio_prob = aspect_ratio_prob
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.preserve_aspect_ratio_transform = PreserveAspectRatioResize(size, antialias)
        self.preserve_aspect_ratio_transform = PreserveAspectRatioResize(size, antialias)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.direct_resize_transform = T.Resize(size, antialias=True)
        self.direct_resize_transform = T.Resize(size, antialias=True)
    
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, img, keep_aspect_ratio=True):
    def __call__(self, img, keep_aspect_ratio=True):

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.direct_resize_transform(img)
        return self.direct_resize_transform(img)



# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def save_video_as_gif(video_tensor, save_path, fps=24):
def save_video_as_gif(video_tensor, save_path, fps=24):

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：save_dir = os.path.dirname(save_path)
    save_dir = os.path.dirname(save_path)
    # 中文说明：根据条件选择执行分支；代码：if save_dir and not os.path.exists(save_dir):
    if save_dir and not os.path.exists(save_dir):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.makedirs(save_dir)
        os.makedirs(save_dir)
    

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：images = []
    images = []

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_np = video_tensor.permute(1, 2, 3, 0).numpy()
    video_np = video_tensor.permute(1, 2, 3, 0).numpy()
    
    # 中文说明：根据条件选择执行分支；代码：if video_np.max() <= 1.1:
    if video_np.max() <= 1.1:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_np = (video_np * 255).astype(np.uint8)
        video_np = (video_np * 255).astype(np.uint8)
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_np = video_np.astype(np.uint8)
        video_np = video_np.astype(np.uint8)
    
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for frame in video_np:
    for frame in video_np:

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：img = Image.fromarray(frame)
        img = Image.fromarray(frame)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：images.append(img)
        images.append(img)
    

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：duration = int(1000 / fps)
    duration = int(1000 / fps)  
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：images[0].save(
    images[0].save(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：save_path,
        save_path,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：save_all=True,
        save_all=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：append_images=images[1:],
        append_images=images[1:],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：duration=duration,
        duration=duration,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：loop=0
        loop=0  
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"GIF has been saved to: {save_path}")
    print(f"GIF has been saved to: {save_path}")


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def save_video_as_frames(video_tensor, save_dir, frame_prefix="frame_", format="png"):
def save_video_as_frames(video_tensor, save_dir, frame_prefix="frame_", format="png"):

    # 中文说明：根据条件选择执行分支；代码：if save_dir and not os.path.exists(save_dir):
    if save_dir and not os.path.exists(save_dir):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.makedirs(save_dir)
        os.makedirs(save_dir)
    

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_np = video_tensor.permute(1, 2, 3, 0).numpy()
    video_np = video_tensor.permute(1, 2, 3, 0).numpy()
    

    # 中文说明：根据条件选择执行分支；代码：if video_np.max() <= 1.1:
    if video_np.max() <= 1.1:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_np = (video_np * 255).astype(np.uint8)
        video_np = (video_np * 255).astype(np.uint8)
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_np = video_np.astype(np.uint8)
        video_np = video_np.astype(np.uint8)
    

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：total_frames = video_np.shape[0]
    total_frames = video_np.shape[0]
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i, frame in enumerate(video_np):
    for i, frame in enumerate(video_np):

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：img = Image.fromarray(frame)
        img = Image.fromarray(frame)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：filename = f"{frame_prefix}{i:04d}.{format}"
        filename = f"{frame_prefix}{i:04d}.{format}"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：file_path = os.path.join(save_dir, filename)
        file_path = os.path.join(save_dir, filename)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：img.save(file_path)
        img.save(file_path)
    
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"The total number of frames ({total_frames}) has been saved to the directory: {save_di...
    print(f"The total number of frames ({total_frames}) has been saved to the directory: {save_dir}")





# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def generate_folder_frame_meta(dataset_dir, output_meta_path='./folder_frame_meta.json', imag...
def generate_folder_frame_meta(dataset_dir, output_meta_path='./folder_frame_meta.json', image_keys=None, sample_size=50):

    # 中文说明：根据条件选择执行分支；代码：if image_keys is None:
    if image_keys is None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：image_keys = ['image', 'rgb', 'front_rgb', 'hand_image', 'image_1', 'rgb_static', 'agentview_...
        image_keys = ['image', 'rgb', 'front_rgb', 'hand_image', 'image_1', 'rgb_static', 'agentview_rgb']
    
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：folder_frame_meta = {
    folder_frame_meta = {
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：'dataset_dir': dataset_dir,
        'dataset_dir': dataset_dir,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：'timestamp': str(np.datetime64('now')),
        'timestamp': str(np.datetime64('now')),
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：'subfolders': {}
        'subfolders': {}
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
    }
    
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for subfolder in tqdm(os.listdir(dataset_dir)):
    for subfolder in tqdm(os.listdir(dataset_dir)):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：subfolder_path = os.path.join(dataset_dir, subfolder)
        subfolder_path = os.path.join(dataset_dir, subfolder)
        
        # 中文说明：根据条件选择执行分支；代码：if not os.path.isdir(subfolder_path):
        if not os.path.isdir(subfolder_path):
            # 中文说明：执行循环控制或空操作；代码：continue
            continue
        
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"Counting frames in the subfolder {subfolder}...")
        print(f"Counting frames in the subfolder {subfolder}...")
        
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pickle_files = []
        pickle_files = []
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for file in os.listdir(subfolder_path):
        for file in os.listdir(subfolder_path):
            # 中文说明：根据条件选择执行分支；代码：if file.endswith('.pickle') or file.endswith('.pkl'):
            if file.endswith('.pickle') or file.endswith('.pkl'):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pickle_files.append(os.path.join(subfolder_path, file))
                pickle_files.append(os.path.join(subfolder_path, file))
        
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：total_files = len(pickle_files)
        total_files = len(pickle_files)
        
        # 中文说明：根据条件选择执行分支；代码：if total_files == 0:
        if total_files == 0:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：folder_frame_meta['subfolders'][subfolder] = {
            folder_frame_meta['subfolders'][subfolder] = {
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：'total_files': 0,
                'total_files': 0,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：'estimated_total_frames': 0,
                'estimated_total_frames': 0,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：'frames_per_file': 0
                'frames_per_file': 0
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
            }
            # 中文说明：执行循环控制或空操作；代码：continue
            continue
        
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sampled_files = random.sample(pickle_files, min(sample_size, total_files)) if total_files > 0...
        sampled_files = random.sample(pickle_files, min(sample_size, total_files)) if total_files > 0 else []
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：total_sampled_frames = 0
        total_sampled_frames = 0
        
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for file_path in sampled_files:
        for file_path in sampled_files:
            # 中文说明：开始一个可捕获异常的代码块；代码：try:
            try:
                # 中文说明：处理异常、清理资源或管理上下文；代码：with open(file_path, 'rb') as f:
                with open(file_path, 'rb') as f:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data = pickle.load(f)
                    data = pickle.load(f)
                
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：steps_key = None
                steps_key = None
                # 中文说明：根据条件选择执行分支；代码：if 'steps' in data:
                if 'steps' in data:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：steps_key = 'steps'
                    steps_key = 'steps'
                # 中文说明：根据条件选择执行分支；代码：elif 'step' in data:
                elif 'step' in data:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：steps_key = 'step'
                    steps_key = 'step'
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：执行循环控制或空操作；代码：continue
                    continue
                
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：steps = data[steps_key]
                steps = data[steps_key]
                # 中文说明：根据条件选择执行分支；代码：if not steps or not isinstance(steps, list):
                if not steps or not isinstance(steps, list):
                    # 中文说明：执行循环控制或空操作；代码：continue
                    continue
                
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：file_frames = 0
                file_frames = 0
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for step in steps:
                for step in steps:
                    # 中文说明：根据条件选择执行分支；代码：if not isinstance(step, dict) or 'observation' not in step:
                    if not isinstance(step, dict) or 'observation' not in step:
                        # 中文说明：执行循环控制或空操作；代码：continue
                        continue
                    
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：observation = step['observation']
                    observation = step['observation']
                    # 中文说明：根据条件选择执行分支；代码：if not isinstance(observation, dict):
                    if not isinstance(observation, dict):
                        # 中文说明：执行循环控制或空操作；代码：continue
                        continue
                    
        
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：has_valid_image = False
                    has_valid_image = False
                    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key in image_keys:
                    for key in image_keys:
                        # 中文说明：根据条件选择执行分支；代码：if key in observation:
                        if key in observation:
                            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：image_data = observation[key]
                            image_data = observation[key]
                            # 中文说明：根据条件选择执行分支；代码：if isinstance(image_data, bytes) or isinstance(image_data, np.ndarray):
                            if isinstance(image_data, bytes) or isinstance(image_data, np.ndarray):
                                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：has_valid_image = True
                                has_valid_image = True
                                # 中文说明：执行循环控制或空操作；代码：break
                                break
                    
                    # 中文说明：根据条件选择执行分支；代码：if has_valid_image:
                    if has_valid_image:
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：file_frames += 1
                        file_frames += 1
                
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：total_sampled_frames += file_frames
                total_sampled_frames += file_frames
            # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
            except Exception as e:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：warnings.warn(f"Error when processing {file_path}: {str(e)}")
                warnings.warn(f"Error when processing {file_path}: {str(e)}")
                # 中文说明：执行循环控制或空操作；代码：continue
                continue
        
        # 中文说明：根据条件选择执行分支；代码：if len(sampled_files) > 0:
        if len(sampled_files) > 0:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：avg_frames_per_file = total_sampled_frames / len(sampled_files)
            avg_frames_per_file = total_sampled_frames / len(sampled_files)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：estimated_total_frames = avg_frames_per_file * total_files
            estimated_total_frames = avg_frames_per_file * total_files
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：avg_frames_per_file = 100
            avg_frames_per_file = 100
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：estimated_total_frames = 100 * total_files
            estimated_total_frames = 100 * total_files
        

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：folder_frame_meta['subfolders'][subfolder] = {
        folder_frame_meta['subfolders'][subfolder] = {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：'total_files': total_files,
            'total_files': total_files,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：'sampled_files': len(sampled_files),
            'sampled_files': len(sampled_files),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：'frames_per_file': avg_frames_per_file,
            'frames_per_file': avg_frames_per_file,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：'estimated_total_frames': estimated_total_frames
            'estimated_total_frames': estimated_total_frames
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }
    
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.makedirs(os.path.dirname(output_meta_path), exist_ok=True)
    os.makedirs(os.path.dirname(output_meta_path), exist_ok=True)
    # 中文说明：处理异常、清理资源或管理上下文；代码：with open(output_meta_path, 'w', encoding='utf-8') as f:
    with open(output_meta_path, 'w', encoding='utf-8') as f:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：json.dump(folder_frame_meta, f, ensure_ascii=False, indent=2)
        json.dump(folder_frame_meta, f, ensure_ascii=False, indent=2)
    
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"The subfolder frame count statistics have been saved to: {output_meta_path}")
    print(f"The subfolder frame count statistics have been saved to: {output_meta_path}")
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return folder_frame_meta
    return folder_frame_meta


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class EnhancedOpenXPickleDataset(Dataset):
class EnhancedOpenXPickleDataset(Dataset):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset_dir="datasets/openx_untar/",
        dataset_dir="datasets/openx_untar/",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_frames=93,
        num_frames=93,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_size=[256, 256],
        video_size=[256, 256],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：subfolders=None,
        subfolders=None, 
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctrl_type=None,
        ctrl_type=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extra_video=False,
        extra_video=False,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ctrl_path="",
        ctrl_path="",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：aspect_ratio_prob=0.5,
        aspect_ratio_prob=0.5,  
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：image_keys=None,
        image_keys=None,  
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：meta_path="datasets/openx_videocraft_meta.json",
        meta_path="datasets/openx_videocraft_meta.json",  
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_frame_based_sampling=True,
        use_frame_based_sampling=True,  
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_path=None,
        cache_path=None,  
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_cache=True,
        use_cache=True,  
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_interval=1,
        frame_interval=1,  
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_infer_mode=False,
        is_infer_mode=False, 
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fps_variation=True
        fps_variation=True  
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dataset_dir = dataset_dir
        self.dataset_dir = dataset_dir
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.sequence_length = num_frames
        self.sequence_length = num_frames
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.video_size = video_size
        self.video_size = video_size
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.subfolders = subfolders
        self.subfolders = subfolders
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.ctrl_type = ctrl_type
        self.ctrl_type = ctrl_type
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.extra_video = extra_video
        self.extra_video = extra_video
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.ctrl_path = ctrl_path
        self.ctrl_path = ctrl_path
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.aspect_ratio_prob = aspect_ratio_prob
        self.aspect_ratio_prob = aspect_ratio_prob
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.use_frame_based_sampling = use_frame_based_sampling
        self.use_frame_based_sampling = use_frame_based_sampling
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.use_cache = use_cache
        self.use_cache = use_cache
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.frame_interval = frame_interval
        self.frame_interval = frame_interval  
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.is_infer_mode = is_infer_mode
        self.is_infer_mode = is_infer_mode
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.fps_variation = fps_variation
        self.fps_variation = fps_variation  
        
        # 中文说明：根据条件选择执行分支；代码：if cache_path is None:
        if cache_path is None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset_name = os.path.basename(os.path.normpath(dataset_dir))
            dataset_name = os.path.basename(os.path.normpath(dataset_dir))
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：subfolder_suffix = "_" + "_" .join(subfolders) if subfolders else "all"
            subfolder_suffix = "_" + "_" .join(subfolders) if subfolders else "all"
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_filename = f"pickle_paths_cache_{dataset_name}_{subfolder_suffix}.json"
            cache_filename = f"pickle_paths_cache_{dataset_name}_{subfolder_suffix}.json"
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), cache_filename)
            cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), cache_filename)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.cache_path = cache_path
        self.cache_path = cache_path
        
  
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.image_keys = image_keys if image_keys else [
        self.image_keys = image_keys if image_keys else [
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：'image', 'rgb', 'front_rgb', 'hand_image', 'image_1', 'rgb_static', 'agentview_rgb'
            'image', 'rgb', 'front_rgb', 'hand_image', 'image_1', 'rgb_static', 'agentview_rgb'
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
        ]
        

        # 中文说明：根据条件选择执行分支；代码：if meta_path is None:
        if meta_path is None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：meta_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'folder_frame_meta.json')
            meta_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'folder_frame_meta.json')
        

        # 中文说明：根据条件选择执行分支；代码：if os.path.exists(meta_path):
        if os.path.exists(meta_path):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"Loading meta dictionary: {meta_path}")
            print(f"Loading meta dictionary: {meta_path}")
            # 中文说明：处理异常、清理资源或管理上下文；代码：with open(meta_path, 'r', encoding='utf-8') as f:
            with open(meta_path, 'r', encoding='utf-8') as f:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.folder_meta = json.load(f)
                self.folder_meta = json.load(f)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"Meta dictionary does not exist, generating: {meta_path}")
            print(f"Meta dictionary does not exist, generating: {meta_path}")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.folder_meta = generate_folder_frame_meta(
            self.folder_meta = generate_folder_frame_meta(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dataset_dir,
                dataset_dir, 
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_meta_path=meta_path,
                output_meta_path=meta_path, 
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：image_keys=self.image_keys
                image_keys=self.image_keys
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.pickle_paths = []
        self.pickle_paths = []
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.pickle_paths_by_folder = {}
        self.pickle_paths_by_folder = {}

        # 中文说明：根据条件选择执行分支；代码：if self.use_cache and os.path.exists(self.cache_path):
        if self.use_cache and os.path.exists(self.cache_path):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"Loading file paths from cache: {self.cache_path}")
            print(f"Loading file paths from cache: {self.cache_path}")
            # 中文说明：开始一个可捕获异常的代码块；代码：try:
            try:
                # 中文说明：处理异常、清理资源或管理上下文；代码：with open(self.cache_path, 'r', encoding='utf-8') as f:
                with open(self.cache_path, 'r', encoding='utf-8') as f:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_data = json.load(f)
                    cache_data = json.load(f)

                    # 中文说明：根据条件选择执行分支；代码：if self.subfolders and 'pickle_paths_by_folder' in cache_data:
                    if self.subfolders and 'pickle_paths_by_folder' in cache_data:
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.pickle_paths_by_folder = {}
                        self.pickle_paths_by_folder = {}
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.pickle_paths = []
                        self.pickle_paths = []
                        
             
                        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for subfolder in self.subfolders:
                        for subfolder in self.subfolders:
            
                            # 中文说明：根据条件选择执行分支；代码：if subfolder in cache_data['pickle_paths_by_folder']:
                            if subfolder in cache_data['pickle_paths_by_folder']:
                     
                                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：folder_files = cache_data['pickle_paths_by_folder'][subfolder]
                                folder_files = cache_data['pickle_paths_by_folder'][subfolder]
                                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.pickle_paths_by_folder[subfolder] = folder_files
                                self.pickle_paths_by_folder[subfolder] = folder_files
                                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.pickle_paths.extend(folder_files)
                                self.pickle_paths.extend(folder_files)
                                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"Loaded {len(folder_files)} file paths from cache for subfolder {subfolder}")
                                print(f"Loaded {len(folder_files)} file paths from cache for subfolder {subfolder}")
                    # 中文说明：根据条件选择执行分支；代码：else:
                    else:
                        
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.pickle_paths = cache_data['pickle_paths']
                        self.pickle_paths = cache_data['pickle_paths']
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.pickle_paths_by_folder = cache_data.get('pickle_paths_by_folder', {})
                        self.pickle_paths_by_folder = cache_data.get('pickle_paths_by_folder', {})
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"Successfully loaded {len(self.pickle_paths)} file paths from cache")
                        print(f"Successfully loaded {len(self.pickle_paths)} file paths from cache")
            # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
            except Exception as e:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"Failed to load from cache: {str(e)}")
                print(f"Failed to load from cache: {str(e)}")
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print("Re-collecting file paths")
                print("Re-collecting file paths")
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._collect_pickle_files()
                self._collect_pickle_files()
        # 中文说明：根据条件选择执行分支；代码：else:
        else:

            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._collect_pickle_files()
            self._collect_pickle_files()
        
 
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.preprocess = T.Compose([
        self.preprocess = T.Compose([
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：T.ToTensor(),
            T.ToTensor(),  
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：RandomResizeStrategy(tuple(video_size), antialias=True, aspect_ratio_prob=aspect_ratio_prob)
            RandomResizeStrategy(tuple(video_size), antialias=True, aspect_ratio_prob=aspect_ratio_prob)
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：])
        ])
        

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.folder_probs = None
        self.folder_probs = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.folder_list = None
        self.folder_list = None
        # 中文说明：根据条件选择执行分支；代码：if self.use_frame_based_sampling:
        if self.use_frame_based_sampling:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._compute_sampling_probs()
            self._compute_sampling_probs()
        
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"{len(self.pickle_paths)} pickle files loaded")
        print(f"{len(self.pickle_paths)} pickle files loaded")
    
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _load_single_frame(self, pkl_data, frame_idx):
    def _load_single_frame(self, pkl_data, frame_idx):
        
    
        # 中文说明：根据条件选择执行分支；代码：if 'obs_images' in pkl_data:
        if 'obs_images' in pkl_data:
            
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = pkl_data['obs_images'].permute(1, 0, 2, 3) # [C, T_original, H, W]
            video = pkl_data['obs_images'].permute(1, 0, 2, 3)  # [C, T_original, H, W]
            
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = video.permute(1, 0, 2, 3) # [T_original, C, H, W]
            video = video.permute(1, 0, 2, 3)  # [T_original, C, H, W]
            
           
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for frame_tensor in video:
            for frame_tensor in video:
    
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_np = frame_tensor.permute(1, 2, 0).numpy()
                frame_np = frame_tensor.permute(1, 2, 0).numpy()
                # 中文说明：根据条件选择执行分支；代码：if frame_np.max() <= 1.0:
                if frame_np.max() <= 1.0:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_np = (frame_np * 255).astype(np.uint8)
                    frame_np = (frame_np * 255).astype(np.uint8)
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_np = frame_np.astype(np.uint8)
                    frame_np = frame_np.astype(np.uint8)
                
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：image = Image.fromarray(frame_np)
            image = Image.fromarray(frame_np)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：steps_key = None
            steps_key = None
            # 中文说明：根据条件选择执行分支；代码：if 'steps' in pkl_data:
            if 'steps' in pkl_data:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：steps_key = 'steps'
                steps_key = 'steps'
            # 中文说明：根据条件选择执行分支；代码：elif 'step' in pkl_data:
            elif 'step' in pkl_data:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：steps_key = 'step'
                steps_key = 'step'
            
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：empty_image = Image.new('RGB', (self.video_size[1], self.video_size[0]), color='white')
            empty_image = Image.new('RGB', (self.video_size[1], self.video_size[0]), color='white')
            # 中文说明：根据条件选择执行分支；代码：if steps_key:
            if steps_key:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：steps = pkl_data[steps_key]
                steps = pkl_data[steps_key]
                # 中文说明：根据条件选择执行分支；代码：if steps and isinstance(steps, list):
                if steps and isinstance(steps, list):
       
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：step = steps[frame_idx]
                    step = steps[frame_idx]
                    
                    # 中文说明：开始一个可捕获异常的代码块；代码：try:
                    try:
      
                        # 中文说明：根据条件选择执行分支；代码：if not isinstance(step, dict) or 'observation' not in step:
                        if not isinstance(step, dict) or 'observation' not in step:
                            # 中文说明：从当前函数返回结果或结束函数执行；代码：return empty_image
                            return empty_image
                        
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：observation = step['observation']
                        observation = step['observation']
                        # 中文说明：根据条件选择执行分支；代码：if not isinstance(observation, dict):
                        if not isinstance(observation, dict):
                            # 中文说明：从当前函数返回结果或结束函数执行；代码：return empty_image
                            return empty_image
                        
     
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：image_bytes = None
                        image_bytes = None
                        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key in self.image_keys:
                        for key in self.image_keys:
                            # 中文说明：根据条件选择执行分支；代码：if key in observation:
                            if key in observation:
                                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：image_bytes = observation[key]
                                image_bytes = observation[key]
                                # 中文说明：执行循环控制或空操作；代码：break
                                break
                        
                        # 中文说明：根据条件选择执行分支；代码：if image_bytes is None:
                        if image_bytes is None:
            
                            # 中文说明：从当前函数返回结果或结束函数执行；代码：return empty_image
                            return empty_image
                        
       
                        # 中文说明：开始一个可捕获异常的代码块；代码：try:
                        try:
                            # 中文说明：根据条件选择执行分支；代码：if isinstance(image_bytes, bytes):
                            if isinstance(image_bytes, bytes):
                               
                                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：image = Image.open(io.BytesIO(image_bytes))
                                image = Image.open(io.BytesIO(image_bytes))
                            # 中文说明：根据条件选择执行分支；代码：elif isinstance(image_bytes, np.ndarray):
                            elif isinstance(image_bytes, np.ndarray):
                                
                                # 中文说明：根据条件选择执行分支；代码：if image_bytes.max() <= 1.0:
                                if image_bytes.max() <= 1.0:
                                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：image_bytes = (image_bytes * 255).astype(np.uint8)
                                    image_bytes = (image_bytes * 255).astype(np.uint8)
                                # 中文说明：根据条件选择执行分支；代码：else:
                                else:
                                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：image_bytes = image_bytes.astype(np.uint8)
                                    image_bytes = image_bytes.astype(np.uint8)
                                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：image = Image.fromarray(image_bytes)
                                image = Image.fromarray(image_bytes)
                            # 中文说明：根据条件选择执行分支；代码：else:
                            else:
                                # 中文说明：从当前函数返回结果或结束函数执行；代码：return empty_image
                                return empty_image
                            
                        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception:
                        except Exception:
                            # 中文说明：从当前函数返回结果或结束函数执行；代码：return empty_image
                            return empty_image
                    # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception:
                    except Exception:
                        # 中文说明：从当前函数返回结果或结束函数执行；代码：return empty_image
                        return empty_image
      
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return image
        return image

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _collect_pickle_files(self):
    def _collect_pickle_files(self):
        
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for subfolder in tqdm(os.listdir(self.dataset_dir)):
        for subfolder in tqdm(os.listdir(self.dataset_dir)):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"Load {subfolder}")
            print(f"Load {subfolder}")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：subfolder_path = os.path.join(self.dataset_dir, subfolder)
            subfolder_path = os.path.join(self.dataset_dir, subfolder)
            

            # 中文说明：根据条件选择执行分支；代码：if not os.path.isdir(subfolder_path):
            if not os.path.isdir(subfolder_path):
                # 中文说明：执行循环控制或空操作；代码：continue
                continue
            
            # 中文说明：根据条件选择执行分支；代码：if self.subfolders is not None and subfolder not in self.subfolders:
            if self.subfolders is not None and subfolder not in self.subfolders:
                # 中文说明：执行循环控制或空操作；代码：continue
                continue
            
           
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：folder_files = []
            folder_files = []
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for file in os.listdir(subfolder_path):
            for file in os.listdir(subfolder_path):
                # 中文说明：根据条件选择执行分支；代码：if file.endswith('.pickle') or file.endswith('.pkl'):
                if file.endswith('.pickle') or file.endswith('.pkl'):
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：file_path = os.path.join(subfolder_path, file)
                    file_path = os.path.join(subfolder_path, file)
                    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.pickle_paths.append(file_path)
                    self.pickle_paths.append(file_path)
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：folder_files.append(file_path)
                    folder_files.append(file_path)
            

            # 中文说明：根据条件选择执行分支；代码：if folder_files:
            if folder_files:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.pickle_paths_by_folder[subfolder] = folder_files
                self.pickle_paths_by_folder[subfolder] = folder_files
        

        # 中文说明：根据条件选择执行分支；代码：if self.use_cache:
        if self.use_cache:
            # 中文说明：开始一个可捕获异常的代码块；代码：try:
            try:

                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
                os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
                

                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_data = {
                cache_data = {
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：'pickle_paths': self.pickle_paths,
                    'pickle_paths': self.pickle_paths,
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：'pickle_paths_by_folder': self.pickle_paths_by_folder,
                    'pickle_paths_by_folder': self.pickle_paths_by_folder,
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：'timestamp': str(np.datetime64('now')),
                    'timestamp': str(np.datetime64('now')),
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：'dataset_dir': self.dataset_dir,
                    'dataset_dir': self.dataset_dir,
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：'subfolders': self.subfolders
                    'subfolders': self.subfolders
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
                }
                
                # 中文说明：处理异常、清理资源或管理上下文；代码：with open(self.cache_path, 'w', encoding='utf-8') as f:
                with open(self.cache_path, 'w', encoding='utf-8') as f:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：json.dump(cache_data, f, ensure_ascii=False, indent=2)
                    json.dump(cache_data, f, ensure_ascii=False, indent=2)
                
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"File paths have been saved to cache: {self.cache_path}")
                print(f"File paths have been saved to cache: {self.cache_path}")
            # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
            except Exception as e:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"Failed to save cache: {str(e)}")
                print(f"Failed to save cache: {str(e)}")

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _compute_sampling_probs(self):
    def _compute_sampling_probs(self):

        # 中文说明：根据条件选择执行分支；代码：if not hasattr(self, 'folder_meta') or 'subfolders' not in self.folder_meta:
        if not hasattr(self, 'folder_meta') or 'subfolders' not in self.folder_meta:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print("Warning: No valid folder_meta data available, unable to perform frame-based sampling")
            print("Warning: No valid folder_meta data available, unable to perform frame-based sampling")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.use_frame_based_sampling = False
            self.use_frame_based_sampling = False
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return
            return

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.folder_list = []
        self.folder_list = []
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：folder_frames = []
        folder_frames = []
        
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for subfolder, folder_files in self.pickle_paths_by_folder.items():
        for subfolder, folder_files in self.pickle_paths_by_folder.items():
            # 中文说明：根据条件选择执行分支；代码：if folder_files and subfolder in self.folder_meta['subfolders']:
            if folder_files and subfolder in self.folder_meta['subfolders']:
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.folder_list.append(subfolder)
                self.folder_list.append(subfolder)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：folder_frames.append(self.folder_meta['subfolders'][subfolder]['estimated_total_frames'])
                folder_frames.append(self.folder_meta['subfolders'][subfolder]['estimated_total_frames'])
        
  
        # 中文说明：根据条件选择执行分支；代码：if folder_frames:
        if folder_frames:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：total_frames = sum(folder_frames)
            total_frames = sum(folder_frames)
            # 中文说明：根据条件选择执行分支；代码：if total_frames > 0:
            if total_frames > 0:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.folder_probs = [frames / total_frames for frames in folder_frames]
                self.folder_probs = [frames / total_frames for frames in folder_frames]
                # 中文说明：从当前函数返回结果或结束函数执行；代码：return
                return
        
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print("Warning: Unable to compute frame-based sampling probabilities, falling back to uniform...
        print("Warning: Unable to compute frame-based sampling probabilities, falling back to uniform distribution")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.folder_probs = None
        self.folder_probs = None
    
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __len__(self):
    def __len__(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return len(self.pickle_paths)
        return len(self.pickle_paths)
    
    

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __getitem__(self, index):
    def __getitem__(self, index):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：selected_folder = ''
        selected_folder = ''
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data = dict()
            data = dict()
            # 中文说明：根据条件选择执行分支；代码：if self.use_frame_based_sampling and self.folder_list and self.folder_probs:
            if self.use_frame_based_sampling and self.folder_list and self.folder_probs:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：np.random.seed(index)
                np.random.seed(index)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：random.seed(index)
                random.seed(index)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：selected_folder = np.random.choice(self.folder_list, p=self.folder_probs)
                selected_folder = np.random.choice(self.folder_list, p=self.folder_probs)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：selected_file = random.choice(self.pickle_paths_by_folder[selected_folder])
                selected_file = random.choice(self.pickle_paths_by_folder[selected_folder])
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：selected_file = self.pickle_paths[index]
                selected_file = self.pickle_paths[index]
            
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = []
            frames = []
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_mp4 = False
            is_mp4 = False
            # 中文说明：根据条件选择执行分支；代码：if selected_file.endswith('.mp4'):
            if selected_file.endswith('.mp4'):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：vr = VideoReader(selected_file, ctx=cpu(0), num_threads=2)
                vr = VideoReader(selected_file, ctx=cpu(0), num_threads=2)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_ids = np.arange(0, len(vr)).tolist()
                frame_ids = np.arange(0, len(vr)).tolist()
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_ids = frame_ids[::2]
                frame_ids = frame_ids[::2]
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：vr.seek(0)
                vr.seek(0)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_data = vr.get_batch(frame_ids).asnumpy()
                frame_data = vr.get_batch(frame_ids).asnumpy()
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for frame in frame_data:
                for frame in frame_data:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pil_image = Image.fromarray(frame)
                    pil_image = Image.fromarray(frame)
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：frames.append(pil_image)
                    frames.append(pil_image)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_mp4 = True
                is_mp4 = True
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：original_length = len(frames)
                original_length = len(frames)
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：处理异常、清理资源或管理上下文；代码：with open(selected_file, 'rb') as f:
                with open(selected_file, 'rb') as f:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pkl_data = pickle.load(f)
                    pkl_data = pickle.load(f)

                # 中文说明：根据条件选择执行分支；代码：if 'obs_images' in pkl_data:
                if 'obs_images' in pkl_data:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：original_length = pkl_data['obs_images'].shape[0]
                    original_length = pkl_data['obs_images'].shape[0]
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：original_length = len(pkl_data['steps'])
                    original_length = len(pkl_data['steps'])

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = [i for i in range(original_length)] if not is_mp4 else frames
            frames = [i for i in range(original_length)] if not is_mp4 else frames
            # 中文说明：根据条件选择执行分支；代码：if self.is_infer_mode:
            if self.is_infer_mode:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：all_clips = []
                all_clips = []
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：all_t5_embeddings = []
                all_t5_embeddings = []
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：all_t5_masks = []
                all_t5_masks = []
                
              
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_clips = 0
                num_clips = 0
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：current_start = 0
                current_start = 0
                # 中文说明：在条件成立时重复执行循环体；代码：while True:
                while True:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：current_end = current_start + self.sequence_length
                    current_end = current_start + self.sequence_length
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_clips += 1
                    num_clips += 1
                   
                    # 中文说明：根据条件选择执行分支；代码：if current_end - 1 < original_length:
                    if current_end - 1 < original_length:
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：current_start = current_end - 1
                        current_start = current_end - 1  
                    # 中文说明：根据条件选择执行分支；代码：else:
                    else:
                        # 中文说明：执行循环控制或空操作；代码：break
                        break
                
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：clip_ranges = []
                clip_ranges = []
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：current_start = 0
                current_start = 0
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _ in range(num_clips):
                for _ in range(num_clips):
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：current_end = current_start + self.sequence_length
                    current_end = current_start + self.sequence_length
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：clip_ranges.append((current_start, current_end))
                    clip_ranges.append((current_start, current_end))
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：current_start = current_end - 1
                    current_start = current_end - 1 
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for start_idx, end_idx in clip_ranges:
                for start_idx, end_idx in clip_ranges:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：actual_end = min(end_idx, original_length)
                    actual_end = min(end_idx, original_length)
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：clip_frames = frames[start_idx:actual_end]
                    clip_frames = frames[start_idx:actual_end]
                    
                    # 中文说明：根据条件选择执行分支；代码：if len(clip_frames) < self.sequence_length:
                    if len(clip_frames) < self.sequence_length:
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pad_length = self.sequence_length - len(clip_frames)
                        pad_length = self.sequence_length - len(clip_frames)
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：last_frame = clip_frames[-1] if clip_frames else Image.new('RGB', (self.video_size[1], self.v...
                        last_frame = clip_frames[-1] if clip_frames else Image.new('RGB', (self.video_size[1], self.video_size[0]), color='white')
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：clip_frames += [last_frame for _ in range(pad_length)]
                        clip_frames += [last_frame for _ in range(pad_length)]
                    
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：processed_clip = []
                    processed_clip = []
                    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for frame in clip_frames:
                    for frame in clip_frames:
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：processed = self.preprocess(frame)
                        processed = self.preprocess(frame)
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：processed_clip.append(processed)
                        processed_clip.append(processed)
                    
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：clip_video = torch.stack(processed_clip).permute(1, 0, 2, 3)
                    clip_video = torch.stack(processed_clip).permute(1, 0, 2, 3)
                    # 中文说明：根据条件选择执行分支；代码：if clip_video.max() < 1.5:
                    if clip_video.max() < 1.5:
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：clip_video = torch.clamp(clip_video, 0, 1)
                        clip_video = torch.clamp(clip_video, 0, 1)
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：clip_video = (clip_video * 255).to(torch.uint8)
                    clip_video = (clip_video * 255).to(torch.uint8)
                    
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：all_clips.append(clip_video)
                    all_clips.append(clip_video)
                
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = torch.stack(all_clips)
                video = torch.stack(all_clips)
                
        
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：instruction = ""
                instruction = ""
                
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t5_embedding = np.zeros((512, 1024), dtype=np.float32)
                t5_embedding = np.zeros((512, 1024), dtype=np.float32)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_tokens = 0
                n_tokens = 0  
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t5_text_mask = torch.zeros(512, dtype=torch.int64)
                t5_text_mask = torch.zeros(512, dtype=torch.int64)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t5_text_mask[:n_tokens] = 1
                t5_text_mask[:n_tokens] = 1
                
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t5_embeddings = [torch.from_numpy(t5_embedding) for _ in range(num_clips)]
                t5_embeddings = [torch.from_numpy(t5_embedding) for _ in range(num_clips)]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t5_masks = [t5_text_mask.clone() for _ in range(num_clips)]
                t5_masks = [t5_text_mask.clone() for _ in range(num_clips)]
                
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["t5_text_embeddings"] = torch.stack(t5_embeddings)
                data["t5_text_embeddings"] = torch.stack(t5_embeddings)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["t5_text_mask"] = torch.stack(t5_masks)
                data["t5_text_mask"] = torch.stack(t5_masks)
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_start_idx = 0
                min_start_idx = 0  
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_start_idx = max(0, original_length - 30)
                max_start_idx = max(0, original_length - 30) 
                
                # 中文说明：根据条件选择执行分支；代码：if min_start_idx <= max_start_idx:
                if min_start_idx <= max_start_idx:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：start_idx = random.randint(min_start_idx, max_start_idx)
                    start_idx = random.randint(min_start_idx, max_start_idx)
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：start_idx = 0
                    start_idx = 0 
                
                
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# start_idx = 0
                # start_idx = 0
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
                # import pdb;pdb.set_trace()
                # 中文说明：根据条件选择执行分支；代码：if is_mp4 or original_length < self.sequence_length:
                if is_mp4 or original_length < self.sequence_length:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：start_idx = 0
                    start_idx = 0
                # 中文说明：根据条件选择执行分支；代码：if is_mp4:
                if is_mp4:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(selected_file, start_idx)
                    print(selected_file, start_idx)

                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sampled_frames = []
                sampled_frames = []

                # 中文说明：根据条件选择执行分支；代码：if self.fps_variation and self.sequence_length > 1:
                if self.fps_variation and self.sequence_length > 1:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fps_scale = random.uniform(0.25, 1.0)
                    fps_scale = random.uniform(0.25, 1.0)
                    
                    # 中文说明：根据条件选择执行分支；代码：if fps_scale <= 0.5:
                    if fps_scale <= 0.5:
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：remaining_frames = self.sequence_length - 1
                        remaining_frames = self.sequence_length - 1
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group_size = int(1 / fps_scale)
                        group_size = int(1 / fps_scale)
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups = (remaining_frames + group_size - 1) // group_size
                        num_groups = (remaining_frames + group_size - 1) // group_size
                        
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：current_idx = start_idx
                        current_idx = start_idx
                        # 中文说明：根据条件选择执行分支；代码：if current_idx < original_length:
                        if current_idx < original_length:
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sampled_frames.append(frames[current_idx])
                            sampled_frames.append(frames[current_idx])
                            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：current_idx += self.frame_interval
                            current_idx += self.frame_interval
                        
                       
                        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i in range(num_groups):
                        for i in range(num_groups):
                            # 中文说明：根据条件选择执行分支；代码：if current_idx < original_length:
                            if current_idx < original_length:
                               
                                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：current_frame = frames[current_idx]
                                current_frame = frames[current_idx]
                                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames_to_add = min(group_size, self.sequence_length - len(sampled_frames))
                                frames_to_add = min(group_size, self.sequence_length - len(sampled_frames))
                                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sampled_frames.extend([current_frame for _ in range(frames_to_add)])
                                sampled_frames.extend([current_frame for _ in range(frames_to_add)])
                                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：current_idx += self.frame_interval
                                current_idx += self.frame_interval
                    # 中文说明：根据条件选择执行分支；代码：else:
                    else:
                
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：adjusted_interval = max(1, int(self.frame_interval / fps_scale))
                        adjusted_interval = max(1, int(self.frame_interval / fps_scale))
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：current_idx = start_idx
                        current_idx = start_idx
                        # 中文说明：在条件成立时重复执行循环体；代码：while len(sampled_frames) < self.sequence_length and current_idx < original_length:
                        while len(sampled_frames) < self.sequence_length and current_idx < original_length:
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sampled_frames.append(frames[current_idx])
                            sampled_frames.append(frames[current_idx])
                            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：current_idx += adjusted_interval
                            current_idx += adjusted_interval

                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：current_idx = start_idx
                    current_idx = start_idx
                    # 中文说明：在条件成立时重复执行循环体；代码：while len(sampled_frames) < self.sequence_length and current_idx < original_length:
                    while len(sampled_frames) < self.sequence_length and current_idx < original_length:
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sampled_frames.append(frames[current_idx])
                        sampled_frames.append(frames[current_idx])
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：current_idx += self.frame_interval
                        current_idx += self.frame_interval
                
                # 中文说明：根据条件选择执行分支；代码：if len(sampled_frames) < self.sequence_length:
                if len(sampled_frames) < self.sequence_length:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pad_length = self.sequence_length - len(sampled_frames)
                    pad_length = self.sequence_length - len(sampled_frames)
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：last_frame = frames[-1:] if frames else [Image.new('RGB', (self.video_size[1], self.video_siz...
                    last_frame = frames[-1:] if frames else [Image.new('RGB', (self.video_size[1], self.video_size[0]), color='white')]
                    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _ in range(pad_length):
                    for _ in range(pad_length):
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sampled_frames.append(last_frame[0])
                        sampled_frames.append(last_frame[0])
                
                # 中文说明：根据条件选择执行分支；代码：if self.sequence_length == 2 and len(sampled_frames) >= 2:
                if self.sequence_length == 2 and len(sampled_frames) >= 2:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：first_frame = sampled_frames[0]
                    first_frame = sampled_frames[0]
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：second_frame = sampled_frames[1]
                    second_frame = sampled_frames[1]
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sampled_frames = [first_frame] + [second_frame for _ in range(4)]
                    sampled_frames = [first_frame] + [second_frame for _ in range(4)]
                
                # 中文说明：根据条件选择执行分支；代码：if not is_mp4:
                if not is_mp4:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_sampled_frames = sampled_frames
                    _sampled_frames = sampled_frames
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sampled_frames = []
                    sampled_frames = []
                    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for idx in _sampled_frames:
                    for idx in _sampled_frames:
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_frame = self._load_single_frame(pkl_data, idx)
                        _frame = self._load_single_frame(pkl_data, idx)
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sampled_frames.append(_frame)
                        sampled_frames.append(_frame)


                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：processed_frames = []
                processed_frames = []
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：keep_aspect_ratio = random.random() < 0.5
                keep_aspect_ratio = random.random() < 0.5
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for frame in sampled_frames:
                for frame in sampled_frames:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：processed = self.preprocess(frame)
                    processed = self.preprocess(frame)
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：processed_frames.append(processed)
                    processed_frames.append(processed)
                

                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = torch.stack(processed_frames).permute(1, 0, 2, 3)
                video = torch.stack(processed_frames).permute(1, 0, 2, 3)
                # 中文说明：根据条件选择执行分支；代码：if video.max() < 1.5:
                if video.max() < 1.5:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = torch.clamp(video, 0, 1)
                    video = torch.clamp(video, 0, 1)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = (video * 255).to(torch.uint8)
                video = (video * 255).to(torch.uint8)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data['selected_folder'] = selected_folder
            data['selected_folder'] = selected_folder 
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["video"] = video
            data["video"] = video
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["video_name"] = {
            data["video_name"] = {
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："video_path": selected_file,
                "video_path": selected_file,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："start_idx": start_idx,
                "start_idx": start_idx,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："t5_embedding_path": selected_file.replace('.pkl', '.pickle').replace('.pickle', '.pickle'),
                "t5_embedding_path": selected_file.replace('.pkl', '.pickle').replace('.pickle', '.pickle'),
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
            }
            

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：instruction = ""
            instruction = ""
            
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
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["fps"] = 24
            data["fps"] = 24 
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["image_size"] = torch.tensor([self.video_size[0], self.video_size[1], self.video_size[0]...
            data["image_size"] = torch.tensor([self.video_size[0], self.video_size[1], self.video_size[0], self.video_size[1]])
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["num_frames"] = self.sequence_length
            data["num_frames"] = self.sequence_length
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["padding_mask"] = torch.zeros(1, self.video_size[0], self.video_size[1])
            data["padding_mask"] = torch.zeros(1, self.video_size[0], self.video_size[1])
            

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# data["robot_and_gripper"] = pkl_data.get('robot_and_gripper', [])
            # data["robot_and_gripper"] = pkl_data.get('robot_and_gripper', [])
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data["instruction"] = instruction
            data["instruction"] = instruction
            
  
            # 中文说明：根据条件选择执行分支；代码：if self.ctrl_type is not None:
            if self.ctrl_type is not None:
                # 中文说明：执行循环控制或空操作；代码：pass
                pass
            
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return data
            return data
            
        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
        except Exception as e:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：warnings.warn(f"Invalid data encountered: {self.pickle_paths[index] if index < len(self.pickl...
            warnings.warn(f"Invalid data encountered: {self.pickle_paths[index] if index < len(self.pickle_paths) else 'unknown path'}. Skipped.")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：warnings.warn(f"Error: {str(e)}")
            warnings.warn(f"Error: {str(e)}")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：warnings.warn("FULL TRACEBACK:")
            warnings.warn("FULL TRACEBACK:")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：warnings.warn(traceback.format_exc())
            warnings.warn(traceback.format_exc())
            
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return self[np.random.randint(len(self))]
            return self[np.random.randint(len(self))]


# 中文说明：根据条件选择执行分支；代码：if __name__ == "__main__":
if __name__ == "__main__":  

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
    # import pdb;pdb.set_trace()
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset = EnhancedOpenXPickleDataset(
    dataset = EnhancedOpenXPickleDataset(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_size=[240, 416],
        video_size=[240, 416],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：aspect_ratio_prob=0.5,
        aspect_ratio_prob=0.5, 
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_frames=93,
        num_frames=93,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_frame_based_sampling=True,
        use_frame_based_sampling=True, 
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_cache=True,
        use_cache=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_path="datasets/openx_videocraft_cache.json",
        cache_path="datasets/openx_videocraft_cache.json",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：meta_path="datasets/openx_videocraft_meta.json",
        meta_path="datasets/openx_videocraft_meta.json",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_interval=1,
        frame_interval=1,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：subfolders=['bridge'],
        subfolders=['bridge'],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_infer_mode=False,
        is_infer_mode=False,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fps_variation=False
        fps_variation=False        

    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"Dataset size: {len(dataset)}")
    print(f"Dataset size: {len(dataset)}")
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i in range(100):
    for i in range(100):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sample = dataset[i]
        sample = dataset[i]
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"Sample keys: {list(sample.keys())}")
        print(f"Sample keys: {list(sample.keys())}")
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"Video shape: {sample['video'].shape}")
        print(f"Video shape: {sample['video'].shape}")
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"Instruction: {sample.get('instruction', 'No instruction')}")
        print(f"Instruction: {sample.get('instruction', 'No instruction')}")
        
        # 中文说明：根据条件选择执行分支；代码：if sample['video'].ndim == 5:
        if sample['video'].ndim == 5:
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for ci, vid in enumerate(sample['video']):
            for ci, vid in enumerate(sample['video']):

                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：save_path = f"datasets/openx_out/enhanced_output_video_{i}_part{ci}.gif"
                save_path = f"datasets/openx_out/enhanced_output_video_{i}_part{ci}.gif"
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：save_video_as_gif(vid, save_path, fps=16)
                save_video_as_gif(vid, save_path, fps=16)

        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：save_path = f"datasets/openx_out/enhanced_output_video_clip_{i}.gif"
            save_path = f"datasets/openx_out/enhanced_output_video_clip_{i}.gif"
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：save_video_as_gif(sample['video'], save_path, fps=16)
            save_video_as_gif(sample['video'], save_path, fps=16)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames_dir = f"datasets/openx_out/enhanced_output_frames_{i}"
            frames_dir = f"datasets/openx_out/enhanced_output_frames_{i}"
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：save_video_as_frames(sample['video'], frames_dir, frame_prefix=f"video_{i}_frame_")
            save_video_as_frames(sample['video'], frames_dir, frame_prefix=f"video_{i}_frame_")

            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(sample['selected_folder'], sample['video'].max(), sample['video'].min())
            print(sample['selected_folder'], sample['video'].max(), sample['video'].min())


