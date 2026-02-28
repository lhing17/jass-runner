# Constant 常量支持实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use @superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 扩展 globals 模块以支持 `constant` 常量声明，实现编译期只读检查。

**Architecture:** 在现有 `GlobalDecl` 节点添加 `is_constant` 标记，解析阶段检测并阻止对常量的修改，解释器端无需额外改动。

**Tech Stack:** Python 3.8+, pytest, 现有 JASS Runner 解析器和解释器框架

---

## 前置检查

运行以下命令确保环境就绪：

```bash
# 验证项目可导入
python -c "from jass_runner.parser.parser import Parser; from jass_runner.interpreter.interpreter import Interpreter; print('OK')"

# 运行现有 globals 测试确保基础功能正常
pytest tests/parser/test_globals.py tests/interpreter/test_globals_interp.py -v
```

Expected: 所有现有测试通过

---

## Task 1: 扩展 GlobalDecl AST 节点

**Files:**
- Modify: `src/jass_runner/parser/parser.py:60-66`
- Test: `tests/parser/test_globals.py`

**Step 1: 编写失败测试**

在 `tests/parser/test_globals.py` 末尾添加：

```python
def test_parse_constant_declaration():
    """测试解析 constant 常量声明。"""
    code = """
globals
    constant integer MAX_SIZE = 100
endglobals

function main takes nothing returns nothing
endfunction
"""
    parser = Parser(code)
    ast = parser.parse()

    assert len(ast.globals) == 1
    assert ast.globals[0].name == 'MAX_SIZE'
    assert ast.globals[0].type == 'integer'
    assert ast.globals[0].value == 100
    assert ast.globals[0].is_constant is True
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/parser/test_globals.py::test_parse_constant_declaration -v
```

Expected: FAIL with `AttributeError: 'GlobalDecl' object has no attribute 'is_constant'`

**Step 3: 实现 AST 扩展**

修改 `src/jass_runner/parser/parser.py` 第60-66行：

```python
@dataclass
class GlobalDecl:
    """全局变量声明节点。"""
    name: str
    type: str
    value: Any
    is_constant: bool = False  # 新增：是否为常量
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/parser/test_globals.py::test_parse_constant_declaration -v
```

Expected: PASS

**Step 5: 提交**

```bash
git add tests/parser/test_globals.py src/jass_runner/parser/parser.py
git commit -m "feat(ast): 为 GlobalDecl 添加 is_constant 标记

- 支持 constant 常量声明的 AST 表示
- 默认为 False 保持向后兼容

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 2: 解析 constant 关键字

**Files:**
- Modify: `src/jass_runner/parser/parser.py:232-278`
- Test: `tests/parser/test_globals.py`

**Step 1: 编写失败测试**

在 `tests/parser/test_globals.py` 末尾添加：

```python
def test_parse_constant_real_declaration():
    """测试解析 constant real 常量声明。"""
    code = """
globals
    constant real PI = 3.14159
endglobals

function main takes nothing returns nothing
endfunction
"""
    parser = Parser(code)
    ast = parser.parse()

    assert len(ast.globals) == 1
    assert ast.globals[0].name == 'PI'
    assert ast.globals[0].type == 'real'
    assert ast.globals[0].value == 3.14159
    assert ast.globals[0].is_constant is True
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/parser/test_globals.py::test_parse_constant_real_declaration -v
```

Expected: FAIL - 解析器无法识别 `constant` 关键字，返回空 globals 列表

**Step 3: 修改 parse_global_declaration**

修改 `src/jass_runner/parser/parser.py` 第232-278行的 `parse_global_declaration` 方法：

```python
def parse_global_declaration(self) -> Optional[GlobalDecl]:
    """解析单个全局变量声明。

    格式: [constant] <type> <name> [= <initial_value>]

    返回：
        GlobalDecl节点或None（如果解析失败）
    """
    try:
        is_constant = False

        # 检查是否为 constant 关键字
        if (self.current_token and
                self.current_token.type == 'KEYWORD' and
                self.current_token.value == 'constant'):
            is_constant = True
            self.next_token()

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
                    value = self.current_token.value[1:-1]
                    self.next_token()
                elif (self.current_token.type == 'KEYWORD' and
                      self.current_token.value in ('true', 'false')):
                    value = self.current_token.value == 'true'
                    self.next_token()

        return GlobalDecl(
            name=var_name,
            type=var_type,
            value=value,
            is_constant=is_constant
        )

    except Exception:
        return None
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/parser/test_globals.py::test_parse_constant_declaration tests/parser/test_globals.py::test_parse_constant_real_declaration -v
```

Expected: PASS

**Step 5: 提交**

```bash
git add tests/parser/test_globals.py src/jass_runner/parser/parser.py
git commit -m "feat(parser): 支持解析 constant 关键字

