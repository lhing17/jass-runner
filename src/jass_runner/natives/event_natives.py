"""事件类型转换 native 函数。

此模块包含将整数转换为事件类型 handle 的 native 函数。
"""

import logging
from .base import NativeFunction


logger = logging.getLogger(__name__)


class ConvertPlayerUnitEvent(NativeFunction):
    """将整数转换为 playerunitevent handle。"""

    @property
    def name(self) -> str:
        return "ConvertPlayerUnitEvent"

    def execute(self, state_context, event_id: int):
        handle_manager = state_context.handle_manager
        event = handle_manager.create_playerunit_event(event_id)
        logger.debug(f"[ConvertPlayerUnitEvent] 创建事件 handle: {event.id}, event_id: {event_id}")
        return event


class ConvertPlayerEvent(NativeFunction):
    """将整数转换为 playerevent handle。"""

    @property
    def name(self) -> str:
        return "ConvertPlayerEvent"

    def execute(self, state_context, event_id: int):
        handle_manager = state_context.handle_manager
        event = handle_manager.create_playerevent(event_id)
        logger.debug(f"[ConvertPlayerEvent] 创建事件 handle: {event.id}, event_id: {event_id}")
        return event


class ConvertGameEvent(NativeFunction):
    """将整数转换为 gameevent handle。"""

    @property
    def name(self) -> str:
        return "ConvertGameEvent"

    def execute(self, state_context, event_id: int):
        handle_manager = state_context.handle_manager
        event = handle_manager.create_gameevent(event_id)
        logger.debug(f"[ConvertGameEvent] 创建事件 handle: {event.id}, event_id: {event_id}")
        return event


class ConvertUnitEvent(NativeFunction):
    """将整数转换为 unitevent handle。"""

    @property
    def name(self) -> str:
        return "ConvertUnitEvent"

    def execute(self, state_context, event_id: int):
        handle_manager = state_context.handle_manager
        event = handle_manager.create_unitevent(event_id)
        logger.debug(f"[ConvertUnitEvent] 创建事件 handle: {event.id}, event_id: {event_id}")
        return event
