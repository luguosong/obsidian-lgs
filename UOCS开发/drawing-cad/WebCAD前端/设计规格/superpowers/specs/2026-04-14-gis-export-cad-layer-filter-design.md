# DWG 导出 GIS 按 CAD 图层过滤 — 设计文档

**日期**: 2026-04-14
**分支**: [[feat-zfs]]

## 背景

当前 `ExportGisModal` 里的"选择图层"Checkbox 列的是 `gisStore.featureLayers`（GIS 侧导入的 MapServer 要素图层），与"要导出哪些 CAD 图层"完全无关。即便用户勾选，`Cmd_GIS_EXPORT` 也只读取 `format` 和 `path`，第三个参数被静默丢弃；`ConvertDWGToGIS` 始终遍历整个 ModelSpace 全量输出。

目标：让用户在导出时按 CAD [[图层过滤]]，只导出勾选的图层实体。

## 设计决策

| # | 决策项 | 选择 |
|---|-------|------|
| 1 | UI 范围 | 直接替换现有"选择图层"Checkbox，移除无关的 `featureLayers` 列表 |
| 2 | 默认选中策略 | 仅选中"可见 (`on`) 且未冻结 (`!frozen`)"的 CAD 图层 |
| 3 | 列表展示信息 | 图层名 + 可见/冻结/锁定状态图标 |
| 4 | 参数透传方式 | 沿用 `pushFeatures` 的 `dwgLayerFilter` 模式：逗号分隔的图层名字符串，`""` = 全部 |

## 架构与数据流

```
[ExportGisModal.jsx] (前端)
  ├─ Modal 打开时调用 viewer.getLayersWithInfo() 读取当前 DWG 的 CAD 图层
  ├─ 默认勾选 layer.on && !layer.frozen 的图层
  ├─ 每行渲染: [Checkbox] [图层名] [可见图标] [冻结图标] [锁定图标]
  └─ 点"导出": layerFilter = 已选中图层名.join(',')  // 全选或全空均传 ""
     → viewer.execute('GIS_EXPORT', [format, exportPath, layerFilter])
  ▼
[Cmd_GIS_EXPORT::execute] (DrawingWeb/GisCommands.cpp)
  ├─ pIO->getString() 读取 3 个参数: format, path, layerFilter
  └─ IU_GisService_exportToGis(pDb, path, fmt, epsg, layerFilter)
  ▼
[IUcoGisService::exportToGis] (include/uaodcadcore/gdal/uaodco_igisservice.h)
  └─ 接口签名扩展第 5 个参数 const std::string& layerFilter = ""
  ▼
[UcoGisServiceImpl::exportToGis] (src/uaodcadcore/gdal/uaodco_gisservice_impl.cpp)
  └─ 转调 uodgdal::ConvertDWGToGIS(pDb, path, fmt, epsg, layerFilter)
  ▼
[uodgdal::ConvertDWGToGIS] (src/uaodcadcore/gdal/uaodco_converttogis.cpp)
  ├─ 解析 layerFilter 为 std::set<std::string>（空集 = 不过滤）
  ├─ 遍历 ModelSpace 时: 若 filter 非空 && !filter.contains(entity.layer()) 则跳过
  └─ 其余按 CAD 图层名分组 → 写 OGR（现有逻辑不变）
```

## 组件级变更清单

### 前端 (DrawingWebApp)

**文件**: `src/components/GisService/ExportGisModal.jsx`

- 新增 state: `cadLayers`（完整图层列表）、`selectedCadLayers`（勾选集合）
- 新增 `useEffect`: Modal 每次打开时调用 `viewerRef.current.getLayersWithInfo()`，写入 `cadLayers`，并把 `layer.on && !layer.frozen` 的 `layer.name` 作为初始 `selectedCadLayers`
- 删除原有 `layerOptions`（基于 `gisStore.featureLayers`）逻辑
- 新增自定义 Checkbox 列表渲染：每行 `[Checkbox] [图层名] [EyeOutlined|EyeInvisibleOutlined] [SnowflakeIcon|空] [LockOutlined|空]`
  - 图标复用 LayerManagerDialog 已有的 `@ant-design/icons` 图标和 `SnowflakeIcon` SVG
- Form.Item 标签改为"选择要导出的 CAD 图层（留空导出全部）"
- `handleOk` 中把 `layers` 变量的含义改为：若 `selectedCadLayers.length === cadLayers.length || selectedCadLayers.length === 0` 则传 `""`（全部语义），否则 `selectedCadLayers.join(',')`
- 导出后上传到 `gisStore.addLog` 的消息保留格式信息不变

### WASM 层 (DrawingWeb)

**文件**: `DrawingWeb/GisCommands.cpp` (Cmd_GIS_EXPORT)

```cpp
OdString format      = pIO->getString(L"Export format");
OdString path        = pIO->getString(L"Export path");
OdString layerFilter = pIO->getString(L"Layer filter");   // 新增
std::string sFormat = toUtf8(format);
std::string sPath   = toUtf8(path);
std::string sFilter = toUtf8(layerFilter);

bool ok = IU_GisService_exportToGis(pDb, sPath, sFormat, 0, sFilter);
```

