"""TimerDialog native 函数测试。"""

import pytest
from unittest.mock import MagicMock, patch
from jass_runner.natives.timerdialog import TimerDialog
from jass_runner.natives.timerdialog_natives import (
    CreateTimerDialog,
    DestroyTimerDialog,
    TimerDialogSetTitle,
    TimerDialogDisplay,
    IsTimerDialogDisplayed,
    _resolve_timerdialog,
)


class TestResolveTimerDialog:
    """测试 _resolve_timerdialog 辅助函数。"""

    def test_resolve_with_timerdialog_object(self):
        """测试解析 TimerDialog 对象。"""
        state_context = MagicMock()
        mock_timer = MagicMock()
        timerdialog = TimerDialog("timerdialog_1", mock_timer)

        result = _resolve_timerdialog(state_context, timerdialog)

        assert result == timerdialog

    def test_resolve_with_string_id(self):
        """测试解析字符串 ID。"""
        state_context = MagicMock()
        mock_timerdialog = MagicMock()
        state_context.handle_manager.get_timerdialog.return_value = mock_timerdialog

        result = _resolve_timerdialog(state_context, "timerdialog_1")

        assert result == mock_timerdialog
        state_context.handle_manager.get_timerdialog.assert_called_once_with("timerdialog_1")

    def test_resolve_with_invalid_string(self):
        """测试解析无效的字符串 ID。"""
        state_context = MagicMock()
        state_context.handle_manager.get_timerdialog.return_value = None

        result = _resolve_timerdialog(state_context, "invalid_id")

        assert result is None

    def test_resolve_with_none(self):
        """测试解析 None。"""
        state_context = MagicMock()

        result = _resolve_timerdialog(state_context, None)

        assert result is None


class TestCreateTimerDialog:
    """测试 CreateTimerDialog native 函数。"""

    def test_create_timer_dialog(self):
        """测试创建 timerdialog。"""
        native = CreateTimerDialog()
        state_context = MagicMock()
        mock_timer = MagicMock()
        mock_timer.id = "timer_1"

        mock_timerdialog = MagicMock()
        mock_timerdialog.id = "timerdialog_1"
        state_context.handle_manager.create_timerdialog.return_value = mock_timerdialog

        result = native.execute(state_context, mock_timer)

        assert result == mock_timerdialog
        state_context.handle_manager.create_timerdialog.assert_called_once_with(mock_timer)


class TestDestroyTimerDialog:
    """测试 DestroyTimerDialog native 函数。"""

    def test_destroy_timer_dialog_with_object(self):
        """测试使用 TimerDialog 对象销毁。"""
        native = DestroyTimerDialog()
        state_context = MagicMock()
        mock_timer = MagicMock()
        timerdialog = TimerDialog("timerdialog_1", mock_timer)
        state_context.handle_manager.destroy_handle.return_value = True

        result = native.execute(state_context, timerdialog)

        assert result is True
        state_context.handle_manager.destroy_handle.assert_called_once_with("timerdialog_1")

    def test_destroy_timer_dialog_with_string_id(self):
        """测试使用字符串 ID 销毁。"""
        native = DestroyTimerDialog()
        state_context = MagicMock()
        mock_timerdialog = MagicMock()
        mock_timerdialog.id = "timerdialog_1"
        state_context.handle_manager.get_timerdialog.return_value = mock_timerdialog
        state_context.handle_manager.destroy_handle.return_value = True

        result = native.execute(state_context, "timerdialog_1")

        assert result is True
        state_context.handle_manager.get_timerdialog.assert_called_once_with("timerdialog_1")
        state_context.handle_manager.destroy_handle.assert_called_once_with("timerdialog_1")

    def test_destroy_timer_dialog_invalid(self):
        """测试销毁无效的 timerdialog。"""
        native = DestroyTimerDialog()
        state_context = MagicMock()

        result = native.execute(state_context, None)

        assert result is False


class TestTimerDialogSetTitle:
    """测试 TimerDialogSetTitle native 函数。"""

    def test_set_title_with_object(self):
        """测试使用 TimerDialog 对象设置标题。"""
        native = TimerDialogSetTitle()
        state_context = MagicMock()
        mock_timer = MagicMock()
        timerdialog = TimerDialog("timerdialog_1", mock_timer)

        result = native.execute(state_context, timerdialog, "游戏时间")

        assert result is True
        assert timerdialog.title == "游戏时间"

    def test_set_title_with_string_id(self):
        """测试使用字符串 ID 设置标题。"""
        native = TimerDialogSetTitle()
        state_context = MagicMock()
        mock_timerdialog = MagicMock()
        mock_timerdialog.id = "timerdialog_1"
        state_context.handle_manager.get_timerdialog.return_value = mock_timerdialog

        result = native.execute(state_context, "timerdialog_1", "游戏时间")

        assert result is True
        assert mock_timerdialog.title == "游戏时间"
        state_context.handle_manager.get_timerdialog.assert_called_once_with("timerdialog_1")

    def test_set_title_invalid_timerdialog(self):
        """测试设置无效 timerdialog 的标题。"""
        native = TimerDialogSetTitle()
        state_context = MagicMock()

        result = native.execute(state_context, None, "游戏时间")

        assert result is False


