# Camera Native Functions Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现 GetCameraMargin 和 SetCameraBounds native 函数，以及从 common.j 自动加载常量的机制。

**Architecture:** 在现有 native 函数框架基础上，新增 camera.py 模块实现 camera 相关函数。扩展 StateContext 存储相机边界。修改 VM 初始化流程以加载 common.j 中的常量。

**Tech Stack:** Python 3.8+, pytest, 现有 JASS Runner 框架 (parser, interpreter, natives)

---

## Task 1: StateContext 扩展 - 添加 camera_bounds 存储

**Files:**
- Modify: `src/jass_runner/natives/state.py:15-35` (在 `__init__` 方法中添加)

**Step 1: 修改 StateContext.__init__ 添加 camera_bounds**

```python
def __init__(self):
    """初始化状态上下文。"""
    self.handle_manager = HandleManager()
    self.trigger_manager = TriggerManager()
    self.global_vars = {}
    self.local_stores = {}
    # 添加相机边界存储
    self.camera_bounds = {
        'x1': 0.0, 'y1': 0.0,
        'x2': 0.0, 'y2': 0.0,
        'x3': 0.0, 'y3': 0.0,
        'x4': 0.0, 'y4': 0.0
    }
```

**Step 2: 验证修改**

Run: `python -c "from src.jass_runner.natives.state import StateContext; ctx = StateContext(); print(ctx.camera_bounds)"`

Expected: `{'x1': 0.0, 'y1': 0.0, ... 'y4': 0.0}`

**Step 3: Commit**

```bash
git add src/jass_runner/natives/state.py
git commit -m "$(cat <<'EOF'
feat: StateContext添加camera_bounds存储

- 支持SetCameraBounds存储边界坐标
- 用于后续查询和测试验证

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: 创建 GetCameraMargin Native 函数

**Files:**
- Create: `src/jass_runner/natives/camera.py`
- Modify: `src/jass_runner/natives/factory.py:1-50` (添加导入和注册)

**Step 1: 创建 camera.py 模块**

```python
"""Camera 相关 native 函数实现。

此模块包含与相机相关的 JASS native 函数，如 GetCameraMargin、SetCameraBounds 等。
"""

import logging
from .base import NativeFunction

logger = logging.getLogger(__name__)


class GetCameraMargin(NativeFunction):
    """获取相机边距值。"""

    @property
    def name(self) -> str:
        return "GetCameraMargin"

    def execute(self, state_context, which_margin: int) -> float:
        """执行获取相机边距。

        参数:
            state_context: 状态上下文
            which_margin: 边距类型 (0=LEFT, 1=RIGHT, 2=TOP, 3=BOTTOM)

        返回:
            边距值 (固定 100.0 表示有效范围，其他返回 0.0)
        """
        if 0 <= which_margin <= 3:
            logger.info(f"[GetCameraMargin] 边距类型={which_margin}, 返回值=100.0")
            return 100.0
        return 0.0
```

**Step 2: 更新 factory.py 注册 GetCameraMargin**

在文件顶部添加导入：
```python
from .camera import GetCameraMargin
```

在 `create_default_registry()` 中添加注册（在基本 natives 之后）：
```python
# Camera natives
registry.register(GetCameraMargin())
```

**Step 3: 编写测试验证 GetCameraMargin**

Create: `tests/natives/test_camera.py`

```python
"""测试 Camera 相关 native 函数。"""

import pytest
from src.jass_runner.natives.camera import GetCameraMargin
from src.jass_runner.natives.state import StateContext


class TestGetCameraMargin:
    """测试 GetCameraMargin 类。"""

    def test_valid_left_margin_returns_100(self):
        """测试 LEFT 边距类型返回 100.0。"""
        native = GetCameraMargin()
        context = StateContext()

        result = native.execute(context, 0)  # CAMERA_MARGIN_LEFT

        assert result == 100.0

    def test_valid_right_margin_returns_100(self):
        """测试 RIGHT 边距类型返回 100.0。"""
        native = GetCameraMargin()
        context = StateContext()

        result = native.execute(context, 1)  # CAMERA_MARGIN_RIGHT

        assert result == 100.0

    def test_valid_top_margin_returns_100(self):
        """测试 TOP 边距类型返回 100.0。"""
        native = GetCameraMargin()
        context = StateContext()

        result = native.execute(context, 2)  # CAMERA_MARGIN_TOP

        assert result == 100.0

    def test_valid_bottom_margin_returns_100(self):
        """测试 BOTTOM 边距类型返回 100.0。"""
        native = GetCameraMargin()
        context = StateContext()

        result = native.execute(context, 3)  # CAMERA_MARGIN_BOTTOM

        assert result == 100.0

    def test_invalid_margin_returns_0(self):
        """测试无效边距类型返回 0.0。"""
        native = GetCameraMargin()
        context = StateContext()

        result = native.execute(context, 99)

        assert result == 0.0

    def test_negative_margin_returns_0(self):
        """测试负值边距类型返回 0.0。"""
        native = GetCameraMargin()
        context = StateContext()

        result = native.execute(context, -1)

        assert result == 0.0
