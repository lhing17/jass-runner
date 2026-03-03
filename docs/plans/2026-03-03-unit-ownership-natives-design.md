# 单位所有权与关系Native函数设计文档

## 概述

本文档描述JASS Runner第五批Native函数的实现设计，包括单位所有权管理和单位范围检测功能。

## 背景

当前项目已实现85个Native函数，涵盖触发器系统、数学函数、单位属性、单位组、技能系统等。本批函数补充单位所有权变更和玩家关系检测能力。

## 目标

实现7个Native函数：
1. `SetUnitOwner` - 变更单位所属玩家
2. `IsUnitOwnedByPlayer` - 检查单位是否属于指定玩家
3. `IsUnitAlly` - 检查单位所属玩家与指定玩家是否盟友
4. `IsUnitEnemy` - 检查单位所属玩家与指定玩家是否敌对
5. `IsUnitInRange` - 检查单位是否在另一单位指定距离内
6. `IsUnitInRangeXY` - 检查单位是否在指定坐标指定距离内
7. `IsUnitInRangeLoc` - 检查单位是否在指定位置指定距离内

## 架构设计

### 1. 玩家关系系统扩展

**Player类扩展** (`src/jass_runner/handles/player.py`):

```python
class Player(Handle):
    def __init__(self, player_id: int):
        super().__init__()
        self.player_id = player_id
        self._allies: Set[int] = set()  # 盟友玩家ID集合
        self._enemies: Set[int] = set()  # 敌人玩家ID集合

    def set_alliance(self, other_player_id: int, is_ally: bool) -> None:
        """设置与其他玩家的关系。"""
        if is_ally:
            self._allies.add(other_player_id)
            self._enemies.discard(other_player_id)
        else:
            self._enemies.add(other_player_id)
            self._allies.discard(other_player_id)

    def is_ally(self, other_player_id: int) -> bool:
        """检查是否是指定玩家的盟友。"""
        return other_player_id in self._allies

    def is_enemy(self, other_player_id: int) -> bool:
        """检查是否是指定玩家的敌人。"""
        return other_player_id in self._enemies
```

**设计决策**:
- 使用集合存储关系，查询时间复杂度O(1)
- 盟友和敌人互斥，设置一方时移除另一方
- 默认无关系（非盟友也非敌人）

### 2. 新增Native函数模块

#### 2.1 单位所有权模块 (`unit_ownership_natives.py`)

**SetUnitOwner**:
- 参数: `whichUnit: Unit`, `whichPlayer: Player`, `changeColor: bool`
- 功能: 变更单位所属玩家
- 实现: 更新`unit.player_id`，如`changeColor`为True记录日志

**IsUnitOwnedByPlayer**:
- 参数: `whichUnit: Unit`, `whichPlayer: Player`
- 返回: `boolean`
- 实现: 比较`unit.player_id == player.player_id`

**IsUnitAlly**:
- 参数: `whichUnit: Unit`, `whichPlayer: Player`
- 返回: `boolean`
- 实现: 通过`HandleManager`获取单位所属玩家，检查盟友关系

**IsUnitEnemy**:
- 参数: `whichUnit: Unit`, `whichPlayer: Player`
- 返回: `boolean`
- 实现: 通过`HandleManager`获取单位所属玩家，检查敌对关系

#### 2.2 单位范围检测模块 (`unit_range_natives.py`)

**IsUnitInRangeXY**:
- 参数: `whichUnit: Unit`, `x: real`, `y: real`, `distance: real`
- 返回: `boolean`
- 实现: 计算欧几里得距离 `sqrt((ux-x)^2 + (uy-y)^2) <= distance`

**IsUnitInRange**:
- 参数: `whichUnit: Unit`, `otherUnit: Unit`, `distance: real`
- 返回: `boolean`
- 实现: 获取`otherUnit`坐标，调用`IsUnitInRangeXY`逻辑

**IsUnitInRangeLoc**:
- 参数: `whichUnit: Unit`, `whichLocation: Location`, `distance: real`
- 返回: `boolean`
- 实现: 获取`Location`坐标，调用`IsUnitInRangeXY`逻辑

### 3. 辅助函数

**HandleManager扩展**:
- `get_player_by_id(player_id: int) -> Optional[Player]` - 通过ID获取玩家对象

## 错误处理

- 参数为`null`时返回默认值（`false`对于布尔函数）
- 距离为负数时视为0
- 单位已死亡时范围检测返回`false`

## 测试策略

1. **单元测试**: 每个Native函数独立测试
2. **集成测试**: 完整工作流程测试（创建单位->变更所有权->检测关系->范围检测）
3. **边界测试**: null参数、死亡单位、负距离等边界情况

## 集成点

1. **NativeFactory**: 注册所有新函数到默认注册表
2. **HandleManager**: 扩展玩家管理方法
3. **Player类**: 添加关系管理属性

## 实施顺序

1. Player类扩展（添加关系管理）
2. HandleManager扩展（玩家查询方法）
3. IsUnitOwnedByPlayer（最简单）
4. IsUnitInRangeXY（基础距离计算）
5. IsUnitInRangeLoc（复用XY逻辑）
6. IsUnitInRange（复用XY逻辑）
7. SetUnitOwner（需要修改单位属性）
8. IsUnitAlly/IsUnitEnemy（需要关系系统）
9. 集成测试和工厂注册

---
*设计日期: 2026-03-03*
*版本: v0.5.0*
