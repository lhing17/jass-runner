# Version系统设计方案

## 概述

本文档描述JASS Runner中Version系统的实现方案，支持 `VersionGet` 和 `ConvertVersion` native函数。

## 需求

支持JASS代码：
```jass
if VersionGet() == VERSION_FROZEN_THRONE then
    // 执行冰封王座特定逻辑
endif
```

## 架构设计

采用简单整数常量方案：
- `VERSION_REIGN_OF_CHAOS = 0` (混乱之治)
- `VERSION_FROZEN_THRONE = 1` (冰封王座)
- `VersionGet()` 始终返回 `1` (冰封王座)
- `ConvertVersion(v)` 直接返回传入的整数

## 实现方案

### 1. 版本常量定义

位置：`src/jass_runner/natives/version_natives.py`

```python
# 版本常量
VERSION_REIGN_OF_CHAOS = 0   # 混乱之治
VERSION_FROZEN_THRONE = 1    # 冰封王座
```

### 2. VersionGet Native函数

```python
class VersionGet(NativeFunction):
    """获取当前游戏版本。"""

    @property
    def name(self) -> str:
        return "VersionGet"

    def execute(self, state_context) -> int:
        """获取当前游戏版本。

        在本模拟器中，始终返回冰封王座版本。

        返回：
            VERSION_FROZEN_THRONE (1)
        """
        return VERSION_FROZEN_THRONE
```

### 3. ConvertVersion Native函数

```python
class ConvertVersion(NativeFunction):
    """转换版本类型。"""

    @property
    def name(self) -> str:
        return "ConvertVersion"

    def execute(self, state_context, version: int) -> int:
        """转换版本类型。

        在本实现中，直接返回传入的版本值。

        参数：
            state_context: 状态上下文
            version: 版本整数值

        返回：
            传入的版本值
        """
        return version
```

### 4. 工厂注册

在 `src/jass_runner/natives/factory.py` 中注册新的native函数。

## 使用示例

```jass
globals
    integer bj_gameVersion
endglobals

function InitGlobals takes nothing returns nothing
    set bj_gameVersion = VersionGet()
endfunction
```

## 测试策略

1. 单元测试：`VersionGet` 返回 `VERSION_FROZEN_THRONE` (1)
2. 单元测试：`ConvertVersion` 返回传入的值
3. 单元测试：验证常量值正确

## 实现计划

参考：`2026-03-04-version-system-implementation.md`
