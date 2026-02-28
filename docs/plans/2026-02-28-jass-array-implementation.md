# JASS数组语法支持实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 扩展JASS Runner解释器，支持array语法（声明、赋值、访问）

**Architecture:** 采用分离存储策略，数组和普通变量分开管理；新增AST节点ArrayDecl/ArrayAccess/SetArrayStmt；索引支持任意表达式

**Tech Stack:** Python 3.8+, pytest, 现有JASS Runner解析器和解释器框架

---

## 前置检查

### Task 0: 验证当前项目状态

**Files:**
- Read: `src/jass_runner/parser/ast_nodes.py`
- Read: `src/jass_runner/parser/lexer.py`
- Read: `src/jass_runner/interpreter/context.py`

**Step 1: 确认array关键字已在lexer中**

验证`src/jass_runner/parser/lexer.py`第20-28行的KEYWORDS包含'array'。

**Step 2: 确认现有AST节点结构**

阅读`src/jass_runner/parser/ast_nodes.py`，了解现有节点定义模式。

**Step 3: 确认ExecutionContext结构**

阅读`src/jass_runner/interpreter/context.py`，了解变量存储方式。

---

## 阶段1: AST节点定义

### Task 1: 添加ArrayDecl节点

**Files:**
- Modify: `src/jass_runner/parser/ast_nodes.py`
- Test: `tests/parser/test_ast_nodes.py`（新建）

**Step 1: 编写失败测试**

```python
def test_array_decl_node_exists():
    from jass_runner.parser.ast_nodes import ArrayDecl
    node = ArrayDecl(name="counts", element_type="integer",
                     is_global=True, is_constant=False)
    assert node.name == "counts"
    assert node.element_type == "integer"
    assert node.is_global is True
    assert node.is_constant is False
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/parser/test_ast_nodes.py::test_array_decl_node_exists -v
```
Expected: FAIL - ImportError

**Step 3: 实现ArrayDecl节点**

在`src/jass_runner/parser/ast_nodes.py`末尾添加：

```python
@dataclass
class ArrayDecl:
    """数组声明节点（全局或局部）。

    属性：
        name: 数组名称
        element_type: 元素类型（integer, real, string, boolean, handle等）
        is_global: True表示全局数组，False表示局部数组
        is_constant: 是否常量（仅全局数组可标记为constant）
    """
    name: str
    element_type: str
    is_global: bool
    is_constant: bool = False
```

**Step 4: 运行测试确认通过**

```bash
pytest tests/parser/test_ast_nodes.py::test_array_decl_node_exists -v
```
Expected: PASS

**Step 5: 提交**

```bash
git add tests/parser/test_ast_nodes.py src/jass_runner/parser/ast_nodes.py
git commit -m "feat(ast): 添加ArrayDecl节点"
```

---

### Task 2: 添加ArrayAccess节点

**Files:**
- Modify: `src/jass_runner/parser/ast_nodes.py`
- Test: `tests/parser/test_ast_nodes.py`

**Step 1: 编写失败测试**

```python
def test_array_access_node_exists():
    from jass_runner.parser.ast_nodes import ArrayAccess, VariableExpr
    index = VariableExpr(name="i")
    node = ArrayAccess(array_name="counts", index=index)
    assert node.array_name == "counts"
    assert node.index == index
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/parser/test_ast_nodes.py::test_array_access_node_exists -v
```
Expected: FAIL

**Step 3: 实现ArrayAccess节点**

在`src/jass_runner/parser/ast_nodes.py`添加：

```python
@dataclass
class ArrayAccess:
    """数组访问节点（作为表达式值）。

    属性：
        array_name: 数组名称
        index: 索引表达式（支持任意复杂表达式）
    """
    array_name: str
    index: Any
```

**Step 4: 运行测试确认通过**

```bash
pytest tests/parser/test_ast_nodes.py::test_array_access_node_exists -v
```
Expected: PASS

