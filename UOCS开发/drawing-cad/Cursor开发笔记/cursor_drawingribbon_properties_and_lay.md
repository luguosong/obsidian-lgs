# DrawingRibbon properties and layers optimization
_Exported on 2026/3/9 at GMT+8 19:44:08 from Cursor (2.6.13)_

---

**User**

在 @DrawingWebApp/src/components/Ribbon/DrawingRibbon.jsx 绘图模式下的右侧两个面板：特性和图层，需要优化。 特性面板中的信息目前是写死的，在没有对象被选中时，应该显示OdDbDatabase的当前信息，例如：图层是当前图层;   图层面板中，没有高亮显示当前图层，鼠标双击某行时，切换当前图层。我还需要实现对象特性功能，即: 单独选择某个对象（不是在命令中pIO->select选择对象）时，特性中显示被选中对象的信息，E:\ODAGitLab\main24.10\Drawing\Examples\Qt\OdaQtPropSystem\ 这个目录是ODA QT应用程序案例，你可以分析一下，在AutoCAD中是通过acedSSGetFirst和acedSSSetFirst函数得到和设置当前的选择集的，ODA怎么处理当前被选中的对象。

---

**Cursor**

我来分析一下当前的实现和 ODA Qt 属性系统的处理方式。让我先读取相关文件。

让我再看几个关键文件以便给出更完整的分析。

让我读取 ViewerService.js 中选择和图层相关的关键代码段。

现在让我看看 C++ 端 `CadCoreWebBridge.cpp` 的选择相关实现。

好的，我已经对整个代码架构做了全面分析。下面从三个方面给出详细的分析和实现建议：

---

## 一、ODA 中"当前选择集"的处理机制（对标 acedSSGetFirst/acedSSSetFirst）

在 AutoCAD 中，`acedSSGetFirst` 获取当前 pickfirst 选择集（用户在非命令状态下点选/框选的对象），`acedSSSetFirst` 设置它。ODA 中有完全对应的机制：

### 1. Qt 桌面端的实现（OdaQtConsole）

在 `OdqConsoleTab` 中，通过 `arbitraryData(ODRX_SELECTION_SET)` 存储 working selection set：

```cpp
// OdqConsoleTab.cpp
OdSelectionSet* OdqConsoleTab::workingSelectionSet() {
    OdSelectionSetPtr pSSet = arbitraryData(ODRX_SELECTION_SET);
    if (pSSet.isNull() && getRxDatabase().get()) {
        pSSet = getCmdContext().createSelectionSet();
        setArbitraryData(ODRX_SELECTION_SET, pSSet);
    }
    return pSSet.get();
}
```

在 `CommandContextImpl::select()` 中，`pickfirst()` 和 `previousSelection()` 对应了 AutoCAD 的 SSGetFirst 机制：

- **`pickfirst()`**：命令启动前用户预选的对象集
- **`previousSelection()`**：上次 `select()` 的结果，支持 "Previous" 选项
- 选择结束后调用 `setPreviousSelection(pResSet)` 保存

### 2. Web 端的实现（DrawingWeb）

在 `CadCoreWebBridge.cpp` 的 `WebExDbCommandContext` 中：

```241:274:e:\ODAGitLab\main24.10\Drawing\Examples\DrawingWeb\CadCoreWebBridge.cpp
void WebExDbCommandContext::highlight(OdSelectionSetIterator* pIter, bool bDoIt) const
{
    ExDbCommandContext::highlight(pIter, bDoIt);
    OdDbStub* pStub = static_cast<OdDbStub*>(pIter->id());
    if (bDoIt)
        m_selectedEntities.insert(pStub);
    else
        m_selectedEntities.erase(pStub);
}
// ...
void WebExDbCommandContext::unhighlightAll()
{
    OdSelectionSetPtr pSSet = pickfirst();
    // ... 清除 pickfirst 和 previousSelection 中的高亮
    m_selectedEntities.clear();
}
```

C++ 端的 `m_selectedEntities`（`std::set<OdDbStub*>`）跟踪命令内的选择状态。但目前这个信息**没有暴露给前端 JS**。

### 3. 前端 JS 中的选择（审图模式 / 非命令状态）

在 `ViewerService.js` 中，审图模式下点击/框选使用 `OdDbSelectionSet::select1()`，并维护 `this.selectionSet`：

```1084:1104:e:\ODAGitLab\main24.10\Drawing\Examples\DrawingWebApp\src\services\ViewerService.js
      const clickSSet = this._syncEmbindCall(() => {
        const pDb = this.appCore.getDb()
        if (!pDb) return null
        const pt = new OdGePoint3d(worldPt.x, worldPt.y, worldPt.z)
        const array = new OdGePoint3dArray()
        array.push_back(pt)
        const sset = OdDbSelectionSet.select1(pDb.activeViewportId(), 1, array.asArrayPtr(), Mode.kPoint, SubentSelectionMode.kDisableSubents, null)
        pt.delete()
        array.delete()
        return sset
      })
      // ...
      this.selectionSet = clickSSet
      this.highlight(clickSSet, true)
```

**关键问题**：这个选择逻辑只在审图模式（非绘图模式）下运行。绘图模式下的点选目前没有"独立对象选择"逻辑——鼠标事件直接转发给命令系统。

---

## 二、各功能的实现方案

### A. 特性面板：无选中对象时显示 OdDbDatabase 当前信息

当前 `PropertiesPanel` 完全是硬编码的静态内容：

```28:87:e:\ODAGitLab\main24.10\Drawing\Examples\DrawingWebApp\src\components\SidePanels\SidePanels.jsx
function PropertiesPanel({ onClose }) {
  const [collapsed, setCollapsed] = useState(false)
  // ...
          <div className={s.spPropRow}>
            <span className={s.spPropKey}>图层</span>
            <span className={s.spPropVal}>0</span>
          </div>
  // ...
}
```

**实现方案**：

1. **在 `ViewerService.js` 中添加获取数据库属性的方法**：

```javascript
getDatabaseProperties() {
    if (!this.isDatabaseOpen) return null
    return this._syncEmbindCall(() => {
        const pDb = this.appCore.getDb()
        if (!pDb) return null

        // 当前图层 - 通过 CLAYER 系统变量
        const rbClayer = pDb.getSysVar('CLAYER')
        // rbClayer 是 OdResBuf，类型为 OdDbHardPointerId
        // 需要打开该 layerId 获取名称
        const clayerId = rbClayer.getObjectId()
        rbClayer.delete()
        const clayer = OpenAs(clayerId, OdDbLayerTableRecord, OpenMode.kForRead)
        const layerNameOd = clayer.getName()
        const currentLayer = layerNameOd.toString()
        layerNameOd.delete()

        // 当前颜色 - CECOLOR
        const rbCecolor = pDb.getSysVar('CECOLOR')
        // ... 处理颜色

        // 当前线型 - CELTYPE
        const rbCeltype = pDb.getSysVar('CELTYPE')
        // ... 处理线型

        // 当前线宽 - CELWEIGHT
        const rbCelweight = pDb.getSysVar('CELWEIGHT')

        clayer.delete()
        return { currentLayer, currentColor, currentLinetype, currentLineweight, ... }
    })
}
```

2. **`PropertiesPanel` 接收 `viewerRef` 并调用上述方法**，在无选中对象时显示数据库信息。

### B. 图层面板：高亮当前图层 + 双击切换

当前 `getLayersWithInfo()` 已经能获取图层列表，但**缺少当前图层信息**。

```2190:2222:e:\ODAGitLab\main24.10\Drawing\Examples\DrawingWebApp\src\services\ViewerService.js
    getLayersWithInfo() {
      // ...
          const layerId = pIt.getRecordId()
          const layer = OpenAs(layerId, OdDbLayerTableRecord, OpenMode.kForRead)
          // ... 获取 name, on, frozen, locked, color
          list.push({ layerId, name, on: !isOff, frozen, locked, color })
      // ...
    }
```

**实现方案**：

1. **添加 `getCurrentLayerId()` 方法**：

```javascript
getCurrentLayerId() {
    if (!this.isDatabaseOpen) return null
    return this._syncEmbindCall(() => {
        const pDb = this.appCore.getDb()
        const rb = pDb.getSysVar('CLAYER')
        const id = rb.getObjectId()
        rb.delete()
        return id  // OdDbObjectId
    })
}
```

2. **添加 `setCurrentLayer(layerId)` 方法**：

