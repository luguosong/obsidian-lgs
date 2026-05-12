# 瞬态批注系统设计文档

> 日期: 2026-04-17  
> 状态: 实施中

## 1. 概述

在 [[WebUACAD]] 前端实现批注（Markup / Annotation）功能，支持**云线 + 箭头 + 批注文本**的组合批注。批注对象不写入 DWG 数据库，而是作为 ODA 引擎的**瞬态图元**（Transient Drawable）渲染在 GsView 上，数据以 JSON 格式独立存储。

### 核心设计原则

- **不修改 DWG**：批注实体通过 `OdGsView::add()` 瞬态显示，不调用 `appendOdDbEntity()`
- **渲染一致性**：复用 ODA 引擎渲染管线，与 DWG 图元视觉风格完全一致
- **零坐标同步**：ODA 引擎自动处理 zoom/pan 时的坐标变换，无需 JS 侧手动同步
- **数据独立存储**：批注数据以 JSON 存储在前端，与 DWG 文件关联但不嵌入

## 2. 架构总览

```
┌─────────────── JS 前端 ─────────────────────┐
│                                              │
│  AnnotationStore (MobX)                      │
│   ├── annotations: Map<id, AnnotationData>   │
│   ├── loadAnnotations(json)                  │
│   ├── saveAnnotations() → json               │
│   ├── addCloudAnnotation(points, text)       │
│   ├── removeAnnotation(id)                   │
│   └── zoomToAnnotation(id)                   │
│                                              │
│  AnnotationPanel (UI)                        │
│   ├── 批注列表（选择、导航、删除）             │
│   └── 批注工具栏（创建、模式切换）             │
│                                              │
│  ViewerService                               │
│   ├── addTransientCloud(...)                  │
│   ├── addTransientArrow(...)                  │
│   ├── addTransientText(...)                   │
│   ├── removeTransient(id)                     │
│   └── clearAllTransients()                   │
│                                              │
└──────────────┬──────────────────────────────┘
               │  WASM embind 调用
               ▼
┌─────────────── C++ CadCore ─────────────────┐
│                                              │
│  CadCore (CadCoreAnnotation.cpp)             │
│   ├── AddTransientCloud(json, arcLen, color) │
│   ├── AddTransientArrow(from, to, color)     │
│   ├── AddTransientText(pos, text, h, color)  │
│   ├── RemoveTransient(id)                    │
│   ├── ClearAllTransients()                   │
│   ├── SetTransientVisible(id, visible)       │
│   └── GetTransientExtents(id) → bbox json    │
│                                              │
│  内部管理：                                   │
│   ├── m_transients: map<int, OdDbEntityPtr>  │
│   ├── m_nextTransientId: int                 │
│   └── reattachAllTransients() [视图重建后]    │
│                                              │
└──────────────┬──────────────────────────────┘
               │  OdGsView::add(pEntity, nullptr)
               ▼
┌─────────────── ODA 渲染引擎 ────────────────┐
│  瞬态图元在 GsView 中渲染                    │
│  ├── 不写入 OdDbDatabase                     │
│  ├── 随视图 zoom/pan 自动变换                │
│  └── 与 DWG 图元完全一致的渲染质量            │
└──────────────────────────────────────────────┘
```

## 3. 瞬态图元类型

### 3.1 云线 (Revision Cloud)

使用 `OdDbPolyline`，每对相邻顶点间为半圆弧（`bulge = -1.0`）。

算法源自 `Drawing/Examples/ExCommands/ExRevcloud.cpp`：

- 弦长 = `2 × arcLen / π`
- 沿路径按弦长间距采样顶点
- 每段设 `bulge = -1.0`（半圆弧，向外凸出）
- 支持手绘、矩形、多边形三种创建模式

### 3.2 箭头 (Arrow / Leader)

使用 `OdDbLeader`，支持：
- 箭头起点（指向目标位置）
- 一个或多个折点
- 箭头末端连接文本

### 3.3 批注文本 (Annotation Text)

使用 `OdDbMText`，支持：
- 多行[[文本内容]]
- 字高、颜色、对齐方式
- 自动换行宽度

## 4. C++ 接口设计

### 4.1 CadCore 新增方法

```cpp
// ---- 瞬态批注管理 ----

// 创建云线批注，返回 transient ID
// pointsJson: [{"x":100,"y":200}, ...] 闭合多边形角点
int AddTransientCloud(std::string pointsJson, double arcLen, int colorIndex);

// 创建箭头/引线批注
int AddTransientArrow(double fromX, double fromY,
                      double toX, double toY, int colorIndex);

// 创建文本批注
int AddTransientText(double x, double y,
                     std::wstring text, double height, int colorIndex);

// 移除单个瞬态图元
void RemoveTransient(int id);

// 清除所有瞬态图元
void ClearAllTransients();

// 显示/隐藏
void SetTransientVisible(int id, bool visible);

// 获取图元包围盒（用于 ZoomToRect）
// 返回 JSON: {"minX":...,"minY":...,"maxX":...,"maxY":...}
std::string GetTransientExtents(int id);
```

### 4.2 内部数据结构

```cpp
// CadCore.h private section
struct TransientEntry {
    OdDbEntityPtr pEntity;
    bool visible;
};
std::map<int, TransientEntry> m_transients;
int m_nextTransientId = 1;

// 视图重建后重新 add 所有瞬态图元
void reattachAllTransients();
```

### 4.3 关键实现细节

**实体创建**（以云线为例）：

```cpp
OdDbPolylinePtr pPl = OdDbPolyline::createObject();
pPl->setDatabaseDefaults(m_pDatabase);  // 初始化默认属性
// ... 设置顶点和 bulge ...
// 不调用 pSpace->appendOdDbEntity(pPl) — 不写入数据库

OdGsView* pView = getActiveView();
pView->add(pPl, nullptr);  // 瞬态显示，无 GsModel
pView->invalidate();
m_pDevice->update();
```

