# Globals 全局变量块实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现 JASS `globals` 全局变量块的解析与访问，支持基础变量声明和可选初始值。

**Architecture:** 扩展 AST 添加 `GlobalDecl` 节点和 `AST.globals` 列表；解析器添加 `parse_globals_block()` 方法；解释器在 `execute()` 中初始化全局变量到 `global_context`；解析时检查局部变量与全局变量同名冲突。

**Tech Stack:** Python 3.8+, pytest, 现有 Parser/Interpreter 框架

---

## Task 1: 添加 GlobalDecl AST 节点

**Files:**
- Modify: `src/jass_runner/parser/parser.py` (在现有 dataclass 后添加)

**Step 1: 添加 GlobalDecl 节点定义**

在 `ReturnStmt` 类定义之后，`Parser` 类定义之前添加：

```python
@dataclass
class GlobalDecl:
    """全局变量声明节点。"""
    name: str           # 变量名
    type: str           # 类型（integer, real, string, boolean等）
    value: Any          # 可选初始值，None表示未初始化
```

**Step 2: 扩展 AST 根节点**

修改 `AST` dataclass：

```python
@dataclass
class AST:
    """抽象语法树根节点。"""
    globals: List[GlobalDecl]       # 全局变量列表（新增）
    functions: List[FunctionDecl]   # 函数列表
```

**Step 3: Commit**

```bash
git add src/jass_runner/parser/parser.py
git commit -m "feat(parser): 添加 GlobalDecl AST 节点

- 添加 GlobalDecl 数据类表示全局变量声明
- 扩展 AST 根节点添加 globals 列表

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 2: 实现 parse_globals_block 方法

**Files:**
- Modify: `src/jass_runner/parser/parser.py`

**Step 1: 添加 parse_globals_block 方法**

在 `Parser` 类中添加新方法（建议在 `parse` 方法附近）：

```python
def parse_globals_block(self) -> List[GlobalDecl]:
    """解析可选的globals块。

    返回：
        如果存在globals块返回GlobalDecl列表，否则返回空列表
    """
    globals_list = []

    # 检查是否存在 globals 关键字
    if not self.current_token or not (self.current_token.type == 'KEYWORD' and self.current_token.value == 'globals'):
        return globals_list

    # 跳过 'globals' 关键字
    self.next_token()

    # 解析变量声明列表直到 endglobals
    while (self.current_token and
           not (self.current_token.type == 'KEYWORD' and self.current_token.value == 'endglobals')):
        global_decl = self.parse_global_declaration()
        if global_decl:
            globals_list.append(global_decl)

    # 跳过 'endglobals' 关键字
    if self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value == 'endglobals':
        self.next_token()

    return globals_list

def parse_global_declaration(self) -> Optional[GlobalDecl]:
    """解析单个全局变量声明。

    格式: <type> <name> [= <initial_value>]

    返回：
        GlobalDecl节点或None（如果解析失败）
    """
    try:
        # 获取变量类型
        if not self.current_token:
            return None

        var_type = self.current_token.value
        if var_type not in self.TYPE_KEYWORDS:
            return None
        self.next_token()

        # 获取变量名
        if not self.current_token or self.current_token.type != 'IDENTIFIER':
            return None
        var_name = self.current_token.value
        self.next_token()

        # 检查可选的初始值
        value = None
        if self.current_token and self.current_token.value == '=':
            self.next_token()
            if self.current_token:
                if self.current_token.type == 'INTEGER':
                    value = self.current_token.value
                    self.next_token()
                elif self.current_token.type == 'REAL':
                    value = self.current_token.value
                    self.next_token()
                elif self.current_token.type == 'STRING':
                    value = self.current_token.value[1:-1]  # 移除引号
                    self.next_token()
                elif self.current_token.type == 'KEYWORD' and self.current_token.value in ('true', 'false'):
                    value = self.current_token.value == 'true'
                    self.next_token()

        return GlobalDecl(name=var_name, type=var_type, value=value)

    except Exception:
        return None
```

**Step 2: Commit**

```bash
git add src/jass_runner/parser/parser.py
git commit -m "feat(parser): 实现 parse_globals_block 方法

- 添加 parse_globals_block 方法解析 globals/endglobals 块
- 添加 parse_global_declaration 方法解析单个全局变量声明
- 支持可选初始值（integer, real, string, boolean）

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 3: 修改 parse 方法整合 globals 解析

