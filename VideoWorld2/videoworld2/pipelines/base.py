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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from PIL import Image
from PIL import Image
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torchvision.transforms import GaussianBlur
from torchvision.transforms import GaussianBlur


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class BasePipeline(torch.nn.Module):
class BasePipeline(torch.nn.Module):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, device="cuda", torch_dtype=torch.float16, height_division_factor=64, width...
    def __init__(self, device="cuda", torch_dtype=torch.float16, height_division_factor=64, width_division_factor=64):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__()
        super().__init__()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.device = device
        self.device = device
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.torch_dtype = torch_dtype
        self.torch_dtype = torch_dtype
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.height_division_factor = height_division_factor
        self.height_division_factor = height_division_factor
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.width_division_factor = width_division_factor
        self.width_division_factor = width_division_factor
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.cpu_offload = False
        self.cpu_offload = False
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.model_names = []
        self.model_names = []

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def check_resize_height_width(self, height, width):
    def check_resize_height_width(self, height, width):
        # 中文说明：根据条件选择执行分支；代码：if height % self.height_division_factor != 0:
        if height % self.height_division_factor != 0:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：height = (
            height = (
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：(height + self.height_division_factor - 1) // self.height_division_factor * self.height_divis...
                (height + self.height_division_factor - 1) // self.height_division_factor * self.height_division_factor
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"The height cannot be evenly divided by {self.height_division_factor}. We round it up ...
            print(f"The height cannot be evenly divided by {self.height_division_factor}. We round it up to {height}.")
        # 中文说明：根据条件选择执行分支；代码：if width % self.width_division_factor != 0:
        if width % self.width_division_factor != 0:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：width = (width + self.width_division_factor - 1) // self.width_division_factor * self.width_d...
            width = (width + self.width_division_factor - 1) // self.width_division_factor * self.width_division_factor
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"The width cannot be evenly divided by {self.width_division_factor}. We round it up to...
            print(f"The width cannot be evenly divided by {self.width_division_factor}. We round it up to {width}.")
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return height, width
        return height, width

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def preprocess_image(self, image):
    def preprocess_image(self, image):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：image = torch.Tensor(np.array(image, dtype=np.float32) * (2 / 255) - 1).permute(2, 0, 1).unsq...
        image = torch.Tensor(np.array(image, dtype=np.float32) * (2 / 255) - 1).permute(2, 0, 1).unsqueeze(0)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return image
        return image

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def preprocess_images(self, images):
    def preprocess_images(self, images):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return [self.preprocess_image(image) for image in images]
        return [self.preprocess_image(image) for image in images]

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def vae_output_to_image(self, vae_output):
    def vae_output_to_image(self, vae_output):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：image = vae_output[0].cpu().float().permute(1, 2, 0).numpy()
        image = vae_output[0].cpu().float().permute(1, 2, 0).numpy()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：image = Image.fromarray(((image / 2 + 0.5).clip(0, 1) * 255).astype("uint8"))
        image = Image.fromarray(((image / 2 + 0.5).clip(0, 1) * 255).astype("uint8"))
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return image
        return image

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def vae_output_to_video(self, vae_output):
    def vae_output_to_video(self, vae_output):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = vae_output.cpu().permute(1, 2, 0).numpy()
        video = vae_output.cpu().permute(1, 2, 0).numpy()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = [Image.fromarray(((image / 2 + 0.5).clip(0, 1) * 255).astype("uint8")) for image in v...
        video = [Image.fromarray(((image / 2 + 0.5).clip(0, 1) * 255).astype("uint8")) for image in video]
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return video
        return video

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def merge_latents(self, value, latents, masks, scales, blur_kernel_size=33, blur_sigma=10.0):
    def merge_latents(self, value, latents, masks, scales, blur_kernel_size=33, blur_sigma=10.0):
        # 中文说明：根据条件选择执行分支；代码：if len(latents) > 0:
        if len(latents) > 0:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：blur = GaussianBlur(kernel_size=blur_kernel_size, sigma=blur_sigma)
            blur = GaussianBlur(kernel_size=blur_kernel_size, sigma=blur_sigma)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：height, width = value.shape[-2:]
            height, width = value.shape[-2:]
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：weight = torch.ones_like(value)
            weight = torch.ones_like(value)
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for latent, mask, scale in zip(latents, masks, scales):
            for latent, mask, scale in zip(latents, masks, scales):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mask = self.preprocess_image(mask.resize((width, height))).mean(dim=1, keepdim=True) > 0
                mask = self.preprocess_image(mask.resize((width, height))).mean(dim=1, keepdim=True) > 0
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mask = mask.repeat(1, latent.shape[1], 1, 1).to(dtype=latent.dtype, device=latent.device)
                mask = mask.repeat(1, latent.shape[1], 1, 1).to(dtype=latent.dtype, device=latent.device)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mask = blur(mask)
                mask = blur(mask)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：value += latent * mask * scale
                value += latent * mask * scale
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：weight += mask * scale
                weight += mask * scale
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：value /= weight
            value /= weight
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return value
        return value

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def control_noise_via_local_prompts(
    def control_noise_via_local_prompts(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：prompt_emb_global,
        prompt_emb_global,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：prompt_emb_locals,
        prompt_emb_locals,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：masks,
        masks,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：mask_scales,
        mask_scales,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：inference_callback,
        inference_callback,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：special_kwargs=None,
        special_kwargs=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：special_local_kwargs_list=None,
        special_local_kwargs_list=None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：根据条件选择执行分支；代码：if special_kwargs is None:
        if special_kwargs is None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：noise_pred_global = inference_callback(prompt_emb_global)
            noise_pred_global = inference_callback(prompt_emb_global)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：noise_pred_global = inference_callback(prompt_emb_global, special_kwargs)
            noise_pred_global = inference_callback(prompt_emb_global, special_kwargs)
        # 中文说明：根据条件选择执行分支；代码：if special_local_kwargs_list is None:
        if special_local_kwargs_list is None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：noise_pred_locals = [inference_callback(prompt_emb_local) for prompt_emb_local in prompt_emb_...
            noise_pred_locals = [inference_callback(prompt_emb_local) for prompt_emb_local in prompt_emb_locals]
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：noise_pred_locals = [
            noise_pred_locals = [
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：inference_callback(prompt_emb_local, special_kwargs)
                inference_callback(prompt_emb_local, special_kwargs)
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for prompt_emb_local, special_kwargs in zip(prompt_emb_locals, special_local_kwargs_list)
                for prompt_emb_local, special_kwargs in zip(prompt_emb_locals, special_local_kwargs_list)
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
            ]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：noise_pred = self.merge_latents(noise_pred_global, noise_pred_locals, masks, mask_scales)
        noise_pred = self.merge_latents(noise_pred_global, noise_pred_locals, masks, mask_scales)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return noise_pred
        return noise_pred

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def extend_prompt(self, prompt, local_prompts, masks, mask_scales):
    def extend_prompt(self, prompt, local_prompts, masks, mask_scales):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：local_prompts = local_prompts or []
        local_prompts = local_prompts or []
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：masks = masks or []
        masks = masks or []
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mask_scales = mask_scales or []
        mask_scales = mask_scales or []
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extended_prompt_dict = self.prompter.extend_prompt(prompt)
        extended_prompt_dict = self.prompter.extend_prompt(prompt)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prompt = extended_prompt_dict.get("prompt", prompt)
        prompt = extended_prompt_dict.get("prompt", prompt)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：local_prompts += extended_prompt_dict.get("prompts", [])
        local_prompts += extended_prompt_dict.get("prompts", [])
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：masks += extended_prompt_dict.get("masks", [])
        masks += extended_prompt_dict.get("masks", [])
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：mask_scales += [100.0] * len(extended_prompt_dict.get("masks", []))
        mask_scales += [100.0] * len(extended_prompt_dict.get("masks", []))
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return prompt, local_prompts, masks, mask_scales
        return prompt, local_prompts, masks, mask_scales

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def enable_cpu_offload(self):
    def enable_cpu_offload(self):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.cpu_offload = True
        self.cpu_offload = True

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def load_models_to_device(self, loadmodel_names=[]):
    def load_models_to_device(self, loadmodel_names=[]):
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# only load models to device if cpu_offload is enabled
        # only load models to device if cpu_offload is enabled
        # 中文说明：根据条件选择执行分支；代码：if not self.cpu_offload:
        if not self.cpu_offload:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return
            return
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# offload the unneeded models to cpu
        # offload the unneeded models to cpu
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for model_name in self.model_names:
        for model_name in self.model_names:
            # 中文说明：根据条件选择执行分支；代码：if model_name not in loadmodel_names:
            if model_name not in loadmodel_names:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model = getattr(self, model_name)
                model = getattr(self, model_name)
                # 中文说明：根据条件选择执行分支；代码：if model is not None:
                if model is not None:
                    # 中文说明：根据条件选择执行分支；代码：if hasattr(model, "vram_management_enabled") and model.vram_management_enabled:
                    if hasattr(model, "vram_management_enabled") and model.vram_management_enabled:
                        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for module in model.modules():
                        for module in model.modules():
                            # 中文说明：根据条件选择执行分支；代码：if hasattr(module, "offload"):
                            if hasattr(module, "offload"):
                                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：module.offload()
                                module.offload()
                    # 中文说明：根据条件选择执行分支；代码：else:
                    else:
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model.cpu()
                        model.cpu()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# load the needed models to device
        # load the needed models to device
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for model_name in loadmodel_names:
        for model_name in loadmodel_names:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model = getattr(self, model_name)
            model = getattr(self, model_name)
            # 中文说明：根据条件选择执行分支；代码：if model is not None:
            if model is not None:
                # 中文说明：根据条件选择执行分支；代码：if hasattr(model, "vram_management_enabled") and model.vram_management_enabled:
                if hasattr(model, "vram_management_enabled") and model.vram_management_enabled:
                    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for module in model.modules():
                    for module in model.modules():
                        # 中文说明：根据条件选择执行分支；代码：if hasattr(module, "onload"):
                        if hasattr(module, "onload"):
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：module.onload()
                            module.onload()
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：model.to(self.device)
                    model.to(self.device)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# fresh the cuda cache
        # fresh the cuda cache
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.empty_cache()
        torch.cuda.empty_cache()

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def generate_noise(self, shape, seed=None, device="cpu", dtype=torch.float16):
    def generate_noise(self, shape, seed=None, device="cpu", dtype=torch.float16):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：generator = None if seed is None else torch.Generator(device).manual_seed(seed)
        generator = None if seed is None else torch.Generator(device).manual_seed(seed)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：noise = torch.randn(shape, generator=generator, device=device, dtype=dtype)
        noise = torch.randn(shape, generator=generator, device=device, dtype=dtype)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return noise
        return noise
