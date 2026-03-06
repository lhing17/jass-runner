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


class AddPlayerTechResearched(NativeFunction):
    """增加玩家科技研究等级。"""

    @property
    def name(self) -> str:
        """获取native函数名称。

        返回：
            函数名称 "AddPlayerTechResearched"
        """
        return "AddPlayerTechResearched"

    def execute(self, state_context: 'StateContext', whichPlayer: 'Player',
                techid: int, levels: int) -> None:
        """执行AddPlayerTechResearched native函数。

        参数：
            state_context: 状态上下文
            whichPlayer: 玩家对象
            techid: 科技ID（FourCC格式）
            levels: 要增加的等级数
        """
        if whichPlayer is None:
            logger.warning("[AddPlayerTechResearched] 玩家对象为None")
            return None

        whichPlayer.add_tech_researched(techid, levels)
        new_level = whichPlayer.get_tech_count(techid, False)
        logger.info(f"[AddPlayerTechResearched] 玩家{whichPlayer.player_id} 科技{techid} 增加{levels}级，当前等级{new_level}")
        return None


class SetPlayerTechResearched(NativeFunction):
    """设置玩家科技研究等级。"""

    @property
    def name(self) -> str:
        """获取native函数名称。

        返回：
            函数名称 "SetPlayerTechResearched"
        """
        return "SetPlayerTechResearched"

    def execute(self, state_context: 'StateContext', whichPlayer: 'Player',
                techid: int, setToLevel: int) -> None:
        """执行SetPlayerTechResearched native函数。

        参数：
            state_context: 状态上下文
            whichPlayer: 玩家对象
            techid: 科技ID（FourCC格式）
            setToLevel: 要设置的等级
        """
        if whichPlayer is None:
            logger.warning("[SetPlayerTechResearched] 玩家对象为None")
            return None

        whichPlayer.set_tech_researched(techid, setToLevel)
        logger.info(f"[SetPlayerTechResearched] 玩家{whichPlayer.player_id} 科技{techid} 等级设为{setToLevel}")
        return None


class GetPlayerTechResearched(NativeFunction):
    """获取玩家科技是否已研究。"""

    @property
    def name(self) -> str:
        """获取native函数名称。

        返回：
            函数名称 "GetPlayerTechResearched"
        """
        return "GetPlayerTechResearched"

    def execute(self, state_context: 'StateContext', whichPlayer: 'Player',
                techid: int, specificonly: bool) -> bool:
        """执行GetPlayerTechResearched native函数。

        参数：
            state_context: 状态上下文
            whichPlayer: 玩家对象
            techid: 科技ID（FourCC格式）
            specificonly: 是否只检查特定科技（当前忽略）

        返回：
            等级大于0返回True，否则返回False
        """
        if whichPlayer is None:
            logger.warning("[GetPlayerTechResearched] 玩家对象为None")
            return False

        result = whichPlayer.get_tech_researched(techid, specificonly)
        logger.info(f"[GetPlayerTechResearched] 玩家{whichPlayer.player_id} 科技{techid} 已研究: {result}")
        return result
