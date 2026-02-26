# JASS模拟运行工具状态管理系统设计文档

## 项目背景

JASS Runner项目已完成前三个阶段的核心功能实现，包括：
1. **Phase 1**: 项目设置和核心基础设施
2. **Phase 2**: 解释器和执行引擎
3. **Phase 3**: Native函数框架

目前native函数实现存在一个关键问题：每个native函数独立模拟，没有在内存中保存数据的状态。例如：
- `CreateUnit`创建一个单位，只是生成一个ID并输出日志
- `GetUnitState`查询单位状态，返回固定值（100.0生命值）
- `KillUnit`杀死单位，只是输出日志，不更新单位状态

这导致模拟不真实，无法支持复杂的脚本测试。

## 问题描述

### 当前实现局限性
1. **状态孤立**：每个native函数调用不共享状态
2. **无内存模型**：没有在Python内存中维护JASS handle的状态
3. **类型不安全**：没有严格的handle类型体系
4. **生命周期缺失**：没有handle的创建、使用、销毁生命周期管理

### 需求分析
基于项目目标（魔兽地图开发者测试和自动化测试），需要实现：
1. **状态持久化**：在内存中维护JASS handle的状态
2. **类型体系**：实现JASS handle的层级关系（Handle → Unit/Timer等）
3. **生命周期管理**：支持handle的创建、查询、销毁
4. **状态一致性**：`CreateUnit`、`GetUnitState`、`KillUnit`等函数共享同一状态

## 设计方案：集中式Handle管理器

### 总体架构

```
┌─────────────────────────────────────────────────────────┐
│                    StateContext                         │
│                                                         │
│  ┌─────────────────┐  ┌────────────────────────────┐  │
│  │ HandleManager   │  │ Global/Local State Storage │  │
│  │                 │  │                            │  │
│  │ • 创建/销毁handle │  │ • 全局变量               │  │
│  │ • 类型安全查询    │  │ • 上下文局部状态         │  │
│  │ • 存活状态管理    │  │ • 状态隔离               │  │
│  └─────────────────┘  └────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
         │                            │
         ▼                            ▼
┌─────────────────┐        ┌─────────────────────┐
│  ExecutionContext │        │    NativeFunction   │
│                  │        │                     │
│ • 变量作用域     │        │ • 访问HandleManager │
│ • 状态上下文引用 │        │ • 状态感知执行      │
│ • 父上下文链     │        │ • 类型安全操作      │
└─────────────────┘        └─────────────────────┘
```

### 1. Handle类体系设计

#### 继承层次结构
```
Handle (基类)
├── Unit (单位)
│   ├── HeroUnit (英雄单位)
│   └── Building (建筑)
├── Timer (计时器)
├── Location (位置)
├── Group (单位组)
└── ... (其他JASS handle类型)
```

#### Handle基类
```python
class Handle:
    """所有JASS handle的基类。

    属性：
        id: 唯一标识符（字符串）
        type_name: handle类型名称
        alive: 是否存活
    """

    def __init__(self, handle_id: str, type_name: str):
        self.id = handle_id
        self.type_name = type_name
        self.alive = True

    def destroy(self):
        """标记handle为销毁状态。"""
        self.alive = False

    def is_alive(self) -> bool:
        """检查handle是否存活。"""
        return self.alive
```

#### Unit类示例
```python
class Unit(Handle):
    """单位handle。

    属性：
        unit_type: 单位类型代码（如'hfoo'）
        player_id: 所属玩家ID
        x, y: 位置坐标
        facing: 面向角度
        life: 当前生命值
        max_life: 最大生命值
        mana: 当前魔法值
        max_mana: 最大魔法值
    """

    def __init__(self, handle_id: str, unit_type: str, player_id: int,
                 x: float, y: float, facing: float):
        super().__init__(handle_id, "unit")
        self.unit_type = unit_type
        self.player_id = player_id
        self.x = x
        self.y = y
        self.facing = facing
        self.life = 100.0
        self.max_life = 100.0
        self.mana = 50.0
        self.max_mana = 50.0
```

### 2. HandleManager设计

#### 核心功能
```python
class HandleManager:
    """集中式handle管理器。

    负责所有handle的生命周期管理。
    """

    def __init__(self):
        self._handles: Dict[str, Handle] = {}  # id -> handle对象
        self._type_index: Dict[str, List[str]] = {}  # 类型索引
        self._next_id = 1

    def create_unit(self, unit_type: str, player_id: int,
                   x: float, y: float, facing: float) -> str:
        """创建一个单位并返回handle ID。"""
        handle_id = f"unit_{self._generate_id()}"
        unit = Unit(handle_id, unit_type, player_id, x, y, facing)
        self._register_handle(unit)
        return handle_id

    def get_handle(self, handle_id: str) -> Optional[Handle]:
        """通过ID获取handle对象。"""
        handle = self._handles.get(handle_id)
        if handle and handle.is_alive():
            return handle
        return None

    def get_unit(self, unit_id: str) -> Optional[Unit]:
        """获取单位对象，进行类型检查。"""
        handle = self.get_handle(unit_id)
        if isinstance(handle, Unit):
            return handle
        return None

    def destroy_handle(self, handle_id: str) -> bool:
        """销毁指定的handle。"""
        handle = self._handles.get(handle_id)
        if handle and handle.is_alive():
            handle.destroy()
            return True
        return False
```

