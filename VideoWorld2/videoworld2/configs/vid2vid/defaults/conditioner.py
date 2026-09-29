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

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.conditioner import BooleanFlag, GeneralConditioner, ReMapkey, T2VCondition, ...
from videoworld2.conditioner import BooleanFlag, GeneralConditioner, ReMapkey, T2VCondition, TextAttr
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.utils.context_parallel import broadcast_split_tensor
from videoworld2.utils.context_parallel import broadcast_split_tensor
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import LazyCall as L
from imaginaire.lazy_config import LazyCall as L
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import LazyDict
from imaginaire.lazy_config import LazyDict


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@dataclass(frozen=True)
@dataclass(frozen=True)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Vid2VidCondition(T2VCondition):
class Vid2VidCondition(T2VCondition):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：use_video_condition: bool = False
    use_video_condition: bool = False
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# the following two attributes are used to set the video condition; during training, inference
    # the following two attributes are used to set the video condition; during training, inference
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：gt_frames: Optional[torch.Tensor] = None
    gt_frames: Optional[torch.Tensor] = None
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：condition_video_input_mask_B_C_T_H_W: Optional[torch.Tensor] = None
    condition_video_input_mask_B_C_T_H_W: Optional[torch.Tensor] = None
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：control_input_depth: Optional[torch.Tensor] = None
    control_input_depth: Optional[torch.Tensor] = None
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：recon_image: Optional[torch.Tensor] = None
    recon_image: Optional[torch.Tensor] = None
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：decoder_feature: Optional[torch.Tensor] = None
    decoder_feature: Optional[torch.Tensor] = None

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def set_video_condition(
    def set_video_condition(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：gt_frames: torch.Tensor,
        gt_frames: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：random_min_num_conditional_frames: int,
        random_min_num_conditional_frames: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：random_max_num_conditional_frames: int,
        random_max_num_conditional_frames: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_conditional_frames: Optional[int] = None,
        num_conditional_frames: Optional[int] = None,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**extra_kwargs,
        **extra_kwargs,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> "Vid2VidCondition":
    ) -> "Vid2VidCondition":
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Sets the video conditioning frames for video-to-video generation.

        This method creates a conditioning mask for the input video frames that determines
        which frames will be used as context frames for generating new frames. The method
        handles both image batches (T=1) and video batches (T>1) differently.

        Args:
            gt_frames: A tensor of ground truth frames with shape [B, C, T, H, W], where:
                B = batch size
                C = number of channels
                T = number of frames
                H = height
                W = width

            random_min_num_conditional_frames: Minimum number of frames to use for conditioning
                when randomly selecting a number of conditioning frames.

            random_max_num_conditional_frames: Maximum number of frames to use for conditioning
                when randomly selecting a number of conditioning frames.

            num_conditional_frames: Optional; If provided, all examples in the batch will use
                exactly this many frames for conditioning. If None, a random number of frames
                between random_min_num_conditional_frames and random_max_num_conditional_frames
                will be selected for each example in the batch.

        Returns:
            A new Vid2VidCondition object with the gt_frames and conditioning mask set.
            The conditioning mask (condition_video_input_mask_B_C_T_H_W) is a binary tensor
            of shape [B, 1, T, H, W] where 1 indicates frames used for conditioning and 0
            indicates frames to be generated.

        Notes:
            - For image batches (T=1), no conditioning frames are used (num_conditional_frames_B = 0).
            - For video batches:
                - If num_conditional_frames is provided, all examples use that fixed number of frames.
                - Otherwise, each example randomly uses between random_min_num_conditional_frames and
                random_max_num_conditional_frames frames.
            - The mask marks the first N frames as conditioning frames (set to 1) for each example.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs = self.to_dict(skip_underscore=False)
        kwargs = self.to_dict(skip_underscore=False)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["gt_frames"] = gt_frames
        kwargs["gt_frames"] = gt_frames
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for key in extra_kwargs:
        for key in extra_kwargs:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs[key] = extra_kwargs[key]
            kwargs[key] = extra_kwargs[key]

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# condition_video_input_mask_B_C_T_H_W
        # condition_video_input_mask_B_C_T_H_W
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：B, _, T, H, W = gt_frames.shape
        B, _, T, H, W = gt_frames.shape
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：condition_video_input_mask_B_C_T_H_W = torch.zeros(
        condition_video_input_mask_B_C_T_H_W = torch.zeros(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：B, 1, T, H, W, dtype=gt_frames.dtype, device=gt_frames.device
            B, 1, T, H, W, dtype=gt_frames.dtype, device=gt_frames.device
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：根据条件选择执行分支；代码：if T == 1: # handle image batch
        if T == 1:  # handle image batch
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_conditional_frames_B = torch.zeros(B, dtype=torch.int32)
            num_conditional_frames_B = torch.zeros(B, dtype=torch.int32)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：else: # handle video batch
        else:  # handle video batch
            # 中文说明：根据条件选择执行分支；代码：if num_conditional_frames is not None:
            if num_conditional_frames is not None:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_conditional_frames_B = torch.ones(B, dtype=torch.int32) * num_conditional_frames
                num_conditional_frames_B = torch.ones(B, dtype=torch.int32) * num_conditional_frames
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_conditional_frames_B = torch.randint(
                num_conditional_frames_B = torch.randint(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：random_min_num_conditional_frames, random_max_num_conditional_frames + 1, size=(B,)
                    random_min_num_conditional_frames, random_max_num_conditional_frames + 1, size=(B,)
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for idx in range(B):
        for idx in range(B):
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：condition_video_input_mask_B_C_T_H_W[idx, :, : num_conditional_frames_B[idx], :, :] += 1
            condition_video_input_mask_B_C_T_H_W[idx, :, : num_conditional_frames_B[idx], :, :] += 1

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["condition_video_input_mask_B_C_T_H_W"] = condition_video_input_mask_B_C_T_H_W
        kwargs["condition_video_input_mask_B_C_T_H_W"] = condition_video_input_mask_B_C_T_H_W
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return type(self)(**kwargs)
        return type(self)(**kwargs)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def edit_for_inference(
    def edit_for_inference(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, is_cfg_conditional: bool = True, num_conditional_frames: int = 1
        self, is_cfg_conditional: bool = True, num_conditional_frames: int = 1
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> "Vid2VidCondition":
    ) -> "Vid2VidCondition":
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_condition = self.set_video_condition(
        _condition = self.set_video_condition(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gt_frames=self.gt_frames,
            gt_frames=self.gt_frames,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：random_min_num_conditional_frames=0,
            random_min_num_conditional_frames=0,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：random_max_num_conditional_frames=0,
            random_max_num_conditional_frames=0,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_conditional_frames=num_conditional_frames,
            num_conditional_frames=num_conditional_frames,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：根据条件选择执行分支；代码：if not is_cfg_conditional:
        if not is_cfg_conditional:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Do not use classifier free guidance on conditional frames.
            # Do not use classifier free guidance on conditional frames.
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# YB found that it leads to worse results.
            # YB found that it leads to worse results.
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_condition.use_video_condition.fill_(True)
            _condition.use_video_condition.fill_(True)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return _condition
        return _condition

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def broadcast(self, process_group: torch.distributed.ProcessGroup) -> "Vid2VidCondition":
    def broadcast(self, process_group: torch.distributed.ProcessGroup) -> "Vid2VidCondition":
        # 中文说明：根据条件选择执行分支；代码：if self.is_broadcasted:
        if self.is_broadcasted:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return self
            return self
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# extra efforts
        # extra efforts
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gt_frames = self.gt_frames
        gt_frames = self.gt_frames
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：condition_video_input_mask_B_C_T_H_W = self.condition_video_input_mask_B_C_T_H_W
        condition_video_input_mask_B_C_T_H_W = self.condition_video_input_mask_B_C_T_H_W
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：control_input_depth = self.control_input_depth
        control_input_depth = self.control_input_depth
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：recon_image = self.recon_image
        recon_image = self.recon_image
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：decoder_feature = self.decoder_feature
        decoder_feature = self.decoder_feature
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs = self.to_dict(skip_underscore=False)
        kwargs = self.to_dict(skip_underscore=False)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["gt_frames"] = None
        kwargs["gt_frames"] = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["condition_video_input_mask_B_C_T_H_W"] = None
        kwargs["condition_video_input_mask_B_C_T_H_W"] = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["recon_image"] = None
        kwargs["recon_image"] = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["control_input_depth"] = None
        kwargs["control_input_depth"] = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["decoder_feature"] = None
        kwargs["decoder_feature"] = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：new_condition = T2VCondition.broadcast(
        new_condition = T2VCondition.broadcast(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：type(self)(**kwargs),
            type(self)(**kwargs),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：process_group,
            process_group,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs = new_condition.to_dict(skip_underscore=False)
        kwargs = new_condition.to_dict(skip_underscore=False)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_, _, T, _, _ = gt_frames.shape
        _, _, T, _, _ = gt_frames.shape
        # 中文说明：根据条件选择执行分支；代码：if process_group is not None:
        if process_group is not None:
            # 中文说明：根据条件选择执行分支；代码：if T > 1 and process_group.size() > 1:
            if T > 1 and process_group.size() > 1:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gt_frames = broadcast_split_tensor(gt_frames, seq_dim=2, process_group=process_group)
                gt_frames = broadcast_split_tensor(gt_frames, seq_dim=2, process_group=process_group)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：condition_video_input_mask_B_C_T_H_W = broadcast_split_tensor(
                condition_video_input_mask_B_C_T_H_W = broadcast_split_tensor(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：condition_video_input_mask_B_C_T_H_W, seq_dim=2, process_group=process_group
                    condition_video_input_mask_B_C_T_H_W, seq_dim=2, process_group=process_group
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：根据条件选择执行分支；代码：if control_input_depth is not None:
                if control_input_depth is not None:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：control_input_depth = broadcast_split_tensor(
                    control_input_depth = broadcast_split_tensor(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：control_input_depth, seq_dim=2, process_group=process_group
                        control_input_depth, seq_dim=2, process_group=process_group
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                # 中文说明：根据条件选择执行分支；代码：if recon_image is not None:
                if recon_image is not None:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：recon_image = broadcast_split_tensor(
                    recon_image = broadcast_split_tensor(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：recon_image, seq_dim=2, process_group=process_group
                        recon_image, seq_dim=2, process_group=process_group
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                # 中文说明：根据条件选择执行分支；代码：if decoder_feature is not None:
                if decoder_feature is not None:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：decoder_feature = broadcast_split_tensor(
                    decoder_feature = broadcast_split_tensor(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：decoder_feature, seq_dim=2, process_group=process_group
                        decoder_feature, seq_dim=2, process_group=process_group
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["gt_frames"] = gt_frames
        kwargs["gt_frames"] = gt_frames
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["condition_video_input_mask_B_C_T_H_W"] = condition_video_input_mask_B_C_T_H_W
        kwargs["condition_video_input_mask_B_C_T_H_W"] = condition_video_input_mask_B_C_T_H_W
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["control_input_depth"] = control_input_depth
        kwargs["control_input_depth"] = control_input_depth
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["recon_image"] = recon_image
        kwargs["recon_image"] = recon_image
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：kwargs["decoder_feature"] = decoder_feature
        kwargs["decoder_feature"] = decoder_feature
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return type(self)(**kwargs)
        return type(self)(**kwargs)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Vid2VidConditionV2(Vid2VidCondition):
class Vid2VidConditionV2(Vid2VidCondition):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    compared to Vid2VidCondition, this class apply zero frames when use_video_condition is False~(unconditional generation in cfg)
    in the case, we do zero-out conditional frames in the video condition
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def set_video_condition(
    def set_video_condition(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：gt_frames: torch.Tensor,
        gt_frames: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：random_min_num_conditional_frames: int,
        random_min_num_conditional_frames: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：random_max_num_conditional_frames: int,
        random_max_num_conditional_frames: int,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_conditional_frames: Optional[int] = None,
        num_conditional_frames: Optional[int] = None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> "Vid2VidConditionV2":
    ) -> "Vid2VidConditionV2":
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_conditional_frames = 0 if not self.use_video_condition else num_conditional_frames
        num_conditional_frames = 0 if not self.use_video_condition else num_conditional_frames
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return super().set_video_condition(
        return super().set_video_condition(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gt_frames=gt_frames,
            gt_frames=gt_frames,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：random_min_num_conditional_frames=random_min_num_conditional_frames,
            random_min_num_conditional_frames=random_min_num_conditional_frames,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：random_max_num_conditional_frames=random_max_num_conditional_frames,
            random_max_num_conditional_frames=random_max_num_conditional_frames,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_conditional_frames=num_conditional_frames,
            num_conditional_frames=num_conditional_frames,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def edit_for_inference(
    def edit_for_inference(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, is_cfg_conditional: bool = True, num_conditional_frames: int = 1
        self, is_cfg_conditional: bool = True, num_conditional_frames: int = 1
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> "Vid2VidConditionV2":
    ) -> "Vid2VidConditionV2":
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del is_cfg_conditional
        del is_cfg_conditional
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_condition = super().set_video_condition(
        _condition = super().set_video_condition(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gt_frames=self.gt_frames,
            gt_frames=self.gt_frames,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：random_min_num_conditional_frames=0,
            random_min_num_conditional_frames=0,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：random_max_num_conditional_frames=0,
            random_max_num_conditional_frames=0,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_conditional_frames=num_conditional_frames,
            num_conditional_frames=num_conditional_frames,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return _condition
        return _condition


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Vid2VidConditioner(GeneralConditioner):
class Vid2VidConditioner(GeneralConditioner):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(
    def forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：batch: Dict,
        batch: Dict,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：override_dropout_rate: Optional[Dict[str, float]] = None,
        override_dropout_rate: Optional[Dict[str, float]] = None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Vid2VidCondition:
    ) -> Vid2VidCondition:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output = super()._forward(batch, override_dropout_rate)
        output = super()._forward(batch, override_dropout_rate)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return Vid2VidCondition(**output)
        return Vid2VidCondition(**output)


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Vid2VidConditionerV2(GeneralConditioner):
class Vid2VidConditionerV2(GeneralConditioner):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def forward(
    def forward(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：batch: Dict,
        batch: Dict,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：override_dropout_rate: Optional[Dict[str, float]] = None,
        override_dropout_rate: Optional[Dict[str, float]] = None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Vid2VidConditionV2:
    ) -> Vid2VidConditionV2:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output = super()._forward(batch, override_dropout_rate)
        output = super()._forward(batch, override_dropout_rate)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return Vid2VidConditionV2(**output)
        return Vid2VidConditionV2(**output)


# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_SHARED_CONFIG = dict(
_SHARED_CONFIG = dict(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fps=L(ReMapkey)(
    fps=L(ReMapkey)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_key="fps",
        input_key="fps",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_key="fps",
        output_key="fps",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout_rate=0.0,
        dropout_rate=0.0,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dtype=None,
        dtype=None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：padding_mask=L(ReMapkey)(
    padding_mask=L(ReMapkey)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_key="padding_mask",
        input_key="padding_mask",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_key="padding_mask",
        output_key="padding_mask",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout_rate=0.0,
        dropout_rate=0.0,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dtype=None,
        dtype=None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text=L(TextAttr)(
    text=L(TextAttr)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_key=["t5_text_embeddings"],
        input_key=["t5_text_embeddings"],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout_rate=0.2,
        dropout_rate=0.2,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_video_condition=L(BooleanFlag)(
    use_video_condition=L(BooleanFlag)(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_key="fps",
        input_key="fps",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：output_key="use_video_condition",
        output_key="use_video_condition",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dropout_rate=0.2,
        dropout_rate=0.2,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：VideoPredictionConditioner: LazyDict = L(Vid2VidConditioner)(
VideoPredictionConditioner: LazyDict = L(Vid2VidConditioner)(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**_SHARED_CONFIG,
    **_SHARED_CONFIG,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：VideoPredictionConditionerV2: LazyDict = L(Vid2VidConditionerV2)(
VideoPredictionConditionerV2: LazyDict = L(Vid2VidConditionerV2)(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**_SHARED_CONFIG,
    **_SHARED_CONFIG,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def register_conditioner():
def register_conditioner():
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cs = ConfigStore.instance()
    cs = ConfigStore.instance()
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(
    cs.store(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group="conditioner",
        group="conditioner",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：package="model.config.conditioner",
        package="model.config.conditioner",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="video_prediction_conditioner",
        name="video_prediction_conditioner",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：node=VideoPredictionConditioner,
        node=VideoPredictionConditioner,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(
    cs.store(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group="conditioner",
        group="conditioner",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：package="model.config.conditioner",
        package="model.config.conditioner",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="video_prediction_conditioner_v2",
        name="video_prediction_conditioner_v2",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：node=VideoPredictionConditionerV2,
        node=VideoPredictionConditionerV2,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
