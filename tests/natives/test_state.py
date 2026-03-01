"""StateContext测试。"""


def test_state_context_creation():
    """测试StateContext创建和基本属性。"""
    from jass_runner.natives.state import StateContext

    context = StateContext()
    assert context.handle_manager is not None
    assert context.global_vars == {}
    assert context.local_stores == {}


def test_state_context_has_trigger_manager():
    """测试StateContext包含trigger_manager属性。"""
    from jass_runner.natives.state import StateContext
    from jass_runner.trigger.manager import TriggerManager

    context = StateContext()
    assert hasattr(context, 'trigger_manager')
    assert isinstance(context.trigger_manager, TriggerManager)


def test_state_context_trigger_manager_functionality():
    """测试StateContext的trigger_manager可以创建触发器和触发事件。"""
    from jass_runner.natives.state import StateContext

    context = StateContext()

    # 测试创建触发器
    trigger_id = context.trigger_manager.create_trigger()
    assert trigger_id is not None
    assert trigger_id.startswith("trigger_")

    # 测试获取触发器
    trigger = context.trigger_manager.get_trigger(trigger_id)
    assert trigger is not None

    # 测试注册事件
    event_handle = context.trigger_manager.register_event(trigger_id, "unit_death")
    assert event_handle is not None

    # 测试触发事件（不抛出异常即可）
    context.trigger_manager.fire_event("unit_death", {"unit": "test_unit"})


def test_state_context_get_context_store():
    """测试StateContext获取上下文存储功能。"""
    from jass_runner.natives.state import StateContext

    context = StateContext()

    # 获取不存在的上下文存储
    store = context.get_context_store("test_context")
    assert store == {}

    # 验证存储已创建
    assert "test_context" in context.local_stores
    assert context.local_stores["test_context"] == {}

    # 修改存储并验证
    store["key"] = "value"
    assert context.local_stores["test_context"]["key"] == "value"

    # 再次获取相同上下文存储
    store2 = context.get_context_store("test_context")
    assert store2["key"] == "value"


def test_state_context_handle_manager_triggers_events():
    """测试kill_unit能触发TriggerManager的事件。

    完整流程：
    1. 创建触发器
    2. 注册单位死亡事件监听
    3. 创建单位
    4. 杀死单位（触发事件）
    5. 验证动作执行
    """
    from jass_runner.natives.state import StateContext
    from jass_runner.trigger.event_types import EVENT_UNIT_DEATH

    context = StateContext()

    # 跟踪回调是否被调用
    callbacks_called = []

    def mock_callback(state_context):
        """模拟回调函数。"""
        callbacks_called.append(state_context)

    # 创建触发器
    trigger_id = context.trigger_manager.create_trigger()
    trigger = context.trigger_manager.get_trigger(trigger_id)

    # 注册事件监听
    context.trigger_manager.register_event(trigger_id, EVENT_UNIT_DEATH)

    # 添加动作
    trigger.add_action(mock_callback)

    # 创建一个单位
    unit = context.handle_manager.create_unit("footman", 0, 100.0, 100.0, 0.0)
    unit_id = unit.id
    unit_type = unit.unit_type

    # 杀死单位（应触发事件）
    result = context.handle_manager.kill_unit(unit_id)
    assert result is True

    # 验证事件触发了回调
    assert len(callbacks_called) == 1
    assert callbacks_called[0]["event_data"] == {
        "unit_id": unit_id,
        "unit_type": unit_type
    }


def test_state_context_kill_unit_no_trigger_manager():
    """测试在没有TriggerManager连接时kill_unit仍能工作。"""
    from jass_runner.natives.manager import HandleManager

    # 单独创建HandleManager（没有连接到TriggerManager）
    handle_manager = HandleManager()

    # 创建单位
    unit = handle_manager.create_unit("footman", 0, 100.0, 100.0, 0.0)
    unit_id = unit.id

    # 杀死单位（不抛出异常即可）
    result = handle_manager.kill_unit(unit_id)
    assert result is True

    # 验证单位已死亡
    assert not unit.is_alive()
