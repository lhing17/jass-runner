# JASS Runner 项目笔记

## 项目概述
JASS Runner 是一个用Python实现的JASS脚本模拟运行工具，用于魔兽争霸III地图开发者测试和自动化测试。

### 核心需求
1. 在游戏外解释执行JASS脚本
2. 模拟JASS native函数行为，输出日志（如"XXX单位已被杀死"）
3. 用帧系统模拟计时器执行，支持快速模拟长时间游戏行为
4. 可扩展的native函数模拟框架
5. 简单帧循环和调试支持
6. 从文件读取JASS脚本

## 项目进展

### 已完成的工作

#### 1. 需求分析和设计阶段 (2026-02-24)
- 使用superpowers:brainstorming技能进行需求分析
- 确定技术方案：Python实现，轻量级解释器+插件系统
- 创建详细设计文档：`docs/plans/2026-02-24-jass-simulator-design.md`
  - 架构设计（5个核心组件）
  - 目录结构
  - 详细类设计
  - 使用示例和扩展性设计

#### 2. 实施计划阶段 (2026-02-24)
- 创建5个阶段的详细实施计划：
  1. **Phase 1**: 项目设置和核心基础设施 (`docs/plans/2026-02-24-jass-simulator-phase1-setup.md`)
  2. **Phase 2**: 解释器和执行引擎 (`docs/plans/2026-02-24-jass-simulator-phase2-interpreter.md`)
  3. **Phase 3**: Native函数框架 (`docs/plans/2026-02-24-jass-simulator-phase3-natives.md`)
  4. **Phase 4**: 计时器系统 (`docs/plans/2026-02-24-jass-simulator-phase4-timer.md`)
  5. **Phase 5**: 虚拟机核心 (`docs/plans/2026-02-24-jass-simulator-phase5-vm.md`)

#### 3. 第一阶段实施 - 任务1完成 (2026-02-24)
- 使用superpowers:executing-plans技能开始实施
- 完成Phase 1 Task 1: 创建项目结构
  - 创建 `pyproject.toml` - 项目配置和依赖管理
  - 创建 `README.md` - 项目文档
  - 创建 `src/jass_runner/__init__.py` - 包结构
  - 创建 `tests/__init__.py` - 测试包
  - 创建 `examples/hello_world.j` - 示例JASS脚本
- 提交更改：`git commit -m "feat: initial project setup"`

#### 4. 项目文档完善 (2026-02-24)
- 创建 `CLAUDE.md` - Claude Code工作指导文档（中文）
  - 项目概述和架构设计
  - 开发命令和测试流程
  - 关键设计模式和扩展指南

#### 5. 双语README文档同步 (2026-02-24)
- 创建 `README_zh.md` - 中文版项目文档
  - 完整的中文项目说明
  - 项目状态、技术架构、使用指南
  - 开发指导和扩展说明
- 更新 `README.md` - 英文版项目文档
  - 扩展内容以匹配中文版本
  - 添加项目状态、技术架构等详细信息
  - 确保中英文文档内容一致

#### 6. 第一阶段实施 - 任务2完成 (2026-02-25)
- 完成Phase 1 Task 2: 设置测试基础设施
  - 创建 `tests/conftest.py` - pytest配置文件，设置Python路径
  - 创建 `tests/test_project_structure.py` - 项目结构测试文件
  - 安装开发依赖：`pip install -e ".[dev]"`
  - 运行测试验证：`pytest tests/test_project_structure.py::test_package_can_be_imported -v`
  - 测试通过，验证了包可以正确导入和版本号正确

#### 7. 第一阶段实施 - 任务3完成 (2026-02-25)
- 完成Phase 1 Task 3: 创建基本词法分析器
  - 创建 `src/jass_runner/parser/__init__.py` - 解析器模块初始化
  - 创建 `src/jass_runner/parser/lexer.py` - JASS词法分析器
  - 创建 `tests/parser/test_lexer.py` - 词法分析器测试
  - 实现Token类表示JASS代码标记
  - 实现Lexer类，支持JASS关键词识别
  - 支持行号和列号跟踪，便于错误定位
  - 遵循TDD方法：先写失败测试，再实现功能
  - 测试验证：`pytest tests/parser/test_lexer.py -v` 全部通过

#### 9. 词法分析器完善 (2026-02-25)
- 完善Phase 1 Task 3: 扩展词法分析器功能
  - 根据用户提供的关键词列表完善JASS关键词识别
    - 新增10个关键词：`true`, `false`, `null`, `elseif`, `return`, `and`, `or`, `not`, `globals`, `endglobals`
    - 完整支持35个JASS关键词，覆盖用户提供的完整列表
  - 添加对 `/* ... */` 格式的多行注释支持
    - 更新token模式，添加 `MULTILINE_COMMENT` 正则表达式模式
    - 修改注释跳过逻辑，正确处理多行注释
  - 扩展测试覆盖，验证新功能：
    - 新增 `test_lexer_new_keywords()` 测试新关键词识别
    - 新增 `test_lexer_multiline_comment()` 测试多行注释处理
    - 新增 `test_lexer_all_keywords()` 验证所有35个关键词
  - 测试验证：`pytest tests/parser/test_lexer.py -v` 所有5个测试通过

