"""事件类型 handle 类。

此模块包含各种事件类型的 handle 类，用于 JASS 触发器系统。
"""

from .handle_base import Handle


class PlayerUnitEvent(Handle):
    """玩家-单位事件类型 handle。

    用于表示与玩家和单位相关的事件类型，如单位被攻击、单位死亡等。

    属性：
        event_id: 事件类型标识符（整数）
    """

    def __init__(self, handle_id: str, event_id: int):
        super().__init__(handle_id, "playerunitevent")
        self.event_id = event_id


class PlayerEvent(Handle):
    """玩家事件类型 handle。

    用于表示与玩家相关的事件类型，如玩家离开、玩家聊天等。

    属性：
        event_id: 事件类型标识符（整数）
    """

    def __init__(self, handle_id: str, event_id: int):
        super().__init__(handle_id, "playerevent")
        self.event_id = event_id


class GameEvent(Handle):
    """游戏事件类型 handle。

    用于表示与游戏相关的事件类型，如游戏开始、游戏结束等。

    属性：
        event_id: 事件类型标识符（整数）
    """

    def __init__(self, handle_id: str, event_id: int):
        super().__init__(handle_id, "gameevent")
        self.event_id = event_id


class UnitEvent(Handle):
    """通用单位事件类型 handle。

    用于表示与单位相关的事件类型，如单位被选中、单位升级等。

    属性：
        event_id: 事件类型标识符（整数）
    """

    def __init__(self, handle_id: str, event_id: int):
        super().__init__(handle_id, "unitevent")
        self.event_id = event_id
