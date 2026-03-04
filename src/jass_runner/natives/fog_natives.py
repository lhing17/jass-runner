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


class FogMaskEnable(NativeFunction):
    """启用或禁用黑色遮罩。"""

    name = "FogMaskEnable"
    parameters = ["boolean"]
    return_type = "nothing"

    def __init__(self, fog_state: FogState):
        """初始化。

        参数：
            fog_state: 迷雾状态管理器
        """
        self._fog_state = fog_state

    def execute(self, args: List[Any]) -> None:
        """执行函数。

        参数：
            args: [enable] - 是否启用黑色遮罩
        """
        enable = args[0]
        self._fog_state.mask_enabled = enable
        status = "启用" if enable else "禁用"
        print(f"[Fog] 黑色遮罩状态: {status}")


class FogEnable(NativeFunction):
    """启用或禁用战争迷雾。"""

    name = "FogEnable"
    parameters = ["boolean"]
    return_type = "nothing"

    def __init__(self, fog_state: FogState):
        """初始化。

        参数：
            fog_state: 迷雾状态管理器
        """
        self._fog_state = fog_state

    def execute(self, args: List[Any]) -> None:
        """执行函数。

        参数：
            args: [enable] - 是否启用战争迷雾
        """
        enable = args[0]
        self._fog_state.fog_enabled = enable
        status = "启用" if enable else "禁用"
        print(f"[Fog] 战争迷雾状态: {status}")
