# 事件系统改造实施计划

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将事件系统从字符串类型改造为符合 JASS 语义的 handle 类型，解决类型检查失败问题。

**Architecture:** 创建事件 handle 类（PlayerUnitEvent 等），实现 Convert 函数，更新类型层次和事件注册函数，保持与现有触发器系统的兼容性。

**Tech Stack:** Python 3.8+, pytest, 项目自定义的 Handle 框架和类型检查系统

---

## 文件结构

| 文件 | 操作 | 说明 |
|------|------|------|
| `src/jass_runner/natives/event_handles.py` | 创建 | 事件 handle 类（PlayerUnitEvent, PlayerEvent, GameEvent, UnitEvent） |
| `src/jass_runner/natives/event_natives.py` | 创建 | Convert 函数（ConvertPlayerUnitEvent 等） |
| `src/jass_runner/trigger/event_types.py` | 修改 | 字符串常量改为整数，添加 EVENT_ID_TO_NAME 映射 |
| `src/jass_runner/types/hierarchy.py` | 修改 | 添加事件类型到 HANDLE_SUBTYPES |
| `src/jass_runner/natives/manager.py` | 修改 | 添加创建事件类型的方法 |
| `src/jass_runner/natives/trigger_register_event_natives.py` | 修改 | 更新参数类型为事件 handle 类 |
| `src/jass_runner/natives/factory.py` | 修改 | 导入并注册新类和函数 |
| `tests/natives/test_event_handles.py` | 创建 | 事件 handle 类单元测试 |
| `tests/natives/test_event_natives.py` | 创建 | Convert 函数单元测试 |

---

## Chunk 1: 创建事件 Handle 类

### Task 1: 创建 event_handles.py

**Files:**
- 创建: `src/jass_runner/natives/event_handles.py`

- [ ] **Step 1: 编写事件 handle 类**

```python
"""事件类型 handle 类。

此模块包含所有 JASS 事件类型的 handle 类。
"""

from .handle_base import Handle


class PlayerUnitEvent(Handle):
    """玩家-单位事件类型 handle。

    对应 JASS 中的 playerunitevent 类型。
    """

    def __init__(self, handle_id: str, event_id: int):
        """初始化玩家-单位事件 handle。

        参数：
            handle_id: 唯一标识符
            event_id: 事件整数 ID（如 274）
        """
        super().__init__(handle_id, "playerunitevent")
        self.event_id = event_id


class PlayerEvent(Handle):
    """玩家事件类型 handle。

    对应 JASS 中的 playerevent 类型。
    """

    def __init__(self, handle_id: str, event_id: int):
        """初始化玩家事件 handle。

        参数：
            handle_id: 唯一标识符
            event_id: 事件整数 ID
        """
        super().__init__(handle_id, "playerevent")
        self.event_id = event_id


class GameEvent(Handle):
    """游戏事件类型 handle。

    对应 JASS 中的 gameevent 类型。
    """

    def __init__(self, handle_id: str, event_id: int):
        """初始化游戏事件 handle。

        参数：
            handle_id: 唯一标识符
            event_id: 事件整数 ID
        """
        super().__init__(handle_id, "gameevent")
        self.event_id = event_id


class UnitEvent(Handle):
    """通用单位事件类型 handle。

    对应 JASS 中的 unitevent 类型。
    """

    def __init__(self, handle_id: str, event_id: int):
        """初始化通用单位事件 handle。

        参数：
            handle_id: 唯一标识符
            event_id: 事件整数 ID
        """
        super().__init__(handle_id, "unitevent")
        self.event_id = event_id
```

- [ ] **Step 2: 验证导入**

运行: `python -c "from jass_runner.natives.event_handles import PlayerUnitEvent, PlayerEvent, GameEvent, UnitEvent; print('Import OK')"`
Expected: `Import OK`

- [ ] **Step 3: Commit**

```bash
git add src/jass_runner/natives/event_handles.py
git commit -m "feat(handles): 添加事件类型 handle 类"
```

---

## Chunk 2: 更新事件常量

### Task 2: 修改 event_types.py

**Files:**
- 修改: `src/jass_runner/trigger/event_types.py`

- [ ] **Step 1: 更新所有事件常量为整数**

