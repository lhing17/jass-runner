# Globals 模块扩展：Constant 常量支持设计文档

> 创建日期: 2026-02-28
> 状态: 已批准，待实施
> 相关计划: 2026-02-28-globals-global-variables-design.md

## 概述

本文档描述 JASS Runner 中 `constant` 常量支持的扩展设计。在现有 globals 全局变量基础上，增加对 `constant` 常量的解析和执行支持。

## 背景

当前 globals 实现已支持普通全局变量：

```jass
globals
    integer global_counter = 0
    real global_x
endglobals
```

需要扩展支持 constant 常量：

```jass
globals
    constant integer UNIT_ATTR_AGI = 1
    constant real PI = 3.14159
endglobals
```

## 设计目标

1. **解析支持**：能够解析 `constant <type> <name> = <value>` 语法
2. **编译期检查**：constant 必须在声明时初始化
3. **只读保护**：解析阶段阻止任何对 constant 的修改尝试
4. **兼容现有**：不影响现有 globals 功能

## 非目标（未来扩展）

- 局部常量（`local constant integer MAX = 10`）
- 常量表达式计算（如 `constant integer SIZE = WIDTH * HEIGHT`）
- 数组常量

## 设计详情

### 1. 语法设计

```jass
globals
    // 普通全局变量（已有）
    integer global_counter = 0
    real global_x

    // constant 常量（新增）
    constant integer UNIT_ATTR_AGI = 1
    constant real PI = 3.14159
    constant string APP_NAME = "MyGame"
    constant boolean DEBUG_MODE = true
endglobals
```

**语法规则：**
- `constant` 关键字放在类型之前
- constant **必须**有初始值（编译期确定）
- constant 只能在 `globals` 块内声明

### 2. AST 扩展

扩展 `GlobalDecl` 节点，添加 `is_constant` 标记：

```python
@dataclass
class GlobalDecl:
    """全局变量声明节点。"""
    name: str           # 变量名
    type: str           # 类型
    value: Any          # 初始值，constant必须有值
    is_constant: bool = False  # 是否为常量
```

### 3. 解析器实现

#### 3.1 修改 parse_global_declaration()

```python
def parse_global_declaration(self) -> Optional[GlobalDecl]:
    """解析单个全局变量声明。

    格式: [constant] <type> <name> [= <initial_value>]
    """
    try:
        is_constant = False

        # 检查是否为 constant
        if self.current_token and self.current_token.type == 'KEYWORD' and \
           self.current_token.value == 'constant':
            is_constant = True
            self.next_token()

        # 获取变量类型（原有逻辑）
        # ... 类型解析 ...

        # 获取变量名（原有逻辑）
        # ... 名称解析 ...

        # 检查可选的初始值
        value = None
        if self.current_token and self.current_token.value == '=':
            # ... 解析初始值 ...
        elif is_constant:
            # constant 必须有初始值
            self.errors.append(ParseError(
                message=f"常量 '{var_name}' 必须指定初始值",
                line=self.current_token.line if self.current_token else 0,
                column=self.current_token.column if self.current_token else 0
            ))
            return None

        return GlobalDecl(name=var_name, type=var_type, value=value,
                         is_constant=is_constant)
```

#### 3.2 新增常量名集合

```python
def parse(self) -> AST:
    # ... 原有代码 ...

    # 存储常量名用于冲突检查
    self.constant_names = {g.name for g in globals_list if g.is_constant}

    # ... 原有代码 ...
```

#### 3.3 修改 parse_set_statement() 检查常量修改

```python
def parse_set_statement(self) -> Optional[SetStmt]:
    # ... 跳过 'set' 关键字，获取变量名 ...

    var_name = self.current_token.value

    # 检查是否尝试修改常量
    if hasattr(self, 'constant_names') and var_name in self.constant_names:
        self.errors.append(ParseError(
            message=f"不能修改常量 '{var_name}'",
            line=self.current_token.line,
            column=self.current_token.column
        ))
        # 继续解析以收集更多错误，但返回None
        return None

    # ... 原有代码 ...
```

