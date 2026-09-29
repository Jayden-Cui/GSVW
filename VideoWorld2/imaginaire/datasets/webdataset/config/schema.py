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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Optional, Type
from typing import Optional, Type

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import attrs
import attrs
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from torch.utils.data import IterableDataset
from torch.utils.data import IterableDataset

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire import config
from imaginaire import config
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.config import make_freezable
from imaginaire.config import make_freezable
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.datasets.webdataset.augmentors.augmentor import Augmentor
from imaginaire.datasets.webdataset.augmentors.augmentor import Augmentor


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@make_freezable
@make_freezable
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class DatasetInfo:
class DatasetInfo:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：wdinfo: list[str] # List of wdinfo files
    wdinfo: list[str]  # List of wdinfo files
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：opts: dict = attrs.Factory(dict) # Additional dataset info args
    opts: dict = attrs.Factory(dict)  # Additional dataset info args
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：per_dataset_keys: list[str] = attrs.Factory(list) # List of keys per dataset
    per_dataset_keys: list[str] = attrs.Factory(list)  # List of keys per dataset
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：source: str = "" # data source
    source: str = ""  # data source


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@make_freezable
@make_freezable
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class TarSample:
class TarSample:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：path: str # Path to the sample
    path: str  # Path to the sample
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：root: str # Root folder
    root: str  # Root folder
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：keys: list # List of keys to be loaded from the webdataset
    keys: list  # List of keys to be loaded from the webdataset
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：meta: DatasetInfo # Metadata
    meta: DatasetInfo  # Metadata
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dset_id: str # Dataset id
    dset_id: str  # Dataset id
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sample_keys_full_list: str = None # Path to the file containing full sample keys for the tar ...
    sample_keys_full_list: str = None  # Path to the file containing full sample keys for the tar file


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@make_freezable
@make_freezable
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class Wdinfo:
class Wdinfo:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：tar_files: list[TarSample] # List of all tar samples
    tar_files: list[TarSample]  # List of all tar samples
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：total_key_count: int # Total number of elements present in the dataset
    total_key_count: int  # Total number of elements present in the dataset
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：chunk_size: int # Number of elements present in each tar
    chunk_size: int  # Number of elements present in each tar


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@make_freezable
@make_freezable
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class AugmentorConfig:
class AugmentorConfig:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Type of augmentor
    # Type of augmentor
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：type: Type[Augmentor]
    type: Type[Augmentor]
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Input keys used by the augmentor
    # Input keys used by the augmentor
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：input_keys: list[str]
    input_keys: list[str]
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Output keys returned by the augmentor
    # Output keys returned by the augmentor
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：output_keys: Optional[list[str]] = None
    output_keys: Optional[list[str]] = None
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Additional arguments used by the augmentor
    # Additional arguments used by the augmentor
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：args: Optional[dict] = None
    args: Optional[dict] = None

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def make_instance(self) -> Augmentor:
    def make_instance(self) -> Augmentor:
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return self.type(input_keys=self.input_keys, output_keys=self.output_keys, args=self.args)
        return self.type(input_keys=self.input_keys, output_keys=self.output_keys, args=self.args)


# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@make_freezable
@make_freezable
# 中文说明：为下面的函数或类应用装饰器，以改变或补充其行为；代码：@attrs.define(slots=False)
@attrs.define(slots=False)
# 中文说明：定义一个类，用来组织本行声明的对象状态和行为；代码：class DatasetConfig:
class DatasetConfig:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：keys: list[str] # List of keys used
    keys: list[str]  # List of keys used
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：buffer_size: int # Buffer size used by each worker
    buffer_size: int  # Buffer size used by each worker
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：dataset_info: list[DatasetInfo] # List of dataset info files, one for each dataset
    dataset_info: list[DatasetInfo]  # List of dataset info files, one for each dataset
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：distributor: IterableDataset # Iterator for returning list of tar files
    distributor: IterableDataset  # Iterator for returning list of tar files
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：decoders: list # List of decoder functions for decoding bytestream
    decoders: list  # List of decoder functions for decoding bytestream
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：augmentation: dict[str, AugmentorConfig] # Dictionary containing all augmentations
    augmentation: dict[str, AugmentorConfig]  # Dictionary containing all augmentations
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：streaming_download: bool = True # Whether to use streaming loader
    streaming_download: bool = True  # Whether to use streaming loader
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：remove_extension_from_keys: bool = True # True: objects will have a key of data_type; False: ...
    remove_extension_from_keys: bool = True  # True: objects will have a key of data_type; False: data_type.extension
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：sample_keys_full_list_path: Optional[
    sample_keys_full_list_path: Optional[
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：str
        str
    # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：] = None # Path to the file containing all keys present in the dataset, e.g., "index"
    ] = None  # Path to the file containing all keys present in the dataset, e.g., "index"
