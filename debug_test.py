"""调试脚本：测试原生函数调用解析和执行。"""

import logging
from jass_runner.parser.parser import Parser
from jass_runner.natives.factory import NativeFactory
from jass_runner.natives.state import StateContext

# 启用调试日志
logging.basicConfig(level=logging.DEBUG)

jass_code = """
function test_natives takes nothing returns nothing
    call DisplayTextToPlayer(0, 0, 0, "Hello from JASS!")
    call KillUnit("footman_001")
endfunction
"""

print("解析代码...")
parser = Parser(jass_code)
ast = parser.parse()

print(f"AST函数数量: {len(ast.functions)}")
if ast.functions:
    func = ast.functions[0]
    print(f"函数名: {func.name}")
    print(f"函数体语句数量: {len(func.body) if func.body else 0}")

    if func.body:
        for i, stmt in enumerate(func.body):
            print(f"语句 {i}: {type(stmt).__name__} - {stmt}")

            if hasattr(stmt, 'func_name'):
                print(f"  函数名: {stmt.func_name}")
                print(f"  参数: {stmt.args}")

# 测试原生函数注册
print("\n测试原生函数注册...")
factory = NativeFactory()
registry = factory.create_default_registry()

display_func = registry.get("DisplayTextToPlayer")
kill_func = registry.get("KillUnit")

print(f"DisplayTextToPlayer 找到: {display_func is not None}")
print(f"KillUnit 找到: {kill_func is not None}")

if display_func:
    print(f"调用 DisplayTextToPlayer...")
    state_context = StateContext()
    result = display_func.execute(state_context, 0, 0, 0, "Test message")
    print(f"结果: {result}")