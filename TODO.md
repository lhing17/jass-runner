# JASS Runner 功能缺失分析与实施路线图

本文档基于对当前工程的全面代码审查，列出了 JASS 解释器和运行模拟器的功能缺失情况，并规划了后续开发的实施路线图。

## 1. JASS 语言规范支持现状

| 核心特性 | 子项 | 状态 | 详细说明 |
| :--- | :--- | :--- | :--- |
| **语法解析** | 基础结构 | ✅ 实现 | 支持 `function` 定义、`local` 变量声明、`set` 赋值、函数调用、`if`/`loop`/`return` 控制流。不支持 `globals` 块、`type` 定义、`native` 声明。 |
| | 复杂表达式 | ✅ 实现 | 支持完整数学和逻辑表达式解析（如 `(a + b) * c`，`a > 0 and b < 10`）。 |
| **类型系统** | 基础类型 | ✅ 实现 | 支持 `integer`, `real`, `string`, `boolean`, `code`, `handle` 及其子类型。 |
| | 数组类型 | ❌ 缺失 | 不支持 `array` 关键字及数组索引访问（`a[i]`）。 |
| | 类型检查 | ❌ 缺失 | 无静态或运行时类型检查，赋值时未验证类型兼容性。 |
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

### 3.1 Warcraft III 原生 API (Native API)
- [ ] **触发器 API**: 实现 `TriggerRegister...`, `TriggerAddAction`, `TriggerEvaluate` 等。
- [ ] **技能/Buff API**: 实现 `UnitAddAbility`, `GetUnitAbilityLevel` 等。
- [ ] **物品交互 API**: 实现 `UnitAddItem`, `UnitUseItem` 等。
- [ ] **命令系统 API**: 实现 `IssueOrder`, `IssueTargetOrder` 等。
- [ ] **数学/几何 API**: 实现 `Cos`, `Sin`, `Pow`, `SquareRoot` 等。

### 3.2 触发器事件系统
- [ ] **事件分发中心**: 实现核心事件系统，能够监听游戏事件（如单位死亡、进入区域）并分发给注册触发器。
- [ ] **条件求值**: 实现 `TriggerAddCondition` 注册的布尔表达式求值。

### 3.3 并发与异步模型
- [ ] **多线程模拟**: 实现 `StartThread` 或 `ExecuteFunc`（开启新的伪线程）。
- [ ] **异步等待**: 实现 `TriggerSleepAction` (Wait) 或 `PolledWait`。需要支持解释器的挂起（Suspend）和恢复（Resume）。

## 4. 实施路线图 (Roadmap)

### v0.2.0: 解释器核心补全 (Interpreter Core) ✅ 已完成
> 目标：使解释器能够运行纯算法类的 JASS 代码（如斐波那契数列计算）。

- [x] **P0** [Interpreter] 实现控制流语句 (`if`, `loop`, `exitwhen`, `return`)。
- [x] **P0** [Interpreter] 实现完整的运算符解析与表达式求值。
- [x] **P0** [Interpreter] 实现 `globals` 全局变量块的解析与访问（基础变量声明）。
- [ ] **P1** [Interpreter] 扩展 `globals` 支持 `constant` 常量声明。
- [ ] **P1** [Interpreter] 扩展 `globals` 支持 `array` 数组声明（如 `integer array counts`）。

**v0.2.0 状态**: ✅ 已完成（2026-02-28）

### v0.3.0: 运行时与基础 API (Runtime & Basic API)
> 目标：能够运行简单的魔兽地图逻辑，处理基本的单位操作。

- [ ] **P0** [Simulator] 实现基础触发器系统（事件注册、动作执行）。
- [ ] **P1** [Language] 实现数组 (`array`) 支持。
- [ ] **P1** [Simulator] 补全常用数学 (`Math`) 和基础单位 (`Unit`) API。

### v0.4.0: 高级特性与并发 (Advanced Features)
> 目标：支持复杂的异步逻辑和过场动画脚本。

- [ ] **P1** [Simulator] 实现异步等待 (`TriggerSleepAction` / `Wait`)。
- [ ] **P2** [Simulator] 实现并发执行 (`ExecuteFunc`)。

### v0.5.0: 健壮性与完整性 (Robustness)
> 目标：接近真实的 JASS 运行环境，具备良好的错误提示。

- [ ] **P2** [Language] 实现静态或运行时类型检查。
- [ ] **P2** [Simulator] 持续补充 `common.j` 中的 Native 函数 Mock。
