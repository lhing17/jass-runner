# Sound系统实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现Sound相关native函数，支持CreateSoundFromLabel创建声音对象，以及PlaySound、StopSound、KillSoundWhenDone等操作。

**Architecture:** 复用现有Handle管理模式，创建Sound类继承Handle，在HandleManager中统一管理声音对象的生命周期。

**Tech Stack:** Python, pytest, 项目现有的Handle管理框架

---

## 前置检查

### Task 0: 检查现有代码结构

**Files:**
- Read: `src/jass_runner/natives/handle.py`
- Read: `src/jass_runner/natives/manager.py`
- Read: `src/jass_runner/natives/sound_natives.py`

**目的:** 确认现有代码结构，为后续实现做准备。

---

## Phase 1: 核心数据结构

### Task 1: 添加Sound类和HandleType.SOUND

**Files:**
- Modify: `src/jass_runner/natives/handle.py`

**Step 1: 在HandleType枚举中添加SOUND**

```python
class HandleType(Enum):
    """Handle类型枚举。"""
    EFFECT = "effect"
    SOUND = "sound"  # 新增
```

**Step 2: 在文件末尾添加Sound类**

```python
class Sound(Handle):
    """声音对象，代表一个JASS sound handle。

    用于管理游戏中的声音资源，支持播放、停止等操作。
    """

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
        """初始化声音对象。

        参数：
            handle_id: 唯一标识符
            sound_label: 声音标签（如"Rescue"）
            looping: 是否循环播放
            is3D: 是否为3D音效
            stopwhenoutofrange: 超出范围时是否停止
            fadeInRate: 淡入速率
            fadeOutRate: 淡出速率
        """
        super().__init__(handle_id, HandleType.SOUND)
        self.sound_label = sound_label
        self.looping = looping
        self.is3D = is3D
        self.stopwhenoutofrange = stopwhenoutofrange
        self.fadeInRate = fadeInRate
        self.fadeOutRate = fadeOutRate
        self.is_playing = False
        self.kill_when_done = False

    def __repr__(self) -> str:
        """返回声音对象的字符串表示。"""
        return (f"Sound(id={self.id}, label='{self.sound_label}', "
                f"playing={self.is_playing})")
```

**Step 3: 确保Sound类被导出**

在 `src/jass_runner/natives/handle.py` 的 `__all__` 列表中添加 `Sound`（如果存在的话）。

**Step 4: Commit**

```bash
git add src/jass_runner/natives/handle.py
git commit -m "feat(sound): 添加Sound类和HandleType.SOUND枚举"
```

---

### Task 2: 在HandleManager中添加声音管理方法

**Files:**
- Modify: `src/jass_runner/natives/manager.py`

**Step 1: 导入Sound类**

在文件顶部添加：
```python
from jass_runner.natives.handle import Effect, Sound, HandleType
```

**Step 2: 在HandleManager类中添加声音管理方法**

在 `create_effect_target` 方法之后添加：

```python
    def create_sound(
        self,
        sound_label: str,
        looping: bool,
        is3D: bool,
        stopwhenoutofrange: bool,
        fadeInRate: int,
        fadeOutRate: int
    ) -> Sound:
        """创建声音对象。

        参数：
            sound_label: 声音标签（如"Rescue"）
            looping: 是否循环播放
            is3D: 是否为3D音效
            stopwhenoutofrange: 超出范围时是否停止
            fadeInRate: 淡入速率
            fadeOutRate: 淡出速率

        返回：
            创建的Sound对象
        """
        handle_id = self._next_handle_id
        self._next_handle_id += 1

        sound = Sound(
            handle_id=handle_id,
            sound_label=sound_label,
            looping=looping,
            is3D=is3D,
            stopwhenoutofrange=stopwhenoutofrange,
            fadeInRate=fadeInRate,
            fadeOutRate=fadeOutRate
        )

        self._handles[handle_id] = sound
        logger.info(
            f"[CreateSoundFromLabel] 声音已创建: "
            f"ID={handle_id}, 标签={sound_label}, 循环={looping}"
        )
        return sound

    def destroy_sound(self, sound: Sound) -> bool:
        """销毁声音对象。

        参数：
            sound: 要销毁的声音对象

        返回：
            销毁成功返回True，声音已死亡返回False
        """
        if sound.is_dead:
            return False

        sound.mark_dead()
        if sound.id in self._handles:
            del self._handles[sound.id]

        logger.info(f"[DestroySound] 声音已销毁: ID={sound.id}")
        return True
```

**Step 3: Commit**

