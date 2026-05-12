# Legend Analysis Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the `ent.color()` runtime error and redesign the legend analysis workflow to use programmatic region scanning instead of Vision-guessing for building legend-to-layer mappings.

**Architecture:** Modify `forEachEntity` to auto-cast to `OdDbEntity`, rewrite the System Prompt legend workflow to scan entities within the user-selected region (collecting text + graphic entities with spatial coordinates), and update RAG examples to match.

**Tech Stack:** ODA WASM API (Emscripten), Node.js (AI server), Vercel AI SDK

---

### Task 1: Fix `forEachEntity` to cast to `OdDbEntity`

**Files:**
- Modify: `src/services/CadCodeExecutor.js:314-323`

- [ ] **Step 1: Modify `forEachEntity` to auto-cast**

In `src/services/CadCodeExecutor.js`, replace lines 314-323:

```js
  sandbox.forEachEntity = function (btr, callback) {
    const iter = btr.newIterator(true, true, false)
    allocated.push(iter)
    for (; !iter.done(); iter.step(true, true)) {
      const entId = iter.objectId()
      const ent = entId.safeOpenObject(Module.OpenMode.kForRead, false)
      allocated.push(ent)
      callback(ent, entId)
    }
  }
```

With:

```js
  sandbox.forEachEntity = function (btr, callback) {
    const iter = btr.newIterator(true, true, false)
    allocated.push(iter)
    for (; !iter.done(); iter.step(true, true)) {
      const entId = iter.objectId()
      const obj = entId.safeOpenObject(Module.OpenMode.kForRead, false)
      allocated.push(obj)
      // cast 为 OdDbEntity，使 .color()/.linetype() 等方法可用
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

- [ ] **Step 2: Commit**

```bash
git add src/services/CadCodeExecutor.js
git commit -m "fix: forEachEntity auto-cast to OdDbEntity for color()/linetype() access"
```

---

### Task 2: Update `forEachEntity` documentation in System Prompt

**Files:**
- Modify: `server/tools/cadTools.js:441-450`

- [ ] **Step 1: Update the `forEachEntity` description (line 441)**

Replace:
```
- \`forEachEntity(btr, callback)\` — 遍历块表记录中所有实体。callback 签名：\`(entity, entityId)\`。entity 类型为基类 OdDbObject。可用于 modelSpace 或任意 OdDbBlockTableRecord。
```

With:
```
- \`forEachEntity(btr, callback)\` — 遍历块表记录中所有实体。callback 签名：\`(entity, entityId)\`。entity 已自动 cast 为 OdDbEntity（非 Entity 对象保持 OdDbObject）。可用于 modelSpace 或任意 OdDbBlockTableRecord。
```

- [ ] **Step 2: Update the key note #1 (line 446)**

Replace:
```
1. forEachEntity 回调中的 entity 是 OdDbObject 基类，但 **\`.layer\`、\`.handle\`、\`.isA()\`、\`.color()\`、\`.isKindOf()\` 等基础属性可以直接访问**，无需 OpenAs 转换。
```

With:
```
1. forEachEntity 回调中的 entity 已自动 cast 为 OdDbEntity（非 Entity 对象保持 OdDbObject）。**\`.layer\`、\`.handle\`、\`.isA()\`、\`.color()\`、\`.linetype()\`、\`.isKindOf()\` 等属性均可直接访问**，无需 OpenAs 转换。
```

- [ ] **Step 3: Commit**

```bash
git add server/tools/cadTools.js
git commit -m "docs: update forEachEntity description to reflect auto-cast to OdDbEntity"
```

---

### Task 3: Rewrite Legend Analysis Workflow in System Prompt

**Files:**
- Modify: `server/tools/cadTools.js:556-612`

- [ ] **Step 1: Replace the entire `## 图例分析工作流` section (lines 556-612)**

Replace lines 556-612 with:

```
## 图例分析工作流

当用户要求"根据图例分析图纸"或需要理解图纸中各种元素的语义时，按以下步骤编排。
**核心原则**：程序化扫描图例区域内的实际 CAD 实体，建立确定性映射，不依赖 Vision 猜测颜色。

### 获取图例区域
直接提示用户提供图例区域：
- "请先**缩放到图例区域**，然后点击**区域选择按钮**框选图例范围。"
- 提醒用户确保图例中的**符号和文字标签**都在框选范围内。
**禁止**：不要先调 capture_viewport 截图查看布局，不要调 search_code_examples，直接等用户操作。

### 截图 + 区域内实体扫描（合并为一次回复）
收到用户的区域选择数据后，**在同一条回复中**完成以下两件事：

**A) 调用 capture_viewport 截取当前视图**：
截图发给 Vision，辅助识别图例文字（作为交叉验证，非主要依据）。

**B) 调用 execute_js_code 扫描区域内实体**（isQuery: true）：
用用户交互数据中的 bounds 过滤模型空间实体，将实体分为文字和图形两类。代码模板：
\`\`\`javascript
const bounds = { minX: /*用户区域*/, minY: /*...*/, maxX: /*...*/, maxY: /*...*/ };
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
\`\`\`

### 空间关联 → 生成确定性映射表
收到第二步的扫描结果后：
1. **空间关联**：对每个文字实体，按坐标距离找最近的图形实体（或同一行的图形实体组），建立映射
2. **生成映射表**：文字标签 → { layer, colorIndex, RGB, linetype, entityTypes }
   - Vision 截图识别结果用于交叉验证和补充（例如某些文字是图片/符号而非 Text 实体时）
   - **图层 AND 颜色必须同时满足**才判定为某个图例类型
3. **输出映射表供用户确认**
4. **全图扫描统计**：调用 execute_js_code 遍历整个模型空间（包括块参照内的子实体），使用 isQuery: true
   - 对每个实体检查（图层 AND 颜色）是否匹配映射表中的某个类型
   - 统计每种类型的实体数量
   - 对封闭曲线计算面积（块内实体面积需乘以缩放系数 Math.abs(sf.sx * sf.sy)）
   - 对非封闭曲线计算长度

### 保存分析结果
- 调用 save_analysis 工具，传入 legendMapping、statistics 和 summary
- 分析结果自动保存为 Markdown 文件并注入后续对话上下文

### 失败处理
- 区域内文字实体数量为 0 → 可能图例文字是图片/块，回退到 Vision 截图识别文字
- 程序化扫描的图形实体与文字无法合理关联 → 列出原始数据，请用户确认
- 找不到足够的图例实体 → 提示用户重新框选更大范围
```

- [ ] **Step 2: Commit**

```bash
git add server/tools/cadTools.js
git commit -m "feat: rewrite legend analysis workflow to use programmatic region scanning"
```

---

### Task 4: Update RAG code examples

**Files:**
- Modify: `server/rag/code_examples/query_entity_attributes.js`
- Modify: `server/rag/code_examples/find_similar_entities.js`
- Create: `server/rag/code_examples/scan_legend_region.js`

- [ ] **Step 1: Update `query_entity_attributes.js` comments**

In `server/rag/code_examples/query_entity_attributes.js`, replace line 4:

```
// @description: 使用沙箱预定义的 forEachEntity 遍历模型空间所有实体，提取图层名、颜色、实体类型等基础属性。forEachEntity 回调中的 entity 是 OdDbObject 基类，但 layer、color() 等基础属性可直接访问。
```

With:

```
// @description: 使用沙箱预定义的 forEachEntity 遍历模型空间所有实体，提取图层名、颜色、实体类型等基础属性。forEachEntity 回调中的 entity 已自动 cast 为 OdDbEntity，layer、color()、linetype() 等属性可直接访问。
```

Also replace lines 6-8:

```
// ⚠️ 必须使用沙箱预定义的 forEachEntity，不要自己写 newIterator
// forEachEntity 回调签名：(entity, entityId)
// entity 是 OdDbObject 基类，可直接读取 .layer, .color(), .isA() 等
```

