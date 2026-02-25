"""Test native function factory."""

def test_native_factory_creation():
    """Test that native factory can be created."""
    from jass_runner.natives.factory import NativeFactory

    factory = NativeFactory()
    assert factory is not None
    assert hasattr(factory, 'create_default_registry')


def test_create_default_registry():
    """Test creating default registry with native functions."""
    from jass_runner.natives.factory import NativeFactory

    factory = NativeFactory()
    registry = factory.create_default_registry()

    # Check registry is created
    assert registry is not None

    # Check native functions are registered
    display_func = registry.get("DisplayTextToPlayer")
    kill_func = registry.get("KillUnit")

    assert display_func is not None
    assert display_func.name == "DisplayTextToPlayer"

    assert kill_func is not None
    assert kill_func.name == "KillUnit"

    # Check total count
    all_funcs = registry.get_all()
    assert len(all_funcs) == 2