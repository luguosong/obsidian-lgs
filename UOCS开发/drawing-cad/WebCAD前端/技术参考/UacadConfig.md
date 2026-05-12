# UacadConfig — 跨平台 CAD 配置持久化方案

## 概述

UacadConfig 是一个跨平台的 JSON 配置管理系统，用于替代 Windows 注册表，为 UACAD 提供统一的配置持久化方案。支持 **WASM (浏览器)**、**Windows**、**Linux**、**macOS** 四个平台。

**核心理念：所有平台统一使用 `uacad.json` 文件，不再使用 Windows 注册表。**

---

## 架构

```
┌─────────────────────────────────────────────────────────┐
│                  C++ ExCommands (.tx / WASM)             │
│                                                         │
│  ExRevcloud   ExRectang   ExPolygon   ExPline  ExSpline │
│       │           │           │          │         │    │
│       └─────┬─────┘───────────┘──────────┘─────────┘    │
│             ▼                                           │
│     UacadConfig (KernelBase/Include/UacadConfig.h)      │
│     ├─ load(getConfigPath())                            │
│     ├─ save(getConfigPath())                            │
│     ├─ getDouble("/command/REVCLOUD/minArcLen", 0.5)    │
│     └─ setDouble("/command/REVCLOUD/minArcLen", val)    │
│             │                                           │
│             ▼                                           │
│     getConfigPath() — 平台自适应路径                      │
│     ┌──────────────┬──────────────┬──────────────┐      │
│  WASM:             Win:           Linux:                │
│  /uacad/Configure  %APPDATA%/     ~/.config/            │
│  /uacad.json       uacad/...      uacad/...             │
└─────┼──────────────┴──────────────┴──────────────────────┘
      │ (仅 WASM 平台)
      ▼
┌─────────────────────────────────┐
│  JS 同步层 (useWasmModule.js)   │
│                                 │
│  preRun:   localStorage → FS    │
│  onCmdEnd: FS → localStorage    │
└─────────────────────────────────┘
```

---

## 配置文件路径

| 平台 | 配置文件路径 |
|------|-------------|
| WASM (浏览器) | `/uacad/Configure/uacad.json` (Emscripten 虚拟 FS) + `localStorage["uacad_config"]` |
| Windows | `%APPDATA%\uacad\Configure\uacad.json` |
| Linux | `~/.config/uacad/Configure/uacad.json` |
| macOS | `~/Library/Application Support/uacad/Configure/uacad.json` |

---

## uacad.json 数据结构

```json
{
  "profile": "Default",
  "version": "24.10",

  "vars": {                          // CAD 系统变量 (对应 SETVAR)
    "OSMODE": 4133,
    "GRIDMODE": 0,
    "DIMSCALE": 1.0
  },

  "options": {                       // OPTIONS 对话框设置
    "files": { ... },
    "display": { ... },
    "openAndSave": { ... },
    "system": {},
    "userPreferences": {},
    "drafting": {},
    "3dModeling": {},
    "selection": {},
    "profiles": {}
  },

  "command": {                       // 命令上次输入值
    "REVCLOUD": {
      "minArcLen": 0.5,
      "maxArcLen": 0.5,
      "style": 0,
      "lineWidth": 0.05
    },
    "RECTANG": { ... },
    "POLYGON": { ... },
    "PLINE":   { ... },
    "SPLINE":  { ... },
    "HATCH":   { ... }
  }
}
```

### 三大分区说明

| 分区 | 用途 | 对应 [[AutoCAD]] 机制 |
|------|------|-------------------|
| `vars` | CAD 系统变量 | `SETVAR` / `REGVAR_DEF` / 注册表 `vars\td` |
| `options` | 应用选项设置 | `OPTIONS` 对话框 / 注册表 `Profiles\...\General` |
| `command` | 命令上次输入参数 | C++ `static` 变量 / 注册表 |

---

## 三层优先级

```
浏览器 localStorage   >   /uacad/Configure/uacad.json   >   C++ 硬编码默认值
     (用户修改)              (出厂预设/安装包)                (代码中的默认参数)
```

- **C++ 默认值** — 写在各 `xxxLoadConfig()` 函数的 `getDouble(..., defaultVal)` 参数中
- **出厂预设** — `DrawingWeb/Configure/uacad.json` 文件，打包进 `DrawingJs.data`
- **用户修改** — 存在浏览器 `localStorage["uacad_config"]` 中（桌面平台直接写文件）

---

## C++ 使用指南

### 头文件

```cpp
#include "UacadConfig.h"
```

需要在 CMakeLists.txt 中添加 include 路径：
```cmake
include_directories(${TKERNELBASE_ROOT}/Include  ${TH_ROOT})
```

### API

```cpp
UacadConfig& cfg = UacadConfig::instance();

// 加载（从平台默认路径）
cfg.load();

// 获取值（JSON Pointer 路径 + 默认值）
double v = cfg.getDouble("/command/REVCLOUD/minArcLen", 0.5);
int    n = cfg.getInt   ("/vars/OSMODE", 4133);
bool   b = cfg.getBool  ("/command/SPLINE/fitMode", false);
std::string s = cfg.getString("/vars/TEXTSTYLE", "Standard");

// 设置值（自动创建中间节点）
cfg.setDouble("/command/REVCLOUD/minArcLen", 1.5);
cfg.setInt   ("/vars/OSMODE", 0);

// 保存到文件
cfg.save();
```

