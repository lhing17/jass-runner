# v0.4.0 异步等待功能设计文档

## 1. 概述和目标

### 1.1 背景

JASS Runner v0.3.0 已实现触发器系统、数学API和数组支持。v0.4.0 目标是实现异步等待功能，支持 JASS 中的 `TriggerSleepAction` (Wait) 和 `ExecuteFunc` 函数。

### 1.2 目标

- 实现 `TriggerSleepAction` - 暂停当前执行流指定时间后继续
- 实现 `ExecuteFunc` - 创建新执行流（协程）执行指定函数
- 与现有计时器系统和模拟循环集成
- 保持与现有代码的向后兼容性

### 1.3 设计原则

- **最小侵入性**：尽量保持现有解释器架构不变
- **渐进改造**：通过生成器模式逐步引入异步能力
- **简单优先**：`ExecuteFunc` 采用简单顺序执行，不引入复杂并发模型

## 2. 架构设计

### 2.1 核心思想：生成器协程方案

将解释器改造为生成器模式，使用 Python 的 `yield` 实现挂起/恢复机制：

```python
def run_function(self, func):
    for statement in func.body:
        if isinstance(statement, SleepStmt):
            yield SleepSignal(duration)  # 挂起，返回等待时间
        else:
            self.execute_statement(statement)
```

### 2.2 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                     SimulationLoop                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              CoroutineRunner                        │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌────────────┐  │   │
│  │  │  Coroutine  │  │  Coroutine  │  │  ...       │  │   │
│  │  │  (main)     │  │  (ExecuteFunc)│ │            │  │   │
│  │  └─────────────┘  └─────────────┘  └────────────┘  │   │
│  │                                                     │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │           SleepScheduler                    │   │   │
│  │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐       │   │   │
│  │  │  │sleep_1s │ │sleep_2s │ │  ...    │       │   │   │
│  │  │  └─────────┘ └─────────┘ └─────────┘       │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              TimerSystem (现有)                     │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 3. 核心组件详细设计

### 3.1 Coroutine 类

包装单个 JASS 函数执行的协程：

```python
from enum import Enum
from typing import Optional, Any, Generator

class CoroutineStatus(Enum):
    PENDING = "pending"      # 刚创建，未开始执行
    RUNNING = "running"      # 正在执行
    SLEEPING = "sleeping"    # 调用 TriggerSleepAction 后暂停
    FINISHED = "finished"    # 执行完成

class SleepSignal:
    """协程暂停信号，携带等待时间"""
    def __init__(self, duration: float):
        self.duration = duration  # 秒数

class Coroutine:
    """包装 JASS 函数执行的协程"""

    def __init__(self, interpreter: 'Interpreter',
                 func: 'FunctionDecl', args: list = None):
        self.interpreter = interpreter
        self.func = func
        self.args = args or []
        self.status = CoroutineStatus.PENDING
        self.generator: Optional[Generator] = None
        self.wake_time: float = 0.0
        self.return_value: Any = None

    def start(self):
        """启动协程，创建生成器"""
        self.generator = self._run()
        self.status = CoroutineStatus.RUNNING

    def _run(self) -> Generator:
        """实际的生成器函数"""
        # 设置函数上下文
        # 执行函数体
        for statement in self.func.body:
            result = self._execute_statement_with_sleep(statement)
            if isinstance(result, SleepSignal):
                yield result
        self.status = CoroutineStatus.FINISHED

    def resume(self) -> Optional[SleepSignal]:
        """恢复执行，直到遇到下一个 SleepSignal 或完成"""
        if self.status != CoroutineStatus.RUNNING:
            return None

        try:
            signal = next(self.generator)
            if isinstance(signal, SleepSignal):
                self.status = CoroutineStatus.SLEEPING
                return signal
        except StopIteration:
            self.status = CoroutineStatus.FINISHED

        return None

    def wake(self, current_time: float):
        """从睡眠中唤醒"""
        if (self.status == CoroutineStatus.SLEEPING and
            current_time >= self.wake_time):
            self.status = CoroutineStatus.RUNNING

    def sleep(self, duration: float, current_time: float):
        """设置睡眠状态"""
        self.wake_time = current_time + duration
        self.status = CoroutineStatus.SLEEPING
```

### 3.2 SleepScheduler 类

