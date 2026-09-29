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
# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Loss config options
"""Loss config options

Loss weights are scheduled using a piecewise linear LR schedule. The schedule is defined by a list of boundaries and values.

`boundaries` is a list of integers representing the iteration at which the weight value changes.
`values` is a list of floats representing the weight value at each boundary. It should have one more value than `boundaries`.

Example:
 A loss's weight will be:
    values[0] when step <= boundaries[0],
    values[1] when step > boundaries[0] and step <= boundaries[1],
    ..., and
    values[-1] when step > boundaries[-1].
"""
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import attrs
import attrs
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.latent_dynamics.metrics import CodeUsageMetric, PSNRMetric, SSIMMetric, Toke...
from videoworld2.latent_dynamics.metrics import CodeUsageMetric, PSNRMetric, SSIMMetric, TokenizerMetric
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.latent_dynamics.losses import ReduceMode
from videoworld2.latent_dynamics.losses import ReduceMode
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.latent_dynamics.losses.continuous import (
from videoworld2.latent_dynamics.losses.continuous import (
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ColorLoss,
    ColorLoss,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：FlowLoss,
    FlowLoss,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：KLLoss,
    KLLoss,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：PerceptualLoss,
    PerceptualLoss,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：TokenizerLoss,
    TokenizerLoss,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：VideoConsistencyLoss,
    VideoConsistencyLoss,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.latent_dynamics.modules import DiscreteQuantizer, Encoder3DType, Decoder3DType
from videoworld2.latent_dynamics.modules import DiscreteQuantizer, Encoder3DType, Decoder3DType
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.config import make_freezable
from imaginaire.config import make_freezable
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import LazyCall as L
from imaginaire.lazy_config import LazyCall as L
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import LazyDict
from imaginaire.lazy_config import LazyDict
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.latent_dynamics.discrete_video_latent_dynamic import CausalDiscreteVideoLate...
from videoworld2.latent_dynamics.discrete_video_latent_dynamic import CausalDiscreteVideoLatentDynamicTokenizer
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.latent_dynamics.cosmos_tokenizer import CausalDiscreteVideoTokenizer
from videoworld2.latent_dynamics.cosmos_tokenizer import CausalDiscreteVideoTokenizer

# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class KLConfig:
class KLConfig:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# each step is greater than boundaries[-1], so weight=values[-1]
    # each step is greater than boundaries[-1], so weight=values[-1]
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：boundaries: list[int] = [0]
    boundaries: list[int] = [0]
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：values: list[float] = [1e-6]
    values: list[float] = [1e-6]


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class PerceptualConfig:
class PerceptualConfig:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：lpips_boundaries: list[int] = [500000]
    lpips_boundaries: list[int] = [500000]
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：lpips_values: list[float] = [0.1, 0.073]
    lpips_values: list[float] = [0.1, 0.073]
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Layer weights for linearly combining the multi-layer vgg-based losses.
    # Layer weights for linearly combining the multi-layer vgg-based losses.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：layer_weights: list[float] = [1.0 / 2.6, 1.0 / 4.8, 1.0 / 3.7, 1.0 / 5.6, 10.0 / 1.5]
    layer_weights: list[float] = [1.0 / 2.6, 1.0 / 4.8, 1.0 / 3.7, 1.0 / 5.6, 10.0 / 1.5]
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Gram loss, whether to turn on, and what weights to use.
    # Gram loss, whether to turn on, and what weights to use.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：gram_enabled: bool = True
    gram_enabled: bool = True
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：gram_boundaries: list[int] = [500000]
    gram_boundaries: list[int] = [500000]
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：gram_values: list[float] = [0.0, 0.062]
    gram_values: list[float] = [0.0, 0.062]
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Corr loss, whether to turn on, and what weights to use.
    # Corr loss, whether to turn on, and what weights to use.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：corr_enabled: bool = False
    corr_enabled: bool = False
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：corr_boundaries: list[int] = [0]
    corr_boundaries: list[int] = [0]
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：corr_values: list[float] = [0.0]
    corr_values: list[float] = [0.0]
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# In the example training memory usage dropped from 64.03 GiB to 60.54 GiB
    # In the example training memory usage dropped from 64.03 GiB to 60.54 GiB
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# with checkpointing enabled for this loss for about 3.2% slowdown.
    # with checkpointing enabled for this loss for about 3.2% slowdown.
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# With checkpointing this and PerceptualLoss memory usage dropped
    # With checkpointing this and PerceptualLoss memory usage dropped
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# from 64.03 GiB to 52.94 GiB for about 18% slowdown
    # from 64.03 GiB to 52.94 GiB for about 18% slowdown
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# more details in MR:949
    # more details in MR:949
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：checkpoint_activations: bool = False
    checkpoint_activations: bool = False

# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Metric:
class Metric:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# The combined loss function, and its reduction mode.
    # The combined loss function, and its reduction mode.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：PSNR: LazyDict = L(PSNRMetric)()
    PSNR: LazyDict = L(PSNRMetric)()
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：SSIM: LazyDict = L(SSIMMetric)()
    SSIM: LazyDict = L(SSIMMetric)()


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class DiscreteTokenizerMetric:
class DiscreteTokenizerMetric:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# with code usage (perplexity PPL), for discrete tokenizers only
    # with code usage (perplexity PPL), for discrete tokenizers only
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：PSNR: LazyDict = L(PSNRMetric)()
    PSNR: LazyDict = L(PSNRMetric)()
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：SSIM: LazyDict = L(SSIMMetric)()
    SSIM: LazyDict = L(SSIMMetric)()
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CodeUsage: LazyDict = L(CodeUsageMetric)(codebook_size=64000)
    CodeUsage: LazyDict = L(CodeUsageMetric)(codebook_size=64000)


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ColorConfig:
class ColorConfig:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Color (RGB) basic loss and its weight schedule.
    # Color (RGB) basic loss and its weight schedule.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：norm: str = "L1"
    norm: str = "L1"
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：boundaries: list[int] = [0]
    boundaries: list[int] = [0]
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：values: list[float] = [1.0]
    values: list[float] = [1.0]


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class FlowConfig:
class FlowConfig:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Flow loss and its weight schedule.
    # Flow loss and its weight schedule.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：boundaries: list[int] = [250000]
    boundaries: list[int] = [250000]
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：values: list[float] = [0.0, 0.01]
    values: list[float] = [0.0, 0.01]
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scale: int = 2
    scale: int = 2
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Flow loss depends on RAFT, as such it requires a specific dtype.
    # Flow loss depends on RAFT, as such it requires a specific dtype.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dtype: str = "bfloat16"
    dtype: str = "bfloat16"
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# In the example training memory usage dropped from 28GB to 23GB
    # In the example training memory usage dropped from 28GB to 23GB
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# with checkpointing enabled for this loss
    # with checkpointing enabled for this loss
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# With checkpointing this and PerceptualLoss memory usage dropped
    # With checkpointing this and PerceptualLoss memory usage dropped
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# from 64.03 GiB to 52.94 GiB for about 18% slowdown
    # from 64.03 GiB to 52.94 GiB for about 18% slowdown
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# more details in MR:949
    # more details in MR:949
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：checkpoint_activations: bool = False
    checkpoint_activations: bool = False
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：enabled: bool = False
    enabled: bool = False
    

# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class VideoConsistencyConfig:
class VideoConsistencyConfig:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Add consistency loss between overlapped video frames
    # Add consistency loss between overlapped video frames
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：boundaries: list[int] = [250000]
    boundaries: list[int] = [250000]
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：values: list[float] = [0.0, 0.01]
    values: list[float] = [0.0, 0.01]
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：enabled: bool = False
    enabled: bool = False
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_frames: int = 9
    num_frames: int = 9
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：step: int = 1
    step: int = 1


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class VideoLoss:
class VideoLoss:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# The combined loss function, and its reduction mode.
    # The combined loss function, and its reduction mode.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：color: LazyDict = L(ColorLoss)(config=ColorConfig())
    color: LazyDict = L(ColorLoss)(config=ColorConfig())
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：kl: LazyDict = L(KLLoss)(config=KLConfig())
    kl: LazyDict = L(KLLoss)(config=KLConfig())
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：perceptual: LazyDict = L(PerceptualLoss)(config=PerceptualConfig())
    perceptual: LazyDict = L(PerceptualLoss)(config=PerceptualConfig())
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：flow: LazyDict = L(FlowLoss)(config=FlowConfig())
    flow: LazyDict = L(FlowLoss)(config=FlowConfig())
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video_consistency: LazyDict = L(VideoConsistencyLoss)(config=VideoConsistencyConfig())
    video_consistency: LazyDict = L(VideoConsistencyLoss)(config=VideoConsistencyConfig())
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：reduce: str = ReduceMode.MEAN.value # model.config.loss.config.reduce={'MEAN', 'SUM', 'SUM_PE...
    reduce: str = ReduceMode.MEAN.value  # model.config.loss.config.reduce={'MEAN', 'SUM', 'SUM_PER_FRAME'}


# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：VideoLossConfig: LazyDict = L(TokenizerLoss)(config=VideoLoss())
VideoLossConfig: LazyDict = L(TokenizerLoss)(config=VideoLoss())
# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：MetricConfig: LazyDict = L(TokenizerMetric)(config=Metric())
MetricConfig: LazyDict = L(TokenizerMetric)(config=Metric())

# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@make_freezable
@make_freezable
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class LatentDynamicModelConfig:
class LatentDynamicModelConfig:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：network: LazyDict
    network: LazyDict
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ldm_path: str
    ldm_path: str
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：loss: LazyDict
    loss: LazyDict
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：metric: LazyDict
    metric: LazyDict

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：LDM_DEFAULT = LatentDynamicModelConfig(
LDM_DEFAULT = LatentDynamicModelConfig(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：network=L(CausalDiscreteVideoLatentDynamicTokenizer)(
    network=L(CausalDiscreteVideoLatentDynamicTokenizer)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn_resolutions=[32],
        attn_resolutions=[32],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：channels=128,
        channels=128,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：channels_mult=[2, 4, 4],
        channels_mult=[2, 4, 4],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=0.0,
        dropout=0.0,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=3,
        in_channels=3,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_res_blocks=2,
        num_res_blocks=2,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=3,
        out_channels=3,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resolution=1024,
        resolution=1024,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：patch_size=4,
        patch_size=4,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：patch_method="haar",
        patch_method="haar",
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# The encoder output channels just before quantization is changed to 256
        # The encoder output channels just before quantization is changed to 256
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# from 16 (old versions). It aligns with the DI that uses 256 channels,
        # from 16 (old versions). It aligns with the DI that uses 256 channels,
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# making initialization from image tokenizers easier.
        # making initialization from image tokenizers easier.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_channels=256,
        z_channels=256,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_factor=1,
        z_factor=1,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=1,
        num_groups=1,
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Most of the CV and DV tokenizers trained before September 1, 2024,
        # Most of the CV and DV tokenizers trained before September 1, 2024,
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# used temporal upsampling that was not perfectly mirrored with the
        # used temporal upsampling that was not perfectly mirrored with the
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# # encoder's temporal downsampling. Moving forward, new CV/DV tokenizers
        # # encoder's temporal downsampling. Moving forward, new CV/DV tokenizers
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# will use legacy_mode=False, meaning they will adopt mirrored upsampling.
        # will use legacy_mode=False, meaning they will adopt mirrored upsampling.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：legacy_mode=False,
        legacy_mode=False,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：spatial_compression=16,
        spatial_compression=16,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_compression=4,
        temporal_compression=4,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quantizer=DiscreteQuantizer.FSQ.name,
        quantizer=DiscreteQuantizer.FSQ.name,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：embedding_dim=1,
        embedding_dim=1,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：levels=[8],
        levels=[8],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：persistent_quantizer=False,
        persistent_quantizer=False,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：encoder=Encoder3DType.LDM.name,
        encoder=Encoder3DType.LDM.name,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：decoder=Decoder3DType.LDM.name,
        decoder=Decoder3DType.LDM.name,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="CausalDiscreteFactorizedVideoLatentDynamicTokenizer",
        name="CausalDiscreteFactorizedVideoLatentDynamicTokenizer",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：connector_type='conv',
        connector_type='conv',
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：act_embedding_num=4
        act_embedding_num=4
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ldm_path="checkpoints/Cosmos-Tokenize1-DV8x16x16-720p/model_1level.pt",
        ldm_path="checkpoints/Cosmos-Tokenize1-DV8x16x16-720p/model_1level.pt",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：loss=VideoLossConfig,
        loss=VideoLossConfig,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：metric=MetricConfig
        metric=MetricConfig

# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)


# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：LDM_DEFAULT = LatentDynamicModelConfig(
LDM_DEFAULT = LatentDynamicModelConfig(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：network=L(CausalDiscreteVideoLatentDynamicTokenizer)(
    network=L(CausalDiscreteVideoLatentDynamicTokenizer)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn_resolutions=[32],
        attn_resolutions=[32],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：channels=128,
        channels=128,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：channels_mult=[2, 4, 4],
        channels_mult=[2, 4, 4],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=0.0,
        dropout=0.0,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=3,
        in_channels=3,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_res_blocks=2,
        num_res_blocks=2,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=3,
        out_channels=3,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resolution=1024,
        resolution=1024,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：patch_size=4,
        patch_size=4,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：patch_method="haar",
        patch_method="haar",
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# The encoder output channels just before quantization is changed to 256
        # The encoder output channels just before quantization is changed to 256
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# from 16 (old versions). It aligns with the DI that uses 256 channels,
        # from 16 (old versions). It aligns with the DI that uses 256 channels,
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# making initialization from image tokenizers easier.
        # making initialization from image tokenizers easier.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_channels=256,
        z_channels=256,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_factor=1,
        z_factor=1,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=1,
        num_groups=1,
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Most of the CV and DV tokenizers trained before September 1, 2024,
        # Most of the CV and DV tokenizers trained before September 1, 2024,
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# used temporal upsampling that was not perfectly mirrored with the
        # used temporal upsampling that was not perfectly mirrored with the
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# # encoder's temporal downsampling. Moving forward, new CV/DV tokenizers
        # # encoder's temporal downsampling. Moving forward, new CV/DV tokenizers
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# will use legacy_mode=False, meaning they will adopt mirrored upsampling.
        # will use legacy_mode=False, meaning they will adopt mirrored upsampling.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：legacy_mode=False,
        legacy_mode=False,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：spatial_compression=16,
        spatial_compression=16,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_compression=4,
        temporal_compression=4,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quantizer=DiscreteQuantizer.FSQ.name,
        quantizer=DiscreteQuantizer.FSQ.name,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：embedding_dim=1,
        embedding_dim=1,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：levels=[8],
        levels=[8],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：persistent_quantizer=False,
        persistent_quantizer=False,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：encoder=Encoder3DType.LDM.name,
        encoder=Encoder3DType.LDM.name,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：decoder=Decoder3DType.LDM.name,
        decoder=Decoder3DType.LDM.name,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="CausalDiscreteFactorizedVideoLatentDynamicTokenizer",
        name="CausalDiscreteFactorizedVideoLatentDynamicTokenizer",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：connector_type='conv',
        connector_type='conv',
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：act_embedding_num=4,
        act_embedding_num=4,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：qformer_type='QFormerMF',
        qformer_type='QFormerMF',
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ldm_path="checkpoints/Cosmos-Tokenize1-DV8x16x16-720p/model_1level.pt",
        ldm_path="checkpoints/Cosmos-Tokenize1-DV8x16x16-720p/model_1level.pt",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：loss=VideoLossConfig,
        loss=VideoLossConfig,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：metric=MetricConfig
        metric=MetricConfig

# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：COSMOS_TOKENIZER = LatentDynamicModelConfig(
COSMOS_TOKENIZER = LatentDynamicModelConfig(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：network=L(CausalDiscreteVideoTokenizer)(
    network=L(CausalDiscreteVideoTokenizer)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn_resolutions=[32],
        attn_resolutions=[32],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：channels=128,
        channels=128,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：channels_mult=[2, 4, 4],
        channels_mult=[2, 4, 4],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=0.0,
        dropout=0.0,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=3,
        in_channels=3,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_res_blocks=2,
        num_res_blocks=2,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=3,
        out_channels=3,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resolution=1024,
        resolution=1024,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：patch_size=4,
        patch_size=4,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：patch_method="haar",
        patch_method="haar",
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# The encoder output channels just before quantization is changed to 256
        # The encoder output channels just before quantization is changed to 256
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# from 16 (old versions). It aligns with the DI that uses 256 channels,
        # from 16 (old versions). It aligns with the DI that uses 256 channels,
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# making initialization from image tokenizers easier.
        # making initialization from image tokenizers easier.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_channels=256,
        z_channels=256,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_factor=1,
        z_factor=1,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=1,
        num_groups=1,
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Most of the CV and DV tokenizers trained before September 1, 2024,
        # Most of the CV and DV tokenizers trained before September 1, 2024,
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# used temporal upsampling that was not perfectly mirrored with the
        # used temporal upsampling that was not perfectly mirrored with the
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# # encoder's temporal downsampling. Moving forward, new CV/DV tokenizers
        # # encoder's temporal downsampling. Moving forward, new CV/DV tokenizers
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# will use legacy_mode=False, meaning they will adopt mirrored upsampling.
        # will use legacy_mode=False, meaning they will adopt mirrored upsampling.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：legacy_mode=False,
        legacy_mode=False,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：spatial_compression=16,
        spatial_compression=16,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_compression=8,
        temporal_compression=8,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quantizer=DiscreteQuantizer.FSQ.name,
        quantizer=DiscreteQuantizer.FSQ.name,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：embedding_dim=6,
        embedding_dim=6,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：levels=[8, 8, 8, 5, 5, 5],
        levels=[8, 8, 8, 5, 5, 5],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：persistent_quantizer=False,
        persistent_quantizer=False,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：encoder=Encoder3DType.FACTORIZED.name,
        encoder=Encoder3DType.FACTORIZED.name,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：decoder=Decoder3DType.FACTORIZED.name,
        decoder=Decoder3DType.FACTORIZED.name,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="CausalDiscreteFactorizedVideoTokenizer",
        name="CausalDiscreteFactorizedVideoTokenizer",
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ldm_path="checkpoints/Cosmos-Tokenize1-DV8x16x16-720p/model.pt",
        ldm_path="checkpoints/Cosmos-Tokenize1-DV8x16x16-720p/model.pt",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：loss=VideoLossConfig,
        loss=VideoLossConfig,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：metric=MetricConfig
        metric=MetricConfig
   
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)
