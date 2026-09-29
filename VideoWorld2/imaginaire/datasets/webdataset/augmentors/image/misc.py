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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Union
from typing import Union

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from PIL import Image
from PIL import Image


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def obtain_image_size(data_dict: dict, input_keys: list) -> tuple[int, int]:
def obtain_image_size(data_dict: dict, input_keys: list) -> tuple[int, int]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Function for obtaining the image size from the data dict.
    r"""Function for obtaining the image size from the data dict.

    Args:
        data_dict (dict): Input data dict
        input_keys (list): List of input keys
    Returns:
        width (int): Width of the input image
        height (int): Height of the input image
    """

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data1 = data_dict[input_keys[0]]
    data1 = data_dict[input_keys[0]]
    # 中文说明：根据条件选择执行分支；代码：if isinstance(data1, Image.Image):
    if isinstance(data1, Image.Image):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：width, height = data1.size
        width, height = data1.size
    # 中文说明：根据条件选择执行分支；代码：elif isinstance(data1, torch.Tensor):
    elif isinstance(data1, torch.Tensor):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：height, width = data1.size()[-2:]
        height, width = data1.size()[-2:]
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError("data to random crop should be PIL Image or tensor")
        raise ValueError("data to random crop should be PIL Image or tensor")

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return width, height
    return width, height


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def obtain_augmentation_size(data_dict: dict, augmentor_cfg: dict) -> Union[int, tuple]:
def obtain_augmentation_size(data_dict: dict, augmentor_cfg: dict) -> Union[int, tuple]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Function for obtaining size of the augmentation.
    r"""Function for obtaining size of the augmentation.
    When dealing with multi-aspect ratio dataloaders, we need to
    find the augmentation size from the aspect ratio of the data.

    Args:
        data_dict (dict): Input data dict
        augmentor_cfg (dict): Augmentor config
    Returns:
        aug_size (int): Size of augmentation
    """
    # 中文说明：根据条件选择执行分支；代码：if "__url__" in data_dict and "aspect_ratio" in data_dict["__url__"].meta.opts:
    if "__url__" in data_dict and "aspect_ratio" in data_dict["__url__"].meta.opts:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：aspect_ratio = data_dict["__url__"].meta.opts["aspect_ratio"]
        aspect_ratio = data_dict["__url__"].meta.opts["aspect_ratio"]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：aug_size = augmentor_cfg["size"][aspect_ratio]
        aug_size = augmentor_cfg["size"][aspect_ratio]
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：else: # Non-webdataset format
    else:  # Non-webdataset format
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：aspect_ratio = data_dict["aspect_ratio"]
        aspect_ratio = data_dict["aspect_ratio"]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：aug_size = augmentor_cfg["size"][aspect_ratio]
        aug_size = augmentor_cfg["size"][aspect_ratio]
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return aug_size
    return aug_size