**Step 5: 提交**

```bash
git add src/jass_runner/parser/ast_nodes.py tests/parser/test_ast_nodes.py
git commit -m "feat(ast): 添加ArrayAccess节点"
```

---

### Task 3: 添加SetArrayStmt节点

**Files:**
- Modify: `src/jass_runner/parser/ast_nodes.py`
- Test: `tests/parser/test_ast_nodes.py`

**Step 1: 编写失败测试**

```python
def test_set_array_stmt_node_exists():
    from jass_runner.parser.ast_nodes import SetArrayStmt, IntegerExpr, VariableExpr
    index = VariableExpr(name="i")
    value = IntegerExpr(value=10)
    node = SetArrayStmt(array_name="counts", index=index, value=value)
    assert node.array_name == "counts"
    assert node.index == index
    assert node.value == value
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/parser/test_ast_nodes.py::test_set_array_stmt_node_exists -v
```
Expected: FAIL

**Step 3: 实现SetArrayStmt节点**

在`src/jass_runner/parser/ast_nodes.py`添加：

```python
@dataclass
class SetArrayStmt:
    """数组元素赋值语句节点。

    属性：
        array_name: 数组名称
        index: 索引表达式
        value: 右侧值表达式
    """
    array_name: str
    index: Any
    value: Any
```

**Step 4: 运行测试确认通过**

```bash
pytest tests/parser/test_ast_nodes.py::test_set_array_stmt_node_exists -v
```
Expected: PASS

**Step 5: 提交**

```bash
git add src/jass_runner/parser/ast_nodes.py tests/parser/test_ast_nodes.py
git commit -m "feat(ast): 添加SetArrayStmt节点"
```

---

## 阶段2: 解析器扩展

### Task 4: 扩展全局数组声明解析

**Files:**
- Modify: `src/jass_runner/parser/global_parser.py`
- Test: `tests/parser/test_globals.py`

**Step 1: 编写失败测试**

```python
def test_parse_global_integer_array():
    from jass_runner.parser.parser import JassParser
    code = """
    globals
        integer array counts
    endglobals
    """
    parser = JassParser()
    result = parser.parse(code)
    assert len(result.globals) == 1
    assert result.globals[0].name == "counts"
    assert result.globals[0].element_type == "integer"
    assert result.globals[0].is_global is True
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/parser/test_globals.py::test_parse_global_integer_array -v
```
Expected: FAIL

**Step 3: 修改全局变量解析器**

在`src/jass_runner/parser/global_parser.py`的`parse_global_declaration`方法中：

1. 在类型关键字后检查`array`关键字
2. 如果是数组，返回ArrayDecl节点
3. 检查数组声明不能有初始化

```python
def parse_global_declaration(self) -> Optional[Any]:
    """解析单个全局变量声明。

    格式: [constant] <type> [array] <name> [= <initial_value>]
    注意: array声明不支持初始化
    """
    # ... 现有constant检查代码 ...

    # 获取变量类型
    var_type = self.current_token.value
    if var_type not in self.TYPE_KEYWORDS:
        return None
    self.next_token()

    # 检查是否是数组声明
    is_array = False
    if self.current_token.type == TokenType.KEYWORD and \
       self.current_token.value == 'array':
        is_array = True
        self.next_token()

    # 获取变量名
    if self.current_token.type != TokenType.IDENTIFIER:
        return None
    var_name = self.current_token.value
    self.next_token()

    # 数组声明不支持初始化
    if is_array:
        if self.current_token.value == '=':
            self.errors.append(ParseError(
                "数组声明不支持初始化",
                self.current_token.line,
                self.current_token.column
            ))
            return None
        return ArrayDecl(
            name=var_name,
            element_type=var_type,
            is_global=True,
            is_constant=is_constant
        )

    # ... 普通变量声明的现有代码 ...
```

**Step 4: 运行测试确认通过**

