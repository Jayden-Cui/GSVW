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

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.conditioner import DataType
from videoworld2.conditioner import DataType
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.models.text2image_dit import MiniTrainDIT
from videoworld2.models.text2image_dit import MiniTrainDIT


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class MinimalV1LVGDiT(MiniTrainDIT):
class MinimalV1LVGDiT(MiniTrainDIT):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, *args, **kwargs):
    def __init__(self, *args, **kwargs):
        # 中文说明：检查运行时假设是否成立；代码：assert "in_channels" in kwargs, "in_channels must be provided"
        assert "in_channels" in kwargs, "in_channels must be provided"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["in_channels"] += 1 # Add 1 for the condition mask
        kwargs["in_channels"] += 1  # Add 1 for the condition mask
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)

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
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**kwargs,
        **kwargs,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor | List[torch.Tensor] | Tuple[torch.Tensor, List[torch.Tensor]]:
    ) -> torch.Tensor | List[torch.Tensor] | Tuple[torch.Tensor, List[torch.Tensor]]:
        
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_ctrl = kwargs.get('x_ctrl', None)
        x_ctrl = kwargs.get('x_ctrl', None)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del kwargs
        del kwargs
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs = {"x_ctrl": x_ctrl}
        kwargs = {"x_ctrl": x_ctrl}
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
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return super().forward(
        return super().forward(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_C_T_H_W=x_B_C_T_H_W,
            x_B_C_T_H_W=x_B_C_T_H_W,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：timesteps_B_T=timesteps_B_T,
            timesteps_B_T=timesteps_B_T,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：crossattn_emb=crossattn_emb,
            crossattn_emb=crossattn_emb,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fps=fps,
            fps=fps,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding_mask=padding_mask,
            padding_mask=padding_mask,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_type=data_type,
            data_type=data_type,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_cuda_graphs=use_cuda_graphs,
            use_cuda_graphs=use_cuda_graphs,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**kwargs
            **kwargs
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
