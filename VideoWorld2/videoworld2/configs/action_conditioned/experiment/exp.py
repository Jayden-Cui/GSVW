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

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cs = ConfigStore.instance()
cs = ConfigStore.instance()

# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
"""
torchrun --nproc_per_node=2 --master_port=12341 -m scripts.train --config=cosmos_predict2/configs/base/config.py -- experiment="action_conditional_predict2_video2world_2b_training"
"""
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：action_conditioned_predict2_video2world_2b_training = dict(
action_conditioned_predict2_video2world_2b_training = dict(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：defaults=[
    defaults=[
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"override /model": "action_conditioned_predict2_v2w_2b_fsdp"},
        {"override /model": "action_conditioned_predict2_v2w_2b_fsdp"},
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"override /optimizer": "fusedadamw"},
        {"override /optimizer": "fusedadamw"},
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"override /ckpt_type": "standard"},
        {"override /ckpt_type": "standard"},
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"override /dataloader_train": "bridge_train"},
        {"override /dataloader_train": "bridge_train"},
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："_self_",
        "_self_",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：],
    ],
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model=dict(
    model=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config=dict(
        config=dict(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fsdp_shard_size=-1,
            fsdp_shard_size=-1,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：job=dict(group="debug", name="action_conditioned_predict2_video2world_2b_training_${now:%Y-%m...
    job=dict(group="debug", name="action_conditioned_predict2_video2world_2b_training_${now:%Y-%m-%d}_${now:%H-%M-%S}"),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_parallel=dict(
    model_parallel=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：context_parallel_size=1,
        context_parallel_size=1,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataloader_train=dict(
    dataloader_train=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch_size=2,
        batch_size=2,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trainer=dict(
    trainer=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distributed_parallelism="fsdp",
        distributed_parallelism="fsdp",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)


# 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _item in [
for _item in [
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# predict2_video2world_2b
    # predict2_video2world_2b
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：action_conditioned_predict2_video2world_2b_training,
    action_conditioned_predict2_video2world_2b_training,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]:
]:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Get the experiment name from the global variable, e.g. exp01_wan_lora -> experiment_name = ...
    # Get the experiment name from the global variable, e.g. exp01_wan_lora -> experiment_name = "exp01_wan_lora"
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：experiment_name = [name.lower() for name, value in globals().items() if value is _item][0]
    experiment_name = [name.lower() for name, value in globals().items() if value is _item][0]

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(
    cs.store(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group="experiment",
        group="experiment",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：package="_global_",
        package="_global_",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name=experiment_name,
        name=experiment_name,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：node=_item,
        node=_item,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
