# Fog Native 函数设计文档

## 概述

实现魔兽争霸III战争迷雾（Fog of War）相关的 native 函数，用于控制迷雾显示和查询迷雾状态。

## 背景

在 `resources/common.j` 第1727-1728行定义了以下 native 函数：

```jass
native FogMaskEnable takes boolean enable returns nothing
native FogEnable   takes boolean enable returns nothing
native IsFogMaskEnabled takes nothing returns boolean
native IsFogEnabled   takes nothing returns boolean
```

注意：`FogMaskEnableOff` 和 `FogEnableOff` 是在 `blizzard.j` 中通过调用 `FogMaskEnable(false)` 和 `FogEnable(false)` 实现的包装函数，不属于 native 函数，无需在 native 层实现。

## 设计决策

### 架构选择

采用**独立模块方案（方案A）**：
- 创建独立的 `fog_natives.py` 文件
- 与 camera 模块解耦，职责清晰
- 便于后续扩展其他 Fog 相关功能

### 状态管理

```python
class FogState:
    mask_enabled: bool   # 黑色遮罩（未探索区域显示黑色）
    fog_enabled: bool    # 战争迷雾
```

默认状态：两者均为 `True`（启用）

### 实现细节

**Native 函数列表**：

| 函数名 | 参数 | 返回值 | 功能 |
|--------|------|--------|------|
| `FogMaskEnable` | `boolean enable` | `nothing` | 启用/禁用黑色遮罩 |
| `FogEnable` | `boolean enable` | `nothing` | 启用/禁用战争迷雾 |
| `IsFogMaskEnabled` | `nothing` | `boolean` | 查询黑色遮罩状态 |
| `IsFogEnabled` | `nothing` | `boolean` | 查询战争迷雾状态 |

**日志输出格式**：
```
[Fog] 黑色遮罩状态: 启用
[Fog] 战争迷雾状态: 禁用
```

## 文件变更

### 新增文件
- `src/jass_runner/natives/fog_natives.py` - Fog native 函数实现

### 修改文件
- `src/jass_runner/natives/factory.py` - 注册新 native 函数

## 测试策略

1. **单元测试**：测试每个 native 函数的行为
2. **状态测试**：验证状态切换和查询的正确性
3. **日志测试**：验证日志输出格式

## 实现检查清单

- [ ] 创建 `fog_natives.py` 实现 FogState 和 native 函数类
- [ ] 在 `factory.py` 中注册 native 函数
- [ ] 编写单元测试
- [ ] 验证所有测试通过
