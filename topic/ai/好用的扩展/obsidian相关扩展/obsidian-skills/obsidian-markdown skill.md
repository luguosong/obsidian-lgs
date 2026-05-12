---
title: obsidian-markdown skill
description: 创建和编辑 Obsidian Flavored Markdown，支持 wikilinks、callout、properties 等
created: 2026-05-10
tags:
  - ai
  - claude-code
  - obsidian
  - skill
  - markdown
---

# obsidian-markdown

> [!summary]
> 创建和编辑 **[[Obsidian]] Flavored Markdown（OFM）** 文件，覆盖 wikilinks、嵌入、callout、properties、标签、块引用、数学公式等 [[Obsidian]] 专属语法。

**触发词**：`创建 Obsidian 笔记`、`wikilink`、`callout`、`frontmatter`、`properties`、`.md 文件`

## 与标准 Markdown 的区别

OFM 在标准 Markdown 之上扩展了 [[Obsidian]] 独有功能：wikilinks（双向链接）、嵌入（`![[...]]`）、callout（`> [!type]`）、properties（YAML frontmatter）、标签（`#tag`）。

## 核心语法

### Wikilinks（双向链接）

```markdown
[[笔记名称]]                    <!-- 基础链接 -->
[[笔记名称|显示文本]]            <!-- 自定义显示 -->
[[文件夹/笔记名称]]              <!-- 带路径 -->
[[笔记名称#标题]]                <!-- 链接到标题 -->
[[笔记名称#^块引用ID]]           <!-- 链接到块 -->
```

### 嵌入（Embeds）

在 wikilink 前加 `!`：

```markdown
![[笔记名称]]                   <!-- 嵌入笔记 -->
![[笔记名称#标题]]               <!-- 嵌入章节 -->
![[图片.png]]                   <!-- 嵌入图片 -->
![[图片.png|300]]               <!-- 图片指定宽度 -->
![[图片.png|300x200]]           <!-- 图片指定宽高 -->
![[音频.mp3]]                   <!-- 嵌入音频 -->
![[视频.mp4]]                   <!-- 嵌入视频 -->
![[文档.pdf]]                   <!-- 嵌入 PDF -->
```

### Callouts（标注块）

```markdown
> [!note] 标题
> 内容

> [!warning] 警告
> 内容

> [!danger] 危险
> 内容

> [!info]
> 无自定义标题时用类型名
```

**支持的类型**：`note`、`tip`、`important`、`warning`、`danger`、`info`、`success`、`question`、`quote`、`example`、`abstract`、`todo`、`bug`

**可折叠**：

```markdown
> [!tip]- 默认折叠
> 点击展开

> [!tip]+ 默认展开
> 已展开
```

### Properties（YAML Frontmatter）

```yaml
---
title: "笔记标题"
date: 2024-01-15
tags:
  - 标签1
  - 标签2
aliases:
  - 别名1
cssclasses:
  - wide-page
status: draft
rating: 4
---
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `title` | 文本 | 覆盖文件名显示 |
| `tags` | 列表 | 标签 |
| `aliases` | 列表 | 别名，影响搜索 |
| `cssclasses` | 列表 | 自定义 CSS |
| `date` / `created` | 日期 | 创建日期 |
| `modified` | 日期 | 修改日期 |

### 标签（Tags）

```markdown
#标签                  <!-- 行内标签 -->
#父标签/子标签          <!-- 嵌套标签 -->
#多词标签用连字符        <!-- 连字符替代空格 -->
```

### 块引用（Block References）

```markdown
这是一个段落。^my-block-id

<!-- 引用 -->
![[笔记名#^my-block-id]]
```

### 数学公式

```markdown
行内：$E = mc^2$

块级：
$$
\sum_{i=1}^{n} x_i = \frac{n(n+1)}{2}
$$
```

## 使用示例

```
# 创建笔记
帮我创建一篇 Obsidian 笔记，主题是 [主题]
要求：包含 frontmatter、wikilinks、callout

# 批量整理
帮我把普通 > 引用块转换为 Callout 格式

# 知识图谱
创建一组互相链接的笔记，形成知识网络
```

## 协作关系

- [[defuddle skill]] → 提取网页内容 → 本 skill 格式化
- 本 skill → [[obsidian-cli skill]] 写入 vault
- 本 skill 的 properties → [[obsidian-bases skill]] 读取查询

## 参考链接

- [Obsidian Flavored Markdown 文档](https://help.obsidian.md/obsidian-flavored-markdown)
- [Callout 语法参考](https://help.obsidian.md/Editing+and+formatting/Callouts)
- [Properties 文档](https://help.obsidian.md/Editing+and+formatting/Properties)

---

→ 返回 [[obsidian-skills 套件总览]]

## 相关笔记

- [[json-canvas skill]]
- [[Superpowers 使用手册与最佳实践 — 实施计划]]
- [[axton-obsidian-visual-skills 套件总览]]
- [[excalidraw-diagram skill]]
