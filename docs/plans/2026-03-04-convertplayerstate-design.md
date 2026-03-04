# ConvertPlayerState Native 函数及扩展 PlayerState 支持设计文档

## 概述

实现 `ConvertPlayerState` native 函数，并扩展 `Player` 类支持 `common.j` 中定义的所有 playerstate 常量。

## 背景

在 Warcraft 3 JASS 中，`playerstate` 类型用于表示玩家的各种状态，包括资源（金币、木材、食物）、游戏状态（观察者、联盟胜利等）。

`common.j` 中定义了以下 playerstate 常量：
```jass
constant playerstate PLAYER_STATE_GAME_RESULT               = ConvertPlayerState(0)
constant playerstate PLAYER_STATE_RESOURCE_GOLD             = ConvertPlayerState(1)
constant playerstate PLAYER_STATE_RESOURCE_LUMBER           = ConvertPlayerState(2)
constant playerstate PLAYER_STATE_RESOURCE_HERO_TOKENS      = ConvertPlayerState(3)
constant playerstate PLAYER_STATE_RESOURCE_FOOD_CAP         = ConvertPlayerState(4)
constant playerstate PLAYER_STATE_RESOURCE_FOOD_USED        = ConvertPlayerState(5)
constant playerstate PLAYER_STATE_FOOD_CAP_CEILING          = ConvertPlayerState(6)
constant playerstate PLAYER_STATE_GIVES_BOUNTY              = ConvertPlayerState(7)
constant playerstate PLAYER_STATE_ALLIED_VICTORY            = ConvertPlayerState(8)
constant playerstate PLAYER_STATE_PLACED                    = ConvertPlayerState(9)
constant playerstate PLAYER_STATE_OBSERVER_ON_DEATH         = ConvertPlayerState(10)
constant playerstate PLAYER_STATE_OBSERVER                  = ConvertPlayerState(11)
constant playerstate PLAYER_STATE_UNFOLLOWABLE              = ConvertPlayerState(12)
constant playerstate PLAYER_STATE_GOLD_UPKEEP_RATE          = ConvertPlayerState(13)
constant playerstate PLAYER_STATE_LUMBER_UPKEEP_RATE        = ConvertPlayerState(14)
constant playerstate PLAYER_STATE_GOLD_GATHERED             = ConvertPlayerState(15)
constant playerstate PLAYER_STATE_LUMBER_GATHERED           = ConvertPlayerState(16)
constant playerstate PLAYER_STATE_NO_CREEP_SLEEP            = ConvertPlayerState(25)
```

## 设计目标

1. 实现 `ConvertPlayerState` native 函数（参考 `ConvertAllianceType` 实现）
2. 扩展 `Player` 类支持所有 playerstate 常量
3. 保持向后兼容（现有资源状态逻辑不变）
4. 使用简单字典存储非资源类状态
5. 确保 `ConvertPlayerState` 调用结果可作为函数参数使用

## 架构设计

### 核心组件

```
┌─────────────────────────────────────────────────────────┐
│              Player._state_data: Dict[int, int]          │
│  存储所有玩家状态，key 为 state_type，value 为状态值      │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ConvertPlayer │   │GetPlayerState│   │SetPlayerState│
│State         │   │              │   │              │
└──────────────┘   └──────────────┘   └──────────────┘
```

### Player 类扩展

```python
class Player:
    # 现有的资源状态常量保留
    PLAYER_STATE_RESOURCE_GOLD = 1
    PLAYER_STATE_RESOURCE_LUMBER = 2
    PLAYER_STATE_RESOURCE_FOOD_CAP = 4
    PLAYER_STATE_RESOURCE_FOOD_USED = 5

    def __init__(self, handle_id: str, player_id: int):
        # 现有的资源属性保留
        self._gold: int = 500
        self._lumber: int = 0
        self._food_cap: int = 100
        self._food_used: int = 0

        # 新增：通用状态存储字典
        self._state_data: Dict[int, int] = {}

    def get_state(self, state_type: int) -> int:
        """获取玩家状态值。"""
        # 优先处理资源类状态（保持向后兼容）
        if state_type == Player.PLAYER_STATE_RESOURCE_GOLD:
            return self._gold
        elif state_type == Player.PLAYER_STATE_RESOURCE_LUMBER:
            return self._lumber
        elif state_type == Player.PLAYER_STATE_RESOURCE_FOOD_CAP:
            return self._food_cap
        elif state_type == Player.PLAYER_STATE_RESOURCE_FOOD_USED:
            return self._food_used

        # 其他状态从字典读取，默认为 0
        return self._state_data.get(state_type, 0)

    def set_state(self, state_type: int, value: int) -> int:
        """设置玩家状态值。"""
        # 优先处理资源类状态
        if state_type == Player.PLAYER_STATE_RESOURCE_GOLD:
            self._gold = self._clamp_resource(value, 0, 1000000)
            return self._gold
        elif state_type == Player.PLAYER_STATE_RESOURCE_LUMBER:
            self._lumber = self._clamp_resource(value, 0, 1000000)
            return self._lumber
        elif state_type == Player.PLAYER_STATE_RESOURCE_FOOD_CAP:
            self._food_cap = self._clamp_resource(value, 0, 300)
            return self._food_cap
        elif state_type == Player.PLAYER_STATE_RESOURCE_FOOD_USED:
            self._food_used = self._clamp_resource(value, 0, self._food_cap)
            return self._food_used

        # 其他状态存入字典
        self._state_data[state_type] = value
        return value
```