```bash
git add src/jass_runner/natives/manager.py
git commit -m "feat(sound): 在HandleManager中添加声音创建和销毁方法"
```

---

## Phase 2: Native函数实现

### Task 3: 实现CreateSoundFromLabel

**Files:**
- Modify: `src/jass_runner/natives/sound_natives.py`
- Create: `tests/natives/test_sound_natives.py`

**Step 1: 编写失败测试**

```python
import pytest
from unittest.mock import MagicMock
from jass_runner.natives.sound_natives import CreateSoundFromLabel
from jass_runner.natives.handle import Sound


class TestCreateSoundFromLabel:
    """测试CreateSoundFromLabel native函数。"""

    def test_create_sound_from_label_returns_sound(self):
        """测试CreateSoundFromLabel返回Sound对象。"""
        # 准备
        native = CreateSoundFromLabel()
        mock_state = MagicMock()
        mock_manager = MagicMock()
        mock_sound = MagicMock(spec=Sound)
        mock_sound.id = 1
        mock_manager.create_sound.return_value = mock_sound
        mock_state.handle_manager = mock_manager

        # 执行
        result = native.execute(
            mock_state,
            "Rescue",
            False,
            False,
            False,
            10000,
            10000
        )

        # 验证
        assert result == mock_sound
        mock_manager.create_sound.assert_called_once_with(
            "Rescue", False, False, False, 10000, 10000
        )
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_sound_natives.py::TestCreateSoundFromLabel::test_create_sound_from_label_returns_sound -v
```

Expected: FAIL - CreateSoundFromLabel未定义或参数不匹配

**Step 3: 实现CreateSoundFromLabel**

在 `src/jass_runner/natives/sound_natives.py` 末尾添加：

```python
class CreateSoundFromLabel(NativeFunction):
    """从标签创建声音对象。"""

    @property
    def name(self) -> str:
        return "CreateSoundFromLabel"

    def execute(
        self,
        state_context,
        sound_label: str,
        looping: bool,
        is3D: bool,
        stopwhenoutofrange: bool,
        fadeInRate: int,
        fadeOutRate: int
    ) -> Sound:
        """从标签创建声音对象。

        参数：
            state_context: 状态上下文
            sound_label: 声音标签（如"Rescue"）
            looping: 是否循环播放
            is3D: 是否为3D音效
            stopwhenoutofrange: 超出范围时是否停止
            fadeInRate: 淡入速率
            fadeOutRate: 淡出速率

        返回：
            创建的Sound对象
        """
        handle_manager = state_context.handle_manager
        return handle_manager.create_sound(
            sound_label,
            looping,
            is3D,
            stopwhenoutofrange,
            fadeInRate,
            fadeOutRate
        )
```

**Step 4: 添加Sound导入**

在文件顶部添加：
```python
from jass_runner.natives.handle import Sound
```

**Step 5: 运行测试验证通过**

```bash
pytest tests/natives/test_sound_natives.py::TestCreateSoundFromLabel::test_create_sound_from_label_returns_sound -v
```

Expected: PASS

**Step 6: Commit**

```bash
git add tests/natives/test_sound_natives.py src/jass_runner/natives/sound_natives.py
git commit -m "feat(sound): 实现CreateSoundFromLabel native函数"
```

---

### Task 4: 实现PlaySound

**Files:**
- Modify: `src/jass_runner/natives/sound_natives.py`
- Modify: `tests/natives/test_sound_natives.py`

**Step 1: 编写失败测试**

在 `test_sound_natives.py` 中添加：

```python
class TestPlaySound:
    """测试PlaySound native函数。"""

    def test_play_sound_sets_is_playing(self):
        """测试PlaySound设置is_playing为True。"""
        # 准备
        native = PlaySound()
        mock_state = MagicMock()
        mock_sound = MagicMock(spec=Sound)
        mock_sound.id = 1
        mock_sound.sound_label = "Rescue"
        mock_sound.is_playing = False

        # 执行
        native.execute(mock_state, mock_sound)

        # 验证
        assert mock_sound.is_playing is True
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_sound_natives.py::TestPlaySound::test_play_sound_sets_is_playing -v
```

Expected: FAIL

**Step 3: 实现PlaySound**

在 `sound_natives.py` 中添加：

