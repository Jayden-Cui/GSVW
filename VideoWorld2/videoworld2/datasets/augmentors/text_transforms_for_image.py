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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import random
import random
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Optional
from typing import Optional

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.datasets.webdataset.augmentors.augmentor import Augmentor
from imaginaire.datasets.webdataset.augmentors.augmentor import Augmentor
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# For the qwen captions, we have 3 variants: short, medium, long
# For the qwen captions, we have 3 variants: short, medium, long
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# In addition, for synthetic data, we create prompt embeddings as well.
# In addition, for synthetic data, we create prompt embeddings as well.
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# There is quite a bit of entropy in the way prompt data is saved.
# There is quite a bit of entropy in the way prompt data is saved.
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Captions are saved as "prompts", while the corresponding embeddings are saved as "original_...
# Captions are saved as "prompts", while the corresponding embeddings are saved as "original_prompt"
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# This part will be cleaned after synthetic data is cleaned to be in the same format as real ...
# This part will be cleaned after synthetic data is cleaned to be in the same format as real data.
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_AVAILABLE_QWEN_CAPTIONS = ["qwen2p5_7b_short", "qwen2p5_7b_medium", "qwen2p5_7b_long"]
_AVAILABLE_QWEN_CAPTIONS = ["qwen2p5_7b_short", "qwen2p5_7b_medium", "qwen2p5_7b_long"]
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_CAPTION_EMBEDDING_MAPPING = {
_CAPTION_EMBEDDING_MAPPING = {
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："qwen2p5_7b_short": "qwen2p5_7b_short",
    "qwen2p5_7b_short": "qwen2p5_7b_short",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："qwen2p5_7b_medium": "qwen2p5_7b_medium",
    "qwen2p5_7b_medium": "qwen2p5_7b_medium",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："qwen2p5_7b_long": "qwen2p5_7b_long",
    "qwen2p5_7b_long": "qwen2p5_7b_long",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："prompts": "original_prompt",
    "prompts": "original_prompt",
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
}


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def pad_and_resize(
def pad_and_resize(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：arr_np: np.ndarray, ntokens: int, is_mask_all_ones: bool = False
    arr_np: np.ndarray, ntokens: int, is_mask_all_ones: bool = False
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> tuple[torch.Tensor, torch.Tensor]:
) -> tuple[torch.Tensor, torch.Tensor]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Function for padding and resizing a numpy array.
    r"""Function for padding and resizing a numpy array.
    Args:
        arr (np.ndarray): Input array
        ntokens (int): Number of output tokens after padding
        is_mask_all_ones (bool): if true, set mask to ones
    Returns:
        arr_padded (torch.Tensor): Padded output tensor
        mask (torch.Tensor): Padding mask
    """

    # 中文说明：根据条件选择执行分支；代码：if isinstance(arr_np, np.ndarray):
    if isinstance(arr_np, np.ndarray):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：arr = torch.from_numpy(arr_np)
        arr = torch.from_numpy(arr_np)
    # 中文说明：根据条件选择执行分支；代码：elif isinstance(arr_np, torch.Tensor):
    elif isinstance(arr_np, torch.Tensor):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：arr = arr_np.clone().detach()
        arr = arr_np.clone().detach()
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError("`arr_np` should be a numpy array or torch tensor.")
        raise TypeError("`arr_np` should be a numpy array or torch tensor.")
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：embed_dim = arr.shape[1]
    embed_dim = arr.shape[1]

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：arr_padded = torch.zeros(ntokens, embed_dim, device=arr.device, dtype=torch.float32)
    arr_padded = torch.zeros(ntokens, embed_dim, device=arr.device, dtype=torch.float32)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# If the input text is larger than num_text_tokens, clip it.
    # If the input text is larger than num_text_tokens, clip it.
    # 中文说明：根据条件选择执行分支；代码：if arr.shape[0] > ntokens:
    if arr.shape[0] > ntokens:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：arr = arr[0:ntokens]
        arr = arr[0:ntokens]

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mask = torch.LongTensor(ntokens).zero_()
    mask = torch.LongTensor(ntokens).zero_()
    # 中文说明：根据条件选择执行分支；代码：if len(arr.shape) > 1:
    if len(arr.shape) > 1:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：mask[0 : arr.shape[0]] = 1
        mask[0 : arr.shape[0]] = 1

    # 中文说明：根据条件选择执行分支；代码：if len(arr.shape) > 1:
    if len(arr.shape) > 1:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：arr_padded[0 : arr.shape[0]] = arr
        arr_padded[0 : arr.shape[0]] = arr

    # 中文说明：根据条件选择执行分支；代码：if is_mask_all_ones:
    if is_mask_all_ones:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：mask.fill_(1)
        mask.fill_(1)

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return arr_padded, mask
    return arr_padded, mask


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class TextTransformForImage(Augmentor):
class TextTransformForImage(Augmentor):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, input_keys: list, output_keys: Optional[list] = None, args: Optional[dict]...
    def __init__(self, input_keys: list, output_keys: Optional[list] = None, args: Optional[dict] = None) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(input_keys, output_keys, args)
        super().__init__(input_keys, output_keys, args)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, data_dict: dict) -> dict:
    def __call__(self, data_dict: dict) -> dict:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Performs camera transformation.
        r"""Performs camera transformation.

        Args:
            data_dict (dict): Input data dict
        Returns:
            data_dict (dict): Output dict with camera attributes added
        """

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：caption_type = self.args["caption_type"]
        caption_type = self.args["caption_type"]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：embedding_key_in_dict = _CAPTION_EMBEDDING_KEY_MAPPING_IMAGES[caption_type]
        embedding_key_in_dict = _CAPTION_EMBEDDING_KEY_MAPPING_IMAGES[caption_type]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：embedding_type = self.args["embedding_type"]
        embedding_type = self.args["embedding_type"]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：embedding_input_key_prefix = "" if embedding_type == "t5_xxl" else "umt5_"
        embedding_input_key_prefix = "" if embedding_type == "t5_xxl" else "umt5_"

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：captions_key, embeddings_key = (
        captions_key, embeddings_key = (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"captions_{caption_type}",
            f"captions_{caption_type}",
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"{embedding_input_key_prefix}embeddings_captions_{embedding_key_in_dict}",
            f"{embedding_input_key_prefix}embeddings_captions_{embedding_key_in_dict}",
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：decoded_captions_ai = data_dict[captions_key]
        decoded_captions_ai = data_dict[captions_key]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：decoded_embeddings_ai = data_dict[embeddings_key]
        decoded_embeddings_ai = data_dict[embeddings_key]

        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Hotfix: Some captions are labeled as "captions" and some are labeled as "caption"
            # Hotfix: Some captions are labeled as "captions" and some are labeled as "caption"
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# This issue needs to be fixed in the synthetic data. This is a hack and will be removed
            # This issue needs to be fixed in the synthetic data. This is a hack and will be removed
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# once the data is cleaned.
            # once the data is cleaned.
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：caption_key = "captions" if "captions" in decoded_captions_ai else "caption"
            caption_key = "captions" if "captions" in decoded_captions_ai else "caption"
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：embedding_key = "t5_xxl_fp8" if embedding_type == "t5_xxl" else "umt5_xxl"
            embedding_key = "t5_xxl_fp8" if embedding_type == "t5_xxl" else "umt5_xxl"
            # 中文说明：根据条件选择执行分支；代码：if caption_type == "qwen2p5_7b_v4":
            if caption_type == "qwen2p5_7b_v4":
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：selected_caption_type = random.choice(_AVAILABLE_QWEN_CAPTIONS)
                selected_caption_type = random.choice(_AVAILABLE_QWEN_CAPTIONS)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_dict["raw_captions"] = decoded_captions_ai[caption_key][selected_caption_type]
                data_dict["raw_captions"] = decoded_captions_ai[caption_key][selected_caption_type]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t5_embedding = decoded_embeddings_ai[selected_caption_type]["embeddings"][embedding_key]
                t5_embedding = decoded_embeddings_ai[selected_caption_type]["embeddings"][embedding_key]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_dict["selected_caption_type"] = selected_caption_type
                data_dict["selected_caption_type"] = selected_caption_type
            # 中文说明：根据条件选择执行分支；代码：elif caption_type == "prompts":
            elif caption_type == "prompts":
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_dict["raw_captions"] = decoded_captions_ai["caption"]["prompt"]
                data_dict["raw_captions"] = decoded_captions_ai["caption"]["prompt"]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t5_embedding = decoded_embeddings_ai[_CAPTION_EMBEDDING_MAPPING[caption_type]]["embeddings"][
                t5_embedding = decoded_embeddings_ai[_CAPTION_EMBEDDING_MAPPING[caption_type]]["embeddings"][
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：embedding_key
                    embedding_key
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
                ]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_dict["selected_caption_type"] = caption_type
                data_dict["selected_caption_type"] = caption_type

            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out_t5, out_t5_mask = pad_and_resize(
            out_t5, out_t5_mask = pad_and_resize(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：t5_embedding,
                t5_embedding,
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.args["t5_tokens"]["num"],
                self.args["t5_tokens"]["num"],
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_mask_all_ones=self.args["is_mask_all_ones"],
                is_mask_all_ones=self.args["is_mask_all_ones"],
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_dict["t5_text_embeddings"] = out_t5
            data_dict["t5_text_embeddings"] = out_t5
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_dict["t5_text_mask"] = out_t5_mask
            data_dict["t5_text_mask"] = out_t5_mask
        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
        except Exception as e:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(
            log.warning(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"TextTransform dataloader error: {data_dict['__url__']}, {data_dict['__key__']}\n error {e}",
                f"TextTransform dataloader error: {data_dict['__url__']}, {data_dict['__key__']}\n error {e}",
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank0_only=False,
                rank0_only=False,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return None
            return None

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del data_dict[captions_key]
        del data_dict[captions_key]
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del data_dict[embeddings_key]
        del data_dict[embeddings_key]

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return data_dict
        return data_dict
