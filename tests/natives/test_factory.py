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
    create_item_func = registry.get("CreateItem")
    remove_item_func = registry.get("RemoveItem")

    assert display_func is not None
    assert display_func.name == "DisplayTextToPlayer"

    assert kill_func is not None
    assert kill_func.name == "KillUnit"

    assert create_unit_func is not None
    assert create_unit_func.name == "CreateUnit"

    assert get_unit_state_func is not None
    assert get_unit_state_func.name == "GetUnitState"

    assert create_item_func is not None
    assert create_item_func.name == "CreateItem"

    assert remove_item_func is not None
    assert remove_item_func.name == "RemoveItem"

    # 检查Player原生函数已注册
    player_func = registry.get("Player")
    assert player_func is not None
    assert player_func.name == "Player"

    # 检查总数
    all_funcs = registry.get_all()
    assert len(all_funcs) == 7


def test_factory_with_timer_system():
    """测试工厂与计时器系统集成。"""
    from jass_runner.natives.factory import NativeFactory
    from jass_runner.timer.system import TimerSystem

    timer_system = TimerSystem()
    factory = NativeFactory(timer_system=timer_system)
    registry = factory.create_default_registry()

    # 检查计时器原生函数已注册
    create_timer_func = registry.get("CreateTimer")
    timer_start_func = registry.get("TimerStart")
    timer_elapsed_func = registry.get("TimerGetElapsed")

    assert create_timer_func is not None
    assert create_timer_func.name == "CreateTimer"

    assert timer_start_func is not None
    assert timer_start_func.name == "TimerStart"

    assert timer_elapsed_func is not None
    assert timer_elapsed_func.name == "TimerGetElapsed"