"""Interpreter类型检查集成测试。"""

import pytest
from jass_runner.types.errors import JassTypeError


def test_local_declaration_with_type_check():
    """测试局部变量声明的类型检查。"""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.ast_nodes import LocalDecl

    interpreter = Interpreter()

    # local integer x = 10
    decl = LocalDecl(name='x', type='integer', value=10)
    interpreter.execute_local_declaration(decl)

    assert interpreter.current_context.get_variable('x') == 10
    assert interpreter.current_context.get_variable_type('x') == 'integer'


def test_set_statement_type_mismatch_raises():
    """测试set语句类型不匹配抛出异常。"""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.ast_nodes import LocalDecl, SetStmt

    interpreter = Interpreter()

    # local integer x = 10
    decl = LocalDecl(name='x', type='integer', value=10)
    interpreter.execute_local_declaration(decl)

    # set x = "hello" - 应该抛出类型错误
    set_stmt = SetStmt(var_name='x', value='hello')

    with pytest.raises(JassTypeError):
        interpreter.execute_set_statement(set_stmt)


def test_integer_to_real_implicit_conversion():
    """测试integer到real的隐式转换。"""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.ast_nodes import LocalDecl, SetStmt

    interpreter = Interpreter()

    # local real r = 10
    decl = LocalDecl(name='r', type='real', value=10)
    interpreter.execute_local_declaration(decl)

    assert interpreter.current_context.get_variable('r') == 10.0
    assert isinstance(interpreter.current_context.get_variable('r'), float)


def test_function_call_with_type_check():
    """测试函数调用时的参数类型检查。"""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.ast_nodes import FunctionDecl, Parameter, ReturnStmt

    interpreter = Interpreter()

    # 定义函数: function add takes integer a, integer b returns integer
    func = FunctionDecl(
        name='add',
        parameters=[
            Parameter(name='a', type='integer', line=1, column=1),
            Parameter(name='b', type='integer', line=1, column=1)
        ],
        return_type='integer',
        line=1,
        column=1,
        body=[ReturnStmt(value='a + b')]
    )

    interpreter.functions['add'] = func

    # 调用 add(1, 2)
    result = interpreter._call_function_with_args(func, [1, 2])

    assert result == 3


def test_function_call_type_mismatch_raises():
    """测试函数调用参数类型不匹配抛出异常。"""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.ast_nodes import FunctionDecl, Parameter

    interpreter = Interpreter()

    # 定义函数: function foo takes integer x returns nothing
    func = FunctionDecl(
        name='foo',
        parameters=[Parameter(name='x', type='integer', line=1, column=1)],
        return_type='nothing',
        line=1,
        column=1,
        body=[]
    )

    # 调用 foo("hello") - 应该抛出类型错误
    with pytest.raises(JassTypeError):
        interpreter._call_function_with_args(func, ['hello'])
