def test_jass_type_error_creation():
    """测试JassTypeError异常创建。"""
    from jass_runner.types.errors import JassTypeError

    error = JassTypeError(
        message="类型错误测试",
        source_type="string",
        target_type="integer",
        line=5,
        column=10
    )

    assert str(error) == "类型错误测试"
    assert error.source_type == "string"
    assert error.target_type == "integer"
    assert error.line == 5
    assert error.column == 10