```python
"""JASS触发器事件类型定义模块。

此模块定义了JASS触发器系统中使用的所有事件类型常量，
包括玩家-单位事件、通用单位事件、玩家事件和游戏事件。

注意：常量值与 common.j 中的定义保持一致。
"""

# =============================================================================
# 玩家-单位事件 (Player-Unit Events)
# =============================================================================
# 当特定玩家的单位发生特定行为时触发的事件

EVENT_PLAYER_UNIT_DEATH = 275
"""玩家单位死亡事件 - 当指定玩家的单位死亡时触发。"""

EVENT_PLAYER_UNIT_ATTACKED = 276
"""玩家单位被攻击事件 - 当指定玩家的单位受到攻击时触发。"""

EVENT_PLAYER_UNIT_SPELL_EFFECT = 274
"""玩家单位施法效果事件 - 当指定玩家的单位施放技能产生效果时触发。"""

EVENT_PLAYER_UNIT_DAMAGED = 277
"""玩家单位受到伤害事件 - 当指定玩家的单位受到伤害时触发。"""

EVENT_PLAYER_UNIT_PICKUP_ITEM = 278
"""玩家单位拾取物品事件 - 当指定玩家的单位拾取物品时触发。"""

EVENT_PLAYER_UNIT_DROP_ITEM = 279
"""玩家单位丢弃物品事件 - 当指定玩家的单位丢弃物品时触发。"""

EVENT_PLAYER_UNIT_USE_ITEM = 280
"""玩家单位使用物品事件 - 当指定玩家的单位使用物品时触发。"""

EVENT_PLAYER_UNIT_ISSUED_ORDER = 281
"""玩家单位接收命令事件 - 当指定玩家的单位接收到命令时触发。"""


# =============================================================================
# 通用单位事件 (Unit Events)
# =============================================================================
# 当任何单位发生特定行为时触发的事件

EVENT_UNIT_DEATH = 100
"""单位死亡事件 - 当任何单位死亡时触发。"""

EVENT_UNIT_DAMAGED = 101
"""单位受到伤害事件 - 当任何单位受到伤害时触发。"""


# =============================================================================
# 玩家事件 (Player Events)
# =============================================================================
# 与玩家状态变化相关的事件

EVENT_PLAYER_DEFEAT = 200
"""玩家失败事件 - 当玩家失败时触发。"""

EVENT_PLAYER_VICTORY = 201
"""玩家胜利事件 - 当玩家胜利时触发。"""

EVENT_PLAYER_LEAVE = 202
"""玩家离开事件 - 当玩家离开游戏时触发。"""

EVENT_PLAYER_CHAT = 203
"""玩家聊天事件 - 当玩家发送聊天消息时触发。"""


# =============================================================================
# 游戏事件 (Game Events)
# =============================================================================
# 与游戏整体状态相关的事件

EVENT_GAME_TIMER_EXPIRED = 300
"""游戏计时器到期事件 - 当游戏计时器到期时触发。"""

EVENT_GAME_STATE_LIMIT = 301
"""游戏状态限制事件 - 当游戏状态达到指定限制条件时触发。"""


# =============================================================================
# 事件分类列表（用于内部事件分发索引）
# =============================================================================

PLAYER_UNIT_EVENTS = [
    EVENT_PLAYER_UNIT_DEATH,
    EVENT_PLAYER_UNIT_ATTACKED,
    EVENT_PLAYER_UNIT_SPELL_EFFECT,
    EVENT_PLAYER_UNIT_DAMAGED,
    EVENT_PLAYER_UNIT_PICKUP_ITEM,
    EVENT_PLAYER_UNIT_DROP_ITEM,
    EVENT_PLAYER_UNIT_USE_ITEM,
    EVENT_PLAYER_UNIT_ISSUED_ORDER,
]
"""玩家-单位事件列表，包含所有与特定玩家单位相关的事件类型。"""

UNIT_EVENTS = [
    EVENT_UNIT_DEATH,
    EVENT_UNIT_DAMAGED,
]
"""通用单位事件列表，包含所有与任意单位相关的事件类型。"""

PLAYER_EVENTS = [
    EVENT_PLAYER_DEFEAT,
    EVENT_PLAYER_VICTORY,
    EVENT_PLAYER_LEAVE,
    EVENT_PLAYER_CHAT,
]
"""玩家事件列表，包含所有与玩家状态变化相关的事件类型。"""

GAME_EVENTS = [
    EVENT_GAME_TIMER_EXPIRED,
    EVENT_GAME_STATE_LIMIT,
]
"""游戏事件列表，包含所有与游戏整体状态相关的事件类型。"""

ALL_EVENTS = (
    PLAYER_UNIT_EVENTS +
    UNIT_EVENTS +
    PLAYER_EVENTS +
    GAME_EVENTS
)
"""所有事件类型列表，包含定义的全部事件类型。"""


# =============================================================================
# 事件 ID 到名称的映射（用于内部事件分发和日志）
# =============================================================================

EVENT_ID_TO_NAME = {
    # 玩家-单位事件
    EVENT_PLAYER_UNIT_DEATH: "player_unit_death",
    EVENT_PLAYER_UNIT_ATTACKED: "player_unit_attacked",
    EVENT_PLAYER_UNIT_SPELL_EFFECT: "player_unit_spell_effect",
    EVENT_PLAYER_UNIT_DAMAGED: "player_unit_damaged",
    EVENT_PLAYER_UNIT_PICKUP_ITEM: "player_unit_pickup_item",
    EVENT_PLAYER_UNIT_DROP_ITEM: "player_unit_drop_item",
    EVENT_PLAYER_UNIT_USE_ITEM: "player_unit_use_item",
    EVENT_PLAYER_UNIT_ISSUED_ORDER: "player_unit_issued_order",
    # 通用单位事件
    EVENT_UNIT_DEATH: "unit_death",
    EVENT_UNIT_DAMAGED: "unit_damaged",
    # 玩家事件
    EVENT_PLAYER_DEFEAT: "player_defeat",
    EVENT_PLAYER_VICTORY: "player_victory",
    EVENT_PLAYER_LEAVE: "player_leave",
    EVENT_PLAYER_CHAT: "player_chat",
    # 游戏事件
    EVENT_GAME_TIMER_EXPIRED: "game_timer_expired",
    EVENT_GAME_STATE_LIMIT: "game_state_limit",
}
"""事件 ID 到事件名称的映射，用于内部事件索引和日志输出。"""
```