#### 10. 第一阶段实施 - 任务4完成 (2026-02-25)
- 完成Phase 1 Task 4: 创建基本语法分析器
  - 创建 `src/jass_runner/parser/parser.py` - JASS语法分析器
    - 实现AST节点定义：`Parameter`, `FunctionDecl`, `AST` dataclass
    - 实现递归下降解析器 `Parser` 类
    - 支持JASS函数声明语法：`function <name> takes <parameters> returns <type>`
    - 支持参数列表解析：`takes nothing` 和 `takes integer x, real y`
    - 实现错误恢复机制：`skip_to_next_function()` 方法
    - 集成现有词法分析器，过滤注释和空白令牌
  - 创建 `tests/parser/test_parser.py` - 语法分析器测试
    - 10个测试用例覆盖核心功能
    - 基础功能测试：函数声明解析、参数列表解析、多函数解析
    - 错误处理测试：无效语法跳过、缺失关键词处理、格式错误处理
    - 边界条件测试：空代码、仅注释代码、单参数函数
    - 位置信息测试：验证行号和列号正确传递
  - 遵循TDD方法：先写失败测试，再实现功能
  - 代码质量检查：通过flake8检查，符合PEP8规范
  - 测试验证：`pytest tests/parser/test_parser.py -v` 所有10个测试通过
  - 集成测试：`pytest tests/ -v` 所有16个测试通过，无回归

#### 11. 第一阶段实施 - 任务5完成 (2026-02-25)
- 完成Phase 1 Task 5: 错误处理和报告机制
  - 增强解析器错误报告功能：
    - 定义错误类层次结构：`ParseError`, `MissingKeywordError`, `UnexpectedTokenError`, `ParameterError`
    - 实现错误收集机制：Parser类维护`errors`列表收集所有解析错误
    - 添加详细错误信息：包括错误类型、位置（行、列）、预期内容、实际内容
  - 改进错误恢复和继续解析能力：
    - 保持现有的`skip_to_next_function()`错误恢复机制
    - 在解析失败时收集错误并继续解析，不中断整个解析过程
    - 检测常见语法错误：缺少关键字、意外令牌、参数列表错误（如缺少逗号）
  - 创建增强的错误处理测试：
    - 4个新测试用例验证错误报告功能
    - 测试错误收集而不是静默失败
    - 测试解析器在错误后继续解析
    - 测试详细的错误消息和位置信息
    - 测试多错误收集能力
  - 保持向后兼容性：
    - 现有测试全部通过，无回归
    - 解析器API保持不变，新增`errors`属性供检查错误
  - 测试验证：`pytest tests/parser/test_parser.py -v` 所有14个测试通过（原有10个 + 新增4个）
  - 集成测试：`pytest tests/ -v` 所有20个测试通过，项目测试覆盖率增加

#### 12. 第一阶段实施 - 任务7完成 (2026-02-25)
- 完成Phase 1 Task 7: 创建集成测试
  - 创建 `tests/integration/test_basic_parsing.py` - 集成测试文件
  - 实现端到端测试：从文件读取到AST生成的完整流程
  - 测试示例脚本 `examples/hello_world.j` 的解析
  - 验证解析器正确识别main函数、参数列表和返回类型
  - 测试验证：`pytest tests/integration/test_basic_parsing.py::test_parse_example_script -v` 通过

#### 13. 第一阶段实施 - 任务8完成 (2026-02-25)
- 完成Phase 1 Task 8: 创建Phase 1总结
  - 创建 `docs/phase1_summary.md` - Phase 1完整总结文档
  - 详细记录所有已完成任务和技术成果
  - 列出创建的关键文件和测试覆盖情况
  - 包含测试覆盖率报告：88%总体覆盖率
  - 规划Phase 2下一步工作：解释器和执行引擎
  - 运行覆盖率检查：`pytest --cov=src/jass_runner --cov-report=term-missing` 显示详细覆盖率

#### 14. 第二阶段实施 - 任务1完成 (2026-02-25)
- 完成Phase 2 Task 1: 创建解释器结构
  - 创建解释器包结构：`src/jass_runner/interpreter/`
  - 创建 `src/jass_runner/interpreter/__init__.py` - 解释器模块初始化
  - 创建 `src/jass_runner/interpreter/context.py` - 执行上下文实现
    - `ExecutionContext` 类管理变量作用域
    - 支持父上下文（嵌套作用域）
    - 变量设置、获取和存在性检查方法
    - 变量查找遍历父上下文链
  - 创建 `tests/interpreter/test_context.py` - 执行上下文测试
    - 测试执行上下文创建和基本属性
    - 遵循TDD方法：先写失败测试，再实现功能
  - 测试验证：`pytest tests/interpreter/test_context.py::test_execution_context_creation -v` 通过
  - 所有现有测试通过：22个测试全部通过，无回归

#### 8. 代码库维护和推送 (2026-02-25)
- 添加 `.gitignore` 文件，管理版本控制忽略规则
  - 忽略Python开发缓存文件（__pycache__, *.pyc等）
  - 忽略构建产物（.egg-info/, dist/等）
  - 忽略本地开发文件（.claude/settings.local.json等）
- 提交所有当前修改并推送到远程仓库
  - 提交消息：`chore: add gitignore and update local settings`
  - 成功推送到GitHub远程仓库
- 清理开发环境，准备下一阶段任务

#### 15. 第三阶段实施 - 任务1完成 (2026-02-25)
- 完成Phase 3 Task 1: 创建Native Function基础类
  - 使用superpowers:executing-plans技能开始Phase 3实施
  - 创建natives包结构：`src/jass_runner/natives/`
  - 创建 `src/jass_runner/natives/__init__.py` - natives模块初始化
  - 创建 `src/jass_runner/natives/base.py` - NativeFunction抽象基类
    - 实现抽象类`NativeFunction`，继承自`ABC`
    - 定义抽象属性`name`和抽象方法`execute`
    - 支持所有native函数的统一接口
  - 创建 `tests/natives/test_base.py` - 基础类测试
    - 测试抽象类无法实例化
    - 验证抽象方法和属性存在
    - 遵循TDD方法：先写失败测试，再实现功能
  - 测试验证：`pytest tests/natives/test_base.py::test_native_function_base_class -v` 通过
  - 提交更改：`git commit -m "feat: add NativeFunction base class"`

