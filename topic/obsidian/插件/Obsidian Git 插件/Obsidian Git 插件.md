---
title: Obsidian Git 插件
source: "https://github.com/Vinzent03/obsidian-git"
description: 在 Obsidian 中集成 Git 版本控制，支持自动提交同步及高级功能
author:
published:
tags:
  - obsidian
  - git
  - 插件
---

## Obsidian Git 插件

一款功能强大的 [[Obsidian]] 社区插件，将 Git 集成直接带入你的 Vault。在 [[Obsidian]] 内即可完成自动提交、pull、push 以及变更查看等操作。

## 📚 文档

所有配置说明（含移动端）、常见问题、技巧及[[高级配置]]，均可在 📖 [完整文档](https://publish.obsidian.md/git-doc) 中找到。

> [!warning] 移动端用户注意
> 该插件在移动端**极不稳定**，请务必查阅下方 [移动端支持](#-移动端支持--实验性) 章节。

## 核心功能

- 🔁 **自动提交同步**：按计划自动执行 commit、pull 和 push
- 📥 **启动时自动 pull**：[[Obsidian]] 启动时自动拉取最新内容
- 📂 **子模块支持**：管理多个仓库（仅限桌面端，需手动开启）
- 🔧 **Source Control View**：暂存/取消暂存、提交和查看文件差异——通过 `Open source control view` 命令打开
- 📜 **History View**：浏览提交记录和变更文件——通过 `Open history view` 命令打开
- 🔍 **Diff View**：查看文件变更内容——通过 `Open diff view` 命令打开
- 📝 **编辑器行标记**：在编辑器中直接显示新增、修改和删除的行/块（仅限桌面端）
- GitHub 集成：在浏览器中打开文件及其历史记录

> [!tip] 搭配使用
> 如需详细的文件历史记录，可将本插件与 Version History Diff 插件搭配使用。

## 界面预览

### 🔧 Source Control View

在 [[Obsidian]] 内直接管理文件变更，支持暂存/取消暂存单个文件并提交。

![Source Control View](https://raw.githubusercontent.com/Vinzent03/obsidian-git/master/images/source-view.png)

### 📜 History View

展示仓库的提交历史，可显示提交信息、作者、日期和变更文件。作者和日期默认关闭（如截图所示），可在设置中开启。

![History View](https://raw.githubusercontent.com/Vinzent03/obsidian-git/master/images/history-view.png)

### 🔍 Diff View

通过清晰简洁的差异查看器对比版本。可从 Source Control View 打开，或使用 `Open diff view` 命令。

![Diff View](https://raw.githubusercontent.com/Vinzent03/obsidian-git/master/images/diff-view.png)

### 📝 编辑器行标记

在编辑器中逐行查看新增、修改和删除的变更标记，支持直接从标记处暂存或重置变更，也有命令用于在块之间跳转、暂存/重置光标处的块。需在插件设置中手动开启。

![编辑器行标记](https://raw.githubusercontent.com/Vinzent03/obsidian-git/master/images/signs.png)

## 可用命令

> [!info] 说明
> 以下仅列出最常用的命令，完整命令列表请在 [[Obsidian]] 命令面板中查看。

- 🔄 变更
	- `List changed files`：在弹窗中列出所有变更
		- `Open diff view`：为当前文件打开 Diff View
		- `Stage current file`：暂存当前文件
		- `Unstage current file`：取消暂存当前文件
		- `Discard all changes`：丢弃仓库中的所有变更
- ✅ 提交
	- `Commit`：若有已暂存文件则只提交暂存内容，否则提交所有变更
		- `Commit with specific message`：同上，但使用自定义提交信息
		- `Commit all changes`：提交所有变更，不执行 push
		- `Commit all changes with specific message`：同上，但使用自定义提交信息
- 🔀 提交同步
	- `Commit-and-sync`：默认行为为提交所有变更、pull，然后 push
		- `Commit-and-sync with specific message`：同上，但使用自定义提交信息
		- `Commit-and-sync and close`：同 `Commit-and-sync`，在桌面端还会关闭 [[Obsidian]] 窗口（移动端不会退出应用）
- 🌐 远程操作
	- `Push`、`Pull`
		- `Edit remotes`：添加或编辑远程仓库
		- `Remove remote`：移除远程仓库
		- `Clone an existing remote repo`：打开对话框，输入 URL 和认证信息克隆远程仓库
		- `Open file on GitHub`：在浏览器中打开当前文件的 GitHub 页面（仅限桌面端）
		- `Open file history on GitHub`：在浏览器中打开当前文件的 GitHub 历史记录（仅限桌面端）
- 🏠 本地仓库管理
	- `Initialize a new repo`：初始化新仓库
		- `Create new branch`：创建新分支
		- `Delete branch`：删除分支
		- `CAUTION: Delete repository`：⚠️ 删除仓库
- 🧪 其他
	- `Open source control view`：打开 Source Control View 侧边栏
		- `Open history view`：打开 History View 侧边栏
		- `Edit .gitignore`：编辑 `.gitignore` 文件
		- `Add file to .gitignore`：将当前文件添加到 `.gitignore`

## 💻 桌面端说明

### 🔐 认证

部分 Git 服务需要额外配置 HTTPS/SSH 认证，请参阅 [认证指南](https://publish.obsidian.md/git-doc/Authentication)。

### Linux 上的 Obsidian

- ⚠️ 不支持 Snap（受其沙箱限制）
- ⚠️ 不推荐 Flatpak，因为它无法访问所有系统文件。虽然社区在积极修复相关问题，但仍存在一些缺陷，尤其是复杂配置场景下。
- ✅ 请使用 AppImage 或通过系统包管理器完整安装（参见 [Linux 安装指南](https://publish.obsidian.md/git-doc/Installation#Linux)）

## 📱 移动端支持（⚠️ 实验性）

移动端的 Git 实现**非常不稳定**！不建议在移动端使用本插件，请考虑其他同步方案。

一个可选替代方案是 [GitSync](https://github.com/ViscousPot/GitSync)，支持 Android 和 iOS，与本插件无关联，但对移动端用户可能是更好的选择。相关教程可参考[此处](https://viscouspotenti.al/posts/gitsync-all-devices-tutorial)。

> [!info] 技术背景
> 移动端 Git 功能通过 [isomorphic-git](https://isomorphic-git.org/) 实现——这是一个基于 JavaScript 的 Git 重实现，但存在严重的局限性和问题。[[Obsidian]] 插件无法在 Android 或 iOS 上调用原生 Git 安装。

### ❌ 移动端功能限制

- 不支持 **SSH 认证**（[isomorphic-git 相关 issue](https://github.com/isomorphic-git/isomorphic-git/issues/231)）
- 仓库大小受内存限制
- 不支持 rebase 合并策略
- 不支持子模块

### ⚠️ 性能注意事项

> [!caution] 注意
> 根据你的设备和可用内存，[[Obsidian]] 可能出现以下情况：
>
> - 在 clone/pull 时崩溃
> - 产生缓冲区溢出错误
> - 无限运行卡死
>
> 这是由移动端底层 Git 实现效率低下导致的，目前暂无解决办法。如果你遇到了这些问题，很遗憾本插件可能不适合你在移动端使用。提交 issue 或新建 issue 也无法解决该问题，对此深表歉意。

### 移动端使用建议

如果你的仓库/Vault 较大，建议逐个暂存文件，并只提交已暂存的文件。

## 🙋 联系与致谢

- 行标记（Line Authoring）功能由 [GollyTicker](https://github.com/GollyTicker) 开发，相关问题可直接联系她。
- 本插件最初由 [denolehov](https://github.com/denolehov) 开发。自 2021 年 3 月起由 [Vinzent03](https://github.com/Vinzent03) 接手维护，GitHub 仓库也于 2024 年 7 月迁移至其账号下。
- 如有任何反馈或问题，欢迎通过 GitHub Issues 联系。

## 相关笔记

- [[扩展体系]]
- [[Superpowers 使用手册与最佳实践 — 实施计划]]
- [[axton-obsidian-visual-skills 套件总览]]
- [[excalidraw-diagram skill]]
- [[Mermaid 语法规则参考]]
- [[mermaid-visualizer skill]]
- [[obsidian-canvas-creator skill]]
- [[defuddle skill]]