- [ ] **Step 2: 运行测试确保无回归**

运行: `pytest tests/trigger/test_event_types.py -v`
Expected: 可能需要更新测试，因为常量类型从字符串变为整数

- [ ] **Step 3: 更新测试文件**

修改 `tests/trigger/test_event_types.py`:
- 将 `isinstance(EVENT_PLAYER_UNIT_SPELL_EFFECT, str)` 改为 `isinstance(EVENT_PLAYER_UNIT_SPELL_EFFECT, int)`
- 将字符串比较改为整数比较

- [ ] **Step 4: 运行测试验证**

运行: `pytest tests/trigger/test_event_types.py -v`
Expected: 所有测试 PASS

- [ ] **Step 5: Commit**

```bash
git add src/jass_runner/trigger/event_types.py tests/trigger/test_event_types.py
git commit -m "refactor(events): 将事件常量从字符串改为整数"
```

---

## Chunk 3: 更新类型层次

### Task 3: 修改 hierarchy.py

**Files:**
- 修改: `src/jass_runner/types/hierarchy.py`

- [ ] **Step 1: 添加事件类型到 HANDLE_SUBTYPES**

在第12-29行之间添加：
```python
    HANDLE_SUBTYPES = {
        'unit': 'handle',
        'item': 'handle',
        'timer': 'handle',
        'trigger': 'handle',
        'player': 'handle',
        'destructable': 'handle',
        'itempool': 'handle',
        'unitpool': 'handle',
        'group': 'handle',
        'force': 'handle',
        'rect': 'handle',
        'region': 'handle',
        'sound': 'handle',
        'effect': 'handle',
        'location': 'handle',
        'version': 'handle',
        'playerunitevent': 'handle',
        'playerevent': 'handle',
        'gameevent': 'handle',
        'unitevent': 'handle',
    }
```

- [ ] **Step 2: 验证修改**

