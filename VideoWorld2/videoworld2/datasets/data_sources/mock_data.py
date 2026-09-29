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
# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
"""
Mock data for fast testing and debugging.
"""

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from functools import partial
from functools import partial

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.datasets.utils import IMAGE_RES_SIZE_INFO, VIDEO_RES_SIZE_INFO
from videoworld2.datasets.utils import IMAGE_RES_SIZE_INFO, VIDEO_RES_SIZE_INFO
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.datasets.mock_dataset import CombinedDictDataset, LambdaDataset
from imaginaire.datasets.mock_dataset import CombinedDictDataset, LambdaDataset


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_image_dataset(
def get_image_dataset(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：resolution: str = "512",
    resolution: str = "512",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：len_t5: int = 512,
    len_t5: int = 512,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：t5_dim: int = 1024,
    t5_dim: int = 1024,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**kwargs,
    **kwargs,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：h, w = IMAGE_RES_SIZE_INFO[resolution]["9:16"]
    h, w = IMAGE_RES_SIZE_INFO[resolution]["9:16"]
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del kwargs
    del kwargs
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return CombinedDictDataset(
    return CombinedDictDataset(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**{
        **{
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："images": LambdaDataset(partial(torch.randn, size=(3, h, w))),
            "images": LambdaDataset(partial(torch.randn, size=(3, h, w))),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："t5_text_embeddings": LambdaDataset(partial(torch.randn, size=(len_t5, t5_dim))),
            "t5_text_embeddings": LambdaDataset(partial(torch.randn, size=(len_t5, t5_dim))),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："t5_text_mask": LambdaDataset(partial(torch.randint, low=0, high=2, size=(len_t5,), dtype=tor...
            "t5_text_mask": LambdaDataset(partial(torch.randint, low=0, high=2, size=(len_t5,), dtype=torch.int64)),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："fps": LambdaDataset(lambda: 1.0),
            "fps": LambdaDataset(lambda: 1.0),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："image_size": LambdaDataset(partial(torch.tensor, [h, w, h, w], dtype=torch.float32)),
            "image_size": LambdaDataset(partial(torch.tensor, [h, w, h, w], dtype=torch.float32)),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："num_frames": LambdaDataset(lambda: 1),
            "num_frames": LambdaDataset(lambda: 1),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："padding_mask": LambdaDataset(partial(torch.zeros, size=(1, h, w))),
            "padding_mask": LambdaDataset(partial(torch.zeros, size=(1, h, w))),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："dataset_name": LambdaDataset(lambda: "image_data"),
            "dataset_name": LambdaDataset(lambda: "image_data"),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："raw_captions": LambdaDataset(lambda: "placeholder"),
            "raw_captions": LambdaDataset(lambda: "placeholder"),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："__url__": LambdaDataset(lambda: "placeholder"),
            "__url__": LambdaDataset(lambda: "placeholder"),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："__key__": LambdaDataset(lambda: "placeholder"),
            "__key__": LambdaDataset(lambda: "placeholder"),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_video_dataset(
def get_video_dataset(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_video_frames: int,
    num_video_frames: int,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：resolution: str = "512",
    resolution: str = "512",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：len_t5: int = 512,
    len_t5: int = 512,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：t5_dim: int = 1024,
    t5_dim: int = 1024,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**kwargs,
    **kwargs,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del kwargs
    del kwargs
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：h, w = VIDEO_RES_SIZE_INFO[resolution]["9:16"]
    h, w = VIDEO_RES_SIZE_INFO[resolution]["9:16"]

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def video_fn():
    def video_fn():
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return torch.randint(0, 255, size=(3, num_video_frames, h, w)).to(dtype=torch.uint8)
        return torch.randint(0, 255, size=(3, num_video_frames, h, w)).to(dtype=torch.uint8)

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return CombinedDictDataset(
    return CombinedDictDataset(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**{
        **{
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："video": LambdaDataset(video_fn),
            "video": LambdaDataset(video_fn),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："t5_text_embeddings": LambdaDataset(partial(torch.randn, size=(len_t5, t5_dim))),
            "t5_text_embeddings": LambdaDataset(partial(torch.randn, size=(len_t5, t5_dim))),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："t5_text_mask": LambdaDataset(partial(torch.randint, low=0, high=2, size=(len_t5,), dtype=tor...
            "t5_text_mask": LambdaDataset(partial(torch.randint, low=0, high=2, size=(len_t5,), dtype=torch.int64)),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："fps": LambdaDataset(lambda: 24.0),
            "fps": LambdaDataset(lambda: 24.0),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："image_size": LambdaDataset(partial(torch.tensor, [h, w, h, w], dtype=torch.float32)),
            "image_size": LambdaDataset(partial(torch.tensor, [h, w, h, w], dtype=torch.float32)),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："num_frames": LambdaDataset(lambda: num_video_frames),
            "num_frames": LambdaDataset(lambda: num_video_frames),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："padding_mask": LambdaDataset(partial(torch.zeros, size=(1, h, w))),
            "padding_mask": LambdaDataset(partial(torch.zeros, size=(1, h, w))),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："ai_caption": LambdaDataset(lambda: "placeholder"),
            "ai_caption": LambdaDataset(lambda: "placeholder"),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："dataset_name": LambdaDataset(lambda: "video_data"),
            "dataset_name": LambdaDataset(lambda: "video_data"),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："chunk_index": LambdaDataset(lambda: 0),
            "chunk_index": LambdaDataset(lambda: 0),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："frame_end": LambdaDataset(lambda: 0),
            "frame_end": LambdaDataset(lambda: 0),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："frame_start": LambdaDataset(lambda: 0),
            "frame_start": LambdaDataset(lambda: 0),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："n_orig_video_frames": LambdaDataset(lambda: 0),
            "n_orig_video_frames": LambdaDataset(lambda: 0),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："__url__": LambdaDataset(lambda: "placeholder"),
            "__url__": LambdaDataset(lambda: "placeholder"),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："__key__": LambdaDataset(lambda: "placeholder"),
            "__key__": LambdaDataset(lambda: "placeholder"),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
