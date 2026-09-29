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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import List, Optional, Tuple
from typing import List, Optional, Tuple
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from einops import rearrange
from einops import rearrange
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch import nn
from torch import nn
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.conditioner import DataType
from videoworld2.conditioner import DataType
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.models.video2world_dit import MinimalV1LVGDiT
from videoworld2.models.video2world_dit import MinimalV1LVGDiT
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.models.text2image_dit import PatchEmbed
from videoworld2.models.text2image_dit import PatchEmbed
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torchvision import transforms
from torchvision import transforms
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def zero_module(module):
def zero_module(module):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Zero out the parameters of a module and return it.
    """
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for p in module.parameters():
    for p in module.parameters():
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：p.detach().zero_()
        p.detach().zero_()
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return module
    return module

# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class CtrlEncoder(MinimalV1LVGDiT):
class CtrlEncoder(MinimalV1LVGDiT):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, *args, **kwargs):
    def __init__(self, *args, **kwargs):
        # 中文说明：检查运行时假设是否成立；代码：assert "in_channels" in kwargs, "in_channels must be provided"
        assert "in_channels" in kwargs, "in_channels must be provided"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hint_channels = kwargs.pop("hint_channels", 16)
        hint_channels = kwargs.pop("hint_channels", 16)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：control_weight = kwargs.pop("control_weight", 16)
        control_weight = kwargs.pop("control_weight", 16)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_control_blocks = kwargs.pop("num_control_blocks", None)
        num_control_blocks = kwargs.pop("num_control_blocks", None)
        # 中文说明：根据条件选择执行分支；代码：if num_control_blocks is not None:
        if num_control_blocks is not None:
            # 中文说明：检查运行时假设是否成立；代码：assert num_control_blocks > 0 and num_control_blocks <= kwargs["num_blocks"]
            assert num_control_blocks > 0 and num_control_blocks <= kwargs["num_blocks"]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["layer_mask"] = [False] * num_control_blocks + [True] * (kwargs["num_blocks"] - num_co...
            kwargs["layer_mask"] = [False] * num_control_blocks + [True] * (kwargs["num_blocks"] - num_control_blocks)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_blocks = self.num_blocks
        num_blocks = self.num_blocks
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_channels = self.model_channels
        model_channels = self.model_channels
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：layer_mask = kwargs.get("layer_mask", None)
        layer_mask = kwargs.get("layer_mask", None)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：layer_mask = [False] * num_blocks if layer_mask is None else layer_mask
        layer_mask = [False] * num_blocks if layer_mask is None else layer_mask
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.layer_mask = layer_mask
        self.layer_mask = layer_mask
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.hint_channels = hint_channels
        self.hint_channels = hint_channels
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.control_weight = control_weight
        self.control_weight = control_weight
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.build_hint_patch_embed()
        self.build_hint_patch_embed()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hint_nf = [16, 16, 32, 32, 96, 96, 256]
        hint_nf = [16, 16, 32, 32, 96, 96, 256]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：nonlinearity = nn.SiLU()
        nonlinearity = nn.SiLU()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_hint_block = [nn.Linear(model_channels, hint_nf[0]), nonlinearity]
        input_hint_block = [nn.Linear(model_channels, hint_nf[0]), nonlinearity]
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i in range(len(hint_nf) - 1):
        for i in range(len(hint_nf) - 1):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_hint_block += [nn.Linear(hint_nf[i], hint_nf[i + 1]), nonlinearity]
            input_hint_block += [nn.Linear(hint_nf[i], hint_nf[i + 1]), nonlinearity]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.input_hint_block = nn.Sequential(*input_hint_block)
        self.input_hint_block = nn.Sequential(*input_hint_block)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Initialize weights
        # Initialize weights
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.init_weights()
        self.init_weights()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.zero_blocks = nn.ModuleDict()
        self.zero_blocks = nn.ModuleDict()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for idx in range(num_blocks):
        for idx in range(num_blocks):
            # 中文说明：根据条件选择执行分支；代码：if layer_mask[idx]:
            if layer_mask[idx]:
                # 中文说明：执行循环控制或空操作；代码：continue
                continue
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.zero_blocks[f"block{idx}"] = zero_module(nn.Linear(model_channels, model_channels))
            self.zero_blocks[f"block{idx}"] = zero_module(nn.Linear(model_channels, model_channels))
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.input_hint_block.append(zero_module(nn.Linear(hint_nf[-1], model_channels)))
        self.input_hint_block.append(zero_module(nn.Linear(hint_nf[-1], model_channels)))

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def build_hint_patch_embed(self):
    def build_hint_patch_embed(self):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：concat_padding_mask, in_channels, patch_spatial, patch_temporal, model_channels = (
        concat_padding_mask, in_channels, patch_spatial, patch_temporal, model_channels = (
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.concat_padding_mask,
            self.concat_padding_mask,
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.hint_channels,
            self.hint_channels,
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.patch_spatial,
            self.patch_spatial,
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.patch_temporal,
            self.patch_temporal,
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.model_channels,
            self.model_channels,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：patch_spatial = patch_spatial if in_channels == 128 else 1
        patch_spatial = patch_spatial if in_channels == 128 else 1
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels = in_channels + 1 if (concat_padding_mask and in_channels == 128) else in_channels
        in_channels = in_channels + 1 if (concat_padding_mask and in_channels == 128) else in_channels
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.x_embedder2 = PatchEmbed(
        self.x_embedder2 = PatchEmbed(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：spatial_patch_size=patch_spatial,
            spatial_patch_size=patch_spatial,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_patch_size=patch_temporal,
            temporal_patch_size=patch_temporal,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=in_channels,
            in_channels=in_channels,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=model_channels,
            out_channels=model_channels,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def prepare_hint_embedded_sequence(
    def prepare_hint_embedded_sequence(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, x_B_C_T_H_W: torch.Tensor, fps: Optional[torch.Tensor] = None, padding_mask: Optional[t...
        self, x_B_C_T_H_W: torch.Tensor, fps: Optional[torch.Tensor] = None, padding_mask: Optional[torch.Tensor] = None
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[torch.Tensor, Optional[torch.Tensor]]:
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor]]:
        # 中文说明：根据条件选择执行分支；代码：if self.concat_padding_mask and self.hint_channels==128:
        if self.concat_padding_mask and self.hint_channels==128:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding_mask = transforms.functional.resize(
            padding_mask = transforms.functional.resize(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：padding_mask, list(x_B_C_T_H_W.shape[-2:]), interpolation=transforms.InterpolationMode.NEAREST
                padding_mask, list(x_B_C_T_H_W.shape[-2:]), interpolation=transforms.InterpolationMode.NEAREST
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_C_T_H_W = torch.cat(
            x_B_C_T_H_W = torch.cat(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：[x_B_C_T_H_W, padding_mask.unsqueeze(1).repeat(x_B_C_T_H_W.shape[0], 1, x_B_C_T_H_W.shape[2],...
                [x_B_C_T_H_W, padding_mask.unsqueeze(1).repeat(x_B_C_T_H_W.shape[0], 1, x_B_C_T_H_W.shape[2], 1, 1)],
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dim=1,
                dim=1,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_T_H_W_D = self.x_embedder2(x_B_C_T_H_W)
        x_B_T_H_W_D = self.x_embedder2(x_B_C_T_H_W)

        # 中文说明：根据条件选择执行分支；代码：if "rope" in self.pos_emb_cls.lower():
        if "rope" in self.pos_emb_cls.lower():
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return x_B_T_H_W_D, self.pos_embedder(x_B_T_H_W_D, fps=fps)
            return x_B_T_H_W_D, self.pos_embedder(x_B_T_H_W_D, fps=fps)

        # 中文说明：根据条件选择执行分支；代码：if "fps_aware" in self.pos_emb_cls:
        if "fps_aware" in self.pos_emb_cls:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_T_H_W_D = x_B_T_H_W_D + self.pos_embedder(x_B_T_H_W_D, fps=fps) # [B, T, H, W, D]
            x_B_T_H_W_D = x_B_T_H_W_D + self.pos_embedder(x_B_T_H_W_D, fps=fps)  # [B, T, H, W, D]
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_T_H_W_D = x_B_T_H_W_D + self.pos_embedder(x_B_T_H_W_D) # [B, T, H, W, D]
            x_B_T_H_W_D = x_B_T_H_W_D + self.pos_embedder(x_B_T_H_W_D)  # [B, T, H, W, D]
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x_B_T_H_W_D, None
        return x_B_T_H_W_D, None

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def encode_hint(
    def encode_hint(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：hint: torch.Tensor,
        hint: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：fps: Optional[torch.Tensor] = None,
        fps: Optional[torch.Tensor] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：padding_mask: Optional[torch.Tensor] = None,
        padding_mask: Optional[torch.Tensor] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_type: Optional[DataType] = DataType.VIDEO,
        data_type: Optional[DataType] = DataType.VIDEO,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor:
    ) -> torch.Tensor:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# assert hint.size(1) <= self.hint_channels, f"Expected hint channels <= {self.hint_channels}...
        # assert hint.size(1) <= self.hint_channels, f"Expected hint channels <= {self.hint_channels}, got {hint.size(1)}"
        # 中文说明：根据条件选择执行分支；代码：if hint.size(1) < self.hint_channels:
        if hint.size(1) < self.hint_channels:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding_shape = list(hint.shape)
            padding_shape = list(hint.shape)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding_shape[1] = self.hint_channels - hint.size(1)
            padding_shape[1] = self.hint_channels - hint.size(1)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hint = torch.cat([hint, torch.zeros(*padding_shape, dtype=hint.dtype, device=hint.device)], d...
            hint = torch.cat([hint, torch.zeros(*padding_shape, dtype=hint.dtype, device=hint.device)], dim=1)
        
        # 中文说明：检查运行时假设是否成立；代码：assert isinstance(
        assert isinstance(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_type, DataType
            data_type, DataType
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"Expected DataType, got {type(data_type)}. We need discuss this flag later."
        ), f"Expected DataType, got {type(data_type)}. We need discuss this flag later."

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：hint_B_T_H_W_D, _ = self.prepare_hint_embedded_sequence(hint, fps=fps, padding_mask=padding_m...
        hint_B_T_H_W_D, _ = self.prepare_hint_embedded_sequence(hint, fps=fps, padding_mask=padding_mask)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hint = rearrange(hint_B_T_H_W_D, "B T H W D -> T H W B D")
        hint = rearrange(hint_B_T_H_W_D, "B T H W D -> T H W B D")
  
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：guided_hint = self.input_hint_block(hint)
        guided_hint = self.input_hint_block(hint)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return guided_hint
        return guided_hint
    
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(
    def forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_B_C_T_H_W: torch.Tensor,
        x_B_C_T_H_W: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：timesteps_B_T: torch.Tensor,
        timesteps_B_T: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：crossattn_emb: torch.Tensor,
        crossattn_emb: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：condition_video_input_mask_B_C_T_H_W: Optional[torch.Tensor] = None,
        condition_video_input_mask_B_C_T_H_W: Optional[torch.Tensor] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：fps: Optional[torch.Tensor] = None,
        fps: Optional[torch.Tensor] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：padding_mask: Optional[torch.Tensor] = None,
        padding_mask: Optional[torch.Tensor] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_type: Optional[DataType] = DataType.VIDEO,
        data_type: Optional[DataType] = DataType.VIDEO,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：use_cuda_graphs: bool = False,
        use_cuda_graphs: bool = False,
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# For Ctrl
        # For Ctrl
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：hint_key: Optional[str] = None,
        hint_key: Optional[str] = None,
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# control_weight: Optional[float] = 1.0,
        # control_weight: Optional[float] = 1.0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_layers_to_use: Optional[int] = -1,
        num_layers_to_use: Optional[int] = -1,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：condition_video_input_mask: Optional[torch.Tensor] = None,
        condition_video_input_mask: Optional[torch.Tensor] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：is_training_base_model: bool = False,
        is_training_base_model: bool = False,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**kwargs,
        **kwargs,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor | List[torch.Tensor] | Tuple[torch.Tensor, List[torch.Tensor]]:
    ) -> torch.Tensor | List[torch.Tensor] | Tuple[torch.Tensor, List[torch.Tensor]]:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_input = x_B_C_T_H_W
        x_input = x_B_C_T_H_W
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hint = kwargs.pop(hint_key) #[1, 16, T, 60, 104]
        hint = kwargs.pop(hint_key) #[1, 16, T, 60, 104]
        # 中文说明：检查运行时假设是否成立；代码：assert hint is not None
        assert hint is not None
       
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：guided_hints = self.encode_hint(hint, fps=fps, padding_mask=padding_mask, data_type=data_type...
        guided_hints = self.encode_hint(hint, fps=fps, padding_mask=padding_mask, data_type=data_type) #T, 30, 56, 1, 2048
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：guided_hints = torch.chunk(guided_hints, hint.shape[0] // x_input.shape[0], dim=3)
        guided_hints = torch.chunk(guided_hints, hint.shape[0] // x_input.shape[0], dim=3)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Only support multi-control at inference time
        # Only support multi-control at inference time
        # 中文说明：检查运行时假设是否成立；代码：assert len(guided_hints) == 1 or not torch.is_grad_enabled()
        assert len(guided_hints) == 1 or not torch.is_grad_enabled()
        

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：B, C, T, H, W = x_input.shape
        B, C, T, H, W = x_input.shape
        # 中文说明：根据条件选择执行分支；代码：if data_type == DataType.VIDEO:
        if data_type == DataType.VIDEO:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_C_T_H_W = torch.cat([x_B_C_T_H_W, condition_video_input_mask_B_C_T_H_W.type_as(x_B_C_T_H_...
            x_B_C_T_H_W = torch.cat([x_B_C_T_H_W, condition_video_input_mask_B_C_T_H_W.type_as(x_B_C_T_H_W)], dim=1)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：B, _, T, H, W = x_B_C_T_H_W.shape
            B, _, T, H, W = x_B_C_T_H_W.shape
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_C_T_H_W = torch.cat(
            x_B_C_T_H_W = torch.cat(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：[x_B_C_T_H_W, torch.zeros((B, 1, T, H, W), dtype=x_B_C_T_H_W.dtype, device=x_B_C_T_H_W.device...
                [x_B_C_T_H_W, torch.zeros((B, 1, T, H, W), dtype=x_B_C_T_H_W.dtype, device=x_B_C_T_H_W.device)], dim=1
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.crossattn_emb = crossattn_emb
        self.crossattn_emb = crossattn_emb
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：outs = {}
        outs = {}

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_control_blocks = self.layer_mask.index(True)
        num_control_blocks = self.layer_mask.index(True)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_layers_to_use = num_control_blocks
        num_layers_to_use = num_control_blocks
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：control_gate_per_layer = [i < num_layers_to_use for i in range(num_control_blocks)]
        control_gate_per_layer = [i < num_layers_to_use for i in range(num_control_blocks)]

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_training = torch.is_grad_enabled()
        is_training = torch.is_grad_enabled()
        # 中文说明：根据条件选择执行分支；代码：if is_training and is_training_base_model:
        if is_training and is_training_base_model:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：coin_flip = torch.rand(B).to(x_B_C_T_H_W.device) > self.dropout_ctrl_branch # prob for only t...
            coin_flip = torch.rand(B).to(x_B_C_T_H_W.device) > self.dropout_ctrl_branch  # prob for only training base model
            # 中文说明：根据条件选择执行分支；代码：if self.blocks["block0"].x_format == "THWBD":
            if self.blocks["block0"].x_format == "THWBD":
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：coin_flip = coin_flip[None, None, None, :, None]
                coin_flip = coin_flip[None, None, None, :, None]
            # 中文说明：根据条件选择执行分支；代码：elif self.blocks["block0"].x_format == "BTHWD":
            elif self.blocks["block0"].x_format == "BTHWD":
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：coin_flip = coin_flip[:, None, None, None, None]
                coin_flip = coin_flip[:, None, None, None, None]
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：coin_flip = 1
            coin_flip = 1

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# if isinstance(control_weight, torch.Tensor):
        # if isinstance(control_weight, torch.Tensor):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# if control_weight.ndim == 0: # Single scalar tensor
        #     if control_weight.ndim == 0:  # Single scalar tensor
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# control_weight = [float(control_weight)] * len(guided_hints)
        #         control_weight = [float(control_weight)] * len(guided_hints)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# elif control_weight.ndim == 1: # List of scalar weights
        #     elif control_weight.ndim == 1:  # List of scalar weights
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# control_weight = [float(w) for w in control_weight]
        #         control_weight = [float(w) for w in control_weight]
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# else: # Spatial-temporal weight maps
        #     else:  # Spatial-temporal weight maps
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# control_weight = [w for w in control_weight] # Keep as tensor
        #         control_weight = [w for w in control_weight]  # Keep as tensor
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# else:
        # else:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：control_weight = self.control_weight
        control_weight = self.control_weight
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：control_weight = [control_weight] * len(guided_hints)
        control_weight = [control_weight] * len(guided_hints)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_before_blocks = x_B_C_T_H_W.clone()
        x_before_blocks = x_B_C_T_H_W.clone()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i, guided_hint in enumerate(guided_hints):
        for i, guided_hint in enumerate(guided_hints):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_C_T_H_W = x_before_blocks
            x_B_C_T_H_W = x_before_blocks
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：blocks = self.blocks
            blocks = self.blocks
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：zero_blocks = self.zero_blocks
            zero_blocks = self.zero_blocks
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t_embedder = self.t_embedder
            t_embedder = self.t_embedder
    

            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_B_T_H_W_D, rope_emb_L_1_1_D, extra_pos_emb_B_T_H_W_D_or_T_H_W_B_D = self.prepare_embedded_s...
            x_B_T_H_W_D, rope_emb_L_1_1_D, extra_pos_emb_B_T_H_W_D_or_T_H_W_B_D = self.prepare_embedded_sequence(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_B_C_T_H_W, fps=fps, padding_mask=padding_mask
                    x_B_C_T_H_W, fps=fps, padding_mask=padding_mask
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )   

            # 中文说明：根据条件选择执行分支；代码：if timesteps_B_T.ndim == 1:
            if timesteps_B_T.ndim == 1:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：timesteps_B_T = timesteps_B_T.unsqueeze(1)
                timesteps_B_T = timesteps_B_T.unsqueeze(1)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：t_embedding_B_T_D, adaln_lora_B_T_3D = self.t_embedder(timesteps_B_T)
            t_embedding_B_T_D, adaln_lora_B_T_3D = self.t_embedder(timesteps_B_T)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t_embedding_B_T_D = self.t_embedding_norm(t_embedding_B_T_D)
            t_embedding_B_T_D = self.t_embedding_norm(t_embedding_B_T_D)
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# for logging purpose
            # for logging purpose
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：affline_scale_log_info = {}
            affline_scale_log_info = {}
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：affline_scale_log_info["t_embedding_B_T_D"] = t_embedding_B_T_D.detach()
            affline_scale_log_info["t_embedding_B_T_D"] = t_embedding_B_T_D.detach()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.affline_scale_log_info = affline_scale_log_info
            self.affline_scale_log_info = affline_scale_log_info
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.affline_emb = t_embedding_B_T_D
            self.affline_emb = t_embedding_B_T_D
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.crossattn_emb = crossattn_emb
            self.crossattn_emb = crossattn_emb

            # 中文说明：根据条件选择执行分支；代码：if extra_pos_emb_B_T_H_W_D_or_T_H_W_B_D is not None:
            if extra_pos_emb_B_T_H_W_D_or_T_H_W_B_D is not None:
                # 中文说明：检查运行时假设是否成立；代码：assert (
                assert (
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_T_H_W_D.shape == extra_pos_emb_B_T_H_W_D_or_T_H_W_B_D.shape
                    x_B_T_H_W_D.shape == extra_pos_emb_B_T_H_W_D_or_T_H_W_B_D.shape
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"{x_B_T_H_W_D.shape} != {extra_pos_emb_B_T_H_W_D_or_T_H_W_B_D.shape}"
                ), f"{x_B_T_H_W_D.shape} != {extra_pos_emb_B_T_H_W_D_or_T_H_W_B_D.shape}"

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_kwargs = {
            block_kwargs = {
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："rope_emb_L_1_1_D": rope_emb_L_1_1_D,
                "rope_emb_L_1_1_D": rope_emb_L_1_1_D,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："adaln_lora_B_T_3D": adaln_lora_B_T_3D,
                "adaln_lora_B_T_3D": adaln_lora_B_T_3D,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："extra_per_block_pos_emb": extra_pos_emb_B_T_H_W_D_or_T_H_W_B_D,
                "extra_per_block_pos_emb": extra_pos_emb_B_T_H_W_D_or_T_H_W_B_D,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
            }
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for idx, block in enumerate(blocks):
            for idx, block in enumerate(blocks):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_T_H_W_D = block(
                x_B_T_H_W_D = block(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_B_T_H_W_D,
                    x_B_T_H_W_D,
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：t_embedding_B_T_D,
                    t_embedding_B_T_D,
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：crossattn_emb,
                    crossattn_emb,
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**block_kwargs,
                    **block_kwargs,
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：根据条件选择执行分支；代码：if guided_hint is not None:
                if guided_hint is not None:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_T_H_W_D = x_B_T_H_W_D + guided_hint.permute(3, 0, 1, 2, 4)
                    x_B_T_H_W_D = x_B_T_H_W_D + guided_hint.permute(3, 0, 1, 2, 4)
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：guided_hint = None
                    guided_hint = None

                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name = f"block{idx}"
                name = f"block{idx}"
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gate = control_gate_per_layer[idx]
                gate = control_gate_per_layer[idx]
                # 中文说明：根据条件选择执行分支；代码：if isinstance(control_weight[i], (float, int)):
                if isinstance(control_weight[i], (float, int)):
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hint_val = zero_blocks[name](x_B_T_H_W_D) * control_weight[i] * coin_flip * gate
                    hint_val = zero_blocks[name](x_B_T_H_W_D) * control_weight[i] * coin_flip * gate
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：else: # Spatial-temporal weights [num_controls, B, 1, T, H, W]
                else:  # Spatial-temporal weights [num_controls, B, 1, T, H, W]
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：control_feat = zero_blocks[name](x)
                    control_feat = zero_blocks[name](x)
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Get current feature dimensions
                    # Get current feature dimensions
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：weight_map = control_weight[i] # [B, 1, T, H, W]
                    weight_map = control_weight[i]  # [B, 1, T, H, W]
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Reshape to match THWBD format
                    # Reshape to match THWBD format
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：weight_map = weight_map.permute(2, 3, 4, 0, 1) # [T, H, W, B, 1]
                    weight_map = weight_map.permute(2, 3, 4, 0, 1)  # [T, H, W, B, 1]
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：weight_map = weight_map.view(T * H * W, 1, 1, B, 1)
                    weight_map = weight_map.view(T * H * W, 1, 1, B, 1)

                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hint_val = control_feat * weight_map * coin_flip * gate
                    hint_val = control_feat * weight_map * coin_flip * gate
                # 中文说明：根据条件选择执行分支；代码：if name not in outs:
                if name not in outs:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：outs[name] = hint_val
                    outs[name] = hint_val
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：outs[name] += hint_val
                    outs[name] += hint_val


        # 中文说明：从当前函数返回结果或结束函数执行；代码：return outs
        return outs