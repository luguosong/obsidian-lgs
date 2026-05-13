# GIS服务 Ribbon 标签页 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use [[superpower]]s:subagent-driven-development (recommended) or [[superpower]]s:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在审图模式 ReviewRibbon 中新增"GIS服务"标签页，包含 4 组 19 个按钮的完整 UI Shell（所有按钮暂用 `onNotImpl` 桩回调，C++ 功能后续开发）。

**Architecture:** 遵循现有模式——所有 Tab 组件（`SealTab`、`MeasureTab` 等）都定义在 `ReviewRibbon.jsx` 内部。新增的 `GisServiceTab` 同样在该文件中定义，使用 `RvBtn` + `RvGroup` + `Divider` 复用组件。`TabBar.jsx` 新增标签项。

**Tech Stack:** React 19, MobX, Ant Design, SVG icons (stroke-based 18x18)

**Design Spec:** `docs/specs/2026-04-10-gis-service-ribbon-tab-design.md`

---

## File Structure

| 文件 | 操作 | 职责 |
|------|------|------|
| `src/components/TabBar/TabBar.jsx` | 修改 | `REVIEW_TABS` 数组插入 `'GIS服务'` |
| `src/components/Ribbon/ReviewRibbon.jsx` | 修改 | 新增 19 个 SVG 图标 + `GisServiceTab` 组件 + `case` 分支 |

---

### Task 1: 在 TabBar 中添加"GIS服务"标签

**Files:**
- Modify: `src/components/TabBar/TabBar.jsx:7`

- [ ] **Step 1: 修改 REVIEW_TABS 数组**

在"签章"后插入"GIS服务"：

```js
const REVIEW_TABS = ['主页', '比对', '测量', '签章', 'GIS服务', '审查流程', 'BIM审查', '输出']
```

- [ ] **Step 2: 验证语法**

Run: `npx eslint src/components/TabBar/TabBar.jsx --no-error-on-unmatched-pattern`
Expected: 无错误

- [ ] **Step 3: Commit**

```bash
git add src/components/TabBar/TabBar.jsx
git commit -m "feat: add GIS服务 tab to ReviewRibbon tab bar"
```

---

### Task 2: 添加 GIS 图标定义

**Files:**
- Modify: `src/components/Ribbon/ReviewRibbon.jsx` — `I` 对象（约第 68–208 行）

- [ ] **Step 1: 在 `I` 对象末尾（`fullscreen` 之后）添加 19 个 GIS 图标**

在 `I` 对象的最后一个现有图标后（`fullscreen` 行之后、对象闭合 `}` 之前），追加以下 SVG 图标定义：

