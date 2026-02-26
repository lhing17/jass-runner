"""Handle基类测试。"""


def test_handle_base_class():
    """测试Handle基类的创建和基本属性。"""
    from jass_runner.natives.handle import Handle

    # 创建Handle实例
    handle = Handle("test_001", "test_type")

    # 验证基本属性
    assert handle.id == "test_001"
    assert handle.type_name == "test_type"
    assert handle.alive is True
    assert handle.is_alive() is True


def test_handle_destroy():
    """测试Handle销毁功能。"""
    from jass_runner.natives.handle import Handle

    handle = Handle("test_002", "test_type")
    assert handle.is_alive() is True

    # 销毁handle
    handle.destroy()
    assert handle.alive is False
    assert handle.is_alive() is False