```bash
pytest tests/parser/test_globals.py::test_parse_global_integer_array -v
```
Expected: PASS

**Step 5: 添加更多测试并提交**

```python
def test_parse_global_constant_unit_array():
    from jass_runner.parser.parser import JassParser
    code = """
    globals
        constant unit array heroes
    endglobals
    """
    parser = JassParser()
    result = parser.parse(code)
    assert len(result.globals) == 1
    assert result.globals[0].name == "heroes"
    assert result.globals[0].element_type == "unit"
    assert result.globals[0].is_constant is True
```

```bash
pytest tests/parser/test_globals.py -v
git add tests/parser/test_globals.py src/jass_runner/parser/global_parser.py
git commit -m "feat(parser): 支持全局数组声明解析"
```

---

### Task 5: 扩展局部数组声明解析

**Files:**
- Modify: `src/jass_runner/parser/assignment_parser.py`
- Test: `tests/parser/test_assignment.py`

**Step 1: 编写失败测试**

```python
def test_parse_local_integer_array():
    from jass_runner.parser.parser import JassParser
    code = """
    function Test takes nothing returns nothing
        local integer array temp
    endfunction
    """
    parser = JassParser()
    result = parser.parse(code)
    func = result.functions[0]
    assert len(func.locals) == 1
    assert func.locals[0].name == "temp"
    assert func.locals[0].element_type == "integer"
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/parser/test_assignment.py::test_parse_local_integer_array -v
```
Expected: FAIL

**Step 3: 修改局部变量解析器**

在`src/jass_runner/parser/assignment_parser.py`的`parse_local_declaration`方法中：

```python
def parse_local_declaration(self) -> Optional[Any]:
    """解析局部变量声明。

    格式: local <type> [array] <name> [= <value>]
    """
    # 跳过'local'关键字
    self.next_token()

    # 获取类型
    if self.current_token.type != TokenType.KEYWORD:
        return None
    var_type = self.current_token.value
    self.next_token()

    # 检查是否是数组
    is_array = False
    if self.current_token.type == TokenType.KEYWORD and \
       self.current_token.value == 'array':
        is_array = True
        self.next_token()

    # 获取变量名
    if self.current_token.type != TokenType.IDENTIFIER:
        return None
    var_name = self.current_token.value
    self.next_token()

    # 检查名称冲突
    if var_name in self.global_names:
        self.errors.append(ParseError(
            f"局部变量'{var_name}'与全局变量同名",
            self.current_token.line,
            self.current_token.column
        ))
        return None

    # 数组声明不支持初始化
    if is_array:
        if self.current_token.value == '=':
            self.errors.append(ParseError(
                "数组声明不支持初始化",
                self.current_token.line,
                self.current_token.column
            ))
            return None
        return ArrayDecl(
            name=var_name,
            element_type=var_type,
            is_global=False
        )

    # ... 普通局部变量声明的现有代码 ...
```

**Step 4: 运行测试确认通过**

```bash
pytest tests/parser/test_assignment.py::test_parse_local_integer_array -v
```
Expected: PASS

**Step 5: 提交**

```bash
git add tests/parser/test_assignment.py src/jass_runner/parser/assignment_parser.py
git commit -m "feat(parser): 支持局部数组声明解析"
```

---

### Task 6: 扩展表达式解析支持数组访问

**Files:**
- Modify: `src/jass_runner/parser/expression_parser.py`
- Test: `tests/parser/test_expressions.py`

**Step 1: 编写失败测试**

```python
def test_parse_array_access_expression():
    from jass_runner.parser.parser import JassParser
    code = """
    function Test takes nothing returns nothing
        local integer x
        local integer array arr
        set x = arr[0]
    endfunction
    """
    parser = JassParser()
    result = parser.parse(code)
    func = result.functions[0]
    set_stmt = func.body[2]  # 第三个语句是set
    # 验证右侧是ArrayAccess节点
    from jass_runner.parser.ast_nodes import ArrayAccess
    assert isinstance(set_stmt.value, ArrayAccess)
    assert set_stmt.value.array_name == "arr"
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/parser/test_expressions.py::test_parse_array_access_expression -v
```
Expected: FAIL

