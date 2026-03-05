"""Rect native函数实现。

此模块包含JASS Rect相关native函数的实现：
- Rect: 创建矩形区域
- RemoveRect: 移除矩形区域
- GetRectCenterX: 获取矩形中心X坐标
- GetRectCenterY: 获取矩形中心Y坐标
- GetRectMinX: 获取矩形最小X坐标
- GetRectMinY: 获取矩形最小Y坐标
- GetRectMaxX: 获取矩形最大X坐标
- GetRectMaxY: 获取矩形最大Y坐标
"""

import logging
from .base import NativeFunction

logger = logging.getLogger(__name__)


class GetRectCenterX(NativeFunction):
    """获取矩形中心X坐标（JASS GetRectCenterX native函数）。"""

    @property
    def name(self) -> str:
        """获取native函数名称。

        返回：
            native函数名称字符串 "GetRectCenterX"
        """
        return "GetRectCenterX"

    def execute(self, state_context, rect):
        """执行GetRectCenterX native函数，获取矩形中心X坐标。

        参数：
            state_context: 状态上下文，提供对HandleManager的访问
            rect: Rect对象或rect handle

        返回：
            矩形中心X坐标，无效handle返回0.0
        """
        if rect is None:
            logger.warning("[GetRectCenterX] 传入的rect为None，返回0.0")
            return 0.0

        # 如果传入的是handle ID字符串，通过HandleManager获取Rect对象
        if isinstance(rect, str):
            handle_manager = state_context.handle_manager
            rect = handle_manager.get_rect(rect)
            if rect is None:
                logger.warning(f"[GetRectCenterX] 无效的rect handle ID，返回0.0")
                return 0.0

        # 计算中心X坐标
        center_x = (rect.min_x + rect.max_x) / 2.0
        logger.debug(f"[GetRectCenterX] 矩形 {rect.id} 中心X坐标: {center_x}")
        return center_x


class GetRectCenterY(NativeFunction):
    """获取矩形中心Y坐标（JASS GetRectCenterY native函数）。"""

    @property
    def name(self) -> str:
        """获取native函数名称。

        返回：
            native函数名称字符串 "GetRectCenterY"
        """
        return "GetRectCenterY"

    def execute(self, state_context, rect):
        """执行GetRectCenterY native函数，获取矩形中心Y坐标。

        参数：
            state_context: 状态上下文，提供对HandleManager的访问
            rect: Rect对象或rect handle

        返回：
            矩形中心Y坐标，无效handle返回0.0
        """
        if rect is None:
            logger.warning("[GetRectCenterY] 传入的rect为None，返回0.0")
            return 0.0

        # 如果传入的是handle ID字符串，通过HandleManager获取Rect对象
        if isinstance(rect, str):
            handle_manager = state_context.handle_manager
            rect = handle_manager.get_rect(rect)
            if rect is None:
                logger.warning(f"[GetRectCenterY] 无效的rect handle ID，返回0.0")
                return 0.0

        # 计算中心Y坐标
        center_y = (rect.min_y + rect.max_y) / 2.0
        logger.debug(f"[GetRectCenterY] 矩形 {rect.id} 中心Y坐标: {center_y}")
        return center_y


class GetRectMinX(NativeFunction):
    """获取矩形最小X坐标（JASS GetRectMinX native函数）。"""

    @property
    def name(self) -> str:
        """获取native函数名称。

        返回：
            native函数名称字符串 "GetRectMinX"
        """
        return "GetRectMinX"

    def execute(self, state_context, rect):
        """执行GetRectMinX native函数，获取矩形最小X坐标。

        参数：
            state_context: 状态上下文，提供对HandleManager的访问
            rect: Rect对象或rect handle

        返回：
            矩形最小X坐标，无效handle返回0.0
        """
        if rect is None:
            logger.warning("[GetRectMinX] 传入的rect为None，返回0.0")
            return 0.0

        # 如果传入的是handle ID字符串，通过HandleManager获取Rect对象
        if isinstance(rect, str):
            handle_manager = state_context.handle_manager
            rect = handle_manager.get_rect(rect)
            if rect is None:
                logger.warning(f"[GetRectMinX] 无效的rect handle ID，返回0.0")
                return 0.0

        logger.debug(f"[GetRectMinX] 矩形 {rect.id} 最小X坐标: {rect.min_x}")
        return rect.min_x


