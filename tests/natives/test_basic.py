"""基础原生函数测试。"""

def test_display_text_to_player():
    """测试DisplayTextToPlayer原生函数。"""
    from jass_runner.natives.basic import DisplayTextToPlayer
    from jass_runner.natives.registry import NativeRegistry

    # 创建原生函数实例
    native = DisplayTextToPlayer()
    assert native.name == "DisplayTextToPlayer"

    # 测试执行
    result = native.execute(0, 0, 0, "Hello World")
    assert result is None  # DisplayTextToPlayer返回None


def test_kill_unit():
    """测试KillUnit原生函数。"""
    from jass_runner.natives.basic import KillUnit

    native = KillUnit()
    assert native.name == "KillUnit"

    # 使用单位标识符测试执行
    result = native.execute("footman_001")
    assert result is True  # KillUnit返回布尔值

    # 使用None单位测试执行
    result = native.execute(None)
    assert result is False


def test_create_unit():
    """测试CreateUnit原生函数。"""
    from jass_runner.natives.basic import CreateUnit

    native = CreateUnit()
    assert native.name == "CreateUnit"

    result = native.execute(0, 'hfoo', 0.0, 0.0, 0.0)
    assert isinstance(result, str)  # 返回单位标识符
    assert 'unit_' in result  # 生成的单位ID


def test_get_unit_state():
    """测试GetUnitState原生函数。"""
    from jass_runner.natives.basic import GetUnitState

    native = GetUnitState()
    assert native.name == "GetUnitState"

    # 测试获取生命值
    result = native.execute("footman_001", "UNIT_STATE_LIFE")
    assert isinstance(result, float)
    assert result > 0.0