"""单位所有权Native函数实现。

此模块包含JASS单位所有权相关native函数的实现。
"""

import logging
from .base import NativeFunction

logger = logging.getLogger(__name__)


class IsUnitOwnedByPlayer(NativeFunction):
    """检查单位是否被指定玩家拥有。

    对应JASS native函数: boolean IsUnitOwnedByPlayer(unit whichUnit, player whichPlayer)
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "IsUnitOwnedByPlayer"

    def execute(self, state_context, unit, player) -> bool:
        """执行IsUnitOwnedByPlayer native函数。

        参数：
            state_context: 状态上下文
            unit: 单位对象
            player: 玩家对象

        返回：
            单位被该玩家拥有返回True，否则返回False
        """
        if unit is None:
            return False

        if player is None:
            return False

        # 获取单位的玩家ID和玩家的玩家ID
        unit_player_id = getattr(unit, 'player_id', None)
        player_id = getattr(player, 'player_id', None)

        if unit_player_id is None or player_id is None:
            return False

        return unit_player_id == player_id
