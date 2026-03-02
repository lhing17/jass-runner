# 类型检查系统实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现JASS运行时类型检查系统，验证赋值和传参的类型兼容性

**Architecture:** 创建独立的TypeChecker组件，在Interpreter执行赋值和函数调用时进行类型验证，支持integer→real隐式转换和handle子类型协变

**Tech Stack:** Python 3.8+, pytest

---

## 前置信息

### 相关设计文档
- `docs/plans/2026-03-02-type-checker-design.md` - 类型检查系统设计文档

### 关键现有文件
- `src/jass_runner/interpreter/interpreter.py` - 解释器核心
- `src/jass_runner/interpreter/context.py` - 执行上下文
- `src/jass_runner/parser/ast_nodes.py` - AST节点定义（包含类型信息）

---

## Task 1: 创建 JassTypeError 异常类

**Files:**
- Create: `src/jass_runner/types/__init__.py`
- Create: `src/jass_runner/types/errors.py`
- Test: `tests/types/test_errors.py`

**Step 1: 编写失败测试**

```python
def test_jass_type_error_creation():
    """测试JassTypeError异常创建。"""
    from jass_runner.types.errors import JassTypeError

    error = JassTypeError(
        message="类型错误测试",
        source_type="string",
        target_type="integer",
        line=5,
        column=10
    )

    assert str(error) == "类型错误测试"
    assert error.source_type == "string"
    assert error.target_type == "integer"
    assert error.line == 5
    assert error.column == 10
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/types/test_errors.py::test_jass_type_error_creation -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'jass_runner.types'"

**Step 3: 实现异常类**

```python
"""JASS类型系统错误类。"""


class JassTypeError(TypeError):
    """JASS类型错误异常。

    当类型检查失败时抛出，包含详细的类型和位置信息。

    属性：
        source_type: 源类型名称
        target_type: 目标类型名称
        line: 源代码行号（可选）
        column: 源代码列号（可选）
    """

    def __init__(self, message: str, source_type: str, target_type: str,
                 line: int = None, column: int = None):
        super().__init__(message)
        self.source_type = source_type
        self.target_type = target_type
        self.line = line
        self.column = column
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/types/test_errors.py::test_jass_type_error_creation -v
```

Expected: PASS

**Step 5: 提交**

```bash
git add src/jass_runner/types/ tests/types/
git commit -m "feat(types): add JassTypeError exception class"
```

---

## Task 2: 创建 TypeHierarchy 类型层次管理

**Files:**
- Create: `src/jass_runner/types/hierarchy.py`
- Test: `tests/types/test_hierarchy.py`

**Step 1: 编写失败测试**

```python
def test_is_subtype_unit_to_handle():
    """unit是handle的子类型。"""
    from jass_runner.types.hierarchy import TypeHierarchy

    assert TypeHierarchy.is_subtype('unit', 'handle') is True


def test_is_subtype_handle_to_unit():
    """handle不是unit的子类型。"""
    from jass_runner.types.hierarchy import TypeHierarchy

    assert TypeHierarchy.is_subtype('handle', 'unit') is False


def test_get_base_type_of_unit():
    """获取unit的基类型。"""
    from jass_runner.types.hierarchy import TypeHierarchy

    assert TypeHierarchy.get_base_type('unit') == 'handle'


def test_get_base_type_of_integer():
    """基础类型的基类型是其自身。"""
    from jass_runner.types.hierarchy import TypeHierarchy

    assert TypeHierarchy.get_base_type('integer') == 'integer'
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/types/test_hierarchy.py -v
```

Expected: FAIL with "ModuleNotFoundError"

**Step 3: 实现 TypeHierarchy 类**

```python
"""JASS类型层次结构管理。"""


