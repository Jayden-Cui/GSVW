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
# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""The combined loss functions for continuous-space tokenizers training."""
"""The combined loss functions for continuous-space tokenizers training."""

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.nn as nn
import torch.nn as nn
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from skimage.metrics import structural_similarity as ssim
from skimage.metrics import structural_similarity as ssim

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.latent_dynamics.modules.utils import time2batch
from videoworld2.latent_dynamics.modules.utils import time2batch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import LazyDict, instantiate
from imaginaire.lazy_config import LazyDict, instantiate

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_VALID_METRIC_NAMES = ["PSNR", "SSIM", "CodeUsage"]
_VALID_METRIC_NAMES = ["PSNR", "SSIM", "CodeUsage"]
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_UINT8_MAX_F = float(torch.iinfo(torch.uint8).max)
_UINT8_MAX_F = float(torch.iinfo(torch.uint8).max)
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_FLOAT32_EPS = torch.finfo(torch.float32).eps
_FLOAT32_EPS = torch.finfo(torch.float32).eps
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_RECONSTRUCTION = "reconstructions"
_RECONSTRUCTION = "reconstructions"
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_QUANT_INFO = "quant_info"
_QUANT_INFO = "quant_info"


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class TokenizerMetric(nn.Module):
class TokenizerMetric(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, config) -> None:
    def __init__(self, config) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.config = config
        self.config = config
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.metric_modules = nn.ModuleDict()
        self.metric_modules = nn.ModuleDict()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key in _VALID_METRIC_NAMES:
        for key in _VALID_METRIC_NAMES:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.metric_modules[key] = instantiate(getattr(config, key)) if hasattr(config, key) else NUL...
            self.metric_modules[key] = instantiate(getattr(config, key)) if hasattr(config, key) else NULLMetric()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(
    def forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, inputs: dict[str, torch.Tensor], output_batch: dict[str, torch.Tensor], iteration: int
        self, inputs: dict[str, torch.Tensor], output_batch: dict[str, torch.Tensor], iteration: int
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> dict[str, torch.Tensor]:
    ) -> dict[str, torch.Tensor]:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：metric = dict()
        metric = dict()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _, module in self.metric_modules.items():
        for _, module in self.metric_modules.items():
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：metric.update(module(inputs, output_batch, iteration))
            metric.update(module(inputs, output_batch, iteration))
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return dict(metric=metric)
        return dict(metric=metric)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class NULLMetric(torch.nn.Module):
