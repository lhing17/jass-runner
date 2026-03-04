# Condition 和 Filter Native 函数实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现 JASS 中的布尔表达式类型（boolexpr, conditionfunc, filterfunc）和相关的 7 个 native 函数

**Architecture:** 在现有 Handle 类层次结构中添加 BoolExpr 基类和 ConditionFunc/FilterFunc 子类，通过 HandleManager 管理生命周期，实现 And/Or/Not 组合逻辑

**Tech Stack:** Python 3.8+, pytest, 现有 JASS Runner 框架

---

## 前置知识

### 类型层次结构（common.j）
```jass
type boolexpr           extends     agent
type conditionfunc      extends     boolexpr
type filterfunc         extends     boolexpr
```

### 需要实现的 Native 函数
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

### 现有代码位置
- Handle 基类: `src/jass_runner/natives/handle.py`
- HandleManager: `src/jass_runner/natives/manager.py`
- Native 基类: `src/jass_runner/natives/base.py`
- Native 工厂: `src/jass_runner/natives/factory.py`

---

### Task 1: 添加 BoolExpr 基类

**Files:**
- Modify: `src/jass_runner/natives/handle.py`

**Step 1: 在 handle.py 末尾添加 BoolExpr 类（在 Effect 类之后）**

```python
class BoolExpr(Handle):
    """布尔表达式基类，用于条件判断和过滤。

    属性：
        _func: 包装的函数（可为None）
    """

    def __init__(self, handle_id: str):
        """初始化布尔表达式。

        参数：
            handle_id: 唯一标识符
        """
        super().__init__(handle_id, "boolexpr")
        self._func = None

    def evaluate(self, *args, **kwargs) -> bool:
        """评估表达式，返回布尔值。

        参数：
            *args, **kwargs: 传递给包装函数的参数

        返回：
            评估结果，无函数时返回False
        """
        if self._func:
            return bool(self._func(*args, **kwargs))
        return False
```

**Step 2: 验证语法**

Run: `python -c "from src.jass_runner.natives.handle import BoolExpr; print('OK')"`
Expected: `OK`

**Step 3: Commit**

```bash
git add src/jass_runner/natives/handle.py
git commit -m "feat: 添加 BoolExpr 基类"
```

---

### Task 2: 添加 ConditionFunc 类

**Files:**
- Modify: `src/jass_runner/natives/handle.py`

**Step 1: 在 BoolExpr 类后添加 ConditionFunc 类**

```python
class ConditionFunc(BoolExpr):
    """条件函数，用于触发器条件判断。

    继承自 BoolExpr，专门用于 TriggerAddCondition。
    包装的函数不接受参数，返回布尔值。
    """

    def __init__(self, handle_id: str, func=None):
        """初始化条件函数。

        参数：
            handle_id: 唯一标识符
            func: 条件函数（无参数，返回bool）
        """
        super().__init__(handle_id)
        self.type_name = "conditionfunc"
        self._func = func

    def evaluate(self) -> bool:
        """评估条件。

        返回：
            条件函数的执行结果，无函数时返回False
        """
        if self._func:
            return bool(self._func())
        return False
```

**Step 2: 验证语法**

Run: `python -c "from src.jass_runner.natives.handle import ConditionFunc; print('OK')"`
Expected: `OK`

**Step 3: Commit**

```bash
git add src/jass_runner/natives/handle.py
git commit -m "feat: 添加 ConditionFunc 类"
```

---

### Task 3: 添加 FilterFunc 类

**Files:**
- Modify: `src/jass_runner/natives/handle.py`

**Step 1: 在 ConditionFunc 类后添加 FilterFunc 类**

```python
class FilterFunc(BoolExpr):
    """过滤函数，用于单位组枚举过滤。

    继承自 BoolExpr，专门用于 GroupEnumUnits 等函数。
    包装的函数接受一个单位参数，返回布尔值。
    """

    def __init__(self, handle_id: str, func=None):
        """初始化过滤函数。

        参数：
            handle_id: 唯一标识符
            func: 过滤函数（接受unit参数，返回bool）
        """
        super().__init__(handle_id)
        self.type_name = "filterfunc"
        self._func = func

    def evaluate(self, unit) -> bool:
        """评估单位是否符合过滤条件。

        参数：
            unit: 要评估的单位对象

        返回：
            过滤函数的执行结果，无函数时返回False
        """
        if self._func:
            return bool(self._func(unit))
        return False
```