class TypeHierarchy:
    """管理JASS类型之间的继承关系。

    JASS使用handle作为所有游戏对象的基类，
    unit、item、timer等都继承自handle。
    """

    # handle子类型映射: {子类型: 父类型}
    HANDLE_SUBTYPES = {
        'unit': 'handle',
        'item': 'handle',
        'timer': 'handle',
        'trigger': 'handle',
        'player': 'handle',
        'destructable': 'handle',
        'itempool': 'handle',
        'unitpool': 'handle',
        'group': 'handle',
        'force': 'handle',
        'rect': 'handle',
        'region': 'handle',
        'sound': 'handle',
        'effect': 'handle',
        'location': 'handle',
    }

    @classmethod
    def is_subtype(cls, subtype: str, basetype: str) -> bool:
        """判断subtype是否是basetype的子类型。

        参数：
            subtype: 子类型名称
            basetype: 基类型名称

        返回：
            如果是子类型返回True，否则返回False
        """
        if subtype == basetype:
            return True

        # 检查handle类型层次
        current = subtype
        while current in cls.HANDLE_SUBTYPES:
            parent = cls.HANDLE_SUBTYPES[current]
            if parent == basetype:
                return True
            current = parent

        return False

    @classmethod
    def get_base_type(cls, type_name: str) -> str:
        """获取类型的基类型。

        对于handle子类型，返回'handle'。
        对于其他类型，返回其自身。

        参数：
            type_name: 类型名称

        返回：
            基类型名称
        """
        if type_name in cls.HANDLE_SUBTYPES:
            return cls.HANDLE_SUBTYPES[type_name]
        return type_name
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/types/test_hierarchy.py -v
```

Expected: PASS

**Step 5: 提交**

```bash
git add src/jass_runner/types/hierarchy.py tests/types/test_hierarchy.py
git commit -m "feat(types): add TypeHierarchy for handle subtype management"
```

---

## Task 3: 创建 TypeChecker 核心类

**Files:**
- Create: `src/jass_runner/types/checker.py`
- Modify: `src/jass_runner/types/__init__.py`
- Test: `tests/types/test_checker.py`

**Step 1: 编写失败测试**

```python
import pytest
from jass_runner.types.errors import JassTypeError


def test_is_compatible_same_type():
    """相同类型总是兼容。"""
    from jass_runner.types.checker import TypeChecker

    checker = TypeChecker()
    assert checker.is_compatible('integer', 'integer') is True
    assert checker.is_compatible('real', 'real') is True


def test_is_compatible_integer_to_real():
    """integer可隐式转为real。"""
    from jass_runner.types.checker import TypeChecker

    checker = TypeChecker()
    assert checker.is_compatible('integer', 'real') is True


def test_is_compatible_real_to_integer():
    """real不可隐式转为integer。"""
    from jass_runner.types.checker import TypeChecker

    checker = TypeChecker()
    assert checker.is_compatible('real', 'integer') is False


def test_is_compatible_unit_to_handle():
    """unit可赋值给handle（协变）。"""
    from jass_runner.types.checker import TypeChecker

    checker = TypeChecker()
    assert checker.is_compatible('unit', 'handle') is True


def test_check_assignment_integer_to_real():
    """integer赋值给real变量应转换成功。"""
    from jass_runner.types.checker import TypeChecker

    checker = TypeChecker()
    result = checker.check_assignment('real', 10, 'integer')

    assert result == 10.0
    assert isinstance(result, float)


def test_check_assignment_string_to_integer_raises():
    """string赋值给integer应抛出异常。"""
    from jass_runner.types.checker import TypeChecker

    checker = TypeChecker()

    with pytest.raises(JassTypeError) as exc_info:
        checker.check_assignment('integer', 'hello', 'string')

    assert 'string' in str(exc_info.value)
    assert 'integer' in str(exc_info.value)
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/types/test_checker.py -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'jass_runner.types.checker'"

**Step 3: 实现 TypeChecker 类**

