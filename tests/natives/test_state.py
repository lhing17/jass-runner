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
