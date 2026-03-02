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
