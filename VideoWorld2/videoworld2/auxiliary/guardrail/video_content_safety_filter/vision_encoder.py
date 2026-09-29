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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from PIL import Image
from PIL import Image
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from transformers import SiglipModel, SiglipProcessor
from transformers import SiglipModel, SiglipProcessor


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class SigLIPEncoder(torch.nn.Module):
class SigLIPEncoder(torch.nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：checkpoint_dir: str,
        checkpoint_dir: str,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model_name: str = "google/siglip-so400m-patch14-384",
        model_name: str = "google/siglip-so400m-patch14-384",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：device="cuda" if torch.cuda.is_available() else "cpu",
        device="cuda" if torch.cuda.is_available() else "cpu",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dtype=torch.float32,
        dtype=torch.float32,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.checkpoint_dir = checkpoint_dir
        self.checkpoint_dir = checkpoint_dir
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.device = device
        self.device = device
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dtype = dtype
        self.dtype = dtype
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.model = SiglipModel.from_pretrained(model_name, cache_dir=self.checkpoint_dir)
        self.model = SiglipModel.from_pretrained(model_name, cache_dir=self.checkpoint_dir)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.processor = SiglipProcessor.from_pretrained(model_name, cache_dir=self.checkpoint_dir)
        self.processor = SiglipProcessor.from_pretrained(model_name, cache_dir=self.checkpoint_dir)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.model.to(self.device, dtype=self.dtype).eval()
        self.model.to(self.device, dtype=self.dtype).eval()

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.inference_mode()
    @torch.inference_mode()
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def encode_image(self, input_img: Image.Image) -> torch.Tensor:
    def encode_image(self, input_img: Image.Image) -> torch.Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Encode an image into a feature vector."""
        """Encode an image into a feature vector."""
        # 中文说明：处理异常、清理资源或管理上下文；代码：with torch.no_grad():
        with torch.no_grad():
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：inputs = self.processor(images=input_img, return_tensors="pt").to(self.device, dtype=self.dtype)
            inputs = self.processor(images=input_img, return_tensors="pt").to(self.device, dtype=self.dtype)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：image_features = self.model.get_image_features(**inputs)
            image_features = self.model.get_image_features(**inputs)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：image_features /= image_features.norm(dim=-1, keepdim=True)
            image_features /= image_features.norm(dim=-1, keepdim=True)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return image_features
        return image_features
