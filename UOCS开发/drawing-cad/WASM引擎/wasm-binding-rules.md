# WASM Emscripten 绑定规律手册

> 本文档记录 drawing-cad 前端调用 ODA WASM API 时必须遵守的绑定规律，  
> 由 P18 阶段原子工具 Bug 排查过程中总结归纳（2026-04-24）。

---

## 重载方法命名规则

Emscripten 绑定 C++ 重载方法时，使用 `class_<T>.function("name", overload_cast<>())` 方式。  
当同一类有多个重载时，绑定器对**第一个重载**保留原名，后续重载追加数字后缀。

### Symbol Table 的 has() 方法

| 表类型 | 重载情况 | JS 调用方式 |
|-------|---------|-----------|
| `OdDbBlockTable` | `has(OdDbObjectId)` + `has(OdString)` 两个重载 | `has(objectId)` / `has1("name")` |
| `OdDbLayerTable` | `has(OdDbObjectId)` + `has(OdString)` 两个重载 | `has(objectId)` / `has1("name")` |
| `OdDbSymbolTable`（基类） | 同上 | `has(objectId)` / `has1("name")` |
| `OdDbDimStyleTable` | 只有 `has(OdString)` 一个重载 | **`has("name")`**（不加数字） |
| `OdDbLinetypeTable` | 只有 `has(OdString)` 一个重载 | **`has("name")`**（不加数字） |

**⚠️ 常见误区**：写 `ltTable.has1("name")` 查询线型，实际绑定是 `has`，调用 `has1` 会抛 `is not a function`。

**判断原则**：查对应的 `drawingweb/Wrappers/plan/Od*TableWrapper.cpp`，数一下 `.function("has", ...)` 出现几次：
- 出现 2 次 → 第二个绑定为 `has1`  
- 出现 1 次 → 只有 `has`（按名称查）

### getAt() 方法

所有 SymbolTable 的 `getAt` 均有 `(OdString name, bool getErase)` 两参数版本。  
**必须传 2 个参数**（第二个参数 `false` = 不含已删除）：

```js
// ✅ 正确
const ltId = ltTable.getAt("DASHED", false)

// ❌ 错误（只传 1 个参数，可能匹配到不同重载或抛错）
const ltId = ltTable.getAt("DASHED")
```

---

## erase() 方法无默认参数

C++ 定义：`OdDbObject::erase(bool doSubErase = true)`

Emscripten 绑定**不保留 C++ 默认参数值**。JS 调用 `obj.erase()` 无参时，  
等同于 `erase(false)`（即 unerase，**取消删除**），而非预期的删除操作。

```js
// ✅ 正确 —— 删除实体
ent.erase(true)

// ❌ 错误 —— 等同于 unerase（取消删除），什么都不发生
ent.erase()
```

绑定文件：`drawingweb/Wrappers/plan/OdDbObjectWrapper.cpp:50`：
```cpp
.function("erase", &OdDbObject::erase)   // 无默认值！
```

---

## OdGePoint3d 构造函数重载

C++ 有两个构造：`(double x, double y, double z)` 和 `(OdGePlanarEnt, OdGePoint2d)`。

**必须传 3 个数值参数**，不得用 spread 展开二元坐标数组：

```js
// ✅ 正确
new Module.OdGePoint3d(x, y, 0)

// ❌ 错误 —— 二元数组展开触发 2参数重载，类型错误
new Module.OdGePoint3d(...[x, y])
```

---

## getObjectIdByHandle 快路径

当已知实体 handle 时，直接用 `getObjectIdByHandle` 比遍历 ModelSpace 快且可靠：

```js
const objId = pDb.getObjectIdByHandle(handle)  // handle: 十六进制字符串（大写）
if (!objId || objId.isNull()) { /* not found */ }
const ent = objId.safeOpenObject(Module.OpenMode.kForWrite)
ent.erase(true)
ent.delete()
```

**注意**：handle 格式为大写十六进制（`"35A0C"`），与 `safeHandle()` 返回格式一致。  
AI 工具调用传入的 handle 直接来自 `create_entities` 返回值，格式相同，无需转换。

---

## OdGeMatrix3d.scaling 重载陷阱

C++ 绑定文件（`OdGeMatrix3dWrapper.cpp`）中有两个同名 `class_function("scaling", ...)`：
1. `scaling(double, OdGePoint3d)` —— 均匀缩放（uniform scale）  
2. `scaling(OdGeScale3d, OdGePoint3d)` —— 非均匀缩放（non-uniform）

**Emscripten 只暴露第一个绑定**（双重声明时后者覆盖但 JS 侧只见一个名字）。

```js
// ✅ 正确 —— WASM 只绑定了此版本，矩阵有效
const mat = Module.OdGeMatrix3d.scaling(2.0, centerPt)   // factor: double

// ❌ 错误 —— OdGeScale3d 虽可构造，传入后矩阵为 NaN，transformBy 静默失败
const scale = new Module.OdGeScale3d(2.0)
const mat = Module.OdGeMatrix3d.scaling(scale, centerPt)  // 返回 NaN 矩阵！
```

**验证命令**（WASM 控制台）：
```js
const c = new Module.OdGePoint3d(350, 350, 0)
const m = Module.OdGeMatrix3d.scaling(2.0, c)
const p = new Module.OdGePoint3d(200, 200, 0)
p.transformBy(m)
// → x=50, y=50 ✅（(200-350)*2+350 = -300+350 = 50）
```

---

## 已验证的原子工具 E2E 结果（2026-04-24）

| 工具 | Bug 修复 | E2E 结果 |
|------|---------|---------|
| `add_aligned_dimension` | `dimTable.has1` → `has` | ✅ 通过 |
| `add_linear_dimension` | `dimTable.has1` → `has` | ✅ 通过 |
| `create_axis_grid` | — | ✅ 通过 |
| `array_rectangular` | — | ✅ 通过 |
| `create_hatch` | `evaluateHatch` 参数修正 | ✅ 通过 |
| `set_layer_properties`（含 linetype） | `ltTable.has1` → `has` | ✅ 通过 |
| `create_entities` + `transform_entities(translate)` | — | ✅ 通过 |
| `delete_entities` | `erase()` → `erase(true)` + handles 快路径 | ✅ 通过 |
| `insert_block_ref` | `has1` → `has` + `getAt(name, false)` | ✅ 通过 |
| `transform_entities(scale)` | 移除 OdGeScale3d（NaN矩阵）+ handles 快路径 | ✅ 通过 |