运行: `python -c "from jass_runner.types.hierarchy import TypeHierarchy; print('playerunitevent is handle:', TypeHierarchy.is_subtype('playerunitevent', 'handle'))"`
Expected: `playerunitevent is handle: True`

- [ ] **Step 3: Commit**

```bash
git add src/jass_runner/types/hierarchy.py
git commit -m "feat(types): 添加事件类型到类型层次"
```

---

## Chunk 4: 扩展 HandleManager

### Task 4: 修改 manager.py

**Files:**
- 修改: `src/jass_runner/natives/manager.py`

- [ ] **Step 1: 导入事件 handle 类**

在第8-9行添加导入：
```python
from .handle import Handle, Unit, Player, Item, Group, Rect, Effect, BoolExpr, Sound
from .hashtable import Hashtable
from .event_handles import PlayerUnitEvent, PlayerEvent, GameEvent, UnitEvent
```

- [ ] **Step 2: 添加创建事件类型的方法**

在文件末尾（get_hashtable 方法之后）添加：

```python
    def create_playerunit_event(self, event_id: int) -> PlayerUnitEvent:
        """创建玩家-单位事件类型 handle。

        参数：
            event_id: 事件整数 ID（如 274）

        返回：
            PlayerUnitEvent 对象
        """
        handle_id = f"playerunitevent_{self._generate_id()}"
        event = PlayerUnitEvent(handle_id, event_id)
        self._register_handle(event)
        return event

    def create_playerevent(self, event_id: int) -> PlayerEvent:
        """创建玩家事件类型 handle。

        参数：
            event_id: 事件整数 ID

        返回：
            PlayerEvent 对象
        """
        handle_id = f"playerevent_{self._generate_id()}"
        event = PlayerEvent(handle_id, event_id)
        self._register_handle(event)
        return event

    def create_gameevent(self, event_id: int) -> GameEvent:
        """创建游戏事件类型 handle。

        参数：
            event_id: 事件整数 ID

        返回：
            GameEvent 对象
        """
        handle_id = f"gameevent_{self._generate_id()}"
        event = GameEvent(handle_id, event_id)
        self._register_handle(event)
        return event

    def create_unitevent(self, event_id: int) -> UnitEvent:
        """创建通用单位事件类型 handle。

        参数：
            event_id: 事件整数 ID

        返回：
            UnitEvent 对象
        """
        handle_id = f"unitevent_{self._generate_id()}"
        event = UnitEvent(handle_id, event_id)
        self._register_handle(event)
        return event
```

- [ ] **Step 3: 验证导入和方法**

运行: `python -c "from jass_runner.natives.manager import HandleManager; m = HandleManager(); e = m.create_playerunit_event(274); print(f'Created event: {e.id}, type: {e.type_name}, event_id: {e.event_id}')"`
Expected: `Created event: playerunitevent_X, type: playerunitevent, event_id: 274`

- [ ] **Step 4: Commit**

```bash
git add src/jass_runner/natives/manager.py
git commit -m "feat(manager): 添加创建事件类型 handle 的方法"
```

---

## Chunk 5: 实现 Convert 函数

### Task 5: 创建 event_natives.py

**Files:**
- 创建: `src/jass_runner/natives/event_natives.py`

- [ ] **Step 1: 编写 Convert 函数**

