# GetPlayerSlotState 及相关类型设计文档

## 概述

实现 `GetPlayerSlotState` native 函数，用于获取玩家的插槽状态（EMPTY、PLAYING、LEFT）。同时实现 `playerslotstate` 类型和 `ConvertPlayerSlotState` 类型转换函数。

## 背景

在 Warcraft 3 JASS 中，`playerslotstate` 是表示玩家插槽状态的内置类型：

```jass
constant playerslotstate PLAYER_SLOT_STATE_EMPTY   = ConvertPlayerSlotState(0)
constant playerslotstate PLAYER_SLOT_STATE_PLAYING = ConvertPlayerSlotState(1)
constant playerslotstate PLAYER_SLOT_STATE_LEFT    = ConvertPlayerSlotState(2)
```

`GetPlayerSlotState` native 函数返回指定玩家的插槽状态：

```jass
native GetPlayerSlotState takes player whichPlayer returns playerslotstate
```

## 设计方案

### 1. Player 类修改

将 `Player.slot_state` 属性从字符串类型改为整数类型（0-2），与 JASS 中的常量定义保持一致：

- 0: PLAYER_SLOT_STATE_EMPTY
- 1: PLAYER_SLOT_STATE_PLAYING
- 2: PLAYER_SLOT_STATE_LEFT

默认映射规则：
- player_id 0-11: PLAYER_SLOT_STATE_PLAYING (1)
- player_id 12-15: PLAYER_SLOT_STATE_EMPTY (0)

### 2. 新建 player_slot_state_natives.py

创建新模块 `src/jass_runner/natives/player_slot_state_natives.py`，包含：

#### GetPlayerSlotState 类
- 继承 `NativeFunction`
- 接收 `player` 参数
- 返回 `player.slot_state` 整数值
- 如果 player 为 None，返回 0（PLAYER_SLOT_STATE_EMPTY）并记录警告日志

#### ConvertPlayerSlotState 类
- 继承 `NativeFunction`
- 接收整数参数，直接返回该整数
- 这是一个类型转换函数，在 Python 实现中只是透传

### 3. 类型检查器更新

在 `src/jass_runner/types/checker.py` 中添加 integer→playerslotstate 的隐式类型转换支持。

### 4. 工厂注册

在 `NativeFactory.create_default_registry()` 中注册两个新的 native 函数。

## 接口定义

```python
# GetPlayerSlotState
class GetPlayerSlotState(NativeFunction):
    @property
    def name(self) -> str: ...

    def execute(self, state_context: StateContext, player: Player) -> int: ...

# ConvertPlayerSlotState
class ConvertPlayerSlotState(NativeFunction):
    @property
    def name(self) -> str: ...

    def execute(self, state_context: StateContext, slot_state: int) -> int: ...
```

## 测试策略

1. 单元测试：测试 `GetPlayerSlotState` 对不同 player_id 的返回值
2. 单元测试：测试 `ConvertPlayerSlotState` 的透传行为
3. 集成测试：在 JASS 脚本中使用这些函数

## 实现步骤

1. 修改 `player.py` 中的 slot_state 初始化为整数
2. 创建 `player_slot_state_natives.py` 模块
3. 在 `factory.py` 中导入并注册新 native 函数
4. 更新类型检查器支持 integer→playerslotstate 转换
5. 编写单元测试
6. 编写集成测试
