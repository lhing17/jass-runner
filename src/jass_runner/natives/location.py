"""Location 位置类实现。

此模块包含 JASS location 类型的实现，用于管理游戏世界中的位置坐标。
"""


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
