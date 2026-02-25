"""Integration tests for basic parsing."""

def test_parse_example_script():
    """Test parsing the example script."""
    from src.jass_runner.parser.parser import Parser

    with open('examples/hello_world.j', 'r', encoding='utf-8') as f:
        code = f.read()

    parser = Parser(code)
    ast = parser.parse()

    # Should find the main function
    assert len(ast.functions) == 1
    assert ast.functions[0].name == 'main'
    assert ast.functions[0].return_type == 'nothing'
    assert len(ast.functions[0].parameters) == 0