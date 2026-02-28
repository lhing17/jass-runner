# Phase 3: Interpreter层控制流执行实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 扩展Interpreter以支持控制流语句的执行（if、loop、return）

**Architecture:** 使用异常机制处理控制流跳转（ReturnSignal、ExitLoopSignal），在execute_statement中添加分发逻辑

**Tech Stack:** Python 3.8+, 现有Interpreter框架

**Dependencies:** Phase 1和Phase 2完成（Parser和Evaluator支持）

---

## 前置知识

### 现有Interpreter结构
- 文件位置: `src/jass_runner/interpreter/interpreter.py`
- 当前execute_statement()只处理local/call/set
- execute_function()顺序执行函数体，无控制流处理

### 需要添加的控制流信号
```python
class ReturnSignal(Exception):
    """函数返回信号"""
    def __init__(self, value):
        self.value = value

class ExitLoopSignal(Exception):
    """退出循环信号"""
    pass
```

---

## Task 1: 添加控制流异常类

**Files:**
- Create: `src/jass_runner/interpreter/control_flow.py`
- Test: `tests/interpreter/test_control_flow.py` (可选，异常类较简单)

**Step 1: 创建控制流异常模块**

```python
"""控制流异常定义。

此模块定义用于控制流跳转的特殊异常类。
"""


class ReturnSignal(Exception):
    """函数返回信号，携带返回值。

    当执行return语句时抛出，用于从函数任意位置提前返回。

    属性:
        value: 返回值，对于return nothing为None
    """

    def __init__(self, value):
        self.value = value
        super().__init__(f"Return with value: {value}")


class ExitLoopSignal(Exception):
    """退出当前循环的信号。

    当执行exitwhen语句且条件为真时抛出，用于跳出loop循环。
    """
    pass
```

**Step 2: 提交**

```bash
git add src/jass_runner/interpreter/control_flow.py
git commit -m "feat(interpreter): 添加控制流异常类

- 添加ReturnSignal用于函数返回
- 添加ExitLoopSignal用于退出循环

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 2: 实现if语句执行

**Files:**
- Modify: `src/jass_runner/interpreter/interpreter.py`
- Test: `tests/interpreter/test_interpreter.py`

**Step 1: 编写失败测试**

```python
def test_execute_if_then_branch():
    """测试执行if语句的then分支"""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.parser import Parser

    code = """
    function main takes nothing returns nothing
        if true then
            call DisplayTextToPlayer("then branch")
        endif
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.execute(ast)
    # 如果没有异常抛出，说明执行成功
    assert True
```

```python
def test_execute_if_else_branch():
    """测试执行if语句的else分支"""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.parser import Parser

    code = """
    function main takes nothing returns nothing
        if false then
            call DisplayTextToPlayer("then branch")
        else
            call DisplayTextToPlayer("else branch")
        endif
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.execute(ast)
    assert True
```

```python
def test_execute_if_elseif():
    """测试执行if/elseif语句"""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.parser import Parser

    code = """
    function main takes nothing returns nothing
        local integer x = 2
        if x == 1 then
            call DisplayTextToPlayer("one")
        elseif x == 2 then
            call DisplayTextToPlayer("two")
        else
            call DisplayTextToPlayer("other")
        endif
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.execute(ast)
    assert True
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/interpreter/test_interpreter.py::test_execute_if_then_branch tests/interpreter/test_interpreter.py::test_execute_if_else_branch tests/interpreter/test_interpreter.py::test_execute_if_elseif -v
```
Expected: FAIL (Interpreter不支持IfStmt)

**Step 3: 添加if语句执行支持**

在interpreter.py导入AST节点和异常:
```python
from jass_runner.parser.parser import IfStmt, LoopStmt, ExitWhenStmt, ReturnStmt
from jass_runner.interpreter.control_flow import ReturnSignal, ExitLoopSignal
```

在execute_statement()中添加:
```python
elif isinstance(statement, IfStmt):
    self.execute_if_statement(statement)
```

添加execute_if_statement方法:
```python
def execute_if_statement(self, stmt: IfStmt):
    """执行if语句。

    按顺序检查条件，执行第一个为真的分支。
    """
    # 检查if条件
    if self.evaluator.evaluate_condition(stmt.condition):
        for s in stmt.then_body:
            self.execute_statement(s)
        return

    # 检查elseif条件
    for condition, body in stmt.elseif_branches:
        if self.evaluator.evaluate_condition(condition):
            for s in body:
                self.execute_statement(s)
            return

    # 执行else分支
    for s in stmt.else_body:
        self.execute_statement(s)
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/interpreter/test_interpreter.py::test_execute_if_then_branch tests/interpreter/test_interpreter.py::test_execute_if_else_branch tests/interpreter/test_interpreter.py::test_execute_if_elseif -v
```
Expected: PASS

**Step 5: 提交**

```bash
git add tests/interpreter/test_interpreter.py src/jass_runner/interpreter/interpreter.py src/jass_runner/interpreter/control_flow.py
git commit -m "feat(interpreter): 实现if语句执行

- 添加execute_if_statement方法
- 支持if/then/elseif/else/endif所有分支
- 按顺序检查条件，执行第一个为真的分支

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 3: 实现嵌套if语句执行

**Files:**
- Test: `tests/interpreter/test_interpreter.py`

**Step 1: 编写测试**

```python
def test_execute_nested_if():
    """测试执行嵌套if语句"""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.parser import Parser

    code = """
    function main takes nothing returns nothing
        local integer x = 5
        local integer y = 3
        if x > 0 then
            if y > 0 then
                call DisplayTextToPlayer("both positive")
            endif
        endif
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.execute(ast)
    assert True