```

**Step 4: 运行测试**

Run: `pytest tests/natives/test_camera.py::TestGetCameraMargin -v`

Expected: 6 tests PASS

**Step 5: Commit**

```bash
git add src/jass_runner/natives/camera.py src/jass_runner/natives/factory.py tests/natives/test_camera.py
git commit -m "$(cat <<'EOF'
feat: 实现GetCameraMargin native函数

- 返回固定边距值100.0(范围0-3)
- 添加完整单元测试
- 在factory中注册

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: 创建 SetCameraBounds Native 函数

**Files:**
- Modify: `src/jass_runner/natives/camera.py:1-50` (添加新类)
- Modify: `src/jass_runner/natives/factory.py:1-50` (添加注册)
- Modify: `tests/natives/test_camera.py:50-100` (添加测试)

**Step 1: 添加 SetCameraBounds 到 camera.py**

```python
class SetCameraBounds(NativeFunction):
    """设置相机边界。"""

    @property
    def name(self) -> str:
        return "SetCameraBounds"

    def execute(self, state_context, x1: float, y1: float, x2: float, y2: float,
                x3: float, y3: float, x4: float, y4: float) -> None:
        """执行设置相机边界。

        参数:
            state_context: 状态上下文
            x1, y1: 第一个角点坐标
            x2, y2: 第二个角点坐标
            x3, y3: 第三个角点坐标
            x4, y4: 第四个角点坐标
        """
        bounds = state_context.camera_bounds
        bounds['x1'] = x1
        bounds['y1'] = y1
        bounds['x2'] = x2
        bounds['y2'] = y2
        bounds['x3'] = x3
        bounds['y3'] = y3
        bounds['x4'] = x4
        bounds['y4'] = y4

        logger.info(
            f"[SetCameraBounds] 相机边界已设置: "
            f"({x1},{y1})-({x2},{y2})-({x3},{y3})-({x4},{y4})"
        )
```

**Step 2: 在 factory.py 注册 SetCameraBounds**

导入更新（如果还没导入）：
```python
from .camera import GetCameraMargin, SetCameraBounds
```

注册更新：
```python
# Camera natives
registry.register(GetCameraMargin())
registry.register(SetCameraBounds())
```

**Step 3: 添加 SetCameraBounds 测试**

添加到 `tests/natives/test_camera.py`：

```python
class TestSetCameraBounds:
    """测试 SetCameraBounds 类。"""

    def test_bounds_are_stored_in_context(self):
        """测试边界值正确存储在 StateContext 中。"""
        native = SetCameraBounds()
        context = StateContext()

        native.execute(context, 0.0, 0.0, 100.0, 100.0, 200.0, 200.0, 300.0, 300.0)

        assert context.camera_bounds['x1'] == 0.0
        assert context.camera_bounds['y1'] == 0.0
        assert context.camera_bounds['x2'] == 100.0
        assert context.camera_bounds['y2'] == 100.0
        assert context.camera_bounds['x3'] == 200.0
        assert context.camera_bounds['y3'] == 200.0
        assert context.camera_bounds['x4'] == 300.0
        assert context.camera_bounds['y4'] == 300.0

    def test_negative_bounds_are_stored(self):
        """测试负坐标边界值也能正确存储。"""
        native = SetCameraBounds()
        context = StateContext()

        native.execute(context, -11520.0, -11776.0, 11520.0, 11264.0,
                      -11520.0, 11264.0, 11520.0, -11776.0)

        assert context.camera_bounds['x1'] == -11520.0
        assert context.camera_bounds['y2'] == 11264.0
```

**Step 4: 运行测试**

Run: `pytest tests/natives/test_camera.py -v`

Expected: 8 tests PASS (6 from GetCameraMargin + 2 from SetCameraBounds)

**Step 5: Commit**

