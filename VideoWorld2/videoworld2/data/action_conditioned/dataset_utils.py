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
https://github.com/bytedance/IRASim/blob/main/dataset/dataset_util.py
"""

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import math
import math
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torchvision.transforms.functional as F
import torchvision.transforms.functional as F


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def alpha2rotm(a):
def alpha2rotm(a):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Alpha euler angle to rotation matrix."""
    """Alpha euler angle to rotation matrix."""
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rotm = np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])
    rotm = np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return rotm
    return rotm


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def beta2rotm(b):
def beta2rotm(b):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Beta euler angle to rotation matrix."""
    """Beta euler angle to rotation matrix."""
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rotm = np.array([[np.cos(b), 0, np.sin(b)], [0, 1, 0], [-np.sin(b), 0, np.cos(b)]])
    rotm = np.array([[np.cos(b), 0, np.sin(b)], [0, 1, 0], [-np.sin(b), 0, np.cos(b)]])
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return rotm
    return rotm


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def gamma2rotm(c):
def gamma2rotm(c):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Gamma euler angle to rotation matrix."""
    """Gamma euler angle to rotation matrix."""
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rotm = np.array([[np.cos(c), -np.sin(c), 0], [np.sin(c), np.cos(c), 0], [0, 0, 1]])
    rotm = np.array([[np.cos(c), -np.sin(c), 0], [np.sin(c), np.cos(c), 0], [0, 0, 1]])
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return rotm
    return rotm


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def euler2rotm(euler_angles):
def euler2rotm(euler_angles):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Euler angle (ZYX) to rotation matrix."""
    """Euler angle (ZYX) to rotation matrix."""
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：alpha = euler_angles[0]
    alpha = euler_angles[0]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：beta = euler_angles[1]
    beta = euler_angles[1]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gamma = euler_angles[2]
    gamma = euler_angles[2]

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rotm_a = alpha2rotm(alpha)
    rotm_a = alpha2rotm(alpha)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rotm_b = beta2rotm(beta)
    rotm_b = beta2rotm(beta)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rotm_c = gamma2rotm(gamma)
    rotm_c = gamma2rotm(gamma)

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rotm = rotm_c @ rotm_b @ rotm_a
    rotm = rotm_c @ rotm_b @ rotm_a

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return rotm
    return rotm


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def isRotm(R):
def isRotm(R):
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Checks if a matrix is a valid rotation matrix.
    # Checks if a matrix is a valid rotation matrix.
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Forked from Andy Zeng
    # Forked from Andy Zeng
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：Rt = np.transpose(R)
    Rt = np.transpose(R)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：shouldBeIdentity = np.dot(Rt, R)
    shouldBeIdentity = np.dot(Rt, R)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：I = np.identity(3, dtype=R.dtype)
    I = np.identity(3, dtype=R.dtype)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n = np.linalg.norm(I - shouldBeIdentity)
    n = np.linalg.norm(I - shouldBeIdentity)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return n < 1e-6
    return n < 1e-6


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def rotm2euler(R):
def rotm2euler(R):
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Forked from: https://learnopencv.com/rotation-matrix-to-euler-angles/
    # Forked from: https://learnopencv.com/rotation-matrix-to-euler-angles/
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# R = Rz * Ry * Rx
    # R = Rz * Ry * Rx
    # 中文说明：检查运行时假设是否成立；代码：assert isRotm(R)
    assert isRotm(R)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])
    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：singular = sy < 1e-6
    singular = sy < 1e-6

    # 中文说明：根据条件选择执行分支；代码：if not singular:
    if not singular:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = math.atan2(R[2, 1], R[2, 2])
        x = math.atan2(R[2, 1], R[2, 2])
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：y = math.atan2(-R[2, 0], sy)
        y = math.atan2(-R[2, 0], sy)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z = math.atan2(R[1, 0], R[0, 0])
        z = math.atan2(R[1, 0], R[0, 0])
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = math.atan2(-R[1, 2], R[1, 1])
        x = math.atan2(-R[1, 2], R[1, 1])
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：y = math.atan2(-R[2, 0], sy)
        y = math.atan2(-R[2, 0], sy)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z = 0
        z = 0

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# (-pi , pi]
    # (-pi , pi]
    # 中文说明：在条件成立时重复执行循环体；代码：while x > np.pi:
    while x > np.pi:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x -= 2 * np.pi
        x -= 2 * np.pi
    # 中文说明：在条件成立时重复执行循环体；代码：while x <= -np.pi:
    while x <= -np.pi:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x += 2 * np.pi
        x += 2 * np.pi
    # 中文说明：在条件成立时重复执行循环体；代码：while y > np.pi:
    while y > np.pi:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：y -= 2 * np.pi
        y -= 2 * np.pi
    # 中文说明：在条件成立时重复执行循环体；代码：while y <= -np.pi:
    while y <= -np.pi:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：y += 2 * np.pi
        y += 2 * np.pi
    # 中文说明：在条件成立时重复执行循环体；代码：while z > np.pi:
    while z > np.pi:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z -= 2 * np.pi
        z -= 2 * np.pi
    # 中文说明：在条件成立时重复执行循环体；代码：while z <= -np.pi:
    while z <= -np.pi:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z += 2 * np.pi
        z += 2 * np.pi
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return np.array([x, y, z])
    return np.array([x, y, z])


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


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Preprocess:
class Preprocess:
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, size):
    def __init__(self, size):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.size = size
        self.size = size

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, clip):
    def __call__(self, clip):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：clip = Preprocess.resize_scale(clip, self.size[0], self.size[1], interpolation_mode="bilinear")
        clip = Preprocess.resize_scale(clip, self.size[0], self.size[1], interpolation_mode="bilinear")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return clip
        return clip

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __repr__(self) -> str:
    def __repr__(self) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return f"{self.__class__.__name__}(size={self.size})"
        return f"{self.__class__.__name__}(size={self.size})"

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def resize_scale(clip, target_height, target_width, interpolation_mode):
    def resize_scale(clip, target_height, target_width, interpolation_mode):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：target_ratio = target_height / target_width
        target_ratio = target_height / target_width
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：H = clip.size(-2)
        H = clip.size(-2)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：W = clip.size(-1)
        W = clip.size(-1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：clip_ratio = H / W
        clip_ratio = H / W
        # 中文说明：根据条件选择执行分支；代码：if clip_ratio > target_ratio:
        if clip_ratio > target_ratio:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scale_ = target_width / W
            scale_ = target_width / W
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scale_ = target_height / H
            scale_ = target_height / H
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return torch.nn.functional.interpolate(clip, scale_factor=scale_, mode=interpolation_mode, al...
        return torch.nn.functional.interpolate(clip, scale_factor=scale_, mode=interpolation_mode, align_corners=False)


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