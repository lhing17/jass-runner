"""测试 Timer 类。"""

from unittest.mock import Mock

from jass_runner.timer.timer import Timer


def test_timer_creation():
    """测试 Timer 可以创建。"""
    timer = Timer(timer_id="timer_001")
    assert timer is not None
    assert timer.timer_id == "timer_001"
    assert timer.elapsed == 0.0
    assert timer.periodic is False
    assert timer.running is False


def test_timer_set_trigger_manager():
    """测试 set_trigger_manager 方法设置 trigger_manager。"""
    timer = Timer(timer_id="timer_001")
    mock_trigger_manager = Mock()

    timer.set_trigger_manager(mock_trigger_manager)

    assert timer._trigger_manager == mock_trigger_manager


def test_timer_fires_event_on_expire():
    """测试计时器到期时触发事件。"""
    timer = Timer(timer_id="timer_001")
    mock_trigger_manager = Mock()
    timer.set_trigger_manager(mock_trigger_manager)

    callback_called = []

    def callback():
        callback_called.append(True)

    timer.start(timeout=1.0, periodic=False, callback=callback)
    timer.update(1.0)  # 触发到期

    # 验证 trigger_manager.fire_event 被调用
    mock_trigger_manager.fire_event.assert_called_once()
    call_args = mock_trigger_manager.fire_event.call_args
    assert call_args[0][0] == "game_timer_expired"
    assert call_args[0][1]["timer_id"] == "timer_001"


def test_timer_no_error_without_trigger_manager():
    """测试没有 trigger_manager 时计时器到期不报错。"""
    timer = Timer(timer_id="timer_001")

    callback_called = []

    def callback():
        callback_called.append(True)

    timer.start(timeout=1.0, periodic=False, callback=callback)
    # 不应抛出异常
    timer.update(1.0)

    assert len(callback_called) == 1
