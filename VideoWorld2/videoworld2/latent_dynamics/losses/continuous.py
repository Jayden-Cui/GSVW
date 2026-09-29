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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import einops
import einops
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.nn as nn
import torch.nn as nn
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.nn.functional as F
import torch.nn.functional as F
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.utils.checkpoint as checkpoint
import torch.utils.checkpoint as checkpoint
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torchvision.models.optical_flow as optical_flow
import torchvision.models.optical_flow as optical_flow

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.latent_dynamics.modules.utils import batch2time, time2batch
from videoworld2.latent_dynamics.modules.utils import batch2time, time2batch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.latent_dynamics.losses import ReduceMode
from videoworld2.latent_dynamics.losses import ReduceMode
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.latent_dynamics.losses.lpips import LPIPS
from videoworld2.latent_dynamics.losses.lpips import LPIPS
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import LazyDict, instantiate
from imaginaire.lazy_config import LazyDict, instantiate

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：IMAGE_KEY = "images"
IMAGE_KEY = "images"
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：VIDEO_KEY = "video"
VIDEO_KEY = "video"
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：RECON_KEY = "reconstructions"
RECON_KEY = "reconstructions"
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：LATENT_KEY = "latent"
LATENT_KEY = "latent"
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：INPUT_KEY = "INPUT"
INPUT_KEY = "INPUT"
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：MASK_KEY = "loss_mask"
MASK_KEY = "loss_mask"

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_VALID_LOSS_NAMES = ["color", "perceptual", "flow", "kl", "video_consistency"]
_VALID_LOSS_NAMES = ["color", "perceptual", "flow", "kl", "video_consistency"]
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：VIDEO_CONSISTENCY_LOSS = "video_consistency"
VIDEO_CONSISTENCY_LOSS = "video_consistency"
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：RECON_CONSISTENCY_KEY = f"{RECON_KEY}_consistency"
RECON_CONSISTENCY_KEY = f"{RECON_KEY}_consistency"


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class TokenizerLoss(nn.Module):
class TokenizerLoss(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, config) -> None:
    def __init__(self, config) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.config = config
        self.config = config
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_reduce = ReduceMode(config.reduce.upper()) if hasattr(config, "reduce") else None
        _reduce = ReduceMode(config.reduce.upper()) if hasattr(config, "reduce") else None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.reduce = _reduce.function
        self.reduce = _reduce.function
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.loss_modules = nn.ModuleDict()
        self.loss_modules = nn.ModuleDict()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key in _VALID_LOSS_NAMES:
        for key in _VALID_LOSS_NAMES:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.loss_modules[key] = instantiate(getattr(config, key)) if hasattr(config, key) else NullL...
            self.loss_modules[key] = instantiate(getattr(config, key)) if hasattr(config, key) else NullLoss()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, inputs, output_batch, iteration) -> tuple[dict[str, torch.Tensor], torch.Te...
    def forward(self, inputs, output_batch, iteration) -> tuple[dict[str, torch.Tensor], torch.Tensor]:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：loss = dict()
        loss = dict()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：total_loss = 0.0
        total_loss = 0.0

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：inputs[MASK_KEY] = torch.ones_like(inputs[INPUT_KEY])
        inputs[MASK_KEY] = torch.ones_like(inputs[INPUT_KEY])
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Calculates reconstruction losses (`total_loss`).
        # Calculates reconstruction losses (`total_loss`).
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key, module in self.loss_modules.items():
        for key, module in self.loss_modules.items():
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：curr_loss = module(inputs, output_batch, iteration)
            curr_loss = module(inputs, output_batch, iteration)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：loss.update({k: torch.mean(v) for k, v in curr_loss.items()})
            loss.update({k: torch.mean(v) for k, v in curr_loss.items()})
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：total_loss += sum([self.reduce(v) if (v.dim() > 0) else v for v in curr_loss.values()])
            total_loss += sum([self.reduce(v) if (v.dim() > 0) else v for v in curr_loss.values()])

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：loss.update({k: torch.mean(v) for k, v in curr_loss.items()})
        loss.update({k: torch.mean(v) for k, v in curr_loss.items()})

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Computes the overall loss as sum of the reconstruction losses and the generator loss.
        # Computes the overall loss as sum of the reconstruction losses and the generator loss.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：total_loss += sum([self.reduce(v) if (v.dim() > 0) else v for v in curr_loss.values()])
        total_loss += sum([self.reduce(v) if (v.dim() > 0) else v for v in curr_loss.values()])
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return dict(loss=loss), total_loss
        return dict(loss=loss), total_loss


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class WeightScheduler(torch.nn.Module):
class WeightScheduler(torch.nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, boundaries, values):
    def __init__(self, boundaries, values):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.boundaries = list(boundaries)
        self.boundaries = list(boundaries)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.values = list(values)
        self.values = list(values)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, iteration):
    def forward(self, iteration):
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for boundary, value in zip(self.boundaries, self.values):
        for boundary, value in zip(self.boundaries, self.values):
            # 中文说明：根据条件选择执行分支；代码：if iteration < boundary:
            if iteration < boundary:
                # 中文说明：从当前函数返回结果或结束函数执行；代码：return value
                return value
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.values[-1]
        return self.values[-1]


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class NullLoss(torch.nn.Module):
class NullLoss(torch.nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self) -> None:
    def __init__(self) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, inputs, output_batch, iteration) -> dict[dict, torch.Tensor]:
    def forward(self, inputs, output_batch, iteration) -> dict[dict, torch.Tensor]:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return dict()
        return dict()


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ColorLoss(torch.nn.Module):
class ColorLoss(torch.nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, config) -> None:
    def __init__(self, config) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.schedule = WeightScheduler(boundaries=config.boundaries, values=config.values)
        self.schedule = WeightScheduler(boundaries=config.boundaries, values=config.values)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, inputs, output_batch, iteration) -> dict[str, torch.Tensor]:
    def forward(self, inputs, output_batch, iteration) -> dict[str, torch.Tensor]:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：reconstructions = output_batch[RECON_KEY]
        reconstructions = output_batch[RECON_KEY]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：weights = inputs[MASK_KEY]
        weights = inputs[MASK_KEY]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：recon = weights * torch.abs(inputs[INPUT_KEY].contiguous() - reconstructions.contiguous())
        recon = weights * torch.abs(inputs[INPUT_KEY].contiguous() - reconstructions.contiguous())
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：color_weighted = self.schedule(iteration) * recon
        color_weighted = self.schedule(iteration) * recon
        # 中文说明：根据条件选择执行分支；代码：if torch.isnan(color_weighted).any():
        if torch.isnan(color_weighted).any():
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError("[COLOR] NaN detected in loss")
            raise ValueError("[COLOR] NaN detected in loss")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return dict(color=color_weighted)
        return dict(color=color_weighted)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class KLLoss(torch.nn.Module):
