"""Test JASS interpreter."""

def test_interpreter_can_execute_simple_script():
    """Test that interpreter can execute a simple script."""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.parser import Parser

    code = """
    function main takes nothing returns nothing
        local integer x = 42
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.execute(ast)

    # Should have executed without error
    assert True  # Just checking it doesn't crash


def test_interpreter_handles_local_variables():
    """Test that interpreter handles local variable declarations."""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.parser import Parser

    code = """
    function test takes nothing returns nothing
        local integer x = 10
        local string name = "test"
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.execute(ast)

    # Function should be registered
    assert 'test' in interpreter.functions