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
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import importlib
import importlib
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import os
import os
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import pkgutil
import pkgutil
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import sys
import sys
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from dataclasses import fields as dataclass_fields
from dataclasses import fields as dataclass_fields
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from dataclasses import is_dataclass
from dataclasses import is_dataclass
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from typing import Any, Dict, Optional
from typing import Any, Dict, Optional

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import attr
import attr
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：import attrs
import attrs
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from hydra import compose, initialize
from hydra import compose, initialize
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from hydra.core.config_store import ConfigStore
from hydra.core.config_store import ConfigStore
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from hydra.core.global_hydra import GlobalHydra
from hydra.core.global_hydra import GlobalHydra
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from omegaconf import DictConfig, OmegaConf
from omegaconf import DictConfig, OmegaConf

# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.config import Config
from imaginaire.config import Config
# 中文说明：导入本行列出的模块或名称，为后续代码提供依赖；代码：from imaginaire.utils import log
from imaginaire.utils import log


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def is_attrs_or_dataclass(obj) -> bool:
def is_attrs_or_dataclass(obj) -> bool:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Check if the object is an instance of an attrs class or a dataclass.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is an instance of an attrs class or a dataclass, False otherwise.
    """
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return is_dataclass(obj) or attr.has(type(obj))
    return is_dataclass(obj) or attr.has(type(obj))


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_fields(obj):
def get_fields(obj):
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Get the fields of an attrs class or a dataclass.

    Args:
        obj: The object to get fields from. Must be an instance of an attrs class or a dataclass.

    Returns:
        list: A list of field names.

    Raises:
        ValueError: If the object is neither an attrs class nor a dataclass.
    """
    # 中文说明：根据条件选择执行分支；代码：if is_dataclass(obj):
    if is_dataclass(obj):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return [field.name for field in dataclass_fields(obj)]
        return [field.name for field in dataclass_fields(obj)]
    # 中文说明：根据条件选择执行分支；代码：elif attr.has(type(obj)):
    elif attr.has(type(obj)):
        # 中文说明：从当前函数返回结果或结束函数执行；代码：return [field.name for field in attr.fields(type(obj))]
        return [field.name for field in attr.fields(type(obj))]
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError("The object is neither an attrs class nor a dataclass.")
        raise ValueError("The object is neither an attrs class nor a dataclass.")


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def override(config: Config, overrides: Optional[list[str]] = None) -> Config:
def override(config: Config, overrides: Optional[list[str]] = None) -> Config:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    :param config: the instance of class `Config` (usually from `make_config`)
    :param overrides: list of overrides for config
    :return: the composed instance of class `Config`
    """
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Store the class of the config for reconstruction after overriding.
    # Store the class of the config for reconstruction after overriding.
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# config_class = type(config)
    # config_class = type(config)

    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Convert Config object to a DictConfig object
    # Convert Config object to a DictConfig object
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config_dict = attrs.asdict(config)
    config_dict = attrs.asdict(config)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config_omegaconf = DictConfig(content=config_dict, flags={"allow_objects": True})
    config_omegaconf = DictConfig(content=config_dict, flags={"allow_objects": True})
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Enforce "--" separator between the script arguments and overriding configs.
    # Enforce "--" separator between the script arguments and overriding configs.
    # 中文说明：根据条件选择执行分支；代码：if overrides:
    if overrides:
        # 中文说明：根据条件选择执行分支；代码：if overrides[0] != "--":
        if overrides[0] != "--":
            # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise ValueError('Hydra config overrides must be separated with a "--" token.')
            raise ValueError('Hydra config overrides must be separated with a "--" token.')
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：overrides = overrides[1:]
        overrides = overrides[1:]
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Use Hydra to handle overrides
    # Use Hydra to handle overrides
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：cs = ConfigStore.instance()
    cs = ConfigStore.instance()
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：cs.store(name="config", node=config_omegaconf)
    cs.store(name="config", node=config_omegaconf)
    # 中文说明：根据条件选择执行分支；代码：if not GlobalHydra().is_initialized():
    if not GlobalHydra().is_initialized():
        # 中文说明：处理异常、清理资源或管理上下文；代码：with initialize(version_base=None):
        with initialize(version_base=None):
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config_omegaconf = compose(config_name="config", overrides=overrides)
            config_omegaconf = compose(config_name="config", overrides=overrides)
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：OmegaConf.resolve(config_omegaconf)
            OmegaConf.resolve(config_omegaconf)
    # 中文说明：根据条件选择执行分支；代码：else:
    else:
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config_omegaconf = compose(config_name="config", overrides=overrides)
        config_omegaconf = compose(config_name="config", overrides=overrides)
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：OmegaConf.resolve(config_omegaconf)
        OmegaConf.resolve(config_omegaconf)

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def config_from_dict(ref_instance: Any, kwargs: Any) -> Any:
    def config_from_dict(ref_instance: Any, kwargs: Any) -> Any:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Construct an instance of the same type as ref_instance using the provided dictionary or data or unstructured data

        Args:
            ref_instance: The reference instance to determine the type and fields when needed
            kwargs: A dictionary of keyword arguments to use for constructing the new instance or primitive data or unstructured data

        Returns:
            Any: A new instance of the same type as ref_instance constructed using the provided kwargs or the primitive data or unstructured data

        Raises:
            AssertionError: If the fields do not match or if extra keys are found.
            Exception: If there is an error constructing the new instance.
        """
        # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：is_type = is_attrs_or_dataclass(ref_instance)
        is_type = is_attrs_or_dataclass(ref_instance)
        # 中文说明：根据条件选择执行分支；代码：if not is_type:
        if not is_type:
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return kwargs
            return kwargs
        # 中文说明：根据条件选择执行分支；代码：else:
        else:
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：ref_fields = set(get_fields(ref_instance))
            ref_fields = set(get_fields(ref_instance))
            # 中文说明：检查运行时假设是否成立；代码：assert isinstance(kwargs, dict) or isinstance(
            assert isinstance(kwargs, dict) or isinstance(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：kwargs, DictConfig
                kwargs, DictConfig
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), "kwargs must be a dictionary or a DictConfig"
            ), "kwargs must be a dictionary or a DictConfig"
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：keys = set(kwargs.keys())
            keys = set(kwargs.keys())

            # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# ref_fields must equal to or include all keys
            # ref_fields must equal to or include all keys
            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：extra_keys = keys - ref_fields
            extra_keys = keys - ref_fields
            # 中文说明：检查运行时假设是否成立；代码：assert ref_fields == keys or keys.issubset(
            assert ref_fields == keys or keys.issubset(
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：ref_fields
                ref_fields
            # 中文说明：结束前面开始的多行表达式、容器或代码块；代码：), f"Fields mismatch: {ref_fields} != {keys}. Extra keys found: {extra_keys} \n \t when const...
            ), f"Fields mismatch: {ref_fields} != {keys}. Extra keys found: {extra_keys} \n \t when constructing {type(ref_instance)} with {keys}"

            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：resolved_kwargs: Dict[str, Any] = {}
            resolved_kwargs: Dict[str, Any] = {}
            # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for f in keys:
            for f in keys:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：resolved_kwargs[f] = config_from_dict(getattr(ref_instance, f), kwargs[f])
                resolved_kwargs[f] = config_from_dict(getattr(ref_instance, f), kwargs[f])
            # 中文说明：开始一个可捕获异常的代码块；代码：try:
            try:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：new_instance = type(ref_instance)(**resolved_kwargs)
                new_instance = type(ref_instance)(**resolved_kwargs)
            # 中文说明：处理异常、清理资源或管理上下文；代码：except Exception as e:
            except Exception as e:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.error(f"Error when constructing {type(ref_instance)} with {resolved_kwargs}")
                log.error(f"Error when constructing {type(ref_instance)} with {resolved_kwargs}")
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.error(e)
                log.error(e)
                # 中文说明：主动抛出异常，报告当前无法继续处理的情况；代码：raise e
                raise e
            # 中文说明：从当前函数返回结果或结束函数执行；代码：return new_instance
            return new_instance

    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config = config_from_dict(config, config_omegaconf)
    config = config_from_dict(config, config_omegaconf)

    # 中文说明：从当前函数返回结果或结束函数执行；代码：return config
    return config


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def get_config_module(config_file: str) -> str:
def get_config_module(config_file: str) -> str:
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# import pdb;pdb.set_trace()
    # import pdb;pdb.set_trace()
    # 中文说明：根据条件选择执行分支；代码：if not config_file.endswith(".py"):
    if not config_file.endswith(".py"):
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.error("Config file cannot be specified as module.")
        log.error("Config file cannot be specified as module.")
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.error("Please provide the path to the Python config file (relative to the Imaginaire4 roo...
        log.error("Please provide the path to the Python config file (relative to the Imaginaire4 root).")
    # 中文说明：检查运行时假设是否成立；代码：assert os.path.isfile(config_file), f"Imaginaire4 config file ({config_file}) not found."
    assert os.path.isfile(config_file), f"Imaginaire4 config file ({config_file}) not found."
    # 中文说明：保留原有注释，帮助说明项目背景或实现约束；原文：# Convert to importable module format.
    # Convert to importable module format.
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：config_module = config_file.replace("/", ".").replace(".py", "")
    config_module = config_file.replace("/", ".").replace(".py", "")
    # 中文说明：从当前函数返回结果或结束函数执行；代码：return config_module
    return config_module


# 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def import_all_modules_from_package(package_path: str, reload: bool = False, skip_underscore:...
def import_all_modules_from_package(package_path: str, reload: bool = False, skip_underscore: bool = True) -> None:
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
    """
    Import all modules from the specified package path recursively.

    This function is typically used in conjunction with Hydra to ensure that all modules
    within a specified package are imported, which is necessary for registering configurations.

    Example usage:
    ```python
    import_all_modules_from_package("projects.cosmos.diffusion.v1.config.experiment", reload=True, skip_underscore=False)
    ```

    Args:
        package_path (str): The dotted path to the package from which to import all modules.
        reload (bool): Flag to determine whether to reload modules if they're already imported.
        skip_underscore (bool): If True, skips importing modules that start with an underscore.
    """
    # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.critical(f"{'Reloading' if reload else 'Importing'} all modules from package {package_pat...
    log.critical(f"{'Reloading' if reload else 'Importing'} all modules from package {package_path}")
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：package = importlib.import_module(package_path)
    package = importlib.import_module(package_path)
    # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：package_directory = package.__path__
    package_directory = package.__path__

    # 中文说明：定义一个函数或方法，封装本行声明的行为；代码：def import_modules_recursively(directory: str, prefix: str) -> None:
    def import_modules_recursively(directory: str, prefix: str) -> None:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码："""
        """
        Recursively imports or reloads all modules in the given directory.

        Args:
            directory (str): The file system path to the current package directory.
            prefix (str): The module prefix (e.g., 'projects.cosmos.diffusion.v1.config').
        """
        # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for _, module_name, is_pkg in pkgutil.iter_modules([directory]):
        for _, module_name, is_pkg in pkgutil.iter_modules([directory]):
            # 中文说明：根据条件选择执行分支；代码：if skip_underscore and module_name.startswith("_"):
            if skip_underscore and module_name.startswith("_"):
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(f"Skipping module {module_name} as it starts with an underscore")
                log.debug(f"Skipping module {module_name} as it starts with an underscore")
                # 中文说明：执行循环控制或空操作；代码：continue
                continue

            # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：full_module_name = f"{prefix}.{module_name}"
            full_module_name = f"{prefix}.{module_name}"
            # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：log.debug(f"{'Reloading' if reload else 'Importing'} module {full_module_name}")
            log.debug(f"{'Reloading' if reload else 'Importing'} module {full_module_name}")

            # 中文说明：根据条件选择执行分支；代码：if full_module_name in sys.modules and reload:
            if full_module_name in sys.modules and reload:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：importlib.reload(sys.modules[full_module_name])
                importlib.reload(sys.modules[full_module_name])
            # 中文说明：根据条件选择执行分支；代码：else:
            else:
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：importlib.import_module(full_module_name)
                importlib.import_module(full_module_name)

            # 中文说明：根据条件选择执行分支；代码：if is_pkg:
            if is_pkg:
                # 中文说明：计算右侧表达式并保存或更新左侧变量；代码：sub_package_directory = os.path.join(directory, module_name)
                sub_package_directory = os.path.join(directory, module_name)
                # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：import_modules_recursively(sub_package_directory, full_module_name)
                import_modules_recursively(sub_package_directory, full_module_name)

    # 中文说明：遍历本行指定的序列或迭代器，并处理每个元素；代码：for directory in package_directory:
    for directory in package_directory:
        # 中文说明：执行当前语句，完成该行表达式所表示的处理；代码：import_modules_recursively(directory, package_path)
        import_modules_recursively(directory, package_path)
