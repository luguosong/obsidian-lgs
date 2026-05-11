---
title: Canvas 布局算法参考
description: Obsidian Canvas MindMap 和 Freeform 布局的定位算法
created: 2026-05-10
tags:
  - 参考
  - obsidian
  - canvas
  - 算法
  - 布局
---

# Canvas 布局算法参考

> [!note] 来源
> 整理自 [axton-obsidian-visual-skills/references/layout-algorithms.md](https://github.com/axtonliu/axton-obsidian-visual-skills/blob/master/obsidian-canvas-creator/references/layout-algorithms.md)

## 通用间距常量

```
HORIZONTAL_SPACING = 320  # 节点中心间最小水平距离
VERTICAL_SPACING   = 200  # 节点中心间最小垂直距离
NODE_PADDING       = 20   # 节点内边距
```

## 碰撞检测

```python
def check_collision(node1, node2):
    """检测两个节点是否重叠或过近"""
    dx = abs(center1_x - center2_x)
    dy = abs(center1_y - center2_y)
    min_dx = (node1.width + node2.width) / 2 + HORIZONTAL_SPACING
    min_dy = (node1.height + node2.height) / 2 + VERTICAL_SPACING
    return dx < min_dx or dy < min_dy
```

---

## MindMap 布局

### 1. 放射树布局

#### Step 1：定位根节点

```
root.x = 0 - (root_width / 2)
root.y = 0 - (root_height / 2)
```

#### Step 2：一级分支定位

将一级子节点围绕根节点均匀分布：

```python
def position_primary_branches(root, children, radius=400):
    n = len(children)
    angle_step = 2 * pi / n

    for i, child in enumerate(children):
        angle = i * angle_step
        x = root.center_x + radius * cos(angle) - child.width / 2
        y = root.center_y + radius * sin(angle) - child.height / 2
```

**半径选择**：

| 子节点数 | 半径 |
|---------|------|
| ≤10 | 400px |
| 11-20 | 500px |
| >20 | 600px |

#### Step 3：二级分支定位

**水平布局**（推荐）：

```python
def position_secondary_horizontal(parent, children, distance=350):
    total_height = sum(child.height for child in children)
    total_spacing = (n - 1) * VERTICAL_SPACING
    start_y = parent.center_y - (total_height + total_spacing) / 2

    for child in children:
        child.x = parent.x + parent.width + distance
        child.y = current_y
        current_y += child.height + VERTICAL_SPACING
```

**垂直布局**（用于左右方向的分支）：

```python
def position_secondary_vertical(parent, children, distance=250):
    # 水平排列在父节点下方
    for child in children:
        child.x = current_x
        child.y = parent.y + parent.height + distance
        current_x += child.width + HORIZONTAL_SPACING
```

#### Step 4：平衡调整

迭代检测碰撞并调整位置（最多 10 轮）。

### 2. 树形布局（自上而下）

```python
def position_tree_layout(root, tree):
    root.x = 0 - root.width / 2
    root.y = 0 - root.height / 2

    for level in range(1, max_depth):
        nodes_at_level = get_nodes_at_level(tree, level)
        total_width = sum(node.width for node in nodes_at_level)
        start_x = -(total_width + total_spacing) / 2
        y = level * (150 + VERTICAL_SPACING)
```

---

## Freeform 布局

### 1. 内容分组

按语义关系将节点分成若干组。

### 2. 网格分区

```python
def layout_zones(groups, canvas_width=2000, canvas_height=1500):
    cols = ceil(sqrt(n_groups))
    rows = ceil(n_groups / cols)
    zone_width = canvas_width / cols
    zone_height = canvas_height / rows
```

### 3. 区内节点定位

**有机流动**：从左上角开始，行内排列，超出宽度换行。

**结构网格**：在分区内按网格居中排列。

### 4. 跨区连接

根据两节点中心相对方向自动选择最优连接边：

```python
def calculate_edge_path(from_node, to_node):
    if abs(dx) > abs(dy):
        # 水平连接
        from_side = "right" if dx > 0 else "left"
    else:
        # 垂直连接
        from_side = "bottom" if dy > 0 else "top"
```

---

## 高级算法

### 力导向布局

适用于复杂网络的弹簧模型：

```python
SPRING_LENGTH = 200       # 弹簧自然长度
SPRING_CONSTANT = 0.1     # 弹簧刚度
REPULSION_CONSTANT = 5000 # 斥力常数
```

- 所有节点对之间有斥力（防重叠）
- 有边连接的节点之间有引力（保持靠近）
- 迭代 100 次趋于稳定

### 边交叉最小化

通过交换相邻节点位置来减少交叉边数。

### 视觉平衡

计算所有节点的加权质心，将整体偏移至 (0,0) 附近。

---

## 常用布局模式

| 模式 | 算法 |
|------|------|
| **时间线** | 水平/垂直等距排列 |
| **环形** | 节点均匀分布在圆周上 |
| **矩阵** | rows × cols 网格 |

## 质量检查

1. **无重叠** — 所有节点满足最小间距
2. **平衡** — 视觉中心接近 (0,0)
3. **可达** — 所有节点通过边可达
4. **可读** — 文本大小适合缩放级别
5. **高效** — 边路径相对直接

---

→ 返回 [[obsidian-canvas-creator skill]] | [[axton-obsidian-visual-skills 套装总览]]