#### 16. 第三阶段实施 - 任务2完成 (2026-02-25)
- 完成Phase 3 Task 2: 创建Native Registry系统
  - 创建 `src/jass_runner/natives/registry.py` - NativeRegistry注册系统
    - 实现`NativeRegistry`类管理native函数
    - 提供`register()`方法注册native函数
    - 提供`get()`方法按名称获取native函数
    - 提供`get_all()`方法获取所有注册函数
    - 使用字典存储函数，以name为键
  - 更新 `src/jass_runner/natives/__init__.py` - 导出registry
    - 添加`NativeRegistry`到`__all__`导出列表
  - 创建 `tests/natives/test_registry.py` - registry测试
    - 测试registry创建和基本方法
    - 遵循TDD方法：先写失败测试，再实现功能
  - 测试验证：`pytest tests/natives/test_registry.py::test_native_registry_creation -v` 通过
  - 提交更改：`git commit -m "feat: add native function registry"`

#### 17. 第三阶段实施 - 任务3完成 (2026-02-25)
- 完成Phase 3 Task 3: 实现第一个Native Function (DisplayTextToPlayer)
  - 创建 `src/jass_runner/natives/basic.py` - 基础native函数实现
    - 实现`DisplayTextToPlayer`类，继承自`NativeFunction`
    - `name`属性返回"DisplayTextToPlayer"
    - `execute()`方法模拟显示文本到玩家，使用logging输出信息
    - 参数：`player`（玩家ID）、`x`、`y`（坐标）、`message`（消息文本）
  - 创建 `tests/natives/test_basic.py` - 基础native函数测试
    - 测试`DisplayTextToPlayer`创建和执行
    - 验证`name`属性和返回类型
  - 更新 `tests/natives/test_registry.py` - 添加registry集成测试
    - 测试`DisplayTextToPlayer`在registry中的注册和获取
    - 验证native函数实例可以被正确检索
  - 测试验证：两个测试全部通过
    - `pytest tests/natives/test_basic.py::test_display_text_to_player -v` 通过
    - `pytest tests/natives/test_registry.py::test_register_and_get_native_function -v` 通过
  - 提交更改：`git commit -m "feat: implement DisplayTextToPlayer native function"`

#### 18. 第三阶段实施 - 任务7完成 (2026-02-26)
- 完成Phase 3 Task 7: 添加Native Function Call支持到Interpreter
  - 在Evaluator类中添加`evaluate_native_call`方法 (`src/jass_runner/interpreter/evaluator.py:13-77`)
  - 修改`evaluate`方法以支持AST节点处理，保持对字符串表达式的向后兼容
  - 在解析器中添加`NativeCallNode`类定义 (`src/jass_runner/parser/parser.py:86-90`)
  - 支持`call`语句解析：添加`parse_call_statement`方法和更新`parse_statement`方法
  - 测试验证：`pytest tests/interpreter/test_evaluator.py::test_evaluator_can_evaluate_native_call -v`通过

#### 19. 第三阶段实施 - 任务8完成 (2026-02-26)
- 完成Phase 3 Task 8: 创建集成测试
  - 创建`tests/integration/test_native_integration.py` - 原生函数集成测试
  - 测试完整流程：JASS代码解析 → 原生函数注册 → 解释执行 → 日志输出验证
  - 修复Interpreter以支持native_registry参数 (`src/jass_runner/interpreter/interpreter.py:12-16`)
  - 更新测试以使用中文日志断言（匹配native函数实现）
  - 测试验证：`pytest tests/integration/test_native_integration.py::test_native_function_integration -v`通过

#### 20. 第三阶段实施 - 任务9完成 (2026-02-26)
- 完成Phase 3 Task 9: 添加更多基础原生函数
  - 实现`CreateUnit`原生函数：生成唯一单位ID并记录创建日志 (`src/jass_runner/natives/basic.py:115-135`)
  - 实现`GetUnitState`原生函数：模拟单位状态（生命值、魔法值）查询 (`src/jass_runner/natives/basic.py:137-173`)
  - 更新`NativeFactory`包含新函数 (`src/jass_runner/natives/factory.py:25-27`)
  - 添加相应测试 (`tests/natives/test_basic.py:35-60`)
  - 更新factory测试以验证4个原生函数 (`tests/natives/test_factory.py:12-34`)
  - 测试验证：所有新增测试通过

#### 21. 第三阶段实施 - 任务10完成 (2026-02-26)
- 完成Phase 3 Task 10: 完成第3阶段文档
  - 创建原生函数框架文档`docs/natives/README.md`
    - 详细说明架构、使用方法、扩展指南
    - 列出所有已实现的native函数及其参数说明
    - 提供集成示例和设计原则
  - 更新主`README.md`反映项目进度和文档链接
    - 更新项目状态：Phase 1-3完成，Phase 4-5待实现
    - 更新代码库结构说明，添加native函数层描述
    - 添加指向native函数文档的链接

#### 22. 状态管理系统设计完成 (2026-02-26)
- 完成状态管理系统架构设计文档
  - 创建 `docs/plans/2026-02-26-jass-simulator-state-management-design.md`
    - 详细分析当前代码耦合问题（ExecutionContext职责过重）
    - 设计五层架构：Store、Reducer、Middleware、Selector、Integration
    - 参考Redux模式，采用不可变状态更新
    - 设计State、Action、Reducer、Store核心类
  - 创建Phase 1-5实施计划文档

