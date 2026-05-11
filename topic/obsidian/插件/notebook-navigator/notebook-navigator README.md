---
title: "Notebook Navigator 插件"
source: "https://github.com/johansan/notebook-navigator"
description: "用简洁的双栏界面替换 Obsidian 默认文件浏览器，支持文件夹树、标签浏览、文件预览、键盘导航、拖拽、置顶笔记和自定义显示选项。"
author:
---
字数：4058
阅读其他语言版本：[English](https://notebooknavigator.com/docs.html) • [العربية](https://notebooknavigator.com/ar/docs.html) • [Deutsch](https://notebooknavigator.com/de/docs.html) • [Español](https://notebooknavigator.com/es/docs.html) • [فارسی](https://notebooknavigator.com/fa/docs.html) • [Français](https://notebooknavigator.com/fr/docs.html) • [Bahasa Indonesia](https://notebooknavigator.com/id/docs.html) • [Italiano](https://notebooknavigator.com/it/docs.html) • [Nederlands](https://notebooknavigator.com/nl/docs.html) • [Polski](https://notebooknavigator.com/pl/docs.html) • [Português](https://notebooknavigator.com/pt/docs.html) • [Português (Brasil)](https://notebooknavigator.com/pt-br/docs.html) • [Русский](https://notebooknavigator.com/ru/docs.html) • [ไทย](https://notebooknavigator.com/th/docs.html) • [Türkçe](https://notebooknavigator.com/tr/docs.html) • [Українська](https://notebooknavigator.com/uk/docs.html) • [Tiếng Việt](https://notebooknavigator.com/vi/docs.html) • [日本語](https://notebooknavigator.com/ja/docs.html) • [한국어](https://notebooknavigator.com/ko/docs.html) • [中文简体](https://notebooknavigator.com/zh-cn/docs.html) • [中文繁體](https://notebooknavigator.com/zh-tw/docs.html)

[![Notebook Navigator Screenshot](https://github.com/johansan/notebook-navigator/raw/main/images/notebook-navigator.png?raw=true)](https://github.com/johansan/notebook-navigator/blob/main/images/notebook-navigator.png?raw=true)

将 Obsidian 变成快速、可定制的笔记浏览器——文件夹、标签、属性和快捷方式一览无余。可视化预览。完整键盘导航。双栏布局。移动端优化。支持 100,000+ 篇笔记。

如果你喜欢 Notebook Navigator，请考虑 [☕️ 请我喝杯咖啡](https://buymeacoffee.com/johansan) 或 [在 GitHub 上赞助 ❤️](https://github.com/sponsors/johansan)。

## 1 安装

1. **安装 Obsidian** - 从 [obsidian.md](https://obsidian.md/) 下载并安装
2. **启用社区插件** - 进入 设置 → 社区插件 → 开启社区插件
3. **安装 Notebook Navigator** - 点击"浏览" → 搜索"Notebook Navigator" → 安装
4. **安装 Style Settings（可选）** - 如需自定义颜色和外观，在社区插件中搜索"Style Settings"安装 [Style Settings](https://github.com/mgmeyers/obsidian-style-settings) 插件

## 2 快速上手

以下是官方教程，帮助你学习并掌握 Notebook Navigator：

[![Mastering Notebook Navigator](https://raw.githubusercontent.com/johansan/notebook-navigator/main/images/youtube-thumbnail.jpg)](https://www.youtube.com/watch?v=BewIlG8wLAM)

视频支持 21 种语言字幕。

## 3 安全与质量

Notebook Navigator 在代码合入前会经过 [TypeScript](https://www.typescriptlang.org/)、[ESLint](https://eslint.org/)（配合官方 [Obsidian ESLint plugin](https://github.com/obsidianmd/eslint-plugin)）、[Prettier](https://prettier.io/)、[Vitest](https://vitest.dev/) 以及生产构建检查。构建必须零错误、零警告才能通过。

安全检查通过 [CodeQL](https://codeql.github.com/) 运行，扫描历史可在 [CodeQL workflow runs](https://github.com/johansan/notebook-navigator/actions/workflows/codeql.yml) 以及 [OpenSSF Scorecard](https://securityscorecards.dev/viewer/?uri=github.com/johansan/notebook-navigator) 中查看。当前状态显示在本页顶部的徽章中。

Notebook Navigator 本地运行，但部分功能会发起文档中说明的 HTTP 请求，用于更新、下载和远程内容。完整列表参见[第 11 节 - 网络使用声明](#11-network-usage-disclosure)。

## 目录

## 4 文档

- [**API 参考**](https://github.com/johansan/notebook-navigator/blob/main/docs/api-reference.md) - 公开 API 文档。涵盖元数据管理、导航控制和事件订阅，面向 JavaScript/TypeScript 开发者。
- [**主题开发指南**](https://github.com/johansan/notebook-navigator/blob/main/docs/theming-guide.md) - 面向主题开发者的指南。包含 CSS class 参考、自定义属性以及明暗模式主题示例。
- [**启动流程**](https://github.com/johansan/notebook-navigator/blob/main/docs/startup-process.md) - 插件初始化序列。冷启动与热启动流程、元数据缓存解析、延迟清理以及内容生成 pipeline。包含 Mermaid 图表。
- [**元数据 Pipeline**](https://github.com/johansan/notebook-navigator/blob/main/docs/metadata-pipeline.md) - 缓存重建序列、provider pipeline 阶段以及完成信号。包含 Mermaid 图表。
- [**存储架构**](https://github.com/johansan/notebook-navigator/blob/main/docs/storage-architecture.md) - 存储容器（IndexedDB、Local Storage、Memory Cache、Settings）指南。数据流模式与使用说明。
- [**渲染架构**](https://github.com/johansan/notebook-navigator/blob/main/docs/rendering-architecture.md) - React 组件层级、基于 TanStack Virtual 的虚拟滚动、性能优化以及数据流。
- [**滚动编排**](https://github.com/johansan/notebook-navigator/blob/main/docs/scroll-orchestration.md) - 插件如何在树结构变化（标签可见性、设置等）时确保滚动定位准确。
- [**服务架构**](https://github.com/johansan/notebook-navigator/blob/main/docs/service-architecture.md) - 业务逻辑层：MetadataService、FileSystemOperations、ContentProviderRegistry。依赖注入模式与服务数据流。

## 5 键盘快捷键

| 按键 | 操作 |
| --- | --- |
| ↑/↓ | 在当前面板中上下导航 |
| ← | 导航面板：折叠或返回上级 / 列表面板：切换到导航面板 |
| → | 导航面板：展开或切换到列表面板 / 列表面板：切换到编辑器 |
| Tab | 导航面板：切换到列表面板 / 列表面板：切换到编辑器 / 搜索框：切换到列表面板 |
| Shift+Tab | 列表面板：切换到导航面板 / 搜索框：切换到导航面板 |
| Enter | 导航面板：打开文件夹笔记 / 列表面板：打开选中文件（需在设置中启用） / 搜索框：切换到列表面板 |
| Escape | 搜索框：关闭搜索并聚焦列表面板 |
| PageUp/PageDown | 在导航面板和列表面板中上下滚动 |
| Home/End | 跳转到当前面板的首项/末项 |
| Delete (Windows/Linux) / Backspace (macOS) | 删除选中项 |
| Cmd/Ctrl+A | 选中当前文件夹中的所有笔记 |
| Cmd/Ctrl+Click | 切换笔记选中状态 |
| Shift+Click | 选择一个范围内的笔记 |
| Shift+Home/End | 从当前位置选到首项/末项 |
| Shift+↑/↓ | 向上/向下扩展选择 |

> [!note] 所有键盘快捷键均可自定义。添加 VIM 风格导航（h,j,k,l）、替代按键以及修饰键组合的详细方法参见[第 8 节 - 自定义快捷键](#8-custom-hotkeys)。

## 6 同步设置与本地设置

Notebook Navigator 的许多设置旁边都有一个同步开关——一个云图标，可在"启用同步"和"禁用同步"之间切换。它控制每个设置的存储位置，以及是否在设备间共享。

### 6.1 同步机制

Obsidian 插件将配置存储在 `data.json` 中，位于 vault 文件夹内的 `.obsidian/plugins/notebook-navigator/data.json`。当你使用同步服务（如 [Obsidian Sync](https://obsidian.md/sync)、iCloud、GitHub、Dropbox 或 Google Drive）时，该文件会随 vault 的其余内容一起同步到所有设备。保存到 `data.json` 的任何设置都会传播到每个同步该 vault 的设备。

[![Screenshot 2026-02-18 at 22 58 05](https://private-user-images.githubusercontent.com/2589839/551794300-01d92458-1967-4008-acae-f722eee0d0a2.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3Nzg0ODA0MjEsIm5iZiI6MTc3ODQ4MDEyMSwicGF0aCI6Ii8yNTg5ODM5LzU1MTc5NDMwMC0wMWQ5MjQ1OC0xOTY3LTQwMDgtYWNhZS1mNzIyZWVlMGQwYTIucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDUxMSUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjA1MTFUMDYxNTIxWiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9NjNiYjUzZWY5YjVmZTUzNWZmMDA2NGIxMGQ5MTNjZDI1NTZhNGY1ZDZiNGRjNzQyNTQ3OTVlZTdlNGM1YmQ0NiZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmcmVzcG9uc2UtY29udGVudC10eXBlPWltYWdlJTJGcG5nIn0.TJwDKaigqIm8OtW8ejH4PYfTkSJ4HqPrkQtnx0ezljs)](https://private-user-images.githubusercontent.com/2589839/551794300-01d92458-1967-4008-acae-f722eee0d0a2.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3Nzg0ODA0MjEsIm5iZiI6MTc3ODQ4MDEyMSwicGF0aCI6Ii8yNTg5ODM5LzU1MTc5NDMwMC0wMWQ5MjQ1OC0xOTY3LTQwMDgtYWNhZS1mNzIyZWVlMGQwYTIucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDUxMSUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjA1MTFUMDYxNTIxWiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9NjNiYjUzZWY5YjVmZTUzNWZmMDA2NGIxMGQ5MTNjZDI1NTZhNGY1ZDZiNGRjNzQyNTQ3OTVlZTdlNGM1YmQ0NiZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmcmVzcG9uc2UtY29udGVudC10eXBlPWltYWdlJTJGcG5nIn0.TJwDKaigqIm8OtW8ejH4PYfTkSJ4HqPrkQtnx0ezljs)

当某项设置的同步**启用**（默认）时，值会保存到 `data.json`，并通过同步服务同步到所有设备。

[![Screenshot 2026-02-18 at 22 58 14](https://private-user-images.githubusercontent.com/2589839/551794426-f6f4c839-f8b8-42b5-be43-1cb6c78abdb3.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3Nzg0ODA0MjEsIm5iZiI6MTc3ODQ4MDEyMSwicGF0aCI6Ii8yNTg5ODM5LzU1MTc5NDQyNi1mNmY0YzgzOS1mOGI4LTQyYjUtYmU0My0xY2I2Yzc4YWJkYjMucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDUxMSUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjA1MTFUMDYxNTIxWiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9MDA2ZjE0NDY5YjFiMzllNjcyMmMyZjU2ZjNlMTM5YWE2NDBkYWFmMWY0MTQ1YmJkZmViNWFkOWM4M2M0NDAwZiZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmcmVzcG9uc2UtY29udGVudC10eXBlPWltYWdlJTJGcG5nIn0.HLg530rv5XUaI60cjWb3fcbR2PQqxGiKE3ymYzSln8k)](https://private-user-images.githubusercontent.com/2589839/551794426-f6f4c839-f8b8-42b5-be43-1cb6c78abdb3.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3Nzg0ODA0MjEsIm5iZiI6MTc3ODQ4MDEyMSwicGF0aCI6Ii8yNTg5ODM5LzU1MTc5NDQyNi1mNmY0YzgzOS1mOGI4LTQyYjUtYmU0My0xY2I2Yzc4YWJkYjMucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDUxMSUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjA1MTFUMDYxNTIxWiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9MDA2ZjE0NDY5YjFiMzllNjcyMmMyZjU2ZjNlMTM5YWE2NDBkYWFmMWY0MTQ1YmJkZmViNWFkOWM4M2M0NDAwZiZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmcmVzcG9uc2UtY29udGVudC10eXBlPWltYWdlJTJGcG5nIn0.HLg530rv5XUaI60cjWb3fcbR2PQqxGiKE3ymYzSln8k)  

当某项设置的同步**禁用**时，值会保存到 Obsidian 的本地存储中。本地存储是设备特定的，不包含在 vault 同步中。该设置在每台设备上将有独立的值。禁用同步时，当前值会复制到当前设备的本地存储，同时从 `data.json` 中移除该值，以防止其覆盖其他设备上的本地值。

如果你不使用同步服务，同步开关没有实际效果，因为 `data.json` 仅存储在本地。

## 7 搜索

Notebook Navigator 有两种搜索模式：过滤搜索和 Omnisearch。使用上下方向键或点击搜索图标在两者之间切换。可以在一个查询中组合文件名、属性、标签、日期和过滤器（如 `meeting .status=active #work @thisweek`）。

### 7.1 过滤搜索

在当前文件夹及其子文件夹中，按名称、标签、属性、日期、文件夹、扩展名和任务过滤文件。默认搜索模式。

**文件名**

- `word` - 匹配文件名包含"word"的笔记
- `word1 word2` - 要求每个词都匹配文件名
- `-word` - 排除文件名包含"word"的笔记

**标签**

- `#tag` - 包含该标签的笔记（也匹配嵌套标签，如 `#tag/subtag`）
- `#` - 仅包含有标签的笔记
- `-#tag` - 排除该标签的笔记
- `-#` - 仅包含无标签的笔记
- `#tag1 #tag2` - 同时匹配两个标签（隐式 AND）
- `#tag1 AND #tag2` - 同时匹配两个标签（显式 AND）
- `#tag1 OR #tag2` - 匹配任一标签
- `#a OR #b AND #c` - AND 优先级更高：匹配 `#a`，或同时匹配 `#b` 和 `#c`
- Cmd/Ctrl+Click 标签以 AND 方式添加，Cmd/Ctrl+Shift+Click 以 OR 方式添加

**属性**

- `.key` - 包含该属性键的笔记
- `.key=value` - 属性值包含 `value` 的笔记
- `."Reading Status"` - 包含空格的属性键（双引号）
- `."Reading Status"="In Progress"` - 键和值包含空格时必须双引号包裹
- `-.key` - 排除包含该属性键的笔记
- `-.key=value` - 排除属性值包含 `value` 的笔记
- Cmd/Ctrl+Click 属性以 AND 方式添加，Cmd/Ctrl+Shift+Click 以 OR 方式添加

**过滤器**

- `has:task` - 包含未完成任务的笔记
- `-has:task` - 排除包含未完成任务的笔记
- `folder:meetings` - 文件夹名包含 `meetings` 的笔记
- `folder:/work/meetings` - 仅在 `work/meetings` 中的笔记（不含子文件夹）
- `folder:/` - 仅在 vault 根目录中的笔记
- `-folder:archive` - 排除文件夹名包含 `archive` 的笔记
- `-folder:/archive` - 仅排除 `archive` 中的笔记（不含子文件夹）
- `ext:md` - 扩展名为 `md` 的笔记（也支持 `ext:.md`）
- `-ext:pdf` - 排除扩展名为 `pdf` 的笔记
- 可与标签、名称和日期组合（如 `folder:/work/meetings ext:md @thisweek`）

**日期**

- `@today` - 匹配今天的笔记（使用默认日期字段）
- `@yesterday`、`@last7d`、`@last30d`、`@thisweek`、`@thismonth` - 相对日期范围
- `@2026-02-07` - 匹配某一天（也支持 `@20260207`）
- `@2026` - 匹配某个日历年
- `@2026-02` 或 `@202602` - 匹配某个日历月
- `@2026-W05` 或 `@2026W05` - 匹配某个 ISO 周
- `@2026-Q2` 或 `@2026Q2` - 匹配某个日历季度
- `@13/02/2026` - 带分隔符的数字格式（`@07022026` 在有歧义时遵循你的区域设置）
- `@2026-02-01..2026-02-07` - 匹配日期范围（含两端，支持开放区间）
- `@c:...` 或 `@m:...` - 指定创建日期或修改日期
- `-@...` - 排除日期匹配

默认日期字段跟随当前排序方式。按名称排序时，日期字段在 设置 → 笔记 → 日期 → 按名称排序时 中配置。

**AND/OR 行为**

`AND` 和 `OR` 运算符仅在纯标签/属性查询中生效（即仅包含 `#tag`、`-#tag`、`#`、`-#`、`.key`、`-.key`、`.key=value` 或 `-.key=value` 过滤器的查询）。如果查询还包含名称、日期、任务过滤器、文件夹过滤器或扩展名过滤器，`AND` 和 `OR` 将作为文件名中的普通词匹配。

- 运算符查询：`#work OR .status=started`
- 混合查询：`#work OR ext:md`（`OR` 会在文件名中匹配）

### 7.2 Omnisearch

全文本搜索整个 vault，过滤范围为当前文件夹、子文件夹或选中的标签。需要安装 [Omnisearch](https://github.com/scambier/obsidian-omnisearch) 插件。如果未安装 Omnisearch，搜索会回退到过滤搜索。

笔记预览会显示 Omnisearch 结果摘要，替代默认预览文本。

**已知限制**

- **性能** - 在大型 vault 中搜索少于 3 个字符时可能较慢
- **路径 Bug** - 无法搜索包含非 ASCII 字符的路径，且不能正确搜索子路径
- **结果有限** - Omnisearch 搜索整个 vault，在过滤前返回有限数量的结果，因此如果其他位置有很多匹配，当前文件夹中的相关文件可能不会出现
- **预览文本** - 笔记预览被 Omnisearch 结果摘要替代，如果实际搜索匹配出现在文件的其他位置，可能不会显示高亮

## 8 自定义快捷键

编辑 `.obsidian/plugins/notebook-navigator/data.json` 来自定义 Notebook Navigator 快捷键。打开文件并找到 `keyboardShortcuts` 部分。每个条目将一个操作映射到一个或多个按键绑定：

```
"pane:move-up": [ { "key": "ArrowUp", "modifiers": [] }, { "key": "K", "modifiers": [] } ]
```

可以为每个操作添加多个绑定以支持替代按键，如上面 `ArrowUp` 和 `K` 的示例。在同一个条目中组合修饰键，例如 `"modifiers": ["Mod", "Shift"]`。不支持键盘序列（如 `gg` 或 `dd`）。编辑文件后需重新加载 Obsidian。

### 8.1 修饰键

| 修饰键 | 按键 |
| --- | --- |
| `Mod` | Cmd (macOS) / Ctrl (Win/Linux) |
| `Alt` | Alt / Option |
| `Shift` | Shift |
| `Ctrl` | Control（跨平台建议使用 `Mod`） |

### 8.2 可用操作

| 操作 | 默认按键 |
| --- | --- |
| `pane:move-up` | ArrowUp |
| `pane:move-down` | ArrowDown |
| `pane:page-up` | PageUp |
| `pane:page-down` | PageDown |
| `pane:home` | 主页 |
| `pane:end` | End |
| `pane:delete-selected` | Delete, Backspace |
| `navigation:collapse-or-parent` | ArrowLeft |
| `navigation:expand-or-focus-list` | ArrowRight |
| `navigation:focus-list` | Tab |
| `list:focus-navigation` | ArrowLeft, Shift+Tab |
| `list:focus-editor` | ArrowRight, Tab |
| `list:select-all` | Mod+A |
| `list:extend-selection-up` | Shift+ArrowUp |
| `list:extend-selection-down` | Shift+ArrowDown |
| `list:range-to-start` | Shift+Home |
| `list:range-to-end` | Shift+End |
| `search:focus-list` | Tab, Enter |
| `search:focus-navigation` | Shift+Tab |
| `search:close` | Escape |

## 9 命令

在 Obsidian 的快捷键设置中为这些命令设置自定义快捷键：

**视图与导航**

- `Notebook Navigator: Open` 在左侧边栏打开 Notebook Navigator。如果已打开，则将键盘焦点移到列表面板。**建议：** 绑定到 `Cmd/Ctrl+Shift+E` 等快捷键，将焦点移到列表面板——这对完整键盘导航至关重要
- `Notebook Navigator: Toggle left sidebar` 切换左侧边栏。打开时，将左侧边栏视图设置为 Notebook Navigator（与 Obsidian 内置的"切换左侧边栏"命令不同，后者会恢复之前的左侧边栏视图）
- `Notebook Navigator: Open homepage` 打开 Notebook Navigator 视图并加载设置中配置的主页目标
- `Notebook Navigator: Select vault profile` 打开弹窗切换 vault 配置
- `Notebook Navigator: Reveal file` 在导航器中显示当前文件。展开父文件夹并滚动到文件。如果你关闭了"自动显示活动笔记"设置，这个命令可手动显示笔记。**建议：** 绑定到 `Cmd/Ctrl+Shift+R` 等快捷键，快速将选中的文件夹或标签切换到当前文件
- `Notebook Navigator: Open all files` 打开当前选中文件夹或标签中的所有笔记。打开 15 个及以上文件时会弹出确认对话框
- `Notebook Navigator: Navigate to folder` 搜索对话框，跳转到任意文件夹
- `Notebook Navigator: Navigate to tag` 搜索对话框，跳转到任意标签
- `Notebook Navigator: Navigate to property` 搜索对话框，跳转到任意属性键或值
- `Notebook Navigator: Navigate back` 在导航历史中返回上一个文件夹、标签或属性选择
- `Notebook Navigator: Navigate forward` 在导航历史中前进到下一个文件夹、标签或属性选择
- `Notebook Navigator: Add to shortcuts` 将当前文件、文件夹、标签或属性添加到快捷方式，或从中移除
- `Notebook Navigator: Open shortcut 1-9` 按位置打开快捷方式列表中的快捷方式
- `Notebook Navigator: Search` 打开快速搜索框，如已打开则聚焦。搜索内容在会话间保持。**建议：** 绑定到 `Cmd/Ctrl+Shift+S` 等快捷键，快速过滤文件
- `Notebook Navigator: Search in vault root` 选择 vault 根文件夹并打开搜索（需启用"显示根文件夹"）

**选择**

- `Notebook Navigator: Select next file` 将选择移动到当前文件夹或标签视图中的下一个文件。遵循自定义排序。**建议：** 绑定到 `Option+Cmd+Right` 等快捷键，快速跳到列表中的下一个文件
- `Notebook Navigator: Select previous file` 将选择移动到当前文件夹或标签视图中的上一个文件。遵循自定义排序。**建议：** 绑定到 `Option+Cmd+Left` 等快捷键，快速跳到列表中的上一个文件

**布局与显示**

- `Notebook Navigator: Toggle dual pane layout` 切换单栏/双栏布局（桌面端）。**建议：** 绑定到 `Cmd/Ctrl+Shift+A` 等快捷键，快速在单栏和双栏布局之间切换
- `Notebook Navigator: Toggle dual pane orientation` 在水平和垂直方向之间切换双栏方向
- `Notebook Navigator: Toggle descendants` 切换文件夹和标签的子文件夹/后代笔记显示。**建议：** 绑定到 `Cmd/Ctrl+Shift+D` 等快捷键，快速切换子文件夹/后代笔记的显示
- `Notebook Navigator: Toggle hidden items` 显示或隐藏已隐藏的文件夹、标签和笔记
- `Notebook Navigator: Toggle tag sort` 在字母排序和频率排序之间切换标签排序方式
- `Notebook Navigator: Toggle tags by selection` 切换是否将标签限制为所选文件夹或属性中笔记的标签
- `Notebook Navigator: Toggle properties by selection` 切换是否将属性限制为所选文件夹或标签中笔记的属性
- `Notebook Navigator: Toggle compact mode` 在标准和紧凑列表模式之间切换
- `Notebook Navigator: Toggle pinned section` 显示或隐藏列表面板中置顶的笔记
- `Notebook Navigator: Collapse / expand all items` 根据当前状态折叠或展开所有项目。当启用"保持选中项展开"（默认开启）时，除当前文件夹外所有文件夹都会被折叠。这在搜索文档时非常方便，可以保持导航树整洁

**日历**

- `Notebook Navigator: Toggle calendar` 开关日历。**建议：** 绑定到 `Cmd/Ctrl+Shift+C` 等快捷键，快速显示日历
- `Notebook Navigator: Open daily note` 根据日历设置打开今天的日记。如不存在则创建
- `Notebook Navigator: Open weekly note` 打开当前周记。如不存在则创建
- `Notebook Navigator: Open monthly note` 打开当前月记。如不存在则创建
- `Notebook Navigator: Open quarterly note` 打开当前季记。如不存在则创建
- `Notebook Navigator: Open yearly note` 打开当前年记。如不存在则创建

**文件操作**

> [!warning] Obsidian 没有"当前文件夹或标签"的概念，因此默认在 Obsidian 中创建笔记时，它们会被创建在根文件夹、当前文件所在文件夹或指定文件夹中。使用 Notebook Navigator 时，你总是希望在新笔记创建在当前选中的文件夹或标签中，所以你应该做的第一件事就是将 `Cmd/Ctrl+N` 绑定到 `Notebook Navigator: Create new note`，这样新笔记总是创建在当前选中的文件夹或标签中。移动和删除文件也是如此。这就是为什么使用 Notebook Navigator 时应该用这些命令而不是 Obsidian 内置命令的原因。

- `Notebook Navigator: Create new note` 在当前选中文件夹中创建笔记。**建议：** 将 `Cmd/Ctrl+N` 绑定到此命令（先取消 Obsidian 默认的"创建新笔记"绑定）
- `Notebook Navigator: Create new note from template` 在当前选中文件夹中从模板创建笔记（需要 Templater）
- `Notebook Navigator: Move files` 将选中文件移动到其他文件夹。自动选择当前文件夹中的下一个文件
- `Notebook Navigator: Convert to folder note` 创建与文件名匹配的文件夹，并将文件作为文件夹笔记移入其中
- `Notebook Navigator: Set as folder note` 将活动文件重命名为其文件夹笔记名称
- `Notebook Navigator: Detach folder note` 分离所选文件夹中的文件夹笔记并重命名
- `Notebook Navigator: Pin all folder notes` 置顶所有文件夹中的文件夹笔记。仅当文件夹笔记功能已启用且至少存在一个未置顶的文件夹笔记时可见
- `Notebook Navigator: Delete files` 删除选中文件。自动选择当前文件夹中的下一个文件

**标签操作**

- `Notebook Navigator: Add tag to selected files` 弹窗为选中文件添加标签。支持创建新标签
- `Notebook Navigator: Set property on selected files` 弹窗为选中文件设置属性
- `Notebook Navigator: Remove tag from selected files` 弹窗移除特定标签。如果只有一个标签则立即移除
- `Notebook Navigator: Remove all tags from selected files` 清除选中文件的所有标签（需确认）

**维护**

- `Notebook Navigator: Rebuild cache` 重建 Notebook Navigator 本地缓存。遇到标签缺失、预览不正确或特征图片缺失时使用

### 9.1 命令 ID

| 命令 ID | 命令名称 |
| --- | --- |
| `notebook-navigator:open` | Notebook Navigator: Open |
| `notebook-navigator:toggle-left-sidebar` | Notebook Navigator: Toggle left sidebar |
| `notebook-navigator:open-homepage` | Notebook Navigator: Open homepage |
| `notebook-navigator:select-profile` | Notebook Navigator: Select vault profile |
| `notebook-navigator:select-profile-1` | Notebook Navigator: Select vault profile 1 |
| `notebook-navigator:select-profile-2` | Notebook Navigator: Select vault profile 2 |
| `notebook-navigator:select-profile-3` | Notebook Navigator: Select vault profile 3 |
| `notebook-navigator:reveal-file` | Notebook Navigator: Reveal file |
| `notebook-navigator:open-all-files` | Notebook Navigator: Open all files |
| `notebook-navigator:navigate-to-folder` | Notebook Navigator: Navigate to folder |
| `notebook-navigator:navigate-to-tag` | Notebook Navigator: Navigate to tag |
| `notebook-navigator:navigate-to-property` | Notebook Navigator: Navigate to property |
| `notebook-navigator:navigate-back` | Notebook Navigator: Navigate back |
| `notebook-navigator:navigate-forward` | Notebook Navigator: Navigate forward |
| `notebook-navigator:add-shortcut` | Notebook Navigator: Add to shortcuts |
| `notebook-navigator:open-shortcut-1` | Notebook Navigator: Open shortcut 1 |
| `notebook-navigator:open-shortcut-2` | Notebook Navigator: Open shortcut 2 |
| `notebook-navigator:open-shortcut-3` | Notebook Navigator: Open shortcut 3 |
| `notebook-navigator:open-shortcut-4` | Notebook Navigator: Open shortcut 4 |
| `notebook-navigator:open-shortcut-5` | Notebook Navigator: Open shortcut 5 |
| `notebook-navigator:open-shortcut-6` | Notebook Navigator: Open shortcut 6 |
| `notebook-navigator:open-shortcut-7` | Notebook Navigator: Open shortcut 7 |
| `notebook-navigator:open-shortcut-8` | Notebook Navigator: Open shortcut 8 |
| `notebook-navigator:open-shortcut-9` | Notebook Navigator: Open shortcut 9 |
| `notebook-navigator:search` | Notebook Navigator: Search |
| `notebook-navigator:search-vault` | Notebook Navigator: Search in vault root |
| `notebook-navigator:toggle-dual-pane` | Notebook Navigator: Toggle dual pane layout |
| `notebook-navigator:toggle-dual-pane-orientation` | Notebook Navigator: Toggle dual pane orientation |
| `notebook-navigator:toggle-calendar` | Notebook Navigator: Toggle calendar |
| `notebook-navigator:open-daily-note` | Notebook Navigator: Open daily note |
| `notebook-navigator:open-weekly-note` | Notebook Navigator: Open weekly note |
| `notebook-navigator:open-monthly-note` | Notebook Navigator: Open monthly note |
| `notebook-navigator:open-quarterly-note` | Notebook Navigator: Open quarterly note |
| `notebook-navigator:open-yearly-note` | Notebook Navigator: Open yearly note |
| `notebook-navigator:toggle-descendants` | Notebook Navigator: Toggle descendants |
| `notebook-navigator:toggle-hidden` | Notebook Navigator: Toggle hidden items (folders, tags, notes) |
| `notebook-navigator:toggle-tag-sort` | Notebook Navigator: Toggle tag sort |
| `notebook-navigator:toggle-tags-by-selection` | Notebook Navigator: Toggle tags by selection |
| `notebook-navigator:toggle-properties-by-selection` | Notebook Navigator: Toggle properties by selection |
| `notebook-navigator:toggle-compact-mode` | Notebook Navigator: Toggle compact mode |
| `notebook-navigator:toggle-pinned-section` | Notebook Navigator: Toggle pinned section |
| `notebook-navigator:collapse-expand` | Notebook Navigator: Collapse / expand all items |
| `notebook-navigator:new-note` | Notebook Navigator: Create new note |
| `notebook-navigator:new-note-from-template` | Notebook Navigator: Create new note from template |
| `notebook-navigator:move-files` | Notebook Navigator: Move files |
| `notebook-navigator:select-next-file` | Notebook Navigator: Select next file |
| `notebook-navigator:select-previous-file` | Notebook Navigator: Select previous file |
| `notebook-navigator:convert-to-folder-note` | Notebook Navigator: Convert to folder note |
| `notebook-navigator:set-as-folder-note` | Notebook Navigator: Set as folder note |
| `notebook-navigator:detach-folder-note` | Notebook Navigator: Detach folder note |
| `notebook-navigator:pin-all-folder-notes` | Notebook Navigator: Pin all folder notes (requires folder notes enabled and an unpinned folder note) |
| `notebook-navigator:delete-files` | Notebook Navigator: Delete files |
| `notebook-navigator:add-tag` | Notebook Navigator: Add tag to selected files |
| `notebook-navigator:set-property` | Notebook Navigator: Set property on selected files |
| `notebook-navigator:remove-tag` | Notebook Navigator: Remove tag from selected files |
| `notebook-navigator:remove-all-tags` | Notebook Navigator: Remove all tags from selected files |
| `notebook-navigator:rebuild-cache` | Notebook Navigator: Rebuild cache |

## 10 功能

### 10.1 界面

- **双栏布局** - 导航面板（文件夹/标签/属性）和列表面板（文件）
- **单栏模式** - 导航和列表视图，带动画过渡
- **可调整面板大小** - 水平或垂直分割方向
- **独立 UI 缩放** - 缩放 Notebook Navigator 而不影响 Obsidian 的缩放
- **启动视图** - 导航优先或列表优先
- **多语言支持** - 21 种语言，支持 RTL 布局
- **界面图标集** - 可自定义插件中的 UI 图标

### 10.2 导航

- **Vault 配置** - 多个过滤视图，每个配置有独立的隐藏文件夹/标签/笔记、文件可见性、横幅和快捷方式
- **快捷方式** - 笔记、文件夹、标签和已保存的搜索，支持置顶和重新排序
- **最近笔记/文件** - 按 vault 配置存储的最近项目区域，可选择通过快捷方式置顶
- **日历** - 日记日历，支持日期选择、特征图片预览和垂直分割
- **文件夹树** - 展开/折叠导航，支持手动排序根文件夹
- **标签树** - 层级标签，支持配置根标签排序
- **属性浏览器** - 按键和值浏览文件属性，显示文件计数、自定义颜色、图标，支持拖放
- **自动显示活动文件** - 文件夹展开并滚动到选中项
- **键盘与命令** - 可配置快捷键、选择历史前进/后退命令、下一个/上一个文件命令、打开快捷方式 1-9 命令

### 10.3 组织管理

- **置顶笔记** - 将重要笔记保持在文件夹和标签顶部
- **文件夹笔记** - 设置/分离文件夹笔记、置顶文件夹笔记、在新标签页打开选项
- **标签操作** - 添加/移除/清除标签、重命名/删除标签、在标签中创建笔记、拖放标签层级
- **自定义排序和分组** - 按文件夹或标签覆盖排序/分组设置
- **按文件夹/标签设置外观** - 标题行、预览行、紧凑模式、后代切换
- **隐藏内容** - 隐藏文件夹/标签/笔记/文件，支持模式匹配、frontmatter 属性和基于标签的过滤，按 vault 配置独立设置
- **颜色和图标系统** - 文件夹/标签/属性/文件颜色、图标包、emoji/Lucide 图标、frontmatter 读写、按文件名和文件类型类别映射图标
- **命名警告** - 命名文件和文件夹时，对禁止的文件系统字符和会破坏 Obsidian 链接的字符发出警告

### 10.4 文件显示

- **笔记预览** - 1-5 行预览，可选去除 HTML
- **缩略图** - 特征图片以及自动生成并存储在元数据缓存中的缩略图
- **外部图片** - 可选下载外部图片和 YouTube 缩略图
- **日期分组** - 按日期排序时，可将笔记按今天、昨天、7 天之前、30 天之前、月份和年份分组
- **Frontmatter 支持** - 从 frontmatter 字段读取笔记名称和时间戳
- **笔记元数据** - 在文件列表中显示修改日期和标签
- **自定义属性** - 在文件列表中显示 frontmatter 属性或字数，支持按文件夹/标签覆盖和自定义颜色
- **父文件夹显示** - 可选在文件列表中显示父文件夹名称和图标
- **紧凑模式** - 禁用预览、日期和图片时的紧凑显示
- **可点击标签** - 文件列表中的标签可直接导航到该标签

### 10.5 效率工具

- **搜索** - 按文件名、标签、属性、日期、文件夹、扩展名和任务过滤，支持 AND/OR/排除
- **Omnisearch 集成** - 通过 [Omnisearch](https://github.com/scambier/obsidian-omnisearch) 进行全文本搜索
- **拖放** - 文件移动、标签添加、快捷方式分配、标签树重新挂载、弹簧文件夹
- **上下文菜单** - 创建笔记/文件夹/Canvas/Bases/绘图，执行文件/标签操作
- **绘图** - 从导航和列表面板菜单创建 Excalidraw 和 Tldraw 绘图
- **模板** - 通过 Templater 插件从模板创建新笔记
- **文件操作** - 创建、重命名、复制、移动、回收文件和文件夹
- **过滤** - 通过模式匹配和 frontmatter 属性排除文件夹/标签/笔记/文件

## 11 网络使用声明

Notebook Navigator 本地运行，但部分功能会从 Obsidian 发起 HTTP 请求。

### 11.1 版本更新检查（可选）

- **设置：** "启动时检查新版本"
- **请求：** `https://api.github.com/repos/johansan/notebook-navigator/releases/latest`
- **频率：** 启动时最多每 24 小时一次
- **数据：** 发送标准 HTTP 元数据；不包含 vault 内容

### 11.2 图标包下载（可选）

- **设置：** 在图标包标签页中启用图标包
- **请求：** `https://raw.githubusercontent.com/johansan/notebook-navigator/main/icon-assets/...`（清单、字体、元数据）
- **存储：** 本地存储在 IndexedDB 中

### 11.3 外部图片和 YouTube 缩略图

- **特征图片（可选）：** 由"下载外部图片"设置控制。下载远程图片和 YouTube 缩略图作为特征图片，并本地存储在 IndexedDB 中。
- **欢迎弹窗（首次启动）：** 从 `https://raw.githubusercontent.com/johansan/notebook-navigator/main/images/youtube-thumbnail.jpg` 加载静态缩略图。
- **更新日志弹窗（更新时/手动打开时）：** 从 `https://raw.githubusercontent.com/johansan/notebook-navigator/main/images/version-banners/<id>.jpg` 加载版本横幅图片，用于包含横幅的更新说明。
- **更新日志弹窗（更新时/手动打开时）：** 从 `https://img.youtube.com/vi/<id>/...` 加载 YouTube 缩略图，用于包含 YouTube 链接的更新说明。
- Notebook Navigator 不会将笔记内容、文件名或标签发送到 Notebook Navigator 服务器。
- 对 GitHub、YouTube 和任何外部图片主机的请求直接从你的设备发出，包含标准 HTTP 元数据（IP 地址、user-agent 等）。
- 下载的图标包和图片本地存储（IndexedDB）。最近笔记/文件和 UI 状态本地存储（Obsidian 本地存储）。

## 12 Star 历史

[![Star History Chart](https://camo.githubusercontent.com/cd1d3d82961766284d710361626dbd00de0b367359d9124510a21c62fcdaa4be/68747470733a2f2f6170692e737461722d686973746f72792e636f6d2f7376673f7265706f733d6a6f68616e73616e2f6e6f7465626f6f6b2d6e6176696761746f7226747970653d64617465266c6567656e643d746f702d6c656674)](https://www.star-history.com/#johansan/notebook-navigator&type=date&legend=top-left)

## 13 联系方式

Notebook Navigator 由 [Johan Sanneblad](https://www.linkedin.com/in/johansan/) 开发和维护。Johan 拥有软件开发博士学位，曾为 Apple、Electronic Arts、Google、Microsoft、Lego、SKF、Volvo Cars、Volvo Group 和 Yamaha 等公司从事创新开发工作。

欢迎在 [LinkedIn](https://www.linkedin.com/in/johansan/) 上与我联系。

## 14 问题或反馈？

**[加入我们的 Discord](https://discord.gg/6eeSUvzEJr)** 获取支持和讨论，或在 [GitHub 仓库](https://github.com/johansan/notebook-navigator) 上提交 issue。

## 15 许可证

本项目基于 GNU General Public License v3.0 许可——详见 [LICENSE](https://github.com/johansan/notebook-navigator/blob/main/LICENSE) 文件。