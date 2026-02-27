# 计时器系统

计时器系统提供基于帧的 JASS 计时器模拟，用于快速测试长期游戏行为。

## 架构

- **Timer**: 具有经过时间跟踪和回调支持的单个计时器
- **TimerSystem**: 管理多个计时器并提供 CRUD 操作
- **SimulationLoop**: 用于运行计时器的基于帧的模拟循环
- **Timer Natives**: 用于计时器操作的原生函数（CreateTimer、TimerStart 等）

## 用法

```python
from jass_runner.timer.system import TimerSystem
from jass_runner.timer.simulation import SimulationLoop
from jass_runner.natives.factory import NativeFactory

# 创建计时器系统
timer_system = TimerSystem()

# 创建带有计时器系统的原生工厂
factory = NativeFactory(timer_system=timer_system)
registry = factory.create_default_registry()

# 获取计时器原生函数
create_timer = registry.get("CreateTimer")
timer_start = registry.get("TimerStart")

# 创建并启动计时器
timer_id = create_timer.execute(None)

def my_callback():
    print("Timer fired!")

timer_start.execute(None, timer_id, 2.5, False, my_callback)

# 运行模拟
simulation = SimulationLoop(timer_system)
simulation.run_seconds(3.0)  # 运行 3 秒模拟时间
```

## 基于帧的模拟

模拟使用离散时间步长（帧）而非实时：

- 默认帧持续时间：0.033 秒（约 30 FPS）
- 计时器每帧根据经过的模拟时间更新
- 允许快速推进长时间模拟
- 测试期间无实时延迟

## 计时器类型

- **一次性**: 超时后触发一次
- **周期性**: 以指定间隔重复
- **可暂停**: 可以暂停和恢复
