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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import pandas as pd
import pandas as pd
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch


# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class TensorDataset(torch.utils.data.Dataset):
class TensorDataset(torch.utils.data.Dataset):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __init__(self, base_path, metadata_path, steps_per_epoch, debug_without_randomness=False):
    def __init__(self, base_path, metadata_path, steps_per_epoch, debug_without_randomness=False):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：metadata = pd.read_csv(metadata_path)
        metadata = pd.read_csv(metadata_path)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.path = [os.path.join(base_path, "train", file_name) for file_name in metadata["file_name"]]
        self.path = [os.path.join(base_path, "train", file_name) for file_name in metadata["file_name"]]
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(len(self.path), "videos in metadata.")
        print(len(self.path), "videos in metadata.")
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.path = [i + ".tensors.pth" for i in self.path if os.path.exists(i + ".tensors.pth")]
        self.path = [i + ".tensors.pth" for i in self.path if os.path.exists(i + ".tensors.pth")]
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(len(self.path), "tensors cached in metadata.")
        print(len(self.path), "tensors cached in metadata.")
        # 中文说明：检查运行时假设是否成立；代码：assert len(self.path) > 0
        assert len(self.path) > 0
        # 中文说明：根据条件选择执行分支；代码：if debug_without_randomness:
        if debug_without_randomness:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.path = self.path[:1]
            self.path = self.path[:1]
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"debug_without_randomness mode: only {len(self.path)} tensors will be used: {self.path}")
            print(f"debug_without_randomness mode: only {len(self.path)} tensors will be used: {self.path}")

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：self.steps_per_epoch = steps_per_epoch
        self.steps_per_epoch = steps_per_epoch

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __getitem__(self, index):
    def __getitem__(self, index):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_id = torch.randint(0, len(self.path), (1,))[0]
        data_id = torch.randint(0, len(self.path), (1,))[0]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data_id = (data_id + index) % len(self.path) # For fixed seed.
        data_id = (data_id + index) % len(self.path)  # For fixed seed.
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：path = self.path[data_id]
        path = self.path[data_id]
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：data = torch.load(path, weights_only=True, map_location="cpu")
        data = torch.load(path, weights_only=True, map_location="cpu")

        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Batch dimension will be added when collating the data
        # Batch dimension will be added when collating the data
        # 中文说明：根据条件选择执行分支；代码：if "prompt_emb" in data:
        if "prompt_emb" in data:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data["prompt_emb"]["context"] = data["prompt_emb"]["context"][0]
            data["prompt_emb"]["context"] = data["prompt_emb"]["context"][0]
        # 中文说明：根据条件选择执行分支；代码：if "image_emb" in data:
        if "image_emb" in data:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data["image_emb"]["clip_feature"] = data["image_emb"]["clip_feature"][0]
            data["image_emb"]["clip_feature"] = data["image_emb"]["clip_feature"][0]
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：data["image_emb"]["y"] = data["image_emb"]["y"][0]
            data["image_emb"]["y"] = data["image_emb"]["y"][0]

        # 中文说明：从当前函数返回结果或结束函数执行；代码：return data
        return data

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def __len__(self):
    def __len__(self):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.steps_per_epoch
        return self.steps_per_epoch