- 在 parse_global_declaration 中检测 constant 关键字
- 设置 is_constant 标记
- 支持所有基础类型：integer, real, string, boolean

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 3: 验证 constant 必须有初始值

**Files:**
- Modify: `src/jass_runner/parser/parser.py:232-278`
- Test: `tests/parser/test_globals.py`

**Step 1: 编写失败测试**

在 `tests/parser/test_globals.py` 末尾添加：

```python
def test_parse_constant_without_initial_value_errors():
    """测试 constant 没有初始值时报错。"""
    code = """
globals
    constant integer MAX_SIZE
endglobals

function main takes nothing returns nothing
endfunction
"""
    parser = Parser(code)
    ast = parser.parse()

    # 应该记录错误
    assert len(parser.errors) > 0
    assert any('MAX_SIZE' in str(e) and '必须指定初始值' in str(e) for e in parser.errors)
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/parser/test_globals.py::test_parse_constant_without_initial_value_errors -v
```

Expected: FAIL - 当前代码允许 constant 没有初始值

**Step 3: 添加初始值验证**

在 `parse_global_declaration` 方法中，解析完初始值后添加验证：

```python
# 检查可选的初始值
value = None
if self.current_token and self.current_token.value == '=':
    # ... 原有解析初始值代码 ...
elif is_constant:
    # constant 必须有初始值
    self.errors.append(ParseError(
        message=f"常量 '{var_name}' 必须指定初始值",
        line=self.current_token.line if self.current_token else 0,
        column=self.current_token.column if self.current_token else 0
    ))
    return None
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/parser/test_globals.py::test_parse_constant_without_initial_value_errors -v
```

Expected: PASS

**Step 5: 提交**

```bash
git add tests/parser/test_globals.py src/jass_runner/parser/parser.py
git commit -m "feat(parser): constant 必须有初始值

- 在解析阶段验证 constant 是否指定初始值
- 未指定时记录错误并返回 None

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 4: 阻止修改 constant 常量

**Files:**
- Modify: `src/jass_runner/parser/parser.py:166-202`, `src/jass_runner/parser/parser.py:778-876`
- Test: `tests/parser/test_globals.py`

**Step 1: 编写失败测试**

在 `tests/parser/test_globals.py` 末尾添加：

```python
def test_parse_set_constant_errors():
    """测试尝试修改 constant 时报错。"""
    code = """
globals
    constant integer MAX_SIZE = 100
endglobals

function test takes nothing returns nothing
    set MAX_SIZE = 200
endfunction
"""
    parser = Parser(code)
    ast = parser.parse()

    # 应该记录错误
    assert len(parser.errors) > 0
    assert any('MAX_SIZE' in str(e) and '不能修改常量' in str(e) for e in parser.errors)
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/parser/test_globals.py::test_parse_set_constant_errors -v
```

Expected: FAIL - 当前代码允许修改 constant

**Step 3: 在 parse 方法中收集常量名**

修改 `src/jass_runner/parser/parser.py` 第166-202行的 `parse` 方法，在解析完 globals 后添加：

```python
# 首先解析可选的 globals 块
globals_list = self.parse_globals_block()

# 存储全局变量名和常量名用于冲突检查
self.global_names = {g.name for g in globals_list}
self.constant_names = {g.name for g in globals_list if g.is_constant}
```

**Step 4: 在 parse_set_statement 中检查常量修改**

修改 `src/jass_runner/parser/parser.py` 第778-876行的 `parse_set_statement` 方法，在获取变量名后添加检查：

```python
def parse_set_statement(self) -> Optional[SetStmt]:
    """解析set赋值语句。"""
    try:
        # 跳过'set'关键词
        self.next_token()

        # 获取变量名
        if not self.current_token or self.current_token.type != 'IDENTIFIER':
            return None
        var_name = self.current_token.value

        # 检查是否尝试修改常量
        if hasattr(self, 'constant_names') and var_name in self.constant_names:
            self.errors.append(ParseError(
                message=f"不能修改常量 '{var_name}'",
                line=self.current_token.line,
                column=self.current_token.column
            ))
            # 继续消耗token以同步，但返回None表示解析失败
            self.next_token()
            if self.current_token and self.current_token.value == '=':
                self.next_token()
                # 跳过右侧值
                while (self.current_token and
                       not (self.current_token.type == 'KEYWORD' and
                            self.current_token.value in ('set', 'call', 'local', 'return',
                                                         'exitwhen', 'loop', 'if', 'elseif',
                                                         'else', 'endif', 'endloop', 'endfunction'))):
                    self.next_token()
            return None

        # ... 原有代码继续 ...
