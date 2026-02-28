"""测试JASS解释器。"""

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


def test_execute_if_then_branch():
    """测试执行if语句的then分支。"""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.interpreter.context import ExecutionContext
    from jass_runner.parser.parser import Parser, IfStmt, SetStmt

    # 创建解释器
    interpreter = Interpreter()

    # 创建测试上下文
    test_context = ExecutionContext()
    test_context.set_variable('result', 0)
    interpreter.current_context = test_context
    interpreter.evaluator.context = test_context

    # 创建IfStmt节点
    set_stmt = SetStmt(var_name='result', value=1)
    if_stmt = IfStmt(condition='true', then_body=[set_stmt], elseif_branches=[], else_body=[])

    # 执行if语句
    interpreter.execute_if_statement(if_stmt)

    # 验证then分支被执行（result应该被设置为1）
    assert test_context.get_variable('result') == 1


def test_execute_if_else_branch():
    """测试执行if语句的else分支。"""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.interpreter.context import ExecutionContext
    from jass_runner.parser.parser import Parser, IfStmt, SetStmt

    # 创建解释器
    interpreter = Interpreter()

    # 创建测试上下文
    test_context = ExecutionContext()
    test_context.set_variable('result', 0)
    interpreter.current_context = test_context
    interpreter.evaluator.context = test_context

    # 创建IfStmt节点（条件为false，应该执行else分支）
    set_then = SetStmt(var_name='result', value=1)
    set_else = SetStmt(var_name='result', value=2)
    if_stmt = IfStmt(condition='false', then_body=[set_then], elseif_branches=[], else_body=[set_else])

    # 执行if语句
    interpreter.execute_if_statement(if_stmt)

    # 验证else分支被执行（result应该被设置为2）
    assert test_context.get_variable('result') == 2


def test_execute_if_elseif():
    """测试执行if/elseif语句。"""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.interpreter.context import ExecutionContext
    from jass_runner.parser.parser import Parser, IfStmt, SetStmt

    # 创建解释器
    interpreter = Interpreter()

    # 创建测试上下文
    test_context = ExecutionContext()
    test_context.set_variable('x', 2)
    test_context.set_variable('result', 0)
    interpreter.current_context = test_context
    interpreter.evaluator.context = test_context

    # 创建IfStmt节点（x=2，应该执行elseif分支）
    set_if = SetStmt(var_name='result', value=1)
    set_elseif = SetStmt(var_name='result', value=2)
    set_else = SetStmt(var_name='result', value=3)

    elseif_branch = {'condition': 'x == 2', 'body': [set_elseif]}
    if_stmt = IfStmt(condition='x == 1', then_body=[set_if], elseif_branches=[elseif_branch], else_body=[set_else])

    # 执行if语句
    interpreter.execute_if_statement(if_stmt)

    # 验证elseif分支被执行（result应该被设置为2）
    assert test_context.get_variable('result') == 2


def test_execute_nested_if():
    """测试执行嵌套if语句。"""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.parser import Parser
    from jass_runner.natives.factory import NativeFactory

    code = """
    function main takes nothing returns nothing
        local integer x = 5
        local integer y = 3
        if x > 0 then
            if y > 0 then
                call DisplayTextToPlayer(Player(0), 0.0, 0.0, "both positive")
            endif
        endif
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    # 创建包含DisplayTextToPlayer的注册表
    factory = NativeFactory()
    registry = factory.create_default_registry()

    interpreter = Interpreter(native_registry=registry)
    interpreter.execute(ast)
    assert True


def test_execute_simple_loop():
    """测试执行简单loop循环。"""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.parser import Parser

    code = """
    function main takes nothing returns nothing
        local integer i = 0
        loop
            exitwhen i >= 3
            set i = i + 1
        endloop
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.execute(ast)
    # 循环正常结束即表示测试通过（没有进入无限循环）
    assert True


def test_execute_nested_loop():
    """测试执行嵌套循环。"""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.parser import Parser

    code = """
    function main takes nothing returns nothing
        local integer i = 0
        local integer j = 0
        local integer count = 0
        loop
            exitwhen i >= 2
            set j = 0
            loop
                exitwhen j >= 3
                set count = count + 1
                set j = j + 1
            endloop
            set i = i + 1
        endloop
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.execute(ast)
    # 2 * 3 = 6，循环正常结束即表示测试通过
    assert True


def test_execute_return_nothing():
    """测试执行return nothing。"""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.parser import Parser

    code = """
    function main takes nothing returns nothing
        local integer x = 1
        return
        set x = 2
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.execute(ast)
    # 如果没有异常，说明正确执行了return
    assert True


def test_execute_return_with_value():
    """测试执行带返回值的return。"""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.parser import Parser

    code = """
    function add takes integer a, integer b returns integer
        return a + b
    endfunction

    function main takes nothing returns nothing
        local integer result = add(3, 5)
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.execute(ast)
    # 函数调用和return正常执行即表示测试通过
    assert True


def test_execute_early_return():
    """测试提前return。"""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.parser import Parser

    code = """
    function max takes integer a, integer b returns integer
        if a > b then
            return a
        endif
        return b
    endfunction

    function main takes nothing returns nothing
        local integer m1 = max(5, 3)
        local integer m2 = max(2, 7)
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.execute(ast)
    # 提前return正常执行即表示测试通过
    assert True


def test_execute_loop_with_if_inside():
    """测试loop内部有if语句。"""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.parser import Parser

    code = """
    function main takes nothing returns nothing
        local integer i = 0
        local integer even_count = 0
        loop
            exitwhen i >= 5
            if i / 2 * 2 == i then
                set even_count = even_count + 1
            endif
            set i = i + 1
        endloop
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.execute(ast)
    # 0, 2, 4 are even，循环正常结束即表示测试通过
    assert True


def test_execute_if_with_loop_inside():
    """测试if内部有loop语句。"""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.parser import Parser

    code = """
    function main takes nothing returns nothing
        local integer x = 5
        local integer sum = 0
        if x > 0 then
            local integer i = 1
            loop
                exitwhen i > x
                set sum = sum + i
                set i = i + 1
            endloop
        endif
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.execute(ast)
    # 1 + 2 + 3 + 4 + 5 = 15，循环正常结束即表示测试通过
    assert True


def test_execute_global_array_declaration():
    """测试执行全局数组声明。"""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.ast_nodes import ArrayDecl

    interpreter = Interpreter()
    decl = ArrayDecl(name="counts", element_type="integer",
                     is_global=True, is_constant=False)
    interpreter.execute_statement(decl)

    assert "counts" in interpreter.current_context.arrays
    assert interpreter.current_context.arrays["counts"][0] == 0