# Drawing Memory Vision Init — Plan 1 (Stage A + Stage B + UI)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the slow text-only memory init flow with a vision-driven Stage A (full-image analysis) + Stage B (region-by-region precise reading) pipeline, producing accurate `keyFacts` / `layerSemantics` / `mainAreaDescription` / `candidateObjects` into Redis-backed `DrawingMemory`. This plan delivers a ship-able milestone where opening a drawing automatically builds vision-derived memory in ≤ 30s P50.

**Architecture:**
- Frontend pulls zero-cost layer metadata via `viewer.getLayersWithInfo()`, captures full-extent screenshot, POSTs to `/init` for Stage A
- Backend Stage A (single vision LLM call) returns `drawingType` + `drawingUnit` + `drawingLayout` + `keyRegions[]` (each with bbox + splitStrategy)
- Frontend orchestrates Stage B: zoom into each region (ODA re-render), capture sharp tiles per `splitStrategy`, POST per-region to `/region`
- Backend Stage B uses region-specific prompts (technical-table / legend / main-area) and writes structured findings to `DrawingMemory`
- UI panel renders new fields (mainArea, keyAnnotations, candidateObjects)

**Scope of this plan (Plan 1):**
- IN: Phases P1-P4 from spec (cleanup-1, Stage A, Stage B, UI)
- OUT: Phase P5 (Stage C object extraction) and P6 (LandBoundary* deletion) — these go to Plan 2 after Plan 1 lands

**Tech Stack:**
- Frontend: React 19 + Vite 6 + MobX + Ant Design. **Adds Vitest** for pure-function unit tests
- Backend: [[Spring Boot]] 3.5 + [[Spring AI]] 1.1.2 + [[Spring AI]] Alibaba (DashScope) + Qdrant + Redis
- [[Vision]] model: configured via [[Spring AI]] Alibaba DashScope (multimodal)

**Reference docs:**
- Spec: [DrawingWebApp/docs/specs/2026-04-30-drawing-memory-vision-init-design.md](../specs/2026-04-30-drawing-memory-vision-init-design.md)
- Existing pattern reference: `drawing-ai-server/src/main/java/com/lvjian/drawingai/memory/DrawingTypeSkillProvider.java` (UserMessage.builder().media() pattern)

---

## File Structure

### Files to CREATE

**Frontend (`DrawingWebApp/`):**
| File | Responsibility |
|---|---|
| `vitest.config.js` | Vitest configuration |
| `src/services/memory/sliceBbox.js` | Pure function: bbox + splitStrategy → tile bbox array |
| `src/services/memory/__tests__/sliceBbox.test.js` | Unit tests for sliceBbox |
| `src/services/memory/captureRegionTiles.js` | ODA viewer.zoomTo + captureCurrentView orchestration for one region |
| `src/services/memory/VisionMemoryPipeline.js` | Stage A/B 调度入口 (`run(viewer, clientId, fileId)`) |
| `src/components/AiAssistant/DrawingMemoryPanel/MainAreaSection.jsx` | UI: 主体区描述 + keyAnnotations |
| `src/components/AiAssistant/DrawingMemoryPanel/CandidateObjectsList.jsx` | UI: candidateObjects 列表 |

**Backend (`drawing-ai-server/`):**
| File | Responsibility |
|---|---|
| `src/main/java/com/lvjian/drawingai/memory/vision/StageAService.java` | 全图分析视觉调用 |
| `src/main/java/com/lvjian/drawingai/memory/vision/StageBService.java` | 区域精读分发器(按 regionType 路由) |
| `src/main/java/com/lvjian/drawingai/memory/vision/regions/IndicatorTablePromptBuilder.java` | 技经表 prompt 组装 |
| `src/main/java/com/lvjian/drawingai/memory/vision/regions/LegendPromptBuilder.java` | 图例 prompt 组装 |
| `src/main/java/com/lvjian/drawingai/memory/vision/regions/MainAreaPromptBuilder.java` | 主体区 prompt 组装 |
| `src/main/java/com/lvjian/drawingai/memory/vision/dto/StageAResult.java` | Stage A 输出 DTO |
| `src/main/java/com/lvjian/drawingai/memory/vision/dto/KeyRegion.java` | keyRegions[] 元素 DTO |
| `src/main/java/com/lvjian/drawingai/memory/vision/dto/RegionResult.java` | Stage B 输出 DTO(union by type) |
| `src/main/java/com/lvjian/drawingai/memory/vision/dto/CandidateObject.java` | 主体区候选对象 DTO |
| `src/main/java/com/lvjian/drawingai/memory/vision/dto/KeyAnnotation.java` | 关键标注 DTO |
| `src/test/java/com/lvjian/drawingai/memory/vision/StageAServiceTest.java` | Stage A 测试(mock ChatModel) |
| `src/test/java/com/lvjian/drawingai/memory/vision/StageBServiceTest.java` | Stage B 测试(mock ChatModel) |

### Files to MODIFY

**Frontend:**
- `package.json` — add `vitest` devDep + `test` script
- `src/components/AiAssistant/AiAssistant.jsx` — replace `triggerMemoryAutoInit` body with `VisionMemoryPipeline.run()`; flip `AUTO_DRAWING_ANALYSIS_ENABLED` to `true`
- `src/services/DrawingMemoryApi.js` — add `postInitV2()` and `postRegion()`
- `src/services/DwgResultSummarizer.js` — DELETE `_aggregateSiteAreas` and "绿地: 合计 X ㎡" output blocks
- `src/services/DwgReadAdapter.js` — DELETE `_categorizeSiteLayer` (also remove its only call site if any)
- `src/components/AiAssistant/DrawingMemoryPanel.jsx` — render `<MainAreaSection>` + `<CandidateObjectsList>`

**Backend:**
- `src/main/java/com/lvjian/drawingai/memory/DrawingMemory.java` — add fields: `mainAreaDescription` (String), `keyAnnotations` (List), `candidateObjects` (List), `legendItems` (List); add `drawingUnit` to `Summary`. **Note**: existing `layerSemantics` section is NOT populated by Stage B (legend → separate `legendItems` section instead, no layer-name mapping)
- `src/main/java/com/lvjian/drawingai/memory/DrawingMemoryStore.java` — Redis hash 序列化适配三个新字段
- `src/main/java/com/lvjian/drawingai/memory/DrawingMemoryInitService.java` — replace `doStage2()` body with `StageAService.runStageA()` synchronous call; **DELETE** `SYSTEM_PROMPT` constant for old stage 2
- `src/main/java/com/lvjian/drawingai/controller/DrawingMemoryController.java` — change `/init` request body schema to accept `metadata + fullScreenshot`; add `POST /region` endpoint
- `src/main/java/com/lvjian/drawingai/memory/DrawingTypeSkillProvider.java` — mark `@Deprecated` with note pointing to `StageAService` (keep file for one release cycle to avoid call site breakage)

### Files to DELETE in this plan

None. Plan 2 will delete `LandBoundaryVisionTest.js`, `LandBoundaryAnalyzer.js`, `RUN_LAND_BOUNDARY_TEST` const, and `DrawingTypeSkillProvider.java`.

---

## Phase 1 — Cleanup & Test Setup

> Goal: remove the proven-incorrect "图层名猜类型 + 面积聚合" code path, set up frontend test framework. This phase intentionally produces no functional change beyond removing logged "绿地: 合计 X ㎡" lines from the prompt. After this phase, opening a drawing should still produce the same memory init result (since `AUTO_DRAWING_ANALYSIS_ENABLED=false`, init is still skipped).

### Task 1.1: Add Vitest to frontend

**Files:**
- Modify: `DrawingWebApp/package.json`
- Create: `DrawingWebApp/vitest.config.js`

- [ ] **Step 1: Install Vitest**

Run from `DrawingWebApp/`:
```bash
npm install -D vitest @vitest/ui
```
Expected: vitest added under devDependencies in package.json.

- [ ] **Step 2: Add test scripts to package.json**

In `DrawingWebApp/package.json`, modify the `scripts` block:
```json
"scripts": {
  "dev": "vite",
  "build": "vite build",
  "lint": "eslint .",
  "preview": "vite preview",
  "test": "vitest run",
  "test:watch": "vitest"
}
```

- [ ] **Step 3: Create vitest.config.js**

Create `DrawingWebApp/vitest.config.js`:
```javascript
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    environment: 'node',
    include: ['src/**/__tests__/**/*.test.js', 'src/**/*.test.js'],
    globals: false,
  },
})
```

- [ ] **Step 4: Verify test runner works (no tests yet)**

Run: `npm test`
Expected: "No test files found" or success with 0 tests. If error, fix vitest version compatibility.

- [ ] **Step 5: Commit**

```bash
git add DrawingWebApp/package.json DrawingWebApp/package-lock.json DrawingWebApp/vitest.config.js
git commit -m "build(test): add Vitest for frontend unit tests"
```

### Task 1.2: Delete `_aggregateSiteAreas` and area aggregation output

**Files:**
- Modify: `DrawingWebApp/src/services/DwgResultSummarizer.js`

- [ ] **Step 1: Read DwgResultSummarizer.js to locate target functions**

Run via Read tool: `DrawingWebApp/src/services/DwgResultSummarizer.js`. Locate:
- `_aggregateSiteAreas` function (around line 513 per spec)
- `summarizeForMemoryInit` function (around line 599)
- Any output sections containing "绿地: 合计" or "areaByCategory"

- [ ] **Step 2: Delete `_aggregateSiteAreas` function**

Delete the entire function body of `_aggregateSiteAreas`. If it's the only export from a sub-module, also remove the export.

- [ ] **Step 3: Remove area-aggregation block from `summarizeForMemoryInit`**

Inside `summarizeForMemoryInit`, locate the section that calls `_aggregateSiteAreas(...)` and emits text like "## 场地面积聚合" / "绿地: 合计 X ㎡" / etc. Delete that whole block (call + output string assembly).

- [ ] **Step 4: Lint check**

Run from `DrawingWebApp/`:
```bash
npm run lint
```
Expected: no errors (warnings about unused imports are OK if any). If errors, remove unused imports referenced only by deleted code.

- [ ] **Step 5: Commit**

```bash
git add DrawingWebApp/src/services/DwgResultSummarizer.js
git commit -m "refactor(memory): remove unreliable layer-name area aggregation

The _aggregateSiteAreas + 'category' regex inference produced
unreliable area sums (DWG objects often not on their 'expected'
layer). Vision-driven Stage B (technical-indicators table) will
read authoritative values directly from the drawing."
```

### Task 1.3: Delete `_categorizeSiteLayer`

**Files:**
- Modify: `DrawingWebApp/src/services/DwgReadAdapter.js`

- [ ] **Step 1: Locate `_categorizeSiteLayer` and all call sites**

Run via Grep tool:
```
pattern: _categorizeSiteLayer
glob: src/**/*.js
```
Note all call sites.

- [ ] **Step 2: Delete `_categorizeSiteLayer` function**

In `DrawingWebApp/src/services/DwgReadAdapter.js` (around line 1504), delete the entire function.

- [ ] **Step 3: Remove call sites**

For each call site found in Step 1, remove the call. If a call site uses the result for downstream computation, that whole computation block must be removed (it depended on unreliable categorization).

- [ ] **Step 4: Lint check**

Run from `DrawingWebApp/`: `npm run lint`. Fix unused imports if any.

- [ ] **Step 5: Verify build still works**

Run: `npm run build`
Expected: build succeeds. If build fails, the deletions broke something — investigate and either reinstate the function (with a TODO to refactor in a follow-up) or fix the dependent code.

