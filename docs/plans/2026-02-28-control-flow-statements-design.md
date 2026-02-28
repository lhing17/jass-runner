# JASS解释器控制流语句设计文档

## 概述

本文档描述JASS Runner解释器控制流语句扩展的设计方案，包括if/elseif/else/endif条件语句、loop/endloop循环、exitwhen退出语句和return返回语句的实现。

## 设计目标

1. 实现完整的if/elseif/else/endif条件语句，支持嵌套
2. 实现loop/endloop循环，支持exitwhen任意布尔表达式退出
3. 实现return语句，支持在函数任意位置提前返回
4. 实现完整的运算符支持：算术(+,-,*,/)、比较(==,!=,<,>,<=,>=)、逻辑(and,or,not)
5. 遵循标准运算符优先级
6. 采用TDD方法，实现完整测试覆盖

## 架构设计

采用分层处理架构，Parser、Interpreter、Evaluator各司其职。

### 1. Parser层设计

#### 1.1 新增AST节点

```python
@dataclass
class IfStmt:
    """if/elseif/else语句节点"""
    condition: Any          # 条件表达式
    then_body: List[Any]    # then分支语句列表
    elseif_branches: List[Tuple[Any, List[Any]]]  # [(条件, 语句列表), ...]
    else_body: List[Any]    # else分支语句列表（可为空）

@dataclass
class LoopStmt:
    """loop循环节点"""
    body: List[Any]         # 循环体内语句列表

@dataclass
class ExitWhenStmt:
    """exitwhen退出循环节点"""
    condition: Any          # 退出条件表达式

@dataclass
class ReturnStmt:
    """return语句节点"""
    value: Optional[Any]    # 返回值表达式（可为None表示return nothing）
```

#### 1.2 新增解析方法

- `parse_if_statement()` - 解析if及其elseif/else分支
- `parse_loop_statement()` - 解析循环体
- `parse_exitwhen_statement()` - 解析退出条件
- `parse_return_statement()` - 解析return语句
- `parse_condition()` - 解析条件表达式
- 修改 `parse_statement()` - 添加对新语句类型的分发

### 2. Interpreter层设计

#### 2.1 控制流异常机制

```python
class ReturnSignal(Exception):
    """函数返回信号，携带返回值"""
    def __init__(self, value):
        self.value = value

class ExitLoopSignal(Exception):
    """退出当前循环的信号"""
    pass
```

#### 2.2 新增执行方法

- `execute_if_statement(stmt)` - 执行if语句，按顺序检查条件，执行第一个为真的分支
- `execute_loop_statement(stmt)` - 执行loop循环，捕获ExitLoopSignal退出
- `execute_exitwhen_statement(stmt)` - 执行exitwhen，条件为真时抛出ExitLoopSignal
- `execute_return_statement(stmt)` - 执行return，抛出ReturnSignal

#### 2.3 execute_function修改

捕获ReturnSignal并返回其携带的值。

### 3. Evaluator层设计

#### 3.1 运算符优先级

```
OR = 1          # or
AND = 2         # and
EQUALITY = 3    # ==, !=
RELATIONAL = 4  # <, >, <=, >=
ADDITIVE = 5    # +, -
MULTIPLICATIVE = 6  # *, /
UNARY = 7       # not, - (一元负号)
```

#### 3.2 表达式求值增强

- `evaluate(expression)` - 主入口，支持运算符
- `parse_expression(tokens, min_precedence)` - 使用递归下降解析表达式
- `evaluate_binary_op(left, op, right)` - 求值二元运算符
- `evaluate_unary_op(op, operand)` - 求值一元运算符
- `evaluate_condition(condition)` - 求值条件表达式，返回布尔结果

#### 3.3 类型转换规则

- `integer` → Python `int`
- `real` → Python `float`
- `string` → Python `str`
- `boolean` → Python `bool`

运算时自动类型转换，如 `integer + real` 结果为 `real`。

## 测试策略

采用TDD方法，按功能模块编写测试：

### Parser层测试

- if语句解析（简单if、带else、带elseif、嵌套）
- loop语句解析
- exitwhen解析
- return解析（带返回值、不带返回值）
- 运算符表达式解析

### Evaluator层测试

- 算术运算符（+、-、*、/）
- 比较运算符（==、!=、<、>、<=、>=）
- 逻辑运算符（and、or、not）及短路求值
- 运算符优先级验证

### Interpreter层测试

- if语句执行（各种分支场景）
- loop执行（指定次数、exitwhen退出、嵌套循环）
- return语句（末尾返回、提前返回、带返回值）
- 控制流集成（if内有loop、loop内有if）

### 集成测试

编写完整JASS脚本验证所有控制流特性协同工作。

## 实现顺序

1. Parser层AST节点和解析方法
2. Evaluator层运算符支持
3. Interpreter层控制流执行
4. 集成测试和示例脚本

## 验收标准

- [x] 支持嵌套if语句
- [x] 支持逻辑运算符（and、or、not）
- [x] exitwhen支持任意布尔表达式
- [x] return支持函数任意位置提前返回
- [x] 遵循标准运算符优先级
- [x] 完整测试覆盖（TDD方法）
