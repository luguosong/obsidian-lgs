# 前端 dist 部署 checklist（drawing-web-app）

## 适用范围

`drawing-cad/drawing-web-app/` 源码变更后，将 dist 产物同步到[[测试服务器]]（192.168.3.228）的完整流程。

> 深度背景见 `docker-compose/docs/测试服务器.md`（SSH / SVN / 全局部署链路）。本文档只覆盖前端子模块专属步骤。

## 部署链路

```text
drawing-web-app/src (Git)
        │
        │ npm run build（自动包含 verify:bundle 校验）
        ▼
drawing-web-app/dist
        │
        │ robocopy /MIR /XD .svn
        ▼
docker-compose/uocs-app/drawing-cad/web-app/dist (SVN 工作副本)
        │
        │ svn add / svn delete / svn commit
        ▼
SVN 仓库
        │
        │ ssh 228: svn update
        ▼
/root/uocs-deploy/uocs-app/drawing-cad/web-app/dist
        │
        │ docker compose up -d --build drawing-web-app
        ▼
nginx 容器（端口 17010）
```

## 发布 checklist

### 本地构建

- [ ] 切换到 `drawing-cad/drawing-web-app/`
- [ ] `npm run build`
  - vite 构建产物到 `dist/`
  - **自动**执行 `npm run verify:bundle`，校验关键字符串是否在 bundle 中
  - 失败退出码非 0 → **禁止继续发布**，重新检查源码或补构建
- [ ] （可选）本地浏览器自测：`npm run preview`

### 同步到 SVN 工作副本

- [ ] 用 `robocopy` 镜像同步 dist（必须排除 `.svn` 目录避免污染 SVN 元数据）：

    ```powershell
    robocopy `
      "E:\OpenCloud24.10\upda-code\drawing-cad\drawing-web-app\dist" `
      "E:\OpenCloud24.10\upda-code\docker-compose\uocs-app\drawing-cad\web-app\dist" `
      /MIR /XD .svn
    ```

  > `robocopy` exit code `0-3` 都是成功（有变化 = 1，DIR 变化 = 2），只有 ≥ 8 才是失败。

### SVN 提交

- [ ] `cd docker-compose/uocs-app/drawing-cad/web-app/dist`
- [ ] `svn status` 确认变更集
- [ ] 对新增文件 `svn add`，对移除文件 `svn delete`（vite 每次 hash 不同，需处理旧的 `index-*.js`）
- [ ] `svn commit -m "rebuild drawing-web-app: <简要说明>"`

### 服务器更新

- [ ] SSH 到[[测试服务器]]执行 `svn update`
- [ ] `docker compose up -d --build drawing-web-app`（耗时操作，放后台）：

    ```bash
    ssh -i ~/.ssh/id_ed25519_uocs_deploy -o StrictHostKeyChecking=no root@192.168.3.228 \
      'cd /root/uocs-deploy && svn update --username root --password Upda123! && \
       nohup docker compose up -d --build drawing-web-app > /tmp/rebuild.log 2>&1 &'
    ```

  > drawing-web-app 重建会级联重启 drawing-ai-server，后者 [[Spring Boot]] 冷启动 + `start_period: 180s`，总等待约 3-4 分钟。

### 验证

- [ ] `docker compose ps` 确认 `drawing-web-app` 和 `drawing-ai-server` 均为 `healthy`
- [ ] 打开 <http://192.168.3.228:17010/>，硬刷新（Ctrl+F5）
- [ ] 浏览器 DevTools → Network 确认加载的 `index-*.js` 是最新 hash
- [ ] 执行关键功能一次（例如上传 DWG → 打开 AI 助手 → 看到"[[图纸记忆]]"面板初始化）

## 常见问题

### 旧 bundle 仍在生效

| 症状 | 根因 | 处理 |
|------|------|------|
| 浏览器里 `index-*.js` 还是旧 hash | 浏览器缓存 / nginx 未生效 | 硬刷新；必要时 `docker compose restart drawing-web-app` |
| grep bundle 找不到新功能关键字（如 `MemoryAutoInit`） | 漏 `npm run build` 或 tree-shake 移除 | 重新构建，`verify:bundle` 会自动拦截 |
| SVN 工作副本没变化 | dist 没覆盖过去 | 确认 `robocopy` 路径；检查排除规则是否误排 |

### `verify:bundle` 校验失败

脚本位置：`scripts/verify-bundle.mjs`，关键字清单在 `REQUIRED_MARKERS`。

- **失败且改动与记忆功能无关** → 说明新增改动意外移除了这些字符串，排查源码是否误删 `[MemoryAutoInit]` 日志等
- **新增功能上线** → 在 `REQUIRED_MARKERS` 增加一条稳定字符串字面量（例如日志 tag、API 路径、UI 文案），**不要**使用函数/变量名（会被 minifier 压缩）

### drawing-ai-server 未跟随重启

`drawing-ai-server` 在 `compose.yaml` 中依赖 `drawing-web-app`；`docker compose up -d --build drawing-web-app` 通常会联动，但若观察到 `ai-server` 仍为旧版，可显式执行：

```bash
docker compose up -d --build drawing-ai-server
```

## 相关文件

| 路径 | 作用 |
|------|------|
| `drawing-cad/drawing-web-app/scripts/verify-bundle.mjs` | bundle 关键字校验脚本 |
| `drawing-cad/drawing-web-app/package.json` | `build` 脚本已串接 `verify:bundle` |
| `docker-compose/uocs-app/drawing-cad/web-app/dist/` | SVN 工作副本，对接服务器部署目录 |
| `docker-compose/docs/测试服务器.md` | SSH、SVN、全局部署链路权威文档 |

## 相关笔记

- [[WebCAD前端]]
- [[东莞红线工具 — WebUACAD 开发评估报告]]
- [[OdDbPolyline 长度计算错误修复方案]]
- [[前端架构详情]]
- [[速度优化架构]]
- [[架构总览]]
- [[Harness Engineering 架构详解]]
- [[Docker 部署架构]]