class TestTimerDialogDisplay:
    """测试 TimerDialogDisplay native 函数。"""

    def test_display_show_with_object(self):
        """测试使用 TimerDialog 对象显示。"""
        native = TimerDialogDisplay()
        state_context = MagicMock()
        mock_timer = MagicMock()
        timerdialog = TimerDialog("timerdialog_1", mock_timer)

        result = native.execute(state_context, timerdialog, True)

        assert result is True
        assert timerdialog.displayed is True

    def test_display_hide_with_object(self):
        """测试使用 TimerDialog 对象隐藏。"""
        native = TimerDialogDisplay()
        state_context = MagicMock()
        mock_timer = MagicMock()
        timerdialog = TimerDialog("timerdialog_1", mock_timer)

        result = native.execute(state_context, timerdialog, False)

        assert result is True
        assert timerdialog.displayed is False

    def test_display_with_string_id(self):
        """测试使用字符串 ID 显示。"""
        native = TimerDialogDisplay()
        state_context = MagicMock()
        mock_timerdialog = MagicMock()
        mock_timerdialog.id = "timerdialog_1"
        state_context.handle_manager.get_timerdialog.return_value = mock_timerdialog

        result = native.execute(state_context, "timerdialog_1", True)

        assert result is True
        assert mock_timerdialog.displayed is True
        state_context.handle_manager.get_timerdialog.assert_called_once_with("timerdialog_1")

    def test_display_invalid_timerdialog(self):
        """测试显示无效的 timerdialog。"""
        native = TimerDialogDisplay()
        state_context = MagicMock()

        result = native.execute(state_context, None, True)

        assert result is False


class TestIsTimerDialogDisplayed:
    """测试 IsTimerDialogDisplayed native 函数。"""

    def test_is_displayed_true_with_object(self):
        """测试使用 TimerDialog 对象检查显示状态为 true。"""
        native = IsTimerDialogDisplayed()
        state_context = MagicMock()
        mock_timer = MagicMock()
        timerdialog = TimerDialog("timerdialog_1", mock_timer)
        timerdialog.displayed = True

        result = native.execute(state_context, timerdialog)

        assert result is True

    def test_is_displayed_false_with_object(self):
        """测试使用 TimerDialog 对象检查显示状态为 false。"""
        native = IsTimerDialogDisplayed()
        state_context = MagicMock()
        mock_timer = MagicMock()
        timerdialog = TimerDialog("timerdialog_1", mock_timer)
        timerdialog.displayed = False

        result = native.execute(state_context, timerdialog)

        assert result is False

    def test_is_displayed_with_string_id(self):
        """测试使用字符串 ID 检查显示状态。"""
        native = IsTimerDialogDisplayed()
        state_context = MagicMock()
        mock_timerdialog = MagicMock()
        mock_timerdialog.displayed = True
        state_context.handle_manager.get_timerdialog.return_value = mock_timerdialog

        result = native.execute(state_context, "timerdialog_1")

        assert result is True
        state_context.handle_manager.get_timerdialog.assert_called_once_with("timerdialog_1")

    def test_is_displayed_invalid(self):
        """测试检查无效 timerdialog 的显示状态。"""
        native = IsTimerDialogDisplayed()
        state_context = MagicMock()

        result = native.execute(state_context, None)

        assert result is False


class TestTimerDialogClass:
    """测试 TimerDialog 类。"""

    def test_timerdialog_creation(self):
        """测试 TimerDialog 创建。"""
        mock_timer = MagicMock()
        timerdialog = TimerDialog("timerdialog_1", mock_timer)

        assert timerdialog.id == "timerdialog_1"
        assert timerdialog.type_name == "timerdialog"
        assert timerdialog.timer == mock_timer
        assert timerdialog.title == ""
        assert timerdialog.displayed is False
        assert timerdialog.alive is True

    def test_timerdialog_destroy(self):
        """测试 TimerDialog 销毁。"""
        mock_timer = MagicMock()
        timerdialog = TimerDialog("timerdialog_1", mock_timer)

        timerdialog.destroy()

        assert timerdialog.alive is False
