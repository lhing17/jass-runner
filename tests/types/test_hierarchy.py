"""TypeHierarchy模块测试。"""


def test_is_subtype_unit_to_handle():
    """unit是handle的子类型。"""
    from jass_runner.types.hierarchy import TypeHierarchy

    assert TypeHierarchy.is_subtype('unit', 'handle') is True


def test_is_subtype_handle_to_unit():
    """handle不是unit的子类型。"""
    from jass_runner.types.hierarchy import TypeHierarchy

    assert TypeHierarchy.is_subtype('handle', 'unit') is False


def test_get_base_type_of_unit():
    """获取unit的基类型。"""
    from jass_runner.types.hierarchy import TypeHierarchy

    assert TypeHierarchy.get_base_type('unit') == 'handle'


def test_get_base_type_of_integer():
    """基础类型的基类型是其自身。"""
    from jass_runner.types.hierarchy import TypeHierarchy

    assert TypeHierarchy.get_base_type('integer') == 'integer'
