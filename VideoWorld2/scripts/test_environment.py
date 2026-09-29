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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import importlib
import importlib
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import sys
import sys


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def check_packages(package_list, success_status=True):
def check_packages(package_list, success_status=True):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def print_success(package, version=None):
    def print_success(package, version=None):
        # 中文说明：根据条件选择执行分支；代码：if version:
        if version:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"\033[92m[SUCCESS]\033[0m {package} found (v{version})")
            print(f"\033[92m[SUCCESS]\033[0m {package} found (v{version})")
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"\033[92m[SUCCESS]\033[0m {package} found")
            print(f"\033[92m[SUCCESS]\033[0m {package} found")

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def print_error(message):
    def print_error(message):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"\033[91m[ERROR]\033[0m {message}")
        print(f"\033[91m[ERROR]\033[0m {message}")

    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for package in package_list:
    for package in package_list:
        # 中文说明：根据条件选择执行分支；代码：if isinstance(package, tuple):
        if isinstance(package, tuple):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：found = False
            found = False
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for alt_package in package:
            for alt_package in package:
                # 中文说明：开始一个可捕获异常的代码块；代码：try:
                try:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：module = importlib.import_module(alt_package)
                    module = importlib.import_module(alt_package)
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：version = getattr(module, "__version__", None)
                    version = getattr(module, "__version__", None)
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print_success(alt_package, version)
                    print_success(alt_package, version)
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：found = True
                    found = True
                    # 中文说明：执行循环控制或空操作；代码：break
                    break
                # 中文说明：处理异常、清理资源或管理上下文；代码：except ImportError:
                except ImportError:
                    # 中文说明：执行循环控制或空操作；代码：continue
                    continue
            # 中文说明：根据条件选择执行分支；代码：if not found:
            if not found:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print_error(f"None of the alternative packages found: \033[93m{', '.join(package)}\033[0m")
                print_error(f"None of the alternative packages found: \033[93m{', '.join(package)}\033[0m")
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：success_status = False
                success_status = False
        # 中文说明：根据条件选择执行分支；代码：elif package == "apex":
        elif package == "apex":
            # 中文说明：开始一个可捕获异常的代码块；代码：try:
            try:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：module = importlib.import_module(package)
                module = importlib.import_module(package)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：version = getattr(module, "__version__", None)
                version = getattr(module, "__version__", None)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print_success(package, version)
                print_success(package, version)
                # 中文说明：开始一个可捕获异常的代码块；代码：try:
                try:
                    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from apex import multi_tensor_apply
                    from apex import multi_tensor_apply

                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print_success("apex.multi_tensor_apply")
                    print_success("apex.multi_tensor_apply")
                # 中文说明：处理异常、清理资源或管理上下文；代码：except ImportError:
                except ImportError:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print_error("apex.multi_tensor_apply not found")
                    print_error("apex.multi_tensor_apply not found")
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：success_status = False
                    success_status = False
            # 中文说明：处理异常、清理资源或管理上下文；代码：except ImportError:
            except ImportError:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print_error("apex not found")
                print_error("apex not found")
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：success_status = False
                success_status = False
        # 中文说明：根据条件选择执行分支；代码：elif package == "transformer_engine":
        elif package == "transformer_engine":
            # 中文说明：开始一个可捕获异常的代码块；代码：try:
            try:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：module = importlib.import_module(package)
                module = importlib.import_module(package)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：version = getattr(module, "__version__", None)
                version = getattr(module, "__version__", None)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print_success(package, version)
                print_success(package, version)
                # 中文说明：开始一个可捕获异常的代码块；代码：try:
                try:
                    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import transformer_engine.pytorch
                    import transformer_engine.pytorch

                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print_success("transformer_engine.pytorch")
                    print_success("transformer_engine.pytorch")
                # 中文说明：处理异常、清理资源或管理上下文；代码：except ImportError:
                except ImportError:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print_error("transformer_engine.pytorch not found")
                    print_error("transformer_engine.pytorch not found")
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：success_status = False
                    success_status = False
            # 中文说明：处理异常、清理资源或管理上下文；代码：except ImportError:
            except ImportError:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print_error("transformer_engine not found")
                print_error("transformer_engine not found")
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：success_status = False
                success_status = False
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：开始一个可捕获异常的代码块；代码：try:
            try:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：module = importlib.import_module(package)
                module = importlib.import_module(package)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：version = getattr(module, "__version__", None)
                version = getattr(module, "__version__", None)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print_success(package, version)
                print_success(package, version)
            # 中文说明：处理异常、清理资源或管理上下文；代码：except ImportError as e:
            except ImportError as e:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print_error(f"Package not successfully imported: \033[93m{package}\033[0m")
                print_error(f"Package not successfully imported: \033[93m{package}\033[0m")
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：success_status = False
                success_status = False
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return success_status
    return success_status


# 中文说明：根据条件选择执行分支；代码：if not (sys.version_info.major == 3 and sys.version_info.minor >= 10):
if not (sys.version_info.major == 3 and sys.version_info.minor >= 10):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：detected = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    detected = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"\033[91m[ERROR]\033[0m Python 3.10+ is required. You have: \033[93m{detected}\033[0m")
    print(f"\033[91m[ERROR]\033[0m Python 3.10+ is required. You have: \033[93m{detected}\033[0m")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sys.exit(1)
    sys.exit(1)

# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print("Attempting to import critical packages...")
print("Attempting to import critical packages...")

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：packages = [
packages = [
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："torch",
    "torch",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："torchvision",
    "torchvision",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："diffusers",
    "diffusers",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："transformers",
    "transformers",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："transformer_engine",
    "transformer_engine",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："megatron.core",
    "megatron.core",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：("flash_attn", "flash_attn_interface"),
    ("flash_attn", "flash_attn_interface"),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
]
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：packages_training = [
packages_training = [
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："apex",
    "apex",
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
]

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：all_success = check_packages(packages)
all_success = check_packages(packages)
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：training_success = check_packages(packages_training)
training_success = check_packages(packages_training)
# 中文说明：根据条件选择执行分支；代码：if not training_success:
if not training_success:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print("\033[93m[WARNING]\033[0m Training packages not found. Training features will be unavai...
    print("\033[93m[WARNING]\033[0m Training packages not found. Training features will be unavailable.")

# 中文说明：根据条件选择执行分支；代码：if all_success:
if all_success:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print("-----------------------------------------------------------")
    print("-----------------------------------------------------------")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print("\033[92m[SUCCESS]\033[0m Cosmos-predict2 environment setup is successful!")
    print("\033[92m[SUCCESS]\033[0m Cosmos-predict2 environment setup is successful!")
