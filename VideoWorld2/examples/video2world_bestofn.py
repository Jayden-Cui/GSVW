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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import base64
import base64
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import functools
import functools
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import glob
import glob
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import json
import json
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import re
import re
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import xml.etree.ElementTree as ET
import xml.etree.ElementTree as ET
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any, Callable, Dict, List, Optional
from typing import Any, Callable, Dict, List, Optional

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Set TOKENIZERS_PARALLELISM environment variable to avoid deadlocks with multiprocessing
# Set TOKENIZERS_PARALLELISM environment variable to avoid deadlocks with multiprocessing
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.auxiliary.cosmos_reason1 import CosmosReason1
from videoworld2.auxiliary.cosmos_reason1 import CosmosReason1
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.pipelines.video2world import Video2WorldPipeline
from videoworld2.pipelines.video2world import Video2WorldPipeline
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from examples.video2world import _DEFAULT_NEGATIVE_PROMPT, cleanup_distributed
from examples.video2world import _DEFAULT_NEGATIVE_PROMPT, cleanup_distributed
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from examples.video2world import process_single_generation as process_single_generation_default
from examples.video2world import process_single_generation as process_single_generation_default
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from examples.video2world import setup_pipeline as setup_pipeline_default
from examples.video2world import setup_pipeline as setup_pipeline_default
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from examples.video2world import validate_input_file
from examples.video2world import validate_input_file
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from examples.video2world_gr00t import process_single_generation as process_single_generation...
from examples.video2world_gr00t import process_single_generation as process_single_generation_gr00t
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from examples.video2world_gr00t import setup_pipeline as setup_pipeline_gr00t
from examples.video2world_gr00t import setup_pipeline as setup_pipeline_gr00t
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.distributed import get_rank
from imaginaire.utils.distributed import get_rank


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def parse_response(response: str) -> Optional[Dict[str, Any]]:
def parse_response(response: str) -> Optional[Dict[str, Any]]:
    # 中文说明：开始一个可捕获异常的代码块；代码：try:
    try:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：wrapped = f"<root>{response.strip()}</root>"
        wrapped = f"<root>{response.strip()}</root>"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：root = ET.fromstring(wrapped)
        root = ET.fromstring(wrapped)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：result = {"think": {}, "answer": None}
        result = {"think": {}, "answer": None}

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Parse <think> section
        # Parse <think> section
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：think_element = root.find("think")
        think_element = root.find("think")
        # 中文说明：根据条件选择执行分支；代码：if think_element is not None:
        if think_element is not None:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Parse overview
            # Parse overview
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：overview = think_element.find("overview")
            overview = think_element.find("overview")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：result["think"]["overview"] = overview.text.strip() if overview is not None and overview.text...
            result["think"]["overview"] = overview.text.strip() if overview is not None and overview.text else ""

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Parse components
            # Parse components
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：result["think"]["components"] = []
            result["think"]["components"] = []
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for comp in think_element.findall("component"):
            for comp in think_element.findall("component"):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：component_data = {"name": comp.get("name", "")}
                component_data = {"name": comp.get("name", "")}

                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：analysis = comp.find("analysis")
                analysis = comp.find("analysis")
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：component_data["analysis"] = analysis.text.strip() if analysis is not None and analysis.text ...
                component_data["analysis"] = analysis.text.strip() if analysis is not None and analysis.text else ""

                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：anomaly = comp.find("anomaly")
                anomaly = comp.find("anomaly")
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：component_data["anomaly"] = anomaly.text.strip() if anomaly is not None and anomaly.text else ""
                component_data["anomaly"] = anomaly.text.strip() if anomaly is not None and anomaly.text else ""

                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：result["think"]["components"].append(component_data)
                result["think"]["components"].append(component_data)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Parse <answer> section
        # Parse <answer> section
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：answer_element = root.find("answer")
        answer_element = root.find("answer")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：result["answer"] = answer_element.text.strip() if answer_element is not None and answer_eleme...
        result["answer"] = answer_element.text.strip() if answer_element is not None and answer_element.text else ""

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return result
        return result
    # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception:
    except Exception:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return None
        return None


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def video_to_base64(video_path: str) -> str:
def video_to_base64(video_path: str) -> str:
    # 中文说明：处理异常、清理资源或管理上下文；代码：with open(video_path, "rb") as video_file:
    with open(video_path, "rb") as video_file:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return base64.b64encode(video_file.read()).decode("utf-8")
        return base64.b64encode(video_file.read()).decode("utf-8")


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def build_html_report(video_path: str, responses: List[str]) -> str:
def build_html_report(video_path: str, responses: List[str]) -> str:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Convert video to base64
    # Convert video to base64
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_base64 = video_to_base64(video_path)
    video_base64 = video_to_base64(video_path)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mime_type = "video/mp4"
    mime_type = "video/mp4"

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Parse responses
    # Parse responses
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：parsed_responses = [parse_response(response) for response in responses]
    parsed_responses = [parse_response(response) for response in responses]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：valid_responses = [r for r in parsed_responses if r is not None]
    valid_responses = [r for r in parsed_responses if r is not None]

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Count answers
    # Count answers
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：yes_count = sum(1 for r in valid_responses if r.get("answer", "").lower() == "yes")
    yes_count = sum(1 for r in valid_responses if r.get("answer", "").lower() == "yes")
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：no_count = sum(1 for r in valid_responses if r.get("answer", "").lower() == "no")
    no_count = sum(1 for r in valid_responses if r.get("answer", "").lower() == "no")

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：html = f"""<!DOCTYPE html>
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Cosmos-Reason1 Video Analysis Report - {os.path.basename(video_path)}</title>
    <style>
        body {{ font-family: sans-serif; max-width: 1000px; margin: 0 auto; padding: 20px; }}
        video {{ width: 100%; max-width: 600px; }}
        .red {{ background-color: #ffebee; color: #c62828; padding: 10px; margin: 5px 0; }}
        .green {{ background-color: #e8f5e8; color: #2e7d32; padding: 10px; margin: 5px 0; }}
        .trial {{ border: 1px solid #ddd; padding: 15px; margin: 10px 0; }}
        .stats {{ display: flex; gap: 20px; margin: 20px 0; }}
        .stat {{ text-align: center; padding: 15px; }}
    </style>
</head>
<body>
    <h1>Cosmos-Reason1 Video Analysis Report</h1>
    <p>File: {os.path.basename(video_path)}</p>

    <h2>Video</h2>
    <video controls>
        <source src="data:{mime_type};base64,{video_base64}" type="{mime_type}">
    </video>

    <h2>Summary</h2>
    <div class="stats">
        <div class="stat red">
            <div style="font-size: 24px; font-weight: bold;">{yes_count}</div>
            <div>Anomaly Detected</div>
        </div>
        <div class="stat green">
            <div style="font-size: 24px; font-weight: bold;">{no_count}</div>
            <div>No Anomaly</div>
        </div>
        <div class="stat">
            <div style="font-size: 24px; font-weight: bold;">{len(valid_responses)}</div>
            <div>Total Responses</div>
        </div>
    </div>

    <h2>Detailed Analysis ({len(responses)} trials)</h2>
"""

    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i, (response, parsed) in enumerate(zip(responses, parsed_responses), 1):
    for i, (response, parsed) in enumerate(zip(responses, parsed_responses), 1):
        # 中文说明：根据条件选择执行分支；代码：if parsed is not None:
        if parsed is not None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：answer = parsed.get("answer", "").lower()
            answer = parsed.get("answer", "").lower()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：answer_class = "red" if answer == "yes" else "green"
            answer_class = "red" if answer == "yes" else "green"

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：html += f"""
            html += f"""
    <div class="trial">
        <h3>Trial {i}</h3>
