"""声音相关 native 函数实现。

此模块包含与声音相关的 JASS native 函数，如 NewSoundEnvironment 等。
"""

import logging
from .base import NativeFunction
from .handle import Sound

logger = logging.getLogger(__name__)


class NewSoundEnvironment(NativeFunction):
    """设置新的声音环境。"""

    @property
    def name(self) -> str:
        return "NewSoundEnvironment"

    def execute(self, state_context, environment_name: str) -> None:
        """执行设置声音环境。

        参数:
            state_context: 状态上下文
            environment_name: 声音环境名称（如 "Default"）
        """
        logger.info(
            f"[NewSoundEnvironment] 声音环境已设置: "
            f"环境名称={environment_name}"
        )


class SetAmbientDaySound(NativeFunction):
    """设置日间环境音效。"""

    @property
    def name(self) -> str:
        return "SetAmbientDaySound"

    def execute(self, state_context, ambient_sound_name: str) -> None:
        """执行设置日间环境音效。

        参数:
            state_context: 状态上下文
            ambient_sound_name: 日间环境音效名称（如 "LordaeronSummerDay"）
        """
        logger.info(
            f"[SetAmbientDaySound] 日间环境音效已设置: "
            f"音效名称={ambient_sound_name}"
        )


class SetAmbientNightSound(NativeFunction):
    """设置夜间环境音效。"""

    @property
    def name(self) -> str:
        return "SetAmbientNightSound"

    def execute(self, state_context, ambient_sound_name: str) -> None:
        """执行设置夜间环境音效。

        参数:
            state_context: 状态上下文
            ambient_sound_name: 夜间环境音效名称（如 "LordaeronSummerNight"）
        """
        logger.info(
            f"[SetAmbientNightSound] 夜间环境音效已设置: "
            f"音效名称={ambient_sound_name}"
        )


class SetMapMusic(NativeFunction):
    """设置地图背景音乐。"""

    @property
    def name(self) -> str:
        return "SetMapMusic"

    def execute(self, state_context, music_name: str, random: bool, index: int) -> None:
        """执行设置地图背景音乐。

        参数:
            state_context: 状态上下文
            music_name: 音乐名称或音乐集合名称
            random: 是否随机播放
            index: 音乐索引
        """
        logger.info(
            f"[SetMapMusic] 地图音乐已设置: "
            f"音乐名称={music_name}, 随机播放={random}, 索引={index}"
        )


class CreateSoundFromLabel(NativeFunction):
    """从标签创建声音对象。"""

    @property
    def name(self) -> str:
        return "CreateSoundFromLabel"

    def execute(
        self,
        state_context,
        sound_label: str,
        looping: bool,
        is3D: bool,
        stopwhenoutofrange: bool,
        fadeInRate: int,
        fadeOutRate: int
    ) -> Sound:
        """从标签创建声音对象。

        参数：
            state_context: 状态上下文
            sound_label: 声音标签（如"Rescue"）
            looping: 是否循环播放
            is3D: 是否为3D音效
            stopwhenoutofrange: 超出范围时是否停止
            fadeInRate: 淡入速率
            fadeOutRate: 淡出速率

        返回：
            创建的Sound对象
        """
        handle_manager = state_context.handle_manager
        return handle_manager.create_sound(
            sound_label,
            looping,
            is3D,
            stopwhenoutofrange,
            fadeInRate,
            fadeOutRate
        )


class PlaySound(NativeFunction):
    """播放声音。"""

    @property
    def name(self) -> str:
        return "PlaySound"

    def execute(self, state_context, sound: Sound) -> None:
        """播放声音。

        参数：
            state_context: 状态上下文
            sound: 要播放的声音对象
        """
        sound.is_playing = True
        logger.info(
            f"[PlaySound] 声音开始播放: "
            f"ID={sound.id}, 标签={sound.sound_label}"
        )


class StopSound(NativeFunction):
    """停止声音播放。"""

    @property
    def name(self) -> str:
        return "StopSound"

    def execute(
        self,
        state_context,
        sound: Sound,
        killWhenDone: bool = False,
        fadeOut: bool = False
    ) -> None:
        """停止声音播放。

        参数：
            state_context: 状态上下文
            sound: 要停止的声音对象
            killWhenDone: 是否在播放完成后销毁
            fadeOut: 是否淡出
        """
        sound.is_playing = False
        if killWhenDone:
            sound.kill_when_done = True
        logger.info(
            f"[StopSound] 声音已停止: "
            f"ID={sound.id}, 标签={sound.sound_label}, "
            f"淡出={fadeOut}"
        )
