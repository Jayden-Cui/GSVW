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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import argparse
import argparse
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import AutoModelForCausalLM, AutoTokenizer

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.auxiliary.guardrail.common.core import ContentSafetyGuardrail, GuardrailRunner
from videoworld2.auxiliary.guardrail.common.core import ContentSafetyGuardrail, GuardrailRunner
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.auxiliary.guardrail.llamaGuard3.categories import UNSAFE_CATEGORIES
from videoworld2.auxiliary.guardrail.llamaGuard3.categories import UNSAFE_CATEGORIES
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log, misc
from imaginaire.utils import log, misc

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：SAFE = misc.Color.green("SAFE")
SAFE = misc.Color.green("SAFE")
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：UNSAFE = misc.Color.red("UNSAFE")
UNSAFE = misc.Color.red("UNSAFE")


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class LlamaGuard3(ContentSafetyGuardrail):
class LlamaGuard3(ContentSafetyGuardrail):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：checkpoint_dir: str,
        checkpoint_dir: str,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：offload_model_to_cpu: bool = True,
        offload_model_to_cpu: bool = True,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Llama Guard 3 model for text filtering safety check.
        """Llama Guard 3 model for text filtering safety check.

        Args:
            checkpoint_dir (str): Path to the checkpoint directory.
            offload_model_to_cpu (bool, optional): Whether to offload the model to CPU. Defaults to True.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.checkpoint_dir = checkpoint_dir
        self.checkpoint_dir = checkpoint_dir
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.offload_model = offload_model_to_cpu
        self.offload_model = offload_model_to_cpu
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dtype = torch.bfloat16
        self.dtype = torch.bfloat16

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_id = "meta-llama/Llama-Guard-3-8B"
        model_id = "meta-llama/Llama-Guard-3-8B"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_dir = os.path.join(self.checkpoint_dir, model_id)
        model_dir = os.path.join(self.checkpoint_dir, model_id)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.model = AutoModelForCausalLM.from_pretrained(model_dir)
        self.model = AutoModelForCausalLM.from_pretrained(model_dir)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Move model to GPU unless offload_model_to_cpu is True
        # Move model to GPU unless offload_model_to_cpu is True
        # 中文说明：根据条件选择执行分支；代码：if not offload_model_to_cpu:
        if not offload_model_to_cpu:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.model = self.model.to("cuda", dtype=self.dtype).eval()
            self.model = self.model.to("cuda", dtype=self.dtype).eval()
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug("Moved llamaGuard3 model to GPU")
            log.debug("Moved llamaGuard3 model to GPU")
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.model = self.model.to("cpu", dtype=self.dtype).eval()
            self.model = self.model.to("cpu", dtype=self.dtype).eval()
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug("Moved llamaGuard3 model to CPU")
            log.debug("Moved llamaGuard3 model to CPU")

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_llamaGuard3_block_message(self, moderation_output: str) -> str:
    def get_llamaGuard3_block_message(self, moderation_output: str) -> str:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Extract the blocked category from the Llama Guard 3 model output."""
        """Extract the blocked category from the Llama Guard 3 model output."""
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_msg = "Prompt blocked by Llama Guard 3."
        block_msg = "Prompt blocked by Llama Guard 3."
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lines = moderation_output.splitlines()
            lines = moderation_output.splitlines()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：categories_detected = []
            categories_detected = []
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for line in lines[1:]:
            for line in lines[1:]:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：line_stripped = line.split("<|eot_id|>")[0].strip()
                line_stripped = line.split("<|eot_id|>")[0].strip()
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for catagory in line_stripped.split(","):
                for catagory in line_stripped.split(","):
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：catagory = catagory.strip()
                    catagory = catagory.strip()
                    # 中文说明：根据条件选择执行分支；代码：if catagory not in UNSAFE_CATEGORIES:
                    if catagory not in UNSAFE_CATEGORIES:
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(f"Unrecognized category from moderation output: {catagory}")
                        log.warning(f"Unrecognized category from moderation output: {catagory}")
                    # 中文说明：根据条件选择执行分支；代码：else:
                    else:
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：categories_detected.append(catagory)
                        categories_detected.append(catagory)
            # 中文说明：根据条件选择执行分支；代码：if len(categories_detected) > 0:
            if len(categories_detected) > 0:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：blocked_catagories = ", ".join([UNSAFE_CATEGORIES[catagory][:-1] for catagory in categories_d...
                blocked_catagories = ", ".join([UNSAFE_CATEGORIES[catagory][:-1] for catagory in categories_detected])
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_msg = f"{block_msg} Violations: {blocked_catagories}."
                block_msg = f"{block_msg} Violations: {blocked_catagories}."
        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
        except Exception as e:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(f"Unable to extract blocked category from Llama Guard 3 output: {e}")
            log.warning(f"Unable to extract blocked category from Llama Guard 3 output: {e}")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return block_msg
        return block_msg

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def filter_llamaGuard3_output(self, prompt: str) -> tuple[bool, str]:
    def filter_llamaGuard3_output(self, prompt: str) -> tuple[bool, str]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Filter the Llama Guard 3 model output and return the safety status and message."""
        """Filter the Llama Guard 3 model output and return the safety status and message."""
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：conversation = [{"role": "user", "content": prompt}]
        conversation = [{"role": "user", "content": prompt}]
        # 中文说明：根据条件选择执行分支；代码：if self.offload_model:
        if self.offload_model:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.model = self.model.to("cuda")
            self.model = self.model.to("cuda")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug("Move llamaGuard3 model to GPU")
            log.debug("Move llamaGuard3 model to GPU")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_ids = self.tokenizer.apply_chat_template(
        input_ids = self.tokenizer.apply_chat_template(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：conversation, categories=UNSAFE_CATEGORIES, return_tensors="pt"
            conversation, categories=UNSAFE_CATEGORIES, return_tensors="pt"
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：).to("cuda")
        ).to("cuda")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prompt_len = input_ids.shape[1]
        prompt_len = input_ids.shape[1]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output = self.model.generate(
        output = self.model.generate(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_ids=input_ids,
            input_ids=input_ids,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_new_tokens=100,
            max_new_tokens=100,
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return_dict_in_generate=True,
            return_dict_in_generate=True,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pad_token_id=0,
            pad_token_id=0,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：generated_tokens = output.sequences[:, prompt_len:]
        generated_tokens = output.sequences[:, prompt_len:]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：moderation_output = self.tokenizer.decode(generated_tokens[0], skip_special_tokens=False).str...
        moderation_output = self.tokenizer.decode(generated_tokens[0], skip_special_tokens=False).strip()
        # 中文说明：根据条件选择执行分支；代码：if self.offload_model:
        if self.offload_model:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.model = self.model.to("cpu")
            self.model = self.model.to("cpu")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug("Offload llamaGuard3 model to CPU")
            log.debug("Offload llamaGuard3 model to CPU")
        # 中文说明：根据条件选择执行分支；代码：if "unsafe" in moderation_output.lower():
        if "unsafe" in moderation_output.lower():
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：block_msg = self.get_llamaGuard3_block_message(moderation_output)
            block_msg = self.get_llamaGuard3_block_message(moderation_output)
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return False, block_msg
            return False, block_msg
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return True, ""
            return True, ""

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_safe(self, prompt: str) -> tuple[bool, str]:
    def is_safe(self, prompt: str) -> tuple[bool, str]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Check if the input prompt is safe according to the Llama Guard 3 model."""
        """Check if the input prompt is safe according to the Llama Guard 3 model."""
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.filter_llamaGuard3_output(prompt)
            return self.filter_llamaGuard3_output(prompt)
        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
        except Exception as e:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.error(f"Unexpected error occurred when running Llama Guard 3 guardrail: {e}")
            log.error(f"Unexpected error occurred when running Llama Guard 3 guardrail: {e}")
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return True, "Unexpected error occurred when running Llama Guard 3 guardrail."
            return True, "Unexpected error occurred when running Llama Guard 3 guardrail."


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def parse_args():
def parse_args():
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser()
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument("--prompt", type=str, required=True, help="Input prompt")
    parser.add_argument("--prompt", type=str, required=True, help="Input prompt")
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return parser.parse_args()
    return parser.parse_args()


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def main(args):
def main(args):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：llamaGuard3 = LlamaGuard3(checkpoint_dir="checkpoints/meta-llama/Llama-Guard-3-8B")
    llamaGuard3 = LlamaGuard3(checkpoint_dir="checkpoints/meta-llama/Llama-Guard-3-8B")
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：runner = GuardrailRunner(safety_models=[llamaGuard3])
    runner = GuardrailRunner(safety_models=[llamaGuard3])
    # 中文说明：处理异常、清理资源或管理上下文；代码：with misc.timer("Llama Guard 3 safety check"):
    with misc.timer("Llama Guard 3 safety check"):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：safety, message = runner.run_safety_check(args.prompt)
        safety, message = runner.run_safety_check(args.prompt)
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Input is: {'SAFE' if safety else 'UNSAFE'}")
    log.info(f"Input is: {'SAFE' if safety else 'UNSAFE'}")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Message: {message}") if not safety else None
    log.info(f"Message: {message}") if not safety else None


# 中文说明：根据条件选择执行分支；代码：if __name__ == "__main__":
if __name__ == "__main__":
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：args = parse_args()
    args = parse_args()
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：main(args)
    main(args)
