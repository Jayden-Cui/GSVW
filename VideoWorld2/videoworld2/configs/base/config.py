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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any, List
from typing import Any, List

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import attrs
import attrs

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.configs.action_conditioned.defaults.data import register_training_and_val_da...
from videoworld2.configs.action_conditioned.defaults.data import register_training_and_val_data_action_conditioned
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.configs.action_conditioned.defaults.model import register_model_action_condi...
from videoworld2.configs.action_conditioned.defaults.model import register_model_action_conditioned
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.configs.base.defaults.callbacks import register_callbacks
from videoworld2.configs.base.defaults.callbacks import register_callbacks
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.configs.base.defaults.checkpoint import register_checkpoint
from videoworld2.configs.base.defaults.checkpoint import register_checkpoint
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.configs.base.defaults.data import register_training_and_val_data
from videoworld2.configs.base.defaults.data import register_training_and_val_data
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.configs.base.defaults.ema import register_ema
from videoworld2.configs.base.defaults.ema import register_ema
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.configs.base.defaults.model import register_model
from videoworld2.configs.base.defaults.model import register_model
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.configs.base.defaults.optimizer import register_optimizer
from videoworld2.configs.base.defaults.optimizer import register_optimizer
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.configs.base.defaults.scheduler import register_scheduler
from videoworld2.configs.base.defaults.scheduler import register_scheduler
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire import config
from imaginaire import config
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.trainer import ImaginaireTrainer as Trainer
from imaginaire.trainer import ImaginaireTrainer as Trainer
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.config_helper import import_all_modules_from_package
from imaginaire.utils.config_helper import import_all_modules_from_package


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Config(config.Config):
class Config(config.Config):
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# default config groups that will be used unless overwritten
    # default config groups that will be used unless overwritten
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# see config groups in registry.py
    # see config groups in registry.py
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：defaults: List[Any] = attrs.field(
    defaults: List[Any] = attrs.field(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：factory=lambda: [
        factory=lambda: [
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："_self_",
            "_self_",
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"dataloader_train": None},
            {"dataloader_train": None},
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"dataloader_val": None},
            {"dataloader_val": None},
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"optimizer": "fusedadamw"},
            {"optimizer": "fusedadamw"},
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"scheduler": "constant"},
            {"scheduler": "constant"},
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"model": "predict2_video2world_fsdp_2b"},
            {"model": "predict2_video2world_fsdp_2b"},
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"callbacks": ["basic"]},
            {"callbacks": ["basic"]},
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"net": None},
            {"net": None},
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"ema": None},
            {"ema": None},
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"checkpoint": None},
            {"checkpoint": None},
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"ckpt_type": None},
            {"ckpt_type": None},
            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# the list is with order, we need global experiment to be the last one
            # the list is with order, we need global experiment to be the last one
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"experiment": None},
            {"experiment": None},
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]
        ]
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def make_config() -> Config:
def make_config() -> Config:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：c = Config(
    c = Config(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model=None,
        model=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：optimizer=None,
        optimizer=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scheduler=None,
        scheduler=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataloader_train=None,
        dataloader_train=None,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataloader_val=None,
        dataloader_val=None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Specifying values through instances of attrs
    # Specifying values through instances of attrs
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：c.job.project = "videoworld2"
    c.job.project = "videoworld2"
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：c.job.group = "debug"
    c.job.group = "debug"
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：c.job.name = "delete_${now:%Y-%m-%d}_${now:%H-%M-%S}"
    c.job.name = "delete_${now:%Y-%m-%d}_${now:%H-%M-%S}"

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：c.trainer.type = Trainer
    c.trainer.type = Trainer
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：c.trainer.max_iter = 400_000
    c.trainer.max_iter = 400_000
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：c.trainer.logging_iter = 10
    c.trainer.logging_iter = 10
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：c.trainer.validation_iter = 10000
    c.trainer.validation_iter = 10000
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：c.trainer.run_validation = True
    c.trainer.run_validation = True
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：c.trainer.max_val_iter = 10000
    c.trainer.max_val_iter = 10000
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：c.trainer.callbacks = None
    c.trainer.callbacks = None

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Call this function to register config groups for advanced overriding. the order follows the...
    # Call this function to register config groups for advanced overriding. the order follows the default config groups
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：register_training_and_val_data()
    register_training_and_val_data()
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：register_optimizer()
    register_optimizer()
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：register_scheduler()
    register_scheduler()
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：register_model()
    register_model()

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：register_ema()
    register_ema()
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：register_checkpoint()
    register_checkpoint()
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：register_callbacks()
    register_callbacks()

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# action conditional post-training config
    # action conditional post-training config
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：register_training_and_val_data_action_conditioned()
    register_training_and_val_data_action_conditioned()
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：register_model_action_conditioned()
    register_model_action_conditioned()

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# experiment config are defined in the experiment folder
    # experiment config are defined in the experiment folder
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# call import_all_modules_from_package to register them
    # call import_all_modules_from_package to register them
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：import_all_modules_from_package("videoworld2.configs.base.experiment", reload=True)
    import_all_modules_from_package("videoworld2.configs.base.experiment", reload=True)
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：import_all_modules_from_package("videoworld2.configs.action_conditioned.experiment", reload=T...
    import_all_modules_from_package("videoworld2.configs.action_conditioned.experiment", reload=True)
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return c
    return c
