# JASS 数学 Native 函数设计文档

**日期**: 2026-03-01
**主题**: 数学 Native 函数实现设计
**参考**: common.j 标准库

---

## 1. 概述

### 1.1 目标
实现 common.j 中定义的数学 Native 函数，支持 JASS 脚本中的数学运算需求。

### 1.2 设计原则
- **标准兼容**: 严格遵循 common.j 函数签名和行为
- **分阶段实现**: 核心函数优先，扩展函数次之
- **错误处理**: 参数异常时返回默认值，不中断执行

---

## 2. 架构设计

### 2.1 文件结构
```
src/jass_runner/natives/
├── math_core.py      # 核心数学函数 (6个)
└── math_extended.py  # 扩展数学函数 (9个)
```

### 2.2 函数分类

#### 核心数学函数 (math_core.py)
| 函数名 | 参数 | 返回值 | 用途 |
|--------|------|--------|------|
| SquareRoot | real r | real | 平方根计算 |
| Pow | real x, real power | real | 幂运算 |
| Cos | real r | real | 余弦函数 |
| Sin | real r | real | 正弦函数 |
| R2I | real r | integer | 实数转整数 |
| I2R | integer i | real | 整数转实数 |

#### 扩展数学函数 (math_extended.py)
| 函数名 | 参数 | 返回值 | 用途 |
|--------|------|--------|------|
| Tan | real r | real | 正切函数 |
| ModuloInteger | integer a, integer b | integer | 整数取模 |
| ModuloReal | real a, real b | real | 实数取模 |
| R2S | real r | string | 实数转字符串 |
| S2R | string s | real | 字符串转实数 |
| I2S | integer i | string | 整数转字符串 |
| S2I | string s | integer | 字符串转整数 |
| GetRandomInt | integer low, integer high | integer | 随机整数 |
| GetRandomReal | real low, real high | real | 随机实数 |

---

## 3. 技术细节

### 3.1 角度单位
- JASS 使用弧度制
- Python math 模块也是弧度制，直接对应

### 3.2 类型转换规则
- R2I: 向零截断（Python int() 行为一致）
- I2R: 直接转换
- S2I/S2R: 无效字符串返回 0

### 3.3 随机数实现
- 使用 Python random 模块
- 支持设置随机种子（通过单独的 SetRandomSeed 函数）

### 3.4 错误处理
- 参数为 null/None 时返回 0 或默认值
- 不抛出异常，符合 JASS 行为

---

## 4. 集成方案

### 4.1 注册到 NativeFactory
在 `NativeFactory.create_default_registry()` 中注册所有数学函数：
1. 从 math_core 导入核心函数
2. 从 math_extended 导入扩展函数
3. 依次注册到 registry

### 4.2 模块导出
更新 `natives/__init__.py` 导出数学函数类。

---

## 5. 测试策略

### 5.1 单元测试
- 每个函数独立测试
- 测试正常输入和边界条件
- 测试错误处理（null 参数）

### 5.2 集成测试
- 测试在 JASS 脚本中的使用
- 验证与 Evaluator 的集成

---

## 6. 实施计划

### 阶段1: 核心数学函数
实现 math_core.py 中的 6 个函数，包含完整测试。

### 阶段2: 扩展数学函数
实现 math_extended.py 中的 9 个函数，包含完整测试。

### 阶段3: 集成与注册
注册到 NativeFactory，运行完整测试套件验证无回归。

---

## 7. 审批

| 项目 | 状态 |
|------|------|
| 函数清单 | 已确认 |
| 文件结构 | 已确认 |
| 实施计划 | 已确认 |

**审批人**: [用户]
**日期**: 2026-03-01