**Step 2: 验证语法**

Run: `python -c "from src.jass_runner.natives.handle import FilterFunc; print('OK')"`
Expected: `OK`

**Step 3: Commit**

```bash
git add src/jass_runner/natives/handle.py
git commit -m "feat: 添加 FilterFunc 类"
```

---

### Task 4: 添加组合表达式类（AndExpr, OrExpr, NotExpr）

**Files:**
- Modify: `src/jass_runner/natives/handle.py`

**Step 1: 在 FilterFunc 类后添加三个组合表达式类**

```python
class AndExpr(BoolExpr):
    """逻辑与表达式。

    组合两个布尔表达式，当两者都为True时返回True。
    """

    def __init__(self, handle_id: str, operand_a: BoolExpr, operand_b: BoolExpr):
        """初始化逻辑与表达式。

        参数：
            handle_id: 唯一标识符
            operand_a: 第一个操作数
            operand_b: 第二个操作数
        """
        super().__init__(handle_id)
        self._operand_a = operand_a
        self._operand_b = operand_b

    def evaluate(self, *args, **kwargs) -> bool:
        """评估逻辑与表达式。

        参数：
            *args, **kwargs: 传递给操作数的参数

        返回：
            两个操作数都为True时返回True
        """
        return self._operand_a.evaluate(*args, **kwargs) and self._operand_b.evaluate(*args, **kwargs)


class OrExpr(BoolExpr):
    """逻辑或表达式。

    组合两个布尔表达式，当任一者为True时返回True。
    """

    def __init__(self, handle_id: str, operand_a: BoolExpr, operand_b: BoolExpr):
        """初始化逻辑或表达式。

        参数：
            handle_id: 唯一标识符
            operand_a: 第一个操作数
            operand_b: 第二个操作数
        """
        super().__init__(handle_id)
        self._operand_a = operand_a
        self._operand_b = operand_b

    def evaluate(self, *args, **kwargs) -> bool:
        """评估逻辑或表达式。

        参数：
            *args, **kwargs: 传递给操作数的参数

        返回：
            任一操作数为True时返回True
        """
        return self._operand_a.evaluate(*args, **kwargs) or self._operand_b.evaluate(*args, **kwargs)


class NotExpr(BoolExpr):
    """逻辑非表达式。

    对一个布尔表达式取反。
    """

    def __init__(self, handle_id: str, operand: BoolExpr):
        """初始化逻辑非表达式。

        参数：
            handle_id: 唯一标识符
            operand: 操作数
        """
        super().__init__(handle_id)
        self._operand = operand

    def evaluate(self, *args, **kwargs) -> bool:
        """评估逻辑非表达式。

        参数：
            *args, **kwargs: 传递给操作数的参数

        返回：
            操作数为False时返回True
        """
        return not self._operand.evaluate(*args, **kwargs)
```

**Step 2: 验证语法**

Run: `python -c "from src.jass_runner.natives.handle import AndExpr, OrExpr, NotExpr; print('OK')"`
Expected: `OK`

**Step 3: Commit**

```bash
git add src/jass_runner/natives/handle.py
git commit -m "feat: 添加 AndExpr, OrExpr, NotExpr 组合表达式类"
```

---

### Task 5: 在 HandleManager 中添加 BoolExpr 管理方法

**Files:**
- Modify: `src/jass_runner/natives/manager.py`
- Modify: `src/jass_runner/natives/handle.py` (导出 BoolExpr)

**Step 1: 修改 manager.py 导入 BoolExpr**

在文件顶部的导入语句中，从 handle 模块导入 BoolExpr：

```python
from .handle import Handle, Unit, Player, Item, Group, Rect, Effect, BoolExpr
```