```python
"""JASS运行时类型检查器。"""

from typing import Any
from .errors import JassTypeError
from .hierarchy import TypeHierarchy


class TypeChecker:
    """JASS运行时类型检查器。

    负责验证类型兼容性并执行允许的隐式类型转换。

    支持的隐式转换：
    - integer -> real
    - handle子类型 -> handle
    """

    # 允许的隐式转换规则: {目标类型: [允许的来源类型列表]}
    _ALLOWED_IMPLICIT_CONVERSIONS = {
        'real': ['integer'],
    }

    def is_compatible(self, source_type: str, target_type: str) -> bool:
        """判断源类型是否可以隐式赋值给目标类型。

        规则：
        1. 类型完全相同：允许
        2. 目标类型在转换规则中且源类型在允许列表中：允许
        3. handle子类型可赋值给handle父类型：允许

        参数：
            source_type: 源类型名称
            target_type: 目标类型名称

        返回：
            如果兼容返回True，否则返回False
        """
        # 类型完全相同
        if source_type == target_type:
            return True

        # 检查handle子类型协变
        if target_type == 'handle':
            return TypeHierarchy.is_subtype(source_type, 'handle')

        # 检查隐式转换规则
        if target_type in self._ALLOWED_IMPLICIT_CONVERSIONS:
            allowed_sources = self._ALLOWED_IMPLICIT_CONVERSIONS[target_type]
            if source_type in allowed_sources:
                return True

        return False

    def check_assignment(self, target_type: str, value: Any,
                        value_type: str, line: int = None,
                        column: int = None) -> Any:
        """检查赋值操作是否合法，返回转换后的值。

        参数：
            target_type: 目标变量声明类型
            value: 要赋的值
            value_type: 值的实际类型
            line: 源代码行号（用于错误报告）
            column: 源代码列号（用于错误报告）

        返回：
            转换后的值

        抛出：
            JassTypeError: 类型不兼容
        """
        if not self.is_compatible(value_type, target_type):
            raise JassTypeError(
                message=f"类型错误：不能将'{value_type}'类型的值赋值给'{target_type}'类型的变量",
                source_type=value_type,
                target_type=target_type,
                line=line,
                column=column
            )

        # 执行转换
        if value_type == 'integer' and target_type == 'real':
            return float(value)

        return value

    def check_function_arg(self, param_type: str, arg_value: Any,
                          arg_type: str, line: int = None,
                          column: int = None) -> Any:
        """检查函数参数类型是否匹配。

        参数：
            param_type: 形参声明类型
            arg_value: 实参值
            arg_type: 实参类型
            line: 源代码行号
            column: 源代码列号

        返回：
            转换后的值

        抛出：
            JassTypeError: 类型不兼容
        """
        if not self.is_compatible(arg_type, param_type):
            raise JassTypeError(
                message=f"类型错误：参数类型不匹配，期望'{param_type}'，实际得到'{arg_type}'",
                source_type=arg_type,
                target_type=param_type,
                line=line,
                column=column
            )

        # 执行转换
        if arg_type == 'integer' and param_type == 'real':
            return float(arg_value)

        return arg_value

    def check_return_value(self, return_type: str, value: Any,
                          value_type: str, line: int = None,
                          column: int = None) -> Any:
        """检查返回值类型是否匹配。

        参数：
            return_type: 函数声明的返回类型
            value: 返回值
            value_type: 返回值类型
            line: 源代码行号
            column: 源代码列号

        返回：
            转换后的值

        抛出：
            JassTypeError: 类型不兼容
        """
        if return_type == 'nothing':
            return value

        if not self.is_compatible(value_type, return_type):
            raise JassTypeError(
                message=f"类型错误：返回值类型不匹配，期望'{return_type}'，实际得到'{value_type}'",
                source_type=value_type,
                target_type=return_type,
                line=line,
                column=column
            )

        # 执行转换
        if value_type == 'integer' and return_type == 'real':
            return float(value)

        return value
```

**Step 4: 更新 types 模块导出**

```python
"""JASS类型系统模块。

此模块提供JASS运行时类型检查功能。
"""

from .errors import JassTypeError
from .hierarchy import TypeHierarchy
from .checker import TypeChecker

__all__ = ['JassTypeError', 'TypeHierarchy', 'TypeChecker']
```

**Step 5: 运行测试验证通过**

