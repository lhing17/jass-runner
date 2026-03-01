"""natives模块导入测试。"""


def test_natives_module_imports():
    """测试natives模块的所有导出。"""
    # 测试基础导入
    from jass_runner.natives import NativeFunction, NativeRegistry, NativeFactory

    # 测试新模块导入
    from jass_runner.natives import Handle, Unit, HandleManager, StateContext

    # 验证类型
    assert NativeFunction is not None
    assert NativeRegistry is not None
    assert NativeFactory is not None
    assert Handle is not None
    assert Unit is not None
    assert HandleManager is not None
    assert StateContext is not None


def test_trigger_natives_imports():
    """测试所有触发器Native函数可以从jass_runner.natives导入。"""
    # 从natives模块导入所有触发器类
    from jass_runner.natives import (
        CreateTrigger, DestroyTrigger, EnableTrigger, DisableTrigger,
        IsTriggerEnabled, TriggerAddAction, TriggerRemoveAction, TriggerClearActions,
        TriggerAddCondition, TriggerRemoveCondition, TriggerClearConditions,
        TriggerEvaluate, TriggerRegisterTimerEvent, TriggerRegisterTimerExpireEvent,
        TriggerRegisterPlayerUnitEvent, TriggerRegisterUnitEvent,
        TriggerRegisterPlayerEvent, TriggerRegisterGameEvent, TriggerClearEvents,
    )

    # 验证所有类都已成功导入（不为None）
    assert CreateTrigger is not None
    assert DestroyTrigger is not None
    assert EnableTrigger is not None
    assert DisableTrigger is not None
    assert IsTriggerEnabled is not None
    assert TriggerAddAction is not None
    assert TriggerRemoveAction is not None
    assert TriggerClearActions is not None
    assert TriggerAddCondition is not None
    assert TriggerRemoveCondition is not None
    assert TriggerClearConditions is not None
    assert TriggerEvaluate is not None
    assert TriggerRegisterTimerEvent is not None
    assert TriggerRegisterTimerExpireEvent is not None
    assert TriggerRegisterPlayerUnitEvent is not None
    assert TriggerRegisterUnitEvent is not None
    assert TriggerRegisterPlayerEvent is not None
    assert TriggerRegisterGameEvent is not None
    assert TriggerClearEvents is not None

    # 验证每个类都可以实例化（base类验证）
    from jass_runner.natives import NativeFunction

    assert issubclass(CreateTrigger, NativeFunction)
    assert issubclass(DestroyTrigger, NativeFunction)
    assert issubclass(EnableTrigger, NativeFunction)
    assert issubclass(DisableTrigger, NativeFunction)
    assert issubclass(IsTriggerEnabled, NativeFunction)
    assert issubclass(TriggerAddAction, NativeFunction)
    assert issubclass(TriggerRemoveAction, NativeFunction)
    assert issubclass(TriggerClearActions, NativeFunction)
    assert issubclass(TriggerAddCondition, NativeFunction)
    assert issubclass(TriggerRemoveCondition, NativeFunction)
    assert issubclass(TriggerClearConditions, NativeFunction)
    assert issubclass(TriggerEvaluate, NativeFunction)
    assert issubclass(TriggerRegisterTimerEvent, NativeFunction)
    assert issubclass(TriggerRegisterTimerExpireEvent, NativeFunction)
    assert issubclass(TriggerRegisterPlayerUnitEvent, NativeFunction)
    assert issubclass(TriggerRegisterUnitEvent, NativeFunction)
    assert issubclass(TriggerRegisterPlayerEvent, NativeFunction)
    assert issubclass(TriggerRegisterGameEvent, NativeFunction)
    assert issubclass(TriggerClearEvents, NativeFunction)
