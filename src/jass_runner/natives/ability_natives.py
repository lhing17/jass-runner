"""技能系统Native函数实现。

此模块包含JASS技能相关native函数的实现。
"""

import logging
from .base import NativeFunction
from .handle import Unit

logger = logging.getLogger(__name__)


class UnitAddAbility(NativeFunction):
    """给单位添加技能。

    对应JASS native函数: boolean UnitAddAbility(unit whichUnit, integer abilityId)
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "UnitAddAbility"

    def execute(self, state_context, unit: Unit, ability_id: int) -> bool:
        """执行UnitAddAbility native函数。

        参数：
            state_context: 状态上下文
            unit: 目标单位
            ability_id: 技能ID（fourcc整数）

        返回：
            添加成功返回True，否则返回False
        """
        if unit is None:
            logger.warning("[UnitAddAbility] 单位为None")
            return False

        if not isinstance(unit, Unit):
            logger.warning("[UnitAddAbility] 参数类型错误")
            return False

        result = unit.add_ability(ability_id)

        if result:
            logger.info(f"[UnitAddAbility] 单位{unit.id}添加技能{ability_id}")
        else:
            logger.debug(f"[UnitAddAbility] 单位{unit.id}已拥有技能{ability_id}")

        return result


class UnitRemoveAbility(NativeFunction):
    """从单位移除技能。

    对应JASS native函数: boolean UnitRemoveAbility(unit whichUnit, integer abilityId)
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "UnitRemoveAbility"

    def execute(self, state_context, unit: Unit, ability_id: int) -> bool:
        """执行UnitRemoveAbility native函数。

        参数：
            state_context: 状态上下文
            unit: 目标单位
            ability_id: 技能ID

        返回：
            移除成功返回True，否则返回False
        """
        if unit is None:
            logger.warning("[UnitRemoveAbility] 单位为None")
            return False

        if not isinstance(unit, Unit):
            logger.warning("[UnitRemoveAbility] 参数类型错误")
            return False

        result = unit.remove_ability(ability_id)

        if result:
            logger.info(f"[UnitRemoveAbility] 单位{unit.id}移除技能{ability_id}")
        else:
            logger.debug(f"[UnitRemoveAbility] 单位{unit.id}没有技能{ability_id}")

        return result


class GetUnitAbilityLevel(NativeFunction):
    """获取单位技能等级。

    对应JASS native函数: integer GetUnitAbilityLevel(unit whichUnit, integer abilityId)
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "GetUnitAbilityLevel"

    def execute(self, state_context, unit: Unit, ability_id: int) -> int:
        """执行GetUnitAbilityLevel native函数。

        参数：
            state_context: 状态上下文
            unit: 目标单位
            ability_id: 技能ID

        返回：
            技能等级，单位不存在或技能不存在返回0
        """
        if unit is None:
            return 0

        if not isinstance(unit, Unit):
            return 0

        level = unit.get_ability_level(ability_id)
        return level


class SetUnitAbilityLevel(NativeFunction):
    """设置单位技能等级。

    对应JASS native函数: boolean SetUnitAbilityLevel(unit whichUnit, integer abilityId, integer level)
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "SetUnitAbilityLevel"

    def execute(self, state_context, unit: Unit, ability_id: int, level: int) -> bool:
        """执行SetUnitAbilityLevel native函数。

        参数：
            state_context: 状态上下文
            unit: 目标单位
            ability_id: 技能ID
            level: 新等级

        返回：
            设置成功返回True，否则返回False
        """
        if unit is None:
            logger.warning("[SetUnitAbilityLevel] 单位为None")
            return False

        if not isinstance(unit, Unit):
            logger.warning("[SetUnitAbilityLevel] 参数类型错误")
            return False

        result = unit.set_ability_level(ability_id, level)

        if result:
            logger.info(f"[SetUnitAbilityLevel] 单位{unit.id}技能{ability_id}等级设为{level}")

        return result
