# 解析器嵌套函数调用修复实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 修复解析器无法正确处理嵌套函数调用的问题，通过提取公共方法 `_parse_call_args` 统一处理参数解析

**Architecture:** 创建 `_parse_call_args` 方法支持嵌套调用，重构 `parse_call_statement`、`parse_set_statement` 和 `parse_local_declaration` 使用新方法

**Tech Stack:** Python 3.8+, pytest, 现有 Parser 框架

---

## 前置信息

### 相关设计文档
- `docs/plans/2026-03-02-parser-nested-calls-design.md` - 详细设计文档

### 关键现有文件
- `src/jass_runner/parser/assignment_parser.py` - 需要修改的主文件
- `src/jass_runner/parser/ast_nodes.py` - NativeCallNode 定义
- `tests/parser/test_parser.py` - 现有解析器测试
- `tests/integration/test_unit_natives.py` - 需要修复的集成测试

### 问题复现
```python
# 当前解析结果（错误）
CreateUnit(Player(0), 1213484355, 100.0, 200.0, 0.0)
# 解析为: args=['Player', '0']  # 只有2个参数，且嵌套调用丢失

# 期望解析结果
# 解析为: args=[NativeCallNode('Player', ['0']), '1213484355', '100.0', '200.0', '0.0']
```

---

## Task 1: 创建 `_parse_call_args` 方法

**Files:**
- Modify: `src/jass_runner/parser/assignment_parser.py`
- Test: `tests/parser/test_assignment_parser.py`（新建）

**Step 1: 编写失败测试**

创建 `tests/parser/test_assignment_parser.py`：

```python
"""赋值解析器测试。"""

import pytest
from jass_runner.parser.parser import Parser


class TestParseCallArgs:
    """测试 _parse_call_args 方法。"""

    def test_parse_call_args_with_nested_call(self):
        """测试解析嵌套函数调用参数。"""
        code = '''
        function main takes nothing returns nothing
            set u = CreateUnit(Player(0), 1213484355, 100.0, 200.0, 0.0)
        endfunction
        '''
        parser = Parser(code)
        ast = parser.parse()

        # 获取 set 语句
        func = ast.functions[0]
        set_stmt = func.body[0]

        # 验证参数数量
        assert len(set_stmt.value.args) == 5

        # 验证第一个参数是嵌套调用
        from jass_runner.parser.ast_nodes import NativeCallNode
        assert isinstance(set_stmt.value.args[0], NativeCallNode)
        assert set_stmt.value.args[0].func_name == 'Player'
        assert set_stmt.value.args[0].args == ['0']

        # 验证其他参数
        assert set_stmt.value.args[1] == '1213484355'
        assert set_stmt.value.args[2] == '100.0'
        assert set_stmt.value.args[3] == '200.0'
        assert set_stmt.value.args[4] == '0.0'
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/parser/test_assignment_parser.py::TestParseCallArgs::test_parse_call_args_with_nested_call -v
```

Expected: FAIL（参数数量不对或类型不对）

**Step 3: 实现 `_parse_call_args` 方法**

在 `src/jass_runner/parser/assignment_parser.py` 的 `AssignmentParserMixin` 类中添加：

