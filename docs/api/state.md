# StateContext

状态上下文，管理全局和局部状态。

## 类定义

```python
class StateContext:
    def __init__(self)
    def get_context_store(self, context_id: str) -> Dict
```

## 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `handle_manager` | HandleManager | handle管理器实例 |
| `global_vars` | Dict | 全局变量存储 |
| `local_stores` | Dict | 上下文局部存储 |

## 方法

### `get_context_store(context_id)` -> Dict

获取指定上下文的局部存储。如果不存在则自动创建。

**参数**:
- `context_id` (str): 上下文ID

**返回**: 该上下文的局部存储字典

## 使用场景

### 场景1: 基础状态管理

```python
from jass_runner.natives.state import StateContext

state = StateContext()
manager = state.handle_manager

# 创建单位
unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 270.0)

# 使用全局变量存储游戏状态
state.global_vars["game_time"] = 0.0
state.global_vars["winner"] = None
```

### 场景2: 多上下文状态隔离

```python
state = StateContext()

# 上下文A的局部存储
store_a = state.get_context_store("context_a")
store_a["temp_var"] = "value_a"

# 上下文B的局部存储
store_b = state.get_context_store("context_b")
store_b["temp_var"] = "value_b"

# 两个上下文互不影响
assert state.get_context_store("context_a")["temp_var"] == "value_a"
assert state.get_context_store("context_b")["temp_var"] == "value_b"
```

### 场景3: 与ExecutionContext集成

```python
from jass_runner.interpreter.context import ExecutionContext
from jass_runner.natives.factory import NativeFactory
from jass_runner.natives.state import StateContext

# 创建状态上下文
state_context = StateContext()

# 创建执行上下文，共享状态
native_registry = NativeFactory.create_default_registry()
exec_context = ExecutionContext(
    native_registry=native_registry,
    state_context=state_context
)

# 通过执行上下文访问handle管理器
manager = state_context.handle_manager
unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 270.0)
```

## 架构说明

StateContext采用混合持久化方案：

1. **全局状态**（handle引用）由HandleManager管理
2. **局部状态**（临时变量）由ExecutionContext管理
3. **上下文隔离**通过local_stores实现

```
StateContext
├── handle_manager (HandleManager) - 全局handle状态
├── global_vars (Dict) - 全局变量
└── local_stores (Dict[context_id, Dict]) - 上下文局部存储
```