### 服务接口 (uaodcadcore)

**文件**: `include/uaodcadcore/gdal/uaodco_igisservice.h`

接口增加 layerFilter 参数（默认空串，向后兼容）：
```cpp
virtual bool exportToGis(
    OdDbDatabase* pDb,
    const std::string& outputPath,
    const std::string& format,
    int epsgCode = 0,
    const std::string& dwgLayerFilter = "") = 0;
```

同时更新 inline 封装 `IU_GisService_exportToGis` 的签名与参数透传。

**文件**: `src/uaodcadcore/gdal/uaodco_gisservice_impl.h` / `.cpp`

匹配基类新签名，`exportToGis` 末尾改为：
```cpp
return uodgdal::ConvertDWGToGIS(pDb, outputPath.c_str(), format.c_str(), epsgCode, dwgLayerFilter);
```

### 转换核心 (uaodcadcore)

**文件**: `include/uaodcadcore/gdal/uaodco_converttogis.h`

```cpp
UAODCORE_API bool ConvertDWGToGIS(
    OdDbDatabase* poDb,
    const char* pszOutputFile,
    const char* pszFormat = "ESRI Shapefile",
    int iEPSGCode = 0,
    const std::string& dwgLayerFilter = "");
```

**文件**: `src/uaodcadcore/gdal/uaodco_converttogis.cpp`

在函数体入口增加过滤集解析：
```cpp
std::set<std::string> filterSet;
if (!dwgLayerFilter.empty()) {
    std::stringstream ss(dwgLayerFilter);
    std::string item;
    while (std::getline(ss, item, ',')) {
        // 去首尾空格
        auto l = item.find_first_not_of(" \t");
        auto r = item.find_last_not_of(" \t");
        if (l != std::string::npos)
            filterSet.insert(item.substr(l, r - l + 1));
    }
}
```

在 ModelSpace 遍历循环（现第 706-716 行）增加：
```cpp
if (!filterSet.empty() && filterSet.find(sLayerName) == filterSet.end())
    continue;
```

其余逻辑（按图层分组、`g_LayerGeometryMap` 查找、写 OGR）不变。

## 边界与异常处理

- **`layerFilter` 为空串** → 保持全量导出（向后兼容所有现有调用方）
- **用户勾选了所有图层** → 前端同样传 `""`，减少 C++ 侧无谓的字符串比较
- **用户一个都不勾** → 前端也传 `""`，语义与原 UI "留空=全部"一致（替代"不勾=什么都不导出"的迷惑选项）
- **图层名含中文** → `pIO->getString()` 返回 `OdString` 走 `toUtf8`，后续比较均在 UTF-8 空间内，`poEntity->layer()` 也是 UTF-8，字节级相等可行
- **勾选了不存在的图层名** → `ConvertDWGToGIS` 按实体层名筛选，筛不到就产出空结果，不报错

## 明确不在本次范围

- `g_LayerGeometryMap` 硬编码仅覆盖 5 个中文图层名的问题 —— 独立议题，本次保持现状
- 跨布局（PaperSpace/其他 BlockTableRecord）导出 —— 当前仅导出 ModelSpace
- 导入侧 (`importGisFile`) 的图层选择 UX —— 不涉及

## 测试策略

- **手工端到端**：
  1. 打开含多图层的 DWG，执行"导出 GIS"
  2. 验证 Modal 列出所有 CAD 图层，默认勾选状态与图层 on/frozen 一致
  3. 部分勾选后导出 GeoPackage，用 QGIS / ogrinfo 验证只有选中图层
  4. 全选 / 全不选两种极端情况均导出全部（兼容原行为）
- **回归**：LayerManagerDialog 正常工作（未改动其引用的 `getLayersWithInfo`）、AI Assistant 生成的 `GIS_EXPORT` 代码（仅 2 参）仍能跑通（`layerFilter` 默认空串）

## 向后兼容

- C++ 接口的新参数均带默认值，老调用方（如 `pushFeatures` 内部的 `ConvertDWGToGIS` 调用）无需改动
- `Cmd_GIS_EXPORT` 读第 3 个参数：若前端旧代码仍只传 2 个参数，`pIO->getString` 会等待第三个输入 —— 需确认 `OdDbUserIO::getString` 在 args 数组耗尽时的行为（通常返回空串，但需验证）。实施阶段在 WASM 端验证并在必要时加 try/catch

## 相关笔记

- [[specs]]
- [[GIS 目录面板 + 调图/属性查询 设计文档]]
- [[Legend Analysis Redesign: Programmatic Region Scan + Vision]]
- [[Industry Standards RAG Knowledge Base Design]]
- [[WASM License Gate 设计（DrawingWebApp）]]
- [[审图批注沙箱 API 设计]]
- [[设计文档：同步 quzhen 分支审查批注功能至 feat-zfs]]
- [[quzhen 审查批注功能同步 Implementation Plan]]