```python
def _parse_call_args(self: 'BaseParser') -> list:
    """解析函数调用参数列表，支持嵌套调用。

    前置条件：当前 token 是 '('
    后置条件：当前 token 是 ')'

    返回：
        参数列表，支持嵌套 NativeCallNode
    """
    from .ast_nodes import NativeCallNode

    args = []

    while self.current_token and self.current_token.value != ')':
        arg_value = None

        if self.current_token.type == 'INTEGER':
            arg_value = str(self.current_token.value)
            self.next_token()
        elif self.current_token.type == 'REAL':
            arg_value = str(self.current_token.value)
            self.next_token()
        elif self.current_token.type == 'STRING':
            arg_value = self.current_token.value
            self.next_token()
        elif self.current_token.type == 'FOURCC':
            arg_value = str(self.current_token.value)
            self.next_token()
        elif self.current_token.type == 'IDENTIFIER':
            arg_name = self.current_token.value
            self.next_token()

            # 检查是否是嵌套函数调用
            if self.current_token and self.current_token.value == '(':
                # 嵌套函数调用
                self.next_token()  # 跳过 '('
                nested_args = self._parse_call_args()
                # 跳过右括号
                if self.current_token and self.current_token.value == ')':
                    self.next_token()
                arg_value = NativeCallNode(func_name=arg_name, args=nested_args)
            else:
                # 普通标识符（变量名）
                arg_value = arg_name
        elif self.current_token.type == 'KEYWORD' and self.current_token.value in ('true', 'false'):
            # 布尔值
            arg_value = self.current_token.value
            self.next_token()
        else:
            # 不支持的类型，跳过
            self.next_token()

        if arg_value is not None:
            args.append(arg_value)

        # 检查是否有逗号继续下一个参数
        if self.current_token and self.current_token.value == ',':
            self.next_token()
            continue
        elif self.current_token and self.current_token.value == ')':
            break

    return args
```

**Step 4: 修改 `parse_set_statement` 使用新方法**

找到 `parse_set_statement` 中解析函数调用的部分（约第 398-429 行），替换为：

```python
elif self.current_token and self.current_token.value == '(':
    # 这是一个函数调用
    self.next_token()  # 跳过 '('

    # 使用 _parse_call_args 解析参数列表
    args = self._parse_call_args()

    # 跳过右括号
    if self.current_token and self.current_token.value == ')':
        self.next_token()

    value = NativeCallNode(func_name=expr_name, args=args)
```

**Step 5: 运行测试验证通过**

```bash
pytest tests/parser/test_assignment_parser.py::TestParseCallArgs::test_parse_call_args_with_nested_call -v
```

Expected: PASS

**Step 6: 提交**

```bash
git add src/jass_runner/parser/assignment_parser.py tests/parser/test_assignment_parser.py
git commit -m "feat(parser): add _parse_call_args method to support nested function calls"
```

---

## Task 2: 修改 `parse_local_declaration` 支持嵌套调用

**Files:**
- Modify: `src/jass_runner/parser/assignment_parser.py`
- Test: `tests/parser/test_assignment_parser.py`

**Step 1: 编写失败测试**

在 `tests/parser/test_assignment_parser.py` 中添加：

```python
def test_parse_local_declaration_with_nested_call(self):
    """测试 local 声明支持嵌套函数调用。"""
    code = '''
    function main takes nothing returns nothing
        local unit u = CreateUnit(Player(0), 1213484355, 100.0, 200.0, 0.0)
    endfunction
    '''
    parser = Parser(code)
    ast = parser.parse()

    # 获取 local 声明
    func = ast.functions[0]
    local_decl = func.body[0]

    # 验证参数数量
    assert len(local_decl.value.args) == 5

    # 验证第一个参数是嵌套调用
    from jass_runner.parser.ast_nodes import NativeCallNode
    assert isinstance(local_decl.value.args[0], NativeCallNode)
    assert local_decl.value.args[0].func_name == 'Player'
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/parser/test_assignment_parser.py::TestParseLocalDeclarationWithNestedCall -v
```

Expected: FAIL

**Step 3: 修改 `parse_local_declaration`**

找到 `parse_local_declaration` 中解析函数调用的部分（约第 88-119 行），替换参数解析逻辑为使用 `_parse_call_args`：

```python
if self.current_token and self.current_token.value == '(':
    # 这是一个函数调用
    self.next_token()  # 跳过 '('

    # 使用 _parse_call_args 解析参数列表
    args = self._parse_call_args()

    # 跳过右括号
    if self.current_token and self.current_token.value == ')':
        self.next_token()

    value = NativeCallNode(func_name=func_name, args=args)
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/parser/test_assignment_parser.py -v
```

Expected: PASS

**Step 5: 提交**

```bash
git add src/jass_runner/parser/assignment_parser.py tests/parser/test_assignment_parser.py
git commit -m "feat(parser): support nested calls in local declarations"
```

