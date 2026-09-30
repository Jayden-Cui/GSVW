# Copyright (c) 2025 ByteDance Ltd. and/or its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# cd VideoWorld2
# 阅读：环境安装脚本；包含原作者绝对路径，执行前须核对。
pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt --user
# 编译 Transformer Engine 组件，需匹配本机 CUDA 工具链。
pip install --no-build-isolation transformer-engine[pytorch]==1.12.0

cd ../
# 在项目上级目录获取 Apex；这里会创建独立源码目录。
git clone https://github.com/NVIDIA/apex
cd apex
pip install -v --disable-pip-version-check --no-cache-dir --no-build-isolation --config-settings "--build-option=--cpp_ext" --config-settings "--build-option=--cuda_ext" .
# 原作者机器上的项目路径；不是当前仓库位置。
cd /opt/tiger/PointVIS/VideoWorld2
python3 scripts/test_environment.py
pip install scikit-image
pip install fvcore
pip install qwen_vl_utils
pip install flash-attn==2.6.3 --no-build-isolation
pip install albumentations
pip install kornia
pip install lpips

sudo apt-get install git-lfs
git lfs install

mkdir -p checkpoints
mkdir -p datasets/Video-CraftBench