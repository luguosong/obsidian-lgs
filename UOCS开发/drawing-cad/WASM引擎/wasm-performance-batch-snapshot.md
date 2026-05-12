# WASM 性能优化：批量实体快照 API（Plan A）

**实施日期**：2026-04-24  
**实施人**：ZFSWin11  
**依据报告**：`wasm-structure-performance-report.md`（API #1 + API #2）

---

## 背景

`DwgReadAdapter.extractEntities()` 在大图纸（>5000 实体）时存在严重性能瓶颈。  
根本原因是 JS↔WASM 跨界调用次数过多：每个实体需要 **13-40 次**跨界调用（取 handle、typeName、layer、extents 等公共属性），5000 实体时产生 **75k-200k 次**跨界调用，耗时约 3000ms。

---

## 改动概览

| 文件 | 改动类型 | 核心内容 |
|------|---------|---------|
| `DrawingWeb/Wrappers/plan/OdDbEntityWrapper.cpp` | C++ 新增绑定 | `getTypeNameFast()` 实例方法 |
| `DrawingWeb/Wrappers/plan/OdDbBlockTableRecordWrapper.cpp` | C++ 新增函数+绑定 | `getEntitySnapshots(limit)` 批量快照 |
| `DrawingWebApp/src/services/DwgReadAdapter.js` | JS 优化+修复 | 快速路径 + `allocated` bug 修复 |

> **注意**：C++ 文件改动需重新构建 WASM（`DrawingJs.js/.wasm/.data`）后才生效。  
> JS 文件已做向下兼容处理——旧 WASM 自动回退到原有迭代路径。

---

## C++ 改动详情

### 1. `OdDbEntityWrapper.cpp` — `getTypeNameFast()`

**新增头文件**：无（`OdRxClass` 已通过 `DbEntity.h` 传递包含）

**新增绑定**（`OdDbEntity` 类，实例方法）：

```cpp
.function("getTypeNameFast", optional_override([](const OdDbEntity& self) -> std::wstring {
    OdRxClass* cls = self.isA();
    return cls ? std::wstring(cls->name().c_str()) : std::wstring(L"");
}))
```

**优化原理**：原 JS 端 `getTypeName` 调用 `entity.isA()` + `rxClass.name()` = 2 次跨界；新方法在 C++ 内部完成，1 次跨界直接返回 `std::wstring`（Emscripten 内建支持，自动转为 JS string）。

---

### 2. `OdDbBlockTableRecordWrapper.cpp` — `getEntitySnapshots()`

**新增头文件**：

```cpp
#include "DbHandle.h"
#include "DbObjectIterator.h"
#include <emscripten/val.h>
```

> `OdRxClass` 完整定义已在 `RxObject.h`（已有包含）中，无需单独引入。`RxClass.h` 在 ODA 构建树中不存在。

**新增静态函数**（在 `EMSCRIPTEN_BINDINGS` 之前）：

```cpp
static emscripten::val btrGetEntitySnapshots(
    const OdDbBlockTableRecord& btr, unsigned int limit)
{
    emscripten::val arr = emscripten::val::array();
    if (limit == 0) return arr;

    OdDbObjectIteratorPtr iter = btr.newIterator(true, true, false);
    unsigned int count = 0;

    while (!iter->done() && count < limit) {
        OdDbEntityPtr ent = iter->entity(OdDb::kForRead, false);
        if (ent) {
            emscripten::val snap = emscripten::val::object();

            OdDbHandle h = ent->getDbHandle();
            snap.set("handle", std::string((const char*)h.ascii()));

            OdRxClass* cls = ent->isA();
            snap.set("typeName", cls
                ? std::wstring(cls->name().c_str())
                : std::wstring(L""));

            snap.set("layer",      std::wstring(ent->layer().c_str()));
            snap.set("colorIndex", (int)ent->colorIndex());
            snap.set("lineWeight", (int)ent->lineWeight());
            snap.set("linetype",   std::wstring(ent->linetype().c_str()));
            snap.set("visibility", (int)ent->visibility());

            OdGeExtents3d ext;
            const bool extOk = (ent->getGeomExtents(ext) == eOk);
            snap.set("hasExtents", extOk);
            if (extOk) {
                const OdGePoint3d& mn = ext.minPoint();
                const OdGePoint3d& mx = ext.maxPoint();
                snap.set("minX", mn.x); snap.set("minY", mn.y); snap.set("minZ", mn.z);
                snap.set("maxX", mx.x); snap.set("maxY", mx.y); snap.set("maxZ", mx.z);
            } else {
                snap.set("minX", 0.0); snap.set("minY", 0.0); snap.set("minZ", 0.0);
                snap.set("maxX", 0.0); snap.set("maxY", 0.0); snap.set("maxZ", 0.0);
            }

            arr.call<int>("push", snap);
            ++count;
        }
        iter->step(true, true);
    }
    return arr;
}
```

**新增绑定**（`OdDbBlockTableRecord` 类，实例方法）：