**Files:**
- Modify: `src/jass_runner/parser/parser.py`

**Step 1: 修改 parse 方法**

找到 `parse` 方法并修改：

```python
def parse(self) -> AST:
    """解析JASS代码并返回AST。"""
    self.tokens = self.lexer.tokenize()
    self.token_index = 0
    if self.tokens:
        self.current_token = self.tokens[0]
    else:
        self.current_token = None

    # 首先解析可选的 globals 块（新增）
    globals_list = self.parse_globals_block()

    # 解析所有函数
    functions = []
    while self.current_token:
        func = self.parse_function()
        if func:
            functions.append(func)

    return AST(globals=globals_list, functions=functions)  # 修改：添加 globals 参数
```

**Step 2: Commit**

```bash
git add src/jass_runner/parser/parser.py
git commit -m "feat(parser): 整合 globals 解析到 parse 方法

- 修改 parse 方法首先调用 parse_globals_block
- AST 构造函数添加 globals 参数

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 4: 编写解析器测试

**Files:**
- Create: `tests/parser/test_globals.py`

**Step 1: 编写测试文件**

```python
"""测试全局变量解析。"""

from jass_runner.parser.parser import Parser, GlobalDecl


def test_parse_globals_with_initial_values():
    """测试解析带初始值的全局变量。"""
    code = """
globals
    integer global_counter = 0
    real global_x = 1.5
    string app_name = "test"
    boolean is_enabled = true
endglobals

function main takes nothing returns nothing
endfunction
"""
    parser = Parser(code)
    ast = parser.parse()

    assert len(ast.globals) == 4
    assert ast.globals[0].name == 'global_counter'
    assert ast.globals[0].type == 'integer'
    assert ast.globals[0].value == 0
    assert ast.globals[1].name == 'global_x'
    assert ast.globals[1].type == 'real'
    assert ast.globals[1].value == 1.5
    assert ast.globals[2].name == 'app_name'
    assert ast.globals[2].type == 'string'
    assert ast.globals[2].value == 'test'
    assert ast.globals[3].name == 'is_enabled'
    assert ast.globals[3].type == 'boolean'
    assert ast.globals[3].value == True


def test_parse_globals_without_initial_values():
    """测试解析无初始值的全局变量。"""
    code = """
globals
    integer count
    real value
endglobals

function main takes nothing returns nothing
endfunction
"""
    parser = Parser(code)
    ast = parser.parse()

    assert len(ast.globals) == 2
    assert ast.globals[0].name == 'count'
    assert ast.globals[0].type == 'integer'
    assert ast.globals[0].value is None
    assert ast.globals[1].name == 'value'
    assert ast.globals[1].type == 'real'
    assert ast.globals[1].value is None


def test_parse_empty_globals():
    """测试解析空的 globals 块。"""
    code = """
globals
endglobals

function main takes nothing returns nothing
endfunction
"""
    parser = Parser(code)
    ast = parser.parse()

    assert len(ast.globals) == 0


def test_parse_no_globals():
    """测试没有 globals 块的代码。"""
    code = """
function main takes nothing returns nothing
endfunction
"""
    parser = Parser(code)
    ast = parser.parse()

    assert len(ast.globals) == 0
    assert len(ast.functions) == 1
```

**Step 2: 运行测试验证**

```bash
pytest tests/parser/test_globals.py -v
```
Expected: PASS (4 tests)

**Step 3: Commit**

```bash
git add tests/parser/test_globals.py
git commit -m "test(parser): 添加 globals 解析测试

- 测试带初始值的全局变量解析
- 测试无初始值的全局变量解析
- 测试空的 globals 块
- 测试没有 globals 块的代码

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 5: 添加变量名冲突检查

**Files:**
- Modify: `src/jass_runner/parser/parser.py`

**Step 1: 修改 parse 方法存储全局变量名**

```python
def parse(self) -> AST:
    """解析JASS代码并返回AST。"""
    self.tokens = self.lexer.tokenize()
    self.token_index = 0
    if self.tokens:
        self.current_token = self.tokens[0]
    else:
        self.current_token = None

    # 首先解析可选的 globals 块
    globals_list = self.parse_globals_block()

    # 存储全局变量名用于冲突检查（新增）
    self.global_names = {g.name for g in globals_list}

    # 解析所有函数
    functions = []
    while self.current_token:
        func = self.parse_function()
        if func:
            functions.append(func)

    return AST(globals=globals_list, functions=functions)
```

