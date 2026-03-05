# CLAUDE.md

此文件为Claude Code (claude.ai/code) 在此代码库中工作时提供指导。

## 项目概述

JASS Runner 是一个用Python实现的JASS脚本模拟运行工具，用于魔兽争霸III地图开发者测试和自动化测试。项目目标是：
1. 在游戏外解释执行JASS脚本
2. 模拟JASS native函数行为，输出日志（如"XXX单位已被杀死"）
3. 用帧系统模拟计时器执行，支持快速模拟长时间游戏行为
4. 可扩展的native函数模拟框架
5. 模拟触发器系统，支持事件注册和触发

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

## 硬性指标（Must-Follow）

### 文件行数限制
- 每个python代码文件不超过 500 行
- 每个函数不超过 200 行

### 注释要求
- 项目源代码**必须**统一使用中文注释

## 开发命令

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

## 开发测试规范

###  测试文件结构

项目采用模块化测试结构，测试目录与源码结构对应：

```
tests/
├── parser/                 # 解析器相关测试
│   ├── test_lexer.py      # 词法分析器测试
│   └── test_parser.py     # 语法分析器测试
├── interpreter/           # 解释器相关测试
│   ├── test_context.py    # 执行上下文测试
│   ├── test_evaluator.py  # 表达式求值器测试
│   └── test_interpreter.py # 解释器核心测试
├── integration/           # 集成测试
│   ├── test_basic_parsing.py      # 基础解析集成测试
│   └── test_parser_interpreter.py # 解析器-解释器集成测试
└── fixtures/              # 测试数据（待创建）
```

**目录命名约定**：
- 测试目录与`src/jass_runner/`下的源码目录对应
- 每个测试文件前缀为`test_`
- 集成测试放在`integration/`目录中

### 3. 测试编写规范

#### 3.1 测试类命名
- 格式：`Test{被测试类名}`
- 示例：`TestEvaluator`, `TestParser`

#### 3.2 测试方法命名
- 格式：`test_{测试场景}_{预期结果}`
- 示例：`test_string_literal_returns_string`, `test_integer_literal_returns_int`

#### 3.3 测试用例组织
```python
class TestEvaluator:
    """测试Evaluator类的功能。"""

    def test_string_literal_returns_string(self):
        """测试字符串字面量求值返回字符串。"""
        # 准备
        context = ExecutionContext()
        evaluator = Evaluator(context)

        # 执行
        result = evaluator.evaluate('"hello"')

        # 验证
        assert result == "hello"
        assert isinstance(result, str)

    def test_integer_literal_returns_int(self):
        """测试整数字面量求值返回整数。"""
        # 准备-执行-验证模式
        ...
```

### 4. 测试质量要求

1. **独立性**：测试之间不依赖执行顺序
2. **可重复性**：同一测试每次结果一致
3. **快速执行**：单元测试应在毫秒级完成
4. **明确失败**：失败信息应清晰指出问题
5. **覆盖关键路径**：优先测试核心功能

### 5. 测试覆盖率

1. **目标**：核心模块达到90%以上覆盖率
2. **测量**：使用pytest-cov生成报告
3. **命令**：
   ```bash
   # 运行测试并生成覆盖率报告
   pytest --cov=src/jass_runner --cov-report=term-missing

   # 生成HTML报告
   pytest --cov=src/jass_runner --cov-report=html
   ```

### 6. 集成测试规范

1. **端到端测试**：测试完整流程
2. **真实数据**：使用实际JASS脚本
3. **预期输出**：验证控制台输出或文件结果
4. **示例**：
   ```python
   def test_complete_jass_script_execution():
       """测试完整JASS脚本执行流程。"""
       # 加载示例脚本
       with open('examples/hello_world.j') as f:
           code = f.read()

       # 执行完整流程
       vm = JassVM()
       result = vm.execute(code)

       # 验证执行结果
       assert result.success
       assert "Hello World" in result.output
   ```

## 其他资源
- 项目笔记: PROJECT_NOTES.md