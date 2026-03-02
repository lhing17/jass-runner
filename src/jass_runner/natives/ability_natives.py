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
