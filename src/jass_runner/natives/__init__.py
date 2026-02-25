"""JASS native函数模块。

此模块包含JASS native函数的框架实现，支持插件式扩展。
"""

from .base import NativeFunction
from .registry import NativeRegistry

__all__ = ['NativeFunction', 'NativeRegistry']