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

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.nn as nn
import torch.nn as nn
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from einops import rearrange
from einops import rearrange

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.conditioner import DataType
from videoworld2.conditioner import DataType
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.models.video2world_dit import MinimalV1LVGDiT
from videoworld2.models.video2world_dit import MinimalV1LVGDiT


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Mlp(nn.Module):
class Mlp(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, in_features, hidden_features=None, out_features=None, act_layer=nn.GELU, d...
    def __init__(self, in_features, hidden_features=None, out_features=None, act_layer=nn.GELU, drop=0.0):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_features = out_features or in_features
        out_features = out_features or in_features
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hidden_features = hidden_features or in_features
        hidden_features = hidden_features or in_features
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.fc1 = nn.Linear(in_features, hidden_features)
        self.fc1 = nn.Linear(in_features, hidden_features)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.activation = act_layer()
        self.activation = act_layer()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.fc2 = nn.Linear(hidden_features, out_features)
        self.fc2 = nn.Linear(hidden_features, out_features)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.drop = nn.Dropout(drop)
        self.drop = nn.Dropout(drop)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x):
    def forward(self, x):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.fc1(x)
        x = self.fc1(x)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.activation(x)
        x = self.activation(x)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.drop(x)
        x = self.drop(x)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.fc2(x)
        x = self.fc2(x)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self.drop(x)
        x = self.drop(x)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x
        return x


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ActionConditionedMinimalV1LVGDiT(MinimalV1LVGDiT):
class ActionConditionedMinimalV1LVGDiT(MinimalV1LVGDiT):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, *args, **kwargs):
    def __init__(self, *args, **kwargs):
        # 中文说明：检查运行时假设是否成立；代码：assert "action_dim" in kwargs, "action_dim must be provided"
        assert "action_dim" in kwargs, "action_dim must be provided"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：action_dim = kwargs["action_dim"]
        action_dim = kwargs["action_dim"]
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del kwargs["action_dim"]
        del kwargs["action_dim"]
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.action_embedder_B_D = Mlp(
        self.action_embedder_B_D = Mlp(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_features=action_dim,
            in_features=action_dim,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hidden_features=self.model_channels * 4,
            hidden_features=self.model_channels * 4,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_features=self.model_channels,
            out_features=self.model_channels,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：act_layer=lambda: nn.GELU(approximate="tanh"),
            act_layer=lambda: nn.GELU(approximate="tanh"),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：drop=0,
            drop=0,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.action_embedder_B_3D = Mlp(
        self.action_embedder_B_3D = Mlp(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_features=action_dim,
            in_features=action_dim,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hidden_features=self.model_channels * 4,
            hidden_features=self.model_channels * 4,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_features=self.model_channels * 3,
            out_features=self.model_channels * 3,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：act_layer=lambda: nn.GELU(approximate="tanh"),
            act_layer=lambda: nn.GELU(approximate="tanh"),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：drop=0,
            drop=0,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

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
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：action: Optional[torch.Tensor] = None,
        action: Optional[torch.Tensor] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**kwargs,
        **kwargs,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor | List[torch.Tensor] | Tuple[torch.Tensor, List[torch.Tensor]]:
    ) -> torch.Tensor | List[torch.Tensor] | Tuple[torch.Tensor, List[torch.Tensor]]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del kwargs
        del kwargs

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
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# NOTE: project action to action embedding
        # NOTE: project action to action embedding
        # 中文说明：检查运行时假设是否成立；代码：assert action is not None, "action must be provided"
        assert action is not None, "action must be provided"
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# action = rearrange(action, "b t d -> b 1 (t d)") # For LDM
        # action = rearrange(action, "b t d -> b 1 (t d)") # For LDM
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：action_emb_B_D = self.action_embedder_B_D(action)
        action_emb_B_D = self.action_embedder_B_D(action)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：action_emb_B_3D = self.action_embedder_B_3D(action)
        action_emb_B_3D = self.action_embedder_B_3D(action)

        # 中文说明：检查运行时假设是否成立；代码：assert isinstance(
        assert isinstance(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_type, DataType
            data_type, DataType
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"Expected DataType, got {type(data_type)}. We need discuss this flag later."
        ), f"Expected DataType, got {type(data_type)}. We need discuss this flag later."
        # 中文说明：检查运行时假设是否成立；代码：assert not (self.training and use_cuda_graphs), "CUDA Graphs are supported only for inference"
        assert not (self.training and use_cuda_graphs), "CUDA Graphs are supported only for inference"
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_B_T_H_W_D, rope_emb_L_1_1_D, extra_pos_emb_B_T_H_W_D_or_T_H_W_B_D = self.prepare_embedded_s...
        x_B_T_H_W_D, rope_emb_L_1_1_D, extra_pos_emb_B_T_H_W_D_or_T_H_W_B_D = self.prepare_embedded_sequence(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_B_C_T_H_W,
            x_B_C_T_H_W,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fps=fps,
            fps=fps,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding_mask=padding_mask,
            padding_mask=padding_mask,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：根据条件选择执行分支；代码：if timesteps_B_T.ndim == 1:
        if timesteps_B_T.ndim == 1:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：timesteps_B_T = timesteps_B_T.unsqueeze(1)
            timesteps_B_T = timesteps_B_T.unsqueeze(1)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：t_embedding_B_T_D, adaln_lora_B_T_3D = self.t_embedder(timesteps_B_T)
        t_embedding_B_T_D, adaln_lora_B_T_3D = self.t_embedder(timesteps_B_T)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# NOTE: add action embedding to the timestep embedding and adaln_lora
        # NOTE: add action embedding to the timestep embedding and adaln_lora
        # 中文说明：根据条件选择执行分支；代码：if t_embedding_B_T_D.shape[1] != 1: # For LDM
        if t_embedding_B_T_D.shape[1] != 1: # For LDM
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank = torch.distributed.get_rank()
            rank = torch.distributed.get_rank()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：context_parallel_size = 2
            context_parallel_size = 2
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：chunk_size = t_embedding_B_T_D.shape[1]
            chunk_size = t_embedding_B_T_D.shape[1]
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# world_size = torch.distributed.get_world_size()
            # world_size = torch.distributed.get_world_size()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：chunk_idx = rank % context_parallel_size
            chunk_idx = rank % context_parallel_size
            # 中文说明：根据条件选择执行分支；代码：if chunk_idx == 0:
            if chunk_idx == 0:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t_embedding_B_T_D[:, 1:] = t_embedding_B_T_D[:, 1:] + action_emb_B_D[:, :chunk_size-1]
                t_embedding_B_T_D[:, 1:] = t_embedding_B_T_D[:, 1:] + action_emb_B_D[:, :chunk_size-1]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：adaln_lora_B_T_3D[:, 1:] = adaln_lora_B_T_3D[:, 1:] + action_emb_B_3D[:, :chunk_size-1]
                adaln_lora_B_T_3D[:, 1:] = adaln_lora_B_T_3D[:, 1:] + action_emb_B_3D[:, :chunk_size-1]
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t_embedding_B_T_D = t_embedding_B_T_D + action_emb_B_D[:, chunk_idx*chunk_size-1:(chunk_idx+1...
                t_embedding_B_T_D = t_embedding_B_T_D + action_emb_B_D[:, chunk_idx*chunk_size-1:(chunk_idx+1)*chunk_size-1]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：adaln_lora_B_T_3D = adaln_lora_B_T_3D + action_emb_B_3D[:, chunk_idx*chunk_size-1:(chunk_idx+...
                adaln_lora_B_T_3D = adaln_lora_B_T_3D + action_emb_B_3D[:, chunk_idx*chunk_size-1:(chunk_idx+1)*chunk_size-1]
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t_embedding_B_T_D = t_embedding_B_T_D + action_emb_B_D
            t_embedding_B_T_D = t_embedding_B_T_D + action_emb_B_D
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：adaln_lora_B_T_3D = adaln_lora_B_T_3D + action_emb_B_3D
            adaln_lora_B_T_3D = adaln_lora_B_T_3D + action_emb_B_3D

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

        # 中文说明：根据条件选择执行分支；代码：if use_cuda_graphs:
        if use_cuda_graphs:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：shapes_key = create_cuda_graph(
            shapes_key = create_cuda_graph(
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.cuda_graphs,
                self.cuda_graphs,
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.blocks,
                self.blocks,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x_B_T_H_W_D,
                x_B_T_H_W_D,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：t_embedding_B_T_D,
                t_embedding_B_T_D,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：crossattn_emb,
                crossattn_emb,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rope_emb_L_1_1_D,
                rope_emb_L_1_1_D,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：adaln_lora_B_T_3D,
                adaln_lora_B_T_3D,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：extra_pos_emb_B_T_H_W_D_or_T_H_W_B_D,
                extra_pos_emb_B_T_H_W_D_or_T_H_W_B_D,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：blocks = self.cuda_graphs[shapes_key]
            blocks = self.cuda_graphs[shapes_key]
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：blocks = self.blocks
            blocks = self.blocks

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
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for block in blocks:
        for block in blocks:
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

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_T_H_W_O = self.final_layer(x_B_T_H_W_D, t_embedding_B_T_D, adaln_lora_B_T_3D=adaln_lora_B...
        x_B_T_H_W_O = self.final_layer(x_B_T_H_W_D, t_embedding_B_T_D, adaln_lora_B_T_3D=adaln_lora_B_T_3D)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_C_Tt_Hp_Wp = self.unpatchify(x_B_T_H_W_O)
        x_B_C_Tt_Hp_Wp = self.unpatchify(x_B_T_H_W_O)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x_B_C_Tt_Hp_Wp
        return x_B_C_Tt_Hp_Wp
