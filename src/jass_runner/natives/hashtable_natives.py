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
