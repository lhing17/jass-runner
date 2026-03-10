# 事件系统改造设计文档

## 概述

将 JASS Runner 的事件系统从字符串类型改造为符合 JASS 语义的 handle 类型，解决 `TriggerRegisterPlayerUnitEvent` 等函数的参数类型不匹配问题。

## 问题背景

### 当前问题
- JASS 中事件类型是 handle 的子类型（`playerunitevent`、`playerevent`、`gameevent` 等）
- 当前 Python 实现使用字符串表示事件类型（如 `"player_unit_spell_effect"`）
- 类型检查器期望 `playerunitevent` 类型，但实际得到 `string`
- 调用 `TriggerRegisterAnyUnitEventBJ` 时抛出 `JassTypeError`

### 目标
- 使事件系统符合 JASS 语义
- 支持 `ConvertPlayerUnitEvent(274)` 等 Convert 函数
- 保持与现有触发器系统的兼容性

## 设计方案

### 1. 创建事件 Handle 类

**文件**: `src/jass_runner/natives/event_handles.py`

```python
class PlayerUnitEvent(Handle):
    """玩家-单位事件类型 handle"""
    def __init__(self, handle_id: str, event_id: int):
        super().__init__(handle_id, "playerunitevent")
        self.event_id = event_id

class PlayerEvent(Handle):
    """玩家事件类型 handle"""
    def __init__(self, handle_id: str, event_id: int):
        super().__init__(handle_id, "playerevent")
        self.event_id = event_id

class GameEvent(Handle):
    """游戏事件类型 handle"""
    def __init__(self, handle_id: str, event_id: int):
        super().__init__(handle_id, "gameevent")
        self.event_id = event_id

class UnitEvent(Handle):
    """通用单位事件类型 handle"""
    def __init__(self, handle_id: str, event_id: int):
        super().__init__(handle_id, "unitevent")
        self.event_id = event_id
```

### 2. 更新事件常量

**文件**: `src/jass_runner/trigger/event_types.py`

- 将字符串常量改为整数常量（与 common.j 中的值保持一致）
- 添加 `EVENT_ID_TO_NAME` 映射用于内部索引

```python
# 玩家-单位事件 ID 常量（与 common.j 保持一致）
EVENT_PLAYER_UNIT_DEATH = 275
EVENT_PLAYER_UNIT_ATTACKED = 276
EVENT_PLAYER_UNIT_SPELL_EFFECT = 274
# ... 其他事件

# 事件 ID 到名称的映射（用于内部事件分发）
EVENT_ID_TO_NAME = {
    EVENT_PLAYER_UNIT_SPELL_EFFECT: "player_unit_spell_effect",
    EVENT_PLAYER_UNIT_DEATH: "player_unit_death",
    # ...
}
```

### 3. 实现 Convert 函数

**文件**: `src/jass_runner/natives/event_natives.py`（新建）

```python
class ConvertPlayerUnitEvent(NativeFunction):
    """将整数转换为 playerunitevent 类型"""
    @property
    def name(self) -> str:
        return "ConvertPlayerUnitEvent"

    def execute(self, state_context, event_id: int):
        handle_manager = state_context.handle_manager
        return handle_manager.create_playerunit_event(event_id)

class ConvertPlayerEvent(NativeFunction):
    """将整数转换为 playerevent 类型"""
    @property
    def name(self) -> str:
        return "ConvertPlayerEvent"

    def execute(self, state_context, event_id: int):
        return state_context.handle_manager.create_playerevent(event_id)

class ConvertGameEvent(NativeFunction):
    """将整数转换为 gameevent 类型"""
    @property
    def name(self) -> str:
        return "ConvertGameEvent"

    def execute(self, state_context, event_id: int):
        return state_context.handle_manager.create_gameevent(event_id)

class ConvertUnitEvent(NativeFunction):
    """将整数转换为 unitevent 类型"""
    @property
    def name(self) -> str:
        return "ConvertUnitEvent"

    def execute(self, state_context, event_id: int):
        return state_context.handle_manager.create_unitevent(event_id)
```

### 4. 扩展 HandleManager

**文件**: `src/jass_runner/natives/manager.py`

添加创建事件类型的方法：

