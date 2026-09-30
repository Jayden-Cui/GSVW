# VideoWorld2 中文代码阅读指南

这份指南只保留理解 VideoWorld2 主流程所需的信息。建议先跑通推理，再阅读训练和工程代码。

## 一、核心主线

官方 Video-CraftBench 演示的调用链是：

```text
scripts/test.sh
  -> scripts/test.py
  -> Predict2Video2WorldModelWithCtrl.inference
  -> dLDM 解码动态码
  -> 控制分支生成逐层残差
  -> 共享 DiT 去噪
  -> scheduler 更新 latent
  -> 连续视频 VAE 解码
```

这里有三种容易混淆的表示：

- **离散动态码**：整数索引，保存在 `Video-Craft-dLDM-codes.pt`。
- **量化向量**：离散码反量化后的连续向量，供 dLDM 解码和 DiT 条件连接器使用。
- **连续视频 latent**：视频 VAE 产生的扩散空间表示，供 DiT 和 scheduler 使用。

## 二、推荐阅读顺序

### 1. 先看官方推理入口

1. `README.md`
   - 只看权重目录、推理命令和训练阶段。
2. `scripts/test.sh`
   - 确认配置名和启动参数。
3. `scripts/test.py`
   - 重点看 `infer`、`load_frame` 和 `model.inference`。
   - `load_video` 是辅助分支，图片演示不会经过它。
4. `videoworld2/models/video2world_model.py`
   - 先看 `Predict2Video2WorldModelWithCtrl.inference`。
   - 再看 `Predict2Video2WorldModel.training_step`，理解训练如何得到动态码。

### 2. 再看 dLDM

5. `videoworld2/latent_dynamics/discrete_video_latent_dynamic.py`
   - 总入口：编码、量化、解码和条件连接器。
   - 注意区分 `quant_info`、`quant_codes` 和重建视频。
6. `videoworld2/latent_dynamics/modules/qformer_ldm.py`
   - `QFormerAdjacentFSingleQ` 用相邻潜帧提取动态变化。
7. `videoworld2/latent_dynamics/modules/quantizers.py`
   - 先看 `FSQuantizer`，再看 `ResidualFSQuantizer`、`VectorQuantizer` 和 `LFQuantizer`。
8. `videoworld2/latent_dynamics/modules/layers3d.py`
   - 需要追踪 3D 编解码器的层级结构时再展开。
9. `videoworld2/latent_dynamics/modules/patching.py`
   - 需要理解时空分块和维度变换时阅读。

### 3. 看控制分支和 DiT

10. `videoworld2/pipelines/video2world_ctrl.py`
    - 控制管线先运行 `dit_ctrl`，再把残差传给共享 DiT。
11. `videoworld2/models/ctrl_video2world_dit.py`
    - `CtrlEncoder` 将灰度重建提示转换为逐层控制残差。
12. `videoworld2/models/video2world_dit.py`
    - VideoWorld2 的薄封装，负责条件帧掩码等输入适配。
13. `videoworld2/models/text2image_dit.py`
    - 名字虽然是 `text2image`，但其中的 `MiniTrainDIT`、`Block` 和 `Attention` 是共享 DiT 主干，不能直接跳过。

### 4. 补齐采样和条件

14. `videoworld2/pipelines/video2world.py`
    - 视频编码、条件构造、引导去噪和最终解码。
15. `videoworld2/tokenizers/tokenizer.py`
    - 连续视频 VAE；不要和 dLDM tokenizer 混淆。
16. `videoworld2/conditioner.py`
    - 统一封装动态嵌入、条件帧和控制提示。
17. `videoworld2/module/denoiser_scaling.py`
    - 噪声级别对应的网络输入输出预条件。
18. `videoworld2/module/denoise_prediction.py`
    - 保存 `x0` 和 `eps` 等去噪结果。
19. `videoworld2/schedulers/rectified_flow_scheduler.py`
    - 首步使用 Euler，后续结合上一轮预测进行更新。

### 5. 最后看训练

20. `videoworld2/configs/base/experiment/openx.py`
    - 先确认预热、联合训练和推理配置的开关。
21. `scripts/train_dldm_warmup.sh`
    - 阶段一：只训练 dLDM 重建。
22. `scripts/extract_ldm_pth.py`
    - 从预热检查点提取 dLDM 权重。
23. `scripts/add_ctrl_branch.py`
    - 为基础 DiT 补齐控制分支参数。
24. `scripts/train_dldm.sh`
    - 阶段二：联合训练 DiT、控制分支和 dLDM。
25. `scripts/inference_dldm_codes.sh`
    - 用完整视频顺序提取动态码。
26. `scripts/train.py`、`imaginaire/trainer.py`
    - 最后再看通用配置、训练循环、分布式和检查点逻辑。

## 三、脚本目录

| 脚本 | 作用 | 阅读优先级 |
| --- | --- | --- |
| `scripts/test.sh` | 官方演示启动器 | 必看 |
| `scripts/test.py` | 官方 dLDM 推理入口 | 必看 |
| `scripts/train_dldm_warmup.sh` | dLDM 预热训练 | 训练时看 |
| `scripts/extract_ldm_pth.py` | 提取 dLDM 检查点 | 训练时看 |
| `scripts/add_ctrl_branch.py` | 创建控制分支初始权重 | 训练时看 |
| `scripts/train_dldm.sh` | 联合训练 | 训练时看 |
| `scripts/inference_dldm_codes.sh` | 批量提取动态码 | 训练后看 |
| `scripts/test_infer.py` | 通用管线测试示例 | 按需 |
| `scripts/test_environment.py` | CUDA、依赖和权重诊断 | 出错时看 |
| `scripts/infer.sh` | 旧动作生成示例，引用的入口已不在当前目录 | 可跳过 |
| `install.sh` | 环境安装，含原作者机器路径 | 运行环境异常时看 |

## 四、哪些代码第一遍可以跳过

以下代码不是算法主线的前置知识：

- `imaginaire/utils/`、`imaginaire/lazy_config/`
  - 分布式、检查点、I/O、配置实例化等通用基础设施。
- `videoworld2/utils/`
  - FSDP、DTensor、优化器和并行训练辅助。
- `videoworld2/callbacks/`
  - 日志、梯度裁剪、设备监控和训练回调。
- `videoworld2/auxiliary/guardrail/`
  - 内容安全、人脸模糊和过滤逻辑。
- `videoworld2/utils/flash_attn_3/`
  - FlashAttention 性能适配。
- `videoworld2/vram_management/`
  - 显存卸载和部署包装。
- `action_video2world*`、`video2world_gr00t.py`
  - 动作条件或机器人扩展，不影响基础 dLDM 演示。
- `examples/text2image.py`、`pipelines/text2image.py`
  - 文本生图分支；但 `models/text2image_dit.py` 的共享 DiT 主干仍需阅读。

这些文件不是无用代码，而是“当前阅读目标不需要先理解”的代码。运行项目时仍可能被间接调用。

## 五、注释约定

源码注释只保留四类信息：

1. 文件在主流程中的位置。
2. 关键函数的输入、输出和张量形状。
3. 离散码、量化向量和连续 latent 的边界。
4. 会改变训练或推理行为的分支、梯度和状态。

普通导入、简单赋值、括号闭合和显而易见的语法不再逐行重复解释。此次修改只调整注释和阅读文档，没有改变 Python AST、可执行 token 或 Shell 命令。