class KLLoss(torch.nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, config) -> None:
    def __init__(self, config) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.schedule = WeightScheduler(boundaries=config.boundaries, values=config.values)
        self.schedule = WeightScheduler(boundaries=config.boundaries, values=config.values)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def kl(self, mean, logvar):
    def kl(self, mean, logvar):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_dims = [idx for idx in range(1, mean.ndim)]
        _dims = [idx for idx in range(1, mean.ndim)]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：var = torch.exp(logvar)
        var = torch.exp(logvar)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return 0.5 * (torch.pow(mean, 2) + var - 1.0 - logvar)
        return 0.5 * (torch.pow(mean, 2) + var - 1.0 - logvar)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, inputs, output_batch, iteration) -> dict[str, torch.Tensor]:
    def forward(self, inputs, output_batch, iteration) -> dict[str, torch.Tensor]:
        # 中文说明：根据条件选择执行分支；代码：if "posteriors" not in output_batch: # No KL loss for discrete tokens.
        if "posteriors" not in output_batch:  # No KL loss for discrete tokens.
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return dict()
            return dict()
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：mean, logvar = output_batch["posteriors"]
        mean, logvar = output_batch["posteriors"]
        # 中文说明：根据条件选择执行分支；代码：if mean.ndim == 1: # No KL if the mean is a scalar.
        if mean.ndim == 1:  # No KL if the mean is a scalar.
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return dict()
            return dict()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kl = self.kl(mean, logvar)
        kl = self.kl(mean, logvar)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kl_weighted = self.schedule(iteration) * kl
        kl_weighted = self.schedule(iteration) * kl
        # 中文说明：根据条件选择执行分支；代码：if torch.isnan(kl_weighted).any():
        if torch.isnan(kl_weighted).any():
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError("[KL] NaN detected in loss")
            raise ValueError("[KL] NaN detected in loss")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return dict(kl=kl_weighted)
        return dict(kl=kl_weighted)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class PerceptualLoss(LPIPS):
