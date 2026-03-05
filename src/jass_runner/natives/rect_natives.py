"""Rect native函数实现。

此模块包含JASS Rect相关native函数的实现：
- Rect: 创建矩形区域
- RemoveRect: 移除矩形区域
"""

import logging
from .base import NativeFunction

logger = logging.getLogger(__name__)


class RectNative(NativeFunction):
    """创建矩形区域（JASS Rect native函数）。"""

    @property
    def name(self) -> str:
        """获取native函数名称。

        返回：
            native函数名称字符串 "Rect"
        """
        return "Rect"

    def execute(self, state_context, min_x: float, min_y: float,
                max_x: float, max_y: float):
        """执行Rect native函数，创建矩形区域。

        参数：
            state_context: 状态上下文，提供对HandleManager的访问
            min_x: 最小X坐标（左边界）
            min_y: 最小Y坐标（下边界）
            max_x: 最大X坐标（右边界）
            max_y: 最大Y坐标（上边界）

        返回：
            新创建的Rect对象
        """
        handle_manager = state_context.handle_manager
        rect = handle_manager.create_rect(min_x, min_y, max_x, max_y)
        logger.debug(f"[Rect] 创建矩形区域: ({min_x}, {min_y}) - ({max_x}, {max_y}), ID={rect.id}")
        return rect


class RemoveRect(NativeFunction):
    """移除矩形区域（JASS RemoveRect native函数）。"""

    @property
    def name(self) -> str:
        """获取native函数名称。

        返回：
            native函数名称字符串 "RemoveRect"
        """
        return "RemoveRect"

    def execute(self, state_context, rect):
        """执行RemoveRect native函数，移除矩形区域。

        参数：
            state_context: 状态上下文，提供对HandleManager的访问
            rect: 要移除的Rect对象

        返回：
            None
        """
        if rect is None:
            logger.warning("[RemoveRect] 尝试移除 None 矩形区域")
            return

        handle_manager = state_context.handle_manager
        handle_manager.destroy_handle(rect.id)
        logger.debug(f"[RemoveRect] 移除矩形区域: {rect.id}")