#### 23. Handle系统核心实现 (2026-02-26)
- 创建Handle基础架构 (`src/jass_runner/handles/`)
  - 实现`Handle`基类：所有游戏对象的抽象基类
    - 支持唯一ID分配和管理
    - 提供基础属性和方法
  - 实现`Unit`类：游戏单位对象
    - 单位类型（FourCC格式）
    - 生命值、魔法值状态管理
    - 单位坐标位置
  - 实现`Player`类：玩家对象
    - 自动初始化16个玩家（0-15）
    - 支持玩家名称和状态

#### 24. 状态上下文和句柄管理器 (2026-02-26)
- 实现`StateContext`类 (`src/jass_runner/state_context.py`)
  - 管理HandleManager实例
  - 提供统一的状态访问接口
  - 支持扩展其他状态管理器
- 实现`HandleManager`类 (`src/jass_runner/handle_manager.py`)
  - 句柄创建和分配
  - 句柄查询和检索（通过ID或类型）
  - 句柄销毁和清理
  - 单位状态修改（设置/增减生命值、魔法值）
  - 单位状态查询（获取生命值、魔法值、类型、所有者）
  - 统计方法：获取总句柄数、活跃句柄列表

#### 25. FourCC工具函数实现 (2026-02-26)
- 创建`src/jass_runner/utils/fourcc.py` - FourCC转换工具
  - `string_to_fourcc()`：将4字符字符串转换为整数（小端序）
  - `fourcc_to_string()`：将整数转换回4字符字符串
  - `int_to_fourcc()`：别名函数，与fourcc_to_string相同
  - 支持JASS单位类型ID格式（如'Hpal'→1214542384）
  - 完整测试覆盖 (`tests/utils/test_fourcc.py`)

#### 26. 词法分析器增强 - FourCC字面量支持 (2026-02-26)
- 扩展`Lexer`类支持FourCC格式字面量
  - 识别单引号包围的4字符字面量（如`'Hpal'`）
  - 自动转换为对应的整数值
  - 添加`FOURCC` token类型
  - 更新测试验证FourCC解析功能

#### 27. 解析器增强 - 函数调用作为变量初始值 (2026-02-26)
- 扩展`parse_variable_decl`方法支持函数调用初始化
  - 变量声明时可以使用函数调用作为初始值
  - 示例：`local unit u = CreateUnit(...)`
  - 保持向后兼容性
  - 更新测试覆盖新功能

#### 28. 解释器增强 - Set语句和函数调用赋值 (2026-02-26)
- 实现`set`语句执行支持
  - 支持`set x = expression`语法
  - 变量赋值和更新
- 实现函数调用返回值赋值
  - 支持将函数调用结果赋值给变量
  - 示例：`set u = CreateUnit(...)`
  - 正确处理返回值类型
- 更新测试验证新功能

#### 29. 原生函数状态上下文支持 (2026-02-26)
- 为原生函数添加`state_context`参数支持
  - 修改`NativeFunction.execute`签名支持状态访问
  - 更新`DisplayTextToPlayer`、`KillUnit`等函数
  - 支持部分函数返回`Unit`类型替代`None`
  - 更新工厂类和注册表集成
  - 添加Phase 1集成测试验证完整流程

### 当前状态
- ✅ 需求分析和设计完成
- ✅ 5个阶段实施计划完成
- ✅ Phase 1 Task 1完成（项目基础结构）
- ✅ Phase 1 Task 2完成（测试基础设施）
- ✅ Phase 1 Task 3完成（基本词法分析器已完善）
- ✅ Phase 1 Task 4完成（基本语法分析器）
- ✅ Phase 1 Task 5完成（错误处理和报告机制）
- ✅ Phase 1 Task 6完成（集成测试）
- ✅ Phase 1 Task 7完成（Phase 1总结）
- ✅ **Phase 1 所有任务完成**
- ✅ Phase 2 Task 1完成（创建解释器结构）
- ✅ Phase 2 Task 2完成（添加变量操作测试）
- ✅ Phase 2 Task 3完成（创建表达式求值器）
- ✅ Phase 2 Task 4完成（创建解释器核心）
- ✅ Phase 2 Task 5完成（增强解析器以处理语句）
- ✅ Phase 2 Task 6完成（实现语句执行）
- ✅ Phase 2 Task 7完成（创建解析器和解释器的集成测试）
- ✅ Phase 2 Task 8完成（创建Phase 2总结）
- ✅ **Phase 2 所有任务完成**
- ✅ Phase 3 Task 1完成（创建NativeFunction基础类）
- ✅ Phase 3 Task 2完成（创建NativeRegistry系统）
- ✅ Phase 3 Task 3完成（实现DisplayTextToPlayer native函数）
- ✅ Phase 3 Task 4完成（实现KillUnit native函数）
- ✅ Phase 3 Task 5完成（创建NativeFunction Factory）
- ✅ Phase 3 Task 6完成（集成Natives与Interpreter）
- ✅ Phase 3 Task 7完成（添加Native Function Call支持到Interpreter）
- ✅ Phase 3 Task 8完成（创建集成测试）
- ✅ Phase 3 Task 9完成（添加更多基础原生函数）
- ✅ Phase 3 Task 10完成（完成第3阶段文档）
- ✅ **Phase 3 所有任务完成**
- ✅ 状态管理系统架构设计完成
  - 五阶段实施计划已创建（Phase 1-5）
  - 核心架构：Store、Reducer、Middleware、Selector、DevTools
  - 解决ExecutionContext职责过重问题
- ✅ Handle系统核心实现
  - Handle基类、Unit类、Player类（16个玩家初始化）
  - HandleManager句柄管理器
  - StateContext状态上下文
  - 单位状态查询和修改功能
