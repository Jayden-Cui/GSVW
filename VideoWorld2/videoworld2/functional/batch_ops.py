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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch import Tensor
from torch import Tensor


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def common_broadcast(x: Tensor, y: Tensor) -> tuple[Tensor, Tensor]:
def common_broadcast(x: Tensor, y: Tensor) -> tuple[Tensor, Tensor]:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ndims1 = x.ndim
    ndims1 = x.ndim
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ndims2 = y.ndim
    ndims2 = y.ndim

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：common_ndims = min(ndims1, ndims2)
    common_ndims = min(ndims1, ndims2)
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for axis in range(common_ndims):
    for axis in range(common_ndims):
        # 中文说明：检查运行时假设是否成立；代码：assert x.shape[axis] == y.shape[axis], "Dimensions not equal at axis {}".format(axis)
        assert x.shape[axis] == y.shape[axis], "Dimensions not equal at axis {}".format(axis)

    # 中文说明：根据条件选择执行分支；代码：if ndims1 < ndims2:
    if ndims1 < ndims2:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = x.reshape(x.shape + (1,) * (ndims2 - ndims1))
        x = x.reshape(x.shape + (1,) * (ndims2 - ndims1))
    # 中文说明：根据条件选择执行分支；代码：elif ndims2 < ndims1:
    elif ndims2 < ndims1:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：y = y.reshape(y.shape + (1,) * (ndims1 - ndims2))
        y = y.reshape(y.shape + (1,) * (ndims1 - ndims2))

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return x, y
    return x, y


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def batch_add(x: Tensor, y: Tensor) -> Tensor:
def batch_add(x: Tensor, y: Tensor) -> Tensor:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x, y = common_broadcast(x, y)
    x, y = common_broadcast(x, y)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return x + y
    return x + y


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def batch_mul(x: Tensor, y: Tensor) -> Tensor:
def batch_mul(x: Tensor, y: Tensor) -> Tensor:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x, y = common_broadcast(x, y)
    x, y = common_broadcast(x, y)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return x * y
    return x * y


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def batch_sub(x: Tensor, y: Tensor) -> Tensor:
def batch_sub(x: Tensor, y: Tensor) -> Tensor:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x, y = common_broadcast(x, y)
    x, y = common_broadcast(x, y)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return x - y
    return x - y


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def batch_div(x: Tensor, y: Tensor) -> Tensor:
def batch_div(x: Tensor, y: Tensor) -> Tensor:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x, y = common_broadcast(x, y)
    x, y = common_broadcast(x, y)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return x / y
    return x / y
