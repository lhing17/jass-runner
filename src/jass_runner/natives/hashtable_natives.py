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


class LoadInteger(NativeFunction):
    """LoadInteger native 函数"""

    @property
    def name(self) -> str:
        return "LoadInteger"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, *args, **kwargs) -> int:
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[LoadInteger] state_context or handle_manager not found")
            return 0

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[LoadInteger] Hashtable not found: {hashtable_id}")
            return 0

        return hashtable.load_integer(parent_key, child_key)


class LoadReal(NativeFunction):
    """LoadReal native 函数"""

    @property
    def name(self) -> str:
        return "LoadReal"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, *args, **kwargs) -> float:
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[LoadReal] state_context or handle_manager not found")
            return 0.0

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[LoadReal] Hashtable not found: {hashtable_id}")
            return 0.0

        return hashtable.load_real(parent_key, child_key)


class LoadBoolean(NativeFunction):
    """LoadBoolean native 函数"""

    @property
    def name(self) -> str:
        return "LoadBoolean"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, *args, **kwargs) -> bool:
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[LoadBoolean] state_context or handle_manager not found")
            return False

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[LoadBoolean] Hashtable not found: {hashtable_id}")
            return False

        return hashtable.load_boolean(parent_key, child_key)


class LoadStr(NativeFunction):
    """LoadStr native 函数"""

    @property
    def name(self) -> str:
        return "LoadStr"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, *args, **kwargs):
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[LoadStr] state_context or handle_manager not found")
            return None

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[LoadStr] Hashtable not found: {hashtable_id}")
            return None

        return hashtable.load_string(parent_key, child_key)


class LoadUnitHandle(NativeFunction):
    """LoadUnitHandle native 函数"""

    @property
    def name(self) -> str:
        return "LoadUnitHandle"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, *args, **kwargs):
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[LoadUnitHandle] state_context or handle_manager not found")
            return None

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[LoadUnitHandle] Hashtable not found: {hashtable_id}")
            return None

        return hashtable.load_unit_handle(parent_key, child_key, state_context.handle_manager)


class LoadItemHandle(NativeFunction):
    """LoadItemHandle native 函数"""

    @property
    def name(self) -> str:
        return "LoadItemHandle"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, *args, **kwargs):
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[LoadItemHandle] state_context or handle_manager not found")
            return None

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[LoadItemHandle] Hashtable not found: {hashtable_id}")
            return None

        return hashtable.load_item_handle(parent_key, child_key, state_context.handle_manager)


class LoadPlayerHandle(NativeFunction):
    """LoadPlayerHandle native 函数"""

    @property
    def name(self) -> str:
        return "LoadPlayerHandle"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, *args, **kwargs):
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[LoadPlayerHandle] state_context or handle_manager not found")
            return None

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[LoadPlayerHandle] Hashtable not found: {hashtable_id}")
            return None

        return hashtable.load_player_handle(parent_key, child_key, state_context.handle_manager)


# ========== HaveSaved* 函数 ==========

class HaveSavedInteger(NativeFunction):
    """HaveSavedInteger native 函数"""

    @property
    def name(self) -> str:
        return "HaveSavedInteger"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, *args, **kwargs) -> bool:
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[HaveSavedInteger] state_context or handle_manager not found")
            return False

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[HaveSavedInteger] Hashtable not found: {hashtable_id}")
            return False

        return hashtable.have_saved_integer(parent_key, child_key)


class HaveSavedReal(NativeFunction):
    """HaveSavedReal native 函数"""

    @property
    def name(self) -> str:
        return "HaveSavedReal"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, *args, **kwargs) -> bool:
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[HaveSavedReal] state_context or handle_manager not found")
            return False

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[HaveSavedReal] Hashtable not found: {hashtable_id}")
            return False

        return hashtable.have_saved_real(parent_key, child_key)


class HaveSavedBoolean(NativeFunction):
    """HaveSavedBoolean native 函数"""

    @property
    def name(self) -> str:
        return "HaveSavedBoolean"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, *args, **kwargs) -> bool:
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[HaveSavedBoolean] state_context or handle_manager not found")
            return False

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[HaveSavedBoolean] Hashtable not found: {hashtable_id}")
            return False

        return hashtable.have_saved_boolean(parent_key, child_key)


