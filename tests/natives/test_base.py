"""Test native function base class."""

def test_native_function_base_class():
    """Test that NativeFunction base class can be created."""
    from jass_runner.natives.base import NativeFunction

    # Test abstract class cannot be instantiated
    import pytest
    with pytest.raises(TypeError):
        NativeFunction()

    # Test abstract methods exist
    assert hasattr(NativeFunction, 'name')
    assert hasattr(NativeFunction, 'execute')