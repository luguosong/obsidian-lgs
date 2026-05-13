---
title: "draw.io MCP Server"
source: "https://github.com/jgraph/drawio-mcp#skill--cli"
description: "draw.io 官方 MCP 服务器，让 LLM 在 draw.io 编辑器中创建和打开图表"
tags:
  - MCP
  - drawio
  - 画图
  - AI工具
author:
published:
---

## Draw.io MCP Server

draw.io 官方 [MCP](https://modelcontextprotocol.io/)（Model Context Protocol）服务器，让 LLM 在 draw.io 编辑器中创建和打开图表。

## 四种创建图表的方式

本仓库提供四种将 draw.io 与 AI 助手集成的方案，按需选择：

| | [MCP App Server](#mcp-app-server) | [MCP Tool Server](#mcp-tool-server) | [Skill + CLI](#skill--cli) | [项目指令方案](#alternative-project-instructions-no-mcp-required) |
| --- | --- | --- | --- | --- |
| **工作方式** | 在对话中内联渲染图表 | 在浏览器中打开图表 | 生成 `.drawio` 文件，可选导出 PNG/SVG/PDF | Claude 通过 Python 生成 draw.io URL |
| **图表输出** | 嵌入对话的交互式查看器 | 新标签页中的 draw.io 编辑器 | `.drawio` 或 `.drawio.png` / `.svg` / `.pdf` | 可点击的 draw.io 链接 |
| **需要安装** | 不需要（托管在 `mcp.draw.io`） | 需要（npm 包） | 复制 skill 文件 + draw.io Desktop | 不需要 — 只需粘贴指令 |
| **支持 XML、CSV、Mermaid** | 仅 XML | ✅ 全部支持 | 仅 XML（原生格式） | ✅ 全部支持 |
| **可在 draw.io 中编辑** | 通过 "Open in draw.io" 按钮 | ✅ 直接编辑 | ✅ 直接编辑 | 通过链接 |
| **适用平台** | Claude.ai、VS Code、任何 MCP Apps 宿主 | Claude Desktop、任何 MCP 客户端 | Claude Code | Claude.ai（配合 Projects） |
| **最适合** | 对话中内联预览 | 本地桌面工作流 | 本地开发工作流 | 快速上手，无需安装 |

---

## MCP App Server

MCP App 服务器使用 [MCP Apps](https://modelcontextprotocol.io/docs/extensions/apps) 协议在 AI 聊天界面中**内联**渲染 draw.io 图表。图表以交互式 iframe 形式直接显示在对话中，无需打开浏览器标签页。

官方托管端点：

```
https://mcp.draw.io/mcp
```

在 Claude.ai 或任何兼容 MCP Apps 的宿主中将此 URL 添加为远程 MCP 服务器即可，无需安装。

也可以通过 Node.js 本地运行，或部署自己的 Cloudflare Workers 实例。

**工具：**

- **`create_diagram`** — 将 draw.io XML 渲染为交互式图表，内联显示在对话中
- **`search_shapes`** — 按关键词搜索 draw.io 所有图形库中的 10,000+ 图形（AWS、Azure、GCP、P&ID、电气、Cisco、Kubernetes、UML、BPMN 等）。返回可直接用于 XML 的精确样式字符串。在调用 `create_diagram` 之前使用此工具查找正确的图形。

**[完整文档 →](https://github.com/jgraph/drawio-mcp/blob/main/mcp-app-server/README.md)**

> [!note] 内联图表渲染需要支持 MCP Apps 扩展的宿主环境。在不支持 MCP Apps 的宿主中，工具仍然可用，但会以文本形式返回 XML。

---

## MCP Tool Server

原始 MCP 服务器，直接在 draw.io 编辑器中打开图表。支持 XML、CSV 和 Mermaid.js 格式，带有 lightbox 和暗色模式选项。已发布为 npm 包 [`@drawio/mcp`](https://www.npmjs.com/package/@drawio/mcp)。

快速启动：`npx @drawio/mcp`

**[完整文档 →](https://github.com/jgraph/drawio-mcp/blob/main/mcp-tool-server/README.md)**

---

## Skill + CLI

Claude Code skill，生成原生 `.drawio` 文件，可选导出为 PNG、SVG 或 PDF（导出文件内嵌 XML，仍可在 draw.io 中编辑）。无需 MCP 配置 — 只需复制一个 skill 文件。

默认情况下，skill 会写入 `.drawio` 文件并在 draw.io 中打开。在请求中指定格式（`/drawio png ...`）即可使用 draw.io 桌面 CLI 进行导出，并启用 `--embed-diagram` 选项。

**[完整文档 →](https://github.com/jgraph/drawio-mcp/blob/main/skill-cli/README.md)**

---

## 备选方案：项目指令（无需 MCP）

一种**无需安装任何东西**的替代方案。将指令添加到 Claude Project 中，教 Claude 通过 Python 代码执行生成 draw.io URL。不需要 MCP 服务器，不需要桌面应用 — 粘贴即可使用。

**[完整文档 →](https://github.com/jgraph/drawio-mcp/blob/main/project-instructions/README.md)**

---

## XML 参考（唯一事实来源）

draw.io XML 生成参考 — 涵盖边路由、容器、图层、标签、元数据、暗色模式、样式属性和 XML 良构性 — 位于一个规范的单一文件中：

**[`shared/xml-reference.md`](https://github.com/jgraph/drawio-mcp/blob/main/shared/xml-reference.md)**

以上四种方案均使用此文件作为 LLM prompt 的唯一事实来源：

| 方案 | 访问方式 |
| --- | --- |
| MCP App Server | 启动 / 构建时读取文件，包含在工具描述中 |
| MCP Tool Server | 启动时从仓库或通过 `prepack` 打包的副本读取 |
| Skill + CLI | 引用 [GitHub raw URL](https://raw.githubusercontent.com/jgraph/drawio-mcp/main/shared/xml-reference.md) |
| 项目指令 | 用户将内容复制到自己的 Claude Project 中 |

更新 XML 生成指南时，只需编辑 `shared/xml-reference.md` — 变更会自动传播到所有使用方。

---

## 图形搜索索引

`search_shapes` 工具由预构建的 draw.io 全量图形索引驱动。该索引从 draw.io 客户端源码（`app.min.js`）生成，通过 jsdom 在 Node.js 中运行所有侧边栏调色板初始化并捕获图形数据。

```
# 生成图形搜索索引（需要 ../drawio-dev checkout）
cd shape-search
npm install
DRAWIO_DEV_PATH=../../drawio-dev node generate-index.js

# 重新构建 MCP App Server worker 以嵌入更新后的索引
cd ../mcp-app-server
npm run build:worker
```

**何时重新生成：** 更新 `drawio-dev` 后（新增图形、重命名 stencil、更新样式字符串）重新运行 `generate-index.js`。该脚本加载 `app.min.js` 和所有侧边栏调色板，因此能自动捕获图形库的任何变更。

生成的 `search-index.json` 已提交到仓库，这样 MCP App Server 就可以在没有本地 `drawio-dev` checkout 的情况下构建和部署。

---

## 开发

```
# MCP App Server
cd mcp-app-server
npm install
npm start

# MCP Tool Server
cd mcp-tool-server
npm install
npm start
```

## 相关资源

- [draw.io](https://www.draw.io/) - 免费在线图表编辑器
- [draw.io Desktop](https://github.com/jgraph/drawio-desktop) - 桌面应用
- [@drawio/mcp on npm](https://www.npmjs.com/package/@drawio/mcp) - npm 包
- [drawio-mcp on GitHub](https://github.com/jgraph/drawio-mcp) - 源码仓库
- [Mermaid.js Documentation](https://mermaid.js.org/intro/) - Mermaid.js 文档
- [MCP Specification](https://modelcontextprotocol.io/) - MCP 规范
- [MCP Apps Extension](https://modelcontextprotocol.io/docs/extensions/apps) - MCP Apps 扩展