- [ ] **Step 6: Commit**

```bash
git add DrawingWebApp/src/services/DwgReadAdapter.js
git commit -m "refactor(memory): remove _categorizeSiteLayer (unreliable layer-name inference)"
```

### Task 1.4: Mark `DrawingTypeSkillProvider` as deprecated

**Files:**
- Modify: `drawing-ai-server/src/main/java/com/lvjian/drawingai/memory/DrawingTypeSkillProvider.java`

- [ ] **Step 1: Add @Deprecated annotation to class**

At the top of `DrawingTypeSkillProvider.java`, change:
```java
@Component
public class DrawingTypeSkillProvider {
```
to:
```java
/**
 * @deprecated since 2026-04-30. Functionality moved to
 *   {@link com.lvjian.drawingai.memory.vision.StageAService}, which combines
 *   drawing-type classification + layout analysis + region detection in a
 *   single vision call. This class is kept for one release cycle to avoid
 *   breaking call sites; will be removed in Plan 2 of the vision-init refactor.
 */
@Deprecated
@Component
public class DrawingTypeSkillProvider {
```

- [ ] **Step 2: Verify compile**

Run from `drawing-ai-server/`:
```bash
mvn compile -q
```
Expected: success (deprecation warning OK, errors not).

- [ ] **Step 3: Commit**

```bash
git add drawing-ai-server/src/main/java/com/lvjian/drawingai/memory/DrawingTypeSkillProvider.java
git commit -m "refactor(memory): mark DrawingTypeSkillProvider @Deprecated

Functionality migrating to StageAService which combines
classification + layout + region detection in a single vision call."
```

---

## Phase 2 — Stage A (full-image vision analysis)

> Goal: implement the new `/init` endpoint and Stage A vision call. After this phase, the frontend can invoke a new pipeline that returns drawingType + drawingUnit + keyRegions, but writes nothing to memory yet.

### Task 2.1: Create Stage A DTOs

**Files:**
- Create: `drawing-ai-server/src/main/java/com/lvjian/drawingai/memory/vision/dto/StageAResult.java`
- Create: `drawing-ai-server/src/main/java/com/lvjian/drawingai/memory/vision/dto/KeyRegion.java`

- [ ] **Step 1: Create StageAResult.java**

```java
package com.lvjian.drawingai.memory.vision.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

/**
 * Stage A — full-image vision analysis result.
 * Spec: docs/specs/2026-04-30-drawing-memory-vision-init-design.md §5.3
 */
public record StageAResult(
    @JsonProperty("drawingType")  String drawingType,    // REGULATORY_PLAN | SITE_PLAN | ARCHITECTURAL_DESIGN | MUNICIPAL_ENGINEERING | LANDSCAPE | OTHER
    @JsonProperty("drawingUnit")  String drawingUnit,    // meter | millimeter | unknown
    @JsonProperty("drawingLayout") String drawingLayout, // free-text layout description, ≤ 200 chars
    @JsonProperty("keyRegions")   List<KeyRegion> keyRegions
) {}
```

- [ ] **Step 2: Create KeyRegion.java**

```java
package com.lvjian.drawingai.memory.vision.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

/**
 * One key region identified by Stage A. bbox is in screen pixel coords of the full screenshot.
 */
public record KeyRegion(
    @JsonProperty("type")           String type,           // 技经表 | 图例 | 主体区
    @JsonProperty("bbox")           List<Integer> bbox,    // [x1, y1, x2, y2] pixel coords (length 4)
    @JsonProperty("splitStrategy")  String splitStrategy,  // single | vertical-N | horizontal-N | grid-MxN
    @JsonProperty("splitReason")    String splitReason,
    @JsonProperty("confidence")     String confidence      // high | mid | low
) {}
```

- [ ] **Step 3: Compile**

Run from `drawing-ai-server/`:
```bash
mvn compile -q
```
Expected: success.

- [ ] **Step 4: Commit**

```bash
git add drawing-ai-server/src/main/java/com/lvjian/drawingai/memory/vision/dto/StageAResult.java drawing-ai-server/src/main/java/com/lvjian/drawingai/memory/vision/dto/KeyRegion.java
git commit -m "feat(memory/vision): add StageAResult and KeyRegion DTOs"
```

### Task 2.2: Implement StageAService

**Files:**
- Create: `drawing-ai-server/src/main/java/com/lvjian/drawingai/memory/vision/StageAService.java`

- [ ] **Step 1: Create StageAService.java skeleton**

```java
package com.lvjian.drawingai.memory.vision;

import com.lvjian.drawingai.memory.vision.dto.StageAResult;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.ai.chat.messages.SystemMessage;
import org.springframework.ai.chat.messages.UserMessage;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.ai.content.Media;
import org.springframework.ai.converter.BeanOutputConverter;
import org.springframework.stereotype.Service;
import org.springframework.util.MimeTypeUtils;

import java.util.Base64;
import java.util.List;

/**
 * Stage A — full-image vision analysis.
 * Single vision call: drawingType + drawingUnit + drawingLayout + keyRegions.
 * Spec: docs/specs/2026-04-30-drawing-memory-vision-init-design.md §5
 */
@Service
public class StageAService {
    private static final Logger log = LoggerFactory.getLogger(StageAService.class);

    private final ChatModel chatModel;

    public StageAService(ChatModel chatModel) {
        this.chatModel = chatModel;
    }

    /**
     * @param fullScreenshotBase64 image data, may be data URL or raw base64. Required.
     * @param layersJson           layer metadata JSON for context, may be empty string.
     * @return StageAResult, or null on parse/timeout failure.
     */
    public StageAResult runStageA(String fullScreenshotBase64, String layersJson) {
        if (fullScreenshotBase64 == null || fullScreenshotBase64.isBlank()) {
            log.warn("[StageA] fullScreenshot is empty; cannot run vision analysis");
            return null;
        }
        try {
            var converter = new BeanOutputConverter<>(StageAResult.class);
            String formatInstructions = converter.getFormat();
            String systemPrompt = SYSTEM_PROMPT + "\n\n" + formatInstructions;

            Media media = buildImageMedia(fullScreenshotBase64);
            if (media == null) {
                log.warn("[StageA] failed to parse screenshot media");
                return null;
            }

            UserMessage userMessage = UserMessage.builder()
                    .text("【图层元数据】\n" + (layersJson == null ? "[]" : layersJson)
                            + "\n\n请分析全图截屏并按指定 schema 输出。")
                    .media(media)
                    .build();

            var prompt = new Prompt(List.of(new SystemMessage(systemPrompt), userMessage));
            var response = chatModel.call(prompt);
            String output = response.getResult().getOutput().getText();
            StageAResult result = converter.convert(output);

            if (result != null) {
                log.info("[StageA] type={}, unit={}, regions={}",
                        result.drawingType(), result.drawingUnit(),
                        result.keyRegions() == null ? 0 : result.keyRegions().size());
            }
            return result;
        } catch (Exception e) {
            log.warn("[StageA] vision call failed: {}", e.getMessage());
            return null;
        }
    }

    private Media buildImageMedia(String base64OrDataUrl) {
        try {
            String raw = base64OrDataUrl;
            var mimeType = MimeTypeUtils.IMAGE_JPEG;
            if (raw.startsWith("data:")) {
                int comma = raw.indexOf(',');
                if (comma == -1) return null;
                if (raw.substring(0, comma).contains("image/png")) {
                    mimeType = MimeTypeUtils.IMAGE_PNG;
                }
                raw = raw.substring(comma + 1);
            }
            byte[] bytes = Base64.getDecoder().decode(raw);
            return Media.builder().mimeType(mimeType).data(bytes).build();
        } catch (Exception e) {
            log.warn("[StageA] base64 decode failed: {}", e.getMessage());
            return null;
        }
    }

    /** Inline SYSTEM_PROMPT — see spec §5.2 for canonical text */
    private static final String SYSTEM_PROMPT = """
        你是 CAD 图纸分析专家。请基于全图截屏 + 图层列表,完成以下任务:

        任务 1 — 判断图纸类型 (drawingType),取值之一:
          REGULATORY_PLAN  (控规图)
          SITE_PLAN        (总平面图)
          ARCHITECTURAL_DESIGN (建筑单体设计图)
          MUNICIPAL_ENGINEERING (市政图)
          LANDSCAPE        (景观图)
          OTHER

        任务 2 — 由 drawingType 派生 drawingUnit:
          REGULATORY_PLAN / SITE_PLAN / LANDSCAPE / MUNICIPAL_ENGINEERING → meter
          ARCHITECTURAL_DESIGN → millimeter
          OTHER → unknown

        任务 3 — 描述全图布局 drawingLayout (≤ 200 字)。

        任务 4 — 识别关键区域 keyRegions,只识别以下三类:
          - 技经表: "技术经济指标表" / "经济指标" / "Indicators" 等
          - 图例: "图例" / "Legend" / 符号说明
          - 主体区: 总平面图的核心绘制区域 (建筑/道路/绿地的主分布区)

          对每个 region 输出:
            type, bbox (屏幕像素坐标 [x1,y1,x2,y2]),
            splitStrategy:
              - 'single': 区域不大或文字不密集,单次重渲足以读清
              - 'vertical-N' (N=2-4): 区域细长,按高度切 N 段
              - 'horizontal-N' (N=2-4): 区域扁平,按宽度切 N 段
              - 'grid-MxN': 区域大且密集,按 M 行 N 列网格切
            splitReason: 一句话理由 (single 时填 'no split needed')
            confidence: high | mid | low

          评估 splitStrategy 的标准:
            - 估算 bbox 在原图的像素尺寸
            - 若区域内文字行数 > 15 且高/宽 > 2 → vertical
            - 若区域内文字列数 > 8 且宽/高 > 2 → horizontal
            - 若两者都大且密集 → grid
            - 其他 → single

        返回严格 JSON,字段全部填,不要 markdown 代码块。
        """;
}
```

- [ ] **Step 2: Compile**

Run from `drawing-ai-server/`:
```bash
mvn compile -q
```
Expected: success. If compile errors about [[Spring AI]] imports, check classpath: confirm `spring-ai-starter-model-openai` version 1.1.2 provides `ChatModel`, `Media`, `BeanOutputConverter`.

- [ ] **Step 3: Commit**

```bash
git add drawing-ai-server/src/main/java/com/lvjian/drawingai/memory/vision/StageAService.java
git commit -m "feat(memory/vision): implement StageAService for full-image analysis

Single vision call returns drawingType + drawingUnit +
drawingLayout + keyRegions[] with splitStrategy. Replaces the
two-step doStage1 (classify) + doStage2 (text-summary) flow.
Spec §5."
```

### Task 2.3: Add unit test for StageAService (mocked ChatModel)

**Files:**
- Create: `drawing-ai-server/src/test/java/com/lvjian/drawingai/memory/vision/StageAServiceTest.java`

- [ ] **Step 1: Write failing test**

