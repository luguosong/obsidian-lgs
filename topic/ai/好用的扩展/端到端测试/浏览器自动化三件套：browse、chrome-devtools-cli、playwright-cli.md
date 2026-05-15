---
tags:
  - claude-code
  - 浏览器自动化
  - gstack
  - Playwright
  - CDP
  - E2E测试
created: 2026-05-15
aliases:
  - 浏览器自动化工具对比
  - browse vs devtools vs playwright
---

# 浏览器自动化三件套：browse、chrome-devtools-cli、playwright-cli

## 前言

在 [[Claude Code]] 生态中，有三个浏览器自动化 Skill 经常被混淆。它们的技术栈有重叠（都涉及 Playwright 或 CDP），但定位和能力边界截然不同。本文从架构原理出发，理清三者的分工。

## 架构总览

```
┌─────────────────────────────────────────────────────────┐
│                    Claude Code                          │
│                                                         │
│  /browse ──HTTP──┐   /chrome-devtools-cli ──CLI──┐      │
│                  │                                │      │
│  /playwright-cli ──CLI──┐                         │      │
│                         ▼                         ▼      │
│              ┌─────────────────┐  ┌──────────────────┐   │
│              │ gstack browse   │  │chrome-devtools-mcp│   │
│              │ 常驻守护进程     │  │ (npm 全局包)      │   │
│              │ Playwright+CDP  │  │ 纯 CDP           │   │
│              └────────┬────────┘  └────────┬─────────┘   │
│                       │                    │              │
│  /playwright-cli ─────┼────────────────────┤              │
│                       ▼                    ▼              │
│              ┌──────────────────────────────────┐        │
│              │        Chromium 浏览器            │        │
│              └──────────────────────────────────┘        │
└─────────────────────────────────────────────────────────┘
```

## 1. gstack `/browse` — 日常浏览工具

### 定位

gstack 的 `/browse` 是日常 Web 操作的默认工具。所有常规浏览、页面交互、截图都走这个。

### 架构原理

```
Claude Code
    ↓ HTTP POST /command
browse.exe (CLI 客户端，~113MB Bun 编译单文件)
    ↓ HTTP localhost:<随机端口>
server-node.mjs (常驻守护进程)
    ↓ Playwright API + CDP Bridge
Chromium 浏览器
```

**关键设计：**

| 特性 | 说明 |
|------|------|
| 常驻守护进程 | 首次调用启动（~3s），后续命令 ~100ms 响应，30 分钟空闲自动关闭 |
| Playwright 驱动 | 导航、点击、填表、截图等核心操作 |
| CDP 桥接 | 白名单机制，仅允许特定 CDP 方法（CSS 检查、PDF、性能指标） |
| 反检测 | 隐藏 `navigator.webdriver`，但不伪造 plugins/languages（保持指纹一致性） |
| 状态持久化 | `.gstack/browse.json` 保存端口、PID、auth token |
| 认证 | UUID root token + 按 spawn 分发的 scoped token |

**两种运行模式：**

- **Headless（默认）**：`chromium.launch()` 启动，用于常规浏览
- **Headed（可见）**：`/connect-chrome` 触发，使用 `launchPersistentContext()` 加载 gstack 侧边栏扩展，配置文件位于 `~/.gstack/chromium-profile`

**Windows 特殊处理：**

Windows 上因 Bun 兼容性问题，守护进程使用 Node.js 版本（`server-node.mjs`）而非 Bun。

### 典型用法

```bash
# 启动浏览并导航
$B goto https://example.com

# 获取页面快照（Accessibility Tree）
$B snapshot

# 点击元素
$B click "1_3"

# 截图
$B screenshot
```

## 2. `/chrome-devtools-cli` — 性能调优工具

### 定位

直接通过 CDP 协议控制 Chrome，专注于**性能分析和 Lighthouse 审计**。不做日常浏览用。

### 架构原理

```
Claude Code
    ↓ Shell 命令
chrome-devtools (CLI)
    ↓ CDP WebSocket
Chrome 浏览器 (必须 headed 模式)
```

基于 `chrome-devtools-mcp` npm 包，所有操作通过 CLI 调用：

```bash
chrome-devtools take_snapshot
chrome-devtools click "1_3"
```

### 独占能力