class PerceptualLoss(LPIPS):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Relevant changes that're internal to us:
    """Relevant changes that're internal to us:

    - Remove linear projection layers, simply use the raw pre-normalized features.
    - Use pyramid-layer weights: [1.0 / 2.6, 1.0 / 4.8, 1.0 / 3.7, 1.0 / 5.6, 10.0 / 1.5].
    - Accepts pixel-wise masks and modulates the features before norm calculation.
    - Implements gram-matrix and correlation losses.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, config):
    def __init__(self, config):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super(PerceptualLoss, self).__init__(config.checkpoint_activations)
        super(PerceptualLoss, self).__init__(config.checkpoint_activations)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.net = self.net.eval()
        self.net = self.net.eval()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.gram_enabled = config.gram_enabled
        self.gram_enabled = config.gram_enabled
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.corr_enabled = config.corr_enabled
        self.corr_enabled = config.corr_enabled
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.layer_weights = list(config.layer_weights)
        self.layer_weights = list(config.layer_weights)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.lpips_schedule = WeightScheduler(config.lpips_boundaries, config.lpips_values)
        self.lpips_schedule = WeightScheduler(config.lpips_boundaries, config.lpips_values)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.gram_schedule = WeightScheduler(config.gram_boundaries, config.gram_values)
        self.gram_schedule = WeightScheduler(config.gram_boundaries, config.gram_values)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.corr_schedule = WeightScheduler(config.corr_boundaries, config.corr_values)
        self.corr_schedule = WeightScheduler(config.corr_boundaries, config.corr_values)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.checkpoint_activations = config.checkpoint_activations
        self.checkpoint_activations = config.checkpoint_activations

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _temporal_gram_matrix(self, x, batch_size=None):
    def _temporal_gram_matrix(self, x, batch_size=None):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = batch2time(x, batch_size)
        x = batch2time(x, batch_size)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：c, t, h, w = x.shape[-4], x.shape[-3], x.shape[-2], x.shape[-1]
        c, t, h, w = x.shape[-4], x.shape[-3], x.shape[-2], x.shape[-1]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：reshaped_x = torch.reshape(x, [-1, c, t * h * w])
        reshaped_x = torch.reshape(x, [-1, c, t * h * w])
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return torch.matmul(reshaped_x, reshaped_x.transpose(1, 2)) / float(t * h * w)
        return torch.matmul(reshaped_x, reshaped_x.transpose(1, 2)) / float(t * h * w)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _gram_matrix(self, x, batch_size=None):
    def _gram_matrix(self, x, batch_size=None):
        # 中文说明：根据条件选择执行分支；代码：if batch_size is not None and x.shape[0] != batch_size:
        if batch_size is not None and x.shape[0] != batch_size:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return self._temporal_gram_matrix(x, batch_size)
            return self._temporal_gram_matrix(x, batch_size)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：c, h, w = x.shape[-3], x.shape[-2], x.shape[-1]
        c, h, w = x.shape[-3], x.shape[-2], x.shape[-1]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：reshaped_x = torch.reshape(x, [-1, c, h * w])
        reshaped_x = torch.reshape(x, [-1, c, h * w])
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return torch.matmul(reshaped_x, reshaped_x.transpose(1, 2)) / float(h * w)
        return torch.matmul(reshaped_x, reshaped_x.transpose(1, 2)) / float(h * w)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, inputs, output_batch, iteration):
    def forward(self, inputs, output_batch, iteration):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_dict = dict()
        output_dict = dict()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：reconstructions = output_batch[RECON_KEY]
        reconstructions = output_batch[RECON_KEY]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：weights = inputs[MASK_KEY]
        weights = inputs[MASK_KEY]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_images = inputs[INPUT_KEY]
        input_images = inputs[INPUT_KEY]

        # 中文说明：根据条件选择执行分支；代码：if input_images.ndim == 5:
        if input_images.ndim == 5:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：input_images, batch_size = time2batch(input_images)
            input_images, batch_size = time2batch(input_images)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：reconstructions, _ = time2batch(reconstructions)
            reconstructions, _ = time2batch(reconstructions)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：weights, _ = time2batch(weights)
            weights, _ = time2batch(weights)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch_size = input_images.shape[0]
            batch_size = input_images.shape[0]

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：in0_input, in1_input = (self.scaling_layer(input_images), self.scaling_layer(reconstructions))
        in0_input, in1_input = (self.scaling_layer(input_images), self.scaling_layer(reconstructions))
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：outs0, outs1 = self.net(in0_input), self.net(in1_input)
        outs0, outs1 = self.net(in0_input), self.net(in1_input)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_layer_weights = self.layer_weights
        _layer_weights = self.layer_weights
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：weights_map, res, diffs = {}, {}, {}
        weights_map, res, diffs = {}, {}, {}
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for kk in range(len(self.chns)):
        for kk in range(len(self.chns)):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：weights_map[kk] = torch.nn.functional.interpolate(weights[:, :1, ...], outs0[kk].shape[-2:])
            weights_map[kk] = torch.nn.functional.interpolate(weights[:, :1, ...], outs0[kk].shape[-2:])
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：diffs[kk] = weights_map[kk] * torch.abs(outs0[kk] - outs1[kk])
            diffs[kk] = weights_map[kk] * torch.abs(outs0[kk] - outs1[kk])
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：res[kk] = _layer_weights[kk] * diffs[kk].mean([1, 2, 3], keepdim=True)
            res[kk] = _layer_weights[kk] * diffs[kk].mean([1, 2, 3], keepdim=True)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：val = res[0]
        val = res[0]
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for ll in range(1, len(self.chns)):
        for ll in range(1, len(self.chns)):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：val += res[ll]
            val += res[ll]
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Scale by number of pixels to match pixel-wise losses.
        # Scale by number of pixels to match pixel-wise losses.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：val = val.expand(-1, input_images.shape[-3], input_images.shape[-2], input_images.shape[-1])
        val = val.expand(-1, input_images.shape[-3], input_images.shape[-2], input_images.shape[-1])
        # 中文说明：根据条件选择执行分支；代码：if batch_size != input_images.shape[0]:
        if batch_size != input_images.shape[0]:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：val = batch2time(val, batch_size)
            val = batch2time(val, batch_size)
        # 中文说明：根据条件选择执行分支；代码：if torch.isnan(val).any():
        if torch.isnan(val).any():
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError("[LPIPS] NaN detected in loss")
            raise ValueError("[LPIPS] NaN detected in loss")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_dict["lpips"] = self.lpips_schedule(iteration) * val
        output_dict["lpips"] = self.lpips_schedule(iteration) * val

        # 中文说明：根据条件选择执行分支；代码：if self.gram_enabled and self.gram_schedule(iteration) > 0.0:
        if self.gram_enabled and self.gram_schedule(iteration) > 0.0:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_chans = len(self.chns)
            num_chans = len(self.chns)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：grams0 = [self._gram_matrix(weights_map[kk] * outs0[kk], batch_size) for kk in range(num_chans)]
            grams0 = [self._gram_matrix(weights_map[kk] * outs0[kk], batch_size) for kk in range(num_chans)]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：grams1 = [self._gram_matrix(weights_map[kk] * outs1[kk], batch_size) for kk in range(num_chans)]
            grams1 = [self._gram_matrix(weights_map[kk] * outs1[kk], batch_size) for kk in range(num_chans)]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gram_diffs = [(grams0[kk] - grams1[kk]) ** 2 for kk in range(num_chans)]
            gram_diffs = [(grams0[kk] - grams1[kk]) ** 2 for kk in range(num_chans)]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：grams_res = [_layer_weights[kk] * gram_diffs[kk].mean([1, 2], keepdim=True) for kk in range(n...
            grams_res = [_layer_weights[kk] * gram_diffs[kk].mean([1, 2], keepdim=True) for kk in range(num_chans)]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gram_val = grams_res[0]
            gram_val = grams_res[0]
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for ll in range(1, len(self.chns)):
            for ll in range(1, len(self.chns)):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gram_val += grams_res[ll]
                gram_val += grams_res[ll]

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Scale by number of total pixels to match pixel-wise losses.
            # Scale by number of total pixels to match pixel-wise losses.
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gram_val = gram_val.unsqueeze(1).expand(
            gram_val = gram_val.unsqueeze(1).expand(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：-1, input_images.shape[-3], input_images.shape[-2], input_images.shape[-1]
                -1, input_images.shape[-3], input_images.shape[-2], input_images.shape[-1]
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：根据条件选择执行分支；代码：if batch_size != input_images.shape[0]:
            if batch_size != input_images.shape[0]:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gram_val = batch2time(gram_val, batch_size)
                gram_val = batch2time(gram_val, batch_size)
            # 中文说明：根据条件选择执行分支；代码：if torch.isnan(gram_val).any():
            if torch.isnan(gram_val).any():
                # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError("[GRAM] NaN detected in loss")
                raise ValueError("[GRAM] NaN detected in loss")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_dict["gram"] = self.gram_schedule(iteration) * gram_val
            output_dict["gram"] = self.gram_schedule(iteration) * gram_val
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return output_dict
        return output_dict

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def torch_compile(self):
    def torch_compile(self):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        This method invokes torch.compile() on this loss
        """
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# cuda-graphs crash after 1k iterations
        # cuda-graphs crash after 1k iterations
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.net = torch.compile(self.net, dynamic=False)
        self.net = torch.compile(self.net, dynamic=False)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class FlowLoss(torch.nn.Module):
