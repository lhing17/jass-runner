# 特效系统实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现极简日志方案的特效系统，支持 5 个核心 native 函数

**Architecture:** 在现有 Handle 体系中添加 Effect 类，通过 HandleManager 管理特效生命周期，Native 函数仅输出日志不保存复杂状态

**Tech Stack:** Python 3.8+, pytest, 项目既有 Native 函数框架

---

## 前置准备

确保已阅读：
- `docs/plans/2026-03-03-effect-system-design.md` - 设计文档
- `src/jass_runner/natives/handle.py` - 现有 Handle 类体系
- `src/jass_runner/natives/manager.py` - HandleManager 实现
- `src/jass_runner/natives/item_inventory_natives.py` - 参考实现示例

---

## Task 1: 添加 Effect Handle 类

**Files:**
- Modify: `src/jass_runner/natives/handle.py`
- Test: `tests/natives/test_effect_handle.py`

**Step 1: 编写 Effect 类测试**

```python
def test_effect_creation():
    """测试 Effect 类创建。"""
    from src.jass_runner.natives.handle import Effect

    effect = Effect(1, "Abilities\\Spells\\Human\\Thunderclap\\ThunderclapCaster.mdl",
                    target=(100.0, 200.0, 0.0))

    assert effect.id == 1
    assert effect.type_name == "effect"
    assert effect.model_path == "Abilities\\Spells\\Human\\Thunderclap\\ThunderclapCaster.mdl"
    assert effect.target == (100.0, 200.0, 0.0)
    assert effect.attach_point is None
    assert effect.alive is True
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/natives/test_effect_handle.py::test_effect_creation -v
```

Expected: FAIL - "Effect not defined"

**Step 3: 实现 Effect 类**

在 `src/jass_runner/natives/handle.py` 中，在 `Rect` 类之后添加：

```python
class Effect(Handle):
    """特效句柄，用于标识一个已创建的特效。"""

    def __init__(self, effect_id: int, model_path: str,
                 target: Optional[Union[Unit, Item, Tuple[float, float, float]]] = None,
                 attach_point: Optional[str] = None):
        """初始化特效句柄。

        参数：
            effect_id: 特效唯一标识符
            model_path: 模型路径（原样保存）
            target: 绑定目标，可以是单位、物品或坐标三元组
            attach_point: 附着点名称（如 "hand", "origin"）
        """
        super().__init__(effect_id, "effect")
        self.model_path = model_path
        self.target = target
        self.attach_point = attach_point
```

确保导入 `Optional`, `Union`, `Tuple` 等类型提示。

**Step 4: 运行测试确认通过**

```bash
pytest tests/natives/test_effect_handle.py::test_effect_creation -v
```

Expected: PASS

**Step 5: 添加更多测试并提交**

```python
def test_effect_with_unit_target():
    """测试绑定到单位的特效。"""
    from src.jass_runner.natives.handle import Effect, Unit

    unit = Unit(1, 'hfoo')  # 步兵
    effect = Effect(2, "Abilities\\Spells\\Orc\\Bloodlust\\BloodlustTarget.mdl",
                    target=unit, attach_point="hand")

    assert effect.target == unit
    assert effect.attach_point == "hand"
```

```bash
git add tests/natives/test_effect_handle.py src/jass_runner/natives/handle.py
git commit -m "feat(handle): 添加 Effect 类"
```

---

## Task 2: 在 HandleManager 中添加特效生命周期管理

**Files:**
- Modify: `src/jass_runner/natives/manager.py`
- Test: `tests/natives/test_handle_manager_effect.py`

**Step 1: 编写测试**

