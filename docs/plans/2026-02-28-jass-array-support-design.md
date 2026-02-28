# JASS数组语法支持设计文档

日期: 2026-02-28
主题: 扩展解释器支持array语法
状态: 已批准

---

## 1. 需求概述

扩展JASS Runner解释器，支持JASS数组语法，包括：
- 全局和局部数组声明（`integer array counts`）
- 数组元素赋值（`set arr[i] = value`）
- 数组元素访问作为表达式（`set x = arr[i]`）
- 数组索引支持任意表达式（`arr[x * 20 + 1]`）

### 1.1 约束条件

- 数组大小固定为8192（索引范围0-8191）
- 不支持声明时初始化
- 不支持二维及多维数组
- 每行只能针对一个元素赋值
- 不进行运行时边界检查

---

## 2. 架构设计

### 2.1 存储方案：分离存储（方案A）

采用分离存储策略，数组和普通变量分开管理：

```python
class ExecutionContext:
    def __init__(self, parent=None, ...):
        self.variables: Dict[str, Any] = {}      # 普通变量
        self.arrays: Dict[str, List[Any]] = {}   # 数组变量
```

**选择理由**：
- JASS中数组和普通变量语法完全不同
- 分离存储逻辑清晰，易于调试
- 避免运行时类型推断开销

### 2.2 支持的数据类型

数组支持以下元素类型：

| 类型 | 默认值 |
|------|--------|
| `integer array` | `0` |
| `real array` | `0.0` |
| `string array` | `null` |
| `boolean array` | `false` |
| `handle array`（如`unit array`, `item array`） | `null` |

不支持：`nothing array`, `code array`

---

## 3. AST节点设计

### 3.1 新增节点

```python
@dataclass
class ArrayDecl:
    """数组声明节点（全局或局部）。"""
    name: str
    element_type: str          # integer, real, string, boolean, handle等
    is_global: bool            # True表示全局数组，False表示局部数组
    is_constant: bool = False  # 仅全局数组可标记为constant

@dataclass
class ArrayAccess:
    """数组访问节点（作为表达式值）。"""
    array_name: str
    index: Any                 # 索引表达式，支持任意复杂表达式

@dataclass
class SetArrayStmt:
    """数组元素赋值语句节点。"""
    array_name: str
    index: Any                 # 索引表达式
    value: Any                 # 右侧值表达式
```

### 3.2 设计说明

为什么不复用`SetStmt`？
- 添加`index`字段会使其变为optional
- 使用方需要频繁检查，容易出错
- 单独定义语义更清晰

---

## 4. 解析器设计

### 4.1 全局数组声明

格式：`[constant] <type> array <name>`

示例：
```jass
globals
    integer array counts
    constant unit array heroes
    string array names
endglobals
```

解析逻辑：
1. 检查`constant`关键字（可选）
2. 获取类型关键字
3. 检查`array`关键字
4. 获取数组名称
5. 检查：数组声明后不能有初始化表达式

### 4.2 局部数组声明

格式：`local <type> array <name>`

示例：
```jass
function Test takes nothing returns nothing
    local integer array temp
    local unit array units
endfunction
```

解析逻辑：
1. 跳过`local`关键字
2. 获取类型关键字
3. 检查`array`关键字
4. 获取数组名称
5. 检查名称冲突

### 4.3 数组访问和赋值

数组访问作为表达式：
```jass
set x = counts[0]           // 整数字面量索引
set y = counts[i]           // 变量索引
set z = counts[i + 1]       // 表达式索引
set w = arr[x * 20 + 1]     // 复杂表达式索引
```

数组赋值语句：
```jass
set counts[0] = 10
set units[heroIndex] = hero
set temp[x * 20 + 1] = 1
```

解析逻辑：
- 识别`name[`模式
- 解析方括号内的表达式直到`]`
- 根据上下文生成`ArrayAccess`或`SetArrayStmt`

---

## 5. 解释器设计

### 5.1 执行上下文扩展

```python
class ExecutionContext:
    def declare_array(self, name: str, element_type: str,
                      initial_values: List[Any]):
        """声明数组，初始化8192个元素。"""
        self.arrays[name] = initial_values

    def get_array_element(self, name: str, index: int) -> Any:
        """获取数组元素（不做边界检查）。"""
        return self.arrays[name][index]

    def set_array_element(self, name: str, index: int, value: Any):
        """设置数组元素（不做边界检查）。"""
        self.arrays[name][index] = value
```

### 5.2 解释器执行逻辑

