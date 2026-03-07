# TriggerExecute Native 函数实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现 `TriggerExecute` native 函数，用于手动执行触发器中已添加的所有 action，不评估条件。

**Architecture:** 采用简单委托模式，在 `TriggerExecute` 中直接调用 `trigger.execute_actions(state_context)`，复用 Trigger 类现有的 `execute_actions` 方法。

**Tech Stack:** Python 3.8+, pytest, unittest.mock

---

### Task 1: 编写 TriggerExecute 的单元测试

**Files:**
- Modify: `tests/natives/test_trigger_natives_unit.py`

**Step 1: 编写测试代码**

在文件末尾添加 `TestTriggerExecute` 测试类：

```python
class TestTriggerExecute:
    """测试 TriggerExecute 原生函数。"""

    def test_execute_trigger_returns_none(self, mock_state_context):
        """测试 TriggerExecute 成功时返回None。"""
        from jass_runner.natives.trigger_natives import TriggerExecute

        mock_trigger = MagicMock()
        mock_state_context.trigger_manager.get_trigger.return_value = mock_trigger

        native = TriggerExecute()
        assert native.name == "TriggerExecute"

        result = native.execute(mock_state_context, "trigger_0")

        assert result is None
        mock_state_context.trigger_manager.get_trigger.assert_called_once_with("trigger_0")
        mock_trigger.execute_actions.assert_called_once_with(mock_state_context)

    def test_execute_trigger_invalid_trigger(self, mock_state_context):
        """测试执行不存在的触发器返回None。"""
        from jass_runner.natives.trigger_natives import TriggerExecute

        mock_state_context.trigger_manager.get_trigger.return_value = None

        native = TriggerExecute()
        result = native.execute(mock_state_context, "trigger_invalid")

        assert result is None

    def test_execute_trigger_without_trigger_manager(self, mock_state_context):
        """测试没有trigger_manager时执行触发器返回None。"""
        from jass_runner.natives.trigger_natives import TriggerExecute

        delattr(mock_state_context, 'trigger_manager')

        native = TriggerExecute()
        result = native.execute(mock_state_context, "trigger_0")

        assert result is None
```

**Step 2: 运行测试验证失败**

Run: `pytest tests/natives/test_trigger_natives_unit.py::TestTriggerExecute -v`
Expected: FAIL with "ImportError: cannot import name 'TriggerExecute'"

**Step 3: Commit**

```bash
git add tests/natives/test_trigger_natives_unit.py
git commit -m "test(trigger): 添加 TriggerExecute 单元测试"
```

---

### Task 2: 实现 TriggerExecute Native 函数

**Files:**
- Modify: `src/jass_runner/natives/trigger_natives.py`

**Step 1: 在 TriggerClearEvents 类后添加 TriggerExecute 类**

```python
class TriggerExecute(NativeFunction):
    """手动执行触发器动作的原生函数。

    获取触发器并调用其execute_actions方法执行所有动作。
    注意：此函数不评估条件，直接执行所有动作。
    """

    @property
    def name(self) -> str:
        """获取native函数的名称。

        返回：
            "TriggerExecute"
        """
        return "TriggerExecute"

    def execute(self, state_context, trigger_id: str, *args, **kwargs):
        """执行 TriggerExecute 原生函数。

        参数：
            state_context: 状态上下文，必须包含trigger_manager
            trigger_id: 要执行的触发器ID
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            None（对应JASS的nothing返回类型）
        """
        # 检查state_context和trigger_manager存在性
        if state_context is None or not hasattr(state_context, 'trigger_manager'):
            logger.error("[TriggerExecute] state_context or trigger_manager not found")
            return None

        # 获取触发器
        trigger = state_context.trigger_manager.get_trigger(trigger_id)
        if trigger is None:
            logger.warning(f"[TriggerExecute] Trigger not found: {trigger_id}")
            return None

        # 执行所有动作
        trigger.execute_actions(state_context)
        logger.info(f"[TriggerExecute] Executed trigger: {trigger_id}")

        # 始终返回None（nothing）
        return None
```

**Step 2: 运行单元测试验证通过**

Run: `pytest tests/natives/test_trigger_natives_unit.py::TestTriggerExecute -v`
Expected: PASS (3 tests passed)

**Step 3: Commit**

```bash
git add src/jass_runner/natives/trigger_natives.py
git commit -m "feat(trigger): 实现 TriggerExecute native函数"
```

---

### Task 3: 在 NativeFactory 中注册 TriggerExecute

**Files:**
- Modify: `src/jass_runner/natives/factory.py`

**Step 1: 修改 import 语句**

在文件顶部找到 `from .trigger_natives import (` 部分，在 `TriggerClearEvents,` 后添加 `TriggerExecute,`：

```python
from .trigger_natives import (
    CreateTrigger,
    DestroyTrigger,
    EnableTrigger,
    DisableTrigger,
    IsTriggerEnabled,
    TriggerAddAction,
    TriggerRemoveAction,
    TriggerClearActions,
    TriggerAddCondition,
    TriggerRemoveCondition,
    TriggerClearConditions,
    TriggerEvaluate,
    TriggerClearEvents,
    TriggerExecute,  # 添加这一行
)
```

**Step 2: 在 create_default_registry 方法中注册**

