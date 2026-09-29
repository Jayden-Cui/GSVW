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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Optional
from typing import Optional

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import omegaconf
import omegaconf
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torchvision.transforms.functional as transforms_F
import torchvision.transforms.functional as transforms_F

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.datasets.webdataset.augmentors.augmentor import Augmentor
from imaginaire.datasets.webdataset.augmentors.augmentor import Augmentor
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.datasets.webdataset.augmentors.image.misc import obtain_augmentation_size, ob...
from imaginaire.datasets.webdataset.augmentors.image.misc import obtain_augmentation_size, obtain_image_size


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ReflectionPadding(Augmentor):
class ReflectionPadding(Augmentor):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, input_keys: list, output_keys: Optional[list] = None, args: Optional[dict]...
    def __init__(self, input_keys: list, output_keys: Optional[list] = None, args: Optional[dict] = None) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(input_keys, output_keys, args)
        super().__init__(input_keys, output_keys, args)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, data_dict: dict) -> dict:
    def __call__(self, data_dict: dict) -> dict:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Performs reflection padding. This function also returns a padding mask.
        r"""Performs reflection padding. This function also returns a padding mask.

        Args:
            data_dict (dict): Input data dict
        Returns:
            data_dict (dict): Output dict where images are center cropped.
        """

        # 中文说明：检查运行时假设是否成立；代码：assert self.args is not None, "Please specify args in augmentation"
        assert self.args is not None, "Please specify args in augmentation"
        # 中文说明：根据条件选择执行分支；代码：if self.output_keys is None:
        if self.output_keys is None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.output_keys = self.input_keys
            self.output_keys = self.input_keys

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Obtain image and augmentation sizes
        # Obtain image and augmentation sizes
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：orig_w, orig_h = obtain_image_size(data_dict, self.input_keys)
        orig_w, orig_h = obtain_image_size(data_dict, self.input_keys)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：target_size = obtain_augmentation_size(data_dict, self.args)
        target_size = obtain_augmentation_size(data_dict, self.args)

        # 中文说明：检查运行时假设是否成立；代码：assert isinstance(target_size, (tuple, omegaconf.listconfig.ListConfig)), "Please specify tar...
        assert isinstance(target_size, (tuple, omegaconf.listconfig.ListConfig)), "Please specify target size as tuple"
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：target_w, target_h = target_size
        target_w, target_h = target_size

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：target_w = int(target_w)
        target_w = int(target_w)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：target_h = int(target_h)
        target_h = int(target_h)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Calculate padding vals
        # Calculate padding vals
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding_left = int((target_w - orig_w) / 2)
        padding_left = int((target_w - orig_w) / 2)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding_right = target_w - orig_w - padding_left
        padding_right = target_w - orig_w - padding_left
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding_top = int((target_h - orig_h) / 2)
        padding_top = int((target_h - orig_h) / 2)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding_bottom = target_h - orig_h - padding_top
        padding_bottom = target_h - orig_h - padding_top
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding_vals = [padding_left, padding_top, padding_right, padding_bottom]
        padding_vals = [padding_left, padding_top, padding_right, padding_bottom]

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for inp_key, out_key in zip(self.input_keys, self.output_keys):
        for inp_key, out_key in zip(self.input_keys, self.output_keys):
            # 中文说明：根据条件选择执行分支；代码：if max(padding_vals[0], padding_vals[2]) >= orig_w or max(padding_vals[1], padding_vals[3]) >...
            if max(padding_vals[0], padding_vals[2]) >= orig_w or max(padding_vals[1], padding_vals[3]) >= orig_h:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# In this case, we can't perform reflection padding. This is because padding values
                # In this case, we can't perform reflection padding. This is because padding values
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# are larger than the image size. So, perform edge padding instead.
                # are larger than the image size. So, perform edge padding instead.
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_dict[out_key] = transforms_F.pad(data_dict[inp_key], padding_vals, padding_mode="edge")
                data_dict[out_key] = transforms_F.pad(data_dict[inp_key], padding_vals, padding_mode="edge")
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Perform reflection padding
                # Perform reflection padding
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_dict[out_key] = transforms_F.pad(data_dict[inp_key], padding_vals, padding_mode="reflect")
                data_dict[out_key] = transforms_F.pad(data_dict[inp_key], padding_vals, padding_mode="reflect")

            # 中文说明：根据条件选择执行分支；代码：if out_key != inp_key:
            if out_key != inp_key:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del data_dict[inp_key]
                del data_dict[inp_key]

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Return padding_mask when padding is performed.
        # Return padding_mask when padding is performed.
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Padding mask denotes which pixels are padded.
        # Padding mask denotes which pixels are padded.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding_mask = torch.ones((1, target_h, target_w))
        padding_mask = torch.ones((1, target_h, target_w))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding_mask[:, padding_top : (padding_top + orig_h), padding_left : (padding_left + orig_w)]...
        padding_mask[:, padding_top : (padding_top + orig_h), padding_left : (padding_left + orig_w)] = 0
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_dict["padding_mask"] = padding_mask
        data_dict["padding_mask"] = padding_mask
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_dict["image_size"] = torch.tensor([target_h, target_w, orig_h, orig_w], dtype=torch.float)
        data_dict["image_size"] = torch.tensor([target_h, target_w, orig_h, orig_w], dtype=torch.float)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return data_dict
        return data_dict
