# RemoveUnit Native 函数实施计划

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现 `RemoveUnit` native 函数，用于立即移除单位而不触发死亡事件。

**Architecture:** 参考现有的 `KillUnit` 和 `RemoveItem` 实现，在 `basic.py` 中添加 `RemoveUnit` 类，通过 `HandleManager.destroy_handle()` 销毁单位，并在 `NativeFactory` 中注册。

**Tech Stack:** Python 3.8+, pytest, 项目自定义的 NativeFunction 框架

---

## 文件结构

| 文件 | 操作 | 说明 |
|------|------|------|
| `src/jass_runner/natives/basic.py` | 修改 | 添加 `RemoveUnit` 类（放在 `KillUnit` 类之后） |
| `src/jass_runner/natives/factory.py` | 修改 | 导入并注册 `RemoveUnit` 类 |
| `tests/natives/test_basic.py` | 修改 | 添加 `RemoveUnit` 的单元测试 |

---

## Chunk 1: 实现 RemoveUnit 类

### Task 1: 添加 RemoveUnit 类到 basic.py

**Files:**
- 修改: `src/jass_runner/natives/basic.py:93-95`（在 KillUnit 类之后，CreateUnit 类之前）

- [ ] **Step 1: 编写 RemoveUnit 类**

```python
class RemoveUnit(NativeFunction):
    """立即移除一个单位，不触发死亡事件。

    此函数模拟JASS中的RemoveUnit native函数，通过HandleManager立即销毁单位。
    与KillUnit不同，RemoveUnit不会触发任何死亡事件。
    """

    @property
    def name(self) -> str:
        """获取函数名称。

        返回：
            函数名称"RemoveUnit"
        """
        return "RemoveUnit"

    def execute(self, state_context, unit: Unit):
        """执行RemoveUnit native函数。

        参数：
            state_context: 状态上下文
            unit: Unit对象（由CreateUnit返回）

        返回：
            bool: 成功移除单位返回True，否则返回False
        """
        if unit is None:
            logger.warning("[RemoveUnit] 尝试移除None单位")
            return False

        # 通过HandleManager销毁单位
        handle_manager = state_context.handle_manager
        success = handle_manager.destroy_handle(unit.id)

        if success:
            logger.info(f"[RemoveUnit] 单位{unit.id}已被移除")
        else:
            logger.warning(f"[RemoveUnit] 单位{unit.id}不存在或已被移除")

        return success
```

- [ ] **Step 2: 验证代码格式**

运行: `flake8 src/jass_runner/natives/basic.py`
Expected: 无错误，或通过

- [ ] **Step 3: Commit**

```bash
git add src/jass_runner/natives/basic.py
git commit -m "feat(natives): 添加 RemoveUnit native 函数实现"
```

---

## Chunk 2: 注册 RemoveUnit 函数

### Task 2: 在 factory.py 中导入和注册 RemoveUnit

**Files:**
- 修改: `src/jass_runner/natives/factory.py:7`（修改导入语句）
- 修改: `src/jass_runner/natives/factory.py:188-194`（在基础 native 函数注册区域添加）

- [ ] **Step 1: 修改导入语句**

将第7行从：
```python
from .basic import DisplayTextToPlayer, KillUnit, CreateUnit, GetUnitState, CreateItem, RemoveItem, PlayerNative, GetLocalPlayer
```

改为：
```python
from .basic import DisplayTextToPlayer, KillUnit, RemoveUnit, CreateUnit, GetUnitState, CreateItem, RemoveItem, PlayerNative, GetLocalPlayer
```

- [ ] **Step 2: 注册 RemoveUnit 函数**

在第192行（`registry.register(RemoveItem())`）之后添加：
```python
        registry.register(RemoveUnit())
```

- [ ] **Step 3: 验证导入和语法**

运行: `python -c "from jass_runner.natives.factory import NativeFactory; print('Import OK')"`
Expected: `Import OK`

- [ ] **Step 4: Commit**