```python
"""事件类型相关 Native 函数。

此模块包含 Convert 函数，用于将整数转换为事件类型 handle。
"""

import logging
from .base import NativeFunction
from .event_handles import PlayerUnitEvent, PlayerEvent, GameEvent, UnitEvent

logger = logging.getLogger(__name__)


class ConvertPlayerUnitEvent(NativeFunction):
    """将整数转换为 playerunitevent 类型。"""

    @property
    def name(self) -> str:
        return "ConvertPlayerUnitEvent"

    def execute(self, state_context, event_id: int):
        """执行 ConvertPlayerUnitEvent native 函数。

        参数：
            state_context: 状态上下文
            event_id: 事件整数 ID

        返回：
            PlayerUnitEvent 对象
        """
        handle_manager = state_context.handle_manager
        event = handle_manager.create_playerunit_event(event_id)
        logger.debug(f"[ConvertPlayerUnitEvent] 创建事件 handle: {event.id}, event_id: {event_id}")
        return event


class ConvertPlayerEvent(NativeFunction):
    """将整数转换为 playerevent 类型。"""

    @property
    def name(self) -> str:
        return "ConvertPlayerEvent"

    def execute(self, state_context, event_id: int):
        """执行 ConvertPlayerEvent native 函数。

        参数：
            state_context: 状态上下文
            event_id: 事件整数 ID

        返回：
            PlayerEvent 对象
        """
        handle_manager = state_context.handle_manager
        event = handle_manager.create_playerevent(event_id)
        logger.debug(f"[ConvertPlayerEvent] 创建事件 handle: {event.id}, event_id: {event_id}")
        return event


class ConvertGameEvent(NativeFunction):
    """将整数转换为 gameevent 类型。"""

    @property
    def name(self) -> str:
        return "ConvertGameEvent"

    def execute(self, state_context, event_id: int):
        """执行 ConvertGameEvent native 函数。

        参数：
            state_context: 状态上下文
            event_id: 事件整数 ID

        返回：
            GameEvent 对象
        """
        handle_manager = state_context.handle_manager
        event = handle_manager.create_gameevent(event_id)
        logger.debug(f"[ConvertGameEvent] 创建事件 handle: {event.id}, event_id: {event_id}")
        return event


class ConvertUnitEvent(NativeFunction):
    """将整数转换为 unitevent 类型。"""

    @property
    def name(self) -> str:
        return "ConvertUnitEvent"

    def execute(self, state_context, event_id: int):
        """执行 ConvertUnitEvent native 函数。

        参数：
            state_context: 状态上下文
            event_id: 事件整数 ID

        返回：
            UnitEvent 对象
        """
        handle_manager = state_context.handle_manager
        event = handle_manager.create_unitevent(event_id)
        logger.debug(f"[ConvertUnitEvent] 创建事件 handle: {event.id}, event_id: {event_id}")
        return event
```

- [ ] **Step 2: 验证导入**

运行: `python -c "from jass_runner.natives.event_natives import ConvertPlayerUnitEvent, ConvertPlayerEvent, ConvertGameEvent, ConvertUnitEvent; print('Import OK')"`
Expected: `Import OK`

- [ ] **Step 3: Commit**

```bash
git add src/jass_runner/natives/event_natives.py
git commit -m "feat(natives): 添加事件类型 Convert 函数"
```

---

## Chunk 6: 更新事件注册函数

### Task 6: 修改 trigger_register_event_natives.py

**Files:**
- 修改: `src/jass_runner/natives/trigger_register_event_natives.py`

- [ ] **Step 1: 导入事件 handle 类和常量映射**

在文件顶部添加导入：
```python
from ..trigger.event_types import EVENT_ID_TO_NAME
from ..natives.event_handles import PlayerUnitEvent, PlayerEvent, GameEvent, UnitEvent
```

- [ ] **Step 2: 修改 TriggerRegisterPlayerUnitEvent**

找到 `TriggerRegisterPlayerUnitEvent` 类，修改 `execute` 方法的参数类型：

```python
class TriggerRegisterPlayerUnitEvent(NativeFunction):
    """注册玩家-单位事件到触发器。"""

    @property
    def name(self) -> str:
        return "TriggerRegisterPlayerUnitEvent"

    def execute(self, state_context, trigger, event: PlayerUnitEvent,
                filter_func=None, *args, **kwargs):
        """执行 TriggerRegisterPlayerUnitEvent native 函数。

        参数：
            state_context: 状态上下文
            trigger: Trigger 对象或 trigger ID
            event: PlayerUnitEvent 事件类型对象
            filter_func: 可选的过滤函数

        返回：
            事件 handle 字符串，失败返回 None
        """
        trigger_manager = state_context.trigger_manager
        if trigger_manager is None:
            logger.warning("[TriggerRegisterPlayerUnitEvent] TriggerManager 未初始化")
            return None

        # 从 event 对象获取事件 ID 和名称
        event_id = event.event_id
        event_name = EVENT_ID_TO_NAME.get(event_id, f"unknown_event_{event_id}")

        # 获取 trigger ID
        trigger_id = trigger.id if hasattr(trigger, 'id') else trigger

        filter_data = {"event_id": event_id}
        if filter_func:
            filter_data["filter"] = filter_func

        result = trigger_manager.register_event(
            trigger_id,
            event_name,
            filter_data
        )

        if result:
            logger.info(f"[TriggerRegisterPlayerUnitEvent] 为触发器 {trigger_id} 注册事件 {event_name} (ID: {event_id})")
        else:
            logger.warning(f"[TriggerRegisterPlayerUnitEvent] 注册事件失败")

        return result
```

