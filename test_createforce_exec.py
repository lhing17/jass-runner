"""测试 CreateForce 执行问题。"""

import sys
sys.path.insert(0, 'src')

from jass_runner.parser.lexer import Lexer
from jass_runner.parser.parser import Parser
from jass_runner.interpreter.interpreter import Interpreter
from jass_runner.natives.factory import NativeFactory

# 测试代码
code = '''
globals
    force bj_FORCE_ALL_PLAYERS
endglobals

function Test takes nothing returns nothing
    set bj_FORCE_ALL_PLAYERS = CreateForce()
endfunction
'''

# 解析
parser = Parser(code)
ast = parser.parse()

print("AST:")
for func in ast.functions:
    print(f"  Function: {func.name}")
    for stmt in func.body:
        print(f"    Statement: {stmt}")
        if hasattr(stmt, 'value'):
            print(f"      Value type: {type(stmt.value).__name__}")
            print(f"      Value: {stmt.value}")

print("\n" + "="*50)

# 执行
factory = NativeFactory()
registry = factory.create_default_registry()
interpreter = Interpreter(native_registry=registry)

print("\n执行:")
try:
    interpreter.execute(ast)
    print("AST 执行成功!")
    # 调用 Test 函数
    from jass_runner.parser.parser import FunctionDecl
    test_func = None
    for func in ast.functions:
        if isinstance(func, FunctionDecl) and func.name == "Test":
            test_func = func
            break

    if test_func:
        print("调用 Test 函数...")
        interpreter.execute_function(test_func)
        print("Test 函数执行成功!")

    # 检查变量值
    print("Checking variable 'bj_FORCE_ALL_PLAYERS'...")
    print(f"Variables in global_context: {interpreter.global_context.variables}")
    force_value = interpreter.global_context.get_variable('bj_FORCE_ALL_PLAYERS')
    print(f"bj_FORCE_ALL_PLAYERS = {force_value}")
except Exception as e:
    print(f"执行错误: {e}")
    import traceback
    traceback.print_exc()
