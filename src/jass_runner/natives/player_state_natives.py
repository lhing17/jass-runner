"""玩家资源相关 native 函数实现。

此模块包含与玩家资源状态相关的 JASS native 函数。
"""

import logging
from typing import TYPE_CHECKING

from .base import NativeFunction

if TYPE_CHECKING:
    from .state import StateContext
    from .handle import Player

logger = logging.getLogger(__name__)


class GetPlayerState(NativeFunction):
    """获取玩家状态。"""

    @property
    def name(self) -> str:
        """获取 native 函数名称。

        返回：
            函数名称 "GetPlayerState"
        """
        return "GetPlayerState"

    def execute(self, state_context: 'StateContext', player: 'Player',
                state_type: int) -> int:
        """执行 GetPlayerState native 函数。

        参数：
            state_context: 状态上下文
            player: 玩家对象
            state_type: 状态类型（PLAYER_STATE_RESOURCE_*）

        返回：
            玩家状态值
        """
        if player is None:
            logger.warning("[GetPlayerState] 玩家对象为 None")
            return 0

        result = player.get_state(state_type)
        logger.info(f"[GetPlayerState] 玩家{player.player_id} 状态{state_type}: {result}")
        return result