```python
class Interpreter:
    def execute_statement(self, statement: Any):
        if isinstance(statement, ArrayDecl):
            self.execute_array_declaration(statement)
        elif isinstance(statement, SetArrayStmt):
            self.execute_set_array_statement(statement)
        # ... 其他语句类型

    def execute_array_declaration(self, stmt: ArrayDecl):
        """执行数组声明。"""
        default_value = self._get_default_value(stmt.element_type)
        initial_values = [default_value] * 8192
        self.current_context.declare_array(
            stmt.name, stmt.element_type, initial_values
        )

    def execute_set_array_statement(self, stmt: SetArrayStmt):
        """执行数组元素赋值。"""
        index = self.evaluator.evaluate(stmt.index)
        value = self.evaluator.evaluate(stmt.value)
        self.current_context.set_array_element(
            stmt.array_name, int(index), value
        )
```

### 5.3 求值器扩展

```python
class Evaluator:
    def evaluate(self, expression: Any) -> Any:
        if isinstance(expression, ArrayAccess):
            return self._evaluate_array_access(expression)
        # ... 其他表达式类型

    def _evaluate_array_access(self, access: ArrayAccess) -> Any:
        """求值数组访问表达式。"""
        index = self.evaluate(access.index)  # 递归求值索引表达式
        return self.context.get_array_element(
            access.array_name, int(index)
        )
```

---

## 6. 错误处理

### 6.1 解析阶段错误

| 错误场景 | 错误信息 |
|---------|---------|
| `integer array arr = 10` | 数组声明不支持初始化 |
| `set arr[i, j] = 10` | 不支持多维数组语法 |
| `integer array`（缺少名称） | 缺少数组名称 |
| 数组名与普通变量名冲突 | 变量名已存在 |

### 6.2 运行时错误（可选）

| 错误场景 | 处理方式 |
|---------|---------|
| 访问未声明的数组 | 抛出NameError |
| 索引不是整数 | 抛出TypeError |
| 索引超出范围 | 不检查（由Python列表行为决定） |

---

## 7. 测试策略

### 7.1 单元测试

**解析器测试**：
- 全局数组声明（带/不带constant）
- 局部数组声明
- 数组访问表达式（各种索引形式）
- 数组赋值语句
- 错误语法检测

**解释器测试**：
- 数组声明执行
- 元素赋值与读取
- 默认值验证
- 索引表达式求值

### 7.2 集成测试

示例测试脚本：
```jass
globals
    integer array scores
    unit array heroes
endglobals

function Test takes nothing returns nothing
    local integer array temp
    set scores[0] = 100
    set temp[1] = scores[0] + 50
    set temp[x * 20 + 1] = 1
endfunction
```

---

## 8. 实现文件清单

| 文件 | 修改内容 |
|------|---------|
| `src/jass_runner/parser/ast_nodes.py` | 添加`ArrayDecl`, `ArrayAccess`, `SetArrayStmt` |
| `src/jass_runner/parser/global_parser.py` | 扩展`parse_global_declaration`支持数组 |
| `src/jass_runner/parser/assignment_parser.py` | 扩展局部变量和赋值解析 |
| `src/jass_runner/parser/expression_parser.py` | 扩展表达式解析支持数组访问 |
| `src/jass_runner/interpreter/context.py` | 添加数组存储和管理方法 |
| `src/jass_runner/interpreter/interpreter.py` | 添加数组声明和赋值执行 |
| `src/jass_runner/interpreter/evaluator.py` | 添加数组访问求值 |

---

## 9. 附录：JASS数组语法示例

```jass
// 全局数组声明
globals
    integer array playerScores
    constant unit array heroes
    string array playerNames
    boolean array isAlive
endglobals

// 局部数组声明
function InitArrays takes nothing returns nothing
    local integer array temp
    local unit array units

    // 数组赋值
    set playerScores[0] = 100
    set temp[5] = playerScores[0] + 50

    // 复杂索引表达式
    local integer x
    set x = 2
    set temp[x * 20 + 1] = 999

    // 数组访问作为表达式
    set playerScores[1] = temp[0]
endfunction
```

---

## 10. 设计决策记录

| 决策 | 选择 | 理由 |
|------|------|------|
| 存储方案 | 分离存储 | 逻辑清晰，符合JASS语义 |
| SetStmt处理 | 单独定义SetArrayStmt | 避免optional字段，语义清晰 |
| 边界检查 | 不实现 | 按需求简化实现 |
| 数组大小 | 8192 | 与魔兽争霸III JASS一致 |
| string默认值 | null | JASS中字符串默认可为null |
