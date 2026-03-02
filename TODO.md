# JASS Runner 功能缺失分析与实施路线图

本文档基于对当前工程的全面代码审查，列出了 JASS 解释器和运行模拟器的功能缺失情况，并规划了后续开发的实施路线图。

## 1. JASS 语言规范支持现状

| 核心特性 | 子项 | 状态 | 详细说明 |
| :--- | :--- | :--- | :--- |
| **语法解析** | 基础结构 | ✅ 实现 | 支持 `function` 定义、`local` 变量声明、`set` 赋值、函数调用、`if`/`loop`/`return` 控制流、嵌套函数调用。不支持 `type` 定义、`native` 声明。 |
| | 复杂表达式 | ✅ 实现 | 支持完整数学和逻辑表达式解析（如 `(a + b) * c`，`a > 0 and b < 10`）。 |
| **类型系统** | 基础类型 | ✅ 实现 | 支持 `integer`, `real`, `string`, `boolean`, `code`, `handle` 及其子类型。 |
| | 数组类型 | ✅ 实现 | 已支持 `array` 关键字及数组索引访问（`a[i]`），支持全局和局部数组声明。 |
| | 类型检查 | ✅ 实现 | 运行时类型检查已实现，支持integer→real隐式转换和handle子类型协变。 |
| **作用域规则** | 局部作用域 | ⚠️ 部分 | 支持函数级 `local` 变量，但赋值逻辑存在遮蔽父级变量的缺陷。 |
| | 全局作用域 | ✅ 实现 | 支持 `globals`/`endglobals` 块解析，支持基础变量声明和可选初始值。 |
| **标准库** | Native 函数 | ⚠️ 部分 | 仅通过 Python 模拟了极少量（<1%）的 `common.j` 函数。 |

## 2. 解释器模块 (Interpreter) 深度分析

### 2.1 AST 生成与遍历
- [x] **完善 AST 节点结构**: 已实现完整的 AST 节点结构，包括 `IfStmt`, `LoopStmt`, `ExitWhenStmt`, `ReturnStmt` 等控制流节点。

### 2.2 控制流语句 (Control Flow) ✅ 已完成
- [x] **If/Else 语句**: 实现 `if / then / elseif / else / endif` 的解析与执行。
- [x] **循环语句**: 实现 `loop / endloop` 的解析与执行。
- [x] **退出语句**: 实现 `exitwhen` 的解析与执行。
- [x] **返回语句**: 实现 `return` 的解析与执行（支持提前返回和带值返回）。

### 2.3 运算符 (Operators) ✅ 已完成
- [x] **算术运算符**: 实现 `+`, `-`, `*`, `/`。
- [x] **比较运算符**: 实现 `==`, `!=`, `<`, `>`, `<=`, `>=`。
- [x] **逻辑运算符**: 实现 `and`, `or`, `not`。
- [x] **优先级与短路**: 实现正确的运算符优先级解析和逻辑短路求值。

### 2.4 内存模型
- [ ] **Handle 引用计数**: 增加针对 JASS Handle 的引用计数或垃圾回收模拟。
- [ ] **String Table**: 模拟 JASS 的字符串表机制（目前直接使用 Python str）。

## 3. 运行模拟器模块 (Runtime Simulator) 深度分析

### Native API 实现状态

- [x] **基础单位操作**: CreateUnit, KillUnit, GetUnitState, SetUnitState
- [x] **位置操作**: GetUnitX/Y/Loc, SetUnitPosition, CreateUnitAtLoc
- [x] **朝向控制**: GetUnitFacing, SetUnitFacing
- [x] **单位信息**: GetUnitTypeId, GetUnitName
- [x] **Location 操作**: Location, RemoveLocation
- [ ] **单位组操作**: CreateGroup, GroupAddUnit, ForGroup（未来版本）
- [ ] **技能系统**: UnitAddAbility, GetUnitAbilityLevel（未来版本）

### 3.1 Warcraft III 原生 API (Native API)
- [x] **触发器 API**: 实现 `TriggerRegister...`, `TriggerAddAction`, `TriggerEvaluate` 等。 ✅ 已完成（2026-03-01）
- [ ] **技能/Buff API**: 实现 `UnitAddAbility`, `GetUnitAbilityLevel` 等。
- [ ] **物品交互 API**: 实现 `UnitAddItem`, `UnitUseItem` 等。
- [ ] **命令系统 API**: 实现 `IssueOrder`, `IssueTargetOrder` 等。
- [ ] **数学/几何 API**: 实现 `Cos`, `Sin`, `Pow`, `SquareRoot` 等。

### 3.2 触发器事件系统 ✅ 已完成（2026-03-01）
- [x] **事件分发中心**: 实现核心事件系统，能够监听游戏事件（如单位死亡、进入区域）并分发给注册触发器。
- [x] **条件求值**: 实现 `TriggerAddCondition` 注册的布尔表达式求值。