### 3. StateContext设计（混合持久化方案）

```python
class StateContext:
    """状态上下文，管理全局和局部状态。

    采用混合方案：
    - 全局状态（handle引用）由HandleManager管理
    - 局部状态（临时变量）由ExecutionContext管理
    """

    def __init__(self):
        self.handle_manager = HandleManager()
        self.global_vars = {}  # 全局变量存储
        self.local_stores = {}  # 上下文局部存储

    def get_context_store(self, context_id: str) -> Dict:
        """获取指定上下文的局部存储。"""
        if context_id not in self.local_stores:
            self.local_stores[context_id] = {}
        return self.local_stores[context_id]
```

### 4. ExecutionContext集成

```python
class ExecutionContext:
    """执行上下文，扩展以支持状态管理。"""

    def __init__(self, parent=None, native_registry=None, state_context=None):
        # 现有属性
        self.parent = parent
        self.native_registry = native_registry
        self.variables = {}

        # 新增：状态上下文
        self.state_context = state_context or StateContext()
        self.context_id = str(uuid.uuid4())  # 唯一上下文ID

    def get_state_context(self) -> StateContext:
        """获取状态上下文。"""
        return self.state_context

    def get_handle_manager(self) -> HandleManager:
        """获取handle管理器。"""
        return self.state_context.handle_manager
```

### 5. NativeFunction接口改造

#### 新NativeFunction基类
```python
class NativeFunction(ABC):
    """JASS native函数的抽象基类（新版本）。

    所有native函数必须接收ExecutionContext作为第一个参数。
    """

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def execute(self, context: ExecutionContext, *args, **kwargs):
        """执行native函数。

        参数：
            context: 执行上下文，提供状态访问
            *args: 函数参数
            **kwargs: 关键字参数

        返回：
            native函数的执行结果
        """
        pass
```

#### Evaluator调用改造
```python
class Evaluator:
    """求值JASS表达式。"""

    def evaluate_native_call(self, node):
        """求值原生函数调用。"""
        func_name = node.func_name
        args = [self.evaluate(arg) for arg in node.args]

        native_func = self.context.get_native_function(func_name)
        if native_func is None:
            raise RuntimeError(f"Native function not found: {func_name}")

        # 关键：传递context作为第一个参数
        return native_func.execute(self.context, *args)
```

#### NativeFunction改造示例

**CreateUnit**：
```python
class CreateUnit(NativeFunction):
    @property
    def name(self) -> str:
        return "CreateUnit"

    def execute(self, context: ExecutionContext, player: int, unit_type: str,
               x: float, y: float, facing: float):
        handle_manager = context.get_handle_manager()
        unit_id = handle_manager.create_unit(unit_type, player, x, y, facing)
        logger.info(f"[CreateUnit] 为玩家{player}在({x}, {y})创建{unit_type}，单位ID: {unit_id}")
        return unit_id
```

**KillUnit**：
```python
class KillUnit(NativeFunction):
    @property
    def name(self) -> str:
        return "KillUnit"

    def execute(self, context: ExecutionContext, unit_identifier: str):
        if not unit_identifier:
            logger.warning("[KillUnit] 尝试击杀None单位")
            return False

        handle_manager = context.get_handle_manager()
        unit = handle_manager.get_unit(unit_identifier)
        if not unit:
            logger.warning(f"[KillUnit] 单位不存在: {unit_identifier}")
            return False

        unit.life = 0
        unit.destroy()
        logger.info(f"[KillUnit] 单位{unit_identifier}（{unit.unit_type}）已被击杀")
        return True
```

**GetUnitState**：
```python
class GetUnitState(NativeFunction):
    @property
    def name(self) -> str:
        return "GetUnitState"

    def execute(self, context: ExecutionContext, unit_identifier: str, state_type: str):
        handle_manager = context.get_handle_manager()
        unit = handle_manager.get_unit(unit_identifier)
        if not unit:
            logger.warning(f"[GetUnitState] 单位不存在: {unit_identifier}")
            return 0.0

        if state_type == "UNIT_STATE_LIFE":
            return unit.life
        elif state_type == "UNIT_STATE_MAX_LIFE":
            return unit.max_life
        elif state_type == "UNIT_STATE_MANA":
            return unit.mana
        elif state_type == "UNIT_STATE_MAX_MANA":
            return unit.max_mana
        else:
            logger.warning(f"[GetUnitState] 未知状态类型: {state_type}")
            return 0.0
```

