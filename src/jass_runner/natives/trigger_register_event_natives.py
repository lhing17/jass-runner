"""触发器事件注册相关的原生函数。

此模块包含JASS触发器系统中事件注册相关的native函数实现，
包括计时器事件、玩家单位事件、单位事件、玩家事件和游戏事件的注册功能。
"""

import logging
from typing import Any

from ..natives.base import NativeFunction
from jass_runner.trigger.event_types import EVENT_GAME_TIMER_EXPIRED


logger = logging.getLogger(__name__)


class TriggerRegisterTimerEvent(NativeFunction):
    """注册计时器事件的原生函数。

    为触发器注册一个基于时间的周期性或一次性事件。
    """

    @property
    def name(self) -> str:
        """获取native函数的名称。

        返回：
            "TriggerRegisterTimerEvent"
        """
        return "TriggerRegisterTimerEvent"

    def execute(self, state_context, trigger_id: str, timeout: float,
                periodic: bool, *args, **kwargs):
        """执行 TriggerRegisterTimerEvent 原生函数。

        参数：
            state_context: 状态上下文，必须包含trigger_manager
            trigger_id: 要注册事件的触发器ID
            timeout: 计时器超时时间（秒）
            periodic: 是否周期性触发
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            事件handle字符串，如果触发器不存在则返回None
        """
        # 检查state_context和trigger_manager存在性
        if state_context is None or not hasattr(state_context, 'trigger_manager'):
            logger.error("[TriggerRegisterTimerEvent] state_context or trigger_manager not found")
            return None

        filter_data = {"timeout": timeout, "periodic": periodic}
        result = state_context.trigger_manager.register_event(
            trigger_id, EVENT_GAME_TIMER_EXPIRED, filter_data
        )

        if result:
            logger.info(
                f"[TriggerRegisterTimerEvent] Registered timer event "
                f"{result} on trigger {trigger_id}"
            )
        else:
            logger.warning(
                f"[TriggerRegisterTimerEvent] Failed to register timer "
                f"event on trigger {trigger_id}"
            )

        return result


class TriggerRegisterTimerExpireEvent(NativeFunction):
    """注册特定计时器过期事件的原生函数。

    为触发器注册一个当特定计时器过期时触发的事件。
    """

    @property
    def name(self) -> str:
        """获取native函数的名称。

        返回：
            "TriggerRegisterTimerExpireEvent"
        """
        return "TriggerRegisterTimerExpireEvent"

    def execute(self, state_context, trigger_id: str, timer_id: str,
                *args, **kwargs):
        """执行 TriggerRegisterTimerExpireEvent 原生函数。

        参数：
            state_context: 状态上下文，必须包含trigger_manager
            trigger_id: 要注册事件的触发器ID
            timer_id: 要监听的计时器ID
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            事件handle字符串，如果触发器不存在则返回None
        """
        # 检查state_context和trigger_manager存在性
        if state_context is None or not hasattr(state_context, 'trigger_manager'):
            logger.error("[TriggerRegisterTimerExpireEvent] state_context or trigger_manager not found")
            return None

        filter_data = {"timer_id": timer_id}
        result = state_context.trigger_manager.register_event(
            trigger_id, EVENT_GAME_TIMER_EXPIRED, filter_data
        )

        if result:
            logger.info(f"[TriggerRegisterTimerExpireEvent] Registered timer expire event "
                       f"{result} for timer {timer_id} on trigger {trigger_id}")
        else:
            logger.warning(f"[TriggerRegisterTimerExpireEvent] Failed to register timer "
                        f"expire event on trigger {trigger_id}")

        return result


class TriggerRegisterPlayerUnitEvent(NativeFunction):
    """注册玩家单位事件的原生函数。

    为触发器注册一个当特定玩家的单位发生特定行为时触发的事件。
    """

    @property
    def name(self) -> str:
        """获取native函数的名称。

        返回：
            "TriggerRegisterPlayerUnitEvent"
        """
        return "TriggerRegisterPlayerUnitEvent"

    def execute(self, state_context, trigger_id: str, player_id: int,
                event_type: str, filter_func: Any = None, *args, **kwargs):
        """执行 TriggerRegisterPlayerUnitEvent 原生函数。

        参数：
            state_context: 状态上下文，必须包含trigger_manager
            trigger_id: 要注册事件的触发器ID
            player_id: 玩家ID
            event_type: 事件类型
            filter_func: 可选的过滤函数
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            事件handle字符串，如果触发器不存在则返回None
        """
        # 检查state_context和trigger_manager存在性
        if state_context is None or not hasattr(state_context, 'trigger_manager'):
            logger.error("[TriggerRegisterPlayerUnitEvent] state_context or trigger_manager not found")
            return None

        filter_data = {"player_id": player_id}
        if filter_func is not None:
            filter_data["filter"] = filter_func

        result = state_context.trigger_manager.register_event(
            trigger_id, event_type, filter_data
        )

        if result:
            logger.info(f"[TriggerRegisterPlayerUnitEvent] Registered player unit event "
                       f"{result} (type={event_type}, player_id={player_id}) on trigger {trigger_id}")
        else:
            logger.warning(f"[TriggerRegisterPlayerUnitEvent] Failed to register player "
                        f"unit event on trigger {trigger_id}")

        return result


