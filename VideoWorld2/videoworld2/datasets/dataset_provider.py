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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import omegaconf
import omegaconf

# 中文说明：开始一个可捕获异常的代码块；代码：try:
try:
    # 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from megatron.core import parallel_state
    from megatron.core import parallel_state

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：USE_MEGATRON = True
    USE_MEGATRON = True
# 中文说明：处理异常、清理资源或管理上下文；代码：except ImportError:
except ImportError:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：USE_MEGATRON = False
    USE_MEGATRON = False
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from webdataset.handlers import warn_and_continue
from webdataset.handlers import warn_and_continue

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import cosmos_predict2.datasets.decoders.video_decoder as video_decoder
import cosmos_predict2.datasets.decoders.video_decoder as video_decoder
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import cosmos_predict2.datasets.distributor.parallel_sync_multi_aspect_ratio as parallel_sync...
import cosmos_predict2.datasets.distributor.parallel_sync_multi_aspect_ratio as parallel_sync_multi_aspect_ratio
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import cosmos_predict2.datasets.webdataset as webdataset
import cosmos_predict2.datasets.webdataset as webdataset
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import imaginaire.datasets.webdataset.decoders.image as image_decoders
import imaginaire.datasets.webdataset.decoders.image as image_decoders
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import imaginaire.datasets.webdataset.decoders.pickle as pickle_decoders
import imaginaire.datasets.webdataset.decoders.pickle as pickle_decoders
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import imaginaire.datasets.webdataset.distributors as distributors
import imaginaire.datasets.webdataset.distributors as distributors
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.datasets.augmentor_provider import AUGMENTOR_OPTIONS
from videoworld2.datasets.augmentor_provider import AUGMENTOR_OPTIONS
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from videoworld2.datasets.utils import IMAGE_RES_SIZE_INFO, VIDEO_RES_SIZE_INFO
from videoworld2.datasets.utils import IMAGE_RES_SIZE_INFO, VIDEO_RES_SIZE_INFO
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.datasets.webdataset.config.schema import DatasetConfig
from imaginaire.datasets.webdataset.config.schema import DatasetConfig
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_video_dataset(
def get_video_dataset(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dataset_name: str,
    dataset_name: str,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video_decoder_name: str,
    video_decoder_name: str,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：resolution: str,
    resolution: str,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：is_train: bool = True,
    is_train: bool = True,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：num_video_frames: int = 121,
    num_video_frames: int = 121,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：chunk_size: int = 0,
    chunk_size: int = 0,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：min_fps_thres: int = 10,
    min_fps_thres: int = 10,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：max_fps_thres: int = 60,
    max_fps_thres: int = 60,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：augmentor_name: str = "video_basic_augmentor_v2",
    augmentor_name: str = "video_basic_augmentor_v2",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：caption_type: str = "t2w_qwen2p5_7b",
    caption_type: str = "t2w_qwen2p5_7b",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：embedding_type: str = "t5_xxl",
    embedding_type: str = "t5_xxl",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：detshuffle: bool = False,
    detshuffle: bool = False,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：long_caption_ratio: int = 7,
    long_caption_ratio: int = 7,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：medium_caption_ratio: int = 2,
    medium_caption_ratio: int = 2,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：short_caption_ratio: int = 1,
    short_caption_ratio: int = 1,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：user_caption_ratio: int = 90,
    user_caption_ratio: int = 90,
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> omegaconf.dictconfig.DictConfig:
) -> omegaconf.dictconfig.DictConfig:
    # 中文说明：检查运行时假设是否成立；代码：assert resolution in VIDEO_RES_SIZE_INFO.keys(), "The provided resolution cannot be found in ...
    assert resolution in VIDEO_RES_SIZE_INFO.keys(), "The provided resolution cannot be found in VIDEO_RES_SIZE_INFO."
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：basic_augmentor_names = ["video_basic_augmentor_v2", "video_basic_augmentor_v2_with_edge_cont...
    basic_augmentor_names = ["video_basic_augmentor_v2", "video_basic_augmentor_v2_with_edge_control"]
    # 中文说明：根据条件选择执行分支；代码：if video_decoder_name == "video_naive_bytes":
    if video_decoder_name == "video_naive_bytes":
        # 中文说明：检查运行时假设是否成立；代码：assert (
        assert (
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：augmentor_name in basic_augmentor_names
            augmentor_name in basic_augmentor_names
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), "We can only use video_basic_augmentor_v2 with video_naive_bytes decoder."
        ), "We can only use video_basic_augmentor_v2 with video_naive_bytes decoder."
    # 中文说明：根据条件选择执行分支；代码：if augmentor_name in basic_augmentor_names:
    if augmentor_name in basic_augmentor_names:
        # 中文说明：检查运行时假设是否成立；代码：assert (
        assert (
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_decoder_name == "video_naive_bytes"
            video_decoder_name == "video_naive_bytes"
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), "We can only use video_naive_bytes decoder with video_basic_augmentor_v2."
        ), "We can only use video_naive_bytes decoder with video_basic_augmentor_v2."

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset_info_fn = DATASET_OPTIONS[dataset_name]
    dataset_info_fn = DATASET_OPTIONS[dataset_name]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset_info = dataset_info_fn("", caption_type, embedding_type)
    dataset_info = dataset_info_fn("", caption_type, embedding_type)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：augmentor = AUGMENTOR_OPTIONS[augmentor_name](
    augmentor = AUGMENTOR_OPTIONS[augmentor_name](
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resolution=resolution,
        resolution=resolution,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：caption_type=caption_type,
        caption_type=caption_type,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：embedding_type=embedding_type,
        embedding_type=embedding_type,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_fps=min_fps_thres,
        min_fps=min_fps_thres,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_fps=max_fps_thres,
        max_fps=max_fps_thres,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：long_caption_ratio=long_caption_ratio,
        long_caption_ratio=long_caption_ratio,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：medium_caption_ratio=medium_caption_ratio,
        medium_caption_ratio=medium_caption_ratio,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：short_caption_ratio=short_caption_ratio,
        short_caption_ratio=short_caption_ratio,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：user_caption_ratio=user_caption_ratio,
        user_caption_ratio=user_caption_ratio,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：num_video_frames=num_video_frames,
        num_video_frames=num_video_frames,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )

    # 中文说明：根据条件选择执行分支；代码：if parallel_state.is_initialized() and (
    if parallel_state.is_initialized() and (
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parallel_state.get_context_parallel_world_size() > 1
        parallel_state.get_context_parallel_world_size() > 1
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：or parallel_state.get_tensor_model_parallel_world_size() > 1
        or parallel_state.get_tensor_model_parallel_world_size() > 1
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.critical(
        log.critical(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Using parallelism size CP :{parallel_state.get_context_parallel_world_size()}, TP :{paralle...
            f"Using parallelism size CP :{parallel_state.get_context_parallel_world_size()}, TP :{parallel_state.get_tensor_model_parallel_world_size()} for video dataset, switch to ShardlistMultiAspectRatioParallelSync distributor"
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distributor = parallel_sync_multi_aspect_ratio.ShardlistMultiAspectRatioParallelSync(
        distributor = parallel_sync_multi_aspect_ratio.ShardlistMultiAspectRatioParallelSync(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：shuffle=True,
            shuffle=True,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：split_by_node=True,
            split_by_node=True,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：split_by_worker=True,
            split_by_worker=True,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resume_flag=True,
            resume_flag=True,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：verbose=True,
            verbose=True,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_infinite_loader=is_train,
            is_infinite_loader=is_train,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：detshuffle = True # overwrite detshuffle.
        detshuffle = True  # overwrite detshuffle.
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distributor = distributors.ShardlistMultiAspectRatio(
        distributor = distributors.ShardlistMultiAspectRatio(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：shuffle=True,
            shuffle=True,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：split_by_node=True,
            split_by_node=True,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：split_by_worker=True,
            split_by_worker=True,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resume_flag=True,
            resume_flag=True,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：verbose=False,
            verbose=False,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_infinite_loader=is_train,
            is_infinite_loader=is_train,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_data_config = DatasetConfig(
    video_data_config = DatasetConfig(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：keys=[], # use the per_dataset_keys in DatasetInfo instead
        keys=[],  # use the per_dataset_keys in DatasetInfo instead
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：buffer_size=100,
        buffer_size=100,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：streaming_download=True,
        streaming_download=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset_info=dataset_info,
        dataset_info=dataset_info,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distributor=distributor,
        distributor=distributor,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：decoders=[
        decoders=[
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：video_decoder.construct_video_decoder(
            video_decoder.construct_video_decoder(
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：video_decoder_name=video_decoder_name,
                video_decoder_name=video_decoder_name,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sequence_length=num_video_frames,
                sequence_length=num_video_frames,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：chunk_size=chunk_size,
                chunk_size=chunk_size,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：min_fps_thres=min_fps_thres,
                min_fps_thres=min_fps_thres,
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：max_fps_thres=max_fps_thres,
                max_fps_thres=max_fps_thres,
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：),
            ),
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pickle_decoders.pkl_decoder,
            pickle_decoders.pkl_decoder,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：],
        ],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：augmentation=augmentor,
        augmentation=augmentor,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：remove_extension_from_keys=True,
        remove_extension_from_keys=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sample_keys_full_list_path=None,
        sample_keys_full_list_path=None,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return webdataset.Dataset(config=video_data_config, decoder_handler=warn_and_continue, detshu...
    return webdataset.Dataset(config=video_data_config, decoder_handler=warn_and_continue, detshuffle=detshuffle)


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_image_dataset(
def get_image_dataset(
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dataset_name: str,
    dataset_name: str,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：resolution: str,
    resolution: str,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dataset_resolution_type: str = "all",
    dataset_resolution_type: str = "all",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：is_train: bool = True,
    is_train: bool = True,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：augmentor_name: str = "image_basic_augmentor",
    augmentor_name: str = "image_basic_augmentor",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：detshuffle: bool = False,
    detshuffle: bool = False,
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：caption_type: str = "ai_v3p1",
    caption_type: str = "ai_v3p1",
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：embedding_type: str = "t5_xxl",
    embedding_type: str = "t5_xxl",
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：) -> omegaconf.dictconfig.DictConfig:
) -> omegaconf.dictconfig.DictConfig:
    # 中文说明：检查运行时假设是否成立；代码：assert resolution in IMAGE_RES_SIZE_INFO.keys(), "The provided resolution cannot be found in ...
    assert resolution in IMAGE_RES_SIZE_INFO.keys(), "The provided resolution cannot be found in IMAGE_RES_SIZE_INFO."
    # 中文说明：检查运行时假设是否成立；代码：assert dataset_resolution_type in [
    assert dataset_resolution_type in [
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："all",
        "all",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："gt720p",
        "gt720p",
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："gt1080p",
        "gt1080p",
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：], f"The provided dataset resolution type {dataset_resolution_type} is not supported."
    ], f"The provided dataset resolution type {dataset_resolution_type} is not supported."
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# dataset_resolution_type
    # dataset_resolution_type
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# -- all - uses all dataset resolutions
    # -- all - uses all dataset resolutions
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# -- gt720p - Uses only resolutions >= 720p
    # -- gt720p - Uses only resolutions >= 720p
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# -- gt1080p - Uses only resolutions >= 1080p
    # -- gt1080p - Uses only resolutions >= 1080p
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset_info_fn = DATASET_OPTIONS[dataset_name]
    dataset_info_fn = DATASET_OPTIONS[dataset_name]
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset_info = dataset_info_fn("", caption_type, embedding_type, dataset_resolution_type)
    dataset_info = dataset_info_fn("", caption_type, embedding_type, dataset_resolution_type)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：augmentation = AUGMENTOR_OPTIONS[augmentor_name](
    augmentation = AUGMENTOR_OPTIONS[augmentor_name](
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resolution=resolution,
        resolution=resolution,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：caption_type=caption_type,
        caption_type=caption_type,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：embedding_type=embedding_type,
        embedding_type=embedding_type,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )

    # 中文说明：根据条件选择执行分支；代码：if parallel_state.is_initialized() and (
    if parallel_state.is_initialized() and (
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：parallel_state.get_context_parallel_world_size() > 1
        parallel_state.get_context_parallel_world_size() > 1
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：or parallel_state.get_tensor_model_parallel_world_size() > 1
        or parallel_state.get_tensor_model_parallel_world_size() > 1
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：):
    ):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.critical(
        log.critical(
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：f"Using parallelism size CP :{parallel_state.get_context_parallel_world_size()}, TP :{paralle...
            f"Using parallelism size CP :{parallel_state.get_context_parallel_world_size()}, TP :{parallel_state.get_tensor_model_parallel_world_size()} for image dataset, switch to ShardlistMultiAspectRatioParallelSync distributor"
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distributor = parallel_sync_multi_aspect_ratio.ShardlistMultiAspectRatioParallelSync(
        distributor = parallel_sync_multi_aspect_ratio.ShardlistMultiAspectRatioParallelSync(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：shuffle=True,
            shuffle=True,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：split_by_node=True,
            split_by_node=True,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：split_by_worker=True,
            split_by_worker=True,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resume_flag=True,
            resume_flag=True,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：verbose=True,
            verbose=True,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_infinite_loader=is_train,
            is_infinite_loader=is_train,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：detshuffle = True # overwrite detshuffle.
        detshuffle = True  # overwrite detshuffle.
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distributor = distributors.ShardlistMultiAspectRatio(
        distributor = distributors.ShardlistMultiAspectRatio(
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：shuffle=True,
            shuffle=True,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：split_by_node=True,
            split_by_node=True,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：split_by_worker=True,
            split_by_worker=True,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resume_flag=True,
            resume_flag=True,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：verbose=False,
            verbose=False,
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_infinite_loader=is_train,
            is_infinite_loader=is_train,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
        )

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：image_data_config = DatasetConfig(
    image_data_config = DatasetConfig(
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：keys=[],
        keys=[],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：buffer_size=25,
        buffer_size=25,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：streaming_download=True,
        streaming_download=True,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：dataset_info=dataset_info,
        dataset_info=dataset_info,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：distributor=distributor,
        distributor=distributor,
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：decoders=[
        decoders=[
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：image_decoders.pil_loader,
            image_decoders.pil_loader,
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：pickle_decoders.pkl_decoder,
            pickle_decoders.pkl_decoder,
        # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：],
        ],
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：augmentation=augmentation,
        augmentation=augmentation,
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：)
    )

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return webdataset.Dataset(config=image_data_config, detshuffle=detshuffle)
    return webdataset.Dataset(config=image_data_config, detshuffle=detshuffle)