**Step 2: 修改 parse_local_declaration 添加冲突检查**

找到 `parse_local_declaration` 方法，在获取变量名后添加检查：

```python
def parse_local_declaration(self) -> Optional[LocalDecl]:
    """解析局部变量声明。"""
    try:
        # 跳过'local'关键词
        self.next_token()

        # 获取变量类型
        if not self.current_token:
            return None
        var_type = self.current_token.value
        self.next_token()

        # 获取变量名
        if not self.current_token or self.current_token.type != 'IDENTIFIER':
            return None
        var_name = self.current_token.value

        # 检查是否与全局变量同名（新增）
        if hasattr(self, 'global_names') and var_name in self.global_names:
            self.errors.append(ParseError(
                message=f"局部变量 '{var_name}' 与全局变量同名",
                line=self.current_token.line,
                column=self.current_token.column
            ))
            return None

        self.next_token()
        # ... 剩余代码保持不变
```

**Step 3: 编写冲突检查测试**

在 `tests/parser/test_globals.py` 中添加：

```python
def test_local_variable_name_conflict_with_global():
    """测试局部变量与全局变量同名时报错。"""
    code = """
globals
    integer counter = 0
endglobals

function main takes nothing returns nothing
    local integer counter = 1
endfunction
"""
    parser = Parser(code)
    ast = parser.parse()

    # 应该记录错误
    assert len(parser.errors) > 0
    assert any("counter" in str(e) and "同名" in str(e) for e in parser.errors)
```

**Step 4: 运行测试**

```bash
pytest tests/parser/test_globals.py::test_local_variable_name_conflict_with_global -v
```
Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/parser/parser.py tests/parser/test_globals.py
git commit -m "feat(parser): 添加局部变量与全局变量同名检查

- 在 parse 中存储全局变量名集合
- 在 parse_local_declaration 中检查冲突
- 冲突时记录解析错误

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 6: 修改解释器支持全局变量初始化

**Files:**
- Modify: `src/jass_runner/interpreter/interpreter.py`

**Step 1: 修改 execute 方法**

找到 `execute` 方法并修改：

```python
def execute(self, ast: AST):
    """执行AST。"""
    # 注册所有函数
    for func in ast.functions:
        self.functions[func.name] = func

    # 初始化全局变量（新增）
    for global_var in ast.globals:
        initial_value = global_var.value
        # 如果有初始值且是字符串表达式，需要求值
        if isinstance(initial_value, str):
            initial_value = self.evaluator.evaluate(initial_value)
        self.global_context.set_variable(global_var.name, initial_value)

    # 查找并执行main函数
    if 'main' in self.functions:
        self.execute_function(self.functions['main'])
```

**Step 2: Commit**

```bash
git add src/jass_runner/interpreter/interpreter.py
git commit -m "feat(interpreter): 添加全局变量初始化支持

- 在 execute 方法中遍历 ast.globals
- 求值初始值（如果是表达式）
- 设置到 global_context

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 7: 编写解释器测试

**Files:**
- Create: `tests/interpreter/test_globals.py`

**Step 1: 编写测试文件**

```python
"""测试全局变量执行。"""

from jass_runner.interpreter.interpreter import Interpreter
from jass_runner.parser.parser import Parser


def test_execute_globals_initialization():
    """测试全局变量正确初始化。"""
    code = """
globals
    integer counter = 10
    real value = 3.14
endglobals

function main takes nothing returns nothing
endfunction
"""
    parser = Parser(code)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.execute(ast)

    # 验证全局变量已初始化
    assert interpreter.global_context.get_variable('counter') == 10
    assert interpreter.global_context.get_variable('value') == 3.14


def test_execute_globals_access_in_function():
    """测试函数内访问全局变量。"""
    code = """
globals
    integer global_x = 5
endglobals

function main takes nothing returns nothing
    local integer y = global_x + 1
endfunction
"""
    parser = Parser(code)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.execute(ast)

    # 函数执行成功即表示测试通过
    assert True


def test_execute_globals_modify_in_function():
    """测试函数内修改全局变量。"""
    code = """
globals
    integer counter = 0
endglobals

function main takes nothing returns nothing
    set counter = counter + 1
endfunction
"""
    parser = Parser(code)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.execute(ast)

    # 验证全局变量已被修改
    assert interpreter.global_context.get_variable('counter') == 1


