"""游戏状态相关的 handle 类。

此模块包含与游戏状态、玩家状态、单位状态相关的 handle 类。
"""

from .handle_base import Handle


class GameState(Handle):
    """游戏状态类型 handle。"""

    def __init__(self, handle_id: str, state_id: int):
        super().__init__(handle_id, "gamestate")
        self.state_id = state_id


class IGameState(Handle):
    """整数游戏状态类型 handle。"""

    def __init__(self, handle_id: str, state_id: int):
        super().__init__(handle_id, "igamestate")
        self.state_id = state_id


class FGameState(Handle):
    """浮点游戏状态类型 handle。"""

    def __init__(self, handle_id: str, state_id: int):
        super().__init__(handle_id, "fgamestate")
        self.state_id = state_id


class PlayerState(Handle):
    """玩家状态类型 handle。"""

    def __init__(self, handle_id: str, state_id: int):
        super().__init__(handle_id, "playerstate")
        self.state_id = state_id


class UnitState(Handle):
    """单位状态类型 handle。"""

    def __init__(self, handle_id: str, state_id: int):
        super().__init__(handle_id, "unitstate")
        self.state_id = state_id


class AllianceType(Handle):
    """联盟类型 handle。"""

    def __init__(self, handle_id: str, alliance_id: int):
        super().__init__(handle_id, "alliancetype")
        self.alliance_id = alliance_id


class LimitOp(Handle):
    """限制操作类型 handle。"""

    def __init__(self, handle_id: str, op_id: int):
        super().__init__(handle_id, "limitop")
        self.op_id = op_id


class WidgetEvent(Handle):
    """控件事件类型 handle。"""

    def __init__(self, handle_id: str, event_id: int):
        super().__init__(handle_id, "widgetevent")
        self.event_id = event_id


class DialogEvent(Handle):
    """对话框事件类型 handle。"""

    def __init__(self, handle_id: str, event_id: int):
        super().__init__(handle_id, "dialogevent")
        self.event_id = event_id