### 3.3 并发与异步模型
- [ ] **多线程模拟**: 实现 `StartThread` 或 `ExecuteFunc`（开启新的伪线程）。
- [ ] **异步等待**: 实现 `TriggerSleepAction` (Wait) 或 `PolledWait`。需要支持解释器的挂起（Suspend）和恢复（Resume）。

## 4. 实施路线图 (Roadmap)

### v0.2.0: 解释器核心补全 (Interpreter Core) ✅ 已完成
> 目标：使解释器能够运行纯算法类的 JASS 代码（如斐波那契数列计算）。

- [x] **P0** [Interpreter] 实现控制流语句 (`if`, `loop`, `exitwhen`, `return`)。
- [x] **P0** [Interpreter] 实现完整的运算符解析与表达式求值。
- [x] **P0** [Interpreter] 实现 `globals` 全局变量块的解析与访问（基础变量声明）。
- [x] **P1** [Interpreter] 扩展 `globals` 支持 `constant` 常量声明。
- [x] **P1** [Interpreter] 扩展 `globals` 支持 `array` 数组声明（如 `integer array counts`）。

**v0.2.0 状态**: ✅ 已完成（2026-02-28）
- 控制流语句：`if`/`else`/`elseif`/`endif`, `loop`/`endloop`, `exitwhen`, `return`
- 运算符：`+`, `-`, `*`, `/`, `==`, `!=`, `<`, `>`, `<=`, `>=`, `and`, `or`, `not`
- `globals` 全局变量块支持（含 `constant` 常量）
- `array` 数组支持：声明、访问、赋值（全局/局部数组，8192元素标准）
- 测试覆盖：190个测试通过

### v0.3.0: 运行时与基础 API (Runtime & Basic API) ✅ 已完成
> 目标：能够运行简单的魔兽地图逻辑，处理基本的单位操作。

- [x] **P0** [Simulator] 实现基础触发器系统（事件注册、动作执行）。
- [x] **P1** [Language] 实现数组 (`array`) 支持。
- [x] **P1** [Simulator] 补全常用数学 (`Math`) API。

**v0.3.0 状态**: ✅ 已完成（2026-03-01）
- 触发器系统：Trigger类、TriggerManager类、20个Native函数
- 事件系统集成：单位死亡事件、计时器事件
- 数组支持：已完成于v0.2.0
- 数学API：15个数学Native函数（SquareRoot, Pow, Cos, Sin, R2I, I2R, Tan, Modulo, R2S, S2R, I2S, S2I, GetRandomInt, GetRandomReal）
- 测试覆盖：421个测试通过

### v0.4.0: 高级特性与并发 (Advanced Features) ✅ 已完成
> 目标：支持复杂的异步逻辑和过场动画脚本。

- [x] **P1** [Simulator] 实现异步等待 (`TriggerSleepAction` / `Wait`)。
- [x] **P2** [Simulator] 实现并发执行 (`ExecuteFunc`)。

**v0.4.0 状态**: ✅ 已完成（2026-03-01）
- 协程核心组件：Coroutine、SleepScheduler、CoroutineRunner
- 解释器改造：JassCoroutine、create_main_coroutine
- SimulationLoop 集成：run 方法、_update_frame
- 异步Native函数：TriggerSleepAction、ExecuteFunc
- 测试覆盖：460个测试通过

### v0.5.0: 健壮性与完整性 (Robustness)
> 目标：接近真实的 JASS 运行环境，具备良好的错误提示。

- [x] **P2** [Language] 实现运行时类型检查。 ✅ 已完成（2026-03-02）
  - 运行时类型检查系统
  - 支持integer→real隐式转换
  - 支持handle子类型协变
  - 类型不匹配时抛出JassTypeError
- [ ] **P2** [Simulator] 持续补充 `common.j` 中的 Native 函数 Mock。
  - [x] 第一批：单位组核心（CreateGroup, DestroyGroup, GroupAddUnit, GroupRemoveUnit, GroupClear, FirstOfGroup, IsUnitInGroup, ForGroup）✅ 已完成
  - [x] 第二批：技能系统核心（UnitAddAbility, UnitRemoveAbility, GetUnitAbilityLevel, SetUnitAbilityLevel, IncUnitAbilityLevel, DecUnitAbilityLevel, UnitMakeAbilityPermanent）✅ 已完成
  - [x] 第三批：单位组枚举（GroupEnumUnitsOfPlayer, GroupEnumUnitsInRange, GroupEnumUnitsInRangeOfLoc, GroupEnumUnitsInRect, BlzGroupGetSize, BlzGroupUnitAt）✅ 已完成
  - [x] 第四批：单位状态扩展（GetWidgetLife, SetWidgetLife, UnitDamageTarget, GetUnitLevel, IsUnitType, IsUnitAlive, IsUnitDead）✅ 已完成
  - [ ] 第五批：单位所有权和关系（SetUnitOwner, IsUnitOwnedByPlayer, IsUnitAlly, IsUnitEnemy, IsUnitInRange系列）
