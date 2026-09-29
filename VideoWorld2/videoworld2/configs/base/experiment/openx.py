# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Copyright (c) 2025 ByteDance Ltd. and/or its affiliates
# Copyright (c) 2025 ByteDance Ltd. and/or its affiliates
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：#
#
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Licensed under the Apache License, Version 2.0 (the "License");
# Licensed under the Apache License, Version 2.0 (the "License");
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# you may not use this file except in compliance with the License.
# you may not use this file except in compliance with the License.
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# You may obtain a copy of the License at
# You may obtain a copy of the License at
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：#
#
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# http:#www.apache.org/licenses/LICENSE-2.0
#     http:#www.apache.org/licenses/LICENSE-2.0
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：#
#
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Unless required by applicable law or agreed to in writing, software
# Unless required by applicable law or agreed to in writing, software
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# distributed under the License is distributed on an "AS IS" BASIS,
# distributed under the License is distributed on an "AS IS" BASIS,
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# See the License for the specific language governing permissions and
# See the License for the specific language governing permissions and
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# limitations under the License.
# limitations under the License.
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from hydra.core.config_store import ConfigStore
from hydra.core.config_store import ConfigStore
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from megatron.core import parallel_state
from megatron.core import parallel_state
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.utils.data import DataLoader, DistributedSampler
from torch.utils.data import DataLoader, DistributedSampler
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.latent_dynamics.modules import DiscreteQuantizer, Encoder3DType, Decoder3DType
from videoworld2.latent_dynamics.modules import DiscreteQuantizer, Encoder3DType, Decoder3DType
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.data.dataset_video import Dataset, InferDataset
from videoworld2.data.dataset_video import Dataset, InferDataset
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.lazy_config import LazyCall as L
from imaginaire.lazy_config import LazyCall as L
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.data.dataset_openx_pickle import EnhancedOpenXPickleDataset
from videoworld2.data.dataset_openx_pickle import  EnhancedOpenXPickleDataset
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# from videoworld2.data.dataset_openx_pickle_latent_gen import EnhancedOpenXPickleLatentGenDa...
# from videoworld2.data.dataset_openx_pickle_latent_gen import EnhancedOpenXPickleLatentGenDataset
# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# from videoworld2.data.dataset_calvin import CALVINDataset
# from videoworld2.data.dataset_calvin import CALVINDataset

# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_sampler(dataset, shuffle=True) -> DistributedSampler:
def get_sampler(dataset, shuffle=True) -> DistributedSampler:
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return DistributedSampler(
    return DistributedSampler(
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dataset,
        dataset,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_replicas=parallel_state.get_data_parallel_world_size(),
        num_replicas=parallel_state.get_data_parallel_world_size(),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：rank=parallel_state.get_data_parallel_rank(),
        rank=parallel_state.get_data_parallel_rank(),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：shuffle=shuffle,
        shuffle=shuffle,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：seed=0,
        seed=0,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )


# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cs = ConfigStore.instance()
cs = ConfigStore.instance()


# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# training with only videocraft
# training with only videocraft 
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：example_video_dataset_videocraft = L(Dataset)(
example_video_dataset_videocraft = L(Dataset)(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset_dir="datasets/Video-CraftBench/Paper_and_Block_clips",
    dataset_dir="datasets/Video-CraftBench/Paper_and_Block_clips",
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_frames=93,
    num_frames=93,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_size=(480, 832),
    video_size=(480, 832),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：example_video_dataset_videocraft_val = L(InferDataset)(
example_video_dataset_videocraft_val = L(InferDataset)(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset_dir="datasets/Video-CraftBench/Paper_and_Block_clips",
    dataset_dir="datasets/Video-CraftBench/Paper_and_Block_clips",
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_frames=93,
    num_frames=93,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_size=(480, 832),
    video_size=(480, 832),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# training with only videocraft and openx
# training with only videocraft and openx
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：example_video_dataset_openx_videocraft = L(EnhancedOpenXPickleDataset)(
example_video_dataset_openx_videocraft = L(EnhancedOpenXPickleDataset)(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset_dir="datasets/openx_untar",
    dataset_dir="datasets/openx_untar",
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_frames=93,
    num_frames=93,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_size=(480, 832),
    video_size=(480, 832),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：subfolders=None,
    subfolders=None,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_cache=True,
    use_cache=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cache_path="datasets/openx_videocraft_cache.json",
    cache_path="datasets/openx_videocraft_cache.json",
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：meta_path="datasets/openx_videocraft_meta.json",
    meta_path="datasets/openx_videocraft_meta.json",
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：fps_variation=False
    fps_variation=False
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)



# 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# dataloader: openx train
# dataloader: openx train
# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataloader_train_videocraft = L(DataLoader)(
dataloader_train_videocraft = L(DataLoader)(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset=example_video_dataset_videocraft,
    dataset=example_video_dataset_videocraft,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sampler=L(get_sampler)(dataset=example_video_dataset_videocraft),
    sampler=L(get_sampler)(dataset=example_video_dataset_videocraft),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch_size=1,
    batch_size=1,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：drop_last=True,
    drop_last=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_workers=8,
    num_workers=8,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pin_memory=True,
    pin_memory=True,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataloader_val_videocraft = L(DataLoader)(
dataloader_val_videocraft = L(DataLoader)(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset=example_video_dataset_videocraft_val,
    dataset=example_video_dataset_videocraft_val,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sampler=L(get_sampler)(dataset=example_video_dataset_videocraft_val),
    sampler=L(get_sampler)(dataset=example_video_dataset_videocraft_val),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch_size=1,
    batch_size=1,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：drop_last=True,
    drop_last=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_workers=8,
    num_workers=8,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pin_memory=True,
    pin_memory=True,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataloader_train_openx_videocraft = L(DataLoader)(
dataloader_train_openx_videocraft = L(DataLoader)(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset=example_video_dataset_openx_videocraft,
    dataset=example_video_dataset_openx_videocraft,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sampler=L(get_sampler)(dataset=example_video_dataset_openx_videocraft),
    sampler=L(get_sampler)(dataset=example_video_dataset_openx_videocraft),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：batch_size=1,
    batch_size=1,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：drop_last=True,
    drop_last=True,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_workers=8,
    num_workers=8,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pin_memory=True,
    pin_memory=True,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)


# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：videoworld2_dldm_openx_and_videocraft_wodit_warmup = dict(
videoworld2_dldm_openx_and_videocraft_wodit_warmup = dict(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：defaults=[
    defaults=[
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"override /model": "predict2_video2world_ldm_fsdp_2b_480p_16fps"},
        {"override /model": "predict2_video2world_ldm_fsdp_2b_480p_16fps"},
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"override /optimizer": "fusedadamw"},
        {"override /optimizer": "fusedadamw"},
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"override /scheduler": "lambdalinear"},
        {"override /scheduler": "lambdalinear"},
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"override /ckpt_type": "standard"},
        {"override /ckpt_type": "standard"},
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："_self_",
        "_self_",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：],
    ],
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：job=dict(
    job=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：project="posttraining",
        project="posttraining",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group="video2world",
        group="video2world",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="videoworld2_dldm_openx_and_videocraft_wodit_warmup",
        name="videoworld2_dldm_openx_and_videocraft_wodit_warmup",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model=dict(
    model=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config=dict(
        config=dict(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dldm_warmup=True,
            dldm_warmup=True,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe_config=dict(
            pipe_config=dict(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resize_online=False,
                resize_online=False,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ema=dict(enabled=False),
                ema=dict(enabled=False),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：guardrail_config=dict(enabled=False),
                guardrail_config=dict(enabled=False),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_num_conditional_frames=1,
                min_num_conditional_frames=1,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_num_conditional_frames=1,
                max_num_conditional_frames=1,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：train_architecture='lora',
            train_architecture='lora',
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ldm_config=dict(
            ldm_config=dict(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：network=dict(
                network=dict(
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：decoder=Decoder3DType.LDM_V2.name,
                    decoder=Decoder3DType.LDM_V2.name, 
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：levels=[8,5,5,5],
                    levels=[8,5,5,5],
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：embedding_dim=4,
                    embedding_dim=4,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：persistent_quantizer=False,
                    persistent_quantizer=False,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_channels=256,
                    z_channels=256,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：channels_mult=[2, 4, 4],
                    channels_mult=[2, 4, 4],
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：patch_size=4,
                    patch_size=4,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：legacy_mode=False,
                    legacy_mode=False,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_compression=4,
                    temporal_compression=4,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：spatial_compression=16,
                    spatial_compression=16,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：act_embedding_num=4,
                    act_embedding_num=4,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：qformer_type='QFormerAdjacentFSingleQ',
                    qformer_type='QFormerAdjacentFSingleQ',
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
                ),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ldm_path="checkpoints/VideoWorld2_dLDM_2B/tokenizer/ldm_tokenizer_training_init_weights.pt"
                ldm_path="checkpoints/VideoWorld2_dLDM_2B/tokenizer/ldm_tokenizer_training_init_weights.pt"
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_parallel=dict(
    model_parallel=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：context_parallel_size=1,
        context_parallel_size=1,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataloader_train=dataloader_train_openx_videocraft,
    dataloader_train=dataloader_train_openx_videocraft,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataloader_val=dataloader_val_videocraft,
    dataloader_val=dataloader_val_videocraft,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trainer=dict(
    trainer=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distributed_parallelism="fsdp",
        distributed_parallelism="fsdp",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：callbacks=dict(
        callbacks=dict(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iter_speed=dict(hit_thres=100000),
            iter_speed=dict(hit_thres=100000),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_iter=100000,
        max_iter=100000,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：run_validation=False
        run_validation=False
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint=dict(
    checkpoint=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：save_iter=5000,
        save_iter=5000,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：optimizer=dict(
    optimizer=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lr=2 ** (-14.5),
        lr=2 ** (-14.5),
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scheduler=dict(
    scheduler=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：warm_up_steps=[2_000],
        warm_up_steps=[2_000],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cycle_lengths=[400_000],
        cycle_lengths=[400_000],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：f_max=[0.6],
        f_max=[0.6],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：f_min=[0.3],
        f_min=[0.3],
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)


# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：videoworld2_dldm_openx_and_videocraft_only_dit = dict(
videoworld2_dldm_openx_and_videocraft_only_dit = dict(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：defaults=[
    defaults=[
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"override /model": "predict2_video2world_ldm_fsdp_2b_480p_16fps"},
        {"override /model": "predict2_video2world_ldm_fsdp_2b_480p_16fps"},
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"override /optimizer": "fusedadamw"},
        {"override /optimizer": "fusedadamw"},
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"override /scheduler": "lambdalinear"},
        {"override /scheduler": "lambdalinear"},
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"override /ckpt_type": "standard"},
        {"override /ckpt_type": "standard"},
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："_self_",
        "_self_",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：],
    ],
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：job=dict(
    job=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：project="posttraining",
        project="posttraining",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group="video2world",
        group="video2world",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="videoworld2_dldm_openx_and_videocraft_only_dit",
        name="videoworld2_dldm_openx_and_videocraft_only_dit",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model=dict(
    model=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config=dict(
        config=dict(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：only_dit=True,
            only_dit=True,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_cross_embedding=False,
            use_cross_embedding=False,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe_config=dict(
            pipe_config=dict(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resize_online=False,
                resize_online=False,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ema=dict(enabled=False),
                ema=dict(enabled=False),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：guardrail_config=dict(enabled=False),
                guardrail_config=dict(enabled=False),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_num_conditional_frames=1,
                min_num_conditional_frames=1,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_num_conditional_frames=1,
                max_num_conditional_frames=1,                
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：train_architecture='lora',
            train_architecture='lora',
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ldm_config=dict(
            ldm_config=dict(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：network=dict(
                network=dict(
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：decoder=Decoder3DType.LDM_V2.name,
                    decoder=Decoder3DType.LDM_V2.name, 
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：levels=[8,5,5,5],
                    levels=[8,5,5,5],
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：embedding_dim=4,
                    embedding_dim=4,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：persistent_quantizer=False,
                    persistent_quantizer=False,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_channels=256,
                    z_channels=256,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：channels_mult=[2, 4, 4],
                    channels_mult=[2, 4, 4],
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：patch_size=4,
                    patch_size=4,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：legacy_mode=False,
                    legacy_mode=False,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_compression=4,
                    temporal_compression=4,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：spatial_compression=16,
                    spatial_compression=16,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：act_embedding_num=4,
                    act_embedding_num=4,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：qformer_type='QFormerAdjacentFSingleQ',
                    qformer_type='QFormerAdjacentFSingleQ',
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
                ),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ldm_path="checkpoints/VideoWorld2_dLDM_2B/tokenizer/ldm_tokenizer_training_init_weights.pt"
                ldm_path="checkpoints/VideoWorld2_dLDM_2B/tokenizer/ldm_tokenizer_training_init_weights.pt"
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_parallel=dict(
    model_parallel=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：context_parallel_size=1,
        context_parallel_size=1,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataloader_train=dataloader_train_openx_videocraft,
    dataloader_train=dataloader_train_openx_videocraft,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataloader_val=dataloader_val_videocraft,
    dataloader_val=dataloader_val_videocraft,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trainer=dict(
    trainer=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distributed_parallelism="fsdp",
        distributed_parallelism="fsdp",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：callbacks=dict(
        callbacks=dict(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iter_speed=dict(hit_thres=100000),
            iter_speed=dict(hit_thres=100000),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_iter=300000,
        max_iter=300000,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint=dict(
    checkpoint=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：save_iter=20000,
        save_iter=20000,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：optimizer=dict(
    optimizer=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lr=2 ** (-14.5),
        lr=2 ** (-14.5),
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scheduler=dict(
    scheduler=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：warm_up_steps=[2_000],
        warm_up_steps=[2_000],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cycle_lengths=[400_000],
        cycle_lengths=[400_000],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：f_max=[0.6],
        f_max=[0.6],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：f_min=[0.3],
        f_min=[0.3],
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)


# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：videoworld2_dldm_openx_and_videocraft = dict(
videoworld2_dldm_openx_and_videocraft = dict(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：defaults=[
    defaults=[
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"override /model": "predict2_video2world_ctrl_ldm_fsdp_2b_480p_16fps"},
        {"override /model": "predict2_video2world_ctrl_ldm_fsdp_2b_480p_16fps"},
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"override /optimizer": "fusedadamw"},
        {"override /optimizer": "fusedadamw"},
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"override /scheduler": "lambdalinear"},
        {"override /scheduler": "lambdalinear"},
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"override /ckpt_type": "standard"},
        {"override /ckpt_type": "standard"},
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# {"override /dataloader_val": "mock"},
        # {"override /dataloader_val": "mock"},
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："_self_",
        "_self_",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：],
    ],
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：job=dict(
    job=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：project="posttraining",
        project="posttraining",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group="video2world",
        group="video2world",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="videoworld2_dldm_openx_and_videocraft",
        name="videoworld2_dldm_openx_and_videocraft",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model=dict(
    model=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config=dict(
        config=dict(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_cross_embedding=True,
            use_cross_embedding=True,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：finetune_base_model=True,
            finetune_base_model=True,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe_config=dict(
            pipe_config=dict(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resize_online=False,
                resize_online=False,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ema=dict(enabled=False),
                ema=dict(enabled=False),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：guardrail_config=dict(enabled=False),
                guardrail_config=dict(enabled=False),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_num_conditional_frames=1,
                min_num_conditional_frames=1,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_num_conditional_frames=1,
                max_num_conditional_frames=1,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net_ctrl=dict(
                net_ctrl=dict(
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：control_weight=0.5,
                    control_weight=0.5,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：layer_mask=[True if (i >= 3) else False for i in range(28)],
                    layer_mask=[True if (i >= 3) else False for i in range(28)],
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
                ),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hint_key="recon_image"
                hint_key="recon_image"
                
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：train_architecture='base',
            train_architecture='base',
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ldm_config=dict(
            ldm_config=dict(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：network=dict(
                network=dict(
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：decoder=Decoder3DType.LDM_V2.name,
                    decoder=Decoder3DType.LDM_V2.name, 
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：levels=[8,5,5,5],
                    levels=[8,5,5,5],
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：embedding_dim=4,
                    embedding_dim=4,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：persistent_quantizer=False,
                    persistent_quantizer=False,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_channels=256,
                    z_channels=256,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：channels_mult=[2, 4, 4],
                    channels_mult=[2, 4, 4],
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：patch_size=4,
                    patch_size=4,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：legacy_mode=False,
                    legacy_mode=False,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_compression=4,
                    temporal_compression=4,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：spatial_compression=16,
                    spatial_compression=16,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：act_embedding_num=4,
                    act_embedding_num=4,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：qformer_type='QFormerAdjacentFSingleQ',
                    qformer_type='QFormerAdjacentFSingleQ',
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
                ),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ldm_path="checkpoints/VideoWorld2_dLDM_2B/VideoWorld2_dLDM_VAE.pt"
                ldm_path="checkpoints/VideoWorld2_dLDM_2B/VideoWorld2_dLDM_VAE.pt"
                # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# ldm_path="checkpoints/posttraining/video2world/VideoWorld2_dLDM_2B/videoworld2_dldm_openx_a...
                # ldm_path="checkpoints/posttraining/video2world/VideoWorld2_dLDM_2B/videoworld2_dldm_openx_and_videocraft_wodit_warmup/checkpoints/model/iter_000100000_ldm.pt"
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_parallel=dict(
    model_parallel=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：context_parallel_size=1,
        context_parallel_size=1,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataloader_train=dataloader_train_openx_videocraft,
    dataloader_train=dataloader_train_openx_videocraft,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataloader_val=dataloader_val_videocraft,
    dataloader_val=dataloader_val_videocraft,

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trainer=dict(
    trainer=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distributed_parallelism="fsdp",
        distributed_parallelism="fsdp",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：callbacks=dict(
        callbacks=dict(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iter_speed=dict(hit_thres=100000),
            iter_speed=dict(hit_thres=100000),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_iter=30000,
        max_iter=30000,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：run_validation=False
        run_validation=False
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint=dict(
    checkpoint=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：save_iter=5000,
        save_iter=5000,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：optimizer=dict(
    optimizer=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lr=2 ** (-14.5),
        lr=2 ** (-14.5),
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scheduler=dict(
    scheduler=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：warm_up_steps=[2_000],
        warm_up_steps=[2_000],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cycle_lengths=[400_000],
        cycle_lengths=[400_000],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：f_max=[0.6],
        f_max=[0.6],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：f_min=[0.3],
        f_min=[0.3],
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)



# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：videoworld2_dldm_openx_and_videocraft_infer = dict(
videoworld2_dldm_openx_and_videocraft_infer = dict(
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：defaults=[
    defaults=[
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"override /model": "predict2_video2world_ctrl_ldm_fsdp_2b_480p_16fps_infer"},
        {"override /model": "predict2_video2world_ctrl_ldm_fsdp_2b_480p_16fps_infer"},
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"override /optimizer": "fusedadamw"},
        {"override /optimizer": "fusedadamw"},
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"override /scheduler": "lambdalinear"},
        {"override /scheduler": "lambdalinear"},
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：{"override /ckpt_type": "standard"},
        {"override /ckpt_type": "standard"},
        # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# {"override /dataloader_val": "mock"},
        # {"override /dataloader_val": "mock"},
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："_self_",
        "_self_",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：],
    ],
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：job=dict(
    job=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：project="posttraining",
        project="posttraining",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group="video2world",
        group="video2world",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name="videoworld2_dldm_openx_and_videocraft_infer",
        name="videoworld2_dldm_openx_and_videocraft_infer",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model=dict(
    model=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config=dict(
        config=dict(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：use_cross_embedding=True,
            use_cross_embedding=True,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：finetune_base_model=True,
            finetune_base_model=True,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_manager_config=dict(
            model_manager_config=dict(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dit_path="checkpoints/VideoWorld2_dLDM_2B/VideoWorld2_dLDM_DiT.pth",
                dit_path="checkpoints/VideoWorld2_dLDM_2B/VideoWorld2_dLDM_DiT.pth",
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：pipe_config=dict(
            pipe_config=dict(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resize_online=False,
                resize_online=False,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ema=dict(enabled=False),
                ema=dict(enabled=False),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：guardrail_config=dict(enabled=False),
                guardrail_config=dict(enabled=False),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_num_conditional_frames=1,
                min_num_conditional_frames=1,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_num_conditional_frames=1,
                max_num_conditional_frames=1,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：net_ctrl=dict(
                net_ctrl=dict(
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：control_weight=0.5,
                    control_weight=0.5,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：layer_mask=[True if (i >= 3) else False for i in range(28)],
                    layer_mask=[True if (i >= 3) else False for i in range(28)],
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
                ),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：hint_key="recon_image"
                hint_key="recon_image"
                
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：train_architecture='base',
            train_architecture='base',
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ldm_config=dict(
            ldm_config=dict(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：network=dict(
                network=dict(
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：decoder=Decoder3DType.LDM_V2.name,
                    decoder=Decoder3DType.LDM_V2.name, 
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：levels=[8,5,5,5],
                    levels=[8,5,5,5],
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：embedding_dim=4,
                    embedding_dim=4,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：persistent_quantizer=False,
                    persistent_quantizer=False,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：z_channels=256,
                    z_channels=256,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：channels_mult=[2, 4, 4],
                    channels_mult=[2, 4, 4],
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：patch_size=4,
                    patch_size=4,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：legacy_mode=False,
                    legacy_mode=False,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：temporal_compression=4,
                    temporal_compression=4,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：spatial_compression=16,
                    spatial_compression=16,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：act_embedding_num=4,
                    act_embedding_num=4,
                    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：qformer_type='QFormerAdjacentFSingleQ',
                    qformer_type='QFormerAdjacentFSingleQ',
                # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
                ),
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ldm_path="checkpoints/VideoWorld2_dLDM_2B/VideoWorld2_dLDM_VAE.pt"
                ldm_path="checkpoints/VideoWorld2_dLDM_2B/VideoWorld2_dLDM_VAE.pt"
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：model_parallel=dict(
    model_parallel=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：context_parallel_size=1,
        context_parallel_size=1,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataloader_train=dataloader_train_videocraft,
    dataloader_train=dataloader_train_videocraft,
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataloader_val=dataloader_train_videocraft,
    dataloader_val=dataloader_train_videocraft,

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：trainer=dict(
    trainer=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distributed_parallelism="fsdp",
        distributed_parallelism="fsdp",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：callbacks=dict(
        callbacks=dict(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：iter_speed=dict(hit_thres=100000),
            iter_speed=dict(hit_thres=100000),
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
        ),
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_iter=300000,
        max_iter=300000,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：run_validation=True
        run_validation=True
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：checkpoint=dict(
    checkpoint=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：save_iter=5000,
        save_iter=5000,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：optimizer=dict(
    optimizer=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：lr=2 ** (-14.5),
        lr=2 ** (-14.5),
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：scheduler=dict(
    scheduler=dict(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：warm_up_steps=[2_000],
        warm_up_steps=[2_000],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cycle_lengths=[400_000],
        cycle_lengths=[400_000],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：f_max=[0.6],
        f_max=[0.6],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：f_min=[0.3],
        f_min=[0.3],
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
    ),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
)




# 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _item in [
for _item in [
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# 2b, paper_airplane
    # 2b, paper_airplane
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：videoworld2_dldm_openx_and_videocraft,
    videoworld2_dldm_openx_and_videocraft,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：videoworld2_dldm_openx_and_videocraft_only_dit,
    videoworld2_dldm_openx_and_videocraft_only_dit,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：videoworld2_dldm_openx_and_videocraft_wodit_warmup,
    videoworld2_dldm_openx_and_videocraft_wodit_warmup,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：videoworld2_dldm_openx_and_videocraft_infer #only for inference
    videoworld2_dldm_openx_and_videocraft_infer #only for inference
  
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：]:
]:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Get the experiment name from the global variable.
    # Get the experiment name from the global variable.
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：experiment_name = [name.lower() for name, value in globals().items() if value is _item][0]
    experiment_name = [name.lower() for name, value in globals().items() if value is _item][0]

    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(
    cs.store(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：group="experiment",
        group="experiment",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：package="_global_",
        package="_global_",
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：name=experiment_name,
        name=experiment_name,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：node=_item,
        node=_item,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )



