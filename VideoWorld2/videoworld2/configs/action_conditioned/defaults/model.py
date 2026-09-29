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

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.configs.action_conditioned.config_action_conditioned import (
from videoworld2.configs.action_conditioned.config_action_conditioned import (
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ACTION_CONDITIONED_PREDICT2_VIDEO2WORLD_PIPELINE_2B,
    ACTION_CONDITIONED_PREDICT2_VIDEO2WORLD_PIPELINE_2B, 
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：LDM_CONDITIONED_PREDICT2_VIDEO2WORLD_PIPELINE_2B
    LDM_CONDITIONED_PREDICT2_VIDEO2WORLD_PIPELINE_2B
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.models.action_video2world_model import ActionConditionedPredict2Video2WorldM...
from videoworld2.models.action_video2world_model import ActionConditionedPredict2Video2WorldModel
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.models.video2world_model import Predict2ModelManagerConfig, Predict2Video2Wo...
from videoworld2.models.video2world_model import Predict2ModelManagerConfig, Predict2Video2WorldModelConfig
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import LazyCall as L
from imaginaire.lazy_config import LazyCall as L
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.configs.base.config_ldm import LDM_DEFAULT, COSMOS_TOKENIZER
from videoworld2.configs.base.config_ldm import LDM_DEFAULT, COSMOS_TOKENIZER

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ACTION_CONDITIONED_PREDICT2_V2W_2B_FSDP_CONFIG = dict(
ACTION_CONDITIONED_PREDICT2_V2W_2B_FSDP_CONFIG = dict(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trainer=dict(
    trainer=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distributed_parallelism="fsdp",
        distributed_parallelism="fsdp",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model=L(ActionConditionedPredict2Video2WorldModel)(
    model=L(ActionConditionedPredict2Video2WorldModel)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config=Predict2Video2WorldModelConfig(
        config=Predict2Video2WorldModelConfig(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe_config=ACTION_CONDITIONED_PREDICT2_VIDEO2WORLD_PIPELINE_2B,
            pipe_config=ACTION_CONDITIONED_PREDICT2_VIDEO2WORLD_PIPELINE_2B,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_manager_config=L(Predict2ModelManagerConfig)(
            model_manager_config=L(Predict2ModelManagerConfig)(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path="checkpoints/nvidia/Cosmos-Predict2-2B-Video2World/model-720p-16fps.pt",
                dit_path="checkpoints/nvidia/Cosmos-Predict2-2B-Video2World/model-720p-16fps.pt",
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text_encoder_path="", # Do not load text encoder for training.
                text_encoder_path="",  # Do not load text encoder for training.
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fsdp_shard_size=-1,
            fsdp_shard_size=-1,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_recursive_=False,
        _recursive_=False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ACTION_CONDITIONED_PREDICT2_V2W_2B_FSDP_LDM_CONFIG = dict(
ACTION_CONDITIONED_PREDICT2_V2W_2B_FSDP_LDM_CONFIG = dict(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trainer=dict(
    trainer=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distributed_parallelism="fsdp",
        distributed_parallelism="fsdp",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model=L(ActionConditionedPredict2Video2WorldModel)(
    model=L(ActionConditionedPredict2Video2WorldModel)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config=Predict2Video2WorldModelConfig(
        config=Predict2Video2WorldModelConfig(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe_config=LDM_CONDITIONED_PREDICT2_VIDEO2WORLD_PIPELINE_2B,
            pipe_config=LDM_CONDITIONED_PREDICT2_VIDEO2WORLD_PIPELINE_2B,
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


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def register_model_action_conditioned() -> None:
def register_model_action_conditioned() -> None:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cs = ConfigStore.instance()
    cs = ConfigStore.instance()
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# predict2 v2w 2b model
    # predict2 v2w 2b model
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(
    cs.store(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group="model",
        group="model",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：package="_global_",
        package="_global_",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="action_conditioned_predict2_v2w_2b_fsdp",
        name="action_conditioned_predict2_v2w_2b_fsdp",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：node=ACTION_CONDITIONED_PREDICT2_V2W_2B_FSDP_CONFIG,
        node=ACTION_CONDITIONED_PREDICT2_V2W_2B_FSDP_CONFIG,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(
    cs.store(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group="model",
        group="model",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：package="_global_",
        package="_global_",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="action_conditioned_predict2_v2w_2b_ldm_fsdp",
        name="action_conditioned_predict2_v2w_2b_ldm_fsdp",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：node=ACTION_CONDITIONED_PREDICT2_V2W_2B_FSDP_LDM_CONFIG,
        node=ACTION_CONDITIONED_PREDICT2_V2W_2B_FSDP_LDM_CONFIG,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
