"""Native函数工厂测试。"""


def test_all_trigger_natives_registered():
    """测试所有触发器Native函数已注册。"""
    from jass_runner.natives.factory import NativeFactory
    from jass_runner.natives.trigger_natives import (
        CreateTrigger, DestroyTrigger, EnableTrigger, DisableTrigger,
        IsTriggerEnabled,
        TriggerAddAction, TriggerRemoveAction, TriggerClearActions,
        TriggerAddCondition, TriggerRemoveCondition, TriggerClearConditions,
        TriggerEvaluate, TriggerClearEvents,
    )
    from jass_runner.natives.trigger_register_event_natives import (
        TriggerRegisterTimerEvent, TriggerRegisterTimerExpireEvent,
        TriggerRegisterPlayerUnitEvent, TriggerRegisterUnitEvent,
        TriggerRegisterPlayerEvent, TriggerRegisterGameEvent,
    )

    factory = NativeFactory()
    registry = factory.create_default_registry()

    # 定义所有触发器函数名称
    trigger_natives = [
        "CreateTrigger",
        "DestroyTrigger",
        "EnableTrigger",
        "DisableTrigger",
        "IsTriggerEnabled",
        "TriggerAddAction",
        "TriggerRemoveAction",
        "TriggerClearActions",
        "TriggerAddCondition",
        "TriggerRemoveCondition",
        "TriggerClearConditions",
        "TriggerEvaluate",
        "TriggerClearEvents",
        "TriggerRegisterTimerEvent",
        "TriggerRegisterTimerExpireEvent",
        "TriggerRegisterPlayerUnitEvent",
        "TriggerRegisterUnitEvent",
        "TriggerRegisterPlayerEvent",
        "TriggerRegisterGameEvent",
    ]

    # 验证所有函数已注册且类型正确
    expected_classes = {
        "CreateTrigger": CreateTrigger,
        "DestroyTrigger": DestroyTrigger,
        "EnableTrigger": EnableTrigger,
        "DisableTrigger": DisableTrigger,
        "IsTriggerEnabled": IsTriggerEnabled,
        "TriggerAddAction": TriggerAddAction,
        "TriggerRemoveAction": TriggerRemoveAction,
        "TriggerClearActions": TriggerClearActions,
        "TriggerAddCondition": TriggerAddCondition,
        "TriggerRemoveCondition": TriggerRemoveCondition,
        "TriggerClearConditions": TriggerClearConditions,
        "TriggerEvaluate": TriggerEvaluate,
        "TriggerClearEvents": TriggerClearEvents,
        "TriggerRegisterTimerEvent": TriggerRegisterTimerEvent,
        "TriggerRegisterTimerExpireEvent": TriggerRegisterTimerExpireEvent,
        "TriggerRegisterPlayerUnitEvent": TriggerRegisterPlayerUnitEvent,
        "TriggerRegisterUnitEvent": TriggerRegisterUnitEvent,
        "TriggerRegisterPlayerEvent": TriggerRegisterPlayerEvent,
        "TriggerRegisterGameEvent": TriggerRegisterGameEvent,
    }

    for func_name in trigger_natives:
        func = registry.get(func_name)
        assert func is not None, f"触发器函数 {func_name} 未注册"
        assert func.name == func_name, f"函数名称不匹配: {func.name} != {func_name}"
        assert isinstance(func, expected_classes[func_name]), \
            f"函数 {func_name} 类型错误: 期望 {expected_classes[func_name]}, 实际 {type(func)}"


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

    # 检查基础函数数量（7个基础 + 19个触发器 + 15个数学 + 2个异步 + 14个单位操作 + 8个单位组 + 7个技能 = 72）
    all_funcs = registry.get_all()
    assert len(all_funcs) == 72


def test_all_math_natives_registered():
    """测试所有数学Native函数已注册。"""
    from jass_runner.natives.factory import NativeFactory
    from jass_runner.natives.math_core import (
        SquareRoot, Pow, Cos, Sin, R2I, I2R,
    )
    from jass_runner.natives.math_extended import (
        Tan, ModuloInteger, ModuloReal, R2S, S2R, I2S, S2I, GetRandomInt, GetRandomReal,
    )

    factory = NativeFactory()
    registry = factory.create_default_registry()

    # 数学函数名称列表（15个）
    math_names = [
        "SquareRoot", "Pow", "Cos", "Sin", "R2I", "I2R",
        "Tan", "ModuloInteger", "ModuloReal", "R2S", "S2R", "I2S", "S2I",
        "GetRandomInt", "GetRandomReal",
    ]

    # 预期的类映射
    expected_classes = {
        "SquareRoot": SquareRoot,
        "Pow": Pow,
        "Cos": Cos,
        "Sin": Sin,
        "R2I": R2I,
        "I2R": I2R,
        "Tan": Tan,
        "ModuloInteger": ModuloInteger,
        "ModuloReal": ModuloReal,
        "R2S": R2S,
        "S2R": S2R,
        "I2S": I2S,
        "S2I": S2I,
        "GetRandomInt": GetRandomInt,
        "GetRandomReal": GetRandomReal,
    }

    # 验证所有函数已注册
    for name in math_names:
        func = registry.get(name)
        assert func is not None, f"数学函数 {name} 未注册"
        assert func.name == name, f"函数名称不匹配: {func.name} != {name}"
        assert isinstance(func, expected_classes[name]), \
            f"函数 {name} 类型错误: 期望 {expected_classes[name]}, 实际 {type(func)}"


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


def test_factory_registers_async_natives():
    """测试工厂注册异步 native 函数。"""
    from jass_runner.natives.factory import NativeFactory
    from jass_runner.natives.async_natives import TriggerSleepAction, ExecuteFunc

    factory = NativeFactory()
    registry = factory.create_default_registry()

    # 检查异步原生函数已注册
    sleep_action = registry.get("TriggerSleepAction")
    execute_func = registry.get("ExecuteFunc")

    assert sleep_action is not None
    assert sleep_action.name == "TriggerSleepAction"
    assert isinstance(sleep_action, TriggerSleepAction)

    assert execute_func is not None
    assert execute_func.name == "ExecuteFunc"
    assert isinstance(execute_func, ExecuteFunc)