With:

```
// ⚠️ 必须使用沙箱预定义的 forEachEntity，不要自己写 newIterator
// forEachEntity 回调签名：(entity, entityId)
// entity 已自动 cast 为 OdDbEntity，可直接读取 .layer, .color(), .linetype(), .isA() 等
```

- [ ] **Step 2: Update `find_similar_entities.js` comments**

In `server/rag/code_examples/find_similar_entities.js`, replace line 4:

```
// @description: 通过用户选择的样板实体 handle，查找图纸中相同图层和类型的所有实体。注意：forEachEntity 回调中的 ent 是 OdDbObject 基类，但 .layer、.handle、.isA()、.color() 等基础属性可以直接访问，无需 OpenAs 转换。只有调用子类方法（如 isClosed()、getArea()）时才需要 OpenAs。
```

With:

```
// @description: 通过用户选择的样板实体 handle，查找图纸中相同图层和类型的所有实体。注意：forEachEntity 回调中的 ent 已自动 cast 为 OdDbEntity，.layer、.handle、.isA()、.color() 等属性可直接访问，无需 OpenAs 转换。只有调用子类方法（如 isClosed()、getArea()）时才需要 OpenAs。
```

Also replace line 17:

```
// ⚠️ forEachEntity 回调中的 ent 可以直接访问 .layer、.handle、.isA()
```

With:

```
// ⚠️ forEachEntity 回调中的 ent 已自动 cast 为 OdDbEntity，可直接访问 .layer、.handle、.isA()、.color()
```

- [ ] **Step 3: Create `scan_legend_region.js`**

Create new file `server/rag/code_examples/scan_legend_region.js`:

```javascript
// @title: 扫描图例区域内的实体（文字+图形分类）
// @tags: legend, 图例, region, 区域, 扫描, scan, 映射, mapping, 文字, text, 图形, graphic, getGeomExtents, bounds, 分析
// @api: forEachEntity, OdDbText, OdDbMText, OpenAs, getGeomExtents, color, layer, setResult
// @description: 扫描用户框选的图例区域内所有实体，按文字和图形分类收集属性及坐标，用于建立图例含义与图层/颜色的确定性映射。

// bounds 从用户交互数据中获取（区域选择返回的包围盒）
const bounds = { minX: 0, minY: 0, maxX: 200, maxY: 100 };

const texts = [];
const graphics = [];

forEachEntity(modelSpace, (ent, entId) => {
  try {
    const ext = ent.getGeomExtents();
    const cx = (ext.minPoint().x + ext.maxPoint().x) / 2;
    const cy = (ext.minPoint().y + ext.maxPoint().y) / 2;

    // 过滤：仅保留区域内的实体
    if (cx < bounds.minX || cx > bounds.maxX || cy < bounds.minY || cy > bounds.maxY) return;

    const typeName = ent.isA().name();

    if (typeName === 'AcDbText' || typeName === 'AcDbMText') {
      // 文字实体：提取文本内容和位置
      const textEnt = typeName === 'AcDbText'
        ? OpenAs(entId, OdDbText, OpenMode.kForRead)
        : OpenAs(entId, OdDbMText, OpenMode.kForRead);
      if (textEnt) {
        texts.push({ text: textEnt.textString?.() || '', x: cx, y: cy });
      }
    } else {
      // 图形实体：提取图层、颜色、类型和位置
      const color = ent.color();
      graphics.push({
        type: typeName,
        layer: ent.layer,
        colorIndex: color.colorIndex(),
        r: color.red(),
        g: color.green(),
        b: color.blue(),
        x: cx,
        y: cy,
      });
    }
  } catch (_) {}
});

setResult({ texts, graphics });
```

- [ ] **Step 4: Commit**

```bash
git add server/rag/code_examples/query_entity_attributes.js server/rag/code_examples/find_similar_entities.js server/rag/code_examples/scan_legend_region.js
git commit -m "docs: update RAG examples for OdDbEntity auto-cast, add legend region scan example"
```