- [ ] **Step 3: 修改其他事件注册函数**

类似地修改：
- `TriggerRegisterPlayerEvent` - 参数类型改为 `PlayerEvent`
- `TriggerRegisterGameEvent` - 参数类型改为 `GameEvent`
- `TriggerRegisterUnitEvent` - 参数类型改为 `UnitEvent`

- [ ] **Step 4: 运行测试验证**

运行: `pytest tests/natives/test_trigger_register_event_natives_unit.py -v`
Expected: 可能需要更新测试以使用事件对象而非字符串

- [ ] **Step 5: Commit**

```bash
git add src/jass_runner/natives/trigger_register_event_natives.py
git commit -m "refactor(natives): 更新事件注册函数参数类型为事件 handle"
```

---

## Chunk 7: 注册新类和函数

### Task 7: 修改 factory.py

**Files:**
- 修改: `src/jass_runner/natives/factory.py`

- [ ] **Step 1: 添加导入**

在第7行附近添加：
```python
from .event_natives import ConvertPlayerUnitEvent, ConvertPlayerEvent, ConvertGameEvent, ConvertUnitEvent
```

- [ ] **Step 2: 注册 Convert 函数**

在 `create_default_registry` 方法中，在合适位置（如其他基础 native 函数之后）添加：

```python
        # 注册事件类型 Convert 函数
        registry.register(ConvertPlayerUnitEvent())
        registry.register(ConvertPlayerEvent())
        registry.register(ConvertGameEvent())
        registry.register(ConvertUnitEvent())
```

- [ ] **Step 3: 验证导入和注册**

运行: `python -c "from jass_runner.natives.factory import NativeFactory; f = NativeFactory(); r = f.create_default_registry(); print('ConvertPlayerUnitEvent registered:', r.get('ConvertPlayerUnitEvent') is not None)"`
Expected: `ConvertPlayerUnitEvent registered: True`

- [ ] **Step 4: Commit**

```bash
git add src/jass_runner/natives/factory.py
git commit -m "feat(factory): 注册事件类型 Convert 函数"
```

---

## Chunk 8: 添加单元测试

### Task 8: 创建测试文件

**Files:**
- 创建: `tests/natives/test_event_handles.py`
- 创建: `tests/natives/test_event_natives.py`

- [ ] **Step 1: 创建 test_event_handles.py**

```python
"""事件类型 handle 类单元测试。"""

import pytest
from jass_runner.natives.event_handles import PlayerUnitEvent, PlayerEvent, GameEvent, UnitEvent


class TestPlayerUnitEvent:
    """测试 PlayerUnitEvent 类。"""

    def test_creation(self):
        """测试创建 PlayerUnitEvent 对象。"""
        event = PlayerUnitEvent("playerunitevent_1", 274)
        assert event.id == "playerunitevent_1"
        assert event.type_name == "playerunitevent"
        assert event.event_id == 274
        assert event.is_alive()

    def test_different_event_ids(self):
        """测试不同的事件 ID。"""
        event1 = PlayerUnitEvent("playerunitevent_1", 274)
        event2 = PlayerUnitEvent("playerunitevent_2", 275)
        assert event1.event_id == 274
        assert event2.event_id == 275


class TestPlayerEvent:
    """测试 PlayerEvent 类。"""

    def test_creation(self):
        """测试创建 PlayerEvent 对象。"""
        event = PlayerEvent("playerevent_1", 200)
        assert event.id == "playerevent_1"
        assert event.type_name == "playerevent"
        assert event.event_id == 200


class TestGameEvent:
    """测试 GameEvent 类。"""

    def test_creation(self):
        """测试创建 GameEvent 对象。"""
        event = GameEvent("gameevent_1", 300)
        assert event.id == "gameevent_1"
        assert event.type_name == "gameevent"
        assert event.event_id == 300


class TestUnitEvent:
    """测试 UnitEvent 类。"""

    def test_creation(self):
        """测试创建 UnitEvent 对象。"""
        event = UnitEvent("unitevent_1", 100)
        assert event.id == "unitevent_1"
        assert event.type_name == "unitevent"
        assert event.event_id == 100
```

