# JASS触发器系统设计文档

**日期**: 2026-02-28
**主题**: 触发器系统（Trigger System）实现设计
**决策**: 采用方案C（混合架构）

---

## 1. 概述

### 1.1 背景

JASS触发器系统是魔兽争霸III地图开发中的核心机制，允许开发者定义事件驱动逻辑：
- **事件**（Events）：如单位死亡、计时器到期、游戏开始等
- **条件**（Conditions）：可选的过滤器决定是否执行动作
- **动作**（Actions）：事件发生时执行的代码

### 1.2 目标

实现完整的JASS触发器系统支持，包括：
- 20个核心native函数（生命周期管理、事件注册、动作/条件管理）
- 12个标准事件类型（单位事件、玩家事件、游戏事件、计时器事件）
- 与现有计时器系统和native函数框架无缝集成
- 支持条件评估和动作执行的完整流程

---

## 2. 架构设计

### 2.1 方案选择：混合架构（方案C）

**设计原则**：
- 与现有`TimerSystem`和`Handle`系统风格一致
- 保持架构灵活性的同时避免过度复杂
- 在关键native函数（KillUnit、CreateUnit等）中直接触发事件

**决策理由**：
- `TimerSystem`已证明此架构有效且易于维护
- 不需要事件总线模式的额外复杂性
- 便于在现有代码中逐步添加事件触发点

### 2.2 目录结构

```
src/jass_runner/trigger/
├── __init__.py              # 导出Trigger, TriggerManager等
├── trigger.py               # Trigger类：事件、条件、动作的容器
├── manager.py               # TriggerManager：生命周期管理
├── event_types.py           # 事件类型定义（EVENT_PLAYER_UNIT_DEATH等）
└── native_hooks.py          # 触发事件的native函数钩子

src/jass_runner/natives/trigger_natives.py  # 触发器相关native函数
```

---

## 3. 核心组件

### 3.1 Trigger 类

**职责**：单个触发器的完整状态管理

**属性**：
- `trigger_id`: 唯一标识符（UUID）
- `events`: 注册的事件列表（事件类型+过滤条件）
- `conditions`: 条件函数引用列表
- `actions`: 动作函数引用列表
- `enabled`: 布尔值，是否启用

**方法**：
- `add_action(action_func)` → action_handle
- `remove_action(action_handle)` → boolean
- `add_condition(condition_func)` → condition_handle
- `remove_condition(condition_handle)` → boolean
- `evaluate_conditions(state_context)` → boolean（评估所有条件）
- `execute_actions(state_context)` → 执行所有动作
- `register_event(event_type, filter_data)` → event_handle
- `clear_events()` → 清空所有事件

**行数预算**：~80行

### 3.2 TriggerManager 类

**职责**：管理所有触发器生命周期，分发事件

**属性**：
- `_triggers`: Dict[str, Trigger] 所有触发器映射
- `_event_index`: Dict[event_type, List[trigger_ids]] 事件到触发器的索引
- `_global_enabled`: boolean 全局启用状态

**方法**：
- `create_trigger()` → trigger_id
- `destroy_trigger(trigger_id)` → boolean
- `enable_trigger(trigger_id)` → boolean
- `disable_trigger(trigger_id)` → boolean
- `is_trigger_enabled(trigger_id)` → boolean
- `register_event(trigger_id, event_type, filter_data)` → event_handle
- `clear_trigger_events(trigger_id)` → boolean
- `fire_event(event_type, event_data)` → 触发匹配的事件处理器
- `get_trigger(trigger_id)` → Trigger|None

**分发逻辑**：
1. 根据 event_type 查询 `_event_index` 获取候选触发器列表
2. 对每个候选触发器：
   - 检查 `enabled` 状态，跳过禁用的
   - 调用 `evaluate_conditions()`，任一条件失败则跳过
   - 调用 `execute_actions()` 执行动作

**行数预算**：~120行

### 3.3 EventTypes 常量定义

**文件**：`src/jass_runner/trigger/event_types.py`

**事件分类**：

