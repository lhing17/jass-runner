# JASS Runner

一个用于魔兽争霸III地图测试和自动化的JASS脚本模拟运行工具.

## 功能特性

- 在魔兽争霸III游戏外执行JASS脚本
- 模拟JASS原生函数, 通过控制台输出日志(如"XXX单位已被杀死")
- 基于帧的计时器系统, 支持快速模拟长时间游戏行为
- 可扩展的插件架构, 支持自定义原生函数模拟
- 简单的帧循环和调试支持

## 项目状态

### 已完成
- ✅ 项目需求分析和架构设计
- ✅ 5个阶段详细实施计划文档
- ✅ Phase 1 Task 1: 项目基础结构搭建
- ✅ 项目文档(CLAUDE.md, PROJECT_NOTES.md)

### 进行中
- 🔄 Phase 1: 项目设置和核心基础设施(剩余Tasks 2-4)

## 技术架构

项目采用五层架构设计:

1. **解析器层** (`src/jass_runner/parser/`) - JASS语法解析, 生成AST
2. **解释器层** (`src/jass_runner/interpreter/`) - AST执行, 变量作用域管理
3. **Native函数框架** (`src/jass_runner/natives/`) - 插件式原生函数模拟
4. **计时器系统** (`src/jass_runner/timer/`) - 帧基计时器模拟
5. **虚拟机核心** (`src/jass_runner/vm/`) - 组件集成和命令行接口

## 安装

```bash
# 安装开发版本
pip install -e .

# 安装开发依赖
pip install -e ".[dev]"
```

## 使用方法

### 通过Python API使用

```python
from jass_runner import JassVM

# 创建虚拟机实例
vm = JassVM()

# 加载JASS脚本
vm.load_script("map_script.j")

# 执行脚本
vm.execute()

# 运行计时器模拟(可选)
vm.run_simulation(10.0)  # 模拟10秒游戏时间
```

### 通过命令行使用

```bash
# 执行JASS脚本
jass-runner script.j

# 执行并模拟计时器(10秒)
jass-runner script.j --simulate 10

# 禁用计时器系统
jass-runner script.j --no-timers

# 显示详细输出
jass-runner script.j --verbose
```

## 开发指南

### 环境设置

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 运行特定测试
pytest tests/path/to/test_file.py
pytest tests/path/to/test_file.py::test_function_name -v

# 代码检查
flake8 src tests
```

### 项目结构

```
jass-runner/
├── pyproject.toml          # 项目配置
├── README.md              # 英文说明文档
├── README_zh.md           # 中文说明文档(本文档)
├── CLAUDE.md              # Claude Code工作指导
├── PROJECT_NOTES.md       # 项目进展笔记
├── src/jass_runner/       # 源代码
│   ├── __init__.py        # 包入口
│   ├── parser/           # 解析器(待实现)
│   ├── interpreter/      # 解释器(待实现)
│   ├── natives/          # Native函数(待实现)
│   ├── timer/           # 计时器系统(待实现)
│   └── vm/              # 虚拟机核心(待实现)
├── tests/                # 测试代码
│   └── __init__.py       # 测试包
├── examples/             # 示例脚本
│   └── hello_world.j     # 简单示例
└── docs/plans/          # 实施计划文档
    ├── 2026-02-24-jass-simulator-design.md
    ├── 2026-02-24-jass-simulator-phase1-setup.md
    ├── 2026-02-24-jass-simulator-phase2-interpreter.md
    ├── 2026-02-24-jass-simulator-phase3-natives.md
    ├── 2026-02-24-jass-simulator-phase4-timer.md
    └── 2026-02-24-jass-simulator-phase5-vm.md
```

### 实施计划

项目按5个阶段实施, 详细计划见 `docs/plans/` 目录:

1. **Phase 1**: 项目设置和核心基础设施(当前阶段)
2. **Phase 2**: 解释器和执行引擎
3. **Phase 3**: Native函数框架
4. **Phase 4**: 计时器系统
5. **Phase 5**: 虚拟机核心

## 示例

### 简单示例 (examples/hello_world.j)

```jass
// examples/hello_world.j
// 简单的JASS测试脚本

function main takes nothing returns nothing
    call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "Hello, World!")
endfunction
```

### 运行示例

```bash
# 通过CLI运行示例
jass-runner examples/hello_world.j

# 或通过Python脚本
python examples/run_complete_example.py
```

## 扩展开发

### 添加新的Native函数

1. 创建类继承 `NativeFunction` 基类
2. 实现 `name` 属性和 `execute` 方法
3. 在 `NativeFactory.create_default_registry()` 中注册

示例:
```python
from jass_runner.natives.base import NativeFunction

class MyNative(NativeFunction):
    @property
    def name(self) -> str:
        return "MyNative"

    def execute(self, *args):
        print(f"MyNative called with {args}")
        return None
```

## 许可证

MIT

## 相关文档

- [项目设计文档](docs/plans/2026-02-24-jass-simulator-design.md)
- [实施计划](docs/plans/)
- [项目笔记](PROJECT_NOTES.md)
- [Claude工作指导](CLAUDE.md)