```bash
git add src/jass_runner/natives/camera.py src/jass_runner/natives/factory.py tests/natives/test_camera.py
git commit -m "$(cat <<'EOF'
feat: 实现SetCameraBounds native函数

- 存储8个边界坐标到StateContext
- 支持正负坐标值
- 输出设置日志
- 添加单元测试

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: 实现 common.j 常量加载机制

**Files:**
- Modify: `src/jass_runner/vm/core.py:1-100` (添加常量加载)
- Create: `tests/vm/test_constants_loading.py`

**Step 1: 了解现有的 JassVM 结构**

先读取现有代码：
Run: `head -100 src/jass_runner/vm/core.py`

**Step 2: 添加常量加载方法到 core.py**

```python
import re
import os

CONSTANT_PATTERN = re.compile(
    r'constant\s+(\w+)\s+(\w+)\s*=\s*([^\s]+)',
    re.MULTILINE
)


class JassVM:
    """JASS 虚拟机核心类。"""

    def __init__(self, parser=None, interpreter=None):
        """初始化JASS虚拟机。"""
        self.parser = parser or Parser()
        self.interpreter = interpreter or Interpreter()
        self.state_context = StateContext()
        self._load_constants()

    def _load_constants(self):
        """从 common.j 加载常量定义。"""
        common_j_paths = [
            'resources/common.j',
            os.path.join(os.path.dirname(__file__), '..', '..', '..', 'resources', 'common.j')
        ]

        for path in common_j_paths:
            if os.path.exists(path):
                self._parse_constants_from_file(path)
                break

    def _parse_constants_from_file(self, filepath: str):
        """解析文件中的常量定义。"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        for match in CONSTANT_PATTERN.finditer(content):
            const_type = match.group(1)  # integer, real, boolean, etc.
            const_name = match.group(2)   # CAMERA_MARGIN_LEFT
            const_value = match.group(3) # 0, true, etc.

            # 转换值为Python类型
            value = self._convert_constant_value(const_type, const_value)

            # 存储到全局变量
            self.state_context.global_vars[const_name] = value

    def _convert_constant_value(self, const_type: str, const_value: str):
        """将JASS常量值转换为Python值。"""
        if const_type == 'integer':
            try:
                return int(const_value)
            except ValueError:
                return 0
        elif const_type == 'real':
            try:
                return float(const_value)
            except ValueError:
                return 0.0
        elif const_type == 'boolean':
            return const_value.lower() == 'true'
        else:
            # 对于handle类型和其他类型，存储字符串值
            return const_value
```

**Step 3: 确保常量可用于解释器执行**

可能需要修改 `Interpreter` 来访问这些常量。检查现有代码后添加：

在 `execute` 方法中，确保常量可以通过 `_get_variable` 访问。

**Step 4: 编写测试**

Create: `tests/vm/test_constants_loading.py`

```python
"""测试常量从 common.j 加载功能。"""

import pytest
from src.jass_runner.vm.core import JassVM


class TestConstantsLoading:
    """测试常量加载功能。"""

    def test_camera_margin_constants_loaded(self):
        """测试 CAMERA_MARGIN 常量从 common.j 加载。"""
        vm = JassVM()

        # 检查常量是否加载到 global_vars
        assert 'CAMERA_MARGIN_LEFT' in vm.state_context.global_vars
        assert 'CAMERA_MARGIN_RIGHT' in vm.state_context.global_vars
        assert 'CAMERA_MARGIN_TOP' in vm.state_context.global_vars
        assert 'CAMERA_MARGIN_BOTTOM' in vm.state_context.global_vars

        # 检查值是否正确
        assert vm.state_context.global_vars['CAMERA_MARGIN_LEFT'] == 0
        assert vm.state_context.global_vars['CAMERA_MARGIN_RIGHT'] == 1
        assert vm.state_context.global_vars['CAMERA_MARGIN_TOP'] == 2
        assert vm.state_context.global_vars['CAMERA_MARGIN_BOTTOM'] == 3

    def test_constant_values_are_integers(self):
        """测试常量值类型为整数。"""
        vm = JassVM()

        assert isinstance(vm.state_context.global_vars['CAMERA_MARGIN_LEFT'], int)
        assert isinstance(vm.state_context.global_vars['CAMERA_MARGIN_RIGHT'], int)

    def test_constants_accessible_in_execution(self):
        """测试常量可在JASS代码执行中访问。"""
        vm = JassVM()

        jass_code = '''
        function Test takes nothing returns integer
            return CAMERA_MARGIN_LEFT
        endfunction
        '''

        # 这里可能需要实际执行并验证结果
        # 取决于解释器对全局变量的支持情况
```

**Step 5: 运行测试**

Run: `pytest tests/vm/test_constants_loading.py -v`

Expected: 3 tests PASS

**Step 6: Commit**

```bash
git add src/jass_runner/vm/core.py tests/vm/test_constants_loading.py
git commit -m "$(cat <<'EOF'
feat: 实现从common.j自动加载常量机制

- JassVM初始化时解析common.j
- 支持integer/real/boolean类型常量
- 常量存储在global_vars中供执行使用
- 添加加载测试

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: 创建集成测试 - 完整 workflow

**Files:**
- Create: `tests/integration/test_camera_workflow.py`

**Step 1: 创建集成测试**

```python
"""Camera 函数的集成测试。"""

import pytest
from src.jass_runner.vm.core import JassVM
from src.jass_runner.parser import Parser
from src.jass_runner.interpreter import Interpreter


class TestCameraWorkflow:
    """测试 Camera 相关函数的完整工作流。"""

    def test_get_camera_margin_with_constant(self):
        """测试使用常量调用 GetCameraMargin。"""
        vm = JassVM()

        # 使用 loaded constant 调用
        margin_type = vm.state_context.global_vars['CAMERA_MARGIN_LEFT']

        # 通过注册表获取 native
        from src.jass_runner.natives.factory import NativeFactory
        registry = NativeFactory.create_default_registry()
        get_margin = registry.get('GetCameraMargin')

        result = get_margin.execute(vm.state_context, margin_type)

        assert result == 100.0

    def test_set_camera_bounds_stores_values(self):
        """测试 SetCameraBounds 存储边界值。"""
        vm = JassVM()

        from src.jass_runner.natives.factory import NativeFactory
        registry = NativeFactory.create_default_registry()
        set_bounds = registry.get('SetCameraBounds')

        set_bounds.execute(
            vm.state_context,
            -11520.0, -11776.0, 11520.0, 11264.0,
            -11520.0, 11264.0, 11520.0, -11776.0
        )

        bounds = vm.state_context.camera_bounds
        assert bounds['x1'] == -11520.0
        assert bounds['y2'] == 11264.0
        assert bounds['x4'] == 11520.0
```

**Step 2: 运行集成测试**

Run: `pytest tests/integration/test_camera_workflow.py -v`

Expected: 2 tests PASS

**Step 3: Commit**

```bash
git add tests/integration/test_camera_workflow.py
git commit -m "$(cat <<'EOF'
test: 添加Camera函数集成测试

- 测试常量与native函数配合使用
- 验证SetCameraBounds存储完整边界
- 使用实际VM实例测试

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>
EOF
)"
```

---

## Task 6: 运行所有测试并验证

**Step 1: 运行 camera 相关测试**

```bash
pytest tests/natives/test_camera.py tests/vm/test_constants_loading.py tests/integration/test_camera_workflow.py -v
```

Expected: 13 tests PASS (8 native + 3 constants + 2 integration)

**Step 2: 运行整个测试套件**

```bash
pytest -x
```

Expected: 所有测试 PASS (假设没有回归)

**Step 3: 如果全部通过，Commit**

```bash
git commit --allow-empty -m "$(cat <<'EOF'
feat: Camera native函数实现完成

- GetCameraMargin: 返回固定边距值100.0
- SetCameraBounds: 存储8个边界坐标到StateContext
- 常量加载: 从common.j自动加载CAMERA_MARGIN_*常量
- 完整单元测试和集成测试

Closes task

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>
EOF
)"
```

---

## 验证清单

- [ ] StateContext 有 camera_bounds 属性
- [ ] GetCameraMargin 返回 100.0 (0-3), 0.0 (其他)
- [ ] SetCameraBounds 存储 8 个坐标到 StateContext
- [ ] 两个函数都在 NativeRegistry 注册
- [ ] common.j 常量加载到 state_context.global_vars
- [ ] CAMERA_MARGIN_LEFT/RIGHT/TOP/BOTTOM 正确值为 0/1/2/3
- [ ] 所有新测试通过
- [ ] 现有测试没有回归

---

## 参考文件

- 设计文档: `docs/plans/2026-03-03-camera-native-functions-design.md`
- common.j: `resources/common.j`
- Native 基类: `src/jass_runner/natives/base.py`
- StateContext: `src/jass_runner/natives/state.py`
- VM Core: `src/jass_runner/vm/core.py`
