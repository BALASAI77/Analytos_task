# LangGraph Prospect-to-Lead Workflow

## Overview
End-to-end LangGraph system that discovers, enriches, scores, and contacts B2B prospects and learns via a feedback loop.

## Setup
- **Python**: 3.10+
- **Install deps**:
```bash
pip install -r requirements.txt
```
- **Environment**:
  - Copy `.env.example` to `.env` and fill keys. Set `MOCK_MODE=true` to run without external APIs.
  - For Google Sheets, place your service account JSON at the path in `GOOGLE_SHEETS_SERVICE_ACCOUNT_JSON`.

## Run
```bash
python langgraph_builder.py --workflow workflow.json --persist ./state
```

## Files
- `workflow.json` single source of truth.
- `langgraph_builder.py` reads, validates, builds, and executes LangGraph.
- `agents/` modular sub-agents with structured I/O and logging.

## Extend/Modify
- Add a new step in `workflow.json` with `id`, `agent`, `inputs`, `instructions`, `tools`, `output_schema`.
- Implement a new agent class in `agents/` deriving from `BaseAgent` and register it in `AGENT_REGISTRY` in `agents/__init__.py`.

## Notes
- Mock mode returns deterministic demo data and skips external calls.
- Real mode requires valid API keys and may incur API costs.
