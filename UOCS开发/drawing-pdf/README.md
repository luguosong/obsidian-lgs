# drawing-pdf — PDF 查看器

> 基于 pdfjs-dist 的 PDF 文件查看器，含国密签名验证。

## 概览

drawing-pdf 是一个独立的 PDF 查看器应用，不依赖 UOCS 后端微服务体系。它的核心功能：

- **PDF 文件渲染** — 基于 Mozilla 的 pdfjs-dist 库
- **SM2/SM3 签名验证** — 国密算法验证 PDF 文件中的数字签名

## 技术栈

| 技术 | 用途 |
|------|------|
| React 19 | UI 框架 |
| MUI 7 (Material UI) | 组件库 |
| MobX 6 | 状态管理 |
| pdfjs-dist | PDF 渲染引擎 |

## 运行端口

开发环境 `:5200`，Docker 部署时通过 Nginx 反向代理。

## 与其他项目的关系

- 与 `drawing-ofd`（OFD 查看器）技术栈相似（React + MUI + MobX）
- `signature/` 模块的 SM2/SM3 签名验证逻辑与 drawing-ofd 共享设计
- 与 upda-cloud 无代码依赖，独立运行
