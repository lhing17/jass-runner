"""单位状态Native函数实现。

此模块包含JASS单位状态相关native函数的实现。
"""

import logging
from typing import Optional
from .base import NativeFunction
from .handle import Unit

logger = logging.getLogger(__name__)


class GetWidgetLife(NativeFunction):
    """获取widget（单位/建筑）的生命值。

    对应JASS native函数: real GetWidgetLife(widget whichWidget)

    注意: 在JASS中widget是unit和destructable的基类。
    这里我们主要处理unit类型。
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "GetWidgetLife"

    def execute(self, state_context, widget) -> float:
        """执行GetWidgetLife native函数。

        参数：
            state_context: 状态上下文
            widget: widget对象（通常是unit）

        返回：
            当前生命值，如果widget为None返回0
        """
        if widget is None:
            return 0.0

        # 检查是否有life属性
        if hasattr(widget, 'life'):
            return float(widget.life)

        return 0.0


class SetWidgetLife(NativeFunction):
    """设置widget（单位/建筑）的生命值。

    对应JASS native函数: void SetWidgetLife(widget whichWidget, real newLife)

    注意: 如果设置为0或以下，单位会被杀死。
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "SetWidgetLife"

    def execute(self, state_context, widget, new_life: float):
        """执行SetWidgetLife native函数。

        参数：
            state_context: 状态上下文
            widget: widget对象（通常是unit）
            new_life: 新的生命值
        """
        if widget is None:
            logger.warning("[SetWidgetLife] widget为None")
            return

        if not hasattr(widget, 'life'):
            logger.warning("[SetWidgetLife] widget没有life属性")
            return

        widget.life = new_life

        # 如果生命值<=0，杀死单位
        if new_life <= 0:
            widget.destroy()
            logger.debug(f"[SetWidgetLife] widget {widget.id} 已被杀死")

        logger.debug(f"[SetWidgetLife] widget {widget.id} 生命值设置为 {new_life}")


class UnitDamageTarget(NativeFunction):
    """让单位对目标造成伤害。

    对应JASS native函数: boolean UnitDamageTarget(unit whichUnit, widget target, real amount, boolean attack, boolean ranged, attacktype attackType, damagetype damageType, weapontype weaponType)

    注意: 这是一个简化实现，忽略攻击类型参数。
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "UnitDamageTarget"

    def execute(self, state_context, attacker, target, amount: float,
                attack: bool = True, ranged: bool = False,
                attack_type: int = 0, damage_type: int = 0,
                weapon_type: int = 0) -> bool:
        """执行UnitDamageTarget native函数。

        参数：
            state_context: 状态上下文
            attacker: 攻击单位
            target: 目标widget
            amount: 伤害数值
            attack: 是否为攻击伤害
            ranged: 是否为远程伤害
            attack_type: 攻击类型（简化实现中忽略）
            damage_type: 伤害类型（简化实现中忽略）
            weapon_type: 武器类型（简化实现中忽略）

        返回：
            伤害成功返回True
        """
        if attacker is None or target is None:
            logger.warning("[UnitDamageTarget] 攻击者或目标为None")
            return False

        if not hasattr(target, 'life'):
            logger.warning("[UnitDamageTarget] 目标没有life属性")
            return False

        # 应用伤害
        target.life -= amount

        # 如果生命值<=0，杀死目标
        if target.life <= 0:
            target.destroy()
            logger.info(f"[UnitDamageTarget] 目标 {target.id} 被 {attacker.id} 杀死")
        else:
            logger.debug(f"[UnitDamageTarget] {attacker.id} 对 {target.id} 造成 {amount} 点伤害")

        return True


class GetUnitLevel(NativeFunction):
    """获取单位等级。

    对应JASS native函数: integer GetUnitLevel(unit whichUnit)
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "GetUnitLevel"

    def execute(self, state_context, unit) -> int:
        """执行GetUnitLevel native函数。

        参数：
            state_context: 状态上下文
            unit: 单位对象

        返回：
            单位等级，如果单位为None返回0
        """
        if unit is None:
            return 0

        if hasattr(unit, 'level'):
            return int(unit.level)

        return 0
