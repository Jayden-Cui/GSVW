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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import hydra
import hydra
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch import nn
from torch import nn

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.fused_adam import FusedAdam
from imaginaire.utils.fused_adam import FusedAdam


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_regular_param_group(net: nn.Module):
def get_regular_param_group(net: nn.Module):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    seperate the parameters of the network into two groups: decay and no_decay.
    based on nano_gpt codebase.
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：param_dict = {pn: p for pn, p in net.named_parameters()}
    param_dict = {pn: p for pn, p in net.named_parameters()}
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：param_dict = {pn: p for pn, p in param_dict.items() if p.requires_grad}
    param_dict = {pn: p for pn, p in param_dict.items() if p.requires_grad}

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：decay_params = [p for n, p in param_dict.items() if p.dim() >= 2]
    decay_params = [p for n, p in param_dict.items() if p.dim() >= 2]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：nodecay_params = [p for n, p in param_dict.items() if p.dim() < 2]
    nodecay_params = [p for n, p in param_dict.items() if p.dim() < 2]
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return decay_params, nodecay_params
    return decay_params, nodecay_params


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_base_optimizer(
def get_base_optimizer(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model: nn.Module,
    model: nn.Module,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：lr: float,
    lr: float,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：weight_decay: float,
    weight_decay: float,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：optim_type: str = "adamw",
    optim_type: str = "adamw",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sharding: bool = False,
    sharding: bool = False,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**kwargs,
    **kwargs,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.optim.Optimizer:
) -> torch.optim.Optimizer:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：net_decay_param, net_nodecay_param = get_regular_param_group(model)
    net_decay_param, net_nodecay_param = get_regular_param_group(model)

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_decay_params = sum(p.numel() for p in net_decay_param)
    num_decay_params = sum(p.numel() for p in net_decay_param)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_nodecay_params = sum(p.numel() for p in net_nodecay_param)
    num_nodecay_params = sum(p.numel() for p in net_nodecay_param)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net_param_total = num_decay_params + num_nodecay_params
    net_param_total = num_decay_params + num_nodecay_params
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.critical(f"total num parameters : {net_param_total:,}")
    log.critical(f"total num parameters : {net_param_total:,}")

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：param_group = [
    param_group = [
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{
        {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："params": net_decay_param + net_nodecay_param,
            "params": net_decay_param + net_nodecay_param,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："lr": lr,
            "lr": lr,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："weight_decay": weight_decay,
            "weight_decay": weight_decay,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：},
        },
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
    ]

    # 中文说明：根据条件选择执行分支；代码：if optim_type == "adamw":
    if optim_type == "adamw":
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：opt_cls = torch.optim.AdamW
        opt_cls = torch.optim.AdamW
    # 中文说明：根据条件选择执行分支；代码：elif optim_type == "fusedadam":
    elif optim_type == "fusedadam":
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：opt_cls = FusedAdam
        opt_cls = FusedAdam
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"Unknown optimizer type: {optim_type}")
        raise ValueError(f"Unknown optimizer type: {optim_type}")

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return opt_cls(param_group, **kwargs)
    return opt_cls(param_group, **kwargs)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_base_scheduler(
def get_base_scheduler(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：optimizer: torch.optim.Optimizer,
    optimizer: torch.optim.Optimizer,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model: nn.Module,
    model: nn.Module,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scheduler_config: dict,
    scheduler_config: dict,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net_scheduler = hydra.utils.instantiate(scheduler_config)
    net_scheduler = hydra.utils.instantiate(scheduler_config)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net_scheduler.model = model
    net_scheduler.model = model

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return torch.optim.lr_scheduler.LambdaLR(
    return torch.optim.lr_scheduler.LambdaLR(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：optimizer,
        optimizer,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lr_lambda=[
        lr_lambda=[
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：net_scheduler.schedule,
            net_scheduler.schedule,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：],
        ],
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