### JSON Pointer 路径规则

路径以 `/` 开头，每级用 `/` 分隔，对应 JSON 的嵌套层级：

```
"/command/REVCLOUD/minArcLen"  →  json["command"]["REVCLOUD"]["minArcLen"]
"/vars/OSMODE"                 →  json["vars"]["OSMODE"]
"/options/display/modelBackground" → json["options"]["display"]["modelBackground"]
```

遵循 [RFC 6901 JSON Pointer](https://datatracker.ietf.org/doc/html/rfc6901) 标准，由 RapidJSON 原生支持。

### 命令集成模式

每个命令文件遵循统一的 Load → 使用 → Save 模式：

```cpp
#include "UacadConfig.h"

// 1. 静态变量作为运行时缓存
static double s_dMyParam = 1.0;

// 2. Load/Save 函数
static void myCommandLoadConfig()
{
  UacadConfig& cfg = UacadConfig::instance();
  s_dMyParam = cfg.getDouble("/command/MYCOMMAND/myParam", 1.0);
}

static void myCommandSaveConfig()
{
  UacadConfig& cfg = UacadConfig::instance();
  cfg.setDouble("/command/MYCOMMAND/myParam", s_dMyParam);
  cfg.save();
}

// 3. RAII guard — 确保任何 return 路径都会保存
struct MyCommandConfigGuard { ~MyCommandConfigGuard() { myCommandSaveConfig(); } };

// 4. 命令入口
void _MYCOMMAND_func(OdEdCommandContext* pCmdCtx)
{
  myCommandLoadConfig();
  MyCommandConfigGuard _cfgGuard;  // 函数退出时自动保存

  // ... 命令逻辑，正常读写 s_dMyParam ...
}
```

**关键点：**
- `static` 变量保留为运行时缓存，命令执行中高性能直接访问
- RAII guard 保证无论哪个 `return` 路径都会保存配置
- `cfg.save()` 在 WASM 中写入 Emscripten 虚拟 FS，后续由 JS 同步到 localStorage

---

## JS 同步机制 (仅 WASM)

### 启动时: localStorage → FS

在 `useWasmModule.js` 的 `preRun` 中：

1. 读取 Emscripten FS 中的 `/uacad/Configure/uacad.json`（出厂默认）
2. 读取 `localStorage["uacad_config"]`（用户修改）
3. 深度合并（用户值覆盖默认值）
4. 写回 FS，供 C++ 读取

### 命令完成后: FS → localStorage

在 `window.__onCommandComplete` 回调中：

1. 从 Emscripten FS 读取 `/uacad/Configure/uacad.json`
2. 写入 `localStorage["uacad_config"]`

这样页面刷新后用户设置不会丢失。

---

## 文件清单

| 文件 | 作用 |
|------|------|
| `KernelBase/Include/UacadConfig.h` | 配置管理器（header-only, RapidJSON） |
| `DrawingWeb/Configure/uacad.json` | 出厂默认配置（打包进 DrawingJs.data） |
| `DrawingWebApp/src/hooks/useWasmModule.js` | JS 侧 localStorage ↔ FS 同步 |
| `Drawing/Examples/ExCommands/ExCommandsModule.cpp` | 模块 init/uninit 时 load/save |
| `Drawing/Examples/ExCommands/CMakeLists.txt` | 添加了 RapidJSON 和 KernelBase 头文件路径 |
| `Drawing/Examples/ExCommands/Ex*.cpp` | 各命令的 Load/Save 集成 |

---

## 已集成的命令

| 命令 | 文件 | 持久化变量 |
|------|------|-----------|
| REVCLOUD | ExRevcloud.cpp | minArcLen, maxArcLen, style, lineWidth |
| RECTANG | ExRectang.cpp | chamfer1, chamfer2, fillet, elevation, thickness, width |
| POLYGON | ExPolygon.cpp | sides, inscribed |
| PLINE | ExPline.cpp | width |
| SPLINE | ExSpline.cpp | fitMode, degree, knotParam |

---

## 添加新命令配置

1. 在 `DrawingWeb/Configure/uacad.json` 的 `command` 中添加默认值
2. 在命令 `.cpp` 文件中 `#include "UacadConfig.h"`
3. 按上述模式编写 `xxxLoadConfig()` / `xxxSaveConfig()` / RAII guard
4. 在命令入口调用 load 并声明 guard

## 添加新系统变量

在 `uacad.json` 的 `vars` 中添加键值对即可。C++ 侧通过：
```cpp
int osmode = UacadConfig::instance().getInt("/vars/OSMODE", 4133);
```
读取。

## 添加 OPTIONS 设置

在 `uacad.json` 的 `options` 对应的 Tab 页节点下添加。未来实现 OPTIONS 命令时，直接读写这些节点。

---

## 依赖

- **RapidJSON** (header-only) — `ThirdParty/rapidjson/`，已在 ODA SDK 中
- 无额外编译库依赖，UacadConfig.h 是纯头文件实现
