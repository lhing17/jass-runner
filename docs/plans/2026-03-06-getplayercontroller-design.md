# GetPlayerController 及相关类型设计文档

## 概述

实现 `GetPlayerController` native 函数，用于获取玩家的控制器类型（用户、电脑、中立等）。同时实现 `mapcontrol` 类型和 `ConvertMapControl` 类型转换函数。

## 背景

在 Warcraft 3 JASS 中，`mapcontrol` 是表示玩家控制器类型的内置类型：

```jass
constant mapcontrol MAP_CONTROL_USER      = ConvertMapControl(0)
constant mapcontrol MAP_CONTROL_COMPUTER  = ConvertMapControl(1)
constant mapcontrol MAP_CONTROL_RESCUABLE = ConvertMapControl(2)
constant mapcontrol MAP_CONTROL_NEUTRAL   = ConvertMapControl(3)
constant mapcontrol MAP_CONTROL_CREEP     = ConvertMapControl(4)
constant mapcontrol MAP_CONTROL_NONE      = ConvertMapControl(5)
```

`GetPlayerController` native 函数返回指定玩家的控制器类型：

```jass
native GetPlayerController takes player whichPlayer returns mapcontrol
```

## 设计方案

### 1. Player 类修改

将 `Player.controller` 属性从字符串类型改为整数类型（0-5），与 JASS 中的常量定义保持一致：

- 0: MAP_CONTROL_USER
- 1: MAP_CONTROL_COMPUTER
- 2: MAP_CONTROL_RESCUABLE
- 3: MAP_CONTROL_NEUTRAL
- 4: MAP_CONTROL_CREEP
- 5: MAP_CONTROL_NONE

默认映射规则：
- player_id 0-7: MAP_CONTROL_USER (0)
- player_id 8-11: MAP_CONTROL_COMPUTER (1)
- player_id 12-15: MAP_CONTROL_NEUTRAL (3)

### 2. 新建 player_controller_natives.py

创建新模块 `src/jass_runner/natives/player_controller_natives.py`，包含：

#### GetPlayerController 类
- 继承 `NativeFunction`
- 接收 `player` 参数
- 返回 `player.controller` 整数值
- 如果 player 为 None，返回 0（MAP_CONTROL_USER）并记录警告日志

#### ConvertMapControl 类
- 继承 `NativeFunction`
- 接收整数参数，直接返回该整数
- 这是一个类型转换函数，在 Python 实现中只是透传

### 3. 工厂注册

在 `NativeFactory.create_default_registry()` 中注册两个新的 native 函数。

## 接口定义

```python
# GetPlayerController
class GetPlayerController(NativeFunction):
    @property
    def name(self) -> str: ...

    def execute(self, state_context: StateContext, player: Player) -> int: ...

# ConvertMapControl
class ConvertMapControl(NativeFunction):
    @property
    def name(self) -> str: ...

    def execute(self, state_context: StateContext, control_type: int) -> int: ...
```

## 测试策略

1. 单元测试：测试 `GetPlayerController` 对不同 player_id 的返回值
2. 单元测试：测试 `ConvertMapControl` 的透传行为
3. 集成测试：在 JASS 脚本中使用这些函数

## 实现步骤

1. 修改 `player.py` 中的 controller 初始化为整数
2. 创建 `player_controller_natives.py` 模块
3. 在 `factory.py` 中导入并注册新 native 函数
4. 编写单元测试
5. 编写集成测试
