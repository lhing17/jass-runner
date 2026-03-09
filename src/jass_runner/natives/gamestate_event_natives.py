"""游戏状态事件注册相关的原生函数。

此模块包含 JASS 触发器系统中游戏状态事件注册相关的 native 函数实现。
"""

import logging

from .base import NativeFunction

logger = logging.getLogger(__name__)


class TriggerRegisterGameStateEvent(NativeFunction):
    """注册游戏状态事件的原生函数。

    当游戏状态满足指定条件时触发事件。
    示例：TriggerRegisterGameStateEvent(trg, GAME_STATE_TIME_OF_DAY, EQUAL, 6.0)
    """

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "TriggerRegisterGameStateEvent"
        """
        return "TriggerRegisterGameStateEvent"

    def execute(self, state_context, trigger_id: str, state_id: int,
                opcode: int, limit_value: float, *args, **kwargs):
        """执行 TriggerRegisterGameStateEvent 原生函数。

        参数：
            state_context: 状态上下文，必须包含 game_state_manager
            trigger_id: 要注册事件的触发器ID
            state_id: 游戏状态ID (如 FGameState.TIME_OF_DAY)
            opcode: 比较操作符 (如 LimitOp.EQUAL)
            limit_value: 目标限制值
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            事件 handle 字符串，如果注册失败则返回 None
        """
        # 检查 state_context 和 game_state_manager 存在性
        if state_context is None or not hasattr(state_context, 'game_state_manager'):
            logger.error(
                "[TriggerRegisterGameStateEvent] state_context or "
                "game_state_manager not found"
            )
            return None

        game_state_manager = state_context.game_state_manager

        result = game_state_manager.register_state_listener(
            trigger_id,
            state_id,
            opcode,
            limit_value
        )

        if result:
            logger.info(
                f"[TriggerRegisterGameStateEvent] Registered game state event "
                f"{result} (state={state_id}, opcode={opcode}, "
                f"limit={limit_value}) on trigger {trigger_id}"
            )
        else:
            logger.warning(
                f"[TriggerRegisterGameStateEvent] Failed to register game "
                f"state event on trigger {trigger_id}"
            )

        return result


class SuspendTimeOfDay(NativeFunction):
    """暂停/恢复日夜循环的原生函数。

    在模拟环境中仅记录日志。
    """

    @property
    def name(self) -> str:
        """获取 native 函数的名称。"""
        return "SuspendTimeOfDay"

    def execute(self, state_context, pause: bool, *args, **kwargs):
        """执行 SuspendTimeOfDay 原生函数。

        参数：
            state_context: 状态上下文
            pause: True 表示暂停，False 表示恢复
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            None
        """
        action = "暂停" if pause else "恢复"
        logger.info(f"[SuspendTimeOfDay] {action}日夜循环")
        return None