```java
package com.lvjian.drawingai.memory.vision;

import com.lvjian.drawingai.memory.vision.dto.StageAResult;
import org.junit.jupiter.api.Test;
import org.springframework.ai.chat.messages.AssistantMessage;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.ai.chat.model.Generation;
import org.springframework.ai.chat.prompt.Prompt;

import java.util.Base64;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

class StageAServiceTest {

    @Test
    void runStageA_parsesValidJsonResponse() {
        ChatModel mockModel = mock(ChatModel.class);
        String mockJson = """
            {
              "drawingType": "SITE_PLAN",
              "drawingUnit": "meter",
              "drawingLayout": "测试布局",
              "keyRegions": [
                {
                  "type": "技经表",
                  "bbox": [100, 200, 400, 500],
                  "splitStrategy": "single",
                  "splitReason": "no split needed",
                  "confidence": "high"
                }
              ]
            }
            """;
        when(mockModel.call(any(Prompt.class))).thenReturn(
            new ChatResponse(List.of(new Generation(new AssistantMessage(mockJson))))
        );

        StageAService service = new StageAService(mockModel);
        // Provide a tiny valid base64 image (1x1 PNG)
        String tinyPng = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkAAIAAAUAAeIVWUMAAAAASUVORK5CYII=";
        StageAResult result = service.runStageA(tinyPng, "[]");

        assertThat(result).isNotNull();
        assertThat(result.drawingType()).isEqualTo("SITE_PLAN");
        assertThat(result.drawingUnit()).isEqualTo("meter");
        assertThat(result.keyRegions()).hasSize(1);
        assertThat(result.keyRegions().get(0).type()).isEqualTo("技经表");
    }

    @Test
    void runStageA_returnsNullForEmptyScreenshot() {
        ChatModel mockModel = mock(ChatModel.class);
        StageAService service = new StageAService(mockModel);
        assertThat(service.runStageA("", "[]")).isNull();
        assertThat(service.runStageA(null, "[]")).isNull();
    }

    @Test
    void runStageA_returnsNullOnChatModelException() {
        ChatModel mockModel = mock(ChatModel.class);
        when(mockModel.call(any(Prompt.class))).thenThrow(new RuntimeException("network down"));
        StageAService service = new StageAService(mockModel);
        String tinyPng = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkAAIAAAUAAeIVWUMAAAAASUVORK5CYII=";
        assertThat(service.runStageA(tinyPng, "[]")).isNull();
    }
}
```

- [ ] **Step 2: Run test (should pass)**

Run from `drawing-ai-server/`:
```bash
mvn test -Dtest=StageAServiceTest -q
```
Expected: 3 tests pass.

If JSON parse fails (BeanOutputConverter strict mode), inspect [[Spring AI]] version's parser behavior. May need to wrap mockJson in `BeanOutputConverter.getFormat()`-compatible structure.

- [ ] **Step 3: Commit**

```bash
git add drawing-ai-server/src/test/java/com/lvjian/drawingai/memory/vision/StageAServiceTest.java
git commit -m "test(memory/vision): unit tests for StageAService"
```

### Task 2.4: Update DrawingMemoryInitService to call StageAService

**Files:**
- Modify: `drawing-ai-server/src/main/java/com/lvjian/drawingai/memory/DrawingMemoryInitService.java`

- [ ] **Step 1: Read DrawingMemoryInitService.java**

Locate `doStage2` method, `SYSTEM_PROMPT` constant, and the public entry method (likely `init(...)`).

- [ ] **Step 2: Inject StageAService into DrawingMemoryInitService**

Add field + constructor parameter:
```java
private final StageAService stageAService;

public DrawingMemoryInitService(/* existing params */, StageAService stageAService) {
    // existing assignments
    this.stageAService = stageAService;
}
```

- [ ] **Step 3: Replace `doStage2` body to call stageAService**

Find the existing `doStage2` method. Replace the body (KEEPING the @Async annotation if present) with:
```java
@Async
public void doStageA(String clientId, String fileId, String fullScreenshotBase64, String layersJson) {
    StageAResult result = stageAService.runStageA(fullScreenshotBase64, layersJson);
    if (result == null) {
        log.warn("[MemoryInit] StageA failed for {}/{}", clientId, fileId);
        memoryStore.markStaleness(clientId, fileId, "stage_a_failed");
        return;
    }
    // Persist drawingType + drawingUnit to summary
    memoryStore.updateSummary(clientId, fileId, summary -> {
        summary.put("drawingType", result.drawingType());
        summary.put("drawingUnit", result.drawingUnit());
        summary.put("drawingLayout", result.drawingLayout());
    });
    // Stage B will be triggered by frontend per region; do not block here.
    log.info("[MemoryInit] StageA complete for {}/{} — drawingType={}, regions={}",
        clientId, fileId, result.drawingType(),
        result.keyRegions() == null ? 0 : result.keyRegions().size());
}
```

(Method renamed to `doStageA` for clarity. Update its single caller in the same file.)

- [ ] **Step 4: Delete old `SYSTEM_PROMPT` constant**

Delete the multi-line string constant (~50-100 lines) labeled "SYSTEM_PROMPT" used by the old text-only stage 2.

- [ ] **Step 5: Update `init()` method signature and body to accept new request shape**

Find the public `init(...)` method (called by controller). Change signature:
```java
public InitResponse init(String clientId, String fileId, InitRequestV2 request) {
    // request: { metadata, fullScreenshot }
    String layersJson = request.metadata() == null ? "[]"
        : new ObjectMapper().writeValueAsString(request.metadata().get("layers"));
    StageAResult stageA = stageAService.runStageA(request.fullScreenshot(), layersJson);
    // Persist immediately (synchronously) so controller can return stageA to frontend
    if (stageA != null) {
        memoryStore.updateSummary(clientId, fileId, s -> {
            s.put("drawingType", stageA.drawingType());
            s.put("drawingUnit", stageA.drawingUnit());
            s.put("drawingLayout", stageA.drawingLayout());
        });
    }
    return new InitResponse(stageA != null, stageA);
}
```

- [ ] **Step 6: Define InitRequestV2 + InitResponse records inline (or in dto/)**

In a fitting place (top of `DrawingMemoryInitService` or new file `dto/InitRequestV2.java`):
```java
public record InitRequestV2(
    Map<String, Object> metadata,
    String fullScreenshot
) {}

public record InitResponse(boolean initialized, StageAResult stageA) {}
```

- [ ] **Step 7: Compile**

Run: `mvn compile -q`. Fix any reference to old `summary` parameter or `comprehensive` in the controller.

- [ ] **Step 8: Run existing tests**

Run: `mvn test -q`. Ensure no regression. If `DrawingMemoryInitServiceTest` breaks, update it minimally to use new signature (or skip with @Disabled and TODO note for follow-up).

- [ ] **Step 9: Commit**

```bash
git add drawing-ai-server/src/main/java/com/lvjian/drawingai/memory/
git commit -m "refactor(memory): rewrite InitService to use StageA vision call

- doStage2 (text-only LLM summarization) → doStageA (vision call)
- Delete obsolete SYSTEM_PROMPT (text summarization no longer used)
- /init now accepts InitRequestV2 { metadata, fullScreenshot }
- Returns StageAResult synchronously so frontend can drive Stage B"
```

### Task 2.5: Update DrawingMemoryController for new /init schema

**Files:**
- Modify: `drawing-ai-server/src/main/java/com/lvjian/drawingai/controller/DrawingMemoryController.java`

- [ ] **Step 1: Read controller and find existing /init endpoint**

Locate the `@PostMapping("/init")` handler. Note its current request body shape.

- [ ] **Step 2: Update /init handler to accept InitRequestV2**

```java
@PostMapping("/{clientId}/{fileId}/init")
public Mono<InitResponse> init(
    @PathVariable String clientId,
    @PathVariable String fileId,
    @RequestBody InitRequestV2 request
) {
    return Mono.fromCallable(() -> initService.init(clientId, fileId, request))
        .subscribeOn(Schedulers.boundedElastic());
}
```

(If the existing controller is non-reactive `@RestController`, keep that style — just change the body type.)

- [ ] **Step 3: Compile**

Run: `mvn compile -q`.

- [ ] **Step 4: Smoke test with curl**

Start server in dev mode (background), then:
```bash
curl -X POST http://localhost:3001/api/ai/drawing-memory/test-client/test-file/init \
  -H "Content-Type: application/json" \
  -d '{"metadata":{"layers":[]},"fullScreenshot":"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkAAIAAAUAAeIVWUMAAAAASUVORK5CYII="}'
```
Expected: 200 with `{"initialized": false, "stageA": null}` (vision call to a 1x1 image will fail/return garbage — expected). If 400/500, review the request body parsing.

