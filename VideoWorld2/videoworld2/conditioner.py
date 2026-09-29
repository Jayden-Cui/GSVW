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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from __future__ import annotations
from __future__ import annotations

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import copy
import copy
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from abc import ABC, abstractmethod
from abc import ABC, abstractmethod
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from collections import defaultdict
from collections import defaultdict
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from contextlib import nullcontext
from contextlib import nullcontext
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from dataclasses import dataclass, fields
from dataclasses import dataclass, fields
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from enum import Enum
from enum import Enum
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any, Dict, List, Optional, Tuple, TypeVar, Union
from typing import Any, Dict, List, Optional, Tuple, TypeVar, Union

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import omegaconf
import omegaconf
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.nn as nn
import torch.nn as nn
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.distributed import ProcessGroup
from torch.distributed import ProcessGroup

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.functional.batch_ops import batch_mul
from videoworld2.functional.batch_ops import batch_mul
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.utils.context_parallel import broadcast
from videoworld2.utils.context_parallel import broadcast
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.utils.misc import count_params, disabled_train
from videoworld2.utils.misc import count_params, disabled_train
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import instantiate
from imaginaire.lazy_config import instantiate
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：T = TypeVar("T", bound="BaseCondition")
T = TypeVar("T", bound="BaseCondition")


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class DataType(str, Enum):
class DataType(str, Enum):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：IMAGE = "image"
    IMAGE = "image"
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：VIDEO = "video"
    VIDEO = "video"
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：MIX = "mix"
    MIX = "mix"

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __str__(self) -> str:
    def __str__(self) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.value
        return self.value


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def broadcast_condition(condition: BaseCondition, process_group: Optional[ProcessGroup] = Non...
def broadcast_condition(condition: BaseCondition, process_group: Optional[ProcessGroup] = None) -> BaseCondition:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Broadcast the condition from the minimum rank in the specified group(s).
    """
    # 中文说明：根据条件选择执行分支；代码：if condition.is_broadcasted:
    if condition.is_broadcasted:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return condition
        return condition

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs = condition.to_dict(skip_underscore=False)
    kwargs = condition.to_dict(skip_underscore=False)
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key, value in kwargs.items():
    for key, value in kwargs.items():
        # 中文说明：根据条件选择执行分支；代码：if value is not None:
        if value is not None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs[key] = broadcast(value, process_group)
            kwargs[key] = broadcast(value, process_group)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["_is_broadcasted"] = True
    kwargs["_is_broadcasted"] = True
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return type(condition)(**kwargs)
    return type(condition)(**kwargs)


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@dataclass(frozen=True)
@dataclass(frozen=True)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class BaseCondition(ABC):
class BaseCondition(ABC):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Attributes:
        _is_broadcasted: Flag indicating if parallel broadcast splitting
            has been performed. This is an internal implementation detail.
    """

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_is_broadcasted: bool = False
    _is_broadcasted: bool = False

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def to_dict(self, skip_underscore: bool = True) -> Dict[str, Any]:
    def to_dict(self, skip_underscore: bool = True) -> Dict[str, Any]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Converts the condition to a dictionary.
        """Converts the condition to a dictionary.

        Returns:
            Dictionary containing the condition's fields and values.
        """
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# return {f.name: getattr(self, f.name) for f in fields(self) if not f.name.startswith("_")}
        # return {f.name: getattr(self, f.name) for f in fields(self) if not f.name.startswith("_")}
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return {f.name: getattr(self, f.name) for f in fields(self) if not (f.name.startswith("_") an...
        return {f.name: getattr(self, f.name) for f in fields(self) if not (f.name.startswith("_") and skip_underscore)}

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_broadcasted(self) -> bool:
    def is_broadcasted(self) -> bool:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self._is_broadcasted
        return self._is_broadcasted

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def broadcast(self, process_group: torch.distributed.ProcessGroup) -> BaseCondition:
    def broadcast(self, process_group: torch.distributed.ProcessGroup) -> BaseCondition:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Broadcasts and splits the condition across the checkpoint parallelism group.
        """Broadcasts and splits the condition across the checkpoint parallelism group.
        For most condition, such asT2VCondition, we do not need split.

        Args:
            process_group: The process group for broadcast and split

        Returns:
            A new BaseCondition instance with the broadcasted and split condition.
        """
        # 中文说明：根据条件选择执行分支；代码：if self.is_broadcasted:
        if self.is_broadcasted:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return self
            return self
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return broadcast_condition(self, process_group)
        return broadcast_condition(self, process_group)


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@dataclass(frozen=True)
@dataclass(frozen=True)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class T2VCondition(BaseCondition):
class T2VCondition(BaseCondition):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：crossattn_emb: Optional[torch.Tensor] = None
    crossattn_emb: Optional[torch.Tensor] = None
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_type: DataType = DataType.VIDEO
    data_type: DataType = DataType.VIDEO
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：padding_mask: Optional[torch.Tensor] = None
    padding_mask: Optional[torch.Tensor] = None
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：fps: Optional[torch.Tensor] = None
    fps: Optional[torch.Tensor] = None

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def edit_data_type(self, data_type: DataType) -> T2VCondition:
    def edit_data_type(self, data_type: DataType) -> T2VCondition:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Edit the data type of the condition.
        """Edit the data type of the condition.

        Args:
            data_type: The new data type.

        Returns:
            A new T2VCondition instance with the new data type.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs = self.to_dict(skip_underscore=False)
        kwargs = self.to_dict(skip_underscore=False)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["data_type"] = data_type
        kwargs["data_type"] = data_type
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return type(self)(**kwargs)
        return type(self)(**kwargs)

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_video(self) -> bool:
    def is_video(self) -> bool:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.data_type == DataType.VIDEO
        return self.data_type == DataType.VIDEO


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@dataclass(frozen=True)
@dataclass(frozen=True)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class GR00TV1Img2VidCondition(T2VCondition):
class GR00TV1Img2VidCondition(T2VCondition):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：gt_first_frame: Optional[torch.Tensor] = None
    gt_first_frame: Optional[torch.Tensor] = None
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：use_image_condition: bool = False
    use_image_condition: bool = False
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：condition_video_input_mask_B_C_T_H_W: Optional[torch.Tensor] = None
    condition_video_input_mask_B_C_T_H_W: Optional[torch.Tensor] = None

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def edit_video_condition(
    def edit_video_condition(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, x0_B_C_T_H_W, process_group: Optional[ProcessGroup] = None
        self, x0_B_C_T_H_W, process_group: Optional[ProcessGroup] = None
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> GR00TV1Img2VidCondition:
    ) -> GR00TV1Img2VidCondition:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Edit the video condition to include the video mask information.
        """Edit the video condition to include the video mask information.

        Args:
            x0_B_C_T_H_W: The first frame of the video.

        Returns:
            A new GR00TV1Img2VidCondition instance with the video mask information.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pg_size = 1 if process_group is None else process_group.size()
        pg_size = 1 if process_group is None else process_group.size()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs = self.to_dict(skip_underscore=False)
        kwargs = self.to_dict(skip_underscore=False)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：B, _, T, H, W = x0_B_C_T_H_W.shape
        B, _, T, H, W = x0_B_C_T_H_W.shape
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：condition_video_input_mask = torch.zeros((B, 1, T, H, W), dtype=x0_B_C_T_H_W.dtype, device=x0...
        condition_video_input_mask = torch.zeros((B, 1, T, H, W), dtype=x0_B_C_T_H_W.dtype, device=x0_B_C_T_H_W.device)
        # 中文说明：根据条件选择执行分支；代码：if pg_size == 1 or process_group.rank() == 0:
        if pg_size == 1 or process_group.rank() == 0:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["gt_first_frame"] = x0_B_C_T_H_W[:, :, 0].detach()
            kwargs["gt_first_frame"] = x0_B_C_T_H_W[:, :, 0].detach()
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：condition_video_input_mask[:, :, 0] += 1
            condition_video_input_mask[:, :, 0] += 1
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["condition_video_input_mask_B_C_T_H_W"] = condition_video_input_mask
        kwargs["condition_video_input_mask_B_C_T_H_W"] = condition_video_input_mask
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return type(self)(**kwargs)
        return type(self)(**kwargs)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class AbstractEmbModel(nn.Module):
class AbstractEmbModel(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self):
    def __init__(self):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._is_trainable = None
        self._is_trainable = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._dropout_rate = None
        self._dropout_rate = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._input_key = None
        self._input_key = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._return_dict = False
        self._return_dict = False

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_trainable(self) -> bool:
    def is_trainable(self) -> bool:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self._is_trainable
        return self._is_trainable

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def dropout_rate(self) -> Union[float, torch.Tensor]:
    def dropout_rate(self) -> Union[float, torch.Tensor]:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self._dropout_rate
        return self._dropout_rate

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def input_key(self) -> str:
    def input_key(self) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self._input_key
        return self._input_key

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@property
    @property
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_return_dict(self) -> bool:
    def is_return_dict(self) -> bool:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self._return_dict
        return self._return_dict

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@is_trainable.setter
    @is_trainable.setter
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_trainable(self, value: bool):
    def is_trainable(self, value: bool):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._is_trainable = value
        self._is_trainable = value

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@dropout_rate.setter
    @dropout_rate.setter
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def dropout_rate(self, value: Union[float, torch.Tensor]):
    def dropout_rate(self, value: Union[float, torch.Tensor]):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._dropout_rate = value
        self._dropout_rate = value

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@input_key.setter
    @input_key.setter
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def input_key(self, value: str):
    def input_key(self, value: str):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._input_key = value
        self._input_key = value

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@is_return_dict.setter
    @is_return_dict.setter
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_return_dict(self, value: bool):
    def is_return_dict(self, value: bool):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._return_dict = value
        self._return_dict = value

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@is_trainable.deleter
    @is_trainable.deleter
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_trainable(self):
    def is_trainable(self):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del self._is_trainable
        del self._is_trainable

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@dropout_rate.deleter
    @dropout_rate.deleter
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def dropout_rate(self):
    def dropout_rate(self):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del self._dropout_rate
        del self._dropout_rate

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@input_key.deleter
    @input_key.deleter
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def input_key(self):
    def input_key(self):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del self._input_key
        del self._input_key

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@is_return_dict.deleter
    @is_return_dict.deleter
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_return_dict(self):
    def is_return_dict(self):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del self._return_dict
        del self._return_dict

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def random_dropout_input(
    def random_dropout_input(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, in_tensor: torch.Tensor, dropout_rate: Optional[float] = None, key: Optional[str] = None
        self, in_tensor: torch.Tensor, dropout_rate: Optional[float] = None, key: Optional[str] = None
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor:
    ) -> torch.Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del key
        del key
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout_rate = dropout_rate if dropout_rate is not None else self.dropout_rate
        dropout_rate = dropout_rate if dropout_rate is not None else self.dropout_rate
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return batch_mul(
        return batch_mul(
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.bernoulli((1.0 - dropout_rate) * torch.ones(in_tensor.shape[0])).type_as(in_tensor),
            torch.bernoulli((1.0 - dropout_rate) * torch.ones(in_tensor.shape[0])).type_as(in_tensor),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：in_tensor,
            in_tensor,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def details(self) -> str:
    def details(self) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return ""
        return ""

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def summary(self) -> str:
    def summary(self) -> str:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_key = self.input_key if self.input_key is not None else getattr(self, "input_keys", None)
        input_key = self.input_key if self.input_key is not None else getattr(self, "input_keys", None)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return (
        return (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"{self.__class__.__name__} \n\tinput key: {input_key}"
            f"{self.__class__.__name__} \n\tinput key: {input_key}"
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"\n\tParam count: {count_params(self, False)} \n\tTrainable: {self.is_trainable}"
            f"\n\tParam count: {count_params(self, False)} \n\tTrainable: {self.is_trainable}"
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"\n\tDropout rate: {self.dropout_rate}"
            f"\n\tDropout rate: {self.dropout_rate}"
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"\n\t{self.details()}"
            f"\n\t{self.details()}"
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class TextAttr(AbstractEmbModel):
class TextAttr(AbstractEmbModel):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, input_key: List[str], dropout_rate: Optional[float] = 0.0):
    def __init__(self, input_key: List[str], dropout_rate: Optional[float] = 0.0):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._input_key = input_key
        self._input_key = input_key
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._dropout_rate = dropout_rate
        self._dropout_rate = dropout_rate
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# self._dropout_rate = 0
        # self._dropout_rate = 0

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, token: torch.Tensor):
    def forward(self, token: torch.Tensor):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return {"crossattn_emb": token}
        return {"crossattn_emb": token}

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def random_dropout_input(
    def random_dropout_input(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, in_tensor: torch.Tensor, dropout_rate: Optional[float] = None, key: Optional[str] = None
        self, in_tensor: torch.Tensor, dropout_rate: Optional[float] = None, key: Optional[str] = None
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor:
    ) -> torch.Tensor:
        # 中文说明：根据条件选择执行分支；代码：if key is not None and "mask" in key:
        if key is not None and "mask" in key:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return in_tensor
            return in_tensor
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return super().random_dropout_input(in_tensor, dropout_rate, key)
        return super().random_dropout_input(in_tensor, dropout_rate, key)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def details(self) -> str:
    def details(self) -> str:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return "Output key: [crossattn_emb]"
        return "Output key: [crossattn_emb]"


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ReMapkey(AbstractEmbModel):
class ReMapkey(AbstractEmbModel):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：input_key: str,
        input_key: str,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：output_key: Optional[str] = None,
        output_key: Optional[str] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dropout_rate: Optional[float] = 0.0,
        dropout_rate: Optional[float] = 0.0,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dtype: Optional[str] = None,
        dtype: Optional[str] = None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.output_key = output_key
        self.output_key = output_key
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dtype = {
        self.dtype = {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：None: None,
            None: None,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："float": torch.float32,
            "float": torch.float32,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："bfloat16": torch.bfloat16,
            "bfloat16": torch.bfloat16,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："half": torch.float16,
            "half": torch.float16,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："float16": torch.float16,
            "float16": torch.float16,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："int": torch.int32,
            "int": torch.int32,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："long": torch.int64,
            "long": torch.int64,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}[dtype]
        }[dtype]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._input_key = input_key
        self._input_key = input_key
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._output_key = output_key
        self._output_key = output_key
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._dropout_rate = dropout_rate
        self._dropout_rate = dropout_rate

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, element: torch.Tensor) -> Dict[str, torch.Tensor]:
    def forward(self, element: torch.Tensor) -> Dict[str, torch.Tensor]:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：key = self.output_key if self.output_key else self.input_key
        key = self.output_key if self.output_key else self.input_key
        # 中文说明：根据条件选择执行分支；代码：if isinstance(element, torch.Tensor):
        if isinstance(element, torch.Tensor):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：element = element.to(dtype=self.dtype)
            element = element.to(dtype=self.dtype)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return {key: element}
        return {key: element}

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def details(self) -> str:
    def details(self) -> str:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：key = self.output_key if self.output_key else self.input_key
        key = self.output_key if self.output_key else self.input_key
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return f"Output key: {key} \n\tDtype: {self.dtype}"
        return f"Output key: {key} \n\tDtype: {self.dtype}"


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class BooleanFlag(AbstractEmbModel):
class BooleanFlag(AbstractEmbModel):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, input_key: str, output_key: Optional[str] = None, dropout_rate: Optional[f...
    def __init__(self, input_key: str, output_key: Optional[str] = None, dropout_rate: Optional[float] = 0.0):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._input_key = input_key
        self._input_key = input_key
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._dropout_rate = dropout_rate
        self._dropout_rate = dropout_rate
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.output_key = output_key
        self.output_key = output_key

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, *args, **kwargs) -> Dict[str, torch.Tensor]:
    def forward(self, *args, **kwargs) -> Dict[str, torch.Tensor]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del args, kwargs
        del args, kwargs
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：key = self.output_key if self.output_key else self.input_key
        key = self.output_key if self.output_key else self.input_key
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return {key: self.flag}
        return {key: self.flag}

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def random_dropout_input(
    def random_dropout_input(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, in_tensor: torch.Tensor, dropout_rate: Optional[float] = None, key: Optional[str] = None
        self, in_tensor: torch.Tensor, dropout_rate: Optional[float] = None, key: Optional[str] = None
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> torch.Tensor:
    ) -> torch.Tensor:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del key
        del key
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout_rate = dropout_rate if dropout_rate is not None else self.dropout_rate
        dropout_rate = dropout_rate if dropout_rate is not None else self.dropout_rate
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.flag = torch.bernoulli((1.0 - dropout_rate) * torch.ones(1)).bool().to(device=in_tensor....
        self.flag = torch.bernoulli((1.0 - dropout_rate) * torch.ones(1)).bool().to(device=in_tensor.device)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return in_tensor
        return in_tensor

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def details(self) -> str:
    def details(self) -> str:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：key = self.output_key if self.output_key else self.input_key
        key = self.output_key if self.output_key else self.input_key
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return f"Output key: {key} \n\t This is a boolean flag"
        return f"Output key: {key} \n\t This is a boolean flag"


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class GeneralConditioner(nn.Module, ABC):
class GeneralConditioner(nn.Module, ABC):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    An abstract module designed to handle various embedding models with conditional and unconditional configurations.
    This abstract base class initializes and manages a collection of embedders that can dynamically adjust
    their dropout rates based on conditioning.

    Attributes:
        KEY2DIM (dict): A mapping from output keys to dimensions used for concatenation.
        embedders (nn.ModuleDict): A dictionary containing all embedded models initialized and configured
                                   based on the provided configurations.

    Parameters:
        emb_models (Union[List, Any]): A dictionary where keys are embedder names and values are configurations
                                       for initializing the embedders.
    """

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：KEY2DIM = {"crossattn_emb": 1}
    KEY2DIM = {"crossattn_emb": 1}

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, **emb_models: Union[List, Any]):
    def __init__(self, **emb_models: Union[List, Any]):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.embedders = nn.ModuleDict()
        self.embedders = nn.ModuleDict()
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for n, (emb_name, emb_config) in enumerate(emb_models.items()):
        for n, (emb_name, emb_config) in enumerate(emb_models.items()):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：embedder = instantiate(emb_config)
            embedder = instantiate(emb_config)
            # 中文说明：检查运行时假设是否成立；代码：assert isinstance(
            assert isinstance(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：embedder, AbstractEmbModel
                embedder, AbstractEmbModel
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"embedder model {embedder.__class__.__name__} has to inherit from AbstractEmbModel"
            ), f"embedder model {embedder.__class__.__name__} has to inherit from AbstractEmbModel"
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：embedder.is_trainable = getattr(emb_config, "is_trainable", True)
            embedder.is_trainable = getattr(emb_config, "is_trainable", True)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：embedder.dropout_rate = getattr(emb_config, "dropout_rate", 0.0)
            embedder.dropout_rate = getattr(emb_config, "dropout_rate", 0.0)
            # 中文说明：根据条件选择执行分支；代码：if not embedder.is_trainable:
            if not embedder.is_trainable:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：embedder.train = disabled_train
                embedder.train = disabled_train
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for param in embedder.parameters():
                for param in embedder.parameters():
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：param.requires_grad = False
                    param.requires_grad = False
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：embedder.eval()
                embedder.eval()

            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(f"Initialized embedder #{n}-{emb_name}: \n {embedder.summary()}")
            log.debug(f"Initialized embedder #{n}-{emb_name}: \n {embedder.summary()}")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.embedders[emb_name] = embedder
            self.embedders[emb_name] = embedder

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@abstractmethod
    @abstractmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(
    def forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：batch: Dict,
        batch: Dict,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：override_dropout_rate: Optional[Dict[str, float]] = None,
        override_dropout_rate: Optional[Dict[str, float]] = None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Any:
    ) -> Any:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Should be implemented in subclasses to handle conditon datatype"""
        """Should be implemented in subclasses to handle conditon datatype"""
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise NotImplementedError
        raise NotImplementedError

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _forward(
    def _forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：batch: Dict,
        batch: Dict,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：override_dropout_rate: Optional[Dict[str, float]] = None,
        override_dropout_rate: Optional[Dict[str, float]] = None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Dict:
    ) -> Dict:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Processes the input batch through all configured embedders, applying conditional dropout rates if specified.
        Output tensors for each key are concatenated along the dimensions specified in KEY2DIM.

        Parameters:
            batch (Dict): The input data batch to process.
            override_dropout_rate (Optional[Dict[str, float]]): Optional dictionary to override default dropout rates
                                                                per embedder key.

        Returns:
            Dict: A dictionary of output tensors concatenated by specified dimensions.

        Note:
            In case the network code is sensitive to the order of concatenation, you can either control the order via \
            config file or make sure the embedders return a unique key for each output.
        """
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output = defaultdict(list)
        output = defaultdict(list)
        # 中文说明：根据条件选择执行分支；代码：if override_dropout_rate is None:
        if override_dropout_rate is None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：override_dropout_rate = {}
            override_dropout_rate = {}

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# make sure emb_name in override_dropout_rate is valid
        # make sure emb_name in override_dropout_rate is valid
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for emb_name in override_dropout_rate.keys():
        for emb_name in override_dropout_rate.keys():
            # 中文说明：检查运行时假设是否成立；代码：assert emb_name in self.embedders, f"invalid name found {emb_name}"
            assert emb_name in self.embedders, f"invalid name found {emb_name}"

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for emb_name, embedder in self.embedders.items():
        for emb_name, embedder in self.embedders.items():
            # 中文说明：根据条件选择执行分支；代码：if emb_name == 'text' and batch['t5_text_embeddings'].grad_fn is not None:
            if emb_name == 'text' and batch['t5_text_embeddings'].grad_fn is not None:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：embedding_context = nullcontext
                embedding_context = nullcontext
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：embedding_context = nullcontext if embedder.is_trainable else torch.no_grad
                embedding_context = nullcontext if embedder.is_trainable else torch.no_grad
            # 中文说明：处理异常、清理资源或管理上下文；代码：with embedding_context():
            with embedding_context():
                # 中文说明：根据条件选择执行分支；代码：if isinstance(embedder.input_key, str):
                if isinstance(embedder.input_key, str):
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：emb_out = embedder(
                    emb_out = embedder(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：embedder.random_dropout_input(
                        embedder.random_dropout_input(
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：batch[embedder.input_key], override_dropout_rate.get(emb_name, None)
                            batch[embedder.input_key], override_dropout_rate.get(emb_name, None)
                        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                        )
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                # 中文说明：根据条件选择执行分支；代码：elif isinstance(embedder.input_key, (list, omegaconf.listconfig.ListConfig)):
                elif isinstance(embedder.input_key, (list, omegaconf.listconfig.ListConfig)):
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：emb_out = embedder(
                    emb_out = embedder(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：*[
                        *[
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：embedder.random_dropout_input(batch.get(k), override_dropout_rate.get(emb_name, None), k)
                            embedder.random_dropout_input(batch.get(k), override_dropout_rate.get(emb_name, None), k)
                            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for k in embedder.input_key
                            for k in embedder.input_key
                        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
                        ]
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise KeyError(
                    raise KeyError(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Embedder '{embedder.__class__.__name__}' requires an 'input_key' attribute to be defined as...
                        f"Embedder '{embedder.__class__.__name__}' requires an 'input_key' attribute to be defined as either a string or list of strings"
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for k, v in emb_out.items():
            for k, v in emb_out.items():
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：output[k].append(v)
                output[k].append(v)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Concatenate the outputs
        # Concatenate the outputs
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return {k: torch.cat(v, dim=self.KEY2DIM.get(k, -1)) for k, v in output.items()}
        return {k: torch.cat(v, dim=self.KEY2DIM.get(k, -1)) for k, v in output.items()}

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_condition_uncondition(
    def get_condition_uncondition(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_batch: Dict,
        data_batch: Dict,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[Any, Any]:
    ) -> Tuple[Any, Any]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Processes the provided data batch to generate two sets of outputs: conditioned and unconditioned. This method
        manipulates the dropout rates of embedders to simulate two scenarios — one where all conditions are applied
        (conditioned), and one where they are removed or reduced to the minimum (unconditioned).

        This method first sets the dropout rates to zero for the conditioned scenario to fully apply the embedders' effects.
        For the unconditioned scenario, it sets the dropout rates to 1 (or to 0 if the initial unconditional dropout rate
        is insignificant) to minimize the embedders' influences, simulating an unconditioned generation.

        Parameters:
            data_batch (Dict): The input data batch that contains all necessary information for embedding processing. The
                            data is expected to match the required format and keys expected by the embedders.

        Returns:
            Tuple[Any, Any]: A tuple containing two condition:
                - The first one contains the outputs with all embedders fully applied (conditioned outputs).
                - The second one contains the outputs with embedders minimized or not applied (unconditioned outputs).
        """
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cond_dropout_rates, dropout_rates = {}, {}
        cond_dropout_rates, dropout_rates = {}, {}
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for emb_name, embedder in self.embedders.items():
        for emb_name, embedder in self.embedders.items():
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cond_dropout_rates[emb_name] = 0.0
            cond_dropout_rates[emb_name] = 0.0
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout_rates[emb_name] = 1.0 if embedder.dropout_rate > 1e-4 else 0.0
            dropout_rates[emb_name] = 1.0 if embedder.dropout_rate > 1e-4 else 0.0

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：condition: Any = self(data_batch, override_dropout_rate=cond_dropout_rates)
        condition: Any = self(data_batch, override_dropout_rate=cond_dropout_rates)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：un_condition: Any = self(data_batch, override_dropout_rate=dropout_rates)
        un_condition: Any = self(data_batch, override_dropout_rate=dropout_rates)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return condition, un_condition
        return condition, un_condition

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_condition_with_negative_prompt(
    def get_condition_with_negative_prompt(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data_batch: Dict,
        data_batch: Dict,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[Any, Any]:
    ) -> Tuple[Any, Any]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Similar functionality as get_condition_uncondition
        But use negative prompts for unconditon
        """
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cond_dropout_rates, uncond_dropout_rates = {}, {}
        cond_dropout_rates, uncond_dropout_rates = {}, {}
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for emb_name, embedder in self.embedders.items():
        for emb_name, embedder in self.embedders.items():
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cond_dropout_rates[emb_name] = 0.0
            cond_dropout_rates[emb_name] = 0.0
            # 中文说明：根据条件选择执行分支；代码：if isinstance(embedder, TextAttr):
            if isinstance(embedder, TextAttr):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：uncond_dropout_rates[emb_name] = 0.0
                uncond_dropout_rates[emb_name] = 0.0
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：uncond_dropout_rates[emb_name] = 1.0 if embedder.dropout_rate > 1e-4 else 0.0
                uncond_dropout_rates[emb_name] = 1.0 if embedder.dropout_rate > 1e-4 else 0.0

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch_neg_prompt = copy.deepcopy(data_batch)
        data_batch_neg_prompt = copy.deepcopy(data_batch)
        # 中文说明：根据条件选择执行分支；代码：if "neg_t5_text_embeddings" in data_batch_neg_prompt:
        if "neg_t5_text_embeddings" in data_batch_neg_prompt:
            # 中文说明：根据条件选择执行分支；代码：if isinstance(data_batch_neg_prompt["neg_t5_text_embeddings"], torch.Tensor):
            if isinstance(data_batch_neg_prompt["neg_t5_text_embeddings"], torch.Tensor):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_batch_neg_prompt["t5_text_embeddings"] = data_batch_neg_prompt["neg_t5_text_embeddings"]
                data_batch_neg_prompt["t5_text_embeddings"] = data_batch_neg_prompt["neg_t5_text_embeddings"]

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：condition: Any = self(data_batch, override_dropout_rate=cond_dropout_rates)
        condition: Any = self(data_batch, override_dropout_rate=cond_dropout_rates)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：un_condition: Any = self(data_batch_neg_prompt, override_dropout_rate=uncond_dropout_rates)
        un_condition: Any = self(data_batch_neg_prompt, override_dropout_rate=uncond_dropout_rates)

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return condition, un_condition
        return condition, un_condition


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class VideoConditioner(GeneralConditioner):
class VideoConditioner(GeneralConditioner):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(
    def forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：batch: Dict,
        batch: Dict,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：override_dropout_rate: Optional[Dict[str, float]] = None,
        override_dropout_rate: Optional[Dict[str, float]] = None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> T2VCondition:
    ) -> T2VCondition:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output = super()._forward(batch, override_dropout_rate)
        output = super()._forward(batch, override_dropout_rate)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return T2VCondition(**output)
        return T2VCondition(**output)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class GR00TV1Img2VidConditioner(GeneralConditioner):
class GR00TV1Img2VidConditioner(GeneralConditioner):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(
    def forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：batch: Dict,
        batch: Dict,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：override_dropout_rate: Optional[Dict[str, float]] = None,
        override_dropout_rate: Optional[Dict[str, float]] = None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> GR00TV1Img2VidCondition:
    ) -> GR00TV1Img2VidCondition:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output = super()._forward(batch, override_dropout_rate)
        output = super()._forward(batch, override_dropout_rate)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return GR00TV1Img2VidCondition(**output)
        return GR00TV1Img2VidCondition(**output)
