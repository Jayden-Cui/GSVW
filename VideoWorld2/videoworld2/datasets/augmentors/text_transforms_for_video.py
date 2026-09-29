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


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class TextTransformForVideo(Augmentor):
class TextTransformForVideo(Augmentor):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, input_keys: dict, output_keys: Optional[list] = None, args: Optional[dict]...
    def __init__(self, input_keys: dict, output_keys: Optional[list] = None, args: Optional[dict] = None) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(input_keys, output_keys, args)
        super().__init__(input_keys, output_keys, args)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# our caption is saved in json with format: {"<key>": "xxx", "<caption_windows_key1>": [{"sta...
        # our caption is saved in json with format: {"<key>": "xxx", "<caption_windows_key1>": [{"start_frame": x, "end_frame": x, "<caption_type>": xxx}, ...], "<caption_windows_key2>": [{"start_frame":...]}
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# our t5 embedding is saved in pickle with format: [{"<embedding_caption_type1>": array1, "<e...
        # our t5 embedding is saved in pickle with format: [{"<embedding_caption_type1>": array1, "<embedding_caption_type2>": array2}, ...]
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.captions_key: str = args[
        self.captions_key: str = args[
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："captions_key"
            "captions_key"
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：] # Saves the captions; this get mapped to the key in data_dict to fetch the caption field
        ]  # Saves the captions; this get mapped to the key in data_dict to fetch the caption field
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.embeddings_key: str = args[
        self.embeddings_key: str = args[
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："embeddings_key"
            "embeddings_key"
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：] # Saves the embeddings; this get mapped to the key in data_dict to fetch the embedding field
        ]  # Saves the embeddings; this get mapped to the key in data_dict to fetch the embedding field
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.caption_windows_key: str = args[
        self.caption_windows_key: str = args[
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："caption_windows_key"
            "caption_windows_key"
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：] # key to get the caption windows from the caption field
        ]  # key to get the caption windows from the caption field
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.caption_type: str = args["caption_type"] # key of caption type to fetch the caption from...
        self.caption_type: str = args["caption_type"]  # key of caption type to fetch the caption from caption windows
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.embedding_caption_type: str = args[
        self.embedding_caption_type: str = args[
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："embedding_caption_type"
            "embedding_caption_type"
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：] # key to get the embedding of a particular caption type from the embedding field
        ]  # key to get the embedding of a particular caption type from the embedding field
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.t5_tokens_num = args["t5_tokens"]["num"] # number of tokens we cap after padding
        self.t5_tokens_num = args["t5_tokens"]["num"]  # number of tokens we cap after padding
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.is_mask_all_ones = args["is_mask_all_ones"] # if true, set mask for t5 to all ones
        self.is_mask_all_ones = args["is_mask_all_ones"]  # if true, set mask for t5 to all ones

        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.caption_probs: dict[str, float] = args[
        self.caption_probs: dict[str, float] = args[
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："caption_probs"
            "caption_probs"
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：] # probabilities for user/short/medium/long captions
        ]  # probabilities for user/short/medium/long captions
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.caption_style_mapping = {
        self.caption_style_mapping = {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："long": self.caption_type,
            "long": self.caption_type,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："short": f"{self.caption_type}_short",
            "short": f"{self.caption_type}_short",
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："medium": f"{self.caption_type}_medium",
            "medium": f"{self.caption_type}_medium",
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："user": f"{self.caption_type}_user",
            "user": f"{self.caption_type}_user",
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.embedding_style_mapping = {
        self.embedding_style_mapping = {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："long": self.embedding_caption_type,
            "long": self.embedding_caption_type,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："short": f"{self.embedding_caption_type}_short",
            "short": f"{self.embedding_caption_type}_short",
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："medium": f"{self.embedding_caption_type}_medium",
            "medium": f"{self.embedding_caption_type}_medium",
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："user": f"{self.embedding_caption_type}_user",
            "user": f"{self.embedding_caption_type}_user",
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }
        # 中文说明：检查运行时假设是否成立；代码：assert (
        assert (
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.caption_probs.keys() == self.caption_style_mapping.keys() == self.embedding_style_mappin...
            self.caption_probs.keys() == self.caption_style_mapping.keys() == self.embedding_style_mapping.keys()
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), "The keys for caption_probs, caption_style_mapping, and embedding_style_mapping should match"
        ), "The keys for caption_probs, caption_style_mapping, and embedding_style_mapping should match"

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, data_dict: dict) -> dict:
    def __call__(self, data_dict: dict) -> dict:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r"""Performs text transformation.
        r"""Performs text transformation.

        Args:
            data_dict (dict): Input data dict
        Returns:
            data_dict (dict): Output dict with captions and t5 embeddings added
        """

        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：windows = data_dict[self.captions_key][self.caption_windows_key]
            windows = data_dict[self.captions_key][self.caption_windows_key]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n_windows = len(windows)
            n_windows = len(windows)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：chunk_index = data_dict["chunk_index"]
            chunk_index = data_dict["chunk_index"]

            # 中文说明：根据条件选择执行分支；代码：if chunk_index == n_windows:
            if chunk_index == n_windows:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# This will only happen when the number of captions does not match number of chunks due to re...
                # This will only happen when the number of captions does not match number of chunks due to re-transcoding the videos.
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(
                log.warning(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"TextTransform dataloader error: Found {data_dict['n_orig_video_frames']} in video but capti...
                    f"TextTransform dataloader error: Found {data_dict['n_orig_video_frames']} in video but captioning is done with videos of {windows[-1]['end_frame']} frames. This mismatch is due to video re-transcoding.",
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank0_only=False,
                    rank0_only=False,
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：chunk_index -= 1
                chunk_index -= 1

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：selected_caption_window = windows[chunk_index]
            selected_caption_window = windows[chunk_index]
        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
        except Exception as e:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(
            log.warning(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"TextTransform dataloader error -- url: {data_dict['__url__']}, key: {data_dict['__key__']},...
                f"TextTransform dataloader error -- url: {data_dict['__url__']}, key: {data_dict['__key__']}, chunk_index: {data_dict['chunk_index']}\n error {e}",
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank0_only=False,
                rank0_only=False,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return None
            return None

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sampled_caption_style = None
        sampled_caption_style = None
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：available_caption_styles = []
            available_caption_styles = []
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for k in selected_caption_window.keys():
            for k in selected_caption_window.keys():
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：caption_style = k.replace(self.caption_type, "").replace("_", "")
                caption_style = k.replace(self.caption_type, "").replace("_", "")
                # 中文说明：根据条件选择执行分支；代码：if caption_style == "": # it is long caption by default
                if caption_style == "":  # it is long caption by default
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：available_caption_styles.append("long")
                    available_caption_styles.append("long")
                # 中文说明：根据条件选择执行分支；代码：elif caption_style in self.caption_style_mapping:
                elif caption_style in self.caption_style_mapping:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：available_caption_styles.append(caption_style)
                    available_caption_styles.append(caption_style)
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：检查运行时假设是否成立；代码：assert caption_style in ["startframe", "endframe"], f"Unsupported caption_type {caption_style}"
                    assert caption_style in ["startframe", "endframe"], f"Unsupported caption_type {caption_style}"

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：probabilities_for_available_caption_styles = {
            probabilities_for_available_caption_styles = {
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：k: v for k, v in self.caption_probs.items() if k in available_caption_styles
                k: v for k, v in self.caption_probs.items() if k in available_caption_styles
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
            }
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sampled_caption_style = random.choices(
            sampled_caption_style = random.choices(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：list(probabilities_for_available_caption_styles),
                list(probabilities_for_available_caption_styles),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：weights=probabilities_for_available_caption_styles.values(),
                weights=probabilities_for_available_caption_styles.values(),
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)[0]
            )[0]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_dict["ai_caption"] = selected_caption_window[self.caption_style_mapping[sampled_caption_...
            data_dict["ai_caption"] = selected_caption_window[self.caption_style_mapping[sampled_caption_style]]
        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
        except Exception as e:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(
            log.warning(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"TextTransform dataloader error -- url: {data_dict['__url__']}, key: {data_dict['__key__']},...
                f"TextTransform dataloader error -- url: {data_dict['__url__']}, key: {data_dict['__key__']}, selected_caption_window: {selected_caption_window}\n error {e}",
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank0_only=False,
                rank0_only=False,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return None
            return None
        # 中文说明：根据条件选择执行分支；代码：if data_dict["ai_caption"] == "":
        if data_dict["ai_caption"] == "":
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(
            log.warning(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"TextTransform dataloader error -- empty caption! url: {data_dict['__url__']}, key: {data_di...
                f"TextTransform dataloader error -- empty caption! url: {data_dict['__url__']}, key: {data_dict['__key__']}, selected_caption_window: {selected_caption_window}",
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank0_only=False,
                rank0_only=False,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return None
            return None

        # 中文说明：检查运行时假设是否成立；代码：assert data_dict["ai_caption"] is not None and sampled_caption_style is not None
        assert data_dict["ai_caption"] is not None and sampled_caption_style is not None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_dict["sampled_caption_style"] = sampled_caption_style
        data_dict["sampled_caption_style"] = sampled_caption_style

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del data_dict[self.captions_key] # delete the field as we have extracted ai_caption from it
        del data_dict[self.captions_key]  # delete the field as we have extracted ai_caption from it

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ai_caption_embedding_data = data_dict[self.embeddings_key]
        ai_caption_embedding_data = data_dict[self.embeddings_key]
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t5_embedding = ai_caption_embedding_data[chunk_index][self.embedding_style_mapping[sampled_ca...
            t5_embedding = ai_caption_embedding_data[chunk_index][self.embedding_style_mapping[sampled_caption_style]]
        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
        except Exception as e:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(
            log.warning(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"TextTransform dataloader error -- url: {data_dict['__url__']}, key: {data_dict['__key__']},...
                f"TextTransform dataloader error -- url: {data_dict['__url__']}, key: {data_dict['__key__']}, chunk_index: {data_dict['chunk_index']}, n embeddings: {len(ai_caption_embedding_data)}, n captions: {n_windows} \n error {e}",
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank0_only=False,
                rank0_only=False,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return None
            return None
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：out_t5, out_t5_mask = pad_and_resize(
        out_t5, out_t5_mask = pad_and_resize(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：t5_embedding,
            t5_embedding,
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.t5_tokens_num,
            self.t5_tokens_num,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_mask_all_ones=self.is_mask_all_ones,
            is_mask_all_ones=self.is_mask_all_ones,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_dict["t5_text_embeddings"] = out_t5
        data_dict["t5_text_embeddings"] = out_t5
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_dict["t5_text_mask"] = out_t5_mask
        data_dict["t5_text_mask"] = out_t5_mask
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del data_dict[self.embeddings_key] # delete the field as we have extracted t5 embedding from it
        del data_dict[self.embeddings_key]  # delete the field as we have extracted t5 embedding from it

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return data_dict
        return data_dict
