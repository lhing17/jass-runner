"""Test native function registry."""

def test_native_registry_creation():
    """Test that native registry can be created."""
    from jass_runner.natives.registry import NativeRegistry

    registry = NativeRegistry()
    assert registry is not None
    assert hasattr(registry, 'register')
    assert hasattr(registry, 'get')
    assert hasattr(registry, 'get_all')


def test_register_and_get_native_function():
    """Test registering and getting a native function."""
    from jass_runner.natives.registry import NativeRegistry
    from jass_runner.natives.basic import DisplayTextToPlayer

    registry = NativeRegistry()
    native = DisplayTextToPlayer()

    registry.register(native)

    retrieved = registry.get("DisplayTextToPlayer")
    assert retrieved is native
    assert retrieved.name == "DisplayTextToPlayer"