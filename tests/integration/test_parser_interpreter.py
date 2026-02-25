"""Integration tests for parser and interpreter."""

def test_end_to_end_simple_script():
    """Test end-to-end parsing and execution of simple script."""
    from jass_runner.parser.parser import Parser
    from jass_runner.interpreter.interpreter import Interpreter

    code = """
    function main takes nothing returns nothing
        local integer answer = 42
        local string message = "Hello, World!"
    endfunction
    """

    # Parse
    parser = Parser(code)
    ast = parser.parse()

    # Execute
    interpreter = Interpreter()
    interpreter.execute(ast)

    # Verify
    assert len(ast.functions) == 1
    assert ast.functions[0].name == 'main'
    assert 'main' in interpreter.functions

    # Check that function has body with statements
    func = interpreter.functions['main']
    assert func.body is not None
    assert len(func.body) == 2