| 能力 | 说明 |
|------|------|
| **Lighthouse 审计** | navigation/snapshot 模式，mobile/desktop 双配置 |
| **Performance Profiling** | Chrome Performance Trace、堆快照、Performance Insights 分析 |
| **CPU/网络节流** | `--cpuThrottlingRate`、离线模式、自定义网络条件 |
| **地理位置模拟** | 设置经纬度坐标 |
| **网络请求详情** | 按资源类型过滤、保存 request/response body 到文件 |
| **Console 消息检查** | 分页查询、按类型过滤 |

### 何时使用

- 需要跑 Lighthouse 看性能分数
- 需要抓 Performance Trace 分析卡顿
- 需要查看具体网络请求的 request/response 内容

## 3. `/playwright-cli` — 测试开发工具

### 定位

Playwright 的完整 CLI 包装，专注于**编写、调试、录制 E2E 测试**。不做日常浏览用。

### 架构原理

```
Claude Code
    ↓ Shell 命令
playwright-cli (npm 全局包)
    ↓ Playwright Node.js API
Chromium / Firefox / WebKit
```

支持 `--browser=chrome --headed`（必须 headed 模式）。

### 独占能力

| 能力 | 说明 |
|------|------|
| **请求 Mock/拦截** | 按 URL pattern 拦截、模拟、修改或阻断网络请求 |
| **测试代码自动生成** | 每个操作自动生成对应的 Playwright TypeScript 代码 |
| **Playwright 测试 Debug** | `--debug=cli` 模式，断点暂停、实时探索 |
| **Trace 录制** | 每步操作记录 DOM 快照 + 网络 + Console + 截图 |
| **并发隔离 Session** | `-s=name` 创建独立浏览器上下文，各有 cookie/storage |
| **完整 Storage 管理** | Cookie/LocalStorage/SessionStorage 增删查改、状态导出恢复 |
| **视频录制** | WebM 格式，支持章节标记和自定义 HTML 叠加层 |
| **任意代码执行** | `run-code` 执行任何 Playwright API 调用 |
| **PDF 导出** | 保存页面为 PDF |

### 何时使用

- 编写 E2E 测试用例
- Mock 网络请求测试异常场景
- 调试已有的 Playwright 测试
- 录制测试操作生成代码

## 能力对比矩阵

| 能力 | `/browse` | `/chrome-devtools-cli` | `/playwright-cli` |
|------|:-:|:-:|:-:|
| 基本 Web 浏览/交互 | ✅ | ✅ | ✅ |
| 常驻守护进程（快速复用） | ✅ | ❌ | ❌ |
| 反检测/Stealth | ✅ | ❌ | ❌ |
| Lighthouse 审计 | ❌ | ✅ | ❌ |
| Performance Profiling | ❌ | ✅ | ❌ |
| 网络请求 Mock | ❌ | ❌ | ✅ |
| 测试代码生成 | ❌ | ❌ | ✅ |
| Playwright 测试 Debug | ❌ | ❌ | ✅ |
| Trace 录制/回放 | ❌ | ❌ | ✅ |
| 并发隔离 Session | ❌ | ❌ | ✅ |
| 视频录制 | ❌ | ❌ | ✅ |
| Cookie/Storage 管理 | 基础 | 基础 | 完整 |

## 全局规则

在 `~/.claude/CLAUDE.md` 中已配置：

> 所有 Web 浏览操作必须使用 gstack 的 `/browse` skill，禁止使用 `mcp__claude-in-chrome__*` 工具。

**原因：** `mcp__claude-in-chrome__*` 通过 Chrome 扩展连接，与 browse 争夺同一个浏览器实例的 CDP 连接，会导致端口/会话冲突和状态不一致。

## 选型决策树

```
需要操作浏览器？
├── 日常浏览/查看网页/截图 → /browse
├── 需要性能分析？
│   ├── 跑 Lighthouse → /chrome-devtools-cli
│   ├── 抓 Performance Trace → /chrome-devtools-cli
│   └── 看网络请求详情 → /chrome-devtools-cli
└── 需要测试相关？
    ├── 写 E2E 测试 → /playwright-cli
    ├── Mock 网络请求 → /playwright-cli
    ├── 调试已有测试 → /playwright-cli
    └── 录制操作生成代码 → /playwright-cli
```
