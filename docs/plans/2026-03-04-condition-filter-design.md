# Condition 和 Filter 类型及 Native 函数设计

## 概述

实现 JASS 中的布尔表达式相关类型和 native 函数，用于触发器条件和单位过滤功能的组合。

## 需要实现的内容

### 1. 类型定义（common.j 第 23-26 行）

```jass
type boolexpr           extends     agent
type conditionfunc      extends     boolexpr
type filterfunc         extends     boolexpr
```

- `boolexpr`: 布尔表达式基础类型，继承自 `agent`
- `conditionfunc`: 条件函数类型，用于触发器条件，继承自 `boolexpr`
- `filterfunc`: 过滤函数类型，用于单位组枚举过滤，继承自 `filterfunc`

### 2. Native 函数（common.j 第 1052-1059 行）

```jass
native And              takes boolexpr operandA, boolexpr operandB returns boolexpr
native Or               takes boolexpr operandA, boolexpr operandB returns boolexpr
native Not              takes boolexpr operand returns boolexpr
native Condition        takes code func returns conditionfunc
native DestroyCondition takes conditionfunc c returns nothing
native Filter           takes code func returns filterfunc
native DestroyFilter    takes filterfunc f returns nothing
native DestroyBoolExpr  takes boolexpr e returns nothing
```

## 架构设计

### Handle 类层次结构

```
Handle (agent)
  └── BoolExpr (boolexpr)
        ├── ConditionFunc (conditionfunc)
        └── FilterFunc (filterfunc)
```

### 类设计

#### BoolExpr 基类

```python
class BoolExpr(Handle):
    """布尔表达式基类。"""
    def __init__(self, handle_id: str):
        super().__init__(handle_id, "boolexpr")
        self._func = None  # 可调用函数
```

#### ConditionFunc 类

```python
class ConditionFunc(BoolExpr):
    """条件函数，用于触发器条件判断。"""
    def __init__(self, handle_id: str, func: Callable):
        super().__init__(handle_id)
        self.type_name = "conditionfunc"
        self._func = func

    def evaluate(self) -> bool:
        """评估条件，返回布尔值。"""
        if self._func:
            return bool(self._func())
        return False
```

#### FilterFunc 类

```python
class FilterFunc(BoolExpr):
    """过滤函数，用于单位组枚举过滤。"""
    def __init__(self, handle_id: str, func: Callable):
        super().__init__(handle_id)
        self.type_name = "filterfunc"
        self._func = func

    def evaluate(self, unit) -> bool:
        """评估单位是否符合过滤条件。"""
        if self._func:
            return bool(self._func(unit))
        return False
```

#### 组合表达式类

```python
class AndExpr(BoolExpr):
    """逻辑与表达式。"""
    def __init__(self, handle_id: str, operand_a: BoolExpr, operand_b: BoolExpr):
        super().__init__(handle_id)
        self._operand_a = operand_a
        self._operand_b = operand_b

    def evaluate(self, *args) -> bool:
        return self._operand_a.evaluate(*args) and self._operand_b.evaluate(*args)

class OrExpr(BoolExpr):
    """逻辑或表达式。"""
    def __init__(self, handle_id: str, operand_a: BoolExpr, operand_b: BoolExpr):
        super().__init__(handle_id)
        self._operand_a = operand_a
        self._operand_b = operand_b

    def evaluate(self, *args) -> bool:
        return self._operand_a.evaluate(*args) or self._operand_b.evaluate(*args)

class NotExpr(BoolExpr):
    """逻辑非表达式。"""
    def __init__(self, handle_id: str, operand: BoolExpr):
        super().__init__(handle_id)
        self._operand = operand

    def evaluate(self, *args) -> bool:
        return not self._operand.evaluate(*args)
```

### Native 函数实现

#### Condition native

```python
class Condition(NativeFunction):
    """将 code 函数包装为 conditionfunc。"""

    @property
    def name(self) -> str:
        return "Condition"

    def execute(self, state_context, func: Callable, *args, **kwargs):
        handle_id = f"condition_{generate_id()}"
        condition = ConditionFunc(handle_id, func)
        state_context.handle_manager.register_boolexpr(condition)
        return handle_id
```

#### Filter native

```python
class Filter(NativeFunction):
    """将 code 函数包装为 filterfunc。"""

    @property
    def name(self) -> str:
        return "Filter"

    def execute(self, state_context, func: Callable, *args, **kwargs):
        handle_id = f"filter_{generate_id()}"
        filter_func = FilterFunc(handle_id, func)
        state_context.handle_manager.register_boolexpr(filter_func)
        return handle_id
```

#### And/Or/Not natives

```python
class And(NativeFunction):
    """创建逻辑与表达式。"""

    @property
    def name(self) -> str:
        return "And"

    def execute(self, state_context, operand_a: str, operand_b: str, *args, **kwargs):
        # 从 handle_manager 获取 BoolExpr 对象
        expr_a = state_context.handle_manager.get_boolexpr(operand_a)
        expr_b = state_context.handle_manager.get_boolexpr(operand_b)

        handle_id = f"boolexpr_{generate_id()}"
        and_expr = AndExpr(handle_id, expr_a, expr_b)
        state_context.handle_manager.register_boolexpr(and_expr)
        return handle_id
```

#### Destroy 系列 natives

```python
class DestroyCondition(NativeFunction):
    """销毁 conditionfunc。"""

    @property
    def name(self) -> str:
        return "DestroyCondition"

    def execute(self, state_context, condition_id: str, *args, **kwargs):
        state_context.handle_manager.destroy_handle(condition_id)
```

## HandleManager 扩展

需要在 HandleManager 中添加：

```python
def register_boolexpr(self, boolexpr: BoolExpr):
    """注册布尔表达式 handle。"""
    self._register_handle(boolexpr)

def get_boolexpr(self, handle_id: str) -> Optional[BoolExpr]:
    """获取布尔表达式对象。"""
    handle = self.get_handle(handle_id)
    if isinstance(handle, BoolExpr):
        return handle
    return None
```

## 测试策略

1. **单元测试**：测试每个 native 函数的基本功能
2. **集成测试**：测试 Condition/Filter 与 TriggerAddCondition/ForGroup 的集成
3. **组合测试**：测试 And/Or/Not 的组合逻辑

## 文件变更

1. `src/jass_runner/natives/handle.py` - 添加 BoolExpr, ConditionFunc, FilterFunc 类
2. `src/jass_runner/natives/manager.py` - 添加 boolexpr 相关管理方法
3. `src/jass_runner/natives/boolexpr_natives.py` - 新建，实现所有 native 函数
4. `src/jass_runner/natives/factory.py` - 注册新的 native 函数
