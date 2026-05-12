# GIS 后端接口参考文档

> **目标读者**：负责 Java 后端的开发者
>
> **文档版本**：2026-04-15
>
> **当前实现**：Node.js (Express) — `DrawingWebApp/server/index.js`

---

## 架构概览

```
┌──────────────────────────────────────────────────────────────┐
│  浏览器 (React + WASM)                                       │
│                                                              │
│  GisServiceTab / ImportGisModal / AddServiceModal ...        │
│      │                                                       │
│      │  fetch('/api/gis/proxy?url=<encodedURL>')             │
│      ▼                                                       │
├──────────────────────────────────────────────────────────────┤
│  后端服务 (当前 Node.js / 待替换为 Java)                      │
│                                                              │
│  GET /api/gis/proxy?url=...  ──→  透传 HTTP GET 到上游       │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  上游 ArcGIS Server (内网)                                    │
│                                                              │
│  MapServer REST  /  FeatureServer REST                       │
└──────────────────────────────────────────────────────────────┘
```

### 为什么需要后端代理？

1. **CORS** — 内网 ArcGIS Server 通常未配置 CORS，浏览器直接请求会被拦截。
2. **WASM 限制** — ODA WASM 引擎中的 libcurl 被 Emscripten 降级为 Web[[Socket]]，无法发起普通 HTTP 请求。

---

## 需要实现的后端接口

**只有一个接口：`GET /api/gis/proxy`** — 一个通用的 HTTP GET 透传代理。

### 接口定义

| 项目 | 值 |
|------|-----|
| **方法** | `GET` |
| **路径** | `/api/gis/proxy` |
| **功能** | 将前端传入的完整 URL 作为上游目标，用服务端 HTTP 客户端 GET 请求该 URL，并将上游响应原样返回给前端 |

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `url` | Query String | String | 是 | 完整的上游 URL（以 `http://` 或 `https://` 开头），前端已做 `encodeURIComponent` 编码 |

**示例请求：**

```
GET /api/gis/proxy?url=http%3A%2F%2F10.147.2.74%3A6080%2Farcgis%2Frest%2Fservices%2Fydyzt%2F%E7%94%A8%E5%9C%B0%E7%BA%A2%E7%BA%BF%2FMapServer%3Ff%3Dpjson
```

解码后的上游 URL：

```
http://10.147.2.74:6080/arcgis/rest/services/ydyzt/用地红线/MapServer?f=pjson
```

### 成功响应

- **状态码**：与上游 HTTP 响应状态码一致（100-599 范围内直接转发）
- **Content-Type**：转发上游的 `Content-Type` 头
- **Body**：上游响应的**原始字节**（不做任何转换）

> **关键**：响应 Body 不能做 UTF-8 重编码或 JSON 解析后再序列化，必须是原始二进制字节，因为有些请求返回的是 PNG 图片。

### 错误响应

| 场景 | HTTP 状态码 | 响应格式 |
|------|------------|---------|
| `url` 参数缺失或非法 | `400` | `{ "error": "missing or invalid url param", "got": "<收到的值>" }` |
| 上游请求失败（网络错误、超时等） | `502` | `{ "error": "upstream fetch failed", "detail": "<错误信息>" }` |
| 上游返回的状态码不在 100-599 范围 | `502` | 同上 |

### Java 参考实现 (Spring Boot)

