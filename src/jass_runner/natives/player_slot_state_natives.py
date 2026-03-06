"""玩家插槽状态相关 native 函数实现。

此模块包含与玩家插槽状态相关的 JASS native 函数。
"""

import logging
from typing import TYPE_CHECKING

from .base import NativeFunction

if TYPE_CHECKING:
    from .state import StateContext
    from .handle import Player

logger = logging.getLogger(__name__)


class GetPlayerSlotState(NativeFunction):
    """获取玩家插槽状态。"""

    @property
    def name(self) -> str:
        """获取 native 函数名称。

        返回：
            函数名称 "GetPlayerSlotState"
        """
        return "GetPlayerSlotState"

    def execute(self, state_context: 'StateContext', player: 'Player') -> int:
        """执行 GetPlayerSlotState native 函数。

        参数：
            state_context: 状态上下文
            player: 玩家对象

        返回：
            插槽状态整数（0=EMPTY, 1=PLAYING, 2=LEFT）
        """
        if player is None:
            logger.warning("[GetPlayerSlotState] 玩家对象为 None")
            return 0  # PLAYER_SLOT_STATE_EMPTY

        result = player.slot_state
        logger.info(f"[GetPlayerSlotState] 玩家{player.player_id} 插槽状态: {result}")
        return result


class ConvertPlayerSlotState(NativeFunction):
    """将整数转换为插槽状态类型。

    在 Warcraft 3 中，这是一个类型转换函数，
    在我们的实现中直接返回传入的整数。
    """

    @property
    def name(self) -> str:
        return "ConvertPlayerSlotState"

    def execute(self, state_context: 'StateContext', slot_state: int) -> int:
        """执行 ConvertPlayerSlotState。

        参数：
            state_context: 状态上下文
            slot_state: 插槽状态整数

        返回：
            传入的插槽状态整数
        """
        logger.info(f"[ConvertPlayerSlotState] 转换插槽状态: {slot_state}")
        return slot_state