- ✅ FourCC工具函数实现
  - 字符串与整数互转
  - 词法分析器支持FourCC字面量
- ✅ 解析器增强
  - 支持函数调用作为变量初始值
- ✅ 解释器增强
  - 支持set语句
  - 支持函数调用返回值赋值
- ✅ 原生函数状态上下文支持
  - 集成StateContext访问
  - Phase 1集成测试通过

### 代码库结构 (更新)
```
jass-runner/
├── pyproject.toml          # 项目配置
├── README.md              # 项目说明
├── CLAUDE.md              # Claude工作指导
├── src/jass_runner/
│   ├── __init__.py        # 包入口
│   ├── parser/           # 解析器层
│   │   ├── __init__.py
│   │   ├── lexer.py      # 词法分析器
│   │   └── parser.py     # 语法分析器
│   ├── interpreter/      # 解释器层
│   │   ├── __init__.py
│   │   ├── context.py    # 执行上下文
│   │   ├── evaluator.py  # 表达式求值器
│   │   └── interpreter.py # 解释器核心
│   ├── natives/          # Native函数框架 (Phase 3)
│   │   ├── __init__.py   # 模块初始化
│   │   ├── base.py       # NativeFunction抽象基类
│   │   ├── registry.py   # NativeRegistry注册系统
│   │   ├── factory.py    # Native函数工厂
│   │   ├── basic.py      # 基础native函数实现
│   │   ├── handle.py     # Handle类定义（Player、Unit、Item）
│   │   ├── manager.py    # HandleManager句柄管理器
│   │   ├── state.py      # StateContext状态上下文
│   │   ├── timer_natives.py # 计时器相关原生函数
│   │   ├── trigger_natives.py # 触发器生命周期/动作/条件管理
│   │   └── trigger_register_event_natives.py # 触发器事件注册
│   ├── trigger/          # 触发器系统
│   │   ├── __init__.py   # 模块初始化
│   │   ├── trigger.py    # Trigger类
│   │   ├── manager.py    # TriggerManager类
│   │   └── event_types.py # 事件类型定义
│   ├── handles/          # Handle系统
│   │   ├── __init__.py   # 模块初始化
│   │   ├── handle.py     # Handle基类
│   │   ├── unit.py       # 单位类
│   │   └── player.py     # 玩家类
│   ├── handle_manager.py # 句柄管理器
│   ├── state_context.py  # 状态上下文
│   ├── timer/            # 计时器系统
│   │   ├── __init__.py
│   │   ├── timer.py      # Timer类
│   │   ├── system.py     # TimerSystem计时器管理
│   │   └── simulation.py # SimulationLoop模拟循环
│   ├── utils/            # 工具函数
│   │   ├── __init__.py
│   │   └── fourcc.py     # FourCC转换工具
│   └── vm/               # 虚拟机核心
│       ├── __init__.py
│       ├── jass_vm.py    # JassVM主类
│       └── cli.py        # 命令行接口
├── tests/
│   ├── __init__.py       # 测试包
│   ├── conftest.py       # pytest配置
│   ├── test_project_structure.py
│   ├── parser/          # 解析器测试
│   ├── interpreter/     # 解释器测试
│   ├── natives/         # native函数测试 (Phase 3)
│   │   ├── test_base.py       # 基础类测试
│   │   ├── test_registry.py   # 注册系统测试
│   │   ├── test_basic.py      # 基础native函数测试
│   │   ├── test_handle.py     # Handle类测试
│   │   ├── test_manager.py    # HandleManager测试
│   │   ├── test_timer_natives.py # Timer原生函数测试
│   │   ├── test_trigger_natives_unit.py # 触发器native函数测试
│   │   └── test_trigger_register_event_natives_unit.py # 触发器事件注册测试
│   ├── trigger/         # 触发器测试
│   │   ├── test_event_types.py    # 事件类型测试
│   │   ├── test_trigger.py        # Trigger类测试
│   │   ├── test_trigger_manager.py # TriggerManager测试
│   │   └── test_trigger_imports.py # 模块导入测试
│   ├── timer/           # 计时器测试
│   │   ├── test_timer.py
│   │   └── test_simulation.py
│   ├── vm/              # 虚拟机测试
│   │   ├── test_jass_vm.py
│   │   └── test_integration.py
│   ├── integration/     # 集成测试
│   │   ├── test_trigger_system.py      # 触发器系统基础集成测试
│   │   ├── test_trigger_natives.py     # 触发器Native函数集成测试
│   │   └── test_trigger_timer.py       # 计时器事件集成测试
├── examples/hello_world.j # 示例脚本
├── docs/plans/         # 实施计划文档
│   ├── 2026-02-24-jass-simulator-design.md
│   ├── 2026-02-24-jass-simulator-phase1-setup.md
│   ├── 2026-02-24-jass-simulator-phase2-interpreter.md
│   ├── 2026-02-24-jass-simulator-phase3-natives.md
│   ├── 2026-02-24-jass-simulator-phase4-timer.md
│   ├── 2026-02-24-jass-simulator-phase5-vm.md
│   ├── 2026-02-26-jass-simulator-state-management-design.md      # 状态管理设计
│   ├── 2026-02-26-jass-simulator-state-management-phase1-implementation.md  # Store核心
│   ├── 2026-02-26-jass-simulator-state-management-phase2-implementation.md  # Middleware
│   ├── 2026-02-26-jass-simulator-state-management-phase3-implementation.md  # Selector
│   ├── 2026-02-26-jass-simulator-state-management-phase4-implementation.md  # 集成
│   └── 2026-02-26-jass-simulator-state-management-phase5-implementation.md  # DevTools
├── docs/natives/README.md # Native函数文档
├── docs/phase1_summary.md # Phase 1总结
├── docs/phase2_summary.md # Phase 2总结
└── .git/               # 版本控制
```

