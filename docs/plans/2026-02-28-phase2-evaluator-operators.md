# Phase 2: Evaluator层运算符支持实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 扩展Evaluator以支持算术、比较、逻辑运算符和表达式求值

**Architecture:** 在evaluator.py中添加运算符优先级表，使用调度场算法或递归下降解析表达式，支持完整运算符

**Tech Stack:** Python 3.8+, 现有Evaluator框架

**Dependencies:** Phase 1完成（Parser层控制流支持）

---

## 前置知识

### 现有Evaluator结构
- 文件位置: `src/jass_runner/interpreter/evaluator.py`
- 当前evaluate()方法只处理简单字面量（整数、字符串、布尔值）
- 需要扩展以支持运算符表达式

### JASS运算符优先级（从高到低）
```
1. not, - (一元)
2. *, /
3. +, -
4. <, >, <=, >=
5. ==, !=
6. and
7. or
```

---

## Task 1: 添加运算符优先级定义

**Files:**
- Modify: `src/jass_runner/interpreter/evaluator.py`
- Test: `tests/interpreter/test_evaluator.py`

**Step 1: 编写失败测试**

```python
def test_operator_precedence_constants():
    """测试运算符优先级常量定义"""
    from jass_runner.interpreter.evaluator import Evaluator, OperatorPrecedence

    assert OperatorPrecedence.UNARY == 7
    assert OperatorPrecedence.MULTIPLICATIVE == 6
    assert OperatorPrecedence.ADDITIVE == 5
    assert OperatorPrecedence.RELATIONAL == 4
    assert OperatorPrecedence.EQUALITY == 3
    assert OperatorPrecedence.AND == 2
    assert OperatorPrecedence.OR == 1
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/interpreter/test_evaluator.py::test_operator_precedence_constants -v
```
Expected: FAIL (OperatorPrecedence not defined)

**Step 3: 添加OperatorPrecedence类**

在evaluator.py中添加:
```python
class OperatorPrecedence:
    """运算符优先级（数字越大优先级越高）"""
    OR = 1
    AND = 2
    EQUALITY = 3
    RELATIONAL = 4
    ADDITIVE = 5
    MULTIPLICATIVE = 6
    UNARY = 7
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/interpreter/test_evaluator.py::test_operator_precedence_constants -v
```
Expected: PASS

**Step 5: 提交**

```bash
git add tests/interpreter/test_evaluator.py src/jass_runner/interpreter/evaluator.py
git commit -m "feat(evaluator): 添加运算符优先级常量

- 定义OperatorPrecedence类
- 设置标准运算符优先级

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 2: 实现算术运算符求值

**Files:**
- Modify: `src/jass_runner/interpreter/evaluator.py`
- Test: `tests/interpreter/test_evaluator.py`

**Step 1: 编写失败测试**

```python
def test_evaluate_arithmetic_addition():
    """测试加法运算"""
    from jass_runner.interpreter.evaluator import Evaluator
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    evaluator = Evaluator(context)

    result = evaluator.evaluate("5 + 3")
    assert result == 8
```

```python
def test_evaluate_arithmetic_mixed_types():
    """测试混合类型运算"""
    from jass_runner.interpreter.evaluator import Evaluator
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    evaluator = Evaluator(context)

    result = evaluator.evaluate("5 + 3.5")
    assert result == 8.5
    assert isinstance(result, float)
```

```python
def test_evaluate_arithmetic_all_operators():
    """测试所有算术运算符"""
    from jass_runner.interpreter.evaluator import Evaluator
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    evaluator = Evaluator(context)

    assert evaluator.evaluate("10 - 3") == 7
    assert evaluator.evaluate("4 * 5") == 20
    assert evaluator.evaluate("15 / 3") == 5.0
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/interpreter/test_evaluator.py::test_evaluate_arithmetic_addition tests/interpreter/test_evaluator.py::test_evaluate_arithmetic_mixed_types tests/interpreter/test_evaluator.py::test_evaluate_arithmetic_all_operators -v
```
Expected: FAIL (evaluate()不支持运算符)

**Step 3: 扩展evaluate()方法支持算术运算**

修改evaluate()方法，添加表达式分词和解析:
```python
def evaluate(self, expression: str) -> Any:
    """求值一个JASS表达式，支持运算符"""
    expression = expression.strip()

    # 分词
    tokens = self._tokenize_expression(expression)

    if len(tokens) == 1:
        # 单个值，按原有方式处理
        return self._evaluate_single_value(tokens[0])

    # 多个token，解析表达式
    return self._parse_and_evaluate(tokens)

