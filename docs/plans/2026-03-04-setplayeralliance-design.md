# SetPlayerAlliance Native 函数设计文档

## 概述

实现魔兽争霸3 JASS 中的玩家联盟系统相关 native 函数，包括：
- `ConvertAllianceType` - 将整数转换为联盟类型
- `SetPlayerAlliance` - 设置两个玩家之间的联盟关系
- `GetPlayerAlliance` - 获取两个玩家之间的联盟关系状态

## 背景

在 Warcraft 3 JASS 中，联盟系统允许玩家之间建立各种关系，如：
- `ALLIANCE_PASSIVE` - 单位不会自动攻击对方
- `ALLIANCE_SHARED_VISION` - 共享视野
- `ALLIANCE_SHARED_CONTROL` - 共享单位控制
- 等等

这些联盟类型在 `common.j` 中定义为：
```jass
constant alliancetype ALLIANCE_PASSIVE = ConvertAllianceType(0)
constant alliancetype ALLIANCE_SHARED_VISION = ConvertAllianceType(5)
```

## 设计目标

1. 支持 `common.j` 中定义的联盟类型常量
2. 维护玩家之间的联盟关系数据结构
3. 提供清晰的日志输出用于调试
4. 暂不实现联盟关系对游戏逻辑的实际影响

## 架构设计

### 核心组件

```
┌─────────────────────────────────────────────────────────┐
│                    AllianceManager                       │
├─────────────────────────────────────────────────────────┤
│  职责：集中管理所有玩家之间的联盟关系                       │
├─────────────────────────────────────────────────────────┤
│  _alliances: Dict[Tuple[int, int], Set[int]]            │
│  - key: (source_player_id, other_player_id)             │
│  - value: 已启用的联盟类型整数集合                        │
└─────────────────────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ConvertAlliance│ │SetPlayer     │ │GetPlayer     │
│Type          │ │Alliance      │ │Alliance      │
└──────────────┘ └──────────────┘ └──────────────┘
```

### AllianceManager 职责

- `set_alliance(source, other, alliance_type, value)` - 设置/取消联盟关系
- `get_alliance(source, other, alliance_type)` - 查询特定联盟类型状态
- `get_all_alliances(source, other)` - 获取所有已启用的联盟类型

## 数据结构设计

### 联盟类型常量

与 `common.j` 对应：

| 常量名 | 值 | 描述 |
|--------|-----|------|
| ALLIANCE_PASSIVE | 0 | 单位不会自动攻击 |
| ALLIANCE_HELP_REQUEST | 1 | 可以请求帮助 |
| ALLIANCE_HELP_RESPONSE | 2 | 会响应帮助请求 |
| ALLIANCE_SHARED_XP | 3 | 共享经验值 |
| ALLIANCE_SHARED_SPELLS | 4 | 共享法术效果 |
| ALLIANCE_SHARED_VISION | 5 | 共享视野 |
| ALLIANCE_SHARED_CONTROL | 6 | 共享单位控制 |
| ALLIANCE_SHARED_ADVANCED_CONTROL | 7 | 共享高级控制 |
| ALLIANCE_RESCUABLE | 8 | 单位可被救援 |
| ALLIANCE_SHARED_VISION_FORCED | 9 | 强制共享视野 |

### 存储示例

```python
_alliances = {
    # (source_id, other_id): {alliance_types}
    (0, 1): {0, 5},      # 玩家0对玩家1: PASSIVE + SHARED_VISION
    (1, 0): {0, 5},      # 玩家1对玩家0: PASSIVE + SHARED_VISION（双向联盟）
    (0, 2): {0},         # 玩家0对玩家2: 仅 PASSIVE（单向）
    (2, 0): set(),       # 玩家2对玩家0: 无联盟
}
```

## Native 函数设计

### ConvertAllianceType

- **函数签名**: `takes integer i returns alliancetype`
- **参数**: `i` - 整数 0-9
- **返回**: `int`（直接返回传入的整数）
- **日志**: `[ConvertAllianceType] 转换联盟类型: {i}`

### SetPlayerAlliance

- **函数签名**: `takes player sourcePlayer, player otherPlayer, alliancetype whichAllianceSetting, boolean value returns nothing`
- **参数**:
  - `sourcePlayer` - 源玩家（谁的联盟设置）
  - `otherPlayer` - 目标玩家（对谁的关系）
  - `whichAllianceSetting` - 联盟类型（整数 0-9）
  - `value` - `true` 启用, `false` 禁用
- **日志**: `[SetPlayerAlliance] 玩家{source} 对 玩家{other} 设置 {alliance_name}={value}`

### GetPlayerAlliance

- **函数签名**: `takes player sourcePlayer, player otherPlayer, alliancetype whichAllianceSetting returns boolean`
- **参数**:
  - `sourcePlayer` - 源玩家
  - `otherPlayer` - 目标玩家
  - `whichAllianceSetting` - 联盟类型
- **返回**: `bool` - 该联盟类型是否启用
- **日志**: `[GetPlayerAlliance] 玩家{source} 对 玩家{other} 的 {alliance_name}={result}`

## 文件结构

```
src/jass_runner/natives/
├── alliance.py              # 联盟类型常量定义
├── alliance_manager.py      # AllianceManager 类
├── alliance_natives.py      # native 函数实现
├── factory.py               # 修改：注册新的 native 函数
```

## 错误处理

- 如果 `sourcePlayer` 或 `otherPlayer` 为 `None`，记录警告日志并返回默认值
- 如果 `alliance_type` 超出有效范围，仍然接受但记录警告（保持与 War3 兼容性）

## 测试策略

### 单元测试

1. **ConvertAllianceType** - 测试整数直接返回
2. **SetPlayerAlliance** - 测试设置后状态正确存储
3. **GetPlayerAlliance** - 测试读取正确的联盟状态
4. **多类型设置** - 测试同一对玩家可以设置多个联盟类型
5. **独立性** - 测试不同玩家对之间的独立性
6. **边界情况** - 测试 None player 的处理

### 集成测试

测试完整流程：
```jass
call SetPlayerAlliance(Player(0), Player(1), ALLIANCE_PASSIVE, true)
set b = GetPlayerAlliance(Player(0), Player(1), ALLIANCE_PASSIVE)
// 期望 b = true
```

## 实现注意事项

1. **中文注释**: 所有代码必须使用中文注释
2. **日志输出**: 使用 logging 模块，信息级别为 INFO
3. **代码行数**: 每个文件不超过 500 行，每个函数不超过 200 行
4. **注册**: 在 `NativeFactory.create_default_registry()` 中注册三个新 native 函数

## 后续扩展

当前设计仅维护联盟关系数据，未来可以扩展：
- 根据 `ALLIANCE_PASSIVE` 控制单位自动攻击行为
- 根据 `ALLIANCE_SHARED_VISION` 共享视野信息
- 根据 `ALLIANCE_SHARED_CONTROL` 允许控制对方单位