```python
# 玩家-单位事件 (EVENT_PLAYER_UNIT_*)
EVENT_PLAYER_UNIT_DEATH = "EVENT_PLAYER_UNIT_DEATH"
EVENT_PLAYER_UNIT_ATTACKED = "EVENT_PLAYER_UNIT_ATTACKED"
EVENT_PLAYER_UNIT_RESCUED = "EVENT_PLAYER_UNIT_RESCUED"
EVENT_PLAYER_UNIT_DAMAGED = "EVENT_PLAYER_UNIT_DAMAGED"
EVENT_PLAYER_UNIT_PICKUP_ITEM = "EVENT_PLAYER_UNIT_PICKUP_ITEM"
EVENT_PLAYER_UNIT_DROP_ITEM = "EVENT_PLAYER_UNIT_DROP_ITEM"
EVENT_PLAYER_UNIT_USE_ITEM = "EVENT_PLAYER_UNIT_USE_ITEM"

# 通用单位事件 (EVENT_UNIT_*)
EVENT_UNIT_DEATH = "EVENT_UNIT_DEATH"
EVENT_UNIT_DAMAGED = "EVENT_UNIT_DAMAGED"

# 玩家事件 (EVENT_PLAYER_*)
EVENT_PLAYER_DEFEAT = "EVENT_PLAYER_DEFEAT"
EVENT_PLAYER_VICTORY = "EVENT_PLAYER_VICTORY"
EVENT_PLAYER_LEAVE = "EVENT_PLAYER_LEAVE"

# 游戏事件 (EVENT_GAME_*)
EVENT_GAME_START = "EVENT_GAME_START"
EVENT_GAME_END = "EVENT_GAME_END"

# 计时器事件
EVENT_TIMER_EXPIRED = "EVENT_TIMER_EXPIRED"
```

---

## 4. Native 函数清单（20个）

### 4.1 生命周期管理

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| CreateTrigger | 无 | trigger | 创建新触发器 |
| DestroyTrigger | trigger | nothing | 销毁触发器并清理资源 |
| EnableTrigger | trigger | nothing | 启用触发器 |
| DisableTrigger | trigger | nothing | 禁用触发器 |
| IsTriggerEnabled | trigger | boolean | 检查触发器是否启用 |

### 4.2 动作管理

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| TriggerAddAction | trigger, actionFunc | actionId | 添加动作函数 |
| TriggerRemoveAction | trigger, actionId | boolean | 移除指定动作 |
| TriggerClearActions | trigger | nothing | 清空所有动作 |

### 4.3 条件管理

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| TriggerAddCondition | trigger, conditionFunc | conditionId | 添加条件函数 |
| TriggerRemoveCondition | trigger, conditionId | boolean | 移除指定条件 |
| TriggerClearConditions | trigger | nothing | 清空所有条件 |
| TriggerEvaluate | trigger | boolean | 手动评估条件 |

### 4.4 事件注册

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| TriggerRegisterTimerEvent | trigger, timeout, periodic | eventId | 注册计时器事件 |
| TriggerRegisterTimerExpireEvent | trigger, timer | eventId | 注册特定计时器过期事件 |
| TriggerRegisterPlayerUnitEvent | trigger, player, eventType, filter | eventId | 玩家单位事件 |
| TriggerRegisterUnitEvent | trigger, eventType, filter | eventId | 任意单位事件 |
| TriggerRegisterPlayerEvent | trigger, player, eventType | eventId | 玩家级事件 |
| TriggerRegisterGameEvent | trigger, eventType | eventId | 游戏级事件 |

### 4.5 清理

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| TriggerClearEvents | trigger | nothing | 清空触发器的所有事件 |

---

## 5. 数据流与执行逻辑

### 5.1 触发器执行流程

```
[Native函数触发事件]
         ↓
[TriggerManager.fire_event(event_type, event_data)]
         ↓
[查询_event_index获取候选触发器列表]
         ↓
[foreach 触发器]
    ├─[检查是否启用] ──No──> [跳过]
    │         ↓ Yes
    ├─[评估所有条件] ──Any False──> [跳过]
    │         ↓ All True
    └─[依次执行动作函数]
```

### 5.2 与现有系统集成

**HandleManager 集成**（单位相关事件）：
```python
# 在 natives/manager.py KillUnit.execute() 中
def execute(self, state_context, unit_id):
    # ... 原有逻辑 ...

    # 触发事件
    trigger_manager = state_context.trigger_manager
    if trigger_manager:
        trigger_manager.fire_event(EVENT_UNIT_DEATH, {
            'unit_id': unit_id,
            'unit_type': unit.unit_type if unit else None
        })
```

**TimerSystem 集成**（计时器事件）：
```python
# 在 timer/timer.py Timer.update() 中
def update(self, delta_time):
    # ... 原有逻辑 ...

    if self._fired and self.callback:
        # 先执行回调
        self.callback()

        # 再触发全局计时器事件
        if self._trigger_manager:
            self._trigger_manager.fire_event(EVENT_TIMER_EXPIRED, {
                'timer_id': self.timer_id
            })
```

**ExecutionContext 访问**：
- `state_context` 的 `trigger_manager` 属性支持触发器访问
- Interpreter 在执行时传递 state_context

---

## 6. 测试策略

### 6.1 单元测试

**test_trigger.py**：
- 测试条件评估（AND逻辑：所有条件为True才执行）
- 测试动作执行顺序
- 测试启用/禁用状态

