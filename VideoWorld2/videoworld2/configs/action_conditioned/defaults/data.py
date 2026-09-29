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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from hydra.core.config_store import ConfigStore
from hydra.core.config_store import ConfigStore
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from megatron.core import parallel_state
from megatron.core import parallel_state
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.utils.data import DataLoader, DistributedSampler
from torch.utils.data import DataLoader, DistributedSampler

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.data.action_conditioned.action_conditioned_dataset import ActionConditionedD...
from videoworld2.data.action_conditioned.action_conditioned_dataset import ActionConditionedDataset
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import LazyCall as L
from imaginaire.lazy_config import LazyCall as L

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：base_path = "./datasets/bridge/"
base_path = "./datasets/bridge/"
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：train_annotation_path = os.path.join(base_path, "annotation/train")
train_annotation_path = os.path.join(base_path, "annotation/train")
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：val_annotation_path = os.path.join(base_path, "annotation/val")
val_annotation_path = os.path.join(base_path, "annotation/val")
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：test_annotation_path = os.path.join(base_path, "annotation/test")
test_annotation_path = os.path.join(base_path, "annotation/test")


# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：bridge_train_dataset = L(ActionConditionedDataset)(
bridge_train_dataset = L(ActionConditionedDataset)(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：train_annotation_path=train_annotation_path,
    train_annotation_path=train_annotation_path,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：val_annotation_path=val_annotation_path,
    val_annotation_path=val_annotation_path,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：test_annotation_path=test_annotation_path,
    test_annotation_path=test_annotation_path,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_path=base_path,
    video_path=base_path,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sequence_interval=1,
    sequence_interval=1,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_frames=13,
    num_frames=13,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cam_ids=[0],
    cam_ids=[0],
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：accumulate_action=False,
    accumulate_action=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_size=[480, 640],
    video_size=[480, 640],
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：val_start_frame_interval=1,
    val_start_frame_interval=1,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mode="train",
    mode="train",
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：bridge_val_dataset = L(ActionConditionedDataset)(
bridge_val_dataset = L(ActionConditionedDataset)(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：train_annotation_path=train_annotation_path,
    train_annotation_path=train_annotation_path,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：val_annotation_path=val_annotation_path,
    val_annotation_path=val_annotation_path,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：test_annotation_path=test_annotation_path,
    test_annotation_path=test_annotation_path,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_path=base_path,
    video_path=base_path,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sequence_interval=1,
    sequence_interval=1,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_frames=13,
    num_frames=13,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cam_ids=[0],
    cam_ids=[0],
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：accumulate_action=False,
    accumulate_action=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_size=[480, 640],
    video_size=[480, 640],
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：val_start_frame_interval=1,
    val_start_frame_interval=1,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mode="val",
    mode="val",
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_sampler(dataset):
def get_sampler(dataset):
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return DistributedSampler(
    return DistributedSampler(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dataset,
        dataset,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_replicas=parallel_state.get_data_parallel_world_size(),
        num_replicas=parallel_state.get_data_parallel_world_size(),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank=parallel_state.get_data_parallel_rank(),
        rank=parallel_state.get_data_parallel_rank(),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：shuffle=True,
        shuffle=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：seed=0,
        seed=0,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )


# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：bridge_train_dataloader = L(DataLoader)(
bridge_train_dataloader = L(DataLoader)(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset=bridge_train_dataset,
    dataset=bridge_train_dataset,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sampler=L(get_sampler)(dataset=bridge_train_dataset),
    sampler=L(get_sampler)(dataset=bridge_train_dataset),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch_size=1,
    batch_size=1,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：drop_last=True,
    drop_last=True,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：bridge_val_dataloader = L(DataLoader)(
bridge_val_dataloader = L(DataLoader)(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset=bridge_val_dataset,
    dataset=bridge_val_dataset,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sampler=L(get_sampler)(dataset=bridge_val_dataset),
    sampler=L(get_sampler)(dataset=bridge_val_dataset),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch_size=1,
    batch_size=1,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：drop_last=True,
    drop_last=True,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def register_training_and_val_data_action_conditioned():
def register_training_and_val_data_action_conditioned():
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cs = ConfigStore.instance()
    cs = ConfigStore.instance()

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# for local dataset
    # for local dataset
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(
    cs.store(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group="dataloader_train",
        group="dataloader_train",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：package="dataloader_train",
        package="dataloader_train",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="bridge_train",
        name="bridge_train",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：node=bridge_train_dataloader,
        node=bridge_train_dataloader,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(
    cs.store(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group="dataloader_val",
        group="dataloader_val",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：package="dataloader_val",
        package="dataloader_val",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="bridge_val",
        name="bridge_val",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：node=bridge_val_dataloader,
        node=bridge_val_dataloader,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
