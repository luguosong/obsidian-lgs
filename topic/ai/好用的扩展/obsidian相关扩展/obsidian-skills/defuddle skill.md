---
title: defuddle skill
description: 使用 Defuddle CLI 从网页提取干净 Markdown，Token 节省 80-95%
created: 2026-05-10
tags:
  - ai
  - claude-code
  - obsidian
  - skill
  - defuddle
  - 网页抓取
---

# defuddle

> [!summary]
> 使用 **Defuddle CLI** 将网页 URL 转换为干净 Markdown，自动剥离导航、广告、侧边栏等冗余元素，**Token 节省 80-95%**。与 [[Obsidian]] Web Clipper 使用相同引擎。

**触发词**：`抓取网页`、`保存文章`、`网页剪藏`、`读取 URL`、`总结在线文章`

## 安装

```bash
npm install -g defuddle-cli
defuddle --version
```

## 基础用法

```bash
defuddle https://example.com/article                    # 输出 Markdown
defuddle https://example.com/article -o output.md       # 保存到文件
defuddle https://example.com/article --json             # JSON（含元数据）
defuddle https://example.com/article --text             # 纯文本
defuddle https://example.com/article --html             # 清理后的 HTML
```

### 提取特定元素

```bash
defuddle https://example.com --title          # 仅标题
defuddle https://example.com --author         # 仅作者
defuddle https://example.com --date           # 仅日期
defuddle https://example.com --description    # 仅摘要
```

### JSON 输出格式

```json
{
  "title": "文章标题",
  "author": "作者",
  "date": "2024-01-15T10:30:00Z",
  "description": "摘要",
  "domain": "example.com",
  "url": "https://example.com/article",
  "image": "https://example.com/cover.jpg",
  "content": "# 文章标题\n\n正文..."
}
```

## 高级用法

### 自定义选择器

```bash
defuddle https://example.com --selector "article.post-content"       # 指定内容区域
defuddle https://example.com --exclude ".sidebar, .comments"         # 排除区域
```

### 动态页面

```bash
defuddle https://example.com/spa --wait 3000          # 等待 JS 执行
defuddle https://example.com/members --puppeteer       # Puppeteer 模式
```

### 批量处理

```bash
defuddle --batch urls.txt --output-dir ~/vault/剪藏/
```

### 管道组合

```bash
defuddle https://example.com | wc -w                              # 统计字数
defuddle https://example.com --json | jq '.title, .author'         # jq 处理
defuddle https://example.com -o "剪藏/$(date +%Y-%m-%d)-文章.md"   # 保存笔记
```

## Token 节省效果

| 项目 | 原始 HTML | Defuddle 输出 |
|------|----------|--------------|
| 导航栏/侧边栏/页脚 | 包含 | 去除 |
| 广告/推荐 | 包含 | 去除 |
| 评论区 | 包含 | 去除 |
| **Token 量** | ~15000 | ~800（**节省 ~95%**） |

## 使用示例

```
# 简单阅读
读取并总结这篇文章：[URL]

# 保存为笔记
把 [URL] 保存为 Obsidian 笔记到 [文件夹]，标签：[标签]

# 批量处理
把以下 URL 的文章都保存到 vault：[URL1] [URL2] [URL3]
```

## 协作关系

```
网页 URL → defuddle 提取 → [[obsidian-markdown skill]] 格式化 → [[obsidian-cli skill]] 写入 Vault
```

> [!warning] 不适用场景
> - URL 以 `.md` 结尾（已是 Markdown，直接用 WebFetch）
> - 需登录的页面（需 `--puppeteer`）
> - API 接口 URL（返回 JSON 而非 HTML）

## 参考链接

- [Defuddle CLI 源码](https://github.com/kepano/defuddle-cli)
- [Defuddle 核心库](https://github.com/kepano/defuddle)
- [Obsidian Web Clipper](https://obsidian.md/clipper)（同引擎图形界面版）

---

→ 返回 [[obsidian-skills 套件总览]]
