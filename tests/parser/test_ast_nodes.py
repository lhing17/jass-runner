"""AST节点测试。

此模块包含JASS解析器AST节点的单元测试。
"""


def test_array_decl_node_exists():
    """测试ArrayDecl节点存在并可正确创建。"""
    from jass_runner.parser.ast_nodes import ArrayDecl
    node = ArrayDecl(name="counts", element_type="integer",
                     is_global=True, is_constant=False)
    assert node.name == "counts"
    assert node.element_type == "integer"
    assert node.is_global is True
    assert node.is_constant is False


def test_array_access_node_exists():
    """测试ArrayAccess节点存在并可正确创建。"""
    from jass_runner.parser.ast_nodes import ArrayAccess
    node = ArrayAccess(array_name="counts", index=0)
    assert node.array_name == "counts"
    assert node.index == 0


def test_set_array_stmt_node_exists():
    """测试SetArrayStmt节点存在并可正确创建。"""
    from jass_runner.parser.ast_nodes import SetArrayStmt, IntegerExpr
    index = IntegerExpr(value=5)
    value = IntegerExpr(value=10)
    node = SetArrayStmt(array_name="counts", index=index, value=value)
    assert node.array_name == "counts"
    assert node.index == index
    assert node.value == value
