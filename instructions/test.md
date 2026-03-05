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