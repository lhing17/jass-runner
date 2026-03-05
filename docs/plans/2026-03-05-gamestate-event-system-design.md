# GameState 事件系统设计文档

## 概述

实现 `TriggerRegisterGameStateEvent` native 函数及相关类型支持，用于在 JASS 脚本中注册游戏状态变化事件。此功能将支持 `GAME_STATE_TIME_OF_DAY` 状态监控，并实现日夜循环系统。

## 使用示例

```jass
set bj_dncSoundsDawn = CreateTrigger()
call TriggerRegisterGameStateEvent(bj_dncSoundsDawn, GAME_STATE_TIME_OF_DAY, EQUAL, bj_TOD_DAWN)
call TriggerAddAction(bj_dncSoundsDawn, function SetDNCSoundsDawn)
```

## 架构设计

### 1. 类型定义

#### 1.1 LimitOp 类型 (`src/jass_runner/types/limitop.py`)

定义比较操作符类型和常量：

```python
class LimitOp:
    """比较操作符类型。"""

    LESS_THAN = 0
    LESS_THAN_OR_EQUAL = 1
    EQUAL = 2
    GREATER_THAN_OR_EQUAL = 3
    GREATER_THAN = 4
    NOT_EQUAL = 5

    @staticmethod
    def compare(opcode: int, actual: float, target: float) -> bool:
        """根据操作码执行比较。"""
```

#### 1.2 GameState 类型 (`src/jass_runner/types/gamestate.py`)

定义游戏状态类型和常量：

```python
class IGameState:
    """整数类型游戏状态。"""
    DIVINE_INTERVENTION = 0
    DISCONNECTED = 1

class FGameState:
    """浮点类型游戏状态。"""
    TIME_OF_DAY = 2
```

### 2. 游戏状态管理器 (`src/jass_runner/gamestate/manager.py`)

#### 职责
- 管理游戏状态值的存储和更新
- 实现日夜循环系统
- 检测状态变化并触发事件

#### 核心实现

```python
class GameStateManager:
    """游戏状态管理器。

    管理所有游戏状态的当前值，实现日夜循环逻辑，
    并在状态满足条件时触发事件。
    """

    def __init__(self, trigger_manager: TriggerManager):
        self._trigger_manager = trigger_manager
        self._float_states = {}
        self._int_states = {}
        self._time_of_day = 0.0  # 0.0 - 24.0
        self._cycle_frames = 9000  # 5分钟 = 9000帧 (30fps)
        self._frame_counter = 0

    def update(self, delta_frames: int = 1):
        """每帧调用，更新游戏状态。

        参数：
            delta_frames: 经过的帧数
        """
        # 更新日夜循环
        self._frame_counter += delta_frames
        self._time_of_day = (self._frame_counter % self._cycle_frames) / self._cycle_frames * 24.0

        # 检查注册的触发器条件
        self._check_state_listeners()

    def get_float_state(self, state_id: int) -> float:
        """获取浮点类型游戏状态值。"""
        if state_id == FGameState.TIME_OF_DAY:
            return self._time_of_day
        return self._float_states.get(state_id, 0.0)
```

### 3. 事件注册增强

#### 3.1 新增事件类型 (`src/jass_runner/trigger/event_types.py`)

```python
EVENT_GAME_STATE_LIMIT = "game_state_limit"
"""游戏状态达到限制条件事件 - 当游戏状态满足注册条件时触发。"""
```

#### 3.2 状态监听器注册

在 `TriggerManager` 中添加：

```python
def register_game_state_listener(
    self,
    trigger_id: str,
    state_id: int,
    opcode: int,
    limit_value: float
) -> Optional[str]:
    """注册游戏状态监听器。

    参数：
        trigger_id: 触发器ID
        state_id: 游戏状态ID (如 FGameState.TIME_OF_DAY)
        opcode: 比较操作符 (如 LimitOp.EQUAL)
        limit_value: 目标限制值

    返回：
        监听器handle，失败返回None
    """
```