```bash
pytest tests/types/test_checker.py -v
```

Expected: PASS

**Step 6: 提交**

```bash
git add src/jass_runner/types/ tests/types/test_checker.py
git commit -m "feat(types): add TypeChecker with assignment and function arg checking"
```

---

## Task 4: 增强 ExecutionContext 存储变量类型

**Files:**
- Modify: `src/jass_runner/interpreter/context.py`
- Test: `tests/interpreter/test_context.py`

**Step 1: 编写失败测试**

```python
def test_set_variable_with_type():
    """测试带类型信息的变量设置。"""
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    context.set_variable('x', 10, 'integer')

    assert context.get_variable('x') == 10
    assert context.get_variable_type('x') == 'integer'


def test_get_variable_type_from_parent():
    """测试从父上下文获取变量类型。"""
    from jass_runner.interpreter.context import ExecutionContext

    parent = ExecutionContext()
    parent.set_variable('x', 10, 'integer')

    child = ExecutionContext(parent)
    assert child.get_variable_type('x') == 'integer'


def test_declare_array_stores_type():
    """测试数组声明存储元素类型。"""
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    context.declare_array('arr', 'real')

    assert context.get_array_type('arr') == 'real'
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/interpreter/test_context.py::test_set_variable_with_type -v
```

Expected: FAIL with "TypeError: set_variable() takes 3 positional arguments but 4 were given"

**Step 3: 修改 ExecutionContext**

```python
# 在 __init__ 方法中添加类型存储
self.variable_types: Dict[str, str] = {}      # 变量类型存储
self.array_types: Dict[str, str] = {}         # 数组元素类型存储

# 修改 set_variable 方法
def set_variable(self, name: str, value: Any, var_type: str = None):
    """在此上下文中设置变量。

    参数：
        name: 变量名
        value: 变量值
        var_type: 变量类型（可选）
    """
    self.variables[name] = value
    if var_type is not None:
        self.variable_types[name] = var_type

# 添加 get_variable_type 方法
def get_variable_type(self, name: str) -> Optional[str]:
    """获取变量声明类型。

    参数：
        name: 变量名

    返回：
        变量类型，如果未找到返回None
    """
    if name in self.variable_types:
        return self.variable_types[name]
    if self.parent:
        return self.parent.get_variable_type(name)
    return None

# 修改 declare_array 方法
def declare_array(self, name: str, element_type: str):
    """声明数组，初始化8192个元素为类型默认值。

    参数：
        name: 数组名称
        element_type: 元素类型
    """
    default_value = self._default_values.get(element_type, None)
    self.arrays[name] = [default_value] * self._array_size
    self.array_types[name] = element_type

# 添加 get_array_type 方法
def get_array_type(self, name: str) -> Optional[str]:
    """获取数组元素类型。

    参数：
        name: 数组名

    返回：
        元素类型，如果未找到返回None
    """
    if name in self.array_types:
        return self.array_types[name]
    if self.parent:
        return self.parent.get_array_type(name)
    return None
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/interpreter/test_context.py -v
```

Expected: PASS（包括新测试和原有测试）

**Step 5: 提交**

```bash
git add src/jass_runner/interpreter/context.py tests/interpreter/test_context.py
git commit -m "feat(context): add variable and array type tracking"
```

---

## Task 5: 在 Interpreter 中集成类型检查

**Files:**
- Modify: `src/jass_runner/interpreter/interpreter.py`
- Test: `tests/interpreter/test_interpreter_type_check.py`

**Step 1: 编写失败测试**

