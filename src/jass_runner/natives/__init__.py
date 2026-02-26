"""JASS native函数框架。

此包包含JASS native函数的模拟实现和状态管理系统。
"""

from .base import NativeFunction
from .registry import NativeRegistry
from .factory import NativeFactory
from .handle import Handle, Unit
from .manager import HandleManager
from .state import StateContext

__all__ = [
    "NativeFunction",
    "NativeRegistry",
    "NativeFactory",
    "Handle",
    "Unit",
    "HandleManager",
    "StateContext",
]