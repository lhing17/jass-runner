# 技术债务记录 (Technical Debt Log)

本文档用于记录项目开发过程中识别出的技术债务，包括设计缺陷、代码异味、临时解决方案以及已知的局限性。这些问题目前可能不影响核心功能，但长期来看会影响可维护性、扩展性或性能，需要在未来的重构周期中予以解决。

## 1. Parser 与 Evaluator 的职责重叠 (Parsing/Evaluation Responsibility Overlap)

### 问题描述
目前的表达式解析和求值逻辑在 `ExpressionParser` 和 `Evaluator` 之间存在不合理的职责重叠和重复解析问题。

- **现象**：
  - `ExpressionParser.parse_expression` 将复杂的算术表达式（如 `3 * 8 + 2`）解析并扁平化为字符串（如 `"3 * 8 + 2"`），而不是构建结构化的 AST（如 `BinaryOpNode`）。
  - `GlobalParser` 将这个字符串直接作为 `GlobalDecl.value` 存储。
  - 在解释执行阶段，`Interpreter` 将该字符串传递给 `Evaluator.evaluate`。
  - `Evaluator.evaluate` 内部再次对该字符串进行 tokenize 和 parsing，然后计算结果。

### 影响
1.  **性能损耗**：同一段代码被解析了两次（Parser 一次，Evaluator 一次）。
2.  **类型系统混乱**：AST 节点中的 `value` 字段类型不明确，既可以是字面量（`int`, `float`），也可以是表达式字符串（`str`），还可以是 `NativeCallNode`。
3.  **架构不纯粹**：解释器依赖于字符串作为中间表示（IR），而非标准的 AST。

### 推荐解决方案
1.  修改 `ExpressionParser`，使其返回结构化的 AST 节点（如 `BinaryOpNode`, `UnaryOpNode`, `LiteralNode`）。
2.  更新 `GlobalDecl` 和其他 AST 节点以存储结构化表达式。
3.  重构 `Evaluator`，使其主要基于 AST 节点进行求值，逐步移除对复杂字符串表达式的解析支持（仅保留用于调试或特殊动态场景）。

### 优先级
**中** (Medium) - 目前功能正常且稳定，但在引入更复杂的表达式优化或静态分析时会成为阻碍。

---

## 2. 脆弱的常量解析 (Fragile Constant Parsing in ConstantLoader)

### 问题描述
`src/jass_runner/utils/constant_loader.py` 使用正则表达式来解析 `common.j` 和 `blizzard.j` 中的常量定义。

- **现象**：
  - 使用 `re.compile(r'^\s*constant\s+(\w+)\s+(\w+)\s*=\s*([^/\r\n]+)', ...)` 进行匹配。
  - 这种正则匹配对于包含注释、复杂表达式或特殊格式的常量定义非常脆弱。
  - 即使项目已经有了完整的 `Parser`，这里却维护了一套独立的、简化的正则解析逻辑。

### 影响
1.  **维护成本**：如果 JASS 语法有细微变化，需要同时维护 Parser 和正则。
2.  **鲁棒性差**：容易被特殊格式的常量定义破坏（例如值中包含除号 `/` 可能被误判为注释）。

### 推荐解决方案
复用 `Parser` 来解析常量文件。由于 `common.j` 主要是声明序列，可以使用 `Parser` 解析并遍历 AST 来提取常量，或者为 `Parser` 添加专门的“仅解析声明”模式。

### 优先级
**低** (Low) - `common.j` 文件格式相对固定，目前的正则方案在当前场景下尚能工作。

---

## 3. Handle 类型解析的硬编码 (Hardcoded Handle Type Parsing)

### 问题描述
在 `ConstantLoader._parse_handle_type` 和其他部分，存在大量针对特定 Handle 类型（如 `playerunitevent`, `gamestate`）的硬编码逻辑。

### 影响
违反开闭原则（OCP），每增加一种 Handle 类型都需要修改解析逻辑。

### 推荐解决方案
建立统一的 Handle 类型注册表，通过元数据驱动的方式自动处理不同类型的 Handle 创建和转换。

### 优先级
**低** (Low) - 已通过字典映射进行了初步优化，但仍有改进空间。
