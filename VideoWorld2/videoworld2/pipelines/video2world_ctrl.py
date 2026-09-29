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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.pipelines.video2world import *
from videoworld2.pipelines.video2world import *


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Video2WorldPipelineWithCtrl(Video2WorldPipeline):
class Video2WorldPipelineWithCtrl(Video2WorldPipeline):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, device: str = "cuda", torch_dtype: torch.dtype = torch.bfloat16):
    def __init__(self, device: str = "cuda", torch_dtype: torch.dtype = torch.bfloat16):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(device=device, torch_dtype=torch_dtype)
        super().__init__(device=device, torch_dtype=torch_dtype)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.text_encoder: CosmosT5TextEncoder = None
        self.text_encoder: CosmosT5TextEncoder = None
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.dit: torch.nn.Module = None
        self.dit: torch.nn.Module = None
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.dit_ema: torch.nn.Module = None
        self.dit_ema: torch.nn.Module = None
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.tokenizer: TokenizerInterface = None
        self.tokenizer: TokenizerInterface = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.conditioner = None
        self.conditioner = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.prompt_refiner = None
        self.prompt_refiner = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.text_guardrail_runner = None
        self.text_guardrail_runner = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.video_guardrail_runner = None
        self.video_guardrail_runner = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.model_names = ["text_encoder", "dit", "tokenizer"]
        self.model_names = ["text_encoder", "dit", "tokenizer"]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.height_division_factor = 16
        self.height_division_factor = 16
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.width_division_factor = 16
        self.width_division_factor = 16
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.use_unified_sequence_parallel = False
        self.use_unified_sequence_parallel = False

    # 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@staticmethod
    @staticmethod
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def from_config(
    def from_config(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：config: Video2WorldWithCtrlPipelineConfig,
        config: Video2WorldWithCtrlPipelineConfig,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dit_path: str = "",
        dit_path: str = "",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：text_encoder_path: str = "",
        text_encoder_path: str = "",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：device: str = "cuda",
        device: str = "cuda",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：torch_dtype: torch.dtype = torch.bfloat16,
        torch_dtype: torch.dtype = torch.bfloat16,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：load_prompt_refiner: bool = False,
        load_prompt_refiner: bool = False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Any:
    ) -> Any:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdbc;pdb.set_trace()
        # import pdbc;pdb.set_trace()
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Create a pipe
        # Create a pipe
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe = Video2WorldPipelineWithCtrl(device=device, torch_dtype=torch_dtype)
        pipe = Video2WorldPipelineWithCtrl(device=device, torch_dtype=torch_dtype)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.config = config
        pipe.config = config
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.precision = {
        pipe.precision = {
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："float32": torch.float32,
            "float32": torch.float32,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："float16": torch.float16,
            "float16": torch.float16,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："bfloat16": torch.bfloat16,
            "bfloat16": torch.bfloat16,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}[config.precision]
        }[config.precision]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.tensor_kwargs = {"device": "cuda", "dtype": pipe.precision}
        pipe.tensor_kwargs = {"device": "cuda", "dtype": pipe.precision}
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(f"precision {pipe.precision}")
        log.warning(f"precision {pipe.precision}")

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 1. set data keys and data information
        # 1. set data keys and data information
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.sigma_data = config.sigma_data
        pipe.sigma_data = config.sigma_data
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pipe.setup_data_key()
        pipe.setup_data_key()

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 2. setup up diffusion processing and scaling~(pre-condition)
        # 2. setup up diffusion processing and scaling~(pre-condition)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.scheduler = RectifiedFlowAB2Scheduler(
        pipe.scheduler = RectifiedFlowAB2Scheduler(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_min=config.timestamps.t_min,
            sigma_min=config.timestamps.t_min,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_max=config.timestamps.t_max,
            sigma_max=config.timestamps.t_max,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：order=config.timestamps.order,
            order=config.timestamps.order,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：t_scaling_factor=config.rectified_flow_t_scaling_factor,
            t_scaling_factor=config.rectified_flow_t_scaling_factor,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.scaling = RectifiedFlowScaling(pipe.sigma_data, config.rectified_flow_t_scaling_factor)
        pipe.scaling = RectifiedFlowScaling(pipe.sigma_data, config.rectified_flow_t_scaling_factor)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 3. Set up tokenizer
        # 3. Set up tokenizer
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.tokenizer = instantiate(config.tokenizer)
        pipe.tokenizer = instantiate(config.tokenizer)
        # 中文说明：检查运行时假设是否成立；代码：assert (
        assert (
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.tokenizer.latent_ch == pipe.config.state_ch
            pipe.tokenizer.latent_ch == pipe.config.state_ch
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"latent_ch {pipe.tokenizer.latent_ch} != state_shape {pipe.config.state_ch}"
        ), f"latent_ch {pipe.tokenizer.latent_ch} != state_shape {pipe.config.state_ch}"

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 4. Load text encoder
        # 4. Load text encoder
        # 中文说明：根据条件选择执行分支；代码：if text_encoder_path:
        if text_encoder_path:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# inference
            # inference
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.text_encoder = CosmosT5TextEncoder(device=device, cache_dir=text_encoder_path)
            pipe.text_encoder = CosmosT5TextEncoder(device=device, cache_dir=text_encoder_path)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pipe.text_encoder.to(device)
            pipe.text_encoder.to(device)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# training
            # training
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.text_encoder = None
            pipe.text_encoder = None

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 5. Initialize conditioner
        # 5. Initialize conditioner
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.conditioner = instantiate(config.conditioner)
        pipe.conditioner = instantiate(config.conditioner)
        # 中文说明：检查运行时假设是否成立；代码：assert (
        assert (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sum(p.numel() for p in pipe.conditioner.parameters() if p.requires_grad) == 0
            sum(p.numel() for p in pipe.conditioner.parameters() if p.requires_grad) == 0
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), "conditioner should not have learnable parameters"
        ), "conditioner should not have learnable parameters"


        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.text_guardrail_runner = None
        pipe.text_guardrail_runner = None
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.video_guardrail_runner = None
        pipe.video_guardrail_runner = None

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 6. Set up DiT
        # 6. Set up DiT
        # 中文说明：根据条件选择执行分支；代码：if dit_path:
        if dit_path:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Loading DiT from {dit_path}")
            log.info(f"Loading DiT from {dit_path}")
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning("dit_path not provided, initializing DiT with random weights")
            log.warning("dit_path not provided, initializing DiT with random weights")
        # 中文说明：处理异常、清理资源或管理上下文；代码：with init_weights_on_device():
        with init_weights_on_device():
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_config = config.net
            dit_config = config.net
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_ctrl_config = config.net_ctrl
            dit_ctrl_config = config.net_ctrl
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.dit = instantiate(dit_config).eval() # inference
            pipe.dit = instantiate(dit_config).eval()  # inference
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.dit_ctrl = instantiate(dit_ctrl_config).eval() # inference
            pipe.dit_ctrl = instantiate(dit_ctrl_config).eval()  # inference

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：根据条件选择执行分支；代码：if dit_path:
        if dit_path:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dict = load_state_dict(dit_path)
            state_dict = load_state_dict(dit_path)
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# drop net. prefix
        # drop net. prefix
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dict_dit_compatible = dict()
        state_dict_dit_compatible = dict()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dict_dit_ctrl_compatible = dict()
        state_dict_dit_ctrl_compatible = dict()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：has_pretrained_ctrl = False
        has_pretrained_ctrl = False
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for k, v in state_dict.items():
        for k, v in state_dict.items():
            # 中文说明：根据条件选择执行分支；代码：if 'ldm_net' in k:
            if 'ldm_net' in k:
                # 中文说明：执行循环控制或空操作；代码：continue
                continue
            # 中文说明：根据条件选择执行分支；代码：if k.startswith("net."):
            if k.startswith("net."):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：state_dict_dit_compatible[k[4:]] = v
                state_dict_dit_compatible[k[4:]] = v
            # 中文说明：根据条件选择执行分支；代码：elif k.startswith("net_ctrl."):
            elif k.startswith("net_ctrl."):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：has_pretrained_ctrl = True
                has_pretrained_ctrl = True
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：state_dict_dit_ctrl_compatible[k[9:]] = v
                state_dict_dit_ctrl_compatible[k[9:]] = v
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dict_dit_compatible[k] = v
                state_dict_dit_compatible[k] = v
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state_dict_dit_ctrl_compatible[k] = v
                state_dict_dit_ctrl_compatible[k] = v

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pipe.dit.load_state_dict(state_dict_dit_compatible, strict=False, assign=True)
        pipe.dit.load_state_dict(state_dict_dit_compatible, strict=False, assign=True)
        # 中文说明：根据条件选择执行分支；代码：if has_pretrained_ctrl:
        if has_pretrained_ctrl:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pipe.dit_ctrl.load_state_dict(state_dict_dit_ctrl_compatible, strict=False, assign=True)
            pipe.dit_ctrl.load_state_dict(state_dict_dit_ctrl_compatible, strict=False, assign=True)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pipe.dit_ctrl.load_state_dict(state_dict_dit_compatible, strict=False, assign=True)
            pipe.dit_ctrl.load_state_dict(state_dict_dit_compatible, strict=False, assign=True)

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：del state_dict, state_dict_dit_compatible
        del state_dict, state_dict_dit_compatible
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.success(f"Successfully loaded DiT from {dit_path}")
        log.success(f"Successfully loaded DiT from {dit_path}")

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 6-2. Handle EMA
        # 6-2. Handle EMA
        # 中文说明：根据条件选择执行分支；代码：if config.ema.enabled:
        if config.ema.enabled:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.dit_ema = instantiate(dit_config).eval()
            pipe.dit_ema = instantiate(dit_config).eval()
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pipe.dit_ema.requires_grad_(False)
            pipe.dit_ema.requires_grad_(False)

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.dit_ema_worker = FastEmaModelUpdater() # default when not using FSDP
            pipe.dit_ema_worker = FastEmaModelUpdater()  # default when not using FSDP

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：s = config.ema.rate
            s = config.ema.rate
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.ema_exp_coefficient = np.roots([1, 7, 16 - s**-2, 12 - s**-2]).real.max()
            pipe.ema_exp_coefficient = np.roots([1, 7, 16 - s**-2, 12 - s**-2]).real.max()
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# copying is only necessary when starting the training at iteration 0.
            # copying is only necessary when starting the training at iteration 0.
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Actual state_dict should be loaded after the pipe is created.
            # Actual state_dict should be loaded after the pipe is created.
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pipe.dit_ema_worker.copy_to(src_model=pipe.dit, tgt_model=pipe.dit_ema)
            pipe.dit_ema_worker.copy_to(src_model=pipe.dit, tgt_model=pipe.dit_ema)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# for n, p in pipe.dit.named_parameters():
        # for n, p in pipe.dit.named_parameters():
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# print(n, p.device)
        #     print(n, p.device)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.dit = pipe.dit.to(device=device, dtype=torch_dtype)
        pipe.dit = pipe.dit.to(device=device, dtype=torch_dtype)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.dit_ctrl = pipe.dit_ctrl.to(device=device, dtype=torch_dtype)
        pipe.dit_ctrl = pipe.dit_ctrl.to(device=device, dtype=torch_dtype)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.cuda.empty_cache()
        torch.cuda.empty_cache()

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 7. training states
        # 7. training states
        # 中文说明：根据条件选择执行分支；代码：if parallel_state.is_initialized():
        if parallel_state.is_initialized():
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.data_parallel_size = parallel_state.get_data_parallel_world_size()
            pipe.data_parallel_size = parallel_state.get_data_parallel_world_size()
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe.data_parallel_size = 1
            pipe.data_parallel_size = 1

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return pipe
        return pipe
    
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def broadcast_split_for_model_parallelsim(
    def broadcast_split_for_model_parallelsim(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x0_B_C_T_H_W: torch.Tensor,
        x0_B_C_T_H_W: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：condition: torch.Tensor,
        condition: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：epsilon_B_C_T_H_W: torch.Tensor,
        epsilon_B_C_T_H_W: torch.Tensor,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sigma_B_T: torch.Tensor,
        sigma_B_T: torch.Tensor,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Broadcast and split the input data and condition for model parallelism.
        Currently, we only support context parallelism.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cp_group = self.get_context_parallel_group()
        cp_group = self.get_context_parallel_group()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cp_size = 1 if cp_group is None else cp_group.size()
        cp_size = 1 if cp_group is None else cp_group.size()
        # 中文说明：根据条件选择执行分支；代码：if condition.is_video and cp_size > 1:
        if condition.is_video and cp_size > 1:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x0_B_C_T_H_W = broadcast_split_tensor(x0_B_C_T_H_W, seq_dim=2, process_group=cp_group)
            x0_B_C_T_H_W = broadcast_split_tensor(x0_B_C_T_H_W, seq_dim=2, process_group=cp_group)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：epsilon_B_C_T_H_W = broadcast_split_tensor(epsilon_B_C_T_H_W, seq_dim=2, process_group=cp_group)
            epsilon_B_C_T_H_W = broadcast_split_tensor(epsilon_B_C_T_H_W, seq_dim=2, process_group=cp_group)
            # 中文说明：根据条件选择执行分支；代码：if sigma_B_T is not None:
            if sigma_B_T is not None:
                # 中文说明：检查运行时假设是否成立；代码：assert sigma_B_T.ndim == 2, "sigma_B_T should be 2D tensor"
                assert sigma_B_T.ndim == 2, "sigma_B_T should be 2D tensor"
                # 中文说明：根据条件选择执行分支；代码：if sigma_B_T.shape[-1] == 1: # single sigma is shared across all frames
                if sigma_B_T.shape[-1] == 1:  # single sigma is shared across all frames
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_B_T = broadcast(sigma_B_T, cp_group)
                    sigma_B_T = broadcast(sigma_B_T, cp_group)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：else: # different sigma for each frame
                else:  # different sigma for each frame
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_B_T = broadcast_split_tensor(sigma_B_T, seq_dim=1, process_group=cp_group)
                    sigma_B_T = broadcast_split_tensor(sigma_B_T, seq_dim=1, process_group=cp_group)
            # 中文说明：根据条件选择执行分支；代码：if condition is not None:
            if condition is not None:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：condition = condition.broadcast(cp_group)
                condition = condition.broadcast(cp_group)
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.dit.enable_context_parallel(cp_group)
            self.dit.enable_context_parallel(cp_group)
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.dit_ctrl.enable_context_parallel(cp_group)
            self.dit_ctrl.enable_context_parallel(cp_group)
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.dit.disable_context_parallel()
            self.dit.disable_context_parallel()
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.dit_ctrl.disable_context_parallel()
            self.dit_ctrl.disable_context_parallel()

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return x0_B_C_T_H_W, condition, epsilon_B_C_T_H_W, sigma_B_T
        return x0_B_C_T_H_W, condition, epsilon_B_C_T_H_W, sigma_B_T
    
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def denoise(
    def denoise(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self, xt_B_C_T_H_W: torch.Tensor, sigma: torch.Tensor, condition: T2VCondition, use_cuda_grap...
        self, xt_B_C_T_H_W: torch.Tensor, sigma: torch.Tensor, condition: T2VCondition, use_cuda_graphs: bool = False
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> DenoisePrediction:
    ) -> DenoisePrediction:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Performs denoising on the input noise data, noise level, and condition

        Args:
            xt (torch.Tensor): The input noise data.
            sigma (torch.Tensor): The noise level.
            condition (T2VCondition): conditional information, generated from self.conditioner
            use_cuda_graphs (bool, optional): Whether to use CUDA Graphs for inference. Defaults to False.

        Returns:
            DenoisePrediction: The denoised prediction, it includes clean data predicton (x0), \
                noise prediction (eps_pred).
        """
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：根据条件选择执行分支；代码：if sigma.ndim == 1:
        if sigma.ndim == 1:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_B_T = rearrange(sigma, "b -> b 1")
            sigma_B_T = rearrange(sigma, "b -> b 1")
        # 中文说明：根据条件选择执行分支；代码：elif sigma.ndim == 2:
        elif sigma.ndim == 2:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_B_T = sigma
            sigma_B_T = sigma
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError(f"sigma shape {sigma.shape} is not supported")
            raise ValueError(f"sigma shape {sigma.shape} is not supported")

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_B_1_T_1_1 = rearrange(sigma_B_T, "b t -> b 1 t 1 1")
        sigma_B_1_T_1_1 = rearrange(sigma_B_T, "b t -> b 1 t 1 1")
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# get precondition for the network
        # get precondition for the network
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：c_skip_B_1_T_1_1, c_out_B_1_T_1_1, c_in_B_1_T_1_1, c_noise_B_1_T_1_1 = self.scaling(sigma=sig...
        c_skip_B_1_T_1_1, c_out_B_1_T_1_1, c_in_B_1_T_1_1, c_noise_B_1_T_1_1 = self.scaling(sigma=sigma_B_1_T_1_1)

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net_state_in_B_C_T_H_W = xt_B_C_T_H_W * c_in_B_1_T_1_1
        net_state_in_B_C_T_H_W = xt_B_C_T_H_W * c_in_B_1_T_1_1

        # 中文说明：根据条件选择执行分支；代码：if condition.is_video:
        if condition.is_video:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：condition_state_in_B_C_T_H_W = condition.gt_frames.type_as(net_state_in_B_C_T_H_W) / self.con...
            condition_state_in_B_C_T_H_W = condition.gt_frames.type_as(net_state_in_B_C_T_H_W) / self.config.sigma_data
            # 中文说明：根据条件选择执行分支；代码：if not condition.use_video_condition:
            if not condition.use_video_condition:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# When using random dropout, we zero out the ground truth frames
                # When using random dropout, we zero out the ground truth frames
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：condition_state_in_B_C_T_H_W = condition_state_in_B_C_T_H_W * 0
                condition_state_in_B_C_T_H_W = condition_state_in_B_C_T_H_W * 0

            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_, C, _, _, _ = xt_B_C_T_H_W.shape
            _, C, _, _, _ = xt_B_C_T_H_W.shape
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：condition_video_mask = condition.condition_video_input_mask_B_C_T_H_W.repeat(1, C, 1, 1, 1).t...
            condition_video_mask = condition.condition_video_input_mask_B_C_T_H_W.repeat(1, C, 1, 1, 1).type_as(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：net_state_in_B_C_T_H_W
                net_state_in_B_C_T_H_W
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )

            # 中文说明：根据条件选择执行分支；代码：if self.config.conditioning_strategy == str(ConditioningStrategy.FRAME_REPLACE):
            if self.config.conditioning_strategy == str(ConditioningStrategy.FRAME_REPLACE):
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# In case of frame replacement strategy, replace the first few frames of the video with the c...
                # In case of frame replacement strategy, replace the first few frames of the video with the conditional frames
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Update the c_noise as the conditional frames are clean and have very low noise
                # Update the c_noise as the conditional frames are clean and have very low noise

                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Make the first few frames of x_t be the ground truth frames
                # Make the first few frames of x_t be the ground truth frames
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net_state_in_B_C_T_H_W = (
                net_state_in_B_C_T_H_W = (
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：condition_state_in_B_C_T_H_W * condition_video_mask
                    condition_state_in_B_C_T_H_W * condition_video_mask
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：+ net_state_in_B_C_T_H_W * (1 - condition_video_mask)
                    + net_state_in_B_C_T_H_W * (1 - condition_video_mask)
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )

                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Adjust c_noise for the conditional frames
                # Adjust c_noise for the conditional frames
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sigma_cond_B_1_T_1_1 = torch.ones_like(sigma_B_1_T_1_1) * self.config.sigma_conditional
                sigma_cond_B_1_T_1_1 = torch.ones_like(sigma_B_1_T_1_1) * self.config.sigma_conditional
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_, _, _, c_noise_cond_B_1_T_1_1 = self.scaling(sigma=sigma_cond_B_1_T_1_1)
                _, _, _, c_noise_cond_B_1_T_1_1 = self.scaling(sigma=sigma_cond_B_1_T_1_1)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：condition_video_mask_B_1_T_1_1 = condition_video_mask.mean(dim=[1, 3, 4], keepdim=True)
                condition_video_mask_B_1_T_1_1 = condition_video_mask.mean(dim=[1, 3, 4], keepdim=True)
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：c_noise_B_1_T_1_1 = c_noise_cond_B_1_T_1_1 * condition_video_mask_B_1_T_1_1 + c_noise_B_1_T_1...
                c_noise_B_1_T_1_1 = c_noise_cond_B_1_T_1_1 * condition_video_mask_B_1_T_1_1 + c_noise_B_1_T_1_1 * (
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：1 - condition_video_mask_B_1_T_1_1
                    1 - condition_video_mask_B_1_T_1_1
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
            # 中文说明：根据条件选择执行分支；代码：elif self.config.conditioning_strategy == str(ConditioningStrategy.CHANNEL_CONCAT):
            elif self.config.conditioning_strategy == str(ConditioningStrategy.CHANNEL_CONCAT):
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# In case of channel concatenation strategy, concatenate the conditional frames in the channe...
                # In case of channel concatenation strategy, concatenate the conditional frames in the channel dimension
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：condition_state_in_masked_B_C_T_H_W = condition_state_in_B_C_T_H_W * condition_video_mask
                condition_state_in_masked_B_C_T_H_W = condition_state_in_B_C_T_H_W * condition_video_mask
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net_state_in_B_C_T_H_W = torch.cat([net_state_in_B_C_T_H_W, condition_state_in_masked_B_C_T_H...
                net_state_in_B_C_T_H_W = torch.cat([net_state_in_B_C_T_H_W, condition_state_in_masked_B_C_T_H_W], dim=1)

        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# In case of image batch, simply concatenate the 0 frames when channel concat strategy is used
            # In case of image batch, simply concatenate the 0 frames when channel concat strategy is used
            # 中文说明：根据条件选择执行分支；代码：if self.config.conditioning_strategy == str(ConditioningStrategy.CHANNEL_CONCAT):
            if self.config.conditioning_strategy == str(ConditioningStrategy.CHANNEL_CONCAT):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net_state_in_B_C_T_H_W = torch.cat(
                net_state_in_B_C_T_H_W = torch.cat(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：[net_state_in_B_C_T_H_W, torch.zeros_like(net_state_in_B_C_T_H_W)], dim=1
                    [net_state_in_B_C_T_H_W, torch.zeros_like(net_state_in_B_C_T_H_W)], dim=1
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_ctrl = self.dit_ctrl(
        x_ctrl = self.dit_ctrl(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_C_T_H_W=net_state_in_B_C_T_H_W.to(**self.tensor_kwargs),
            x_B_C_T_H_W=net_state_in_B_C_T_H_W.to(**self.tensor_kwargs),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：timesteps_B_T=c_noise_B_1_T_1_1.squeeze(dim=[1, 3, 4]).to(**self.tensor_kwargs),
            timesteps_B_T=c_noise_B_1_T_1_1.squeeze(dim=[1, 3, 4]).to(**self.tensor_kwargs),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**condition.to_dict(),
            **condition.to_dict(),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_cuda_graphs=use_cuda_graphs,
            use_cuda_graphs=use_cuda_graphs,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hint_key=self.config.hint_key
            hint_key=self.config.hint_key
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# forward pass through the network
        # forward pass through the network
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net_output_B_C_T_H_W = self.dit(
        net_output_B_C_T_H_W = self.dit(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_B_C_T_H_W=net_state_in_B_C_T_H_W.to(**self.tensor_kwargs),
            x_B_C_T_H_W=net_state_in_B_C_T_H_W.to(**self.tensor_kwargs),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：timesteps_B_T=c_noise_B_1_T_1_1.squeeze(dim=[1, 3, 4]).to(**self.tensor_kwargs),
            timesteps_B_T=c_noise_B_1_T_1_1.squeeze(dim=[1, 3, 4]).to(**self.tensor_kwargs),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：**condition.to_dict(),
            **condition.to_dict(),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_cuda_graphs=use_cuda_graphs,
            use_cuda_graphs=use_cuda_graphs,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x_ctrl=x_ctrl
            x_ctrl=x_ctrl
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：).float()
        ).float()

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x0_pred_B_C_T_H_W = c_skip_B_1_T_1_1 * xt_B_C_T_H_W + c_out_B_1_T_1_1 * net_output_B_C_T_H_W
        x0_pred_B_C_T_H_W = c_skip_B_1_T_1_1 * xt_B_C_T_H_W + c_out_B_1_T_1_1 * net_output_B_C_T_H_W
        # 中文说明：根据条件选择执行分支；代码：if condition.is_video:
        if condition.is_video:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Set the first few frames to the ground truth frames. This will ensure that the loss is not ...
            # Set the first few frames to the ground truth frames. This will ensure that the loss is not computed for the first few frames.
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：x0_pred_B_C_T_H_W = condition.gt_frames.type_as(
            x0_pred_B_C_T_H_W = condition.gt_frames.type_as(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：x0_pred_B_C_T_H_W
                x0_pred_B_C_T_H_W
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) * condition_video_mask + x0_pred_B_C_T_H_W * (1 - condition_video_mask)
            ) * condition_video_mask + x0_pred_B_C_T_H_W * (1 - condition_video_mask)

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# get noise prediction
        # get noise prediction
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：eps_pred_B_C_T_H_W = (xt_B_C_T_H_W - x0_pred_B_C_T_H_W) / sigma_B_1_T_1_1
        eps_pred_B_C_T_H_W = (xt_B_C_T_H_W - x0_pred_B_C_T_H_W) / sigma_B_1_T_1_1

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return DenoisePrediction(x0_pred_B_C_T_H_W, eps_pred_B_C_T_H_W, None)
        return DenoisePrediction(x0_pred_B_C_T_H_W, eps_pred_B_C_T_H_W, None)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def apply_fsdp(self, dp_mesh: DeviceMesh) -> None:
    def apply_fsdp(self, dp_mesh: DeviceMesh) -> None:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.dit.fully_shard(mesh=dp_mesh)
        self.dit.fully_shard(mesh=dp_mesh)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dit = fully_shard(self.dit, mesh=dp_mesh, reshard_after_forward=True)
        self.dit = fully_shard(self.dit, mesh=dp_mesh, reshard_after_forward=True)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：broadcast_dtensor_model_states(self.dit, dp_mesh)
        broadcast_dtensor_model_states(self.dit, dp_mesh)
        # 中文说明：根据条件选择执行分支；代码：if self.dit_ema:
        if self.dit_ema:
            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.dit_ema.fully_shard(mesh=dp_mesh)
            self.dit_ema.fully_shard(mesh=dp_mesh)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dit_ema = fully_shard(self.dit_ema, mesh=dp_mesh, reshard_after_forward=True)
            self.dit_ema = fully_shard(self.dit_ema, mesh=dp_mesh, reshard_after_forward=True)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：broadcast_dtensor_model_states(self.dit_ema, dp_mesh)
            broadcast_dtensor_model_states(self.dit_ema, dp_mesh)
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dit_ema_worker = DTensorFastEmaModelUpdater()
            self.dit_ema_worker = DTensorFastEmaModelUpdater()

        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.dit_ctrl.fully_shard(mesh=dp_mesh)
        self.dit_ctrl.fully_shard(mesh=dp_mesh)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.dit_ctrl = fully_shard(self.dit_ctrl, mesh=dp_mesh, reshard_after_forward=True)
        self.dit_ctrl = fully_shard(self.dit_ctrl, mesh=dp_mesh, reshard_after_forward=True)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：broadcast_dtensor_model_states(self.dit_ctrl, dp_mesh)
        broadcast_dtensor_model_states(self.dit_ctrl, dp_mesh)