### 4. 解释器实现

解释器端的改动较小，因为 constant 的只读特性在解析阶段已保证：

```python
def execute(self, ast: AST):
    """执行AST。"""
    # 注册所有函数
    for func in ast.functions:
        self.functions[func.name] = func

    # 初始化全局变量（包括 constant）
    for global_var in ast.globals:
        value = self._evaluate_initial_value(global_var.value)
        self.global_context.set_variable(global_var.name, value)
        # constant 和普通变量在运行时存储方式相同
        # 因为解析阶段已阻止了任何修改尝试

    # 查找并执行main函数
    if 'main' in self.functions:
        self.execute_function(self.functions['main'])
```

### 5. 错误处理

#### 5.1 错误类型

复用现有的 `ParseError`，无需创建新错误类型。

#### 5.2 错误信息

| 场景 | 错误信息 | 示例 |
|------|----------|------|
| constant 缺少初始值 | `常量 '{name}' 必须指定初始值` | `常量 'MAX_SIZE' 必须指定初始值` |
| 尝试修改 constant | `不能修改常量 '{name}'` | `不能修改常量 'MAX_SIZE'` |

#### 5.3 错误位置

所有错误都包含准确的行号和列号，指向：
- 常量声明中的类型位置（缺少初始值时）
- `set` 语句中的变量名位置（尝试修改时）

### 6. 测试策略

#### 6.1 解析器测试

```python
def test_parse_constant_declaration():
    """测试解析 constant 常量声明。"""
    code = '''
    globals
        constant integer MAX_SIZE = 100
    endglobals
    '''
    parser = Parser(code)
    ast = parser.parse()

    assert len(ast.globals) == 1
    assert ast.globals[0].name == "MAX_SIZE"
    assert ast.globals[0].is_constant is True
    assert ast.globals[0].value == 100

def test_parse_constant_without_initial_value_errors():
    """测试 constant 没有初始值时报错。"""
    code = '''
    globals
        constant integer MAX_SIZE
    endglobals
    '''
    parser = Parser(code)
    ast = parser.parse()

    assert len(parser.errors) > 0
    assert "必须指定初始值" in str(parser.errors[0])

def test_parse_set_constant_errors():
    """测试尝试修改 constant 时报错。"""
    code = '''
    globals
        constant integer MAX_SIZE = 100
    endglobals

    function test takes nothing returns nothing
        set MAX_SIZE = 200
    endfunction
    '''
    parser = Parser(code)
    ast = parser.parse()

    assert len(parser.errors) > 0
    assert "不能修改常量" in str(parser.errors[0])
```

#### 6.2 解释器测试

```python
def test_execute_constant_access():
    """测试在函数内访问 constant 常量。"""
    code = '''
    globals
        constant string APP_NAME = "TestApp"
    endglobals

    function main takes nothing returns nothing
        local string name = APP_NAME
    endfunction
    '''
    # 验证能正常执行
```

#### 6.3 集成测试

```python
def test_mixed_globals_and_constants():
    """测试普通全局变量和 constant 混合使用。"""
    code = '''
    globals
        constant integer MAX_HP = 100
        integer current_hp = 50
    endglobals

    function heal takes nothing returns nothing
        set current_hp = MAX_HP
    endfunction
    '''
    # 验证能正确解析和执行
```

## 实施计划

详见 `docs/plans/YYYY-MM-DD-constant-globals-implementation.md`（将由 writing-plans skill 生成）

## 风险与缓解

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|----------|
| 与现有 globals 解析冲突 | 低 | 高 | 全面的测试覆盖，特别是混合场景 |
| constant 检测不完整 | 低 | 中 | 测试所有修改路径（set语句） |
| 错误信息不明确 | 低 | 低 | 测试验证错误信息内容 |

## 附录

### 相关文档

- 2026-02-28-globals-global-variables-design.md - 基础 globals 设计
- TODO.md - 功能路线图

### 变更历史

- 2026-02-28: 初始设计文档创建
