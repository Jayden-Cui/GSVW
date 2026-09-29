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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from dataclasses import dataclass
from dataclasses import dataclass
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Dict, Optional
from typing import Dict, Optional

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from hydra.core.config_store import ConfigStore
from hydra.core.config_store import ConfigStore

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.configs.vid2vid.defaults.conditioner import Vid2VidCondition, Vid2VidConditi...
from videoworld2.configs.vid2vid.defaults.conditioner import Vid2VidCondition, Vid2VidConditioner
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import LazyCall as L
from imaginaire.lazy_config import LazyCall as L
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import LazyDict
from imaginaire.lazy_config import LazyDict


# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# NOTE: extend the condition class to include action
# NOTE: extend the condition class to include action
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@dataclass(frozen=True)
@dataclass(frozen=True)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ActionConditionedCondition(Vid2VidCondition):
class ActionConditionedCondition(Vid2VidCondition):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：action: Optional[torch.Tensor] = None
    action: Optional[torch.Tensor] = None


# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# NOTE: extend the conditioner class to include action
# NOTE: extend the conditioner class to include action
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ActionConditionedConditioner(Vid2VidConditioner):
class ActionConditionedConditioner(Vid2VidConditioner):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(
    def forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：batch: Dict,
        batch: Dict,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：override_dropout_rate: Optional[Dict[str, float]] = None,
        override_dropout_rate: Optional[Dict[str, float]] = None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> ActionConditionedCondition:
    ) -> ActionConditionedCondition:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output = super()._forward(batch, override_dropout_rate)
        output = super()._forward(batch, override_dropout_rate)
        # 中文说明：检查运行时假设是否成立；代码：assert "action" in batch, "ActionConditionalConditioner requires 'action' in batch"
        assert "action" in batch, "ActionConditionalConditioner requires 'action' in batch"
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output["action"] = batch["action"]
        output["action"] = batch["action"]
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return ActionConditionedCondition(**output)
        return ActionConditionedCondition(**output)
