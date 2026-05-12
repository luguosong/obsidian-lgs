---
title: Mastering Notebook Navigator
source: https://www.youtube.com/watch?v=BewIlG8wLAM
author: Johan Sanneblad
date: 2026-01-04
tags:
  - Obsidian
  - 插件
  - Notebook-Navigator
  - 文件管理
---

# Mastering Notebook Navigator

> [!info] 视频信息
> - **标题**：Mastering Notebook [[Navigator]] for [[Obsidian]]
> - **作者**：Johan Sanneblad（[YouTube 频道](https://www.youtube.com/@JohanSanneblad)）
> - **发布日期**：2026-01-04
> - **观看量**：35,000+
> - **时长**：约 30 分钟
> - **链接**：[YouTube](https://www.youtube.com/watch?v=BewIlG8wLAM)
> - **官网**：[notebooknavigator.com](https://notebooknavigator.com/)
> - **GitHub**：[johansan/notebook-navigator](https://github.com/johansan/notebook-navigator)

## 插件简介

Notebook [[Navigator]] 是 [[Obsidian]] 的现代文件管理器替代品，用**双窗格界面**取代默认的文件浏览器，灵感来自 Apple Notes / Bear / Evernote 风格。免费开源，支持 100,000+ 笔记的库。

## 视频章节与要点

### 0:26 — 安装

1. 打开 [[Settings]] → Community plugins
2. 搜索 [["Notebook]] [[Navigator]]"
3. 点击 Install → Enable

> [!tip] 安装后记得**禁用默认的 File Explorer 插件**，避免界面冲突。

### 1:05 — 配置布局

- **双窗格布局**：左侧为文件夹导航树，右侧为文件列表
- 可拖拽调整窗格宽度
- `Cmd/Ctrl + Shift + A` 在单窗格/双窗格之间切换
- `Tab` 键在左右窗格之间快速切换焦点

### 3:37 — 显示子文件夹笔记

- 启用 "Show notes from descendants" 后，当前文件夹会**同时展示所有子文件夹中的笔记**
- 适合扁平化浏览，不用逐层展开文件夹
- 每个文件夹可单独配置是否显示子文件夹内容

### 5:46 — 紧凑模式

- **Compact mode**（Slim mode）：隐藏预览文本，只显示文件名
- 适合笔记数量多、需要快速扫描的场景
- 可按文件夹/标签分别设置是否使用紧凑模式

### 8:06 — 快捷键与热键

- 完全键盘导航，支持自定义快捷键
- 上下箭头浏览笔记列表
- 回车打开笔记
- 搜索模式切换：用**上下箭头键**或点击搜索图标在 filter search 和 Omnisearch 之间切换

### 12:20 — 自定义导航

- 支持自定义文件夹树的显示方式
- **Folder notes**：文件夹可关联笔记，点击即打开
- **自动展开并滚动**到当前活动文件（auto-reveal）
- 每个文件夹/标签可单独设置排序方式和外观

### 13:43 — 自定义列表窗格

- 可配置预览行数（1-5 行）
- 支持自动生成缩略图（配合 Featured Image 插件）
- **日期分组**：Today / Yesterday / This Week / Last Week
- 可点击的标签，支持自定义颜色

### 15:39 — 搜索与标签筛选

- **两种搜索模式**：
  - Filter search：内置过滤搜索
  - Omnisearch：集成 Omnisearch 插件
- **标签管理**：
  - 支持层级标签，如 `#project/work/urgent`
  - 拖放添加/移除标签
  - **收藏标签**：固定常用标签到专用区域
  - 拖到 "Untagged" 可批量移除标签
  - 支持隐藏标签层级（隐藏 `archive` 会同时隐藏 `archive/2024` 等）

### 19:32 — 固定笔记

- **Pinned notes**：将重要笔记固定在列表顶部
- 快速访问高频使用的笔记
- 固定状态持久化保存

### 23:47 — 高级自定义

- 每个文件夹/标签可独立配置显示选项
- 自定义排序规则
- 拖放排序和移动文件
- 上下文菜单提供精确的标签操作

### 27:08 — 从 Frontmatter 读取数据

- 可从笔记的 frontmatter 中提取字段显示在列表中
- 支持显示 Feature Image（从 frontmatter 或第一张嵌入图片）
- 实现类似数据库的视图效果

## 核心特性一览

| 特性 | 说明 |
|------|------|
| 双窗格界面 | 左侧文件夹树 + 右侧文件列表，可拖拽调整 |
| 富文本预览 | 可配置 1-5 行预览文本，自动缩略图 |
| 标签管理 | 层级标签、收藏标签、拖放操作、颜色自定义 |
| 键盘导航 | 完整键盘操作，快捷键可自定义 |
| 搜索过滤 | Filter search + Omnisearch 双模式 |
| 固定笔记 | 重要笔记置顶 |
| Frontmatter 集成 | 读取属性字段，显示缩略图 |
| 移动端优化 | 适配手机端操作 |
| 高性能 | 支持 100,000+ 笔记 |

## 关键快捷键

| 快捷键 | 功能 |
|--------|------|
| `Cmd/Ctrl + Shift + A` | 切换单/双窗格 |
| `Tab` | 切换左右窗格焦点 |
| `↑` / `↓` | 浏览笔记列表 / 切换搜索模式 |
| `Enter` | 打开选中笔记 |

## 相关资源

- 官方文档：[notebooknavigator.com/docs](https://notebooknavigator.com/)
- GitHub 仓库：[johansan/notebook-navigator](https://github.com/johansan/notebook-navigator)
- Discord 社区：通过官网链接加入
- 中文介绍（繁体）：[notebooknavigator.com/zh-tw](https://notebooknavigator.com/zh-tw/docs.html)
