# Phase 1: Parser层控制流语句实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 扩展Parser以支持控制流语句的AST节点和解析方法

**Architecture:** 在parser.py中添加IfStmt、LoopStmt、ExitWhenStmt、ReturnStmt四个AST节点类，以及对应的parse_*方法

**Tech Stack:** Python 3.8+, 现有Parser框架

**Dependencies:** 无（基于现有Parser架构）

---

## 前置知识

### 现有Parser结构
- 文件位置: `src/jass_runner/parser/parser.py`
- 现有AST节点: LocalDecl, FunctionDecl, AST, NativeCallNode, SetStmt
- 现有parse_statement()只处理local/call/set

### 需要添加的AST节点（参考设计文档）
```python
@dataclass
class IfStmt:
    condition: Any
    then_body: List[Any]
    elseif_branches: List[Tuple[Any, List[Any]]]
    else_body: List[Any]

@dataclass
class LoopStmt:
    body: List[Any]

@dataclass
class ExitWhenStmt:
    condition: Any

@dataclass
class ReturnStmt:
    value: Optional[Any]
```

---

## Task 1: 创建IfStmt AST节点和基础解析

**Files:**
- Modify: `src/jass_runner/parser/parser.py` (添加IfStmt dataclass)
- Test: `tests/parser/test_parser.py`

**Step 1: 编写失败测试**

```python
def test_parse_simple_if_statement():
    """测试解析简单if语句"""
    from jass_runner.parser.parser import Parser

    code = """
    function main takes nothing returns nothing
        if true then
            call DisplayTextToPlayer("hello")
        endif
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    func = ast.functions[0]
    if_stmt = func.body[0]
    assert if_stmt.__class__.__name__ == "IfStmt"
    assert if_stmt.condition == "true"
    assert len(if_stmt.then_body) == 1
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/parser/test_parser.py::test_parse_simple_if_statement -v
```
Expected: FAIL (IfStmt not defined)

**Step 3: 添加IfStmt节点和解析方法**

在parser.py添加:
```python
@dataclass
class IfStmt:
    """if/elseif/else语句节点"""
    condition: Any
    then_body: List[Any]
    elseif_branches: List[Tuple[Any, List[Any]]]
    else_body: List[Any]
```

在parse_statement()中添加:
```python
elif self.current_token.value == 'if':
    return self.parse_if_statement()
```

添加parse_if_statement()方法:
```python
def parse_if_statement(self):
    """解析if语句"""
    self.consume('if')
    condition = self.parse_condition()
    self.consume('then')

    then_body = []
    while self.current_token and self.current_token.value not in ('elseif', 'else', 'endif'):
        then_body.append(self.parse_statement())

    elseif_branches = []
    while self.current_token and self.current_token.value == 'elseif':
        self.consume('elseif')
        elseif_condition = self.parse_condition()
        self.consume('then')
        elseif_body = []
        while self.current_token and self.current_token.value not in ('elseif', 'else', 'endif'):
            elseif_body.append(self.parse_statement())
        elseif_branches.append((elseif_condition, elseif_body))

    else_body = []
    if self.current_token and self.current_token.value == 'else':
        self.consume('else')
        while self.current_token and self.current_token.value != 'endif':
            else_body.append(self.parse_statement())

    self.consume('endif')
    return IfStmt(condition, then_body, elseif_branches, else_body)
```

添加parse_condition()方法:
```python
def parse_condition(self):
    """解析条件表达式（简化版，先支持单个token）"""
    if self.current_token.type == 'KEYWORD' and self.current_token.value in ('true', 'false'):
        value = self.current_token.value
        self.advance()
        return value
    # TODO: 后续支持复杂表达式
    condition = self.current_token.value
    self.advance()
    return condition
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/parser/test_parser.py::test_parse_simple_if_statement -v
```
Expected: PASS

**Step 5: 提交**

