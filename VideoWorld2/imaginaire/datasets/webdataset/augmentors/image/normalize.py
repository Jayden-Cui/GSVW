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

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torchvision.transforms.functional as transforms_F
import torchvision.transforms.functional as transforms_F

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.datasets.webdataset.augmentors.augmentor import Augmentor
from imaginaire.datasets.webdataset.augmentors.augmentor import Augmentor


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Normalize(Augmentor):
class Normalize(Augmentor):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, input_keys: list, output_keys: Optional[list] = None, args: Optional[dict]...
    def __init__(self, input_keys: list, output_keys: Optional[list] = None, args: Optional[dict] = None) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(input_keys, output_keys, args)
        super().__init__(input_keys, output_keys, args)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, data_dict: dict) -> dict:
    def __call__(self, data_dict: dict) -> dict:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Performs data normalization.
        r"""Performs data normalization.

        Args:
            data_dict (dict): Input data dict
        Returns:
            data_dict (dict): Output dict where images are center cropped.
        """
        # 中文说明：检查运行时假设是否成立；代码：assert self.args is not None, "Please specify args"
        assert self.args is not None, "Please specify args"

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mean = self.args["mean"]
        mean = self.args["mean"]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：std = self.args["std"]
        std = self.args["std"]

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key in self.input_keys:
        for key in self.input_keys:
            # 中文说明：根据条件选择执行分支；代码：if isinstance(data_dict[key], torch.Tensor):
            if isinstance(data_dict[key], torch.Tensor):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_dict[key] = data_dict[key].to(dtype=torch.get_default_dtype()).div(255)
                data_dict[key] = data_dict[key].to(dtype=torch.get_default_dtype()).div(255)
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_dict[key] = transforms_F.to_tensor(data_dict[key]) # division by 255 is applied in to_te...
                data_dict[key] = transforms_F.to_tensor(data_dict[key])  # division by 255 is applied in to_tensor()

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_dict[key] = transforms_F.normalize(tensor=data_dict[key], mean=mean, std=std)
            data_dict[key] = transforms_F.normalize(tensor=data_dict[key], mean=mean, std=std)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return data_dict
        return data_dict
