# 批注数据持久化方案

> 创建日期: 2026-04-17

## 概述

瞬态批注（Transient Annotation）仅存在于 `OdGsView` 运行时内存中，页面刷新或文件关闭后即丢失。本文档描述如何将批注数据持久化，使其在重新打开 DWG 文件时能够恢复。

## 现有基础

`AnnotationStore` 已具备完整的序列化/反序列化能力：

| 方法 | 作用 |
|------|------|
| `toJSON()` | 将所有批注导出为纯 JSON（自动剥离运行时 `transientIds`） |
| `loadAnnotations(viewer, json)` | 从 JSON 恢复批注并重建 C++ 侧瞬态图元 |

核心问题：**JSON 存到哪里？**

## 存储位置对比

| 方案 | 实现难度 | 多人协作 | 离线可用 | 容量限制 |
|------|---------|---------|---------|---------|
| **A. localStorage** | 最简单 | 不支持 | 是 | ~5 MB |
| **B. IndexedDB** | 简单 | 不支持 | 是 | 数百 MB+ |
| **C. 服务端 (Node 后端)** | 中等 | 支持 | 需联网 | 无限 |

**推荐：方案 A 起步，按需升级。**

项目已在 `useWasmModule.js` 中使用 `localStorage` 保存 `uacad_config`，模式完全一致，零额外依赖。

## 详细设计 (方案 A — localStorage)

### 存储 Key 设计

以 DWG 文件名为 key，每个文件的批注独立存储：

```
annotations_{fileName}
```

### AnnotationStore 新增方法

```javascript
/**
 * 打开文件后调用 — 从 localStorage 恢复批注
 */
persistLoad(viewer, fileName) {
  this.dwgFileName = fileName
  const key = `annotations_${fileName}`
  const json = localStorage.getItem(key)
  if (json) {
    this.loadAnnotations(viewer, json)
  }
}

/**
 * 批注变更后调用 — 保存到 localStorage
 */
persistSave() {
  if (!this.dwgFileName) return
  const key = `annotations_${this.dwgFileName}`
  localStorage.setItem(key, JSON.stringify(this.toJSON()))
}
```

### 调用时机

| 事件 | 操作 |
|------|------|
| 打开 DWG 文件后 | `persistLoad(viewer, fileName)` — 从 localStorage 恢复 |
| 添加 / 删除 / 修改批注后 | `persistSave()` — 自动保存 |
| 关闭文件 / 切换文件前 | `persistSave()` 后再 `clearAllTransients()` |
| 页面关闭 (`beforeunload`) | 最后一次 `persistSave()` |

### 调用点位置

1. **打开文件后** — `useWasmModule.js` 的 `openFile` 成功回调中调用 `persistLoad`
2. **批注变更后** — `addAnnotation` / `removeAnnotation` / `setAnnotationStatus` 末尾调用 `persistSave`
3. **关闭文件时** — `closeFile` 中先 `persistSave` 再 `clearAllTransients`

## 导出 / 导入功能（可选）

提供手动导出/导入按钮，方便用户将批注文件分享给其他人：

```javascript
/**
 * 导出为 .json 文件下载
 */
exportAnnotations() {
  const json = JSON.stringify(this.toJSON(), null, 2)
  const blob = new Blob([json], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${this.dwgFileName}_annotations.json`
  a.click()
  URL.revokeObjectURL(url)
}

/**
 * 从文件导入
 */
importAnnotations(viewer, file) {
  const reader = new FileReader()
  reader.onload = (e) => {
    this.loadAnnotations(viewer, e.target.result)
    this.persistSave()
  }
  reader.readAsText(file)
}
```

## JSON 数据格式

`toJSON()` 输出格式：

```json
{
  "version": 1,
  "dwgFileName": "building.dwg",
  "createdAt": "2026-04-17T10:30:00.000Z",
  "annotations": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "type": "cloud_with_arrow_with_text",
      "author": "",
      "status": "open",
      "comment": "此处尺寸标注有误",
      "createdAt": "2026-04-17T10:00:00.000Z",
      "viewState": {
        "centerX": 150.0,
        "centerY": 200.0,
        "fieldWidth": 100.0,
        "fieldHeight": 80.0
      },
      "elements": {
        "cloud": {
          "points": [
            { "x": 100, "y": 160 },
            { "x": 200, "y": 160 },
            { "x": 200, "y": 240 },
            { "x": 100, "y": 240 }
          ],
          "arcLength": 5.0,
          "colorIndex": 1
        },
        "arrow": {
          "from": { "x": 200, "y": 200 },
          "to": { "x": 250, "y": 220 },
          "colorIndex": 1
        },
        "text": {
          "position": { "x": 255, "y": 220 },
          "content": "尺寸标注有误",
          "height": 3.0,
          "colorIndex": 1
        }
      }
    }
  ]
}
```

## 后续升级路径 (方案 C — 服务端)

当需要多人协作或跨设备同步时：

1. 在 `server/index.js` 新增两个 REST 端点：
   - `GET  /api/annotations/:fileName` — 读取
   - `PUT  /api/annotations/:fileName` — 保存
2. `persistLoad` / `persistSave` 改为调用 `fetch` API
3. 服务端将 JSON 存到文件系统或数据库
4. localStorage 可保留为离线缓存层

## 相关文件

| 文件 | 说明 |
|------|------|
| `DrawingWebApp/src/stores/AnnotationStore.js` | 前端批注状态管理 (MobX) |
| `DrawingWebApp/src/hooks/useWasmModule.js` | WASM 加载 & 文件打开入口 |
| `DrawingWebApp/src/services/ViewerService.js` | Viewer 服务封装 |
| `DrawingWeb/CadCore.h` | C++ 瞬态批注 API 声明 |
| `DrawingWeb/CadCoreAnnotation.cpp` | C++ 瞬态批注实现 |
| `DrawingWebApp/docs/specs/2026-04-17-transient-annotation-design.md` | 瞬态批注[[架构设计]]文档 |
