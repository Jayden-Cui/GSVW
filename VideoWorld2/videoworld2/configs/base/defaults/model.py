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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from hydra.core.config_store import ConfigStore
from hydra.core.config_store import ConfigStore

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.configs.base.config_video2world import (
from videoworld2.configs.base.config_video2world import (
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：PREDICT2_VIDEO2WORLD_PIPELINE_2B, # 720p, 16fps
    PREDICT2_VIDEO2WORLD_PIPELINE_2B,  # 720p, 16fps
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：PREDICT2_VIDEO2WORLD_PIPELINE_2B_480P_10FPS,
    PREDICT2_VIDEO2WORLD_PIPELINE_2B_480P_10FPS,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：PREDICT2_VIDEO2WORLD_PIPELINE_2B_480P_16FPS,
    PREDICT2_VIDEO2WORLD_PIPELINE_2B_480P_16FPS,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：PREDICT2_VIDEO2WORLD_PIPELINE_2B_720P_10FPS,
    PREDICT2_VIDEO2WORLD_PIPELINE_2B_720P_10FPS,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：PREDICT2_VIDEO2WORLD_PIPELINE_2B_720P_16FPS,
    PREDICT2_VIDEO2WORLD_PIPELINE_2B_720P_16FPS,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：PREDICT2_VIDEO2WORLD_PIPELINE_14B, # 720p, 16fps
    PREDICT2_VIDEO2WORLD_PIPELINE_14B,  # 720p, 16fps
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：PREDICT2_VIDEO2WORLD_PIPELINE_14B_480P_10FPS,
    PREDICT2_VIDEO2WORLD_PIPELINE_14B_480P_10FPS,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：PREDICT2_VIDEO2WORLD_PIPELINE_14B_480P_16FPS,
    PREDICT2_VIDEO2WORLD_PIPELINE_14B_480P_16FPS,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：PREDICT2_VIDEO2WORLD_PIPELINE_14B_720P_10FPS,
    PREDICT2_VIDEO2WORLD_PIPELINE_14B_720P_10FPS,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：PREDICT2_VIDEO2WORLD_PIPELINE_14B_720P_16FPS,
    PREDICT2_VIDEO2WORLD_PIPELINE_14B_720P_16FPS,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：PREDICT2_VIDEO2WORLD_PIPELINE_CTRL_2B_480P_16FPS,
    PREDICT2_VIDEO2WORLD_PIPELINE_CTRL_2B_480P_16FPS,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：PREDICT2_VIDEO2WORLD_PIPELINE_CTRL_2B_480P_16FPS_INFER
    PREDICT2_VIDEO2WORLD_PIPELINE_CTRL_2B_480P_16FPS_INFER
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.configs.base.config_ldm import LDM_DEFAULT, COSMOS_TOKENIZER
from videoworld2.configs.base.config_ldm import LDM_DEFAULT, COSMOS_TOKENIZER

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.models.video2world_model import (
from videoworld2.models.video2world_model import (
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：Predict2ModelManagerConfig,
    Predict2ModelManagerConfig,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：Predict2Video2WorldModel,
    Predict2Video2WorldModel,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：Predict2Video2WorldModelConfig,
    Predict2Video2WorldModelConfig,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：Predict2Video2WorldModelWithCtrl,
    Predict2Video2WorldModelWithCtrl,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：Predict2Video2WorldModelWithCtrlConfig
    Predict2Video2WorldModelWithCtrlConfig
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import LazyCall as L
from imaginaire.lazy_config import LazyCall as L



# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# default 2b model config for predict2 video2world (720p, 16fps)
# default 2b model config for predict2 video2world (720p, 16fps)
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_FSDP_2B = dict(
PREDICT2_VIDEO2WORLD_FSDP_2B = dict(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trainer=dict(
    trainer=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distributed_parallelism="fsdp",
        distributed_parallelism="fsdp",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model=L(Predict2Video2WorldModel)(
    model=L(Predict2Video2WorldModel)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config=Predict2Video2WorldModelConfig(
        config=Predict2Video2WorldModelConfig(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe_config=PREDICT2_VIDEO2WORLD_PIPELINE_2B,
            pipe_config=PREDICT2_VIDEO2WORLD_PIPELINE_2B,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_manager_config=L(Predict2ModelManagerConfig)(
            model_manager_config=L(Predict2ModelManagerConfig)(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path="checkpoints/Cosmos-Predict2-2B-Video2World/model-720p-16fps.pt",
                dit_path="checkpoints/Cosmos-Predict2-2B-Video2World/model-720p-16fps.pt",
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text_encoder_path="", # Do not load text encoder for training.
                text_encoder_path="",  # Do not load text encoder for training.
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fsdp_shard_size=8,
            fsdp_shard_size=8,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：high_sigma_ratio=0.05,
            high_sigma_ratio=0.05,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_recursive_=False,
        _recursive_=False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# default 14b model config for predict2 video2world (720p, 16fps)
# default 14b model config for predict2 video2world (720p, 16fps)
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_FSDP_14B = dict(
PREDICT2_VIDEO2WORLD_FSDP_14B = dict(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trainer=dict(
    trainer=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distributed_parallelism="fsdp",
        distributed_parallelism="fsdp",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model=L(Predict2Video2WorldModel)(
    model=L(Predict2Video2WorldModel)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config=Predict2Video2WorldModelConfig(
        config=Predict2Video2WorldModelConfig(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe_config=PREDICT2_VIDEO2WORLD_PIPELINE_14B,
            pipe_config=PREDICT2_VIDEO2WORLD_PIPELINE_14B,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_manager_config=L(Predict2ModelManagerConfig)(
            model_manager_config=L(Predict2ModelManagerConfig)(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path="checkpoints/Cosmos-Predict2-14B-Video2World/model-720p-16fps.pt",
                dit_path="checkpoints/Cosmos-Predict2-14B-Video2World/model-720p-16fps.pt",
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text_encoder_path="", # Do not load text encoder for training.
                text_encoder_path="",  # Do not load text encoder for training.
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fsdp_shard_size=32,
            fsdp_shard_size=32,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：high_sigma_ratio=0.05,
            high_sigma_ratio=0.05,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_recursive_=False,
        _recursive_=False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 2b model configs for predict2 video2world with different resolutions and fps
# 2b model configs for predict2 video2world with different resolutions and fps
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_FSDP_2B_480P_10FPS = dict(
PREDICT2_VIDEO2WORLD_FSDP_2B_480P_10FPS = dict(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trainer=dict(
    trainer=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distributed_parallelism="fsdp",
        distributed_parallelism="fsdp",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model=L(Predict2Video2WorldModel)(
    model=L(Predict2Video2WorldModel)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config=Predict2Video2WorldModelConfig(
        config=Predict2Video2WorldModelConfig(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe_config=PREDICT2_VIDEO2WORLD_PIPELINE_2B_480P_10FPS,
            pipe_config=PREDICT2_VIDEO2WORLD_PIPELINE_2B_480P_10FPS,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_manager_config=L(Predict2ModelManagerConfig)(
            model_manager_config=L(Predict2ModelManagerConfig)(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path="checkpoints/Cosmos-Predict2-2B-Video2World/model-480p-10fps.pt",
                dit_path="checkpoints/Cosmos-Predict2-2B-Video2World/model-480p-10fps.pt",
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text_encoder_path="", # Do not load text encoder for training.
                text_encoder_path="",  # Do not load text encoder for training.
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fsdp_shard_size=8,
            fsdp_shard_size=8,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：high_sigma_ratio=0.05,
            high_sigma_ratio=0.05,
            
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_recursive_=False,
        _recursive_=False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_LDM_FSDP_2B_480P_16FPS = dict(
PREDICT2_VIDEO2WORLD_LDM_FSDP_2B_480P_16FPS = dict(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trainer=dict(
    trainer=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distributed_parallelism="fsdp",
        distributed_parallelism="fsdp",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model=L(Predict2Video2WorldModel)(
    model=L(Predict2Video2WorldModel)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config=Predict2Video2WorldModelConfig(
        config=Predict2Video2WorldModelConfig(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe_config=PREDICT2_VIDEO2WORLD_PIPELINE_2B_480P_16FPS,
            pipe_config=PREDICT2_VIDEO2WORLD_PIPELINE_2B_480P_16FPS,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_manager_config=L(Predict2ModelManagerConfig)(
            model_manager_config=L(Predict2ModelManagerConfig)(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path="checkpoints/Cosmos-Predict2-2B-Video2World/model-480p-16fps.pt",
                dit_path="checkpoints/Cosmos-Predict2-2B-Video2World/model-480p-16fps.pt",
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text_encoder_path="", # Do not load text encoder for training.
                text_encoder_path="",  # Do not load text encoder for training.
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fsdp_shard_size=8,
            fsdp_shard_size=8,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：high_sigma_ratio=0.05,
            high_sigma_ratio=0.05,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ldm_config=LDM_DEFAULT,
            ldm_config=LDM_DEFAULT,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_recursive_=False,
        _recursive_=False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_CTRL_LDM_FSDP_2B_480P_16FPS = dict(
PREDICT2_VIDEO2WORLD_CTRL_LDM_FSDP_2B_480P_16FPS = dict(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trainer=dict(
    trainer=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distributed_parallelism="fsdp",
        distributed_parallelism="fsdp",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model=L(Predict2Video2WorldModelWithCtrl)(
    model=L(Predict2Video2WorldModelWithCtrl)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config=Predict2Video2WorldModelWithCtrlConfig(
        config=Predict2Video2WorldModelWithCtrlConfig(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe_config=PREDICT2_VIDEO2WORLD_PIPELINE_CTRL_2B_480P_16FPS,
            pipe_config=PREDICT2_VIDEO2WORLD_PIPELINE_CTRL_2B_480P_16FPS,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe_type="Video2WorldPipelineWithCtrl",
            pipe_type="Video2WorldPipelineWithCtrl",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_manager_config=L(Predict2ModelManagerConfig)(
            model_manager_config=L(Predict2ModelManagerConfig)(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path="checkpoints/Cosmos-Predict2-2B-Video2World/model-480p-16fps-ctrl.pt",
                dit_path="checkpoints/Cosmos-Predict2-2B-Video2World/model-480p-16fps-ctrl.pt",
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text_encoder_path="", # Do not load text encoder for training.
                text_encoder_path="",  # Do not load text encoder for training.
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fsdp_shard_size=8,
            fsdp_shard_size=8,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：high_sigma_ratio=0.05,
            high_sigma_ratio=0.05,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ldm_config=LDM_DEFAULT,
            ldm_config=LDM_DEFAULT,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_recursive_=False,
        _recursive_=False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_CTRL_LDM_FSDP_2B_480P_16FPS_INFER = dict(
PREDICT2_VIDEO2WORLD_CTRL_LDM_FSDP_2B_480P_16FPS_INFER = dict(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trainer=dict(
    trainer=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distributed_parallelism="fsdp",
        distributed_parallelism="fsdp",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model=L(Predict2Video2WorldModelWithCtrl)(
    model=L(Predict2Video2WorldModelWithCtrl)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config=Predict2Video2WorldModelWithCtrlConfig(
        config=Predict2Video2WorldModelWithCtrlConfig(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe_config=PREDICT2_VIDEO2WORLD_PIPELINE_CTRL_2B_480P_16FPS_INFER,
            pipe_config=PREDICT2_VIDEO2WORLD_PIPELINE_CTRL_2B_480P_16FPS_INFER,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe_type="Video2WorldPipelineWithCtrl",
            pipe_type="Video2WorldPipelineWithCtrl",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_manager_config=L(Predict2ModelManagerConfig)(
            model_manager_config=L(Predict2ModelManagerConfig)(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path="checkpoints/VideoWorld2_dLDM_2B/VideoWorld2_dLDM_DiT.pt",
                dit_path="checkpoints/VideoWorld2_dLDM_2B/VideoWorld2_dLDM_DiT.pt",
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text_encoder_path="", # Do not load text encoder for training.
                text_encoder_path="",  # Do not load text encoder for training.
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fsdp_shard_size=8,
            fsdp_shard_size=8,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：high_sigma_ratio=0.05,
            high_sigma_ratio=0.05,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ldm_config=LDM_DEFAULT,
            ldm_config=LDM_DEFAULT,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_recursive_=False,
        _recursive_=False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_COSMOS_TOKENIZER_FSDP_2B_480P_16FPS = dict(
PREDICT2_VIDEO2WORLD_COSMOS_TOKENIZER_FSDP_2B_480P_16FPS = dict(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trainer=dict(
    trainer=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distributed_parallelism="fsdp",
        distributed_parallelism="fsdp",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model=L(Predict2Video2WorldModel)(
    model=L(Predict2Video2WorldModel)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config=Predict2Video2WorldModelConfig(
        config=Predict2Video2WorldModelConfig(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe_config=PREDICT2_VIDEO2WORLD_PIPELINE_2B_480P_16FPS,
            pipe_config=PREDICT2_VIDEO2WORLD_PIPELINE_2B_480P_16FPS,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_manager_config=L(Predict2ModelManagerConfig)(
            model_manager_config=L(Predict2ModelManagerConfig)(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path="checkpoints/Cosmos-Predict2-2B-Video2World/model-480p-16fps.pt",
                dit_path="checkpoints/Cosmos-Predict2-2B-Video2World/model-480p-16fps.pt",
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text_encoder_path="", # Do not load text encoder for training.
                text_encoder_path="",  # Do not load text encoder for training.
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fsdp_shard_size=8,
            fsdp_shard_size=8,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：high_sigma_ratio=0.05,
            high_sigma_ratio=0.05,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ldm_config=COSMOS_TOKENIZER,
            ldm_config=COSMOS_TOKENIZER,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_recursive_=False,
        _recursive_=False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_FSDP_2B_480P_16FPS = dict(
PREDICT2_VIDEO2WORLD_FSDP_2B_480P_16FPS = dict(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trainer=dict(
    trainer=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distributed_parallelism="fsdp",
        distributed_parallelism="fsdp",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model=L(Predict2Video2WorldModel)(
    model=L(Predict2Video2WorldModel)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config=Predict2Video2WorldModelConfig(
        config=Predict2Video2WorldModelConfig(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe_config=PREDICT2_VIDEO2WORLD_PIPELINE_2B_480P_16FPS,
            pipe_config=PREDICT2_VIDEO2WORLD_PIPELINE_2B_480P_16FPS,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_manager_config=L(Predict2ModelManagerConfig)(
            model_manager_config=L(Predict2ModelManagerConfig)(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path="checkpoints/Cosmos-Predict2-2B-Video2World/model-480p-16fps.pt",
                dit_path="checkpoints/Cosmos-Predict2-2B-Video2World/model-480p-16fps.pt",
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text_encoder_path="", # Do not load text encoder for training.
                text_encoder_path="",  # Do not load text encoder for training.
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fsdp_shard_size=8,
            fsdp_shard_size=8,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：high_sigma_ratio=0.05,
            high_sigma_ratio=0.05,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_recursive_=False,
        _recursive_=False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_FSDP_2B_720P_10FPS = dict(
PREDICT2_VIDEO2WORLD_FSDP_2B_720P_10FPS = dict(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trainer=dict(
    trainer=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distributed_parallelism="fsdp",
        distributed_parallelism="fsdp",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model=L(Predict2Video2WorldModel)(
    model=L(Predict2Video2WorldModel)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config=Predict2Video2WorldModelConfig(
        config=Predict2Video2WorldModelConfig(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe_config=PREDICT2_VIDEO2WORLD_PIPELINE_2B_720P_10FPS,
            pipe_config=PREDICT2_VIDEO2WORLD_PIPELINE_2B_720P_10FPS,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_manager_config=L(Predict2ModelManagerConfig)(
            model_manager_config=L(Predict2ModelManagerConfig)(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path="checkpoints/Cosmos-Predict2-2B-Video2World/model-720p-10fps.pt",
                dit_path="checkpoints/Cosmos-Predict2-2B-Video2World/model-720p-10fps.pt",
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text_encoder_path="", # Do not load text encoder for training.
                text_encoder_path="",  # Do not load text encoder for training.
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fsdp_shard_size=8,
            fsdp_shard_size=8,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：high_sigma_ratio=0.05,
            high_sigma_ratio=0.05,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_recursive_=False,
        _recursive_=False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_FSDP_2B_720P_16FPS = dict(
PREDICT2_VIDEO2WORLD_FSDP_2B_720P_16FPS = dict(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trainer=dict(
    trainer=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distributed_parallelism="fsdp",
        distributed_parallelism="fsdp",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model=L(Predict2Video2WorldModel)(
    model=L(Predict2Video2WorldModel)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config=Predict2Video2WorldModelConfig(
        config=Predict2Video2WorldModelConfig(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe_config=PREDICT2_VIDEO2WORLD_PIPELINE_2B_720P_16FPS,
            pipe_config=PREDICT2_VIDEO2WORLD_PIPELINE_2B_720P_16FPS,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_manager_config=L(Predict2ModelManagerConfig)(
            model_manager_config=L(Predict2ModelManagerConfig)(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path="checkpoints/Cosmos-Predict2-2B-Video2World/model-720p-16fps.pt",
                dit_path="checkpoints/Cosmos-Predict2-2B-Video2World/model-720p-16fps.pt",
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text_encoder_path="", # Do not load text encoder for training.
                text_encoder_path="",  # Do not load text encoder for training.
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fsdp_shard_size=8,
            fsdp_shard_size=8,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：high_sigma_ratio=0.05,
            high_sigma_ratio=0.05,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_recursive_=False,
        _recursive_=False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 14b model configs for predict2 video2world with different resolutions and fps
# 14b model configs for predict2 video2world with different resolutions and fps
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_FSDP_14B_480P_10FPS = dict(
PREDICT2_VIDEO2WORLD_FSDP_14B_480P_10FPS = dict(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trainer=dict(
    trainer=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distributed_parallelism="fsdp",
        distributed_parallelism="fsdp",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model=L(Predict2Video2WorldModel)(
    model=L(Predict2Video2WorldModel)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config=Predict2Video2WorldModelConfig(
        config=Predict2Video2WorldModelConfig(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe_config=PREDICT2_VIDEO2WORLD_PIPELINE_14B_480P_10FPS,
            pipe_config=PREDICT2_VIDEO2WORLD_PIPELINE_14B_480P_10FPS,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_manager_config=L(Predict2ModelManagerConfig)(
            model_manager_config=L(Predict2ModelManagerConfig)(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path="checkpoints/Cosmos-Predict2-14B-Video2World/model-480p-10fps.pt",
                dit_path="checkpoints/Cosmos-Predict2-14B-Video2World/model-480p-10fps.pt",
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text_encoder_path="", # Do not load text encoder for training.
                text_encoder_path="",  # Do not load text encoder for training.
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fsdp_shard_size=8,
            fsdp_shard_size=8,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：high_sigma_ratio=0.05,
            high_sigma_ratio=0.05,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_recursive_=False,
        _recursive_=False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_FSDP_14B_480P_16FPS = dict(
PREDICT2_VIDEO2WORLD_FSDP_14B_480P_16FPS = dict(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trainer=dict(
    trainer=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distributed_parallelism="fsdp",
        distributed_parallelism="fsdp",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model=L(Predict2Video2WorldModel)(
    model=L(Predict2Video2WorldModel)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config=Predict2Video2WorldModelConfig(
        config=Predict2Video2WorldModelConfig(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe_config=PREDICT2_VIDEO2WORLD_PIPELINE_14B_480P_16FPS,
            pipe_config=PREDICT2_VIDEO2WORLD_PIPELINE_14B_480P_16FPS,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_manager_config=L(Predict2ModelManagerConfig)(
            model_manager_config=L(Predict2ModelManagerConfig)(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path="checkpoints/Cosmos-Predict2-14B-Video2World/model-480p-16fps.pt",
                dit_path="checkpoints/Cosmos-Predict2-14B-Video2World/model-480p-16fps.pt",
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text_encoder_path="", # Do not load text encoder for training.
                text_encoder_path="",  # Do not load text encoder for training.
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fsdp_shard_size=8,
            fsdp_shard_size=8,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：high_sigma_ratio=0.05,
            high_sigma_ratio=0.05,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_recursive_=False,
        _recursive_=False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_FSDP_14B_720P_10FPS = dict(
PREDICT2_VIDEO2WORLD_FSDP_14B_720P_10FPS = dict(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trainer=dict(
    trainer=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distributed_parallelism="fsdp",
        distributed_parallelism="fsdp",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model=L(Predict2Video2WorldModel)(
    model=L(Predict2Video2WorldModel)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config=Predict2Video2WorldModelConfig(
        config=Predict2Video2WorldModelConfig(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe_config=PREDICT2_VIDEO2WORLD_PIPELINE_14B_720P_10FPS,
            pipe_config=PREDICT2_VIDEO2WORLD_PIPELINE_14B_720P_10FPS,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_manager_config=L(Predict2ModelManagerConfig)(
            model_manager_config=L(Predict2ModelManagerConfig)(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path="checkpoints/Cosmos-Predict2-14B-Video2World/model-720p-10fps.pt",
                dit_path="checkpoints/Cosmos-Predict2-14B-Video2World/model-720p-10fps.pt",
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text_encoder_path="", # Do not load text encoder for training.
                text_encoder_path="",  # Do not load text encoder for training.
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fsdp_shard_size=8,
            fsdp_shard_size=8,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：high_sigma_ratio=0.05,
            high_sigma_ratio=0.05,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_recursive_=False,
        _recursive_=False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：PREDICT2_VIDEO2WORLD_FSDP_14B_720P_16FPS = dict(
PREDICT2_VIDEO2WORLD_FSDP_14B_720P_16FPS = dict(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trainer=dict(
    trainer=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distributed_parallelism="fsdp",
        distributed_parallelism="fsdp",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model=L(Predict2Video2WorldModel)(
    model=L(Predict2Video2WorldModel)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config=Predict2Video2WorldModelConfig(
        config=Predict2Video2WorldModelConfig(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe_config=PREDICT2_VIDEO2WORLD_PIPELINE_14B_720P_16FPS,
            pipe_config=PREDICT2_VIDEO2WORLD_PIPELINE_14B_720P_16FPS,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_manager_config=L(Predict2ModelManagerConfig)(
            model_manager_config=L(Predict2ModelManagerConfig)(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path="checkpoints/Cosmos-Predict2-14B-Video2World/model-720p-16fps.pt",
                dit_path="checkpoints/Cosmos-Predict2-14B-Video2World/model-720p-16fps.pt",
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text_encoder_path="", # Do not load text encoder for training.
                text_encoder_path="",  # Do not load text encoder for training.
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fsdp_shard_size=8,
            fsdp_shard_size=8,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：high_sigma_ratio=0.05,
            high_sigma_ratio=0.05,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_recursive_=False,
        _recursive_=False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def register_model() -> None:
def register_model() -> None:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cs = ConfigStore.instance()
    cs = ConfigStore.instance()
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# predict2 v2w 2b model (default 720p, 16fps)
    # predict2 v2w 2b model (default 720p, 16fps)
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(group="model", package="_global_", name="predict2_video2world_fsdp_2b", node=PREDICT...
    cs.store(group="model", package="_global_", name="predict2_video2world_fsdp_2b", node=PREDICT2_VIDEO2WORLD_FSDP_2B)
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# predict2 v2w 14b model (default 720p, 16fps)
    # predict2 v2w 14b model (default 720p, 16fps)
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(
    cs.store(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group="model", package="_global_", name="predict2_video2world_fsdp_14b", node=PREDICT2_VIDEO2...
        group="model", package="_global_", name="predict2_video2world_fsdp_14b", node=PREDICT2_VIDEO2WORLD_FSDP_14B
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# predict2 v2w 2b model by resolution and fps
    # predict2 v2w 2b model by resolution and fps
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(
    cs.store(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group="model",
        group="model",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：package="_global_",
        package="_global_",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="predict2_video2world_fsdp_2b_480p_10fps",
        name="predict2_video2world_fsdp_2b_480p_10fps",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：node=PREDICT2_VIDEO2WORLD_FSDP_2B_480P_10FPS,
        node=PREDICT2_VIDEO2WORLD_FSDP_2B_480P_10FPS,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(
    cs.store(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group="model",
        group="model",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：package="_global_",
        package="_global_",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="predict2_video2world_fsdp_2b_480p_16fps",
        name="predict2_video2world_fsdp_2b_480p_16fps",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：node=PREDICT2_VIDEO2WORLD_FSDP_2B_480P_16FPS,
        node=PREDICT2_VIDEO2WORLD_FSDP_2B_480P_16FPS,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(
    cs.store(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group="model",
        group="model",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：package="_global_",
        package="_global_",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="predict2_video2world_ldm_fsdp_2b_480p_16fps",
        name="predict2_video2world_ldm_fsdp_2b_480p_16fps",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：node=PREDICT2_VIDEO2WORLD_LDM_FSDP_2B_480P_16FPS,
        node=PREDICT2_VIDEO2WORLD_LDM_FSDP_2B_480P_16FPS,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(
    cs.store(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group="model",
        group="model",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：package="_global_",
        package="_global_",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="predict2_video2world_ctrl_ldm_fsdp_2b_480p_16fps_infer",
        name="predict2_video2world_ctrl_ldm_fsdp_2b_480p_16fps_infer",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：node=PREDICT2_VIDEO2WORLD_CTRL_LDM_FSDP_2B_480P_16FPS_INFER,
        node=PREDICT2_VIDEO2WORLD_CTRL_LDM_FSDP_2B_480P_16FPS_INFER,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(
    cs.store(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group="model",
        group="model",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：package="_global_",
        package="_global_",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="predict2_video2world_ctrl_ldm_fsdp_2b_480p_16fps",
        name="predict2_video2world_ctrl_ldm_fsdp_2b_480p_16fps",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：node=PREDICT2_VIDEO2WORLD_CTRL_LDM_FSDP_2B_480P_16FPS,
        node=PREDICT2_VIDEO2WORLD_CTRL_LDM_FSDP_2B_480P_16FPS,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )


    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(
    cs.store(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group="model",
        group="model",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：package="_global_",
        package="_global_",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="predict2_video2world_cosmostokenizer_fsdp_2b_480p_16fps",
        name="predict2_video2world_cosmostokenizer_fsdp_2b_480p_16fps",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：node=PREDICT2_VIDEO2WORLD_COSMOS_TOKENIZER_FSDP_2B_480P_16FPS,
        node=PREDICT2_VIDEO2WORLD_COSMOS_TOKENIZER_FSDP_2B_480P_16FPS,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(
    cs.store(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group="model",
        group="model",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：package="_global_",
        package="_global_",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="predict2_video2world_fsdp_2b_720p_10fps",
        name="predict2_video2world_fsdp_2b_720p_10fps",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：node=PREDICT2_VIDEO2WORLD_FSDP_2B_720P_10FPS,
        node=PREDICT2_VIDEO2WORLD_FSDP_2B_720P_10FPS,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(
    cs.store(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group="model",
        group="model",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：package="_global_",
        package="_global_",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="predict2_video2world_fsdp_2b_720p_16fps",
        name="predict2_video2world_fsdp_2b_720p_16fps",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：node=PREDICT2_VIDEO2WORLD_FSDP_2B_720P_16FPS,
        node=PREDICT2_VIDEO2WORLD_FSDP_2B_720P_16FPS,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# predict2 v2w 14b model by resolution and fps
    # predict2 v2w 14b model by resolution and fps
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(
    cs.store(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group="model",
        group="model",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：package="_global_",
        package="_global_",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="predict2_video2world_fsdp_14b_480p_10fps",
        name="predict2_video2world_fsdp_14b_480p_10fps",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：node=PREDICT2_VIDEO2WORLD_FSDP_14B_480P_10FPS,
        node=PREDICT2_VIDEO2WORLD_FSDP_14B_480P_10FPS,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(
    cs.store(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group="model",
        group="model",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：package="_global_",
        package="_global_",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="predict2_video2world_fsdp_14b_480p_16fps",
        name="predict2_video2world_fsdp_14b_480p_16fps",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：node=PREDICT2_VIDEO2WORLD_FSDP_14B_480P_16FPS,
        node=PREDICT2_VIDEO2WORLD_FSDP_14B_480P_16FPS,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(
    cs.store(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group="model",
        group="model",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：package="_global_",
        package="_global_",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="predict2_video2world_fsdp_14b_720p_10fps",
        name="predict2_video2world_fsdp_14b_720p_10fps",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：node=PREDICT2_VIDEO2WORLD_FSDP_14B_720P_10FPS,
        node=PREDICT2_VIDEO2WORLD_FSDP_14B_720P_10FPS,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(
    cs.store(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group="model",
        group="model",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：package="_global_",
        package="_global_",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="predict2_video2world_fsdp_14b_720p_16fps",
        name="predict2_video2world_fsdp_14b_720p_16fps",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：node=PREDICT2_VIDEO2WORLD_FSDP_14B_720P_16FPS,
        node=PREDICT2_VIDEO2WORLD_FSDP_14B_720P_16FPS,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
