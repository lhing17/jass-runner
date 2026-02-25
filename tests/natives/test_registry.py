"""Test native function registry."""

def test_native_registry_creation():
    """Test that native registry can be created."""
    from jass_runner.natives.registry import NativeRegistry

    registry = NativeRegistry()
    assert registry is not None
    assert hasattr(registry, 'register')
    assert hasattr(registry, 'get')
    assert hasattr(registry, 'get_all')