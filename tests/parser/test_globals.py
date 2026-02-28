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


def test_global_decl_has_is_constant_attribute():
    """测试 GlobalDecl 节点具有 is_constant 属性。"""
    # 测试默认值
    decl = GlobalDecl(name='test_var', type='integer', value=100)
    assert hasattr(decl, 'is_constant')
    assert decl.is_constant is False

    # 测试显式设置为 True
    const_decl = GlobalDecl(name='MAX_SIZE', type='integer', value=100, is_constant=True)
    assert const_decl.is_constant is True
    assert const_decl.name == 'MAX_SIZE'
    assert const_decl.type == 'integer'
    assert const_decl.value == 100


def test_parse_constant_real_declaration():
    """测试解析 constant real 常量声明。"""
    code = """
globals
    constant real PI = 3.14159
endglobals

function main takes nothing returns nothing
endfunction
"""
    parser = Parser(code)
    ast = parser.parse()

    assert len(ast.globals) == 1
    assert ast.globals[0].name == 'PI'
    assert ast.globals[0].type == 'real'
    assert ast.globals[0].value == 3.14159
    assert ast.globals[0].is_constant is True


def test_parse_constant_without_initial_value_errors():
    """测试 constant 没有初始值时报错。"""
    code = """
globals
    constant integer MAX_SIZE
endglobals

function main takes nothing returns nothing
endfunction
"""
    parser = Parser(code)
    ast = parser.parse()

    # 应该记录错误
    assert len(parser.errors) > 0
    assert any('MAX_SIZE' in str(e) and '必须指定初始值' in str(e) for e in parser.errors)


def test_parse_set_constant_errors():
    """测试尝试修改 constant 时报错。"""
    code = """
globals
    constant integer MAX_SIZE = 100
endglobals

function test takes nothing returns nothing
    set MAX_SIZE = 200
endfunction
"""
    parser = Parser(code)
    ast = parser.parse()

    # 应该记录错误
    assert len(parser.errors) > 0
    assert any('MAX_SIZE' in str(e) and '不能修改常量' in str(e) for e in parser.errors)