```

**Step 5: 运行测试验证通过**

```bash
pytest tests/parser/test_globals.py::test_parse_set_constant_errors -v
```

Expected: PASS

**Step 6: 提交**

```bash
git add tests/parser/test_globals.py src/jass_runner/parser/parser.py
git commit -m "feat(parser): 阻止修改 constant 常量

- 在 parse 方法中收集 constant_names 集合
- 在 parse_set_statement 中检查并阻止对常量的修改
- 提供清晰的错误信息

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 5: 测试解释器执行 constant 访问

**Files:**
- Test: `tests/interpreter/test_globals_interp.py`

**Step 1: 编写测试**

在 `tests/interpreter/test_globals_interp.py` 末尾添加：

```python
def test_execute_constant_access():
    """测试在函数内访问 constant 常量。"""
    code = """
globals
    constant integer MAX_SIZE = 100
    constant real PI = 3.14159
    constant string APP_NAME = "TestApp"
    constant boolean DEBUG_MODE = true
endglobals

function main takes nothing returns nothing
    local integer size = MAX_SIZE
    local real pi_value = PI
    local string name = APP_NAME
    local boolean debug = DEBUG_MODE
endfunction
"""
    parser = Parser(code)
    ast = parser.parse()

    assert len(parser.errors) == 0, f"解析错误: {parser.errors}"

    interpreter = Interpreter()
    interpreter.execute(ast)

    # 验证常量已正确初始化
    assert interpreter.global_context.get_variable('MAX_SIZE') == 100
    assert interpreter.global_context.get_variable('PI') == 3.14159
    assert interpreter.global_context.get_variable('APP_NAME') == 'TestApp'
    assert interpreter.global_context.get_variable('DEBUG_MODE') is True
```

**Step 2: 运行测试**

```bash
pytest tests/interpreter/test_globals_interp.py::test_execute_constant_access -v
```

Expected: PASS（解释器无需改动，因为 constant 在解析阶段已保护）

**Step 3: 提交**

```bash
git add tests/interpreter/test_globals_interp.py
git commit -m "test(interpreter): 添加 constant 访问测试

- 验证所有基础类型常量正确初始化
- 验证函数内可以正常访问常量

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 6: 添加集成测试

**Files:**
- Test: `tests/integration/test_globals_integration.py`

**Step 1: 编写集成测试**

在 `tests/integration/test_globals_integration.py` 末尾添加：

```python
def test_mixed_globals_and_constants():
    """测试普通全局变量和 constant 混合使用。"""
    from jass_runner.parser.parser import Parser
    from jass_runner.interpreter.interpreter import Interpreter

    code = """
globals
    constant integer MAX_HP = 100
    integer current_hp = 50
endglobals

function heal takes nothing returns nothing
    set current_hp = MAX_HP
endfunction

function main takes nothing returns nothing
    call heal()
endfunction
"""
    parser = Parser(code)
    ast = parser.parse()

    assert len(parser.errors) == 0, f"解析错误: {parser.errors}"

    interpreter = Interpreter()
    interpreter.execute(ast)

    # 验证普通全局变量被修改为常量值
    assert interpreter.global_context.get_variable('current_hp') == 100
    assert interpreter.global_context.get_variable('MAX_HP') == 100
```

**Step 2: 运行测试**

```bash
pytest tests/integration/test_globals_integration.py::test_mixed_globals_and_constants -v
```

Expected: PASS

**Step 3: 提交**

```bash
git add tests/integration/test_globals_integration.py
git commit -m "test(integration): 添加常量与变量混合使用测试

- 验证常量可用于给普通变量赋值
- 验证混合场景下解析和执行正常

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 7: 运行完整测试套件

**Step 1: 运行所有相关测试**

```bash
pytest tests/parser/test_globals.py tests/interpreter/test_globals_interp.py tests/integration/test_globals_integration.py -v
```

Expected: 所有测试通过

**Step 2: 运行完整测试套件确保无回归**

```bash
pytest
```

Expected: 所有测试通过

**Step 3: 提交（如需要）**

如果测试全部通过，任务完成。

---

## 完成检查清单

- [ ] Task 1: GlobalDecl 扩展完成并提交
- [ ] Task 2: constant 关键字解析完成并提交
- [ ] Task 3: 初始值验证完成并提交
- [ ] Task 4: 常量修改检查完成并提交
- [ ] Task 5: 解释器测试完成并提交
- [ ] Task 6: 集成测试完成并提交
- [ ] Task 7: 所有测试通过

---

## 执行选项

**Plan complete and saved to `docs/plans/2026-02-28-constant-globals-implementation.md`. Two execution options:**

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?**
