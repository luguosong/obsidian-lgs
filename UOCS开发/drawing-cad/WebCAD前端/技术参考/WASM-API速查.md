# WASM API 速查

> 来源：`drawing-cad/drawingweb/` C++ Emscripten 绑定。如需完整参考，直接阅读该仓库源码。

## CadCore (App) — `Module.App`

| 方法 | 说明 |
|------|------|
| `getDb()` → `OdDbDatabase*` | 获取当前数据库 |
| `getDevice()` → `OdGsDevice*` | 获取图形设备 |
| `getViewAt0()` → `OdGsView*` | 获取第一个视图 |
| `OpenFile(path)` / `CreateNewFile()` | 打开/创建文件 |
| `ZoomExtents()` / `Zoom(factor)` / `Dolly(dx, dy)` | 视图操作 |
| `ExecuteCommand(cmdStr)` | 执行 [[AutoCAD]] 命令（ASYNCIFY） |
| `ExecuteScript(code)` | 执行 SCR 脚本（ASYNCIFY） |
| `ScreenToWorld(sx, sy)` / `WorldToScreen(wx, wy, wz)` | 坐标转换 |
| `Update()` / `Redraw()` / `regenAll()` | 刷新显示 |
| `GetLayoutNames()` / `SwitchLayout(name)` | 布局切换 |
| `StartCompare(...)` / `ExitCompare()` | 像素级比对 |
| `StartObjectCompare(...)` / `ExitObjectCompare()` | 对象级比对 |
| `GetEntityProperties(handle)` / `SetEntityProperty(handle, prop, val)` | CDA 属性 |

## OdDbDatabase — 数据库核心

| 方法 | 说明 |
|------|------|
| `getBlockTableId()` / `getLayerTableId()` / `getTextStyleTableId()` / `getLinetypeTableId()` / `getDimStyleTableId()` | 获取符号表 ID |
| `getModelSpaceId()` / `getPaperSpaceId()` | 模型空间/图纸空间 |
| `getSysVar(name)` / `setSysVar(name, value)` | 系统变量 |
| `getOdDbObjectId(handle, createIfNotExist, reserved)` | Handle → ObjectId |
| `startUndoRecord()` / `undo()` / `redo()` | 撤销/重做 |
| `writeFile(filename, type, version, saveThumbnail, compressionType)` | 保存文件 |

## OdDbEntity 基类 — 所有图形实体通用

| 方法 | 说明 |
|------|------|
| `color()` / `setColor(color)` / `colorIndex()` / `setColorIndex(idx)` | 颜色 |
| `layer()` / `setLayer(name)` / `layerId()` | 图层 |
| `linetype()` / `setLinetype(name)` / `linetypeScale()` / `setLinetypeScale(s)` | 线型 |
| `lineWeight()` / `setLineWeight(lw)` | 线宽 |
| `transparency()` / `setTransparency(trans)` | 透明度 |
| `visibility()` / `setVisibility(vis)` | 可见性 |
| `transformBy(matrix)` | 几何变换 |
| `getGeomExtents(extents)` | 获取包围盒 |
| `explode(entitySet)` | 分解 |
| `erase(flag)` | 删除 |

## OdDbCurve 基类 — 所有曲线通用

`isClosed()`, `getStartPoint()`, `getEndPoint()`, `getArea()`, `getPointAtParam(param)`, `getPointAtDist(dist)`, `getClosestPointTo(point)`, `getOffsetCurves(dist)`, `reverseCurve()`

## 常用绘图实体方法签名

