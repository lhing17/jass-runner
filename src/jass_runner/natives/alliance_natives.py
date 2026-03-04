"""联盟相关 native 函数实现。

此模块包含 SetPlayerAlliance、GetPlayerAlliance 和 ConvertAllianceType
等联盟系统相关的 native 函数。
"""

import logging
from typing import TYPE_CHECKING

from .base import NativeFunction
from .alliance import get_alliance_name

if TYPE_CHECKING:
    from .manager import StateContext
    from .handle import Player

logger = logging.getLogger(__name__)


class ConvertAllianceType(NativeFunction):
    """将整数转换为联盟类型。

    在 Warcraft 3 中，这是一个类型转换函数，
    在我们的实现中直接返回传入的整数。
    """

    @property
    def name(self) -> str:
        return "ConvertAllianceType"

    def execute(self, state_context: 'StateContext',
                alliance_type: int) -> int:
        """执行 ConvertAllianceType。

        参数：
            state_context: 状态上下文
            alliance_type: 联盟类型整数

        返回：
            传入的联盟类型整数
        """
        logger.info(f"[ConvertAllianceType] 转换联盟类型: {alliance_type}")
        return alliance_type


class SetPlayerAlliance(NativeFunction):
    """设置两个玩家之间的联盟关系。"""

    @property
    def name(self) -> str:
        return "SetPlayerAlliance"

    def execute(self, state_context: 'StateContext',
                source_player: 'Player', other_player: 'Player',
                alliance_type: int, value: bool) -> None:
        """执行 SetPlayerAlliance。

        参数：
            state_context: 状态上下文
            source_player: 源玩家
            other_player: 目标玩家
            alliance_type: 联盟类型
            value: True 启用，False 禁用
        """
        if source_player is None or other_player is None:
            logger.warning("[SetPlayerAlliance] 玩家对象为 None")
            return

        alliance_manager = state_context.alliance_manager
        alliance_name = get_alliance_name(alliance_type)

        alliance_manager.set_alliance(
            source_player.player_id,
            other_player.player_id,
            alliance_type,
            value
        )

        logger.info(
            f"[SetPlayerAlliance] 玩家{source_player.player_id} 对 "
            f"玩家{other_player.player_id} 设置 {alliance_name}={value}"
        )


class GetPlayerAlliance(NativeFunction):
    """获取两个玩家之间的联盟关系状态。"""

    @property
    def name(self) -> str:
        return "GetPlayerAlliance"

    def execute(self, state_context: 'StateContext',
                source_player: 'Player', other_player: 'Player',
                alliance_type: int) -> bool:
        """执行 GetPlayerAlliance。

        参数：
            state_context: 状态上下文
            source_player: 源玩家
            other_player: 目标玩家
            alliance_type: 联盟类型

        返回：
            该联盟类型是否启用
        """
        if source_player is None or other_player is None:
            logger.warning("[GetPlayerAlliance] 玩家对象为 None")
            return False

        alliance_manager = state_context.alliance_manager
        alliance_name = get_alliance_name(alliance_type)

        result = alliance_manager.get_alliance(
            source_player.player_id,
            other_player.player_id,
            alliance_type
        )

        logger.info(
            f"[GetPlayerAlliance] 玩家{source_player.player_id} 对 "
            f"玩家{other_player.player_id} 的 {alliance_name}={result}"
        )

        return result