```python
def test_create_effect():
    """测试创建特效。"""
    from src.jass_runner.natives.manager import HandleManager

    manager = HandleManager()
    effect = manager.create_effect("Abilities\\Spells\\Human\\Thunderclap\\ThunderclapCaster.mdl",
                                    100.0, 200.0, 0.0)

    assert effect is not None
    assert effect.type_name == "effect"
    assert effect.model_path == "Abilities\\Spells\\Human\\Thunderclap\\ThunderclapCaster.mdl"
    assert effect.target == (100.0, 200.0, 0.0)
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/natives/test_handle_manager_effect.py::test_create_effect -v
```

Expected: FAIL - "create_effect not defined"

**Step 3: 实现 create_effect 方法**

在 `src/jass_runner/natives/manager.py` 中，在 `create_rect` 方法后添加：

```python
def create_effect(self, model_path: str, x: float, y: float, z: float) -> 'Effect':
    """在指定坐标创建特效。

    参数：
        model_path: 模型路径
        x: X 坐标
        y: Y 坐标
        z: Z 坐标

    返回：
        创建的 Effect 对象
    """
    from .handle import Effect
    effect_id = self._next_id
    self._next_id += 1
    effect = Effect(effect_id, model_path, target=(x, y, z))
    self._handles[effect_id] = effect
    logger.info(f"[特效] 在 ({x}, {y}, {z}) 创建特效: {model_path} (ID: {effect_id})")
    return effect
```

**Step 4: 运行测试确认通过**

```bash
pytest tests/natives/test_handle_manager_effect.py::test_create_effect -v
```

Expected: PASS

**Step 5: 实现 create_effect_target 方法**

```python
def test_create_effect_target():
    """测试在目标上创建特效。"""
    from src.jass_runner.natives.manager import HandleManager

    manager = HandleManager()
    unit = manager.create_unit(0, 'hfoo', 0.0, 0.0, 0.0)

    effect = manager.create_effect_target(
        "Abilities\\Spells\\Orc\\Bloodlust\\BloodlustTarget.mdl",
        unit, "hand"
    )

    assert effect.target == unit
    assert effect.attach_point == "hand"
```

实现代码：

```python
def create_effect_target(self, model_path: str, target: Union['Unit', 'Item'],
                         attach_point: str) -> 'Effect':
    """在目标对象指定附着点创建特效。

    参数：
        model_path: 模型路径
        target: 目标单位或物品
        attach_point: 附着点名称

    返回：
        创建的 Effect 对象
    """
    from .handle import Effect
    effect_id = self._next_id
    self._next_id += 1
    effect = Effect(effect_id, model_path, target=target, attach_point=attach_point)
    self._handles[effect_id] = effect
    logger.info(f"[特效] 在 [{target.type_name}#{target.id}] 的附着点 [{attach_point}] "
                f"创建特效: {model_path} (ID: {effect_id})")
    return effect
```

**Step 6: 实现 destroy_effect 方法并提交**

```python
def test_destroy_effect():
    """测试销毁特效。"""
    from src.jass_runner.natives.manager import HandleManager

    manager = HandleManager()
    effect = manager.create_effect("test.mdl", 0.0, 0.0, 0.0)

    result = manager.destroy_effect(effect)

    assert result is True
    assert effect.alive is False
```

实现代码：

```python
def destroy_effect(self, effect: 'Effect') -> bool:
    """销毁特效。

    参数：
        effect: 要销毁的特效对象

    返回：
        成功销毁返回 True，否则返回 False
    """
    if effect is None or not effect.alive:
        logger.warning(f"[特效] 尝试销毁不存在的特效 (ID: {effect.id if effect else 'None'})")
        return False

    effect.alive = False
    logger.info(f"[特效] 销毁特效 (ID: {effect.id})")
    return True
```

```bash
git add tests/natives/test_handle_manager_effect.py src/jass_runner/natives/manager.py
git commit -m "feat(manager): 添加特效生命周期管理方法"
```

---

## Task 3: 实现 AddSpecialEffect Native 函数

**Files:**
- Create: `src/jass_runner/natives/effect_natives.py`
- Test: `tests/natives/test_effect_natives.py`

**Step 1: 编写测试**

