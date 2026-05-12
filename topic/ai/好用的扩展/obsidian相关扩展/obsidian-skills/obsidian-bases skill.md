---
title: obsidian-bases skill
description: 创建和编辑 Obsidian Bases 数据库视图，支持表格/看板/画廊、过滤、公式和汇总
created: 2026-05-10
tags:
  - ai
  - claude-code
  - obsidian
  - skill
  - bases
  - database
---

# obsidian-bases

> [!summary]
> 创建和编辑 **[[Obsidian]] Bases**（`.base`）文件——[[Obsidian]] 内置的类数据库功能，将 vault 笔记以表格、看板、画廊等视图呈现，支持过滤、排序、公式计算和汇总统计。

**触发词**：`Obsidian Bases`、`.base 文件`、`数据库视图`、`过滤器`、`看板视图`、`表格视图`、`公式列`

> [!info] [[核心概念]]
> Bases 是对 vault 中 Markdown 笔记的**结构化查询视图**。笔记的 `properties`（frontmatter）字段就是数据列，`.base` 文件定义如何展示。

## 视图类型

| 类型 | 说明 | 适用场景 |
|------|------|---------|
| `table` | 表格视图 | 数据对比、列表管理 |
| `board` | 看板视图 | 任务管理、状态跟踪 |
| `gallery` | 画廊视图 | 书单、资源库 |
| `list` | 列表视图 | 快速浏览 |
| `calendar` | 日历视图 | 日程、日志 |

## .base 文件结构

```json
{
  "views": [
    {
      "id": "view-1",
      "name": "所有笔记",
      "type": "table",
      "filter": {},
      "order": []
    }
  ]
}
```

## 过滤器（Filters）

用 `and` / `or` 组合条件：

```json
{
  "filter": {
    "and": [
      { "field": "tags", "operator": "contains", "value": "项目" },
      { "field": "status", "operator": "is", "value": "进行中" }
    ]
  }
}
```

| 操作符 | 说明 |
|--------|------|
| `is` / `is-not` | 精确等于 / 不等于 |
| `contains` / `does-not-contain` | 包含 / 不包含 |
| `starts-with` / `ends-with` | 前缀 / 后缀 |
| `is-empty` / `is-not-empty` | 空 / 非空 |
| `is-before` / `is-after` | 早于 / 晚于（日期） |
| `greater-than` / `less-than` | 大于 / 小于（数字） |

支持变量：`{{today}}` 表示当天日期。

## 排序（Order）

```json
{
  "order": [
    { "field": "priority", "direction": "desc" },
    { "field": "date", "direction": "asc" }
  ]
}
```

## 公式（Formulas）

```json
{
  "columns": [
    {
      "id": "progress",
      "name": "完成进度",
      "type": "formula",
      "formula": "round(completed / total * 100) + \"%\""
    }
  ]
}
```

| 函数 | 说明 | 示例 |
|------|------|------|
| `round(n)` / `floor(n)` / `ceil(n)` | 取整 | `round(3.7)` → `4` |
| `abs(n)` | 绝对值 | `abs(-5)` → `5` |
| `length(s)` | 长度 | `length(tags)` |
| `contains(a, b)` | 包含判断 | `contains(tags, "重要")` |
| `if(cond, a, b)` | 条件 | `if(done, "✅", "⏳")` |
| `now()` | 当前时间 | `now()` |
| `date(s)` | 解析日期 | `date(created)` |
| `dateAdd(d, n, u)` | 日期加减 | `dateAdd(date, 7, "days")` |
| `dateDiff(a, b, u)` | 日期差 | `dateDiff(due, now(), "days")` |
| `format(d, s)` | 格式化日期 | `format(date, "YYYY-MM-DD")` |

## 汇总（Summaries）

```json
{
  "summaries": [
    { "field": "rating", "type": "average" },
    { "field": "status", "type": "count-unique" }
  ]
}
```

| 类型 | 说明 |
|------|------|
| `count` / `count-all` / `count-unique` | 计数 |
| `sum` / `average` | 求和 / 平均 |
| `min` / `max` | 最小 / 最大 |

## 使用示例

```
# 任务看板
创建任务看板，按状态分组，显示优先级和截止日期

# 读书画廊
创建读书清单画廊，只显示评分 4 分以上

# 日历视图
创建日历视图展示每日日记
```

## 协作关系

- [[obsidian-markdown skill]] 的 properties → 本 skill 读取查询
- 本 skill 生成的 `.base` 文件 → [[obsidian-cli skill]] 写入 vault

## 参考链接

- [Obsidian Bases 文档](https://help.obsidian.md/bases/syntax)
- [Bases 公式语法](https://help.obsidian.md/bases/formulas)

---

→ 返回 [[obsidian-skills 套件总览]]