class GetRectMinY(NativeFunction):
    """获取矩形最小Y坐标（JASS GetRectMinY native函数）。"""

    @property
    def name(self) -> str:
        """获取native函数名称。

        返回：
            native函数名称字符串 "GetRectMinY"
        """
        return "GetRectMinY"

    def execute(self, state_context, rect):
        """执行GetRectMinY native函数，获取矩形最小Y坐标。

        参数：
            state_context: 状态上下文，提供对HandleManager的访问
            rect: Rect对象或rect handle

        返回：
            矩形最小Y坐标，无效handle返回0.0
        """
        if rect is None:
            logger.warning("[GetRectMinY] 传入的rect为None，返回0.0")
            return 0.0

        # 如果传入的是handle ID字符串，通过HandleManager获取Rect对象
        if isinstance(rect, str):
            handle_manager = state_context.handle_manager
            rect = handle_manager.get_rect(rect)
            if rect is None:
                logger.warning(f"[GetRectMinY] 无效的rect handle ID，返回0.0")
                return 0.0

        logger.debug(f"[GetRectMinY] 矩形 {rect.id} 最小Y坐标: {rect.min_y}")
        return rect.min_y


class GetRectMaxX(NativeFunction):
    """获取矩形最大X坐标（JASS GetRectMaxX native函数）。"""

    @property
    def name(self) -> str:
        """获取native函数名称。

        返回：
            native函数名称字符串 "GetRectMaxX"
        """
        return "GetRectMaxX"

    def execute(self, state_context, rect):
        """执行GetRectMaxX native函数，获取矩形最大X坐标。

        参数：
            state_context: 状态上下文，提供对HandleManager的访问
            rect: Rect对象或rect handle

        返回：
            矩形最大X坐标，无效handle返回0.0
        """
        if rect is None:
            logger.warning("[GetRectMaxX] 传入的rect为None，返回0.0")
            return 0.0

        # 如果传入的是handle ID字符串，通过HandleManager获取Rect对象
        if isinstance(rect, str):
            handle_manager = state_context.handle_manager
            rect = handle_manager.get_rect(rect)
            if rect is None:
                logger.warning(f"[GetRectMaxX] 无效的rect handle ID，返回0.0")
                return 0.0

        logger.debug(f"[GetRectMaxX] 矩形 {rect.id} 最大X坐标: {rect.max_x}")
        return rect.max_x


class GetRectMaxY(NativeFunction):
    """获取矩形最大Y坐标（JASS GetRectMaxY native函数）。"""

    @property
    def name(self) -> str:
        """获取native函数名称。

        返回：
            native函数名称字符串 "GetRectMaxY"
        """
        return "GetRectMaxY"

    def execute(self, state_context, rect):
        """执行GetRectMaxY native函数，获取矩形最大Y坐标。

        参数：
            state_context: 状态上下文，提供对HandleManager的访问
            rect: Rect对象或rect handle

        返回：
            矩形最大Y坐标，无效handle返回0.0
        """
        if rect is None:
            logger.warning("[GetRectMaxY] 传入的rect为None，返回0.0")
            return 0.0

        # 如果传入的是handle ID字符串，通过HandleManager获取Rect对象
        if isinstance(rect, str):
            handle_manager = state_context.handle_manager
            rect = handle_manager.get_rect(rect)
            if rect is None:
                logger.warning(f"[GetRectMaxY] 无效的rect handle ID，返回0.0")
                return 0.0

        logger.debug(f"[GetRectMaxY] 矩形 {rect.id} 最大Y坐标: {rect.max_y}")
        return rect.max_y


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
