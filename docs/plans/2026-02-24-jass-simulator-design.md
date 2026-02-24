# JASS模拟运行工具设计文档

## 项目概述
创建一个用Python实现的JASS模拟运行工具，用于魔兽地图开发者测试和自动化测试。

## 需求总结
1. 在游戏外解释执行JASS脚本
2. 模拟JASS native函数行为，输出日志（如"XXX单位已被杀死"）
3. 用帧系统模拟计时器执行，支持快速模拟
4. 可扩展的native函数模拟框架
5. 简单帧循环和调试支持
6. 从文件读取JASS脚本

## 架构设计

### 目录结构
```
jass-runner/
├── src/
│   ├── parser/          # JASS语法解析
│   ├── interpreter/     # 解释执行引擎
│   ├── natives/         # Native函数模拟
│   ├── timer/          # 计时器系统
│   └── vm/             # 虚拟机核心
├── examples/           # 示例脚本
├── tests/             # 测试用例
└── docs/              # 文档
```

### 核心组件

#### 1. JASS解析器 (parser/)
- 基于Python的`ast`模块或自定义解析器
- 支持JASS语法：变量声明、函数定义、控制流、表达式
- 输出AST（抽象语法树）供解释器使用

#### 2. 解释器引擎 (interpreter/)
- 遍历AST并执行
- 变量作用域管理
- 函数调用栈
- 错误处理和调试信息

#### 3. Native函数框架 (natives/)
- 插件式架构，每个native函数独立模块
- 基础接口：`NativeFunction`基类
- 注册系统：动态加载native函数
- 日志输出：统一格式化输出

#### 4. 计时器系统 (timer/)
- 基于帧的事件循环
- 计时器队列：按到期时间排序
- 支持单次和周期计时器
- 调试模式：输出计时器生命周期日志

#### 5. 虚拟机核心 (vm/)
- 执行上下文管理
- 全局状态（模拟的游戏状态）
- 脚本加载和执行入口

## 详细设计

### Native函数接口
```python
class NativeFunction:
    def __init__(self, name, signature):
        self.name = name
        self.signature = signature  # 参数类型信息

    def execute(self, vm, args):
        """执行native函数，返回结果"""
        # 默认实现：输出日志
        vm.logger.info(f"{self.name} called with args: {args}")
        return None

# 示例：KillUnit实现
class KillUnit(NativeFunction):
    def execute(self, vm, args):
        unit = args[0]
        vm.logger.info(f"单位 {unit} 已被杀死")
        # 更新游戏状态（如果实现了状态跟踪）
        if hasattr(vm.state, 'units'):
            vm.state.units.remove(unit)
        return None
```

### 计时器系统
```python
class Timer:
    def __init__(self, callback, delay, periodic=False):
        self.callback = callback
        self.delay = delay  # 帧数
        self.periodic = periodic
        self.remaining = delay

class TimerSystem:
    def __init__(self):
        self.timers = []
        self.current_frame = 0

    def update(self):
        """更新所有计时器，执行到期的回调"""
        self.current_frame += 1
        for timer in self.timers[:]:
            timer.remaining -= 1
            if timer.remaining <= 0:
                timer.callback()
                if timer.periodic:
                    timer.remaining = timer.delay
                else:
                    self.timers.remove(timer)

    def fast_forward(self, frames):
        """快速模拟指定帧数"""
        for _ in range(frames):
            self.update()
```

### 虚拟机接口
```python
class JassVM:
    def __init__(self):
        self.parser = JassParser()
        self.interpreter = JassInterpreter()
        self.timer_system = TimerSystem()
        self.native_registry = NativeRegistry()
        self.state = GameState()  # 可选：游戏状态跟踪
        self.logger = logging.getLogger("jass-vm")

    def load_natives(self, native_dir):
        """加载native函数插件"""
        self.native_registry.load_from_directory(native_dir)

    def load_script(self, script_path):
        """加载JASS脚本文件"""
        with open(script_path, 'r', encoding='utf-8') as f:
            script_content = f.read()
        self.ast = self.parser.parse(script_content)

    def execute(self):
        """执行加载的脚本"""
        self.interpreter.execute(self.ast, self)

    def register_native(self, name, func_impl):
        """注册自定义native函数"""
        self.native_registry.register(name, func_impl)
```

## 使用示例

### 基本使用
```python
# 创建虚拟机实例
vm = JassVM()

# 加载native函数
vm.load_natives("natives/")

# 加载和执行JASS脚本
vm.load_script("map_script.j")
vm.execute()

# 快速模拟长时间行为
vm.timer_system.fast_forward(1000)  # 快速模拟1000帧
```

### 自定义Native函数
```python
# 创建自定义native函数
class MyCustomNative(NativeFunction):
    def execute(self, vm, args):
        vm.logger.info(f"自定义函数被调用，参数: {args}")
        return "自定义返回值"

# 注册到虚拟机
vm.register_native("MyCustomFunc", MyCustomNative())
```

### 测试集成
```python
# 在测试中使用
def test_map_logic():
    vm = JassVM()
    vm.load_script("test_map.j")
    vm.execute()

    # 验证游戏状态
    assert len(vm.state.units) == 0  # 所有单位应该被杀死
    assert vm.timer_system.current_frame > 0
```

## 扩展性设计

1. **Native函数插件系统**：用户可自定义native函数实现
2. **状态跟踪扩展**：可选实现单位、物品、玩家等游戏状态管理
3. **调试工具**：执行轨迹记录、断点调试、变量监视
4. **性能分析**：执行时间统计、函数调用频率分析
5. **测试框架集成**：与pytest、unittest等测试框架集成

## 技术栈
- **编程语言**：Python 3.8+
- **解析器**：自定义解析器或基于PLY/ANTLR
- **日志系统**：Python logging模块
- **测试框架**：pytest
- **打包工具**：setuptools, pip

## 下一步
1. 创建详细实现计划
2. 搭建项目脚手架
3. 实现核心解析器和解释器
4. 实现基础native函数
5. 实现计时器系统
6. 编写测试用例
7. 创建示例和文档

---
*设计日期：2026-02-24*
*设计者：Claude (DeepSeek-V3.2)*
*项目：JASS模拟运行工具*