**Step 2: 在 HandleManager 类中添加 get_boolexpr 方法**

在 `get_effect` 方法后添加：

```python
    def get_boolexpr(self, handle_id: str) -> Optional[BoolExpr]:
        """获取布尔表达式对象，进行类型检查。

        参数：
            handle_id: 布尔表达式ID

        返回：
            BoolExpr对象，如果不存在或类型不匹配返回None
        """
        handle = self.get_handle(handle_id)
        if isinstance(handle, BoolExpr):
            return handle
        return None
```

**Step 3: 验证语法**

Run: `python -c "from src.jass_runner.natives.manager import HandleManager; print('OK')"`
Expected: `OK`

**Step 4: Commit**

```bash
git add src/jass_runner/natives/manager.py
git commit -m "feat: HandleManager 添加 get_boolexpr 方法"
```

---

### Task 6: 创建 boolexpr_natives.py 文件 - Condition native

**Files:**
- Create: `src/jass_runner/natives/boolexpr_natives.py`

**Step 1: 创建文件并添加 Condition native**

```python
"""布尔表达式相关的原生函数。

此模块包含 Condition、Filter、And、Or、Not 等 native 函数的实现，
用于创建和管理布尔表达式、条件函数和过滤函数。
"""

import logging
from typing import Callable, Optional
from ..natives.base import NativeFunction


logger = logging.getLogger(__name__)


class Condition(NativeFunction):
    """将 code 函数包装为 conditionfunc。

    创建一个 conditionfunc 对象，包装传入的函数。
    被包装的函数不接受参数，应返回布尔值。
    """

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "Condition"
        """
        return "Condition"

    def execute(self, state_context, func: Callable, *args, **kwargs):
        """执行 Condition native 函数。

        参数：
            state_context: 状态上下文，必须包含 handle_manager
            func: 要包装的条件函数（无参数，返回bool）
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            conditionfunc 的 handle ID，失败返回 None
        """
        # 检查 state_context 和 handle_manager
        if state_context is None:
            logger.error("[Condition] state_context is None")
            return None

        if not hasattr(state_context, 'handle_manager') or state_context.handle_manager is None:
            logger.error("[Condition] handle_manager not found in state_context")
            return None

        # 检查 func 是否可调用
        if not callable(func):
            logger.error("[Condition] func is not callable")
            return None

        # 生成唯一ID
        handle_id = f"condition_{state_context.handle_manager._generate_id()}"

        # 导入 ConditionFunc 类
        from .handle import ConditionFunc

        # 创建 ConditionFunc 对象
        condition = ConditionFunc(handle_id, func)

        # 注册到 handle_manager
        state_context.handle_manager._register_handle(condition)

        logger.info(f"[Condition] Created conditionfunc: {handle_id}")
        return handle_id
```

**Step 2: 验证语法**

Run: `python -c "from src.jass_runner.natives.boolexpr_natives import Condition; print('OK')"`
Expected: `OK`

**Step 3: Commit**

```bash
git add src/jass_runner/natives/boolexpr_natives.py
git commit -m "feat: 实现 Condition native 函数"
```

---

### Task 7: 添加 Filter native

**Files:**
- Modify: `src/jass_runner/natives/boolexpr_natives.py`

**Step 1: 在 Condition 类后添加 Filter 类**

```python

class Filter(NativeFunction):
    """将 code 函数包装为 filterfunc。

    创建一个 filterfunc 对象，包装传入的函数。
    被包装的函数接受一个单位参数，应返回布尔值。
    """

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "Filter"
        """
        return "Filter"

    def execute(self, state_context, func: Callable, *args, **kwargs):
        """执行 Filter native 函数。

        参数：
            state_context: 状态上下文，必须包含 handle_manager
            func: 要包装的过滤函数（接受unit参数，返回bool）
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            filterfunc 的 handle ID，失败返回 None
        """
        # 检查 state_context 和 handle_manager
        if state_context is None:
            logger.error("[Filter] state_context is None")
            return None

        if not hasattr(state_context, 'handle_manager') or state_context.handle_manager is None:
            logger.error("[Filter] handle_manager not found in state_context")
            return None

        # 检查 func 是否可调用
        if not callable(func):
            logger.error("[Filter] func is not callable")
            return None

        # 生成唯一ID
        handle_id = f"filter_{state_context.handle_manager._generate_id()}"

        # 导入 FilterFunc 类
        from .handle import FilterFunc

        # 创建 FilterFunc 对象
        filter_func = FilterFunc(handle_id, func)

        # 注册到 handle_manager
        state_context.handle_manager._register_handle(filter_func)

        logger.info(f"[Filter] Created filterfunc: {handle_id}")
        return handle_id
```