(If you don't have time to actually test live, mark as "manual-verification-deferred" but still verify compilation works.)

- [ ] **Step 5: Commit**

```bash
git add drawing-ai-server/src/main/java/com/lvjian/drawingai/controller/DrawingMemoryController.java
git commit -m "feat(memory): controller accepts InitRequestV2 with fullScreenshot"
```

### Task 2.6: Frontend — VisionMemoryPipeline.runStageA and DrawingMemoryApi changes

**Files:**
- Modify: `DrawingWebApp/src/services/DrawingMemoryApi.js`
- Create: `DrawingWebApp/src/services/memory/VisionMemoryPipeline.js`

- [ ] **Step 1: Add postInitV2 to DrawingMemoryApi.js**

Append (or replace existing `initDrawingMemory`):
```javascript
/**
 * V2: 新视觉化 init 接口
 * @param {string} clientId
 * @param {string} fileId
 * @param {{layers: Array, layouts: Array, extents: object, fileName: string}} metadata
 * @param {string} fullScreenshotBase64
 * @returns {Promise<{initialized: boolean, stageA: object|null}>}
 */
export async function postInitV2(clientId, fileId, metadata, fullScreenshotBase64) {
  const url = `/api/ai/drawing-memory/${encodeURIComponent(clientId)}/${encodeURIComponent(fileId)}/init`
  const resp = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ metadata, fullScreenshot: fullScreenshotBase64 }),
  })
  if (!resp.ok) throw new Error(`init failed: ${resp.status} ${await resp.text()}`)
  return await resp.json()
}
```

Keep `initDrawingMemory` (old) for now — it has callers that Plan 2 will migrate.

- [ ] **Step 2: Create [[Vision]]MemoryPipeline.js (Stage A only for now)**

```javascript
import { captureFullExtents } from '../ScreenshotService'
import { postInitV2 } from '../DrawingMemoryApi'

/**
 * VisionMemoryPipeline — Stage A/B 调度入口。
 * Spec: docs/specs/2026-04-30-drawing-memory-vision-init-design.md
 *
 * 当前实现:
 *   - Stage A (此 commit): 调用 /init,获取 drawingType + keyRegions,写元数据
 *   - Stage B (Task 3.x):  TODO,待 Phase 3 实现
 */
export class VisionMemoryPipeline {
  constructor(viewer, Module) {
    this.viewer = viewer
    this.Module = Module
  }

  /**
   * 主入口
   * @returns {Promise<{stageA: object|null, stageB: object|null}>}
   */
  async run(clientId, fileId) {
    const metadata = this._collectMetadata()
    const screenshot = this._captureFull()
    if (!screenshot) {
      return { stageA: null, stageB: null, error: 'screenshot_failed' }
    }
    let stageA
    try {
      const resp = await postInitV2(clientId, fileId, metadata, screenshot)
      stageA = resp.stageA
    } catch (e) {
      console.warn('[VisionMemoryPipeline] Stage A failed:', e.message)
      return { stageA: null, stageB: null, error: 'stage_a_failed' }
    }
    if (!stageA) {
      return { stageA: null, stageB: null, error: 'stage_a_returned_null' }
    }
    // Stage B: implemented in Phase 3
    return { stageA, stageB: null }
  }

  _collectMetadata() {
    const v = this.viewer
    return {
      layers: v.getLayersWithInfo ? v.getLayersWithInfo() : [],
      layouts: v.getLayoutNames ? v.getLayoutNames() : [],
      activeLayout: v.getActiveLayoutName ? v.getActiveLayoutName() : null,
      extents: this._readExtents(),
      fileName: v.getCurrentFileName ? v.getCurrentFileName() : null,
    }
  }

  _readExtents() {
    try {
      const db = this.viewer?.getDb?.() || (this.Module && this.Module.appCore?.getDb?.())
      if (!db || !db.extents) return null
      const e = db.extents
      return { minX: e.minX, minY: e.minY, maxX: e.maxX, maxY: e.maxY }
    } catch (e) {
      return null
    }
  }

  _captureFull() {
    try {
      const shot = captureFullExtents(this.viewer, { quality: 0.8, format: 'image/jpeg' })
      return shot && shot.success ? shot.dataUrl : null
    } catch (e) {
      console.warn('[VisionMemoryPipeline] capture failed:', e)
      return null
    }
  }
}
```

- [ ] **Step 3: Lint check**

Run from `DrawingWebApp/`: `npm run lint`. Expected: clean.

- [ ] **Step 4: Commit**

```bash
git add DrawingWebApp/src/services/DrawingMemoryApi.js DrawingWebApp/src/services/memory/VisionMemoryPipeline.js
git commit -m "feat(memory/vision): VisionMemoryPipeline + postInitV2 (Stage A wiring)"
```

### Task 2.7: Wire VisionMemoryPipeline into AiAssistant.jsx

**Files:**
- Modify: `DrawingWebApp/src/components/AiAssistant/AiAssistant.jsx`

- [ ] **Step 1: Import [[Vision]]MemoryPipeline at top of AiAssistant.jsx**

Add after existing imports (around line 39 area):
```javascript
import { VisionMemoryPipeline } from '../../services/memory/VisionMemoryPipeline'
```

- [ ] **Step 2: Replace `triggerMemoryAutoInit` body**

Find `triggerMemoryAutoInit` (line 505 area). Replace its entire body (between `try {` and `}` finally `}` at end) with the new pipeline call. Keep the WASM-readiness wait, the fileId race guard, and the existing `fetchDrawingMemory` "already exists" check.

```javascript
const triggerMemoryAutoInit = async (clientId, fileId) => {
  if (!clientId || !fileId) return
  if (memoryInitializingRef.current) return
  try {
    const existing = await fetchDrawingMemory(clientId, fileId)
    if (existing && fileIdRef.current === fileId) {
      setDrawingMemory(existing)
      return
    }
  } catch (_) {}
  if (fileIdRef.current !== fileId) return
  memoryInitializingRef.current = true
  setMemoryInitializing(true)
  try {
    // wait for WASM viewer (15s budget)
    let waited = 0
    while (waited < 15000) {
      const v = viewerRef?.current
      const m = moduleRef?.current || (typeof window !== 'undefined' ? window.Module : null)
      if (v && m) break
      await new Promise(r => setTimeout(r, 500))
      waited += 500
    }
    const viewer = viewerRef?.current
    const Module = moduleRef?.current || (typeof window !== 'undefined' ? window.Module : null)
    if (!viewer || !Module) {
      console.warn('[MemoryAutoInit] viewer/module not ready', { fileId })
      return
    }
    if (fileIdRef.current !== fileId) return

    const pipeline = new VisionMemoryPipeline(viewer, Module)
    const result = await pipeline.run(clientId, fileId)
    if (fileIdRef.current !== fileId) return
    if (result.error) {
      console.warn('[MemoryAutoInit] pipeline error:', result.error)
      return
    }
    // After Stage A, fetch updated memory to display drawingType
    const m = await fetchDrawingMemory(clientId, fileId).catch(() => null)
    if (m && fileIdRef.current === fileId) setDrawingMemory(m)
    console.log('[MemoryAutoInit] Stage A complete:', result.stageA?.drawingType)
  } catch (e) {
    console.warn('[MemoryAutoInit] failed:', e)
  } finally {
    memoryInitializingRef.current = false
    setMemoryInitializing(false)
  }
}
```

- [ ] **Step 3: Flip AUTO_DRAWING_ANALYSIS_ENABLED to true**

In `AiAssistant.jsx` line 49:
```javascript
const AUTO_DRAWING_ANALYSIS_ENABLED = true
```
Update the comment block above to remove "已暂停" — change to:
```javascript
/**
 * 自动归纳总开关。打开图纸 → VisionMemoryPipeline → Stage A 全图分析 → 写元数据。
 * Stage B 由 Phase 3 接入,本 commit 后 Stage A 可独立工作。
 * 设计文档: docs/specs/2026-04-30-drawing-memory-vision-init-design.md
 */
const AUTO_DRAWING_ANALYSIS_ENABLED = true
```

- [ ] **Step 4: Lint check**

`npm run lint` — fix any unused-import warnings (e.g., if `summarizeForMemoryInit` / `runLandBoundaryVisionTest` are no longer called in this file, ESLint may warn — comment them out for now since Plan 2 handles their full removal).

- [ ] **Step 5: Build check**

`npm run build` — must succeed.

- [ ] **Step 6: Manual verification (live test)**

In one terminal: `cd drawing-ai-server && mvn spring-boot:run`
In another: `cd DrawingWebApp && npm run dev`
Open browser to http://localhost:3000, open any DWG file.
**Expected:**
- Console log shows `[VisionMemoryPipeline] Stage A failed` OR `[MemoryAutoInit] Stage A complete: SITE_PLAN` (or some drawingType)
- Network tab: POST to `/api/ai/drawing-memory/.../init` with body containing `metadata` + `fullScreenshot`
- Right sidebar AiAssistant shows drawingType (if Stage A succeeded)

If vision model not configured, expect Stage A to fail gracefully (no crash, error logged).

- [ ] **Step 7: Commit**

```bash
git add DrawingWebApp/src/components/AiAssistant/AiAssistant.jsx
git commit -m "feat(memory): wire VisionMemoryPipeline into auto-init

Replaces triggerMemoryAutoInit body with VisionMemoryPipeline.run().
Re-enables AUTO_DRAWING_ANALYSIS_ENABLED. Stage A only — Stage B
arrives in Phase 3."
```

---

## Phase 3 — Stage B (region-by-region precise reading)

> Goal: implement Stage B end-to-end. After this phase, opening a drawing produces full memory init with mainAreaDescription, keyAnnotations, candidateObjects, layerSemantics, and keyFacts.

### Task 3.1: Create sliceBbox.js + tests

**Files:**
- Create: `DrawingWebApp/src/services/memory/sliceBbox.js`
- Create: `DrawingWebApp/src/services/memory/__tests__/sliceBbox.test.js`

- [ ] **Step 1: Write failing tests**

Create `DrawingWebApp/src/services/memory/__tests__/sliceBbox.test.js`:
```javascript
import { describe, it, expect } from 'vitest'
import { sliceBbox } from '../sliceBbox'

describe('sliceBbox', () => {
  const bbox = [100, 200, 500, 800]  // 400 wide, 600 tall

  it('returns same bbox for single', () => {
    expect(sliceBbox(bbox, 'single')).toEqual([bbox])
  })

  it('vertical-2 splits by height into top and bottom halves', () => {
    expect(sliceBbox(bbox, 'vertical-2')).toEqual([
      [100, 200, 500, 500],  // top half
      [100, 500, 500, 800],  // bottom half
    ])
  })

  it('vertical-3 produces three equal vertical slices', () => {
    const tiles = sliceBbox(bbox, 'vertical-3')
    expect(tiles).toHaveLength(3)
    expect(tiles[0]).toEqual([100, 200, 500, 400])
    expect(tiles[1]).toEqual([100, 400, 500, 600])
    expect(tiles[2]).toEqual([100, 600, 500, 800])
  })

  it('horizontal-2 splits by width', () => {
    expect(sliceBbox(bbox, 'horizontal-2')).toEqual([
      [100, 200, 300, 800],  // left half
      [300, 200, 500, 800],  // right half
    ])
  })

  it('grid-2x2 produces 4 quadrants', () => {
    const tiles = sliceBbox(bbox, 'grid-2x2')
    expect(tiles).toHaveLength(4)
    // row 0, col 0 (top-left)
    expect(tiles[0]).toEqual([100, 200, 300, 500])
    // row 0, col 1 (top-right)
    expect(tiles[1]).toEqual([300, 200, 500, 500])
    // row 1, col 0 (bottom-left)
    expect(tiles[2]).toEqual([100, 500, 300, 800])
    // row 1, col 1 (bottom-right)
    expect(tiles[3]).toEqual([300, 500, 500, 800])
  })

  it('grid-2x3 produces 6 cells (2 rows, 3 cols)', () => {
    const tiles = sliceBbox(bbox, 'grid-2x3')
    expect(tiles).toHaveLength(6)
  })

  it('falls back to single bbox for unknown strategy', () => {
    expect(sliceBbox(bbox, 'unknown-strategy')).toEqual([bbox])
    expect(sliceBbox(bbox, '')).toEqual([bbox])
  })
})
```

- [ ] **Step 2: Run test to verify it fails**

Run from `DrawingWebApp/`: `npm test`
Expected: FAIL with "Cannot find module '../sliceBbox'".

- [ ] **Step 3: Implement sliceBbox.js**

```javascript
/**
 * Slice a bbox into N tiles per the splitStrategy.
 * Spec: docs/specs/2026-04-30-drawing-memory-vision-init-design.md §6.2
 *
 * @param {[number,number,number,number]} bbox  [x1, y1, x2, y2] in screen pixel coords
 * @param {string} strategy  'single' | 'vertical-N' | 'horizontal-N' | 'grid-MxN'
 * @returns {Array<[number,number,number,number]>}  Array of sub-bboxes
 */
export function sliceBbox(bbox, strategy) {
  const [x1, y1, x2, y2] = bbox
  if (strategy === 'single') return [bbox]

  const verticalMatch = String(strategy).match(/^vertical-(\d+)$/)
  if (verticalMatch) {
    const n = +verticalMatch[1]
    const h = (y2 - y1) / n
    return Array.from({ length: n }, (_, i) =>
      [x1, y1 + i * h, x2, y1 + (i + 1) * h]
    )
  }

  const horizontalMatch = String(strategy).match(/^horizontal-(\d+)$/)
  if (horizontalMatch) {
    const n = +horizontalMatch[1]
    const w = (x2 - x1) / n
    return Array.from({ length: n }, (_, i) =>
      [x1 + i * w, y1, x1 + (i + 1) * w, y2]
    )
  }

  const gridMatch = String(strategy).match(/^grid-(\d+)x(\d+)$/)
  if (gridMatch) {
    const m = +gridMatch[1]
    const n = +gridMatch[2]
    const w = (x2 - x1) / n
    const h = (y2 - y1) / m
    const tiles = []
    for (let r = 0; r < m; r++) {
      for (let c = 0; c < n; c++) {
        tiles.push([x1 + c * w, y1 + r * h, x1 + (c + 1) * w, y1 + (r + 1) * h])
      }
    }
    return tiles
  }

  // unknown strategy → fallback to single
  return [bbox]
}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `npm test`
Expected: 7 tests pass in sliceBbox.test.js.

- [ ] **Step 5: Commit**

```bash
git add DrawingWebApp/src/services/memory/sliceBbox.js DrawingWebApp/src/services/memory/__tests__/sliceBbox.test.js
git commit -m "feat(memory/vision): sliceBbox utility + unit tests"
```

### Task 3.2: Create captureRegionTiles helper

**Files:**
- Create: `DrawingWebApp/src/services/memory/captureRegionTiles.js`

- [ ] **Step 1: Implement captureRegionTiles**

```javascript
import { sliceBbox } from './sliceBbox'

/**
 * For one keyRegion, slice the bbox per splitStrategy, zoom & capture each tile.
 * Returns N base64 image data URLs.
 *
 * @param {object} viewer  ODA viewer instance
 * @param {object} keyRegion  { type, bbox, splitStrategy, ... }
 * @param {object} options  { quality, format }
 * @returns {Promise<string[]>}  Array of data URLs (jpeg/png)
 */
export async function captureRegionTiles(viewer, keyRegion, options = {}) {
  const { quality = 0.85, format = 'image/jpeg' } = options
  const tiles = sliceBbox(keyRegion.bbox, keyRegion.splitStrategy)
  const images = []
  for (const tile of tiles) {
    // Note: ODA viewer.zoomTo expects WORLD coords by default. The keyRegion bbox
    // is in SCREEN PIXEL coords (per Stage A prompt). Convert before zoom.
    const worldBbox = _screenBboxToWorld(viewer, tile)
    if (!worldBbox) {
      console.warn('[captureRegionTiles] screen→world conversion failed for tile', tile)
      continue
    }
    await _zoomToBbox(viewer, worldBbox)
    // Small wait for ODA repaint (yields the event loop)
    await new Promise(r => requestAnimationFrame(() => r()))
    const shot = _captureCurrentView(viewer, { quality, format })
    if (shot && shot.dataUrl) images.push(shot.dataUrl)
  }
  return images
}

/**
 * Convert [x1,y1,x2,y2] in screen pixel coords to world coords.
 * Uses viewer.screenToWorld for each corner.
 */
function _screenBboxToWorld(viewer, [x1, y1, x2, y2]) {
  if (typeof viewer.screenToWorld !== 'function') return null
  try {
    const tl = viewer.screenToWorld(x1, y1)
    const br = viewer.screenToWorld(x2, y2)
    if (!tl || !br) return null
    // Normalize (in case y-axis flips between screen and world)
    return {
      minX: Math.min(tl.x, br.x),
      minY: Math.min(tl.y, br.y),
      maxX: Math.max(tl.x, br.x),
      maxY: Math.max(tl.y, br.y),
    }
  } catch (e) {
    return null
  }
}

async function _zoomToBbox(viewer, world) {
  if (typeof viewer.zoomToWindow === 'function') {
    return viewer.zoomToWindow(world.minX, world.minY, world.maxX, world.maxY)
  }
  if (typeof viewer.zoomTo === 'function') {
    return viewer.zoomTo(world)
  }
  throw new Error('viewer has no zoomToWindow or zoomTo method')
}

function _captureCurrentView(viewer, opts) {
  // Reuse existing ScreenshotService if it exposes captureCurrentView
  try {
    const { captureCurrentView } = require('../ScreenshotService')
    return captureCurrentView(viewer, opts)
  } catch (e) {
    // Fallback: use viewer's built-in
    const canvas = viewer.getCanvas?.() || document.querySelector('canvas')
    if (!canvas) return null
    return { dataUrl: canvas.toDataURL(opts.format, opts.quality), success: true }
  }
}
```

- [ ] **Step 2: Verify ScreenshotService.captureCurrentView signature**

Read `DrawingWebApp/src/services/ScreenshotService.js`. Confirm `captureCurrentView(viewer, options)` exists and returns `{success, dataUrl}`. If signature differs, adjust the fallback in `_captureCurrentView` accordingly.

If `ScreenshotService` is ES module (it is — Vite project), replace `require()` call with proper import:
```javascript
import { captureCurrentView } from '../ScreenshotService'
```
and inline the call directly without `_captureCurrentView` wrapper.

- [ ] **Step 3: Verify viewer.zoomToWindow exists**

Run via Grep: `pattern: zoomToWindow|zoomTo\b, glob: src/services/ViewerService.js`. Confirm the actual method name on the Viewer prototype. Adjust call accordingly.

- [ ] **Step 4: Lint check**

`npm run lint` — clean.

- [ ] **Step 5: Commit**

```bash
git add DrawingWebApp/src/services/memory/captureRegionTiles.js
git commit -m "feat(memory/vision): captureRegionTiles helper

Slices keyRegion bbox per splitStrategy, zooms to each tile via
ODA viewer, captures sharp screenshot. Screen→world conversion
handled inline."
```

### Task 3.3: Backend — Stage B DTOs

**Files:**
- Create: `drawing-ai-server/src/main/java/com/lvjian/drawingai/memory/vision/dto/CandidateObject.java`
- Create: `drawing-ai-server/src/main/java/com/lvjian/drawingai/memory/vision/dto/KeyAnnotation.java`
- Create: `drawing-ai-server/src/main/java/com/lvjian/drawingai/memory/vision/dto/RegionResult.java`
- Create: `drawing-ai-server/src/main/java/com/lvjian/drawingai/memory/vision/dto/IndicatorTableResult.java`
- Create: `drawing-ai-server/src/main/java/com/lvjian/drawingai/memory/vision/dto/LegendResult.java`
- Create: `drawing-ai-server/src/main/java/com/lvjian/drawingai/memory/vision/dto/MainAreaResult.java`

- [ ] **Step 1: Create KeyAnnotation.java**

```java
package com.lvjian.drawingai.memory.vision.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public record KeyAnnotation(
    @JsonProperty("text") String text,
    @JsonProperty("confidence") String confidence  // high | mid | low
) {}
```

- [ ] **Step 2: Create CandidateObject.java**

```java
package com.lvjian.drawingai.memory.vision.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

public record CandidateObject(
    @JsonProperty("guess") String guess,        // 用地红线 | 建筑退让线 | 建筑单体 | 道路 | 绿地 | 广场 | 停车场 | 其他
    @JsonProperty("bbox") List<Integer> bbox,  // [x1, y1, x2, y2] screen pixel coords
    @JsonProperty("count") Integer count,
    @JsonProperty("confidence") String confidence
) {}
```

- [ ] **Step 3: Create IndicatorTableResult.java**

```java
package com.lvjian.drawingai.memory.vision.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

public record IndicatorTableResult(
    @JsonProperty("keyFacts") List<KeyFactItem> keyFacts,
    @JsonProperty("_meta") MetaSection meta
) {
    public record KeyFactItem(
        @JsonProperty("name") String name,
        @JsonProperty("value") Object value,    // Number or String (some indicators non-numeric)
        @JsonProperty("unit") String unit,
        @JsonProperty("confidence") String confidence
    ) {}

    public record MetaSection(
        @JsonProperty("extractedComplete") boolean extractedComplete,
        @JsonProperty("suggestedReSlice") String suggestedReSlice
    ) {}
}
```

- [ ] **Step 4: Create LegendResult.java**

```java
package com.lvjian.drawingai.memory.vision.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

/**
 * Legend region output.
 * **Note**: We do NOT map legend items to drawing layer names — the legend
 * describes visual conventions, which often don't align with actual layer
 * names. Layer semantic mapping is populated separately via LLM update_drawing_memory.
 * Spec §6.3.2.
 */
public record LegendResult(
    @JsonProperty("legendItems") List<LegendItem> legendItems,
    @JsonProperty("_meta") IndicatorTableResult.MetaSection meta
) {
    public record LegendItem(
        @JsonProperty("description") String description, // 图例右侧文字 (原文)
        @JsonProperty("visualKind") String visualKind,   // 'line' | 'symbol' | 'pattern'
        @JsonProperty("color") String color,             // "#RRGGBB" or ""
        @JsonProperty("lineType") String lineType,       // solid|dashed|dot-dash|dotted|double, or null
        @JsonProperty("symbol") String symbol,           // free-text shape description, or null
        @JsonProperty("pattern") String pattern,         // free-text fill description, or null
        @JsonProperty("confidence") String confidence
    ) {}
}
```

- [ ] **Step 5: Create MainAreaResult.java**

```java
package com.lvjian.drawingai.memory.vision.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

public record MainAreaResult(
    @JsonProperty("mainAreaDescription") String mainAreaDescription,
    @JsonProperty("keyAnnotations") List<KeyAnnotation> keyAnnotations,
    @JsonProperty("candidateObjects") List<CandidateObject> candidateObjects,
    @JsonProperty("_meta") IndicatorTableResult.MetaSection meta
) {}
```

- [ ] **Step 6: Create RegionResult.java (envelope)**

```java
package com.lvjian.drawingai.memory.vision.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonInclude(JsonInclude.Include.NON_NULL)
public record RegionResult(
    @JsonProperty("regionType") String regionType,
    @JsonProperty("indicatorTable") IndicatorTableResult indicatorTable,
    @JsonProperty("legend") LegendResult legend,
    @JsonProperty("mainArea") MainAreaResult mainArea,
    @JsonProperty("confidence") String confidence,
    @JsonProperty("stalenessReasons") java.util.List<String> stalenessReasons
) {
    public static RegionResult forIndicatorTable(IndicatorTableResult r, String confidence, java.util.List<String> staleness) {
        return new RegionResult("技经表", r, null, null, confidence, staleness);
    }
    public static RegionResult forLegend(LegendResult r, String confidence, java.util.List<String> staleness) {
        return new RegionResult("图例", null, r, null, confidence, staleness);
    }
    public static RegionResult forMainArea(MainAreaResult r, String confidence, java.util.List<String> staleness) {
        return new RegionResult("主体区", null, null, r, confidence, staleness);
    }
}
```

- [ ] **Step 7: Compile**

Run from `drawing-ai-server/`: `mvn compile -q`. Expected: success.

- [ ] **Step 8: Commit**

```bash
git add drawing-ai-server/src/main/java/com/lvjian/drawingai/memory/vision/dto/
git commit -m "feat(memory/vision): Stage B DTOs (CandidateObject, KeyAnnotation, RegionResult etc.)"
```

### Task 3.4: Backend — Region prompt builders

**Files:**
- Create: `drawing-ai-server/src/main/java/com/lvjian/drawingai/memory/vision/regions/IndicatorTablePromptBuilder.java`
- Create: `drawing-ai-server/src/main/java/com/lvjian/drawingai/memory/vision/regions/LegendPromptBuilder.java`
- Create: `drawing-ai-server/src/main/java/com/lvjian/drawingai/memory/vision/regions/MainAreaPromptBuilder.java`

- [ ] **Step 1: Create IndicatorTablePromptBuilder.java**

```java
package com.lvjian.drawingai.memory.vision.regions;

/**
 * Spec: docs/specs/2026-04-30-drawing-memory-vision-init-design.md §6.3.1
 */
public final class IndicatorTablePromptBuilder {
    private IndicatorTablePromptBuilder() {}

    public static final String SYSTEM_PROMPT = """
        你看到的是一张技术经济指标表的截图 (可能由 N 个切片拼接,从上到下 / 从左到右排列)。

        请把表格中**所有可见的行**逐项提取(不论是常见规范指标、项目特异指标、备注、公式、引用条文、文字说明等),
        输出 keyFacts 列表,每项:
          { name, value, unit, confidence }

        字段说明:
          - name:  表格行的名称(原文,不要意译)
          - value:
              * 数值型: 输出数字 (12345 而非 "12345 ㎡")
              * 文本型: 直接输出字符串 (如 "居住用地" / "甲级" / "见图签" / "≥50%")
              * 含范围: 如 "1.0~1.5" 直接作为字符串
          - unit:  单位 (㎡ / m / % / 栋 / kV / dB ...);无单位时填空字符串
          - confidence: high | mid | low

        约束:
          - **完整性优先**:不要遗漏任何一行,包括备注栏、合计栏、表头说明
          - 同名行多次出现,各自独立 entry,可在 name 末尾加序号 (如 "建筑高度 #2")
          - 模糊不清或多义的标 confidence='low' 但仍要输出
          - 严格 JSON,不要 markdown 代码块

        额外字段(必填):
          "_meta": {
            "extractedComplete": true | false,
            "suggestedReSlice": null | "vertical-N" | "horizontal-N" | "grid-MxN"
          }
        """;

    public static String userPromptText(int tileCount) {
        if (tileCount <= 1) {
            return "请提取此技经表的全部行。";
        }
        return String.format("以下 %d 张图片是同一个技经表从上到下/从左到右切出的相邻切片,请合并提取所有行。", tileCount);
    }
}
```

- [ ] **Step 2: Create LegendPromptBuilder.java**

```java
package com.lvjian.drawingai.memory.vision.regions;

/**
 * Spec: §6.3.2
 * Note: We do NOT match legend entries to drawing layer names. Legend describes
 * visual conventions; layer names are internal organization names — they
 * frequently disagree.
 */
public final class LegendPromptBuilder {
    private LegendPromptBuilder() {}

    public static final String SYSTEM_PROMPT = """
        你看到的是图例区域的截图。

        请提取每个图例条目,**只输出视觉信息**(描述 + 颜色 + 形状),
        **不要尝试与图纸图层名匹配**——图例标注的是视觉约定,与实际图层名常不一致。

        输出 legendItems 列表,每项:
          {
            description: 图例右侧文字描述 (原文,如 "规划用地红线" / "建筑退线" / "园区道路"),
            visualKind:  'line' | 'symbol' | 'pattern',
            color:       16 进制 #RRGGBB,看不清填 ""(尽量给主色),
            lineType:    仅当 visualKind='line' 时填: 'solid' | 'dashed' | 'dot-dash' | 'dotted' | 'double',
            symbol:      仅当 visualKind='symbol' 时填: 简短形状描述 (如 "红色实心箭头" / "黄色三角形"),
            pattern:     仅当 visualKind='pattern' 时填: 简短描述 (如 "绿色斜线填充" / "橙色网格"),
            confidence: high | mid | low
          }

        约束:
          - 输出顺序按图例从上到下、从左到右
          - 多列布局的图例(常见左右两列)按列内顺序输出
          - 颜色尽量用 #RRGGBB 表达,实在辨别不清才填空字符串
          - 不输出空行 / 表头 / 边框
          - 严格 JSON,不要 markdown 代码块

        额外字段(必填):
          "_meta": {
            "extractedComplete": true | false,
            "suggestedReSlice": null | "vertical-N" | "horizontal-N" | "grid-MxN"
          }
        """;

    public static String userPromptText(int tileCount) {
        return tileCount <= 1
            ? "请按 schema 提取图例的全部条目。"
            : String.format("以下 %d 张图片是图例区域的相邻切片,请合并提取。", tileCount);
    }
}
```

- [ ] **Step 3: Create MainAreaPromptBuilder.java**

```java
package com.lvjian.drawingai.memory.vision.regions;

/**
 * Spec: §6.3.3
 */
public final class MainAreaPromptBuilder {
    private MainAreaPromptBuilder() {}

    public static final String SYSTEM_PROMPT = """
        你看到的是总平面图的主体绘制区。

        请同时输出三件事:

        任务 1 — 场景描述 mainAreaDescription (≤ 300 字):
          描述场地形状 / 主入口位置 / 建筑分布 / 绿地分布 / 道路网络 / 特殊元素

        任务 2 — 关键标注 keyAnnotations:
          [{ text: '住宅楼 1F=4.5m', confidence: 'high' }, ...]
          捕捉建筑功能 / 层数 / 高度 / 道路宽度 / 绿地名称等图面文字标注

        任务 3 — 候选对象 candidateObjects:
          [
            {
              guess: '用地红线' | '建筑退让线' | '建筑单体' | '道路' | '绿地'
                   | '广场' | '停车场' | '其他',
              bbox: [x1, y1, x2, y2],   // 屏幕像素坐标
              count: number,             // 该类型对象的数量 (建筑单体 5 栋则 count=5)
              confidence: high | mid | low
            },
            ...
          ]
          要求:
            - 精确度优先 (能给单个 bbox 就不给整片)
            - 同类型多个对象,每个独立 entry
            - bbox 紧贴对象,不要包含周围空白

        额外字段(必填):
          "_meta": {
            "extractedComplete": true | false,
            "suggestedReSlice": null | 'vertical-N' | 'horizontal-N' | 'grid-MxN'
          }

        严格 JSON,不要 markdown 代码块。
        """;

    public static String userPromptText(int tileCount) {
        return tileCount <= 1
            ? "请按 schema 提取主体区的描述、标注、候选对象。"
            : String.format("以下 %d 张图片是主体区相邻切片,请合并提取。", tileCount);
    }
}
```

- [ ] **Step 4: Compile**

`mvn compile -q`. Expected: success.

- [ ] **Step 5: Commit**

```bash
git add drawing-ai-server/src/main/java/com/lvjian/drawingai/memory/vision/regions/
git commit -m "feat(memory/vision): region-specific prompt builders"
```

### Task 3.5: Backend — StageBService

**Files:**
- Create: `drawing-ai-server/src/main/java/com/lvjian/drawingai/memory/vision/StageBService.java`

- [ ] **Step 1: Implement StageBService**

```java
package com.lvjian.drawingai.memory.vision;

import com.lvjian.drawingai.memory.vision.dto.*;
import com.lvjian.drawingai.memory.vision.regions.IndicatorTablePromptBuilder;
import com.lvjian.drawingai.memory.vision.regions.LegendPromptBuilder;
import com.lvjian.drawingai.memory.vision.regions.MainAreaPromptBuilder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.ai.chat.messages.SystemMessage;
import org.springframework.ai.chat.messages.UserMessage;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.ai.content.Media;
import org.springframework.ai.converter.BeanOutputConverter;
import org.springframework.stereotype.Service;
import org.springframework.util.MimeTypeUtils;

import java.util.ArrayList;
import java.util.Base64;
import java.util.List;

/**
 * Stage B — region-by-region precise reading.
 * Spec: §6
 */
@Service
public class StageBService {
    private static final Logger log = LoggerFactory.getLogger(StageBService.class);

    private final ChatModel chatModel;

    public StageBService(ChatModel chatModel) {
        this.chatModel = chatModel;
    }

    public RegionResult readIndicatorTable(List<String> imagesBase64) {
        try {
            var converter = new BeanOutputConverter<>(IndicatorTableResult.class);
            String systemText = IndicatorTablePromptBuilder.SYSTEM_PROMPT + "\n\n" + converter.getFormat();
            String userText = IndicatorTablePromptBuilder.userPromptText(imagesBase64.size());
            IndicatorTableResult parsed = callMultiImage(systemText, userText, imagesBase64, converter);
            if (parsed == null) {
                return RegionResult.forIndicatorTable(null, "low", List.of("region_技经表_failed"));
            }
            return RegionResult.forIndicatorTable(parsed, aggregateConfidence(parsed.keyFacts(), KeyFactItemConfidence::ofItem), stalenessFromMeta(parsed.meta(), "技经表"));
        } catch (Exception e) {
            log.warn("[StageB.indicatorTable] failed: {}", e.getMessage());
            return RegionResult.forIndicatorTable(null, "low", List.of("region_技经表_failed"));
        }
    }

    public RegionResult readLegend(List<String> imagesBase64) {
        try {
            var converter = new BeanOutputConverter<>(LegendResult.class);
            String systemText = LegendPromptBuilder.SYSTEM_PROMPT + "\n\n" + converter.getFormat();
            String userText = LegendPromptBuilder.userPromptText(imagesBase64.size());
            LegendResult parsed = callMultiImage(systemText, userText, imagesBase64, converter);
            if (parsed == null) {
                return RegionResult.forLegend(null, "low", List.of("region_图例_failed"));
            }
            return RegionResult.forLegend(parsed, aggregateConfidenceLegend(parsed.legendItems()), stalenessFromMeta(parsed.meta(), "图例"));
        } catch (Exception e) {
            log.warn("[StageB.legend] failed: {}", e.getMessage());
            return RegionResult.forLegend(null, "low", List.of("region_图例_failed"));
        }
    }

    public RegionResult readMainArea(List<String> imagesBase64) {
        try {
            var converter = new BeanOutputConverter<>(MainAreaResult.class);
            String systemText = MainAreaPromptBuilder.SYSTEM_PROMPT + "\n\n" + converter.getFormat();
            String userText = MainAreaPromptBuilder.userPromptText(imagesBase64.size());
            MainAreaResult parsed = callMultiImage(systemText, userText, imagesBase64, converter);
            if (parsed == null) {
                return RegionResult.forMainArea(null, "low", List.of("region_主体区_failed"));
            }
            return RegionResult.forMainArea(parsed, "high", stalenessFromMeta(parsed.meta(), "主体区"));
        } catch (Exception e) {
            log.warn("[StageB.mainArea] failed: {}", e.getMessage());
            return RegionResult.forMainArea(null, "low", List.of("region_主体区_failed"));
        }
    }

    private <T> T callMultiImage(String systemText, String userText, List<String> imagesBase64, BeanOutputConverter<T> converter) {
        List<Media> medias = new ArrayList<>();
        for (String img : imagesBase64) {
            Media m = buildImageMedia(img);
            if (m != null) medias.add(m);
        }
        if (medias.isEmpty()) return null;

        UserMessage userMessage = UserMessage.builder()
                .text(userText)
                .media(medias.toArray(new Media[0]))
                .build();
        var prompt = new Prompt(List.of(new SystemMessage(systemText), userMessage));
        var response = chatModel.call(prompt);
        String output = response.getResult().getOutput().getText();
        return converter.convert(output);
    }

    private Media buildImageMedia(String base64OrDataUrl) {
        try {
            String raw = base64OrDataUrl;
            var mime = MimeTypeUtils.IMAGE_JPEG;
            if (raw.startsWith("data:")) {
                int comma = raw.indexOf(',');
                if (comma == -1) return null;
                if (raw.substring(0, comma).contains("image/png")) mime = MimeTypeUtils.IMAGE_PNG;
                raw = raw.substring(comma + 1);
            }
            return Media.builder().mimeType(mime).data(Base64.getDecoder().decode(raw)).build();
        } catch (Exception e) {
            return null;
        }
    }

    private List<String> stalenessFromMeta(IndicatorTableResult.MetaSection meta, String regionType) {
        List<String> reasons = new ArrayList<>();
        if (meta != null && !meta.extractedComplete()) {
            reasons.add("extracted_partial_" + regionType);
        }
        return reasons;
    }

    private interface KeyFactItemConfidence {
        static String ofItem(IndicatorTableResult.KeyFactItem item) {
            return item == null ? "low" : item.confidence();
        }
    }

    private <T> String aggregateConfidence(List<T> items, java.util.function.Function<T, String> extractor) {
        if (items == null || items.isEmpty()) return "low";
        long lowCount = items.stream().map(extractor).filter("low"::equalsIgnoreCase).count();
        return (lowCount * 2 > items.size()) ? "low" : "mid";
    }

    private String aggregateConfidenceLegend(List<LegendResult.LegendItem> items) {
        if (items == null || items.isEmpty()) return "low";
        long lowCount = items.stream().map(LegendResult.LegendItem::confidence).filter("low"::equalsIgnoreCase).count();
        return (lowCount * 2 > items.size()) ? "low" : "mid";
    }
}
```

- [ ] **Step 2: Compile**

`mvn compile -q`. Fix any import errors. **Note**: `UserMessage.builder().media(Media...)` varargs — verify this signature exists in [[Spring AI]] 1.1.2. If not, change to chained `.media(m1).media(m2)` calls in a loop.

- [ ] **Step 3: Commit**

```bash
git add drawing-ai-server/src/main/java/com/lvjian/drawingai/memory/vision/StageBService.java
git commit -m "feat(memory/vision): StageBService — multi-image region reading"
```

### Task 3.6: Backend — DrawingMemory schema additions

**Files:**
- Modify: `drawing-ai-server/src/main/java/com/lvjian/drawingai/memory/DrawingMemory.java`
- Modify: `drawing-ai-server/src/main/java/com/lvjian/drawingai/memory/DrawingMemoryStore.java`

- [ ] **Step 1: Add fields to DrawingMemory**

Read `DrawingMemory.java`. Add four new fields:
```java
// existing fields ...
private String mainAreaDescription;
private List<KeyAnnotation> keyAnnotations;
private List<CandidateObject> candidateObjects;
private List<LegendResult.LegendItem> legendItems;

// imports
import com.lvjian.drawingai.memory.vision.dto.KeyAnnotation;
import com.lvjian.drawingai.memory.vision.dto.CandidateObject;
import com.lvjian.drawingai.memory.vision.dto.LegendResult;
```

> **Note**: `layerSemantics` (existing section) is **NOT** populated by Stage B legend.
> The legend produces `legendItems` (visual-only). Layer-name semantic mapping
> remains the responsibility of LLM `update_drawing_memory` during conversation.
> Spec §6.3.2 / §8.1.

Add getters/setters or update the record signature accordingly. (Inspect the actual file first — if it's a record, add fields to the constructor; if a class, add fields + accessors.)

- [ ] **Step 2: Add `drawingUnit` to Summary section**

Find the `Summary` inner type or constant. Add `drawingUnit` to it. Update its `keys()` / `VALID_SECTIONS` set if any.

- [ ] **Step 3: Update DrawingMemoryStore Redis serialization**

In `DrawingMemoryStore.java`, find where each section is serialized to Redis hash. Add four new sections:
- `main-area` — JSON of mainAreaDescription
- `key-annotations` — JSON list of KeyAnnotation
- `candidate-objects` — JSON list of CandidateObject
- `legend-items` — JSON list of LegendItem

Add corresponding write methods:
```java
public void saveMainArea(String clientId, String fileId, String description) { ... }
public void saveKeyAnnotations(String clientId, String fileId, List<KeyAnnotation> list) { ... }
public void saveCandidateObjects(String clientId, String fileId, List<CandidateObject> list) { ... }
public void saveLegendItems(String clientId, String fileId, List<LegendResult.LegendItem> list) { ... }
```
And read methods that populate the new fields when loading.

Update `VALID_SECTIONS` set to include the four new keys.

- [ ] **Step 4: Compile + run tests**

`mvn compile -q && mvn test -q`. If existing memory tests break (e.g., section count), adjust them.

- [ ] **Step 5: Commit**

```bash
git add drawing-ai-server/src/main/java/com/lvjian/drawingai/memory/DrawingMemory.java drawing-ai-server/src/main/java/com/lvjian/drawingai/memory/DrawingMemoryStore.java
git commit -m "feat(memory): add mainAreaDescription, keyAnnotations, candidateObjects sections

DrawingMemory schema gains three new sections populated by Stage B.
Redis hash backward compatible (additive)."
```

### Task 3.7: Backend — /region endpoint in controller

**Files:**
- Modify: `drawing-ai-server/src/main/java/com/lvjian/drawingai/controller/DrawingMemoryController.java`

- [ ] **Step 1: Add /region endpoint**

```java
public record RegionRequest(
    String regionType,                 // 技经表 | 图例 | 主体区
    java.util.List<String> images      // base64 data URLs (1 or N tiles)
) {}

@PostMapping("/{clientId}/{fileId}/region")
public Mono<RegionResult> readRegion(
    @PathVariable String clientId,
    @PathVariable String fileId,
    @RequestBody RegionRequest request
) {
    return Mono.fromCallable(() -> {
        RegionResult result = switch (request.regionType()) {
            case "技经表" -> stageBService.readIndicatorTable(request.images());
            case "图例" -> stageBService.readLegend(request.images());
            case "主体区" -> stageBService.readMainArea(request.images());
            default -> RegionResult.forIndicatorTable(null, "low", List.of("unknown_region_type"));
        };
        // Persist to memory
        persistRegionResult(clientId, fileId, result);
        return result;
    }).subscribeOn(Schedulers.boundedElastic());
}

private void persistRegionResult(String clientId, String fileId, RegionResult r) {
    if (r == null) return;
    if (r.indicatorTable() != null && r.indicatorTable().keyFacts() != null) {
        for (var item : r.indicatorTable().keyFacts()) {
            memoryStore.addKeyFact(clientId, fileId, item.name(),
                String.valueOf(item.value()) + (item.unit() == null ? "" : " " + item.unit()),
                item.confidence(),
                "Stage B 技经表视觉读取");
        }
    }
    if (r.legend() != null && r.legend().legendItems() != null) {
        // NOTE: legendItems are visual conventions only — not mapped to layer names.
        // Save them as a separate section, not as layerSemantics.
        memoryStore.saveLegendItems(clientId, fileId, r.legend().legendItems());
    }
    if (r.mainArea() != null) {
        memoryStore.saveMainArea(clientId, fileId, r.mainArea().mainAreaDescription());
        memoryStore.saveKeyAnnotations(clientId, fileId, r.mainArea().keyAnnotations());
        memoryStore.saveCandidateObjects(clientId, fileId, r.mainArea().candidateObjects());
    }
    if (r.stalenessReasons() != null) {
        for (String reason : r.stalenessReasons()) {
            memoryStore.markStaleness(clientId, fileId, reason);
        }
    }
}
```

(Inject `StageBService stageBService` into the controller constructor.)

- [ ] **Step 2: Compile**

`mvn compile -q`. Verify `memoryStore.addKeyFact` / `addLayerSemantic` / `markStaleness` actually exist with these signatures — adjust if different.

- [ ] **Step 3: Commit**

```bash
git add drawing-ai-server/src/main/java/com/lvjian/drawingai/controller/DrawingMemoryController.java
git commit -m "feat(memory): /region endpoint for Stage B per-region reading"
```

### Task 3.8: Frontend — VisionMemoryPipeline.runStageB

**Files:**
- Modify: `DrawingWebApp/src/services/memory/VisionMemoryPipeline.js`
- Modify: `DrawingWebApp/src/services/DrawingMemoryApi.js`

- [ ] **Step 1: Add postRegion to DrawingMemoryApi.js**

```javascript
/**
 * POST a region's images to backend Stage B.
 * @param {string} clientId
 * @param {string} fileId
 * @param {string} regionType  '技经表' | '图例' | '主体区'
 * @param {string[]} images  base64 data URLs (1 or N tiles)
 * @returns {Promise<object>}  RegionResult JSON
 */
export async function postRegion(clientId, fileId, regionType, images) {
  const url = `/api/ai/drawing-memory/${encodeURIComponent(clientId)}/${encodeURIComponent(fileId)}/region`
  const resp = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ regionType, images }),
  })
  if (!resp.ok) throw new Error(`region failed: ${resp.status} ${await resp.text()}`)
  return await resp.json()
}
```

- [ ] **Step 2: Extend [[Vision]]MemoryPipeline with runStageB**

In `VisionMemoryPipeline.js`:
```javascript
import { captureFullExtents } from '../ScreenshotService'
import { postInitV2, postRegion } from '../DrawingMemoryApi'
import { captureRegionTiles } from './captureRegionTiles'

