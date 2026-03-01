"""JASS触发器事件类型定义模块。

此模块定义了JASS触发器系统中使用的所有事件类型常量，
包括玩家-单位事件、通用单位事件、玩家事件和游戏事件。
"""

# =============================================================================
# 玩家-单位事件 (Player-Unit Events)
# =============================================================================
# 当特定玩家的单位发生特定行为时触发的事件

EVENT_PLAYER_UNIT_DEATH = "player_unit_death"
"""玩家单位死亡事件 - 当指定玩家的单位死亡时触发。"""

EVENT_PLAYER_UNIT_ATTACKED = "player_unit_attacked"
"""玩家单位被攻击事件 - 当指定玩家的单位受到攻击时触发。"""

EVENT_PLAYER_UNIT_SPELL_EFFECT = "player_unit_spell_effect"
"""玩家单位施法效果事件 - 当指定玩家的单位施放技能产生效果时触发。"""

EVENT_PLAYER_UNIT_DAMAGED = "player_unit_damaged"
"""玩家单位受到伤害事件 - 当指定玩家的单位受到伤害时触发。"""

EVENT_PLAYER_UNIT_PICKUP_ITEM = "player_unit_pickup_item"
"""玩家单位拾取物品事件 - 当指定玩家的单位拾取物品时触发。"""

EVENT_PLAYER_UNIT_DROP_ITEM = "player_unit_drop_item"
"""玩家单位丢弃物品事件 - 当指定玩家的单位丢弃物品时触发。"""

EVENT_PLAYER_UNIT_USE_ITEM = "player_unit_use_item"
"""玩家单位使用物品事件 - 当指定玩家的单位使用物品时触发。"""

EVENT_PLAYER_UNIT_ISSUED_ORDER = "player_unit_issued_order"
"""玩家单位接收命令事件 - 当指定玩家的单位接收到命令时触发。"""


# =============================================================================
# 通用单位事件 (Unit Events)
# =============================================================================
# 当任何单位发生特定行为时触发的事件

EVENT_UNIT_DEATH = "unit_death"
"""单位死亡事件 - 当任何单位死亡时触发。"""

EVENT_UNIT_DAMAGED = "unit_damaged"
"""单位受到伤害事件 - 当任何单位受到伤害时触发。"""


# =============================================================================
# 玩家事件 (Player Events)
# =============================================================================
# 与玩家状态变化相关的事件

EVENT_PLAYER_DEFEAT = "player_defeat"
"""玩家失败事件 - 当玩家失败时触发。"""

EVENT_PLAYER_VICTORY = "player_victory"
"""玩家胜利事件 - 当玩家胜利时触发。"""

EVENT_PLAYER_LEAVE = "player_leave"
"""玩家离开事件 - 当玩家离开游戏时触发。"""

EVENT_PLAYER_CHAT = "player_chat"
"""玩家聊天事件 - 当玩家发送聊天消息时触发。"""


# =============================================================================
# 游戏事件 (Game Events)
# =============================================================================
# 与游戏整体状态相关的事件

EVENT_GAME_TIMER_EXPIRED = "game_timer_expired"
"""游戏计时器到期事件 - 当游戏计时器到期时触发。"""


# =============================================================================
# 事件分类列表
# =============================================================================
# 用于方便地按类别访问事件类型

PLAYER_UNIT_EVENTS = [
    EVENT_PLAYER_UNIT_DEATH,
    EVENT_PLAYER_UNIT_ATTACKED,
    EVENT_PLAYER_UNIT_SPELL_EFFECT,
    EVENT_PLAYER_UNIT_DAMAGED,
    EVENT_PLAYER_UNIT_PICKUP_ITEM,
    EVENT_PLAYER_UNIT_DROP_ITEM,
    EVENT_PLAYER_UNIT_USE_ITEM,
    EVENT_PLAYER_UNIT_ISSUED_ORDER,
]
"""玩家-单位事件列表，包含所有与特定玩家单位相关的事件类型。"""

UNIT_EVENTS = [
    EVENT_UNIT_DEATH,
    EVENT_UNIT_DAMAGED,
]
"""通用单位事件列表，包含所有与任意单位相关的事件类型。"""

PLAYER_EVENTS = [
    EVENT_PLAYER_DEFEAT,
    EVENT_PLAYER_VICTORY,
    EVENT_PLAYER_LEAVE,
    EVENT_PLAYER_CHAT,
]
"""玩家事件列表，包含所有与玩家状态变化相关的事件类型。"""

GAME_EVENTS = [
    EVENT_GAME_TIMER_EXPIRED,
]
"""游戏事件列表，包含所有与游戏整体状态相关的事件类型。"""

ALL_EVENTS = (
    PLAYER_UNIT_EVENTS +
    UNIT_EVENTS +
    PLAYER_EVENTS +
    GAME_EVENTS
)
"""所有事件类型列表，包含定义的全部事件类型。"""
