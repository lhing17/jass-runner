# JASS Runner 类型检查系统设计文档

## 1. 概述

本文档描述 JASS Runner 运行时类型检查系统的设计，用于在脚本执行期间验证类型兼容性。

## 2. 设计目标

- **宽松模式**：允许安全的隐式类型转换（`integer` → `real`）
- **严格错误处理**：类型不匹配时抛出异常立即中断执行
- **协变支持**：`handle` 子类型可赋值给父类型
- **清晰错误信息**：提供包含源代码位置的有用错误消息

## 3. 架构设计

### 3.1 组件结构

```
┌─────────────────────────────────────────────────────┐
│                    Interpreter                       │
│  ┌─────────────┐    ┌──────────────────────────┐   │
│  │  执行语句   │───▶│      TypeChecker         │   │
│  │  (赋值等)   │◀───│   (类型验证与转换)        │   │
│  └─────────────┘    └──────────────────────────┘   │
│                              │                      │
│                              ▼                      │
│                     ┌──────────────────┐           │
│                     │  TypeHierarchy   │           │
│                     │  (类型关系定义)   │           │
│                     └──────────────────┘           │
└─────────────────────────────────────────────────────┘
```

### 3.2 核心组件

#### TypeChecker 类

负责所有运行时类型检查和转换。

```python
class TypeChecker:
    """JASS运行时类型检查器。"""

    # 允许的隐式转换规则
    _ALLOWED_IMPLICIT_CONVERSIONS = {
        'real': ['integer'],           # integer可隐式转为real
        'handle': ['unit', 'timer', 'trigger', 'player', 'item'],
    }

    def is_compatible(self, source_type: str, target_type: str) -> bool:
        """判断源类型是否可以隐式赋值给目标类型。"""

    def check_assignment(self, target_type: str, value: Any,
                        value_type: str, line: int = None,
                        column: int = None) -> Any:
        """检查赋值操作是否合法，返回转换后的值。"""

    def check_function_arg(self, param_type: str, arg_value: Any,
                          arg_type: str) -> Any:
        """检查函数参数类型是否匹配。"""

    def check_return_value(self, return_type: str, value: Any,
                          value_type: str) -> Any:
        """检查返回值类型是否匹配。"""
```

#### TypeHierarchy 类

管理JASS类型层次结构。

```python
class TypeHierarchy:
    """JASS类型层次结构管理。"""

    HANDLE_SUBTYPES = {
        'unit': 'handle',
        'item': 'handle',
        'timer': 'handle',
        'trigger': 'handle',
        'player': 'handle',
    }

    @classmethod
    def is_subtype(cls, subtype: str, basetype: str) -> bool:
        """判断subtype是否是basetype的子类型。"""

    @classmethod
    def get_base_type(cls, type_name: str) -> str:
        """获取类型的基类型。"""
```

#### JassTypeError 异常类

```python
class JassTypeError(TypeError):
    """JASS类型错误异常。"""

    def __init__(self, message: str, source_type: str,
                 target_type: str, line: int = None, column: int = None):
        super().__init__(message)
        self.source_type = source_type
        self.target_type = target_type
        self.line = line
        self.column = column
```

## 4. 类型检查规则

### 4.1 允许的隐式转换

| 目标类型 | 允许的来源类型 | 转换行为 |
|---------|--------------|---------|
| `real` | `integer` | 转为浮点数 |
| `handle` | `unit`, `timer`, `trigger`, `player`, `item` 等 | 协变允许 |

### 4.2 严格匹配的类型

以下类型必须完全匹配，不允许隐式转换：
- `integer` ← 只允许 `integer`
- `boolean` ← 只允许 `boolean`
- `string` ← 只允许 `string`
- `code` ← 只允许 `code`

### 4.3 不允许的隐式转换

- `real` → `integer`（需显式调用 `R2I()`）
- `integer` → `boolean`
- `boolean` → `integer`
- `string` → 任何数值类型

## 5. 集成设计

### 5.1 ExecutionContext 增强

```python
class ExecutionContext:
    def __init__(self, ...):
        self.variables: Dict[str, Any] = {}
        self.variable_types: Dict[str, str] = {}      # 新增：变量类型存储
        self.arrays: Dict[str, List[Any]] = {}
        self.array_types: Dict[str, str] = {}         # 新增：数组元素类型

    def set_variable(self, name: str, value: Any, var_type: str = None):
        """设置变量，可选记录类型。"""
        self.variables[name] = value
        if var_type:
            self.variable_types[name] = var_type

    def get_variable_type(self, name: str) -> Optional[str]:
        """获取变量声明类型。"""
        if name in self.variable_types:
            return self.variable_types[name]
        if self.parent:
            return self.parent.get_variable_type(name)
        return None
```

### 5.2 Interpreter 集成点

```python
class Interpreter:
    def __init__(self, native_registry=None):
        self.type_checker = TypeChecker()  # 新增
        # ...

    def execute_local_declaration(self, decl: LocalDecl):
        """执行局部变量声明，带类型检查。"""
        value = self._evaluate_value(decl.value)
        value_type = self._infer_type(value)

        # 类型检查
        checked_value = self.type_checker.check_assignment(
            decl.type, value, value_type
        )

        # 存储变量和类型
        self.current_context.set_variable(
            decl.name, checked_value, decl.type
        )

    def execute_set_statement(self, stmt: SetStmt):
        """执行set语句，带类型检查。"""
        target_type = self.current_context.get_variable_type(stmt.var_name)
        value = self._evaluate_value(stmt.value)
        value_type = self._infer_type(value)

        # 类型检查
        checked_value = self.type_checker.check_assignment(
            target_type, value, value_type
        )

        self.current_context.set_variable_recursive(
            stmt.var_name, checked_value
        )
```

## 6. 错误处理

### 6.1 错误信息格式

```
JassTypeError: 类型错误：不能将'string'类型的值赋值给'integer'类型的变量
  在: main函数, 第5行, 第10列
  源代码: set x = "hello"
                ^^^^^^^
```

### 6.2 错误处理流程

1. TypeChecker 检测到类型不匹配
2. 抛出 JassTypeError，包含类型信息和位置
3. Interpreter 捕获异常，添加上下文信息
4. 输出格式化错误信息并终止执行

## 7. 测试策略

### 7.1 单元测试

```python
class TestTypeChecker:
    """测试TypeChecker核心功能。"""

    def test_integer_to_real_conversion(self):
        """integer可隐式转为real。"""

    def test_string_to_integer_raises_error(self):
        """string不能转为integer。"""

    def test_unit_to_handle_compatibility(self):
        """unit子类型可赋值给handle。"""

    def test_handle_to_unit_incompatibility(self):
        """handle不能赋值给unit子类型。"""
```

### 7.2 集成测试

```python
class TestTypeCheckingIntegration:
    """测试类型检查与解释器集成。"""

    def test_assignment_with_type_check(self):
        """赋值操作触发类型检查。"""

    def test_function_call_type_check(self):
        """函数调用时参数类型检查。"""

    def test_type_error_reporting(self):
        """类型错误正确报告位置信息。"""
```

## 8. 实施注意事项

1. **向后兼容**：类型检查是新增功能，不应破坏现有测试
2. **性能考虑**：类型检查在运行时进行，需保持低开销
3. **错误恢复**：一旦发生类型错误，立即终止执行
4. **类型推断**：需要实现 `_infer_type()` 方法从Python值推断JASS类型

## 9. 后续扩展

- 静态类型检查阶段（解析时检查）
- 可配置的类型严格程度
- 更丰富的类型错误提示（建议修复方案）
