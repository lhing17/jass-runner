# 单位操作 Native API 扩展设计文档

> **设计目标**: 扩展单位操作相关 native 函数，支持单位生命周期管理、属性访问与修改、位置控制

---

## 1. 当前实现状态

| 函数 | 状态 | 说明 |
|------|------|------|
| CreateUnit | ✅ 已实现 | 使用 x, y 坐标创建单位 |
| KillUnit | ✅ 已实现 | 通过 HandleManager 销毁单位 |
| GetUnitState | ✅ 已实现 | 支持 LIFE/MAX_LIFE/MANA/MAX_MANA 查询 |
| Unit handle | ✅ 已存在 | 包含 x, y, facing, life, mana 等属性 |

---

## 2. 架构设计

### 2.1 Location 类

```python
class Location:
    """位置类，包含 x, y, z 坐标（z 默认为 0）"""
    x: float
    y: float
    z: float = 0  # 高度，默认为 0，为未来扩展预留
```

**设计说明**:
- z 坐标默认值为 0，保持向后兼容
- 简单实现，不包含地形碰撞检测
- 可通过 Location 对象统一管理位置信息

### 2.2 Unit 类扩展

在现有 `Unit` 类基础上添加：
- `z: float = 0` - Z 轴高度
- `name: str` - 单位名称（可选，用于 GetUnitName）

### 2.3 新增 Native 函数模块

- `unit_property_natives.py` - 单位属性访问与修改
- `unit_position_natives.py` - 单位位置相关操作

---

## 3. Native 函数清单

### 3.1 阶段 1：状态管理补充

| 函数 | 签名 | 说明 |
|------|------|------|
| SetUnitState | `takes unit whichUnit, unitstate whichUnitState, real newVal returns nothing` | 设置单位状态（生命/魔法值） |

### 3.2 阶段 2：位置操作

| 函数 | 签名 | 说明 |
|------|------|------|
| GetUnitX | `takes unit whichUnit returns real` | 获取单位 X 坐标 |
| GetUnitY | `takes unit whichUnit returns real` | 获取单位 Y 坐标 |
| GetUnitLoc | `takes unit whichUnit returns location` | 获取单位位置（Location 对象） |
| SetUnitPosition | `takes unit whichUnit, real newX, real newY returns nothing` | 设置单位位置 |
| SetUnitPositionLoc | `takes unit whichUnit, location whichLocation returns nothing` | 使用 Location 设置位置 |
| CreateUnitAtLoc | `takes player id, integer unitid, location whichLocation, real face returns unit` | 在指定位置创建单位 |

### 3.3 阶段 3：朝向控制

| 函数 | 签名 | 说明 |
|------|------|------|
| GetUnitFacing | `takes unit whichUnit returns real` | 获取单位朝向角度 |
| SetUnitFacing | `takes unit whichUnit, real facingAngle returns nothing` | 设置单位朝向 |
| SetUnitFacingTimed | `takes unit whichUnit, real facingAngle, real duration returns nothing` | 带过渡动画的朝向设置 |

### 3.4 阶段 4：单位信息

| 函数 | 签名 | 说明 |
|------|------|------|
| GetUnitTypeId | `takes unit whichUnit returns integer` | 获取单位类型 ID |
| GetUnitName | `takes unit whichUnit returns string` | 获取单位名称 |
| CreateUnitAtLocByName | `takes player id, string unitname, location whichLocation, real face returns unit` | 按名称创建单位 |

---

## 4. 状态常量

```python
# 单位状态类型常量（与 common.j 保持一致）
UNIT_STATE_LIFE = 0          # 当前生命值
UNIT_STATE_MAX_LIFE = 1      # 最大生命值
UNIT_STATE_MANA = 2          # 当前魔法值
UNIT_STATE_MAX_MANA = 3      # 最大魔法值
```

---

## 5. 测试策略

### 5.1 单元测试

每个 native 函数独立测试：
- 正常输入的返回值验证
- 边界条件（None 单位、无效状态类型）
- 副作用验证（Set 操作后 Get 验证）

### 5.2 集成测试

完整工作流测试：
```
CreateUnit -> GetUnitState -> SetUnitState -> GetUnitX/Y ->
SetUnitPosition -> GetUnitFacing -> SetUnitFacing -> KillUnit
```

### 5.3 Location 类测试

- 创建 Location 对象（含 z 坐标）
- 与 Unit 位置同步
- CreateUnitAtLoc 使用 Location

---

## 6. 实施阶段

| 阶段 | 内容 | 预计函数数 |
|------|------|-----------|
| 1 | Location 类 + SetUnitState | 2 |
| 2 | 位置函数（GetUnitX/Y/Loc, SetUnitPosition, CreateUnitAtLoc） | 5 |
| 3 | 朝向函数（Get/Set UnitFacing） | 3 |
| 4 | 单位信息查询（GetUnitTypeId, GetUnitName, CreateUnitAtLocByName） | 3 |

**总计：约 13 个 native 函数**

---

## 7. 依赖关系

```
Location 类
    ├── GetUnitLoc
    ├── SetUnitPositionLoc
    └── CreateUnitAtLoc

SetUnitState
    └── 需要 HandleManager 支持设置单位状态

位置函数
    └── 依赖 Location 类
```

---

## 8. 风险与注意事项

1. **与现有 CreateUnit 兼容**: 新函数不应破坏现有功能
2. **HandleManager 扩展**: 需要添加 `set_unit_state` 方法
3. **Location 对象生命周期**: 考虑是否需要销毁 Location 对象（当前设计为轻量级值对象，无需销毁）

---

*设计日期: 2026-03-02*
*设计状态: 已确认*