"""

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Overview
            # Overview
            # 中文说明：根据条件选择执行分支；代码：if parsed.get("think", {}).get("overview"):
            if parsed.get("think", {}).get("overview"):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：html += f"""
                html += f"""
        <p><strong>Overview:</strong> {parsed["think"]["overview"]}</p>
"""

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Components
            # Components
            # 中文说明：根据条件选择执行分支；代码：if parsed.get("think", {}).get("components"):
            if parsed.get("think", {}).get("components"):
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for comp in parsed["think"]["components"]:
                for comp in parsed["think"]["components"]:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：anomaly = comp.get("anomaly", "").lower()
                    anomaly = comp.get("anomaly", "").lower()
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：comp_class = "red" if anomaly == "yes" else "green"
                    comp_class = "red" if anomaly == "yes" else "green"
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：html += f"""
                    html += f"""
        <div class="{comp_class}">
            <strong>{comp.get('name', 'Unknown Component')} - {comp.get('anomaly', '')}</strong>
            <p>{comp.get('analysis', 'No analysis provided')}</p>
        </div>
"""

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Final answer
            # Final answer
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：html += f"""
            html += f"""
        <div class="{answer_class}">
            <strong>Final Answer: {parsed.get("answer", "No answer")}</strong>
        </div>
    </div>
"""

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：html += """
    html += """