## 技术架构

### 七层架构设计
1. **解析器层** - JASS语法解析，生成AST
2. **解释器层** - AST执行，变量作用域管理
3. **Native函数框架** - 插件式native函数模拟
4. **Handle系统** - 游戏对象管理（单位、玩家等）
5. **状态管理层** - 统一状态访问接口（StateContext + HandleManager）
6. **计时器系统** - 帧基计时器模拟
7. **虚拟机核心** - 组件集成和CLI

### 关键技术栈
- Python 3.8+
- pytest (测试框架)
- setuptools (包管理)
- 自定义解析器（无外部依赖）

## 下一步行动

### 当前任务 (完善Handle系统和状态管理)
1. **扩展Handle系统**
   - 添加更多游戏对象类型（Ability、Trigger、Timer等）
   - 完善单位属性和状态管理
   - 实现玩家属性和资源管理

2. **扩展原生函数**
   - 实现更多单位操作函数（移动、攻击、施法等）
   - 实现玩家相关函数（获取玩家名称、资源等）
   - 实现更多FourCC相关函数

3. **计时器系统** (Phase 4)
   - 基于帧的事件循环
   - Timer类管理单个计时器
   - TimerSystem管理系统中的多个计时器
   - SimulationLoop帧循环用于快速模拟

4. **虚拟机核心** (Phase 5)
   - JassVM类集成所有组件
   - 脚本加载和执行入口点
   - 命令行接口实现

### 后续任务
- 状态管理Redux-like架构（Store、Middleware、Selector）
- DevTools开发工具（时间旅行调试）
- 性能优化和大规模脚本测试

## 开发原则

1. **TDD方法**：测试驱动开发，先写失败测试
2. **小步提交**：每个任务完成后立即提交
3. **代码质量**：使用flake8进行代码检查
4. **文档驱动**：保持文档与代码同步更新

## 关键决策记录

1. **编程语言选择**：Python 3.8+，因其易用性和丰富的库生态系统
2. **架构选择**：轻量级解释器+插件系统，平衡性能和扩展性
3. **计时器实现**：帧基模拟而非实时，支持快速测试
4. **Native函数设计**：插件式架构，便于扩展和测试
5. **状态管理设计**：Redux-like架构，解耦状态管理与执行上下文，支持时间旅行调试
6. **Handle系统设计**：引入Handle基类和HandleManager，统一管理游戏对象生命周期
7. **状态上下文设计**：StateContext作为统一状态访问接口，便于原生函数访问游戏状态
8. **FourCC处理**：使用小端序整数表示JASS单位类型ID，提供转换工具函数
9. **Native函数参数类型设计**：
   - `DisplayTextToPlayer` 等函数使用对象类型（Player、Unit、Timer）而非原始ID
   - 更符合JASS语义，提供更好的类型安全
10. **触发器系统设计**：采用混合架构，Trigger类管理单个触发器状态，TriggerManager集中管理生命周期和事件分发
11. **事件系统集成**：HandleManager和TimerSystem直接触发事件到TriggerManager，保持架构简洁
10. **Parser设计**：支持嵌套函数调用、布尔值字面量、函数引用等高级语法

## 待解决问题

1. **JASS语法覆盖**：需要确定支持的JASS语法子集
2. **性能考虑**：大规模脚本执行的性能优化
3. **错误处理**：详细的错误信息和调试支持
4. **测试覆盖率**：确保关键功能的测试覆盖

---
#### 30. DisplayTextToPlayer 和 Player 原生函数修复 (2026-02-27)
- **问题修复**：`DisplayTextToPlayer` 第一个参数类型修正
  - 从 `player_id: int` 改为 `player: Player` 对象
  - 更符合 JASS 原生函数的语义
- **新增 `Player` 原生函数**：`src/jass_runner/natives/basic.py`
  - 通过 `player_id` 获取 `Player` 实体
  - 内部通过 `HandleManager.get_player()` 获取或创建 Player 对象
- **NativeFactory 更新**：`src/jass_runner/natives/factory.py`
  - 注册 `PlayerNative` 到默认注册表
- **测试更新**：`tests/natives/test_basic.py`
  - 更新 `test_display_text_to_player` 测试使用 Player 对象
  - 新增 `test_player_native` 测试验证 Player 原生函数
- **示例文件更新**：
  - `hello_world.j`: `GetLocalPlayer()` → `Player(0)`
  - `complete_example.j`: 5处 `0` → `Player(0)`
  - `timer_example.j`: 3处 `0` → `Player(0)`
  - `state_management_test.j`: 5处 `player` → `Player(player)`

#### 31. Parser 增强 - 嵌套函数调用和高级参数支持 (2026-02-27)
- **嵌套函数调用支持**：`src/jass_runner/parser/parser.py`
  - 解析 `DisplayTextToPlayer(Player(0), 0, 0, "Hello")` 语法
  - 支持函数调用作为其他函数的参数
  - 创建 `NativeCallNode` 嵌套节点结构
- **布尔值字面量支持**：
  - 识别 `true` / `false` 关键字
  - 转换为布尔类型传递给原生函数
- **函数引用支持**：
  - 识别 `function func_name` 语法
  - 用于计时器回调等场景
  - 格式化为 `function:func_name` 供求值器处理

#### 32. Evaluator 增强 - 布尔值和函数引用支持 (2026-02-27)
- **布尔值解析**：`src/jass_runner/interpreter/evaluator.py`
  - `'true'` → `True`, `'false'` → `False`
