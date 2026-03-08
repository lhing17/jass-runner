# GetLocalPlayer Native函数设计文档

## 概述

实现JASS native函数 `GetLocalPlayer`，用于在模拟环境中返回"本地玩家"。

## 背景

在真实魔兽争霸III游戏中，`GetLocalPlayer()` 返回当前正在执行代码的本地玩家句柄，常用于多玩家同步代码中区分不同玩家的视角（例如显示本地化的UI消息）。

在当前单线程模拟环境中，"本地玩家"概念需要简化定义。

## 设计决策

### 方案选择

选择**方案A：固定返回 Player(0)**

理由：
- 满足当前单人测试场景需求
- 实现简单，不引入额外复杂度
- 与需求描述一致
- 未来可扩展支持动态设置

### 实现细节

**函数签名**（JASS侧）:
```jass
native GetLocalPlayer takes nothing returns player
```

**行为定义**:
- 不接受任何参数
- 返回 `Player` 类型的handle对象
- 在模拟环境中固定返回玩家ID为0的Player对象

**Python实现**:
```python
class GetLocalPlayer(NativeFunction):
    @property
    def name(self) -> str:
        return "GetLocalPlayer"

    def execute(self, state_context, *args):
        handle_manager = state_context.handle_manager
        return handle_manager.get_player(0)
```

## 文件位置

- 实现文件：`src/jass_runner/natives/basic.py`（与PlayerNative同文件）
- 注册位置：`src/jass_runner/natives/factory.py` 的 `create_default_registry()` 方法

## 测试考虑

- 测试返回值为有效的Player对象
- 测试返回的玩家ID为0
- 测试与Player(0)返回相同对象

## 备注

- 当前设计为简化实现，固定返回Player(0)
- 如未来需要支持多玩家视角测试，可扩展为通过StateContext动态设置本地玩家ID
