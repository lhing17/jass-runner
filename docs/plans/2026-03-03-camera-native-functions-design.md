# Camera Native Functions 设计文档

**日期**: 2026-03-03
**主题**: 实现 GetCameraMargin 和 SetCameraBounds native 函数
**状态**: 已批准，待实现

## 1. 概述

本设计文档描述 JASS Runner 项目中 Camera 相关 native 函数的实现方案，包括 `GetCameraMargin` 和 `SetCameraBounds` 两个核心函数，以及相关的常量加载机制。

## 2. 设计目标

1. 实现 `GetCameraMargin` native 函数，返回固定的相机边距值
2. 实现 `SetCameraBounds` native 函数，存储相机边界坐标供后续查询
3. 建立从 `common.j` 自动加载常量到虚拟机的机制
4. 保持与现有 native 函数框架的一致性

## 3. 功能设计

### 3.1 GetCameraMargin

**函数签名**: `native GetCameraMargin takes integer whichMargin returns real`

**参数说明**:
- `whichMargin`: 边距类型，对应常量:
  - `CAMERA_MARGIN_LEFT = 0`
  - `CAMERA_MARGIN_RIGHT = 1`
  - `CAMERA_MARGIN_TOP = 2`
  - `CAMERA_MARGIN_BOTTOM = 3`

**返回值**:
- 固定返回 `100.0` (简化实现)
- 有效范围外的参数返回 `0.0`

**日志输出**: `[GetCameraMargin] 边距类型=X, 返回值=100.0`

### 3.2 SetCameraBounds

**函数签名**: `native SetCameraBounds takes real x1, real y1, real x2, real y2, real x3, real y3, real x4, real y4 returns nothing`

**参数说明**: 8个 real 值表示相机边界的4个角点坐标

**行为**:
1. 将8个参数存储在 `StateContext.camera_bounds` 字典中
2. 输出日志确认设置完成
3. 支持后续通过 getter 函数查询 (未来扩展)

**日志输出**: `[SetCameraBounds] 相机边界已设置: (x1,y1)-(x2,y2)-(x3,y3)-(x4,y4)`

### 3.3 常量加载机制

**目标**: 在 VM 初始化时，自动从 `common.j` 或 `resources/common.j` 加载所有 `constant` 定义到全局符号表。

**实现方式**:
1. 修改 `JassVM` 初始化流程
2. 在加载用户脚本之前，先解析 `common.j`
3. 提取 `constant integer/string/real/boolean` 定义
4. 注册到全局执行上下文的符号表中
5. 用户脚本可直接引用如 `CAMERA_MARGIN_LEFT` 等常量

## 4. 架构设计

### 4.1 新增模块

```
src/jass_runner/natives/
├── __init__.py
├── base.py              # NativeFunction 抽象基类
├── registry.py          # NativeRegistry 注册表
├── factory.py           # NativeFactory 工厂 (更新)
├── state.py             # StateContext 状态管理 (更新)
├── basic.py             # 基础 native 函数
├── math_core.py         # 数学函数
└── camera.py            # [新增] Camera 相关 native 函数
```

### 4.2 StateContext 扩展

在 `StateContext` 类中添加:

```python
class StateContext:
    def __init__(self):
        # ... 现有属性 ...
        self.camera_bounds = {
            'x1': 0.0, 'y1': 0.0,
            'x2': 0.0, 'y2': 0.0,
            'x3': 0.0, 'y3': 0.0,
            'x4': 0.0, 'y4': 0.0
        }
```

### 4.3 类设计

#### GetCameraMargin

```python
class GetCameraMargin(NativeFunction):
    """获取相机边距值。"""

    @property
    def name(self) -> str:
        return "GetCameraMargin"

    def execute(self, state_context, which_margin: int) -> float:
        """执行获取相机边距。

        参数:
            state_context: 状态上下文
            which_margin: 边距类型 (0-3)

        返回:
            边距值 (固定 100.0)
        """
        if 0 <= which_margin <= 3:
            logger.info(f"[GetCameraMargin] 边距类型={which_margin}, 返回值=100.0")
            return 100.0
        return 0.0
```

#### SetCameraBounds

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
            x1, y1, x2, y2, x3, y3, x4, y4: 边界坐标
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

        logger.info(f"[SetCameraBounds] 相机边界已设置: "
                   f"({x1},{y1})-({x2},{y2})-({x3},{y3})-({x4},{y4})")