def test_execute_globals_persistence():
    """测试全局变量在多次调用间保持状态。"""
    code = """
globals
    integer call_count = 0
endglobals

function increment takes nothing returns nothing
    set call_count = call_count + 1
endfunction

function main takes nothing returns nothing
    call increment()
    call increment()
    call increment()
endfunction
"""
    parser = Parser(code)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.execute(ast)

    # 验证全局变量保持状态
    assert interpreter.global_context.get_variable('call_count') == 3
```

**Step 2: 运行测试**

```bash
pytest tests/interpreter/test_globals.py -v
```
Expected: PASS (4 tests)

**Step 3: Commit**

```bash
git add tests/interpreter/test_globals.py
git commit -m "test(interpreter): 添加全局变量执行测试

- 测试全局变量初始化
- 测试函数内访问全局变量
- 测试函数内修改全局变量
- 测试全局变量状态持久化

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 8: 编写集成测试

**Files:**
- Create: `tests/integration/test_globals_integration.py`

**Step 1: 编写测试文件**

```python
"""全局变量集成测试。"""

from jass_runner.vm.jass_vm import JassVM


def test_globals_with_control_flow():
    """测试全局变量在控制流语句中使用。"""
    code = """
globals
    integer counter = 0
endglobals

function main takes nothing returns nothing
    loop
        exitwhen counter >= 5
        set counter = counter + 1
    endloop
endfunction
"""
    vm = JassVM()
    vm.load_script(code)
    vm.execute()

    # 验证循环结束后全局变量的值
    assert vm.interpreter.global_context.get_variable('counter') == 5


def test_globals_with_function_calls():
    """测试全局变量在函数间共享状态。"""
    code = """
globals
    integer total = 0
endglobals

function add_to_total takes integer value returns nothing
    set total = total + value
endfunction

function main takes nothing returns nothing
    call add_to_total(10)
    call add_to_total(20)
    call add_to_total(30)
endfunction
"""
    vm = JassVM()
    vm.load_script(code)
    vm.execute()

    # 验证全局变量累加结果
    assert vm.interpreter.global_context.get_variable('total') == 60


def test_globals_example_script():
    """测试完整示例脚本。"""
    code = """
globals
    integer game_score = 0
    boolean game_active = true
endglobals

function score_point takes integer points returns nothing
    if game_active then
        set game_score = game_score + points
    endif
endfunction

function main takes nothing returns nothing
    call score_point(10)
    call score_point(20)
    set game_active = false
    call score_point(30)
endfunction
"""
    vm = JassVM()
    vm.load_script(code)
    vm.execute()

    # 验证最终分数（game_active=false后不应再加分）
    assert vm.interpreter.global_context.get_variable('game_score') == 30
```

**Step 2: 运行测试**

```bash
pytest tests/integration/test_globals_integration.py -v
```
Expected: PASS (3 tests)

**Step 3: Commit**

```bash
git add tests/integration/test_globals_integration.py
git commit -m "test(integration): 添加全局变量集成测试

- 测试全局变量在控制流中使用
- 测试全局变量在函数间共享状态
- 测试完整示例脚本

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 9: 运行完整测试套件

**Step 1: 运行所有测试**

```bash
pytest --tb=short
```
Expected: 所有测试通过（原有测试 + 新测试）

**Step 2: 生成覆盖率报告**

```bash
pytest --cov=src/jass_runner --cov-report=term-missing
```
Expected: 核心模块覆盖率保持或提升

**Step 3: 最终提交**

```bash
git add -A
git commit -m "feat: 完成 globals 全局变量块实现

- Parser: 添加 GlobalDecl AST 节点，实现 parse_globals_block
- Interpreter: 支持全局变量初始化和访问
- 添加变量名冲突检查（局部变量与全局变量同名时报错）
- 完整测试覆盖：解析器测试、解释器测试、集成测试

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## 实施检查清单

- [ ] Task 1: GlobalDecl AST 节点添加完成
- [ ] Task 2: parse_globals_block 方法实现完成
- [ ] Task 3: parse 方法整合完成
- [ ] Task 4: 解析器测试通过
- [ ] Task 5: 变量名冲突检查实现完成
- [ ] Task 6: 解释器全局变量初始化完成
- [ ] Task 7: 解释器测试通过
- [ ] Task 8: 集成测试通过
- [ ] Task 9: 完整测试套件通过

---

## 相关文档

- 设计文档: `docs/plans/2026-02-28-globals-global-variables-design.md`
- TODO.md: 功能路线图
