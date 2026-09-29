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
# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""LPIPS loss.
"""LPIPS loss.

Adapted from: github.com/CompVis/stable-diffusion/ldm/modules/losses/contperceptual.py.
"""

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import hashlib
import hashlib
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from collections import namedtuple
from collections import namedtuple

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import requests
import requests
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.distributed as dist
import torch.distributed as dist
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.nn as nn
import torch.nn as nn
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.utils.checkpoint as checkpoint
import torch.utils.checkpoint as checkpoint
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from loguru import logger as logging
from loguru import logger as logging
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torchvision import models
from torchvision import models
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from tqdm import tqdm
from tqdm import tqdm
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.distributed as dist
import torch.distributed as dist

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_TORCH_HOME = os.getenv("TORCH_HOME", "/opt/tiger/.cache/torch")
_TORCH_HOME = os.getenv("TORCH_HOME", "/opt/tiger/.cache/torch")
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_URL_MAP = {"vgg_lpips": "https://heibox.uni-heidelberg.de/f/607503859c864bc1b30b/?dl=1"}
_URL_MAP = {"vgg_lpips": "https://heibox.uni-heidelberg.de/f/607503859c864bc1b30b/?dl=1"}
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_CKPT_MAP = {"vgg_lpips": "vgg.pth"}
_CKPT_MAP = {"vgg_lpips": "vgg.pth"}
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_MD5_MAP = {"vgg_lpips": "d507d7349b931f0638a25a48a722f98a"}
_MD5_MAP = {"vgg_lpips": "d507d7349b931f0638a25a48a722f98a"}

# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_rank(group= None) -> int:
def get_rank(group= None) -> int:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Get the rank (GPU device) of the worker.
    """Get the rank (GPU device) of the worker.

    Returns:
        rank (int): The rank of the worker.
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank = 0
    rank = 0
    # 中文说明：根据条件选择执行分支；代码：if dist.is_available() and dist.is_initialized():
    if dist.is_available() and dist.is_initialized():
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank = dist.get_rank(group)
        rank = dist.get_rank(group)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return rank
    return rank

# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_rank0() -> bool:
def is_rank0() -> bool:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Check if current process is the master GPU.
    """Check if current process is the master GPU.

    Returns:
        (bool): True if this function is called from the master GPU, else False.
    """
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return get_rank() == 0
    return get_rank() == 0


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _download(url, local_path, chunk_size=1024):
def _download(url, local_path, chunk_size=1024):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.makedirs(os.path.split(local_path)[0], exist_ok=True)
    os.makedirs(os.path.split(local_path)[0], exist_ok=True)
    # 中文说明：处理异常、清理资源或管理上下文；代码：with requests.get(url, stream=True) as r:
    with requests.get(url, stream=True) as r:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：total_size = int(r.headers.get("content-length", 0))
        total_size = int(r.headers.get("content-length", 0))
        # 中文说明：处理异常、清理资源或管理上下文；代码：with tqdm(total=total_size, unit="B", unit_scale=True) as pbar:
        with tqdm(total=total_size, unit="B", unit_scale=True) as pbar:
            # 中文说明：处理异常、清理资源或管理上下文；代码：with open(local_path, "wb") as f:
            with open(local_path, "wb") as f:
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for data in r.iter_content(chunk_size=chunk_size):
                for data in r.iter_content(chunk_size=chunk_size):
                    # 中文说明：根据条件选择执行分支；代码：if data:
                    if data:
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f.write(data)
                        f.write(data)
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pbar.update(chunk_size)
                        pbar.update(chunk_size)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _md5_hash(path):
def _md5_hash(path):
    # 中文说明：处理异常、清理资源或管理上下文；代码：with open(path, "rb") as f:
    with open(path, "rb") as f:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：content = f.read()
        content = f.read()
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return hashlib.md5(content).hexdigest()
    return hashlib.md5(content).hexdigest()


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _get_ckpt_path(name, root, check=False):
def _get_ckpt_path(name, root, check=False):
    # 中文说明：检查运行时假设是否成立；代码：assert name in _URL_MAP
    assert name in _URL_MAP
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：path = os.path.join(root, _CKPT_MAP[name])
    path = os.path.join(root, _CKPT_MAP[name])
    # 中文说明：根据条件选择执行分支；代码：if not os.path.exists(path) or (check and not _md5_hash(path) == _MD5_MAP[name]):
    if not os.path.exists(path) or (check and not _md5_hash(path) == _MD5_MAP[name]):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：logging.info("Downloading {} model from {} to {}".format(name, _URL_MAP[name], path))
        logging.info("Downloading {} model from {} to {}".format(name, _URL_MAP[name], path))
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_download(_URL_MAP[name], path)
        _download(_URL_MAP[name], path)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：md5 = _md5_hash(path)
        md5 = _md5_hash(path)
        # 中文说明：检查运行时假设是否成立；代码：assert md5 == _MD5_MAP[name], md5
        assert md5 == _MD5_MAP[name], md5
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return path
    return path


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class LPIPS(nn.Module):
class LPIPS(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, checkpoint_activations: bool = False):
    def __init__(self, checkpoint_activations: bool = False):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.scaling_layer = ScalingLayer()
        self.scaling_layer = ScalingLayer()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.chns = [64, 128, 256, 512, 512] # vg16 features
        self.chns = [64, 128, 256, 512, 512]  # vg16 features
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.net = vgg16(pretrained=True, requires_grad=False, checkpoint_activations=checkpoint_acti...
        self.net = vgg16(pretrained=True, requires_grad=False, checkpoint_activations=checkpoint_activations)

        # 中文说明：根据条件选择执行分支；代码：if dist.is_initialized() and not is_rank0():
        if dist.is_initialized() and not is_rank0():
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dist.barrier()
            dist.barrier()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.load_from_pretrained()
        self.load_from_pretrained()
        # 中文说明：根据条件选择执行分支；代码：if dist.is_initialized() and is_rank0():
        if dist.is_initialized() and is_rank0():
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dist.barrier()
            dist.barrier()

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for param in self.parameters():
        for param in self.parameters():
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：param.requires_grad = False
            param.requires_grad = False

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def load_from_pretrained(self, name="vgg_lpips"):
    def load_from_pretrained(self, name="vgg_lpips"):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ckpt = _get_ckpt_path(name, f"{_TORCH_HOME}/hub/checkpoints")
        ckpt = _get_ckpt_path(name, f"{_TORCH_HOME}/hub/checkpoints")
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.load_state_dict(torch.load(ckpt, map_location=torch.device("cpu")), strict=False)
        self.load_state_dict(torch.load(ckpt, map_location=torch.device("cpu")), strict=False)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：logging.info("Loaded pretrained LPIPS loss from {}".format(ckpt))
        logging.info("Loaded pretrained LPIPS loss from {}".format(ckpt))

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@classmethod
    @classmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def from_pretrained(cls, name="vgg_lpips"):
    def from_pretrained(cls, name="vgg_lpips"):
        # 中文说明：根据条件选择执行分支；代码：if name != "vgg_lpips":
        if name != "vgg_lpips":
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise NotImplementedError
            raise NotImplementedError
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model = cls()
        model = cls()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ckpt = _get_ckpt_path(name)
        ckpt = _get_ckpt_path(name)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model.load_state_dict(torch.load(ckpt, map_location=torch.device("cpu")), strict=False)
        model.load_state_dict(torch.load(ckpt, map_location=torch.device("cpu")), strict=False)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return model
        return model

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, input, target):
    def forward(self, input, target):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：in0_input, in1_input = (self.scaling_layer(input), self.scaling_layer(target))
        in0_input, in1_input = (self.scaling_layer(input), self.scaling_layer(target))
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：outs0, outs1 = self.net(in0_input), self.net(in1_input)
        outs0, outs1 = self.net(in0_input), self.net(in1_input)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：feats0, feats1, diffs = {}, {}, {}
        feats0, feats1, diffs = {}, {}, {}
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for kk in range(len(self.chns)):
        for kk in range(len(self.chns)):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：feats0[kk], feats1[kk] = normalize_tensor(outs0[kk]), normalize_tensor(outs1[kk])
            feats0[kk], feats1[kk] = normalize_tensor(outs0[kk]), normalize_tensor(outs1[kk])
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：diffs[kk] = (feats0[kk] - feats1[kk]) ** 2
            diffs[kk] = (feats0[kk] - feats1[kk]) ** 2

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：res = [diffs[kk].mean([1, 2, 3], keepdim=True) for kk in range(len(self.chns))]
        res = [diffs[kk].mean([1, 2, 3], keepdim=True) for kk in range(len(self.chns))]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：val = res[0]
        val = res[0]
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for l in range(1, len(self.chns)):
        for l in range(1, len(self.chns)):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：val += res[l]
            val += res[l]
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return val
        return val


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class ScalingLayer(nn.Module):
class ScalingLayer(nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self):
    def __init__(self):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super(ScalingLayer, self).__init__()
        super(ScalingLayer, self).__init__()
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.register_buffer("shift", torch.Tensor([-0.030, -0.088, -0.188])[None, :, None, None], pe...
        self.register_buffer("shift", torch.Tensor([-0.030, -0.088, -0.188])[None, :, None, None], persistent=False)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.register_buffer("scale", torch.Tensor([0.458, 0.448, 0.450])[None, :, None, None], persi...
        self.register_buffer("scale", torch.Tensor([0.458, 0.448, 0.450])[None, :, None, None], persistent=False)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, inp):
    def forward(self, inp):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return (inp - self.shift) / self.scale
        return (inp - self.shift) / self.scale


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def normalize_tensor(x, eps=1e-10):
def normalize_tensor(x, eps=1e-10):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：norm_factor = torch.sqrt(torch.sum(x**2, dim=1, keepdim=True))
    norm_factor = torch.sqrt(torch.sum(x**2, dim=1, keepdim=True))
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return x / (norm_factor + eps)
    return x / (norm_factor + eps)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class vgg16(torch.nn.Module):
class vgg16(torch.nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, requires_grad=False, pretrained=True, checkpoint_activations: bool = False):
    def __init__(self, requires_grad=False, pretrained=True, checkpoint_activations: bool = False):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super(vgg16, self).__init__()
        super(vgg16, self).__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：vgg_pretrained_features = models.vgg16(pretrained=pretrained).features
        vgg_pretrained_features = models.vgg16(pretrained=pretrained).features
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.checkpoint_activations = checkpoint_activations
        self.checkpoint_activations = checkpoint_activations
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.slice1 = torch.nn.Sequential()
        self.slice1 = torch.nn.Sequential()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.slice2 = torch.nn.Sequential()
        self.slice2 = torch.nn.Sequential()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.slice3 = torch.nn.Sequential()
        self.slice3 = torch.nn.Sequential()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.slice4 = torch.nn.Sequential()
        self.slice4 = torch.nn.Sequential()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.slice5 = torch.nn.Sequential()
        self.slice5 = torch.nn.Sequential()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.N_slices = 5
        self.N_slices = 5
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for x in range(4):
        for x in range(4):
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.slice1.add_module(str(x), vgg_pretrained_features[x])
            self.slice1.add_module(str(x), vgg_pretrained_features[x])
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for x in range(4, 9):
        for x in range(4, 9):
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.slice2.add_module(str(x), vgg_pretrained_features[x])
            self.slice2.add_module(str(x), vgg_pretrained_features[x])
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for x in range(9, 16):
        for x in range(9, 16):
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.slice3.add_module(str(x), vgg_pretrained_features[x])
            self.slice3.add_module(str(x), vgg_pretrained_features[x])
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for x in range(16, 23):
        for x in range(16, 23):
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.slice4.add_module(str(x), vgg_pretrained_features[x])
            self.slice4.add_module(str(x), vgg_pretrained_features[x])
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for x in range(23, 30):
        for x in range(23, 30):
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.slice5.add_module(str(x), vgg_pretrained_features[x])
            self.slice5.add_module(str(x), vgg_pretrained_features[x])
        # 中文说明：根据条件选择执行分支；代码：if not requires_grad:
        if not requires_grad:
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for param in self.parameters():
            for param in self.parameters():
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：param.requires_grad = False
                param.requires_grad = False

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(self, X):
    def forward(self, X):
        # 中文说明：根据条件选择执行分支；代码：if self.checkpoint_activations:
        if self.checkpoint_activations:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = checkpoint.checkpoint(self.slice1, X, use_reentrant=False)
            h = checkpoint.checkpoint(self.slice1, X, use_reentrant=False)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.slice1(X)
            h = self.slice1(X)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h_relu1_2 = h
        h_relu1_2 = h

        # 中文说明：根据条件选择执行分支；代码：if self.checkpoint_activations:
        if self.checkpoint_activations:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = checkpoint.checkpoint(self.slice2, h, use_reentrant=False)
            h = checkpoint.checkpoint(self.slice2, h, use_reentrant=False)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.slice2(h)
            h = self.slice2(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h_relu2_2 = h
        h_relu2_2 = h

        # 中文说明：根据条件选择执行分支；代码：if self.checkpoint_activations:
        if self.checkpoint_activations:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = checkpoint.checkpoint(self.slice3, h, use_reentrant=False)
            h = checkpoint.checkpoint(self.slice3, h, use_reentrant=False)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.slice3(h)
            h = self.slice3(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h_relu3_3 = h
        h_relu3_3 = h

        # 中文说明：根据条件选择执行分支；代码：if self.checkpoint_activations:
        if self.checkpoint_activations:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = checkpoint.checkpoint(self.slice4, h, use_reentrant=False)
            h = checkpoint.checkpoint(self.slice4, h, use_reentrant=False)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.slice4(h)
            h = self.slice4(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h_relu4_3 = h
        h_relu4_3 = h

        # 中文说明：根据条件选择执行分支；代码：if self.checkpoint_activations:
        if self.checkpoint_activations:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = checkpoint.checkpoint(self.slice5, h, use_reentrant=False)
            h = checkpoint.checkpoint(self.slice5, h, use_reentrant=False)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h = self.slice5(h)
            h = self.slice5(h)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：h_relu5_3 = h
        h_relu5_3 = h

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：vgg_outputs = namedtuple("VggOutputs", ["relu1_2", "relu2_2", "relu3_3", "relu4_3", "relu5_3"])
        vgg_outputs = namedtuple("VggOutputs", ["relu1_2", "relu2_2", "relu3_3", "relu4_3", "relu5_3"])
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：out = vgg_outputs(h_relu1_2, h_relu2_2, h_relu3_3, h_relu4_3, h_relu5_3)
        out = vgg_outputs(h_relu1_2, h_relu2_2, h_relu3_3, h_relu4_3, h_relu5_3)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return out
        return out