class FlowLoss(torch.nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, config) -> None:
    def __init__(self, config) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.schedule = WeightScheduler(config.boundaries, config.values)
        self.schedule = WeightScheduler(config.boundaries, config.values)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.scale = config.scale
        self.scale = config.scale
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dtype = getattr(torch, config.dtype)
        self.dtype = getattr(torch, config.dtype)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.checkpoint_activations = config.checkpoint_activations
        self.checkpoint_activations = config.checkpoint_activations
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.enabled = config.enabled
        self.enabled = config.enabled

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：current_device = torch.device(torch.cuda.current_device())
        current_device = torch.device(torch.cuda.current_device())

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# In order to be able to run model in bf16 we need to change make_coords_grid()
        # In order to be able to run model in bf16 we need to change make_coords_grid()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# to allow it to return arbitrary type provided by us in argument
        # to allow it to return arbitrary type provided by us in argument
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# the line from orginal implementation that caused results to be only fp32 is commented
        # the line from orginal implementation that caused results to be only fp32 is commented
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Additionally I've changed that function to run on GPU instead of CPU, which results in
        # Additionally I've changed that function to run on GPU instead of CPU, which results in
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# less graph breaks when torch.compile() is used
        # less graph breaks when torch.compile() is used
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# This function is copied from
        # This function is copied from
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# https://github.com/pytorch/vision/blob/main/torchvision/models/optical_flow/_utils.py#L22
        # https://github.com/pytorch/vision/blob/main/torchvision/models/optical_flow/_utils.py#L22
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# commit: b06ea39d5f0adbe949d08257837bda912339e415
        # commit: b06ea39d5f0adbe949d08257837bda912339e415
        # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def make_coords_grid(
        def make_coords_grid(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：batch_size: int, h: int, w: int, device: torch.device = current_device, dtype: torch.dtype = ...
            batch_size: int, h: int, w: int, device: torch.device = current_device, dtype: torch.dtype = self.dtype
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
        ):
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Original: def make_coords_grid(batch_size: int, h: int, w: int, device: str = "cpu"):
            # Original: def make_coords_grid(batch_size: int, h: int, w: int, device: str = "cpu"):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：device = torch.device(device)
            device = torch.device(device)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：coords = torch.meshgrid(torch.arange(h, device=device), torch.arange(w, device=device), index...
            coords = torch.meshgrid(torch.arange(h, device=device), torch.arange(w, device=device), indexing="ij")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：coords = torch.stack(coords[::-1], dim=0).to(dtype)
            coords = torch.stack(coords[::-1], dim=0).to(dtype)
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Original: coords = torch.stack(coords[::-1], dim=0).float()
            # Original: coords = torch.stack(coords[::-1], dim=0).float()
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return coords[None].repeat(batch_size, 1, 1, 1)
            return coords[None].repeat(batch_size, 1, 1, 1)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# We also need to specify output dtype of torch.linspace() in index_pyramid()
        # We also need to specify output dtype of torch.linspace() in index_pyramid()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# method of CorrBlock, otherwise it uses default fp32 dtype as output.
        # method of CorrBlock, otherwise it uses default fp32 dtype as output.
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Additionally I've changed that function to run on GPU instead of CPU, which results in
        # Additionally I've changed that function to run on GPU instead of CPU, which results in
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# less graph breaks when torch.compile() is used
        # less graph breaks when torch.compile() is used
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# This function is copied from
        # This function is copied from
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# https://github.com/pytorch/vision/blob/main/torchvision/models/optical_flow/raft.py#L394
        # https://github.com/pytorch/vision/blob/main/torchvision/models/optical_flow/raft.py#L394
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# commit: b06ea39d5f0adbe949d08257837bda912339e415
        # commit: b06ea39d5f0adbe949d08257837bda912339e415
        # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def index_pyramid(
        def index_pyramid(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, centroids_coords, dtype: torch.dtype = self.dtype, device: torch.device = current_device
            self, centroids_coords, dtype: torch.dtype = self.dtype, device: torch.device = current_device
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
        ):
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Original: def index_pyramid(self, centroids_coords):
            # Original: def index_pyramid(self, centroids_coords):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Return correlation features by indexing from the pyramid."""
            """Return correlation features by indexing from the pyramid."""
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：neighborhood_side_len = 2 * self.radius + 1 # see note in __init__ about out_channels
            neighborhood_side_len = 2 * self.radius + 1  # see note in __init__ about out_channels
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：di = torch.linspace(-self.radius, self.radius, neighborhood_side_len, dtype=dtype, device=dev...
            di = torch.linspace(-self.radius, self.radius, neighborhood_side_len, dtype=dtype, device=device)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dj = torch.linspace(-self.radius, self.radius, neighborhood_side_len, dtype=dtype, device=dev...
            dj = torch.linspace(-self.radius, self.radius, neighborhood_side_len, dtype=dtype, device=device)
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Original: di = torch.linspace(-self.radius, self.radius, neighborhood_side_len)
            # Original: di = torch.linspace(-self.radius, self.radius, neighborhood_side_len)
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Original: dj = torch.linspace(-self.radius, self.radius, neighborhood_side_len)
            # Original: dj = torch.linspace(-self.radius, self.radius, neighborhood_side_len)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：delta = torch.stack(torch.meshgrid(di, dj, indexing="ij"), dim=-1).to(centroids_coords.device)
            delta = torch.stack(torch.meshgrid(di, dj, indexing="ij"), dim=-1).to(centroids_coords.device)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：delta = delta.view(1, neighborhood_side_len, neighborhood_side_len, 2)
            delta = delta.view(1, neighborhood_side_len, neighborhood_side_len, 2)

            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：batch_size, _, h, w = centroids_coords.shape # _ = 2
            batch_size, _, h, w = centroids_coords.shape  # _ = 2
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：centroids_coords = centroids_coords.permute(0, 2, 3, 1).reshape(batch_size * h * w, 1, 1, 2)
            centroids_coords = centroids_coords.permute(0, 2, 3, 1).reshape(batch_size * h * w, 1, 1, 2)

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：indexed_pyramid = []
            indexed_pyramid = []
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for corr_volume in self.corr_pyramid:
            for corr_volume in self.corr_pyramid:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sampling_coords = centroids_coords + delta # end shape is (batch_size * h * w, side_len, side...
                sampling_coords = centroids_coords + delta  # end shape is (batch_size * h * w, side_len, side_len, 2)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：indexed_corr_volume = optical_flow.raft.grid_sample(
                indexed_corr_volume = optical_flow.raft.grid_sample(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：corr_volume, sampling_coords, align_corners=True, mode="bilinear"
                    corr_volume, sampling_coords, align_corners=True, mode="bilinear"
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：).view(batch_size, h, w, -1)
                ).view(batch_size, h, w, -1)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：indexed_pyramid.append(indexed_corr_volume)
                indexed_pyramid.append(indexed_corr_volume)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：centroids_coords = centroids_coords / 2
                centroids_coords = centroids_coords / 2

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：corr_features = torch.cat(indexed_pyramid, dim=-1).permute(0, 3, 1, 2).contiguous()
            corr_features = torch.cat(indexed_pyramid, dim=-1).permute(0, 3, 1, 2).contiguous()

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：expected_output_shape = (batch_size, self.out_channels, h, w)
            expected_output_shape = (batch_size, self.out_channels, h, w)
            # 中文说明：根据条件选择执行分支；代码：if corr_features.shape != expected_output_shape:
            if corr_features.shape != expected_output_shape:
                # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(
                raise ValueError(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Output shape of index pyramid is incorrect. Should be {expected_output_shape}, got {corr_fe...
                    f"Output shape of index pyramid is incorrect. Should be {expected_output_shape}, got {corr_features.shape}"
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )

            # 中文说明：从当前函数返回结果或结束函数执行；代码：return corr_features
            return corr_features

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：optical_flow.raft.make_coords_grid = make_coords_grid
        optical_flow.raft.make_coords_grid = make_coords_grid
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：optical_flow.raft.CorrBlock.index_pyramid = index_pyramid
        optical_flow.raft.CorrBlock.index_pyramid = index_pyramid

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：flow_model = optical_flow.raft_large(pretrained=True, progress=False)
        flow_model = optical_flow.raft_large(pretrained=True, progress=False)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：flow_model.requires_grad_(False)
        flow_model.requires_grad_(False)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：flow_model.eval()
        flow_model.eval()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：flow_model = flow_model.to(self.dtype)
        flow_model = flow_model.to(self.dtype)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.flow_model = flow_model
        self.flow_model = flow_model

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _run_model(self, input1: torch.Tensor, input2: torch.Tensor) -> torch.Tensor:
    def _run_model(self, input1: torch.Tensor, input2: torch.Tensor) -> torch.Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Runs flow_model in the forward mode on explicit dtype=float32.
        """Runs flow_model in the forward mode on explicit dtype=float32.

        Args:
            input1: First video frames batch, layout (T, C, H, W), bfloat16.
            input2: Next video frames batch, layout (T, C, H, W), bfloat16.

        Returns:
            Forward optical flow, (T, 2, H, W), bfloat16.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_dtype = input1.dtype
        input_dtype = input1.dtype
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：flow_output = self.flow_model.to(self.dtype)(input1.to(self.dtype), input2.to(self.dtype))[-1]
        flow_output = self.flow_model.to(self.dtype)(input1.to(self.dtype), input2.to(self.dtype))[-1]
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return flow_output.to(input_dtype)
        return flow_output.to(input_dtype)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _run_model_fwd(self, input_video: torch.Tensor) -> torch.Tensor:
    def _run_model_fwd(self, input_video: torch.Tensor) -> torch.Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Runs foward flow on a batch of videos, one batch at a time.
        """Runs foward flow on a batch of videos, one batch at a time.
        Args:
            input_video: The input batch of videos, layout (B, T, C, H, W).

        Returns:
            Forward optical flow, layout (B, 2, T-1, H, W).
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_list = list()
        output_list = list()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for fwd_input_frames in input_video:
        for fwd_input_frames in input_video:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fwd_input_frames = fwd_input_frames.transpose(1, 0)
            fwd_input_frames = fwd_input_frames.transpose(1, 0)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fwd_flow_output = self._run_model(fwd_input_frames[:-1], fwd_input_frames[1:])
            fwd_flow_output = self._run_model(fwd_input_frames[:-1], fwd_input_frames[1:])
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：output_list.append(fwd_flow_output.transpose(1, 0))
            output_list.append(fwd_flow_output.transpose(1, 0))
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return torch.stack(output_list, dim=0)
        return torch.stack(output_list, dim=0)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _bidirectional_flow(self, input_video: torch.Tensor) -> torch.Tensor:
    def _bidirectional_flow(self, input_video: torch.Tensor) -> torch.Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""The bidirectional optical flow on a batch of videos.
        """The bidirectional optical flow on a batch of videos.

        The forward and backward flows are averaged to get the bidirectional flow.
        To reduce memory pressure, the input video is scaled down by a factor of `self.scale`,
        and rescaled back to match other pixel-wise losses.

        Args:
            input_video: The input batch of videos, layout (B, T, C, H, W).

        Returns:
            Biderectinoal flow, layout (B, 2, T-1, H, W).
        """
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# scale down the input video to reduce memory pressure.
        # scale down the input video to reduce memory pressure.
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：t, h, w = input_video.shape[-3:]
        t, h, w = input_video.shape[-3:]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_video_scaled = F.interpolate(input_video, (t, h // self.scale, w // self.scale), mode="...
        input_video_scaled = F.interpolate(input_video, (t, h // self.scale, w // self.scale), mode="trilinear")

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# forward flow.
        # forward flow.
        # 中文说明：根据条件选择执行分支；代码：if self.checkpoint_activations:
        if self.checkpoint_activations:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fwd_flow_output = checkpoint.checkpoint(self._run_model_fwd, input_video_scaled, use_reentran...
            fwd_flow_output = checkpoint.checkpoint(self._run_model_fwd, input_video_scaled, use_reentrant=False)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fwd_flow_output = self._run_model_fwd(input_video_scaled)
            fwd_flow_output = self._run_model_fwd(input_video_scaled)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# backward flow.
        # backward flow.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_video_scaled = input_video_scaled.flip([2])
        input_video_scaled = input_video_scaled.flip([2])
        # 中文说明：根据条件选择执行分支；代码：if self.checkpoint_activations:
        if self.checkpoint_activations:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：bwd_flow_output = checkpoint.checkpoint(self._run_model_fwd, input_video_scaled, use_reentran...
            bwd_flow_output = checkpoint.checkpoint(self._run_model_fwd, input_video_scaled, use_reentrant=False)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：bwd_flow_output = self._run_model_fwd(input_video_scaled)
            bwd_flow_output = self._run_model_fwd(input_video_scaled)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：bwd_flow_output = bwd_flow_output.flip([2])
        bwd_flow_output = bwd_flow_output.flip([2])

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# bidirectional flow, concat fwd and bwd along temporal axis.
        # bidirectional flow, concat fwd and bwd along temporal axis.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：flow_input = torch.cat([fwd_flow_output, bwd_flow_output], dim=2)
        flow_input = torch.cat([fwd_flow_output, bwd_flow_output], dim=2)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.scale * F.interpolate(flow_input, (2 * (t - 1), h, w), mode="trilinear")
        return self.scale * F.interpolate(flow_input, (2 * (t - 1), h, w), mode="trilinear")

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(
    def forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, inputs: dict[str, torch.Tensor], output_batch: dict[str, torch.Tensor], iteration: int
        self, inputs: dict[str, torch.Tensor], output_batch: dict[str, torch.Tensor], iteration: int
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> dict[str, torch.Tensor]:
    ) -> dict[str, torch.Tensor]:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_images = inputs[INPUT_KEY]
        input_images = inputs[INPUT_KEY]
        # 中文说明：根据条件选择执行分支；代码：if input_images.ndim == 4 or input_images.shape[2] == 1:
        if input_images.ndim == 4 or input_images.shape[2] == 1:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return dict()
            return dict()
        # 中文说明：根据条件选择执行分支；代码：if not self.enabled or self.schedule(iteration) == 0.0:
        if not self.enabled or self.schedule(iteration) == 0.0:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return dict()
            return dict()

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Biderectional flow (B, 2, 2*(T-1), H, W)
        # Biderectional flow (B, 2, 2*(T-1), H, W)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：flow_input = self._bidirectional_flow(input_images)
        flow_input = self._bidirectional_flow(input_images)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：flow_recon = self._bidirectional_flow(output_batch[RECON_KEY])
        flow_recon = self._bidirectional_flow(output_batch[RECON_KEY])

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# L1 loss on the flow. (B, 1, 2*(T-1), H, W)
        # L1 loss on the flow. (B, 1, 2*(T-1), H, W)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：flow_loss = torch.abs(flow_input - flow_recon).mean(dim=1, keepdim=True)
        flow_loss = torch.abs(flow_input - flow_recon).mean(dim=1, keepdim=True)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：flow_loss_weighted = self.schedule(iteration) * flow_loss
        flow_loss_weighted = self.schedule(iteration) * flow_loss
        # 中文说明：根据条件选择执行分支；代码：if torch.isnan(flow_loss_weighted).any():
        if torch.isnan(flow_loss_weighted).any():
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError("[FLOW] NaN detected in loss")
            raise ValueError("[FLOW] NaN detected in loss")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return dict(flow=flow_loss_weighted)
        return dict(flow=flow_loss_weighted)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def torch_compile(self):
    def torch_compile(self):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        This method invokes torch.compile() on this loss
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.flow_model = torch.compile(self.flow_model, dynamic=False)
        self.flow_model = torch.compile(self.flow_model, dynamic=False)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class VideoConsistencyLoss(torch.nn.Module):
class VideoConsistencyLoss(torch.nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, config) -> None:
    def __init__(self, config) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.schedule = WeightScheduler(boundaries=config.boundaries, values=config.values)
        self.schedule = WeightScheduler(boundaries=config.boundaries, values=config.values)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.enabled = config.enabled
        self.enabled = config.enabled
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_frames = config.num_frames
        self.num_frames = config.num_frames
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.step = config.step
        self.step = config.step
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_windows = None
        self.num_windows = None

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def shuffle(self, inputs: torch.Tensor) -> torch.Tensor:
    def shuffle(self, inputs: torch.Tensor) -> torch.Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        For input video of [B, 3, T, H, W], this function will reshape the video to
        the shape of [B*(T-num_frames+1)//step, 3, num_frames, H, W] using a sliding window
        This function is used to compute the temporal consistency between overlapped frames
        to enable temporal consistency
        """
        # 中文说明：检查运行时假设是否成立；代码：assert len(inputs.shape) == 5, f"inputs shape should be [B, 3, T, H, W]. currently {inputs.sh...
        assert len(inputs.shape) == 5, f"inputs shape should be [B, 3, T, H, W]. currently {inputs.shape}"
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：B, C, T, H, W = inputs.shape
        B, C, T, H, W = inputs.shape
        # 中文说明：检查运行时假设是否成立；代码：assert T >= self.num_frames, f"inputs {T} should be greater than {self.num_frames}"
        assert T >= self.num_frames, f"inputs {T} should be greater than {self.num_frames}"

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# [B, C, num_windows, H, W, num_frames]
        # [B, C, num_windows, H, W, num_frames]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：outputs = inputs.unfold(dimension=2, size=self.num_frames, step=self.step)
        outputs = inputs.unfold(dimension=2, size=self.num_frames, step=self.step)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.num_windows = outputs.shape[2]
        self.num_windows = outputs.shape[2]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：outputs = einops.rearrange(outputs, "b c m h w n -> (b m) c n h w")
        outputs = einops.rearrange(outputs, "b c m h w n -> (b m) c n h w")

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return outputs
        return outputs

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, inputs, output_batch, iteration) -> dict[str, torch.Tensor]:
    def forward(self, inputs, output_batch, iteration) -> dict[str, torch.Tensor]:
        # 中文说明：根据条件选择执行分支；代码：if not self.enabled or self.num_windows is None:
        if not self.enabled or self.num_windows is None:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return dict()
            return dict()
        # 中文说明：根据条件选择执行分支；代码：if self.schedule(iteration) == 0.0:
        if self.schedule(iteration) == 0.0:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return dict()
            return dict()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# reshape output_batch to compute loss between overlapped frames
        # reshape output_batch to compute loss between overlapped frames
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：reconstructions = output_batch[RECON_CONSISTENCY_KEY]
        reconstructions = output_batch[RECON_CONSISTENCY_KEY]
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：B, C, T, H, W = reconstructions.shape
        B, C, T, H, W = reconstructions.shape

        # 中文说明：检查运行时假设是否成立；代码：assert T == self.num_frames, f"reconstruction shape invalid (shape[2] should be {self.num_fra...
        assert T == self.num_frames, f"reconstruction shape invalid (shape[2] should be {self.num_frames})"
        # 中文说明：检查运行时假设是否成立；代码：assert (
        assert (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：B % self.num_windows == 0
            B % self.num_windows == 0
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"reconstruction shape invalid (shape[0]={B} not dividable by {self.num_windows})"
        ), f"reconstruction shape invalid (shape[0]={B} not dividable by {self.num_windows})"

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：B = B // self.num_windows
        B = B // self.num_windows
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：videos = reconstructions.view(B, self.num_windows, C, self.num_frames, H, W)
        videos = reconstructions.view(B, self.num_windows, C, self.num_frames, H, W)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Compute the L1 distance between overlapped frames for all windows at once
        # Compute the L1 distance between overlapped frames for all windows at once
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：diff = torch.mean(torch.abs(videos[:, :-1, :, self.step :, :, :] - videos[:, 1:, :, : -self.s...
        diff = torch.mean(torch.abs(videos[:, :-1, :, self.step :, :, :] - videos[:, 1:, :, : -self.step, :, :]))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：diff_weighted = self.schedule(iteration) * diff
        diff_weighted = self.schedule(iteration) * diff

        # 中文说明：根据条件选择执行分支；代码：if LATENT_KEY not in output_batch:
        if LATENT_KEY not in output_batch:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return dict(frame_consistency=diff_weighted)
            return dict(frame_consistency=diff_weighted)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：B_latent, C_latent, T_latent, H_latent, W_latent = output_batch["latent"].shape
        B_latent, C_latent, T_latent, H_latent, W_latent = output_batch["latent"].shape
        # 中文说明：检查运行时假设是否成立；代码：assert B_latent % self.num_windows == 0, f"latent batches should be divisible by {self.num_wi...
        assert B_latent % self.num_windows == 0, f"latent batches should be divisible by {self.num_windows}"

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：latents = output_batch[LATENT_KEY].view(
        latents = output_batch[LATENT_KEY].view(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：B_latent // self.num_windows, self.num_windows, C_latent, T_latent, H_latent, W_latent
            B_latent // self.num_windows, self.num_windows, C_latent, T_latent, H_latent, W_latent
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_rate = self.num_frames // T_latent
        temporal_rate = self.num_frames // T_latent
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：spatial_rate = (H // H_latent) * (W // W_latent)
        spatial_rate = (H // H_latent) * (W // W_latent)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：step_latent = self.step // temporal_rate
        step_latent = self.step // temporal_rate
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：latent_diff = torch.mean(
        latent_diff = torch.mean(
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.abs(latents[:, :-1, :, step_latent:, :, :] - latents[:, 1:, :, :-step_latent, :, :])
            torch.abs(latents[:, :-1, :, step_latent:, :, :] - latents[:, 1:, :, :-step_latent, :, :])
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：latent_diff_weighted = self.schedule(iteration) * latent_diff * (C * temporal_rate * spatial_...
        latent_diff_weighted = self.schedule(iteration) * latent_diff * (C * temporal_rate * spatial_rate) / (C_latent)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return dict(frame_consistency=diff_weighted, latent_consistency=latent_diff_weighted)
        return dict(frame_consistency=diff_weighted, latent_consistency=latent_diff_weighted)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def unshuffle(self, inputs: torch.Tensor) -> torch.Tensor:
    def unshuffle(self, inputs: torch.Tensor) -> torch.Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        For input video of [B*num_windows, 3, num_frames, H, W], this function will
        undo the shuffle to a tensor of shape [B, 3, T, H, W]
        """
        # 中文说明：检查运行时假设是否成立；代码：assert len(inputs.shape) == 5, f"inputs shape should be [B, 3, T, H, W]. currently {inputs.sh...
        assert len(inputs.shape) == 5, f"inputs shape should be [B, 3, T, H, W]. currently {inputs.shape}"
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：B, C, T, H, W = inputs.shape
        B, C, T, H, W = inputs.shape
        # 中文说明：检查运行时假设是否成立；代码：assert T == self.num_frames, f"inputs shape invalid (shape[2] should be {self.num_frames})"
        assert T == self.num_frames, f"inputs shape invalid (shape[2] should be {self.num_frames})"
        # 中文说明：检查运行时假设是否成立；代码：assert B % self.num_windows == 0, f"inputs shape invalid (shape[0]={B} not dividable by {self...
        assert B % self.num_windows == 0, f"inputs shape invalid (shape[0]={B} not dividable by {self.num_windows})"

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：B = B // self.num_windows
        B = B // self.num_windows
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：videos = inputs.view(B, self.num_windows, C, self.num_frames, H, W)
        videos = inputs.view(B, self.num_windows, C, self.num_frames, H, W)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：T = self.num_frames + (self.num_windows - 1) * self.step
        T = self.num_frames + (self.num_windows - 1) * self.step
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：current_device = torch.device(torch.cuda.current_device())
        current_device = torch.device(torch.cuda.current_device())
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：outputs = torch.zeros(B, C, T, H, W).to(inputs.dtype).to(current_device)
        outputs = torch.zeros(B, C, T, H, W).to(inputs.dtype).to(current_device)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：counter = torch.zeros_like(outputs)
        counter = torch.zeros_like(outputs)
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i in range(self.num_windows):
        for i in range(self.num_windows):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：outputs[:, :, i * self.step : i * self.step + self.num_frames, :, :] += videos[:, i, :, :, :, :]
            outputs[:, :, i * self.step : i * self.step + self.num_frames, :, :] += videos[:, i, :, :, :, :]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：counter[:, :, i * self.step : i * self.step + self.num_frames, :, :] += 1
            counter[:, :, i * self.step : i * self.step + self.num_frames, :, :] += 1
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：outputs = outputs / counter
        outputs = outputs / counter

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return outputs
        return outputs