def _tokenize_expression(self, expression: str) -> List[str]:
    """将表达式分词"""
    tokens = []
    current = ""
    i = 0
    while i < len(expression):
        char = expression[i]

        # 跳过空白
        if char.isspace():
            if current:
                tokens.append(current)
                current = ""
            i += 1
            continue

        # 运算符
        if char in '+-*/()':
            if current:
                tokens.append(current)
                current = ""
            tokens.append(char)
            i += 1
            continue

        current += char
        i += 1

    if current:
        tokens.append(current)

    return tokens

def _parse_and_evaluate(self, tokens: List[str]) -> Any:
    """解析并求值表达式（使用简单递归下降）"""
    # 先实现简单版本：从左到右处理算术运算
    # 完整版在后续task中实现优先级

    if len(tokens) == 3:
        left = self._evaluate_single_value(tokens[0])
        op = tokens[1]
        right = self._evaluate_single_value(tokens[2])
        return self._apply_operator(left, op, right)

    # 更多token的情况暂时抛出异常或简化处理
    return self._evaluate_simple_left_to_right(tokens)

def _apply_operator(self, left: Any, op: str, right: Any) -> Any:
    """应用二元运算符"""
    if op == '+':
        return left + right
    elif op == '-':
        return left - right
    elif op == '*':
        return left * right
    elif op == '/':
        return left / right
    else:
        raise ValueError(f"未知运算符: {op}")

def _evaluate_simple_left_to_right(self, tokens: List[str]) -> Any:
    """简单从左到右求值（用于基础实现）"""
    result = self._evaluate_single_value(tokens[0])
    i = 1
    while i < len(tokens):
        op = tokens[i]
        right = self._evaluate_single_value(tokens[i + 1])
        result = self._apply_operator(result, op, right)
        i += 2
    return result
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/interpreter/test_evaluator.py::test_evaluate_arithmetic_addition tests/interpreter/test_evaluator.py::test_evaluate_arithmetic_mixed_types tests/interpreter/test_evaluator.py::test_evaluate_arithmetic_all_operators -v
```
Expected: PASS

**Step 5: 提交**

```bash
git add tests/interpreter/test_evaluator.py src/jass_runner/interpreter/evaluator.py
git commit -m "feat(evaluator): 实现算术运算符求值

- 添加表达式分词功能
- 支持+、-、*、/运算符
- 支持整数和实数混合运算

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 3: 实现运算符优先级

**Files:**
- Modify: `src/jass_runner/interpreter/evaluator.py`
- Test: `tests/interpreter/test_evaluator.py`

**Step 1: 编写失败测试**

```python
def test_operator_precedence_multiplication_before_addition():
    """测试乘法优先级高于加法"""
    from jass_runner.interpreter.evaluator import Evaluator
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    evaluator = Evaluator(context)

    # 2 + 3 * 4 应该等于 14，不是 20
    result = evaluator.evaluate("2 + 3 * 4")
    assert result == 14
```

```python
def test_operator_precedence_with_parentheses():
    """测试括号优先级"""
    from jass_runner.interpreter.evaluator import Evaluator
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    evaluator = Evaluator(context)

    # (2 + 3) * 4 应该等于 20
    result = evaluator.evaluate("(2 + 3) * 4")
    assert result == 20
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/interpreter/test_evaluator.py::test_operator_precedence_multiplication_before_addition tests/interpreter/test_evaluator.py::test_operator_precedence_with_parentheses -v
```
Expected: FAIL (当前是简单从左到右求值，不符合优先级)

**Step 3: 实现优先级解析（调度场算法）**

