"""版本相关 native 函数实现。

此模块包含与游戏版本相关的 JASS native 函数。
"""

import logging
from .base import NativeFunction

logger = logging.getLogger(__name__)

# 版本常量
VERSION_REIGN_OF_CHAOS = 0   # 混乱之治
VERSION_FROZEN_THRONE = 1    # 冰封王座


class VersionGet(NativeFunction):
    """获取当前游戏版本。

    在本模拟器中，始终返回冰封王座版本。
    """

    @property
    def name(self) -> str:
        return "VersionGet"

    def execute(self, state_context) -> int:
        """获取当前游戏版本。

        参数：
            state_context: 状态上下文

        返回：
            VERSION_FROZEN_THRONE (1)
        """
        logger.info("[VersionGet] 返回游戏版本: 冰封王座 (1)")
        return VERSION_FROZEN_THRONE


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
