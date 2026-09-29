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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import sys
import sys
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import random
import random
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from tqdm import tqdm
from tqdm import tqdm

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from dataset_openx_pickle import EnhancedOpenXPickleDataset, save_video_as_gif
from dataset_openx_pickle import EnhancedOpenXPickleDataset, save_video_as_gif

# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def generate_subfolder_gifs():
def generate_subfolder_gifs():

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：base_save_dir = 'datasets/openx_out'
    base_save_dir = 'datasets/openx_out'
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.makedirs(base_save_dir, exist_ok=True)
    os.makedirs(base_save_dir, exist_ok=True)
    
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset = EnhancedOpenXPickleDataset(
    dataset = EnhancedOpenXPickleDataset(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_size=[256, 256],
        video_size=[256, 256],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：aspect_ratio_prob=0.5,
        aspect_ratio_prob=0.5,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_frames=93,
        num_frames=93,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_frame_based_sampling=False,
        use_frame_based_sampling=False,  
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_cache=True,
        use_cache=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_path="datasets/openx_videocraft_cache.json",
        cache_path="datasets/openx_videocraft_cache.json",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：subfolders=['bridge']
        subfolders=['bridge']
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )
    
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"Dataset size: {len(dataset)}")
    print(f"Dataset size: {len(dataset)}")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"Subfolders found: {list(dataset.pickle_paths_by_folder.keys())}")
    print(f"Subfolders found: {list(dataset.pickle_paths_by_folder.keys())}")
    

    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for subfolder, file_paths in dataset.pickle_paths_by_folder.items():
    for subfolder, file_paths in dataset.pickle_paths_by_folder.items():
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"Processing subfolder: {subfolder}")
        print(f"Processing subfolder: {subfolder}")
        

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：subfolder_save_dir = os.path.join(base_save_dir, subfolder)
        subfolder_save_dir = os.path.join(base_save_dir, subfolder)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：os.makedirs(subfolder_save_dir, exist_ok=True)
        os.makedirs(subfolder_save_dir, exist_ok=True)
        

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_files_to_sample = min(50, len(file_paths))
        num_files_to_sample = min(50, len(file_paths))
        # 中文说明：根据条件选择执行分支；代码：if num_files_to_sample == 0:
        if num_files_to_sample == 0:
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"No files found in subfolder {subfolder}, skipping...")
            print(f"No files found in subfolder {subfolder}, skipping...")
            # 中文说明：执行循环控制或空操作；代码：continue
            continue
        

        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sampled_files = random.sample(file_paths, num_files_to_sample)
        sampled_files = random.sample(file_paths, num_files_to_sample)
 
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for i, file_path in enumerate(tqdm(sampled_files, desc=f"Generating GIFs for {subfolder}")):
        for i, file_path in enumerate(tqdm(sampled_files, desc=f"Generating GIFs for {subfolder}")):
            # 中文说明：开始一个可捕获异常的代码块；代码：try:
            try:
      
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：file_index = dataset.pickle_paths.index(file_path)
                file_index = dataset.pickle_paths.index(file_path)
                
          
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sample = dataset[file_index]
                sample = dataset[file_index]
                
       
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：file_name = os.path.basename(file_path).split('.')[0]
                file_name = os.path.basename(file_path).split('.')[0]
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：save_path = os.path.join(subfolder_save_dir, f"{file_name}_gif_{i}.gif")
                save_path = os.path.join(subfolder_save_dir, f"{file_name}_gif_{i}.gif")
                
       
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：save_video_as_gif(sample['video'], save_path, fps=16)
                save_video_as_gif(sample['video'], save_path, fps=16)
                
            # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
            except Exception as e:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"Error processing file {file_path}: {str(e)}")
                print(f"Error processing file {file_path}: {str(e)}")
                # 中文说明：执行循环控制或空操作；代码：continue
                continue
    
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"All GIFs have been generated and saved to {base_save_dir}")
    print(f"All GIFs have been generated and saved to {base_save_dir}")


# 中文说明：根据条件选择执行分支；代码：if __name__ == "__main__":
if __name__ == "__main__":
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：generate_subfolder_gifs()
    generate_subfolder_gifs()