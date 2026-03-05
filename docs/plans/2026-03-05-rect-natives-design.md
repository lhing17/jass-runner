# Rect Native 函数设计文档

## 概述

实现 JASS Rect 类型的核心 native 函数，支持创建、修改和查询矩形区域。

## 范围

**第一阶段（本次实现）：**
- 构造函数：Rect, RemoveRect
- 修改函数：SetRect, MoveRectTo
- 查询函数：GetRectCenterX/Y, GetRectMinX/Y, GetRectMaxX/Y

**第二阶段（后续实现）：**
- Location 相关：RectFromLoc, SetRectFromLoc, MoveRectToLoc

## 使用示例

```jass
// 创建矩形
set gg_rct_Region_001 = Rect(-1000.0, -1000.0, 1000.0, 1000.0)

// 查询矩形边界
set minX = GetRectMinX(gg_rct_Region_001)
set centerX = GetRectCenterX(gg_rct_Region_001)

// 修改矩形
call SetRect(gg_rct_Region_001, -500.0, -500.0, 500.0, 500.0)
call MoveRectTo(gg_rct_Region_001, 0.0, 0.0)

// 移除矩形
call RemoveRect(gg_rct_Region_001)
```

## 架构设计

### 1. Rect 构造函数

**Rect native 函数**
- 创建新的 Rect 对象
- 通过 HandleManager 管理生命周期
- 返回 rect handle ID

**RemoveRect native 函数**
- 从 HandleManager 中移除 Rect
- 清理相关资源

### 2. Rect 修改函数

**SetRect**
- 更新现有 Rect 的边界坐标
- 验证坐标有效性（min <= max）

**MoveRectTo**
- 移动矩形到新的中心点
- 保持矩形宽高不变
- 计算：newMin = center - width/2, newMax = center + width/2

### 3. Rect 查询函数

**GetRectCenterX/Y**
- 计算矩形中心点：(min + max) / 2

**GetRectMinX/Y, GetRectMaxX/Y**
- 直接返回 Rect 对象的属性

## 数据流

```
JASS脚本调用 Rect(minx, miny, maxx, maxy)
         |
         v
   Rect Native函数
         |
         v
   HandleManager.create_handle(Rect对象)
         |
         v
   返回rect handle ID

JASS脚本调用 GetRectCenterX(rect_handle)
         |
         v
   GetRectCenterX Native函数
         |
         v
   HandleManager.get_handle(rect_handle) -> Rect对象
         |
         v
   计算并返回 (min_x + max_x) / 2
```

## 文件清单

| 文件路径 | 说明 |
|---------|------|
| `src/jass_runner/natives/rect_natives.py` | Rect native 函数实现 |
| `tests/natives/test_rect_natives.py` | Rect native 函数测试 |

## 依赖

- `src/jass_runner/natives/rect.py` - Rect 类已存在
- `src/jass_runner/natives/manager.py` - HandleManager
- `src/jass_runner/natives/state.py` - StateContext

## 注意事项

1. 所有坐标使用 float 类型
2. Rect 对象通过 HandleManager 管理生命周期
3. 查询函数需要验证 rect handle 有效性
4. MoveRectTo 保持矩形尺寸不变，只改变位置
5. 代码使用中文注释