**Step 3: 修改表达式解析器**

在`src/jass_runner/parser/expression_parser.py`中，修改`parse_primary`方法：

```python
def parse_primary(self) -> Optional[Any]:
    """解析基本表达式（标识符、字面量、括号表达式、数组访问）。"""
    token = self.current_token

    if token.type == TokenType.IDENTIFIER:
        self.next_token()

        # 检查是否是数组访问 arr[...]
        if self.current_token.value == '[':
            return self._parse_array_access(token.value)

        # ... 现有代码（函数调用检查等）...
        return VariableExpr(name=token.value)

    # ... 其他现有代码 ...

def _parse_array_access(self, array_name: str) -> Optional[ArrayAccess]:
    """解析数组访问 [index]。"""
    self.next_token()  # 跳过 '['

    # 解析索引表达式
    index = self.parse_expression()
    if index is None:
        self.errors.append(ParseError(
            "数组索引表达式无效",
            self.current_token.line,
            self.current_token.column
        ))
        return None

    # 期望 ']'
    if self.current_token.value != ']':
        self.errors.append(ParseError(
            "期望']'结束数组索引",
            self.current_token.line,
            self.current_token.column
        ))
        return None
    self.next_token()

    return ArrayAccess(array_name=array_name, index=index)
```

**Step 4: 运行测试确认通过**

```bash
pytest tests/parser/test_expressions.py::test_parse_array_access_expression -v
```
Expected: PASS

**Step 5: 添加复杂索引测试并提交**

```python
def test_parse_array_access_with_complex_index():
    from jass_runner.parser.parser import JassParser
    code = """
    function Test takes nothing returns nothing
        local integer x
        local integer i
        local integer array arr
        set x = arr[i * 20 + 1]
    endfunction
    """
    parser = JassParser()
    result = parser.parse(code)
    func = result.functions[0]
    set_stmt = func.body[3]
    from jass_runner.parser.ast_nodes import ArrayAccess, BinaryExpr
    assert isinstance(set_stmt.value, ArrayAccess)
    # 验证索引是二元表达式
    assert isinstance(set_stmt.value.index, BinaryExpr)
```

```bash
pytest tests/parser/test_expressions.py -v
git add tests/parser/test_expressions.py src/jass_runner/parser/expression_parser.py
git commit -m "feat(parser): 支持数组访问表达式解析"
```

---

### Task 7: 扩展赋值语句解析支持数组赋值

**Files:**
- Modify: `src/jass_runner/parser/assignment_parser.py`
- Test: `tests/parser/test_assignment.py`

**Step 1: 编写失败测试**

```python
def test_parse_set_array_statement():
    from jass_runner.parser.parser import JassParser
    code = """
    function Test takes nothing returns nothing
        local integer array arr
        set arr[0] = 10
    endfunction
    """
    parser = JassParser()
    result = parser.parse(code)
    func = result.functions[0]
    set_stmt = func.body[1]
    from jass_runner.parser.ast_nodes import SetArrayStmt
    assert isinstance(set_stmt, SetArrayStmt)
    assert set_stmt.array_name == "arr"
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/parser/test_assignment.py::test_parse_set_array_statement -v
```
Expected: FAIL

**Step 3: 修改赋值解析器**

在`src/jass_runner/parser/assignment_parser.py`的`parse_set_statement`方法中：