| 实体 | 关键方法 |
|------|---------|
| `OdDbLine` | `startPoint()` / `setStartPoint(pt)`, `endPoint()` / `setEndPoint(pt)` |
| `OdDbCircle` | `center()` / `setCenter(pt)`, `radius()` / `setRadius(r)` |
| `OdDbArc` | `center/setCenter`, `radius/setRadius`, `startAngle/setStartAngle`, `endAngle/setEndAngle` |
| `OdDbEllipse` | `center/setCenter`, `majorAxis()`, `minorAxis()`, `radiusRatio/setRadiusRatio`, `set(center, unitNormal, majorAxis, radiusRatio, startAngle, endAngle)` |
| `OdDbPolyline` | `addVertexAt(idx, pt2d, bulge, startW, endW, vertexId)`, `numVerts()`, `getPointAt(idx)`, `setPointAt(idx, pt)`, `setClosed(bool)`, `setConstantWidth(w)` |
| `OdDbText` | `position/setPosition`, `textString/setTextString`, `height/setHeight`, `rotation/setRotation`, `textStyle/setTextStyle` |
| `OdDbMText` | `location/setLocation`, `contents/setContents`, `textHeight/setTextHeight`, `width/setWidth`, `attachment/setAttachment`, `text()` 纯文本 |
| `OdDbHatch` | `setPattern(type, name)`, `setPatternScale(s)`, `setHatchStyle(style)`, `appendLoopByIds(type, ids)`, `evaluateHatch()` |
| `OdDbSpline` | `numControlPoints()`, `getControlPointAt/setControlPointAt`, `numFitPoints()`, `getFitPointAt/setFitPointAt`, `degree()` |
| `OdDbBlockReference` | `blockTableRecord/setBlockTableRecord`, `position/setPosition`, `scaleFactors/setScaleFactors`, `rotation/setRotation`, `attributeIterator()` |

## 标注实体

| 实体 | 关键方法 |
|------|---------|
| `OdDbDimension`（基类） | `textPosition/setTextPosition`, `dimensionText/setDimensionText`, `dimensionStyle/setDimensionStyle`, `measurement()`, `recomputeDimBlock()` |
| `OdDbAlignedDimension` | `xLine1Point/setXLine1Point`, `xLine2Point/setXLine2Point`, `dimLinePoint/setDimLinePoint` |
| `OdDbRotatedDimension` | 同 Aligned + `rotation()` / `setRotation(angle)` |
| `OdDbRadialDimension` | `center/setCenter`, `chordPoint/setChordPoint`, `leaderLength/setLeaderLength` |
| `OdDbDiametricDimension` | `chordPoint/setChordPoint`, `farChordPoint/setFarChordPoint`, `leaderLength/setLeaderLength` |
| `OdDb3PointAngularDimension` | `arcPoint/setArcPoint`, `xLine1Point/setXLine1Point`, `xLine2Point/setXLine2Point`, `centerPoint/setCenterPoint` |

## 3D 实体

| 实体 | 关键方法 |
|------|---------|
| `OdDb3dSolid` | `createBox/createSphere/createTorus/createFrustum/createWedge/createPyramid`, `extrude/revolve/extrudeAlongPath`, `booleanOper(type, otherSolid)`, `chamferEdges/filletEdges` |
| `OdDbRegion` | `createFromCurves(curves)` 类方法, `booleanOper(type, other)` |
| `OdDbSurface` | `createFrom/trimSurface/createOffsetSurface/createFilletSurface` 类方法 |
| `OdDbSubDMesh` | `setSphere/setCylinder/setCone/setTorus/setBox`, `subdDivideUp/subdDivideDown` |

## 符号表操作模式

```javascript
// 通用符号表遍历模式（图层/线型/文字样式/标注样式/块均适用）
const tableId = pDb.getLayerTableId()
const table = OdDbLayerTable.cast(tableId.safeOpenObject(OpenMode.kForRead, false))
const iter = table.newIterator()
for (iter.start(); !iter.done(); iter.step()) {
  const rec = OdDbLayerTableRecord.cast(iter.getRecord())
  // rec.getName().toString(), rec.isOff(), rec.isFrozen(), rec.isLocked()
}
```

## 几何类 — 高频

