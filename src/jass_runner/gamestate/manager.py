"""GameStateManager类实现模块。

此模块提供游戏状态管理器，负责管理游戏状态如日夜循环，
以及状态监听器的注册和触发。
"""

from typing import Any, Callable, Dict, List, Optional, Protocol

from jass_runner.types.gamestate import FGameState
from jass_runner.types.limitop import LimitOp


class TriggerManagerProtocol(Protocol):
    """TriggerManager协议类。

    定义与TriggerManager交互所需的接口。
    """

    def fire_event(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """触发事件。

        参数：
            event_type: 事件类型字符串
            event_data: 事件数据字典
        """
        ...


class GameStateManager:
    """游戏状态管理器。

    管理游戏状态，包括日夜循环系统（每9000帧一个周期）。
    支持状态监听器注册和事件触发。
    """

    # 日夜循环周期：9000帧 = 24小时
    DAY_NIGHT_CYCLE_FRAMES = 9000

    def __init__(self, trigger_manager: Optional[TriggerManagerProtocol] = None):
        """初始化游戏状态管理器。

        参数：
            trigger_manager: 可选的触发器管理器，用于触发事件
        """
        self.current_frame = 0
        self._next_listener_id = 0
        self._state_listeners: Dict[str, Dict] = {}
        self._trigger_manager = trigger_manager

    def update(self, delta_frames: int):
        """更新游戏状态。

        推进时间并检查状态监听器。

        参数：
            delta_frames: 推进的帧数
        """
        self.current_frame += delta_frames
        self._check_state_listeners()

    def get_float_state(self, state_id: int) -> float:
        """获取浮点类型游戏状态值。

        参数：
            state_id: 游戏状态ID（使用FGameState常量）

        返回：
            游戏状态的当前值
        """
        if state_id == FGameState.TIME_OF_DAY:
            # 计算当前时间（小时），9000帧 = 24小时
            return (self.current_frame % self.DAY_NIGHT_CYCLE_FRAMES) / self.DAY_NIGHT_CYCLE_FRAMES * 24
        return 0.0

    def register_state_listener(
        self,
        state_id: int,
        op: int,
        value: float
    ) -> str:
        """注册状态监听器。

        当游戏状态满足指定条件时触发事件。

        参数：
            state_id: 游戏状态ID（使用FGameState常量）
            op: 比较操作符（使用LimitOp常量）
            value: 比较的目标值

        返回：
            监听器handle字符串
        """
        handle = f"state_listener_{self._next_listener_id}"
        self._next_listener_id += 1

        self._state_listeners[handle] = {
            "state_id": state_id,
            "op": op,
            "value": value,
            "triggered": False,
        }

        return handle

    def _check_state_listeners(self):
        """检查状态监听器。

        遍历所有监听器，检查条件是否满足，
        满足条件时触发事件。
        """
        for handle, listener in self._state_listeners.items():
            if listener["triggered"]:
                continue

            state_id = listener["state_id"]
            op = listener["op"]
            value = listener["value"]

            # 获取当前状态值
            current_value = self.get_float_state(state_id)

            # 检查条件
            if LimitOp.compare(op, current_value, value):
                # 标记为已触发
                listener["triggered"] = True
                # 触发事件
                self._fire_event(
                    "game_state_limit",
                    {
                        "state_id": state_id,
                        "value": current_value,
                    }
                )

    def _fire_event(self, event_type: str, event_data: Dict[str, Any]):
        """触发事件。

        如果配置了触发器管理器，则通过它触发事件。

        参数：
            event_type: 事件类型字符串
            event_data: 事件数据字典
        """
        if self._trigger_manager is not None:
            self._trigger_manager.fire_event(event_type, event_data)