```python
def parse_set_statement(self) -> Optional[Any]:
    """解析set语句（支持普通变量和数组元素）。"""
    # 跳过'set'关键字
    self.next_token()

    # 获取变量名
    if self.current_token.type != TokenType.IDENTIFIER:
        return None
    var_name = self.current_token.value
    self.next_token()

    # 检查是否是数组赋值 arr[...] = ...
    if self.current_token.value == '[':
        return self._parse_set_array_statement(var_name)

    # ... 普通变量赋值的现有代码 ...

def _parse_set_array_statement(self, array_name: str) -> Optional[SetArrayStmt]:
    """解析数组元素赋值语句。"""
    # 当前token是'['
    self.next_token()

    # 解析索引表达式
    index = self.parse_expression()
    if index is None:
        self.errors.append(ParseError(
            "数组索引表达式无效",
            self.current_token.line,
            self.current_token.column
        ))
        return None

    # 期望']'
    if self.current_token.value != ']':
        self.errors.append(ParseError(
            "期望']'结束数组索引",
            self.current_token.line,
            self.current_token.column
        ))
        return None
    self.next_token()

    # 期望'='
    if self.current_token.value != '=':
        self.errors.append(ParseError(
            "数组赋值期望'='",
            self.current_token.line,
            self.current_token.column
        ))
        return None
    self.next_token()

    # 解析右侧值
    value = self.parse_expression()
    if value is None:
        self.errors.append(ParseError(
            "数组赋值右侧表达式无效",
            self.current_token.line,
            self.current_token.column
        ))
        return None

    return SetArrayStmt(
        array_name=array_name,
        index=index,
        value=value
    )
```

**Step 4: 运行测试确认通过**

```bash
pytest tests/parser/test_assignment.py::test_parse_set_array_statement -v
```
Expected: PASS

**Step 5: 提交**

```bash
git add tests/parser/test_assignment.py src/jass_runner/parser/assignment_parser.py
git commit -m "feat(parser): 支持数组赋值语句解析"
```

---

## 阶段3: 执行上下文扩展

### Task 8: 添加数组存储和管理方法

**Files:**
- Modify: `src/jass_runner/interpreter/context.py`
- Test: `tests/interpreter/test_context.py`

**Step 1: 编写失败测试**

```python
def test_declare_array():
    from jass_runner.interpreter.context import ExecutionContext
    context = ExecutionContext()
    context.declare_array("counts", "integer")
    assert "counts" in context.arrays
    assert len(context.arrays["counts"]) == 8192
    assert context.arrays["counts"][0] == 0

def test_get_set_array_element():
    from jass_runner.interpreter.context import ExecutionContext
    context = ExecutionContext()
    context.declare_array("counts", "integer")
    context.set_array_element("counts", 5, 100)
    assert context.get_array_element("counts", 5) == 100
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/interpreter/test_context.py::test_declare_array -v
```
Expected: FAIL

**Step 3: 实现数组存储方法**

在`src/jass_runner/interpreter/context.py`中修改`ExecutionContext`类：

```python
def __init__(self, parent=None, global_names=None, constant_names=None):
    """初始化执行上下文。

    参数：
        parent: 父上下文（用于函数调用链）
        global_names: 全局变量名集合
        constant_names: 常量名集合
    """
    self.variables: Dict[str, Any] = {}
    self.arrays: Dict[str, List[Any]] = {}  # 数组变量存储
    self.parent = parent
    self.global_names = global_names or set()
    self.constant_names = constant_names or set()
    self._array_size = 8192  # JASS数组标准大小

    # 类型默认值映射
    self._default_values = {
        'integer': 0,
        'real': 0.0,
        'string': None,
        'boolean': False,
        'handle': None,
    }

def declare_array(self, name: str, element_type: str):
    """声明数组，初始化8192个元素为类型默认值。

    参数：
        name: 数组名称
        element_type: 元素类型
    """
    default_value = self._default_values.get(element_type, None)
    self.arrays[name] = [default_value] * self._array_size

def get_array_element(self, name: str, index: int) -> Any:
    """获取数组元素（不做边界检查）。

    参数：
        name: 数组名称
        index: 元素索引

    返回：
        数组元素值

    异常：
        NameError: 数组未声明
    """
    if name not in self.arrays:
        if self.parent:
            return self.parent.get_array_element(name, index)
        raise NameError(f"数组'{name}'未声明")
    return self.arrays[name][index]

def set_array_element(self, name: str, index: int, value: Any):
    """设置数组元素（不做边界检查）。

    参数：
        name: 数组名称
        index: 元素索引
        value: 要设置的值

    异常：
        NameError: 数组未声明
    """
    if name not in self.arrays:
        if self.parent:
            self.parent.set_array_element(name, index, value)
            return
        raise NameError(f"数组'{name}'未声明")
    self.arrays[name][index] = value
```

