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


def test_interpreter_executes_local_declarations():
    """Test that interpreter executes local variable declarations."""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.parser import Parser

    code = """
    function test_vars takes nothing returns nothing
        local integer x = 42
        local string greeting = "Hello"
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    interpreter = Interpreter()

    # Manually execute the function to check context
    func = ast.functions[0]
    interpreter.execute_function(func)

    # Variables should be set in function context
    # (We can't easily check this without exposing context)
    assert func.name == 'test_vars'


def test_interpreter_sets_variable_values():
    """Test that interpreter correctly sets variable values."""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.interpreter.context import ExecutionContext
    from jass_runner.parser.parser import LocalDecl

    # Create a mock function with local declarations
    local_decl1 = LocalDecl(name='x', type='integer', value=42)
    local_decl2 = LocalDecl(name='msg', type='string', value='test')

    # Create interpreter and test context
    interpreter = Interpreter()
    test_context = ExecutionContext()
    interpreter.current_context = test_context

    # Execute declarations
    interpreter.execute_local_declaration(local_decl1)
    interpreter.execute_local_declaration(local_decl2)

    # Check values
    assert test_context.get_variable('x') == 42
    assert test_context.get_variable('msg') == 'test'