```python
def create_playerunit_event(self, event_id: int) -> PlayerUnitEvent:
    """创建玩家-单位事件类型 handle"""
    handle_id = f"playerunitevent_{self._generate_id()}"
    event = PlayerUnitEvent(handle_id, event_id)
    self._register_handle(event)
    return event

def create_playerevent(self, event_id: int) -> PlayerEvent:
    """创建玩家事件类型 handle"""
    handle_id = f"playerevent_{self._generate_id()}"
    event = PlayerEvent(handle_id, event_id)
    self._register_handle(event)
    return event

def create_gameevent(self, event_id: int) -> GameEvent:
    """创建游戏事件类型 handle"""
    handle_id = f"gameevent_{self._generate_id()}"
    event = GameEvent(handle_id, event_id)
    self._register_handle(event)
    return event

def create_unitevent(self, event_id: int) -> UnitEvent:
    """创建通用单位事件类型 handle"""
    handle_id = f"unitevent_{self._generate_id()}"
    event = UnitEvent(handle_id, event_id)
    self._register_handle(event)
    return event
```

### 5. 更新类型层次

**文件**: `src/jass_runner/types/hierarchy.py`

在 `HANDLE_SUBTYPES` 中添加事件类型：

```python
HANDLE_SUBTYPES = {
    # ... 现有类型 ...
    'playerunitevent': 'handle',
    'playerevent': 'handle',
    'gameevent': 'handle',
    'unitevent': 'handle',
}
```

### 6. 更新事件注册 Native 函数

**文件**: `src/jass_runner/natives/trigger_register_event_natives.py`

修改参数类型和内部实现：

```python
class TriggerRegisterPlayerUnitEvent(NativeFunction):
    @property
    def name(self) -> str:
        return "TriggerRegisterPlayerUnitEvent"

    def execute(self, state_context, trigger, event: PlayerUnitEvent,
                filter_func=None, *args, **kwargs):
        # 使用 event.event_id 获取整数 ID
        event_id = event.event_id
        # 通过 EVENT_ID_TO_NAME 获取事件名称用于内部索引
        event_name = EVENT_ID_TO_NAME.get(event_id, f"unknown_event_{event_id}")

        filter_data = {"event_id": event_id}
        if filter_func:
            filter_data["filter"] = filter_func

        result = state_context.trigger_manager.register_event(
            trigger.id if hasattr(trigger, 'id') else trigger,
            event_name,  # 内部仍使用字符串索引
            filter_data
        )
        return result
```

### 7. 注册新函数

**文件**: `src/jass_runner/natives/factory.py`

- 导入事件 handle 类和 Convert 函数
- 在 `create_default_registry` 中注册所有新函数

## 兼容性考虑

### 向后兼容性
- TriggerManager 内部仍使用字符串作为事件索引
- `EVENT_ID_TO_NAME` 映射确保新旧系统兼容
- 现有测试无需大幅修改

### 与 common.j 的集成
- 事件常量值与 common.j 保持一致
- 预加载机制正常工作
- Convert 函数返回值类型符合 JASS 语义

## 测试策略

### 单元测试
1. 事件 handle 类创建和属性测试
2. Convert 函数测试（验证返回值类型和 event_id）
3. HandleManager 扩展方法测试
4. 类型检查器兼容性测试

### 集成测试
1. 完整事件注册流程测试
2. common.j 常量解析测试
3. BJ 函数（如 `TriggerRegisterAnyUnitEventBJ`）测试

## 实施步骤

1. 创建 `event_handles.py` - 事件 handle 类
2. 更新 `event_types.py` - 整数常量和映射
3. 创建 `event_natives.py` - Convert 函数
4. 扩展 `manager.py` - HandleManager 方法
5. 更新 `hierarchy.py` - 类型层次
6. 更新 `trigger_register_event_natives.py` - 参数类型
7. 更新 `factory.py` - 注册新函数
8. 添加测试

## 预期结果

- `TriggerRegisterPlayerUnitEvent(t, EVENT_PLAYER_UNIT_SPELL_EFFECT)` 正常工作
- 类型检查通过，无 `JassTypeError`
- `TriggerRegisterAnyUnitEventBJ` 等 BJ 函数正常工作
- 所有现有测试继续通过
