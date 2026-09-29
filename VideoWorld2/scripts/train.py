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

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from loguru import logger as logging
from loguru import logger as logging

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
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
    # import pdb;pdb.set_trace()
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
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parser.add_argument(
    parser.add_argument(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："--dryrun",
        "--dryrun",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：action="store_true",
        action="store_true",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：help="Do a dry run without training. Useful for debugging the config.",
        help="Do a dry run without training. Useful for debugging the config.",
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
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
    # import pdb;pdb.set_trace()
    # 中文说明：根据条件选择执行分支；代码：if args.dryrun:
    if args.dryrun:
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：logging.info(
        logging.info(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："Config:\n" + config.pretty_print(use_color=True) + "\n" + pretty_print_overrides(args.opts, ...
            "Config:\n" + config.pretty_print(use_color=True) + "\n" + pretty_print_overrides(args.opts, use_color=True)
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.makedirs(config.job.path_local, exist_ok=True)
        os.makedirs(config.job.path_local, exist_ok=True)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：LazyConfig.save_yaml(config, f"{config.job.path_local}/config.yaml")
        LazyConfig.save_yaml(config, f"{config.job.path_local}/config.yaml")
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"{config.job.path_local}/config.yaml")
        print(f"{config.job.path_local}/config.yaml")
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Launch the training job.
        # Launch the training job.
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：launch(config, args)
        launch(config, args)