**Step 2: 验证语法**

Run: `python -c "from src.jass_runner.natives.boolexpr_natives import Filter; print('OK')"`
Expected: `OK`

**Step 3: Commit**

```bash
git add src/jass_runner/natives/boolexpr_natives.py
git commit -m "feat: 实现 Filter native 函数"
```

---

### Task 8: 添加 DestroyCondition 和 DestroyFilter natives

**Files:**
- Modify: `src/jass_runner/natives/boolexpr_natives.py`

**Step 1: 在 Filter 类后添加销毁函数**

```python

class DestroyCondition(NativeFunction):
    """销毁 conditionfunc。"""

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "DestroyCondition"
        """
        return "DestroyCondition"

    def execute(self, state_context, condition_id: str, *args, **kwargs):
        """执行 DestroyCondition native 函数。

        参数：
            state_context: 状态上下文，必须包含 handle_manager
            condition_id: 要销毁的 conditionfunc ID
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            None（对应 JASS 的 nothing）
        """
        # 检查 state_context 和 handle_manager
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[DestroyCondition] state_context or handle_manager not found")
            return None

        # 销毁 handle
        success = state_context.handle_manager.destroy_handle(condition_id)
        if success:
            logger.info(f"[DestroyCondition] Destroyed conditionfunc: {condition_id}")
        else:
            logger.warning(f"[DestroyCondition] conditionfunc not found: {condition_id}")

        return None


class DestroyFilter(NativeFunction):
    """销毁 filterfunc。"""

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "DestroyFilter"
        """
        return "DestroyFilter"

    def execute(self, state_context, filter_id: str, *args, **kwargs):
        """执行 DestroyFilter native 函数。

        参数：
            state_context: 状态上下文，必须包含 handle_manager
            filter_id: 要销毁的 filterfunc ID
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            None（对应 JASS 的 nothing）
        """
        # 检查 state_context 和 handle_manager
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[DestroyFilter] state_context or handle_manager not found")
            return None

        # 销毁 handle
        success = state_context.handle_manager.destroy_handle(filter_id)
        if success:
            logger.info(f"[DestroyFilter] Destroyed filterfunc: {filter_id}")
        else:
            logger.warning(f"[DestroyFilter] filterfunc not found: {filter_id}")

        return None
```

**Step 2: 验证语法**

Run: `python -c "from src.jass_runner.natives.boolexpr_natives import DestroyCondition, DestroyFilter; print('OK')"`
Expected: `OK`

**Step 3: Commit**

```bash
git add src/jass_runner/natives/boolexpr_natives.py
git commit -m "feat: 实现 DestroyCondition 和 DestroyFilter native 函数"
```

---

### Task 9: 添加 And, Or, Not natives

**Files:**
- Modify: `src/jass_runner/natives/boolexpr_natives.py`

**Step 1: 在 DestroyFilter 类后添加组合表达式 natives**

