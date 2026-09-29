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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from apex.multi_tensor_apply import multi_tensor_applier
from apex.multi_tensor_apply import multi_tensor_applier

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import distributed, log
from imaginaire.utils import distributed, log
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.misc import get_local_tensor_if_DTensor
from imaginaire.utils.misc import get_local_tensor_if_DTensor


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class FusedAdam(torch.optim.Optimizer):
class FusedAdam(torch.optim.Optimizer):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Implements Adam algorithm.
    """Implements Adam algorithm.

    Currently GPU-only.  Requires Apex to be installed via
    ``pip install -v --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" ./``.

    This version of fused Adam implements 2 fusions.

      * Fusion of the Adam update's elementwise operations
      * A multi-tensor apply launch that batches the elementwise updates applied to all the model's parameters
        into one or a few kernel launches.

    :class:`apex.optimizers.FusedAdam` may be used as a drop-in replacement for ``torch.optim.AdamW``,
    or ``torch.optim.Adam`` with ``adam_w_mode=False``::

        opt = apex.optimizers.FusedAdam(model.parameters(), lr = ....)
        ...
        opt.step()

    :class:`apex.optimizers.FusedAdam` may be used with or without Amp.  If you wish to use :class:`FusedAdam` with Amp,
    you may choose any ``opt_level``::

        opt = apex.optimizers.FusedAdam(model.parameters(), lr = ....)
        model, opt = amp.initialize(model, opt, opt_level="O0" or "O1 or "O2")
        ...
        opt.step()

    In general, ``opt_level="O1"`` is recommended.


    .. warning::
        A previous version of :class:`FusedAdam` allowed a number of additional arguments to ``step``.
        These additional arguments are now deprecated and unnecessary.

    Adam was been proposed in `Adam: A Method for Stochastic Optimization`_.

    Arguments:
        params (iterable): iterable of parameters to optimize or dicts defining
            parameter groups.
        lr (float, optional): learning rate. (default: 1e-3)
        betas (Tuple[float, float], optional): coefficients used for computing
            running averages of gradient and its square. (default: (0.9, 0.999))
        eps (float, optional): term added to the denominator to improve
            numerical stability. (default: 1e-8)
        weight_decay (float, optional): weight decay (L2 penalty) (default: 0)
        amsgrad (boolean, optional): whether to use the AMSGrad variant of this
            algorithm from the paper `On the Convergence of Adam and Beyond`_
            (default: False) NOT SUPPORTED in FusedAdam!
        adam_w_mode (boolean, optional): Apply L2 regularization or weight decay
            True for decoupled weight decay(also known as AdamW) (default: True)
        capturable (bool, optional): whether to use the version of the optimizer
            that can be used with CUDA Graphs. (default: False)
        master_weights (bool, optional): whether to maintain FP32 master weights
           in the optimizer with FP16 mixed precision training, currently can
           only be used with capturable set to True. (default: False)

    .. _Adam - A Method for Stochastic Optimization:
        https://arxiv.org/abs/1412.6980
    .. _On the Convergence of Adam and Beyond:
        https://openreview.net/forum?id=ryQu7f-RZ
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(
    def __init__(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：self,
        self,
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：params,
        params,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lr=1e-3,
        lr=1e-3,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：bias_correction=True,
        bias_correction=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：betas=(0.9, 0.999),
        betas=(0.9, 0.999),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：eps=1e-8,
        eps=1e-8,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：adam_w_mode=True,
        adam_w_mode=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：weight_decay=0.0,
        weight_decay=0.0,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：amsgrad=False,
        amsgrad=False,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：capturable=False,
        capturable=False,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：master_weights=False,
        master_weights=False,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：根据条件选择执行分支；代码：if amsgrad:
        if amsgrad:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise RuntimeError("FusedAdam does not support the AMSGrad variant.")
            raise RuntimeError("FusedAdam does not support the AMSGrad variant.")
        # 中文说明：根据条件选择执行分支；代码：if master_weights and not capturable:
        if master_weights and not capturable:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise RuntimeError("Master weights is currently only supported with the capturable version.")
            raise RuntimeError("Master weights is currently only supported with the capturable version.")
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# If the optimizer is capturable then LR should be a tensor (on GPU)
        # If the optimizer is capturable then LR should be a tensor (on GPU)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.warning(f"FusedAdam master_weights: {master_weights} capturable: {capturable}")
        log.warning(f"FusedAdam master_weights: {master_weights} capturable: {capturable}")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lr = torch.tensor(lr, dtype=torch.float32) if capturable else lr
        lr = torch.tensor(lr, dtype=torch.float32) if capturable else lr
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：defaults = dict(lr=lr, bias_correction=bias_correction, betas=betas, eps=eps, weight_decay=we...
        defaults = dict(lr=lr, bias_correction=bias_correction, betas=betas, eps=eps, weight_decay=weight_decay)
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super(FusedAdam, self).__init__(params, defaults)
        super(FusedAdam, self).__init__(params, defaults)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.adam_w_mode = 1 if adam_w_mode else 0
        self.adam_w_mode = 1 if adam_w_mode else 0

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.capturable = capturable
        self.capturable = capturable
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.master_weights = master_weights
        self.master_weights = master_weights

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.param_groups_master = None
        self.param_groups_master = None

        # 中文说明：根据条件选择执行分支；代码：if capturable:
        if capturable:
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for idx, group in enumerate(self.param_groups):
            for idx, group in enumerate(self.param_groups):
                # 中文说明：根据条件选择执行分支；代码：if len(group["params"]) == 0:
                if len(group["params"]) == 0:
                    # 中文说明：执行循环控制或空操作；代码：continue
                    continue
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：device = group["params"][0].device
                device = group["params"][0].device
                # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for item in ["lr"]:
                for item in ["lr"]:
                    # 中文说明：根据条件选择执行分支；代码：if isinstance(group[item], float):
                    if isinstance(group[item], float):
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group[item] = torch.tensor(group[item], dtype=torch.float32)
                        group[item] = torch.tensor(group[item], dtype=torch.float32)
                    # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.param_groups[idx][item] = group[item].to(device=device)
                    self.param_groups[idx][item] = group[item].to(device=device)

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._step_supports_amp_scaling = True
            self._step_supports_amp_scaling = True

        # 中文说明：根据条件选择执行分支；代码：if multi_tensor_applier.available:
        if multi_tensor_applier.available:
            # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import amp_C
            import amp_C

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Skip buffer
            # Skip buffer
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self._dummy_overflow_buf = torch.tensor([0], dtype=torch.int, device="cuda")
            self._dummy_overflow_buf = torch.tensor([0], dtype=torch.int, device="cuda")
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.multi_tensor_adam = amp_C.multi_tensor_adam
            self.multi_tensor_adam = amp_C.multi_tensor_adam
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.multi_tensor_adam_capturable = amp_C.multi_tensor_adam_capturable
            self.multi_tensor_adam_capturable = amp_C.multi_tensor_adam_capturable
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.multi_tensor_adam_capturable_master = amp_C.multi_tensor_adam_capturable_master
            self.multi_tensor_adam_capturable_master = amp_C.multi_tensor_adam_capturable_master
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise RuntimeError("apex.optimizers.FusedAdam requires cuda extensions")
            raise RuntimeError("apex.optimizers.FusedAdam requires cuda extensions")

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def step(self, closure=None, grads=None, output_params=None, scale=None, grad_norms=None, gra...
    def step(self, closure=None, grads=None, output_params=None, scale=None, grad_norms=None, grad_scaler=None):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Performs a single optimization step.
        """Performs a single optimization step.

        Arguments:
            closure (callable, optional): A closure that reevaluates the model
                and returns the loss.

        The remaining arguments are deprecated, and are only retained (for the moment) for error-checking purposes.
        """
        # 中文说明：根据条件选择执行分支；代码：if any(p is not None for p in [grads, output_params, scale, grad_norms]):
        if any(p is not None for p in [grads, output_params, scale, grad_norms]):
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise RuntimeError(
            raise RuntimeError(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："FusedAdam has been updated. "
                "FusedAdam has been updated. "
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："Simply initialize it identically to torch.optim.Adam, and call step() with no arguments."
                "Simply initialize it identically to torch.optim.Adam, and call step() with no arguments."
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
            )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：loss = None
        loss = None
        # 中文说明：根据条件选择执行分支；代码：if closure is not None:
        if closure is not None:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：loss = closure()
            loss = closure()

        # 中文说明：根据条件选择执行分支；代码：if self.param_groups_master is None:
        if self.param_groups_master is None:
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Create full precision master weights
            # Create full precision master weights
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.param_groups_master = []
            self.param_groups_master = []
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i, pg in enumerate(self.param_groups):
            for i, pg in enumerate(self.param_groups):
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：param_list = pg["params"]
                param_list = pg["params"]
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.param_groups_master.append(
                self.param_groups_master.append(
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{
                    {
                        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Change related to master weights
                        # Change related to master weights
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："params": [
                        "params": [
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：get_local_tensor_if_DTensor(p).clone().detach().float() if self.master_weights else None
                            get_local_tensor_if_DTensor(p).clone().detach().float() if self.master_weights else None
                            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for p in param_list
                            for p in param_list
                        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：],
                        ],
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
                    }
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )

        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for group, group_master in zip(self.param_groups, self.param_groups_master):
        for group, group_master in zip(self.param_groups, self.param_groups_master):
            # 中文说明：根据条件选择执行分支；代码：if len(group["params"]) == 0:
            if len(group["params"]) == 0:
                # 中文说明：执行循环控制或空操作；代码：continue
                continue
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：device = group["params"][0].device
            device = group["params"][0].device
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：bias_correction = 1 if "bias_correction" in group and group["bias_correction"] else 0
            bias_correction = 1 if "bias_correction" in group and group["bias_correction"] else 0
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：beta1, beta2 = group["betas"]
            beta1, beta2 = group["betas"]

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# assume same step across group now to simplify things
            # assume same step across group now to simplify things
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# per parameter step can be easily support by making it tensor, or pass list into kernel
            # per parameter step can be easily support by making it tensor, or pass list into kernel
            # 中文说明：根据条件选择执行分支；代码：if "step" in group:
            if "step" in group:
                # 中文说明：根据条件选择执行分支；代码：if self.capturable:
                if self.capturable:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group["step"] = (
                    group["step"] = (
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group["step"].to(device=device)
                        group["step"].to(device=device)
                        # 中文说明：根据条件选择执行分支；代码：if isinstance(group["step"], torch.Tensor)
                        if isinstance(group["step"], torch.Tensor)
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：else torch.tensor(group["step"], dtype=torch.int32, device=device)
                        else torch.tensor(group["step"], dtype=torch.int32, device=device)
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group["step"] += (self._dummy_overflow_buf != 1).to(torch.int)
                    group["step"] += (self._dummy_overflow_buf != 1).to(torch.int)
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group["step"] += 1
                    group["step"] += 1
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group["step"] = 1 if not self.capturable else torch.tensor([1], dtype=torch.int, device=device)
                group["step"] = 1 if not self.capturable else torch.tensor([1], dtype=torch.int, device=device)

            # 中文说明：根据条件选择执行分支；代码：if self.capturable:
            if self.capturable:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group["lr"] = (
                group["lr"] = (
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group["lr"].to(device=device)
                    group["lr"].to(device=device)
                    # 中文说明：根据条件选择执行分支；代码：if isinstance(group["lr"], torch.Tensor)
                    if isinstance(group["lr"], torch.Tensor)
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：else torch.tensor(group["lr"], dtype=torch.float32, device=device)
                    else torch.tensor(group["lr"], dtype=torch.float32, device=device)
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# create lists for multi-tensor apply
            # create lists for multi-tensor apply
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：g_16, p_16, m_16, v_16 = [], [], [], []
            g_16, p_16, m_16, v_16 = [], [], [], []
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：g_bf, p_bf, m_bf, v_bf = [], [], [], []
            g_bf, p_bf, m_bf, v_bf = [], [], [], []
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：g_32, p_32, m_32, v_32 = [], [], [], []
            g_32, p_32, m_32, v_32 = [], [], [], []
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：p_16_master = []
            p_16_master = []
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：p_32_master = []
            p_32_master = []
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：bf16_master = []
            bf16_master = []

            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for p, p_master in zip(group["params"], group_master["params"]):
            for p, p_master in zip(group["params"], group_master["params"]):
                # 中文说明：根据条件选择执行分支；代码：if p.grad is None:
                if p.grad is None:
                    # 中文说明：执行循环控制或空操作；代码：continue
                    continue
                # 中文说明：根据条件选择执行分支；代码：if p.grad.data.is_sparse:
                if p.grad.data.is_sparse:
                    # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise RuntimeError(
                    raise RuntimeError(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："FusedAdam does not support sparse gradients, please consider SparseAdam instead"
                        "FusedAdam does not support sparse gradients, please consider SparseAdam instead"
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )

                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state = self.state[p]
                state = self.state[p]
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# State initialization
                # State initialization
                # 中文说明：根据条件选择执行分支；代码：if len(state) == 0:
                if len(state) == 0:
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Exponential moving average of gradient values
                    # Exponential moving average of gradient values
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Change that makes .step() not crash
                    # Change that makes .step() not crash
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state["exp_avg"] = torch.zeros_like(get_local_tensor_if_DTensor(p).data).float()
                    state["exp_avg"] = torch.zeros_like(get_local_tensor_if_DTensor(p).data).float()
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Exponential moving average of squared gradient values
                    # Exponential moving average of squared gradient values
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Change that makes .step() not crash
                    # Change that makes .step() not crash
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state["exp_avg_sq"] = torch.zeros_like(get_local_tensor_if_DTensor(p).data).float()
                    state["exp_avg_sq"] = torch.zeros_like(get_local_tensor_if_DTensor(p).data).float()

                # 中文说明：根据条件选择执行分支；代码：if p.dtype == torch.float16:
                if p.dtype == torch.float16:
                    # 中文说明：根据条件选择执行分支；代码：if self.master_weights:
                    if self.master_weights:
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：p_16_master.append(get_local_tensor_if_DTensor(p_master).data)
                        p_16_master.append(get_local_tensor_if_DTensor(p_master).data)
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：g_16.append(get_local_tensor_if_DTensor(p.grad))
                    g_16.append(get_local_tensor_if_DTensor(p.grad))
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：p_16.append(get_local_tensor_if_DTensor(p))
                    p_16.append(get_local_tensor_if_DTensor(p))
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：m_16.append(state["exp_avg"])
                    m_16.append(state["exp_avg"])
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v_16.append(state["exp_avg_sq"])
                    v_16.append(state["exp_avg_sq"])
                # 中文说明：根据条件选择执行分支；代码：elif p.dtype == torch.bfloat16:
                elif p.dtype == torch.bfloat16:
                    # 中文说明：根据条件选择执行分支；代码：if self.master_weights:
                    if self.master_weights:
                        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Change that makes .step() not crash
                        # Change that makes .step() not crash
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：bf16_master.append(get_local_tensor_if_DTensor(p_master).data)
                        bf16_master.append(get_local_tensor_if_DTensor(p_master).data)
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Change that makes .step() not crash
                    # Change that makes .step() not crash
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：g_bf.append(get_local_tensor_if_DTensor(p.grad))
                    g_bf.append(get_local_tensor_if_DTensor(p.grad))
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Change that makes .step() not crash
                    # Change that makes .step() not crash
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：p_bf.append(get_local_tensor_if_DTensor(p))
                    p_bf.append(get_local_tensor_if_DTensor(p))
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：m_bf.append(state["exp_avg"])
                    m_bf.append(state["exp_avg"])
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v_bf.append(state["exp_avg_sq"])
                    v_bf.append(state["exp_avg_sq"])
                # 中文说明：根据条件选择执行分支；代码：elif p.dtype == torch.float32:
                elif p.dtype == torch.float32:
                    # 中文说明：根据条件选择执行分支；代码：if self.master_weights:
                    if self.master_weights:
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：p_32_master.append(p_master.data)
                        p_32_master.append(p_master.data)
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：g_32.append(p.grad.data)
                    g_32.append(p.grad.data)
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：p_32.append(p.data)
                    p_32.append(p.data)
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：m_32.append(state["exp_avg"])
                    m_32.append(state["exp_avg"])
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：v_32.append(state["exp_avg_sq"])
                    v_32.append(state["exp_avg_sq"])
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise RuntimeError("FusedAdam only support fp16 and fp32.")
                    raise RuntimeError("FusedAdam only support fp16 and fp32.")

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# If the optimizer is capturable, then if there's a grad scaler it works
            # If the optimizer is capturable, then if there's a grad scaler it works
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# on the GPU + a different multi_tensor_applier should be called
            # on the GPU + a different multi_tensor_applier should be called
            # 中文说明：根据条件选择执行分支；代码：if self.capturable:
            if self.capturable:
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# overflow check of gradients
                # overflow check of gradients
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：found_inf = (
                found_inf = (
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：grad_scaler._check_inf_per_device(self)[device]
                    grad_scaler._check_inf_per_device(self)[device]
                    # 中文说明：根据条件选择执行分支；代码：if grad_scaler is not None
                    if grad_scaler is not None
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：else torch.zeros((1,), device=device)
                    else torch.zeros((1,), device=device)
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._dummy_overflow_buf.copy_(found_inf)
                self._dummy_overflow_buf.copy_(found_inf)

                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# get unscale scale factor
                # get unscale scale factor
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：scale, inv_scale = None, None
                scale, inv_scale = None, None
                # 中文说明：根据条件选择执行分支；代码：if grad_scaler:
                if grad_scaler:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scale = grad_scaler._get_scale_async()
                    scale = grad_scaler._get_scale_async()
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：inv_scale = scale.double().reciprocal().float()
                    inv_scale = scale.double().reciprocal().float()
                # 中文说明：根据条件选择执行分支；代码：else:
                else:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scale = torch.ones((1,), device=device, dtype=torch.float32)
                    scale = torch.ones((1,), device=device, dtype=torch.float32)
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：inv_scale = torch.ones((1,), device=device, dtype=torch.float32)
                    inv_scale = torch.ones((1,), device=device, dtype=torch.float32)

                # 中文说明：根据条件选择执行分支；代码：if len(g_16) > 0:
                if len(g_16) > 0:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：multi_tensor_applier(
                    multi_tensor_applier(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：(
                        (
                            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.multi_tensor_adam_capturable_master
                            self.multi_tensor_adam_capturable_master
                            # 中文说明：根据条件选择执行分支；代码：if self.master_weights
                            if self.master_weights
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：else self.multi_tensor_adam_capturable
                            else self.multi_tensor_adam_capturable
                        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
                        ),
                        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._dummy_overflow_buf,
                        self._dummy_overflow_buf,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：[g_16, p_16, m_16, v_16, p_16_master] if self.master_weights else [g_16, p_16, m_16, v_16],
                        [g_16, p_16, m_16, v_16, p_16_master] if self.master_weights else [g_16, p_16, m_16, v_16],
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group["lr"],
                        group["lr"],
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：beta1,
                        beta1,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：beta2,
                        beta2,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group["eps"],
                        group["eps"],
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group["step"],
                        group["step"],
                        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.adam_w_mode,
                        self.adam_w_mode,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：bias_correction,
                        bias_correction,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group["weight_decay"],
                        group["weight_decay"],
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：inv_scale,
                        inv_scale,
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )

                # 中文说明：根据条件选择执行分支；代码：if len(g_bf) > 0:
                if len(g_bf) > 0:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：multi_tensor_applier(
                    multi_tensor_applier(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：(
                        (
                            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.multi_tensor_adam_capturable_master
                            self.multi_tensor_adam_capturable_master
                            # 中文说明：根据条件选择执行分支；代码：if self.master_weights
                            if self.master_weights
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：else self.multi_tensor_adam_capturable
                            else self.multi_tensor_adam_capturable
                        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
                        ),
                        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._dummy_overflow_buf,
                        self._dummy_overflow_buf,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：[g_bf, p_bf, m_bf, v_bf, bf16_master] if self.master_weights else [g_bf, p_bf, m_bf, v_bf],
                        [g_bf, p_bf, m_bf, v_bf, bf16_master] if self.master_weights else [g_bf, p_bf, m_bf, v_bf],
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group["lr"],
                        group["lr"],
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：beta1,
                        beta1,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：beta2,
                        beta2,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group["eps"],
                        group["eps"],
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group["step"],
                        group["step"],
                        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.adam_w_mode,
                        self.adam_w_mode,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：bias_correction,
                        bias_correction,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group["weight_decay"],
                        group["weight_decay"],
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：inv_scale,
                        inv_scale,
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )

                # 中文说明：根据条件选择执行分支；代码：if len(g_32) > 0:
                if len(g_32) > 0:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：multi_tensor_applier(
                    multi_tensor_applier(
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：(
                        (
                            # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.multi_tensor_adam_capturable_master
                            self.multi_tensor_adam_capturable_master
                            # 中文说明：根据条件选择执行分支；代码：if self.master_weights
                            if self.master_weights
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：else self.multi_tensor_adam_capturable
                            else self.multi_tensor_adam_capturable
                        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
                        ),
                        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._dummy_overflow_buf,
                        self._dummy_overflow_buf,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：[g_32, p_32, m_32, v_32, p_32_master] if self.master_weights else [g_32, p_32, m_32, v_32],
                        [g_32, p_32, m_32, v_32, p_32_master] if self.master_weights else [g_32, p_32, m_32, v_32],
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group["lr"],
                        group["lr"],
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：beta1,
                        beta1,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：beta2,
                        beta2,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group["eps"],
                        group["eps"],
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group["step"],
                        group["step"],
                        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.adam_w_mode,
                        self.adam_w_mode,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：bias_correction,
                        bias_correction,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group["weight_decay"],
                        group["weight_decay"],
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：inv_scale,
                        inv_scale,
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：根据条件选择执行分支；代码：if len(g_16) > 0:
                if len(g_16) > 0:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：multi_tensor_applier(
                    multi_tensor_applier(
                        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.multi_tensor_adam,
                        self.multi_tensor_adam,
                        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._dummy_overflow_buf,
                        self._dummy_overflow_buf,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：[g_16, p_16, m_16, v_16],
                        [g_16, p_16, m_16, v_16],
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group["lr"],
                        group["lr"],
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：beta1,
                        beta1,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：beta2,
                        beta2,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group["eps"],
                        group["eps"],
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group["step"],
                        group["step"],
                        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.adam_w_mode,
                        self.adam_w_mode,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：bias_correction,
                        bias_correction,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group["weight_decay"],
                        group["weight_decay"],
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )

                # 中文说明：根据条件选择执行分支；代码：if len(g_bf) > 0:
                if len(g_bf) > 0:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：multi_tensor_applier(
                    multi_tensor_applier(
                        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.multi_tensor_adam,
                        self.multi_tensor_adam,
                        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._dummy_overflow_buf,
                        self._dummy_overflow_buf,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：[g_bf, p_bf, m_bf, v_bf],
                        [g_bf, p_bf, m_bf, v_bf],
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group["lr"],
                        group["lr"],
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：beta1,
                        beta1,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：beta2,
                        beta2,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group["eps"],
                        group["eps"],
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group["step"],
                        group["step"],
                        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.adam_w_mode,
                        self.adam_w_mode,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：bias_correction,
                        bias_correction,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group["weight_decay"],
                        group["weight_decay"],
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )

                # 中文说明：根据条件选择执行分支；代码：if len(g_32) > 0:
                if len(g_32) > 0:
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：multi_tensor_applier(
                    multi_tensor_applier(
                        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.multi_tensor_adam,
                        self.multi_tensor_adam,
                        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self._dummy_overflow_buf,
                        self._dummy_overflow_buf,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：[g_32, p_32, m_32, v_32],
                        [g_32, p_32, m_32, v_32],
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group["lr"],
                        group["lr"],
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：beta1,
                        beta1,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：beta2,
                        beta2,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group["eps"],
                        group["eps"],
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group["step"],
                        group["step"],
                        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：self.adam_w_mode,
                        self.adam_w_mode,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：bias_correction,
                        bias_correction,
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group["weight_decay"],
                        group["weight_decay"],
                    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                    )

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return loss
        return loss

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def load_state_dict(self, state_dict):
    def load_state_dict(self, state_dict):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().load_state_dict(state_dict)
        super().load_state_dict(state_dict)
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for group in self.param_groups:
        for group in self.param_groups:
            # 中文说明：根据条件选择执行分支；代码：if self.capturable:
            if self.capturable:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group["lr"] = (
                group["lr"] = (
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group["lr"].cuda()
                    group["lr"].cuda()
                    # 中文说明：根据条件选择执行分支；代码：if isinstance(group["lr"], torch.Tensor)
                    if isinstance(group["lr"], torch.Tensor)
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：else torch.tensor(group["lr"], dtype=torch.float32).cuda()
                    else torch.tensor(group["lr"], dtype=torch.float32).cuda()
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                )

            # 中文说明：根据条件选择执行分支；代码：if "step" in group:
            if "step" in group:
                # 中文说明：根据条件选择执行分支；代码：if self.capturable:
                if self.capturable:
                    # 中文说明：根据条件选择执行分支；代码：if distributed.get_rank() == 0:
                    if distributed.get_rank() == 0:
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：step = (
                        step = (
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：group["step"].cuda()
                            group["step"].cuda()
                            # 中文说明：根据条件选择执行分支；代码：if isinstance(group["step"], torch.Tensor)
                            if isinstance(group["step"], torch.Tensor)
                            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：else torch.tensor([group["step"]], dtype=torch.int32).cuda()
                            else torch.tensor([group["step"]], dtype=torch.int32).cuda()
                        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
                        )
                    # 中文说明：根据条件选择执行分支；代码：else:
                    else:
                        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：step = torch.zeros(1, dtype=torch.int32).cuda()
                        step = torch.zeros(1, dtype=torch.int32).cuda()
                    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# make it compatible with FSDP optimizer
                    # make it compatible with FSDP optimizer
                    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：distributed.broadcast(step, 0)
                    distributed.broadcast(step, 0)
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group["step"] = step
                    group["step"] = step
                # 中文说明：根据条件选择执行分支；代码：elif isinstance(group["step"], torch.Tensor):
                elif isinstance(group["step"], torch.Tensor):
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group["step"] = group["step"].item()
                    group["step"] = group["step"].item()
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for p in group["params"]:
            for p in group["params"]:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state = self.state[p]
                state = self.state[p]
                # 中文说明：根据条件选择执行分支；代码：if "exp_avg" in state:
                if "exp_avg" in state:
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state["exp_avg"] = state["exp_avg"].float()
                    state["exp_avg"] = state["exp_avg"].float()
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：state["exp_avg_sq"] = state["exp_avg_sq"].float()
                    state["exp_avg_sq"] = state["exp_avg_sq"].float()
