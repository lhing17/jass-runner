# 特效系统设计方案

## 概述

本文档描述 JASS Runner 中特效系统的实现方案。特效系统采用极简日志方案，仅输出日志记录特效的创建、销毁和属性设置，不做实际渲染。

## 设计目标

1. 支持魔兽争霸 III 中常用的特效 native 函数
2. 纯日志输出，不保存复杂状态
3. 保持与现有系统（单位、物品）一致的设计模式

## 核心架构

### Effect Handle 类

在 `src/jass_runner/natives/handle.py` 中添加 `Effect` 类：

```python
class Effect(Handle):
    """特效句柄，用于标识一个已创建的特效。"""

    def __init__(self, effect_id: int, model_path: str,
                 target: Optional[Union[Unit, Item, Tuple[float, float, float]]] = None,
                 attach_point: Optional[str] = None):
        super().__init__(effect_id, "effect")
        self.model_path = model_path  # 原样保存模型路径
        self.target = target  # 绑定目标（单位/物品/坐标三元组）
        self.attach_point = attach_point  # 附着点名称（如 "hand", "origin"）
```

### HandleManager 扩展

在 `src/jass_runner/natives/manager.py` 中添加特效生命周期管理方法：

```python
def create_effect(self, model_path: str, x: float, y: float, z: float) -> Effect:
    """在指定坐标创建特效。"""

def create_effect_target(self, model_path: str, target: Union[Unit, Item],
                         attach_point: str) -> Effect:
    """在目标对象指定附着点创建特效。"""

def destroy_effect(self, effect: Effect) -> bool:
    """销毁特效。"""
```

## Native 函数设计

| 函数名 | 参数 | 日志输出示例 |
|--------|------|--------------|
| `AddSpecialEffect` | `modelPath: string, x: real, y: real` | `[特效] 在 (100.0, 200.0) 创建特效: Abilities\Spells\... (ID: 1)` |
| `AddSpecialEffectTarget` | `modelPath: string, target: widget, attachPointName: string` | `[特效] 在 [步兵#123] 的附着点 [hand] 创建特效: ... (ID: 2)` |
| `DestroyEffect` | `whichEffect: effect` | `[特效] 销毁特效 (ID: 1)` |
| `SetSpecialEffectScale` | `whichEffect: effect, scale: real` | `[特效] 设置特效 (ID: 1) 缩放: 1.5` |
| `SetSpecialEffectColor` | `whichEffect: effect, r: int, g: int, b: int, a: int` | `[特效] 设置特效 (ID: 1) 颜色: RGBA(255, 0, 0, 255)` |

## 文件结构

```
src/jass_runner/natives/
├── effect_natives.py      # 新增：5个特效 native 函数
├── handle.py              # 修改：添加 Effect 类
├── manager.py             # 修改：添加特效生命周期方法
└── factory.py             # 修改：注册特效 natives
```

## 测试计划

### 单元测试

`tests/natives/test_effect_natives.py`：
- 测试每个 native 函数的参数处理
- 验证日志输出格式
- 测试边界情况（无效参数、重复销毁等）

### 集成测试

`tests/integration/test_effect_system.py`：
- 测试完整场景（创建→设置属性→销毁）
- 测试坐标绑定和单位绑定
- 测试多个特效同时存在

## 边界情况处理

1. **销毁不存在的特效**：记录警告日志，返回 `False`
2. **无效的模型路径**：原样接受，仅记录日志（不验证）
3. **目标单位已死亡**：仍创建特效，但记录警告

## 设计决策

### 为什么选择极简日志方案？

1. 符合 JASS Runner "纯模拟" 的定位
2. 与项目其他系统保持一致的复杂度
3. 魔兽 JASS 中特效通常是一次性的，状态查询需求较少
4. 实现快速，代码量少

### 为什么原样记录模型路径？

1. 简化实现，避免不必要的路径处理
2. 用户可以通过日志直接看到原始路径
3. 路径格式错误不会影响模拟执行

## 参考

- 项目编码规范：`CLAUDE.md`
- 物品系统实现：`docs/plans/2026-03-03-item-system-design.md`
