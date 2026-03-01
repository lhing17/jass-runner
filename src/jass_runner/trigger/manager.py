"""TriggerManager类实现模块。

此模块提供JASS触发器系统中TriggerManager类的实现，
负责管理所有触发器的生命周期和事件分发。
"""

import logging
from typing import Any, Dict, List, Optional

from jass_runner.trigger.trigger import Trigger

logger = logging.getLogger(__name__)


class TriggerManager:
    """触发器管理器类。

    管理所有触发器的生命周期和事件分发。
    提供创建、销毁、启用/禁用触发器的功能，
    以及事件注册和触发机制。
    """

    def __init__(self):
        """初始化触发器管理器。"""
        self._triggers: Dict[str, Trigger] = {}
        self._event_index: Dict[str, List[str]] = {}
        self._global_enabled: bool = True
        self._next_id: int = 0

    def _generate_trigger_id(self) -> str:
        """生成唯一的触发器ID。

        返回：
            格式为"trigger_ + 自增数字"的唯一ID
        """
        trigger_id = f"trigger_{self._next_id}"
        self._next_id += 1
        return trigger_id

    def create_trigger(self) -> str:
        """创建新触发器。

        返回：
            新触发器的唯一标识符
        """
        trigger_id = self._generate_trigger_id()
        trigger = Trigger(trigger_id)
        self._triggers[trigger_id] = trigger
        return trigger_id

    def destroy_trigger(self, trigger_id: str) -> bool:
        """销毁触发器。

        从所有事件索引中移除触发器的引用，
        然后从触发器映射中删除。

        参数：
            trigger_id: 要销毁的触发器ID

        返回：
            成功销毁返回True，未找到返回False
        """
        if trigger_id not in self._triggers:
            return False

        # 从所有事件索引中移除
        for event_type, trigger_ids in self._event_index.items():
            if trigger_id in trigger_ids:
                trigger_ids.remove(trigger_id)

        # 从触发器映射中删除
        del self._triggers[trigger_id]
        return True

    def enable_trigger(self, trigger_id: str) -> bool:
        """启用触发器。

        参数：
            trigger_id: 要启用的触发器ID

        返回：
            成功启用返回True，未找到返回False
        """
        trigger = self._triggers.get(trigger_id)
        if trigger is None:
            return False
        trigger.enabled = True
        return True

    def disable_trigger(self, trigger_id: str) -> bool:
        """禁用触发器。

        参数：
            trigger_id: 要禁用的触发器ID

        返回：
            成功禁用返回True，未找到返回False
        """
        trigger = self._triggers.get(trigger_id)
        if trigger is None:
            return False
        trigger.enabled = False
        return True

    def is_trigger_enabled(self, trigger_id: str) -> bool:
        """检查触发器是否启用。

        参数：
            trigger_id: 要检查的触发器ID

        返回：
            触发器启用返回True，禁用返回False，未找到返回False
        """
        trigger = self._triggers.get(trigger_id)
        if trigger is None:
            return False
        return trigger.enabled

    def get_trigger(self, trigger_id: str) -> Optional[Trigger]:
        """获取触发器对象。

        参数：
            trigger_id: 触发器ID

        返回：
            触发器对象或None（未找到）
        """
        return self._triggers.get(trigger_id)

    def register_event(
        self,
        trigger_id: str,
        event_type: str,
        filter_data: Optional[Dict] = None
    ) -> Optional[str]:
        """为触发器注册事件。

        在触发器上注册事件，并更新事件索引。

        参数：
            trigger_id: 触发器ID
            event_type: 事件类型字符串
            filter_data: 可选的事件过滤器数据字典

        返回：
            事件handle字符串，未找到触发器返回None
        """
        trigger = self._triggers.get(trigger_id)
        if trigger is None:
            return None

        # 在触发器上注册事件
        event_handle = trigger.register_event(event_type, filter_data)

        # 更新事件索引
        if event_type not in self._event_index:
            self._event_index[event_type] = []
        if trigger_id not in self._event_index[event_type]:
            self._event_index[event_type].append(trigger_id)

        return event_handle

    def clear_trigger_events(self, trigger_id: str) -> bool:
        """清空触发器的所有事件。

        参数：
            trigger_id: 触发器ID

        返回：
            成功返回True，未找到触发器返回False
        """
        trigger = self._triggers.get(trigger_id)
        if trigger is None:
            return False

        # 从事件索引中移除该触发器的所有引用
        for event_type, trigger_ids in self._event_index.items():
            if trigger_id in trigger_ids:
                trigger_ids.remove(trigger_id)

        # 清空触发器的所有事件
        trigger.clear_events()

        return True

    def fire_event(self, event_type: str, event_data: Dict[str, Any]):
        """触发事件。

        遍历指定事件类型的所有候选触发器，
        检查触发器是否启用，评估条件，执行动作。

        事件分发逻辑：
        1. 根据event_type查询_event_index获取候选触发器列表
        2. 对每个候选触发器：
           - 检查enabled状态，跳过禁用的
           - 调用evaluate_conditions()，任一条件失败则跳过
           - 调用execute_actions()执行动作

        参数：
            event_type: 事件类型字符串
            event_data: 事件数据字典
        """
        # 获取候选触发器列表
        candidate_ids = self._event_index.get(event_type, [])
        if not candidate_ids:
            return

        # 构建状态上下文
        state_context = {"event_data": event_data}

        for trigger_id in candidate_ids:
            trigger = self._triggers.get(trigger_id)
            if trigger is None:
                continue

            # 检查触发器是否启用
            if not trigger.enabled:
                continue

            # 评估条件
            if not trigger.evaluate_conditions(state_context):
                continue

            # 执行动作
            try:
                trigger.execute_actions(state_context)
            except Exception as e:
                # 记录异常但继续处理其他触发器
                logger.warning(
                    f"执行触发器动作时出错 [trigger_id={trigger_id}]: {e}"
                )
                continue
