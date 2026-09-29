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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import time
import time

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch import Tensor
from torch import Tensor

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.callbacks.every_n import EveryN
from imaginaire.callbacks.every_n import EveryN
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.model import ImaginaireModel
from imaginaire.model import ImaginaireModel
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.trainer import ImaginaireTrainer
from imaginaire.trainer import ImaginaireTrainer
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.distributed import rank0_only
from imaginaire.utils.distributed import rank0_only
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io import easy_io
from imaginaire.utils.easy_io import easy_io
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch.distributed as dist
import torch.distributed as dist

# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class LDMCallback(EveryN):
class LDMCallback(EveryN):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Args:
        hit_thres (int): Number of iterations to wait before logging.
    """

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, *args, **kwargs):
    def __init__(self, *args, **kwargs):
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：super().__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)
        
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def on_validation_end(self, model: ImaginaireModel, iteration: int = 0) -> None:
    def on_validation_end(self, model: ImaginaireModel, iteration: int = 0) -> None:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：world_size = dist.get_world_size()
        world_size = dist.get_world_size()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_gather_data = [None for _ in range(world_size)]
        _gather_data = [None for _ in range(world_size)]

        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dist.all_gather_object(_gather_data, model.validation_results)
        dist.all_gather_object(_gather_data, model.validation_results)
        # 中文说明：根据条件选择执行分支；代码：if dist.get_rank() == 0:
        if dist.get_rank() == 0:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：gather_data = []
            gather_data = []
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for data in _gather_data:
            for data in _gather_data:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：gather_data.extend(data)
                gather_data.extend(data)
            

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：latent_code_infos = []
            latent_code_infos = []
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for item in gather_data:
            for item in gather_data:
               
                # 中文说明：根据条件选择执行分支；代码：if 'latent_codes' in item:
                if 'latent_codes' in item:
                    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for latent_code, video_path in zip(item['latent_codes'], item['video_path']):
                    for latent_code, video_path in zip(item['latent_codes'], item['video_path']):
                        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：latent_code_infos.append((latent_code.cpu().tolist(), video_path))
                        latent_code_infos.append((latent_code.cpu().tolist(), video_path))



            # 中文说明：根据条件选择执行分支；代码：if len(latent_code_infos) > 0:
            if len(latent_code_infos) > 0:
                # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.save(latent_code_infos, f'latent_code_infos.pt')
                torch.save(latent_code_infos, f'latent_code_infos.pt')
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.info(f"Latent Codes Saved")
            log.info(f"Latent Codes Saved")
            
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dist.barrier()
        dist.barrier()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model.validation_results = []
        model.validation_results = []
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return
        return