管理所有睡眠中的协程：

```python
from typing import List

class SleepScheduler:
    """管理所有睡眠中的协程"""

    def __init__(self):
        self._sleeping: List[Coroutine] = []

    def add(self, coroutine: Coroutine):
        """添加睡眠中的协程"""
        self._sleeping.append(coroutine)

    def wake_ready(self, current_time: float) -> List[Coroutine]:
        """获取并移除所有到期的协程"""
        ready = [c for c in self._sleeping
                 if current_time >= c.wake_time]
        self._sleeping = [c for c in self._sleeping
                         if current_time < c.wake_time]

        for c in ready:
            c.wake(current_time)

        return ready

    def is_empty(self) -> bool:
        return len(self._sleeping) == 0
```

### 3.3 CoroutineRunner 类

主调度器，与 SimulationLoop 集成：

```python
class CoroutineRunner:
    """协程调度器"""

    def __init__(self, max_coroutines: int = 100):
        self._active: List[Coroutine] = []
        self._scheduler = SleepScheduler()
        self._current_time = 0.0
        self._frame_count = 0
        self._main_coroutine: Optional[Coroutine] = None
        self.max_coroutines = max_coroutines

    def start_main(self, interpreter: 'Interpreter', ast: 'AST'):
        """启动主协程（main 函数）"""
        coroutine = interpreter.create_main_coroutine(ast)
        coroutine.start()
        self._active.append(coroutine)
        self._main_coroutine = coroutine

    def execute_func(self, interpreter: 'Interpreter',
                     func: 'FunctionDecl', args: list) -> Coroutine:
        """ExecuteFunc - 创建新协程（简单顺序执行）"""
        # 限制并发协程数
        total = len(self._active) + len(self._scheduler._sleeping)
        if total >= self.max_coroutines:
            raise CoroutineStackOverflow(
                f"协程数超过限制({self.max_coroutines})"
            )

        coroutine = Coroutine(interpreter, func, args)
        coroutine.start()
        self._active.append(coroutine)
        return coroutine

    def update(self, delta_time: float):
        """每帧调用，更新协程状态"""
        self._current_time += delta_time
        self._frame_count += 1

        # 1. 唤醒到期的协程
        ready = self._scheduler.wake_ready(self._current_time)
        self._active.extend(ready)

        # 2. 执行活跃协程
        still_active = []
        for coroutine in self._active:
            signal = coroutine.resume()

            if signal:  # 遇到 SleepSignal
                coroutine.sleep(signal.duration, self._current_time)
                self._scheduler.add(coroutine)
            elif coroutine.status == CoroutineStatus.FINISHED:
                pass  # 协程完成
            else:
                still_active.append(coroutine)

        self._active = still_active

    def is_finished(self) -> bool:
        """检查所有协程是否完成"""
        return (len(self._active) == 0 and
                self._scheduler.is_empty() and
                self._main_coroutine.status == CoroutineStatus.FINISHED)
```

## 4. 与现有系统集成

### 4.1 SimulationLoop 改造

```python
class SimulationLoop:
    """改造后的模拟循环"""

    def __init__(self, fps: float = 30.0):
        self.fps = fps
        self.frame_duration = 1.0 / fps
        self.current_time = 0.0
        self.frame_count = 0

        # 现有系统
        self.timer_system = TimerSystem()

        # 新增：协程调度器
        self.coroutine_runner = CoroutineRunner()
        self._running = False

    def run(self, interpreter: 'Interpreter', ast: 'AST',
            max_frames: int = None) -> dict:
        """运行模拟（主入口）"""
        self._running = True

        # 启动主协程
        self.coroutine_runner.start_main(interpreter, ast)

        while self._running:
            self._update_frame()

            if self.coroutine_runner.is_finished():
                break

            if max_frames and self.frame_count >= max_frames:
                break

        return {
            'frames': self.frame_count,
            'time': self.current_time,
            'success': self.coroutine_runner.is_finished()
        }

    def _update_frame(self):
        """单帧更新"""
        delta = self.frame_duration
        self.current_time += delta
        self.frame_count += 1

        # 1. 更新协程
        self.coroutine_runner.update(delta)

        # 2. 更新计时器
        self.timer_system.update(delta)
```