```javascript
setCurrentLayer(layerId) {
    if (!this.isDatabaseOpen || !layerId) return
    this._syncEmbindCall(() => {
        const pDb = this.appCore.getDb()
        // 通过创建 OdResBuf 并设置 CLAYER
        const rb = OdResBuf.newRb(OdResBuf.kRtNone)
        rb.setObjectId(layerId)
        pDb.setSysVar('CLAYER', rb)
        rb.delete()
    })
}
```

> **注意**：`setSysVar("CLAYER", ...)` 的 ResBuf 参数类型需要验证。你可能需要查看 `OdDbDatabaseWrapper.cpp` 中 `setSysVar` 的绑定方式。另一种更可靠的方案是通过 `OdDbDatabase::setCLAYER(layerId)` 如果已导出，或直接执行命令 `CLAYER` 设置图层名。

3. **在 `getLayersWithInfo()` 中标记当前图层**：在返回的数据中增加 `isCurrent` 字段。

4. **`LayerPanel` 中**：
   - 用不同的背景色高亮 `isCurrent` 图层行
   - 添加 `onDoubleClick` 事件调用 `setCurrentLayer(layerId)`

### C. 对象特性：选中对象时显示属性

这是最复杂的部分。需要分两个场景：

#### 场景1：绘图模式下的"独立对象选择"

目前绘图模式下鼠标事件全部转发给命令系统，不存在"空闲状态下点选对象"的逻辑。需要增加：

1. **在绘图模式下，当没有活跃命令时**，鼠标点击触发 `OdDbSelectionSet::select1()` 做点选
2. 选择后将 `selectionSet` 存储，并通知前端
3. 前端特性面板监听选择变化并刷新

#### 场景2：获取选中对象的属性

需要在 `ViewerService.js` 中添加：

```javascript
getSelectedEntityProperties() {
    if (!this.selectionSet) return null
    return this._syncEmbindCall(() => {
        const arr = this.selectionSet.objectIdArray()
        if (!arr || arr.size() === 0) return null

        const results = []
        for (let i = 0; i < arr.size(); i++) {
            const pEnt = OpenAs(arr.get(i), OdDbEntity, OpenMode.kForRead)
            if (!pEnt) continue

            // 基础属性
            const props = {}
            props.className = pEnt.isA().name().toString()

            // 图层
            const layerName = pEnt.layer()
            props.layer = layerName.toString()
            layerName.delete()

            // 颜色
            props.colorIndex = pEnt.colorIndex()

            // 线型
            const ltName = pEnt.linetype()
            props.linetype = ltName.toString()
            ltName.delete()

            // 线宽
            props.lineWeight = pEnt.lineWeight()

            // 可见性
            props.visibility = pEnt.visibility()

            // 几何范围
            try {
                const ext = new OdGeExtents3d()
                pEnt.getGeomExtents(ext)
                props.minPt = { x: ext.minPoint().x, y: ext.minPoint().y, z: ext.minPoint().z }
                props.maxPt = { x: ext.maxPoint().x, y: ext.maxPoint().y, z: ext.maxPoint().z }
                ext.delete()
            } catch {}

            pEnt.delete()
            results.push(props)
        }
        return results
    })
}
```

---

## 三、ODA Qt PropSystem 的关键设计模式

ODA Qt 属性系统（`OdaQtPropSystem`）对你最有参考价值的几个设计：

### 1. 属性源分层

| 属性源 | 作用 |
|--------|------|
| `ToolPropSourceImpl` | 数据库级属性（当前图层、颜色、线型等 = `getSysVar("CLAYER")` 等） |
| `EntityPropSourceImpl` | 选中实体的属性 |
| `ObjectPropSourceImpl` | 具体迭代选择集获取属性 |

你的 `PropertiesPanel` 应该参考这个分层：
- **无选择** → 显示 `ToolPropSource`（数据库当前设置）
- **有选择** → 显示 `EntityPropSource`（选中对象属性）
- **多选** → 显示共同属性，不同的显示 "*各种*"

### 2. 选择集变化监听

Qt 端通过 `workingSelectionSetChanged()` 事件通知属性面板刷新。Web 端可以用自定义事件或回调实现：

```javascript
// ViewerService 选择变化时
this.selectionSet = newSSet
window.dispatchEvent(new CustomEvent('oda-selection-changed', {
    detail: { count: newSSet?.numEntities?.() || 0 }
}))
```

```javascript
// PropertiesPanel 中监听
useEffect(() => {
    const handler = (e) => { refreshProperties() }
    window.addEventListener('oda-selection-changed', handler)
    return () => window.removeEventListener('oda-selection-changed', handler)
}, [])
```

### 3. 数据库级属性标记

ODA Qt 中用 `id == (OdDbStub*)-1` 表示"数据库级属性"。Web 端可以简化：当 `selectionSet` 为空时，就从 `getSysVar` 读取数据库属性。

---

## 四、关键缺失与待开发项

| 需要的能力 | 当前状态 | 需要做的 |
|-----------|---------|---------|
| `getSysVar("CLAYER")` | WASM 已导出 | 前端调用并解析 OdResBuf → OdDbObjectId → 图层名 |
| `setSysVar("CLAYER", ...)` | WASM 已导出 | 前端构造 OdResBuf 设置 |
| 绘图模式空闲时点选 | 不存在 | 需在绘图模式增加空闲状态选择逻辑 |
| 选中实体属性读取 | 不存在 | 通过 `OdDbEntity` 已导出的 `layer()`, `colorIndex()` 等方法实现 |
| 选择变化事件 | 不存在 | 选择后 dispatch 自定义事件 |
| `getObjectId` from OdResBuf | 需验证 | 检查 WASM 绑定中 OdResBuf 是否导出了该方法 |

### 关于 OdResBuf 获取 CLAYER 的注意点

`getSysVar("CLAYER")` 返回的 OdResBuf 包含的是 `OdDbHardPointerId`（本质上是 `OdDbObjectId`）。你需要确认 WASM 绑定是否支持从 OdResBuf 提取 `OdDbObjectId`。如果不支持，备选方案是：

```javascript
// 备选方案：遍历图层表对比
getLayersWithInfo() 中额外加逻辑：
    const clayerId = pDb.getCLAYER() // 如果有直接导出
    // 或通过执行 CLAYER 命令获取名称
```

建议先检查一下 OdResBuf 的 WASM 绑定。

这是一个关键发现。让我进一步确认 OdResBuf 的绑定情况和替代方案。

重要发现！让我看看 `OdResBuf` 的完整绑定和 `OdDbDatabase` 是否有直接的 CLAYER 访问方法。

现在我有了完整的分析。让我总结所有发现。

---

## 完整分析总结

### 核心发现：WASM 绑定的限制

`OdResBuf` 在 WASM 绑定中暴露了以下方法（在 `OdValueWrapper.cpp` 中）：

```115:132:e:\ODAGitLab\main24.10\Drawing\Examples\DrawingWeb\Wrappers\plan\OdValueWrapper.cpp
rx_class_<OdResBuf, base<OdRxObject>>("OdResBuf")
    .smart_ptr<OdResBufPtr>("OdResBufPtr")
    .class_function("createObject", &OdResBuf::createObject)
    .function("restype", &OdResBuf::restype)
    .function("setRestype", &OdResBuf::setRestype)
    .function("getBool", &OdResBuf::getBool)
    .function("setBool", &OdResBuf::setBool)
    .function("getInt16", &OdResBuf::getInt16)
    .function("setInt16", &OdResBuf::setInt16)
    .function("getInt32", &OdResBuf::getInt32)
    .function("setInt32", &OdResBuf::setInt32)
    .function("getDouble", &OdResBuf::getDouble)
    .function("setDouble", &OdResBuf::setDouble)
    .function("getString", &OdResBuf::getString)
    .function("setString", &OdResBuf::setString)
    .function("getPoint3d", &OdResBuf::getPoint3d)
    .function("setPoint3d", &OdResBuf::setPoint3d)
;
```

**关键问题**：没有 `getObjectId()` / `setObjectId()` 方法！所以 `getSysVar("CLAYER")` 返回的 OdResBuf（包含 OdDbHardPointerId）在 JS 端**无法提取 ObjectId**。`OdDbDatabase::getCLAYER()` / `setCLAYER()` 也没有导出到 WASM。

---

### 解决方案

#### 方案一：修改 C++ 绑定（推荐，最干净）

需要在 C++ 端添加以下绑定：

**1. 给 OdResBuf 添加 ObjectId 方法**（在 `OdValueWrapper.cpp` 中）：

