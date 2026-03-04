"""测试 CreateForce 解析问题。"""

import sys
sys.path.insert(0, 'src')

from jass_runner.parser.lexer import Lexer
from jass_runner.parser.parser import Parser

# 测试代码
code = '''
function Test takes nothing returns nothing
    set bj_FORCE_ALL_PLAYERS = CreateForce()
endfunction
'''

# 语法分析 - Parser 需要代码字符串
from jass_runner.parser.parser import Parser
parser = Parser(code)

print("Tokens:")
lexer = Lexer(code)
for token in lexer.tokenize():
    print(f"  {token}")
ast = parser.parse()

print("\nAST Functions:")
for func in ast.functions:
    print(f"  Function: {func.name}")
    for stmt in func.body:
        print(f"    Statement: {stmt}")
        if hasattr(stmt, 'value'):
            print(f"      Value: {stmt.value} (type: {type(stmt.value).__name__})")
