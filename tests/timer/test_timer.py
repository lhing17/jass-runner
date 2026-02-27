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
