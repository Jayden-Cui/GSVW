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
# 中文说明：设置脚本变量或环境变量；代码：EXP=videoworld2_dldm_openx_and_videocraft_infer
EXP=videoworld2_dldm_openx_and_videocraft_infer
# 中文说明：执行当前 Shell 命令，完成本行指定的脚本操作；代码：torchrun --nproc_per_node=1 --master_port=11114 -m scripts.test --config=videoworld2/configs/...
torchrun --nproc_per_node=1 --master_port=11114 -m scripts.test --config=videoworld2/configs/base/config.py --mode=test --input_path=default  -- experiment=${EXP}