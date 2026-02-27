"""Test timer-related native functions."""

def test_create_timer_native():
    """Test CreateTimer native function."""
    from jass_runner.natives.timer_natives import CreateTimer
    from jass_runner.timer.system import TimerSystem

    system = TimerSystem()
    native = CreateTimer(timer_system=system)
    assert native.name == "CreateTimer"

    # Create a timer (pass None as state_context for testing)
    timer_id = native.execute(None)
    assert timer_id is not None
    assert timer_id.startswith("timer_")

    # Verify timer exists in system
    timer = system.get_timer(timer_id)
    assert timer is not None