- [ ] **Step 2: 创建 test_event_natives.py**

```python
"""事件类型 Native 函数单元测试。"""

import pytest
from jass_runner.natives.event_natives import (
    ConvertPlayerUnitEvent, ConvertPlayerEvent, ConvertGameEvent, ConvertUnitEvent
)
from jass_runner.natives.event_handles import PlayerUnitEvent, PlayerEvent, GameEvent, UnitEvent
from jass_runner.natives.state import StateContext


@pytest.fixture
def state_context():
    """提供测试用的 StateContext 实例。"""
    return StateContext()


class TestConvertPlayerUnitEvent:
    """测试 ConvertPlayerUnitEvent 函数。"""

    def test_creation(self, state_context):
        """测试创建 PlayerUnitEvent。"""
        native = ConvertPlayerUnitEvent()
        assert native.name == "ConvertPlayerUnitEvent"

        event = native.execute(state_context, 274)
        assert isinstance(event, PlayerUnitEvent)
        assert event.event_id == 274
        assert event.type_name == "playerunitevent"

    def test_different_event_ids(self, state_context):
        """测试不同的事件 ID。"""
        native = ConvertPlayerUnitEvent()

        event1 = native.execute(state_context, 274)
        event2 = native.execute(state_context, 275)

        assert event1.event_id == 274
        assert event2.event_id == 275
        assert event1.id != event2.id  # 不同的 handle ID


class TestConvertPlayerEvent:
    """测试 ConvertPlayerEvent 函数。"""

    def test_creation(self, state_context):
        """测试创建 PlayerEvent。"""
        native = ConvertPlayerEvent()
        event = native.execute(state_context, 200)
        assert isinstance(event, PlayerEvent)
        assert event.event_id == 200


class TestConvertGameEvent:
    """测试 ConvertGameEvent 函数。"""

    def test_creation(self, state_context):
        """测试创建 GameEvent。"""
        native = ConvertGameEvent()
        event = native.execute(state_context, 300)
        assert isinstance(event, GameEvent)
        assert event.event_id == 300


class TestConvertUnitEvent:
    """测试 ConvertUnitEvent 函数。"""

    def test_creation(self, state_context):
        """测试创建 UnitEvent。"""
        native = ConvertUnitEvent()
        event = native.execute(state_context, 100)
        assert isinstance(event, UnitEvent)
        assert event.event_id == 100
```

- [ ] **Step 3: 运行测试**

运行: `pytest tests/natives/test_event_handles.py tests/natives/test_event_natives.py -v`
Expected: 所有测试 PASS

- [ ] **Step 4: Commit**

```bash
git add tests/natives/test_event_handles.py tests/natives/test_event_natives.py
git commit -m "test(natives): 添加事件类型 handle 和 Convert 函数测试"
```

---

## 验证清单

实施完成后，请确认以下事项：

- [ ] `PlayerUnitEvent`, `PlayerEvent`, `GameEvent`, `UnitEvent` 类已创建
- [ ] 事件常量已改为整数（与 common.j 一致）
- [ ] `TypeHierarchy` 已添加事件类型
- [ ] `HandleManager` 已添加创建事件类型的方法
- [ ] `ConvertPlayerUnitEvent` 等函数已实现
- [ ] 事件注册函数参数类型已更新
- [ ] 所有 Convert 函数已在 NativeFactory 注册
- [ ] 所有单元测试通过
- [ ] 现有测试无回归

## 预期结果

- `TriggerRegisterPlayerUnitEvent(t, EVENT_PLAYER_UNIT_SPELL_EFFECT)` 正常工作
- 类型检查通过，无 `JassTypeError`
- `TriggerRegisterAnyUnitEventBJ` 等 BJ 函数正常工作
- 所有现有测试继续通过
