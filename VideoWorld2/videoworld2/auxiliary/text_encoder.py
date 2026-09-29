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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import List, Tuple, Union
from typing import List, Tuple, Union

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import transformers
import transformers
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from transformers.models.t5 import T5EncoderModel, T5TokenizerFast
from transformers.models.t5 import T5EncoderModel, T5TokenizerFast

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log

# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：transformers.utils.logging.set_verbosity_error()
transformers.utils.logging.set_verbosity_error()


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class CosmosT5TextEncoder(torch.nn.Module):
class CosmosT5TextEncoder(torch.nn.Module):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Handles T5 text encoding operations."""
    """Handles T5 text encoding operations."""

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model_name: str = "google-t5/t5-11b", # not used by default to match open-source repo
        model_name: str = "google-t5/t5-11b",  # not used by default to match open-source repo
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：device: str = "cuda",
        device: str = "cuda",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cache_dir: str = None,
        cache_dir: str = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：local_files_only: bool = False,
        local_files_only: bool = False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Initializes the T5 tokenizer and encoder.
        """Initializes the T5 tokenizer and encoder.

        Args:
            model_name: The name of the T5 model to use.
            device: The device to use for computations.
        """
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.tokenizer = T5TokenizerFast.from_pretrained(
            self.tokenizer = T5TokenizerFast.from_pretrained(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pretrained_model_name_or_path=cache_dir, cache_dir=cache_dir, local_files_only=local_files_only
                pretrained_model_name_or_path=cache_dir, cache_dir=cache_dir, local_files_only=local_files_only
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.text_encoder = T5EncoderModel.from_pretrained(
            self.text_encoder = T5EncoderModel.from_pretrained(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pretrained_model_name_or_path=cache_dir, cache_dir=cache_dir, local_files_only=local_files_only
                pretrained_model_name_or_path=cache_dir, cache_dir=cache_dir, local_files_only=local_files_only
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：).to(device)
            ).to(device)
        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
        except Exception as e:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.error(e)
            log.error(e)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.tokenizer = T5TokenizerFast.from_pretrained(
            self.tokenizer = T5TokenizerFast.from_pretrained(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pretrained_model_name_or_path=model_name, cache_dir=cache_dir, local_files_only=local_files_only
                pretrained_model_name_or_path=model_name, cache_dir=cache_dir, local_files_only=local_files_only
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.text_encoder = T5EncoderModel.from_pretrained(
            self.text_encoder = T5EncoderModel.from_pretrained(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pretrained_model_name_or_path=model_name, cache_dir=cache_dir, local_files_only=local_files_only
                pretrained_model_name_or_path=model_name, cache_dir=cache_dir, local_files_only=local_files_only
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：).to(device)
            ).to(device)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.text_encoder.eval()
        self.text_encoder.eval()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.device = device
        self.device = device

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.inference_mode()
    @torch.inference_mode()
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def encode_prompts(
    def encode_prompts(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, prompts: Union[str, List[str]], max_length: int = 512, return_mask: bool = False
        self, prompts: Union[str, List[str]], max_length: int = 512, return_mask: bool = False
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Union[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]:
    ) -> Union[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Encodes text prompts into hidden state representations using a T5 encoder.
        """Encodes text prompts into hidden state representations using a T5 encoder.

        This function tokenizes the input prompts, processes them through a T5 text encoder,
        and returns the last hidden states. The encoded outputs beyond the actual sequence
        length are zero-padded. All prompts in a batch are padded to max_length.

        Args:
            prompts: Input text to encode. Can be a single string or a list of strings.
            max_length: Maximum sequence length for tokenization and padding. Longer
                sequences will be truncated. Defaults to 512.
            return_mask: If True, returns the attention mask along with encoded text.
                Defaults to False.

        Returns:
            If return_mask is False:
                torch.Tensor: Encoded text embeddings of shape (batch_size, max_length, hidden_size).
            If return_mask is True:
                tuple[torch.Tensor, torch.Tensor]: A tuple containing:
                    - Encoded text embeddings of shape (batch_size, max_length, hidden_size)
                    - Attention mask of shape (batch_size, max_length) as boolean tensor

        Raises:
            ValueError: If the input prompts list is empty.

        Example:
            >>> encoder = CosmosT5TextEncoder()
            >>> prompts = ["Hello world", "Another example"]
            >>> embeddings = encoder.encode_prompts(prompts, max_length=128)
        """
        # 中文说明：根据条件选择执行分支；代码：if isinstance(prompts, str):
        if isinstance(prompts, str):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prompts = [prompts]
            prompts = [prompts]

        # 中文说明：根据条件选择执行分支；代码：if not prompts:
        if not prompts:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError("The input prompt list is empty.")
            raise ValueError("The input prompt list is empty.")

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch_encoding = self.tokenizer.batch_encode_plus(
        batch_encoding = self.tokenizer.batch_encode_plus(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：prompts,
            prompts,
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return_tensors="pt",
            return_tensors="pt",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：truncation=True,
            truncation=True,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding="max_length",
            padding="max_length",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_length=max_length,
            max_length=max_length,
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return_length=True,
            return_length=True,
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return_offsets_mapping=False,
            return_offsets_mapping=False,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_ids = batch_encoding.input_ids.to(self.device)
        input_ids = batch_encoding.input_ids.to(self.device)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：attn_mask = batch_encoding.attention_mask.to(self.device)
        attn_mask = batch_encoding.attention_mask.to(self.device)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：outputs = self.text_encoder(input_ids=input_ids, attention_mask=attn_mask)
        outputs = self.text_encoder(input_ids=input_ids, attention_mask=attn_mask)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：encoded_text = outputs.last_hidden_state
        encoded_text = outputs.last_hidden_state
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lengths = attn_mask.sum(dim=1).cpu()
        lengths = attn_mask.sum(dim=1).cpu()

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for batch_id in range(encoded_text.shape[0]):
        for batch_id in range(encoded_text.shape[0]):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：encoded_text[batch_id][lengths[batch_id] :] = 0
            encoded_text[batch_id][lengths[batch_id] :] = 0

        # 中文说明：根据条件选择执行分支；代码：if return_mask:
        if return_mask:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return encoded_text, attn_mask.bool()
            return encoded_text, attn_mask.bool()
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return encoded_text
        return encoded_text
