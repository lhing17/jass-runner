"""JASS handle类体系。

此模块包含所有JASS handle的基类和具体实现。

注意：此模块现在作为兼容性入口点，各handle类已拆分到独立模块。
"""

# 从各模块导入handle类，保持向后兼容
from .handle_base import Handle
from .unit import Unit
from .player import Player
from .item import Item
from .group import Group
from .rect import Rect
from .effect import Effect
from .force import Force
from .boolexpr import BoolExpr, ConditionFunc, FilterFunc, AndExpr, OrExpr, NotExpr


class Sound(Handle):
    """声音对象，代表一个JASS sound handle。

    用于管理游戏中的声音资源，支持播放、停止等操作。
    """

    def __init__(
        self,
        handle_id: int,
        sound_label: str,
        looping: bool,
        is3D: bool,
        stopwhenoutofrange: bool,
        fadeInRate: int,
        fadeOutRate: int
    ):
        """初始化声音对象。

        参数：
            handle_id: 唯一标识符
            sound_label: 声音标签（如"Rescue"）
            looping: 是否循环播放
            is3D: 是否为3D音效
            stopwhenoutofrange: 超出范围时是否停止
            fadeInRate: 淡入速率
            fadeOutRate: 淡出速率
        """
        super().__init__(handle_id, "sound")
        self.sound_label = sound_label
        self.looping = looping
        self.is3D = is3D
        self.stopwhenoutofrange = stopwhenoutofrange
        self.fadeInRate = fadeInRate
        self.fadeOutRate = fadeOutRate
        self.is_playing = False
        self.kill_when_done = False

    def __repr__(self) -> str:
        """返回声音对象的字符串表示。"""
        return (f"Sound(id={self.id}, label='{self.sound_label}', "
                f"playing={self.is_playing})")


__all__ = [
    "Handle",
    "Unit",
    "Player",
    "Item",
    "Group",
    "Rect",
    "Effect",
    "Force",
    "BoolExpr",
    "ConditionFunc",
    "FilterFunc",
    "AndExpr",
    "OrExpr",
    "NotExpr",
    "Sound",
]
