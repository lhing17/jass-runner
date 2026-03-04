"""Sound系统集成测试。"""

import pytest
from unittest.mock import MagicMock
from jass_runner.natives.sound_natives import (
    CreateSoundFromLabel,
    PlaySound,
    StopSound,
    KillSoundWhenDone,
)
from jass_runner.natives.handle import Sound


class TestSoundSystemIntegration:
    """测试Sound系统的完整工作流程。"""

    def test_complete_sound_workflow(self):
        """测试完整的声音创建-播放-停止流程。"""
        # 准备
        mock_state = MagicMock()
        mock_manager = MagicMock()

        # 创建真实的Sound对象
        sound = Sound(
            handle_id=1,
            sound_label="Rescue",
            looping=False,
            is3D=False,
            stopwhenoutofrange=False,
            fadeInRate=10000,
            fadeOutRate=10000
        )
        mock_manager.create_sound.return_value = sound
        mock_state.handle_manager = mock_manager

        # 1. 创建声音
        create_native = CreateSoundFromLabel()
        result = create_native.execute(
            mock_state,
            "Rescue",
            False,
            False,
            False,
            10000,
            10000
        )
        assert isinstance(result, Sound)
        assert result.sound_label == "Rescue"
        assert result.is_playing is False

        # 2. 播放声音
        play_native = PlaySound()
        play_native.execute(mock_state, result)
        assert result.is_playing is True

        # 3. 设置播放完成后销毁
        kill_native = KillSoundWhenDone()
        kill_native.execute(mock_state, result, True)
        assert result.kill_when_done is True

        # 4. 停止声音
        stop_native = StopSound()
        stop_native.execute(mock_state, result, False, False)
        assert result.is_playing is False