| 类 | 构造 | 关键方法 |
|---|---|---|
| `OdGePoint3d` | `new OdGePoint3d(x, y, z)` | `.x/.y/.z`, `distanceTo(pt)`, `transformBy(mat)`, `asVector()` |
| `OdGePoint2d` | `new OdGePoint2d(x, y)` | `.x/.y`, `distanceTo(pt)` |
| `OdGeVector3d` | `new OdGeVector3d(x, y, z)` | `.x/.y/.z`, `length()`, `normal()`, `dotProduct(v)`, `crossProduct(v)`, `angleTo(v)` |
| `OdGeMatrix3d` | `new OdGeMatrix3d()` | `setToTranslation(vec)`, `setToRotation(angle, axis, center)`, `setToScaling(factor, center)`, `setToMirroring(point/plane)` |
| `OdCmColor` | `new OdCmColor()` | `setRGB(r, g, b)`, `setColorIndex(idx)`, `red()/green()/blue()` |
| `OdCmTransparency` | `new OdCmTransparency(alpha)` | `setAlphaPercent(p)` |

**类属性常量**：`OdGePoint3d.kOrigin`, `OdGeVector3d.kXAxis/kYAxis/kZAxis`, `OdGePlane.kXYPlane`

## 关键枚举值速查

| 枚举 | 常用值 |
|------|--------|
| `OpenMode` | `kForRead`(0), `kForWrite`(1) |
| `LineWeight` | `kLnWt000`(0) → `kLnWt211`(211), `kLnWtByLayer`(-1) |
| `HatchPatternType` | `kPreDefined`(0), `kUserDefined`(1), `kCustomDefined`(2) |
| `HatchStyle` | `kNormal`(0), `kOuter`(1), `kIgnore`(2) |
| `HatchLoopType` | `kExternal`(1), `kPolyline`(2), `kDerived`(4), `kTextbox`(8) |
| `AttachmentPoint` | `kTopLeft`(1) → `kBottomRight`(9) |
| `Visibility` | `kVisible`(0), `kInvisible`(1) |
| `OsnapMode` | `kOsModeEnd`(1), `kOsModeMid`(2), `kOsModeCen`(3), `kOsModeNear`(7) |
| `SaveType` | `kDwg`(0), `kDxf`(1) |

## 集合/数组 — 统一接口

所有数组类型（`OdGePoint3dArray`, `OdGePoint2dArray`, `OdDbObjectIdArray`, `OdIntArray`, `OdGeDoubleArray`, `VectorString` 等）共享：`push_back(item)`, `size()`, `get(index)`, `clear()`, `empty()`, `resize(n)`, `append(otherArray)`

## 全局函数

| 函数 | 说明 |
|------|------|
| `Module.odcmAcadPalette(background)` | 获取 [[AutoCAD]] 调色板 |
| `Module.oddbCreateEdgesFromEntity(entity)` | 从实体创建边缘数组 |
| `Module.oddbAppendLoopFromPickPoint(hatch, x, y)` | 从拾取点添加填充边界环 |
| `Module.createPolarArrayParameters(...)` / `createPathArrayParameters(...)` | 创建阵列参数 |

## 已知兼容性陷阱

- `SetBackgroundColor()` 不存在 → 使用 `appCore.getDevice().setBackgroundColor()` + `device.setLogicalPalette(Module.odcmAcadPalette(bg), 256)`
- `Module` 是 `createViewerClass(Module)` 的闭包参数，不是 `this.Module`
- `OdDbDimStyleTable` / `OdDbLinetypeTable` 未导出 → DwgReadAdapter 中为非致命错误

## 相关笔记

- [[技术参考]]
- [[UacadConfig — 跨平台 CAD 配置持久化方案]]
- [[CadCodeExecutor 沙箱]]
- [[GIS 后端接口参考文档]]
- [[WebUACAD AI Agent 全面分析报告]]
- [[CAD AI Agent 改进计划]]
- [[规划审图 AI 智能体解决方案]]
- [[AI助手功能开发方向]]
