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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torchvision.transforms.functional as transforms_F
import torchvision.transforms.functional as transforms_F

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.datasets.webdataset.augmentors.augmentor import Augmentor
from imaginaire.datasets.webdataset.augmentors.augmentor import Augmentor
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.datasets.webdataset.augmentors.image.misc import obtain_augmentation_size, ob...
from imaginaire.datasets.webdataset.augmentors.image.misc import obtain_augmentation_size, obtain_image_size


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ResizeSmallestSide(Augmentor):
class ResizeSmallestSide(Augmentor):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, input_keys: list, output_keys: Optional[list] = None, args: Optional[dict]...
    def __init__(self, input_keys: list, output_keys: Optional[list] = None, args: Optional[dict] = None) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(input_keys, output_keys, args)
        super().__init__(input_keys, output_keys, args)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, data_dict: dict) -> dict:
    def __call__(self, data_dict: dict) -> dict:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Performs resizing to smaller side
        r"""Performs resizing to smaller side

        Args:
            data_dict (dict): Input data dict
        Returns:
            data_dict (dict): Output dict where images are resized
        """

        # 中文说明：根据条件选择执行分支；代码：if self.output_keys is None:
        if self.output_keys is None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.output_keys = self.input_keys
            self.output_keys = self.input_keys
        # 中文说明：检查运行时假设是否成立；代码：assert self.args is not None, "Please specify args in augmentations"
        assert self.args is not None, "Please specify args in augmentations"

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for inp_key, out_key in zip(self.input_keys, self.output_keys):
        for inp_key, out_key in zip(self.input_keys, self.output_keys):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_size = obtain_augmentation_size(data_dict, self.args)
            out_size = obtain_augmentation_size(data_dict, self.args)
            # 中文说明：检查运行时假设是否成立；代码：assert isinstance(out_size, int), "Arg size in resize should be an integer"
            assert isinstance(out_size, int), "Arg size in resize should be an integer"
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_dict[out_key] = transforms_F.resize(
            data_dict[out_key] = transforms_F.resize(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_dict[inp_key],
                data_dict[inp_key],
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：size=out_size, # type: ignore
                size=out_size,  # type: ignore
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：interpolation=getattr(self.args, "interpolation", transforms_F.InterpolationMode.BICUBIC),
                interpolation=getattr(self.args, "interpolation", transforms_F.InterpolationMode.BICUBIC),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：antialias=True,
                antialias=True,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：根据条件选择执行分支；代码：if out_key != inp_key:
            if out_key != inp_key:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del data_dict[inp_key]
                del data_dict[inp_key]
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return data_dict
        return data_dict


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ResizeLargestSide(Augmentor):
class ResizeLargestSide(Augmentor):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, input_keys: list, output_keys: Optional[list] = None, args: Optional[dict]...
    def __init__(self, input_keys: list, output_keys: Optional[list] = None, args: Optional[dict] = None) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(input_keys, output_keys, args)
        super().__init__(input_keys, output_keys, args)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, data_dict: dict) -> dict:
    def __call__(self, data_dict: dict) -> dict:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Performs resizing to larger side
        r"""Performs resizing to larger side

        Args:
            data_dict (dict): Input data dict
        Returns:
            data_dict (dict): Output dict where images are resized
        """

        # 中文说明：根据条件选择执行分支；代码：if self.output_keys is None:
        if self.output_keys is None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.output_keys = self.input_keys
            self.output_keys = self.input_keys
        # 中文说明：检查运行时假设是否成立；代码：assert self.args is not None, "Please specify args in augmentations"
        assert self.args is not None, "Please specify args in augmentations"

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for inp_key, out_key in zip(self.input_keys, self.output_keys):
        for inp_key, out_key in zip(self.input_keys, self.output_keys):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_size = obtain_augmentation_size(data_dict, self.args)
            out_size = obtain_augmentation_size(data_dict, self.args)
            # 中文说明：检查运行时假设是否成立；代码：assert isinstance(out_size, int), "Arg size in resize should be an integer"
            assert isinstance(out_size, int), "Arg size in resize should be an integer"
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：orig_w, orig_h = obtain_image_size(data_dict, self.input_keys)
            orig_w, orig_h = obtain_image_size(data_dict, self.input_keys)

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scaling_ratio = min(out_size / orig_w, out_size / orig_h)
            scaling_ratio = min(out_size / orig_w, out_size / orig_h)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：target_size = [int(scaling_ratio * orig_h), int(scaling_ratio * orig_w)]
            target_size = [int(scaling_ratio * orig_h), int(scaling_ratio * orig_w)]

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_dict[out_key] = transforms_F.resize(
            data_dict[out_key] = transforms_F.resize(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_dict[inp_key],
                data_dict[inp_key],
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：size=target_size,
                size=target_size,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：interpolation=getattr(self.args, "interpolation", transforms_F.InterpolationMode.BICUBIC),
                interpolation=getattr(self.args, "interpolation", transforms_F.InterpolationMode.BICUBIC),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：antialias=True,
                antialias=True,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：根据条件选择执行分支；代码：if out_key != inp_key:
            if out_key != inp_key:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del data_dict[inp_key]
                del data_dict[inp_key]
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return data_dict
        return data_dict


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ResizeSmallestSideAspectPreserving(Augmentor):
class ResizeSmallestSideAspectPreserving(Augmentor):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, input_keys: list, output_keys: Optional[list] = None, args: Optional[dict]...
    def __init__(self, input_keys: list, output_keys: Optional[list] = None, args: Optional[dict] = None) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(input_keys, output_keys, args)
        super().__init__(input_keys, output_keys, args)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, data_dict: dict) -> dict:
    def __call__(self, data_dict: dict) -> dict:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Performs aspect-ratio preserving resizing.
        r"""Performs aspect-ratio preserving resizing.
        Image is resized to the dimension which has the smaller ratio of (size / target_size).
        First we compute (w_img / w_target) and (h_img / h_target) and resize the image
        to the dimension that has the smaller of these ratios.

        Args:
            data_dict (dict): Input data dict
        Returns:
            data_dict (dict): Output dict where images are resized
        """

        # 中文说明：根据条件选择执行分支；代码：if self.output_keys is None:
        if self.output_keys is None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.output_keys = self.input_keys
            self.output_keys = self.input_keys
        # 中文说明：检查运行时假设是否成立；代码：assert self.args is not None, "Please specify args in augmentations"
        assert self.args is not None, "Please specify args in augmentations"

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：img_size = obtain_augmentation_size(data_dict, self.args)
        img_size = obtain_augmentation_size(data_dict, self.args)
        # 中文说明：检查运行时假设是否成立；代码：assert isinstance(
        assert isinstance(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：img_size, (tuple, omegaconf.listconfig.ListConfig)
            img_size, (tuple, omegaconf.listconfig.ListConfig)
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"Arg size in resize should be a tuple, get {type(img_size)}, {img_size}"
        ), f"Arg size in resize should be a tuple, get {type(img_size)}, {img_size}"
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：img_w, img_h = img_size
        img_w, img_h = img_size

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：orig_w, orig_h = obtain_image_size(data_dict, self.input_keys)
        orig_w, orig_h = obtain_image_size(data_dict, self.input_keys)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scaling_ratio = max((img_w / orig_w), (img_h / orig_h))
        scaling_ratio = max((img_w / orig_w), (img_h / orig_h))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：target_size = (int(scaling_ratio * orig_h + 0.5), int(scaling_ratio * orig_w + 0.5))
        target_size = (int(scaling_ratio * orig_h + 0.5), int(scaling_ratio * orig_w + 0.5))

        # 中文说明：检查运行时假设是否成立；代码：assert (
        assert (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：target_size[0] >= img_h and target_size[1] >= img_w
            target_size[0] >= img_h and target_size[1] >= img_w
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"Resize error. orig {(orig_w, orig_h)} desire {img_size} compute {target_size}"
        ), f"Resize error. orig {(orig_w, orig_h)} desire {img_size} compute {target_size}"

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for inp_key, out_key in zip(self.input_keys, self.output_keys):
        for inp_key, out_key in zip(self.input_keys, self.output_keys):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_dict[out_key] = transforms_F.resize(
            data_dict[out_key] = transforms_F.resize(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_dict[inp_key],
                data_dict[inp_key],
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：size=target_size, # type: ignore
                size=target_size,  # type: ignore
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：interpolation=getattr(self.args, "interpolation", transforms_F.InterpolationMode.BICUBIC),
                interpolation=getattr(self.args, "interpolation", transforms_F.InterpolationMode.BICUBIC),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：antialias=True,
                antialias=True,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

            # 中文说明：根据条件选择执行分支；代码：if out_key != inp_key:
            if out_key != inp_key:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del data_dict[inp_key]
                del data_dict[inp_key]
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return data_dict
        return data_dict


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ResizeLargestSideAspectPreserving(Augmentor):
class ResizeLargestSideAspectPreserving(Augmentor):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, input_keys: list, output_keys: Optional[list] = None, args: Optional[dict]...
    def __init__(self, input_keys: list, output_keys: Optional[list] = None, args: Optional[dict] = None) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(input_keys, output_keys, args)
        super().__init__(input_keys, output_keys, args)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, data_dict: dict) -> dict:
    def __call__(self, data_dict: dict) -> dict:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Performs aspect-ratio preserving resizing.
        r"""Performs aspect-ratio preserving resizing.
        Image is resized to the dimension which has the larger ratio of (size / target_size).
        First we compute (w_img / w_target) and (h_img / h_target) and resize the image
        to the dimension that has the larger of these ratios.

        Args:
            data_dict (dict): Input data dict
        Returns:
            data_dict (dict): Output dict where images are resized
        """

        # 中文说明：根据条件选择执行分支；代码：if self.output_keys is None:
        if self.output_keys is None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.output_keys = self.input_keys
            self.output_keys = self.input_keys
        # 中文说明：检查运行时假设是否成立；代码：assert self.args is not None, "Please specify args in augmentations"
        assert self.args is not None, "Please specify args in augmentations"

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：img_size = obtain_augmentation_size(data_dict, self.args)
        img_size = obtain_augmentation_size(data_dict, self.args)
        # 中文说明：检查运行时假设是否成立；代码：assert isinstance(
        assert isinstance(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：img_size, (tuple, omegaconf.listconfig.ListConfig)
            img_size, (tuple, omegaconf.listconfig.ListConfig)
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"Arg size in resize should be a tuple, get {type(img_size)}, {img_size}"
        ), f"Arg size in resize should be a tuple, get {type(img_size)}, {img_size}"
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：img_w, img_h = img_size
        img_w, img_h = img_size

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：orig_w, orig_h = obtain_image_size(data_dict, self.input_keys)
        orig_w, orig_h = obtain_image_size(data_dict, self.input_keys)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scaling_ratio = min((img_w / orig_w), (img_h / orig_h))
        scaling_ratio = min((img_w / orig_w), (img_h / orig_h))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：target_size = (int(scaling_ratio * orig_h + 0.5), int(scaling_ratio * orig_w + 0.5))
        target_size = (int(scaling_ratio * orig_h + 0.5), int(scaling_ratio * orig_w + 0.5))

        # 中文说明：检查运行时假设是否成立；代码：assert (
        assert (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：target_size[0] <= img_h and target_size[1] <= img_w
            target_size[0] <= img_h and target_size[1] <= img_w
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"Resize error. orig {(orig_w, orig_h)} desire {img_size} compute {target_size}"
        ), f"Resize error. orig {(orig_w, orig_h)} desire {img_size} compute {target_size}"

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for inp_key, out_key in zip(self.input_keys, self.output_keys):
        for inp_key, out_key in zip(self.input_keys, self.output_keys):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_dict[out_key] = transforms_F.resize(
            data_dict[out_key] = transforms_F.resize(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_dict[inp_key],
                data_dict[inp_key],
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：size=target_size, # type: ignore
                size=target_size,  # type: ignore
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：interpolation=getattr(self.args, "interpolation", transforms_F.InterpolationMode.BICUBIC),
                interpolation=getattr(self.args, "interpolation", transforms_F.InterpolationMode.BICUBIC),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：antialias=True,
                antialias=True,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

            # 中文说明：根据条件选择执行分支；代码：if out_key != inp_key:
            if out_key != inp_key:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del data_dict[inp_key]
                del data_dict[inp_key]
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return data_dict
        return data_dict
