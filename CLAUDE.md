# CLAUDE.md

此文件为Claude Code (claude.ai/code) 在此代码库中工作时提供指导。

## 项目概述

JASS Runner 是一个用Python实现的JASS脚本模拟运行工具，用于魔兽争霸III地图开发者测试和自动化测试。项目目标是：
1. 在游戏外解释执行JASS脚本
2. 模拟JASS native函数行为，输出日志（如"XXX单位已被杀死"）
3. 用帧系统模拟计时器执行，支持快速模拟长时间游戏行为
4. 可扩展的native函数模拟框架

## 架构设计

项目采用五层架构，按阶段实现：

### 1. 解析器层 (`src/jass_runner/parser/`)
- 基于自定义词法分析器和语法分析器
- 将JASS脚本解析为AST（抽象语法树）
- 支持JASS语法：变量声明、函数定义、控制流、表达式

### 2. 解释器层 (`src/jass_runner/interpreter/`)
- 遍历AST并执行
- 变量作用域管理（执行上下文）
- 表达式求值器
- 函数调用栈管理

### 3. Native函数框架 (`src/jass_runner/natives/`)
- 插件式架构，每个native函数独立实现
- `NativeFunction`抽象基类定义接口
- `NativeRegistry`注册系统管理native函数
- `NativeFactory`工厂创建预配置的注册表

### 4. 计时器系统 (`src/jass_runner/timer/`)
- 基于帧的事件循环（非实时）
- `Timer`类管理单个计时器
- `TimerSystem`管理系统中的多个计时器
- `SimulationLoop`帧循环用于快速模拟

### 5. 虚拟机核心 (`src/jass_runner/vm/`)
- `JassVM`类集成所有组件
- 脚本加载和执行入口点
- 命令行接口 (`src/jass_runner/cli.py`)

## 开发命令

### 安装和设置
```bash
# 安装开发依赖
pip install -e ".[dev]"

# 验证项目配置
python -c "import tomllib; tomllib.load(open('pyproject.toml', 'rb'))"
```

### 测试
```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/path/to/test_file.py

# 运行单个测试
pytest tests/path/to/test_file.py::test_function_name -v

# 运行集成测试
pytest tests/integration/
```

### 代码质量
```bash
# 运行代码检查
flake8 src tests

# 格式化代码（如果安装了black）
black src tests
```

### 运行示例
```bash
# 通过CLI运行JASS脚本
python -m jass_runner examples/hello_world.j

# 运行示例脚本
python examples/run_complete_example.py
```

## 实现计划

项目按5个阶段实现，详细计划在 `docs/plans/` 目录中：

1. **Phase 1**: 项目设置和核心基础设施 (`2026-02-24-jass-simulator-phase1-setup.md`)
2. **Phase 2**: 解释器和执行引擎 (`2026-02-24-jass-simulator-phase2-interpreter.md`)
3. **Phase 3**: Native函数框架 (`2026-02-24-jass-simulator-phase3-natives.md`)
4. **Phase 4**: 计时器系统 (`2026-02-24-jass-simulator-phase4-timer.md`)
5. **Phase 5**: 虚拟机核心 (`2026-02-24-jass-simulator-phase5-vm.md`)

## 关键设计模式

### Native函数扩展
要添加新的native函数：
1. 创建类继承 `NativeFunction`
2. 实现 `name` 属性和 `execute` 方法
3. 在 `NativeFactory.create_default_registry()` 中注册

### 计时器模拟
- 使用帧而非实时：默认30FPS（0.033秒/帧）
- 支持单次和周期性计时器
- 可暂停和恢复
- 支持快速模拟长时间行为

### 执行上下文
- `ExecutionContext` 管理变量作用域
- 支持父上下文（函数调用栈）
- 集成native函数注册表和计时器系统

## 文件命名约定

- 测试文件：`test_*.py` 在 `tests/` 目录中
- JASS脚本：`*.j` 扩展名
- 示例脚本：放在 `examples/` 目录中
- 文档：Markdown格式，放在 `docs/` 目录中

## 注意事项

1. **TDD方法**：所有实现遵循测试驱动开发，先写失败测试
2. **小步提交**：每个任务完成后立即提交
3. **Python版本**：要求Python 3.8+
4. **日志输出**：native函数使用logging模块输出模拟结果
5. **错误处理**：所有公开API应有适当的错误处理和验证

## 其他资源
- 项目笔记: PROJECT_NOTES.md