class HaveSavedString(NativeFunction):
    """HaveSavedString native 函数"""

    @property
    def name(self) -> str:
        return "HaveSavedString"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, *args, **kwargs) -> bool:
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[HaveSavedString] state_context or handle_manager not found")
            return False

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[HaveSavedString] Hashtable not found: {hashtable_id}")
            return False

        return hashtable.have_saved_string(parent_key, child_key)


class HaveSavedHandle(NativeFunction):
    """HaveSavedHandle native 函数"""

    @property
    def name(self) -> str:
        return "HaveSavedHandle"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, *args, **kwargs) -> bool:
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[HaveSavedHandle] state_context or handle_manager not found")
            return False

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[HaveSavedHandle] Hashtable not found: {hashtable_id}")
            return False

        return hashtable.have_saved_handle(parent_key, child_key)


# ========== RemoveSaved* 函数 ==========

class RemoveSavedInteger(NativeFunction):
    """RemoveSavedInteger native 函数"""

    @property
    def name(self) -> str:
        return "RemoveSavedInteger"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, *args, **kwargs):
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[RemoveSavedInteger] state_context or handle_manager not found")
            return None

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[RemoveSavedInteger] Hashtable not found: {hashtable_id}")
            return None

        hashtable.remove_saved_integer(parent_key, child_key)
        return None


class RemoveSavedReal(NativeFunction):
    """RemoveSavedReal native 函数"""

    @property
    def name(self) -> str:
        return "RemoveSavedReal"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, *args, **kwargs):
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[RemoveSavedReal] state_context or handle_manager not found")
            return None

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[RemoveSavedReal] Hashtable not found: {hashtable_id}")
            return None

        hashtable.remove_saved_real(parent_key, child_key)
        return None


class RemoveSavedBoolean(NativeFunction):
    """RemoveSavedBoolean native 函数"""

    @property
    def name(self) -> str:
        return "RemoveSavedBoolean"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, *args, **kwargs):
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[RemoveSavedBoolean] state_context or handle_manager not found")
            return None

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[RemoveSavedBoolean] Hashtable not found: {hashtable_id}")
            return None

        hashtable.remove_saved_boolean(parent_key, child_key)
        return None


class RemoveSavedString(NativeFunction):
    """RemoveSavedString native 函数"""

    @property
    def name(self) -> str:
        return "RemoveSavedString"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, *args, **kwargs):
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[RemoveSavedString] state_context or handle_manager not found")
            return None

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[RemoveSavedString] Hashtable not found: {hashtable_id}")
            return None

        hashtable.remove_saved_string(parent_key, child_key)
        return None


class RemoveSavedHandle(NativeFunction):
    """RemoveSavedHandle native 函数"""

    @property
    def name(self) -> str:
        return "RemoveSavedHandle"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, *args, **kwargs):
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[RemoveSavedHandle] state_context or handle_manager not found")
            return None

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[RemoveSavedHandle] Hashtable not found: {hashtable_id}")
            return None

        hashtable.remove_saved_handle(parent_key, child_key)
        return None


class FlushChildHashtable(NativeFunction):
    """FlushChildHashtable native 函数"""

    @property
    def name(self) -> str:
        return "FlushChildHashtable"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                *args, **kwargs):
        """清空指定 parentKey 下所有数据"""
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[FlushChildHashtable] state_context or handle_manager not found")
            return None

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[FlushChildHashtable] Hashtable not found: {hashtable_id}")
            return None

        hashtable.flush_child(parent_key)
        logger.info(f"[FlushChildHashtable] Flushed child {parent_key} from {hashtable_id}")
        return None


class FlushParentHashtable(NativeFunction):
    """FlushParentHashtable native 函数"""

    @property
    def name(self) -> str:
        return "FlushParentHashtable"

    def execute(self, state_context, hashtable_id: str, *args, **kwargs):
        """清空整个 hashtable"""
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[FlushParentHashtable] state_context or handle_manager not found")
            return None

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[FlushParentHashtable] Hashtable not found: {hashtable_id}")
            return None

        hashtable.flush_all()
        logger.info(f"[FlushParentHashtable] Flushed hashtable {hashtable_id}")
        return None
