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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import io
import io
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import re
import re
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Optional
from typing import Optional

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from PIL import Image
from PIL import Image

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：Image.MAX_IMAGE_PIXELS = 933120000
Image.MAX_IMAGE_PIXELS = 933120000
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_IMG_EXTENSIONS = "jpg jpeg png ppm pgm pbm pnm".split()
_IMG_EXTENSIONS = "jpg jpeg png ppm pgm pbm pnm".split()


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def pil_loader(key: str, data: bytes) -> Optional[Image.Image]:
def pil_loader(key: str, data: bytes) -> Optional[Image.Image]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""
    r"""
    Function to load an image.
    If the image is corrupt, it returns a black image.
    Args:
        key (str): Image key.
        data (bytes): Image data stream.
    Returns:
        PIL image
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extension = re.sub(r".*[.]", "", key)
    extension = re.sub(r".*[.]", "", key)
    # 中文说明：根据条件选择执行分支；代码：if extension.lower() not in _IMG_EXTENSIONS:
    if extension.lower() not in _IMG_EXTENSIONS:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return None
        return None

    # 中文说明：处理异常、清理资源或管理上下文；代码：with io.BytesIO(data) as stream:
    with io.BytesIO(data) as stream:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：img = Image.open(stream)
        img = Image.open(stream)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：img.load()
        img.load()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：img = img.convert("RGB")
        img = img.convert("RGB")

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return img
    return img
