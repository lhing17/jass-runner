"""StateContext测试。"""


def test_state_context_creation():
    """测试StateContext创建和基本属性。"""
    from jass_runner.natives.state import StateContext

    context = StateContext()
    assert context.handle_manager is not None
    assert context.global_vars == {}
    assert context.local_stores == {}


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
