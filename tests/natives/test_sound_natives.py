"""测试声音相关 native 函数。"""

import pytest
from unittest.mock import MagicMock
from src.jass_runner.natives.sound_natives import (
    NewSoundEnvironment, SetAmbientDaySound, SetAmbientNightSound, SetMapMusic,
    CreateSoundFromLabel, PlaySound
)
from src.jass_runner.natives.state import StateContext
from src.jass_runner.natives.handle import Sound


class TestNewSoundEnvironment:
    """测试 NewSoundEnvironment 类。"""

    def test_environment_name_is_logged(self):
        """测试环境名称正确记录（通过无异常验证）。"""
        native = NewSoundEnvironment()
        context = StateContext()

        # 应该成功执行，不需要验证返回值（返回None）
        result = native.execute(context, "Default")

        assert result is None

    def test_custom_environment_name_works(self):
        """测试自定义环境名称也能正常工作。"""
        native = NewSoundEnvironment()
        context = StateContext()

        result = native.execute(context, "Dungeon")

        assert result is None

    def test_empty_environment_name_works(self):
        """测试空环境名称也能正常工作。"""
        native = NewSoundEnvironment()
        context = StateContext()

        result = native.execute(context, "")

        assert result is None


class TestSetAmbientDaySound:
    """测试 SetAmbientDaySound 类。"""

    def test_day_sound_name_is_logged(self):
        """测试日间音效名称正确记录。"""
        native = SetAmbientDaySound()
        context = StateContext()

        result = native.execute(context, "LordaeronSummerDay")

        assert result is None

    def test_empty_day_sound_name_works(self):
        """测试空日间音效名称也能正常工作。"""
        native = SetAmbientDaySound()
        context = StateContext()

        result = native.execute(context, "")

        assert result is None


class TestSetAmbientNightSound:
    """测试 SetAmbientNightSound 类。"""

    def test_night_sound_name_is_logged(self):
        """测试夜间音效名称正确记录。"""
        native = SetAmbientNightSound()
        context = StateContext()

        result = native.execute(context, "LordaeronSummerNight")

        assert result is None

    def test_empty_night_sound_name_works(self):
        """测试空夜间音效名称也能正常工作。"""
        native = SetAmbientNightSound()
        context = StateContext()

        result = native.execute(context, "")

        assert result is None


class TestSetMapMusic:
    """测试 SetMapMusic 类。"""

    def test_map_music_with_random_true(self):
        """测试设置地图音乐（随机播放为true）。"""
        native = SetMapMusic()
        context = StateContext()

        result = native.execute(context, "Music", True, 0)

        assert result is None

    def test_map_music_with_random_false(self):
        """测试设置地图音乐（随机播放为false）。"""
        native = SetMapMusic()
        context = StateContext()

        result = native.execute(context, "Music", False, 1)

        assert result is None

    def test_map_music_with_different_index(self):
        """测试设置地图音乐（使用不同的索引）。"""
        native = SetMapMusic()
        context = StateContext()

        result = native.execute(context, "WarcraftMusic", True, 5)

        assert result is None


class TestCreateSoundFromLabel:
    """测试 CreateSoundFromLabel native 函数。"""

    def test_create_sound_from_label_returns_sound(self):
        """测试 CreateSoundFromLabel 返回 Sound 对象。"""
        # 准备
        native = CreateSoundFromLabel()
        mock_state = MagicMock()
        mock_manager = MagicMock()
        mock_sound = MagicMock(spec=Sound)
        mock_sound.id = 1
        mock_manager.create_sound.return_value = mock_sound
        mock_state.handle_manager = mock_manager

        # 执行
        result = native.execute(
            mock_state,
            "Rescue",
            False,
            False,
            False,
            10000,
            10000
        )

        # 验证
        assert result == mock_sound
        mock_manager.create_sound.assert_called_once_with(
            "Rescue", False, False, False, 10000, 10000
        )


class TestPlaySound:
    """测试PlaySound native函数。"""

    def test_play_sound_sets_is_playing(self):
        """测试PlaySound设置is_playing为True。"""
        # 准备
        native = PlaySound()
        mock_state = MagicMock()
        mock_sound = MagicMock(spec=Sound)
        mock_sound.id = 1
        mock_sound.sound_label = "Rescue"
        mock_sound.is_playing = False

        # 执行
        native.execute(mock_state, mock_sound)

        # 验证
        assert mock_sound.is_playing is True