```python

class And(NativeFunction):
    """创建逻辑与表达式。"""

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "And"
        """
        return "And"

    def execute(self, state_context, operand_a: str, operand_b: str, *args, **kwargs):
        """执行 And native 函数。

        参数：
            state_context: 状态上下文，必须包含 handle_manager
            operand_a: 第一个 boolexpr 的 handle ID
            operand_b: 第二个 boolexpr 的 handle ID
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            新的 boolexpr handle ID，失败返回 None
        """
        # 检查 state_context 和 handle_manager
        if state_context is None:
            logger.error("[And] state_context is None")
            return None

        if not hasattr(state_context, 'handle_manager') or state_context.handle_manager is None:
            logger.error("[And] handle_manager not found in state_context")
            return None

        # 获取两个操作数
        expr_a = state_context.handle_manager.get_boolexpr(operand_a)
        expr_b = state_context.handle_manager.get_boolexpr(operand_b)

        if expr_a is None:
            logger.error(f"[And] operand_a not found: {operand_a}")
            return None

        if expr_b is None:
            logger.error(f"[And] operand_b not found: {operand_b}")
            return None

        # 生成唯一ID
        handle_id = f"boolexpr_{state_context.handle_manager._generate_id()}"

        # 导入 AndExpr 类
        from .handle import AndExpr

        # 创建 AndExpr 对象
        and_expr = AndExpr(handle_id, expr_a, expr_b)

        # 注册到 handle_manager
        state_context.handle_manager._register_handle(and_expr)

        logger.info(f"[And] Created boolexpr: {handle_id}")
        return handle_id


class Or(NativeFunction):
    """创建逻辑或表达式。"""

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "Or"
        """
        return "Or"

    def execute(self, state_context, operand_a: str, operand_b: str, *args, **kwargs):
        """执行 Or native 函数。

        参数：
            state_context: 状态上下文，必须包含 handle_manager
            operand_a: 第一个 boolexpr 的 handle ID
            operand_b: 第二个 boolexpr 的 handle ID
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            新的 boolexpr handle ID，失败返回 None
        """
        # 检查 state_context 和 handle_manager
        if state_context is None:
            logger.error("[Or] state_context is None")
            return None

        if not hasattr(state_context, 'handle_manager') or state_context.handle_manager is None:
            logger.error("[Or] handle_manager not found in state_context")
            return None

        # 获取两个操作数
        expr_a = state_context.handle_manager.get_boolexpr(operand_a)
        expr_b = state_context.handle_manager.get_boolexpr(operand_b)

        if expr_a is None:
            logger.error(f"[Or] operand_a not found: {operand_a}")
            return None

        if expr_b is None:
            logger.error(f"[Or] operand_b not found: {operand_b}")
            return None

        # 生成唯一ID
        handle_id = f"boolexpr_{state_context.handle_manager._generate_id()}"

        # 导入 OrExpr 类
        from .handle import OrExpr

        # 创建 OrExpr 对象
        or_expr = OrExpr(handle_id, expr_a, expr_b)

        # 注册到 handle_manager
        state_context.handle_manager._register_handle(or_expr)

        logger.info(f"[Or] Created boolexpr: {handle_id}")
        return handle_id


class Not(NativeFunction):
    """创建逻辑非表达式。"""

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "Not"
        """
        return "Not"

    def execute(self, state_context, operand: str, *args, **kwargs):
        """执行 Not native 函数。

        参数：
            state_context: 状态上下文，必须包含 handle_manager
            operand: boolexpr 的 handle ID
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            新的 boolexpr handle ID，失败返回 None
        """
        # 检查 state_context 和 handle_manager
        if state_context is None:
            logger.error("[Not] state_context is None")
            return None

        if not hasattr(state_context, 'handle_manager') or state_context.handle_manager is None:
            logger.error("[Not] handle_manager not found in state_context")
            return None

        # 获取操作数
        expr = state_context.handle_manager.get_boolexpr(operand)

        if expr is None:
            logger.error(f"[Not] operand not found: {operand}")
            return None

        # 生成唯一ID
        handle_id = f"boolexpr_{state_context.handle_manager._generate_id()}"

        # 导入 NotExpr 类
        from .handle import NotExpr

        # 创建 NotExpr 对象
        not_expr = NotExpr(handle_id, expr)

        # 注册到 handle_manager
        state_context.handle_manager._register_handle(not_expr)

        logger.info(f"[Not] Created boolexpr: {handle_id}")
        return handle_id
```

**Step 2: 验证语法**

Run: `python -c "from src.jass_runner.natives.boolexpr_natives import And, Or, Not; print('OK')"`
Expected: `OK`

