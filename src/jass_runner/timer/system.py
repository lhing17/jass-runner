"""用于管理多个计时器的计时器系统。"""

import uuid
from typing import Any, Dict, Optional
from .timer import Timer


class TimerSystem:
    """用于管理 JASS 计时器的系统。"""

    def __init__(self):
        self._timers: Dict[str, Timer] = {}
        self._current_time: float = 0.0
        self._trigger_manager: Optional[Any] = None

    def set_trigger_manager(self, trigger_manager: Any):
        """设置触发器管理器。

        参数：
            trigger_manager: TriggerManager 实例
        """
        self._trigger_manager = trigger_manager

    def create_timer(self) -> str:
        """创建一个新计时器并返回其 ID。"""
        timer_id = f"timer_{uuid.uuid4().hex[:8]}"
        timer = Timer(timer_id)
        # 如果已设置 trigger_manager，传递给新创建的计时器
        if self._trigger_manager:
            timer.set_trigger_manager(self._trigger_manager)
        self._timers[timer_id] = timer
        return timer_id

    def get_timer(self, timer_id: str) -> Optional[Timer]:
        """通过 ID 获取计时器。"""
        return self._timers.get(timer_id)

    def destroy_timer(self, timer_id: str) -> bool:
        """销毁一个计时器。"""
        if timer_id in self._timers:
            timer = self._timers[timer_id]
            timer.destroy()
            del self._timers[timer_id]
            return True
        return False

    def update(self, delta_time: float):
        """更新所有计时器的经过时间。"""
        self._current_time += delta_time

        timers_to_remove = []
        for timer_id, timer in self._timers.items():
            fired = timer.update(delta_time)
            if fired and not timer.periodic and not timer.running:
                timers_to_remove.append(timer_id)

        # 移除已触发的一次性计时器
        for timer_id in timers_to_remove:
            del self._timers[timer_id]

    def get_elapsed_time(self, timer_id: str) -> Optional[float]:
        """获取计时器的经过时间。"""
        timer = self.get_timer(timer_id)
        if timer:
            return timer.elapsed
        return None

    def pause_timer(self, timer_id: str) -> bool:
        """暂停计时器。"""
        timer = self.get_timer(timer_id)
        if timer:
            timer.pause()
            return True
        return False

    def resume_timer(self, timer_id: str) -> bool:
        """恢复计时器。"""
        timer = self.get_timer(timer_id)
        if timer:
            timer.resume()
            return True
        return False
