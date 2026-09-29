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
# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""The patcher and unpatcher implementation for 2D and 3D data.
"""The patcher and unpatcher implementation for 2D and 3D data.

The idea of Haar wavelet is to compute LL, LH, HL, HH component as two 1D convolutions.
One on the rows and one on the columns.
For example, in 1D signal, we have [a, b], then the low-freq compoenent is [a + b] / 2 and high-freq is [a - b] / 2.
We can use a 1D convolution with kernel [1, 1] and stride 2 to represent the L component.
For H component, we can use a 1D convolution with kernel [1, -1] and stride 2.
Although in principle, we typically only do additional Haar wavelet over the LL component. But here we do it for all
   as we need to support downsampling for more than 2x.
For example, 4x downsampling can be done by 2x Haar and additional 2x Haar, and the shape would be.
   [3, 256, 256] -> [12, 128, 128] -> [48, 64, 64]
"""

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.nn.functional as F
import torch.nn.functional as F
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from einops import rearrange
from einops import rearrange

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_WAVELETS = {
_WAVELETS = {
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："haar": torch.tensor([0.7071067811865476, 0.7071067811865476]),
    "haar": torch.tensor([0.7071067811865476, 0.7071067811865476]),
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："rearrange": torch.tensor([1.0, 1.0]),
    "rearrange": torch.tensor([1.0, 1.0]),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
}
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_PERSISTENT = True
_PERSISTENT = True


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Patcher(torch.nn.Module):
class Patcher(torch.nn.Module):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""A module to convert image tensors into patches using torch operations.
    """A module to convert image tensors into patches using torch operations.

    The main difference from `class Patching` is that this module implements
    all operations using torch, rather than python or numpy, for efficiency purpose.

    It's bit-wise identical to the Patching module outputs, with the added
    benefit of being torch.jit scriptable.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, patch_size=1, patch_method="haar"):
    def __init__(self, patch_size=1, patch_method="haar"):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.patch_size = patch_size
        self.patch_size = patch_size
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.patch_method = patch_method
        self.patch_method = patch_method
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.register_buffer("wavelets", _WAVELETS[patch_method], persistent=_PERSISTENT)
        self.register_buffer("wavelets", _WAVELETS[patch_method], persistent=_PERSISTENT)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.range = range(int(torch.log2(torch.tensor(self.patch_size)).item()))
        self.range = range(int(torch.log2(torch.tensor(self.patch_size)).item()))
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.register_buffer(
        self.register_buffer(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："_arange",
            "_arange",
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.arange(_WAVELETS[patch_method].shape[0]),
            torch.arange(_WAVELETS[patch_method].shape[0]),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：persistent=_PERSISTENT,
            persistent=_PERSISTENT,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for param in self.parameters():
        for param in self.parameters():
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：param.requires_grad = False
            param.requires_grad = False

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x):
    def forward(self, x):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：根据条件选择执行分支；代码：if self.patch_method == "haar":
        if self.patch_method == "haar":
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return self._haar(x)
            return self._haar(x)
        # 中文说明：根据条件选择执行分支；代码：elif self.patch_method == "rearrange":
        elif self.patch_method == "rearrange":
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return self._arrange(x)
            return self._arrange(x)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError("Unknown patch method: " + self.patch_method)
            raise ValueError("Unknown patch method: " + self.patch_method)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _dwt(self, x, mode="reflect", rescale=False):
    def _dwt(self, x, mode="reflect", rescale=False):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dtype = x.dtype
        dtype = x.dtype
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.wavelets
        h = self.wavelets

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n = h.shape[0]
        n = h.shape[0]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：g = x.shape[1]
        g = x.shape[1]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hl = h.flip(0).reshape(1, 1, -1).repeat(g, 1, 1)
        hl = h.flip(0).reshape(1, 1, -1).repeat(g, 1, 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hh = (h * ((-1) ** self._arange)).reshape(1, 1, -1).repeat(g, 1, 1)
        hh = (h * ((-1) ** self._arange)).reshape(1, 1, -1).repeat(g, 1, 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hh = hh.to(dtype=dtype)
        hh = hh.to(dtype=dtype)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hl = hl.to(dtype=dtype)
        hl = hl.to(dtype=dtype)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = F.pad(x, pad=(n - 2, n - 1, n - 2, n - 1), mode=mode).to(dtype)
        x = F.pad(x, pad=(n - 2, n - 1, n - 2, n - 1), mode=mode).to(dtype)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xl = F.conv2d(x, hl.unsqueeze(2), groups=g, stride=(1, 2))
        xl = F.conv2d(x, hl.unsqueeze(2), groups=g, stride=(1, 2))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xh = F.conv2d(x, hh.unsqueeze(2), groups=g, stride=(1, 2))
        xh = F.conv2d(x, hh.unsqueeze(2), groups=g, stride=(1, 2))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xll = F.conv2d(xl, hl.unsqueeze(3), groups=g, stride=(2, 1))
        xll = F.conv2d(xl, hl.unsqueeze(3), groups=g, stride=(2, 1))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xlh = F.conv2d(xl, hh.unsqueeze(3), groups=g, stride=(2, 1))
        xlh = F.conv2d(xl, hh.unsqueeze(3), groups=g, stride=(2, 1))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xhl = F.conv2d(xh, hl.unsqueeze(3), groups=g, stride=(2, 1))
        xhl = F.conv2d(xh, hl.unsqueeze(3), groups=g, stride=(2, 1))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xhh = F.conv2d(xh, hh.unsqueeze(3), groups=g, stride=(2, 1))
        xhh = F.conv2d(xh, hh.unsqueeze(3), groups=g, stride=(2, 1))

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out = torch.cat([xll, xlh, xhl, xhh], dim=1)
        out = torch.cat([xll, xlh, xhl, xhh], dim=1)
        # 中文说明：根据条件选择执行分支；代码：if rescale:
        if rescale:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out = out / 2
            out = out / 2
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return out
        return out

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _haar(self, x):
    def _haar(self, x):
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _ in self.range:
        for _ in self.range:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self._dwt(x, rescale=True)
            x = self._dwt(x, rescale=True)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x
        return x

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _arrange(self, x):
    def _arrange(self, x):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = rearrange(
        x = rearrange(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x,
            x,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："b c (h p1) (w p2) -> b (c p1 p2) h w",
            "b c (h p1) (w p2) -> b (c p1 p2) h w",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：p1=self.patch_size,
            p1=self.patch_size,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：p2=self.patch_size,
            p2=self.patch_size,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：).contiguous()
        ).contiguous()
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x
        return x


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Patcher3D(Patcher):
class Patcher3D(Patcher):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""A 3D discrete wavelet transform for video data, expects 5D tensor, i.e. a batch of videos."""
    """A 3D discrete wavelet transform for video data, expects 5D tensor, i.e. a batch of videos."""

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, patch_size=1, patch_method="haar"):
    def __init__(self, patch_size=1, patch_method="haar"):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(patch_method=patch_method, patch_size=patch_size)
        super().__init__(patch_method=patch_method, patch_size=patch_size)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.register_buffer(
        self.register_buffer(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："patch_size_buffer",
            "patch_size_buffer",
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：patch_size * torch.ones([1], dtype=torch.int32),
            patch_size * torch.ones([1], dtype=torch.int32),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：persistent=_PERSISTENT,
            persistent=_PERSISTENT,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _dwt(self, x, wavelet, mode="reflect", rescale=False):
    def _dwt(self, x, wavelet, mode="reflect", rescale=False):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dtype = x.dtype
        dtype = x.dtype
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.wavelets
        h = self.wavelets

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n = h.shape[0]
        n = h.shape[0]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：g = x.shape[1]
        g = x.shape[1]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hl = h.flip(0).reshape(1, 1, -1).repeat(g, 1, 1)
        hl = h.flip(0).reshape(1, 1, -1).repeat(g, 1, 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hh = (h * ((-1) ** self._arange)).reshape(1, 1, -1).repeat(g, 1, 1)
        hh = (h * ((-1) ** self._arange)).reshape(1, 1, -1).repeat(g, 1, 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hh = hh.to(dtype=dtype)
        hh = hh.to(dtype=dtype)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hl = hl.to(dtype=dtype)
        hl = hl.to(dtype=dtype)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Handles temporal axis.
        # Handles temporal axis.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = F.pad(x, pad=(max(0, n - 2), n - 1, n - 2, n - 1, n - 2, n - 1), mode=mode).to(dtype)
        x = F.pad(x, pad=(max(0, n - 2), n - 1, n - 2, n - 1, n - 2, n - 1), mode=mode).to(dtype)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xl = F.conv3d(x, hl.unsqueeze(3).unsqueeze(4), groups=g, stride=(2, 1, 1))
        xl = F.conv3d(x, hl.unsqueeze(3).unsqueeze(4), groups=g, stride=(2, 1, 1))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xh = F.conv3d(x, hh.unsqueeze(3).unsqueeze(4), groups=g, stride=(2, 1, 1))
        xh = F.conv3d(x, hh.unsqueeze(3).unsqueeze(4), groups=g, stride=(2, 1, 1))

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Handles spatial axes.
        # Handles spatial axes.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xll = F.conv3d(xl, hl.unsqueeze(2).unsqueeze(4), groups=g, stride=(1, 2, 1))
        xll = F.conv3d(xl, hl.unsqueeze(2).unsqueeze(4), groups=g, stride=(1, 2, 1))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xlh = F.conv3d(xl, hh.unsqueeze(2).unsqueeze(4), groups=g, stride=(1, 2, 1))
        xlh = F.conv3d(xl, hh.unsqueeze(2).unsqueeze(4), groups=g, stride=(1, 2, 1))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xhl = F.conv3d(xh, hl.unsqueeze(2).unsqueeze(4), groups=g, stride=(1, 2, 1))
        xhl = F.conv3d(xh, hl.unsqueeze(2).unsqueeze(4), groups=g, stride=(1, 2, 1))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xhh = F.conv3d(xh, hh.unsqueeze(2).unsqueeze(4), groups=g, stride=(1, 2, 1))
        xhh = F.conv3d(xh, hh.unsqueeze(2).unsqueeze(4), groups=g, stride=(1, 2, 1))

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xlll = F.conv3d(xll, hl.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))
        xlll = F.conv3d(xll, hl.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xllh = F.conv3d(xll, hh.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))
        xllh = F.conv3d(xll, hh.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xlhl = F.conv3d(xlh, hl.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))
        xlhl = F.conv3d(xlh, hl.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xlhh = F.conv3d(xlh, hh.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))
        xlhh = F.conv3d(xlh, hh.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xhll = F.conv3d(xhl, hl.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))
        xhll = F.conv3d(xhl, hl.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xhlh = F.conv3d(xhl, hh.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))
        xhlh = F.conv3d(xhl, hh.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xhhl = F.conv3d(xhh, hl.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))
        xhhl = F.conv3d(xhh, hl.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xhhh = F.conv3d(xhh, hh.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))
        xhhh = F.conv3d(xhh, hh.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out = torch.cat([xlll, xllh, xlhl, xlhh, xhll, xhlh, xhhl, xhhh], dim=1)
        out = torch.cat([xlll, xllh, xlhl, xlhh, xhll, xhlh, xhhl, xhhh], dim=1)
        # 中文说明：根据条件选择执行分支；代码：if rescale:
        if rescale:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out = out / (2 * torch.sqrt(torch.tensor(2.0)))
            out = out / (2 * torch.sqrt(torch.tensor(2.0)))
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return out
        return out

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _haar(self, x):
    def _haar(self, x):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：xi, xv = torch.split(x, [1, x.shape[2] - 1], dim=2)
        xi, xv = torch.split(x, [1, x.shape[2] - 1], dim=2)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = torch.cat([xi.repeat_interleave(self.patch_size, dim=2), xv], dim=2)
        x = torch.cat([xi.repeat_interleave(self.patch_size, dim=2), xv], dim=2)
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _ in self.range:
        for _ in self.range:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self._dwt(x, "haar", rescale=True)
            x = self._dwt(x, "haar", rescale=True)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x
        return x

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _arrange(self, x):
    def _arrange(self, x):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：xi, xv = torch.split(x, [1, x.shape[2] - 1], dim=2)
        xi, xv = torch.split(x, [1, x.shape[2] - 1], dim=2)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = torch.cat([xi.repeat_interleave(self.patch_size, dim=2), xv], dim=2)
        x = torch.cat([xi.repeat_interleave(self.patch_size, dim=2), xv], dim=2)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = rearrange(
        x = rearrange(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x,
            x,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："b c (t p1) (h p2) (w p3) -> b (c p1 p2 p3) t h w",
            "b c (t p1) (h p2) (w p3) -> b (c p1 p2 p3) t h w",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：p1=self.patch_size,
            p1=self.patch_size,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：p2=self.patch_size,
            p2=self.patch_size,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：p3=self.patch_size,
            p3=self.patch_size,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：).contiguous()
        ).contiguous()
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x
        return x


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class UnPatcher(torch.nn.Module):
class UnPatcher(torch.nn.Module):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""A module to convert patches into image tensorsusing torch operations.
    """A module to convert patches into image tensorsusing torch operations.

    The main difference from `class Unpatching` is that this module implements
    all operations using torch, rather than python or numpy, for efficiency purpose.

    It's bit-wise identical to the Unpatching module outputs, with the added
    benefit of being torch.jit scriptable.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, patch_size=1, patch_method="haar"):
    def __init__(self, patch_size=1, patch_method="haar"):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.patch_size = patch_size
        self.patch_size = patch_size
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.patch_method = patch_method
        self.patch_method = patch_method
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.register_buffer("wavelets", _WAVELETS[patch_method], persistent=_PERSISTENT)
        self.register_buffer("wavelets", _WAVELETS[patch_method], persistent=_PERSISTENT)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.range = range(int(torch.log2(torch.tensor(self.patch_size)).item()))
        self.range = range(int(torch.log2(torch.tensor(self.patch_size)).item()))
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.register_buffer(
        self.register_buffer(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："_arange",
            "_arange",
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.arange(_WAVELETS[patch_method].shape[0]),
            torch.arange(_WAVELETS[patch_method].shape[0]),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：persistent=_PERSISTENT,
            persistent=_PERSISTENT,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for param in self.parameters():
        for param in self.parameters():
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：param.requires_grad = False
            param.requires_grad = False

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, x):
    def forward(self, x):
        # 中文说明：根据条件选择执行分支；代码：if self.patch_method == "haar":
        if self.patch_method == "haar":
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return self._ihaar(x)
            return self._ihaar(x)
        # 中文说明：根据条件选择执行分支；代码：elif self.patch_method == "rearrange":
        elif self.patch_method == "rearrange":
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return self._iarrange(x)
            return self._iarrange(x)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError("Unknown patch method: " + self.patch_method)
            raise ValueError("Unknown patch method: " + self.patch_method)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _idwt(self, x, wavelet="haar", mode="reflect", rescale=False):
    def _idwt(self, x, wavelet="haar", mode="reflect", rescale=False):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dtype = x.dtype
        dtype = x.dtype
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.wavelets
        h = self.wavelets
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n = h.shape[0]
        n = h.shape[0]

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：g = x.shape[1] // 4
        g = x.shape[1] // 4
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hl = h.flip([0]).reshape(1, 1, -1).repeat([g, 1, 1])
        hl = h.flip([0]).reshape(1, 1, -1).repeat([g, 1, 1])
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hh = (h * ((-1) ** self._arange)).reshape(1, 1, -1).repeat(g, 1, 1)
        hh = (h * ((-1) ** self._arange)).reshape(1, 1, -1).repeat(g, 1, 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hh = hh.to(dtype=dtype)
        hh = hh.to(dtype=dtype)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hl = hl.to(dtype=dtype)
        hl = hl.to(dtype=dtype)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：xll, xlh, xhl, xhh = torch.chunk(x.to(dtype), 4, dim=1)
        xll, xlh, xhl, xhh = torch.chunk(x.to(dtype), 4, dim=1)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Inverse transform.
        # Inverse transform.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：yl = torch.nn.functional.conv_transpose2d(xll, hl.unsqueeze(3), groups=g, stride=(2, 1), padd...
        yl = torch.nn.functional.conv_transpose2d(xll, hl.unsqueeze(3), groups=g, stride=(2, 1), padding=(n - 2, 0))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：yl += torch.nn.functional.conv_transpose2d(xlh, hh.unsqueeze(3), groups=g, stride=(2, 1), pad...
        yl += torch.nn.functional.conv_transpose2d(xlh, hh.unsqueeze(3), groups=g, stride=(2, 1), padding=(n - 2, 0))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：yh = torch.nn.functional.conv_transpose2d(xhl, hl.unsqueeze(3), groups=g, stride=(2, 1), padd...
        yh = torch.nn.functional.conv_transpose2d(xhl, hl.unsqueeze(3), groups=g, stride=(2, 1), padding=(n - 2, 0))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：yh += torch.nn.functional.conv_transpose2d(xhh, hh.unsqueeze(3), groups=g, stride=(2, 1), pad...
        yh += torch.nn.functional.conv_transpose2d(xhh, hh.unsqueeze(3), groups=g, stride=(2, 1), padding=(n - 2, 0))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：y = torch.nn.functional.conv_transpose2d(yl, hl.unsqueeze(2), groups=g, stride=(1, 2), paddin...
        y = torch.nn.functional.conv_transpose2d(yl, hl.unsqueeze(2), groups=g, stride=(1, 2), padding=(0, n - 2))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：y += torch.nn.functional.conv_transpose2d(yh, hh.unsqueeze(2), groups=g, stride=(1, 2), paddi...
        y += torch.nn.functional.conv_transpose2d(yh, hh.unsqueeze(2), groups=g, stride=(1, 2), padding=(0, n - 2))

        # 中文说明：根据条件选择执行分支；代码：if rescale:
        if rescale:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：y = y * 2
            y = y * 2
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return y
        return y

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _ihaar(self, x):
    def _ihaar(self, x):
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _ in self.range:
        for _ in self.range:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self._idwt(x, "haar", rescale=True)
            x = self._idwt(x, "haar", rescale=True)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x
        return x

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _iarrange(self, x):
    def _iarrange(self, x):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = rearrange(
        x = rearrange(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x,
            x,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："b (c p1 p2) h w -> b c (h p1) (w p2)",
            "b (c p1 p2) h w -> b c (h p1) (w p2)",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：p1=self.patch_size,
            p1=self.patch_size,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：p2=self.patch_size,
            p2=self.patch_size,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x
        return x


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class UnPatcher3D(UnPatcher):
class UnPatcher3D(UnPatcher):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""A 3D inverse discrete wavelet transform for video wavelet decompositions."""
    """A 3D inverse discrete wavelet transform for video wavelet decompositions."""

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, patch_size=1, patch_method="haar"):
    def __init__(self, patch_size=1, patch_method="haar"):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(patch_method=patch_method, patch_size=patch_size)
        super().__init__(patch_method=patch_method, patch_size=patch_size)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _idwt(self, x, wavelet="haar", mode="reflect", rescale=False):
    def _idwt(self, x, wavelet="haar", mode="reflect", rescale=False):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dtype = x.dtype
        dtype = x.dtype
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.wavelets
        h = self.wavelets
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：n = h.shape[0]
        n = h.shape[0]

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：g = x.shape[1] // 8 # split into 8 spatio-temporal filtered tesnors.
        g = x.shape[1] // 8  # split into 8 spatio-temporal filtered tesnors.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hl = h.flip([0]).reshape(1, 1, -1).repeat([g, 1, 1])
        hl = h.flip([0]).reshape(1, 1, -1).repeat([g, 1, 1])
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hh = (h * ((-1) ** self._arange)).reshape(1, 1, -1).repeat(g, 1, 1)
        hh = (h * ((-1) ** self._arange)).reshape(1, 1, -1).repeat(g, 1, 1)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hl = hl.to(dtype=dtype)
        hl = hl.to(dtype=dtype)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hh = hh.to(dtype=dtype)
        hh = hh.to(dtype=dtype)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：xlll, xllh, xlhl, xlhh, xhll, xhlh, xhhl, xhhh = torch.chunk(x, 8, dim=1)
        xlll, xllh, xlhl, xlhh, xhll, xhlh, xhhl, xhhh = torch.chunk(x, 8, dim=1)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Height height transposed convolutions.
        # Height height transposed convolutions.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xll = F.conv_transpose3d(xlll, hl.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))
        xll = F.conv_transpose3d(xlll, hl.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xll += F.conv_transpose3d(xllh, hh.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))
        xll += F.conv_transpose3d(xllh, hh.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xlh = F.conv_transpose3d(xlhl, hl.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))
        xlh = F.conv_transpose3d(xlhl, hl.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xlh += F.conv_transpose3d(xlhh, hh.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))
        xlh += F.conv_transpose3d(xlhh, hh.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xhl = F.conv_transpose3d(xhll, hl.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))
        xhl = F.conv_transpose3d(xhll, hl.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xhl += F.conv_transpose3d(xhlh, hh.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))
        xhl += F.conv_transpose3d(xhlh, hh.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xhh = F.conv_transpose3d(xhhl, hl.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))
        xhh = F.conv_transpose3d(xhhl, hl.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xhh += F.conv_transpose3d(xhhh, hh.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))
        xhh += F.conv_transpose3d(xhhh, hh.unsqueeze(2).unsqueeze(3), groups=g, stride=(1, 1, 2))

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Handles width transposed convolutions.
        # Handles width transposed convolutions.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xl = F.conv_transpose3d(xll, hl.unsqueeze(2).unsqueeze(4), groups=g, stride=(1, 2, 1))
        xl = F.conv_transpose3d(xll, hl.unsqueeze(2).unsqueeze(4), groups=g, stride=(1, 2, 1))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xl += F.conv_transpose3d(xlh, hh.unsqueeze(2).unsqueeze(4), groups=g, stride=(1, 2, 1))
        xl += F.conv_transpose3d(xlh, hh.unsqueeze(2).unsqueeze(4), groups=g, stride=(1, 2, 1))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xh = F.conv_transpose3d(xhl, hl.unsqueeze(2).unsqueeze(4), groups=g, stride=(1, 2, 1))
        xh = F.conv_transpose3d(xhl, hl.unsqueeze(2).unsqueeze(4), groups=g, stride=(1, 2, 1))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：xh += F.conv_transpose3d(xhh, hh.unsqueeze(2).unsqueeze(4), groups=g, stride=(1, 2, 1))
        xh += F.conv_transpose3d(xhh, hh.unsqueeze(2).unsqueeze(4), groups=g, stride=(1, 2, 1))

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Handles time axis transposed convolutions.
        # Handles time axis transposed convolutions.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = F.conv_transpose3d(xl, hl.unsqueeze(3).unsqueeze(4), groups=g, stride=(2, 1, 1))
        x = F.conv_transpose3d(xl, hl.unsqueeze(3).unsqueeze(4), groups=g, stride=(2, 1, 1))
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x += F.conv_transpose3d(xh, hh.unsqueeze(3).unsqueeze(4), groups=g, stride=(2, 1, 1))
        x += F.conv_transpose3d(xh, hh.unsqueeze(3).unsqueeze(4), groups=g, stride=(2, 1, 1))

        # 中文说明：根据条件选择执行分支；代码：if rescale:
        if rescale:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = x * (2 * torch.sqrt(torch.tensor(2.0)))
            x = x * (2 * torch.sqrt(torch.tensor(2.0)))
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x
        return x

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _ihaar(self, x):
    def _ihaar(self, x):
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _ in self.range:
        for _ in self.range:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = self._idwt(x, "haar", rescale=True)
            x = self._idwt(x, "haar", rescale=True)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = x[:, :, self.patch_size - 1 :, ...]
        x = x[:, :, self.patch_size - 1 :, ...]
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x
        return x

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _iarrange(self, x):
    def _iarrange(self, x):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = rearrange(
        x = rearrange(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x,
            x,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："b (c p1 p2 p3) t h w -> b c (t p1) (h p2) (w p3)",
            "b (c p1 p2 p3) t h w -> b c (t p1) (h p2) (w p3)",
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：p1=self.patch_size,
            p1=self.patch_size,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：p2=self.patch_size,
            p2=self.patch_size,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：p3=self.patch_size,
            p3=self.patch_size,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x = x[:, :, self.patch_size - 1 :, ...]
        x = x[:, :, self.patch_size - 1 :, ...]
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x
        return x
