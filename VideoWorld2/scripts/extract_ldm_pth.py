# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import sys
import sys

# 中文说明：根据条件选择执行分支；代码：if len(sys.argv) < 3:
if len(sys.argv) < 3:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：print(f"Usage: python {sys.argv[0]} EXP_NAME iter_name")
    print(f"Usage: python {sys.argv[0]} EXP_NAME iter_name")
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sys.exit(1)
    sys.exit(1)

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：EXP_NAME = sys.argv[1]
EXP_NAME = sys.argv[1]
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iter_name = sys.argv[2]
iter_name = sys.argv[2]

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pth = torch.load(f"checkpoints/posttraining/video2world/{EXP_NAME}/checkpoints/model/{iter_na...
pth = torch.load(f"checkpoints/posttraining/video2world/{EXP_NAME}/checkpoints/model/{iter_name}.pt")
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：new_pth = {}
new_pth = {}
# 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for k, v in pth.items():
for k, v in pth.items():
    # 中文说明：根据条件选择执行分支；代码：if 'ldm_net' not in k or 'loss' in k:
    if 'ldm_net' not in k or 'loss' in k:
        # 中文说明：执行循环控制或空操作；代码：continue
        continue
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：new_pth[k.replace('ldm_net.', '')] = v
    new_pth[k.replace('ldm_net.', '')] = v
# 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.save(new_pth, f"checkpoints/posttraining/video2world/{EXP_NAME}/checkpoints/model/{iter...
torch.save(new_pth, f"checkpoints/posttraining/video2world/{EXP_NAME}/checkpoints/model/{iter_name}_ldm.pt")
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import pdb;pdb.set_trace()
import pdb;pdb.set_trace()