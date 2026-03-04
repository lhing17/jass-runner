# Sound系统设计方案

## 概述

本文档描述JASS Runner中Sound系统的实现方案，支持 `CreateSoundFromLabel` 及相关声音操作。

## 需求

支持JASS代码：
```jass
set bj_rescueSound = CreateSoundFromLabel("Rescue", false, false, false, 10000, 10000)
call PlaySound(bj_rescueSound)
```

## 架构设计

### 1. Sound类

位置：`src/jass_runner/natives/handle.py`

```python
class Sound(Handle):
    """声音对象，代表一个JASS sound handle。"""

    def __init__(
        self,
        handle_id: int,
        sound_label: str,
        looping: bool,
        is3D: bool,
        stopwhenoutofrange: bool,
        fadeInRate: int,
        fadeOutRate: int
    ):
        super().__init__(handle_id, HandleType.SOUND)
        self.sound_label = sound_label
        self.looping = looping
        self.is3D = is3D
        self.stopwhenoutofrange = stopwhenoutofrange
        self.fadeInRate = fadeInRate
        self.fadeOutRate = fadeOutRate
        self.is_playing = False
```

### 2. HandleType扩展

在 `HandleType` 枚举中添加 `SOUND = "sound"`。

### 3. HandleManager扩展

位置：`src/jass_runner/natives/manager.py`

添加方法：
- `create_sound(...) -> Sound`: 创建声音对象
- `destroy_sound(sound: Sound) -> bool`: 销毁声音对象

### 4. Native函数

位置：`src/jass_runner/natives/sound_natives.py`

| 函数名 | 功能 |
|--------|------|
| `CreateSoundFromLabel` | 从标签创建声音，返回sound handle |
| `PlaySound` | 播放声音 |
| `StopSound` | 停止声音 |
| `KillSoundWhenDone` | 设置声音播放完成后自动销毁 |

### 5. 工厂注册

位置：`src/jass_runner/natives/factory.py`

在 `create_default_registry` 中注册新的native函数。

## 数据流

```
JASS代码
    ↓
CreateSoundFromLabel native
    ↓
HandleManager.create_sound()
    ↓
返回 Sound 对象 (作为handle使用)
    ↓
PlaySound/StopSound 操作 Sound 对象
```

## 测试策略

1. 单元测试：`CreateSoundFromLabel` 返回有效的Sound对象
2. 单元测试：`PlaySound` 设置 `is_playing = True`
3. 单元测试：`StopSound` 设置 `is_playing = False`
4. 集成测试：完整的声音创建-播放-停止流程

## 实现计划

参考：`2026-03-04-sound-system-implementation.md`
