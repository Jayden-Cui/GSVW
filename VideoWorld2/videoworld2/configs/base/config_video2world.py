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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from copy import deepcopy
from copy import deepcopy
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from enum import Enum
from enum import Enum

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import attrs
import attrs

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.conditioner import BooleanFlag, ReMapkey, TextAttr
from videoworld2.conditioner import BooleanFlag, ReMapkey, TextAttr
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.configs.base.defaults.ema import EMAConfig
from videoworld2.configs.base.defaults.ema import EMAConfig
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.configs.vid2vid.defaults.conditioner import Vid2VidConditioner
from videoworld2.configs.vid2vid.defaults.conditioner import Vid2VidConditioner
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.models.text2image_dit import SACConfig
from videoworld2.models.text2image_dit import SACConfig
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.models.video2world_dit import MinimalV1LVGDiT
from videoworld2.models.video2world_dit import MinimalV1LVGDiT
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.models.ctrl_video2world_dit import CtrlEncoder
from videoworld2.models.ctrl_video2world_dit import CtrlEncoder
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.tokenizers.tokenizer import TokenizerInterface
from videoworld2.tokenizers.tokenizer import TokenizerInterface

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.config import make_freezable
from imaginaire.config import make_freezable
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import LazyCall as L
from imaginaire.lazy_config import LazyCall as L
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import LazyDict
from imaginaire.lazy_config import LazyDict




# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
"""
Video2WorldPipelineConfig
├── conditioner (Vid2VidConditioner)
│   ├── fps (ReMapkey)
│   ├── padding_mask (ReMapkey)
│   ├── text (TextAttr)
│   └── use_video_condition (BooleanFlag)
├── net (MinimalV1LVGDiT)
│   └── sac_config (SACConfig)
├── tokenizer (TokenizerInterface)
├── prompt_refiner_config (CosmosReason1Config)
├── guardrail_config (CosmosGuardrailConfig)
├── ema (EMAConfig)
└── timestamps (SolverTimestampConfig)
"""

# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ConditioningStrategy(str, Enum):
class ConditioningStrategy(str, Enum):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：FRAME_REPLACE = "frame_replace" # First few frames of the video are replaced with the conditi...
    FRAME_REPLACE = "frame_replace"  # First few frames of the video are replaced with the conditional frames
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：CHANNEL_CONCAT = "channel_concat" # First few frames of the video are concatenated in the cha...
    CHANNEL_CONCAT = "channel_concat"  # First few frames of the video are concatenated in the channel dimension

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __str__(self) -> str:
    def __str__(self) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.value
        return self.value


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@make_freezable
@make_freezable
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class SolverTimestampConfig:
class SolverTimestampConfig:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：nfe: int = 35
    nfe: int = 35
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：t_min: float = 0.002
    t_min: float = 0.002
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：t_max: float = 80.0
    t_max: float = 80.0
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：order: float = 7.0
    order: float = 7.0
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：is_forward: bool = False # whether generate forward or backward timestamps
    is_forward: bool = False  # whether generate forward or backward timestamps


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@make_freezable
@make_freezable
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class CosmosReason1Config:
class CosmosReason1Config:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：checkpoint_dir: str
    checkpoint_dir: str
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：offload_model_to_cpu: bool = True
    offload_model_to_cpu: bool = True
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：enabled: bool = True
    enabled: bool = True


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@make_freezable
@make_freezable
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class CosmosGuardrailConfig:
class CosmosGuardrailConfig:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：checkpoint_dir: str
    checkpoint_dir: str
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：offload_model_to_cpu: bool = True
    offload_model_to_cpu: bool = True
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：enabled: bool = True
    enabled: bool = True


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@make_freezable
@make_freezable
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Video2WorldPipelineConfig:
class Video2WorldPipelineConfig:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：adjust_video_noise: bool
    adjust_video_noise: bool
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：conditioner: LazyDict
    conditioner: LazyDict
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：conditioning_strategy: str
    conditioning_strategy: str
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：min_num_conditional_frames: int
    min_num_conditional_frames: int
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_num_conditional_frames: int
    max_num_conditional_frames: int
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sigma_conditional: float
    sigma_conditional: float
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：net: LazyDict
    net: LazyDict
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：tokenizer: LazyDict
    tokenizer: LazyDict
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：prompt_refiner_config: CosmosReason1Config
    prompt_refiner_config: CosmosReason1Config
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：guardrail_config: CosmosGuardrailConfig
    guardrail_config: CosmosGuardrailConfig
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：precision: str
    precision: str
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rectified_flow_t_scaling_factor: float
    rectified_flow_t_scaling_factor: float
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：resize_online: bool
    resize_online: bool
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：resolution: str
    resolution: str
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ema: EMAConfig
    ema: EMAConfig
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sigma_data: float = 1.0
    sigma_data: float = 1.0
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：state_ch: int = 16
    state_ch: int = 16
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：state_t: int = 24
    state_t: int = 24
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：text_encoder_class: str = "T5"
    text_encoder_class: str = "T5"
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：input_data_key: str = "video"
    input_data_key: str = "video"
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：input_image_key: str = "images"
    input_image_key: str = "images"
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：timestamps: SolverTimestampConfig = attrs.field(factory=SolverTimestampConfig)
    timestamps: SolverTimestampConfig = attrs.field(factory=SolverTimestampConfig)

 
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@make_freezable
@make_freezable
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Video2WorldWithCtrlPipelineConfig:
class Video2WorldWithCtrlPipelineConfig:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：adjust_video_noise: bool
    adjust_video_noise: bool
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：conditioner: LazyDict
    conditioner: LazyDict
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：conditioning_strategy: str
    conditioning_strategy: str
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：min_num_conditional_frames: int
    min_num_conditional_frames: int
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_num_conditional_frames: int
    max_num_conditional_frames: int
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sigma_conditional: float
    sigma_conditional: float
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：net: LazyDict
    net: LazyDict
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：net_ctrl: LazyDict
    net_ctrl: LazyDict
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：tokenizer: LazyDict
    tokenizer: LazyDict
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：prompt_refiner_config: CosmosReason1Config
    prompt_refiner_config: CosmosReason1Config
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：guardrail_config: CosmosGuardrailConfig
    guardrail_config: CosmosGuardrailConfig
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：precision: str
    precision: str
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rectified_flow_t_scaling_factor: float
    rectified_flow_t_scaling_factor: float
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：resize_online: bool
    resize_online: bool
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：resolution: str
    resolution: str
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ema: EMAConfig
    ema: EMAConfig
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sigma_data: float = 1.0
    sigma_data: float = 1.0
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：state_ch: int = 16
    state_ch: int = 16
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：state_t: int = 24
    state_t: int = 24
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：text_encoder_class: str = "T5"
    text_encoder_class: str = "T5"
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：input_data_key: str = "video"
    input_data_key: str = "video"
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：input_image_key: str = "images"
    input_image_key: str = "images"
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：timestamps: SolverTimestampConfig = attrs.field(factory=SolverTimestampConfig)
    timestamps: SolverTimestampConfig = attrs.field(factory=SolverTimestampConfig)
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：hint_key: str = "control_input_depth"
    hint_key: str = "control_input_depth"
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ldm_input_key: str = "video"
    ldm_input_key: str = "video"
    


# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Cosmos Predict2 Ctrl Branch
# Cosmos Predict2 Ctrl Branch 
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_CTRL_NET_2B = L(CtrlEncoder)(
PREDICT2_VIDEO2WORLD_CTRL_NET_2B = L(CtrlEncoder)(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_img_h=240,
    max_img_h=240,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_img_w=240,
    max_img_w=240,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_frames=128,
    max_frames=128,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=16,
    in_channels=16,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=16,
    out_channels=16,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：patch_spatial=2,
    patch_spatial=2,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：patch_temporal=1,
    patch_temporal=1,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：concat_padding_mask=True,
    concat_padding_mask=True,
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# attention settings
    # attention settings
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_channels=2048,
    model_channels=2048,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_blocks=28,
    num_blocks=28,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_heads=16,
    num_heads=16,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：atten_backend="minimal_a2a",
    atten_backend="minimal_a2a",
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# positional embedding settings
    # positional embedding settings
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pos_emb_cls="rope3d",
    pos_emb_cls="rope3d",
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pos_emb_learnable=True,
    pos_emb_learnable=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pos_emb_interpolation="crop",
    pos_emb_interpolation="crop",
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_adaln_lora=True,
    use_adaln_lora=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：adaln_lora_dim=256,
    adaln_lora_dim=256,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rope_h_extrapolation_ratio=3.0,
    rope_h_extrapolation_ratio=3.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rope_w_extrapolation_ratio=3.0,
    rope_w_extrapolation_ratio=3.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rope_t_extrapolation_ratio=1.0,
    rope_t_extrapolation_ratio=1.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extra_per_block_abs_pos_emb=False,
    extra_per_block_abs_pos_emb=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rope_enable_fps_modulation=False,
    rope_enable_fps_modulation=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sac_config=L(SACConfig)(
    sac_config=L(SACConfig)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：every_n_blocks=1,
        every_n_blocks=1,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mode="predict2_2b_720",
        mode="predict2_2b_720",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hint_channels=128,
    hint_channels=128,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：layer_mask=[True if (i >= 3) else False for i in range(28)],
    layer_mask=[True if (i >= 3) else False for i in range(28)],
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：control_weight=1,
    control_weight=1,
    
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Cosmos Predict2 Video2World 2B
# Cosmos Predict2 Video2World 2B
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_NET_2B = L(MinimalV1LVGDiT)(
PREDICT2_VIDEO2WORLD_NET_2B = L(MinimalV1LVGDiT)(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_img_h=240,
    max_img_h=240,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_img_w=240,
    max_img_w=240,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_frames=128,
    max_frames=128,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=16,
    in_channels=16,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=16,
    out_channels=16,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：patch_spatial=2,
    patch_spatial=2,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：patch_temporal=1,
    patch_temporal=1,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：concat_padding_mask=True,
    concat_padding_mask=True,
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# attention settings
    # attention settings
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_channels=2048,
    model_channels=2048,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_blocks=28,
    num_blocks=28,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_heads=16,
    num_heads=16,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：atten_backend="minimal_a2a",
    atten_backend="minimal_a2a",
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# positional embedding settings
    # positional embedding settings
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pos_emb_cls="rope3d",
    pos_emb_cls="rope3d",
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pos_emb_learnable=True,
    pos_emb_learnable=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pos_emb_interpolation="crop",
    pos_emb_interpolation="crop",
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_adaln_lora=True,
    use_adaln_lora=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：adaln_lora_dim=256,
    adaln_lora_dim=256,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rope_h_extrapolation_ratio=3.0,
    rope_h_extrapolation_ratio=3.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rope_w_extrapolation_ratio=3.0,
    rope_w_extrapolation_ratio=3.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rope_t_extrapolation_ratio=1.0,
    rope_t_extrapolation_ratio=1.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extra_per_block_abs_pos_emb=False,
    extra_per_block_abs_pos_emb=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rope_enable_fps_modulation=False,
    rope_enable_fps_modulation=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sac_config=L(SACConfig)(
    sac_config=L(SACConfig)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：every_n_blocks=1,
        every_n_blocks=1,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mode="predict2_2b_720",
        mode="predict2_2b_720",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)


# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_PIPELINE_CTRL_2B = Video2WorldWithCtrlPipelineConfig(
PREDICT2_VIDEO2WORLD_PIPELINE_CTRL_2B = Video2WorldWithCtrlPipelineConfig(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：adjust_video_noise=True,
    adjust_video_noise=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：conditioner=L(Vid2VidConditioner)(
    conditioner=L(Vid2VidConditioner)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fps=L(ReMapkey)(
        fps=L(ReMapkey)(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout_rate=0.0,
            dropout_rate=0.0,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dtype=None,
            dtype=None,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_key="fps",
            input_key="fps",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_key="fps",
            output_key="fps",
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding_mask=L(ReMapkey)(
        padding_mask=L(ReMapkey)(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout_rate=0.0,
            dropout_rate=0.0,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dtype=None,
            dtype=None,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_key="padding_mask",
            input_key="padding_mask",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_key="padding_mask",
            output_key="padding_mask",
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text=L(TextAttr)(
        text=L(TextAttr)(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout_rate=0.0,
            dropout_rate=0.0,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_key=["t5_text_embeddings"],
            input_key=["t5_text_embeddings"],
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_video_condition=L(BooleanFlag)(
        use_video_condition=L(BooleanFlag)(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout_rate=0.0,
            dropout_rate=0.0,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_key="fps",
            input_key="fps",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_key="use_video_condition",
            output_key="use_video_condition",
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：conditioning_strategy=str(ConditioningStrategy.FRAME_REPLACE),
    conditioning_strategy=str(ConditioningStrategy.FRAME_REPLACE),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_num_conditional_frames=1,
    min_num_conditional_frames=1,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_num_conditional_frames=2,
    max_num_conditional_frames=2,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net=PREDICT2_VIDEO2WORLD_NET_2B,
    net=PREDICT2_VIDEO2WORLD_NET_2B,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net_ctrl=PREDICT2_VIDEO2WORLD_CTRL_NET_2B,
    net_ctrl=PREDICT2_VIDEO2WORLD_CTRL_NET_2B,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：precision="bfloat16",
    precision="bfloat16",
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rectified_flow_t_scaling_factor=1.0,
    rectified_flow_t_scaling_factor=1.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resize_online=True,
    resize_online=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resolution="720",
    resolution="720",
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ema=L(EMAConfig)(enabled=False), # defaults to inference
    ema=L(EMAConfig)(enabled=False),  # defaults to inference
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_conditional=0.0001,
    sigma_conditional=0.0001,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_data=1.0,
    sigma_data=1.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_ch=16,
    state_ch=16,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_t=24,
    state_t=24,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text_encoder_class="T5",
    text_encoder_class="T5",
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tokenizer=L(TokenizerInterface)(
    tokenizer=L(TokenizerInterface)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：chunk_duration=81,
        chunk_duration=81,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_window=16,
        temporal_window=16,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：load_mean_std=False,
        load_mean_std=False,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="tokenizer",
        name="tokenizer",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：vae_pth="checkpoints/Cosmos-Predict2-2B-Video2World/tokenizer/tokenizer.pth",
        vae_pth="checkpoints/Cosmos-Predict2-2B-Video2World/tokenizer/tokenizer.pth",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prompt_refiner_config=CosmosReason1Config(
    prompt_refiner_config=CosmosReason1Config(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint_dir="checkpoints/Cosmos-Reason1-7B",
        checkpoint_dir="checkpoints/Cosmos-Reason1-7B",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：offload_model_to_cpu=True,
        offload_model_to_cpu=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enabled=True,
        enabled=True,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：guardrail_config=CosmosGuardrailConfig(
    guardrail_config=CosmosGuardrailConfig(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint_dir="checkpoints/",
        checkpoint_dir="checkpoints/",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：offload_model_to_cpu=True,
        offload_model_to_cpu=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enabled=True,
        enabled=True,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hint_key='control_input_depth'
    hint_key='control_input_depth'
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_PIPELINE_2B = Video2WorldPipelineConfig(
PREDICT2_VIDEO2WORLD_PIPELINE_2B = Video2WorldPipelineConfig(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：adjust_video_noise=True,
    adjust_video_noise=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：conditioner=L(Vid2VidConditioner)(
    conditioner=L(Vid2VidConditioner)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fps=L(ReMapkey)(
        fps=L(ReMapkey)(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout_rate=0.0,
            dropout_rate=0.0,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dtype=None,
            dtype=None,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_key="fps",
            input_key="fps",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_key="fps",
            output_key="fps",
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding_mask=L(ReMapkey)(
        padding_mask=L(ReMapkey)(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout_rate=0.0,
            dropout_rate=0.0,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dtype=None,
            dtype=None,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_key="padding_mask",
            input_key="padding_mask",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_key="padding_mask",
            output_key="padding_mask",
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text=L(TextAttr)(
        text=L(TextAttr)(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout_rate=0.0,
            dropout_rate=0.0,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_key=["t5_text_embeddings"],
            input_key=["t5_text_embeddings"],
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_video_condition=L(BooleanFlag)(
        use_video_condition=L(BooleanFlag)(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout_rate=0.0,
            dropout_rate=0.0,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_key="fps",
            input_key="fps",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_key="use_video_condition",
            output_key="use_video_condition",
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：conditioning_strategy=str(ConditioningStrategy.FRAME_REPLACE),
    conditioning_strategy=str(ConditioningStrategy.FRAME_REPLACE),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_num_conditional_frames=1,
    min_num_conditional_frames=1,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_num_conditional_frames=2,
    max_num_conditional_frames=2,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net=PREDICT2_VIDEO2WORLD_NET_2B,
    net=PREDICT2_VIDEO2WORLD_NET_2B,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：precision="bfloat16",
    precision="bfloat16",
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rectified_flow_t_scaling_factor=1.0,
    rectified_flow_t_scaling_factor=1.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resize_online=True,
    resize_online=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resolution="720",
    resolution="720",
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ema=L(EMAConfig)(enabled=False), # defaults to inference
    ema=L(EMAConfig)(enabled=False),  # defaults to inference
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_conditional=0.0001,
    sigma_conditional=0.0001,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_data=1.0,
    sigma_data=1.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_ch=16,
    state_ch=16,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_t=24,
    state_t=24,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text_encoder_class="T5",
    text_encoder_class="T5",
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tokenizer=L(TokenizerInterface)(
    tokenizer=L(TokenizerInterface)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：chunk_duration=81,
        chunk_duration=81,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_window=16,
        temporal_window=16,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：load_mean_std=False,
        load_mean_std=False,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="tokenizer",
        name="tokenizer",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：vae_pth="checkpoints/Cosmos-Predict2-2B-Video2World/tokenizer/tokenizer.pth",
        vae_pth="checkpoints/Cosmos-Predict2-2B-Video2World/tokenizer/tokenizer.pth",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prompt_refiner_config=CosmosReason1Config(
    prompt_refiner_config=CosmosReason1Config(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint_dir="checkpoints/Cosmos-Reason1-7B",
        checkpoint_dir="checkpoints/Cosmos-Reason1-7B",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：offload_model_to_cpu=True,
        offload_model_to_cpu=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enabled=True,
        enabled=True,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：guardrail_config=CosmosGuardrailConfig(
    guardrail_config=CosmosGuardrailConfig(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint_dir="checkpoints/",
        checkpoint_dir="checkpoints/",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：offload_model_to_cpu=True,
        offload_model_to_cpu=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enabled=True,
        enabled=True,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Cosmos Predict2 Video2World 14B
# Cosmos Predict2 Video2World 14B
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_NET_14B = L(MinimalV1LVGDiT)(
PREDICT2_VIDEO2WORLD_NET_14B = L(MinimalV1LVGDiT)(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_img_h=240,
    max_img_h=240,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_img_w=240,
    max_img_w=240,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_frames=128,
    max_frames=128,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_channels=16,
    in_channels=16,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_channels=16,
    out_channels=16,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：patch_spatial=2,
    patch_spatial=2,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：patch_temporal=1,
    patch_temporal=1,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：concat_padding_mask=True,
    concat_padding_mask=True,
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# attention settings
    # attention settings
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_channels=5120,
    model_channels=5120,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_blocks=36,
    num_blocks=36,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_heads=40,
    num_heads=40,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：atten_backend="minimal_a2a",
    atten_backend="minimal_a2a",
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# positional embedding settings
    # positional embedding settings
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pos_emb_cls="rope3d",
    pos_emb_cls="rope3d",
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pos_emb_learnable=True,
    pos_emb_learnable=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pos_emb_interpolation="crop",
    pos_emb_interpolation="crop",
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_adaln_lora=True,
    use_adaln_lora=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：adaln_lora_dim=256,
    adaln_lora_dim=256,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rope_h_extrapolation_ratio=2.0,
    rope_h_extrapolation_ratio=2.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rope_w_extrapolation_ratio=2.0,
    rope_w_extrapolation_ratio=2.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rope_t_extrapolation_ratio=0.8333333333333334,
    rope_t_extrapolation_ratio=0.8333333333333334,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extra_per_block_abs_pos_emb=False,
    extra_per_block_abs_pos_emb=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rope_enable_fps_modulation=False,
    rope_enable_fps_modulation=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sac_config=L(SACConfig)(
    sac_config=L(SACConfig)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：every_n_blocks=1,
        every_n_blocks=1,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mode="predict2_14b_720",
        mode="predict2_14b_720",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_PIPELINE_14B = Video2WorldPipelineConfig(
PREDICT2_VIDEO2WORLD_PIPELINE_14B = Video2WorldPipelineConfig(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：adjust_video_noise=True,
    adjust_video_noise=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：conditioner=L(Vid2VidConditioner)(
    conditioner=L(Vid2VidConditioner)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fps=L(ReMapkey)(
        fps=L(ReMapkey)(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout_rate=0.0,
            dropout_rate=0.0,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dtype=None,
            dtype=None,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_key="fps",
            input_key="fps",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_key="fps",
            output_key="fps",
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding_mask=L(ReMapkey)(
        padding_mask=L(ReMapkey)(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout_rate=0.0,
            dropout_rate=0.0,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dtype=None,
            dtype=None,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_key="padding_mask",
            input_key="padding_mask",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_key="padding_mask",
            output_key="padding_mask",
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text=L(TextAttr)(
        text=L(TextAttr)(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout_rate=0.2,
            dropout_rate=0.2,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_key=["t5_text_embeddings"],
            input_key=["t5_text_embeddings"],
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_video_condition=L(BooleanFlag)(
        use_video_condition=L(BooleanFlag)(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout_rate=0.0,
            dropout_rate=0.0,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_key="fps",
            input_key="fps",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_key="use_video_condition",
            output_key="use_video_condition",
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：conditioning_strategy=str(ConditioningStrategy.FRAME_REPLACE),
    conditioning_strategy=str(ConditioningStrategy.FRAME_REPLACE),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_num_conditional_frames=1,
    min_num_conditional_frames=1,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_num_conditional_frames=2,
    max_num_conditional_frames=2,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net=PREDICT2_VIDEO2WORLD_NET_14B,
    net=PREDICT2_VIDEO2WORLD_NET_14B,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：precision="bfloat16",
    precision="bfloat16",
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rectified_flow_t_scaling_factor=1.0,
    rectified_flow_t_scaling_factor=1.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resize_online=True,
    resize_online=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resolution="720",
    resolution="720",
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ema=L(EMAConfig)(enabled=False), # defaults to inference
    ema=L(EMAConfig)(enabled=False),  # defaults to inference
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_conditional=0.0001,
    sigma_conditional=0.0001,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_data=1.0,
    sigma_data=1.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_ch=16,
    state_ch=16,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_t=24,
    state_t=24,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text_encoder_class="T5",
    text_encoder_class="T5",
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tokenizer=L(TokenizerInterface)(
    tokenizer=L(TokenizerInterface)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：chunk_duration=81,
        chunk_duration=81,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_window=16,
        temporal_window=16,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：load_mean_std=False,
        load_mean_std=False,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="tokenizer",
        name="tokenizer",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：vae_pth="checkpoints/Cosmos-Predict2-14B-Video2World/tokenizer/tokenizer.pth",
        vae_pth="checkpoints/Cosmos-Predict2-14B-Video2World/tokenizer/tokenizer.pth",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prompt_refiner_config=CosmosReason1Config(
    prompt_refiner_config=CosmosReason1Config(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint_dir="checkpoints/Cosmos-Reason1-7B",
        checkpoint_dir="checkpoints/Cosmos-Reason1-7B",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：offload_model_to_cpu=True,
        offload_model_to_cpu=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enabled=True,
        enabled=True,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：guardrail_config=CosmosGuardrailConfig(
    guardrail_config=CosmosGuardrailConfig(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint_dir="checkpoints/",
        checkpoint_dir="checkpoints/",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：offload_model_to_cpu=True,
        offload_model_to_cpu=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enabled=True,
        enabled=True,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Cosmos Predict2 Video2World 2B pipeline config variants - resolution ["480", "720"] and fps...
# Cosmos Predict2 Video2World 2B pipeline config variants - resolution ["480", "720"] and fps [10, 16]
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 2B, resolution 480p, fps 10
# 2B, resolution 480p, fps 10
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_PIPELINE_2B_480P_10FPS = deepcopy(PREDICT2_VIDEO2WORLD_PIPELINE_2B)
PREDICT2_VIDEO2WORLD_PIPELINE_2B_480P_10FPS = deepcopy(PREDICT2_VIDEO2WORLD_PIPELINE_2B)
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_PIPELINE_2B_480P_10FPS.resolution = "480"
PREDICT2_VIDEO2WORLD_PIPELINE_2B_480P_10FPS.resolution = "480"
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_PIPELINE_2B_480P_10FPS.state_t = 16
PREDICT2_VIDEO2WORLD_PIPELINE_2B_480P_10FPS.state_t = 16
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 2B, resolution 480p, fps 16
# 2B, resolution 480p, fps 16
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_PIPELINE_2B_480P_16FPS = deepcopy(PREDICT2_VIDEO2WORLD_PIPELINE_2B)
PREDICT2_VIDEO2WORLD_PIPELINE_2B_480P_16FPS = deepcopy(PREDICT2_VIDEO2WORLD_PIPELINE_2B)
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_PIPELINE_2B_480P_16FPS.resolution = "480"
PREDICT2_VIDEO2WORLD_PIPELINE_2B_480P_16FPS.resolution = "480"

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_PIPELINE_CTRL_2B_480P_16FPS = deepcopy(PREDICT2_VIDEO2WORLD_PIPELINE_CTR...
PREDICT2_VIDEO2WORLD_PIPELINE_CTRL_2B_480P_16FPS = deepcopy(PREDICT2_VIDEO2WORLD_PIPELINE_CTRL_2B)
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_PIPELINE_CTRL_2B_480P_16FPS.resolution = "480"
PREDICT2_VIDEO2WORLD_PIPELINE_CTRL_2B_480P_16FPS.resolution = "480"

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_PIPELINE_CTRL_2B_480P_16FPS_INFER = deepcopy(PREDICT2_VIDEO2WORLD_PIPELI...
PREDICT2_VIDEO2WORLD_PIPELINE_CTRL_2B_480P_16FPS_INFER = deepcopy(PREDICT2_VIDEO2WORLD_PIPELINE_CTRL_2B)
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_PIPELINE_CTRL_2B_480P_16FPS_INFER.resolution = "480"
PREDICT2_VIDEO2WORLD_PIPELINE_CTRL_2B_480P_16FPS_INFER.resolution = "480"
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_PIPELINE_CTRL_2B_480P_16FPS_INFER.tokenizer.vae_pth = "checkpoints/Video...
PREDICT2_VIDEO2WORLD_PIPELINE_CTRL_2B_480P_16FPS_INFER.tokenizer.vae_pth = "checkpoints/VideoWorld2_dLDM_2B/tokenizer/tokenizer.pth"

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 2B, resolution 720p, fps 10
# 2B, resolution 720p, fps 10
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_PIPELINE_2B_720P_10FPS = deepcopy(PREDICT2_VIDEO2WORLD_PIPELINE_2B)
PREDICT2_VIDEO2WORLD_PIPELINE_2B_720P_10FPS = deepcopy(PREDICT2_VIDEO2WORLD_PIPELINE_2B)
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_PIPELINE_2B_720P_10FPS.state_t = 16
PREDICT2_VIDEO2WORLD_PIPELINE_2B_720P_10FPS.state_t = 16
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 2B, resolution 720p, fps 16
# 2B, resolution 720p, fps 16
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_PIPELINE_2B_720P_16FPS = PREDICT2_VIDEO2WORLD_PIPELINE_2B
PREDICT2_VIDEO2WORLD_PIPELINE_2B_720P_16FPS = PREDICT2_VIDEO2WORLD_PIPELINE_2B

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Cosmos Predict2 Video2World 14B pipeline config variants - resolution ["480", "720"] and fp...
# Cosmos Predict2 Video2World 14B pipeline config variants - resolution ["480", "720"] and fps [10, 16}]
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 14B, resolution 480p, fps 10
# 14B, resolution 480p, fps 10
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_PIPELINE_14B_480P_10FPS = deepcopy(PREDICT2_VIDEO2WORLD_PIPELINE_14B)
PREDICT2_VIDEO2WORLD_PIPELINE_14B_480P_10FPS = deepcopy(PREDICT2_VIDEO2WORLD_PIPELINE_14B)
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_PIPELINE_14B_480P_10FPS.resolution = "480"
PREDICT2_VIDEO2WORLD_PIPELINE_14B_480P_10FPS.resolution = "480"
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_PIPELINE_14B_480P_10FPS.state_t = 16
PREDICT2_VIDEO2WORLD_PIPELINE_14B_480P_10FPS.state_t = 16
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 14B, resolution 480p, fps 16
# 14B, resolution 480p, fps 16
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_PIPELINE_14B_480P_16FPS = deepcopy(PREDICT2_VIDEO2WORLD_PIPELINE_14B)
PREDICT2_VIDEO2WORLD_PIPELINE_14B_480P_16FPS = deepcopy(PREDICT2_VIDEO2WORLD_PIPELINE_14B)
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_PIPELINE_14B_480P_16FPS.resolution = "480"
PREDICT2_VIDEO2WORLD_PIPELINE_14B_480P_16FPS.resolution = "480"
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 14B, resolution 720p, fps 10
# 14B, resolution 720p, fps 10
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_PIPELINE_14B_720P_10FPS = deepcopy(PREDICT2_VIDEO2WORLD_PIPELINE_14B)
PREDICT2_VIDEO2WORLD_PIPELINE_14B_720P_10FPS = deepcopy(PREDICT2_VIDEO2WORLD_PIPELINE_14B)
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_PIPELINE_14B_720P_10FPS.state_t = 16
PREDICT2_VIDEO2WORLD_PIPELINE_14B_720P_10FPS.state_t = 16
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 14B, resolution 720p, fps 16
# 14B, resolution 720p, fps 16
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_PIPELINE_14B_720P_16FPS = PREDICT2_VIDEO2WORLD_PIPELINE_14B
PREDICT2_VIDEO2WORLD_PIPELINE_14B_720P_16FPS = PREDICT2_VIDEO2WORLD_PIPELINE_14B
