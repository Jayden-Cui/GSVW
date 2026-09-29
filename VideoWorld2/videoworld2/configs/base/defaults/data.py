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

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.datasets.cached_replay_dataloader import get_cached_replay_dataloader
from videoworld2.datasets.cached_replay_dataloader import get_cached_replay_dataloader
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.datasets.data_sources.mock_data import get_image_dataset, get_video_dataset
from videoworld2.datasets.data_sources.mock_data import get_image_dataset, get_video_dataset
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.datasets.joint_dataloader import IterativeJointDataLoader
from videoworld2.datasets.joint_dataloader import IterativeJointDataLoader
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import LazyCall as L
from imaginaire.lazy_config import LazyCall as L

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_IMAGE_LOADER = L(get_cached_replay_dataloader)(
_IMAGE_LOADER = L(get_cached_replay_dataloader)(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset=L(get_image_dataset)(
    dataset=L(get_image_dataset)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resolution="480",
        resolution="480",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch_size=2,
    batch_size=2,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：shuffle=False,
    shuffle=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_workers=0,
    num_workers=0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pin_memory=True,
    pin_memory=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：webdataset=False,
    webdataset=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_replay_name="image_dataloader",
    cache_replay_name="image_dataloader",
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_VIDEO_LOADER = L(get_cached_replay_dataloader)(
_VIDEO_LOADER = L(get_cached_replay_dataloader)(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset=L(get_video_dataset)(
    dataset=L(get_video_dataset)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resolution="480",
        resolution="480",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_video_frames=93, # number of pixel frames, the number needs to agree with tokenizer encod...
        num_video_frames=93,  # number of pixel frames, the number needs to agree with tokenizer encoder since tokenizer can not handle arbitrary length
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch_size=1,
    batch_size=1,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：shuffle=False,
    shuffle=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_workers=0,
    num_workers=0,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pin_memory=True,
    pin_memory=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：webdataset=False,
    webdataset=False,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_replay_name="video_dataloader",
    cache_replay_name="video_dataloader",
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：MOCK_DATA_INTERLEAVE_CONFIG = L(IterativeJointDataLoader)(
MOCK_DATA_INTERLEAVE_CONFIG = L(IterativeJointDataLoader)(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataloaders={
    dataloaders={
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："image_data": {
        "image_data": {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："dataloader": _IMAGE_LOADER,
            "dataloader": _IMAGE_LOADER,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："ratio": 1,
            "ratio": 1,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：},
        },
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："video_data": {
        "video_data": {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："dataloader": _VIDEO_LOADER,
            "dataloader": _VIDEO_LOADER,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："ratio": 1,
            "ratio": 1,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：},
        },
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
    }
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：MOCK_DATA_IMAGE_ONLY_CONFIG = _IMAGE_LOADER
MOCK_DATA_IMAGE_ONLY_CONFIG = _IMAGE_LOADER

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：MOCK_DATA_VIDEO_ONLY_CONFIG = _VIDEO_LOADER
MOCK_DATA_VIDEO_ONLY_CONFIG = _VIDEO_LOADER


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def register_training_and_val_data():
def register_training_and_val_data():
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cs = ConfigStore()
    cs = ConfigStore()
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(group="dataloader_train", package="dataloader_train", name="mock", node=MOCK_DATA_IN...
    cs.store(group="dataloader_train", package="dataloader_train", name="mock", node=MOCK_DATA_INTERLEAVE_CONFIG)
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(group="dataloader_train", package="dataloader_train", name="mock_image", node=MOCK_D...
    cs.store(group="dataloader_train", package="dataloader_train", name="mock_image", node=MOCK_DATA_IMAGE_ONLY_CONFIG)
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(group="dataloader_train", package="dataloader_train", name="mock_video", node=MOCK_D...
    cs.store(group="dataloader_train", package="dataloader_train", name="mock_video", node=MOCK_DATA_VIDEO_ONLY_CONFIG)
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(group="dataloader_val", package="dataloader_val", name="mock", node=MOCK_DATA_INTERL...
    cs.store(group="dataloader_val", package="dataloader_val", name="mock", node=MOCK_DATA_INTERLEAVE_CONFIG)
