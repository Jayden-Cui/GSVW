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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import kornia as K
import kornia as K
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import kornia.augmentation as K_aug
import kornia.augmentation as K_aug
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from einops import reduce
from einops import reduce
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from skimage.metrics import structural_similarity
from skimage.metrics import structural_similarity
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import hashlib
import hashlib
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from contextlib import contextmanager
from contextlib import contextmanager

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from safetensors.torch import load as safetensors_torch_load
from safetensors.torch import load as safetensors_torch_load

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io import easy_io
from imaginaire.utils.easy_io import easy_io


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@contextmanager
@contextmanager
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def init_weights_on_device(device=torch.device("meta"), include_buffers: bool = False):
def init_weights_on_device(device=torch.device("meta"), include_buffers: bool = False):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：old_register_parameter = torch.nn.Module.register_parameter
    old_register_parameter = torch.nn.Module.register_parameter
    # 中文说明：根据条件选择执行分支；代码：if include_buffers:
    if include_buffers:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：old_register_buffer = torch.nn.Module.register_buffer
        old_register_buffer = torch.nn.Module.register_buffer

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def register_empty_parameter(module, name, param):
    def register_empty_parameter(module, name, param):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：old_register_parameter(module, name, param)
        old_register_parameter(module, name, param)
        # 中文说明：根据条件选择执行分支；代码：if param is not None:
        if param is not None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：param_cls = type(module._parameters[name])
            param_cls = type(module._parameters[name])
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs = module._parameters[name].__dict__
            kwargs = module._parameters[name].__dict__
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["requires_grad"] = param.requires_grad
            kwargs["requires_grad"] = param.requires_grad
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：module._parameters[name] = param_cls(module._parameters[name].to(device), **kwargs)
            module._parameters[name] = param_cls(module._parameters[name].to(device), **kwargs)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def register_empty_buffer(module, name, buffer, persistent=True):
    def register_empty_buffer(module, name, buffer, persistent=True):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：old_register_buffer(module, name, buffer, persistent=persistent)
        old_register_buffer(module, name, buffer, persistent=persistent)
        # 中文说明：根据条件选择执行分支；代码：if buffer is not None:
        if buffer is not None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：module._buffers[name] = module._buffers[name].to(device)
            module._buffers[name] = module._buffers[name].to(device)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def patch_tensor_constructor(fn):
    def patch_tensor_constructor(fn):
        # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def wrapper(*args, **kwargs):
        def wrapper(*args, **kwargs):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["device"] = device
            kwargs["device"] = device
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return fn(*args, **kwargs)
            return fn(*args, **kwargs)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return wrapper
        return wrapper

    # 中文说明：根据条件选择执行分支；代码：if include_buffers:
    if include_buffers:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tensor_constructors_to_patch = {
        tensor_constructors_to_patch = {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：torch_function_name: getattr(torch, torch_function_name)
            torch_function_name: getattr(torch, torch_function_name)
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for torch_function_name in ["empty", "zeros", "ones", "full"]
            for torch_function_name in ["empty", "zeros", "ones", "full"]
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
        }
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：tensor_constructors_to_patch = {}
        tensor_constructors_to_patch = {}

    # 中文说明：开始一个可捕获异常的代码块；代码：try:
    try:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：torch.nn.Module.register_parameter = register_empty_parameter
        torch.nn.Module.register_parameter = register_empty_parameter
        # 中文说明：根据条件选择执行分支；代码：if include_buffers:
        if include_buffers:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：torch.nn.Module.register_buffer = register_empty_buffer
            torch.nn.Module.register_buffer = register_empty_buffer
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for torch_function_name in tensor_constructors_to_patch.keys():
        for torch_function_name in tensor_constructors_to_patch.keys():
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：setattr(torch, torch_function_name, patch_tensor_constructor(getattr(torch, torch_function_na...
            setattr(torch, torch_function_name, patch_tensor_constructor(getattr(torch, torch_function_name)))
        # 中文说明：从生成器逐步产生本行指定的值；代码：yield
        yield
    # 中文说明：处理异常、清理资源或管理上下文；代码：finally:
    finally:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：torch.nn.Module.register_parameter = old_register_parameter
        torch.nn.Module.register_parameter = old_register_parameter
        # 中文说明：根据条件选择执行分支；代码：if include_buffers:
        if include_buffers:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：torch.nn.Module.register_buffer = old_register_buffer
            torch.nn.Module.register_buffer = old_register_buffer
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for torch_function_name, old_torch_function in tensor_constructors_to_patch.items():
        for torch_function_name, old_torch_function in tensor_constructors_to_patch.items():
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：setattr(torch, torch_function_name, old_torch_function)
            setattr(torch, torch_function_name, old_torch_function)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def load_state_dict_from_folder(file_path, torch_dtype=None):
def load_state_dict_from_folder(file_path, torch_dtype=None):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dict = {}
    state_dict = {}
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for file_name in os.listdir(file_path):
    for file_name in os.listdir(file_path):
        # 中文说明：根据条件选择执行分支；代码：if "." in file_name and file_name.split(".")[-1] in ["safetensors", "bin", "ckpt", "pth", "pt"]:
        if "." in file_name and file_name.split(".")[-1] in ["safetensors", "bin", "ckpt", "pth", "pt"]:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：state_dict.update(load_state_dict(os.path.join(file_path, file_name), torch_dtype=torch_dtype))
            state_dict.update(load_state_dict(os.path.join(file_path, file_name), torch_dtype=torch_dtype))
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return state_dict
    return state_dict


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def load_state_dict(file_path, torch_dtype=None):
def load_state_dict(file_path, torch_dtype=None):
    # 中文说明：根据条件选择执行分支；代码：if file_path.endswith(".safetensors"):
    if file_path.endswith(".safetensors"):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return load_state_dict_from_safetensors(file_path, torch_dtype=torch_dtype)
        return load_state_dict_from_safetensors(file_path, torch_dtype=torch_dtype)
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return load_state_dict_from_bin(file_path, torch_dtype=torch_dtype)
        return load_state_dict_from_bin(file_path, torch_dtype=torch_dtype)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def load_state_dict_from_safetensors(file_path, torch_dtype=None):
def load_state_dict_from_safetensors(file_path, torch_dtype=None):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_args = None
    backend_args = None
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dict = {}
    state_dict = {}
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：byte_stream = easy_io.load(file_path, backend_args=backend_args, file_format="byte")
    byte_stream = easy_io.load(file_path, backend_args=backend_args, file_format="byte")
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dict = safetensors_torch_load(byte_stream)
    state_dict = safetensors_torch_load(byte_stream)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return state_dict
    return state_dict


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def load_state_dict_from_bin(file_path, torch_dtype=None):
def load_state_dict_from_bin(file_path, torch_dtype=None):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：backend_args = None
    backend_args = None
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dict = easy_io.load(
    state_dict = easy_io.load(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：file_path, backend_args=backend_args, file_format="pt", map_location="cpu", weights_only=False
        file_path, backend_args=backend_args, file_format="pt", map_location="cpu", weights_only=False
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：根据条件选择执行分支；代码：if torch_dtype is not None:
    if torch_dtype is not None:
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i in state_dict:
        for i in state_dict:
            # 中文说明：根据条件选择执行分支；代码：if isinstance(state_dict[i], torch.Tensor):
            if isinstance(state_dict[i], torch.Tensor):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dict[i] = state_dict[i].to(torch_dtype)
                state_dict[i] = state_dict[i].to(torch_dtype)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return state_dict
    return state_dict


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def search_for_embeddings(state_dict):
def search_for_embeddings(state_dict):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：embeddings = []
    embeddings = []
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for k in state_dict:
    for k in state_dict:
        # 中文说明：根据条件选择执行分支；代码：if isinstance(state_dict[k], torch.Tensor):
        if isinstance(state_dict[k], torch.Tensor):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：embeddings.append(state_dict[k])
            embeddings.append(state_dict[k])
        # 中文说明：根据条件选择执行分支；代码：elif isinstance(state_dict[k], dict):
        elif isinstance(state_dict[k], dict):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：embeddings += search_for_embeddings(state_dict[k])
            embeddings += search_for_embeddings(state_dict[k])
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return embeddings
    return embeddings


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def search_parameter(param, state_dict):
def search_parameter(param, state_dict):
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for name, param_ in state_dict.items():
    for name, param_ in state_dict.items():
        # 中文说明：根据条件选择执行分支；代码：if param.numel() == param_.numel():
        if param.numel() == param_.numel():
            # 中文说明：根据条件选择执行分支；代码：if param.shape == param_.shape:
            if param.shape == param_.shape:
                # 中文说明：根据条件选择执行分支；代码：if torch.dist(param, param_) < 1e-3:
                if torch.dist(param, param_) < 1e-3:
                    # 中文说明：从当前函数返回结果或结束函数执行；代码：return name
                    return name
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：根据条件选择执行分支；代码：if torch.dist(param.flatten(), param_.flatten()) < 1e-3:
                if torch.dist(param.flatten(), param_.flatten()) < 1e-3:
                    # 中文说明：从当前函数返回结果或结束函数执行；代码：return name
                    return name
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return None
    return None


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def build_rename_dict(source_state_dict, target_state_dict, split_qkv=False):
def build_rename_dict(source_state_dict, target_state_dict, split_qkv=False):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：matched_keys = set()
    matched_keys = set()
    # 中文说明：处理异常、清理资源或管理上下文；代码：with torch.no_grad():
    with torch.no_grad():
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for name in source_state_dict:
        for name in source_state_dict:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rename = search_parameter(source_state_dict[name], target_state_dict)
            rename = search_parameter(source_state_dict[name], target_state_dict)
            # 中文说明：根据条件选择执行分支；代码：if rename is not None:
            if rename is not None:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f'"{name}": "{rename}",')
                print(f'"{name}": "{rename}",')
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：matched_keys.add(rename)
                matched_keys.add(rename)
            # 中文说明：根据条件选择执行分支；代码：elif split_qkv and len(source_state_dict[name].shape) >= 1 and source_state_dict[name].shape[...
            elif split_qkv and len(source_state_dict[name].shape) >= 1 and source_state_dict[name].shape[0] % 3 == 0:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：length = source_state_dict[name].shape[0] // 3
                length = source_state_dict[name].shape[0] // 3
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rename = []
                rename = []
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i in range(3):
                for i in range(3):
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：rename.append(
                    rename.append(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：search_parameter(source_state_dict[name][i * length : i * length + length], target_state_dict)
                        search_parameter(source_state_dict[name][i * length : i * length + length], target_state_dict)
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                # 中文说明：根据条件选择执行分支；代码：if None not in rename:
                if None not in rename:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f'"{name}": {rename},')
                    print(f'"{name}": {rename},')
                    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for rename_ in rename:
                    for rename_ in rename:
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：matched_keys.add(rename_)
                        matched_keys.add(rename_)
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for name in target_state_dict:
    for name in target_state_dict:
        # 中文说明：根据条件选择执行分支；代码：if name not in matched_keys:
        if name not in matched_keys:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print("Cannot find", name, target_state_dict[name].shape)
            print("Cannot find", name, target_state_dict[name].shape)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def search_for_files(folder, extensions):
def search_for_files(folder, extensions):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：files = []
    files = []
    # 中文说明：根据条件选择执行分支；代码：if os.path.isdir(folder):
    if os.path.isdir(folder):
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for file in sorted(os.listdir(folder)):
        for file in sorted(os.listdir(folder)):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：files += search_for_files(os.path.join(folder, file), extensions)
            files += search_for_files(os.path.join(folder, file), extensions)
    # 中文说明：根据条件选择执行分支；代码：elif os.path.isfile(folder):
    elif os.path.isfile(folder):
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for extension in extensions:
        for extension in extensions:
            # 中文说明：根据条件选择执行分支；代码：if folder.endswith(extension):
            if folder.endswith(extension):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：files.append(folder)
                files.append(folder)
                # 中文说明：执行循环控制或空操作；代码：break
                break
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return files
    return files


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def convert_state_dict_keys_to_single_str(state_dict, with_shape=True):
def convert_state_dict_keys_to_single_str(state_dict, with_shape=True):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：keys = []
    keys = []
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key, value in state_dict.items():
    for key, value in state_dict.items():
        # 中文说明：根据条件选择执行分支；代码：if isinstance(key, str):
        if isinstance(key, str):
            # 中文说明：根据条件选择执行分支；代码：if isinstance(value, torch.Tensor):
            if isinstance(value, torch.Tensor):
                # 中文说明：根据条件选择执行分支；代码：if with_shape:
                if with_shape:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：shape = "_".join(map(str, list(value.shape)))
                    shape = "_".join(map(str, list(value.shape)))
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：keys.append(key + ":" + shape)
                    keys.append(key + ":" + shape)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：keys.append(key)
                keys.append(key)
            # 中文说明：根据条件选择执行分支；代码：elif isinstance(value, dict):
            elif isinstance(value, dict):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：keys.append(key + "|" + convert_state_dict_keys_to_single_str(value, with_shape=with_shape))
                keys.append(key + "|" + convert_state_dict_keys_to_single_str(value, with_shape=with_shape))
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：keys.sort()
    keys.sort()
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：keys_str = ",".join(keys)
    keys_str = ",".join(keys)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return keys_str
    return keys_str


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def split_state_dict_with_prefix(state_dict):
def split_state_dict_with_prefix(state_dict):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：keys = sorted([key for key in state_dict if isinstance(key, str)])
    keys = sorted([key for key in state_dict if isinstance(key, str)])
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prefix_dict = {}
    prefix_dict = {}
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key in keys:
    for key in keys:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prefix = key if "." not in key else key.split(".")[0]
        prefix = key if "." not in key else key.split(".")[0]
        # 中文说明：根据条件选择执行分支；代码：if prefix not in prefix_dict:
        if prefix not in prefix_dict:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prefix_dict[prefix] = []
            prefix_dict[prefix] = []
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：prefix_dict[prefix].append(key)
        prefix_dict[prefix].append(key)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dicts = []
    state_dicts = []
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for prefix, keys in prefix_dict.items():
    for prefix, keys in prefix_dict.items():
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sub_state_dict = {key: state_dict[key] for key in keys}
        sub_state_dict = {key: state_dict[key] for key in keys}
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：state_dicts.append(sub_state_dict)
        state_dicts.append(sub_state_dict)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return state_dicts
    return state_dicts


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def hash_state_dict_keys(state_dict, with_shape=True):
def hash_state_dict_keys(state_dict, with_shape=True):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：keys_str = convert_state_dict_keys_to_single_str(state_dict, with_shape=with_shape)
    keys_str = convert_state_dict_keys_to_single_str(state_dict, with_shape=with_shape)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：keys_str = keys_str.encode(encoding="UTF-8")
    keys_str = keys_str.encode(encoding="UTF-8")
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return hashlib.md5(keys_str).hexdigest()
    return hashlib.md5(keys_str).hexdigest()



# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.no_grad()
@torch.no_grad()
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def compute_psnr(
def compute_psnr(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ground_truth,
    ground_truth,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：predicted,
    predicted,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) :
) :
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ground_truth = ground_truth.clip(min=0, max=1)
    ground_truth = ground_truth.clip(min=0, max=1)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：predicted = predicted.clip(min=0, max=1)
    predicted = predicted.clip(min=0, max=1)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mse = reduce((ground_truth - predicted) ** 2, "b c h w -> b", "mean")
    mse = reduce((ground_truth - predicted) ** 2, "b c h w -> b", "mean")
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return -10 * mse.log10()
    return -10 * mse.log10()


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.no_grad()
@torch.no_grad()
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def compute_lpips(
def compute_lpips(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：lpips_model,
    lpips_model,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ground_truth,
    ground_truth,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：predicted,
    predicted,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lpips_model = lpips_model.to(predicted.device)
    lpips_model = lpips_model.to(predicted.device)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：value = lpips_model.forward(ground_truth, predicted, normalize=True)
    value = lpips_model.forward(ground_truth, predicted, normalize=True)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lpips_model = lpips_model.to('cpu')
    lpips_model = lpips_model.to('cpu')
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return value[:, 0, 0, 0]
    return value[:, 0, 0, 0]

# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@torch.no_grad()
@torch.no_grad()
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def compute_ssim(
def compute_ssim(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ground_truth,
    ground_truth,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：predicted,
    predicted,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ssim = [
    ssim = [
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：structural_similarity(
        structural_similarity(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：gt.detach().cpu().numpy(),
            gt.detach().cpu().numpy(),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：hat.detach().cpu().numpy(),
            hat.detach().cpu().numpy(),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：win_size=11,
            win_size=11,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gaussian_weights=True,
            gaussian_weights=True,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：channel_axis=0,
            channel_axis=0,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_range=1.0,
            data_range=1.0,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for gt, hat in zip(ground_truth, predicted)
        for gt, hat in zip(ground_truth, predicted)
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
    ]
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return torch.tensor(ssim, dtype=predicted.dtype, device=predicted.device)
    return torch.tensor(ssim, dtype=predicted.dtype, device=predicted.device)

# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class GeometricAugmentor_K():
class GeometricAugmentor_K():
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, geo_on=True) -> None:
    def __init__(self, geo_on=True) -> None:
        # 中文说明：根据条件选择执行分支；代码：if geo_on:
        if geo_on:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.transform = K_aug.AugmentationSequential(
            self.transform = K_aug.AugmentationSequential(
              
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：K_aug.RandomAffine(
                K_aug.RandomAffine(
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：degrees=30.0,
                    degrees=30.0,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：translate=(0.1, 0.1),
                    translate=(0.1, 0.1),
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scale=(0.8, 1.2),
                    scale=(0.8, 1.2), 
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：p=0.7,
                    p=0.7,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：same_on_batch=True,
                    same_on_batch=True,
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
                ),
               
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：K_aug.RandomPerspective(
                K_aug.RandomPerspective(
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distortion_scale=0.2,
                    distortion_scale=0.2, 
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：p=0.7,
                    p=0.7,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：same_on_batch=True,
                    same_on_batch=True,
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
                ),
             
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：K_aug.ColorJitter(
                K_aug.ColorJitter(
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：brightness=0.3,
                    brightness=0.3,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：contrast=0.3,
                    contrast=0.3,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：saturation=0.2,
                    saturation=0.2, 
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hue=0.055,
                    hue=0.055, 
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：p=1.0,
                    p=1.0,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：same_on_batch=True,
                    same_on_batch=True,
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
                ),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_keys=["input"],
                data_keys=["input"],
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.transform = K_aug.AugmentationSequential(
            self.transform = K_aug.AugmentationSequential(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：K_aug.ColorJitter(
                K_aug.ColorJitter(
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：brightness=0.3,
                    brightness=0.3,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：contrast=0.3,
                    contrast=0.3,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：saturation=0.2,
                    saturation=0.2, 
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hue=0.055,
                    hue=0.055,  
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：p=1.0,
                    p=1.0,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：same_on_batch=True,
                    same_on_batch=True,
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
                ),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_keys=["input"],
                data_keys=["input"],
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self.turn_on = turn_on
        # self.turn_on = turn_on

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __call__(self, video_frames: dict) -> dict:
    def __call__(self, video_frames: dict) -> dict:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：根据条件选择执行分支；代码：if video_frames.dtype == torch.uint8:
        if video_frames.dtype == torch.uint8:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_frames = video_frames.float()
            video_frames = video_frames.float()
        # 中文说明：根据条件选择执行分支；代码：if video_frames.max() > 1:
        if video_frames.max() > 1:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_frames = video_frames / 255.0
            video_frames = video_frames / 255.0

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：augmented_frames = self.transform(video_frames)
        augmented_frames = self.transform(video_frames) 
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# augmented_frames = torch.clip(augmented_frames, 0, 255)
        # augmented_frames = torch.clip(augmented_frames, 0, 255)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return augmented_frames
        return augmented_frames