```python
def test_add_special_effect():
    """测试 AddSpecialEffect native 函数。"""
    from src.jass_runner.natives.effect_natives import AddSpecialEffect
    from src.jass_runner.natives.state import StateContext
    from src.jass_runner.natives.manager import HandleManager

    handle_manager = HandleManager()
    state_context = StateContext(handle_manager)
    native = AddSpecialEffect()

    result = native.execute(state_context, "Abilities\\Spells\\Human\\Thunderclap\\ThunderclapCaster.mdl",
                           100.0, 200.0)

    assert result is not None
    assert result.type_name == "effect"
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/natives/test_effect_natives.py::test_add_special_effect -v
```

Expected: FAIL - "effect_natives not found"

**Step 3: 实现 AddSpecialEffect 类**

创建 `src/jass_runner/natives/effect_natives.py`：

```python
"""特效相关 native 函数实现。"""

import logging
from typing import TYPE_CHECKING

from .base import NativeFunction

if TYPE_CHECKING:
    from .state import StateContext
    from .handle import Effect, Unit, Item

logger = logging.getLogger(__name__)


class AddSpecialEffect(NativeFunction):
    """在指定坐标创建特效。"""

    @property
    def name(self) -> str:
        return "AddSpecialEffect"

    def execute(self, state_context: 'StateContext', model_path: str,
                x: float, y: float) -> 'Effect':
        """执行 AddSpecialEffect native 函数。

        参数：
            state_context: 状态上下文
            model_path: 模型路径
            x: X 坐标
            y: Y 坐标

        返回：
            创建的 Effect 对象
        """
        handle_manager = state_context.handle_manager
        return handle_manager.create_effect(model_path, x, y, 0.0)
```

**Step 4: 运行测试确认通过**

```bash
pytest tests/natives/test_effect_natives.py::test_add_special_effect -v
```

Expected: PASS

**Step 5: 提交**

```bash
git add tests/natives/test_effect_natives.py src/jass_runner/natives/effect_natives.py
git commit -m "feat(natives): 实现 AddSpecialEffect native 函数"
```

---

## Task 4: 实现 AddSpecialEffectTarget Native 函数

**Files:**
- Modify: `src/jass_runner/natives/effect_natives.py`
- Test: `tests/natives/test_effect_natives.py`

**Step 1: 编写测试**

```python
def test_add_special_effect_target():
    """测试 AddSpecialEffectTarget native 函数。"""
    from src.jass_runner.natives.effect_natives import AddSpecialEffectTarget
    from src.jass_runner.natives.state import StateContext
    from src.jass_runner.natives.manager import HandleManager

    handle_manager = HandleManager()
    state_context = StateContext(handle_manager)
    native = AddSpecialEffectTarget()

    unit = handle_manager.create_unit(0, 'hfoo', 0.0, 0.0, 0.0)
    result = native.execute(state_context,
                           "Abilities\\Spells\\Orc\\Bloodlust\\BloodlustTarget.mdl",
                           unit, "hand")

    assert result is not None
    assert result.target == unit
    assert result.attach_point == "hand"
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/natives/test_effect_natives.py::test_add_special_effect_target -v
```

Expected: FAIL

**Step 3: 实现 AddSpecialEffectTarget 类**

在 `effect_natives.py` 中添加：

```python
class AddSpecialEffectTarget(NativeFunction):
    """在目标对象指定附着点创建特效。"""

    @property
    def name(self) -> str:
        return "AddSpecialEffectTarget"

    def execute(self, state_context: 'StateContext', model_path: str,
                target: Union['Unit', 'Item'], attach_point: str) -> 'Effect':
        """执行 AddSpecialEffectTarget native 函数。

        参数：
            state_context: 状态上下文
            model_path: 模型路径
            target: 目标单位或物品
            attach_point: 附着点名称

        返回：
            创建的 Effect 对象
        """
        handle_manager = state_context.handle_manager
        return handle_manager.create_effect_target(model_path, target, attach_point)
```

