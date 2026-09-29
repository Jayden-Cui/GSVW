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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.datasets.dataset_provider import get_image_dataset, get_video_dataset
from videoworld2.datasets.dataset_provider import get_image_dataset, get_video_dataset
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.datasets.joint_dataloader import IterativeJointDataLoader
from videoworld2.datasets.joint_dataloader import IterativeJointDataLoader
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.datasets.webdataset.dataloader import DataLoader as _DataLoader
from imaginaire.datasets.webdataset.dataloader import DataLoader as _DataLoader


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_image_dataloader(dataset_name: str):
def get_image_dataloader(dataset_name: str):
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return _DataLoader(
    return _DataLoader(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset=get_image_dataset(
        dataset=get_image_dataset(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset_name=dataset_name,
            dataset_name=dataset_name,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resolution="480",
            resolution="480",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_train=True,
            is_train=True,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_workers=8,
        num_workers=8,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prefetch_factor=4,
        prefetch_factor=4,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch_size=2,
        batch_size=2,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sampler=None,
        sampler=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：persistent_workers=False,
        persistent_workers=False,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pin_memory=True,
        pin_memory=True,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_video_dataloader(dataset_name: str):
def get_video_dataloader(dataset_name: str):
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return _DataLoader(
    return _DataLoader(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset=get_video_dataset(
        dataset=get_video_dataset(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset_name=dataset_name,
            dataset_name=dataset_name,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_decoder_name="video_naive_bytes",
            video_decoder_name="video_naive_bytes",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：augmentor_name="video_basic_augmentor_v2",
            augmentor_name="video_basic_augmentor_v2",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resolution="480",
            resolution="480",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_train=True,
            is_train=True,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：chunk_size=256,
            chunk_size=256,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：embedding_type="umt5_xxl",
            embedding_type="umt5_xxl",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_video_frames=81,
            num_video_frames=81,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_fps_thres=3,
            min_fps_thres=3,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_fps_thres=60,
            max_fps_thres=60,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch_size=1,
        batch_size=1,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_workers=8,
        num_workers=8,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prefetch_factor=2,
        prefetch_factor=2,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sampler=None,
        sampler=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：persistent_workers=False,
        persistent_workers=False,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pin_memory=True,
        pin_memory=True,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def joint_image_video_dataloader(image_dataset_name: str, video_dataset_name: str):
def joint_image_video_dataloader(image_dataset_name: str, video_dataset_name: str):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：image_dataloader = get_image_dataloader(dataset_name=image_dataset_name)
    image_dataloader = get_image_dataloader(dataset_name=image_dataset_name)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_dataloader = get_video_dataloader(dataset_name=video_dataset_name)
    video_dataloader = get_video_dataloader(dataset_name=video_dataset_name)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return IterativeJointDataLoader(
    return IterativeJointDataLoader(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataloaders={
        dataloaders={
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："image_data": {
            "image_data": {
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："dataloader": image_dataloader,
                "dataloader": image_dataloader,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："ratio": 1,
                "ratio": 1,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：},
            },
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："video_data": {
            "video_data": {
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："dataloader": video_dataloader,
                "dataloader": video_dataloader,
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："ratio": 1,
                "ratio": 1,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：},
            },
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class WebDataLoader(_DataLoader):
class WebDataLoader(_DataLoader):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：image_dataset_name: str = None,
        image_dataset_name: str = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video_dataset_name: str = None,
        video_dataset_name: str = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dataloader_type: str = "joint",
        dataloader_type: str = "joint",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：检查运行时假设是否成立；代码：assert dataloader_type == "video", "Currently supports video-only training."
        assert dataloader_type == "video", "Currently supports video-only training."

        # 中文说明：根据条件选择执行分支；代码：if dataloader_type == "image":
        if dataloader_type == "image":
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dataloader = get_image_dataloader(dataset_name=image_dataset_name)
            self.dataloader = get_image_dataloader(dataset_name=image_dataset_name)
        # 中文说明：根据条件选择执行分支；代码：elif dataloader_type == "video":
        elif dataloader_type == "video":
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dataloader = get_video_dataloader(dataset_name=video_dataset_name)
            self.dataloader = get_video_dataloader(dataset_name=video_dataset_name)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dataloader = joint_image_video_dataloader(
            self.dataloader = joint_image_video_dataloader(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：image_dataset_name=image_dataset_name, video_dataset_name=video_dataset_name
                image_dataset_name=image_dataset_name, video_dataset_name=video_dataset_name
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dataloader_iter = iter(self.dataloader)
        self.dataloader_iter = iter(self.dataloader)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __len__(self):
    def __len__(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return len(self.dataloader)
        return len(self.dataloader)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __iter__(self):
    def __iter__(self):
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for data_dict in self.dataloader_iter:
        for data_dict in self.dataloader_iter:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Pack the data in the format we need
            # Pack the data in the format we need

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_data = dict()
            out_data = dict()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_data["first_frame"] = data_dict["video"][:, :, 0, :, :].permute(0, 2, 3, 1)
            out_data["first_frame"] = data_dict["video"][:, :, 0, :, :].permute(0, 2, 3, 1)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_data["video"] = data_dict["video"].to(torch.float32) / 255.0
            out_data["video"] = data_dict["video"].to(torch.float32) / 255.0
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_data["video"] = out_data["video"] * 2 - 1
            out_data["video"] = out_data["video"] * 2 - 1
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_data["text"] = data_dict["ai_caption"]
            out_data["text"] = data_dict["ai_caption"]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_data["path"] = data_dict["__url__"]
            out_data["path"] = data_dict["__url__"]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_data["prompt_emb"] = {"context": data_dict["t5_text_embeddings"]}
            out_data["prompt_emb"] = {"context": data_dict["t5_text_embeddings"]}
            # 中文说明：从生成器逐步产生本行指定的值；代码：yield out_data
            yield out_data