**Step 3: Commit**

```bash
git add src/jass_runner/natives/boolexpr_natives.py
git commit -m "feat: 实现 And, Or, Not native 函数"
```

---

### Task 10: 添加 DestroyBoolExpr native

**Files:**
- Modify: `src/jass_runner/natives/boolexpr_natives.py`

**Step 1: 在 Not 类后添加 DestroyBoolExpr 类**

```python

class DestroyBoolExpr(NativeFunction):
    """销毁 boolexpr。"""

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "DestroyBoolExpr"
        """
        return "DestroyBoolExpr"

    def execute(self, state_context, boolexpr_id: str, *args, **kwargs):
        """执行 DestroyBoolExpr native 函数。

        参数：
            state_context: 状态上下文，必须包含 handle_manager
            boolexpr_id: 要销毁的 boolexpr ID
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            None（对应 JASS 的 nothing）
        """
        # 检查 state_context 和 handle_manager
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[DestroyBoolExpr] state_context or handle_manager not found")
            return None

        # 销毁 handle
        success = state_context.handle_manager.destroy_handle(boolexpr_id)
        if success:
            logger.info(f"[DestroyBoolExpr] Destroyed boolexpr: {boolexpr_id}")
        else:
            logger.warning(f"[DestroyBoolExpr] boolexpr not found: {boolexpr_id}")

        return None
```

**Step 2: 验证完整模块导入**

Run: `python -c "from src.jass_runner.natives.boolexpr_natives import Condition, Filter, DestroyCondition, DestroyFilter, And, Or, Not, DestroyBoolExpr; print('All imports OK')"`
Expected: `All imports OK`

**Step 3: Commit**

```bash
git add src/jass_runner/natives/boolexpr_natives.py
git commit -m "feat: 实现 DestroyBoolExpr native 函数"
```

---

### Task 11: 在 NativeFactory 中注册新的 native 函数

**Files:**
- Modify: `src/jass_runner/natives/factory.py`

**Step 1: 添加导入语句**

在文件顶部的导入区域，添加：

```python
from .boolexpr_natives import (
    Condition,
    Filter,
    DestroyCondition,
    DestroyFilter,
    And,
    Or,
    Not,
    DestroyBoolExpr,
)
```

**Step 2: 在 create_default_registry 方法中注册 natives**

在文件末尾 `return registry` 之前添加：

```python
        # 注册布尔表达式相关 native 函数
        registry.register(Condition())
        registry.register(Filter())
        registry.register(DestroyCondition())
        registry.register(DestroyFilter())
        registry.register(And())
        registry.register(Or())
        registry.register(Not())
        registry.register(DestroyBoolExpr())
```

**Step 3: 验证语法**

Run: `python -c "from src.jass_runner.natives.factory import NativeFactory; print('OK')"`
Expected: `OK`

**Step 4: Commit**

```bash
git add src/jass_runner/natives/factory.py
git commit -m "feat: 在 NativeFactory 中注册布尔表达式相关 native 函数"
```

---

### Task 12: 运行所有测试验证

**Files:**
- 无（仅运行测试）

**Step 1: 运行完整测试套件**

Run: `pytest tests/ -v --tb=short`
Expected: 所有测试通过

**Step 2: 如果测试失败，修复问题**

根据错误信息修复代码。

**Step 3: Commit（如有修改）**

```bash
git add -A
git commit -m "fix: 修复测试中发现的问题"
```

---

### Task 13: 创建示例脚本验证功能

**Files:**
- Create: `examples/boolexpr_demo.py`

**Step 1: 创建示例脚本**

