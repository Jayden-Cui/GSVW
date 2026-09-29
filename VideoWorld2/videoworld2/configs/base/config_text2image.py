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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import attrs
import attrs

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.conditioner import ReMapkey, TextAttr, VideoConditioner
from videoworld2.conditioner import ReMapkey, TextAttr, VideoConditioner
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.models.text2image_dit import MiniTrainDIT
from videoworld2.models.text2image_dit import MiniTrainDIT
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.tokenizers.tokenizer import TokenizerInterface
from videoworld2.tokenizers.tokenizer import TokenizerInterface
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.config import make_freezable
from imaginaire.config import make_freezable
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import LazyCall as L
from imaginaire.lazy_config import LazyCall as L
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import LazyDict
from imaginaire.lazy_config import LazyDict


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
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Text2ImagePipelineConfig:
class Text2ImagePipelineConfig:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：adjust_video_noise: bool
    adjust_video_noise: bool
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：conditioner: LazyDict
    conditioner: LazyDict
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：net: LazyDict
    net: LazyDict
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：tokenizer: LazyDict
    tokenizer: LazyDict
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：precision: str
    precision: str
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rectified_flow_t_scaling_factor: float
    rectified_flow_t_scaling_factor: float
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：resize_online: bool
    resize_online: bool
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：resolution: str
    resolution: str
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：timestamps: SolverTimestampConfig = attrs.field(factory=SolverTimestampConfig)
    timestamps: SolverTimestampConfig = attrs.field(factory=SolverTimestampConfig)
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sigma_data: float = 1.0
    sigma_data: float = 1.0
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：state_ch: int = 16
    state_ch: int = 16
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：state_t: int = 24
    state_t: int = 24
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：text_encoder_class: str = "T5"
    text_encoder_class: str = "T5"
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：guardrail_config: CosmosGuardrailConfig = attrs.field(factory=CosmosGuardrailConfig)
    guardrail_config: CosmosGuardrailConfig = attrs.field(factory=CosmosGuardrailConfig)


# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Cosmos Predict2 Text2Image 2B
# Cosmos Predict2 Text2Image 2B
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_TEXT2IMAGE_NET_2B = L(MiniTrainDIT)(
PREDICT2_TEXT2IMAGE_NET_2B = L(MiniTrainDIT)(
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
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mlp_ratio=4.0,
    mlp_ratio=4.0,
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# cross attention settings
    # cross attention settings
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：crossattn_emb_channels=1024,
    crossattn_emb_channels=1024,
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# positional embedding settings
    # positional embedding settings
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pos_emb_cls="rope3d",
    pos_emb_cls="rope3d",
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pos_emb_learnable=True,
    pos_emb_learnable=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pos_emb_interpolation="crop",
    pos_emb_interpolation="crop",
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_fps=1,
    min_fps=1,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_fps=30,
    max_fps=30,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_adaln_lora=True,
    use_adaln_lora=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：adaln_lora_dim=256,
    adaln_lora_dim=256,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rope_h_extrapolation_ratio=4.0,
    rope_h_extrapolation_ratio=4.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rope_w_extrapolation_ratio=4.0,
    rope_w_extrapolation_ratio=4.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rope_t_extrapolation_ratio=1.0,
    rope_t_extrapolation_ratio=1.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extra_per_block_abs_pos_emb=False,
    extra_per_block_abs_pos_emb=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extra_h_extrapolation_ratio=1.0,
    extra_h_extrapolation_ratio=1.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extra_w_extrapolation_ratio=1.0,
    extra_w_extrapolation_ratio=1.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extra_t_extrapolation_ratio=1.0,
    extra_t_extrapolation_ratio=1.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rope_enable_fps_modulation=False,
    rope_enable_fps_modulation=False,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_TEXT2IMAGE_PIPELINE_2B = Text2ImagePipelineConfig(
PREDICT2_TEXT2IMAGE_PIPELINE_2B = Text2ImagePipelineConfig(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：adjust_video_noise=True,
    adjust_video_noise=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：conditioner=L(VideoConditioner)(
    conditioner=L(VideoConditioner)(
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
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net=PREDICT2_TEXT2IMAGE_NET_2B,
    net=PREDICT2_TEXT2IMAGE_NET_2B,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：precision="bfloat16",
    precision="bfloat16",
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rectified_flow_t_scaling_factor=1.0,
    rectified_flow_t_scaling_factor=1.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resize_online=True,
    resize_online=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resolution="1024",
    resolution="1024",
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
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：load_mean_std=False,
        load_mean_std=False,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="tokenizer",
        name="tokenizer",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：vae_pth="checkpoints/nvidia/Cosmos-Predict2-2B-Text2Image/tokenizer/tokenizer.pth",
        vae_pth="checkpoints/nvidia/Cosmos-Predict2-2B-Text2Image/tokenizer/tokenizer.pth",
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

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Cosmos Predict2 Text2Image 14B
# Cosmos Predict2 Text2Image 14B
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_TEXT2IMAGE_NET_14B = L(MiniTrainDIT)(
PREDICT2_TEXT2IMAGE_NET_14B = L(MiniTrainDIT)(
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
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mlp_ratio=4.0,
    mlp_ratio=4.0,
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# cross attention settings
    # cross attention settings
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：crossattn_emb_channels=1024,
    crossattn_emb_channels=1024,
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# positional embedding settings
    # positional embedding settings
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pos_emb_cls="rope3d",
    pos_emb_cls="rope3d",
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pos_emb_learnable=True,
    pos_emb_learnable=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pos_emb_interpolation="crop",
    pos_emb_interpolation="crop",
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_fps=1,
    min_fps=1,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_fps=30,
    max_fps=30,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_adaln_lora=True,
    use_adaln_lora=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：adaln_lora_dim=256,
    adaln_lora_dim=256,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rope_h_extrapolation_ratio=4.0,
    rope_h_extrapolation_ratio=4.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rope_w_extrapolation_ratio=4.0,
    rope_w_extrapolation_ratio=4.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rope_t_extrapolation_ratio=1.0,
    rope_t_extrapolation_ratio=1.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extra_per_block_abs_pos_emb=False,
    extra_per_block_abs_pos_emb=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extra_h_extrapolation_ratio=1.0,
    extra_h_extrapolation_ratio=1.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extra_w_extrapolation_ratio=1.0,
    extra_w_extrapolation_ratio=1.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extra_t_extrapolation_ratio=1.0,
    extra_t_extrapolation_ratio=1.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rope_enable_fps_modulation=False,
    rope_enable_fps_modulation=False,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_TEXT2IMAGE_PIPELINE_14B = Text2ImagePipelineConfig(
PREDICT2_TEXT2IMAGE_PIPELINE_14B = Text2ImagePipelineConfig(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：adjust_video_noise=True,
    adjust_video_noise=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：conditioner=L(VideoConditioner)(
    conditioner=L(VideoConditioner)(
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
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net=PREDICT2_TEXT2IMAGE_NET_14B,
    net=PREDICT2_TEXT2IMAGE_NET_14B,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：precision="bfloat16",
    precision="bfloat16",
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rectified_flow_t_scaling_factor=1.0,
    rectified_flow_t_scaling_factor=1.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resize_online=True,
    resize_online=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resolution="1024",
    resolution="1024",
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
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：load_mean_std=False,
        load_mean_std=False,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="tokenizer",
        name="tokenizer",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：vae_pth="checkpoints/nvidia/Cosmos-Predict2-14B-Text2Image/tokenizer/tokenizer.pth",
        vae_pth="checkpoints/nvidia/Cosmos-Predict2-14B-Text2Image/tokenizer/tokenizer.pth",
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
