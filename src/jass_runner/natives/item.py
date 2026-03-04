"""JASS Item物品类。

此模块包含JASS物品handle的实现。
"""

from .handle_base import Handle


class Item(Handle):
    """物品handle。

    属性：
        item_type: 物品类型代码（如'ratf'代表攻击之爪）
        x, y: 位置坐标
    """

    def __init__(self, handle_id: str, item_type: str, x: float, y: float):
        super().__init__(handle_id, "item")
        self.item_type = item_type
        self.x = x
        self.y = y