```java
@RestController
@RequestMapping("/api/gis")
public class GisProxyController {

    private final RestTemplate restTemplate = new RestTemplate();

    @GetMapping("/proxy")
    public ResponseEntity<byte[]> proxy(@RequestParam(value = "url", required = false) String targetUrl) {
        // 1. 参数校验
        if (targetUrl == null || targetUrl.isBlank()
                || !(targetUrl.startsWith("http://") || targetUrl.startsWith("https://"))) {
            return ResponseEntity.badRequest()
                    .contentType(MediaType.APPLICATION_JSON)
                    .body(("{\"error\":\"missing or invalid url param\",\"got\":"
                            + "\"" + (targetUrl == null ? "null" : targetUrl) + "\"}").getBytes());
        }

        try {
            // 2. 透传 GET 请求到上游
            ResponseEntity<byte[]> upstream = restTemplate.exchange(
                    targetUrl, HttpMethod.GET, null, byte[].class);

            // 3. 转发上游状态码 + Content-Type + Body
            HttpHeaders headers = new HttpHeaders();
            if (upstream.getHeaders().getContentType() != null) {
                headers.setContentType(upstream.getHeaders().getContentType());
            }

            int status = upstream.getStatusCode().value();
            return ResponseEntity.status(status).headers(headers).body(upstream.getBody());

        } catch (Exception ex) {
            // 4. 上游请求失败 → 502
            String detail = ex.getMessage() != null ? ex.getMessage() : ex.toString();
            String body = "{\"error\":\"upstream fetch failed\",\"detail\":\""
                    + detail.replace("\"", "\\\"") + "\"}";
            return ResponseEntity.status(HttpStatus.BAD_GATEWAY)
                    .contentType(MediaType.APPLICATION_JSON)
                    .body(body.getBytes());
        }
    }
}
```

---

## 前端调用模式详解

前端所有 GIS HTTP 请求都走同一个 `/api/gis/proxy` 端口，区别在于传入的上游 URL 不同。以下是前端会发起的所有请求类型：

### 查询服务元数据

**用途**：获取 ArcGIS MapServer 的全图范围（`fullExtent`）和坐标系（`spatialReference`）。

**前端代码调用**：

```javascript
const metaUrl = `${mapServerUrl}?f=pjson`
const resp = await fetch(`/api/gis/proxy?url=${encodeURIComponent(metaUrl)}`)
const meta = await resp.json()
```

**实际上游 URL 示例**：

```
http://10.147.2.74:6080/arcgis/rest/services/ydyzt/用地红线/MapServer?f=pjson
```

**上游响应格式**（JSON，前端关注的字段）：

```json
{
  "mapName": "用地红线",
  "layers": [
    { "id": 0, "name": "用地规划", "geometryType": "esriGeometryPolygon", "subLayerIds": null },
    { "id": 1, "name": "道路红线", "geometryType": "esriGeometryPolyline", "subLayerIds": null }
  ],
  "fullExtent": {
    "xmin": 38470000.0,
    "ymin": 2530000.0,
    "xmax": 38530000.0,
    "ymax": 2580000.0,
    "spatialReference": { "wkid": 4526, "latestWkid": 4526 }
  },
  "spatialReference": { "wkid": 4526, "latestWkid": 4526 }
}
```

### 导出地图影像（底图 PNG）

**用途**：获取指定范围的地图渲染图片，作为底图叠加到 DWG 视口。

**前端代码调用**：

```javascript
const params = new URLSearchParams({
  bbox: `${minX},${minY},${maxX},${maxY}`,
  size: '1024,768',
  format: 'png',
  bboxSR: String(wkid),
  imageSR: String(wkid),
  transparent: 'true',
  f: 'image',
})
const exportUrl = `${mapServerUrl}/export?${params.toString()}`
const resp = await fetch(`/api/gis/proxy?url=${encodeURIComponent(exportUrl)}`)
const imageBuffer = await resp.arrayBuffer()  // PNG 二进制
```

**实际上游 URL 示例**：

```
http://10.147.2.74:6080/arcgis/rest/services/ydyzt/用地红线/MapServer/export?bbox=38470000,2530000,38530000,2580000&size=1024,768&format=png&bboxSR=4526&imageSR=4526&transparent=true&f=image
```

**上游响应**：

- `Content-Type: image/png`
- Body：PNG 图片二进制数据

> **重要**：这个响应不是 JSON，而是二进制图片。代理必须原样透传字节，不能做文本解码。

### 查询要素数据（Feature Query）

**用途**：从指定图层获取矢量要素的 GeoJSON 数据（ESRI JSON 格式）。

**前端代码调用**：

```javascript
const layerId = 0  // 图层 ID
const target = `${mapServerUrl}/${layerId}/query?where=1%3D1&outFields=*&returnGeometry=true&f=pjson`
const resp = await fetch(`/api/gis/proxy?url=${encodeURIComponent(target)}`)
const json = await resp.text()  // ESRI JSON 字符串
```

**实际上游 URL 示例**：

