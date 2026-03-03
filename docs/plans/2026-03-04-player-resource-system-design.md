# 玩家资源系统设计方案

## 概述

本文档描述 JASS Runner 中玩家资源系统的实现方案。玩家资源系统用于管理魔兽争霸 III 中玩家的核心资源状态。

## 设计目标

1. 实现玩家资源管理（黄金、木材、人口）
2. 支持 `GetPlayerState` 和 `SetPlayerState` native 函数
3. 资源值超出范围时自动截断到边界
4. 保持与现有 Player 类的一致性

## 核心架构

### Player 类扩展

在 `src/jass_runner/natives/handle.py` 的 Player 类中添加资源属性：

```python
class Player(Handle):
    """玩家句柄，管理玩家状态和资源。"""

    def __init__(self, player_id: int, ...):
        # 已有属性...

        # 资源属性（最小集）
        self._gold: int = 500         # 黄金 0-1000000，初始500
        self._lumber: int = 0         # 木材 0-1000000，初始0
        self._food_cap: int = 100     # 人口上限 0-300，初始100
        self._food_used: int = 0      # 已用人口 0-food_cap，初始0
```

### 资源管理方法

```python
def get_state(self, state_type: int) -> int:
    """获取玩家状态值（供 GetPlayerState 调用）。"""

def set_state(self, state_type: int, value: int) -> int:
    """设置玩家状态值（供 SetPlayerState 调用）。

    参数：
        state_type: 状态类型（PLAYER_STATE_RESOURCE_*）
        value: 要设置的值

    返回：
        实际设置的值（超出范围时自动截断到边界）
    """

def _clamp_resource(self, value: int, min_val: int, max_val: int) -> int:
    """将值截断到有效范围。"""
    return max(min_val, min(value, max_val))
```

## Native 函数设计

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `GetPlayerState` | `whichPlayer: player, whichPlayerState: int` | `int` | 获取玩家状态 |
| `SetPlayerState` | `whichPlayer: player, whichPlayerState: int, value: int` | `int` | 设置玩家状态（返回实际设置的值） |

## 状态类型常量

```python
PLAYER_STATE_RESOURCE_GOLD = 1
PLAYER_STATE_RESOURCE_LUMBER = 2
PLAYER_STATE_RESOURCE_FOOD_CAP = 4
PLAYER_STATE_RESOURCE_FOOD_USED = 5
```

## 边界处理

```python
# 资源范围定义
GOLD_RANGE = (0, 1000000)       # 0-100万
LUMBER_RANGE = (0, 1000000)     # 0-100万
FOOD_CAP_RANGE = (0, 300)       # 0-300
FOOD_USED_RANGE = (0, food_cap) # 动态上限
```

## 文件结构

```
src/jass_runner/natives/
├── handle.py                  # 修改：添加资源属性
└── player_state_natives.py    # 新增：GetPlayerState, SetPlayerState

tests/natives/
├── test_player_state.py       # 新增：资源功能测试
└── test_player_natives.py     # 新增：native函数测试

tests/integration/
└── test_player_system.py      # 新增：集成测试
```

## 测试计划

### 单元测试

- `test_get_gold` - 获取黄金值
- `test_set_gold` - 设置黄金值
- `test_set_gold_clamp_max` - 黄金值超出上限时截断
- `test_set_gold_clamp_min` - 黄金值为负时截断为0
- `test_get_lumber` - 获取木材值
- `test_set_lumber` - 设置木材值
- `test_get_food_cap` - 获取人口上限
- `test_set_food_cap` - 设置人口上限
- `test_get_food_used` - 获取已用人口
- `test_set_food_used` - 设置已用人口

### 集成测试

- 完整资源操作流程（获取→设置→验证）
- 边界截断场景测试

## 设计决策

### 为什么选择最小集？

1. 黄金、木材、人口是游戏中最核心的资源
2. 与单位系统紧密相关（训练单位需要资源）
3. 实现简单，功能明确

### 为什么使用截断模式？

1. 与魔兽争霸 III 的行为一致
2. 避免异常中断游戏流程
3. 调用者可以通过返回值了解实际设置的值

### 为什么初始值为 gold=500, lumber=0？

1. 符合标准对战开局设定
2. 足够建造初始建筑
3. 需要采集获得木材

## 参考

- 项目编码规范：`CLAUDE.md`
- 物品系统实现：`docs/plans/2026-03-03-item-system-design.md`
