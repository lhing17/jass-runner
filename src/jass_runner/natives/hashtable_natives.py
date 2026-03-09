"""Hashtable 相关 Native 函数"""

import logging
from typing import Any, Optional

from .base import NativeFunction


logger = logging.getLogger(__name__)


class InitHashtable(NativeFunction):
    """初始化 hashtable 的 native 函数"""

    @property
    def name(self) -> str:
        return "InitHashtable"

    def execute(self, state_context, *args, **kwargs) -> Any:
        """执行 InitHashtable native 函数

        Returns:
            hashtable 对象，如果失败返回 None
        """
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[InitHashtable] state_context or handle_manager not found")
            return None

        hashtable = state_context.handle_manager.create_hashtable()
        logger.info(f"[InitHashtable] Created hashtable: {hashtable.id}")
        return hashtable


class SaveInteger(NativeFunction):
    """SaveInteger native 函数"""

    @property
    def name(self) -> str:
        return "SaveInteger"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, value: int, *args, **kwargs):
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[SaveInteger] state_context or handle_manager not found")
            return None

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[SaveInteger] Hashtable not found: {hashtable_id}")
            return None

        hashtable.save_integer(parent_key, child_key, value)
        logger.debug(f"[SaveInteger] Saved integer {value} at ({parent_key}, {child_key})")
        return None


class SaveReal(NativeFunction):
    """SaveReal native 函数"""

    @property
    def name(self) -> str:
        return "SaveReal"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, value: float, *args, **kwargs):
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[SaveReal] state_context or handle_manager not found")
            return None

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[SaveReal] Hashtable not found: {hashtable_id}")
            return None

        hashtable.save_real(parent_key, child_key, value)
        return None


class SaveBoolean(NativeFunction):
    """SaveBoolean native 函数"""

    @property
    def name(self) -> str:
        return "SaveBoolean"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, value: bool, *args, **kwargs):
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[SaveBoolean] state_context or handle_manager not found")
            return None

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[SaveBoolean] Hashtable not found: {hashtable_id}")
            return None

        hashtable.save_boolean(parent_key, child_key, value)
        return None


class SaveStr(NativeFunction):
    """SaveStr native 函数"""

    @property
    def name(self) -> str:
        return "SaveStr"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, value: str, *args, **kwargs) -> bool:
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[SaveStr] state_context or handle_manager not found")
            return False

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[SaveStr] Hashtable not found: {hashtable_id}")
            return False

        result = hashtable.save_string(parent_key, child_key, value)
        return result


class SaveUnitHandle(NativeFunction):
    """SaveUnitHandle native 函数"""

    @property
    def name(self) -> str:
        return "SaveUnitHandle"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, unit, *args, **kwargs) -> bool:
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[SaveUnitHandle] state_context or handle_manager not found")
            return False

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[SaveUnitHandle] Hashtable not found: {hashtable_id}")
            return False

        return hashtable.save_unit_handle(parent_key, child_key, unit)


class SaveItemHandle(NativeFunction):
    """SaveItemHandle native 函数"""

    @property
    def name(self) -> str:
        return "SaveItemHandle"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, item, *args, **kwargs) -> bool:
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[SaveItemHandle] state_context or handle_manager not found")
            return False

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[SaveItemHandle] Hashtable not found: {hashtable_id}")
            return False

        return hashtable.save_item_handle(parent_key, child_key, item)


class SavePlayerHandle(NativeFunction):
    """SavePlayerHandle native 函数"""

    @property
    def name(self) -> str:
        return "SavePlayerHandle"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, player, *args, **kwargs) -> bool:
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[SavePlayerHandle] state_context or handle_manager not found")
            return False

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[SavePlayerHandle] Hashtable not found: {hashtable_id}")
            return False

        return hashtable.save_player_handle(parent_key, child_key, player)