```
http://10.147.2.74:6080/arcgis/rest/services/ydyzt/用地红线/MapServer/0/query?where=1%3D1&outFields=*&returnGeometry=true&f=pjson
```

**上游响应格式**（ESRI JSON）：

```json
{
  "objectIdFieldName": "OBJECTID",
  "geometryType": "esriGeometryPolygon",
  "spatialReference": { "wkid": 4526 },
  "fields": [
    { "name": "OBJECTID", "type": "esriFieldTypeOID" },
    { "name": "NAME", "type": "esriFieldTypeString" }
  ],
  "features": [
    {
      "attributes": { "OBJECTID": 1, "NAME": "某地块" },
      "geometry": {
        "rings": [[[38500000, 2550000], [38500100, 2550000], ...]]
      }
    }
  ]
}
```

---

## 重要注意事项

### Token 认证

当前实现中 **Token 不由后端管理**。如果 ArcGIS Server 需要 Token 认证，Token 会被前端拼接到 URL 中：

```
http://server/arcgis/rest/services/.../MapServer?f=pjson&token=xxx
```

后端代理只需原样转发含 Token 的完整 URL 即可，不需要额外处理认证逻辑。

### 响应 Content-Type 转发

必须转发上游的 `Content-Type` 头，因为前端根据它判断响应类型：

| 上游 Content-Type | 前端处理方式 |
|---|---|
| `application/json` | `resp.json()` 解析为 JSON |
| `image/png` | `resp.arrayBuffer()` 读取二进制 |

### URL 编码

前端传入的 `url` 参数已经经过 `encodeURIComponent` 编码（作为 Query String 的一部分），Java 框架通常会自动解码 `@RequestParam`，拿到的就是原始 URL。

**注意**：ArcGIS URL 中可能包含中文路径（如 `/用地红线/MapServer`），请确保 HTTP 客户端能正确处理。

### 超时设置

建议将上游请求超时设置为 **60-120 秒**，因为：
- 影像导出（`/export`）在大范围请求时可能较慢
- 要素查询在数据量大时也需要较长时间

### 响应体大小

影像导出可能返回几 MB 的 PNG 图片，要素查询可能返回几十 MB 的 JSON。请确保代理没有对响应体大小做过小的限制。

### 开发环境端口

| 服务 | 端口 | 说明 |
|------|------|------|
| 前端 Vite dev server | 3000 | 通过 `vite.config.js` 中的 proxy 配置将 `/api/*` 转发到后端 |
| 当前 Node.js 后端 | 3001 | Express，同时承载 AI Chat 接口和 GIS 代理 |

Java 后端替换后，只需要保证 `/api/gis/proxy` 端点可达即可。前端可以通过修改 `vite.config.js` 中的 proxy target 来切换后端地址。

---

## 接口测试用例

### 正常 — 查询元数据

```bash
curl "http://localhost:3001/api/gis/proxy?url=http%3A%2F%2F10.147.2.74%3A6080%2Farcgis%2Frest%2Fservices%2Fydyzt%2F%E7%94%A8%E5%9C%B0%E7%BA%A2%E7%BA%BF%2FMapServer%3Ff%3Dpjson"
```

**预期**：返回 `200`，Body 为 ArcGIS 服务的 JSON 元数据。

### 正常 — 导出影像

```bash
curl -o test.png "http://localhost:3001/api/gis/proxy?url=http%3A%2F%2F10.147.2.74%3A6080%2Farcgis%2Frest%2Fservices%2Fydyzt%2F%E7%94%A8%E5%9C%B0%E7%BA%A2%E7%BA%BF%2FMapServer%2Fexport%3Fbbox%3D38470000%2C2530000%2C38530000%2C2580000%26size%3D1024%2C768%26format%3Dpng%26bboxSR%3D4526%26imageSR%3D4526%26transparent%3Dtrue%26f%3Dimage"
```

**预期**：返回 `200`，`Content-Type: image/png`，Body 为 PNG 图片。

### 正常 — 查询要素