- **函数引用解析**：
  - 解析 `function:func_name` 格式
  - 创建回调包装器，支持计时器回调执行
- **ExecutionContext 增强**：`src/jass_runner/interpreter/context.py`
  - 添加 `interpreter` 引用，使 Evaluator 能访问函数定义
- **Interpreter 更新**：`src/jass_runner/interpreter/interpreter.py`
  - 创建上下文时传递 `interpreter=self`

#### 33. Timer 原生函数签名修复 (2026-02-27)
- **CreateTimer 修复**：`src/jass_runner/natives/timer_natives.py`
  - 从返回 `timer_id: str` 改为返回 `Timer` 对象
  - 更符合 JASS 原生函数语义
- **Timer 操作函数修复**：
  - `TimerStart`：第一个参数从 `timer_id: str` 改为 `timer: Timer`
  - `TimerGetElapsed`：第一个参数从 `timer_id: str` 改为 `timer: Timer`
  - `DestroyTimer`：第一个参数从 `timer_id: str` 改为 `timer: Timer`
  - `PauseTimer`：第一个参数从 `timer_id: str` 改为 `timer: Timer`
  - `ResumeTimer`：第一个参数从 `timer_id: str` 改为 `timer: Timer`
- **测试更新**：
  - `tests/natives/test_timer_natives.py`：更新测试使用 Timer 对象
  - `tests/integration/test_timer_integration.py`：更新集成测试

#### 34. 示例脚本修复 (2026-02-27)
- **run_timer_example.py**：更新 API 调用
  - `JassParser` → `Parser`
  - `JassInterpreter` → `Interpreter`
  - 更新方法调用以匹配新类签名

#### 35. 控制流语句扩展完成 (2026-02-28)
- **Phase 1 - Parser层控制流解析**：
  - 创建 `IfStmt`, `LoopStmt`, `ExitWhenStmt`, `ReturnStmt` AST节点
  - 实现 `parse_if_statement` 方法支持 if/elseif/else/endif
  - 实现 `parse_loop_statement` 方法支持 loop/endloop
  - 实现 `parse_exitwhen_statement` 方法支持 exitwhen
  - 实现 `parse_return_statement` 方法支持 return
  - 创建完整测试覆盖：`tests/parser/test_parser.py` 新增控制流测试

- **Phase 2 - Evaluator层运算符支持**：
  - 添加 `evaluate_condition` 方法用于条件求值
  - 实现完整运算符支持：`+`, `-`, `*`, `/`, `==`, `!=`, `<`, `>`, `<=`, `>=`, `and`, `or`, `not`
  - 使用调度场算法处理运算符优先级
  - 支持逻辑运算符短路求值
  - 创建完整测试覆盖：`tests/interpreter/test_evaluator.py` 新增运算符测试

- **Phase 3 - Interpreter层控制流执行**：
  - 添加 `ReturnSignal` 和 `ExitLoopSignal` 控制流异常类
  - 实现 `execute_if_statement` 方法支持 if/elseif/else 执行
  - 实现 `execute_loop_statement` 方法支持 loop 执行
  - 实现 `execute_exitwhen_statement` 方法支持 exitwhen
  - 实现 `execute_return_statement` 方法支持 return
  - 修改 `execute_function` 处理 `ReturnSignal`
  - 添加 `_call_function_with_args` 支持函数调用获取返回值
  - 修复函数调用后上下文恢复问题
  - 创建完整测试覆盖：15个解释器测试全部通过

- **Phase 4 - 集成测试和示例脚本**：
  - 创建 `tests/integration/test_control_flow_integration.py`
    - 斐波那契数列测试（递归+条件）
    - 累加和测试（loop）
    - 素数判断测试（嵌套控制流）
    - 最大公约数测试（loop）
    - 嵌套循环矩阵测试
    - 复杂控制流组合测试（阶乘）
  - 创建 `examples/control_flow_demo.j` 演示脚本
    - 累加和计算
    - 嵌套循环乘法表
    - 查找值示例
    - 简单条件判断示例
  - 修复 `parse_set_statement` 支持表达式赋值（如 `i + 1`）

- **测试统计**：
  - 所有 158 个测试通过
  - 核心模块覆盖率：interpreter 95%+

#### 36. Globals 全局变量块实现完成 (2026-02-28)
- **Parser层实现**：
  - 创建 `GlobalDecl` AST节点 (`src/jass_runner/parser/parser.py`)
  - 扩展 `AST` 根节点添加 `globals` 列表
  - 实现 `parse_globals_block` 方法解析 `globals`/`endglobals` 块
  - 实现 `parse_global_declaration` 方法解析单个全局变量声明
  - 支持可选初始值（integer, real, string, boolean）
  - 添加变量名冲突检查（局部变量与全局变量同名时报错）

- **Interpreter层实现**：
  - 修改 `execute` 方法初始化全局变量到 `global_context`
  - 支持初始值表达式求值
  - 全局变量在函数间共享状态

- **测试覆盖**：
  - 创建 `tests/parser/test_globals.py` - 5个解析器测试
    - 带初始值的全局变量解析
    - 无初始值的全局变量解析
    - 空的 globals 块
    - 没有 globals 块的代码
    - 局部变量与全局变量同名检查
  - 创建 `tests/interpreter/test_globals_interp.py` - 4个解释器测试
    - 全局变量初始化
    - 函数内访问全局变量
    - 函数内修改全局变量
    - 全局变量状态持久化
  - 创建 `tests/integration/test_globals_integration.py` - 3个集成测试
    - 全局变量在控制流中使用
    - 全局变量在函数间共享状态
    - 完整示例脚本（游戏积分系统）

