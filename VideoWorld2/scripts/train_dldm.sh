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
# 阅读：阶段二：补齐控制权重，再启动 8 进程联合训练。
EXP=videoworld2_dldm_openx_and_videocraft
# 生成 -ctrl.pt 权重；检查点路径由脚本写死，需核对与配置一致。
python3 scripts/add_ctrl_branch.py
torchrun --nproc_per_node=8 --master_port=52224 -m scripts.train --config=videoworld2/configs/base/config.py -- experiment=${EXP}
