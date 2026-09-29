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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.handlers.base import BaseFileHandler
from imaginaire.utils.easy_io.handlers.base import BaseFileHandler
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.handlers.byte_handler import ByteHandler
from imaginaire.utils.easy_io.handlers.byte_handler import ByteHandler
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.handlers.csv_handler import CsvHandler
from imaginaire.utils.easy_io.handlers.csv_handler import CsvHandler
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.handlers.gzip_handler import GzipHandler
from imaginaire.utils.easy_io.handlers.gzip_handler import GzipHandler
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.handlers.imageio_video_handler import ImageioVideoHandler
from imaginaire.utils.easy_io.handlers.imageio_video_handler import ImageioVideoHandler
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.handlers.json_handler import JsonHandler
from imaginaire.utils.easy_io.handlers.json_handler import JsonHandler
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.handlers.jsonl_handler import JsonlHandler
from imaginaire.utils.easy_io.handlers.jsonl_handler import JsonlHandler
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.handlers.np_handler import NumpyHandler
from imaginaire.utils.easy_io.handlers.np_handler import NumpyHandler
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.handlers.pandas_handler import PandasHandler
from imaginaire.utils.easy_io.handlers.pandas_handler import PandasHandler
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.handlers.pickle_handler import PickleHandler
from imaginaire.utils.easy_io.handlers.pickle_handler import PickleHandler
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.handlers.pil_handler import PILHandler
from imaginaire.utils.easy_io.handlers.pil_handler import PILHandler
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.handlers.tarfile_handler import TarHandler
from imaginaire.utils.easy_io.handlers.tarfile_handler import TarHandler
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.handlers.torch_handler import TorchHandler
from imaginaire.utils.easy_io.handlers.torch_handler import TorchHandler
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.handlers.torchjit_handler import TorchJitHandler
from imaginaire.utils.easy_io.handlers.torchjit_handler import TorchJitHandler
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.handlers.txt_handler import TxtHandler
from imaginaire.utils.easy_io.handlers.txt_handler import TxtHandler
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils.easy_io.handlers.yaml_handler import YamlHandler
from imaginaire.utils.easy_io.handlers.yaml_handler import YamlHandler

# 中文说明：计算右侧表达式并保存或更新左侧变量；代码：file_handlers = {
file_handlers = {
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："json": JsonHandler(),
    "json": JsonHandler(),
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："yaml": YamlHandler(),
    "yaml": YamlHandler(),
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："yml": YamlHandler(),
    "yml": YamlHandler(),
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："pickle": PickleHandler(),
    "pickle": PickleHandler(),
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："pkl": PickleHandler(),
    "pkl": PickleHandler(),
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："tar": TarHandler(),
    "tar": TarHandler(),
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："jit": TorchJitHandler(),
    "jit": TorchJitHandler(),
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："npy": NumpyHandler(),
    "npy": NumpyHandler(),
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："txt": TxtHandler(),
    "txt": TxtHandler(),
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："csv": CsvHandler(),
    "csv": CsvHandler(),
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："pandas": PandasHandler(),
    "pandas": PandasHandler(),
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："gz": GzipHandler(),
    "gz": GzipHandler(),
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："jsonl": JsonlHandler(),
    "jsonl": JsonlHandler(),
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："byte": ByteHandler(),
    "byte": ByteHandler(),
# 中文说明：结束前面开始的多行表达式、容器或代码块；代码：}
}

# 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for torch_type in ["pt", "pth", "ckpt"]:
for torch_type in ["pt", "pth", "ckpt"]:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：file_handlers[torch_type] = TorchHandler()
    file_handlers[torch_type] = TorchHandler()
# 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for img_type in ["jpg", "jpeg", "png", "bmp", "gif"]:
for img_type in ["jpg", "jpeg", "png", "bmp", "gif"]:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：file_handlers[img_type] = PILHandler()
    file_handlers[img_type] = PILHandler()
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：file_handlers[img_type].format = img_type
    file_handlers[img_type].format = img_type
# 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for video_type in ["mp4", "avi", "mov", "webm", "flv", "wmv"]:
for video_type in ["mp4", "avi", "mov", "webm", "flv", "wmv"]:
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：file_handlers[video_type] = ImageioVideoHandler()
    file_handlers[video_type] = ImageioVideoHandler()


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def _register_handler(handler, file_formats):
def _register_handler(handler, file_formats):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""Register a handler for some file extensions.
    """Register a handler for some file extensions.

    Args:
        handler (:obj:`BaseFileHandler`): Handler to be registered.
        file_formats (str or list[str]): File formats to be handled by this
            handler.
    """
    # 中文说明：根据条件选择执行分支；代码：if not isinstance(handler, BaseFileHandler):
    if not isinstance(handler, BaseFileHandler):
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError(f"handler must be a child of BaseFileHandler, not {type(handler)}")
        raise TypeError(f"handler must be a child of BaseFileHandler, not {type(handler)}")
    # 中文说明：根据条件选择执行分支；代码：if isinstance(file_formats, str):
    if isinstance(file_formats, str):
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：file_formats = [file_formats]
        file_formats = [file_formats]
    # 中文说明：根据条件选择执行分支；代码：if not all([isinstance(item, str) for item in file_formats]):
    if not all([isinstance(item, str) for item in file_formats]):
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise TypeError("file_formats must be a str or a list of str")
        raise TypeError("file_formats must be a str or a list of str")
    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for ext in file_formats:
    for ext in file_formats:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：file_handlers[ext] = handler
        file_handlers[ext] = handler


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def register_handler(file_formats, **kwargs):
def register_handler(file_formats, **kwargs):
    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def wrap(cls):
    def wrap(cls):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：_register_handler(cls(**kwargs), file_formats)
        _register_handler(cls(**kwargs), file_formats)
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return cls
        return cls

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return wrap
    return wrap
