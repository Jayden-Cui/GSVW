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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import cv2
import cv2
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def pixelate_face(face_img: np.ndarray, blocks: int = 5) -> np.ndarray:
def pixelate_face(face_img: np.ndarray, blocks: int = 5) -> np.ndarray:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Pixelate a face region by reducing resolution and then upscaling.

    Args:
        face_img: Face region to pixelate
        blocks: Number of blocks to divide the face into (in each dimension)

    Returns:
        Pixelated face region
    """
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：h, w = face_img.shape[:2]
    h, w = face_img.shape[:2]
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Shrink the image and scale back up to create pixelation effect
    # Shrink the image and scale back up to create pixelation effect
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temp = cv2.resize(face_img, (blocks, blocks), interpolation=cv2.INTER_LINEAR)
    temp = cv2.resize(face_img, (blocks, blocks), interpolation=cv2.INTER_LINEAR)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pixelated = cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)
    pixelated = cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return pixelated
    return pixelated