```python
def _parse_and_evaluate(self, tokens: List[str]) -> Any:
    """使用调度场算法解析表达式"""
    output = []
    operators = []

    i = 0
    while i < len(tokens):
        token = tokens[i]

        if token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            operators.pop()  # 弹出'('
        elif self._is_operator(token):
            while (operators and operators[-1] != '(' and
                   self._get_precedence(operators[-1]) >= self._get_precedence(token)):
                output.append(operators.pop())
            operators.append(token)
        else:
            output.append(self._evaluate_single_value(token))

        i += 1

    while operators:
        output.append(operators.pop())

    return self._evaluate_rpn(output)

def _is_operator(self, token: str) -> bool:
    """判断是否为运算符"""
    return token in ('+', '-', '*', '/', '==', '!=', '<', '>', '<=', '>=', 'and', 'or', 'not')

def _get_precedence(self, op: str) -> int:
    """获取运算符优先级"""
    precedence_map = {
        'or': OperatorPrecedence.OR,
        'and': OperatorPrecedence.AND,
        '==': OperatorPrecedence.EQUALITY,
        '!=': OperatorPrecedence.EQUALITY,
        '<': OperatorPrecedence.RELATIONAL,
        '>': OperatorPrecedence.RELATIONAL,
        '<=': OperatorPrecedence.RELATIONAL,
        '>=': OperatorPrecedence.RELATIONAL,
        '+': OperatorPrecedence.ADDITIVE,
        '-': OperatorPrecedence.ADDITIVE,
        '*': OperatorPrecedence.MULTIPLICATIVE,
        '/': OperatorPrecedence.MULTIPLICATIVE,
        'not': OperatorPrecedence.UNARY,
    }
    return precedence_map.get(op, 0)

def _evaluate_rpn(self, rpn: List[Any]) -> Any:
    """求值逆波兰表达式"""
    stack = []

    for token in rpn:
        if isinstance(token, (int, float, bool, str)):
            stack.append(token)
        elif token in ('+', '-', '*', '/', '==', '!=', '<', '>', '<=', '>=', 'and', 'or'):
            right = stack.pop()
            left = stack.pop()
            result = self._apply_operator(left, token, right)
            stack.append(result)
        elif token == 'not':
            operand = stack.pop()
            stack.append(not operand)

    return stack[0]
```

更新_apply_operator支持更多运算符:
```python
def _apply_operator(self, left: Any, op: str, right: Any) -> Any:
    """应用二元运算符"""
    if op == '+':
        return left + right
    elif op == '-':
        return left - right
    elif op == '*':
        return left * right
    elif op == '/':
        return left / right
    elif op == '==':
        return left == right
    elif op == '!=':
        return left != right
    elif op == '<':
        return left < right
    elif op == '>':
        return left > right
    elif op == '<=':
        return left <= right
    elif op == '>=':
        return left >= right
    elif op == 'and':
        return left and right
    elif op == 'or':
        return left or right
    else:
        raise ValueError(f"未知运算符: {op}")
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/interpreter/test_evaluator.py::test_operator_precedence_multiplication_before_addition tests/interpreter/test_evaluator.py::test_operator_precedence_with_parentheses -v
```
Expected: PASS

**Step 5: 提交**

```bash
git add tests/interpreter/test_evaluator.py src/jass_runner/interpreter/evaluator.py
git commit -m "feat(evaluator): 实现运算符优先级支持

- 使用调度场算法处理运算符优先级
- 支持括号分组
- 构建RPN并求值

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 4: 实现比较运算符

**Files:**
- Test: `tests/interpreter/test_evaluator.py` (运算符已实现，只需测试)

**Step 1: 编写测试**

```python
def test_evaluate_comparison_operators():
    """测试比较运算符"""
    from jass_runner.interpreter.evaluator import Evaluator
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    evaluator = Evaluator(context)

    assert evaluator.evaluate("5 == 5") is True
    assert evaluator.evaluate("5 != 3") is True
    assert evaluator.evaluate("5 > 3") is True
    assert evaluator.evaluate("3 < 5") is True
    assert evaluator.evaluate("5 >= 5") is True
    assert evaluator.evaluate("3 <= 5") is True
```

**Step 2: 运行测试**

```bash
pytest tests/interpreter/test_evaluator.py::test_evaluate_comparison_operators -v
```
Expected: PASS (Task 3已实现)

**Step 3: 提交**

```bash
git add tests/interpreter/test_evaluator.py
git commit -m "test(evaluator): 添加比较运算符测试

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 5: 实现逻辑运算符

**Files:**
- Modify: `src/jass_runner/interpreter/evaluator.py` (更新分词器支持多字符运算符)
- Test: `tests/interpreter/test_evaluator.py`

**Step 1: 编写失败测试**

```python
def test_evaluate_logical_operators():
    """测试逻辑运算符"""
    from jass_runner.interpreter.evaluator import Evaluator
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    evaluator = Evaluator(context)

    assert evaluator.evaluate("true and true") is True
    assert evaluator.evaluate("true and false") is False
    assert evaluator.evaluate("true or false") is True
    assert evaluator.evaluate("false or false") is False
    assert evaluator.evaluate("not true") is False
    assert evaluator.evaluate("not false") is True
```

```python
def test_evaluate_complex_logical_expression():
    """测试复杂逻辑表达式"""
    from jass_runner.interpreter.evaluator import Evaluator
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    evaluator = Evaluator(context)

    # (5 > 3) and (2 < 4)
    result = evaluator.evaluate("5 > 3 and 2 < 4")
    assert result is True
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/interpreter/test_evaluator.py::test_evaluate_logical_operators tests/interpreter/test_evaluator.py::test_evaluate_complex_logical_expression -v
```
Expected: FAIL (分词器不支持多字符运算符如"and", "or", "==", "!=", "<=", ">=")