**Step 4: 运行测试确认通过**

```bash
pytest tests/interpreter/test_context.py::test_declare_array tests/interpreter/test_context.py::test_get_set_array_element -v
```
Expected: PASS

**Step 5: 提交**

```bash
git add tests/interpreter/test_context.py src/jass_runner/interpreter/context.py
git commit -m "feat(context): 添加数组存储和管理方法"
```

---

## 阶段4: 解释器扩展

### Task 9: 实现数组声明执行

**Files:**
- Modify: `src/jass_runner/interpreter/interpreter.py`
- Test: `tests/interpreter/test_interpreter.py`

**Step 1: 编写失败测试**

```python
def test_execute_global_array_declaration():
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.ast_nodes import ArrayDecl

    interpreter = Interpreter()
    decl = ArrayDecl(name="counts", element_type="integer",
                     is_global=True, is_constant=False)
    interpreter.execute_statement(decl)

    assert "counts" in interpreter.current_context.arrays
    assert interpreter.current_context.arrays["counts"][0] == 0
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/interpreter/test_interpreter.py::test_execute_global_array_declaration -v
```
Expected: FAIL

**Step 3: 实现数组声明执行**

在`src/jass_runner/interpreter/interpreter.py`中：

```python
def execute_statement(self, statement: Any):
    """执行单个语句。"""
    if isinstance(statement, ArrayDecl):
        self.execute_array_declaration(statement)
    elif isinstance(statement, SetArrayStmt):
        self.execute_set_array_statement(statement)
    # ... 现有代码 ...

def execute_array_declaration(self, stmt: ArrayDecl):
    """执行数组声明。

    参数：
        stmt: 数组声明节点
    """
    self.current_context.declare_array(stmt.name, stmt.element_type)
```

**Step 4: 运行测试确认通过**

```bash
pytest tests/interpreter/test_interpreter.py::test_execute_global_array_declaration -v
```
Expected: PASS

**Step 5: 提交**

```bash
git add tests/interpreter/test_interpreter.py src/jass_runner/interpreter/interpreter.py
git commit -m "feat(interpreter): 支持数组声明执行"
```

---

### Task 10: 实现数组赋值执行

**Files:**
- Modify: `src/jass_runner/interpreter/interpreter.py`
- Test: `tests/interpreter/test_interpreter.py`

**Step 1: 编写失败测试**

```python
def test_execute_set_array_statement():
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.ast_nodes import ArrayDecl, SetArrayStmt, IntegerExpr

    interpreter = Interpreter()

    # 先声明数组
    decl = ArrayDecl(name="counts", element_type="integer",
                     is_global=True, is_constant=False)
    interpreter.execute_statement(decl)

    # 执行赋值
    set_stmt = SetArrayStmt(
        array_name="counts",
        index=IntegerExpr(value=5),
        value=IntegerExpr(value=100)
    )
    interpreter.execute_statement(set_stmt)

    assert interpreter.current_context.get_array_element("counts", 5) == 100
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/interpreter/test_interpreter.py::test_execute_set_array_statement -v
```
Expected: FAIL

**Step 3: 实现数组赋值执行**

在`src/jass_runner/interpreter/interpreter.py`中：

