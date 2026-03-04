"""Fog native 函数实现。

此模块包含战争迷雾相关的 native 函数。
"""

import logging
from typing import Any
from .base import NativeFunction


logger = logging.getLogger(__name__)


class FogState:
    """管理战争迷雾状态。"""

    def __init__(self):
        """初始化迷雾状态，默认为启用。"""
        self.mask_enabled = True
        self.fog_enabled = True


class FogMaskEnable(NativeFunction):
    """启用或禁用黑色遮罩。"""

    def __init__(self, fog_state: FogState):
        """初始化。

        参数：
            fog_state: 迷雾状态管理器
        """
        self._fog_state = fog_state

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "FogMaskEnable"
        """
        return "FogMaskEnable"

    def execute(self, state_context, enable: bool = None, *args, **kwargs) -> None:
        """执行函数。

        参数：
            state_context: 状态上下文
            enable: 是否启用黑色遮罩
            *args: 额外位置参数
            **kwargs: 关键字参数
        """
        if enable is None:
            enable = False
        self._fog_state.mask_enabled = enable
        status = "启用" if enable else "禁用"
        logger.info(f"[Fog] 黑色遮罩状态: {status}")


class FogEnable(NativeFunction):
    """启用或禁用战争迷雾。"""

    def __init__(self, fog_state: FogState):
        """初始化。

        参数：
            fog_state: 迷雾状态管理器
        """
        self._fog_state = fog_state

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "FogEnable"
        """
        return "FogEnable"

    def execute(self, state_context, enable: bool = None, *args, **kwargs) -> None:
        """执行函数。

        参数：
            state_context: 状态上下文
            enable: 是否启用战争迷雾
            *args: 额外位置参数
            **kwargs: 关键字参数
        """
        if enable is None:
            enable = False
        self._fog_state.fog_enabled = enable
        status = "启用" if enable else "禁用"
        logger.info(f"[Fog] 战争迷雾状态: {status}")


class IsFogMaskEnabled(NativeFunction):
    """查询黑色遮罩是否启用。"""

    def __init__(self, fog_state: FogState):
        """初始化。

        参数：
            fog_state: 迷雾状态管理器
        """
        self._fog_state = fog_state

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "IsFogMaskEnabled"
        """
        return "IsFogMaskEnabled"

    def execute(self, state_context, *args, **kwargs) -> bool:
        """执行函数。

        参数：
            state_context: 状态上下文
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            黑色遮罩是否启用
        """
        return self._fog_state.mask_enabled


class IsFogEnabled(NativeFunction):
    """查询战争迷雾是否启用。"""

    def __init__(self, fog_state: FogState):
        """初始化。

        参数：
            fog_state: 迷雾状态管理器
        """
        self._fog_state = fog_state

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "IsFogEnabled"
        """
        return "IsFogEnabled"

    def execute(self, state_context, *args, **kwargs) -> bool:
        """执行函数。

        参数：
            state_context: 状态上下文
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            战争迷雾是否启用
        """
        return self._fog_state.fog_enabled
