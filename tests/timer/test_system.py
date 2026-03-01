"""测试 TimerSystem 类。"""

import pytest
from unittest.mock import Mock, MagicMock

from jass_runner.timer.system import TimerSystem
from jass_runner.timer.timer import Timer


class TestTimerSystem:
    """测试 TimerSystem 类。"""

    def test_timer_system_creation(self):
        """测试 TimerSystem 可以创建。"""
        system = TimerSystem()
        assert system is not None
        assert hasattr(system, 'create_timer')
        assert hasattr(system, 'get_timer')
        assert hasattr(system, 'update')

    def test_create_timer_sets_trigger_manager(self):
        """测试 create_timer 创建的计时器带有 trigger_manager。"""
        system = TimerSystem()
        mock_trigger_manager = Mock()
        system.set_trigger_manager(mock_trigger_manager)

        timer_id = system.create_timer()
        timer = system.get_timer(timer_id)

        assert timer is not None
        assert timer._trigger_manager == mock_trigger_manager

    def test_create_timer_without_trigger_manager(self):
        """测试没有设置 trigger_manager 时创建计时器不会报错。"""
        system = TimerSystem()

        timer_id = system.create_timer()
        timer = system.get_timer(timer_id)

        assert timer is not None
        assert timer._trigger_manager is None