**视图重建恢复**：SwitchLayout / regenAll 等操作会重建 GsView，需在这些操作后调用 `reattachAllTransients()` 将所有瞬态图元重新 add 到新的 GsView。

## 5. JSON 存储格式

```json
{
  "version": 1,
  "dwgFileName": "building.dwg",
  "createdAt": "2026-04-17T10:30:00Z",
  "annotations": [
    {
      "id": "a1b2c3d4",
      "type": "cloud_with_arrow_and_text",
      "author": "张三",
      "status": "open",
      "createdAt": "2026-04-17T10:30:00Z",
      "comment": "此处尺寸标注有误，请修正",
      "viewState": {
        "centerX": 1500, "centerY": 2300,
        "fieldWidth": 500, "fieldHeight": 350
      },
      "elements": {
        "cloud": {
          "points": [
            {"x": 1400, "y": 2200},
            {"x": 1600, "y": 2200},
            {"x": 1600, "y": 2400},
            {"x": 1400, "y": 2400}
          ],
          "arcLength": 50,
          "colorIndex": 1
        },
        "arrow": {
          "from": {"x": 1600, "y": 2300},
          "to": {"x": 1750, "y": 2450},
          "colorIndex": 1
        },
        "text": {
          "position": {"x": 1750, "y": 2470},
          "content": "此处尺寸标注有误，请修正",
          "height": 20,
          "colorIndex": 1
        }
      },
      "transientIds": []
    }
  ]
}
```

- `viewState`: 创建批注时记录的视图状态，用于点击批注列表时自动定位
- `transientIds`: 运行时填充，对应 C++ 侧的 transient ID 列表
- `status`: "open" | "resolved" | "closed" — 批注状态

## 6. 前端模块

### 6.1 AnnotationStore (MobX)

```
src/stores/AnnotationStore.js
```

职责：
- 管理批注数据（CRUD）
- 调用 ViewerService 创建/删除瞬态图元
- JSON 序列化/反序列化
- 批注选中状态、过滤

### 6.2 ViewerService 扩展

在 `Viewer` 类中新增批注相关方法，封装 `appCore.AddTransient*` 调用。

### 6.3 UI 组件（后续开发）

- `AnnotationPanel`: 批注列表面板（集成在右侧栏或底部停靠区）
- `AnnotationToolbar`: 批注绘制工具栏（集成在 Ribbon 中）

## 7. 生命周期与事件流

```
用户创建批注:
  1. [UI] 用户选择"添加云线批注"
  2. [UI] 用户在图纸上圈选区域 → 获取世界坐标点
  3. [Store] addCloudAnnotation(points, text)
  4. [Viewer] appCore.AddTransientCloud(pointsJson, arcLen, color)
  5. [C++] 创建 OdDbPolyline → pView->add() → invalidate → update
  6. [Store] 记录 transientId，保存到 annotations Map

用户选择批注:
  1. [UI] 用户点击批注列表中的某项
  2. [Store] selectAnnotation(id)
  3. [Viewer] appCore.ZoomToRect(extents) → 定位到批注区域

打开 DWG 文件时加载批注:
  1. [Store] loadAnnotations(json) → 解析 JSON
  2. 遍历所有 annotation，调用 Viewer 创建瞬态图元
  3. 记录 transientId 映射

关闭/切换文件:
  1. [Viewer] appCore.ClearAllTransients()
  2. [Store] 序列化当前批注为 JSON 保存

视图重建 (SwitchLayout / regenAll):
  1. [C++] reattachAllTransients() 自动恢复所有瞬态图元
```

## 8. 开发步骤

| 阶段 | 内容 | 文件 |
|------|------|------|
| **Phase 1** | C++ 瞬态管理器 | `CadCore.h`, `CadCoreAnnotation.cpp`, `App.cpp`, `CMakeLists.txt` |
| **Phase 2** | JS 服务层 | `ViewerService.js`, `AnnotationStore.js`, `RootStore.js` |
| **Phase 3** | 批注 UI（后续） | `AnnotationPanel.jsx`, Ribbon 集成 |
| **Phase 4** | JSON 持久化（后续） | localStorage / IndexedDB / 服务端存储 |

## 9. 注意事项

1. **[[内存管理]]**: 瞬态实体由 `OdSmartPtr` 管理，从 `m_transients` map 移除时自动释放
2. **多视口**: 当前阶段只向 `getActiveView()` 添加瞬态图元
3. **颜色**: 批注默认使用 ACI 红色 (1)，区别于 DWG 图元
4. **云线弧长**: 应根据图纸实际尺度自适应，可参考当前视口范围计算合理值
5. **视图重建**: `SwitchLayout` / `regenAll` / `RefreshActiveViewports` 后需调用 `reattachAllTransients()`
6. **embind upcast**: `OdGsView::add()` 接受 `OdGiDrawable*`，[[OdDbPolyline]] 通过完整的继承链 (`OdDbPolyline → OdDbCurve → OdDbEntity → OdDbObject → OdGiDrawable`) 自动向上转型

## 相关笔记

- [[specs]]
- [[GIS服务 Ribbon 标签页设计规格]]
- [[图例分析功能设计规格]]
- [[ArcGIS Web 服务集成 — C++ 实施架构]]
- [[GIS服务 Ribbon 标签页 Implementation Plan]]
- [[GIS File Import / Save-Back Design]]
- [[GIS服务 Ribbon 标签页 — 后续实施设计]]
- [[GIS服务后续实施 Implementation Plan]]
