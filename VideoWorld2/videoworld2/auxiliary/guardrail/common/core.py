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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any, Tuple
from typing import Any, Tuple

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ContentSafetyGuardrail:
class ContentSafetyGuardrail:
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_safe(self, **kwargs) -> Tuple[bool, str]:
    def is_safe(self, **kwargs) -> Tuple[bool, str]:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise NotImplementedError("Child classes must implement the is_safe method")
        raise NotImplementedError("Child classes must implement the is_safe method")


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class PostprocessingGuardrail:
class PostprocessingGuardrail:
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def postprocess(self, frames: np.ndarray) -> np.ndarray:
    def postprocess(self, frames: np.ndarray) -> np.ndarray:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise NotImplementedError("Child classes must implement the postprocess method")
        raise NotImplementedError("Child classes must implement the postprocess method")


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class GuardrailRunner:
class GuardrailRunner:
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：safety_models: list[ContentSafetyGuardrail] | None = None,
        safety_models: list[ContentSafetyGuardrail] | None = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：generic_block_msg: str = "",
        generic_block_msg: str = "",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：generic_safe_msg: str = "",
        generic_safe_msg: str = "",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：postprocessors: list[PostprocessingGuardrail] | None = None,
        postprocessors: list[PostprocessingGuardrail] | None = None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.safety_models = safety_models
        self.safety_models = safety_models
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.generic_block_msg = generic_block_msg
        self.generic_block_msg = generic_block_msg
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.generic_safe_msg = generic_safe_msg if generic_safe_msg else "Prompt is safe"
        self.generic_safe_msg = generic_safe_msg if generic_safe_msg else "Prompt is safe"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.postprocessors = postprocessors
        self.postprocessors = postprocessors

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def run_safety_check(self, input: Any) -> Tuple[bool, str]:
    def run_safety_check(self, input: Any) -> Tuple[bool, str]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Run the safety check on the input."""
        """Run the safety check on the input."""
        # 中文说明：根据条件选择执行分支；代码：if not self.safety_models:
        if not self.safety_models:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning("No safety models found, returning safe")
            log.warning("No safety models found, returning safe")
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return True, self.generic_safe_msg
            return True, self.generic_safe_msg

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for guardrail in self.safety_models:
        for guardrail in self.safety_models:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：guardrail_name = str(guardrail.__class__.__name__).upper()
            guardrail_name = str(guardrail.__class__.__name__).upper()
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(f"Running guardrail: {guardrail_name}")
            log.debug(f"Running guardrail: {guardrail_name}")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：safe, message = guardrail.is_safe(input)
            safe, message = guardrail.is_safe(input)
            # 中文说明：根据条件选择执行分支；代码：if not safe:
            if not safe:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：reasoning = self.generic_block_msg if self.generic_block_msg else f"{guardrail_name}: {message}"
                reasoning = self.generic_block_msg if self.generic_block_msg else f"{guardrail_name}: {message}"
                # 中文说明：从当前函数返回结果或结束函数执行；代码：return False, reasoning
                return False, reasoning
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return True, self.generic_safe_msg
        return True, self.generic_safe_msg

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def postprocess(self, frames: np.ndarray) -> np.ndarray:
    def postprocess(self, frames: np.ndarray) -> np.ndarray:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Run the postprocessing on the video frames."""
        """Run the postprocessing on the video frames."""
        # 中文说明：根据条件选择执行分支；代码：if not self.postprocessors:
        if not self.postprocessors:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning("No postprocessors found, returning original frames")
            log.warning("No postprocessors found, returning original frames")
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return frames
            return frames

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for guardrail in self.postprocessors:
        for guardrail in self.postprocessors:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：guardrail_name = str(guardrail.__class__.__name__).upper()
            guardrail_name = str(guardrail.__class__.__name__).upper()
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(f"Running guardrail: {guardrail_name}")
            log.debug(f"Running guardrail: {guardrail_name}")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = guardrail.postprocess(frames)
            frames = guardrail.postprocess(frames)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return frames
        return frames