**Step 4: 运行测试确认通过**

```bash
pytest tests/natives/test_effect_natives.py::test_add_special_effect_target -v
```

Expected: PASS

**Step 5: 提交**

```bash
git add tests/natives/test_effect_natives.py src/jass_runner/natives/effect_natives.py
git commit -m "feat(natives): 实现 AddSpecialEffectTarget native 函数"
```

---

## Task 5: 实现 DestroyEffect Native 函数

**Files:**
- Modify: `src/jass_runner/natives/effect_natives.py`
- Test: `tests/natives/test_effect_natives.py`

**Step 1: 编写测试**

```python
def test_destroy_effect():
    """测试 DestroyEffect native 函数。"""
    from src.jass_runner.natives.effect_natives import DestroyEffect
    from src.jass_runner.natives.state import StateContext
    from src.jass_runner.natives.manager import HandleManager

    handle_manager = HandleManager()
    state_context = StateContext(handle_manager)
    native = DestroyEffect()

    effect = handle_manager.create_effect("test.mdl", 0.0, 0.0, 0.0)
    result = native.execute(state_context, effect)

    assert result is True
    assert effect.alive is False
```

**Step 2: 运行测试确认失败**

**Step 3: 实现 DestroyEffect 类**

```python
class DestroyEffect(NativeFunction):
    """销毁特效。"""

    @property
    def name(self) -> str:
        return "DestroyEffect"

    def execute(self, state_context: 'StateContext', effect: 'Effect') -> bool:
        """执行 DestroyEffect native 函数。

        参数：
            state_context: 状态上下文
            effect: 要销毁的特效对象

        返回：
            成功销毁返回 True，否则返回 False
        """
        handle_manager = state_context.handle_manager
        return handle_manager.destroy_effect(effect)
```

**Step 4: 运行测试确认通过并提交**

```bash
git add tests/natives/test_effect_natives.py src/jass_runner/natives/effect_natives.py
git commit -m "feat(natives): 实现 DestroyEffect native 函数"
```

---

## Task 6: 实现 SetSpecialEffectScale Native 函数

**Files:**
- Modify: `src/jass_runner/natives/effect_natives.py`
- Test: `tests/natives/test_effect_natives.py`

**Step 1: 编写测试**

```python
def test_set_special_effect_scale():
    """测试 SetSpecialEffectScale native 函数。"""
    from src.jass_runner.natives.effect_natives import SetSpecialEffectScale
    from src.jass_runner.natives.state import StateContext
    from src.jass_runner.natives.manager import HandleManager

    handle_manager = HandleManager()
    state_context = StateContext(handle_manager)
    native = SetSpecialEffectScale()

    effect = handle_manager.create_effect("test.mdl", 0.0, 0.0, 0.0)
    result = native.execute(state_context, effect, 1.5)

    assert result is None  # 无返回值
```

**Step 2: 实现 SetSpecialEffectScale 类**

```python
class SetSpecialEffectScale(NativeFunction):
    """设置特效缩放。"""

    @property
    def name(self) -> str:
        return "SetSpecialEffectScale"

    def execute(self, state_context: 'StateContext', effect: 'Effect',
                scale: float) -> None:
        """执行 SetSpecialEffectScale native 函数。

        参数：
            state_context: 状态上下文
            effect: 特效对象
            scale: 缩放比例
        """
        logger.info(f"[特效] 设置特效 (ID: {effect.id}) 缩放: {scale}")
```

**Step 3: 运行测试确认通过并提交**

```bash
git add tests/natives/test_effect_natives.py src/jass_runner/natives/effect_natives.py
git commit -m "feat(natives): 实现 SetSpecialEffectScale native 函数"
```

---

## Task 7: 实现 SetSpecialEffectColor Native 函数

