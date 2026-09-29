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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from transformers import LlamaConfig, LlamaModel
from transformers import LlamaConfig, LlamaModel
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from loguru import logger as logging
from loguru import logger as logging
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch import nn
from torch import nn
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import copy
import copy
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.latent_dynamics.modules import Decoder3DType, DiscreteQuantizer, Encoder3DType
from videoworld2.latent_dynamics.modules import Decoder3DType, DiscreteQuantizer, Encoder3DType
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.latent_dynamics.modules.layers3d import CausalConv3d, LDMDecoderFactorized, ...
from videoworld2.latent_dynamics.modules.layers3d import CausalConv3d, LDMDecoderFactorized, LDMEncoderFactorized, CausalResnetBlockFactorized3d
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.latent_dynamics.modules.quantizers import InvQuantizerJit
from videoworld2.latent_dynamics.modules.quantizers import InvQuantizerJit


# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：NetworkEval = namedtuple("NetworkEval", ["quant_info", "quant_loss", "quant_codes", "ldm_quer...
NetworkEval = namedtuple("NetworkEval", ["quant_info", "quant_loss", "quant_codes", "ldm_query", "reconstructions", "mid_h"])

# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class CustomEncoderJIT(nn.Module):
class CustomEncoderJIT(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, original_model):
    def __init__(self, original_model):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.encoder = original_model.encoder
        self.encoder = original_model.encoder
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.quant_conv = original_model.quant_conv
        self.quant_conv = original_model.quant_conv
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.quantizer = original_model.quantizer
        self.quantizer = original_model.quantizer
    
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x):
    def forward(self, x):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：h, query = self.encoder(x)
        h, query = self.encoder(x)
        
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：query = self.quant_conv(query) #B, 16, T-1, 1, 1
        query = self.quant_conv(query) #B, 16, T-1, 1, 1
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant_query = self.quantizer(query)
        quant_query = self.quantizer(query)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：quant_info, quant_codes, quant_loss = quant_query
        quant_info, quant_codes, quant_loss = quant_query

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return h, quant_info, (quant_codes, quant_loss), query
        return h, quant_info, (quant_codes, quant_loss), query

# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class CustomDecoderJIT(nn.Module):
class CustomDecoderJIT(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, original_model):
    def __init__(self, original_model):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.inv_quant = InvQuantizerJit(original_model.quantizer)
        self.inv_quant = InvQuantizerJit(original_model.quantizer)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.post_quant_conv = original_model.post_quant_conv
        self.post_quant_conv = original_model.post_quant_conv
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.decoder = original_model.decoder
        self.decoder = original_model.decoder
    
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, encoded_video, code_b):
    def forward(self, encoded_video, code_b):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant_b = self.inv_quant(code_b)
        quant_b = self.inv_quant(code_b)
        
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant_b = self.post_quant_conv(quant_b) #B, 16, T-1, 1, 1
        quant_b = self.post_quant_conv(quant_b) #B, 16, T-1, 1, 1
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：reconstructions = self.decoder(encoded_video, quant_b)
        reconstructions = self.decoder(encoded_video, quant_b)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return reconstructions
        return reconstructions

# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class LlamaConnector(nn.Module):
class LlamaConnector(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, z_channels, out_channels) -> None:
    def __init__(self, z_channels, out_channels) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.proj_in = CausalResnetBlockFactorized3d(
        self.proj_in = CausalResnetBlockFactorized3d(
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=z_channels,
                    in_channels=z_channels,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=out_channels,
                    out_channels=out_channels,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=0,
                    dropout=0,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=1,
                    num_groups=1,
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config = LlamaConfig(
        config = LlamaConfig(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hidden_size=out_channels,
                hidden_size=out_channels,         
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：intermediate_size=out_channels*2,
                intermediate_size=out_channels*2,   
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_hidden_layers=12,
                num_hidden_layers=12,    
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_attention_heads=8,
                num_attention_heads=8,    
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_position_embeddings=1024,
                max_position_embeddings=1024, 
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rms_norm_eps=1e-6,
                rms_norm_eps=1e-6,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_cache=True,
                use_cache=True,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.llama_model = LlamaModel(config=config)
        self.llama_model = LlamaModel(config=config)
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x):
    def forward(self, x):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.proj_in(x)
        x = self.proj_in(x)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = x.flatten(2).permute(0, 2, 1)
        x = x.flatten(2).permute(0, 2, 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：outputs = self.llama_model(inputs_embeds=x)
        outputs = self.llama_model(inputs_embeds=x)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = outputs.last_hidden_state
        x = outputs.last_hidden_state
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x
        return x
    

# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class CausalDiscreteVideoLatentDynamicTokenizer(nn.Module):
class CausalDiscreteVideoLatentDynamicTokenizer(nn.Module):
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
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self.encoder = LDMEncoderFactorized(
        # self.encoder = LDMEncoderFactorized(
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# z_channels=z_factor * z_channels, act_embedding_num=act_embedding_num, **kwargs
        #     z_channels=z_factor * z_channels, act_embedding_num=act_embedding_num, **kwargs
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# )
        # )
        
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：decoder_name = kwargs.get("decoder", Decoder3DType.BASE.name)
        decoder_name = kwargs.get("decoder", Decoder3DType.BASE.name)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.decoder = Decoder3DType[decoder_name].value(z_channels=z_channels, **kwargs)
        self.decoder = Decoder3DType[decoder_name].value(z_channels=z_channels, **kwargs)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self.decoder = LDMDecoderFactorized(
        # self.decoder = LDMDecoderFactorized(
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# z_channels=z_channels, **kwargs
        #     z_channels=z_channels, **kwargs
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# )
        # )


        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.quant_conv = CausalConv3d(z_factor * z_channels, embedding_dim, kernel_size=1, padding=0)
        self.quant_conv = CausalConv3d(z_factor * z_channels, embedding_dim, kernel_size=1, padding=0)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.post_quant_conv = CausalConv3d(embedding_dim, z_channels, kernel_size=1, padding=0)
        self.post_quant_conv = CausalConv3d(embedding_dim, z_channels, kernel_size=1, padding=0)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self.quant_to_dit_dim = CausalConv3d(z_channels, 1024, kernel_size=1, padding=0)
        # self.quant_to_dit_dim = CausalConv3d(z_channels, 1024, kernel_size=1, padding=0)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：connector_type = kwargs.get('connector_type', 'conv')
        connector_type = kwargs.get('connector_type', 'conv')
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.connector_type = connector_type
        self.connector_type = connector_type
        # 中文说明：根据条件选择执行分支；代码：if connector_type == 'llama':
        if connector_type == 'llama':
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.quant_to_dit_dim = LlamaConnector(z_channels, out_channels=1024)
            self.quant_to_dit_dim = LlamaConnector(z_channels, out_channels=1024)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：total_params = sum(p.numel() for p in self.quant_to_dit_dim.parameters())
            total_params = sum(p.numel() for p in self.quant_to_dit_dim.parameters())
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：logging.info(f"Connector Typ: Llama Transformers. Total parameters: {total_params / 1e9:.2f}B")
            logging.info(f"Connector Typ: Llama Transformers. Total parameters: {total_params / 1e9:.2f}B")
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.quant_to_dit_dim = CausalResnetBlockFactorized3d(
            self.quant_to_dit_dim = CausalResnetBlockFactorized3d(
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=z_channels,
                    in_channels=z_channels,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=1024,
                    out_channels=1024,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout=0,
                    dropout=0,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_groups=1,
                    num_groups=1,
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：total_params = sum(p.numel() for p in self.quant_to_dit_dim.parameters())
            total_params = sum(p.numel() for p in self.quant_to_dit_dim.parameters())
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：logging.info(f"Connector Typ: ConvBlock. Total parameters: {total_params / 1e9:.2f}B")
            logging.info(f"Connector Typ: ConvBlock. Total parameters: {total_params / 1e9:.2f}B")

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
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self.loss_scale = 1.0
        # self.loss_scale = 1.0
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self.loss_reduce = 'mean'
        # self.loss_reduce = 'mean'

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def to(self, *args, **kwargs):
    def to(self, *args, **kwargs):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：setattr(self.quantizer, "dtype", kwargs.get("dtype", torch.bfloat16))
        setattr(self.quantizer, "dtype", kwargs.get("dtype", torch.bfloat16))
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return super(CausalDiscreteVideoLatentDynamicTokenizer, self).to(torch.bfloat16)
        return super(CausalDiscreteVideoLatentDynamicTokenizer, self).to(torch.bfloat16)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def encoder_jit(self):
    def encoder_jit(self):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# return nn.Sequential(
        # return nn.Sequential(
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# OrderedDict(
        #     OrderedDict(
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# [
        #         [
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# ("encoder", self.encoder),
        #             ("encoder", self.encoder),
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# ("quant_conv", self.quant_conv),
        #             ("quant_conv", self.quant_conv),
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# ("quantizer", self.quantizer),
        #             ("quantizer", self.quantizer),
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# ]
        #         ]
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# )
        #     )
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# )
        # )
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return CustomEncoderJIT(self)
        return CustomEncoderJIT(self)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def decoder_jit(self):
    def decoder_jit(self):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# return nn.Sequential(
        # return nn.Sequential(
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# OrderedDict(
        #     OrderedDict(
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# [
        #         [
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# ("inv_quant", InvQuantizerJit(self.quantizer)),
        #             ("inv_quant", InvQuantizerJit(self.quantizer)),
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# ("post_quant_conv", self.post_quant_conv),
        #             ("post_quant_conv", self.post_quant_conv),
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# ("decoder", self.decoder),
        #             ("decoder", self.decoder),
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# ]
        #         ]
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# )
        #     )
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# )
        # )
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return CustomDecoderJIT(self)
        return CustomDecoderJIT(self)
    
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def last_decoder_layer(self):
    def last_decoder_layer(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.decoder.conv_out
        return self.decoder.conv_out

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def encode(self, x):
    def encode(self, x):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：h, query = self.encoder(x)
        h, query = self.encoder(x)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：query = self.quant_conv(query) #B, 16, T-1, 1, 1
        query = self.quant_conv(query) #B, 16, T-1, 1, 1
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant_query = self.quantizer(query)
        quant_query = self.quantizer(query)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：quant_info, quant_codes, quant_loss = quant_query
        quant_info, quant_codes, quant_loss = quant_query

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return h, quant_info, (quant_codes, quant_loss), query
        return h, quant_info, (quant_codes, quant_loss), query

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def decode(self, encoded_video, quant):
    def decode(self, encoded_video, quant):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant = self.post_quant_conv(quant)
        quant = self.post_quant_conv(quant)
        
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.decoder(encoded_video, quant)
        return self.decoder(encoded_video, quant)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def decode_code(self, encoded_video, code_b):
    def decode_code(self, encoded_video, code_b):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant_b = self.quantizer.indices_to_codes(code_b)
        quant_b = self.quantizer.indices_to_codes(code_b)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant_b = self.post_quant_conv(quant_b)
        quant_b = self.post_quant_conv(quant_b)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.decoder(encoded_video, quant_b)
        return self.decoder(encoded_video, quant_b)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, input, input_aug=None):
    def forward(self, input, input_aug=None):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：根据条件选择执行分支；代码：if input_aug is None:
        if input_aug is None:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：encoded_video, quant_info, (quant_codes, quant_loss), query = self.encode(input)
            encoded_video, quant_info, (quant_codes, quant_loss), query = self.encode(input)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：decode_output = self.decode(encoded_video, quant_codes) #quant_codes: torch.Size([1, 6, 4, 1,...
            decode_output = self.decode(encoded_video, quant_codes) #quant_codes: torch.Size([1, 6, 4, 1, 1]) 
            # 中文说明：根据条件选择执行分支；代码：if isinstance(decode_output, tuple):
            if isinstance(decode_output, tuple):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：reconstructions, mid_h = decode_output
                reconstructions, mid_h = decode_output
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：reconstructions = decode_output
                reconstructions = decode_output
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mid_h = None
                mid_h = None

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
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant_codes=quant_codes,
                    quant_codes=quant_codes,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mid_h=mid_h,
                    mid_h=mid_h,
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
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant_codes=quant_codes,
                quant_codes=quant_codes,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ldm_query=query,
                ldm_query=query,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mid_h=mid_h,
                mid_h=mid_h,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tensor_batch_aug_0 = input
            tensor_batch_aug_0 = input
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tensor_batch_aug_1 = input_aug
            tensor_batch_aug_1 = input_aug
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：encoded_video_aug_f0, _ = self.encoder(tensor_batch_aug_0)
            encoded_video_aug_f0, _ = self.encoder(tensor_batch_aug_0)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_, quant_info, (quant_codes, quant_loss), _ = self.encode(tensor_batch_aug_1)
            _, quant_info, (quant_codes, quant_loss), _ = self.encode(tensor_batch_aug_1)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：decode_output = self.decode(encoded_video_aug_f0, quant_codes) #quant_codes: torch.Size([1, 6...
            decode_output = self.decode(encoded_video_aug_f0, quant_codes) #quant_codes: torch.Size([1, 6, 4, 1, 1]) 
            # 中文说明：根据条件选择执行分支；代码：if isinstance(decode_output, tuple):
            if isinstance(decode_output, tuple):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：reconstructions, mid_h = decode_output
                reconstructions, mid_h = decode_output
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：reconstructions = decode_output
                reconstructions = decode_output
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mid_h = None
                mid_h = None

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_dict = dict(
            output_dict =  dict(
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# reconstructions_aug=reconstructions_aug,
                # reconstructions_aug=reconstructions_aug,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：reconstructions=reconstructions,
                reconstructions=reconstructions,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant_loss=quant_loss,
                quant_loss=quant_loss,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant_info=quant_info,
                quant_info=quant_info,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant_codes=quant_codes,
                quant_codes=quant_codes,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mid_h=mid_h,
                mid_h=mid_h,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return output_dict
            return output_dict
