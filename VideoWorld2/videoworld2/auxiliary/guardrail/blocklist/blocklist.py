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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import re
import re
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import string
import string
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from difflib import SequenceMatcher
from difflib import SequenceMatcher

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import nltk
import nltk
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from better_profanity import profanity
from better_profanity import profanity

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.auxiliary.guardrail.blocklist.utils import read_keyword_list_from_dir, to_ascii
from videoworld2.auxiliary.guardrail.blocklist.utils import read_keyword_list_from_dir, to_ascii
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.auxiliary.guardrail.common.core import ContentSafetyGuardrail, GuardrailRunner
from videoworld2.auxiliary.guardrail.common.core import ContentSafetyGuardrail, GuardrailRunner
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log, misc
from imaginaire.utils import log, misc

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：CENSOR = misc.Color.red("*")
CENSOR = misc.Color.red("*")


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Blocklist(ContentSafetyGuardrail):
class Blocklist(ContentSafetyGuardrail):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：checkpoint_dir: str,
        checkpoint_dir: str,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：guardrail_partial_match_min_chars: int = 6,
        guardrail_partial_match_min_chars: int = 6,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：guardrail_partial_match_letter_count: float = 0.4,
        guardrail_partial_match_letter_count: float = 0.4,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> None:
    ) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Blocklist model for text filtering safety check.
        """Blocklist model for text filtering safety check.

        Args:
            checkpoint_dir (str): Path to the checkpoint directory.
            guardrail_partial_match_min_chars (int, optional): Minimum number of characters in a word to check for partial match. Defaults to 6.
            guardrail_partial_match_letter_count (float, optional): Maximum allowed difference in characters for partial match. Defaults to 0.4.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.checkpoint_dir = os.path.join(checkpoint_dir, "nvidia/Cosmos-Guardrail1/blocklist")
        self.checkpoint_dir = os.path.join(checkpoint_dir, "nvidia/Cosmos-Guardrail1/blocklist")
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：nltk.data.path.append(os.path.join(self.checkpoint_dir, "nltk_data"))
        nltk.data.path.append(os.path.join(self.checkpoint_dir, "nltk_data"))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.lemmatizer = nltk.WordNetLemmatizer()
        self.lemmatizer = nltk.WordNetLemmatizer()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.profanity = profanity
        self.profanity = profanity
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.guardrail_partial_match_min_chars = guardrail_partial_match_min_chars
        self.guardrail_partial_match_min_chars = guardrail_partial_match_min_chars
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.guardrail_partial_match_letter_count = guardrail_partial_match_letter_count
        self.guardrail_partial_match_letter_count = guardrail_partial_match_letter_count

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Load blocklist and whitelist keywords
        # Load blocklist and whitelist keywords
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.blocklist_words = read_keyword_list_from_dir(os.path.join(self.checkpoint_dir, "custom"))
        self.blocklist_words = read_keyword_list_from_dir(os.path.join(self.checkpoint_dir, "custom"))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.whitelist_words = read_keyword_list_from_dir(os.path.join(self.checkpoint_dir, "whitelis...
        self.whitelist_words = read_keyword_list_from_dir(os.path.join(self.checkpoint_dir, "whitelist"))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.exact_match_words = read_keyword_list_from_dir(os.path.join(self.checkpoint_dir, "exact_...
        self.exact_match_words = read_keyword_list_from_dir(os.path.join(self.checkpoint_dir, "exact_match"))

        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.profanity.load_censor_words(custom_words=self.blocklist_words, whitelist_words=self.whit...
        self.profanity.load_censor_words(custom_words=self.blocklist_words, whitelist_words=self.whitelist_words)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(f"Loaded {len(self.blocklist_words)} words/phrases from blocklist")
        log.debug(f"Loaded {len(self.blocklist_words)} words/phrases from blocklist")
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(f"Whitelisted {len(self.whitelist_words)} words/phrases from whitelist")
        log.debug(f"Whitelisted {len(self.whitelist_words)} words/phrases from whitelist")
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(f"Loaded {len(self.exact_match_words)} exact match words/phrases from blocklist")
        log.debug(f"Loaded {len(self.exact_match_words)} exact match words/phrases from blocklist")

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def uncensor_whitelist(self, input_prompt: str, censored_prompt: str) -> str:
    def uncensor_whitelist(self, input_prompt: str, censored_prompt: str) -> str:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Explicitly uncensor words that are in the whitelist."""
        """Explicitly uncensor words that are in the whitelist."""
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_words = input_prompt.split()
        input_words = input_prompt.split()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：censored_words = censored_prompt.split()
        censored_words = censored_prompt.split()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：whitelist_words = set(self.whitelist_words)
        whitelist_words = set(self.whitelist_words)
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i, token in enumerate(input_words):
        for i, token in enumerate(input_words):
            # 中文说明：根据条件选择执行分支；代码：if token.strip(string.punctuation).lower() in whitelist_words:
            if token.strip(string.punctuation).lower() in whitelist_words:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：censored_words[i] = token
                censored_words[i] = token
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：censored_prompt = " ".join(censored_words)
        censored_prompt = " ".join(censored_words)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return censored_prompt
        return censored_prompt

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def censor_prompt(self, input_prompt: str) -> tuple[bool, str]:
    def censor_prompt(self, input_prompt: str) -> tuple[bool, str]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Censor the prompt using the blocklist with better-profanity fuzzy matching.
        """Censor the prompt using the blocklist with better-profanity fuzzy matching.

        Args:
            input_prompt: input prompt to censor

        Returns:
            bool: True if the prompt is blocked, False otherwise
            str: A message indicating why the prompt was blocked
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：censored_prompt = self.profanity.censor(input_prompt, censor_char=CENSOR)
        censored_prompt = self.profanity.censor(input_prompt, censor_char=CENSOR)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Uncensor whitelisted words that were censored from blocklist fuzzy matching
        # Uncensor whitelisted words that were censored from blocklist fuzzy matching
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：censored_prompt = self.uncensor_whitelist(input_prompt, censored_prompt)
        censored_prompt = self.uncensor_whitelist(input_prompt, censored_prompt)
        # 中文说明：根据条件选择执行分支；代码：if CENSOR in censored_prompt:
        if CENSOR in censored_prompt:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return True, f"Prompt blocked by censorship: Censored Prompt: {censored_prompt}"
            return True, f"Prompt blocked by censorship: Censored Prompt: {censored_prompt}"
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return False, ""
        return False, ""

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def check_partial_match(
    def check_partial_match(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：normalized_prompt: str, normalized_word: str, guardrail_partial_match_letter_count: float
        normalized_prompt: str, normalized_word: str, guardrail_partial_match_letter_count: float
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> tuple[bool, str]:
    ) -> tuple[bool, str]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Check robustly if normalized word and the matching target have a difference of up to guardrail_partial_match_letter_count characters.

        Args:
            normalized_prompt: a string with many words
            normalized_word: a string with one or multiple words, its length is smaller than normalized_prompt
            guardrail_partial_match_letter_count: maximum allowed difference in characters (float to allow partial characters)

        Returns:
            bool: True if a match is found, False otherwise
            str: A message indicating why the prompt was blocked
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prompt_words = normalized_prompt.split()
        prompt_words = normalized_prompt.split()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：word_length = len(normalized_word.split())
        word_length = len(normalized_word.split())
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_similarity_ratio = (len(normalized_word) - float(guardrail_partial_match_letter_count)) /...
        max_similarity_ratio = (len(normalized_word) - float(guardrail_partial_match_letter_count)) / float(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：len(normalized_word)
            len(normalized_word)
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i in range(len(prompt_words) - word_length + 1):
        for i in range(len(prompt_words) - word_length + 1):
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Extract a substring from the prompt with the same number of words as the normalized_word
            # Extract a substring from the prompt with the same number of words as the normalized_word
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：substring = " ".join(prompt_words[i : i + word_length])
            substring = " ".join(prompt_words[i : i + word_length])
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：similarity_ratio = SequenceMatcher(None, substring, normalized_word).ratio()
            similarity_ratio = SequenceMatcher(None, substring, normalized_word).ratio()
            # 中文说明：根据条件选择执行分支；代码：if similarity_ratio >= max_similarity_ratio:
            if similarity_ratio >= max_similarity_ratio:
                # 中文说明：从当前函数返回结果或结束函数执行；代码：return (
                return (
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：True,
                    True,
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Prompt blocked by partial match blocklist: Prompt: {normalized_prompt}, Partial Match Word:...
                    f"Prompt blocked by partial match blocklist: Prompt: {normalized_prompt}, Partial Match Word: {normalized_word}",
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return False, ""
        return False, ""

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def check_against_whole_word_blocklist(
    def check_against_whole_word_blocklist(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：prompt: str,
        prompt: str,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：blocklist: list[str],
        blocklist: list[str],
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：guardrail_partial_match_min_chars: int = 6,
        guardrail_partial_match_min_chars: int = 6,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：guardrail_partial_match_letter_count: float = 0.4,
        guardrail_partial_match_letter_count: float = 0.4,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> bool:
    ) -> bool:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Check if the prompt contains any whole words from the blocklist.
        The match is case insensitive and robust to multiple spaces between words.

        Args:
            prompt: input prompt to check
            blocklist: list of words to check against
            guardrail_partial_match_min_chars: minimum number of characters in a word to check for partial match
            guardrail_partial_match_letter_count: maximum allowed difference in characters for partial match

        Returns:
            bool: True if a match is found, False otherwise
            str: A message indicating why the prompt was blocked
        """
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Normalize spaces and convert to lowercase
        # Normalize spaces and convert to lowercase
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：normalized_prompt = re.sub(r"\s+", " ", prompt).strip().lower()
        normalized_prompt = re.sub(r"\s+", " ", prompt).strip().lower()

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for word in blocklist:
        for word in blocklist:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Normalize spaces and convert to lowercase for each blocklist word
            # Normalize spaces and convert to lowercase for each blocklist word
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：normalized_word = re.sub(r"\s+", " ", word).strip().lower()
            normalized_word = re.sub(r"\s+", " ", word).strip().lower()

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Use word boundaries to ensure whole word match
            # Use word boundaries to ensure whole word match
            # 中文说明：根据条件选择执行分支；代码：if re.search(r"\b" + re.escape(normalized_word) + r"\b", normalized_prompt):
            if re.search(r"\b" + re.escape(normalized_word) + r"\b", normalized_prompt):
                # 中文说明：从当前函数返回结果或结束函数执行；代码：return True, f"Prompt blocked by exact match blocklist: Prompt: {prompt}, Exact Match Word: {...
                return True, f"Prompt blocked by exact match blocklist: Prompt: {prompt}, Exact Match Word: {word}"

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Check for partial match if the word is long enough
            # Check for partial match if the word is long enough
            # 中文说明：根据条件选择执行分支；代码：if len(normalized_word) >= guardrail_partial_match_min_chars:
            if len(normalized_word) >= guardrail_partial_match_min_chars:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：match, message = Blocklist.check_partial_match(
                match, message = Blocklist.check_partial_match(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：normalized_prompt, normalized_word, guardrail_partial_match_letter_count
                    normalized_prompt, normalized_word, guardrail_partial_match_letter_count
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：根据条件选择执行分支；代码：if match:
                if match:
                    # 中文说明：从当前函数返回结果或结束函数执行；代码：return True, message
                    return True, message

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return False, ""
        return False, ""

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_safe(self, input_prompt: str = "") -> tuple[bool, str]:
    def is_safe(self, input_prompt: str = "") -> tuple[bool, str]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Check if the input prompt is safe using the blocklist."""
        """Check if the input prompt is safe using the blocklist."""
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Check if the input is empty
        # Check if the input is empty
        # 中文说明：根据条件选择执行分支；代码：if not input_prompt:
        if not input_prompt:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return False, "Input is empty"
            return False, "Input is empty"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_prompt = to_ascii(input_prompt)
        input_prompt = to_ascii(input_prompt)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Check full sentence for censored words
        # Check full sentence for censored words
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：censored, message = self.censor_prompt(input_prompt)
        censored, message = self.censor_prompt(input_prompt)
        # 中文说明：根据条件选择执行分支；代码：if censored:
        if censored:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return False, message
            return False, message

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Check lemmatized words for censored words
        # Check lemmatized words for censored words
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tokens = nltk.word_tokenize(input_prompt)
        tokens = nltk.word_tokenize(input_prompt)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lemmas = [self.lemmatizer.lemmatize(token) for token in tokens]
        lemmas = [self.lemmatizer.lemmatize(token) for token in tokens]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lemmatized_prompt = " ".join(lemmas)
        lemmatized_prompt = " ".join(lemmas)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：censored, message = self.censor_prompt(lemmatized_prompt)
        censored, message = self.censor_prompt(lemmatized_prompt)
        # 中文说明：根据条件选择执行分支；代码：if censored:
        if censored:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return False, message
            return False, message

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Check for exact match blocklist words
        # Check for exact match blocklist words
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：censored, message = self.check_against_whole_word_blocklist(
        censored, message = self.check_against_whole_word_blocklist(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：input_prompt,
            input_prompt,
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.exact_match_words,
            self.exact_match_words,
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.guardrail_partial_match_min_chars,
            self.guardrail_partial_match_min_chars,
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.guardrail_partial_match_letter_count,
            self.guardrail_partial_match_letter_count,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：根据条件选择执行分支；代码：if censored:
        if censored:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return False, message
            return False, message

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# If all these checks pass, the input is safe
        # If all these checks pass, the input is safe
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return True, "Input is safe"
        return True, "Input is safe"


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def parse_args():
def parse_args():
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser()
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument("--prompt", type=str, required=True, help="Input prompt")
    parser.add_argument("--prompt", type=str, required=True, help="Input prompt")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--checkpoint_dir",
        "--checkpoint_dir",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type=str,
        type=str,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Path to the Blocklist checkpoint folder",
        help="Path to the Blocklist checkpoint folder",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return parser.parse_args()
    return parser.parse_args()


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def main(args):
def main(args):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：blocklist = Blocklist(checkpoint_dir=args.checkpoint_dir)
    blocklist = Blocklist(checkpoint_dir=args.checkpoint_dir)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：runner = GuardrailRunner(safety_models=[blocklist])
    runner = GuardrailRunner(safety_models=[blocklist])
    # 中文说明：处理异常、清理资源或管理上下文；代码：with misc.timer("blocklist safety check"):
    with misc.timer("blocklist safety check"):
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
