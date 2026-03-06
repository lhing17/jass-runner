"""玩家控制器相关 native 函数实现。

此模块包含与玩家控制器类型相关的 JASS native 函数。
"""

import logging
from typing import TYPE_CHECKING

from .base import NativeFunction

if TYPE_CHECKING:
    from .state import StateContext
    from .handle import Player

logger = logging.getLogger(__name__)


class GetPlayerController(NativeFunction):
    """获取玩家控制器类型。"""

    @property
    def name(self) -> str:
        """获取 native 函数名称。

        返回：
            函数名称 "GetPlayerController"
        """
        return "GetPlayerController"

    def execute(self, state_context: 'StateContext', player: 'Player') -> int:
        """执行 GetPlayerController native 函数。

        参数：
            state_context: 状态上下文
            player: 玩家对象

        返回：
            控制器类型整数（0=USER, 1=COMPUTER, 2=RESCUABLE, 3=NEUTRAL, 4=CREEP, 5=NONE）
        """
        if player is None:
            logger.warning("[GetPlayerController] 玩家对象为 None")
            return 0  # MAP_CONTROL_USER

        result = player.controller
        logger.info(f"[GetPlayerController] 玩家{player.player_id} 控制器类型: {result}")
        return result


class ConvertMapControl(NativeFunction):
    """将整数转换为控制器类型。

    在 Warcraft 3 中，这是一个类型转换函数，
    在我们的实现中直接返回传入的整数。
    """

    @property
    def name(self) -> str:
        return "ConvertMapControl"

    def execute(self, state_context: 'StateContext', control_type: int) -> int:
        """执行 ConvertMapControl。

        参数：
            state_context: 状态上下文
            control_type: 控制器类型整数

        返回：
            传入的控制器类型整数
        """
        logger.info(f"[ConvertMapControl] 转换控制器类型: {control_type}")
        return control_type
