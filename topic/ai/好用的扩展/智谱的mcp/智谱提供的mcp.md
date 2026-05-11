---
title: "智谱 MCP Server 文档"
sources:
  - "https://docs.bigmodel.cn/cn/coding-plan/mcp/vision-mcp-server"
  - "https://docs.bigmodel.cn/cn/coding-plan/mcp/search-mcp-server"
  - "https://docs.bigmodel.cn/cn/coding-plan/mcp/reader-mcp-server"
  - "https://docs.bigmodel.cn/cn/coding-plan/mcp/zread-mcp-server"
tags:
  - ai
  - 扩展

---

# 智谱 MCP Server

智谱为 GLM Coding Plan 用户提供 4 个 MCP Server，覆盖视觉、搜索、网页读取、开源仓库能力。兼容 Claude Code、Cline、OpenCode 等客户端。

## 一览表

| 服务 | 类型 | 传输 | 核心能力 |
|------|------|------|---------|
| **视觉理解 MCP** | Local | stdio | 图像/视频理解（GLM-4.6V） |
| **联网搜索 MCP** | Remote | HTTP | 全网搜索 |
| **网页读取 MCP** | Remote | HTTP | 网页内容抓取 |
| **开源仓库 MCP (ZRead)** | Remote | HTTP | GitHub 仓库知识检索 |

## 工具列表

### 视觉理解 MCP（`@z_ai/mcp-server`，需 Node.js >= 18）

| 工具 | 用途 |
|------|------|
| `ui_to_artifact` | UI 截图 → 代码 / 设计规范 / 描述 |
| `extract_text_from_screenshot` | OCR 文字提取 |
| `diagnose_error_screenshot` | 错误截图诊断与修复建议 |
| `understand_technical_diagram` | 架构图 / 流程图 / UML 解读 |
| `analyze_data_visualization` | 图表趋势与异常分析 |
| `ui_diff_check` | 两张 UI 截图对比差异 |
| `image_analysis` | 通用图像理解 |
| `video_analysis` | 视频场景解析（MP4/MOV/M4V，本地最大 8MB） |

### 联网搜索 MCP

| 工具 | 用途 |
|------|------|
| `webSearchPrime` | 搜索网络信息，返回标题、URL、摘要 |

### 网页读取 MCP

| 工具 | 用途 |
|------|------|
| `webReader` | 抓取 URL 网页内容，返回标题、正文、元数据、链接 |

### 开源仓库 MCP (ZRead)

| 工具 | 用途 |
|------|------|
| `search_doc` | 搜索仓库文档、Issue、PR |
| `get_repo_structure` | 获取目录结构 |
| `read_file` | 读取指定文件代码 |

## 安装

> 将 `your_api_key` 替换为你的 API Key。

### 一键安装

```bash
# 视觉理解（Local）
claude mcp add -s user zai-mcp-server --env Z_AI_API_KEY=your_api_key -- npx -y "@z_ai/mcp-server"

# 联网搜索（Remote）
claude mcp add -s user -t http web-search-prime https://open.bigmodel.cn/api/mcp/web_search_prime/mcp --header "Authorization: Bearer your_api_key"

# 网页读取（Remote）
claude mcp add -s user -t http web-reader https://open.bigmodel.cn/api/mcp/web_reader/mcp --header "Authorization: Bearer your_api_key"

# 开源仓库（Remote）
claude mcp add -s user -t http zread https://open.bigmodel.cn/api/mcp/zread/mcp --header "Authorization: Bearer your_api_key"
```

卸载：`claude mcp list` → `claude mcp remove <name>`

### 手动配置（`~/.claude.json`）

```json
{
  "mcpServers": {
    "zai-mcp-server": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@z_ai/mcp-server"],
      "env": {
        "Z_AI_API_KEY": "your_api_key",
        "Z_AI_MODE": "ZHIPU"
      }
    },
    "web-search-prime": {
      "type": "http",
      "url": "https://open.bigmodel.cn/api/mcp/web_search_prime/mcp",
      "headers": { "Authorization": "Bearer your_api_key" }
    },
    "web-reader": {
      "type": "http",
      "url": "https://open.bigmodel.cn/api/mcp/web_reader/mcp",
      "headers": { "Authorization": "Bearer your_api_key" }
    },
    "zread": {
      "type": "http",
      "url": "https://open.bigmodel.cn/api/mcp/zread/mcp",
      "headers": { "Authorization": "Bearer your_api_key" }
    }
  }
}
```

### 环境变量（视觉理解 MCP）

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `Z_AI_API_KEY` | 智谱 API Key | 必需 |
| `Z_AI_MODE` | 服务平台 | `ZHIPU` |

## 使用额度

| 套餐 | 搜索 + 读取 + ZRead | 视觉理解 |
|------|---------------------|---------|
| Lite | 100 次/月 | 共享 5h prompt 池 |
| Pro | 1,000 次/月 | 共享 5h prompt 池 |
| Max | 4,000 次/月 | 共享 5h prompt 池 |

搜索/读取/ZRead 达到上限后当月无法调用；视觉理解达到上限后在 5 小时周期后恢复。

## 注意事项

- **视觉 MCP 最佳实践**：将图片放到本地目录，通过对话指定路径调用（如 `describe demo.png`）。直接粘贴图片不会走 MCP
- **Windows**：PowerShell 可能遇到 `-y` 参数问题，建议用 CMD 执行
- **npx 缓存**：老用户需用 `@z_ai/mcp-server@latest` 强制最新版
- **ZRead**：仅支持公开开源仓库，确认仓库名格式为 `owner/repo`

## 故障排除

**连接失败 / 超时**
- 确认 Node.js >= 18（视觉 MCP）、网络正常、防火墙未拦截
- 验证 API Key 正确且有余额
- 尝试切换 `Z_AI_MODE`（`ZHIPU` / `ZAI`）

**API Key 无效**
- 确认 Key 正确复制且已激活
- 确认平台选择与 Key 匹配

**视觉 MCP 本地排查**

```bash
Z_AI_API_KEY=your_api_key npx -y @z_ai/mcp-server
```

安装成功 → 问题在客户端配置；安装失败 → 根据错误信息排查环境/权限。
