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
