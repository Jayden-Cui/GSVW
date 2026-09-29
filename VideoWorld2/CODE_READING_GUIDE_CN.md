# VideoWorld2 中文代码阅读指南

这份目录用于帮助你理解 VideoWorld2 的主流程。仓库中有一部分代码是通用训练框架、性能优化或安全过滤器，不需要在第一次阅读时全部展开。

## 一、推荐观看顺序

按下面顺序阅读，可以先建立“输入如何变成视频”的主线，再回头补训练和工程细节。

1. `README.md`
   - 先了解项目目标、环境、模型权重和运行命令。

2. `examples/video2world.py`
   - 最适合的主入口，展示文本/视频条件如何传给推理管线。

3. `videoworld2/pipelines/video2world.py`
   - 读取输入、准备条件、执行采样循环，并调用模型生成视频的总调度器。

4. `videoworld2/models/video2world_model.py`
   - 负责组织视频生成模型、文本条件、视频编码器和去噪过程。

5. `videoworld2/models/video2world_dit.py`
   - VideoWorld2 的 DiT 主干，重点看时空 token、条件注入和 Transformer block。

6. `videoworld2/module/attention.py`
   - 查看注意力模块如何处理视频的空间与时间维度。

7. `videoworld2/module/denoiser_scaling.py`、`videoworld2/module/denoise_prediction.py`
   - 理解扩散/流匹配采样中的缩放和预测参数化。

8. `videoworld2/schedulers/rectified_flow_scheduler.py`
   - 理解每一步采样如何更新 latent。

9. `videoworld2/latent_dynamics/discrete_video_latent_dynamic.py`
   - 了解视频 latent 的离散动态建模，以及编码后的时空表示。

10. `videoworld2/latent_dynamics/cosmos_tokenizer.py`
    - 了解视频如何在像素空间和 latent 空间之间转换。

11. `videoworld2/latent_dynamics/modules/patching.py`、`layers3d.py`
    - 需要深入模型结构时再看 patch 切分、3D 层和 Q-Former。

12. `videoworld2/tokenizers/tokenizer.py`、`videoworld2/conditioner.py`
    - 了解文本 tokenizer、文本编码器和条件特征的封装。

13. `videoworld2/data/` 和 `videoworld2/datasets/`
    - 需要研究训练数据、视频解码、WebDataset 或 action 条件时阅读。

14. `scripts/train.py`、`imaginaire/trainer.py`、`imaginaire/model.py`
    - 最后再看训练启动、训练循环和通用训练框架。

## 二、代码重要性分层

### A. 第一次必须阅读：核心生成链

这些文件决定 VideoWorld2 的主要算法行为：

- `examples/video2world.py`
- `examples/text2world.py`
- `videoworld2/pipelines/video2world.py`
- `videoworld2/models/video2world_model.py`
- `videoworld2/models/video2world_dit.py`
- `videoworld2/module/attention.py`
- `videoworld2/module/denoise_prediction.py`
- `videoworld2/module/denoiser_scaling.py`
- `videoworld2/schedulers/rectified_flow_scheduler.py`
- `videoworld2/latent_dynamics/`
- `videoworld2/tokenizers/`
- `videoworld2/conditioner.py`

### B. 按需求阅读：扩展能力

以下代码并非所有用户都需要：

- `pipelines/action_video2world.py`、`models/action_video2world_*.py`：需要动作条件生成时阅读。
- `pipelines/video2world_ctrl.py`、`models/ctrl_video2world_dit.py`：需要控制分支或额外控制信号时阅读。
- `examples/video2world_gr00t.py`：需要 GR00T 动作/机器人流程时阅读。
- `examples/video2world_lvg.py`：需要 LVG 流程时阅读。
- `examples/video2world_bestofn.py`：需要 Best-of-N 采样和筛选时阅读。
- `examples/text2image.py`、`pipelines/text2image.py`、`models/text2image_dit.py`：只研究文本生图分支时阅读。
- `videoworld2/auxiliary/guardrail/`：研究安全审核、人脸模糊或内容过滤时阅读；普通推理可以先跳过。

### C. 研究训练数据时阅读

- `videoworld2/data/dataset_video.py`
- `videoworld2/data/dataset_openx_pickle.py`
- `videoworld2/data/action_conditioned/`
- `videoworld2/datasets/dataset_provider.py`
- `videoworld2/datasets/decoders/video_decoder.py`
- `videoworld2/datasets/augmentors/`
- `videoworld2/datasets/webdataset.py`
- `videoworld2/datasets/joint_dataloader.py`

### D. 第一遍可以跳过：通用工程与性能代码

这些文件主要负责让大规模训练更快、更稳定或更容易部署，不是理解算法主线的前置知识：

- `imaginaire/utils/`：日志、分布式、检查点、通信、I/O 和通用工具。
- `imaginaire/lazy_config/`：配置懒加载和对象实例化框架。
- `imaginaire/datasets/webdataset/`：通用 WebDataset 基础设施。
- `videoworld2/utils/`：FSDP、DTensor、优化器和并行训练辅助代码。
- `videoworld2/utils/flash_attn_3/`：FlashAttention 适配，属于性能优化。
- `videoworld2/callbacks/`：训练日志、梯度裁剪、设备监控等回调。
- `videoworld2/checkpointer.py`：模型检查点保存和恢复。
- `videoworld2/networks/model_weights_stats.py`：权重统计工具。
- `videoworld2/networks/selective_activation_checkpoint.py`：显存优化工具。
- `scripts/test*.py`、`scripts/test*.sh`：环境和回归检查，不是生成算法本身。

### E. 不需要当作源代码阅读

- `__pycache__/` 下的 `.pyc`：Python 编译缓存，不能直接阅读，也不应手工加注释。
- `assets/` 下的图片：示例输入、论文图和展示素材。
- `LICENSE`、`ATTRIBUTIONS.md`、`CONTRIBUTING.md`：许可、第三方声明和贡献规范。
- `requirements.txt`、`install.sh`：依赖和安装配置，运行环境有问题时再查。

## 三、用一句话理解主流程

示例入口读取条件，`pipeline` 负责调度采样，`model` 组织 VideoWorld2，DiT 在 latent token 上预测去噪方向，scheduler 更新 latent，tokenizer 将 latent 解码回视频；训练部分再通过 `data/datasets` 提供样本，通过 `imaginaire` 的通用训练器优化模型。

## 四、建议的实际阅读方法

先只阅读 A 类文件，并沿着函数调用跳转；遇到数据结构不清楚时补看 `tokenizers` 和 `latent_dynamics`。只有当你要训练、改数据、做动作控制或优化显存时，再分别进入 B、C、D 类目录。这样可以避免把大量框架代码误认为 VideoWorld2 的核心算法。
