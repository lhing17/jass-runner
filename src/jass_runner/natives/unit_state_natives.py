"""单位状态Native函数实现。

此模块包含JASS单位状态相关native函数的实现。
"""

import logging
from typing import Optional
from .base import NativeFunction
from .handle import Unit

logger = logging.getLogger(__name__)


class GetWidgetLife(NativeFunction):
    """获取widget（单位/建筑）的生命值。

    对应JASS native函数: real GetWidgetLife(widget whichWidget)

    注意: 在JASS中widget是unit和destructable的基类。
    这里我们主要处理unit类型。
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "GetWidgetLife"

    def execute(self, state_context, widget) -> float:
        """执行GetWidgetLife native函数。

        参数：
            state_context: 状态上下文
            widget: widget对象（通常是unit）

        返回：
            当前生命值，如果widget为None返回0
        """
        if widget is None:
            return 0.0

        # 检查是否有life属性
        if hasattr(widget, 'life'):
            return float(widget.life)

        return 0.0


class SetWidgetLife(NativeFunction):
    """设置widget（单位/建筑）的生命值。

    对应JASS native函数: void SetWidgetLife(widget whichWidget, real newLife)

    注意: 如果设置为0或以下，单位会被杀死。
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "SetWidgetLife"

    def execute(self, state_context, widget, new_life: float):
        """执行SetWidgetLife native函数。

        参数：
            state_context: 状态上下文
            widget: widget对象（通常是unit）
            new_life: 新的生命值
        """
        if widget is None:
            logger.warning("[SetWidgetLife] widget为None")
            return

        if not hasattr(widget, 'life'):
            logger.warning("[SetWidgetLife] widget没有life属性")
            return

        widget.life = new_life

        # 如果生命值<=0，杀死单位
        if new_life <= 0:
            widget.destroy()
            logger.debug(f"[SetWidgetLife] widget {widget.id} 已被杀死")

        logger.debug(f"[SetWidgetLife] widget {widget.id} 生命值设置为 {new_life}")
