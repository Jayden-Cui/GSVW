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
# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""The network definition for discrete video tokenizer with VQ, LFQ, FSQ or ResidualFSQ. """
"""The network definition for discrete video tokenizer with VQ, LFQ, FSQ or ResidualFSQ. """
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from collections import OrderedDict, namedtuple
from collections import OrderedDict, namedtuple

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from loguru import logger as logging
from loguru import logger as logging
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch import nn
from torch import nn

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.latent_dynamics.modules import Decoder3DType, DiscreteQuantizer, Encoder3DType
from videoworld2.latent_dynamics.modules import Decoder3DType, DiscreteQuantizer, Encoder3DType
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.latent_dynamics.modules.layers3d import CausalConv3d
from videoworld2.latent_dynamics.modules.layers3d import CausalConv3d
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.latent_dynamics.modules.quantizers import InvQuantizerJit
from videoworld2.latent_dynamics.modules.quantizers import InvQuantizerJit

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：NetworkEval = namedtuple("NetworkEval", ["reconstructions", "quant_loss", "quant_info"])
NetworkEval = namedtuple("NetworkEval", ["reconstructions", "quant_loss", "quant_info"])


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class CausalDiscreteVideoTokenizer(nn.Module):
class CausalDiscreteVideoTokenizer(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, z_channels: int, z_factor: int, embedding_dim: int, **kwargs) -> None:
    def __init__(self, z_channels: int, z_factor: int, embedding_dim: int, **kwargs) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.name = kwargs.get("name", "CausalDiscreteVideoTokenizer")
        self.name = kwargs.get("name", "CausalDiscreteVideoTokenizer")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.embedding_dim = embedding_dim
        self.embedding_dim = embedding_dim

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：encoder_name = kwargs.get("encoder", Encoder3DType.BASE.name)
        encoder_name = kwargs.get("encoder", Encoder3DType.BASE.name)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.encoder = Encoder3DType[encoder_name].value(z_channels=z_factor * z_channels, **kwargs)
        self.encoder = Encoder3DType[encoder_name].value(z_channels=z_factor * z_channels, **kwargs)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：decoder_name = kwargs.get("decoder", Decoder3DType.BASE.name)
        decoder_name = kwargs.get("decoder", Decoder3DType.BASE.name)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.decoder = Decoder3DType[decoder_name].value(z_channels=z_channels, **kwargs)
        self.decoder = Decoder3DType[decoder_name].value(z_channels=z_channels, **kwargs)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.quant_conv = CausalConv3d(z_factor * z_channels, embedding_dim, kernel_size=1, padding=0)
        self.quant_conv = CausalConv3d(z_factor * z_channels, embedding_dim, kernel_size=1, padding=0)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.post_quant_conv = CausalConv3d(embedding_dim, z_channels, kernel_size=1, padding=0)
        self.post_quant_conv = CausalConv3d(embedding_dim, z_channels, kernel_size=1, padding=0)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quantizer_name = kwargs.get("quantizer", DiscreteQuantizer.RESFSQ.name)
        quantizer_name = kwargs.get("quantizer", DiscreteQuantizer.RESFSQ.name)
        # 中文说明：根据条件选择执行分支；代码：if quantizer_name == DiscreteQuantizer.VQ.name:
        if quantizer_name == DiscreteQuantizer.VQ.name:
            # 中文说明：检查运行时假设是否成立；代码：assert "num_embeddings" in kwargs, f"`num_embeddings` must be provided for {quantizer_name}."
            assert "num_embeddings" in kwargs, f"`num_embeddings` must be provided for {quantizer_name}."
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：kwargs.update(dict(embedding_dim=embedding_dim))
            kwargs.update(dict(embedding_dim=embedding_dim))
        # 中文说明：根据条件选择执行分支；代码：elif quantizer_name == DiscreteQuantizer.LFQ.name:
        elif quantizer_name == DiscreteQuantizer.LFQ.name:
            # 中文说明：检查运行时假设是否成立；代码：assert "codebook_size" in kwargs, f"`codebook_size` must be provided for {quantizer_name}."
            assert "codebook_size" in kwargs, f"`codebook_size` must be provided for {quantizer_name}."
            # 中文说明：检查运行时假设是否成立；代码：assert "codebook_dim" in kwargs, f"`codebook_dim` must be provided for {quantizer_name}."
            assert "codebook_dim" in kwargs, f"`codebook_dim` must be provided for {quantizer_name}."
        # 中文说明：根据条件选择执行分支；代码：elif quantizer_name == DiscreteQuantizer.FSQ.name:
        elif quantizer_name == DiscreteQuantizer.FSQ.name:
            # 中文说明：检查运行时假设是否成立；代码：assert "levels" in kwargs, f"`levels` must be provided for {quantizer_name}."
            assert "levels" in kwargs, f"`levels` must be provided for {quantizer_name}."
        # 中文说明：根据条件选择执行分支；代码：elif quantizer_name == DiscreteQuantizer.RESFSQ.name:
        elif quantizer_name == DiscreteQuantizer.RESFSQ.name:
            # 中文说明：检查运行时假设是否成立；代码：assert "levels" in kwargs, f"`levels` must be provided for {quantizer_name}."
            assert "levels" in kwargs, f"`levels` must be provided for {quantizer_name}."
            # 中文说明：检查运行时假设是否成立；代码：assert "num_quantizers" in kwargs, f"`num_quantizers` must be provided for {quantizer_name}."
            assert "num_quantizers" in kwargs, f"`num_quantizers` must be provided for {quantizer_name}."
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.quantizer = DiscreteQuantizer[quantizer_name].value(**kwargs)
        self.quantizer = DiscreteQuantizer[quantizer_name].value(**kwargs)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：logging.info(f"{self.name} based on {quantizer_name}-VAE, with {kwargs}.")
        logging.info(f"{self.name} based on {quantizer_name}-VAE, with {kwargs}.")

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_parameters = sum(param.numel() for param in self.parameters())
        num_parameters = sum(param.numel() for param in self.parameters())
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：logging.info(f"model={self.name}, num_parameters={num_parameters:,}")
        logging.info(f"model={self.name}, num_parameters={num_parameters:,}")
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：logging.info(f"z_channels={z_channels}, embedding_dim={self.embedding_dim}.")
        logging.info(f"z_channels={z_channels}, embedding_dim={self.embedding_dim}.")

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def to(self, *args, **kwargs):
    def to(self, *args, **kwargs):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：setattr(self.quantizer, "dtype", kwargs.get("dtype", torch.bfloat16))
        setattr(self.quantizer, "dtype", kwargs.get("dtype", torch.bfloat16))
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return super(CausalDiscreteVideoTokenizer, self).to(*args, **kwargs)
        return super(CausalDiscreteVideoTokenizer, self).to(*args, **kwargs)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def encoder_jit(self):
    def encoder_jit(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return nn.Sequential(
        return nn.Sequential(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：OrderedDict(
            OrderedDict(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：[
                [
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：("encoder", self.encoder),
                    ("encoder", self.encoder),
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：("quant_conv", self.quant_conv),
                    ("quant_conv", self.quant_conv),
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：("quantizer", self.quantizer),
                    ("quantizer", self.quantizer),
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
                ]
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def decoder_jit(self):
    def decoder_jit(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return nn.Sequential(
        return nn.Sequential(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：OrderedDict(
            OrderedDict(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：[
                [
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：("inv_quant", InvQuantizerJit(self.quantizer)),
                    ("inv_quant", InvQuantizerJit(self.quantizer)),
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：("post_quant_conv", self.post_quant_conv),
                    ("post_quant_conv", self.post_quant_conv),
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：("decoder", self.decoder),
                    ("decoder", self.decoder),
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
                ]
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def last_decoder_layer(self):
    def last_decoder_layer(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.decoder.conv_out
        return self.decoder.conv_out

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def encode(self, x):
    def encode(self, x):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.encoder(x)
        h = self.encoder(x)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.quant_conv(h)
        h = self.quant_conv(h)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.quantizer(h)
        return self.quantizer(h)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def decode(self, quant):
    def decode(self, quant):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant = self.post_quant_conv(quant)
        quant = self.post_quant_conv(quant)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.decoder(quant)
        return self.decoder(quant)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def decode_code(self, code_b):
    def decode_code(self, code_b):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant_b = self.quantizer.indices_to_codes(code_b)
        quant_b = self.quantizer.indices_to_codes(code_b)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant_b = self.post_quant_conv(quant_b)
        quant_b = self.post_quant_conv(quant_b)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.decoder(quant_b)
        return self.decoder(quant_b)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, input):
    def forward(self, input):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：quant_info, quant_codes, quant_loss = self.encode(input)
        quant_info, quant_codes, quant_loss = self.encode(input)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：reconstructions = self.decode(quant_codes)
        reconstructions = self.decode(quant_codes)
        # 中文说明：根据条件选择执行分支；代码：if self.training:
        if self.training:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return dict(
            return dict(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：reconstructions=reconstructions,
                reconstructions=reconstructions,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant_loss=quant_loss,
                quant_loss=quant_loss,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant_info=quant_info,
                quant_info=quant_info,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return NetworkEval(
        return NetworkEval(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：reconstructions=reconstructions,
            reconstructions=reconstructions,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant_loss=quant_loss,
            quant_loss=quant_loss,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant_info=quant_info,
            quant_info=quant_info,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )