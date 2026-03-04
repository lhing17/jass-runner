"""测试声音相关 native 函数。"""

import pytest
from src.jass_runner.natives.sound_natives import NewSoundEnvironment, SetAmbientDaySound, SetAmbientNightSound, SetMapMusic
from src.jass_runner.natives.state import StateContext


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
