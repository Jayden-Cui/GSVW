# 中文说明：保留原有 Shell 注释，说明脚本用途或运行约束；原文：# Copyright (c) 2025 ByteDance Ltd. and/or its affiliates
# Copyright (c) 2025 ByteDance Ltd. and/or its affiliates
# 中文说明：保留原有 Shell 注释，说明脚本用途或运行约束；原文：#
#
# 中文说明：保留原有 Shell 注释，说明脚本用途或运行约束；原文：# Licensed under the Apache License, Version 2.0 (the "License");
# Licensed under the Apache License, Version 2.0 (the "License");
# 中文说明：保留原有 Shell 注释，说明脚本用途或运行约束；原文：# you may not use this file except in compliance with the License.
# you may not use this file except in compliance with the License.
# 中文说明：保留原有 Shell 注释，说明脚本用途或运行约束；原文：# You may obtain a copy of the License at
# You may obtain a copy of the License at
# 中文说明：保留原有 Shell 注释，说明脚本用途或运行约束；原文：#
#
# 中文说明：保留原有 Shell 注释，说明脚本用途或运行约束；原文：# http:#www.apache.org/licenses/LICENSE-2.0
#     http:#www.apache.org/licenses/LICENSE-2.0
# 中文说明：保留原有 Shell 注释，说明脚本用途或运行约束；原文：#
#
# 中文说明：保留原有 Shell 注释，说明脚本用途或运行约束；原文：# Unless required by applicable law or agreed to in writing, software
# Unless required by applicable law or agreed to in writing, software
# 中文说明：保留原有 Shell 注释，说明脚本用途或运行约束；原文：# distributed under the License is distributed on an "AS IS" BASIS,
# distributed under the License is distributed on an "AS IS" BASIS,
# 中文说明：保留原有 Shell 注释，说明脚本用途或运行约束；原文：# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# 中文说明：保留原有 Shell 注释，说明脚本用途或运行约束；原文：# See the License for the specific language governing permissions and
# See the License for the specific language governing permissions and
# 中文说明：保留原有 Shell 注释，说明脚本用途或运行约束；原文：# limitations under the License.
# limitations under the License.
# 中文说明：执行当前 Shell 命令，完成本行指定的脚本操作；代码：python3 examples/video2world_action.py \
python3 examples/video2world_action.py \
  --model_size 2B \
  --dit_path "checkpoints/Cosmos-Predict2-2B-Sample-Action-Conditioned/model-480p-4fps.pt" \
  --input_video datasets/bridge/videos/test/13/rgb.mp4 \
  --input_annotation datasets/bridge/annotation/test/13.json \
  --num_conditional_frames 1 \
  --save_path output/action_video.mp4 \
  --guidance 0 \
  --seed 0 \
  --disable_guardrail \
  --disable_prompt_refiner  # 中文说明：执行当前 Shell 命令，完成本行指定的脚本操作；代码：--disable_prompt_refiner