### 4.2 TriggerSleepAction Native 函数

```python
class SleepInterrupt(Exception):
    """睡眠中断异常，用于从深层调用栈传递睡眠信号"""
    def __init__(self, duration: float):
        self.duration = duration

class TriggerSleepAction(NativeFunction):
    """JASS 原生函数：暂停当前协程指定时间"""

    @property
    def name(self) -> str:
        return "TriggerSleepAction"

    def execute(self, timeout: float) -> None:
        """
        参数：
            timeout: 等待时间（秒）
        """
        raise SleepInterrupt(timeout)
```

### 4.3 ExecuteFunc Native 函数

```python
class ExecuteFunc(NativeFunction):
    """JASS 原生函数：创建新协程执行指定函数"""

    @property
    def name(self) -> str:
        return "ExecuteFunc"

    def execute(self, func_name: str) -> None:
        """
        参数：
            func_name: 要执行的函数名称

        行为：
            创建新协程执行函数，但不等待其完成
            当前协程继续执行
        """
        func = self.interpreter.functions.get(func_name)
        if not func:
            return  # 函数不存在静默返回

        self.interpreter.coroutine_runner.execute_func(
            self.interpreter, func, []
        )
```

### 4.4 解释器改造

```python
class Interpreter:
    def __init__(self, native_registry=None, coroutine_runner=None):
        self.state_context = StateContext()
        self.global_context = ExecutionContext(...)
        self.current_context = self.global_context
        self.functions = {}
        self.evaluator = Evaluator(self.current_context)
        self.coroutine_runner = coroutine_runner

    def create_main_coroutine(self, ast: AST) -> Coroutine:
        """创建主协程"""
        # 初始化全局变量
        if ast.globals:
            for global_decl in ast.globals:
                self.execute_global_declaration(global_decl)

        # 注册所有函数
        for func in ast.functions:
            self.functions[func.name] = func

        # 创建 main 函数协程
        main_func = self.functions.get('main')
        if main_func:
            return Coroutine(self, main_func)
        return None

    def run_function_as_generator(self, func: FunctionDecl,
                                   args: list = None):
        """将函数执行转换为生成器"""
        pc = 0  # 程序计数器

        # 设置函数上下文
        func_context = ExecutionContext(
            self.global_context,
            native_registry=self.global_context.native_registry,
            state_context=self.state_context,
            interpreter=self
        )
        self.current_context = func_context

        statements = func.body or []

        while pc < len(statements):
            statement = statements[pc]

            try:
                self.execute_statement(statement)
                pc += 1

            except SleepInterrupt as e:
                pc += 1
                yield SleepSignal(e.duration)

            except ReturnSignal as e:
                self.return_value = e.value
                break

        # 恢复上下文
        self.current_context = self.global_context
```

## 5. 错误处理与边界情况

### 5.1 错误类型

```python
class CoroutineError(Exception):
    """协程执行错误基类"""
    pass

class CoroutineTimeoutError(CoroutineError):
    """协程执行超时"""
    pass

class CoroutineStackOverflow(CoroutineError):
    """协程调用栈溢出"""
    pass
```

### 5.2 边界情况处理

| 边界情况 | 处理策略 |
|---------|---------|
| Sleep 时间 <= 0 | 视为 0，下一帧立即唤醒 |
| Sleep 时游戏暂停 | 计入游戏时间 |
| ExecuteFunc 调用不存在函数 | 静默返回（符合 JASS 行为） |
| 协程执行时出错 | 记录错误，终止该协程，其他协程继续 |
| main 函数提前 return | 标记主协程完成，其他协程继续 |
| 嵌套 ExecuteFunc | 支持，限制最大协程数防止栈溢出 |

### 5.3 最大协程数限制

```python
class CoroutineRunner:
    DEFAULT_MAX_COROUTINES = 100

    def execute_func(self, interpreter, func, args):
        total = len(self._active) + len(self._scheduler._sleeping)
        if total >= self.max_coroutines:
            raise CoroutineStackOverflow(
                f"协程数超过限制({self.max_coroutines})"
            )
        # ...
```

## 6. 测试策略

### 6.1 单元测试

