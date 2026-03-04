"""JASS handle类体系。

此模块包含所有JASS handle的基类和具体实现。

注意：此模块现在作为兼容性入口点，各handle类已拆分到独立模块。
"""

# 从各模块导入handle类，保持向后兼容
from .handle_base import Handle
from .unit import Unit
from .player import Player
from .item import Item
from .group import Group
from .rect import Rect
from .effect import Effect
from .force import Force
from .boolexpr import BoolExpr, ConditionFunc, FilterFunc, AndExpr, OrExpr, NotExpr

__all__ = [
    "Handle",
    "Unit",
    "Player",
    "Item",
    "Group",
    "Rect",
    "Effect",
    "Force",
    "BoolExpr",
    "ConditionFunc",
    "FilterFunc",
    "AndExpr",
    "OrExpr",
    "NotExpr",
]
