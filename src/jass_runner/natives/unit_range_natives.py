"""单位范围检测Native函数实现。

包含单位距离检测相关函数。
"""

import logging
import math
from typing import Any, Optional

from .base import NativeFunction
from .handle import Unit
from .location import Location


logger = logging.getLogger(__name__)


class IsUnitInRangeXY(NativeFunction):
    """检查单位是否在指定坐标指定距离内。"""

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "IsUnitInRangeXY"

    def execute(self, which_unit: Optional[Unit], x: float, y: float, distance: float) -> bool:
        """执行范围检测。

        参数：
            which_unit: 要检查的单位
            x: 目标X坐标
            y: 目标Y坐标
            distance: 检测距离

        返回：
            如果单位在范围内返回True，否则返回False
        """
        if which_unit is None:
            return False

        # 负距离视为0
        if distance < 0:
            distance = 0

        dx = which_unit.x - x
        dy = which_unit.y - y
        actual_distance = math.sqrt(dx * dx + dy * dy)

        return actual_distance <= distance


class IsUnitInRangeLoc(NativeFunction):
    """检查单位是否在指定位置指定距离内。"""

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "IsUnitInRangeLoc"

    def execute(self, which_unit: Optional[Unit], which_location: Optional[Location], distance: float) -> bool:
        """执行范围检测。

        参数：
            which_unit: 要检查的单位
            which_location: 目标位置
            distance: 检测距离

        返回：
            如果单位在范围内返回True，否则返回False
        """
        if which_unit is None or which_location is None:
            return False

        # 负距离视为0
        if distance < 0:
            distance = 0

        dx = which_unit.x - which_location.x
        dy = which_unit.y - which_location.y
        actual_distance = math.sqrt(dx * dx + dy * dy)

        return actual_distance <= distance


class IsUnitInRange(NativeFunction):
    """检查单位是否在另一个单位指定距离内。"""

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "IsUnitInRange"

    def execute(self, which_unit: Optional[Unit], other_unit: Optional[Unit], distance: float) -> bool:
        """执行范围检测。

        参数：
            which_unit: 要检查的单位
            other_unit: 目标单位
            distance: 检测距离

        返回：
            如果单位在范围内返回True，否则返回False
        """
        if which_unit is None or other_unit is None:
            return False

        # 负距离视为0
        if distance < 0:
            distance = 0

        dx = which_unit.x - other_unit.x
        dy = which_unit.y - other_unit.y
        actual_distance = math.sqrt(dx * dx + dy * dy)

        return actual_distance <= distance