```python
def execute_set_array_statement(self, stmt: SetArrayStmt):
    """执行数组元素赋值。

    参数：
        stmt: 数组赋值语句节点
    """
    # 求值索引表达式
    index = self.evaluator.evaluate(stmt.index)
    # 求值右侧值
    value = self.evaluator.evaluate(stmt.value)
    # 设置数组元素
    self.current_context.set_array_element(stmt.array_name, int(index), value)
```

**Step 4: 运行测试确认通过**

```bash
pytest tests/interpreter/test_interpreter.py::test_execute_set_array_statement -v
```
Expected: PASS

**Step 5: 提交**

```bash
git add tests/interpreter/test_interpreter.py src/jass_runner/interpreter/interpreter.py
git commit -m "feat(interpreter): 支持数组赋值执行"
```

---

## 阶段5: 求值器扩展

### Task 11: 实现数组访问求值

**Files:**
- Modify: `src/jass_runner/interpreter/evaluator.py`
- Test: `tests/interpreter/test_evaluator.py`

**Step 1: 编写失败测试**

```python
def test_evaluate_array_access():
    from jass_runner.interpreter.evaluator import Evaluator
    from jass_runner.interpreter.context import ExecutionContext
    from jass_runner.parser.ast_nodes import ArrayAccess, IntegerExpr

    context = ExecutionContext()
    context.declare_array("counts", "integer")
    context.set_array_element("counts", 5, 100)

    evaluator = Evaluator(context)
    access = ArrayAccess(array_name="counts", index=IntegerExpr(value=5))
    result = evaluator.evaluate(access)

    assert result == 100
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/interpreter/test_evaluator.py::test_evaluate_array_access -v
```
Expected: FAIL

**Step 3: 实现数组访问求值**

在`src/jass_runner/interpreter/evaluator.py`中：

```python
def evaluate(self, expression: Any) -> Any:
    """求值表达式。"""
    if isinstance(expression, ArrayAccess):
        return self._evaluate_array_access(expression)
    # ... 现有代码 ...

def _evaluate_array_access(self, access: ArrayAccess) -> Any:
    """求值数组访问表达式。

    参数：
        access: 数组访问节点

    返回：
        数组元素值
    """
    # 递归求值索引表达式（支持复杂表达式如 i * 20 + 1）
    index = self.evaluate(access.index)
    return self.context.get_array_element(access.array_name, int(index))
```

**Step 4: 运行测试确认通过**

```bash
pytest tests/interpreter/test_evaluator.py::test_evaluate_array_access -v
```
Expected: PASS

**Step 5: 添加复杂索引测试并提交**

```python
def test_evaluate_array_access_with_complex_index():
    from jass_runner.interpreter.evaluator import Evaluator
    from jass_runner.interpreter.context import ExecutionContext
    from jass_runner.parser.ast_nodes import ArrayAccess, BinaryExpr, VariableExpr, IntegerExpr

    context = ExecutionContext()
    context.declare_array("counts", "integer")
    context.set_variable("i", 2)
    context.set_array_element("counts", 41, 999)  # i * 20 + 1 = 41

    evaluator = Evaluator(context)
    # 表达式: counts[i * 20 + 1]
    index_expr = BinaryExpr(
        left=BinaryExpr(
            left=VariableExpr(name="i"),
            operator="*",
            right=IntegerExpr(value=20)
        ),
        operator="+",
        right=IntegerExpr(value=1)
    )
    access = ArrayAccess(array_name="counts", index=index_expr)
    result = evaluator.evaluate(access)

    assert result == 999
```

```bash
pytest tests/interpreter/test_evaluator.py -v
git add tests/interpreter/test_evaluator.py src/jass_runner/interpreter/evaluator.py
git commit -m "feat(evaluator): 支持数组访问求值"
```

---

## 阶段6: 集成测试

### Task 12: 创建完整数组功能集成测试

