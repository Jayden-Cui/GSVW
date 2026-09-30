# 阅读：从训练检查点提取 dLDM 权重；结尾保留了原作者的调试断点。
import torch
import sys

# 需要实验名和迭代名，用于定位训练检查点。
if len(sys.argv) < 3:
    print(f"Usage: python {sys.argv[0]} EXP_NAME iter_name")
    sys.exit(1)

EXP_NAME = sys.argv[1]
iter_name = sys.argv[2]

# 读取序列化权重或动态码；文件须来自可信来源。
pth = torch.load(f"checkpoints/posttraining/video2world/{EXP_NAME}/checkpoints/model/{iter_name}.pt")
new_pth = {}
# 只提取 ldm_net 参数，跳过感知损失网络。
for k, v in pth.items():
    if 'ldm_net' not in k or 'loss' in k:
        continue
    # 去掉训练容器前缀，供 TokenizerModel 直接加载。
    new_pth[k.replace('ldm_net.', '')] = v
# 将权重或结果写入指定路径。
torch.save(new_pth, f"checkpoints/posttraining/video2world/{EXP_NAME}/checkpoints/model/{iter_name}_ldm.pt")
# 原作者留下的调试断点；保存后会暂停，不属于算法步骤。
import pdb;pdb.set_trace()