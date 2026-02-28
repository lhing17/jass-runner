"""测试表达式解析。"""

from jass_runner.parser.parser import Parser


def test_parse_array_access_expression():
    """测试解析数组访问表达式。"""
    code = """
function Test takes nothing returns nothing
    local integer x
    local integer array arr
    set x = arr[0]
endfunction
"""
    parser = Parser(code)
    result = parser.parse()
    func = result.functions[0]
    set_stmt = func.body[2]  # 第三个语句是set
    # 验证右侧是ArrayAccess节点
    from jass_runner.parser.ast_nodes import ArrayAccess
    assert isinstance(set_stmt.value, ArrayAccess)
    assert set_stmt.value.array_name == "arr"


def test_parse_array_access_with_variable_index():
    """测试解析带变量索引的数组访问。"""
    code = """
function Test takes nothing returns nothing
    local integer x
    local integer i
    local integer array arr
    set x = arr[i]
endfunction
"""
    parser = Parser(code)
    result = parser.parse()
    func = result.functions[0]
    set_stmt = func.body[3]  # 第四个语句是set
    from jass_runner.parser.ast_nodes import ArrayAccess, VariableExpr
    assert isinstance(set_stmt.value, ArrayAccess)
    assert set_stmt.value.array_name == "arr"
    assert isinstance(set_stmt.value.index, VariableExpr)
    assert set_stmt.value.index.name == "i"
