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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import IO, Optional, Tuple, Union
from typing import IO, Optional, Tuple, Union

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.handlers.base import BaseFileHandler
from imaginaire.utils.easy_io.handlers.base import BaseFileHandler

# 中文说明：开始一个可捕获异常的代码块；代码：try:
try:
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from PIL import Image
    from PIL import Image
# 中文说明：处理异常、清理资源或管理上下文；代码：except ImportError:
except ImportError:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：Image = None
    Image = None


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class PILHandler(BaseFileHandler):
class PILHandler(BaseFileHandler):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：format: str
    format: str
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：str_like = False
    str_like = False

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def load_from_fileobj(
    def load_from_fileobj(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：file: IO[bytes],
        file: IO[bytes],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：fmt: str = "pil",
        fmt: str = "pil",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：size: Optional[Union[int, Tuple[int, int]]] = None,
        size: Optional[Union[int, Tuple[int, int]]] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**kwargs,
        **kwargs,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Load an image from a file-like object and return it in a specified format.

        Args:
            file (IO[bytes]): A file-like object containing the image data.
            fmt (str): The format to convert the image into. Options are \
                'numpy', 'np', 'npy', 'type' (all return numpy arrays), \
                    'pil' (returns PIL Image), 'th', 'torch' (returns a torch tensor).
            size (Optional[Union[int, Tuple[int, int]]]): The new size of the image as a single integer \
                or a tuple of (width, height). If specified, the image is resized accordingly.
            **kwargs: Additional keyword arguments that can be passed to conversion functions.

        Returns:
            Image data in the format specified by `fmt`.

        Raises:
            IOError: If the image cannot be loaded or processed.
            ValueError: If the specified format is unsupported.
        """
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：img = Image.open(file)
            img = Image.open(file)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：img.load() # Explicitly load the image data
            img.load()  # Explicitly load the image data
            # 中文说明：根据条件选择执行分支；代码：if size is not None:
            if size is not None:
                # 中文说明：根据条件选择执行分支；代码：if isinstance(size, int):
                if isinstance(size, int):
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：size = (
                    size = (
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：size,
                        size,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：size,
                        size,
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) # create a tuple if only one integer is provided
                    )  # create a tuple if only one integer is provided
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：img = img.resize(size, Image.ANTIALIAS)
                img = img.resize(size, Image.ANTIALIAS)

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Return the image in the requested format
            # Return the image in the requested format
            # 中文说明：根据条件选择执行分支；代码：if fmt in ["numpy", "np", "npy"]:
            if fmt in ["numpy", "np", "npy"]:
                # 中文说明：从当前函数返回结果或结束函数执行；代码：return np.array(img, **kwargs)
                return np.array(img, **kwargs)
            # 中文说明：根据条件选择执行分支；代码：if fmt == "pil":
            if fmt == "pil":
                # 中文说明：从当前函数返回结果或结束函数执行；代码：return img
                return img
            # 中文说明：根据条件选择执行分支；代码：if fmt in ["th", "torch"]:
            if fmt in ["th", "torch"]:
                # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
                import torch

                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Convert to tensor
                # Convert to tensor
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：img_tensor = torch.from_numpy(np.array(img, **kwargs))
                img_tensor = torch.from_numpy(np.array(img, **kwargs))
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Convert image from HxWxC to CxHxW
                # Convert image from HxWxC to CxHxW
                # 中文说明：根据条件选择执行分支；代码：if img_tensor.ndim == 3:
                if img_tensor.ndim == 3:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：img_tensor = img_tensor.permute(2, 0, 1)
                    img_tensor = img_tensor.permute(2, 0, 1)
                # 中文说明：从当前函数返回结果或结束函数执行；代码：return img_tensor
                return img_tensor
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(
            raise ValueError(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："Unsupported format. Supported formats are 'numpy', 'np', 'npy', 'pil', 'th', and 'torch'."
                "Unsupported format. Supported formats are 'numpy', 'np', 'npy', 'pil', 'th', and 'torch'."
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
        except Exception as e:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise IOError(f"Unable to load image: {e}") from e
            raise IOError(f"Unable to load image: {e}") from e

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def dump_to_fileobj(self, obj, file: IO[bytes], **kwargs):
    def dump_to_fileobj(self, obj, file: IO[bytes], **kwargs):
        # 中文说明：根据条件选择执行分支；代码：if "format" not in kwargs:
        if "format" not in kwargs:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["format"] = self.format
            kwargs["format"] = self.format
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["format"] = "JPEG" if self.format.lower() == "jpg" else self.format.upper()
        kwargs["format"] = "JPEG" if self.format.lower() == "jpg" else self.format.upper()
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：obj.save(file, **kwargs)
        obj.save(file, **kwargs)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def dump_to_str(self, obj, **kwargs):
    def dump_to_str(self, obj, **kwargs):
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise NotImplementedError
        raise NotImplementedError