**Step 3: 更新分词器支持多字符运算符**

重写_tokenize_expression方法:
```python
def _tokenize_expression(self, expression: str) -> List[str]:
    """将表达式分词，支持多字符运算符"""
    tokens = []
    i = 0

    # 多字符运算符（按长度降序排列，优先匹配长的）
    multi_char_ops = ['==', '!=', '<=', '>=', 'and', 'or', 'not']

    while i < len(expression):
        char = expression[i]

        # 跳过空白
        if char.isspace():
            i += 1
            continue

        # 检查多字符运算符
        matched = False
        for op in multi_char_ops:
            if expression[i:i+len(op)] == op:
                tokens.append(op)
                i += len(op)
                matched = True
                break

        if matched:
            continue

        # 单字符运算符
        if char in '+-*/()<>':
            tokens.append(char)
            i += 1
            continue

        # 字面量（数字、标识符、布尔值）
        if char.isalnum() or char == '_' or char == '"':
            current = ""
            if char == '"':
                # 字符串字面量
                current += char
                i += 1
                while i < len(expression) and expression[i] != '"':
                    current += expression[i]
                    i += 1
                if i < len(expression):
                    current += expression[i]
                    i += 1
            else:
                while i < len(expression) and (expression[i].isalnum() or expression[i] == '_'):
                    current += expression[i]
                    i += 1
            tokens.append(current)
            continue

        i += 1

    return tokens
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/interpreter/test_evaluator.py::test_evaluate_logical_operators tests/interpreter/test_evaluator.py::test_evaluate_complex_logical_expression -v
```
Expected: PASS

**Step 5: 提交**

```bash
git add tests/interpreter/test_evaluator.py src/jass_runner/interpreter/evaluator.py
git commit -m "feat(evaluator): 实现逻辑运算符支持

- 更新分词器支持多字符运算符
- 支持and、or、not逻辑运算
- 支持复杂组合表达式

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 6: 实现evaluate_condition方法

**Files:**
- Modify: `src/jass_runner/interpreter/evaluator.py`
- Test: `tests/interpreter/test_evaluator.py`

**Step 1: 编写失败测试**

```python
def test_evaluate_condition_simple():
    """测试条件求值"""
    from jass_runner.interpreter.evaluator import Evaluator
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    evaluator = Evaluator(context)

    assert evaluator.evaluate_condition("5 > 3") is True
    assert evaluator.evaluate_condition("5 < 3") is False
    assert evaluator.evaluate_condition("true") is True
    assert evaluator.evaluate_condition("false") is False
```

```python
def test_evaluate_condition_complex():
    """测试复杂条件求值"""
    from jass_runner.interpreter.evaluator import Evaluator
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    evaluator = Evaluator(context)

    assert evaluator.evaluate_condition("5 > 3 and 2 < 4") is True
    assert evaluator.evaluate_condition("not false") is True
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/interpreter/test_evaluator.py::test_evaluate_condition_simple tests/interpreter/test_evaluator.py::test_evaluate_condition_complex -v
```
Expected: FAIL (evaluate_condition not defined)

**Step 3: 添加evaluate_condition方法**

```python
def evaluate_condition(self, condition: Any) -> bool:
    """求值条件表达式，返回布尔结果"""
    if isinstance(condition, str):
        result = self.evaluate(condition)
    else:
        result = condition

    # 转换结果为布尔值
    if isinstance(result, bool):
        return result
    elif isinstance(result, (int, float)):
        return result != 0
    elif isinstance(result, str):
        return result.lower() == "true"
    return bool(result)
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/interpreter/test_evaluator.py::test_evaluate_condition_simple tests/interpreter/test_evaluator.py::test_evaluate_condition_complex -v
```
Expected: PASS

**Step 5: 提交**

```bash
git add tests/interpreter/test_evaluator.py src/jass_runner/interpreter/evaluator.py
git commit -m "feat(evaluator): 添加evaluate_condition方法

- 专门用于求值条件表达式
- 统一返回布尔结果
- 支持字符串条件解析

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Phase 2 完成检查清单

- [x] OperatorPrecedence常量定义
- [x] 算术运算符支持（+、-、*、/）
- [x] 运算符优先级实现（调度场算法）
- [x] 比较运算符支持（==、!=、<、>、<=、>=）
- [x] 逻辑运算符支持（and、or、not）
- [x] evaluate_condition方法
- [x] 所有测试通过

**下一步:** Phase 3 - Interpreter层控制流执行
