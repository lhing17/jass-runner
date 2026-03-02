"""Location 位置类实现。

此模块包含 JASS location 类型的实现，用于管理游戏世界中的位置坐标。
"""

import logging
from .base import NativeFunction

logger = logging.getLogger(__name__)


class Location:
    """位置类，包含 x, y, z 坐标。

    属性：
        x: X 坐标（水平方向）
        y: Y 坐标（垂直方向）
        z: Z 坐标（高度），默认为 0
    """

    def __init__(self, x: float, y: float, z: float = 0.0):
        """初始化位置对象。

        参数：
            x: X 坐标
            y: Y 坐标
            z: Z 坐标（高度，默认为 0）
        """
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __repr__(self) -> str:
        """返回位置的字符串表示。"""
        return f"Location({self.x}, {self.y}, {self.z})"


class LocationConstructor(NativeFunction):
    """创建 Location 对象（JASS Location native 函数）。"""

    @property
    def name(self) -> str:
        return "Location"

    def execute(self, state_context, x: float, y: float):
        """执行 Location native 函数。

        参数：
            state_context: 状态上下文
            x: X 坐标
            y: Y 坐标

        返回：
            Location: 新创建的 Location 对象
        """
        loc = Location(x, y)
        logger.debug(f"[Location] 创建位置: ({x}, {y})")
        return loc


class RemoveLocation(NativeFunction):
    """移除 Location 对象（JASS RemoveLocation native 函数）。"""

    @property
    def name(self) -> str:
        return "RemoveLocation"

    def execute(self, state_context, loc):
        """执行 RemoveLocation native 函数。

        参数：
            state_context: 状态上下文
            loc: Location 对象

        返回：
            None
        """
        if loc is None:
            logger.warning("[RemoveLocation] 尝试移除 None 位置")
            return

        logger.debug(f"[RemoveLocation] 移除位置: {loc}")
        # Location 对象不需要特殊清理，Python 垃圾回收会自动处理
