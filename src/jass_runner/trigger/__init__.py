"""JASS触发器系统模块。

此模块提供JASS触发器系统的实现，包括事件类型定义、
触发器管理和触发器执行功能。
"""

from jass_runner.trigger.event_types import (
    # 玩家-单位事件
    EVENT_PLAYER_UNIT_DEATH,
    EVENT_PLAYER_UNIT_ATTACKED,
    EVENT_PLAYER_UNIT_SPELL_EFFECT,
    EVENT_PLAYER_UNIT_DAMAGED,
    EVENT_PLAYER_UNIT_PICKUP_ITEM,
    EVENT_PLAYER_UNIT_DROP_ITEM,
    EVENT_PLAYER_UNIT_USE_ITEM,
    EVENT_PLAYER_UNIT_ISSUED_ORDER,
    # 通用单位事件
    EVENT_UNIT_DEATH,
    EVENT_UNIT_DAMAGED,
    # 玩家事件
    EVENT_PLAYER_DEFEAT,
    EVENT_PLAYER_VICTORY,
    EVENT_PLAYER_LEAVE,
    EVENT_PLAYER_CHAT,
    # 游戏事件
    EVENT_GAME_TIMER_EXPIRED,
    # 事件分类列表
    PLAYER_UNIT_EVENTS,
    UNIT_EVENTS,
    PLAYER_EVENTS,
    GAME_EVENTS,
    ALL_EVENTS,
)
from jass_runner.trigger.manager import TriggerManager
from jass_runner.trigger.trigger import Trigger

__all__ = [
    # 玩家-单位事件
    "EVENT_PLAYER_UNIT_DEATH",
    "EVENT_PLAYER_UNIT_ATTACKED",
    "EVENT_PLAYER_UNIT_SPELL_EFFECT",
    "EVENT_PLAYER_UNIT_DAMAGED",
    "EVENT_PLAYER_UNIT_PICKUP_ITEM",
    "EVENT_PLAYER_UNIT_DROP_ITEM",
    "EVENT_PLAYER_UNIT_USE_ITEM",
    "EVENT_PLAYER_UNIT_ISSUED_ORDER",
    # 通用单位事件
    "EVENT_UNIT_DEATH",
    "EVENT_UNIT_DAMAGED",
    # 玩家事件
    "EVENT_PLAYER_DEFEAT",
    "EVENT_PLAYER_VICTORY",
    "EVENT_PLAYER_LEAVE",
    "EVENT_PLAYER_CHAT",
    # 游戏事件
    "EVENT_GAME_TIMER_EXPIRED",
    # 事件分类列表
    "PLAYER_UNIT_EVENTS",
    "UNIT_EVENTS",
    "PLAYER_EVENTS",
    "GAME_EVENTS",
    "ALL_EVENTS",
    # 触发器类
    "Trigger",
    "TriggerManager",
]
