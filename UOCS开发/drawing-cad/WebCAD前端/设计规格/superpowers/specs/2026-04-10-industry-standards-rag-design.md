# Industry Standards RAG Knowledge Base Design

## Overview

Extend the existing RAG system (`server/rag/`) to support a third knowledge source: **industry standard PDF documents** (e.g., city planning regulations). The AI assistant will use this to verify DWG drawing parameters against regulatory requirements.

## Requirements

| Item | Decision |
|---|---|
| PDF content | Mixed: text clauses + tables with critical numeric values |
| Search mode | Independent search via new `/search_standards` endpoint |
| Data scale | Small (<20 PDFs, <100MB total) |
| Core use case | Compare standard table values against DWG parameters for compliance |
| Table accuracy | Critical — merged cells, numeric thresholds must be precisely extracted |

## Architecture

### PDF Parsing (pdfplumber)

- Use `pdfplumber` for page-by-page extraction
- Detect tables via `page.find_tables()` / `page.extract_tables()`
- Convert tables to Markdown format with merged cell fill-down
- Extract non-table text as plain paragraphs
- Auto-detect article numbers (`第 X.X.X 条`) and section headers

### Metadata per chunk

```python
{
    "source": "filename.pdf",
    "source_type": "industry_standard",
    "page_number": int,
    "section": "第一节 城市道路",
    "article": "第 2.1.5 条",
    "has_table": bool,
}
```

### Chunking Strategy

Article-based chunking (NOT fixed-size):
- Single text article → one chunk
- Article + table → one chunk (table never split)
- Long article (>1500 chars) → split at paragraph boundaries, preserve article prefix

### ChromaDB

- New collection: `industry_standards`
- Same `chroma_db` directory, same embedding model (`BAAI/bge-small-zh-v1.5`)
- Coexists with `autocad_help` and `cad_code_examples`

### API

New endpoint `POST /search_standards`:
- Request: `{ "query": str, "top_k": int }`
- Response: `{ "results": [...], "query": str, "total": int }`
- Each result includes: text, source, section, article, page_number, has_table, score

Update `/health` and `/stats` to include `industry_standards` count.

### CLI

Extend `build_index.py` with `--standards-source` argument:
```bash
python build_index.py --standards-source ./industry_standards
```

## File Changes

| File | Change |
|---|---|
| `build_index.py` | Add PDF parsing functions + `build_standards_index()` + `--standards-source` CLI arg |
| `rag_server.py` | Add `industry_standards` collection singleton + `/search_standards` endpoint + update health/stats |
| `requirements.txt` | Add `pdfplumber` |
| `.env` | Add `STANDARDS_DIR=./industry_standards` (optional) |

No new files created — extends existing architecture.
