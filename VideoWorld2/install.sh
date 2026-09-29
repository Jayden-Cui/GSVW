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
# 中文说明：保留原有 Shell 注释，说明脚本用途或运行约束；原文：# cd VideoWorld2
# cd VideoWorld2
# 中文说明：执行当前 Shell 命令，完成本行指定的脚本操作；代码：pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.p...
pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124
# 中文说明：执行当前 Shell 命令，完成本行指定的脚本操作；代码：pip install -r requirements.txt --user
pip install -r requirements.txt --user
# 中文说明：执行当前 Shell 命令，完成本行指定的脚本操作；代码：pip install --no-build-isolation transformer-engine[pytorch]==1.12.0
pip install --no-build-isolation transformer-engine[pytorch]==1.12.0

# 中文说明：执行当前 Shell 命令，完成本行指定的脚本操作；代码：cd ../
cd ../
# 中文说明：执行当前 Shell 命令，完成本行指定的脚本操作；代码：git clone https://github.com/NVIDIA/apex
git clone https://github.com/NVIDIA/apex
# 中文说明：执行当前 Shell 命令，完成本行指定的脚本操作；代码：cd apex
cd apex
# 中文说明：执行当前 Shell 命令，完成本行指定的脚本操作；代码：pip install -v --disable-pip-version-check --no-cache-dir --no-build-isolation --config-setti...
pip install -v --disable-pip-version-check --no-cache-dir --no-build-isolation --config-settings "--build-option=--cpp_ext" --config-settings "--build-option=--cuda_ext" .
# 中文说明：执行当前 Shell 命令，完成本行指定的脚本操作；代码：cd /opt/tiger/PointVIS/VideoWorld2
cd /opt/tiger/PointVIS/VideoWorld2
# 中文说明：执行当前 Shell 命令，完成本行指定的脚本操作；代码：python3 scripts/test_environment.py
python3 scripts/test_environment.py
# 中文说明：执行当前 Shell 命令，完成本行指定的脚本操作；代码：pip install scikit-image
pip install scikit-image
# 中文说明：执行当前 Shell 命令，完成本行指定的脚本操作；代码：pip install fvcore
pip install fvcore
# 中文说明：执行当前 Shell 命令，完成本行指定的脚本操作；代码：pip install qwen_vl_utils
pip install qwen_vl_utils
# 中文说明：执行当前 Shell 命令，完成本行指定的脚本操作；代码：pip install flash-attn==2.6.3 --no-build-isolation
pip install flash-attn==2.6.3 --no-build-isolation
# 中文说明：执行当前 Shell 命令，完成本行指定的脚本操作；代码：pip install albumentations
pip install albumentations
# 中文说明：执行当前 Shell 命令，完成本行指定的脚本操作；代码：pip install kornia
pip install kornia
# 中文说明：执行当前 Shell 命令，完成本行指定的脚本操作；代码：pip install lpips
pip install lpips

# 中文说明：执行当前 Shell 命令，完成本行指定的脚本操作；代码：sudo apt-get install git-lfs
sudo apt-get install git-lfs
# 中文说明：执行当前 Shell 命令，完成本行指定的脚本操作；代码：git lfs install
git lfs install

# 中文说明：执行当前 Shell 命令，完成本行指定的脚本操作；代码：mkdir -p checkpoints
mkdir -p checkpoints
# 中文说明：执行当前 Shell 命令，完成本行指定的脚本操作；代码：mkdir -p datasets/Video-CraftBench
mkdir -p datasets/Video-CraftBench