**Files:**
- Create: `tests/integration/test_array_integration.py`
- Create: `examples/array_demo.j`

**Step 1: 编写集成测试**

```python
def test_complete_array_workflow():
    """测试完整的数组声明、赋值、访问流程。"""
    from jass_runner.parser.parser import JassParser
    from jass_runner.interpreter.interpreter import Interpreter

    code = """
    globals
        integer array scores
    endglobals

    function Test takes nothing returns nothing
        local integer array temp
        local integer i

        set scores[0] = 100
        set i = 2
        set temp[i * 20 + 1] = scores[0] + 50
    endfunction
    """

    # 解析
    parser = JassParser()
    ast = parser.parse(code)
    assert len(parser.errors) == 0

    # 执行
    interpreter = Interpreter()
    interpreter.execute(ast)

    # 验证全局数组
    assert interpreter.current_context.get_array_element("scores", 0) == 100
    # 验证局部数组（在函数上下文中）
    # 注意：函数执行后局部变量会被清理，需要调整测试策略
```

**Step 2: 运行测试**

```bash
pytest tests/integration/test_array_integration.py -v
```

**Step 3: 创建示例JASS脚本**

```jass
// examples/array_demo.j
// 数组功能演示

globals
    integer array playerScores
    string array playerNames
endglobals

function InitArrays takes nothing returns nothing
    local integer i
    local integer array tempScores

    // 初始化全局数组
    set playerScores[0] = 100
    set playerScores[1] = 200
    set playerNames[0] = "Player1"

    // 使用局部数组
    set i = 0
    set tempScores[i] = playerScores[0] + 50
    set tempScores[i + 1] = tempScores[i] * 2
endfunction
```

**Step 4: 提交**

```bash
git add tests/integration/test_array_integration.py examples/array_demo.j
git commit -m "test(integration): 添加数组功能集成测试和示例"
```

---

## 阶段7: 验证和文档更新

### Task 13: 运行完整测试套件

**Step 1: 运行所有测试**

```bash
pytest tests/ -v --tb=short
```
Expected: 所有测试通过

**Step 2: 验证示例脚本**

```bash
python -m jass_runner examples/array_demo.j
```
Expected: 成功执行，无错误

**Step 3: 提交**

```bash
git commit -m "test: 验证数组功能完整测试通过" --allow-empty
```

---

### Task 14: 更新PROJECT_NOTES.md

**Files:**
- Modify: `PROJECT_NOTES.md`

**Step 1: 添加数组功能完成记录**

在PROJECT_NOTES.md的"已完成功能"部分添加：

```markdown
## 2026-02-28 - 数组语法支持

### 新增功能
- 全局数组声明：`integer array counts`
- 局部数组声明：`local integer array temp`
- 数组元素赋值：`set arr[i] = value`
- 数组元素访问：`set x = arr[i]`
- 复杂索引表达式：`arr[x * 20 + 1]`

### 技术实现
- AST节点：ArrayDecl, ArrayAccess, SetArrayStmt
- 数组大小：8192（索引0-8191）
- 存储策略：分离存储（self.arrays）
- 默认值：integer=0, real=0.0, string=null, boolean=false, handle=null

### 限制
- 不支持声明时初始化
- 不支持多维数组
- 不进行运行时边界检查
```

**Step 2: 提交**

```bash
git add PROJECT_NOTES.md
git commit -m "docs: 更新项目笔记记录数组功能完成"
```

---

## 完成总结

所有任务完成后，JASS Runner将支持：

1. **数组声明**：全局和局部数组声明
2. **数组赋值**：支持任意表达式作为索引
3. **数组访问**：作为右值使用
4. **多种类型**：integer, real, string, boolean, handle数组
5. **标准大小**：8192元素（0-8191索引）

**验证命令**：
```bash
pytest tests/ -v
python -m jass_runner examples/array_demo.j
```