**Files:**
- Modify: `src/jass_runner/natives/effect_natives.py`
- Test: `tests/natives/test_effect_natives.py`

**Step 1: 编写测试**

```python
def test_set_special_effect_color():
    """测试 SetSpecialEffectColor native 函数。"""
    from src.jass_runner.natives.effect_natives import SetSpecialEffectColor
    from src.jass_runner.natives.state import StateContext
    from src.jass_runner.natives.manager import HandleManager

    handle_manager = HandleManager()
    state_context = StateContext(handle_manager)
    native = SetSpecialEffectColor()

    effect = handle_manager.create_effect("test.mdl", 0.0, 0.0, 0.0)
    result = native.execute(state_context, effect, 255, 0, 0, 255)

    assert result is None
```

**Step 2: 实现 SetSpecialEffectColor 类**

```python
class SetSpecialEffectColor(NativeFunction):
    """设置特效颜色。"""

    @property
    def name(self) -> str:
        return "SetSpecialEffectColor"

    def execute(self, state_context: 'StateContext', effect: 'Effect',
                r: int, g: int, b: int, a: int) -> None:
        """执行 SetSpecialEffectColor native 函数。

        参数：
            state_context: 状态上下文
            effect: 特效对象
            r: 红色通道 (0-255)
            g: 绿色通道 (0-255)
            b: 蓝色通道 (0-255)
            a: Alpha通道 (0-255)
        """
        logger.info(f"[特效] 设置特效 (ID: {effect.id}) 颜色: RGBA({r}, {g}, {b}, {a})")
```

**Step 3: 运行测试确认通过并提交**

```bash
git add tests/natives/test_effect_natives.py src/jass_runner/natives/effect_natives.py
git commit -m "feat(natives): 实现 SetSpecialEffectColor native 函数"
```

---

## Task 8: 在 NativeFactory 中注册所有特效函数

**Files:**
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_effect_natives.py`

**Step 1: 编写集成测试**

```python
def test_all_effect_natives_registered():
    """测试所有特效 native 函数已注册。"""
    from src.jass_runner.natives.factory import NativeFactory

    registry = NativeFactory.create_default_registry()

    assert registry.get("AddSpecialEffect") is not None
    assert registry.get("AddSpecialEffectTarget") is not None
    assert registry.get("DestroyEffect") is not None
    assert registry.get("SetSpecialEffectScale") is not None
    assert registry.get("SetSpecialEffectColor") is not None
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/natives/test_effect_natives.py::test_all_effect_natives_registered -v
```

Expected: FAIL

**Step 3: 修改 factory.py 注册特效函数**

在 `src/jass_runner/natives/factory.py` 中：

1. 在文件顶部导入特效 native 函数：

```python
from .effect_natives import (
    AddSpecialEffect,
    AddSpecialEffectTarget,
    DestroyEffect,
    SetSpecialEffectScale,
    SetSpecialEffectColor,
)
```

2. 在 `create_default_registry` 方法中注册：

```python
# 特效 native 函数
registry.register(AddSpecialEffect())
registry.register(AddSpecialEffectTarget())
registry.register(DestroyEffect())
registry.register(SetSpecialEffectScale())
registry.register(SetSpecialEffectColor())
```

**Step 4: 运行测试确认通过并提交**

```bash
pytest tests/natives/test_effect_natives.py::test_all_effect_natives_registered -v
```

Expected: PASS

```bash
git add tests/natives/test_effect_natives.py src/jass_runner/natives/factory.py
git commit -m "feat(factory): 注册所有特效 native 函数"
```

---

## Task 9: 编写集成测试

**Files:**
- Create: `tests/integration/test_effect_system.py`

**Step 1: 编写完整场景测试**

```python
"""特效系统集成测试。"""

import pytest
from src.jass_runner.natives.factory import NativeFactory
from src.jass_runner.natives.state import StateContext
from src.jass_runner.natives.manager import HandleManager


