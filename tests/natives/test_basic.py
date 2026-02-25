"""Test basic native functions."""

def test_display_text_to_player():
    """Test DisplayTextToPlayer native function."""
    from jass_runner.natives.basic import DisplayTextToPlayer
    from jass_runner.natives.registry import NativeRegistry

    # Create native function instance
    native = DisplayTextToPlayer()
    assert native.name == "DisplayTextToPlayer"

    # Test execution
    result = native.execute(0, 0, 0, "Hello World")
    assert result is None  # DisplayTextToPlayer returns nothing


def test_kill_unit():
    """Test KillUnit native function."""
    from jass_runner.natives.basic import KillUnit

    native = KillUnit()
    assert native.name == "KillUnit"

    # Test execution with unit identifier
    result = native.execute("footman_001")
    assert result is True  # KillUnit returns boolean

    # Test execution with None unit
    result = native.execute(None)
    assert result is False