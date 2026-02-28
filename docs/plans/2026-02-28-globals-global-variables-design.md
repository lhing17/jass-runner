# Globals 全局变量块设计文档

> 创建日期: 2026-02-28
> 状态: 已批准，待实施
> 相关计划: TODO.md v0.2.0

## 概述

本文档描述 JASS Runner 中 `globals` 全局变量块的解析与访问实现设计。

## 背景

当前 JASS Runner 仅支持函数内 `local` 局部变量声明。标准 JASS 支持在文件级别声明全局变量，通过 `globals` / `endglobals` 块包裹：

```jass
globals
    integer global_counter = 0
    real global_x
endglobals
```

全局变量可在所有函数内访问和修改，是 JASS 脚本状态共享的主要机制。

## 设计目标

1. **解析支持**：能够解析 `globals` / `endglobals` 块内的变量声明
2. **作用域集成**：全局变量可在所有函数内访问
3. **冲突检查**：局部变量不允许与全局变量同名（解析时报错）
4. **初始化支持**：支持可选初始值（如 `integer x = 5`）

## 非目标（未来扩展）

以下特性不在本次实现范围内，已记录到 TODO.md：

- **常量全局变量**（`constant integer MAX_SIZE = 100`）- P1
- **数组全局变量**（`integer array counts`）- P1

## 设计详情

### 1. AST 扩展

#### 新增 GlobalDecl 节点

```python
@dataclass
class GlobalDecl:
    """全局变量声明节点。"""
    name: str           # 变量名
    type: str           # 类型（integer, real, string, boolean等）
    value: Any          # 可选初始值，None表示未初始化
```

#### 扩展 AST 根节点

```python
@dataclass
class AST:
    """抽象语法树根节点。"""
    globals: List[GlobalDecl]       # 全局变量列表（新增）
    functions: List[FunctionDecl]   # 函数列表
```

### 2. 解析器实现

#### 新增 parse_globals_block 方法

```python
def parse_globals_block(self) -> Optional[List[GlobalDecl]]:
    """解析可选的globals块。

    返回：
        如果存在globals块返回GlobalDecl列表，否则返回空列表
    """
    # 检查是否存在 globals 关键字
    # 解析变量声明列表直到 endglobals
    # 每个声明格式: <type> <name> [= <value>]
```

#### 修改 parse 方法

在解析函数之前，首先调用 `parse_globals_block()` 解析可选的全局变量块。

#### 变量名冲突检查

在解析函数局部变量时，检查变量名是否已在全局变量中存在：

```python
# 伪代码
global_names = {g.name for g in ast.globals}
if local_name in global_names:
    raise ParseError(f"局部变量 '{local_name}' 与全局变量同名")
```

### 3. 支持的语法

```jass
globals
    integer global_counter = 0
    real global_x
    string app_name = "test"
    boolean is_enabled = true
endglobals
```

**语法规则：**
- `globals` 块必须位于所有函数之前
- 每个变量声明格式：`<type> <name> [ = <initial_value> ]`
- 支持的基础类型：`integer`, `real`, `string`, `boolean`
- 初始值可选，未指定时为 None

### 4. 解释器实现

#### 修改 Interpreter.execute 方法

在创建 global_context 后，首先初始化所有全局变量：

```python
def execute(self, ast: AST):
    """执行AST。"""
    # 注册所有函数
    for func in ast.functions:
        self.functions[func.name] = func

    # 初始化全局变量（新增）
    for global_var in ast.globals:
        value = self._evaluate_initial_value(global_var.value)
        self.global_context.set_variable(global_var.name, value)

    # 查找并执行main函数
    if 'main' in self.functions:
        self.execute_function(self.functions['main'])
```

#### 变量查找逻辑

保持现有逻辑不变：
1. 首先在局部上下文中查找
2. 如果不存在，在父上下文（global_context）中查找
3. 如果不存在，抛出 NameError

### 5. 作用域规则

```
全局作用域 (global_context)
    ↓ 可被所有函数访问
函数局部作用域 (func_context)
    ↓ 变量查找优先
嵌套作用域 (如有)
```

**规则：**
- 全局变量可在所有函数内读取和修改
- 局部变量优先级高于全局变量
- 局部变量不允许与全局变量同名（解析时报错）

### 6. 测试策略

#### 解析器测试

1. **test_parse_globals_block**：正确解析包含初始值的全局变量
2. **test_parse_globals_without_initial_value**：解析无初始值的全局变量
3. **test_parse_globals_empty**：解析空的 globals 块
4. **test_parse_no_globals**：没有 globals 块的代码
5. **test_globals_variable_name_conflict**：局部变量与全局变量同名时报错

#### 解释器测试

1. **test_execute_globals_initialization**：全局变量正确初始化
2. **test_execute_globals_access_in_function**：函数内访问全局变量
3. **test_execute_globals_modify_in_function**：函数内修改全局变量
4. **test_execute_globals_persistence**：全局变量在多次调用间保持状态

#### 集成测试

1. **test_globals_with_control_flow**：全局变量在控制流语句中使用
2. **test_globals_with_function_calls**：全局变量在函数间共享状态

## 实施计划

详见 `docs/plans/2026-02-28-globals-implementation-plan.md`（将由 writing-plans skill 生成）

## 风险与缓解

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|----------|
| 变量名冲突检查不完善 | 低 | 高 | 全面的测试覆盖 |
| 与现有 local 变量逻辑冲突 | 中 | 中 | 保持现有查找逻辑，仅添加解析时检查 |
| 初始化值求值问题 | 低 | 中 | 复用现有的 evaluate 逻辑 |

## 附录

### 相关文档

- TODO.md - 功能路线图
- docs/plans/2026-02-28-phase3-interpreter-control-flow.md - 控制流实现参考

### 变更历史

- 2026-02-28: 初始设计文档创建