class TriggerRegisterUnitEvent(NativeFunction):
    """注册单位事件的原生函数。

    为触发器注册一个当任何单位发生特定行为时触发的事件。
    """

    @property
    def name(self) -> str:
        """获取native函数的名称。

        返回：
            "TriggerRegisterUnitEvent"
        """
        return "TriggerRegisterUnitEvent"

    def execute(self, state_context, trigger_id: str, event_type: str,
                filter_func: Any = None, *args, **kwargs):
        """执行 TriggerRegisterUnitEvent 原生函数。

        参数：
            state_context: 状态上下文，必须包含trigger_manager
            trigger_id: 要注册事件的触发器ID
            event_type: 事件类型
            filter_func: 可选的过滤函数
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            事件handle字符串，如果触发器不存在则返回None
        """
        # 检查state_context和trigger_manager存在性
        if state_context is None or not hasattr(state_context, 'trigger_manager'):
            logger.error("[TriggerRegisterUnitEvent] state_context or trigger_manager not found")
            return None

        filter_data = {}
        if filter_func is not None:
            filter_data["filter"] = filter_func

        result = state_context.trigger_manager.register_event(
            trigger_id, event_type, filter_data
        )

        if result:
            logger.info(f"[TriggerRegisterUnitEvent] Registered unit event "
                       f"{result} (type={event_type}) on trigger {trigger_id}")
        else:
            logger.warning(f"[TriggerRegisterUnitEvent] Failed to register unit "
                        f"event on trigger {trigger_id}")

        return result


class TriggerRegisterPlayerEvent(NativeFunction):
    """注册玩家事件的原生函数。

    为触发器注册一个当特定玩家的状态发生变化时触发的事件。
    """

    @property
    def name(self) -> str:
        """获取native函数的名称。

        返回：
            "TriggerRegisterPlayerEvent"
        """
        return "TriggerRegisterPlayerEvent"

    def execute(self, state_context, trigger_id: str, player_id: int,
                event_type: str, *args, **kwargs):
        """执行 TriggerRegisterPlayerEvent 原生函数。

        参数：
            state_context: 状态上下文，必须包含trigger_manager
            trigger_id: 要注册事件的触发器ID
            player_id: 玩家ID
            event_type: 事件类型
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            事件handle字符串，如果触发器不存在则返回None
        """
        # 检查state_context和trigger_manager存在性
        if state_context is None or not hasattr(state_context, 'trigger_manager'):
            logger.error("[TriggerRegisterPlayerEvent] state_context or trigger_manager not found")
            return None

        filter_data = {"player_id": player_id}

        result = state_context.trigger_manager.register_event(
            trigger_id, event_type, filter_data
        )

        if result:
            logger.info(f"[TriggerRegisterPlayerEvent] Registered player event "
                       f"{result} (type={event_type}, player_id={player_id}) on trigger {trigger_id}")
        else:
            logger.warning(f"[TriggerRegisterPlayerEvent] Failed to register player "
                        f"event on trigger {trigger_id}")

        return result


class TriggerRegisterGameEvent(NativeFunction):
    """注册游戏事件的原生函数。

    为触发器注册一个当游戏整体状态发生变化时触发的事件。
    """

    @property
    def name(self) -> str:
        """获取native函数的名称。

        返回：
            "TriggerRegisterGameEvent"
        """
        return "TriggerRegisterGameEvent"

    def execute(self, state_context, trigger_id: str, event_type: str,
                *args, **kwargs):
        """执行 TriggerRegisterGameEvent 原生函数。

        参数：
            state_context: 状态上下文，必须包含trigger_manager
            trigger_id: 要注册事件的触发器ID
            event_type: 事件类型
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            事件handle字符串，如果触发器不存在则返回None
        """
        # 检查state_context和trigger_manager存在性
        if state_context is None or not hasattr(state_context, 'trigger_manager'):
            logger.error("[TriggerRegisterGameEvent] state_context or trigger_manager not found")
            return None

        result = state_context.trigger_manager.register_event(
            trigger_id, event_type, None
        )

        if result:
            logger.info(f"[TriggerRegisterGameEvent] Registered game event "
                       f"{result} (type={event_type}) on trigger {trigger_id}")
        else:
            logger.warning(f"[TriggerRegisterGameEvent] Failed to register game "
                        f"event on trigger {trigger_id}")

        return result
