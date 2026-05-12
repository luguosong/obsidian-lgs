# Legend Analysis Redesign: Programmatic Region Scan + Vision

> Date: 2026-04-08
> Status: Approved

## Problem

The current "analyze DWG based on legend" workflow has two critical issues:

1. **`ent.color()` runtime error** — `forEachEntity` callback returns `OdDbObject`, which doesn't have `color()` bound in Emscripten. The system prompt and RAG examples claim it works, but it crashes at runtime with `TypeError: ent.color is not a function`.

2. **Non-deterministic mapping** — Vision reads the legend image to identify text labels and colors visually, then the LLM "guesses" which (layer, color) combination corresponds to each label by color similarity. This has no programmatic guarantee.

## Solution

Replace the Vision-guessing approach with **programmatic region scanning**: scan the actual CAD entities within the user-selected legend region, extract their precise layer/color/linetype attributes and spatial coordinates, then correlate with nearby text entities to build a deterministic mapping.

## Design

### Change 1: Fix `forEachEntity` to return `OdDbEntity`

**File**: `src/services/CadCodeExecutor.js` (lines 314-323)

Modify `forEachEntity` to automatically `cast` opened objects to `OdDbEntity` via `Module.OdDbEntity.cast(obj)`. This makes `.color()`, `.linetype()`, and other `OdDbEntity` methods directly accessible in the callback. Non-Entity objects (e.g., Dictionary) fall back to `OdDbObject`.

```js
sandbox.forEachEntity = function (btr, callback) {
  const iter = btr.newIterator(true, true, false)
  allocated.push(iter)
  for (; !iter.done(); iter.step(true, true)) {
    const entId = iter.objectId()
    const obj = entId.safeOpenObject(Module.OpenMode.kForRead, false)
    allocated.push(obj)
    const ent = Module.OdDbEntity.cast(obj)
    if (ent) {
      allocated.push(ent)
      callback(ent, entId)
    } else {
      callback(obj, entId)
    }
  }
}
```

### Change 2: Rewrite Legend Analysis Workflow in System Prompt

**File**: `server/tools/cadTools.js` (lines 556-612, the `## 图例分析工作流` section)

Replace the current 4-step workflow with:

**Step 1: Get legend region**
- Prompt user to zoom to legend area and use area selection button to select the region.

**Step 2: Screenshot + programmatic scan (in one reply)**

A) Call `capture_viewport` to screenshot the current view → Vision reads text labels with approximate positions.

B) Call `execute_js_code` (isQuery: true) to scan entities within the selected region bounds:
- Filter entities by `getGeomExtents()` center point within bounds
- Separate into two categories:
  - **Text entities** (`AcDbText` / `AcDbMText`): collect text content + center coordinates
  - **Graphic entities** (everything else): collect layer, color (RGB + colorIndex), linetype, entity type, center coordinates

Code template:
```javascript
const bounds = { minX: /*...*/, minY: /*...*/, maxX: /*...*/, maxY: /*...*/ };
const texts = [];
const graphics = [];
forEachEntity(modelSpace, (ent, entId) => {
  try {
    const ext = ent.getGeomExtents();
    const cx = (ext.minPoint().x + ext.maxPoint().x) / 2;
    const cy = (ext.minPoint().y + ext.maxPoint().y) / 2;
    if (cx < bounds.minX || cx > bounds.maxX || cy < bounds.minY || cy > bounds.maxY) return;
    const typeName = ent.isA().name();
    if (typeName === 'AcDbText' || typeName === 'AcDbMText') {
      const textEnt = typeName === 'AcDbText'
        ? OpenAs(entId, OdDbText, OpenMode.kForRead)
        : OpenAs(entId, OdDbMText, OpenMode.kForRead);
      if (textEnt) texts.push({ text: textEnt.textString?.() || '', x: cx, y: cy });
    } else {
      const color = ent.color();
      graphics.push({
        type: typeName, layer: ent.layer,
        colorIndex: color.colorIndex(), r: color.red(), g: color.green(), b: color.blue(),
        x: cx, y: cy,
      });
    }
  } catch (_) {}
});
setResult({ texts, graphics });
```

**Step 3: Spatial correlation → deterministic mapping**
- For each text entity, find the nearest graphic entity (or group of graphic entities on the same row)
- Build mapping: text label → {layer, color, linetype, entityTypes}
- Vision results serve as cross-validation
- Output mapping table for user confirmation

**Step 4: Full drawing scan + save**
- Use the mapping table to traverse the entire drawing (including block references), matching by layer AND color
- Call `save_analysis` to persist results

### Change 3: Update `forEachEntity` documentation in System Prompt

**File**: `server/tools/cadTools.js` (line 446)

Update the description to reflect that `forEachEntity` now auto-casts to `OdDbEntity`:

> `forEachEntity 回调中的 entity 已自动 cast 为 OdDbEntity（非 Entity 对象保持 OdDbObject）。.layer、.color()、.linetype()、.handle、.isA() 等属性均可直接访问。只有子类特有方法（如 isClosed()、getArea()）才需要 OpenAs 转换。`

### Change 4: Update RAG examples

**File**: `server/rag/code_examples/query_entity_attributes.js`
- Update comments: "entity 是 OdDbObject 基类" → "entity 是 OdDbEntity（由 forEachEntity 自动 cast）"

**File**: `server/rag/code_examples/find_similar_entities.js`
- Same comment update

**New file**: `server/rag/code_examples/scan_legend_region.js`
- Contains the region scan code template from Step 2 above
- Tagged for RAG retrieval: legend, 图例, region, 区域扫描, 映射

### Files NOT changed

| File | Reason |
|------|--------|
| `AiAssistant.jsx` | Area selection, screenshot, interaction data injection already work |
| `analysisTools.js` | No new tools needed |
| `AnalysisStore.js` | Data structure unchanged, `save_analysis` interface unchanged |

## Summary of changes

| File | Change |
|------|--------|
| `src/services/CadCodeExecutor.js` | Fix `forEachEntity` to cast to `OdDbEntity` |
| `server/tools/cadTools.js` | Rewrite legend workflow + update forEachEntity docs + update code template |
| `server/rag/code_examples/query_entity_attributes.js` | Update comments |
| `server/rag/code_examples/find_similar_entities.js` | Update comments |
| `server/rag/code_examples/scan_legend_region.js` | **New**: legend region scan example |
