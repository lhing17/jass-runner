"""Sound handle类。

此模块包含Sound类的实现，代表JASS中的sound handle。
"""

from .handle_base import Handle


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
