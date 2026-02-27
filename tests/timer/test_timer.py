"""Test Timer class."""

def test_timer_creation():
    """Test that Timer can be created."""
    from jass_runner.timer.timer import Timer

    timer = Timer(timer_id="timer_001")
    assert timer is not None
    assert timer.timer_id == "timer_001"
    assert timer.elapsed == 0.0
    assert timer.periodic is False
    assert timer.running is False


def test_timer_system_creation():
    """Test that TimerSystem can be created."""
    from jass_runner.timer.system import TimerSystem

    system = TimerSystem()
    assert system is not None
    assert hasattr(system, 'create_timer')
    assert hasattr(system, 'get_timer')
    assert hasattr(system, 'update')
