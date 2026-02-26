"""Native函数工厂测试。"""

def test_native_factory_creation():
    """测试NativeFactory可以被创建。"""
    from jass_runner.natives.factory import NativeFactory

    factory = NativeFactory()
    assert factory is not None
    assert hasattr(factory, 'create_default_registry')


def test_create_default_registry():
    """测试创建包含native函数的默认注册表。"""
    from jass_runner.natives.factory import NativeFactory

    factory = NativeFactory()
    registry = factory.create_default_registry()

    # 检查注册表已创建
    assert registry is not None

    # 检查native函数已注册
    display_func = registry.get("DisplayTextToPlayer")
    kill_func = registry.get("KillUnit")
    create_unit_func = registry.get("CreateUnit")
    get_unit_state_func = registry.get("GetUnitState")

    assert display_func is not None
    assert display_func.name == "DisplayTextToPlayer"

    assert kill_func is not None
    assert kill_func.name == "KillUnit"

    assert create_unit_func is not None
    assert create_unit_func.name == "CreateUnit"

    assert get_unit_state_func is not None
    assert get_unit_state_func.name == "GetUnitState"

    # 检查总数
    all_funcs = registry.get_all()
    assert len(all_funcs) == 4