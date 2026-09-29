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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from qwen_vl_utils import process_vision_info
from qwen_vl_utils import process_vision_info
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from transformers import (
from transformers import (
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：AutoProcessor,
    AutoProcessor,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：LogitsProcessor,
    LogitsProcessor,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：LogitsProcessorList,
    LogitsProcessorList,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：Qwen2_5_VLForConditionalGeneration,
    Qwen2_5_VLForConditionalGeneration,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：set_seed,
    set_seed,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：SYSTEM_PROMPT_REFINE = (
SYSTEM_PROMPT_REFINE = (
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""You are a prompt optimization specialist whose goal is to rewrite the user's input prompts...
    """You are a prompt optimization specialist whose goal is to rewrite the user's input prompts into high-quality English prompts by referring to the details of the user's input images, making them more complete and expressive while maintaining the original meaning. You need to integrate the content of the user's photo with the input prompt for the rewrite, strictly adhering to the formatting of the examples provided.\n"""
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Task Requirements:\n"""
    """Task Requirements:\n"""
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""1. For overly brief user inputs, reasonably infer and supplement details without changing ...
    """1. For overly brief user inputs, reasonably infer and supplement details without changing the original meaning, making the image more complete and visually appealing;\n"""
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""2. Improve the characteristics of the main subject in the user's description (such as appe...
    """2. Improve the characteristics of the main subject in the user's description (such as appearance, actions, expression, quantity, ethnicity, posture, surrounding environment etc.), rendering style, spatial relationships, and camera angles;\n"""
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""3. The overall output should be in English, retaining original text in quotes and book tit...
    """3. The overall output should be in English, retaining original text in quotes and book titles as well as important input information without rewriting them;\n"""
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""4. The prompt should match the user’s intent and provide a precise and detailed style desc...
    """4. The prompt should match the user’s intent and provide a precise and detailed style description. If the user has not specified a style, you need to carefully analyze the style of the user's provided photo and use that as a reference for rewriting;\n"""
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""5. You need to emphasize movement information in the input and different camera angles;\n"""
    """5. You need to emphasize movement information in the input and different camera angles;\n"""
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""6. Your output should convey natural movement attributes, incorporating natural actions re...
    """6. Your output should convey natural movement attributes, incorporating natural actions related to the described subject category, using simple and direct verbs as much as possible;\n"""
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""7. You should reference the detailed information in the image, such as character actions, ...
    """7. You should reference the detailed information in the image, such as character actions, clothing, backgrounds, and emphasize the details in the photo;\n"""
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""8. Control the rewritten prompt to around 80-100 words.\n"""
    """8. Control the rewritten prompt to around 80-100 words.\n"""
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""9. No matter what language the user inputs, you must always output in English.\n"""
    """9. No matter what language the user inputs, you must always output in English.\n"""
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Example of the rewritten English prompt:\n"""
    """Example of the rewritten English prompt:\n"""
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""1. A Japanese fresh film-style video of a young East Asian girl with double braids sitting...
    """1. A Japanese fresh film-style video of a young East Asian girl with double braids sitting by the boat. The girl wears a white square collar puff sleeve dress, decorated with pleats and buttons. She has fair skin, delicate features, and slightly melancholic eyes, staring directly at the camera. Her hair falls naturally, with bangs covering part of her forehead. She rests her hands on the boat, appearing natural and relaxed. The background features a blurred outdoor scene, with hints of blue sky, mountains, and some dry plants. The video has a vintage film texture. A medium shot of a seated portrait.\n"""
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""2. An anime illustration in vibrant thick painting style of a white girl with cat ears hol...
    """2. An anime illustration in vibrant thick painting style of a white girl with cat ears holding a folder, showing a slightly dissatisfied expression. She has long dark purple hair and red eyes, wearing a dark gray skirt and a light gray top with a white waist tie and a name tag in bold Chinese characters that says "Ziyang". The background has a light yellow indoor tone, with faint outlines of some furniture visible. A pink halo hovers above her head, in a smooth Japanese cel-shading style. A close-up shot from a slightly elevated perspective.\n"""
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""3. CG game concept digital art featuring a huge crocodile with its mouth wide open, with t...
    """3. CG game concept digital art featuring a huge crocodile with its mouth wide open, with trees and thorns growing on its back. The crocodile's skin is rough and grayish-white, resembling stone or wood texture. Its back is lush with trees, shrubs, and thorny protrusions. With its mouth agape, the crocodile reveals a pink tongue and sharp teeth. The background features a dusk sky with some distant trees, giving the overall scene a dark and cold atmosphere. A close-up from a low angle.\n"""
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""4. In the style of an American drama promotional poster, Walter White sits in a metal fold...
    """4. In the style of an American drama promotional poster, Walter White sits in a metal folding chair wearing a yellow protective suit, with the words "Breaking Bad" written in sans-serif English above him, surrounded by piles of dollar bills and blue plastic storage boxes. He wears glasses, staring forward, dressed in a yellow jumpsuit, with his hands resting on his knees, exuding a calm and confident demeanor. The background shows an abandoned, dim factory with light filtering through the windows. There's a noticeable grainy texture. A medium shot with a straight-on close-up of the character.\n"""
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Directly output the rewritten English text."""
    """Directly output the rewritten English text."""
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：SYSTEM_PROMPT_CRITIC = """You are a helpful video analyzer. The goal is to identify artifacts...
SYSTEM_PROMPT_CRITIC = """You are a helpful video analyzer. The goal is to identify artifacts and anomalies in the video.
Analyze the video carefully and answer the question according to the following template:

<think>
<overview>
[Brief description of the video.]
</overview>

<component name="Component 1 Name">
<analysis>
[Analysis or reasoning about this component.]
</analysis>
<anomaly>Yes | No</anomaly>
</component>

<component name="Component 2 Name">
<analysis>
[Analysis or reasoning about this component.]
</analysis>
<anomaly>Yes | No</anomaly>
</component>

<!-- Add more components as needed -->
</think>

<answer>
[Whether the video contains anomalies or artifacts. Answer "Yes" or "No".]
</answer>"""

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：USER_PROMPT_CRITIC = "Does the video contain any anomalies or artifacts?"
USER_PROMPT_CRITIC = "Does the video contain any anomalies or artifacts?"


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class AllowedTokensLogitsProcessor(LogitsProcessor):
class AllowedTokensLogitsProcessor(LogitsProcessor):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, allowed_token_ids: list[int]):
    def __init__(self, allowed_token_ids: list[int]):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.allowed_mask = torch.zeros(max(allowed_token_ids) + 1, dtype=torch.bool)
        self.allowed_mask = torch.zeros(max(allowed_token_ids) + 1, dtype=torch.bool)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.allowed_mask[allowed_token_ids] = True
        self.allowed_mask[allowed_token_ids] = True

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor) -> torch.FloatTensor:
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor) -> torch.FloatTensor:
        # 中文说明：根据条件选择执行分支；代码：if scores.shape[-1] > self.allowed_mask.shape[0]:
        if scores.shape[-1] > self.allowed_mask.shape[0]:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.allowed_mask = torch.nn.functional.pad(
            self.allowed_mask = torch.nn.functional.pad(
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.allowed_mask, (0, scores.shape[-1] - self.allowed_mask.shape[0]), value=False
                self.allowed_mask, (0, scores.shape[-1] - self.allowed_mask.shape[0]), value=False
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Vectorized operation: set all disallowed tokens to -inf at once
        # Vectorized operation: set all disallowed tokens to -inf at once
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：device = scores.device
        device = scores.device

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Move mask to the same device as scores if needed
        # Move mask to the same device as scores if needed
        # 中文说明：根据条件选择执行分支；代码：if self.allowed_mask.device != device:
        if self.allowed_mask.device != device:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.allowed_mask = self.allowed_mask.to(device)
            self.allowed_mask = self.allowed_mask.to(device)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Create mask for disallowed tokens and apply it vectorized
        # Create mask for disallowed tokens and apply it vectorized
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：disallowed_mask = ~self.allowed_mask[: scores.shape[-1]]
        disallowed_mask = ~self.allowed_mask[: scores.shape[-1]]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scores[:, disallowed_mask] = float("-inf")
        scores[:, disallowed_mask] = float("-inf")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return scores
        return scores


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class CosmosReason1(torch.nn.Module):
class CosmosReason1(torch.nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, checkpoint_dir: str, offload_model_to_cpu: bool = True, enabled: bool = Tr...
    def __init__(self, checkpoint_dir: str, offload_model_to_cpu: bool = True, enabled: bool = True):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Cosmos Reason1 model for prompt refinement.
        """Cosmos Reason1 model for prompt refinement.

        Args:
            checkpoint_dir (str): Path to the checkpoint directory.
            offload_model_to_cpu (bool, optional): Whether to offload the model to CPU. Defaults to True.
            enabled (bool, optional): Whether to enable the model. Defaults to True.
        """
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_pixels = 256 * 28 * 28
        min_pixels = 256 * 28 * 28
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_pixels = 1280 * 28 * 28
        max_pixels = 1280 * 28 * 28
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.processor = AutoProcessor.from_pretrained(
        self.processor = AutoProcessor.from_pretrained(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：checkpoint_dir, min_pixels=min_pixels, max_pixels=max_pixels, use_fast=True
            checkpoint_dir, min_pixels=min_pixels, max_pixels=max_pixels, use_fast=True
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        self.model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：checkpoint_dir,
            checkpoint_dir,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：torch_dtype=torch.bfloat16,
            torch_dtype=torch.bfloat16,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn_implementation="flash_attention_2",
            attn_implementation="flash_attention_2",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：device_map="cpu",
            device_map="cpu",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_cache=True,
            use_cache=True,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.offload_model = offload_model_to_cpu
        self.offload_model = offload_model_to_cpu
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.enabled = enabled
        self.enabled = enabled
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._compute_allowed_token_ids()
        self._compute_allowed_token_ids()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# move model to GPU if not offload_model_to_cpu and enabled
        # move model to GPU if not offload_model_to_cpu and enabled
        # 中文说明：根据条件选择执行分支；代码：if not offload_model_to_cpu and self.enabled:
        if not offload_model_to_cpu and self.enabled:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.model = self.model.to("cuda")
            self.model = self.model.to("cuda")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug("Move Reason1 model to GPU")
            log.debug("Move Reason1 model to GPU")

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _compute_allowed_token_ids(self):
    def _compute_allowed_token_ids(self):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Pre-compute allowed token IDs for ASCII characters to avoid repeated computation."""
        """Pre-compute allowed token IDs for ASCII characters to avoid repeated computation."""
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug("Pre-computing allowed token IDs for ASCII characters...")
        log.debug("Pre-computing allowed token IDs for ASCII characters...")
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Get all token IDs
        # Get all token IDs
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：all_token_ids = list(range(self.processor.tokenizer.vocab_size))
        all_token_ids = list(range(self.processor.tokenizer.vocab_size))
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Batch decode all tokens at once (much faster than individual decodes)
        # Batch decode all tokens at once (much faster than individual decodes)
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Try batch decoding first (fastest)
            # Try batch decoding first (fastest)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：decoded_tokens = self.processor.tokenizer.batch_decode(
            decoded_tokens = self.processor.tokenizer.batch_decode(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：[[i] for i in all_token_ids], skip_special_tokens=False
                [[i] for i in all_token_ids], skip_special_tokens=False
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Filter for ASCII-only tokens
            # Filter for ASCII-only tokens
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.allowed_token_ids = [
            self.allowed_token_ids = [
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：token_id
                token_id
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for token_id, decoded in zip(all_token_ids, decoded_tokens)
                for token_id, decoded in zip(all_token_ids, decoded_tokens)
                # 中文说明：根据条件选择执行分支；代码：if all(ord(c) < 128 for c in decoded)
                if all(ord(c) < 128 for c in decoded)
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
            ]
        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception:
        except Exception:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Fallback to individual decoding if batch decode fails
            # Fallback to individual decoding if batch decode fails
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning("Batch decode failed, falling back to individual token decoding...")
            log.warning("Batch decode failed, falling back to individual token decoding...")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.allowed_token_ids = [
            self.allowed_token_ids = [
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：i for i in all_token_ids if all(ord(c) < 128 for c in self.processor.tokenizer.decode([i]))
                i for i in all_token_ids if all(ord(c) < 128 for c in self.processor.tokenizer.decode([i]))
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
            ]
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Add special tokens
        # Add special tokens
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.allowed_token_ids.extend(self.processor.tokenizer.all_special_ids)
        self.allowed_token_ids.extend(self.processor.tokenizer.all_special_ids)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.allowed_token_ids = list(set(self.allowed_token_ids)) # Remove duplicates
        self.allowed_token_ids = list(set(self.allowed_token_ids))  # Remove duplicates
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(f"Computed {len(self.allowed_token_ids)} allowed token IDs")
        log.debug(f"Computed {len(self.allowed_token_ids)} allowed token IDs")

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def prepare_dialog(self, image_or_video_path: str, prompt: str) -> list[dict]:
    def prepare_dialog(self, image_or_video_path: str, prompt: str) -> list[dict]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(f"Preparing dialog for {image_or_video_path} with prompt {prompt}")
        log.debug(f"Preparing dialog for {image_or_video_path} with prompt {prompt}")
        # 中文说明：根据条件选择执行分支；代码：if image_or_video_path.endswith(".mp4"):
        if image_or_video_path.endswith(".mp4"):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type = "video"
            type = "video"
        # 中文说明：根据条件选择执行分支；代码：elif image_or_video_path.endswith(".jpg") or image_or_video_path.endswith(".png"):
        elif image_or_video_path.endswith(".jpg") or image_or_video_path.endswith(".png"):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type = "image"
            type = "image"
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Unsupported file type: {image_or_video_path}")
            raise ValueError(f"Unsupported file type: {image_or_video_path}")

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：messages = [
        messages = [
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{
            {
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："role": "system",
                "role": "system",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："content": SYSTEM_PROMPT_REFINE,
                "content": SYSTEM_PROMPT_REFINE,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：},
            },
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"role": "user", "content": [{"type": "text", "text": prompt}, {"type": type, type: image_or_...
            {"role": "user", "content": [{"type": "text", "text": prompt}, {"type": type, type: image_or_video_path}]},
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
        ]
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return messages
        return messages

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def refine_prompt(self, image_or_video_path: str, prompt: str) -> str:
    def refine_prompt(self, image_or_video_path: str, prompt: str) -> str:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# skip prompt refinement if not enabled
        # skip prompt refinement if not enabled
        # 中文说明：根据条件选择执行分支；代码：if not self.enabled:
        if not self.enabled:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return prompt
            return prompt

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# prompt refinement
        # prompt refinement
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dialog = self.prepare_dialog(image_or_video_path, prompt)
        dialog = self.prepare_dialog(image_or_video_path, prompt)
        # 中文说明：根据条件选择执行分支；代码：if self.offload_model:
        if self.offload_model:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.model = self.model.to("cuda")
            self.model = self.model.to("cuda")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug("Move Reason1 model to GPU")
            log.debug("Move Reason1 model to GPU")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text = self.processor.apply_chat_template(dialog, tokenize=False, add_generation_prompt=True)
        text = self.processor.apply_chat_template(dialog, tokenize=False, add_generation_prompt=True)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：image_inputs, video_inputs = process_vision_info(dialog)
        image_inputs, video_inputs = process_vision_info(dialog)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：inputs = self.processor(
        inputs = self.processor(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text=[text],
            text=[text],
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：images=image_inputs,
            images=image_inputs,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：videos=video_inputs,
            videos=video_inputs,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding=True,
            padding=True,
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return_tensors="pt",
            return_tensors="pt",
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Inference: Generation of the output
        # Inference: Generation of the output
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：inputs = inputs.to("cuda")
        inputs = inputs.to("cuda")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：logits_processor = LogitsProcessorList([AllowedTokensLogitsProcessor(self.allowed_token_ids)])
        logits_processor = LogitsProcessorList([AllowedTokensLogitsProcessor(self.allowed_token_ids)])
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：generated_ids = self.model.generate(**inputs, max_new_tokens=512, logits_processor=logits_pro...
        generated_ids = self.model.generate(**inputs, max_new_tokens=512, logits_processor=logits_processor)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：generated_ids_trimmed = [out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, ...
        generated_ids_trimmed = [out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_text = self.processor.batch_decode(
        output_text = self.processor.batch_decode(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
            generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)[0]
        )[0]
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(f"Upsampled prompt: {output_text}")
        log.debug(f"Upsampled prompt: {output_text}")
        # 中文说明：根据条件选择执行分支；代码：if self.offload_model:
        if self.offload_model:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.model = self.model.to("cpu")
            self.model = self.model.to("cpu")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug("Offload Reason1 model to CPU")
            log.debug("Offload Reason1 model to CPU")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return output_text
        return output_text

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def analyze_video(self, video_path: str, num_trials: int = 1, seed: int | None = None) -> str:
    def analyze_video(self, video_path: str, num_trials: int = 1, seed: int | None = None) -> str:
        # 中文说明：根据条件选择执行分支；代码：if self.offload_model:
        if self.offload_model:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.model = self.model.to("cuda")
            self.model = self.model.to("cuda")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug("Move Reason1 model to GPU")
            log.debug("Move Reason1 model to GPU")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dialog = [
        dialog = [
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{
            {
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："role": "system",
                "role": "system",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："content": SYSTEM_PROMPT_CRITIC,
                "content": SYSTEM_PROMPT_CRITIC,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：},
            },
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{
            {
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："role": "user",
                "role": "user",
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："content": [
                "content": [
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"type": "video", "video": video_path, "fps": 16, "total_pixels": 8192 * 28 * 28},
                    {"type": "video", "video": video_path, "fps": 16, "total_pixels": 8192 * 28 * 28},
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"type": "text", "text": USER_PROMPT_CRITIC},
                    {"type": "text", "text": USER_PROMPT_CRITIC},
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：],
                ],
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：},
            },
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
        ]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text = self.processor.apply_chat_template(dialog, tokenize=False, add_generation_prompt=True)
        text = self.processor.apply_chat_template(dialog, tokenize=False, add_generation_prompt=True)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：image_inputs, video_inputs, video_kwargs = process_vision_info(dialog, return_video_kwargs=True)
        image_inputs, video_inputs, video_kwargs = process_vision_info(dialog, return_video_kwargs=True)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：inputs = self.processor(
        inputs = self.processor(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text=[text],
            text=[text],
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：images=image_inputs,
            images=image_inputs,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：videos=video_inputs,
            videos=video_inputs,
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return_tensors="pt",
            return_tensors="pt",
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**video_kwargs,
            **video_kwargs,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Inference: Generation of the output
        # Inference: Generation of the output
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：inputs = inputs.to("cuda")
        inputs = inputs.to("cuda")
        # 中文说明：根据条件选择执行分支；代码：if seed is not None:
        if seed is not None:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：set_seed(seed)
            set_seed(seed)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：generated_ids = self.model.generate(
        generated_ids = self.model.generate(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**inputs,
            **inputs,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：do_sample=True,
            do_sample=True,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temperature=0.6,
            temperature=0.6,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：top_p=0.95,
            top_p=0.95,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：top_k=50,
            top_k=50,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：repetition_penalty=1.05,
            repetition_penalty=1.05,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_return_sequences=num_trials,
            num_return_sequences=num_trials,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_new_tokens=4096,
            max_new_tokens=4096,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_len = len(inputs.input_ids[0])
        in_len = len(inputs.input_ids[0])
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：generated_ids_trimmed = [out_ids[in_len:] for out_ids in generated_ids]
        generated_ids_trimmed = [out_ids[in_len:] for out_ids in generated_ids]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_text = self.processor.batch_decode(generated_ids_trimmed, skip_special_tokens=True)
        output_text = self.processor.batch_decode(generated_ids_trimmed, skip_special_tokens=True)
        # 中文说明：根据条件选择执行分支；代码：if self.offload_model:
        if self.offload_model:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.model = self.model.to("cpu")
            self.model = self.model.to("cpu")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug("Offload Reason1 model to CPU")
            log.debug("Offload Reason1 model to CPU")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return output_text
        return output_text


# 中文说明：根据条件选择执行分支；代码：if __name__ == "__main__":
if __name__ == "__main__":
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model = CosmosReason1("checkpoints/nvidia/Cosmos-Reason1-7B")
    model = CosmosReason1("checkpoints/nvidia/Cosmos-Reason1-7B")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(model.refine_prompt("assets/video2world/input0.jpg", "A bus terminal in the city."))
    print(model.refine_prompt("assets/video2world/input0.jpg", "A bus terminal in the city."))
