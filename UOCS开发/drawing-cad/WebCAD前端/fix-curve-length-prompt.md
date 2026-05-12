# OdDbPolyline 长度计算错误修复方案

## 问题描述

CAD Agent（LLM）在计算 `OdDbPolyline` 的长度时，生成了 `pline.length` 或 `pline.length()` 调用，运行时报错 **`pline.length is not a function`**。

## 根因分析

### 1. ODA SDK 没有 `length()` 方法

ODA C++ SDK 的 `OdDbCurve` 类（所有曲线实体的基类）**不提供** `length()` 方法。计算曲线长度的标准做法是**参数法**：

```javascript
const endParam = curve.getEndParam();           // 获取终点参数值
const length = curve.getDistAtParam(endParam);  // 参数 → 弧长距离 = 总长度
```

### 2. WASM 绑定层已具备所需方法

`OdDbCurveWrapper.cpp` 中已绑定 `getEndParam()` 和 `getDistAtParam()`，并用 `optional_override` 封装为直接返回 `double` 的便捷形式（无需 C++ 输出参数风格）。

`OdDbPolylineWrapper.cpp` 声明了 `rx_class_<OdDbPolyline, base<OdDbCurve>>`，embind 的 `base<>` 机制使子类实例**自动继承**父类所有已绑定的实例方法。因此 `OdDbPolyline` 实例可以直接调用 `getEndParam()`、`getDistAtParam()` 等，**不需要在子类中重复绑定**。

### 3. 提示词缺失导致 LLM 瞎猜

当前 `CORE_PROMPT`（`server/tools/cadTools.js`）第 10 条规则列出了曲线方法，但：

- 只提到了 `isClosed()`、`isPeriodic()`、`getArea()`
- **完全没有说明如何计算曲线长度**
- 第 1004 行虽提到"对非封闭曲线计算长度"，但未给出代码模式

LLM 于是根据训练知识猜测存在 `.length` 属性/方法，导致运行时错误。

---

## 修改内容

### 修改 1：补充 CORE_PROMPT 曲线长度说明

**文件**：`server/tools/cadTools.js`

**定位**：在 `CORE_PROMPT` 中找到第 10 条规则（约第 512 行），当前内容：

```
10. **曲线方法都在 OdDbCurve 及其子类上**，OdDbEntity 上没有任何曲线方法。曲线类型判断用 `ent.isKindOf(OdDbCurve.desc())`，然后用 `const curve = OdDbCurve.cast(ent)` 转换（cast 可能返回 null，须检查）：
   - 简单属性：`curve.isClosed()` → bool，`curve.isPeriodic()` → bool，`curve.getArea()` → double（失败返回 -1）
   - 修改：`curve.reverseCurve()` → OdResult，`curve.extend(newParam)` → OdResult
```

**修改为**：

```
10. **曲线方法都在 OdDbCurve 及其子类上**，OdDbEntity 上没有任何曲线方法。曲线类型判断用 `ent.isKindOf(OdDbCurve.desc())`，然后用 `const curve = OdDbCurve.cast(ent)` 转换（cast 可能返回 null，须检查）：
   - 简单属性：`curve.isClosed()` → bool，`curve.isPeriodic()` → bool，`curve.getArea()` → double（失败返回 -1）
   - **曲线长度**：ODA 没有 `length()` 方法，必须用参数法计算：`const length = curve.getDistAtParam(curve.getEndParam())`。适用于所有 OdDbCurve 子类（Line、Arc、Circle、Polyline、Spline 等）
   - 修改：`curve.reverseCurve()` → OdResult，`curve.extend(newParam)` → OdResult
```

> **关键**：新增的"曲线长度"条目紧跟在"简单属性"之后，让 LLM 在看到面积计算的同时也能看到长度计算模式。

### 修改 2：在代码示例区补充长度计算典型模式

**文件**：`server/tools/cadTools.js`

**定位**：在 `CORE_PROMPT` 中找到"典型模式 — 统计所有封闭曲线面积"代码块之后（约第 586 行），在其后新增一个长度计算的典型模式：