```python
import pytest
from jass_runner.types.errors import JassTypeError


def test_local_declaration_with_type_check():
    """测试局部变量声明的类型检查。"""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.ast_nodes import LocalDecl

    interpreter = Interpreter()

    # local integer x = 10
    decl = LocalDecl(name='x', type='integer', value=10)
    interpreter.execute_local_declaration(decl)

    assert interpreter.current_context.get_variable('x') == 10
    assert interpreter.current_context.get_variable_type('x') == 'integer'


def test_set_statement_type_mismatch_raises():
    """测试set语句类型不匹配抛出异常。"""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.ast_nodes import LocalDecl, SetStmt

    interpreter = Interpreter()

    # local integer x = 10
    decl = LocalDecl(name='x', type='integer', value=10)
    interpreter.execute_local_declaration(decl)

    # set x = "hello" - 应该抛出类型错误
    set_stmt = SetStmt(var_name='x', value='hello')

    with pytest.raises(JassTypeError):
        interpreter.execute_set_statement(set_stmt)


def test_integer_to_real_implicit_conversion():
    """测试integer到real的隐式转换。"""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.ast_nodes import LocalDecl, SetStmt

    interpreter = Interpreter()

    # local real r = 10
    decl = LocalDecl(name='r', type='real', value=10)
    interpreter.execute_local_declaration(decl)

    assert interpreter.current_context.get_variable('r') == 10.0
    assert isinstance(interpreter.current_context.get_variable('r'), float)
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/interpreter/test_interpreter_type_check.py -v
```

Expected: FAIL with "AttributeError: 'Interpreter' object has no attribute 'type_checker'"

**Step 3: 修改 Interpreter 集成 TypeChecker**

```python
# 在 __init__ 中添加 TypeChecker
from ..types import TypeChecker

class Interpreter:
    def __init__(self, native_registry=None):
        self.type_checker = TypeChecker()  # 添加类型检查器
        # ... 其余初始化代码

# 修改 execute_local_declaration 方法
def execute_local_declaration(self, decl: LocalDecl):
    """执行局部变量声明，带类型检查。"""
    # 如果值是函数调用节点，先执行它并获取返回值
    if isinstance(decl.value, NativeCallNode):
        result = self.evaluator.evaluate(decl.value)
        value_type = self._infer_type(result)
    else:
        result = decl.value
        value_type = self._infer_type(result)

    # 类型检查
    checked_value = self.type_checker.check_assignment(
        decl.type, result, value_type
    )

    # 存储变量和类型
    self.current_context.set_variable(decl.name, checked_value, decl.type)

# 修改 execute_set_statement 方法
def execute_set_statement(self, stmt: SetStmt):
    """执行变量赋值语句，带类型检查。"""
    target_type = self.current_context.get_variable_type(stmt.var_name)

    # 如果值是函数调用节点，先执行它并获取返回值
    if isinstance(stmt.value, NativeCallNode):
        result = self.evaluator.evaluate(stmt.value)
        value_type = self._infer_type(result)
    elif isinstance(stmt.value, str):
        # 如果是字符串，可能是表达式，需要求值
        result = self.evaluator.evaluate(stmt.value)
        value_type = self._infer_type(result)
    else:
        result = stmt.value
        value_type = self._infer_type(result)

    # 类型检查
    checked_value = self.type_checker.check_assignment(
        target_type, result, value_type
    )

    self.current_context.set_variable_recursive(stmt.var_name, checked_value)

# 添加 _infer_type 辅助方法
def _infer_type(self, value) -> str:
    """从Python值推断JASS类型。

    参数：
        value: Python值

    返回：
        JASS类型名称
    """
    if value is None:
        return 'nothing'
    if isinstance(value, bool):
        return 'boolean'
    if isinstance(value, int):
        return 'integer'
    if isinstance(value, float):
        return 'real'
    if isinstance(value, str):
        return 'string'

    # handle子类型检测
    type_name = type(value).__name__.lower()
    if type_name in ['unit', 'timer', 'trigger', 'player', 'item']:
        return type_name

    return 'handle'
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/interpreter/test_interpreter_type_check.py -v
```

Expected: PASS

**Step 5: 运行所有测试确保无回归**

```bash
pytest tests/ -v
```

Expected: 所有测试通过

**Step 6: 提交**

```bash
git add src/jass_runner/interpreter/interpreter.py tests/interpreter/test_interpreter_type_check.py
git commit -m "feat(interpreter): integrate TypeChecker for assignment operations"
```