找到 `# 注册触发器事件管理native函数` 部分，在 `registry.register(TriggerClearEvents())` 后添加：

```python
# 注册触发器事件管理native函数
registry.register(TriggerClearEvents())
registry.register(TriggerExecute())  # 添加这一行
```

**Step 3: 运行单元测试确保没有破坏现有功能**

Run: `pytest tests/natives/test_trigger_natives_unit.py -v`
Expected: PASS (所有现有测试 + 新增测试都通过)

**Step 4: Commit**

```bash
git add src/jass_runner/natives/factory.py
git commit -m "feat(trigger): 在 NativeFactory 中注册 TriggerExecute"
```

---

### Task 4: 编写集成测试

**Files:**
- Modify: `tests/integration/test_trigger_natives.py`

**Step 1: 在 TestTriggerNativesIntegration 类中添加测试方法**

```python
    def test_trigger_execute_native_integration(self, state_context, registry):
        """测试手动执行触发器动作。

        验证流程：
        1. 创建触发器
        2. 使用TriggerAddAction添加动作
        3. 使用TriggerExecute手动执行触发器
        4. 验证动作被执行
        """
        # 准备
        create_trigger = registry.get("CreateTrigger")
        add_action = registry.get("TriggerAddAction")
        execute_trigger = registry.get("TriggerExecute")

        trigger_id = create_trigger.execute(state_context)

        # 标记动作执行次数
        action_executed = []

        def action_func(state_context):
            action_executed.append(True)

        # 添加动作
        add_action.execute(state_context, trigger_id, action_func)

        # 执行：手动执行触发器
        result = execute_trigger.execute(state_context, trigger_id)

        # 验证
        assert result is None, "TriggerExecute应该返回None"
        assert len(action_executed) == 1, "动作应该被执行一次"

    def test_trigger_execute_with_multiple_actions(self, state_context, registry):
        """测试TriggerExecute执行多个动作。

        验证流程：
        1. 创建触发器
        2. 添加多个动作
        3. 执行触发器
        4. 验证所有动作都被执行
        """
        # 准备
        create_trigger = registry.get("CreateTrigger")
        add_action = registry.get("TriggerAddAction")
        execute_trigger = registry.get("TriggerExecute")

        trigger_id = create_trigger.execute(state_context)

        # 标记动作执行顺序
        execution_order = []

        def action_func_1(state_context):
            execution_order.append(1)

        def action_func_2(state_context):
            execution_order.append(2)

        def action_func_3(state_context):
            execution_order.append(3)

        # 添加多个动作
        add_action.execute(state_context, trigger_id, action_func_1)
        add_action.execute(state_context, trigger_id, action_func_2)
        add_action.execute(state_context, trigger_id, action_func_3)

        # 执行
        execute_trigger.execute(state_context, trigger_id)

        # 验证
        assert execution_order == [1, 2, 3], "动作应该按添加顺序执行"

    def test_trigger_execute_does_not_evaluate_conditions(self, state_context, registry):
        """测试TriggerExecute不评估条件直接执行动作。

        验证流程：
        1. 创建触发器
        2. 添加返回False的条件
        3. 添加动作
        4. 执行TriggerExecute
        5. 验证动作仍然被执行（不评估条件）
        """
        # 准备
        create_trigger = registry.get("CreateTrigger")
        add_action = registry.get("TriggerAddAction")
        add_condition = registry.get("TriggerAddCondition")
        execute_trigger = registry.get("TriggerExecute")

        trigger_id = create_trigger.execute(state_context)

        action_executed = []

        def action_func(state_context):
            action_executed.append(True)

        def false_condition(state_context):
            return False

        # 添加条件和动作
        add_condition.execute(state_context, trigger_id, false_condition)
        add_action.execute(state_context, trigger_id, action_func)

        # 执行
        execute_trigger.execute(state_context, trigger_id)

        # 验证：即使条件为False，动作仍然被执行
        assert len(action_executed) == 1, "TriggerExecute应该不评估条件直接执行动作"
```

**Step 2: 运行集成测试验证通过**

Run: `pytest tests/integration/test_trigger_natives.py -v`
Expected: PASS (所有集成测试通过)

**Step 3: Commit**

```bash
git add tests/integration/test_trigger_natives.py
git commit -m "test(trigger): 添加 TriggerExecute 集成测试"
```

---

### Task 5: 运行完整测试套件验证

**Step 1: 运行所有相关测试**

Run: `pytest tests/natives/test_trigger_natives_unit.py tests/integration/test_trigger_natives.py -v`
Expected: PASS (所有测试通过)

**Step 2: 运行整体测试确保没有回归**

Run: `pytest tests/ -v --tb=short`
Expected: PASS (所有测试通过)

**Step 3: 最终提交**

```bash
git log --oneline -5  # 查看提交历史
```

---

## 实现要点总结

1. **TriggerExecute 不评估条件**：直接调用 `trigger.execute_actions(state_context)`，与 `TriggerEvaluate`（仅评估条件）形成互补
2. **返回类型**：始终返回 `None`（对应 JASS 的 `nothing`）
3. **错误处理**：触发器不存在时记录 warning 日志，不抛出异常
4. **日志输出**：执行成功时记录 info 日志，包含触发器 ID
