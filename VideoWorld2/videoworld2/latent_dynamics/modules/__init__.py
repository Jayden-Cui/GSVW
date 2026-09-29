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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from enum import Enum
from enum import Enum

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.latent_dynamics.modules.distributions import GaussianDistribution, IdentityD...
from videoworld2.latent_dynamics.modules.distributions import GaussianDistribution, IdentityDistribution
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# from videoworld2.latent_dynamics.modules.layers2d import Decoder, Encoder
# from videoworld2.latent_dynamics.modules.layers2d import Decoder, Encoder
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.latent_dynamics.modules.layers3d import DecoderBase, DecoderFactorized, Enco...
from videoworld2.latent_dynamics.modules.layers3d import DecoderBase, DecoderFactorized, EncoderBase, EncoderFactorized, LDMDecoderFactorized, LDMEncoderFactorizedV2,  LDMEncoderFactorized, LDMDecoderFactorizedV2, LDMDecoderFactorizedV3
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.latent_dynamics.modules.quantizers import FSQuantizer, LFQuantizer, Residual...
from videoworld2.latent_dynamics.modules.quantizers import FSQuantizer, LFQuantizer, ResidualFSQuantizer, VectorQuantizer

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# from videoworld2.latent_dynamics.modules.qformer_ldm import (
# from videoworld2.latent_dynamics.modules.qformer_ldm import (
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# QFormerMF,
#     QFormerMF,
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# QFormerMFSep,
#     QFormerMFSep,
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# QFormerMFSingleQ,
#     QFormerMFSingleQ,
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# # QFormerAdjacentFSingleQ,
#     # QFormerAdjacentFSingleQ,
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# PositionEmbeddingRandom
#     PositionEmbeddingRandom
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# )
# )

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# class EncoderType(Enum):
# class EncoderType(Enum):
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Default = Encoder
#     Default = Encoder


# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# class DecoderType(Enum):
# class DecoderType(Enum):
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Default = Decoder
#     Default = Decoder


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Encoder3DType(Enum):
class Encoder3DType(Enum):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：BASE = EncoderBase
    BASE = EncoderBase
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：FACTORIZED = EncoderFactorized
    FACTORIZED = EncoderFactorized
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：LDM = LDMEncoderFactorized
    LDM = LDMEncoderFactorized
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：LDM_V2 = LDMEncoderFactorizedV2
    LDM_V2 = LDMEncoderFactorizedV2


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Decoder3DType(Enum):
class Decoder3DType(Enum):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：BASE = DecoderBase
    BASE = DecoderBase
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：FACTORIZED = DecoderFactorized
    FACTORIZED = DecoderFactorized
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：LDM = LDMDecoderFactorized
    LDM = LDMDecoderFactorized
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：LDM_V2 = LDMDecoderFactorizedV2
    LDM_V2 = LDMDecoderFactorizedV2
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：LDM_V3 = LDMDecoderFactorizedV3
    LDM_V3 = LDMDecoderFactorizedV3
    


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ContinuousFormulation(Enum):
class ContinuousFormulation(Enum):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：VAE = GaussianDistribution
    VAE = GaussianDistribution
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：AE = IdentityDistribution
    AE = IdentityDistribution


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class DiscreteQuantizer(Enum):
class DiscreteQuantizer(Enum):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：VQ = VectorQuantizer
    VQ = VectorQuantizer
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：LFQ = LFQuantizer
    LFQ = LFQuantizer
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：FSQ = FSQuantizer
    FSQ = FSQuantizer
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：RESFSQ = ResidualFSQuantizer
    RESFSQ = ResidualFSQuantizer
