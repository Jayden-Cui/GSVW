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
# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""The distribution modes to use for continuous image tokenizers."""
"""The distribution modes to use for continuous image tokenizers."""

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class IdentityDistribution(torch.nn.Module):
class IdentityDistribution(torch.nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self):
    def __init__(self):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, parameters):
    def forward(self, parameters):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return parameters, (torch.tensor([0.0]), torch.tensor([0.0]))
        return parameters, (torch.tensor([0.0]), torch.tensor([0.0]))


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class GaussianDistribution(torch.nn.Module):
class GaussianDistribution(torch.nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, min_logvar: float = -30.0, max_logvar: float = 20.0):
    def __init__(self, min_logvar: float = -30.0, max_logvar: float = 20.0):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.min_logvar = min_logvar
        self.min_logvar = min_logvar
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.max_logvar = max_logvar
        self.max_logvar = max_logvar

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def sample(self, mean, logvar):
    def sample(self, mean, logvar):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：std = torch.exp(0.5 * logvar)
        std = torch.exp(0.5 * logvar)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return mean + std * torch.randn_like(mean)
        return mean + std * torch.randn_like(mean)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, parameters):
    def forward(self, parameters):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：mean, logvar = torch.chunk(parameters, 2, dim=1)
        mean, logvar = torch.chunk(parameters, 2, dim=1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：logvar = torch.clamp(logvar, self.min_logvar, self.max_logvar)
        logvar = torch.clamp(logvar, self.min_logvar, self.max_logvar)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.sample(mean, logvar), (mean, logvar)
        return self.sample(mean, logvar), (mean, logvar)