---

## Task 3: 重构 `parse_call_statement` 使用新方法

**Files:**
- Modify: `src/jass_runner/parser/assignment_parser.py`
- Test: `tests/parser/test_parser.py`（验证现有测试）

**Step 1: 运行现有测试确保通过**

```bash
pytest tests/parser/test_parser.py -v
```

Expected: PASS（所有现有测试应该通过）

**Step 2: 重构 `parse_call_statement`**

找到 `parse_call_statement` 方法（第 133-244 行），替换参数解析部分为使用 `_parse_call_args`：

```python
def parse_call_statement(self: 'BaseParser') -> Optional[NativeCallNode]:
    """解析call语句。"""
    try:
        # 跳过'call'关键词
        self.next_token()

        # 获取函数名
        if not self.current_token or self.current_token.type != 'IDENTIFIER':
            return None
        func_name = self.current_token.value
        self.next_token()

        # 检查左括号
        if not self.current_token or self.current_token.value != '(':
            return None
        self.next_token()

        # 使用 _parse_call_args 解析参数列表
        args = self._parse_call_args()

        # 检查右括号
        if self.current_token and self.current_token.value == ')':
            self.next_token()

        # 如果存在分号则跳过
        if self.current_token and self.current_token.value == ';':
            self.next_token()

        return NativeCallNode(func_name=func_name, args=args)

    except Exception:
        return None
```

**Step 3: 运行测试验证通过**

```bash
pytest tests/parser/test_parser.py -v
```

Expected: PASS（所有现有测试应该继续通过）

**Step 4: 提交**

```bash
git add src/jass_runner/parser/assignment_parser.py
git commit -m "refactor(parser): use _parse_call_args in parse_call_statement"
```

---

## Task 4: 添加更多边界情况测试

**Files:**
- Modify: `tests/parser/test_assignment_parser.py`

**Step 1: 编写边界情况测试**

```python
def test_parse_empty_args(self):
    """测试空参数列表。"""
    code = '''
    function main takes nothing returns nothing
        call SomeFunc()
    endfunction
    '''
    parser = Parser(code)
    ast = parser.parse()

    func = ast.functions[0]
    call_stmt = func.body[0]

    assert len(call_stmt.args) == 0


def test_parse_multiple_nested_calls(self):
    """测试多个嵌套调用。"""
    code = '''
    function main takes nothing returns nothing
        call FuncA(FuncB(1), FuncC(2))
    endfunction
    '''
    parser = Parser(code)
    ast = parser.parse()

    func = ast.functions[0]
    call_stmt = func.body[0]

    assert len(call_stmt.args) == 2
    from jass_runner.parser.ast_nodes import NativeCallNode
    assert isinstance(call_stmt.args[0], NativeCallNode)
    assert isinstance(call_stmt.args[1], NativeCallNode)


def test_parse_mixed_args(self):
    """测试混合参数类型。"""
    code = '''
    function main takes nothing returns nothing
        call Func(1, Player(0), "string", 3.14)
    endfunction
    '''
    parser = Parser(code)
    ast = parser.parse()

    func = ast.functions[0]
    call_stmt = func.body[0]

    assert len(call_stmt.args) == 4
    assert call_stmt.args[0] == '1'
    assert call_stmt.args[2] == '"string"'
    assert call_stmt.args[3] == '3.14'
```

**Step 2: 运行测试验证通过**

```bash
pytest tests/parser/test_assignment_parser.py -v
```

Expected: PASS

**Step 3: 提交**

```bash
git add tests/parser/test_assignment_parser.py
git commit -m "test(parser): add edge case tests for nested calls"
```

---

## Task 5: 修复集成测试

**Files:**
- Modify: `tests/integration/test_unit_natives.py`

**Step 1: 恢复完整的集成测试**

修改 `tests/integration/test_unit_natives.py`：