- **测试统计**：
  - 所有 170 个测试通过
  - 核心模块覆盖率：interpreter 98%

#### 37. Constant 常量支持实现完成 (2026-02-28)
- **AST扩展**：
  - 修改 `GlobalDecl` 节点添加 `is_constant` 标记 (`src/jass_runner/parser/ast_nodes.py`)
  - 默认为 `False` 保持向后兼容

- **Parser层实现**：
  - 扩展 `parse_global_declaration` 方法支持 `constant` 关键字解析
  - 验证常量声明必须有初始值，否则记录解析错误
  - 收集常量名称集合用于后续修改检查

- **常量修改保护**：
  - 在 `parse_set_statement` 中检查是否尝试修改常量
  - 检测到常量修改时记录详细错误信息（包含行列号）
  - 错误恢复机制确保解析器继续处理后续代码

- **测试覆盖**：
  - 创建 `tests/parser/test_constant.py` - 4个解析器测试
    - `test_parse_constant_declaration` - 常量声明解析（integer）
    - `test_parse_constant_real_declaration` - real类型常量
    - `test_parse_constant_without_initial_value_errors` - 无初始值错误检查
    - `test_parse_set_constant_errors` - 修改常量错误检查
  - 创建 `tests/interpreter/test_constant_interp.py` - 2个解释器测试
    - `test_constant_initialization` - 常量初始化验证
    - `test_constant_access_in_function` - 函数内访问常量
  - 创建 `tests/integration/test_constant_integration.py` - 1个集成测试
    - `test_constant_with_globals_integration` - 常量与普通变量混合使用

- **测试统计**：
  - 所有 173 个测试通过（新增3个）
  - 常量相关测试全部通过

#### 38. Array 数组语法支持实现完成 (2026-02-28)
- **AST扩展**：
  - 创建 `ArrayDecl`, `ArrayAccess`, `SetArrayStmt`, `IntegerExpr`, `VariableExpr` 节点
- **Parser层**：支持全局/局部数组声明、数组访问表达式、数组赋值
- **Lexer层**：添加 `[` 和 `]` 方括号支持
- **ExecutionContext**：添加数组存储和管理方法（8192元素标准）
- **Interpreter**：支持数组声明和赋值执行
- **Evaluator**：支持数组访问求值
- **测试**：190个测试全部通过（新增17个数组测试）
- **限制**：不支持多维数组，不进行运行时边界检查

#### 39. JASS触发器系统实现完成 (2026-03-01)
- **核心组件实现**：
  - 创建 `src/jass_runner/trigger/event_types.py` - 16个事件类型常量定义
  - 创建 `src/jass_runner/trigger/trigger.py` - Trigger类（事件/条件/动作管理）
  - 创建 `src/jass_runner/trigger/manager.py` - TriggerManager类（生命周期管理和事件分发）
  - 创建 `src/jass_runner/trigger/__init__.py` - 模块导出所有公共API
- **Native函数实现（20个）**：
  - 生命周期管理：`CreateTrigger`, `DestroyTrigger`, `EnableTrigger`, `DisableTrigger`, `IsTriggerEnabled`
  - 动作管理：`TriggerAddAction`, `TriggerRemoveAction`, `TriggerClearActions`
  - 条件管理：`TriggerAddCondition`, `TriggerRemoveCondition`, `TriggerClearConditions`, `TriggerEvaluate`
  - 事件注册：`TriggerRegisterTimerEvent`, `TriggerRegisterTimerExpireEvent`, `TriggerRegisterPlayerUnitEvent`, `TriggerRegisterUnitEvent`, `TriggerRegisterPlayerEvent`, `TriggerRegisterGameEvent`
  - 事件清理：`TriggerClearEvents`
- **系统集成**：
  - StateContext集成TriggerManager
  - HandleManager集成（kill_unit触发EVENT_UNIT_DEATH事件）
  - Timer/TimerSystem集成（计时器到期触发EVENT_GAME_TIMER_EXPIRED事件）
  - ExecutionContext暴露TriggerManager
- **集成测试**：
  - 基础集成测试（5个测试）
  - Native函数集成测试（6个测试）
  - 计时器事件集成测试（5个测试）
- **示例脚本**：
  - `examples/trigger_basic.j` - 基础触发器示例
  - `examples/trigger_unit_death.j` - 单位死亡事件处理示例
  - `examples/trigger_timer.j` - 计时器触发器示例
  - `examples/run_trigger_examples.py` - 示例运行脚本
- **测试统计**：
  - 所有345个测试通过
  - 触发器系统核心模块覆盖率：95%-100%

### 当前状态
- ✅ 需求分析和设计完成
- ✅ 5个阶段实施计划完成
- ✅ Phase 1 所有任务完成
- ✅ Phase 2 所有任务完成
- ✅ Phase 3 所有任务完成
- ✅ 状态管理系统架构设计完成
- ✅ Handle系统核心实现
- ✅ **DisplayTextToPlayer 和 Player 原生函数修复完成**
- ✅ **Timer 原生函数签名修复完成**
- ✅ **Parser 增强（嵌套函数调用、布尔值、函数引用）完成**
- ✅ **Evaluator 增强（布尔值、函数引用）完成**
- ✅ **控制流语句扩展完成（if/loop/exitwhen/return + 运算符）**
- ✅ **Globals 全局变量块实现完成**
- ✅ **Constant 常量支持实现完成**
- ✅ **Array 数组语法支持实现完成**
- ✅ **JASS触发器系统实现完成**
- ✅ 所有 345 个测试通过

---
*最后更新: 2026-03-01*