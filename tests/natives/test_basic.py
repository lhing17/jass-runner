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