</body>
</html>"""

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return html
    return html


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def count_answers(responses: List[str]) -> tuple[int, int]:
def count_answers(responses: List[str]) -> tuple[int, int]:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：no_count = 0
    no_count = 0
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：total_parsed = 0
    total_parsed = 0
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for response in responses:
    for response in responses:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Look for <answer>Yes</answer> or <answer>No</answer> pattern (case insensitive)
        # Look for <answer>Yes</answer> or <answer>No</answer> pattern (case insensitive)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：answer_match = re.search(r"<answer>\s*(yes|no)\s*</answer>", response, re.IGNORECASE)
        answer_match = re.search(r"<answer>\s*(yes|no)\s*</answer>", response, re.IGNORECASE)
        # 中文说明：根据条件选择执行分支；代码：if answer_match:
        if answer_match:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：total_parsed += 1
            total_parsed += 1
            # 中文说明：根据条件选择执行分支；代码：if answer_match.group(1).lower() == "no":
            if answer_match.group(1).lower() == "no":
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：no_count += 1
                no_count += 1
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return no_count, total_parsed
    return no_count, total_parsed


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def parse_args():
def parse_args():
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：parser = argparse.ArgumentParser(description="Best-of-N Video Generation with Cosmos Predict2")
    parser = argparse.ArgumentParser(description="Best-of-N Video Generation with Cosmos Predict2")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--model_size",
        "--model_size",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：choices=["2B", "14B"],
        choices=["2B", "14B"],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default="2B",
        default="2B",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Size of the model to use for video-to-world generation",
        help="Size of the model to use for video-to-world generation",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--resolution",
        "--resolution",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：choices=["480", "720"],
        choices=["480", "720"],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default="720",
        default="720",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type=str,
        type=str,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Resolution of the model to use for video-to-world generation",
        help="Resolution of the model to use for video-to-world generation",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--fps",
        "--fps",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：choices=[10, 16],
        choices=[10, 16],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default=16,
        default=16,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type=int,
        type=int,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="FPS of the model to use for video-to-world generation",
        help="FPS of the model to use for video-to-world generation",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--dit_path",
        "--dit_path",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type=str,
        type=str,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default="",
        default="",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Custom path to the DiT model checkpoint for post-trained models.",
        help="Custom path to the DiT model checkpoint for post-trained models.",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--prompt",
        "--prompt",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type=str,
        type=str,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default="",
        default="",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Text prompt for video generation",
        help="Text prompt for video generation",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--input_path",
        "--input_path",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type=str,
        type=str,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default="assets/video2world/input0.jpg",
        default="assets/video2world/input0.jpg",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Path to input image or video for conditioning (include file extension)",
        help="Path to input image or video for conditioning (include file extension)",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--negative_prompt",
        "--negative_prompt",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type=str,
        type=str,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default=_DEFAULT_NEGATIVE_PROMPT,
        default=_DEFAULT_NEGATIVE_PROMPT,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Negative text prompt for video-to-world generation",
        help="Negative text prompt for video-to-world generation",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--aspect_ratio",
        "--aspect_ratio",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：choices=["1:1", "4:3", "3:4", "16:9", "9:16"],
        choices=["1:1", "4:3", "3:4", "16:9", "9:16"],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default="16:9",
        default="16:9",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type=str,
        type=str,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Aspect ratio of the generated output (width:height)",
        help="Aspect ratio of the generated output (width:height)",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--num_conditional_frames",
        "--num_conditional_frames",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type=int,
        type=int,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default=1,
        default=1,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：choices=[1, 5],
        choices=[1, 5],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Number of frames to condition on (1 for single frame, 5 for multi-frame conditioning)",
        help="Number of frames to condition on (1 for single frame, 5 for multi-frame conditioning)",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument("--guidance", type=float, default=7, help="Guidance value")
    parser.add_argument("--guidance", type=float, default=7, help="Guidance value")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument("--seed", type=int, default=0, help="Random seed for reproducibility")
    parser.add_argument("--seed", type=int, default=0, help="Random seed for reproducibility")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--save_path", type=str, default="output/best-of-n", help="Directory to save the generated vi...
        "--save_path", type=str, default="output/best-of-n", help="Directory to save the generated videos and reports"
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--num_gpus",
        "--num_gpus",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type=int,
        type=int,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default=1,
        default=1,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Number of GPUs to use for context parallel inference (should be a divisor of the total ...
        help="Number of GPUs to use for context parallel inference (should be a divisor of the total frames)",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument("--disable_guardrail", action="store_true", help="Disable guardrail check...
    parser.add_argument("--disable_guardrail", action="store_true", help="Disable guardrail checks on prompts")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument("--offload_guardrail", action="store_true", help="Offload guardrail to CP...
    parser.add_argument("--offload_guardrail", action="store_true", help="Offload guardrail to CPU to save GPU memory")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--disable_prompt_refiner", action="store_true", help="Disable prompt refiner that enhances s...
        "--disable_prompt_refiner", action="store_true", help="Disable prompt refiner that enhances short prompts"
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--offload_prompt_refiner", action="store_true", help="Offload prompt refiner to CPU to save ...
        "--offload_prompt_refiner", action="store_true", help="Offload prompt refiner to CPU to save GPU memory"
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# GR00T-specific settings. Specify --gr00t_variant to enable
    # GR00T-specific settings. Specify --gr00t_variant to enable
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument("--gr00t_variant", type=str, default="", help="GR00T variant to use", cho...
    parser.add_argument("--gr00t_variant", type=str, default="", help="GR00T variant to use", choices=["gr1", "droid"])
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--prompt_prefix", type=str, default="The robot arm is performing a task. ", help="Prefix to ...
        "--prompt_prefix", type=str, default="The robot arm is performing a task. ", help="Prefix to add to all prompts"
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Rejection sampling settings
    # Rejection sampling settings
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument("--num_generations", type=int, default=2, help="Number of generations for...
    parser.add_argument("--num_generations", type=int, default=2, help="Number of generations for the input")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--skip_generation", action="store_true", help="Skip video generation and only run the critic...
        "--skip_generation", action="store_true", help="Skip video generation and only run the critic model"
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument("--num_critic_trials", type=int, default=5, help="Number of critic trials...
    parser.add_argument("--num_critic_trials", type=int, default=5, help="Number of critic trials for each generation")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--checkpoint_dir",
        "--checkpoint_dir",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：type=str,
        type=str,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default="checkpoints/nvidia/Cosmos-Reason1-7B",
        default="checkpoints/nvidia/Cosmos-Reason1-7B",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Path to the Cosmos-Reason1 checkpoint",
        help="Path to the Cosmos-Reason1 checkpoint",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return parser.parse_args()
    return parser.parse_args()


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def generate_video(
def generate_video(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：args: argparse.Namespace, pipe: Video2WorldPipeline, process_single_generation: Callable
    args: argparse.Namespace, pipe: Video2WorldPipeline, process_single_generation: Callable
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> List[str]:
) -> List[str]:
    # 中文说明：根据条件选择执行分支；代码：if not validate_input_file(args.input_path, args.num_conditional_frames):
    if not validate_input_file(args.input_path, args.num_conditional_frames):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.error(f"Input file validation failed: {args.input_path}")
        log.error(f"Input file validation failed: {args.input_path}")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return []
        return []

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prompt = args.prompt
    prompt = args.prompt
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Running Video2WorldPipeline with \ninput: {args.input_path}\nprompt: {prompt}")
    log.info(f"Running Video2WorldPipeline with \ninput: {args.input_path}\nprompt: {prompt}")

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_paths = []
    video_paths = []
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_basename = os.path.splitext(os.path.basename(args.input_path))[0]
    input_basename = os.path.splitext(os.path.basename(args.input_path))[0]

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Ensure the output directory exists
    # Ensure the output directory exists
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.makedirs(args.save_path, exist_ok=True)
    os.makedirs(args.save_path, exist_ok=True)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Generate multiple videos with different seeds
    # Generate multiple videos with different seeds
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for generation_idx in range(args.num_generations):
    for generation_idx in range(args.num_generations):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：current_seed = args.seed + generation_idx
        current_seed = args.seed + generation_idx
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_path = os.path.join(args.save_path, f"{input_basename}_seed{current_seed}.mp4")
        output_path = os.path.join(args.save_path, f"{input_basename}_seed{current_seed}.mp4")

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Generating video {generation_idx + 1}/{args.num_generations} with seed {current_se...
        log.info(f"Generating video {generation_idx + 1}/{args.num_generations} with seed {current_seed}")

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Call the original process_single_generation function directly
        # Call the original process_single_generation function directly
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：success = process_single_generation(
        success = process_single_generation(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe=pipe,
            pipe=pipe,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_path=args.input_path,
            input_path=args.input_path,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prompt=prompt,
            prompt=prompt,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_path=output_path,
            output_path=output_path,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：negative_prompt=args.negative_prompt,
            negative_prompt=args.negative_prompt,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：aspect_ratio=args.aspect_ratio,
            aspect_ratio=args.aspect_ratio,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_conditional_frames=args.num_conditional_frames,
            num_conditional_frames=args.num_conditional_frames,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：guidance=args.guidance,
            guidance=args.guidance,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：seed=current_seed,
            seed=current_seed,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：根据条件选择执行分支；代码：if success:
        if success:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video_paths.append(output_path)
            video_paths.append(output_path)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.success(f"Successfully generated video at {output_path}")
            log.success(f"Successfully generated video at {output_path}")
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(f"Failed to generate video for seed {current_seed}")
            log.warning(f"Failed to generate video for seed {current_seed}")

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Generated {len(video_paths)}/{args.num_generations} videos")
    log.info(f"Generated {len(video_paths)}/{args.num_generations} videos")
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return video_paths
    return video_paths


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def run_critic(args, video_paths):
def run_critic(args, video_paths):
    # 中文说明：根据条件选择执行分支；代码：if not video_paths:
    if not video_paths:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning("No videos to analyze")
        log.warning("No videos to analyze")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return []
        return []

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Initializing CosmosReason1 critic model from {args.checkpoint_dir}")
    log.info(f"Initializing CosmosReason1 critic model from {args.checkpoint_dir}")
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：reason1 = CosmosReason1(args.checkpoint_dir, offload_model_to_cpu=False, enabled=True)
    reason1 = CosmosReason1(args.checkpoint_dir, offload_model_to_cpu=False, enabled=True)

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scores = []
    scores = []
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for video_path in video_paths:
    for video_path in video_paths:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Analyzing video: {video_path}")
        log.info(f"Analyzing video: {video_path}")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：responses = reason1.analyze_video(video_path, args.num_critic_trials, args.seed)
        responses = reason1.analyze_video(video_path, args.num_critic_trials, args.seed)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Count "No" (no anomaly) answers and total successful parses
        # Count "No" (no anomaly) answers and total successful parses
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：no_count, total_parsed = count_answers(responses)
        no_count, total_parsed = count_answers(responses)

        # 中文说明：根据条件选择执行分支；代码：if total_parsed == 0:
        if total_parsed == 0:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(f"No valid responses were parsed for {video_path}")
            log.warning(f"No valid responses were parsed for {video_path}")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：score = 0.0
            score = 0.0
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：score = no_count / total_parsed
            score = no_count / total_parsed

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Create output filename in the same directory as the video
        # Create output filename in the same directory as the video
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_dir = os.path.dirname(video_path)
        video_dir = os.path.dirname(video_path)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_name = os.path.splitext(os.path.basename(video_path))[0]
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：score_pct = int(score * 100)
        score_pct = int(score * 100)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_filename = os.path.join(video_dir, f"{video_name}_score{score_pct:03d}")
        output_filename = os.path.join(video_dir, f"{video_name}_score{score_pct:03d}")

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Save raw responses to JSON
        # Save raw responses to JSON
        # 中文说明：处理异常、清理资源或管理上下文；代码：with open(output_filename + ".json", "w") as f:
        with open(output_filename + ".json", "w") as f:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：json.dump(responses, f, indent=2)
            json.dump(responses, f, indent=2)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.success(f"Saved {len(responses)} responses to {output_filename}.json")
        log.success(f"Saved {len(responses)} responses to {output_filename}.json")
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(
        log.info(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Analysis results: {no_count} 'No anomaly' answers out of {total_parsed} valid responses ({s...
            f"Analysis results: {no_count} 'No anomaly' answers out of {total_parsed} valid responses ({score:.2%})"
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Generate HTML report in the same directory as the video
        # Generate HTML report in the same directory as the video
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：html_content = build_html_report(video_path, responses)
        html_content = build_html_report(video_path, responses)
        # 中文说明：处理异常、清理资源或管理上下文；代码：with open(output_filename + ".html", "w", encoding="utf-8") as f:
        with open(output_filename + ".html", "w", encoding="utf-8") as f:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f.write(html_content)
            f.write(html_content)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.success(f"Generated HTML report: {output_filename}.html")
        log.success(f"Generated HTML report: {output_filename}.html")

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scores.append(score)
        scores.append(score)

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return scores
    return scores


# 中文说明：根据条件选择执行分支；代码：if __name__ == "__main__":
if __name__ == "__main__":
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：args = parse_args()
    args = parse_args()

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Handle GR00T-specific settings if gr00t_variant is provided
    # Handle GR00T-specific settings if gr00t_variant is provided
    # 中文说明：根据条件选择执行分支；代码：if args.gr00t_variant:
    if args.gr00t_variant:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：setup_pipeline = setup_pipeline_gr00t
        setup_pipeline = setup_pipeline_gr00t
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：process_single_generation = functools.partial(process_single_generation_gr00t, prompt_prefix=...
        process_single_generation = functools.partial(process_single_generation_gr00t, prompt_prefix=args.prompt_prefix)
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：setup_pipeline = setup_pipeline_default
        setup_pipeline = setup_pipeline_default
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：process_single_generation = process_single_generation_default
        process_single_generation = process_single_generation_default

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Create output directory if it doesn't exist
    # Create output directory if it doesn't exist
    # 中文说明：根据条件选择执行分支；代码：if not os.path.exists(args.save_path):
    if not os.path.exists(args.save_path):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.makedirs(args.save_path, exist_ok=True)
        os.makedirs(args.save_path, exist_ok=True)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Created output directory: {args.save_path}")
        log.info(f"Created output directory: {args.save_path}")

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank = 0
    rank = 0
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Generate videos if not provided
    # Generate videos if not provided
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_paths = []
    video_paths = []
    # 中文说明：根据条件选择执行分支；代码：if args.skip_generation:
    if args.skip_generation:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Skipping generation, looking for existing videos in {args.save_path}")
        log.info(f"Skipping generation, looking for existing videos in {args.save_path}")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_paths = glob.glob(os.path.join(args.save_path, "*.mp4"))
        video_paths = glob.glob(os.path.join(args.save_path, "*.mp4"))
        # 中文说明：根据条件选择执行分支；代码：if not video_paths:
        if not video_paths:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(f"No video files found in {args.save_path}")
            log.warning(f"No video files found in {args.save_path}")
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe = setup_pipeline(args)
            pipe = setup_pipeline(args)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank = get_rank() # Get rank before destroying the process group
            rank = get_rank()  # Get rank before destroying the process group
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_paths = generate_video(args, pipe, process_single_generation)
            video_paths = generate_video(args, pipe, process_single_generation)
            # 中文说明：根据条件选择执行分支；代码：if not video_paths:
            if not video_paths:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.error("Failed to generate any videos, exiting")
                log.error("Failed to generate any videos, exiting")
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：exit(1)
                exit(1)
        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
        except Exception as e:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.error(f"Error during video generation: {e}")
            log.error(f"Error during video generation: {e}")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：exit(1)
            exit(1)
        # 中文说明：处理异常、清理资源或管理上下文；代码：finally:
        finally:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cleanup_distributed()
            cleanup_distributed()

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del pipe # Free up memory
    del pipe  # Free up memory
    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.empty_cache()
    torch.cuda.empty_cache()

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Run the critic model on rank 0 only
    # Run the critic model on rank 0 only
    # 中文说明：根据条件选择执行分支；代码：if rank == 0:
    if rank == 0:
        # 中文说明：开始一个可捕获异常的代码块；代码：try:
        try:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scores = run_critic(args, video_paths)
            scores = run_critic(args, video_paths)

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Print the final results
            # Print the final results
            # 中文说明：根据条件选择执行分支；代码：if scores:
            if scores:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("\nFinal Results (highest score first):")
                log.info("\nFinal Results (highest score first):")
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("-" * 80)
                log.info("-" * 80)

                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Sort videos by score (highest first)
                # Sort videos by score (highest first)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sorted_results = sorted(zip(scores, video_paths), key=lambda x: x[0], reverse=True)
                sorted_results = sorted(zip(scores, video_paths), key=lambda x: x[0], reverse=True)

                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i, (score, video_path) in enumerate(sorted_results, 1):
                for i, (score, video_path) in enumerate(sorted_results, 1):
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_name = os.path.basename(video_path)
                    video_name = os.path.basename(video_path)
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"#{i}: Score: {score:.2%} - {video_name}")
                    log.info(f"#{i}: Score: {score:.2%} - {video_name}")

                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Print the best video path
                # Print the best video path
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：best_score, best_video = sorted_results[0]
                best_score, best_video = sorted_results[0]
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info("-" * 80)
                log.info("-" * 80)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.success(f"Best video: {os.path.basename(best_video)} with score {best_score:.2%}")
                log.success(f"Best video: {os.path.basename(best_video)} with score {best_score:.2%}")
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.success(f"Full path: {best_video}")
                log.success(f"Full path: {best_video}")
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning("No scores available")
                log.warning("No scores available")
        # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
        except Exception as e:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.error(f"Error during critic evaluation: {e}")
            log.error(f"Error during critic evaluation: {e}")
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：exit(1)
            exit(1)