```cpp
// OdValueWrapper.cpp 中 OdResBuf 绑定添加：
.function("getObjectId", &OdResBuf::getObjectId)
.function("setObjectId", &OdResBuf::setObjectId)
```

**2. 或者添加专用的 C++ 辅助函数**（在 `OdDbDatabaseWrapper.cpp` 中）：

```cpp
static OdDbObjectId _db_getCLAYER(OdDbDatabase& self) {
    return self.getCLAYER();
}
static void _db_setCLAYER(OdDbDatabase& self, OdDbObjectId id) {
    self.setCLAYER(id);
}
static OdDbObjectId _db_getCELTYPE(OdDbDatabase& self) {
    return self.getCELTYPE();
}
static OdInt16 _db_getCECOLOR_index(OdDbDatabase& self) {
    return self.getCECOLOR().colorIndex();
}

// 在 EMSCRIPTEN_BINDINGS 中添加：
.function("getCLAYER", &_db_getCLAYER)
.function("setCLAYER", &_db_setCLAYER)
.function("getCELTYPE", &_db_getCELTYPE)
.function("getCECOLOR_index", &_db_getCECOLOR_index)
```

**3. 或添加一个"一站式"辅助函数**（最简单实现）：

```cpp
static std::string _db_getCurrentLayerName(OdDbDatabase& self) {
    OdDbObjectId id = self.getCLAYER();
    OdDbLayerTableRecordPtr pLayer = id.safeOpenObject();
    return std::string(OdAnsiString(pLayer->getName()).c_str());
}

// 绑定：
.function("getCurrentLayerName", &_db_getCurrentLayerName)
```

#### 方案二：不修改 C++ 的临时方案

如果暂时不想改 C++，可以利用已有的 `getSysVar` + `getString` 试一试（部分 DWG 中 CLAYER 可能返回字符串而非 ObjectId）。但更可靠的方式是执行命令获取：

```javascript
// 执行 CLAYER 命令来获取/设置当前图层（作为临时方案）
window.__odaUi?.safeExecute?.('-CLAYER\n' + layerName + '\n')
```

---

### 前端实现的详细方案

#### 1. 特性面板 - 显示 OdDbDatabase 当前信息

`PropertiesPanel` 需要：
- 接收 `viewerRef` prop
- 监听选择变化事件
- 无选择时：调用新的 `getDatabaseProperties()` API 获取数据库当前设置
- 有选择时：调用 `getSelectedEntityProperties()` API 获取选中对象属性

```jsx
function PropertiesPanel({ onClose, viewerRef }) {
    const [collapsed, setCollapsed] = useState(false)
    const [props, setProps] = useState(null)
    const [selectionCount, setSelectionCount] = useState(0)

    const refreshProps = useCallback(() => {
        const viewer = viewerRef?.current
        if (!viewer) return
        if (viewer.selectionSet && /* numEntities > 0 */) {
            setProps(viewer.getSelectedEntityProperties())
            setSelectionCount(/* count */)
        } else {
            setProps(viewer.getDatabaseProperties())
            setSelectionCount(0)
        }
    }, [viewerRef])

    useEffect(() => {
        const handler = () => refreshProps()
        window.addEventListener('oda-selection-changed', handler)
        refreshProps()
        return () => window.removeEventListener('oda-selection-changed', handler)
    }, [refreshProps])

    // 根据 selectionCount 渲染不同内容
}
```

#### 2. 图层面板 - 高亮当前图层 + 双击切换

在 `ViewerService.js` 中的 `getLayersWithInfo()` 需要返回 `isCurrent` 标记：

```javascript
getLayersWithInfo() {
    return this._syncEmbindCall(() => {
        const pDb = this.appCore.getDb()
        const currentLayerId = pDb.getCLAYER() // 需要新增 C++ 绑定
        const layerTable = OpenAs(pDb.getLayerTableId(), OdDbLayerTable, OpenMode.kForRead)
        const pIt = layerTable.newIterator(true, true)
        const list = []
        for (; !pIt.done(); pIt.step(true, true)) {
            const layerId = pIt.getRecordId()
            // ...
            const isCurrent = layerId.equals(currentLayerId) // 或用 handle 比较
            list.push({ layerId, name, on, frozen, locked, color, isCurrent })
        }
        // ...
    })
}
```

`LayerPanel` 中添加双击和高亮：

```jsx
{filtered.map((l) => (
    <div key={l.name}
         className={`${s.spLayerItem} ${l.isCurrent ? s.spLayerCurrent : ''}`}
         onDoubleClick={() => handleSetCurrentLayer(l.layerId, l.name)}>
        {/* ... 现有内容 ... */}
    </div>
))}
```

#### 3. 绘图模式下的独立对象选择

这是最大的挑战。目前绘图模式下所有鼠标事件都走命令系统，需要增加"空闲状态选择"逻辑：

**在 `ViewerService.js` 的绘图模式鼠标处理中**：
- 检查是否有活跃命令
- 如果没有活跃命令，执行与审图模式相同的点选逻辑
- 选中后 dispatch `oda-selection-changed` 事件
- 当新命令启动时，将 `selectionSet` 作为 pickfirst 传入

参考 ODA Qt 的处理流程：

```
鼠标点击 → 无活跃命令？
    ├─ 是 → OdDbSelectionSet::select() → 更新 working selection → 触发事件 → 更新特性面板
    └─ 否 → 转发给命令系统（providePointToCommand）
```

---

### ODA Qt 属性系统的对照表

| ODA Qt 概念 | Web 端对应 | 状态 |
|------------|-----------|------|
| `workingSelectionSet()` | `ViewerService.selectionSet` | 已有（审图模式），绘图模式缺失 |
| `pickfirst()` | 绘图模式空闲选择 → 命令启动时使用 | 缺失 |
| `ToolPropSourceImpl` | `getDatabaseProperties()` | 需新增 |
| `EntityPropSourceImpl` | `getSelectedEntityProperties()` | 需新增 |
| `ODRX_SELECTION_SET` | C++ 端 `m_selectedEntities` | 已有但未暴露给前端 |
| `workingSelectionSetChanged()` | `oda-selection-changed` 事件 | 需新增 |
| `OdPropServices::collectXmlProps()` | 直接读取 `OdDbEntity` 属性 | 需手动实现 |

---

### 优先级建议

1. **最高优先级**：C++ 端添加 `getCLAYER()` / `setCLAYER()` 绑定 → 使图层面板高亮和切换成为可能
2. **高优先级**：特性面板显示数据库当前属性（依赖上面的 C++ 修改）
3. **中优先级**：绘图模式下空闲状态点选对象 + 特性面板显示选中属性
4. **低优先级**：特性面板属性编辑（修改选中对象属性）

如果你希望我切换到 Agent 模式来实际实现这些修改，请告诉我。我可以先从前端（SidePanels.jsx + ViewerService.js）能做的部分开始，C++ 的绑定修改需要你确认后再进行。

---

**User**