class NULLMetric(torch.nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self) -> None:
    def __init__(self) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(
    def forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, inputs: dict[str, torch.Tensor], output_batch: dict[str, torch.Tensor], iteration: int
        self, inputs: dict[str, torch.Tensor], output_batch: dict[str, torch.Tensor], iteration: int
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> dict[str, torch.Tensor]:
    ) -> dict[str, torch.Tensor]:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return dict()
        return dict()


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class PSNRMetric(torch.nn.Module):
class PSNRMetric(torch.nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self) -> None:
    def __init__(self) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(
    def forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, inputs: dict[str, torch.Tensor], output_batch: dict[str, torch.Tensor], iteration: int
        self, inputs: dict[str, torch.Tensor], output_batch: dict[str, torch.Tensor], iteration: int
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> dict[str, torch.Tensor]:
    ) -> dict[str, torch.Tensor]:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：reconstructions = output_batch[_RECONSTRUCTION]
        reconstructions = output_batch[_RECONSTRUCTION]
        # 中文说明：根据条件选择执行分支；代码：if inputs.ndim == 5:
        if inputs.ndim == 5:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：inputs, _ = time2batch(inputs)
            inputs, _ = time2batch(inputs)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：reconstructions, _ = time2batch(reconstructions)
            reconstructions, _ = time2batch(reconstructions)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Normalize to uint8 [0..255] range.
        # Normalize to uint8 [0..255] range.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：true_image = (inputs.to(torch.float32) + 1) / 2
        true_image = (inputs.to(torch.float32) + 1) / 2
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pred_image = (reconstructions.to(torch.float32) + 1) / 2
        pred_image = (reconstructions.to(torch.float32) + 1) / 2
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：true_image = (true_image * _UINT8_MAX_F + 0.5).to(torch.uint8)
        true_image = (true_image * _UINT8_MAX_F + 0.5).to(torch.uint8)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pred_image = (pred_image * _UINT8_MAX_F + 0.5).to(torch.uint8)
        pred_image = (pred_image * _UINT8_MAX_F + 0.5).to(torch.uint8)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Calculate PNSR, based on Mean Squared Error (MSE)
        # Calculate PNSR, based on Mean Squared Error (MSE)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：true_image = true_image.to(torch.float32)
        true_image = true_image.to(torch.float32)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pred_image = pred_image.to(torch.float32)
        pred_image = pred_image.to(torch.float32)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mse = torch.mean((true_image - pred_image) ** 2, dim=(1, 2, 3))
        mse = torch.mean((true_image - pred_image) ** 2, dim=(1, 2, 3))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：psnr = 10 * torch.log10(_UINT8_MAX_F**2 / (mse + _FLOAT32_EPS))
        psnr = 10 * torch.log10(_UINT8_MAX_F**2 / (mse + _FLOAT32_EPS))
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return dict(PSNR=torch.mean(psnr))
        return dict(PSNR=torch.mean(psnr))


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class SSIMMetric(torch.nn.Module):
class SSIMMetric(torch.nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self) -> None:
    def __init__(self) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(
    def forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, inputs: dict[str, torch.Tensor], output_batch: dict[str, torch.Tensor], iteration: int
        self, inputs: dict[str, torch.Tensor], output_batch: dict[str, torch.Tensor], iteration: int
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> dict[str, torch.Tensor]:
    ) -> dict[str, torch.Tensor]:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：reconstructions = output_batch[_RECONSTRUCTION]
        reconstructions = output_batch[_RECONSTRUCTION]
        # 中文说明：根据条件选择执行分支；代码：if inputs.ndim == 5:
        if inputs.ndim == 5:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：inputs, _ = time2batch(inputs)
            inputs, _ = time2batch(inputs)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：reconstructions, _ = time2batch(reconstructions)
            reconstructions, _ = time2batch(reconstructions)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Normalize to uint8 [0..255] range.
        # Normalize to uint8 [0..255] range.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：true_image = (inputs.to(torch.float32) + 1) / 2
        true_image = (inputs.to(torch.float32) + 1) / 2
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pred_image = (reconstructions.to(torch.float32) + 1) / 2
        pred_image = (reconstructions.to(torch.float32) + 1) / 2
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：true_image = (true_image * _UINT8_MAX_F + 0.5).to(torch.uint8)
        true_image = (true_image * _UINT8_MAX_F + 0.5).to(torch.uint8)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pred_image = (pred_image * _UINT8_MAX_F + 0.5).to(torch.uint8)
        pred_image = (pred_image * _UINT8_MAX_F + 0.5).to(torch.uint8)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Move tensors to CPU and convert to numpy arrays
        # Move tensors to CPU and convert to numpy arrays
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：true_image_np = true_image.permute(0, 2, 3, 1).cpu().numpy()
        true_image_np = true_image.permute(0, 2, 3, 1).cpu().numpy()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pred_image_np = pred_image.permute(0, 2, 3, 1).cpu().numpy()
        pred_image_np = pred_image.permute(0, 2, 3, 1).cpu().numpy()

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Calculate SSIM for each image in the batch and average over the batch
        # Calculate SSIM for each image in the batch and average over the batch
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ssim_values = []
        ssim_values = []
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for true_image_i, pred_image_i in zip(true_image_np, pred_image_np):
        for true_image_i, pred_image_i in zip(true_image_np, pred_image_np):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ssim_value = ssim(true_image_i, pred_image_i, data_range=_UINT8_MAX_F, multichannel=True, cha...
            ssim_value = ssim(true_image_i, pred_image_i, data_range=_UINT8_MAX_F, multichannel=True, channel_axis=-1)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ssim_values.append(ssim_value)
            ssim_values.append(ssim_value)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ssim_mean = np.mean(ssim_values)
        ssim_mean = np.mean(ssim_values)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return dict(SSIM=torch.tensor(ssim_mean, dtype=torch.float32, device=inputs.device))
        return dict(SSIM=torch.tensor(ssim_mean, dtype=torch.float32, device=inputs.device))


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class CodeUsageMetric(torch.nn.Module):
class CodeUsageMetric(torch.nn.Module):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Calculate the perplexity of codebook usage (only for discrete tokenizers)

    :param codebook_indices: Tensor of codebook indices (quant_info)
    :param codebook_size: The total number of codebook entries
    :return: Perplexity of the codebook usage
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, codebook_size: int) -> None:
    def __init__(self, codebook_size: int) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.codebook_size = codebook_size
        self.codebook_size = codebook_size

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(
    def forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, inputs: dict[str, torch.Tensor], output_batch: dict[str, torch.Tensor], iteration: int
        self, inputs: dict[str, torch.Tensor], output_batch: dict[str, torch.Tensor], iteration: int
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> dict[str, torch.Tensor]:
    ) -> dict[str, torch.Tensor]:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：code_indices = output_batch[_QUANT_INFO]
        code_indices = output_batch[_QUANT_INFO]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：usage_counts = torch.bincount(code_indices.flatten().int(), minlength=self.codebook_size)
        usage_counts = torch.bincount(code_indices.flatten().int(), minlength=self.codebook_size)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：total_usage = usage_counts.sum().float()
        total_usage = usage_counts.sum().float()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：usage_probs = usage_counts.float() / total_usage
        usage_probs = usage_counts.float() / total_usage
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：entropy = -torch.sum(usage_probs * torch.log(usage_probs + _FLOAT32_EPS))
        entropy = -torch.sum(usage_probs * torch.log(usage_probs + _FLOAT32_EPS))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：perplexity = torch.exp(entropy)
        perplexity = torch.exp(entropy)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return dict(CodeUsage=torch.tensor(perplexity, dtype=torch.float32, device=code_indices.device))
        return dict(CodeUsage=torch.tensor(perplexity, dtype=torch.float32, device=code_indices.device))
