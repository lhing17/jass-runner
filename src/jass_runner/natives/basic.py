"""基础native函数实现。

此模块包含JASS基础native函数的实现，如DisplayTextToPlayer等。
"""

import logging
from .base import NativeFunction
from .handle import Unit
from ..utils import int_to_fourcc


logger = logging.getLogger(__name__)

# 单位状态常量
UNIT_STATE_LIFE = 0
UNIT_STATE_MAX_LIFE = 1
UNIT_STATE_MANA = 2
UNIT_STATE_MAX_MANA = 3


class DisplayTextToPlayer(NativeFunction):
    """向玩家显示文本（通过控制台输出模拟）。

    此函数模拟JASS中的DisplayTextToPlayer native函数，将文本消息输出到日志。
    """

    @property
    def name(self) -> str:
        """获取函数名称。

        返回：
            函数名称"DisplayTextToPlayer"
        """
        return "DisplayTextToPlayer"

    def execute(self, state_context, player: int, x: float, y: float, message: str):
        """执行DisplayTextToPlayer native函数。

        参数：
            state_context: 状态上下文
            player: 玩家ID
            x: X坐标（游戏中未使用，仅保持接口兼容）
            y: Y坐标（游戏中未使用，仅保持接口兼容）
            message: 要显示的文本消息

        返回：
            None
        """
        logger.info(f"[DisplayTextToPlayer]玩家{player}: {message}")
        return None


class KillUnit(NativeFunction):
    """杀死一个单位（通过状态管理系统）。

    此函数模拟JASS中的KillUnit native函数，通过HandleManager真正销毁单位。
    """

    @property
    def name(self) -> str:
        """获取函数名称。

        返回：
            函数名称"KillUnit"
        """
        return "KillUnit"

    def execute(self, state_context, unit: Unit):
        """执行KillUnit native函数。

        参数：
            state_context: 状态上下文
            unit: Unit对象（由CreateUnit返回）

        返回：
            bool: 成功杀死单位返回True，否则返回False
        """
        if unit is None:
            logger.warning("[KillUnit]尝试击杀None单位")
            return False

        # 通过HandleManager销毁单位
        handle_manager = state_context.handle_manager
        success = handle_manager.destroy_handle(unit.id)

        if success:
            logger.info(f"[KillUnit] 单位{unit.id}已被击杀")
        else:
            logger.warning(f"[KillUnit] 单位{unit.id}不存在或已被销毁")

        return success


class CreateUnit(NativeFunction):
    """创建一个单位（通过状态管理系统）。

    此函数模拟JASS中的CreateUnit native函数，通过HandleManager真正创建单位。
    """

    @property
    def name(self) -> str:
        """获取函数名称。

        返回：
            函数名称"CreateUnit"
        """
        return "CreateUnit"

    def execute(self, state_context, player: int, unit_type: int,
                x: float, y: float, facing: float) -> Unit:
        """执行CreateUnit native函数。

        参数：
            state_context: 状态上下文
            player: 玩家ID
            unit_type: 单位类型代码（fourcc整数格式，如1213484355代表'hfoo'）
            x: X坐标
            y: Y坐标
            facing: 面向角度

        返回：
            Unit: 生成的Unit对象
        """
        # 将fourcc整数转换为字符串（如1213484355 -> 'hfoo'）
        unit_type_str = int_to_fourcc(unit_type)

        # 通过HandleManager创建单位
        handle_manager = state_context.handle_manager
        unit = handle_manager.create_unit(unit_type_str, player, x, y, facing)

        logger.info(f"[CreateUnit] 为玩家{player}在({x}, {y})创建{unit_type_str}，单位ID: {unit.id}")
        return unit


class GetUnitState(NativeFunction):
    """获取单位状态（通过状态管理系统）。

    此函数模拟JASS中的GetUnitState native函数，从HandleManager查询真实单位状态。
    """

    @property
    def name(self) -> str:
        """获取函数名称。

        返回：
            函数名称"GetUnitState"
        """
        return "GetUnitState"

    def execute(self, state_context, unit: Unit, state_type: int) -> float:
        """执行GetUnitState native函数。

        参数：
            state_context: 状态上下文
            unit: Unit对象（由CreateUnit返回）
            state_type: 状态类型常量（如UNIT_STATE_LIFE=0表示生命值）

        返回：
            float: 单位状态值
        """
        if unit is None:
            return 0.0

        # 将整数状态类型转换为字符串
        state_map = {
            UNIT_STATE_LIFE: "UNIT_STATE_LIFE",
            UNIT_STATE_MAX_LIFE: "UNIT_STATE_MAX_LIFE",
            UNIT_STATE_MANA: "UNIT_STATE_MANA",
            UNIT_STATE_MAX_MANA: "UNIT_STATE_MAX_MANA",
        }

        state_str = state_map.get(state_type)
        if state_str is None:
            logger.warning(f"[GetUnitState] 未知状态类型: {state_type}")
            return 0.0

        # 通过HandleManager查询单位状态
        handle_manager = state_context.handle_manager
        value = handle_manager.get_unit_state(unit.id, state_str)

        return value
