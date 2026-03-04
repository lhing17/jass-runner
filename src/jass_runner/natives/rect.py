"""JASS Rect矩形区域类。

此模块包含JASS矩形区域handle的实现。
"""

from .handle_base import Handle


class Rect(Handle):
    """矩形区域handle。

    属性：
        min_x: 最小X坐标（左边界）
        min_y: 最小Y坐标（下边界）
        max_x: 最大X坐标（右边界）
        max_y: 最大Y坐标（上边界）
    """

    def __init__(self, rect_id: str, min_x: float, min_y: float,
                 max_x: float, max_y: float):
        """初始化矩形区域。

        参数：
            rect_id: 矩形ID
            min_x: 最小X坐标
            min_y: 最小Y坐标
            max_x: 最大X坐标
            max_y: 最大Y坐标
        """
        super().__init__(rect_id, "rect")
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

    def contains(self, x: float, y: float) -> bool:
        """检查点是否在矩形内。

        参数：
            x: X坐标
            y: Y坐标

        返回：
            点在矩形内返回True
        """
        return (self.min_x <= x <= self.max_x and
                self.min_y <= y <= self.max_y)