```python
"""布尔表达式 native 函数演示。

此脚本演示 Condition、Filter、And、Or、Not 等 native 函数的使用。
"""

import sys
import os

# 添加 src 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from jass_runner.natives.factory import NativeFactory
from jass_runner.natives.manager import HandleManager


class MockStateContext:
    """模拟状态上下文。"""

    def __init__(self):
        self.handle_manager = HandleManager()


def test_condition():
    """测试 Condition native。"""
    print("=== 测试 Condition ===")

    ctx = MockStateContext()
    condition_native = NativeFactory().create_default_registry().get_native("Condition")

    # 定义条件函数
    def my_condition():
        return True

    # 创建 conditionfunc
    condition_id = condition_native.execute(ctx, my_condition)
    print(f"Created conditionfunc: {condition_id}")

    # 验证可以获取并执行
    condition = ctx.handle_manager.get_boolexpr(condition_id)
    result = condition.evaluate()
    print(f"Condition evaluate: {result}")

    # 销毁
    destroy_native = NativeFactory().create_default_registry().get_native("DestroyCondition")
    destroy_native.execute(ctx, condition_id)
    print(f"Destroyed conditionfunc: {condition_id}")


def test_filter():
    """测试 Filter native。"""
    print("\n=== 测试 Filter ===")

    ctx = MockStateContext()
    filter_native = NativeFactory().create_default_registry().get_native("Filter")

    # 定义过滤函数
    def my_filter(unit):
        return unit is not None

    # 创建 filterfunc
    filter_id = filter_native.execute(ctx, my_filter)
    print(f"Created filterfunc: {filter_id}")

    # 销毁
    destroy_native = NativeFactory().create_default_registry().get_native("DestroyFilter")
    destroy_native.execute(ctx, filter_id)
    print(f"Destroyed filterfunc: {filter_id}")


def test_and_or_not():
    """测试 And、Or、Not natives。"""
    print("\n=== 测试 And、Or、Not ===")

    ctx = MockStateContext()
    registry = NativeFactory().create_default_registry()

    condition_native = registry.get_native("Condition")
    and_native = registry.get_native("And")
    or_native = registry.get_native("Or")
    not_native = registry.get_native("Not")

    # 创建两个条件
    def condition_true():
        return True

    def condition_false():
        return False

    cond_true_id = condition_native.execute(ctx, condition_true)
    cond_false_id = condition_native.execute(ctx, condition_false)

    print(f"Created condition_true: {cond_true_id}")
    print(f"Created condition_false: {cond_false_id}")

    # 测试 And
    and_id = and_native.execute(ctx, cond_true_id, cond_false_id)
    and_expr = ctx.handle_manager.get_boolexpr(and_id)
    print(f"And(True, False) = {and_expr.evaluate()}")  # 应为 False

    # 测试 Or
    or_id = or_native.execute(ctx, cond_true_id, cond_false_id)
    or_expr = ctx.handle_manager.get_boolexpr(or_id)
    print(f"Or(True, False) = {or_expr.evaluate()}")  # 应为 True

    # 测试 Not
    not_id = not_native.execute(ctx, cond_true_id)
    not_expr = ctx.handle_manager.get_boolexpr(not_id)
    print(f"Not(True) = {not_expr.evaluate()}")  # 应为 False

    # 清理
    destroy_bool_expr = registry.get_native("DestroyBoolExpr")
    destroy_bool_expr.execute(ctx, and_id)
    destroy_bool_expr.execute(ctx, or_id)
    destroy_bool_expr.execute(ctx, not_id)
    print("Cleaned up boolexpr objects")


if __name__ == "__main__":
    test_condition()
    test_filter()
    test_and_or_not()
    print("\n=== 所有测试完成 ===")
```

**Step 2: 运行示例**

Run: `python examples/boolexpr_demo.py`
Expected: 输出测试通过信息

**Step 3: Commit**

```bash
git add examples/boolexpr_demo.py
git commit -m "feat: 添加布尔表达式 native 函数演示脚本"
```

---

## 完成总结

实现完成后，代码库将包含：

1. **Handle 类型**: BoolExpr, ConditionFunc, FilterFunc, AndExpr, OrExpr, NotExpr
2. **Native 函数**: Condition, Filter, DestroyCondition, DestroyFilter, And, Or, Not, DestroyBoolExpr
3. **HandleManager 扩展**: get_boolexpr 方法
4. **演示脚本**: examples/boolexpr_demo.py

所有代码遵循现有代码风格，使用中文注释。
