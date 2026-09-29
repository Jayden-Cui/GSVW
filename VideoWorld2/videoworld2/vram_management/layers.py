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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import copy
import copy

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.models.utils import init_weights_on_device
from videoworld2.models.utils import init_weights_on_device


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def cast_to(weight, dtype, device):
def cast_to(weight, dtype, device):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：r = torch.empty_like(weight, dtype=dtype, device=device)
    r = torch.empty_like(weight, dtype=dtype, device=device)
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：r.copy_(weight)
    r.copy_(weight)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return r
    return r


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class AutoWrappedModule(torch.nn.Module):
class AutoWrappedModule(torch.nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：module: torch.nn.Module,
        module: torch.nn.Module,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：offload_dtype,
        offload_dtype,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：offload_device,
        offload_device,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：onload_dtype,
        onload_dtype,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：onload_device,
        onload_device,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：computation_dtype,
        computation_dtype,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：computation_device,
        computation_device,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.module = module.to(dtype=offload_dtype, device=offload_device)
        self.module = module.to(dtype=offload_dtype, device=offload_device)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.offload_dtype = offload_dtype
        self.offload_dtype = offload_dtype
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.offload_device = offload_device
        self.offload_device = offload_device
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.onload_dtype = onload_dtype
        self.onload_dtype = onload_dtype
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.onload_device = onload_device
        self.onload_device = onload_device
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.computation_dtype = computation_dtype
        self.computation_dtype = computation_dtype
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.computation_device = computation_device
        self.computation_device = computation_device
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.state = 0
        self.state = 0

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def offload(self):
    def offload(self):
        # 中文说明：根据条件选择执行分支；代码：if self.state == 1 and (self.offload_dtype != self.onload_dtype or self.offload_device != sel...
        if self.state == 1 and (self.offload_dtype != self.onload_dtype or self.offload_device != self.onload_device):
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.module.to(dtype=self.offload_dtype, device=self.offload_device)
            self.module.to(dtype=self.offload_dtype, device=self.offload_device)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.state = 0
            self.state = 0

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def onload(self):
    def onload(self):
        # 中文说明：根据条件选择执行分支；代码：if self.state == 0 and (self.offload_dtype != self.onload_dtype or self.offload_device != sel...
        if self.state == 0 and (self.offload_dtype != self.onload_dtype or self.offload_device != self.onload_device):
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.module.to(dtype=self.onload_dtype, device=self.onload_device)
            self.module.to(dtype=self.onload_dtype, device=self.onload_device)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.state = 1
            self.state = 1

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, *args, **kwargs):
    def forward(self, *args, **kwargs):
        # 中文说明：根据条件选择执行分支；代码：if self.onload_dtype == self.computation_dtype and self.onload_device == self.computation_dev...
        if self.onload_dtype == self.computation_dtype and self.onload_device == self.computation_device:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：module = self.module
            module = self.module
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：module = copy.deepcopy(self.module).to(dtype=self.computation_dtype, device=self.computation_...
            module = copy.deepcopy(self.module).to(dtype=self.computation_dtype, device=self.computation_device)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return module(*args, **kwargs)
        return module(*args, **kwargs)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class AutoWrappedLinear(torch.nn.Linear):
class AutoWrappedLinear(torch.nn.Linear):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：module: torch.nn.Linear,
        module: torch.nn.Linear,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：offload_dtype,
        offload_dtype,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：offload_device,
        offload_device,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：onload_dtype,
        onload_dtype,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：onload_device,
        onload_device,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：computation_dtype,
        computation_dtype,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：computation_device,
        computation_device,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：处理异常、清理资源或管理上下文；代码：with init_weights_on_device(device=torch.device("meta")):
        with init_weights_on_device(device=torch.device("meta")):
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(
            super().__init__(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：in_features=module.in_features,
                in_features=module.in_features,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out_features=module.out_features,
                out_features=module.out_features,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：bias=module.bias is not None,
                bias=module.bias is not None,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dtype=offload_dtype,
                dtype=offload_dtype,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：device=offload_device,
                device=offload_device,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.weight = module.weight
        self.weight = module.weight
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.bias = module.bias
        self.bias = module.bias
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.offload_dtype = offload_dtype
        self.offload_dtype = offload_dtype
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.offload_device = offload_device
        self.offload_device = offload_device
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.onload_dtype = onload_dtype
        self.onload_dtype = onload_dtype
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.onload_device = onload_device
        self.onload_device = onload_device
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.computation_dtype = computation_dtype
        self.computation_dtype = computation_dtype
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.computation_device = computation_device
        self.computation_device = computation_device
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.state = 0
        self.state = 0

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def offload(self):
    def offload(self):
        # 中文说明：根据条件选择执行分支；代码：if self.state == 1 and (self.offload_dtype != self.onload_dtype or self.offload_device != sel...
        if self.state == 1 and (self.offload_dtype != self.onload_dtype or self.offload_device != self.onload_device):
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.to(dtype=self.offload_dtype, device=self.offload_device)
            self.to(dtype=self.offload_dtype, device=self.offload_device)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.state = 0
            self.state = 0

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def onload(self):
    def onload(self):
        # 中文说明：根据条件选择执行分支；代码：if self.state == 0 and (self.offload_dtype != self.onload_dtype or self.offload_device != sel...
        if self.state == 0 and (self.offload_dtype != self.onload_dtype or self.offload_device != self.onload_device):
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.to(dtype=self.onload_dtype, device=self.onload_device)
            self.to(dtype=self.onload_dtype, device=self.onload_device)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.state = 1
            self.state = 1

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x, *args, **kwargs):
    def forward(self, x, *args, **kwargs):
        # 中文说明：根据条件选择执行分支；代码：if self.onload_dtype == self.computation_dtype and self.onload_device == self.computation_dev...
        if self.onload_dtype == self.computation_dtype and self.onload_device == self.computation_device:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：weight, bias = self.weight, self.bias
            weight, bias = self.weight, self.bias
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：weight = cast_to(self.weight, self.computation_dtype, self.computation_device)
            weight = cast_to(self.weight, self.computation_dtype, self.computation_device)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：bias = None if self.bias is None else cast_to(self.bias, self.computation_dtype, self.computa...
            bias = None if self.bias is None else cast_to(self.bias, self.computation_dtype, self.computation_device)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return torch.nn.functional.linear(x, weight, bias)
        return torch.nn.functional.linear(x, weight, bias)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def enable_vram_management_recursively(
def enable_vram_management_recursively(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model: torch.nn.Module,
    model: torch.nn.Module,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：module_map: dict,
    module_map: dict,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：module_config: dict,
    module_config: dict,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_num_param=None,
    max_num_param=None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：overflow_module_config: dict = None,
    overflow_module_config: dict = None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：total_num_param=0,
    total_num_param=0,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for name, module in model.named_children():
    for name, module in model.named_children():
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for source_module, target_module in module_map.items():
        for source_module, target_module in module_map.items():
            # 中文说明：根据条件选择执行分支；代码：if isinstance(module, source_module):
            if isinstance(module, source_module):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_param = sum(p.numel() for p in module.parameters())
                num_param = sum(p.numel() for p in module.parameters())
                # 中文说明：根据条件选择执行分支；代码：if max_num_param is not None and total_num_param + num_param > max_num_param:
                if max_num_param is not None and total_num_param + num_param > max_num_param:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：module_config_ = overflow_module_config
                    module_config_ = overflow_module_config
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：module_config_ = module_config
                    module_config_ = module_config
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：module_ = target_module(module, **module_config_)
                module_ = target_module(module, **module_config_)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：setattr(model, name, module_)
                setattr(model, name, module_)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：total_num_param += num_param
                total_num_param += num_param
                # 中文说明：执行循环控制或空操作；代码：break
                break
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：total_num_param = enable_vram_management_recursively(
            total_num_param = enable_vram_management_recursively(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：module, module_map, module_config, max_num_param, overflow_module_config, total_num_param
                module, module_map, module_config, max_num_param, overflow_module_config, total_num_param
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return total_num_param
    return total_num_param


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def enable_vram_management(
def enable_vram_management(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model: torch.nn.Module,
    model: torch.nn.Module,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：module_map: dict,
    module_map: dict,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：module_config: dict,
    module_config: dict,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_num_param=None,
    max_num_param=None,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：overflow_module_config: dict = None,
    overflow_module_config: dict = None,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：enable_vram_management_recursively(
    enable_vram_management_recursively(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model, module_map, module_config, max_num_param, overflow_module_config, total_num_param=0
        model, module_map, module_config, max_num_param, overflow_module_config, total_num_param=0
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model.vram_management_enabled = True
    model.vram_management_enabled = True