export class VisionMemoryPipeline {
  // ... existing constructor and run() ...

  async run(clientId, fileId) {
    const metadata = this._collectMetadata()
    const screenshot = this._captureFull()
    if (!screenshot) {
      return { stageA: null, stageB: null, error: 'screenshot_failed' }
    }
    // Stage A
    let stageA
    try {
      const resp = await postInitV2(clientId, fileId, metadata, screenshot)
      stageA = resp.stageA
    } catch (e) {
      console.warn('[VisionMemoryPipeline] Stage A failed:', e.message)
      return { stageA: null, stageB: null, error: 'stage_a_failed' }
    }
    if (!stageA || !stageA.keyRegions || stageA.keyRegions.length === 0) {
      return { stageA, stageB: null, error: 'no_key_regions' }
    }
    // Stage B — per region in parallel
    const stageB = await this._runStageB(clientId, fileId, stageA.keyRegions)
    return { stageA, stageB }
  }

  async _runStageB(clientId, fileId, keyRegions) {
    const tasks = keyRegions.map(region => this._processRegion(clientId, fileId, region))
    const results = await Promise.allSettled(tasks)
    return results.map((r, i) => ({
      region: keyRegions[i].type,
      status: r.status,
      result: r.status === 'fulfilled' ? r.value : null,
      error: r.status === 'rejected' ? String(r.reason) : null,
    }))
  }

