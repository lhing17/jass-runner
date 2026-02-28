"""测试全局变量解析。"""

from jass_runner.parser.parser import Parser, GlobalDecl


def test_parse_globals_with_initial_values():
    """测试解析带初始值的全局变量。"""
    code = """
globals
    integer global_counter = 0
    real global_x = 1.5
    string app_name = "test"
    boolean is_enabled = true
endglobals

function main takes nothing returns nothing
endfunction
"""
    parser = Parser(code)
    ast = parser.parse()

    assert len(ast.globals) == 4
    assert ast.globals[0].name == 'global_counter'
    assert ast.globals[0].type == 'integer'
    assert ast.globals[0].value == 0
    assert ast.globals[1].name == 'global_x'
    assert ast.globals[1].type == 'real'
    assert ast.globals[1].value == 1.5
    assert ast.globals[2].name == 'app_name'
    assert ast.globals[2].type == 'string'
    assert ast.globals[2].value == 'test'
    assert ast.globals[3].name == 'is_enabled'
    assert ast.globals[3].type == 'boolean'
    assert ast.globals[3].value == True


def test_parse_globals_without_initial_values():
    """测试解析无初始值的全局变量。"""
    code = """
globals
    integer count
    real value
endglobals

function main takes nothing returns nothing
endfunction
"""
    parser = Parser(code)
    ast = parser.parse()

    assert len(ast.globals) == 2
    assert ast.globals[0].name == 'count'
    assert ast.globals[0].type == 'integer'
    assert ast.globals[0].value is None
    assert ast.globals[1].name == 'value'
    assert ast.globals[1].type == 'real'
    assert ast.globals[1].value is None


def test_parse_empty_globals():
    """测试解析空的 globals 块。"""
    code = """
globals
endglobals

function main takes nothing returns nothing
endfunction
"""
    parser = Parser(code)
    ast = parser.parse()

    assert len(ast.globals) == 0


def test_parse_no_globals():
    """测试没有 globals 块的代码。"""
    code = """
function main takes nothing returns nothing
endfunction
"""
    parser = Parser(code)
    ast = parser.parse()

    assert len(ast.globals) == 0
    assert len(ast.functions) == 1


def test_local_variable_name_conflict_with_global():
    """测试局部变量与全局变量同名时报错。"""
    code = """
globals
    integer counter = 0
endglobals

function main takes nothing returns nothing
    local integer counter = 1
endfunction
"""
    parser = Parser(code)
    ast = parser.parse()

    # 应该记录错误
    assert len(parser.errors) > 0
    assert any("counter" in str(e) and "同名" in str(e) for e in parser.errors)