```
**典型模式 — 计算曲线长度**：
\`\`\`javascript
const curve = OdDbCurve.cast(ent);
if (!curve) return;
const endParam = curve.getEndParam();           // 终点参数
const length = curve.getDistAtParam(endParam);  // 参数 → 弧长 = 总长度
// ⚠️ ODA 没有 length() 方法，必须用 getDistAtParam(getEndParam()) 计算
\`\`\`
```

### 修改 3：添加 RAG 代码示例

**新建文件**：`server/rag/code_examples/query_curve_length.js`

```javascript
// @title: 计算曲线长度（含块内子实体）
// @tags: 长度, length, 曲线, curve, getEndParam, getDistAtParam, OdDbCurve, polyline, line, arc, spline, 统计, 查询
// @api: OdDbCurve, OdDbBlockReference, getEndParam, getDistAtParam, isClosed, forEachEntity, getBlockDefinition, scaleFactors, setResult
// @description: ODA SDK 没有 length() 方法。曲线长度通过参数法计算：先获取终点参数 getEndParam()，再用 getDistAtParam(endParam) 将参数转为弧长距离，即为总长度。适用于所有 OdDbCurve 子类（Line, Arc, Circle, Polyline, Spline 等）。块内曲线的长度需乘以缩放系数。

const results = [];

forEachEntity(modelSpace, (ent, entId) => {
  // 情况1：模型空间直接曲线
  if (ent.isKindOf(OdDbCurve.desc())) {
    const curve = OdDbCurve.cast(ent);
    if (!curve) return;
    const endParam = curve.getEndParam();
    const length = curve.getDistAtParam(endParam);
    results.push({
      handle: ent.handle(),
      type: str(ent.isA().name()),
      layer: str(ent.layer()),
      closed: curve.isClosed(),
      length,
      source: 'modelSpace',
    });
    return;
  }

  // 情况2：块参照内子实体
  if (ent.isKindOf(OdDbBlockReference.desc())) {
    const blockRef = OpenAs(entId, OdDbBlockReference, OpenMode.kForRead);
    if (!blockRef) return;
    const btr = getBlockDefinition(blockRef);
    if (!btr) return;
    const sf = blockRef.scaleFactors();
    const linearScale = Math.abs(sf.sx);

    forEachEntity(btr, (subEnt) => {
      if (!subEnt.isKindOf(OdDbCurve.desc())) return;
      const curve = OdDbCurve.cast(subEnt);
      if (!curve) return;
      const endParam = curve.getEndParam();
      const localLength = curve.getDistAtParam(endParam);
      results.push({
        type: str(subEnt.isA().name()),
        layer: str(subEnt.layer()),
        closed: curve.isClosed(),
        length: localLength * linearScale,
        source: 'block',
      });
    });
  }
});

setResult({ count: results.length, entities: results });
```

### 修改 4：重建 RAG 索引

添加新示例文件后，需要重建索引：

```bash
cd DrawingWebApp/server/rag
python build_index.py --code-source ./code_examples
```

---

## 不需要修改的地方

| 文件 | 原因 |
|------|------|
| `DrawingWeb/Wrappers/plan/OdDbCurveWrapper.cpp` | `getEndParam()`、`getDistAtParam()` 已绑定，无需改动 |
| `DrawingWeb/Wrappers/plan/OdDbPolylineWrapper.cpp` | `base<OdDbCurve>` 继承已生效，注释掉的 `getEndParam` / `getDistAtParam` / `getArea` 等**不需要取消注释**（embind 子类自动继承父类方法） |
| 其他 Wrapper 文件 | 同理，所有继承 `OdDbCurve` 的子类（`OdDbLine`、`OdDbArc`、`OdDbCircle` 等）都不需要单独绑定长度相关方法 |

---

## 验证方法

修改完成后，在 AI 助手中测试以下提问：

1. "计算当前图纸中所有多段线的总长度"
2. "统计 XX 图层上所有线段和多段线的长度"
3. "这条 polyline 有多长？"

确认 LLM 生成的代码使用 `curve.getDistAtParam(curve.getEndParam())` 模式，而非 `.length` / `.length()` / 手动累加顶点距离等错误方式。