### 6. 测试策略

#### 单元测试更新
```python
def test_create_unit():
    """测试CreateUnit原生函数。"""
    from jass_runner.natives.basic import CreateUnit

    native = CreateUnit()
    assert native.name == "CreateUnit"

    # 创建测试上下文
    context = create_test_context()

    # 测试执行
    result = native.execute(context, 0, 'hfoo', 0.0, 0.0, 0.0)
    assert isinstance(result, str)
    assert 'unit_' in result

    # 验证状态
    unit = context.get_handle_manager().get_unit(result)
    assert unit is not None
    assert unit.unit_type == 'hfoo'
    assert unit.player_id == 0
```

#### 集成测试
```python
def test_unit_lifecycle():
    """测试单位完整生命周期。"""
    context = create_test_context()
    handle_manager = context.get_handle_manager()

    # 创建单位
    unit_id = handle_manager.create_unit('hfoo', 0, 100.0, 200.0, 270.0)
    unit = handle_manager.get_unit(unit_id)
    assert unit is not None
    assert unit.life == 100.0
    assert unit.is_alive()

    # 查询状态
    assert handle_manager.get_unit_state(unit_id, "UNIT_STATE_LIFE") == 100.0

    # 杀死单位
    assert handle_manager.destroy_handle(unit_id)
    assert not unit.is_alive()
    assert unit.life == 0

    # 再次查询应返回None
    assert handle_manager.get_unit(unit_id) is None
```

## 实施路线图

### 阶段1：基础架构（2天）
1. 创建Handle类体系（`src/jass_runner/natives/handle.py`）
2. 实现HandleManager核心功能（`src/jass_runner/natives/manager.py`）
3. 创建StateContext类（`src/jass_runner/natives/state.py`）

### 阶段2：接口改造（1天）
1. 修改NativeFunction基类，添加context参数（`src/jass_runner/natives/base.py`）
2. 修改ExecutionContext，集成StateContext（`src/jass_runner/interpreter/context.py`）
3. 修改Evaluator，传递context（`src/jass_runner/interpreter/evaluator.py`）

### 阶段3：函数迁移（2-3天）
1. 逐个改造现有native函数（`src/jass_runner/natives/basic.py`）
2. 更新NativeFactory注册新函数（`src/jass_runner/natives/factory.py`）
3. 添加新的单元测试

### 阶段4：集成测试（1天）
1. 创建端到端测试脚本
2. 验证状态持久化功能
3. 测试handle生命周期管理
4. 性能基准测试

### 阶段5：文档和优化（1天）
1. 更新API文档
2. 优化内存使用
3. 添加性能监控

## 预期收益

1. **状态一致性**：单位创建、状态查询、销毁操作共享同一状态
2. **类型安全**：严格的handle类型体系，减少运行时错误
3. **可测试性**：状态可观察、可重置，便于自动化测试
4. **可扩展性**：新的handle类型和native函数易于添加
5. **模拟真实性**：更接近JASS实际运行时行为
6. **调试支持**：可以检查内存中的handle状态，便于问题诊断

## 风险与缓解

1. **性能影响**：集中式管理器可能成为瓶颈
   - 缓解：使用字典索引，O(1)复杂度操作
   - 缓解：懒加载，按需创建handle对象

2. **内存泄漏**：handle对象可能未被正确销毁
   - 缓解：实现显式销毁机制
   - 缓解：添加内存使用监控

3. **迁移复杂性**：需要修改所有现有native函数
   - 缓解：分阶段实施，逐个函数迁移
   - 缓解：保持测试覆盖，确保功能正确

4. **向后兼容**：现有测试需要更新
   - 缓解：项目处于开发阶段，无需向后兼容
   - 缓解：提供测试辅助函数，简化测试更新

## 成功标准

1. **功能正确**：所有现有测试通过
2. **状态持久化**：CreateUnit和GetUnitState共享状态
3. **生命周期管理**：KillUnit正确标记单位死亡
4. **类型安全**：get_unit()等方法进行类型检查
5. **性能可接受**：handle操作在微秒级完成
6. **测试覆盖**：新功能有充分的单元测试

## 后续扩展

1. **更多handle类型**：Timer、Location、Group等
2. **状态序列化**：支持保存/加载游戏状态
3. **并发支持**：多个ExecutionContext并行执行
4. **可视化调试**：图形界面查看handle状态
5. **性能分析**：handle操作性能监控

---
*设计批准日期：2026-02-26*
*设计状态：已批准*
*实施责任人：开发团队*