---

## Task 6: 添加函数参数类型检查

**Files:**
- Modify: `src/jass_runner/interpreter/interpreter.py`
- Test: `tests/interpreter/test_interpreter_type_check.py`

**Step 1: 编写失败测试**

```python
def test_function_call_with_type_check():
    """测试函数调用时的参数类型检查。"""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.ast_nodes import FunctionDecl, Parameter, ReturnStmt

    interpreter = Interpreter()

    # 定义函数: function add takes integer a, integer b returns integer
    func = FunctionDecl(
        name='add',
        parameters=[
            Parameter(name='a', type='integer', line=1, column=1),
            Parameter(name='b', type='integer', line=1, column=1)
        ],
        return_type='integer',
        line=1,
        column=1,
        body=[ReturnStmt(value='a + b')]
    )

    interpreter.functions['add'] = func

    # 调用 add(1, 2)
    result = interpreter._call_function_with_args(func, [1, 2])

    assert result == 3


def test_function_call_type_mismatch_raises():
    """测试函数调用参数类型不匹配抛出异常。"""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.ast_nodes import FunctionDecl, Parameter

    interpreter = Interpreter()

    # 定义函数: function foo takes integer x returns nothing
    func = FunctionDecl(
        name='foo',
        parameters=[Parameter(name='x', type='integer', line=1, column=1)],
        return_type='nothing',
        line=1,
        column=1,
        body=[]
    )

    # 调用 foo("hello") - 应该抛出类型错误
    with pytest.raises(JassTypeError):
        interpreter._call_function_with_args(func, ['hello'])
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/interpreter/test_interpreter_type_check.py::test_function_call_with_type_check -v
```

Expected: FAIL（需要修改 _call_function_with_args 添加类型检查）

**Step 3: 修改 _call_function_with_args 方法**

```python
def _call_function_with_args(self, func: FunctionDecl, args: list):
    """使用指定参数调用函数，带类型检查。

    参数：
        func: 函数定义节点
        args: 参数值列表

    返回：
        函数返回值
    """
    # 保存当前上下文以便后续恢复
    previous_context = self.current_context

    # 创建新上下文
    func_context = ExecutionContext(
        self.global_context,
        native_registry=self.global_context.native_registry,
        state_context=self.state_context,
        interpreter=self
    )

    # 设置参数值，带类型检查
    for param, arg_value in zip(func.parameters, args):
        arg_type = self._infer_type(arg_value)
        checked_arg = self.type_checker.check_function_arg(
            param.type, arg_value, arg_type
        )
        func_context.set_variable(param.name, checked_arg, param.type)

    self.current_context = func_context
    self.evaluator.context = func_context

    # 执行函数体
    return_value = None
    try:
        if func.body:
            for statement in func.body:
                self.execute_statement(statement)
    except ReturnSignal as signal:
        # 检查返回值类型
        if signal.value is not None:
            value_type = self._infer_type(signal.value)
            return_value = self.type_checker.check_return_value(
                func.return_type, signal.value, value_type
            )

    # 恢复上下文
    self.current_context = previous_context
    self.evaluator.context = previous_context

    return return_value
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/interpreter/test_interpreter_type_check.py -v
```

Expected: PASS

**Step 5: 运行所有测试确保无回归**

```bash
pytest tests/ -v
```

Expected: 所有测试通过

**Step 6: 提交**

```bash
git add src/jass_runner/interpreter/interpreter.py tests/interpreter/test_interpreter_type_check.py
git commit -m "feat(interpreter): add type checking for function arguments and return values"
```

---

## Task 7: 创建端到端集成测试

**Files:**
- Create: `tests/integration/test_type_checking.py`

**Step 1: 编写集成测试**