```

**Step 2: 运行测试**

```bash
pytest tests/interpreter/test_interpreter.py::test_execute_nested_if -v
```
Expected: PASS (Task 2的递归调用execute_statement应该已支持)

**Step 3: 提交**

```bash
git add tests/interpreter/test_interpreter.py
git commit -m "test(interpreter): 添加嵌套if语句执行测试

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 4: 实现loop循环执行

**Files:**
- Modify: `src/jass_runner/interpreter/interpreter.py`
- Test: `tests/interpreter/test_interpreter.py`

**Step 1: 编写失败测试**

```python
def test_execute_simple_loop():
    """测试执行简单loop循环"""
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
    # 验证i的最终值
    assert interpreter.global_context.get_variable("i") == 3
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/interpreter/test_interpreter.py::test_execute_simple_loop -v
```
Expected: FAIL (不支持LoopStmt和ExitWhenStmt)

**Step 3: 添加loop和exitwhen执行支持**

在execute_statement()中添加:
```python
elif isinstance(statement, LoopStmt):
    self.execute_loop_statement(statement)
elif isinstance(statement, ExitWhenStmt):
    self.execute_exitwhen_statement(statement)
```

添加execute_loop_statement方法:
```python
def execute_loop_statement(self, stmt: LoopStmt):
    """执行loop循环。

    无限循环执行body，直到遇到exitwhen或抛出ExitLoopSignal。
    """
    while True:
        try:
            for s in stmt.body:
                self.execute_statement(s)
        except ExitLoopSignal:
            break
```

添加execute_exitwhen_statement方法:
```python
def execute_exitwhen_statement(self, stmt: ExitWhenStmt):
    """执行exitwhen语句。

    如果条件为真，抛出ExitLoopSignal退出当前循环。
    """
    if self.evaluator.evaluate_condition(stmt.condition):
        raise ExitLoopSignal()
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/interpreter/test_interpreter.py::test_execute_simple_loop -v
```
Expected: PASS

**Step 5: 提交**

```bash
git add tests/interpreter/test_interpreter.py src/jass_runner/interpreter/interpreter.py
git commit -m "feat(interpreter): 实现loop循环执行

- 添加execute_loop_statement方法
- 添加execute_exitwhen_statement方法
- 使用ExitLoopSignal处理循环退出

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 5: 实现嵌套循环执行

**Files:**
- Test: `tests/interpreter/test_interpreter.py`

**Step 1: 编写测试**

```python
def test_execute_nested_loop():
    """测试执行嵌套循环"""
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
    # 2 * 3 = 6
    assert interpreter.global_context.get_variable("count") == 6
```

**Step 2: 运行测试**

```bash
pytest tests/interpreter/test_interpreter.py::test_execute_nested_loop -v
```
Expected: PASS (ExitLoopSignal应该只影响最内层循环)

**Step 3: 提交**

```bash
git add tests/interpreter/test_interpreter.py
git commit -m "test(interpreter): 添加嵌套循环执行测试

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 6: 实现return语句执行

**Files:**
- Modify: `src/jass_runner/interpreter/interpreter.py`
- Test: `tests/interpreter/test_interpreter.py`

**Step 1: 编写失败测试**

```python
def test_execute_return_nothing():
    """测试执行return nothing"""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.parser import Parser

    code = """
    function main takes nothing returns nothing
        call DisplayTextToPlayer("before return")
        return
        call DisplayTextToPlayer("after return")
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.execute(ast)
    # 如果没有异常，说明正确执行了return
    assert True
```

```python
def test_execute_return_with_value():
    """测试执行带返回值的return"""
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
    assert interpreter.global_context.get_variable("result") == 8
```

```python
def test_execute_early_return():
    """测试提前return"""
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
    assert interpreter.global_context.get_variable("m1") == 5
    assert interpreter.global_context.get_variable("m2") == 7
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/interpreter/test_interpreter.py::test_execute_return_nothing tests/interpreter/test_interpreter.py::test_execute_return_with_value tests/interpreter/test_interpreter.py::test_execute_early_return -v
```
Expected: FAIL (不支持ReturnStmt)

**Step 3: 添加return执行支持**

在execute_statement()中添加:
```python
elif isinstance(statement, ReturnStmt):
    self.execute_return_statement(statement)
```