  async _processRegion(clientId, fileId, region) {
    let images = await captureRegionTiles(this.viewer, region, { quality: 0.85, format: 'image/jpeg' })
    if (images.length === 0) throw new Error('no_tiles_captured')

    let result = await postRegion(clientId, fileId, region.type, images)

    // Bounce-back retry: if backend reports extractedComplete=false, re-slice once
    const meta = this._extractMeta(result)
    if (meta && meta.extractedComplete === false && meta.suggestedReSlice) {
      console.log(`[VisionMemoryPipeline] re-slicing ${region.type} per suggestion: ${meta.suggestedReSlice}`)
      const retryRegion = { ...region, splitStrategy: meta.suggestedReSlice }
      const retryImages = await captureRegionTiles(this.viewer, retryRegion, { quality: 0.85, format: 'image/jpeg' })
      if (retryImages.length > 0) {
        result = await postRegion(clientId, fileId, region.type, retryImages)
      }
    }
    return result
  }

  _extractMeta(regionResult) {
    if (!regionResult) return null
    if (regionResult.indicatorTable && regionResult.indicatorTable._meta) return regionResult.indicatorTable._meta
    if (regionResult.legend && regionResult.legend._meta) return regionResult.legend._meta
    if (regionResult.mainArea && regionResult.mainArea._meta) return regionResult.mainArea._meta
    return null
  }

