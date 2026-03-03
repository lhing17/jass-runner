"""单位所有权Native函数实现。

此模块包含JASS单位所有权相关native函数的实现。
"""

import logging
from typing import Optional
from .base import NativeFunction
from .handle import Unit, Player

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


class SetUnitOwner(NativeFunction):
    """设置单位所属玩家。

    对应JASS native函数: nothing SetUnitOwner(unit whichUnit, player whichPlayer, boolean changeColor)
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "SetUnitOwner"

    def execute(self, state_context, which_unit: Optional[Unit], which_player: Optional[Player], change_color: bool) -> None:
        """执行单位所有权变更。

        参数：
            state_context: 状态上下文
            which_unit: 要变更所有者的单位
            which_player: 新所有者玩家
            change_color: 是否改变单位颜色

        返回：
            None
        """
        if which_unit is None or which_player is None:
            return

        old_owner = which_unit.player_id
        which_unit.player_id = which_player.player_id

        if change_color:
            # 改变单位颜色（通过颜色ID）
            which_unit.color = which_player.color
            logger.info(f"单位 {which_unit.name} (ID:{which_unit.id}) 所有权从玩家 {old_owner} 变更为玩家 {which_player.player_id} (颜色已改变)")
        else:
            logger.info(f"单位 {which_unit.name} (ID:{which_unit.id}) 所有权从玩家 {old_owner} 变更为玩家 {which_player.player_id}")
