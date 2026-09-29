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

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.conditioner import BooleanFlag, ReMapkey, TextAttr
from videoworld2.conditioner import BooleanFlag, ReMapkey, TextAttr
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.configs.action_conditioned.defaults.conditioner import ActionConditionedCond...
from videoworld2.configs.action_conditioned.defaults.conditioner import ActionConditionedConditioner
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.configs.base.config_video2world import (
from videoworld2.configs.base.config_video2world import (
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ConditioningStrategy,
    ConditioningStrategy,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CosmosGuardrailConfig,
    CosmosGuardrailConfig,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：CosmosReason1Config,
    CosmosReason1Config,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：SolverTimestampConfig,
    SolverTimestampConfig,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：Video2WorldPipelineConfig,
    Video2WorldPipelineConfig,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.configs.base.defaults.ema import EMAConfig
from videoworld2.configs.base.defaults.ema import EMAConfig
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.models.action_video2world_dit import ActionConditionedMinimalV1LVGDiT
from videoworld2.models.action_video2world_dit import ActionConditionedMinimalV1LVGDiT
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.models.text2image_dit import SACConfig
from videoworld2.models.text2image_dit import SACConfig
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.tokenizers.tokenizer import TokenizerInterface
from videoworld2.tokenizers.tokenizer import TokenizerInterface
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.config import make_freezable
from imaginaire.config import make_freezable
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import LazyCall as L
from imaginaire.lazy_config import LazyCall as L
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import LazyDict
from imaginaire.lazy_config import LazyDict

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Cosmos Predict2 Video2World 2B
# Cosmos Predict2 Video2World 2B
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ACTION_CONDITIONED_PREDICT2_VIDEO2WORLD_NET_2B = L(ActionConditionedMinimalV1LVGDiT)(
ACTION_CONDITIONED_PREDICT2_VIDEO2WORLD_NET_2B = L(ActionConditionedMinimalV1LVGDiT)(
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
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# NOTE: add action dimension
    # NOTE: add action dimension
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：action_dim=7 * 12,
    action_dim=7 * 12,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ACTION_CONDITIONED_PREDICT2_VIDEO2WORLD_PIPELINE_2B = Video2WorldPipelineConfig(
ACTION_CONDITIONED_PREDICT2_VIDEO2WORLD_PIPELINE_2B = Video2WorldPipelineConfig(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：adjust_video_noise=True,
    adjust_video_noise=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：conditioner=L(ActionConditionedConditioner)(
    conditioner=L(ActionConditionedConditioner)(
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
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# NOTE: add additional action as condition
        # NOTE: add additional action as condition
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：action=L(ReMapkey)(
        action=L(ReMapkey)(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_key="action",
            input_key="action",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_key="action",
            output_key="action",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout_rate=0.0,
            dropout_rate=0.0,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dtype=None,
            dtype=None,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：conditioning_strategy=str(ConditioningStrategy.FRAME_REPLACE),
    conditioning_strategy=str(ConditioningStrategy.FRAME_REPLACE),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_num_conditional_frames=1,
    min_num_conditional_frames=1,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_num_conditional_frames=1,
    max_num_conditional_frames=1,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net=ACTION_CONDITIONED_PREDICT2_VIDEO2WORLD_NET_2B,
    net=ACTION_CONDITIONED_PREDICT2_VIDEO2WORLD_NET_2B,
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
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_t=4,
    state_t=4,
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
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：vae_pth="checkpoints/Cosmos-Predict2-2B-Video2World/tokenizer/tokenizer.pth",
        vae_pth="checkpoints/Cosmos-Predict2-2B-Video2World/tokenizer/tokenizer.pth",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# disable prompt refiner and guardrail for action conditional
    # disable prompt refiner and guardrail for action conditional
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prompt_refiner_config=CosmosReason1Config(
    prompt_refiner_config=CosmosReason1Config(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint_dir="checkpoints/nvidia/Cosmos-Reason1-7B",
        checkpoint_dir="checkpoints/nvidia/Cosmos-Reason1-7B",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：offload_model_to_cpu=True,
        offload_model_to_cpu=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enabled=False,
        enabled=False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：guardrail_config=CosmosGuardrailConfig(
    guardrail_config=CosmosGuardrailConfig(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint_dir="checkpoints/",
        checkpoint_dir="checkpoints/",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：offload_model_to_cpu=True,
        offload_model_to_cpu=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enabled=False,
        enabled=False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)


# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：LDM_CONDITIONED_PREDICT2_VIDEO2WORLD_PIPELINE_2B = Video2WorldPipelineConfig(
LDM_CONDITIONED_PREDICT2_VIDEO2WORLD_PIPELINE_2B = Video2WorldPipelineConfig(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：adjust_video_noise=True,
    adjust_video_noise=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：conditioner=L(ActionConditionedConditioner)(
    conditioner=L(ActionConditionedConditioner)(
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
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# NOTE: add additional action as condition
        # NOTE: add additional action as condition
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：action=L(ReMapkey)(
        action=L(ReMapkey)(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_key="action",
            input_key="action",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_key="action",
            output_key="action",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout_rate=0.0,
            dropout_rate=0.0,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dtype=None,
            dtype=None,
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
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net=ACTION_CONDITIONED_PREDICT2_VIDEO2WORLD_NET_2B,
    net=ACTION_CONDITIONED_PREDICT2_VIDEO2WORLD_NET_2B,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：precision="bfloat16",
    precision="bfloat16",
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rectified_flow_t_scaling_factor=1.0,
    rectified_flow_t_scaling_factor=1.0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resize_online=True,
    resize_online=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resolution="480",
    resolution="480",
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