  // ... existing _collectMetadata, _readExtents, _captureFull
}
```

- [ ] **Step 3: Lint check**

`npm run lint`. Clean.

- [ ] **Step 4: Build check**

`npm run build`. Success.

- [ ] **Step 5: Manual end-to-end verification**

Start backend + frontend (as in Task 2.7 Step 6). Open a real DWG with a clear 技经表. Watch:
- Console: `[MemoryAutoInit] Stage A complete: ...` + 3 region POST requests
- Network: 1× /init + 3× /region
- Right sidebar: drawingType, mainAreaDescription, keyFacts populated

Acceptable failure: vision model returns garbage on a particular drawing, and result is partially populated with staleness markers. Goal here is "no crash + no infinite loop".

- [ ] **Step 6: Commit**

```bash
git add DrawingWebApp/src/services/DrawingMemoryApi.js DrawingWebApp/src/services/memory/VisionMemoryPipeline.js
git commit -m "feat(memory/vision): Stage B end-to-end pipeline

VisionMemoryPipeline.run() now drives full Stage A → Stage B
flow: 1× /init then N× /region per keyRegion, with one
re-slice retry on extractedComplete=false."
```

---

## Phase 4 — UI Integration

> Goal: surface the new memory fields (mainAreaDescription, keyAnnotations, candidateObjects) in the right-sidebar AI Assistant panel.

### Task 4.1: Create MainAreaSection component

**Files:**
- Create: `DrawingWebApp/src/components/AiAssistant/DrawingMemoryPanel/MainAreaSection.jsx`

- [ ] **Step 1: Implement component**

```jsx
import React from 'react'
import s from '../DrawingMemoryPanel.module.css'