```js
  // ── GIS 服务 ──
  gisService: <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.3"><path d="M9 2v4M9 12v4M2 9h4M12 9h4"/><circle cx="9" cy="9" r="3"/></svg>,
  gisAdd: <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.3"><circle cx="9" cy="9" r="6"/><path d="M9 6v6M6 9h6"/></svg>,
  gisBrowse: <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.3"><path d="M3 3h4v4H3zM11 3h4v4h-4zM3 11h4v4H3zM11 11h4v4h-4z" opacity="0.6"/></svg>,
  gisAuth: <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.3"><rect x="3" y="5" width="12" height="9" rx="1.5"/><circle cx="9" cy="9.5" r="2"/><path d="M6 5V4a3 3 0 016 0v1"/></svg>,
  gisDisconnect: <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.3"><path d="M4 9h10M7 6l-3 3 3 3M11 6l3 3-3 3"/></svg>,
  gisLoadMap: <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.3"><rect x="2" y="2" width="14" height="14" rx="2"/><path d="M2 12l4-4 3 3 3-5 4 6" opacity="0.5"/><circle cx="6" cy="6" r="1.5" opacity="0.4"/></svg>,
  gisRefresh: <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round"><path d="M14 9a5 5 0 11-1.5-3.5"/><polyline points="14,2 14,6 10,6"/></svg>,
  gisOpacity: <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.3"><rect x="3" y="3" width="12" height="12" rx="1" opacity="0.3"/><rect x="3" y="3" width="12" height="12" rx="1" fill="none"/><path d="M3 9h12" strokeDasharray="2 2"/></svg>,
  gisRemoveMap: <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.3"><rect x="2" y="2" width="14" height="14" rx="2"/><path d="M6 6l6 6M12 6l-6 6"/></svg>,
  gisLoadFeature: <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.3"><polygon points="3,14 7,4 12,10 16,6" opacity="0.3" fill="currentColor"/><polygon points="3,14 7,4 12,10 16,6" fill="none"/><circle cx="7" cy="4" r="1.2"/><circle cx="12" cy="10" r="1.2"/></svg>,
  gisAttrQuery: <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.3"><rect x="2" y="3" width="14" height="12" rx="1.5"/><line x1="5" y1="7" x2="13" y2="7" opacity="0.4"/><line x1="5" y1="10" x2="10" y2="10" opacity="0.4"/><circle cx="13" cy="12" r="2.5"/><path d="M13 10.5v3M11.5 12h3"/></svg>,
  gisSpatialQuery: <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.3"><rect x="4" y="4" width="8" height="8" rx="1" strokeDasharray="2 1.5"/><circle cx="13" cy="13" r="3"/><path d="M15 15l1.5 1.5"/></svg>,
  gisStyleMap: <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.3"><path d="M2 4h5v3H2zM11 4h5v3h-5zM2 11h5v3H2zM11 11h5v3h-5z"/><path d="M7 5.5h4M7 12.5h4" strokeDasharray="1.5 1"/></svg>,
  gisPush: <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.3"><path d="M9 3v8M6 8l3 3 3-3"/><path d="M3 13h12" strokeDasharray="2 1.5"/><path d="M3 15h12"/></svg>,
  gisPull: <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.3"><path d="M9 11V3M6 6l3-3 3 3"/><path d="M3 13h12" strokeDasharray="2 1.5"/><path d="M3 15h12"/></svg>,
  gisSyncStatus: <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.3"><circle cx="9" cy="9" r="6"/><path d="M9 5v4l3 2"/></svg>,
  gisCrs: <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.3"><circle cx="9" cy="9" r="6.5"/><path d="M2.5 9h13M9 2.5c-2 2.5-2 11 0 13M9 2.5c2 2.5 2 11 0 13" opacity="0.5"/><path d="M4 5h10M4 13h10" opacity="0.3"/></svg>,
  gisExport: <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.3"><path d="M5 2v14l4-3 4 3V2z"/></svg>,
  gisLog: <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.3"><rect x="3" y="2" width="12" height="14" rx="1.5"/><line x1="6" y1="6" x2="12" y2="6" opacity="0.4"/><line x1="6" y1="9" x2="12" y2="9" opacity="0.4"/><line x1="6" y1="12" x2="10" y2="12" opacity="0.4"/></svg>,
```

- [ ] **Step 2: 验证语法**

Run: `npx eslint src/components/Ribbon/ReviewRibbon.jsx --no-error-on-unmatched-pattern`
Expected: 无错误

- [ ] **Step 3: Commit**

```bash
git add src/components/Ribbon/ReviewRibbon.jsx
git commit -m "feat: add 19 GIS service SVG icons to ReviewRibbon"
```

---

### Task 3: 创建 GisServiceTab 组件

**Files:**
- Modify: `src/components/Ribbon/ReviewRibbon.jsx` — 在 `SealTab` 组件之后（约第 741 行 `// ===== 审查流程 Tab =====` 之前）插入

- [ ] **Step 1: 在 SealTab 和 ReviewFlowTab 之间插入 GisServiceTab 组件**

在 `ReviewRibbon.jsx` 中找到 `// ===== 审查流程 Tab =====`（约第 743 行），在其上方插入：