### 4. Native 函数实现

#### 4.1 TriggerRegisterGameStateEvent

位置：`src/jass_runner/natives/gamestate_event_natives.py`

```python
class TriggerRegisterGameStateEvent(NativeFunction):
    """注册游戏状态事件的原生函数。

    当游戏状态满足指定条件时触发事件。
    示例：TriggerRegisterGameStateEvent(trg, GAME_STATE_TIME_OF_DAY, EQUAL, 6.0)
    """

    @property
    def name(self) -> str:
        return "TriggerRegisterGameStateEvent"

    def execute(self, state_context, trigger_id: str, state_id: int,
                opcode: int, limit_value: float, *args, **kwargs):
        """执行 TriggerRegisterGameStateEvent 原生函数。

        参数：
            state_context: 状态上下文
            trigger_id: 触发器ID
            state_id: 游戏状态ID
            opcode: 比较操作符
            limit_value: 目标限制值
        """
```

### 5. 集成方案

#### 5.1 与计时器系统集成

```python
# 在 SimulationLoop 或 TimerSystem 中每帧调用
game_state_manager.update(1)
```

#### 5.2 StateContext 扩展

```python
class StateContext:
    def __init__(self):
        # ... 现有代码 ...
        self.game_state_manager = GameStateManager(self.trigger_manager)
```

#### 5.3 NativeFactory 注册

```python
def create_default_registry():
    registry = NativeRegistry()
    # ... 现有注册 ...
    registry.register(TriggerRegisterGameStateEvent())
    return registry
```

## 数据流

```
┌─────────────────┐
│  SimulationLoop │
│  (每帧调用)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────────┐
│ GameStateManager│────▶│   检查监听器条件  │
│  (update)       │     │  (LimitOp.compare)│
└────────┬────────┘     └────────┬─────────┘
         │                       │
         │              条件满足 │
         │                       ▼
         │             ┌──────────────────┐
         │             │  fire_event      │
         │             │  EVENT_GAME_STATE_LIMIT
         │             └────────┬─────────┘
         │                      │
         ▼                      ▼
┌─────────────────┐    ┌──────────────────┐
│  更新TIME_OF_DAY │    │  TriggerManager  │
│  (日夜循环)      │    │  (dispatch)      │
└─────────────────┘    └────────┬─────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │  执行触发器动作    │
                       │  (如播放黎明音效)  │
                       └──────────────────┘
```

## 测试策略

### 单元测试

1. **LimitOp 测试** - 验证所有比较操作符逻辑
2. **GameStateManager 测试** - 验证状态更新和日夜循环
3. **TriggerRegisterGameStateEvent 测试** - 验证 native 函数注册逻辑

### 集成测试

1. **端到端测试** - 注册触发器 -> 模拟时间推进 -> 验证触发
2. **日夜循环测试** - 验证完整 24 小时周期

## 文件清单

| 文件路径 | 说明 |
|---------|------|
| `src/jass_runner/types/limitop.py` | LimitOp 类型定义 |
| `src/jass_runner/types/gamestate.py` | GameState 类型定义 |
| `src/jass_runner/gamestate/manager.py` | GameStateManager 实现 |
| `src/jass_runner/natives/gamestate_event_natives.py` | 事件注册 native 函数 |
| `tests/gamestate/test_manager.py` | GameStateManager 单元测试 |
| `tests/natives/test_gamestate_event_natives.py` | native 函数单元测试 |
| `tests/integration/test_gamestate_events.py` | 集成测试 |

## 注意事项

1. **精度问题**：浮点数比较使用 epsilon 容差（如 `abs(a - b) < 0.001`）
2. **性能考虑**：每帧检查所有监听器，监听器数量较多时需要优化
3. **时间单位**：游戏时间使用 0.0-24.0 表示一天，与现实时间不同
4. **可扩展性**：设计支持未来添加更多游戏状态类型
