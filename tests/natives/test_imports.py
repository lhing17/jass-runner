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