```jsx
// ===== GIS服务 Tab =====

function GisServiceTab({ onNotImpl }) {
  return (
    <>
      <RvGroup label="连接">
        <RvBtn icon={I.gisService} label="常用服务" primary title="从预配置列表快速连接 ArcGIS 服务" onClick={() => onNotImpl('常用服务')} />
        <RvBtn icon={I.gisAdd} label="添加服务" title="手动输入 MapServer/FeatureServer REST URL" onClick={() => onNotImpl('添加服务')} />
        <RvBtn icon={I.gisBrowse} label="浏览目录" title="浏览 ArcGIS Server 服务目录并勾选图层" onClick={() => onNotImpl('浏览目录')} />
        <Divider />
        <RvBtn icon={I.gisAuth} label="认证管理" title="管理 Token 认证和用户名/密码凭证" onClick={() => onNotImpl('认证管理')} />
        <RvBtn icon={I.gisDisconnect} label="断开连接" danger title="断开当前 ArcGIS 服务连接" onClick={() => onNotImpl('断开连接')} />
      </RvGroup>

      <RvGroup label="地图影像">
        <RvBtn icon={I.gisLoadMap} label="加载底图" primary title="从 MapServer 加载影像底图叠加到视口" onClick={() => onNotImpl('加载底图')} />
        <RvBtn icon={I.gisRefresh} label="刷新影像" title="按当前视口范围重新获取影像瓦片" onClick={() => onNotImpl('刷新影像')} />
        <RvBtn icon={I.gisOpacity} label="透明度" title="调节底图影像透明度 (0-100%)" onClick={() => onNotImpl('透明度')} />
        <Divider />
        <RvBtn icon={I.gisRemoveMap} label="移除底图" danger title="移除已加载的 GIS 底图影像" onClick={() => onNotImpl('移除底图')} />
      </RvGroup>

      <RvGroup label="要素数据">
        <RvBtn icon={I.gisLoadFeature} label="加载要素" primary title="从 FeatureServer 加载矢量要素到 DWG" onClick={() => onNotImpl('加载要素')} />
        <RvBtn icon={I.gisAttrQuery} label="属性查询" title="输入 WHERE 条件过滤要素" onClick={() => onNotImpl('属性查询')} />
        <RvBtn icon={I.gisSpatialQuery} label="空间查询" title="框选范围查询要素" onClick={() => onNotImpl('空间查询')} />
        <RvBtn icon={I.gisStyleMap} label="样式映射" amber title="设置要素→DWG 图层/颜色/线型映射规则" onClick={() => onNotImpl('样式映射')} />
        <Divider />
        <RvBtn icon={I.gisPush} label="推送修改" green title="将编辑的要素同步回 FeatureServer" onClick={() => onNotImpl('推送修改')} />
        <RvBtn icon={I.gisPull} label="拉取更新" green title="从 FeatureServer 获取最新数据" onClick={() => onNotImpl('拉取更新')} />
        <RvBtn icon={I.gisSyncStatus} label="同步状态" title="查看已修改/待推送/冲突的要素" onClick={() => onNotImpl('同步状态')} />
      </RvGroup>

      <RvGroup label="工具">
        <RvBtn icon={I.gisCrs} label="坐标系信息" title="查看 DWG 与 GIS 服务坐标系状态" onClick={() => onNotImpl('坐标系信息')} />
        <RvBtn icon={I.gisExport} label="导出GIS" primary title="导出为 GeoPackage/Shapefile/GeoJSON" onClick={() => onNotImpl('导出GIS')} />
        <RvBtn icon={I.gisLog} label="操作日志" title="查看 GIS 操作详细日志" onClick={() => onNotImpl('操作日志')} />
      </RvGroup>
    </>
  )
}
```

- [ ] **Step 2: 验证语法**

Run: `npx eslint src/components/Ribbon/ReviewRibbon.jsx --no-error-on-unmatched-pattern`
Expected: 无错误

- [ ] **Step 3: Commit**

```bash
git add src/components/Ribbon/ReviewRibbon.jsx
git commit -m "feat: add GisServiceTab component with 4 groups and 19 buttons"
```

---

### Task 4: 连接 Tab 路由

**Files:**
- Modify: `src/components/Ribbon/ReviewRibbon.jsx` — `switch` 语句（约第 1242 行）

- [ ] **Step 1: 在 switch 的 `case '签章'` 之后添加 GIS服务 case**

找到这一行（约第 1242 行）：
```js
      case '签章': return <SealTab onNotImpl={handleNotImpl} />
```

在其后面添加：
```js
      case 'GIS服务': return <GisServiceTab onNotImpl={handleNotImpl} />
```

最终该区域应为：
```js
      case '测量': return <MeasureTab onNotImpl={handleNotImpl} />
      case '签章': return <SealTab onNotImpl={handleNotImpl} />
      case 'GIS服务': return <GisServiceTab onNotImpl={handleNotImpl} />
      case '审查流程': return <ReviewFlowTab onNotImpl={handleNotImpl} />
```

- [ ] **Step 2: 验证语法**

Run: `npx eslint src/components/Ribbon/ReviewRibbon.jsx --no-error-on-unmatched-pattern`
Expected: 无错误

- [ ] **Step 3: Commit**

```bash
git add src/components/Ribbon/ReviewRibbon.jsx
git commit -m "feat: wire GIS服务 tab routing in ReviewRibbon switch"
```

---

### Task 5: 最终验证

- [ ] **Step 1: 运行完整 lint 检查**

Run: `npm run lint`
Expected: 无新增错误

- [ ] **Step 2: 验证开发服务器可启动**

Run: `npm run dev` (手动验证页面可加载，切换到审图模式可看到"GIS服务"标签)

- [ ] **Step 3: 如有 lint 错误则修复并提交**

```bash
git add -A
git commit -m "fix: resolve lint issues in GIS service tab"
```

## 相关笔记

- [[specs]]
- [[图例分析功能设计规格]]
- [[ArcGIS Web 服务集成 — C++ 实施架构]]
- [[GIS服务 Ribbon 标签页设计规格]]
- [[批注数据持久化方案]]
- [[瞬态批注系统设计文档]]
- [[首次打开图纸自动归纳 — 视觉化重构设计]]
- [[审查建筑退线距离 — 实现详细说明]]
