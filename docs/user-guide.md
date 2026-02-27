# JASS Runner 用户指南

## 简介

JASS Runner 是一个用Python实现的JASS脚本模拟运行工具，用于魔兽争霸III地图开发者测试和自动化测试。

## 快速开始

### 安装

```bash
pip install -e ".[dev]"
```

### 运行示例脚本

```bash
python -m jass_runner examples/hello_world.j
```

## 状态管理系统

### 核心概念

#### Handle（句柄）

Handle是JASS中所有游戏对象的抽象表示，如单位、计时器等。

```python
from jass_runner.natives.handle import Handle

# Handle是所有游戏对象的基类
handle = Handle("handle_001", "generic")
```

#### Unit（单位）

Unit是Handle的子类，表示游戏中的单位。

```python
from jass_runner.natives.handle import Unit

# 创建一个单位
unit = Unit("unit_001", "hfoo", 0, 100.0, 200.0, 270.0)
print(f"单位类型: {unit.unit_type}")
print(f"生命值: {unit.life}/{unit.max_life}")
```

#### HandleManager（句柄管理器）

HandleManager集中管理所有handle的生命周期。

```python
from jass_runner.natives.manager import HandleManager

manager = HandleManager()

# 创建单位
unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 270.0)

# 查询单位
unit_from_manager = manager.get_unit(unit.id)

# 查询状态
life = manager.get_unit_state(unit.id, "UNIT_STATE_LIFE")

# 销毁单位
manager.destroy_handle(unit.id)
```

### 完整示例

#### 示例1: 基础单位操作

```python
from jass_runner.natives.manager import HandleManager

# 创建管理器
manager = HandleManager()

# 创建玩家0的步兵
unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 270.0)
print(f"创建单位: {unit.id}")

# 查询初始状态
life = manager.get_unit_state(unit.id, "UNIT_STATE_LIFE")
mana = manager.get_unit_state(unit.id, "UNIT_STATE_MANA")
print(f"生命值: {life}")
print(f"魔法值: {mana}")

# 单位受伤
manager.set_unit_state(unit.id, "UNIT_STATE_LIFE", 50.0)
print(f"受伤后生命值: {manager.get_unit_state(unit.id, 'UNIT_STATE_LIFE')}")

# 销毁单位
manager.destroy_handle(unit.id)
print(f"单位存活状态: {manager.get_unit(unit.id) is None}")
```

#### 示例2: 多玩家场景

```python
from jass_runner.natives.manager import HandleManager

manager = HandleManager()

# 为4个玩家各创建3个单位
for player_id in range(4):
    for i in range(3):
        unit = manager.create_unit(
            "hfoo",
            player_id,
            float(player_id * 100),
            float(i * 50),
            0.0
        )
        print(f"玩家{player_id}创建单位: {unit.id}")

# 统计
print(f"总handle数: {manager.get_total_handles()}")
print(f"存活handle数: {manager.get_alive_handles()}")
```

#### 示例3: 与解释器集成

```python
from jass_runner.interpreter.interpreter import Interpreter
from jass_runner.natives.factory import NativeFactory
from jass_runner.parser.parser import Parser

# 创建解释器
native_registry = NativeFactory.create_default_registry()
interpreter = Interpreter(native_registry=native_registry)

# 执行JASS脚本
jass_code = '''
function main takes nothing returns nothing
    call DisplayTextToPlayer(0, 0, 0, "Hello from JASS!")
endfunction
'''

# 解析并执行
parser = Parser(jass_code)
ast = parser.parse()
interpreter.execute(ast)
```

## 内存监控

### 使用MemoryTracker

```python
from jass_runner.utils import MemoryTracker

# 创建内存追踪器
tracker = MemoryTracker()

# 执行操作前记录快照
tracker.snapshot("before_operation")

# 执行操作（如创建大量单位）
manager = HandleManager()
for i in range(1000):
    manager.create_unit("hfoo", 0, float(i), float(i), 0.0)

# 执行操作后记录快照
tracker.snapshot("after_operation")

# 获取统计
stats = tracker.get_stats()
print(f"峰值内存: {stats['peak_memory']}")
print(f"当前内存: {stats['current_memory']}")
```

### 使用HandleMemoryMonitor

```python
from jass_runner.natives.manager import HandleManager
from jass_runner.utils import HandleMemoryMonitor

manager = HandleManager()
monitor = HandleMemoryMonitor(manager)

# 监控单位创建
unit = monitor.monitor_create_unit("hfoo", 0, 100.0, 200.0, 270.0)

# 获取内存报告
report = monitor.get_handle_memory_report()
print(f"总handle数: {report['handle_stats']['total_handles']}")
```

## 性能监控

### 使用PerformanceMonitor

```python
from jass_runner.utils import PerformanceMonitor

monitor = PerformanceMonitor()

# 记录操作耗时
import time

start = time.perf_counter()
# ... 执行操作
monitor.record("my_operation", time.perf_counter() - start)

# 获取统计
stats = monitor.get_stats("my_operation")
print(f"平均耗时: {stats['avg']*1000:.3f} ms")
print(f"调用次数: {stats['count']}")
```

### 使用装饰器

```python
from jass_runner.utils import track_performance

@track_performance("create_unit_batch")
def create_many_units(manager, count):
    for i in range(count):
        manager.create_unit("hfoo", 0, float(i), float(i), 0.0)

# 调用函数会自动记录性能
from jass_runner.utils import get_global_monitor

create_many_units(manager, 1000)

# 查看报告
get_global_monitor().log_report()
```

## 最佳实践

### 1. 及时销毁不需要的handle

```python
# 好：及时销毁
unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 270.0)
# ... 使用单位
manager.destroy_handle(unit.id)

# 避免：创建大量handle不销毁
for i in range(10000):
    manager.create_unit("hfoo", 0, float(i), float(i), 0.0)
    # 不销毁会导致内存泄漏
```

### 2. 使用类型安全的查询方法

```python
# 好：使用类型安全的get_unit
unit = manager.get_unit(unit_id)
if unit:
    print(unit.life)

# 避免：直接使用get_handle然后类型转换
handle = manager.get_handle(unit_id)
if handle and isinstance(handle, Unit):
    print(handle.life)
```

### 3. 检查handle存活状态

```python
unit = manager.get_unit(unit_id)
if unit and unit.is_alive():
    # 安全地操作单位
    manager.set_unit_state(unit.id, "UNIT_STATE_LIFE", 50.0)
```

## 故障排除

### 问题: GetUnitState返回0.0

可能原因：
1. 单位ID不存在
2. 单位已被销毁
3. 状态类型不正确

解决方案：
```python
unit = manager.get_unit(unit_id)
if unit is None:
    print("单位不存在或已销毁")
else:
    life = manager.get_unit_state(unit.id, "UNIT_STATE_LIFE")
```

### 问题: 内存使用过高

使用内存监控工具定位问题：
```python
from jass_runner.utils import MemoryTracker

tracker = MemoryTracker()
# ... 执行操作
tracker.snapshot("checkpoint")
stats = tracker.get_stats()
print(f"内存增量: {stats['total_delta']}")
```

## API参考

详见 [API文档](api/README.md)