class TestEffectSystem:
    """测试特效系统完整流程。"""

    def test_create_and_destroy_effect(self):
        """测试创建并销毁特效的完整流程。"""
        registry = NativeFactory.create_default_registry()
        handle_manager = HandleManager()
        state_context = StateContext(handle_manager)

        # 创建特效
        add_effect = registry.get("AddSpecialEffect")
        effect = add_effect.execute(
            state_context,
            "Abilities\\Spells\\Human\\Thunderclap\\ThunderclapCaster.mdl",
            100.0, 200.0
        )

        assert effect is not None
        assert effect.alive is True

        # 设置属性
        set_scale = registry.get("SetSpecialEffectScale")
        set_scale.execute(state_context, effect, 1.5)

        set_color = registry.get("SetSpecialEffectColor")
        set_color.execute(state_context, effect, 255, 0, 0, 255)

        # 销毁特效
        destroy = registry.get("DestroyEffect")
        result = destroy.execute(state_context, effect)

        assert result is True
        assert effect.alive is False

    def test_effect_on_unit(self):
        """测试在单位上创建特效。"""
        registry = NativeFactory.create_default_registry()
        handle_manager = HandleManager()
        state_context = StateContext(handle_manager)

        # 创建单位
        unit = handle_manager.create_unit(0, 'hfoo', 0.0, 0.0, 0.0)

        # 在单位上创建特效
        add_effect_target = registry.get("AddSpecialEffectTarget")
        effect = add_effect_target.execute(
            state_context,
            "Abilities\\Spells\\Orc\\Bloodlust\\BloodlustTarget.mdl",
            unit,
            "hand"
        )

        assert effect.target == unit
        assert effect.attach_point == "hand"
```

**Step 2: 运行所有集成测试**

```bash
pytest tests/integration/test_effect_system.py -v
```

Expected: ALL PASS

**Step 3: 提交**

```bash
git add tests/integration/test_effect_system.py
git commit -m "test(integration): 添加特效系统集成测试"
```

---

## Task 10: 更新项目笔记

**Files:**
- Modify: `PROJECT_NOTES.md`
- Modify: `TODO.md`

**Step 1: 更新 PROJECT_NOTES.md**

在合适的位置添加：

```markdown
## 特效系统

已实现极简日志方案的特效系统：
- Effect Handle 类用于标识特效
- 支持 5 个核心 native 函数：
  - AddSpecialEffect - 在坐标点创建特效
  - AddSpecialEffectTarget - 在单位/物品上创建特效
  - DestroyEffect - 销毁特效
  - SetSpecialEffectScale - 设置特效缩放（仅日志）
  - SetSpecialEffectColor - 设置特效颜色（仅日志）
- 所有操作仅输出日志，不保存复杂状态
```

**Step 2: 更新 TODO.md**

将特效系统相关任务标记为完成，或添加新的待办项。

**Step 3: 提交**

```bash
git add PROJECT_NOTES.md TODO.md
git commit -m "docs: 更新项目笔记，记录特效系统实现"
```

---

## 验证清单

完成所有任务后，运行以下命令验证：

```bash
# 运行所有特效相关测试
pytest tests/natives/test_effect_handle.py -v
pytest tests/natives/test_handle_manager_effect.py -v
pytest tests/natives/test_effect_natives.py -v
pytest tests/integration/test_effect_system.py -v

# 运行全部测试确保无回归
pytest

# 代码检查
flake8 src/jass_runner/natives/effect_natives.py
```

## 完成标准

- [ ] Effect Handle 类实现并通过测试
- [ ] HandleManager 特效生命周期方法实现并通过测试
- [ ] 5 个特效 native 函数实现并通过测试
- [ ] 所有函数在 NativeFactory 中注册
- [ ] 集成测试覆盖完整场景
- [ ] 项目笔记已更新
- [ ] 所有测试通过
- [ ] 代码符合项目规范（中文注释、行数限制）