```bash
curl "http://localhost:3001/api/gis/proxy?url=http%3A%2F%2F10.147.2.74%3A6080%2Farcgis%2Frest%2Fservices%2Fydyzt%2F%E7%94%A8%E5%9C%B0%E7%BA%A2%E7%BA%BF%2FMapServer%2F0%2Fquery%3Fwhere%3D1%253D1%26outFields%3D*%26returnGeometry%3Dtrue%26f%3Dpjson"
```

**预期**：返回 `200`，Body 为 ESRI JSON 格式的要素数据。

### 异常 — 缺少 url 参数

```bash
curl "http://localhost:3001/api/gis/proxy"
```

**预期**：返回 `400`

```json
{ "error": "missing or invalid url param", "got": null }
```

### 异常 — 非法 url

```bash
curl "http://localhost:3001/api/gis/proxy?url=ftp://bad"
```

**预期**：返回 `400`

```json
{ "error": "missing or invalid url param", "got": "ftp://bad" }
```

### 异常 — 上游不可达

```bash
curl "http://localhost:3001/api/gis/proxy?url=http%3A%2F%2F192.168.99.99%3A9999%2Ftest"
```

**预期**：返回 `502`

```json
{ "error": "upstream fetch failed", "detail": "connect ETIMEDOUT ..." }
```

---

## 当前 Node.js 实现源码

以下是当前生效的完整实现（`DrawingWebApp/server/index.js` 第 73-95 行），可供 Java 端对照参考：

```javascript
// ────────────── GIS HTTP 代理 ──────────────
// 浏览器 WASM 里的 libcurl 被 Emscripten 降级成 WebSocket, 普通 HTTP 走不通;
// 同时内网 ArcGIS Server 通常没开 CORS。前端把请求转到这里, Node 侧直接 fetch。
app.get('/api/gis/proxy', async (req, res) => {
  const target = req.query.url
  console.log('[/api/gis/proxy] incoming:', target)
  if (!target || typeof target !== 'string' || !/^https?:\/\//i.test(target)) {
    return res.status(400).json({ error: 'missing or invalid url param', got: target })
  }
  try {
    const upstream = await fetch(target, { method: 'GET' })
    const body = await upstream.arrayBuffer()
    console.log(`[/api/gis/proxy] upstream ${upstream.status}, ${body.byteLength} bytes`)
    const status = (upstream.status >= 100 && upstream.status < 600) ? upstream.status : 502
    const ct = upstream.headers.get('content-type')
    if (ct) res.setHeader('Content-Type', ct)
    res.status(status).send(Buffer.from(body))
  } catch (err) {
    const detail = err?.cause?.message || err?.message || String(err)
    console.error('[/api/gis/proxy] fetch failed:', detail, 'target:', target)
    res.status(502).json({ error: 'upstream fetch failed', detail })
  }
})
```

---

## 前端文件索引

以下文件会调用 `/api/gis/proxy`，供排查问题时参考：

| 文件 | 调用场景 |
|------|---------|
| `src/components/GisService/GisServiceTab.jsx` | 查询服务元数据、导出地图影像 |
| `src/components/GisService/ImportGisModal.jsx` | 查询指定图层的要素数据 |

其余 GIS 组件（`ExportGisModal`、`AddServiceModal`、`ServiceBrowser`、`CrsInfoModal` 等）通过 WASM 命令（`viewer.execute()`）直接与 C++ 引擎交互，不经过后端 HTTP 代理。

---

## 预置 GIS 服务地址

当前前端硬编码了以下内网测试服务（`src/stores/GisStore.js`）：

| 名称 | MapServer URL | 坐标系 |
|------|--------------|--------|
| 东莞规划地理信息 | `http://10.147.2.74:6080/arcgis/rest/services/ydyzt/用地红线/MapServer` | EPSG:4526 |
| 绿建科技苏州内网测试 | `http://192.168.3.214:6080/arcgis/rest/services/test/MapServer` | EPSG:4526 |

这些仅用于开发测试，后端不需要关心它们。

## 相关笔记

- [[技术参考]]
- [[CadCodeExecutor 沙箱]]
- [[UacadConfig — 跨平台 CAD 配置持久化方案]]
- [[WASM API 速查]]
- [[Java 概述]]
- [[部署与安全]]
- [[更新日志]]
- [[更新日志（≤2.1.98）]]