```bash
git add src/jass_runner/natives/factory.py
git commit -m "feat(natives): 在 NativeFactory 中注册 RemoveUnit 函数"
```

---

## Chunk 3: 编写单元测试

### Task 3: 添加 RemoveUnit 单元测试

**Files:**
- 修改: `tests/natives/test_basic.py`（在文件末尾添加测试函数）

- [ ] **Step 1: 导入 RemoveUnit**

将第4-7行的导入语句从：
```python
from jass_runner.natives.basic import (
    DisplayTextToPlayer, KillUnit, CreateUnit, GetUnitState, PlayerNative,
    UNIT_STATE_LIFE, UNIT_STATE_MANA
)
```

改为：
```python
from jass_runner.natives.basic import (
    DisplayTextToPlayer, KillUnit, RemoveUnit, CreateUnit, GetUnitState, PlayerNative,
    UNIT_STATE_LIFE, UNIT_STATE_MANA
)
```

- [ ] **Step 2: 添加 test_remove_unit 测试函数**

在文件末尾（第227行之后）添加：

```python

def test_remove_unit(state_context):
    """测试RemoveUnit原生函数。"""
    from jass_runner.natives.handle import Unit

    native = RemoveUnit()
    assert native.name == "RemoveUnit"

    # 先创建一个单位
    unit = state_context.handle_manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)

    # 测试移除存在的单位
    result = native.execute(state_context, unit)
    assert result is True

    # 验证单位已被销毁
    retrieved_unit = state_context.handle_manager.get_unit(unit.id)
    assert retrieved_unit is None or not retrieved_unit.is_alive()

    # 测试使用None单位
    result = native.execute(state_context, None)
    assert result is False


def test_remove_unit_already_removed(state_context):
    """测试重复移除已移除的单位。"""
    native = RemoveUnit()

    # 创建一个单位
    unit = state_context.handle_manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)

    # 第一次移除
    result = native.execute(state_context, unit)
    assert result is True

    # 第二次移除（单位已不存在）
    result = native.execute(state_context, unit)
    assert result is False


def test_remove_unit_vs_kill_unit(state_context):
    """测试RemoveUnit和KillUnit的区别。"""
    remove_native = RemoveUnit()
    kill_native = KillUnit()

    # 创建两个单位
    unit1 = state_context.handle_manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)
    unit2 = state_context.handle_manager.create_unit("hkni", 0, 10.0, 10.0, 0.0)

    # 使用RemoveUnit移除第一个单位
    result1 = remove_native.execute(state_context, unit1)
    assert result1 is True
    assert state_context.handle_manager.get_unit(unit1.id) is None

    # 使用KillUnit击杀第二个单位
    result2 = kill_native.execute(state_context, unit2)
    assert result2 is True
    assert state_context.handle_manager.get_unit(unit2.id) is None
```

- [ ] **Step 3: 运行测试验证**

运行: `pytest tests/natives/test_basic.py::test_remove_unit -v`
Expected: PASS

运行: `pytest tests/natives/test_basic.py::test_remove_unit_already_removed -v`
Expected: PASS

运行: `pytest tests/natives/test_basic.py::test_remove_unit_vs_kill_unit -v`
Expected: PASS

- [ ] **Step 4: 运行所有 basic 测试确保无回归**

运行: `pytest tests/natives/test_basic.py -v`
Expected: 所有测试 PASS

- [ ] **Step 5: Commit**

```bash
git add tests/natives/test_basic.py
git commit -m "test(natives): 添加 RemoveUnit 单元测试"
```

---

## 验证清单

实施完成后，请确认以下事项：

- [ ] `RemoveUnit` 类已添加到 `basic.py`
- [ ] `RemoveUnit` 已在 `factory.py` 中导入和注册
- [ ] 所有单元测试通过
- [ ] `flake8` 代码检查通过
- [ ] 三次提交已完成

## 日志输出示例

成功实施后的日志输出应如下：

```
[RemoveUnit] 单位 unit_123 已被移除
[RemoveUnit] 尝试移除None单位
[RemoveUnit] 单位 unit_123 不存在或已被移除
```