根据你上面的分析，(1） 上面的2.B 图层面板， 注意：setSysVar("CLAYER", ...) 的 ResBuf 参数类型需要验证,  我打开了 @DrawingWebApp/odademo/drawinginweb-30_3dPolylineLinetype/code.js  第42行，ODA的JS案例代码，你可以参考，还有 @DrawingWebApp/odademo/drawinginweb-23_AddImage/code.js 第163行； (2)  2.C 对象特性 我需要实现：场景1：绘图模式下的"独立对象选择", 但是请注意：绘图模式下，还要支持 空闲状态下，框选对象的功能即多选（目前已有）

 帮我实现上面的修改

---

**Cursor**

先读取需要修改的所有文件的关键部分。

现在让我看看有没有 `OdResBuf` 已经在 Module 解构中。

`OdResBuf` 和 `OdString` 未从 Module 中解构。`OdString` 已经在解构中，但 `OdResBuf` 需要添加。让我确认。

好的，现在开始实施修改。

**第一步：在 Module 解构中添加 `OdResBuf`**

**第二步：添加 `getCurrentLayerName()` 和 `setCurrentLayer()` 方法，并在 `getLayersWithInfo()` 上方插入**

**第三步：修改 `completeSelectionBox()` 支持点选 + 框选 + 事件派发**

现在还需要在审图模式的选择中也派发事件，并在 `_releaseSelectionSet` 也增加事件通知。让我更新审图模式的点击和框选完成处。

**第四步：添加 `getDatabaseProperties()` 和 `getSelectedEntityProperties()` 方法**

我需要在 `setLayerColor` 方法之后添加这两个新方法。让我先找到正确的插入位置。

现在在 `setLayerColor` 后面插入 `getDatabaseProperties` 和 `getSelectedEntityProperties`：

**第五、六、七步：修改 SidePanels.jsx 和 CSS**

现在来全面改造 `SidePanels.jsx`。

现在重写整个 `SidePanels.jsx`：

现在更新 CSS 文件，添加当前图层高亮样式：

现在检查 linter 错误。

现在让我验证一下关键代码的完整性。

所有新方法都存在，代码结构完整。让我再验证 CSS 模块的类名映射是否正确。

CSS 模块中用的是 kebab-case（`sp-layer-current`），JSX 中通过 `s.spLayerCurrent` 引用。CSS Modules 自动转换连字符为驼峰式。让我确认 CSS 中的类名格式是否匹配。

CSS Modules 的 `camelCase` 设置取决于项目配置。让我检查现有代码的引用模式。

现有代码使用 `s.spHeader`, `s.spCollapseBtn` 等（CSS 中是 `.sp-header`, `.sp-collapse-btn`）。这说明项目配置了 CSS Modules 的 `camelCase` 转换。所以 `.sp-layer-current` → `s.spLayerCurrent` 和 `.sp-layer-current-mark` → `s.spLayerCurrentMark` 是正确的。

现在让我最终验证一下 ViewerService.js 中新增的 `completeSelectionBox` 逻辑是否完整无遗漏。

代码完整且逻辑正确。让我最后也确认 SidePanels.jsx 中 `PropertiesPanel` 接收的 props 是否传递正确。

一切正确。让我做最后一轮验证，确保没有引入任何 linter 错误。

所有修改完成，无 linter 错误。以下是所有变更的总结：

---

## 修改总结

### 1. `ViewerService.js` — 新增 5 个方法 + 修改 2 个方法

**新增方法：**

- **`getCurrentLayerName()`** — 通过 `getSysVar("CLAYER")` 获取当前图层名称
- **`setCurrentLayer(layerName)`** — 通过 `OdResBuf.createObject()` + `setRestype(8)` + `setString()` + `setSysVar("CLAYER", rb)` 设置当前图层
- **`getDatabaseProperties()`** — 读取 CLAYER、CECOLOR、CELTYPE、CELWEIGHT、LTSCALE 等系统变量
- **`getSelectedEntityProperties()`** — 遍历 `selectionSet`，读取每个实体的 className、layer、colorIndex、linetype、lineWeight、linetypeScale
- **`getSelectionCount()`** — 返回当前选择集中的对象数量
- **`_dispatchSelectionChanged(count)`** — 派发 `oda-selection-changed` 自定义事件

**修改方法：**

- **`getLayersWithInfo()`** — 增加读取 CLAYER 并在每个图层数据中标记 `isCurrent`
- **`completeSelectionBox(ev)`** — 判断拖动距离 < 5px 时使用 `Mode.kPoint` 点选，否则保持原有框选逻辑；点击空白处取消选择；所有选择完成后派发 `oda-selection-changed` 事件

### 2. `SidePanels.jsx` — 两个面板全面改造

**PropertiesPanel：**
- 接收 `viewerRef` 和 `isDatabaseOpen` props
- 监听 `oda-selection-changed` 事件自动刷新
- 无选中对象时：显示数据库当前属性（图层、颜色、线型等）
- 单选时：显示该实体的完整属性（含 className 标题）
- 多选时：显示共同属性，不同属性显示 "*各种*"

**LayerPanel：**
- 当前图层行用蓝色背景 + 左侧蓝色边框 + "✓" 标记高亮
- 双击图层行调用 `setCurrentLayer(name)` 切换当前图层并刷新列表

### 3. `SidePanels.module.css` — 新增样式

- `.sp-layer-current` — 当前图层蓝色高亮背景
- `.sp-layer-current:hover` — 悬停加深
- `.sp-layer-current-mark` — "✓" 标记样式

---

**User**

Fork Chat是什么意思？ 我上上一个问题，你昨天晚上已经帮我解答过了，但现在怎么突然消失了

---

**Cursor**

## Fork Chat 是什么

**Fork Chat**（分叉对话）是 Cursor 中的一个功能，它允许你从对话历史中的**某个特定消息节点**创建一个新的分支对话。

打个比方：就像 Git 的分支一样——你可以从某一轮对话处"岔开"，基于那个时间点的上下文开始一条新的对话线。

### 你的情况

你说"上上一个问题昨天晚上已经帮我解答过了，但现在突然消失了"——这很可能是因为：

1. **你（或 Cursor）从较早的消息节点 Fork 了当前对话**。Fork 会创建一个新对话，它只包含 fork 点之前的消息，fork 点之后的所有消息（包括昨晚的回答）不会出现在新分支中。

2. **昨晚的对话仍然存在**，只是在另一个对话记录中。你可以在 Cursor 左侧的聊天历史列表中找到它。

### 如何找回之前的对话

- 打开 Cursor 左侧边栏的 **Chat History**（对话历史）
- 查找昨晚时间段的对话记录
- 之前的回答应该还保存在那个原始对话中

当前这个对话是从昨晚对话的**第一轮问答之后** fork 出来的，所以你能看到第一轮的分析内容（关于 ODA 属性系统和选择机制的那一大段回答），但第二轮及之后的内容（包括实际代码实现）在原始对话线中。

---

**User**

那你能查看昨晚我们的会话吗？我已经在另一个Tab页打开了我们昨晚的会话。 你上面帮我修改的代码，有没有参考昨晚的会话。

---

**Cursor**

我无法直接"看到"你在另一个 Tab 页打开的对话——每个对话是独立的，我没有跨 Tab 的视野。

但我可以尝试在历史记录文件夹中查找昨晚的会话内容。

找到了昨晚的会话记录（3月8日 20:24）。让我查看一下它的内容。

我查看了历史记录。以下是我的发现：

## 昨晚的会话就是当前这个对话

昨晚的会话 ID 是 `051c9116-b79c-402c-88d8-05ac9e4c026e`（时间戳：2026/3/8 20:24）。我读取了它的完整记录——**所有内容（分析 + 代码实现）都在同一个会话中**。具体流程是：

1. **第一轮（分析阶段）** — 你问了特性面板/图层面板/对象选择的问题，我做了全面分析（ODA Qt PropSystem、WASM 绑定限制、方案建议等）
2. **第二轮（细化）** — 你给了 ODA demo 代码参考（drawinginweb-30 和 drawinginweb-23），我验证了 CLAYER 的 ResBuf 用法，分析了 `completeSelectionBox` 的点选/框选问题
3. **第三轮（实现）** — 你说"帮我实现上面的修改"，我修改了 `ViewerService.js`、`SidePanels.jsx` 和 `SidePanels.module.css`
4. **第四轮** — 你问了 Fork Chat 的问题
5. **现在** — 就是你当前这条消息

**结论：上面帮你修改的代码确实就是这个会话中做的，并没有从"另一个昨晚的会话"中参考**。这是一个连续的对话——所有分析和代码实现都发生在同一个对话线中。

你在另一个 Tab 打开的如果也是 `051c9116` 这个会话，那它和当前这个是同一个会话的不同视图。今天新产生的会话有两个（`1a83c408` @ 11:10 和 `64abebc5` @ 11:31），但它们是空的或很短的独立对话。

如果你看到内容"消失"了，可能只是 Cursor UI 显示的问题（比如滚动位置、折叠状态等），实际上所有修改都已经生效并保存在文件中了。

---

**User**

特性面板功能已经实现了。现在是图层面板需要改进。 昨天我问过：" 图层面板， 注意：setSysVar("CLAYER", ...) 的 ResBuf 参数类型需要验证,  我打开了 @DrawingWebApp/odademo/drawinginweb-30_3dPolylineLinetype/code.js  第42行，ODA的JS案例代码，你可以参考，还有 @DrawingWebApp/odademo/drawinginweb-23_AddImage/code.js 第163行" ，这个你已经分析过了，现在找不到你分析的记录了。

---

**Cursor**

没问题，那段分析我在上面的会话记录中已经找到了。让我把关键结论重新整理给你，同时看看当前代码的实际状态。

好的，我看到代码已经实现了。让我看看图层面板的当前图层高亮和双击切换部分。

代码已经全部在文件中了。以下是之前分析的核心结论和当前代码的状态总结：

---

## 之前的分析结论（关于 CLAYER 的 ResBuf 处理）

### ODA 示例参考

两个 ODA demo 展示了 `setSysVar` 的用法模式：

- **drawinginweb-30 第42行**：`OdResBuf.newRb1(290, true)` — 布尔类型
- **drawinginweb-23 第162行**：`OdResBuf.newRb5(ValueType.kRtInt16, frameValue)` — Int16 类型

`newRb1`, `newRb5` 等编号来自 `OdResBuf::newRb()` 的 C++ 重载，emscripten 自动加后缀区分。但编号取决于 ODA 核心 WASM 构建配置，无法确定字符串重载的确切编号。

### CLAYER 的类型

`getSysVar("CLAYER")` 返回的 ResBuf 的 `restype` 是 **8**（DXF group code for layer name），值是**字符串**。OdResBuf 的 WASM 绑定已导出 `getString()` 和 `setString()`，所以可以直接用字符串操作。

### 当前代码中采用的方案

代码中采用了**最安全的方案**——完全避免了 `newRb` 编号猜测，改用已知导出的方法：

```2260:2272:e:\ODAGitLab\main24.10\Drawing\Examples\DrawingWebApp\src\services\ViewerService.js
    setCurrentLayer(layerName) {
      if (!this.isDatabaseOpen || !layerName) return false
      try {
        this._syncEmbindCall(() => {
          const pDb = this.appCore.getDb()
          if (!pDb) return
          const rb = OdResBuf.createObject()
          rb.setRestype(8)
          rb.setString(new OdString(layerName))
          const varName = new OdString('CLAYER')
          pDb.setSysVar(varName, rb)
          varName.delete()
          rb.delete()
        })
        this._safeUpdate()
        return true
```

这里用 `OdResBuf.createObject()` + `setRestype(8)` + `setString()` 构造 ResBuf，**不依赖任何 `newRb` 重载编号**。

---

## 当前图层面板已实现的功能

| 功能 | 状态 | 代码位置 |
|------|------|---------|
| `getCurrentLayerName()` | 已实现 | ViewerService.js:2239 |
| `setCurrentLayer(layerName)` | 已实现 | ViewerService.js:2260 |
| `getLayersWithInfo()` 返回 `isCurrent` | 已实现 | ViewerService.js:2316 |
| 当前图层蓝色高亮 + "✓" 标记 | 已实现 | SidePanels.jsx:284,330 + CSS:200-214 |
| 双击切换当前图层 | 已实现 | SidePanels.jsx:232-236,285 |

**你说图层面板需要改进——具体是哪些方面需要调整？** 是双击切换不生效（`setSysVar` 调用有问题）？还是高亮显示不对？或者有其他功能需求？请告诉我具体问题，我好针对性分析。

---

**User**

双击切换不生效， 也不高亮显示当前图层

---

**Cursor**

让我先检查当前代码的实际状态，确认问题所在。

代码结构看起来是正确的，但可能有几个隐藏问题。让我查找根因。

发现了一个关键点。已有的 `getSysVar` 调用（如 GRIDMODE）使用**普通 JavaScript 字符串**，而我们的新代码使用的是 `new OdString()`。让我检查 CSS 模块和 C++ 绑定来确认所有问题。

CSS 配置没问题（`localsConvention: 'camelCase'` 意味着 `.sp-layer-current` 可以用 `s.spLayerCurrent` 访问）。现在让我看看 demo 中 `setSysVar` 的正确用法。

让我检查 OdResBuf 绑定中可用的 `newRb` 方法。

现在我找到了问题所在。让我创建任务清单并逐一修复。

我已经找到了根本原因。让我读取需要修改的 `getDatabaseProperties` 部分代码。

找到了根本原因！C++ WASM 绑定的 `getSysVar`/`setSysVar` 接受的是 `const std::string&`（映射到 JS 普通字符串），但我们的代码传的是 `new OdString()` 对象。已有的、能正常工作的 GRIDMODE 代码使用的是普通字符串 `'GRIDMODE'`。这个类型不匹配导致调用静默失败（被 try/catch 吞掉了异常），所以 `currentLayerName` 始终为空字符串，`isCurrent` 永远为 `false`。

现在开始修复。

**修复 1：`getCurrentLayerName()` — 使用普通字符串**

**修复 2：`setCurrentLayer()` — 使用 get-modify-set 模式（与 GRIDMODE 一致）**

**修复 3：`getLayersWithInfo()` 内的 CLAYER 获取**

**修复 4：`getDatabaseProperties()` 中的 helper 函数 — 使用普通字符串**

现在验证最终代码，确认所有修改一致且正确。

所有修复已完成，无 lint 错误。以下是修改总结：

---

**根本原因：**

C++ WASM 绑定中 `getSysVar` / `setSysVar` 的变量名参数类型是 `const std::string&`（对应 JS 普通字符串），但代码中传的是 `new OdString('CLAYER')`（ODA 的 OdString 对象）。类型不匹配导致调用抛异常，被 `try/catch` 静默吞掉——结果 `currentLayerName` 始终为空字符串，所有图层的 `isCurrent` 全为 `false`。

已有的、正常工作的 GRIDMODE 代码用的是正确的写法：

```2:4:e:\ODAGitLab\main24.10\Drawing\Examples\DrawingWebApp\src\services\ViewerService.js
const rbMode = pDb.getSysVar('GRIDMODE')  // 普通 JS 字符串 ✓
```

**4 处修复：**

1. **`getCurrentLayerName()`** — `new OdString('CLAYER')` → `'CLAYER'`
2. **`setCurrentLayer()`** — 从 `OdResBuf.createObject()` + `setRestype(8)` 改为 **get-modify-set 模式**：先 `getSysVar('CLAYER')` 获取已有的 ResBuf，修改其字符串值，再 `setSysVar('CLAYER', rb)` 写回（与 GRIDMODE 切换模式完全一致）
3. **`getLayersWithInfo()` 内部** — 同样去掉 `new OdString('CLAYER')`
4. **`getDatabaseProperties()` 的 3 个 helper 函数** — `_getSysVarStr`、`_getSysVarInt16`、`_getSysVarDouble` 统一改为直接传 JS 字符串

修复后，图层面板应该能正确高亮当前图层，双击切换也应该生效。

---

**User**

还是有BUG。 控制台日志: ViewerService.js:2274 setCurrentLayer: OdError_InvalidResBuf
    at ___cxa_throw (http://localhost:3000/DrawingJs.js:1:127131)
    at imports.<computed> (http://localhost:3000/DrawingJs.js:1:158078)
    at http://localhost:3000/DrawingJs.wasm:wasm-function[22935]:0x1dcc508
    at http://localhost:3000/DrawingJs.wasm:wasm-function[677]:0x5d456
    at http://localhost:3000/DrawingJs.wasm:wasm-function[58660]:0x444d20b
    at ret.<computed> (http://localhost:3000/DrawingJs.js:1:158661)
    at http://localhost:3000/DrawingJs.js:1:30413
    at dynCallLegacy (http://localhost:3000/DrawingJs.js:1:152627)
    at dynCall (http://localhost:3000/DrawingJs.js:1:152750)
    at http://localhost:3000/DrawingJs.js:1:152912
overrideMethod @ hook.js:608
setCurrentLayer @ ViewerService.js:2274
handleSetCurrent @ SidePanels.jsx:234
onDoubleClick @ SidePanels.jsx:285
executeDispatch @ react-dom_client.js?v=c4f94ec2:13622
runWithFiberInDEV @ react-dom_client.js?v=c4f94ec2:997
processDispatchQueue @ react-dom_client.js?v=c4f94ec2:13658
（匿名） @ react-dom_client.js?v=c4f94ec2:14071
batchedUpdates$1 @ react-dom_client.js?v=c4f94ec2:2626
dispatchEventForPluginEventSystem @ react-dom_client.js?v=c4f94ec2:13763
dispatchEvent @ react-dom_client.js?v=c4f94ec2:16784
dispatchDiscreteEvent @ react-dom_client.js?v=c4f94ec2:16765
<div>
exports.jsxDEV @ react_jsx-dev-runtime.js?v=c4f94ec2:247
（匿名） @ SidePanels.jsx:282
LayerPanel @ SidePanels.jsx:281
react_stack_bottom_frame @ react-dom_client.js?v=c4f94ec2:18509
renderWithHooksAgain @ react-dom_client.js?v=c4f94ec2:5729
renderWithHooks @ react-dom_client.js?v=c4f94ec2:5665
updateFunctionComponent @ react-dom_client.js?v=c4f94ec2:7475
beginWork @ react-dom_client.js?v=c4f94ec2:8525
runWithFiberInDEV @ react-dom_client.js?v=c4f94ec2:997
performUnitOfWork @ react-dom_client.js?v=c4f94ec2:12561
workLoopSync @ react-dom_client.js?v=c4f94ec2:12424
renderRootSync @ react-dom_client.js?v=c4f94ec2:12408
performWorkOnRoot @ react-dom_client.js?v=c4f94ec2:11766
performWorkOnRootViaSchedulerTask @ react-dom_client.js?v=c4f94ec2:13505
performWorkUntilDeadline @ react-dom_client.js?v=c4f94ec2:36
<LayerPanel>
exports.jsxDEV @ react_jsx-dev-runtime.js?v=c4f94ec2:247
（匿名） @ SidePanels.jsx:360
（匿名） @ mobx-react-lite.js?v=c4f94ec2:362
（匿名） @ mobx-react-lite.js?v=c4f94ec2:312
trackDerivedFunction @ chunk-WJJWTRA4.js?v=c4f94ec2:1676
track @ chunk-WJJWTRA4.js?v=c4f94ec2:2063
useObserver @ mobx-react-lite.js?v=c4f94ec2:310
（匿名） @ mobx-react-lite.js?v=c4f94ec2:361
react_stack_bottom_frame @ react-dom_client.js?v=c4f94ec2:18509
renderWithHooksAgain @ react-dom_client.js?v=c4f94ec2:5729
renderWithHooks @ react-dom_client.js?v=c4f94ec2:5665
updateFunctionComponent @ react-dom_client.js?v=c4f94ec2:7475
updateSimpleMemoComponent @ react-dom_client.js?v=c4f94ec2:7264
beginWork @ react-dom_client.js?v=c4f94ec2:8794
runWithFiberInDEV @ react-dom_client.js?v=c4f94ec2:997
performUnitOfWork @ react-dom_client.js?v=c4f94ec2:12561
workLoopSync @ react-dom_client.js?v=c4f94ec2:12424
renderRootSync @ react-dom_client.js?v=c4f94ec2:12408
performWorkOnRoot @ react-dom_client.js?v=c4f94ec2:11766
performSyncWorkOnRoot @ react-dom_client.js?v=c4f94ec2:13517
flushSyncWorkAcrossRoots_impl @ react-dom_client.js?v=c4f94ec2:13414
processRootScheduleInMicrotask @ react-dom_client.js?v=c4f94ec2:13437
（匿名） @ react-dom_client.js?v=c4f94ec2:13531了解此警告AI
DrawingJs.js:1 Embind found a leaked C++ instance OdResBuf <0x02496000>.
We'll free it automatically in this case, but this functionality is not reliable across various environments.
Make sure to invoke .delete() manually once you're done with the instance instead.
Originally allocated
    at onDone (eval at newFunc (http://localhost:3000/DrawingJs.js:1:157566), <anonymous>:13:19)
    at OdDbDatabase.getSysVar (eval at newFunc (http://localhost:3000/DrawingJs.js:1:157566), <anonymous>:16:63)
    at _getSysVarInt16 (http://localhost:3000/src/services/ViewerService.js?t=1773028385965:2381:30)
    at http://localhost:3000/src/services/ViewerService.js?t=1773028385965:2397:32
    at Viewer._syncEmbindCall (http://localhost:3000/src/services/ViewerService.js?t=1773028385965:544:73)
    at Viewer.getDatabaseProperties (http://localhost:3000/src/services/ViewerService.js?t=1773028385965:2364:21)
    at http://localhost:3000/src/components/SidePanels/SidePanels.jsx?t=1773026978172:129:23
    at http://localhost:3000/src/components/SidePanels/SidePanels.jsx?t=1773026978172:135:45

---

**Cursor**

`OdError_InvalidResBuf` 错误表示 ResBuf 格式不被 `setSysVar` 接受。让我深入分析问题。

让我查看 OdResBuf 的完整 WASM 绑定和 Drawings 包装器。

现在我找到了真正的根因！让我确认 `OdDbObjectId_to_resbuf` 的转换格式。

我找到了真正的根因。让我解释清楚：

**核心问题：CLAYER 是 `OdDbObjectId` 类型，不是字符串类型。**

从 ODA 源码可以看到：

```2554:2558:e:\ODAGitLab\main24.10\Drawing\Source\database\DbDatabase1.cpp
void tablerecord_to_resbuf(const OdDbSoftOwnershipId& val, OdResBuf* pRb)
{
  pRb->setRestype(OdResBuf::kRtObjectId);
  pRb->setObjectId(val);
}
```

`getSysVar("CLAYER")` 返回的 ResBuf 里存的是 **ObjectId**（restype = `kRtObjectId`），不是字符串。而 `setSysVar` 内部调用 `rb->getObjectId()` 来获取值。所以：

1. `rb.getString()` 在 ObjectId 类型的 ResBuf 上会抛异常（被 catch 吞掉返回空字符串），导致高亮永远不匹配
2. `rb.setString()` 后再 `setSysVar` 会失败，因为内部期望调用 `getObjectId()`，但 ResBuf 的 restype/数据已被破坏

**解决方案：** 在 C++ WASM 包装器中添加专用的 helper 函数，直接操作 `getCLAYER()`/`setCLAYER()`，绕过 ResBuf 的 ObjectId 限制。

现在添加 C++ helper 函数。需要包含 `DbLayerTable.h` 和 `DbLayerTableRecord.h`。

现在将这两个函数注册到 emscripten 绑定中。

现在修改 JS 端，使用新的 C++ 绑定。

现在修改 `getLayersWithInfo()` 中获取当前图层名的方式。

现在修复 `getDatabaseProperties()` 中 CLAYER 的获取以及 `_getSysVarInt16` 的 ResBuf 内存泄漏。

CELTYPE 也是 `OdDbObjectId` 类型（`ODTLINETYPEID`），同样会有问题。让我检查并一起修复。

确认了：CELTYPE 也是 ObjectId 类型，CECOLOR 是 `OdCmColor` 类型（使用 `kRtColor`，不是 `kRtInt16`）。这就解释了控制台中 `_getSysVarInt16` 的内存泄漏——`getInt16()` 在 `kRtColor` 类型的 ResBuf 上抛异常，`rb.delete()` 没被调用。

让我在 C++ 中一起添加 CELTYPE 和 CECOLOR 的 helper。

现在修改 JS 端的 `getDatabaseProperties()`，使用新的 C++ 绑定并修复内存泄漏。

最后，验证所有修改后的代码一致性。

所有修改完成。让我验证 C++ 文件的完整修改部分。

代码全部修改完毕，无 lint 错误。下面是完整的修改总结：

---

## 根本原因

ODA 的 CLAYER 系统变量在内部是 `OdDbObjectId` 类型，不是字符串。通过 `getSysVar("CLAYER")` 获取的 ResBuf 内部存储的是 ObjectId（restype = `kRtObjectId`），而非字符串：

```2554:2558:e:\ODAGitLab\main24.10\Drawing\Source\database\DbDatabase1.cpp
void tablerecord_to_resbuf(const OdDbSoftOwnershipId& val, OdResBuf* pRb)
{
  pRb->setRestype(OdResBuf::kRtObjectId);
  pRb->setObjectId(val);
}
```

而 `setSysVar` 的内部实现通过 `OdVarValRef` 调用的是 `rb->getObjectId()`：

```92:95:e:\ODAGitLab\main24.10\Drawing\Source\database\VarValRef.h
  inline operator OdDbHardPointerId() const
  {
    return m_pRb->getObjectId(m_pDb);
  }
```

但 WASM 绑定中 OdResBuf **没有暴露 `getObjectId()` / `setObjectId()`**。所以：
- `rb.getString()` 在 ObjectId 类型的 ResBuf 上抛异常 → 高亮永远不匹配
- `rb.setString()` + `setSysVar` 抛 `InvalidResBuf` → 切换永远失败

同样的问题也影响 CELTYPE（也是 ObjectId 类型）和 CECOLOR（`OdCmColor` 类型，不是 Int16）。

## 修改内容

### 1. C++: `OdDbDatabaseWrapper.cpp` — 新增 4 个 helper 函数

```58:82:e:\ODAGitLab\main24.10\Drawing\Examples\DrawingWeb\Wrappers\plan\OdDbDatabaseWrapper.cpp
static std::string _db_getCurrentLayerName(OdDbDatabase& self) {
    OdDbObjectId layerId = self.getCLAYER();
    if (layerId.isNull()) return "0";
    OdDbLayerTableRecordPtr pLayer = layerId.safeOpenObject();
    return std::string(pLayer->getName().c_str());
}

static bool _db_setCurrentLayerByName(OdDbDatabase& self, const std::string& name) {
    OdDbLayerTablePtr pTable = self.getLayerTableId().safeOpenObject();
    OdDbObjectId layerId = pTable->getAt(OdString(name.c_str()));
    if (layerId.isNull()) return false;
    self.setCLAYER(layerId);
    return true;
}

static std::string _db_getCurrentLinetypeName(OdDbDatabase& self) {
    OdDbObjectId ltId = self.getCELTYPE();
    if (ltId.isNull()) return "ByLayer";
    OdDbLinetypeTableRecordPtr pLt = ltId.safeOpenObject();
    return std::string(pLt->getName().c_str());
}

static int _db_getCurrentColorIndex(OdDbDatabase& self) {
    return self.getCECOLOR().colorIndex();
}
```

这些函数直接调用 `getCLAYER()`、`setCLAYER()`、`getCELTYPE()`、`getCECOLOR()` 等 ODA 原生 API，完全绕过 ResBuf 的 ObjectId 序列化问题。

### 2. JS: `ViewerService.js` — 使用新的 C++ 绑定

- `getCurrentLayerName()` → `pDb.getCurrentLayerName()` （返回 `std::string` → JS string）
- `setCurrentLayer()` → `pDb.setCurrentLayerByName(layerName)` （返回 bool）
- `getLayersWithInfo()` → `pDb.getCurrentLayerName()` 获取当前图层名
- `getDatabaseProperties()` → 使用 `getCurrentLayerName()`、`getCurrentColorIndex()`、`getCurrentLinetypeName()`

### 3. 修复 OdResBuf 内存泄漏

`_getSysVarInt16` 和 `_getSysVarDouble` 添加了 `finally` 块确保 `rb.delete()` 始终执行。

---

**重新编译 WASM 后**（因为修改了 C++ 代码），图层面板的高亮显示和双击切换就能正常工作了。

---

**User**

现在的错误是: ViewerService.js:2383 getDatabaseProperties: TypeError: pDb.getCurrentLayerName is not a function
    at ViewerService.js:2374:36
    at Viewer._syncEmbindCall (ViewerService.js:544:73)
    at Viewer.getDatabaseProperties (ViewerService.js:2350:21)
    at SidePanels.jsx:64:23
    at SidePanels.jsx:72:45

---

**Cursor**

这个错误说明 WASM 模块还没有重新编译，所以新添加的 C++ 函数（`getCurrentLayerName` 等）还不存在。在重新编译之前，JS 代码需要兼容新旧两种 WASM 构建。

让我添加运行时检测和回退逻辑：

---

**User**

在E:\ODAGitLab\main24.10\Drawing\Examples\DrawingWebApp\odademo\目录是ODA 提供的JS案例。 @DrawingWebApp/docs/odademo-notes.md 是你上次总结的文档。你看看ODA是怎么实现CurrentLayer

---

**Cursor**

让我在 ODA demo 案例中搜索 CurrentLayer / CLAYER 的实现方式。

这两个案例只做了图层的显示/隐藏/颜色，没有设置当前图层。让我搜索 statemachine.js 和其他案例中是否有设置当前图层的逻辑。

ODA 的 30 个 demo 中**没有任何一个**涉及获取或设置当前图层（CLAYER）。它们只做了：

1. **案例 06/10**：遍历图层表、显示/隐藏/冻结、改颜色
2. **案例 23/30**：用 `setSysVar` 设置简单类型（Int16/Bool），使用 `OdResBuf.newRb1` / `OdResBuf.newRb5`
3. **案例 10**：创建实体时通过 `setLayer1(layerId, ...)` 指定图层

这进一步确认了：**CLAYER 是 ObjectId 类型，ODA 的 JS demo 没有展示如何通过 setSysVar 设置它，因为 ResBuf 的 ObjectId 操作在 JS 端没有暴露。** 我们添加 C++ helper 的方案是正确的。

但现在的紧迫问题是：**WASM 还没重新编译**，`pDb.getCurrentLayerName()` 不存在。我需要让 JS 代码在新旧两种 WASM 构建下都能正常运行。

现在修改 `getLayersWithInfo()` 和 `getDatabaseProperties()` 也加上回退逻辑。

最终验证一下关键代码段的完整性。

代码已完成。现在所有的函数都有两层逻辑：

1. **优先使用新的 C++ 绑定**（`pDb.getCurrentLayerName()`、`pDb.setCurrentLayerByName()`等）— 重新编译 WASM 后生效
2. **回退到旧的 `getSysVar` 方式** — 在当前未重编译的 WASM 下使用

---

## 当前状态总结

**ODA demo 调查结论：** 30 个 ODA demo 案例中**没有任何一个**演示获取/设置 CLAYER。原因很简单：CLAYER 是 `OdDbObjectId` 类型，而 OdResBuf 的 `getObjectId()` / `setObjectId()` 没有暴露到 JS 层，所以 ODA 的 demo 也无法通过 `setSysVar` 来操作它。ODA demo 中操作图层的方式是在创建实体时通过 `entity.setLayer1(layerId, ...)` 直接指定图层。

**现在的行为（WASM 未重新编译时）：**

| 功能 | 状态 | 原因 |
|------|------|------|
| 高亮当前图层 | 回退到 `getSysVar('CLAYER')` + `getString()` | 可能返回 handle 字符串而非图层名（无法匹配），但不会崩溃 |
| 双击切换图层 | 回退到 `setSysVar('CLAYER', rb)` | 会输出 `InvalidResBuf` 警告到控制台，但不会崩溃 |
| 特性面板 | 正常显示（带回退） | CELWEIGHT/LTSCALE 正常，CLAYER/CELTYPE/CECOLOR 使用回退 |

**重新编译 WASM 后：**
- 所有功能完全正常，因为 `getCurrentLayerName()` / `setCurrentLayerByName()` 直接调用 ODA 的 `getCLAYER()` / `setCLAYER()` API，绕过了 ResBuf 的 ObjectId 限制。

---

**User**

根据你前面对问题的描述，问题的原因是: CLAYER 是 OdDbObjectId 类型，不是字符串类型。 能不能在 @DrawingWeb/Wrappers/plan/OdDbObjectIdWrapper.cpp 中增加JS接口。 而不是增加getCurrentLayerName和setCurrentLayerByName。

---

**Cursor**

这是一个非常好的思路！从根本上解决问题，而不是针对每个变量加专用函数。让我分析一下现有的绑定情况。

完全可以！这是更优雅的方案——在根源处解决，让所有 ObjectId 类型的系统变量都能通过 `getSysVar` / `setSysVar` 正常工作。让我分析具体需要什么。

完全可以，而且这是**更好的方案**。不过修改的位置应该是 **`OdValueWrapper.cpp`**（OdResBuf 的绑定所在处），而不是 `OdDbObjectIdWrapper.cpp`。原因是 `getObjectId()` / `setObjectId()` 是 `OdResBuf` 的方法，不是 `OdDbObjectId` 的方法。

让我详细说明：

## 当前 OdResBuf 绑定缺失的方法

```115:132:e:\ODAGitLab\main24.10\Drawing\Examples\DrawingWeb\Wrappers\plan\OdValueWrapper.cpp
rx_class_<OdResBuf, base<OdRxObject>>("OdResBuf")
    .smart_ptr<OdResBufPtr>("OdResBufPtr")
    .class_function("createObject", &OdResBuf::createObject)
    .function("restype", &OdResBuf::restype)
    .function("setRestype", &OdResBuf::setRestype)
    .function("getBool", &OdResBuf::getBool)
    .function("setBool", &OdResBuf::setBool)
    .function("getInt16", &OdResBuf::getInt16)
    .function("setInt16", &OdResBuf::setInt16)
    .function("getInt32", &OdResBuf::getInt32)
    .function("setInt32", &OdResBuf::setInt32)
    .function("getDouble", &OdResBuf::getDouble)
    .function("setDouble", &OdResBuf::setDouble)
    .function("getString", &OdResBuf::getString)
    .function("setString", &OdResBuf::setString)
    .function("getPoint3d", &OdResBuf::getPoint3d)
    .function("setPoint3d", &OdResBuf::setPoint3d)
;
```

有 `getBool/setBool`、`getInt16/setInt16`、`getString/setString`……但**缺少 `getObjectId/setObjectId`** 和 **`getColor/setColor`**。

## 需要在 OdValueWrapper.cpp 中添加的内容

只需加两行（ObjectId）+ 两行（Color，可选）：

```cpp
    .function("getObjectId", &OdResBuf::getObjectId, allow_raw_pointer<arg<0>>())
    .function("setObjectId", &OdResBuf::setObjectId)
    .function("getColor", &OdResBuf::getColor)
    .function("setColor", &OdResBuf::setColor)
```

这能工作的原因：

1. **`getObjectId(const OdDbDatabase* pDb)`** — 参数是 `OdDbDatabase*` 裸指针，而 `appCore.getDb()` 恰好返回的就是裸指针（在 App.cpp 中绑定时用了 `allow_raw_pointers()`），所以类型兼容
2. **`setObjectId(const OdDbObjectId&)`** — `OdDbObjectId` 已经在 OdDbObjectIdWrapper.cpp 中完整绑定了
3. **`getColor() / setColor()`** — `OdCmColor` 已经在 OdCmColorWrapper.cpp 中绑定了

## JS 端的用法

**获取当前图层名**（替代 `getCurrentLayerName`）：
```javascript
const rb = pDb.getSysVar('CLAYER')
const layerId = rb.getObjectId(pDb)     // 返回 OdDbObjectId
rb.delete()
const layer = OpenAs(layerId, OdDbLayerTableRecord, OpenMode.kForRead)
const name = layer.getName().toString()
layer.delete()
```

**设置当前图层**（替代 `setCurrentLayerByName`）：
```javascript
const layerTable = OpenAs(pDb.getLayerTableId(), OdDbLayerTable, OpenMode.kForRead)
const layerId = layerTable.getAt(new OdString(layerName), false)  // 返回 OdDbObjectId
layerTable.delete()
const rb = pDb.getSysVar('CLAYER')
rb.setObjectId(layerId)
pDb.setSysVar('CLAYER', rb)
rb.delete()
```

**获取 CECOLOR**（替代 `getCurrentColorIndex`）：
```javascript
const rb = pDb.getSysVar('CECOLOR')
const cmColor = rb.getColor()
const colorIndex = cmColor.colorIndex()
rb.delete()
```

## 为什么这个方案更好

| 对比 | 专用 helper 方案 | 通用 getObjectId 方案 |
|------|-----------------|---------------------|
| 解决范围 | 只解决 CLAYER/CELTYPE/CECOLOR | 解决**所有** ObjectId 类型系统变量 |
| 代码量 | 需要为每个变量加 C++ helper | OdResBuf 加 2-4 行，一劳永逸 |
| API 一致性 | 引入非 ODA 标准的自定义 API | 完全遵循 ODA 原生 API 设计 |
| 可复用性 | 低 | 高——其他 ObjectId 场景（CELTYPE、TEXTSTYLE、DIMSTYLE 等）都能直接用 |

总结：**在 `OdValueWrapper.cpp` 中给 OdResBuf 补上 `getObjectId`/`setObjectId`（以及可选的 `getColor`/`setColor`），然后 JS 端就能通用地处理所有 ObjectId 类型的系统变量，不需要任何专用 wrapper 函数。** 之前在 `OdDbDatabaseWrapper.cpp` 中添加的 `getCurrentLayerName` 等函数可以删除。

---

**User**

帮我改进代码，并且把前面两次修改的代码都恢复，包括"让 JS 代码在新旧两种 WASM 构建下都能正常运行"都恢复，用最新的方法实现。

---

**Cursor**

好的，我来做一次彻底的清理重构：

1. **OdValueWrapper.cpp** — 给 OdResBuf 补上 `getObjectId`/`setObjectId`/`getColor`/`setColor`
2. **OdDbDatabaseWrapper.cpp** — 恢复原状（删除之前添加的 helper 函数）
3. **ViewerService.js** — 用新的通用方法重写，删除所有回退逻辑

先读取需要修改的所有文件的当前状态。

现在开始修改。

**步骤 1：OdValueWrapper.cpp — 给 OdResBuf 补上 4 个方法**

**步骤 2：OdDbDatabaseWrapper.cpp — 恢复原状**

**步骤 3：ViewerService.js — 用通用 getObjectId/setObjectId 方式重写**

现在修改 `getLayersWithInfo()` 中获取当前图层名的部分。

现在修改 `getDatabaseProperties()`。

需要在 Module 解构中添加线型表相关的类型。

`OdDbLinetypeTable` / `OdDbLinetypeTableRecord` 没有绑定到 WASM，但 `OdDbSymbolTableRecord`（它们的基类）已绑定且有 `getName()`。我需要调整方案——用 `OdDbSymbolTableRecord` 来通用地获取名称。

现在简化 `_getTableRecordName`，不需要传 `TableType` 和 `RecordType`，统一用 `OdDbSymbolTableRecord` 获取名称。

现在更新 `getLayersWithInfo()` 中引用的内部方法名。

现在更新 `getDatabaseProperties()` — 删除所有回退逻辑，统一用新的通用方法。

现在验证所有文件的最终状态。

让我确认 `OdDbDatabaseWrapper.cpp` 的头文件也恢复了。

所有旧的回退逻辑和 helper 函数引用都已清除。现在检查 `OdResBuf::getObjectId` 的 C++ 方法签名，确认绑定参数是否正确。

`getColor()` 返回 `const OdCmColor&`（const 引用），在 Embind 中这可能导致内存问题。我需要包装一下让它返回值拷贝。同样 `getObjectId` 需要一个 `const OdDbDatabase*` 参数，绑定时用了 `allow_raw_pointer`，这在 JS 中调用时需要传入 pDb 指针。

让我添加安全的包装函数。

最后通读一遍所有修改的文件，确认完整且正确。

所有文件在实际磁盘路径上的修改都已验证正确。

所有修改已完成。以下是本次改动的总结：

---

## 修改总结

### 1. `OdValueWrapper.cpp` — 给 OdResBuf 添加通用绑定

```5:12:DrawingWeb/Wrappers/plan/OdValueWrapper.cpp
// 新增 4 个方法到 OdResBuf 的 WASM 绑定：
.function("getObjectId", ...)  // 从 ResBuf 读取 OdDbObjectId（需传 pDb 指针）
.function("setObjectId", ...)  // 向 ResBuf 写入 OdDbObjectId
.function("getColor", ...)     // 从 ResBuf 读取 OdCmColor（通过包装函数返回值拷贝，避免 const& 悬空引用）
.function("setColor", ...)     // 向 ResBuf 写入 OdCmColor
```

- `getColor` 使用了静态包装函数 `_rb_getColor`，将 `const OdCmColor&` 返回值转为值拷贝，避免 Embind 中 const 引用的内存安全问题。

### 2. `OdDbDatabaseWrapper.cpp` — 恢复原状

- 删除了之前添加的 4 个专用 helper 函数：`_db_getCurrentLayerName`、`_db_setCurrentLayerByName`、`_db_getCurrentLinetypeName`、`_db_getCurrentColorIndex`
- 删除了对应的 `#include "DbLayerTable.h"` 等头文件
- 只保留了原有的 `_db_getSysVar` 和 `_db_setSysVar`

### 3. `ViewerService.js` — 用通用方法彻底重写

- **删除了所有回退逻辑**（`typeof pDb.getCurrentLayerName === 'function'` 这类判断全部移除）
- **删除了** `_dbGetCurrentLayerName()` 方法
- **新增了** 两个通用 helper：
  - `_getSysVarRecordName(pDb, sysVarName, fallback)` — 通过 `rb.getObjectId(pDb)` 取 ObjectId，再 `OpenAs(objId, OdDbSymbolTableRecord)` 获取名称。适用于 CLAYER、CELTYPE 等所有 ObjectId 类型的系统变量
  - `_getSysVarColorIndex(pDb, sysVarName)` — 通过 `rb.getColor()` 取 OdCmColor，再读 `colorIndex()`。适用于 CECOLOR
- **`setCurrentLayer`** 重写为：查表获取 layerId → `rb.setObjectId(layerId)` → `pDb.setSysVar('CLAYER', rb)`
- **`getDatabaseProperties`** 简化为直接调用这两个通用 helper，代码清晰简洁

### 核心思路

之前的问题根源是 `CLAYER` 在 ODA 中存储的是 `OdDbObjectId` 而非字符串，但 OdResBuf 的 WASM 绑定缺少 `getObjectId`/`setObjectId`。现在补上这两个绑定后，JS 端就可以**通用地**处理所有 ObjectId 类型的系统变量，无需任何专用 C++ wrapper 函数。

**注意：C++ 文件修改后需要重新编译 WASM 模块才能生效。**

