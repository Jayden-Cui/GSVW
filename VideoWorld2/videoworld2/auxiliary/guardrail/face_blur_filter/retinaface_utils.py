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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from retinaface.utils.nms.py_cpu_nms import py_cpu_nms
from retinaface.utils.nms.py_cpu_nms import py_cpu_nms

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log


# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Adapted from https://github.com/biubug6/Pytorch_Retinaface/blob/master/detect.py
# Adapted from https://github.com/biubug6/Pytorch_Retinaface/blob/master/detect.py
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def filter_detected_boxes(boxes, scores, confidence_threshold, nms_threshold, top_k, keep_top...
def filter_detected_boxes(boxes, scores, confidence_threshold, nms_threshold, top_k, keep_top_k):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Filter boxes based on confidence score and remove overlapping boxes using NMS."""
    """Filter boxes based on confidence score and remove overlapping boxes using NMS."""
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Keep detections with confidence above threshold
    # Keep detections with confidence above threshold
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：inds = np.where(scores > confidence_threshold)[0]
    inds = np.where(scores > confidence_threshold)[0]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：boxes = boxes[inds]
    boxes = boxes[inds]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scores = scores[inds]
    scores = scores[inds]

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Sort by confidence and keep top K detections
    # Sort by confidence and keep top K detections
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：order = scores.argsort()[::-1][:top_k]
    order = scores.argsort()[::-1][:top_k]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：boxes = boxes[order]
    boxes = boxes[order]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scores = scores[order]
    scores = scores[order]

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Run non-maximum-suppression (NMS) to remove overlapping boxes
    # Run non-maximum-suppression (NMS) to remove overlapping boxes
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dets = np.hstack((boxes, scores[:, np.newaxis])).astype(np.float32, copy=False)
    dets = np.hstack((boxes, scores[:, np.newaxis])).astype(np.float32, copy=False)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：keep = py_cpu_nms(dets, nms_threshold)
    keep = py_cpu_nms(dets, nms_threshold)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dets = dets[keep, :]
    dets = dets[keep, :]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dets = dets[:keep_top_k, :]
    dets = dets[:keep_top_k, :]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：boxes = dets[:, :-1]
    boxes = dets[:, :-1]
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return boxes
    return boxes


# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Adapted from https://github.com/biubug6/Pytorch_Retinaface/blob/master/utils/box_utils.py t...
# Adapted from https://github.com/biubug6/Pytorch_Retinaface/blob/master/utils/box_utils.py to handle batched inputs
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def decode_batch(loc, priors, variances):
def decode_batch(loc, priors, variances):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Decode batched locations from predictions using priors and variances.
    """Decode batched locations from predictions using priors and variances.

    Args:
        loc (tensor): Batched location predictions for loc layers.
            Shape: [batch_size, num_priors, 4]
        priors (tensor): Prior boxes in center-offset form.
            Shape: [num_priors, 4]
        variances: (list[float]): Variances of prior boxes.

    Return:
        Decoded batched bounding box predictions
            Shape: [batch_size, num_priors, 4]
    """
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch_size = loc.size(0)
    batch_size = loc.size(0)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：priors = priors.unsqueeze(0).expand(batch_size, -1, -1)
    priors = priors.unsqueeze(0).expand(batch_size, -1, -1)

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：boxes = torch.cat(
    boxes = torch.cat(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：(
        (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：priors[:, :, :2] + loc[:, :, :2] * variances[0] * priors[:, :, 2:],
            priors[:, :, :2] + loc[:, :, :2] * variances[0] * priors[:, :, 2:],
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：priors[:, :, 2:] * torch.exp(loc[:, :, 2:] * variances[1]),
            priors[:, :, 2:] * torch.exp(loc[:, :, 2:] * variances[1]),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dim=2,
        dim=2,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：boxes[:, :, :2] -= boxes[:, :, 2:] / 2
    boxes[:, :, :2] -= boxes[:, :, 2:] / 2
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：boxes[:, :, 2:] += boxes[:, :, :2]
    boxes[:, :, 2:] += boxes[:, :, :2]
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return boxes
    return boxes


# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Adapted from https://github.com/biubug6/Pytorch_Retinaface/blob/master/detect.py
# Adapted from https://github.com/biubug6/Pytorch_Retinaface/blob/master/detect.py
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _check_keys(model, pretrained_state_dict):
def _check_keys(model, pretrained_state_dict):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ckpt_keys = set(pretrained_state_dict.keys())
    ckpt_keys = set(pretrained_state_dict.keys())
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_keys = set(model.state_dict().keys())
    model_keys = set(model.state_dict().keys())
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：used_pretrained_keys = model_keys & ckpt_keys
    used_pretrained_keys = model_keys & ckpt_keys
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：unused_pretrained_keys = ckpt_keys - model_keys
    unused_pretrained_keys = ckpt_keys - model_keys
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：missing_keys = model_keys - ckpt_keys
    missing_keys = model_keys - ckpt_keys
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug("Missing keys:{}".format(len(missing_keys)))
    log.debug("Missing keys:{}".format(len(missing_keys)))
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug("Unused checkpoint keys:{}".format(len(unused_pretrained_keys)))
    log.debug("Unused checkpoint keys:{}".format(len(unused_pretrained_keys)))
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug("Used keys:{}".format(len(used_pretrained_keys)))
    log.debug("Used keys:{}".format(len(used_pretrained_keys)))
    # 中文说明：检查运行时假设是否成立；代码：assert len(used_pretrained_keys) > 0, "load NONE from pretrained checkpoint"
    assert len(used_pretrained_keys) > 0, "load NONE from pretrained checkpoint"
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return True
    return True


# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Adapted from https://github.com/biubug6/Pytorch_Retinaface/blob/master/detect.py
# Adapted from https://github.com/biubug6/Pytorch_Retinaface/blob/master/detect.py
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _remove_prefix(state_dict, prefix):
def _remove_prefix(state_dict, prefix):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Old version of the model is stored with all names of parameters sharing common prefix 'mod...
    """Old version of the model is stored with all names of parameters sharing common prefix 'module.'"""
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug("Removing prefix '{}'".format(prefix))
    log.debug("Removing prefix '{}'".format(prefix))

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def f(x):
    def f(x):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x.split(prefix, 1)[-1] if x.startswith(prefix) else x
        return x.split(prefix, 1)[-1] if x.startswith(prefix) else x

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return {f(key): value for key, value in state_dict.items()}
    return {f(key): value for key, value in state_dict.items()}


# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Adapted from https://github.com/biubug6/Pytorch_Retinaface/blob/master/detect.py
# Adapted from https://github.com/biubug6/Pytorch_Retinaface/blob/master/detect.py
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def load_model(model, pretrained_path, load_to_cpu):
def load_model(model, pretrained_path, load_to_cpu):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug("Loading pretrained model from {}".format(pretrained_path))
    log.debug("Loading pretrained model from {}".format(pretrained_path))
    # 中文说明：根据条件选择执行分支；代码：if load_to_cpu:
    if load_to_cpu:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pretrained_dict = torch.load(pretrained_path, map_location=lambda storage, loc: storage, weig...
        pretrained_dict = torch.load(pretrained_path, map_location=lambda storage, loc: storage, weights_only=True)
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：device = torch.cuda.current_device()
        device = torch.cuda.current_device()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pretrained_dict = torch.load(
        pretrained_dict = torch.load(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pretrained_path, map_location=lambda storage, loc: storage.cuda(device), weights_only=True
            pretrained_path, map_location=lambda storage, loc: storage.cuda(device), weights_only=True
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
    # 中文说明：根据条件选择执行分支；代码：if "state_dict" in pretrained_dict.keys():
    if "state_dict" in pretrained_dict.keys():
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pretrained_dict = _remove_prefix(pretrained_dict["state_dict"], "module.")
        pretrained_dict = _remove_prefix(pretrained_dict["state_dict"], "module.")
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pretrained_dict = _remove_prefix(pretrained_dict, "module.")
        pretrained_dict = _remove_prefix(pretrained_dict, "module.")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_check_keys(model, pretrained_dict)
    _check_keys(model, pretrained_dict)
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model.load_state_dict(pretrained_dict, strict=False)
    model.load_state_dict(pretrained_dict, strict=False)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return model
    return model
