"""玩家科技相关native函数实现。

此模块包含与玩家科技系统相关的JASS native函数。
"""

import logging
from typing import TYPE_CHECKING

from .base import NativeFunction

if TYPE_CHECKING:
    from .state import StateContext
    from .player import Player

logger = logging.getLogger(__name__)


class SetPlayerTechMaxAllowed(NativeFunction):
    """设置玩家科技最大允许等级。"""

    @property
    def name(self) -> str:
        """获取native函数名称。

        返回：
            函数名称 "SetPlayerTechMaxAllowed"
        """
        return "SetPlayerTechMaxAllowed"

    def execute(self, state_context: 'StateContext', whichPlayer: 'Player',
                techid: int, maximum: int) -> None:
        """执行SetPlayerTechMaxAllowed native函数。

        参数：
            state_context: 状态上下文
            whichPlayer: 玩家对象
            techid: 科技ID（FourCC格式）
            maximum: 最大允许等级
        """
        if whichPlayer is None:
            logger.warning("[SetPlayerTechMaxAllowed] 玩家对象为None")
            return None

        whichPlayer.set_tech_max_allowed(techid, maximum)
        logger.info(f"[SetPlayerTechMaxAllowed] 玩家{whichPlayer.player_id} 科技{techid} 最大等级设为{maximum}")
        return None


class GetPlayerTechMaxAllowed(NativeFunction):
    """获取玩家科技最大允许等级。"""

    @property
    def name(self) -> str:
        """获取native函数名称。

        返回：
            函数名称 "GetPlayerTechMaxAllowed"
        """
        return "GetPlayerTechMaxAllowed"

    def execute(self, state_context: 'StateContext', whichPlayer: 'Player',
                techid: int) -> int:
        """执行GetPlayerTechMaxAllowed native函数。

        参数：
            state_context: 状态上下文
            whichPlayer: 玩家对象
            techid: 科技ID（FourCC格式）

        返回：
            最大允许等级，未设置或玩家为None返回0
        """
        if whichPlayer is None:
            logger.warning("[GetPlayerTechMaxAllowed] 玩家对象为None")
            return 0

        result = whichPlayer.get_tech_max_allowed(techid)
        logger.info(f"[GetPlayerTechMaxAllowed] 玩家{whichPlayer.player_id} 科技{techid} 最大等级为{result}")
        return result
