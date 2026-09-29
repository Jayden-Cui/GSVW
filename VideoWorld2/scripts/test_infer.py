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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.io import save_image_or_video
from imaginaire.utils.io import save_image_or_video
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.configs.base.config_video2world import PREDICT2_VIDEO2WORLD_PIPELINE_2B, PRE...
from videoworld2.configs.base.config_video2world import PREDICT2_VIDEO2WORLD_PIPELINE_2B, PREDICT2_VIDEO2WORLD_PIPELINE_2B_480P_16FPS
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.pipelines.video2world import Video2WorldPipeline
from videoworld2.pipelines.video2world import Video2WorldPipeline

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Create the video generation pipeline.
# Create the video generation pipeline.
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe = Video2WorldPipeline.from_config(
pipe = Video2WorldPipeline.from_config(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config=PREDICT2_VIDEO2WORLD_PIPELINE_2B_480P_16FPS,
    config=PREDICT2_VIDEO2WORLD_PIPELINE_2B_480P_16FPS,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path="checkpoints/Cosmos-Predict2-2B-Video2World/model-480p-16fps.pt",
    dit_path="checkpoints/Cosmos-Predict2-2B-Video2World/model-480p-16fps.pt",
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：text_encoder_path="checkpoints/t5-11b",
    text_encoder_path="checkpoints/t5-11b",
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Specify the input image path and text prompt.
# Specify the input image path and text prompt.
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：image_path = "/opt/tiger/PointVIS/VideoWorld_Cosmos_Predict/assets/video2world/input3.mp4"
image_path = "/opt/tiger/PointVIS/VideoWorld_Cosmos_Predict/assets/video2world/input3.mp4"
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# prompt = "A high-definition video captures the precision of robotic welding in an industria...
# prompt = "A high-definition video captures the precision of robotic welding in an industrial setting. The first frame showcases a robotic arm, equipped with a welding torch, positioned over a large metal structure. The welding process is in full swing, with bright sparks and intense light illuminating the scene, creating a vivid display of blue and white hues. A significant amount of smoke billows around the welding area, partially obscuring the view but emphasizing the heat and activity. The background reveals parts of the workshop environment, including a ventilation system and various pieces of machinery, indicating a busy and functional industrial workspace. As the video progresses, the robotic arm maintains its steady position, continuing the welding process and moving to its left. The welding torch consistently emits sparks and light, and the smoke continues to rise, diffusing slightly as it moves upward. The metal surface beneath the torch shows ongoing signs of heating and melting. The scene retains its industrial ambiance, with the welding sparks and smoke dominating the visual field, underscoring the ongoing nature of the welding operation."
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# prompt = "A high-definition video captures the scene of handicraft production. The first fr...
# prompt = "A high-definition video captures the scene of handicraft production. The first frame shows a pair of hands on a piece of paper, about to pinch the lower left and right corners of the paper and fold the paper in half along the horizontal axis. After the fold is completed, the width of the paper becomes half of the original. Then the two hands press the crease."
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：prompt = "A driving scene, move foward."
prompt = "A driving scene, move foward."
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Run the video generation pipeline.
# Run the video generation pipeline.
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video = pipe(input_path=image_path, prompt=prompt)
video = pipe(input_path=image_path, prompt=prompt)

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Save the resulting output video.
# Save the resulting output video.
# 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：save_image_or_video(video, "output/drive_start0.mp4", fps=16)
save_image_or_video(video, "output/drive_start0.mp4", fps=16)