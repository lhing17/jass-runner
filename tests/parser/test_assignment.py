"""测试局部变量和赋值解析。"""

from jass_runner.parser.parser import Parser


def test_parse_local_integer_array():
    """测试解析局部整数数组声明。"""
    from jass_runner.parser.ast_nodes import ArrayDecl
    code = """
function Test takes nothing returns nothing
    local integer array temp
endfunction
"""
    parser = Parser(code)
    result = parser.parse()
    func = result.functions[0]
    # local声明存储在body中
    local_decls = [stmt for stmt in func.body if isinstance(stmt, ArrayDecl)]
    assert len(local_decls) == 1
    assert local_decls[0].name == "temp"
    assert local_decls[0].element_type == "integer"
    assert local_decls[0].is_global is False
