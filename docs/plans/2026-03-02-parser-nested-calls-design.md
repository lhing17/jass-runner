# 解析器嵌套函数调用修复设计文档

> **设计目标**: 修复解析器无法正确处理嵌套函数调用（如 `CreateUnit(Player(0), ...)`）的问题

---

## 1. 问题分析

### 1.1 根本原因

`parse_call_statement` 已支持嵌套函数调用，但 `parse_set_statement` 和 `parse_local_declaration` 中的函数调用解析没有实现相同的逻辑。

### 1.2 具体表现

当解析 `CreateUnit(Player(0), 1213484355, 100.0, 200.0, 0.0)` 时：
- 参数 1 `Player(0)` 被错误解析为字符串 `'Player'`
- 遇到 `(0)` 后解析器混乱，导致后续参数丢失
- 最终只解析到 `['Player', '0']` 两个参数

### 1.3 影响范围

- `set` 语句中的函数调用
- `local` 声明中的函数调用初始化
- `call` 语句工作正常（已有嵌套调用支持）

---

## 2. 架构设计

### 2.1 核心方案：提取公共方法

创建 `_parse_call_args` 方法统一处理函数调用参数解析。

### 2.2 修改文件

- `src/jass_runner/parser/assignment_parser.py`

### 2.3 修改内容

#### 2.3.1 新增方法 `_parse_call_args`

```python
def _parse_call_args(self: 'BaseParser') -> List[Any]:
    """解析函数调用参数列表，支持嵌套调用。

    前置条件：当前 token 是 '('
    后置条件：当前 token 是 ')'

    返回：
        参数列表，支持嵌套 NativeCallNode
    """
```

**功能：**
- 解析函数调用的所有参数
- 支持嵌套函数调用（如 `Player(0)`）
- 支持字面量（整数、实数、字符串、fourcc）
- 支持标识符（变量名）
- 支持布尔值

#### 2.3.2 修改 `parse_call_statement`

- 使用 `_parse_call_args` 替代内联参数解析
- 删除重复的嵌套调用处理逻辑（约 40 行）

#### 2.3.3 修改 `parse_set_statement`

- 在函数调用参数解析处使用 `_parse_call_args`
- 添加对嵌套调用的支持

#### 2.3.4 修改 `parse_local_declaration`

- 在函数调用参数解析处使用 `_parse_call_args`
- 确保局部变量声明也支持嵌套调用

---

## 3. 数据流示例

### 输入
```jass
set u = CreateUnit(Player(0), 1213484355, 100.0, 200.0, 0.0)
```

### 解析流程

```
parse_set_statement
    │
    ▼
识别 CreateUnit(...)
    │
    ▼
调用 _parse_call_args 解析参数列表:
    │
    ├── 参数 1: Player(0)
    │   ├── IDENTIFIER 'Player'
    │   ├── 遇到 '(' → 递归调用 _parse_call_args
    │   │   └── 解析参数 '0' (INTEGER)
    │   └── 返回 NativeCallNode('Player', ['0'])
    │
    ├── 参数 2: 1213484355 (INTEGER)
    │   └── 返回 '1213484355'
    │
    ├── 参数 3: 100.0 (REAL)
    │   └── 返回 '100.0'
    │
    ├── 参数 4: 200.0 (REAL)
    │   └── 返回 '200.0'
    │
    └── 参数 5: 0.0 (REAL)
        └── 返回 '0.0'
    │
    ▼
返回 NativeCallNode('CreateUnit', [
    NativeCallNode('Player', ['0']),
    '1213484355',
    '100.0',
    '200.0',
    '0.0'
])
```

---

## 4. 错误处理

- 如果参数解析失败，记录错误并继续解析剩余参数
- 保持向后兼容：现有功能不受影响
- 不支持的参数类型记录警告但不中断解析

---

## 5. 测试策略

### 5.1 单元测试

```python
def test_parse_call_args_with_nested_call():
    """测试 _parse_call_args 支持嵌套调用。"""
    # 测试单层嵌套: Player(0)
    # 测试多层嵌套: FuncA(FuncB(1), FuncC(2))
    # 测试混合参数: Func(1, Player(0), "string")

def test_parse_set_statement_with_nested_call():
    """测试 set 语句支持嵌套函数调用。"""
    # set u = CreateUnit(Player(0), 1213484355, 100.0, 200.0, 0.0)

def test_parse_local_declaration_with_nested_call():
    """测试 local 声明支持嵌套函数调用。"""
    # local unit u = CreateUnit(Player(0), ...)
```

### 5.2 集成测试

修复 `tests/integration/test_unit_natives.py`：
- `test_unit_lifecycle_workflow`: 使用完整 JASS 代码测试单位生命周期
- `test_create_unit_at_loc_workflow`: 测试使用 Location 创建单位

---

## 6. 风险与注意事项

1. **向后兼容性**: 确保现有解析功能不受影响
2. **性能影响**: 递归调用可能增加栈深度，但一般调用层级较浅
3. **边界情况**: 需要测试空参数列表、单个参数、多个嵌套等情况

---

## 7. 成功标准

- [ ] `CreateUnit(Player(0), 1213484355, 100.0, 200.0, 0.0)` 正确解析所有 5 个参数
- [ ] 嵌套调用节点 `Player(0)` 作为独立参数传递
- [ ] 所有现有测试继续通过
- [ ] 集成测试可以运行完整的 JASS 代码

---

*设计日期: 2026-03-02*
*设计状态: 已确认*