**test_trigger_manager.py**：
- 测试创建/销毁生命周期
- 测试事件注册和索引
- 测试事件分发和过滤

**test_trigger_natives.py**：
- 每个native函数的参数验证
- 返回值类型检查
- 错误处理（无效trigger_id等）

### 6.2 集成测试

完整流程测试：
```python
def test_complete_trigger_flow():
    # 1. 创建触发器
    # 2. 注册单位死亡事件
    # 3. 添加条件和动作
    # 4. 模拟KillUnit调用
    # 5. 验证动作被执行
```

条件过滤测试：
```python
def test_condition_filtering():
    # 1. 创建两个触发器，注册同一事件
    # 2. 触发器A条件恒为True，触发器B条件恒为False
    # 3. 触发事件
    # 4. 验证只有A的动作执行
```

### 6.3 示例JASS脚本

```jass
function actionOnUnitDeath takes nothing returns nothing
    call DisplayTextToPlayer(0, 0, 0, "A unit has died!")
endfunction

function main takes nothing returns nothing
    local trigger t = CreateTrigger()
    call TriggerRegisterUnitEvent(t, EVENT_UNIT_DEATH, null)
    call TriggerAddAction(t, actionOnUnitDeath)
    // 当任意单位死亡时，将输出 "A unit has died!"
endfunction
```

---

## 7. 错误处理

### 7.1 参数验证

**无效trigger_id**：
- 返回false或None
- 记录warning日志

**无效event_type**：
- 返回None
- 记录error日志

**空action/condition**：
- 记录warning，返回None

### 7.2 异常捕获

**动作执行异常**：
- 捕获异常，记录error
- 继续执行下一个动作（不中断流程）

**条件评估异常**：
- 视为条件失败（返回False）
- 记录error日志

---

## 8. 行数预算

| 文件 | 预估行数 | 说明 |
|------|----------|------|
| trigger/trigger.py | ~80 | Trigger类 |
| trigger/manager.py | ~120 | TriggerManager类 |
| trigger/event_types.py | ~30 | 常量定义 |
| trigger/native_hooks.py | ~50 | Native函数钩子 |
| natives/trigger_natives.py | ~200 | 20个native函数 |
| tests/test_trigger.py | ~150 | 单元测试 |
| tests/test_trigger_manager.py | ~180 | 管理器测试 |
| tests/test_trigger_natives.py | ~250 | Native函数测试 |
| tests/integration/test_trigger.py | ~200 | 集成测试 |
| **总计** | **~1260** | 新文件总行数 |

---

## 9. 设计决策记录

### 9.1 事件数据传递机制（待定）

**方案A：全局状态**（与WC3一致）
- 通过`GetTriggerUnit()`, `GetTriggerPlayer()`等函数访问
- 事件触发时设置全局变量，执行完后清理

**方案B：参数传递**
- 动作函数接收event_data参数
- 需要修改函数签名

**当前决策**：采用方案A，更贴近真实JASS行为（下一步迭代实现）

### 9.2 条件评估逻辑

**AND 逻辑**：所有条件为True才执行（已确认）
- 与WC3触发器编辑器行为一致

**评估顺序**：按添加顺序依次评估
- 任一失败立即返回False（短路优化）

### 9.3 动作执行顺序

**FIFO**：按添加顺序依次执行
- 与WC3行为一致

---

## 10. 后续扩展

### 10.1 事件数据获取函数

下一步迭代实现：
- `GetTriggerUnit()` - 获取触发事件的单位
- `GetTriggerPlayer()` - 获取触发事件的玩家
- `GetEventDamage()` - 获取伤害值（用于受伤事件）
- `GetEventUnit()` - 通用单位获取

### 10.2 高级事件过滤

- `TriggerRegisterPlayerUnitEvent`的filter参数支持
- 按单位类型、区域等过滤

### 10.3 触发器变量

- `SetTriggerVariable` / `GetTriggerVariable`
- 支持在触发器内存储临时数据

---

## 11. 参考资料

- [JASS标准库 common.j](https://jass.sourceforge.net/doc/)
- 现有架构：TimerSystem、HandleManager、NativeFunction基类
- WC3触发器编辑器行为文档

---

## 12. 审批

| 项目 | 状态 |
|------|------|
| 架构设计（方案C） | ✅ 已确认 |
| Native函数清单（20个） | ✅ 已确认 |
| 事件类型（12个） | ✅ 已确认 |
| 数据流设计 | ✅ 已确认 |
| 测试策略 | ✅ 已确认 |
| 行数预算 | ✅ 已确认 |

**审批人**: [用户]
**日期**: 2026-02-28

---

**下一**: 使用 writing-plans skill创建实施计划
