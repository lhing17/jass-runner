"""Fog native 函数实现。

此模块包含战争迷雾相关的 native 函数。
"""

from typing import Any, List
from .base import NativeFunction


class FogState:
    """管理战争迷雾状态。"""

    def __init__(self):
        """初始化迷雾状态，默认为启用。"""
        self.mask_enabled = True
        self.fog_enabled = True