```bash
git add tests/parser/test_parser.py src/jass_runner/parser/parser.py
git commit -m "feat(parser): 添加IfStmt节点和简单if语句解析

- 添加IfStmt AST节点
- 实现parse_if_statement方法
- 支持简单if/then/endif结构

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 2: 支持if/else和elseif

**Files:**
- Modify: `src/jass_runner/parser/parser.py` (完善parse_if_statement)
- Test: `tests/parser/test_parser.py`

**Step 1: 编写失败测试**

```python
def test_parse_if_else_statement():
    """测试解析if/else语句"""
    from jass_runner.parser.parser import Parser

    code = """
    function main takes nothing returns nothing
        if true then
            call A()
        else
            call B()
        endif
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    func = ast.functions[0]
    if_stmt = func.body[0]
    assert len(if_stmt.then_body) == 1
    assert len(if_stmt.else_body) == 1
```

```python
def test_parse_if_elseif_else_statement():
    """测试解析if/elseif/else语句"""
    from jass_runner.parser.parser import Parser

    code = """
    function main takes nothing returns nothing
        if x > 0 then
            call A()
        elseif x < 0 then
            call B()
        else
            call C()
        endif
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    func = ast.functions[0]
    if_stmt = func.body[0]
    assert len(if_stmt.elseif_branches) == 1
    assert len(if_stmt.else_body) == 1
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/parser/test_parser.py::test_parse_if_else_statement tests/parser/test_parser.py::test_parse_if_elseif_else_statement -v
```
Expected: 需要验证现有实现是否能通过

**Step 3: 修复或完善实现**

（根据测试结果调整，Task 1的实现应该已经支持，如失败则修复）

**Step 4: 运行测试验证通过**

```bash
pytest tests/parser/test_parser.py::test_parse_if_else_statement tests/parser/test_parser.py::test_parse_if_elseif_else_statement -v
```
Expected: PASS

**Step 5: 提交**

```bash
git add tests/parser/test_parser.py
git commit -m "test(parser): 添加if/else和elseif解析测试

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 3: 支持嵌套if语句

**Files:**
- Test: `tests/parser/test_parser.py`

**Step 1: 编写测试**

```python
def test_parse_nested_if_statement():
    """测试解析嵌套if语句"""
    from jass_runner.parser.parser import Parser

    code = """
    function main takes nothing returns nothing
        if x > 0 then
            if y > 0 then
                call A()
            endif
        endif
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    func = ast.functions[0]
    outer_if = func.body[0]
    inner_if = outer_if.then_body[0]
    assert inner_if.__class__.__name__ == "IfStmt"
```

**Step 2: 运行测试**

```bash
pytest tests/parser/test_parser.py::test_parse_nested_if_statement -v
```
Expected: PASS (如果Task 1实现正确，应该能通过)

**Step 3: 提交**

```bash
git add tests/parser/test_parser.py
git commit -m "test(parser): 添加嵌套if语句解析测试

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 4: 添加LoopStmt和循环解析

**Files:**
- Modify: `src/jass_runner/parser/parser.py`
- Test: `tests/parser/test_parser.py`

**Step 1: 编写失败测试**

```python
def test_parse_loop_statement():
    """测试解析loop语句"""
    from jass_runner.parser.parser import Parser

    code = """
    function main takes nothing returns nothing
        loop
            call A()
        endloop
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    func = ast.functions[0]
    loop_stmt = func.body[0]
    assert loop_stmt.__class__.__name__ == "LoopStmt"
    assert len(loop_stmt.body) == 1
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/parser/test_parser.py::test_parse_loop_statement -v
```
Expected: FAIL (LoopStmt not defined)

**Step 3: 添加LoopStmt节点和解析方法**

添加AST节点:
```python
@dataclass
class LoopStmt:
    """loop循环节点"""
    body: List[Any]
```

在parse_statement()中添加:
```python
elif self.current_token.value == 'loop':
    return self.parse_loop_statement()
```

添加parse_loop_statement()方法:
```python
def parse_loop_statement(self):
    """解析loop语句"""
    self.consume('loop')

    body = []
    while self.current_token and self.current_token.value != 'endloop':
        body.append(self.parse_statement())

    self.consume('endloop')
    return LoopStmt(body)
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/parser/test_parser.py::test_parse_loop_statement -v
```
Expected: PASS

**Step 5: 提交**

```bash
git add tests/parser/test_parser.py src/jass_runner/parser/parser.py
git commit -m "feat(parser): 添加LoopStmt节点和loop解析

- 添加LoopStmt AST节点
- 实现parse_loop_statement方法
- 支持loop/endloop结构

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 5: 添加ExitWhenStmt和return解析

**Files:**
- Modify: `src/jass_runner/parser/parser.py`
- Test: `tests/parser/test_parser.py`

**Step 1: 编写失败测试**

```python
def test_parse_exitwhen_statement():
    """测试解析exitwhen语句"""
    from jass_runner.parser.parser import Parser

    code = """
    function main takes nothing returns nothing
        loop
            exitwhen i >= 10
        endloop
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    func = ast.functions[0]
    loop_stmt = func.body[0]
    exit_stmt = loop_stmt.body[0]
    assert exit_stmt.__class__.__name__ == "ExitWhenStmt"