/**
 * Renders mainAreaDescription + keyAnnotations from DrawingMemory.
 * Read-only.
 */
export default function MainAreaSection({ mainAreaDescription, keyAnnotations }) {
  if (!mainAreaDescription && (!keyAnnotations || keyAnnotations.length === 0)) {
    return null
  }
  return (
    <section className={s.memorySection}>
      <h4>主体区</h4>
      {mainAreaDescription && (
        <p className={s.description}>{mainAreaDescription}</p>
      )}
      {keyAnnotations && keyAnnotations.length > 0 && (
        <ul className={s.annotationList}>
          {keyAnnotations.map((a, idx) => (
            <li key={idx} data-confidence={a.confidence}>
              {a.text}
              <span className={s.confidenceTag}>{a.confidence}</span>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
```

- [ ] **Step 2: Add minimal CSS**

In `DrawingMemoryPanel.module.css`, add:
```css
.memorySection { margin-bottom: 12px; }
.memorySection h4 { font-size: 13px; margin: 6px 0; color: var(--text-secondary); }
.description { font-size: 12px; color: var(--text-primary); line-height: 1.5; }
.annotationList { list-style: none; padding: 0; margin: 4px 0; }
.annotationList li { font-size: 12px; padding: 2px 0; }
.confidenceTag {
  margin-left: 6px; padding: 0 4px;
  font-size: 10px; border-radius: 2px;
  background: var(--bg-tertiary); color: var(--text-secondary);
}
.annotationList li[data-confidence="low"] { opacity: 0.6; }
```

(If `DrawingMemoryPanel.module.css` doesn't exist, create it. If it does, append.)

- [ ] **Step 3: Commit**

```bash
git add DrawingWebApp/src/components/AiAssistant/DrawingMemoryPanel/
git commit -m "feat(ui/memory): MainAreaSection component"
```

### Task 4.2: Create CandidateObjectsList component

**Files:**
- Create: `DrawingWebApp/src/components/AiAssistant/DrawingMemoryPanel/CandidateObjectsList.jsx`

- [ ] **Step 1: Implement component**

```jsx
import React from 'react'
import { Tag } from 'antd'
import s from '../DrawingMemoryPanel.module.css'

/**
 * Renders candidateObjects identified by Stage B mainArea.
 * Shows as "potential objects, not yet extracted" status.
 */
export default function CandidateObjectsList({ candidateObjects }) {
  if (!candidateObjects || candidateObjects.length === 0) return null
  return (
    <section className={s.memorySection}>
      <h4>识别到的候选对象</h4>
      <ul className={s.candidateList}>
        {candidateObjects.map((c, idx) => (
          <li key={idx}>
            <Tag color={confidenceColor(c.confidence)}>
              {c.guess}
              {c.count > 1 ? ` ×${c.count}` : ''}
            </Tag>
          </li>
        ))}
      </ul>
      <p className={s.hint}>对象提取(Stage C)将在后续阶段或点击审查按钮时触发。</p>
    </section>
  )
}

function confidenceColor(c) {
  return c === 'high' ? 'green' : c === 'mid' ? 'gold' : 'default'
}
```

- [ ] **Step 2: Add CSS**

In `DrawingMemoryPanel.module.css`:
```css
.candidateList { list-style: none; padding: 0; margin: 4px 0; display: flex; flex-wrap: wrap; gap: 4px; }
.hint { font-size: 11px; color: var(--text-tertiary); margin-top: 6px; }
```

- [ ] **Step 3: Commit**

```bash
git add DrawingWebApp/src/components/AiAssistant/DrawingMemoryPanel/CandidateObjectsList.jsx DrawingWebApp/src/components/AiAssistant/DrawingMemoryPanel.module.css
git commit -m "feat(ui/memory): CandidateObjectsList component"
```

### Task 4.3: Wire new sections into DrawingMemoryPanel

**Files:**
- Modify: `DrawingWebApp/src/components/AiAssistant/DrawingMemoryPanel.jsx`

- [ ] **Step 1: Read DrawingMemoryPanel.jsx**

Locate where existing sections (summary, layerSemantics, keyFacts) are rendered.

- [ ] **Step 2: Import + render new sections**

Add at top:
```javascript
import MainAreaSection from './DrawingMemoryPanel/MainAreaSection'
import CandidateObjectsList from './DrawingMemoryPanel/CandidateObjectsList'
```

In the render method, add after existing sections (e.g. after `keyFacts`):
```jsx
<MainAreaSection
  mainAreaDescription={memory.mainAreaDescription}
  keyAnnotations={memory.keyAnnotations}
/>
<CandidateObjectsList candidateObjects={memory.candidateObjects} />
{memory.legendItems && memory.legendItems.length > 0 && (
  <section className={s.memorySection}>
    <h4>图例</h4>
    <ul className={s.legendList}>
      {memory.legendItems.map((item, idx) => (
        <li key={idx}>
          <span
            className={s.swatch}
            style={{ background: item.color || '#888' }}
            title={item.visualKind + (item.lineType ? ` ${item.lineType}` : '')}
          />
          <span>{item.description}</span>
        </li>
      ))}
    </ul>
  </section>
)}
```

In `DrawingMemoryPanel.module.css`, append:
```css
.legendList { list-style: none; padding: 0; margin: 4px 0; }
.legendList li { display: flex; align-items: center; gap: 6px; padding: 2px 0; font-size: 12px; }
.swatch { width: 16px; height: 4px; border-radius: 1px; flex-shrink: 0; }
```

- [ ] **Step 3: Lint + build**

`npm run lint && npm run build`. Both succeed.

- [ ] **Step 4: Manual verification**

Open a DWG with full vision pipeline. Right sidebar should show:
- Old fields (drawingType, layerSemantics, keyFacts)
- New: 主体区 description + annotations
- New: 识别到的候选对象 chips
- New: 图例 list (with color swatch + description)

- [ ] **Step 5: Commit**

```bash
git add DrawingWebApp/src/components/AiAssistant/DrawingMemoryPanel.jsx DrawingWebApp/src/components/AiAssistant/DrawingMemoryPanel.module.css
git commit -m "feat(ui/memory): render MainAreaSection, CandidateObjectsList, legend"
```

### Task 4.4: Final integration verification

- [ ] **Step 1: Full smoke test on 3 different drawings**

Open each of the following test cases (use any available DWGs that match these categories):
1. **Regulatory plan (控规图)** — expect drawingType=REGULATORY_PLAN, drawingUnit=meter, technical-table read OK
2. **Site plan (总平面图)** — expect drawingType=SITE_PLAN, mainArea + candidates populated
3. **Architectural single-building (建筑单体图)** — expect drawingType=ARCHITECTURAL_DESIGN, drawingUnit=millimeter, possibly empty technical-table (OK, staleness=region_技经表_failed)

For each, document:
- drawingType correctness (manually compare)
- keyFacts: top 3 fact accuracy vs human reading of technical-table
- staleness markers (which were set, are they reasonable)
- Total time from file-open to memory-displayed (target ≤ 30s P50)

- [ ] **Step 2: Capture results in commit message of final wrap-up commit**

If acceptance criteria are met (per spec §18), this is the milestone.

- [ ] **Step 3: Tag the milestone**

```bash
git tag plan1-stage-ab-ui-complete
git log -5 --oneline   # confirm history
```

- [ ] **Step 4: Final commit (closing milestone marker)**

```bash
git commit --allow-empty -m "milestone: vision memory init Plan 1 complete

Plan 1 = Phases 1-4 (Stage A + Stage B + UI integration).
Next: Plan 2 = Stage C (object extraction) + cleanup of
LandBoundary* legacy code.

Verified on 3 drawings (regulatory / site / architectural).
Acceptance criteria from spec §18: [list pass/fail]"
```

---

## Acceptance Criteria (from spec §18)

After Plan 1 ships, the following must hold:

1. **Functional**:
   - 3 control plans (控规图): Stage A `drawingType` 100% correct
   - 3 site plans: Stage B technical-table → keyFacts of 总用地面积/容积率/绿地率 within 5% of human-read values
   - 1 site plan with legible legend: Stage B legend → layerSemantics maps ≥ 80% of layer names correctly

2. **Performance**:
   - File open → memory available P50 ≤ 30 seconds (measured by `[MemoryAutoInit] Stage A complete` timestamp minus `[VisionMemoryPipeline] start` timestamp; add a console.time/timeEnd if needed)

3. **Degradation**:
   - With network disconnected: pipeline fails gracefully, no crash, console error visible, memory stays in pre-init state
   - With drawing missing 技经表: that region is failed, others succeed, staleness flag `region_技经表_failed` set

4. **Cleanup-1 (in this plan)**:
   - `_aggregateSiteAreas` deleted
   - `_categorizeSiteLayer` deleted
   - Stage 2 SYSTEM_PROMPT (text summarization) deleted
   - `DrawingTypeSkillProvider` marked @Deprecated

5. **NOT YET (deferred to Plan 2)**:
   - `LandBoundaryVisionTest.js` / `LandBoundaryAnalyzer.js` still present (Plan 2 deletes)
   - `RUN_LAND_BOUNDARY_TEST` const still present (Plan 2 deletes)
   - Stage C object extraction not implemented (Plan 2 builds)

---

## Notes for the Implementing Engineer

1. **[[Spring AI]] 1.1.2 `UserMessage.builder().media(Media...)` varargs**: not 100% verified by reading source. If compile fails on the varargs call, fall back to chained `.media(m1).media(m2).media(m3)` calls or look up the actual API in the version's javadoc.

2. **`viewer.zoomToWindow` vs `viewer.zoomTo`**: the captureRegionTiles helper tries both. If neither exists, the actual method may be on `Module.appCore` or some other path. Read `ViewerService.js:976+` for the real API.

3. **[[Vision]] model availability**: the backend uses [[Spring AI]] Alibaba DashScope. Verify `application.yml` / `application-dev.yml` configures `spring.ai.dashscope.chat.options.model` to a multimodal-capable model (qwen-vl-max or similar). If not, Stage A will return null with no helpful error — add explicit check in `StageAService.runStageA` to log when `chatModel.getDefaultOptions()` shows non-vision model.

4. **`@Async` removal**: the old `doStage2` was annotated `@Async`. The new `init()` flow is synchronous (frontend awaits), so `@EnableAsync` may no longer be needed for memory init. Don't remove `@EnableAsync` from the application — other features may use it. Just make the init path synchronous.

5. **Test framework note**: existing backend tests under `src/test/java/.../memory/` use JUnit 5 + Mockito + AssertJ via `spring-boot-starter-test`. New tests should follow that style — see `DrawingMemoryStoreTest` (if exists) for reference patterns.
