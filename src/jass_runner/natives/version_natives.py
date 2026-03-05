"""版本相关 native 函数实现。

此模块包含与游戏版本相关的 JASS native 函数。
"""

import logging
from .base import NativeFunction
from .handle_base import Handle

logger = logging.getLogger(__name__)

# 版本常量
VERSION_REIGN_OF_CHAOS = 0   # 混乱之治
VERSION_FROZEN_THRONE = 1    # 冰封王座


class Version(Handle):
    """版本类型 handle。

    用于表示游戏版本（混乱之治或冰封王座）。

    属性：
        version_value: 版本整数值（0或1）
    """

    def __init__(self, handle_id: str, version_value: int):
        super().__init__(handle_id, "version")
        self.version_value = version_value


class VersionGet(NativeFunction):
    """获取当前游戏版本。

    在本模拟器中，始终返回冰封王座版本。
    """

    @property
    def name(self) -> str:
        return "VersionGet"

    def execute(self, state_context) -> Version:
        """获取当前游戏版本。

        参数：
            state_context: 状态上下文

        返回：
            Version handle对象（冰封王座版本）
        """
        # 从状态上下文中获取handle管理器来创建唯一handle
        handle_manager = getattr(state_context, 'handle_manager', None)
        if handle_manager:
            handle_id = f"version_{handle_manager._generate_id()}"
        else:
            handle_id = "version_001"

        version = Version(handle_id, VERSION_FROZEN_THRONE)
        logger.info(f"[VersionGet] 返回游戏版本: 冰封王座 (handle={handle_id})")
        return version


class ConvertVersion(NativeFunction):
    """转换版本类型。

    在本实现中，直接返回传入的版本值。
    """

    @property
    def name(self) -> str:
        return "ConvertVersion"

    def execute(self, state_context, version: int) -> int:
        """转换版本类型。

        参数：
            state_context: 状态上下文
            version: 版本整数值

        返回：
            传入的版本值
        """
        logger.info(f"[ConvertVersion] 转换版本: {version}")
        return version
