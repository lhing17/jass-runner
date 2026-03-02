"""ExecutionContext类型跟踪功能测试。"""


def test_set_variable_with_type():
    """测试带类型信息的变量设置。"""
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    context.set_variable('x', 10, 'integer')

    assert context.get_variable('x') == 10
    assert context.get_variable_type('x') == 'integer'


def test_get_variable_type_from_parent():
    """测试从父上下文获取变量类型。"""
    from jass_runner.interpreter.context import ExecutionContext

    parent = ExecutionContext()
    parent.set_variable('x', 10, 'integer')

    child = ExecutionContext(parent)
    assert child.get_variable_type('x') == 'integer'


def test_declare_array_stores_type():
    """测试数组声明存储元素类型。"""
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    context.declare_array('arr', 'real')

    assert context.get_array_type('arr') == 'real'