```

## 5. 常量加载实现

### 5.1 常量解析流程

在 `JassVM.execute()` 方法中:

```python
def execute(self, code: str) -> ExecutionResult:
    # 1. 首先解析 common.j (如果存在)
    constants = self._load_constants_from_common_j()

    # 2. 注册常量到全局符号表
    for name, value in constants.items():
        self.global_context.define_variable(name, value)

    # 3. 解析并执行用户脚本
    ast = self.parser.parse(code)
    result = self.interpreter.execute(ast)
    return result
```

### 5.2 常量提取正则

```python
CONSTANT_PATTERN = re.compile(
    r'constant\s+(\w+)\s+(\w+)\s*=\s*([^\s]+)',
    re.MULTILINE
)
```

## 6. 测试策略

### 6.1 单元测试

```python
class TestGetCameraMargin:
    def test_valid_margin_returns_100(self):
        """测试有效边距类型返回 100.0。"""
        # 准备
        native = GetCameraMargin()
        context = MockStateContext()

        # 执行
        result = native.execute(context, 0)  # LEFT

        # 验证
        assert result == 100.0

    def test_invalid_margin_returns_0(self):
        """测试无效边距类型返回 0.0。"""
        native = GetCameraMargin()
        context = MockStateContext()

        result = native.execute(context, 99)

        assert result == 0.0
```

### 6.2 集成测试

```python
def test_camera_bounds_full_workflow():
    """测试相机边界完整工作流。"""
    code = '''
    function Test takes nothing returns nothing
        call SetCameraBounds(0.0, 0.0, 100.0, 100.0, 200.0, 200.0, 300.0, 300.0)
        call DisplayTextToPlayer(Player(0), 0.0, 0.0, "Camera bounds set")
    endfunction
    '''

    vm = JassVM()
    vm.load_common_j()
    result = vm.execute(code)

    assert result.success
    assert vm.state_context.camera_bounds['x1'] == 0.0
```

## 7. 日志与监控

| 函数 | 日志级别 | 输出示例 |
|------|----------|----------|
| GetCameraMargin | INFO | `[GetCameraMargin] 边距类型=0, 返回值=100.0` |
| SetCameraBounds | INFO | `[SetCameraBounds] 相机边界已设置: (0.0,0.0)-(100.0,100.0)...` |

## 8. 部署清单

- [ ] 创建 `src/jass_runner/natives/camera.py`
- [ ] 更新 `src/jass_runner/natives/factory.py` 注册新函数
- [ ] 更新 `src/jass_runner/natives/state.py` 添加 camera_bounds
- [ ] 实现常量加载机制
- [ ] 添加单元测试
- [ ] 添加集成测试
- [ ] 更新文档

## 9. 风险评估

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|----------|
| 常量加载性能问题 | 低 | 中 | 仅在 VM 初始化时加载一次 |
| 与现有系统冲突 | 低 | 高 | 充分测试，保持向后兼容 |
| StateContext 扩展复杂度 | 中 | 低 | 明确分隔 camera 相关状态 |

## 10. 附录

### 10.1 参考代码

来自 `resources/common.j`:

```jass
// Camera Margin constants
constant integer CAMERA_MARGIN_LEFT    = 0
constant integer CAMERA_MARGIN_RIGHT   = 1
constant integer CAMERA_MARGIN_TOP     = 2
constant integer CAMERA_MARGIN_BOTTOM  = 3

// Native declarations
native GetCameraMargin takes integer whichMargin returns real
native SetCameraBounds takes real x1, real y1, real x2, real y2, real x3, real y3, real x4, real y4 returns nothing
```

### 10.2 使用示例

```jass
// 典型的 SetCameraBounds 调用
call SetCameraBounds(
    -11520.0 + GetCameraMargin(CAMERA_MARGIN_LEFT),
    -11776.0 + GetCameraMargin(CAMERA_MARGIN_BOTTOM),
    11520.0 - GetCameraMargin(CAMERA_MARGIN_RIGHT),
    11264.0 - GetCameraMargin(CAMERA_MARGIN_TOP),
    -11520.0 + GetCameraMargin(CAMERA_MARGIN_LEFT),
    11264.0 - GetCameraMargin(CAMERA_MARGIN_TOP),
    11520.0 - GetCameraMargin(CAMERA_MARGIN_RIGHT),
    -11776.0 + GetCameraMargin(CAMERA_MARGIN_BOTTOM)
)
```