```python
class PlaySound(NativeFunction):
    """播放声音。"""

    @property
    def name(self) -> str:
        return "PlaySound"

    def execute(self, state_context, sound: Sound) -> None:
        """播放声音。

        参数：
            state_context: 状态上下文
            sound: 要播放的声音对象
        """
        sound.is_playing = True
        logger.info(
            f"[PlaySound] 声音开始播放: "
            f"ID={sound.id}, 标签={sound.sound_label}"
        )
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/natives/test_sound_natives.py::TestPlaySound::test_play_sound_sets_is_playing -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_sound_natives.py src/jass_runner/natives/sound_natives.py
git commit -m "feat(sound): 实现PlaySound native函数"
```

---

### Task 5: 实现StopSound

**Files:**
- Modify: `src/jass_runner/natives/sound_natives.py`
- Modify: `tests/natives/test_sound_natives.py`

**Step 1: 编写失败测试**

```python
class TestStopSound:
    """测试StopSound native函数。"""

    def test_stop_sound_clears_is_playing(self):
        """测试StopSound设置is_playing为False。"""
        # 准备
        native = StopSound()
        mock_state = MagicMock()
        mock_sound = MagicMock(spec=Sound)
        mock_sound.id = 1
        mock_sound.sound_label = "Rescue"
        mock_sound.is_playing = True

        # 执行
        native.execute(mock_state, mock_sound, False, 0, 0, 0)

        # 验证
        assert mock_sound.is_playing is False
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_sound_natives.py::TestStopSound::test_stop_sound_clears_is_playing -v
```

Expected: FAIL

**Step 3: 实现StopSound**

注意：JASS中StopSound签名是 `StopSound(sound, killWhenDone, fadeOut)`，但为了简化先实现基础版本。

```python
class StopSound(NativeFunction):
    """停止声音播放。"""

    @property
    def name(self) -> str:
        return "StopSound"

    def execute(
        self,
        state_context,
        sound: Sound,
        killWhenDone: bool = False,
        fadeOut: bool = False
    ) -> None:
        """停止声音播放。

        参数：
            state_context: 状态上下文
            sound: 要停止的声音对象
            killWhenDone: 是否在播放完成后销毁
            fadeOut: 是否淡出
        """
        sound.is_playing = False
        if killWhenDone:
            sound.kill_when_done = True
        logger.info(
            f"[StopSound] 声音已停止: "
            f"ID={sound.id}, 标签={sound.sound_label}, "
            f"淡出={fadeOut}"
        )
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/natives/test_sound_natives.py::TestStopSound::test_stop_sound_clears_is_playing -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_sound_natives.py src/jass_runner/natives/sound_natives.py
git commit -m "feat(sound): 实现StopSound native函数"
```

---

### Task 6: 实现KillSoundWhenDone

**Files:**
- Modify: `src/jass_runner/natives/sound_natives.py`
- Modify: `tests/natives/test_sound_natives.py`

**Step 1: 编写失败测试**

```python
class TestKillSoundWhenDone:
    """测试KillSoundWhenDone native函数。"""

    def test_kill_sound_when_done_sets_flag(self):
        """测试KillSoundWhenDone设置kill_when_done标志。"""
        # 准备
        native = KillSoundWhenDone()
        mock_state = MagicMock()
        mock_sound = MagicMock(spec=Sound)
        mock_sound.id = 1
        mock_sound.sound_label = "Rescue"
        mock_sound.kill_when_done = False

        # 执行
        native.execute(mock_state, mock_sound, True)

        # 验证
        assert mock_sound.kill_when_done is True
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_sound_natives.py::TestKillSoundWhenDone::test_kill_sound_when_done_sets_flag -v
```

Expected: FAIL

**Step 3: 实现KillSoundWhenDone**

```python
class KillSoundWhenDone(NativeFunction):
    """设置声音播放完成后自动销毁。"""

    @property
    def name(self) -> str:
        return "KillSoundWhenDone"

    def execute(self, state_context, sound: Sound, flag: bool) -> None:
        """设置声音播放完成后自动销毁。

        参数：
            state_context: 状态上下文
            sound: 声音对象
            flag: 是否播放完成后销毁
        """
        sound.kill_when_done = flag
        logger.info(
            f"[KillSoundWhenDone] 设置声音自动销毁: "
            f"ID={sound.id}, 标签={sound.sound_label}, 启用={flag}"
        )
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/natives/test_sound_natives.py::TestKillSoundWhenDone::test_kill_sound_when_done_sets_flag -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_sound_natives.py src/jass_runner/natives/sound_natives.py
git commit -m "feat(sound): 实现KillSoundWhenDone native函数"
```

---

## Phase 3: 注册和集成

### Task 7: 在工厂中注册Sound native函数

**Files:**
- Modify: `src/jass_runner/natives/factory.py`

**Step 1: 添加导入**

