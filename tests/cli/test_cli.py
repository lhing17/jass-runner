"""测试命令行接口。"""

def test_cli_parser_creation():
    """测试 CLI 参数解析器可以被创建。"""
    from jass_runner.cli import create_parser

    parser = create_parser()
    assert parser is not None
    assert hasattr(parser, 'parse_args')