添加execute_return_statement方法:
```python
def execute_return_statement(self, stmt: ReturnStmt):
    """执行return语句。

    求值返回值（如果有），然后抛出ReturnSignal。
    """
    value = None
    if stmt.value:
        value = self.evaluator.evaluate(stmt.value)
    raise ReturnSignal(value)
```

修改execute_function以处理ReturnSignal:
```python
def execute_function(self, func: FunctionDecl):
    """执行一个函数。"""
    # 为函数执行创建新上下文
    func_context = ExecutionContext(
        self.global_context,
        native_registry=self.global_context.native_registry,
        state_context=self.state_context,
        interpreter=self
    )
    self.current_context = func_context
    self.evaluator.context = func_context

    # 执行函数体
    return_value = None
    try:
        if func.body:
            for statement in func.body:
                self.execute_statement(statement)
    except ReturnSignal as signal:
        return_value = signal.value

    # 恢复之前的上下文
    self.current_context = self.global_context
    self.evaluator.context = self.global_context

    return return_value
```

注意：还需要处理函数调用时的返回值。检查execute_native_call或添加函数调用逻辑。

可能需要添加函数调用的求值支持:
```python
def _evaluate_single_value(self, value: str) -> Any:
    """求值单个值（变量、字面量或函数调用）。"""
    value = value.strip()

    # 处理函数调用，如 add(3, 5)
    if '(' in value and value.endswith(')'):
        func_name = value[:value.index('(')]
        args_str = value[value.index('(')+1:-1]

        # 解析参数
        args = []
        if args_str.strip():
            for arg in args_str.split(','):
                args.append(self.evaluate(arg.strip()))

        # 调用函数
        if func_name in self.context.interpreter.functions:
            func = self.context.interpreter.functions[func_name]
            return self.context.interpreter._call_function_with_args(func, args)
        else:
            raise ValueError(f"未知函数: {func_name}")

    # ... 原有逻辑
```

添加_call_function_with_args方法:
```python
def _call_function_with_args(self, func: FunctionDecl, args: List[Any]):
    """使用指定参数调用函数。"""
    # 创建新上下文
    func_context = ExecutionContext(
        self.global_context,
        native_registry=self.global_context.native_registry,
        state_context=self.state_context,
        interpreter=self
    )

    # 设置参数值
    for param, arg_value in zip(func.parameters, args):
        func_context.set_variable(param.name, arg_value)

    self.current_context = func_context
    self.evaluator.context = func_context

    # 执行函数体
    return_value = None
    try:
        if func.body:
            for statement in func.body:
                self.execute_statement(statement)
    except ReturnSignal as signal:
        return_value = signal.value

    # 恢复上下文
    self.current_context = self.global_context
    self.evaluator.context = self.global_context

    return return_value
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/interpreter/test_interpreter.py::test_execute_return_nothing tests/interpreter/test_interpreter.py::test_execute_return_with_value tests/interpreter/test_interpreter.py::test_execute_early_return -v
```
Expected: PASS

**Step 5: 提交**

```bash
git add tests/interpreter/test_interpreter.py src/jass_runner/interpreter/interpreter.py src/jass_runner/interpreter/evaluator.py
git commit -m "feat(interpreter): 实现return语句执行

- 添加execute_return_statement方法
- 修改execute_function处理ReturnSignal
- 添加函数调用支持以获取返回值
- 支持提前return和带返回值的return

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 7: 添加loop内if和if内loop的集成测试

**Files:**
- Test: `tests/interpreter/test_interpreter.py`

**Step 1: 编写测试**

```python
def test_execute_loop_with_if_inside():
    """测试loop内部有if语句"""
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
    # 0, 2, 4 are even
    assert interpreter.global_context.get_variable("even_count") == 3
```

```python
def test_execute_if_with_loop_inside():
    """测试if内部有loop语句"""
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
    # 1 + 2 + 3 + 4 + 5 = 15
    assert interpreter.global_context.get_variable("sum") == 15
```

**Step 2: 运行测试**

```bash
pytest tests/interpreter/test_interpreter.py::test_execute_loop_with_if_inside tests/interpreter/test_interpreter.py::test_execute_if_with_loop_inside -v
```
Expected: PASS

**Step 3: 提交**

```bash
git add tests/interpreter/test_interpreter.py
git commit -m "test(interpreter): 添加控制流集成测试

- 测试loop内有if
- 测试if内有loop

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Phase 3 完成检查清单

- [x] ReturnSignal和ExitLoopSignal异常类
- [x] if语句执行（if/then/elseif/else/endif）
- [x] 嵌套if语句支持
- [x] loop循环执行
- [x] exitwhen退出循环
- [x] 嵌套循环支持
- [x] return语句执行（提前返回和带值返回）
- [x] 函数调用和返回值支持
- [x] 控制流集成测试（loop内有if、if内有loop）
- [x] 所有测试通过

**下一步:** Phase 4 - 集成测试和示例脚本