```python
class TestCoroutineAsync:
    """协程异步功能测试"""

    def test_trigger_sleep_action_pauses_coroutine(self):
        """测试 TriggerSleepAction 暂停当前协程"""
        pass

    def test_execute_func_creates_new_coroutine(self):
        """测试 ExecuteFunc 创建新协程"""
        pass

    def test_multiple_coroutines_run_concurrently(self):
        """测试多个协程并发执行"""
        pass

    def test_coroutine_wake_order(self):
        """测试协程按正确顺序唤醒"""
        pass

    def test_sleep_zero_immediate_wake(self):
        """测试 Sleep 时间为 0 立即唤醒"""
        pass
```

### 6.2 集成测试

```python
def test_async_script_execution():
    """测试完整异步脚本执行"""
    code = '''
    function delayed_message takes nothing returns nothing
        call TriggerSleepAction(2.0)
        call DisplayTextToPlayer(Player(0), 0, 0, "延迟消息")
    endfunction

    function main takes nothing returns nothing
        call ExecuteFunc("delayed_message")
        call DisplayTextToPlayer(Player(0), 0, 0, "立即消息")
        call TriggerSleepAction(1.0)
        call DisplayTextToPlayer(Player(0), 0, 0, "1秒后消息")
    endfunction
    '''
    # 验证执行顺序和时序
```

## 7. API 使用示例

### 7.1 基本使用

```python
from jass_runner.vm.jass_vm import JassVM

vm = JassVM()
vm.load_script("examples/async_example.j")

# 运行模拟
result = vm.run(max_frames=10000)

print(f"执行完成: {result['frames']}帧, {result['time']:.2f}秒")
```

### 7.2 JASS 示例脚本

```jass
// async_example.j
function delayed_spawn takes nothing returns nothing
    call TriggerSleepAction(3.0)
    call DisplayTextToPlayer(Player(0), 0, 0, "3秒后开始生成单位")

    local unit u = CreateUnit(Player(0), 'Hpal', 0, 0, 0)
    call DisplayTextToPlayer(Player(0), 0, 0, "单位已生成")
endfunction

function periodic_message takes nothing returns nothing
    local integer i = 0
    loop
        exitwhen i >= 5
        call TriggerSleepAction(1.0)
        call DisplayTextToPlayer(Player(0), 0, 0, "周期消息 " + I2S(i))
        set i = i + 1
    endloop
endfunction

function main takes nothing returns nothing
    call DisplayTextToPlayer(Player(0), 0, 0, "开始执行")

    // 创建两个并行的执行流
    call ExecuteFunc("delayed_spawn")
    call ExecuteFunc("periodic_message")

    call DisplayTextToPlayer(Player(0), 0, 0, "主函数继续执行")

    call TriggerSleepAction(5.0)
    call DisplayTextToPlayer(Player(0), 0, 0, "5秒后结束")
endfunction
```

### 7.3 预期输出时序

```
[0.00s] 开始执行
[0.00s] 主函数继续执行
[1.00s] 周期消息 0
[2.00s] 周期消息 1
[3.00s] 3秒后开始生成单位
[3.00s] 单位已生成
[3.00s] 周期消息 2
[4.00s] 周期消息 3
[5.00s] 周期消息 4
[5.00s] 5秒后结束
```

## 8. 实施计划

### 8.1 实施步骤

1. **Phase 1**: 创建核心协程组件（Coroutine, SleepScheduler, CoroutineRunner）
2. **Phase 2**: 改造解释器为生成器模式
3. **Phase 3**: 改造 SimulationLoop 集成 CoroutineRunner
4. **Phase 4**: 实现 TriggerSleepAction 和 ExecuteFunc native 函数
5. **Phase 5**: 编写测试和示例脚本
6. **Phase 6**: 文档更新和代码审查

### 8.2 风险与缓解

| 风险 | 缓解措施 |
|-----|---------|
| 生成器改造引入 bug | 保持现有测试全部通过，增量添加测试 |
| 性能下降 | 基准测试对比，必要时优化热点路径 |
| 与现有系统不兼容 | 提供向后兼容的同步执行模式 |

## 9. 相关文档

- [项目笔记](../../PROJECT_NOTES.md)
- [待办清单](../../TODO.md)
- [CLAUDE.md](../../CLAUDE.md) - 开发规范

---

*文档创建日期: 2026-03-01*
*版本: v0.4.0 设计文档*
