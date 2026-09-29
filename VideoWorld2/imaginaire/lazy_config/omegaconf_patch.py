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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any, Dict, List, Union
from typing import Any, Dict, List, Union

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from omegaconf import OmegaConf
from omegaconf import OmegaConf
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from omegaconf.base import DictKeyType, SCMode
from omegaconf.base import DictKeyType, SCMode
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from omegaconf.dictconfig import DictConfig # pragma: no cover
from omegaconf.dictconfig import DictConfig  # pragma: no cover


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def to_object(cfg: Any) -> Union[Dict[DictKeyType, Any], List[Any], None, str, Any]:
def to_object(cfg: Any) -> Union[Dict[DictKeyType, Any], List[Any], None, str, Any]:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Converts an OmegaConf configuration object to a native Python container (dict or list), unless
    the configuration is specifically created by LazyCall, in which case the original configuration
    is returned directly.

    This function serves as a modification of the original `to_object` method from OmegaConf,
    preventing DictConfig objects created by LazyCall from being automatically converted to Python
    dictionaries. This ensures that configurations meant to be lazily evaluated retain their intended
    structure and behavior.

    Differences from OmegaConf's original `to_object`:
    - Adds a check at the beginning to return the configuration unchanged if it is created by LazyCall.

    Reference:
    - Original OmegaConf `to_object` method: https://github.com/omry/omegaconf/blob/master/omegaconf/omegaconf.py#L595

    Args:
        cfg (Any): The OmegaConf configuration object to convert.

    Returns:
        Union[Dict[DictKeyType, Any], List[Any], None, str, Any]: The converted Python container if
        `cfg` is not a LazyCall created configuration, otherwise the unchanged `cfg`.

    Examples:
        >>> cfg = DictConfig({"key": "value", "_target_": "Model"})
        >>> to_object(cfg)
        DictConfig({"key": "value", "_target_": "Model"})

        >>> cfg = DictConfig({"list": [1, 2, 3]})
        >>> to_object(cfg)
        {'list': [1, 2, 3]}
    """
    # 中文说明：根据条件选择执行分支；代码：if isinstance(cfg, DictConfig) and "_target_" in cfg.keys():
    if isinstance(cfg, DictConfig) and "_target_" in cfg.keys():
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return cfg
        return cfg

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return OmegaConf.to_container(
    return OmegaConf.to_container(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cfg=cfg,
        cfg=cfg,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resolve=True,
        resolve=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：throw_on_missing=True,
        throw_on_missing=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：enum_to_str=False,
        enum_to_str=False,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：structured_config_mode=SCMode.INSTANTIATE,
        structured_config_mode=SCMode.INSTANTIATE,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