## PlayerState 常量映射

| 常量名 | 值 | 说明 |
|--------|-----|------|
| PLAYER_STATE_GAME_RESULT | 0 | 游戏结果 |
| PLAYER_STATE_RESOURCE_GOLD | 1 | 金币 |
| PLAYER_STATE_RESOURCE_LUMBER | 2 | 木材 |
| PLAYER_STATE_RESOURCE_HERO_TOKENS | 3 | 英雄令牌 |
| PLAYER_STATE_RESOURCE_FOOD_CAP | 4 | 食物上限 |
| PLAYER_STATE_RESOURCE_FOOD_USED | 5 | 已用食物 |
| PLAYER_STATE_FOOD_CAP_CEILING | 6 | 食物上限天花板 |
| PLAYER_STATE_GIVES_BOUNTY | 7 | 提供赏金 |
| PLAYER_STATE_ALLIED_VICTORY | 8 | 联盟胜利 |
| PLAYER_STATE_PLACED | 9 | 已放置 |
| PLAYER_STATE_OBSERVER_ON_DEATH | 10 | 死亡时观察 |
| PLAYER_STATE_OBSERVER | 11 | 观察者 |
| PLAYER_STATE_UNFOLLOWABLE | 12 | 不可跟随 |
| PLAYER_STATE_GOLD_UPKEEP_RATE | 13 | 金币维护费率 |
| PLAYER_STATE_LUMBER_UPKEEP_RATE | 14 | 木材维护费率 |
| PLAYER_STATE_GOLD_GATHERED | 15 | 已收集金币 |
| PLAYER_STATE_LUMBER_GATHERED | 16 | 已收集木材 |
| PLAYER_STATE_NO_CREEP_SLEEP | 25 | 野怪不睡眠 |

## Native 函数设计

### ConvertPlayerState

- **函数签名**: `takes integer i returns playerstate`
- **参数**: `i` - 整数 0-16, 25
- **返回**: `int`（直接返回传入的整数）
- **日志**: `[ConvertPlayerState] 转换玩家状态类型: {i}`

### GetPlayerState（扩展）

- **函数签名**: `takes player whichPlayer, playerstate whichPlayerState returns integer`
- **行为**:
  - 资源类状态（1, 2, 4, 5）使用现有属性
  - 其他状态从 `_state_data` 字典读取

### SetPlayerState（扩展）

- **函数签名**: `takes player whichPlayer, playerstate whichPlayerState, integer value returns nothing`
- **行为**:
  - 资源类状态（1, 2, 4, 5）使用现有属性和截断逻辑
  - 其他状态直接存入 `_state_data` 字典

## 文件结构

```
src/jass_runner/natives/
├── handle.py                # 修改：扩展 Player 类
├── player_state_natives.py  # 修改：添加 ConvertPlayerState
├── factory.py               # 修改：注册 ConvertPlayerState

src/jass_runner/vm/
├── jass_vm.py               # 修改：添加 playerstate 类型常量解析
```

## 常量解析扩展

在 `jass_vm.py` 的 `_convert_constant_value` 方法中添加：

```python
elif const_type == 'playerstate':
    # 处理 ConvertPlayerState(0) 格式的函数调用
    try:
        import re
        match = re.search(r'ConvertPlayerState\((\d+)\)', const_value)
        if match:
            return int(match.group(1))
        else:
            return int(const_value)
    except (ValueError, AttributeError):
        return 0
```

## 测试策略

### 单元测试

1. **ConvertPlayerState** - 测试返回传入的整数
2. **GetPlayerState 资源状态** - 测试现有资源状态仍正常工作
3. **SetPlayerState 资源状态** - 测试资源状态设置和截断
4. **GetPlayerState 非资源状态** - 测试从字典读取状态
5. **SetPlayerState 非资源状态** - 测试向字典写入状态

### 集成测试（必须包含 ConvertPlayerState 调用作为参数）

```python
def test_convert_player_state_as_parameter(self):
    """测试 ConvertPlayerState 调用结果作为函数参数。"""
    jass_code = '''
function main takes nothing returns nothing
    local player p = Player(0)

    // 使用 ConvertPlayerState 返回值作为 SetPlayerState 参数
    call SetPlayerState(p, ConvertPlayerState(25), 1)

    // 使用 ConvertPlayerState 返回值作为 GetPlayerState 参数
    if GetPlayerState(p, ConvertPlayerState(25)) == 1 then
        call DisplayTextToPlayer(p, 0, 0, "No creep sleep enabled")
    endif
endfunction
'''
    vm = JassVM()
    vm.run(jass_code)  # 应成功执行
```

### 常量验证测试

```python
def test_player_state_constants_are_integers(self):
    """测试 playerstate 常量被正确解析为整数。"""
    vm = JassVM()

    # 检查 PLAYER_STATE_NO_CREEP_SLEEP 被解析为整数 25
    assert vm.interpreter.global_context.variables.get('PLAYER_STATE_NO_CREEP_SLEEP') == 25

    # 检查其他常量
    assert vm.interpreter.global_context.variables.get('PLAYER_STATE_RESOURCE_GOLD') == 1
    assert vm.interpreter.global_context.variables.get('PLAYER_STATE_OBSERVER') == 11
```

## 实现注意事项

1. **中文注释**: 所有代码必须使用中文注释
2. **向后兼容**: 现有资源状态逻辑保持不变
3. **日志输出**: 使用 logging 模块，信息级别为 INFO
4. **错误处理**: None player 检查保持不变