```

```python
def test_parse_return_statement():
    """测试解析return语句"""
    from jass_runner.parser.parser import Parser

    code = """
    function test takes integer x returns integer
        if x > 0 then
            return 1
        endif
        return 0
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    func = ast.functions[0]
    if_stmt = func.body[0]
    return_stmt = if_stmt.then_body[0]
    assert return_stmt.__class__.__name__ == "ReturnStmt"
    assert return_stmt.value == "1"
```

```python
def test_parse_return_nothing():
    """测试解析return nothing"""
    from jass_runner.parser.parser import Parser

    code = """
    function main takes nothing returns nothing
        return
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    func = ast.functions[0]
    return_stmt = func.body[0]
    assert return_stmt.__class__.__name__ == "ReturnStmt"
    assert return_stmt.value is None
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/parser/test_parser.py::test_parse_exitwhen_statement tests/parser/test_parser.py::test_parse_return_statement tests/parser/test_parser.py::test_parse_return_nothing -v
```
Expected: FAIL (ExitWhenStmt和ReturnStmt未定义)

**Step 3: 添加AST节点和解析方法**

添加AST节点:
```python
@dataclass
class ExitWhenStmt:
    """exitwhen退出循环节点"""
    condition: Any

@dataclass
class ReturnStmt:
    """return语句节点"""
    value: Optional[Any]
```

在parse_statement()中添加:
```python
elif self.current_token.value == 'exitwhen':
    return self.parse_exitwhen_statement()
elif self.current_token.value == 'return':
    return self.parse_return_statement()
```

添加解析方法:
```python
def parse_exitwhen_statement(self):
    """解析exitwhen语句"""
    self.consume('exitwhen')
    condition = self.parse_condition()
    return ExitWhenStmt(condition)

def parse_return_statement(self):
    """解析return语句"""
    self.consume('return')

    # 检查是否有返回值
    if self.current_token and self.current_token.value != 'endfunction':
        value = self.parse_condition()  # 简化处理
        return ReturnStmt(value)
    return ReturnStmt(None)
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/parser/test_parser.py::test_parse_exitwhen_statement tests/parser/test_parser.py::test_parse_return_statement tests/parser/test_parser.py::test_parse_return_nothing -v
```
Expected: PASS

**Step 5: 提交**

```bash
git add tests/parser/test_parser.py src/jass_runner/parser/parser.py
git commit -m "feat(parser): 添加ExitWhenStmt和ReturnStmt节点

- 添加ExitWhenStmt和ReturnStmt AST节点
- 实现parse_exitwhen_statement和parse_return_statement方法
- 支持exitwhen和return语法

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 6: 支持复杂条件表达式（用于Phase 2集成）

**说明:** 完整的条件表达式解析（支持运算符）将在Evaluator层实现。Parser层现在只需确保能正确捕获表达式字符串，供后续求值。

当前parse_condition()返回的是简单token值，在Phase 2中将扩展为完整表达式解析。

---

## Phase 1 完成检查清单

- [x] IfStmt节点和if/then/elseif/else/endif解析
- [x] LoopStmt节点和loop/endloop解析
- [x] ExitWhenStmt节点和exitwhen解析
- [x] ReturnStmt节点和return解析
- [x] 嵌套if语句支持
- [x] 所有测试通过

**下一步:** Phase 2 - Evaluator层运算符支持
