# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import torch
import torch
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import math
import math
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pth = torch.load("checkpoints/Cosmos-Predict2-2B-Video2World/model-480p-16fps.pt", weights_on...
pth = torch.load("checkpoints/Cosmos-Predict2-2B-Video2World/model-480p-16fps.pt", weights_only=False)
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：new_names = [('x_embedder2.proj.1.weight', torch.Size([2048, 516])), ('input_hint_block.0.wei...
new_names = [('x_embedder2.proj.1.weight', torch.Size([2048, 516])), ('input_hint_block.0.weight', torch.Size([16, 2048])), ('input_hint_block.0.bias', torch.Size([16])), ('input_hint_block.2.weight', torch.Size([16, 16])), ('input_hint_block.2.bias', torch.Size([16])), ('input_hint_block.4.weight', torch.Size([32, 16])), ('input_hint_block.4.bias', torch.Size([32])), ('input_hint_block.6.weight', torch.Size([32, 32])), ('input_hint_block.6.bias', torch.Size([32])), ('input_hint_block.8.weight', torch.Size([96, 32])), ('input_hint_block.8.bias', torch.Size([96])), ('input_hint_block.10.weight', torch.Size([96, 96])), ('input_hint_block.10.bias', torch.Size([96])), ('input_hint_block.12.weight', torch.Size([256, 96])), ('input_hint_block.12.bias', torch.Size([256])), ('input_hint_block.14.weight', torch.Size([2048, 256])), ('input_hint_block.14.bias', torch.Size([2048])), ('zero_blocks.block0.weight', torch.Size([2048, 2048])), ('zero_blocks.block0.bias', torch.Size([2048])), ('zero_blocks.block1.weight', torch.Size([2048, 2048])), ('zero_blocks.block1.bias', torch.Size([2048])), ('zero_blocks.block2.weight', torch.Size([2048, 2048])), ('zero_blocks.block2.bias', torch.Size([2048]))]
# 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for name, shape in new_names:
for name, shape in new_names:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：_name = 'net.' + name
    _name = 'net.' + name
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# if "x_embedder" in _name:
    # if "x_embedder" in _name:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# pth[_name] = pth['net.x_embedder.proj.1.weight']
    #     pth[_name] = pth['net.x_embedder.proj.1.weight']
    # 中文说明：根据条件选择执行分支；代码：if "zero_blocks" in _name:
    if "zero_blocks" in _name:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pth[_name] = torch.zeros(shape, dtype=pth['net.x_embedder.proj.1.weight'].dtype)
        pth[_name] = torch.zeros(shape, dtype=pth['net.x_embedder.proj.1.weight'].dtype)
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace()
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：weight = torch.randn(shape, dtype=pth['net.x_embedder.proj.1.weight'].dtype)
        weight = torch.randn(shape, dtype=pth['net.x_embedder.proj.1.weight'].dtype)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：std = 1.0 / math.sqrt(shape[-1])
        std = 1.0 / math.sqrt(shape[-1])
        # 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.nn.init.trunc_normal_(weight, std=std, a=-3 * std, b=3 * std)
        torch.nn.init.trunc_normal_(weight, std=std, a=-3 * std, b=3 * std)
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pth[_name] = weight
        pth[_name] = weight
# 中文说明：执行当前对象、库函数或返回值相关操作；代码：torch.save(pth, "checkpoints/Cosmos-Predict2-2B-Video2World/model-480p-16fps-ctrl.pt")
torch.save(pth, "checkpoints/Cosmos-Predict2-2B-Video2World/model-480p-16fps-ctrl.pt")
