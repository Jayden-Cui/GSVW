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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import argparse
import argparse
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import importlib
import importlib
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torchvision.transforms.v2 import UniformTemporalSubsample
from torchvision.transforms.v2 import UniformTemporalSubsample
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from loguru import logger as logging
from loguru import logger as logging
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from PIL import Image
from PIL import Image
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torchvision.transforms.functional as F
import torchvision.transforms.functional as F
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.config import Config, pretty_print_overrides
from imaginaire.config import Config, pretty_print_overrides
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import instantiate
from imaginaire.lazy_config import instantiate
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config.lazy import LazyConfig
from imaginaire.lazy_config.lazy import LazyConfig
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import distributed
from imaginaire.utils import distributed
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.config_helper import get_config_module, override
from imaginaire.utils.config_helper import get_config_module, override
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from decord import VideoReader, cpu
from decord import VideoReader, cpu
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import numpy as np
import numpy as np
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torchvision import transforms as T
from torchvision import transforms as T
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.data.dataset_utils import Resize_Preprocess, ToTensorVideo
from videoworld2.data.dataset_utils import Resize_Preprocess, ToTensorVideo


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def load_video(video_path):
def load_video(video_path):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：vr = VideoReader(video_path, ctx=cpu(0), num_threads=2)
    vr = VideoReader(video_path, ctx=cpu(0), num_threads=2)
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# frame_ids = np.linspace(0, len(vr) - 1).astype(np.int32)
    # frame_ids = np.linspace(0, len(vr) - 1).astype(np.int32)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_ids = np.arange(0, len(vr)).tolist()
    frame_ids = np.arange(0, len(vr)).tolist()
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：vr.seek(0)
    vr.seek(0)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frame_data = vr.get_batch(frame_ids).asnumpy()
    frame_data = vr.get_batch(frame_ids).asnumpy()
    # 中文说明：开始一个可捕获异常的代码块；代码：try:
    try:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fps = vr.get_avg_fps()
        fps = vr.get_avg_fps()
    # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception: # failed to read FPS
    except Exception:  # failed to read FPS
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fps = 24
        fps = 24
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return frame_data, fps
    return frame_data, fps

# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_frames(video_path):
def get_frames(video_path):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：preprocess = T.Compose([ToTensorVideo(), Resize_Preprocess((480, 832))])
    preprocess = T.Compose([ToTensorVideo(), Resize_Preprocess((480, 832))])
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：frames, fps = load_video(video_path)
    frames, fps = load_video(video_path)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = frames.astype(np.uint8)
    frames = frames.astype(np.uint8)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = torch.from_numpy(frames).permute(0, 3, 1, 2) # (l, c, h, w)
    frames = torch.from_numpy(frames).permute(0, 3, 1, 2)  # (l, c, h, w)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = UniformTemporalSubsample(93)(frames)
    frames = UniformTemporalSubsample(93)(frames)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = preprocess(frames)
    frames = preprocess(frames)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：frames = torch.clamp(frames * 255.0, 0, 255).to(torch.uint8)
    frames = torch.clamp(frames * 255.0, 0, 255).to(torch.uint8)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return frames, fps
    return frames, fps

# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@logging.catch(reraise=True)
@logging.catch(reraise=True)
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def launch(config: Config, args: argparse.Namespace) -> None:
def launch(config: Config, args: argparse.Namespace) -> None:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Need to initialize the distributed environment before calling config.validate() because it ...
    # Need to initialize the distributed environment before calling config.validate() because it tries to synchronize
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# a buffer across ranks. If you don't do this, then you end up allocating a bunch of buffers ...
    # a buffer across ranks. If you don't do this, then you end up allocating a bunch of buffers on rank 0, and also that
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# check doesn't actually do anything.
    # check doesn't actually do anything.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：distributed.init()
    distributed.init()

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Check that the config is valid
    # Check that the config is valid
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：config.validate()
    config.validate()
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Freeze the config so developers don't change it during training.
    # Freeze the config so developers don't change it during training.
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：config.freeze() # type: ignore
    config.freeze()  # type: ignore
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trainer = config.trainer.type(config)
    trainer = config.trainer.type(config)
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Create the model
    # Create the model
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model = instantiate(config.model)
    model = instantiate(config.model)
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Create the dataloaders.
    # Create the dataloaders.
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataloader_train = instantiate(config.dataloader_train)
    dataloader_train = instantiate(config.dataloader_train)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataloader_val = instantiate(config.dataloader_val)
    dataloader_val = instantiate(config.dataloader_val)
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Start training
    # Start training
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：trainer.train(
    trainer.train(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model,
        model,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dataloader_train,
        dataloader_train,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dataloader_val,
        dataloader_val,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )

# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def load_frame(input_frame_path):
def load_frame(input_frame_path):
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_frame = Image.open(input_frame_path).convert('RGB')
    input_frame = Image.open(input_frame_path).convert('RGB')
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_frame = F.resize(input_frame, (480, 832))
    input_frame = F.resize(input_frame, (480, 832))
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_frame = F.to_tensor(input_frame)
    input_frame = F.to_tensor(input_frame)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_frame = input_frame.view(1, 3, 1, 480, 832)
    input_frame = input_frame.view(1, 3, 1, 480, 832)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_frame = torch.clamp(input_frame * 255.0, 0, 255).to(torch.uint8)
    input_frame = torch.clamp(input_frame * 255.0, 0, 255).to(torch.uint8)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_frame = input_frame.to('cuda')
    input_frame = input_frame.to('cuda')
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return input_frame
    return input_frame

# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@logging.catch(reraise=True)
@logging.catch(reraise=True)
# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def infer(config: Config, args: argparse.Namespace) -> None:
def infer(config: Config, args: argparse.Namespace) -> None:
    
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：config.validate()
    config.validate()
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：config.freeze()
    config.freeze()
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trainer = config.trainer.type(config)
    trainer = config.trainer.type(config)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model = instantiate(config.model)
    model = instantiate(config.model)
    
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model = model.to("cuda", memory_format=trainer.config.trainer.memory_format) # type: ignore
    model = model.to("cuda", memory_format=trainer.config.trainer.memory_format)  # type: ignore
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model.on_train_start(trainer.config.trainer.memory_format)
    model.on_train_start(trainer.config.trainer.memory_format)
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：trainer.callbacks.on_optimizer_init_start()
    trainer.callbacks.on_optimizer_init_start()
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：optimizer, scheduler = model.init_optimizer_scheduler(trainer.config.optimizer, trainer.confi...
    optimizer, scheduler = model.init_optimizer_scheduler(trainer.config.optimizer, trainer.config.scheduler)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：grad_scaler = torch.amp.GradScaler("cuda", **trainer.config.trainer.grad_scaler_args)
    grad_scaler = torch.amp.GradScaler("cuda", **trainer.config.trainer.grad_scaler_args)
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：trainer.callbacks.on_optimizer_init_end()
    trainer.callbacks.on_optimizer_init_end()
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Load the model checkpoint and get the starting iteration number.
    # Load the model checkpoint and get the starting iteration number.

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：quant_infos = torch.load('checkpoints/VideoWorld2_dLDM_2B/VideoCraft-dLDM-codes.pt')
    quant_infos = torch.load('checkpoints/VideoWorld2_dLDM_2B/VideoCraft-dLDM-codes.pt')
    # 中文说明：根据条件选择执行分支；代码：if args.input_path != 'default':
    if args.input_path != 'default':
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_frame = load_frame(args.input_path)
        input_frame = load_frame(args.input_path)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：vid_name = args.input_path.split('/')[-1].replace('.jpg', '')
        vid_name = args.input_path.split('/')[-1].replace('.jpg', '')
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：latent_dynamic_codes = torch.tensor(quant_infos[vid_name]).to('cuda')
        latent_dynamic_codes = torch.tensor(quant_infos[vid_name]).to('cuda')
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model.inference(input_frame, latent_dynamic_codes)
        model.inference(input_frame, latent_dynamic_codes)

    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print('Inference using all assets in videocraft_example folder')
        print('Inference using all assets in videocraft_example folder')
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_frame_root = 'assets/videocraft_example'
        input_frame_root = 'assets/videocraft_example'
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_frame_list = os.listdir(input_frame_root)
        input_frame_list = os.listdir(input_frame_root)
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for input_frame_name in input_frame_list:
        for input_frame_name in input_frame_list:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_frame_path = os.path.join(input_frame_root, input_frame_name)
            input_frame_path = os.path.join(input_frame_root, input_frame_name)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：input_frame = load_frame(input_frame_path)
            input_frame = load_frame(input_frame_path)

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：latent_dynamic_codes = torch.tensor(quant_infos[input_frame_name.replace('.jpg', '')]).to('cu...
            latent_dynamic_codes = torch.tensor(quant_infos[input_frame_name.replace('.jpg', '')]).to('cuda')
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model.inference(input_frame, latent_dynamic_codes)
            model.inference(input_frame, latent_dynamic_codes)

    
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# for quant_info in quant_infos[10:]:
    # for quant_info in quant_infos[10:]:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# vid_name = quant_info[1]
    #     vid_name = quant_info[1]
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# vid_path = f'/opt/tiger/mix_allstep_infer_f177_1110/{vid_name}_0.mp4'
    #     vid_path = f'/opt/tiger/mix_allstep_infer_f177_1110/{vid_name}_0.mp4'
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# video, fps = get_frames(vid_path)
    #     video, fps = get_frames(vid_path)
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# # frames = video.permute(1, 0, 2, 3)[:, :1][None].to('cuda')
    #     # frames = video.permute(1, 0, 2, 3)[:, :1][None].to('cuda')
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# frames = video.permute(1, 0, 2, 3)[:, :1][None].to('cuda')
    #     frames = video.permute(1, 0, 2, 3)[:, :1][None].to('cuda')
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# # frames = video.permute(1, 0, 2, 3)[None].to('cuda')
    #     # frames = video.permute(1, 0, 2, 3)[None].to('cuda')
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# # frames = frames.astype(np.uint8)
    #     # frames = frames.astype(np.uint8)
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# # frames = torch.from_numpy(frames).permute(0, 3, 1, 2) # (l, c, h, w)
    #     # frames = torch.from_numpy(frames).permute(0, 3, 1, 2)  # (l, c, h, w)
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# # frames = F.resize(frames, (480, 832))[:1].permute(1, 0, 2, 3)[None]
    #     # frames = F.resize(frames, (480, 832))[:1].permute(1, 0, 2, 3)[None]
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# # frames = torch.clamp(frames, 0, 255).to(torch.uint8).to('cuda')
    #     # frames = torch.clamp(frames, 0, 255).to(torch.uint8).to('cuda')
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# latent_dynamic_codes = torch.tensor(quant_info[0]).to('cuda')
    #     latent_dynamic_codes = torch.tensor(quant_info[0]).to('cuda')
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# model.inference(frames, latent_dynamic_codes)
    #     model.inference(frames, latent_dynamic_codes)

# 中文说明：根据条件选择执行分支；代码：if __name__ == "__main__":
if __name__ == "__main__":
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Usage: torchrun --nproc_per_node=1 -m scripts.train --config=videoworld2/configs/base/confi...
    # Usage: torchrun --nproc_per_node=1 -m scripts.train --config=videoworld2/configs/base/config.py -- experiments=predict2_video2world_training_2b_cosmos_nemo_assets
    
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Get the config file from the input arguments.
    # Get the config file from the input arguments.
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：parser = argparse.ArgumentParser(description="Training")
    parser = argparse.ArgumentParser(description="Training")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument("--config", help="Path to the config file", required=True)
    parser.add_argument("--config", help="Path to the config file", required=True)
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument("--mode", help="Path to the config file", required=True)
    parser.add_argument("--mode", help="Path to the config file", required=True)
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument("--input_path", default='', required=True)
    parser.add_argument("--input_path", default='', required=True)
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："opts",
        "opts",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="""
        help="""
Modify config options at the end of the command. For Yacs configs, use
space-separated "PATH.KEY VALUE" pairs.
For python-based LazyConfig, use "path.key=value".
        """.strip(),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：default=None,
        default=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：nargs=argparse.REMAINDER,
        nargs=argparse.REMAINDER,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：args = parser.parse_args()
    args = parser.parse_args()
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config_module = get_config_module(args.config)
    config_module = get_config_module(args.config)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config = importlib.import_module(config_module).make_config()
    config = importlib.import_module(config_module).make_config()
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config = override(config, args.opts)
    config = override(config, args.opts)
   
    # 中文说明：根据条件选择执行分支；代码：if args.mode == 'train':
    if args.mode == 'train':
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Launch the training job.
        # Launch the training job.
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：launch(config, args)
        launch(config, args)
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：infer(config, args)
        infer(config, args)