```python
"""单位操作 native 函数集成测试。"""

from jass_runner.vm.jass_vm import JassVM


class TestUnitNativesIntegration:
    """测试单位 native 函数完整工作流。"""

    def test_unit_lifecycle_workflow(self):
        """测试单位完整生命周期。"""
        code = '''
        function main takes nothing returns nothing
            local unit u
            // 创建单位
            set u = CreateUnit(Player(0), 1213484355, 100.0, 200.0, 0.0)

            // 获取并设置状态
            call SetUnitState(u, 0, 80.0)

            // 获取位置
            local real x = GetUnitX(u)
            local real y = GetUnitY(u)

            // 设置新位置
            call SetUnitPosition(u, 300.0, 400.0)

            // 设置朝向
            call SetUnitFacing(u, 90.0)
            local real facing = GetUnitFacing(u)

            // 获取单位信息
            local integer type_id = GetUnitTypeId(u)
            local string name = GetUnitName(u)

            // 杀死单位
            call KillUnit(u)
        endfunction
        '''

        vm = JassVM()
        vm.load_script(code)
        vm.execute()

    def test_create_unit_at_loc_workflow(self):
        """测试使用 Location 创建单位。"""
        code = '''
        function main takes nothing returns nothing
            local location loc = Location(500.0, 600.0)
            local unit u = CreateUnitAtLoc(Player(0), 1213484355, loc, 45.0)

            // 验证位置
            local real x = GetUnitX(u)
            local real y = GetUnitY(u)

            // 清理
            call RemoveLocation(loc)
            call KillUnit(u)
        endfunction
        '''

        vm = JassVM()
        vm.load_script(code)
        vm.execute()
```

**Step 2: 运行集成测试验证通过**

```bash
pytest tests/integration/test_unit_natives.py -v
```

Expected: PASS

**Step 3: 提交**

```bash
git add tests/integration/test_unit_natives.py
git commit -m "test(integration): restore full unit natives integration tests"
```

---

## Task 6: 运行所有测试确保无回归

**Files:**
- 所有测试文件

**Step 1: 运行完整测试套件**

```bash
pytest tests/ -v
```

Expected: 所有测试通过

**Step 2: 提交（如有必要）**

如果有任何修复，提交更改。

---

## Task 7: 更新项目文档

**Files:**
- Modify: `PROJECT_NOTES.md`

**Step 1: 添加完成记录**

在 `PROJECT_NOTES.md` 末尾添加：

```markdown
#### 44. 解析器嵌套函数调用修复完成 (2026-03-02)
- **问题**: 解析器无法正确处理嵌套函数调用（如 `CreateUnit(Player(0), ...)`）
- **解决方案**: 提取公共方法 `_parse_call_args` 统一处理参数解析
- **修改文件**: `src/jass_runner/parser/assignment_parser.py`
- **新增方法**: `_parse_call_args` - 支持嵌套调用的参数解析
- **重构**: `parse_call_statement`, `parse_set_statement`, `parse_local_declaration`
- **测试覆盖**:
  - 单元测试: 嵌套调用、空参数、混合参数
  - 集成测试: 完整的单位生命周期工作流
- **影响**: 所有现有测试继续通过，集成测试可以运行完整 JASS 代码
```

**Step 2: 提交**

```bash
git add PROJECT_NOTES.md
git commit -m "docs: update project notes for parser nested calls fix"
```

---

## 实施完成检查清单

- [ ] Task 1: 创建 `_parse_call_args` 方法
- [ ] Task 2: 修改 `parse_local_declaration` 支持嵌套调用
- [ ] Task 3: 重构 `parse_call_statement` 使用新方法
- [ ] Task 4: 添加边界情况测试
- [ ] Task 5: 修复集成测试
- [ ] Task 6: 运行所有测试确保无回归
- [ ] Task 7: 更新项目文档

---

## 注意事项

1. **向后兼容性**: 确保所有现有测试继续通过
2. **递归深度**: `_parse_call_args` 使用递归处理嵌套调用，但一般调用层级较浅（1-2层）
3. **错误处理**: 不支持的参数类型会跳过并继续解析
4. **测试覆盖**: 需要测试各种参数组合和边界情况
