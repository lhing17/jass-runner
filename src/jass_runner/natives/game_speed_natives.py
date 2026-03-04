"""游戏速度相关的原生函数。

此模块包含 GetGameSpeed、SetGameSpeed、ConvertGameSpeed 等 native 函数的实现。
"""

import logging
from typing import Optional
from ..natives.base import NativeFunction


logger = logging.getLogger(__name__)


class ConvertGameSpeed(NativeFunction):
    """将整数转换为游戏速度类型。"""

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "ConvertGameSpeed"
        """
        return "ConvertGameSpeed"

    def execute(self, state_context, speed_value: int, *args, **kwargs):
        """执行 ConvertGameSpeed native 函数。

        参数：
            state_context: 状态上下文
            speed_value: 游戏速度值（0-4）
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            游戏速度整数，失败返回 None
        """
        if not isinstance(speed_value, int):
            try:
                speed_value = int(speed_value)
            except (ValueError, TypeError):
                logger.error(f"[ConvertGameSpeed] Invalid speed value: {speed_value}")
                return None

        # 确保值在有效范围内
        if speed_value < 0:
            speed_value = 0
        elif speed_value > 4:
            speed_value = 4

        logger.info(f"[ConvertGameSpeed] Converted speed value: {speed_value}")
        return speed_value


class GetGameSpeed(NativeFunction):
    """获取当前游戏速度。"""

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "GetGameSpeed"
        """
        return "GetGameSpeed"

    def execute(self, state_context, *args, **kwargs):
        """执行 GetGameSpeed native 函数。

        参数：
            state_context: 状态上下文
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            当前游戏速度（0-4），默认为 2（NORMAL）
        """
        # 从 state_context 获取游戏速度，默认为 2（NORMAL）
        if state_context is not None:
            if not hasattr(state_context, 'game_speed'):
                state_context.game_speed = 2  # 默认 NORMAL 速度
            logger.info(f"[GetGameSpeed] Current game speed: {state_context.game_speed}")
            return state_context.game_speed

        logger.warning("[GetGameSpeed] state_context not available, returning default")
        return 2  # 默认 NORMAL 速度


class SetGameSpeed(NativeFunction):
    """设置游戏速度。"""

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "SetGameSpeed"
        """
        return "SetGameSpeed"

    def execute(self, state_context, speed: int, *args, **kwargs):
        """执行 SetGameSpeed native 函数。

        参数：
            state_context: 状态上下文
            speed: 游戏速度（0-4）
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            None（对应 JASS 的 nothing）
        """
        if state_context is None:
            logger.error("[SetGameSpeed] state_context is None")
            return None

        # 确保 speed 是整数
        if not isinstance(speed, int):
            try:
                speed = int(speed)
            except (ValueError, TypeError):
                logger.error(f"[SetGameSpeed] Invalid speed value: {speed}")
                return None

        # 确保值在有效范围内
        if speed < 0:
            speed = 0
        elif speed > 4:
            speed = 4

        # 设置游戏速度
        state_context.game_speed = speed

        # 将速度映射为可读的名称
        speed_names = {
            0: "SLOWEST",
            1: "SLOW",
            2: "NORMAL",
            3: "FAST",
            4: "FASTEST"
        }
        speed_name = speed_names.get(speed, "UNKNOWN")

        logger.info(f"[SetGameSpeed] Game speed set to {speed} ({speed_name})")
        return None
