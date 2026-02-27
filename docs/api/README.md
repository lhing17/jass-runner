# JASS Runner API 文档

此目录包含JASS Runner状态管理系统的API文档。

## 模块概览

### Handle 类体系
- [Handle 基类](handle.md#handle) - 所有JASS handle的基类
- [Unit 类](handle.md#unit) - 单位handle实现

### 管理器
- [HandleManager](manager.md#handlemanager) - 集中式handle生命周期管理

### 状态管理
- [StateContext](state.md#statecontext) - 全局和局部状态管理

## 快速开始

```python
from jass_runner.natives import HandleManager, StateContext

# 创建状态上下文
state = StateContext()
manager = state.handle_manager

# 创建单位
unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 270.0)

# 查询状态
life = manager.get_unit_state(unit.id, "UNIT_STATE_LIFE")
print(f"单位生命值: {life}")
```
