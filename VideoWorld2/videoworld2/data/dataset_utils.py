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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torchvision.transforms.functional as F
import torchvision.transforms.functional as F
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import albumentations as A
import albumentations as A
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import kornia as K
import kornia as K
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import kornia.augmentation as K_aug
import kornia.augmentation as K_aug

# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Resize_Preprocess:
class Resize_Preprocess:
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, size):
    def __init__(self, size):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Initialize the preprocessing class with the target size.
        Args:
        size (tuple): The target height and width as a tuple (height, width).
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.size = size
        self.size = size

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, video_frames):
    def __call__(self, video_frames):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Apply the transformation to each frame in the video.
        Args:
        video_frames (torch.Tensor): A tensor representing a batch of video frames.
        Returns:
        torch.Tensor: The transformed video frames.
        """
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Resize each frame in the video
        # Resize each frame in the video
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resized_frames = torch.stack([F.resize(frame, self.size, antialias=True) for frame in video_f...
        resized_frames = torch.stack([F.resize(frame, self.size, antialias=True) for frame in video_frames])
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return resized_frames
        return resized_frames

# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class GeometricAugmentor():
class GeometricAugmentor():
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self,) -> None:
    def __init__(self,) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.transform = A.ReplayCompose([
        self.transform = A.ReplayCompose([
               
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：A.ShiftScaleRotate(
                A.ShiftScaleRotate(
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：shift_limit=0.1,
                    shift_limit=0.1,    
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scale_limit=0.2,
                    scale_limit=0.2,   
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rotate_limit=30,
                    rotate_limit=30,   
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# border_mode=cv2.BORDER_WRAP,
                    # border_mode=cv2.BORDER_WRAP,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：p=0.7
                    p=0.7
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
                ),
                
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：A.Perspective(
                A.Perspective(
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# scale=0.1,
                    # scale=0.1,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：keep_size=True,
                    keep_size=True,
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# pad_mode='reflect',
                    # pad_mode='reflect',
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# fit_output=True,
                    # fit_output=True,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：p=0.7
                    p=0.7
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
                ),
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=1),
                A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=1),
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：A.HueSaturationValue(hue_shift_limit=10, sat_shift_limit=20, val_shift_limit=10, p=1),
                A.HueSaturationValue(hue_shift_limit=10, sat_shift_limit=20, val_shift_limit=10, p=1),
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# A.GaussianBlur(blur_limit=(1, 3), p=0.5),
                # A.GaussianBlur(blur_limit=(1, 3), p=0.5), 
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# A.GaussNoise(var_limit=(10.0, 50.0), p=1),
                # A.GaussNoise(var_limit=(10.0, 50.0), p=1),
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# A.ISONoise()
                # A.ISONoise()

            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：], p=1)
            ], p=1)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self.turn_on = turn_on
        # self.turn_on = turn_on

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, video_frames: dict) -> dict:
    def __call__(self, video_frames: dict) -> dict:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# if not self.turn_on:
        # if not self.turn_on:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# return data_dict
        #     return data_dict
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# for key in self.input_keys:
        # for key in self.input_keys:
        # 中文说明：根据条件选择执行分支；代码：if isinstance(video_frames, torch.Tensor):
        if isinstance(video_frames, torch.Tensor):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data = video_frames.permute(0, 2, 3, 1).numpy()
            data = video_frames.permute(0, 2, 3, 1).numpy()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：first_frame = data[0]
        first_frame = data[0]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：transformed = self.transform(image=first_frame)
        transformed = self.transform(image=first_frame)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：replay_params = transformed['replay']
        replay_params = transformed['replay']

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：augmented_frames = [transformed['image']]
        augmented_frames = [transformed['image']]
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for frame in data[1:]:
        for frame in data[1:]:
            
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：transformed_frame = A.ReplayCompose.replay(replay_params, image=frame)
            transformed_frame = A.ReplayCompose.replay(replay_params, image=frame)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：augmented_frames.append(transformed_frame['image'])
            augmented_frames.append(transformed_frame['image'])
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：augmented_frames = torch.from_numpy(np.stack(augmented_frames)).permute(0, 3, 1, 2)
        augmented_frames = torch.from_numpy(np.stack(augmented_frames)).permute(0, 3, 1, 2)
 
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return augmented_frames
        return augmented_frames

# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class GeometricAugmentor_K():
class GeometricAugmentor_K():
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self,) -> None:
    def __init__(self,) -> None:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.transform = K_aug.AugmentationSequential(
        self.transform = K_aug.AugmentationSequential(
           
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：K_aug.RandomAffine(
            K_aug.RandomAffine(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：degrees=30.0,
                degrees=30.0,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：translate=(0.1, 0.1),
                translate=(0.1, 0.1),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scale=(0.8, 1.2),
                scale=(0.8, 1.2), 
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：p=0.7,
                p=0.7,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：same_on_batch=True,
                same_on_batch=True,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
           
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：K_aug.RandomPerspective(
            K_aug.RandomPerspective(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distortion_scale=0.2,
                distortion_scale=0.2, 
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：p=0.7,
                p=0.7,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：same_on_batch=True,
                same_on_batch=True,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：K_aug.ColorJitter(
            K_aug.ColorJitter(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：brightness=0.3,
                brightness=0.3,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：contrast=0.3,
                contrast=0.3,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：saturation=0.2,
                saturation=0.2,  
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hue=0.055,
                hue=0.055, 
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：p=1.0,
                p=1.0,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：same_on_batch=True,
                same_on_batch=True,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_keys=["input"],
            data_keys=["input"],
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self.turn_on = turn_on
        # self.turn_on = turn_on

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, video_frames: dict) -> dict:
    def __call__(self, video_frames: dict) -> dict:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：根据条件选择执行分支；代码：if video_frames.dtype == torch.uint8:
        if video_frames.dtype == torch.uint8:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_frames = video_frames.float()
            video_frames = video_frames.float()
        # 中文说明：根据条件选择执行分支；代码：if video_frames.max() > 1:
        if video_frames.max() > 1:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_frames = video_frames / 255.0
            video_frames = video_frames / 255.0
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：augmented_frames = self.transform(video_frames)
        augmented_frames = self.transform(video_frames) 
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# augmented_frames = torch.clip(augmented_frames, 0, 255)
        # augmented_frames = torch.clip(augmented_frames, 0, 255)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return augmented_frames
        return augmented_frames



# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ToTensorVideo:
class ToTensorVideo:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Convert tensor data type from uint8 to float, divide value by 255.0 and
    permute the dimensions of clip tensor
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self):
    def __init__(self):
        # 中文说明：执行循环控制或空操作；代码：pass
        pass

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, clip):
    def __call__(self, clip):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Args:
            clip (torch.tensor, dtype=torch.uint8): Size is (T, C, H, W)
        Return:
            clip (torch.tensor, dtype=torch.float): Size is (T, C, H, W)
        """
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return to_tensor(clip)
        return to_tensor(clip)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __repr__(self) -> str:
    def __repr__(self) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.__class__.__name__
        return self.__class__.__name__


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def to_tensor(clip):
def to_tensor(clip):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Convert tensor data type from uint8 to float, divide value by 255.0 and
    permute the dimensions of clip tensor
    Args:
        clip (torch.tensor, dtype=torch.uint8): Size is (T, C, H, W)
    Return:
        clip (torch.tensor, dtype=torch.float): Size is (T, C, H, W)
    """
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_is_tensor_video_clip(clip)
    _is_tensor_video_clip(clip)
    # 中文说明：根据条件选择执行分支；代码：if not clip.dtype == torch.uint8:
    if not clip.dtype == torch.uint8:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError("clip tensor should have data type uint8. Got %s" % str(clip.dtype))
        raise TypeError("clip tensor should have data type uint8. Got %s" % str(clip.dtype))
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# return clip.float().permute(3, 0, 1, 2) / 255.0
    # return clip.float().permute(3, 0, 1, 2) / 255.0
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return clip.float() / 255.0
    return clip.float() / 255.0


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _is_tensor_video_clip(clip):
def _is_tensor_video_clip(clip):
    # 中文说明：根据条件选择执行分支；代码：if not torch.is_tensor(clip):
    if not torch.is_tensor(clip):
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError("clip should be Tensor. Got %s" % type(clip))
        raise TypeError("clip should be Tensor. Got %s" % type(clip))

    # 中文说明：根据条件选择执行分支；代码：if not clip.ndimension() == 4:
    if not clip.ndimension() == 4:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError("clip should be 4D. Got %dD" % clip.dim())
        raise ValueError("clip should be 4D. Got %dD" % clip.dim())

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return True
    return True
