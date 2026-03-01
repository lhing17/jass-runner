"""状态上下文。

此模块包含StateContext类，管理全局和局部状态。
"""

from typing import Dict
from .manager import HandleManager
from ..trigger.manager import TriggerManager


class StateContext:
    """状态上下文，管理全局和局部状态。

    采用混合方案：
    - 全局状态（handle引用）由HandleManager管理
    - 局部状态（临时变量）由ExecutionContext管理
    - 触发器系统由TriggerManager管理
    """

    def __init__(self):
        self.handle_manager = HandleManager()
        self.trigger_manager = TriggerManager()  # 触发器管理器
        self.global_vars = {}  # 全局变量存储
        self.local_stores = {}  # 上下文局部存储

        # 连接HandleManager和TriggerManager
        self.handle_manager.set_trigger_manager(self.trigger_manager)

    def get_context_store(self, context_id: str) -> Dict:
        """获取指定上下文的局部存储。"""
        if context_id not in self.local_stores:
            self.local_stores[context_id] = {}
        return self.local_stores[context_id]
