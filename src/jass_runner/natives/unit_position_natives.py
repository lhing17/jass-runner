"""单位位置操作 native 函数实现。

此模块包含单位位置设置和修改的 native 函数。
"""

import logging
from .base import NativeFunction
from .handle import Unit
from .location import Location

logger = logging.getLogger(__name__)


class SetUnitPosition(NativeFunction):
    """设置单位位置（使用坐标）。"""

    @property
    def name(self) -> str:
        return "SetUnitPosition"

    def execute(self, state_context, unit: Unit, x: float, y: float):
        """执行 SetUnitPosition native 函数。

        参数：
            state_context: 状态上下文
            unit: 单位对象
            x: 新的 X 坐标
            y: 新的 Y 坐标
        """
        if unit is None:
            logger.warning("[SetUnitPosition] 尝试设置 None 单位的位置")
            return

        unit.x = float(x)
        unit.y = float(y)

        logger.debug(f"[SetUnitPosition] 单位 {unit.id} 位置设置为 ({x}, {y})")


class SetUnitPositionLoc(NativeFunction):
    """设置单位位置（使用 Location）。"""

    @property
    def name(self) -> str:
        return "SetUnitPositionLoc"

    def execute(self, state_context, unit: Unit, loc: Location):
        """执行 SetUnitPositionLoc native 函数。

        参数：
            state_context: 状态上下文
            unit: 单位对象
            loc: Location 位置对象
        """
        if unit is None:
            logger.warning("[SetUnitPositionLoc] 尝试设置 None 单位的位置")
            return

        if loc is None:
            logger.warning("[SetUnitPositionLoc] Location 为 None")
            return

        unit.x = loc.x
        unit.y = loc.y
        unit.z = loc.z

        logger.debug(f"[SetUnitPositionLoc] 单位 {unit.id} 位置设置为 ({loc.x}, {loc.y}, {loc.z})")