在文件顶部找到sound_natives的导入，添加新函数：

```python
from .sound_natives import (
    NewSoundEnvironment,
    SetAmbientDaySound,
    SetAmbientNightSound,
    SetMapMusic,
    CreateSoundFromLabel,
    PlaySound,
    StopSound,
    KillSoundWhenDone,
)
```

**Step 2: 在create_default_registry中注册**

找到 `# Sound natives` 注释部分，添加：

```python
        # Sound natives
        registry.register(NewSoundEnvironment())
        registry.register(SetAmbientDaySound())
        registry.register(SetAmbientNightSound())
        registry.register(SetMapMusic())
        registry.register(CreateSoundFromLabel())
        registry.register(PlaySound())
        registry.register(StopSound())
        registry.register(KillSoundWhenDone())
```

**Step 3: 运行所有sound相关测试**

```bash
pytest tests/natives/test_sound_natives.py -v
```

Expected: 所有测试PASS

**Step 4: Commit**

```bash
git add src/jass_runner/natives/factory.py
git commit -m "feat(sound): 在工厂中注册Sound相关native函数"
```

---

## Phase 4: 集成测试

### Task 8: 编写集成测试

**Files:**
- Create: `tests/integration/test_sound_system.py`

**Step 1: 编写集成测试**

```python
"""Sound系统集成测试。"""

import pytest
from unittest.mock import MagicMock
from jass_runner.natives.sound_natives import (
    CreateSoundFromLabel,
    PlaySound,
    StopSound,
    KillSoundWhenDone,
)
from jass_runner.natives.handle import Sound


class TestSoundSystemIntegration:
    """测试Sound系统的完整工作流程。"""

    def test_complete_sound_workflow(self):
        """测试完整的声音创建-播放-停止流程。"""
        # 准备
        mock_state = MagicMock()
        mock_manager = MagicMock()

        # 创建真实的Sound对象
        sound = Sound(
            handle_id=1,
            sound_label="Rescue",
            looping=False,
            is3D=False,
            stopwhenoutofrange=False,
            fadeInRate=10000,
            fadeOutRate=10000
        )
        mock_manager.create_sound.return_value = sound
        mock_state.handle_manager = mock_manager

        # 1. 创建声音
        create_native = CreateSoundFromLabel()
        result = create_native.execute(
            mock_state,
            "Rescue",
            False,
            False,
            False,
            10000,
            10000
        )
        assert isinstance(result, Sound)
        assert result.sound_label == "Rescue"
        assert result.is_playing is False

        # 2. 播放声音
        play_native = PlaySound()
        play_native.execute(mock_state, result)
        assert result.is_playing is True

        # 3. 设置播放完成后销毁
        kill_native = KillSoundWhenDone()
        kill_native.execute(mock_state, result, True)
        assert result.kill_when_done is True

        # 4. 停止声音
        stop_native = StopSound()
        stop_native.execute(mock_state, result, False, False)
        assert result.is_playing is False
```

**Step 2: 运行集成测试**

```bash
pytest tests/integration/test_sound_system.py -v
```

Expected: PASS

**Step 3: Commit**

```bash
git add tests/integration/test_sound_system.py
git commit -m "test(sound): 添加Sound系统集成测试"
```

---

## Phase 5: 验证

### Task 9: 运行所有测试

**Step 1: 运行所有sound相关测试**

```bash
pytest tests/natives/test_sound_natives.py tests/integration/test_sound_system.py -v
```

Expected: 所有测试PASS

**Step 2: 运行完整测试套件**

```bash
pytest
```

Expected: 所有测试PASS

**Step 3: 最终提交**

```bash
git log --oneline -5
```

确认所有提交都已记录。

---

## 总结

实现完成后，项目将支持以下JASS代码：

```jass
set bj_rescueSound = CreateSoundFromLabel("Rescue", false, false, false, 10000, 10000)
call PlaySound(bj_rescueSound)
call KillSoundWhenDone(bj_rescueSound, true)
call StopSound(bj_rescueSound, false, false)
```

**实现文件清单：**
- `src/jass_runner/natives/handle.py` - 添加Sound类和HandleType.SOUND
- `src/jass_runner/natives/manager.py` - 添加create_sound和destroy_sound方法
- `src/jass_runner/natives/sound_natives.py` - 添加CreateSoundFromLabel, PlaySound, StopSound, KillSoundWhenDone
- `src/jass_runner/natives/factory.py` - 注册新的native函数
- `tests/natives/test_sound_natives.py` - 单元测试
- `tests/integration/test_sound_system.py` - 集成测试