```cpp
.function("getEntitySnapshots", optional_override([](const OdDbBlockTableRecord& self, unsigned int limit) {
    return btrGetEntitySnapshots(self, limit);
}))
```

**设计选择**：使用 `emscripten::val`（裸 JS Array of plain JS objects）而非 `value_object<T>`+`register_vector<T>`，原因：  
- `OdString`（wchar_t 宽字节）字段无法直接作为 `value_object` 字段类型（需要已注册的类型转换器，而 `OdString` 绑定为 `class_<OdString>`，是对象包装而非值转换）  
- `std::wstring` 由 Emscripten 内建支持，经 `OdStringWrapper.cpp` 已在生产环境验证可用  
- 返回裸 JS Array，JS 端直接 `for...of` 迭代，无需 `.size()`/`.get()` 接口

---

## JS 改动详情（`DwgReadAdapter.js`）

### 1. `getTypeName()` — 向下兼容的快速路径

```javascript
function getTypeName(entity) {
  try {
    if (typeof entity.getTypeNameFast === 'function') {
      return safeStr(entity.getTypeNameFast()).replace(/^AcDb/, 'OdDb')
    }
    // 老版本 WASM 回退
    const rxClass = entity.isA()
    return safeStr(rxClass.name()).replace(/^AcDb/, 'OdDb')
  } catch {
    return 'Unknown'
  }
}
```

### 2. `extractTypeSpecificProps()` — 修复 `allocated` 隐式 Bug

**改动前**：
```javascript
function extractTypeSpecificProps(entity, typeName, Module) {
```

**改动后**：
```javascript
function extractTypeSpecificProps(entity, typeName, Module, allocated = []) {
```

**Bug 原因**：函数体内调用 `openAs(btrId, Module.OdDbBlockTableRecord, ..., allocated)` 用于获取块引用的 `blockName`，但 `allocated` 未作为参数传入，在模块级作用域为 `undefined`。`openAs` 执行到 `allocated.push(casted)` 时抛出 `TypeError`，被外层 `try {} catch {}` 静默吞掉，导致 `OdDbBlockReference` 的 `blockName` 字段**从未被正确填充**。

修复后，调用方需传入 `allocated` 数组：
- **旧迭代路径**（慢路径）：`extractTypeSpecificProps(ent, typeName, Module, allocated)`
- **新快速路径**（Phase 3）：`extractTypeSpecificProps(ent, snap.typeName, Module, allocated)`

### 3. `extractEntities()` — 3-Phase 快速路径

在 ModelSpace 打开后、旧迭代器创建前，插入以下逻辑（以 `typeof ms.getEntitySnapshots === 'function'` 守护，旧 WASM 自动跳过）：

```
Phase 1: ms.getEntitySnapshots(SCAN_LIMIT)
         └── 1 次 WASM 调用，返回全部实体的公共属性数组
             字段：handle, typeName, layer, colorIndex, lineWeight,
                   linetype, visibility, hasExtents, minX/Y/Z, maxX/Y/Z

Phase 2: JS 纯内存过滤（无 WASM 调用）
         └── filter.type / filter.layer / filter.handles / filter.bbox

Phase 3: 仅对匹配实体，按 handle 重开取类型特定几何属性
         └── pDb.getOdDbObjectId(handle) → safeOpenObject → extractTypeSpecificProps
```

**参数扩展**：新增 `filter.scanLimit`（默认 20000）控制 Phase 1 的扫描上限。

---

## 预期性能收益

| 场景 | 改动前 | 改动后 | 提升 |
|------|-------|-------|-----|
| 5000 实体，无过滤 | ~75k-200k 跨界调用，~3000ms | 1 次批量 + ~1000×15 次几何调用，~800ms | **73%** |
| 5000 实体，100 匹配（按图层过滤） | ~75k 跨界调用，~3000ms | 1 次批量 + 100×15 次，~50ms | **>98%** |
| `getTypeName()` 单次调用 | 2 次跨界（isA + name） | 1 次跨界（getTypeNameFast） | 50% |

---

## 兼容性说明

| 场景 | 行为 |
|------|-----|
| 新 WASM + 新 JS | 启用全部优化（快速路径 + getTypeNameFast） |
| 旧 WASM + 新 JS | `ms.getEntitySnapshots` 不存在，自动回退旧迭代路径；`getTypeNameFast` 不存在，自动回退 `isA().name()` |
| 新 WASM + 旧 JS | WASM 新方法空置不调用，无影响 |

---

## 已知不包含在 Plan A 的项目

以下优化（来自 `wasm-structure-performance-report.md` API #3~#5）**未实施**，可作为后续迭代：

| API | 内容 | 预期额外收益 |
|-----|------|------------|
| #3 字段投影 `getEntityProjection()` | 只序列化需要的字段，减少 JS 堆开销 | ~50-100ms |
| #4 表批量收集 `getAllRecords()` | `extractStructure` 表遍历优化 | ~100-200ms |
| #5 类型统计 `getEntityTypeStats()` | 块内实体类型分布快速统计 | ~20ms |