```python
"""类型检查系统集成测试。"""

import pytest
from jass_runner.types.errors import JassTypeError
from jass_runner.parser.parser import Parser
from jass_runner.interpreter.interpreter import Interpreter


class TestTypeCheckingIntegration:
    """测试类型检查与完整解释器链集成。"""

    def test_valid_integer_to_real_conversion_in_script(self):
        """测试脚本中integer到real的有效转换。"""
        code = '''
        function main takes nothing returns nothing
            local real r
            set r = 10
            return nothing
        endfunction
        '''

        parser = Parser(code)
        ast = parser.parse()

        interpreter = Interpreter()
        interpreter.execute(ast)

        # 验证r被正确转换为real
        assert interpreter.current_context.get_variable('r') == 10.0

    def test_type_error_in_script_raises_exception(self):
        """测试脚本中类型错误抛出异常。"""
        code = '''
        function main takes nothing returns nothing
            local integer x
            set x = "hello"
            return nothing
        endfunction
        '''

        parser = Parser(code)
        ast = parser.parse()

        interpreter = Interpreter()

        with pytest.raises(JassTypeError) as exc_info:
            interpreter.execute(ast)

        assert 'string' in str(exc_info.value)
        assert 'integer' in str(exc_info.value)

    def test_handle_subtype_assignment(self):
        """测试handle子类型赋值。"""
        # 这个测试需要native函数支持，暂时跳过
        # 实际测试需要CreateUnit返回unit类型
        pytest.skip("需要native函数返回类型支持")
```

**Step 2: 运行测试验证通过**

```bash
pytest tests/integration/test_type_checking.py -v
```

Expected: PASS（跳过的测试除外）

**Step 3: 提交**

```bash
git add tests/integration/test_type_checking.py
git commit -m "test(integration): add type checking end-to-end tests"
```

---

## Task 8: 更新项目文档

**Files:**
- Modify: `PROJECT_NOTES.md`
- Modify: `TODO.md`

**Step 1: 更新 PROJECT_NOTES.md**

在文档末尾添加类型检查系统实现记录：

```markdown
#### 42. 类型检查系统实现完成 (2026-03-02)
- **核心组件**:
  - `JassTypeError` 异常类 - 包含类型和位置信息的类型错误
  - `TypeHierarchy` 类 - 管理handle子类型层次关系
  - `TypeChecker` 类 - 运行时类型检查和转换
- **类型检查规则**:
  - 允许: integer → real (隐式转换)
  - 允许: handle子类型 → handle (协变)
  - 禁止: real → integer (需显式R2I)
  - 禁止: string → 数值类型
- **集成点**:
  - ExecutionContext增强: 存储变量和数组类型信息
  - Interpreter集成: 局部变量声明、set语句、函数调用检查
- **测试覆盖**:
  - 单元测试: types模块 (errors, hierarchy, checker)
  - 集成测试: interpreter类型检查、端到端脚本测试
- **测试统计**:
  - 所有测试通过
```

**Step 2: 更新 TODO.md**

将类型检查标记为已完成：

```markdown
### v0.5.0: 健壮性与完整性 (Robustness)

- [x] **P2** [Language] 实现静态或运行时类型检查。 ✅ 已完成（2026-03-02）
  - 运行时类型检查系统
  - 支持integer→real隐式转换
  - 支持handle子类型协变
  - 类型不匹配时抛出JassTypeError
```

**Step 3: 提交**

```bash
git add PROJECT_NOTES.md TODO.md
git commit -m "docs: update project notes and todo for type checker completion"
```

---

## 实施完成检查清单

- [ ] Task 1: JassTypeError 异常类
- [ ] Task 2: TypeHierarchy 类型层次管理
- [ ] Task 3: TypeChecker 核心类
- [ ] Task 4: ExecutionContext 增强
- [ ] Task 5: Interpreter 集成类型检查
- [ ] Task 6: 函数参数类型检查
- [ ] Task 7: 端到端集成测试
- [ ] Task 8: 更新项目文档

---

## 注意事项

1. **向后兼容**: 所有现有测试必须继续通过
2. **性能**: 类型检查在运行时进行，保持低开销
3. **错误信息**: 确保错误消息清晰，包含类型信息
4. **类型推断**: `_infer_type` 方法需要正确处理所有JASS类型
