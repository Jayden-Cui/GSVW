# 阅读：给预训练 DiT 补控制分支参数；第二阶段训练的准备工具。
import torch
import math
# 加载原始 Cosmos DiT；输出到新路径，不覆盖源权重。
pth = torch.load("checkpoints/Cosmos-Predict2-2B-Video2World/model-480p-16fps.pt", weights_only=False)
# 列出新增提示嵌入、MLP 和前三个零投影层的权重形状。
new_names = [('x_embedder2.proj.1.weight', torch.Size([2048, 516])), ('input_hint_block.0.weight', torch.Size([16, 2048])), ('input_hint_block.0.bias', torch.Size([16])), ('input_hint_block.2.weight', torch.Size([16, 16])), ('input_hint_block.2.bias', torch.Size([16])), ('input_hint_block.4.weight', torch.Size([32, 16])), ('input_hint_block.4.bias', torch.Size([32])), ('input_hint_block.6.weight', torch.Size([32, 32])), ('input_hint_block.6.bias', torch.Size([32])), ('input_hint_block.8.weight', torch.Size([96, 32])), ('input_hint_block.8.bias', torch.Size([96])), ('input_hint_block.10.weight', torch.Size([96, 96])), ('input_hint_block.10.bias', torch.Size([96])), ('input_hint_block.12.weight', torch.Size([256, 96])), ('input_hint_block.12.bias', torch.Size([256])), ('input_hint_block.14.weight', torch.Size([2048, 256])), ('input_hint_block.14.bias', torch.Size([2048])), ('zero_blocks.block0.weight', torch.Size([2048, 2048])), ('zero_blocks.block0.bias', torch.Size([2048])), ('zero_blocks.block1.weight', torch.Size([2048, 2048])), ('zero_blocks.block1.bias', torch.Size([2048])), ('zero_blocks.block2.weight', torch.Size([2048, 2048])), ('zero_blocks.block2.bias', torch.Size([2048]))]
# 补齐新增参数；原 DiT 权重保持不变。
for name, shape in new_names:
    _name = 'net.' + name
    # if "x_embedder" in _name:
    #     pth[_name] = pth['net.x_embedder.proj.1.weight']
    # 残差出口置零，初始化时控制分支不扰动基础 DiT。
    if "zero_blocks" in _name:
        pth[_name] = torch.zeros(shape, dtype=pth['net.x_embedder.proj.1.weight'].dtype)
    else:
        # import pdb;pdb.set_trace()
        weight = torch.randn(shape, dtype=pth['net.x_embedder.proj.1.weight'].dtype)
        # 其余新增层使用按输入维度缩放的截断正态初始化。
        std = 1.0 / math.sqrt(shape[-1])
        torch.nn.init.trunc_normal_(weight, std=std, a=-3 * std, b=3 * std)
        pth[_name] = weight
torch.save(pth, "checkpoints/Cosmos-Predict2-2B-Video2World/model-480p-16fps-ctrl.pt")  # 将权重或结果写入指定路径。
