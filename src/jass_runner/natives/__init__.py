"""JASS native函数框架。

此包包含JASS native函数的模拟实现和状态管理系统。
"""

from .base import NativeFunction
from .registry import NativeRegistry
from .factory import NativeFactory
from .handle import Handle, Unit, Player
from .manager import HandleManager
from .state import StateContext
from .trigger_natives import (
    CreateTrigger, DestroyTrigger, EnableTrigger, DisableTrigger,
    IsTriggerEnabled, TriggerAddAction, TriggerRemoveAction, TriggerClearActions,
    TriggerAddCondition, TriggerRemoveCondition, TriggerClearConditions,
    TriggerEvaluate, TriggerClearEvents,
)
from .trigger_register_event_natives import (
    TriggerRegisterTimerEvent, TriggerRegisterTimerExpireEvent,
    TriggerRegisterPlayerUnitEvent, TriggerRegisterUnitEvent,
    TriggerRegisterPlayerEvent, TriggerRegisterGameEvent,
)
from .math_core import (
    SquareRoot, Pow, Cos, Sin, R2I, I2R,
)
from .math_extended import (
    Tan, ModuloInteger, ModuloReal, R2S, S2R, I2S, S2I, GetRandomInt, GetRandomReal,
)

__all__ = [
    "NativeFunction",
    "NativeRegistry",
    "NativeFactory",
    "Handle",
    "Unit",
    "Player",
    "HandleManager",
    "StateContext",
    # 触发器生命周期管理
    "CreateTrigger",
    "DestroyTrigger",
    "EnableTrigger",
    "DisableTrigger",
    "IsTriggerEnabled",
    # 触发器动作管理
    "TriggerAddAction",
    "TriggerRemoveAction",
    "TriggerClearActions",
    # 触发器条件管理
    "TriggerAddCondition",
    "TriggerRemoveCondition",
    "TriggerClearConditions",
    "TriggerEvaluate",
    # 触发器事件管理
    "TriggerClearEvents",
    # 触发器事件注册
    "TriggerRegisterTimerEvent",
    "TriggerRegisterTimerExpireEvent",
    "TriggerRegisterPlayerUnitEvent",
    "TriggerRegisterUnitEvent",
    "TriggerRegisterPlayerEvent",
    "TriggerRegisterGameEvent",
    # 核心数学函数
    "SquareRoot",
    "Pow",
    "Cos",
    "Sin",
    "R2I",
    "I2R",
    # 扩展数学函数
    "Tan",
    "ModuloInteger",
    "ModuloReal",
    "R2S",
    "S2R",
    "I2S",
    "S2I",
    "GetRandomInt",
    "GetRandomReal",
]