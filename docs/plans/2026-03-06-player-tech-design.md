# 玩家科技系统设计文档

## 概述

本文档描述JASS Runner中玩家科技系统的设计，包括6个native函数的实现方案。

## 背景

根据common.j第1702-1707行，需要实现以下6个native函数：

```jass
constant native SetPlayerTechMaxAllowed takes player whichPlayer, integer techid, integer maximum returns nothing
constant native GetPlayerTechMaxAllowed takes player whichPlayer, integer techid returns integer
constant native AddPlayerTechResearched takes player whichPlayer, integer techid, integer levels returns nothing
constant native SetPlayerTechResearched takes player whichPlayer, integer techid, integer setToLevel returns nothing
constant native GetPlayerTechResearched takes player whichPlayer, integer techid, boolean specificonly returns boolean
constant native GetPlayerTechCount      takes player whichPlayer, integer techid, boolean specificonly returns integer
```

## 设计决策

### TechId格式

使用**FourCC整数格式**（如'Hpal'→1214542384），与单位类型ID一致。

### 等级限制

**无限制**，允许任意等级。`SetPlayerTechMaxAllowed`可以设置任意值。

### GetPlayerTechResearched语义

当研究等级**大于0时返回true**，表示该科技已被研究过。

## 架构设计

### Player类修改

在`Player`类中添加两个字典存储科技状态：

```python
self._tech_max_allowed: Dict[int, int] = {}  # techid -> 最大允许等级
self._tech_researched: Dict[int, int] = {}   # techid -> 当前研究等级
```

添加以下方法：

| 方法 | 功能 |
|------|------|
| `set_tech_max_allowed(techid, maximum)` | 设置科技最大允许等级 |
| `get_tech_max_allowed(techid)` | 获取科技最大允许等级（默认0） |
| `add_tech_researched(techid, levels)` | 增加科技研究等级 |
| `set_tech_researched(techid, level)` | 设置科技研究等级 |
| `get_tech_researched(techid, specificonly)` | 获取科技是否已研究（等级>0返回True） |
| `get_tech_count(techid, specificonly)` | 获取科技当前研究等级 |

### Native函数实现

新建文件`src/jass_runner/natives/player_tech_natives.py`，实现6个native函数类：

1. **SetPlayerTechMaxAllowed**
   - 参数：`player`, `techid`, `maximum`
   - 功能：设置指定科技的最大允许等级
   - 日志：记录设置操作

2. **GetPlayerTechMaxAllowed**
   - 参数：`player`, `techid`
   - 返回：最大允许等级（未设置返回0）
   - 日志：记录查询操作

3. **AddPlayerTechResearched**
   - 参数：`player`, `techid`, `levels`
   - 功能：增加指定科技的研究等级
   - 日志：记录增加操作

4. **SetPlayerTechResearched**
   - 参数：`player`, `techid`, `setToLevel`
   - 功能：设置指定科技的研究等级
   - 日志：记录设置操作

5. **GetPlayerTechResearched**
   - 参数：`player`, `techid`, `specificonly`
   - 返回：是否已研究（等级>0返回True）
   - 日志：记录查询操作

6. **GetPlayerTechCount**
   - 参数：`player`, `techid`, `specificonly`
   - 返回：当前研究等级（整数）
   - 日志：记录查询操作

### 工厂注册

在`NativeFactory.create_default_registry()`中注册这6个函数。

## 测试策略

### 单元测试

创建`tests/natives/test_player_tech_natives.py`：

- 每个native函数单独测试
- 边界条件测试：None player、无效techid
- 正常功能测试

### 集成测试

创建`tests/integration/test_player_tech_integration.py`：

- 完整科技升级流程测试
- 多玩家科技独立测试
- 与现有Player系统集成测试

## 文件变更清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `src/jass_runner/natives/player.py` | 修改 | 添加科技相关属性和方法 |
| `src/jass_runner/natives/player_tech_natives.py` | 新建 | 6个native函数实现 |
| `src/jass_runner/natives/factory.py` | 修改 | 注册新函数 |
| `tests/natives/test_player_tech_natives.py` | 新建 | 单元测试 |
| `tests/integration/test_player_tech_integration.py` | 新建 | 集成测试 |

## 示例用法

```jass
function TestPlayerTech takes nothing returns nothing
    local player p = Player(0)
    local integer techId = 'Hpal'  // 圣骑士

    // 设置科技最大允许等级为3
    call SetPlayerTechMaxAllowed(p, techId, 3)

    // 研究科技2级
    call AddPlayerTechResearched(p, techId, 2)

    // 检查是否已研究
    if GetPlayerTechResearched(p, techId, false) then
        call DisplayTextToPlayer(p, 0, 0, "科技已研究")
    endif

    // 获取当前等级
    call DisplayTextToPlayer(p, 0, 0, "当前等级: " + I2S(GetPlayerTechCount(p, techId, false)))
endfunction
```

## 注意事项

1. **specificonly参数**：当前实现中忽略此参数，直接返回等级信息。如需支持特定科技查询，可后续扩展。
2. **线程安全**：Player类的科技操作非线程安全，在单线程解释器环境中使用。
3. **持久化**：当前科技状态存储在内存中，重启后重置。

---

*设计日期: 2026-03-06*
