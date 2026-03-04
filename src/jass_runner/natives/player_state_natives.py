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


class SetPlayerState(NativeFunction):
    """设置玩家状态。"""

    @property
    def name(self) -> str:
        """获取 native 函数名称。

        返回：
            函数名称 "SetPlayerState"
        """
        return "SetPlayerState"

    def execute(self, state_context: 'StateContext', player: 'Player',
                state_type: int, value: int) -> int:
        """执行 SetPlayerState native 函数。

        参数：
            state_context: 状态上下文
            player: 玩家对象
            state_type: 状态类型（PLAYER_STATE_RESOURCE_*）
            value: 要设置的值

        返回：
            实际设置的值（超出范围时自动截断）
        """
        if player is None:
            logger.warning("[SetPlayerState] 玩家对象为 None")
            return 0

        actual_value = player.set_state(state_type, value)
        logger.info(f"[SetPlayerState] 玩家{player.player_id} 设置状态{state_type}为{actual_value}（输入{value}）")
        return actual_value


class ConvertPlayerState(NativeFunction):
    """将整数转换为玩家状态类型。

    在 Warcraft 3 中，这是一个类型转换函数，
    在我们的实现中直接返回传入的整数。
    """

    @property
    def name(self) -> str:
        return "ConvertPlayerState"

    def execute(self, state_context: 'StateContext', player_state: int) -> int:
        """执行 ConvertPlayerState。

        参数：
            state_context: 状态上下文
            player_state: 玩家状态类型整数

        返回：
            传入的玩家状态类型整数
        """
        logger.info(f"[ConvertPlayerState] 转换玩家状态类型: {player_state}")
        return player_state
