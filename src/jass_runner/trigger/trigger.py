"""Trigger类实现模块。

此模块提供JASS触发器系统中Trigger类的实现，
负责管理触发器的事件、条件和动作。
"""

import logging
import uuid
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


class Trigger:
    """JASS触发器类。

    管理单个触发器的事件、条件和动作。
    当事件触发时，会依次评估所有条件，
    如果所有条件都通过，则执行所有动作。
    """

    def __init__(self, trigger_id: str):
        """初始化触发器。

        参数：
            trigger_id: 触发器的唯一标识符
        """
        self.trigger_id = trigger_id
        self.events: List[Dict[str, Any]] = []
        self.conditions: List[Dict[str, Any]] = []
        self.actions: List[Dict[str, Any]] = []
        self.enabled: bool = True

    def _generate_handle(self, prefix: str) -> str:
        """生成带前缀的handle。

        参数：
            prefix: handle前缀（如"action_", "condition_", "event_"）

        返回：
            格式为"prefix_ + uuid前8位"的handle字符串
        """
        return f"{prefix}{uuid.uuid4().hex[:8]}"

    def add_action(self, action_func: Callable) -> str:
        """添加动作到触发器。

        参数：
            action_func: 动作函数，接收state_context参数

        返回：
            动作handle字符串（格式：action_ + uuid前8位）
        """
        handle = self._generate_handle("action_")
        self.actions.append({
            "handle": handle,
            "func": action_func
        })
        return handle

    def remove_action(self, action_handle: str) -> bool:
        """移除指定的动作。

        参数：
            action_handle: 要移除的动作handle

        返回：
            成功移除返回True，未找到返回False
        """
        for i, action in enumerate(self.actions):
            if action["handle"] == action_handle:
                self.actions.pop(i)
                return True
        return False

    def clear_actions(self):
        """清空所有动作。"""
        self.actions.clear()

    def add_condition(self, condition_func: Callable) -> str:
        """添加条件到触发器。

        参数：
            condition_func: 条件函数，接收state_context参数，返回bool

        返回：
            条件handle字符串（格式：condition_ + uuid前8位）
        """
        handle = self._generate_handle("condition_")
        self.conditions.append({
            "handle": handle,
            "func": condition_func
        })
        return handle

    def remove_condition(self, condition_handle: str) -> bool:
        """移除指定的条件。

        参数：
            condition_handle: 要移除的条件handle

        返回：
            成功移除返回True，未找到返回False
        """
        for i, condition in enumerate(self.conditions):
            if condition["handle"] == condition_handle:
                self.conditions.pop(i)
                return True
        return False

    def clear_conditions(self):
        """清空所有条件。"""
        self.conditions.clear()

    def register_event(self, event_type: str, filter_data: Optional[Dict]) -> str:
        """注册事件到触发器。

        参数：
            event_type: 事件类型字符串
            filter_data: 可选的事件过滤器数据字典

        返回：
            事件handle字符串（格式：event_ + uuid前8位）
        """
        handle = self._generate_handle("event_")
        self.events.append({
            "handle": handle,
            "type": event_type,
            "filter": filter_data
        })
        return handle

    def clear_events(self):
        """清空所有事件。"""
        self.events.clear()

    def evaluate_conditions(self, state_context: Dict) -> bool:
        """评估所有条件。

        按添加顺序依次评估所有条件，
        任一条件失败返回False，全部通过返回True，
        无条件时默认返回True。

        参数：
            state_context: 状态上下文字典

        返回：
            所有条件是否通过
        """
        # 无条件时默认返回True
        if not self.conditions:
            return True

        # 依次评估所有条件，任一失败立即返回False
        for condition in self.conditions:
            try:
                result = condition["func"](state_context)
                if not result:
                    return False
            except Exception as e:
                logger.warning(
                    f"条件评估出错 [trigger_id={self.trigger_id}]: {e}"
                )
                return False

        return True

    def execute_actions(self, state_context: Dict):
        """按顺序执行所有动作。

        按添加顺序依次执行所有动作，
        即使某个动作抛出异常也不中断，继续执行后续动作。

        参数：
            state_context: 状态上下文字典
        """
        for action in self.actions:
            try:
                action["func"](state_context)
            except Exception as e:
                # 记录异常但继续执行后续动作
                logger.warning(
                    f"动作执行出错 [trigger_id={self.trigger_id}, "
                    f"action={action['handle']}]: {e}"
                )
                continue
