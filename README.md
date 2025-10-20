
# 🚀 LangGraph Prospect-to-Lead Workflow

## 🧩 Overview
An **end-to-end LangGraph system** that discovers, enriches, scores, and contacts **B2B prospects**, continuously improving through a **feedback loop**.

---

## ⚙️ Setup

### 🐍 Requirements
- **Python:** 3.10+  
- **Install dependencies:**  
  ```bash
  pip install -r requirements.txt
  ```

### 🌱 Environment Setup
1. Copy `.env.example` → `.env`  
2. Fill in required keys.  
3. To run in mock mode (no external API calls):  
   ```bash
   MOCK_MODE=true
   ```
4. For **Google Sheets integration**, place your service account JSON at the path specified in:  
   ```bash
   GOOGLE_SHEETS_SERVICE_ACCOUNT_JSON
   ```

---

## ▶️ Run the Workflow

```bash
python langgraph_builder.py --workflow workflow.json --persist ./state
```

---

## 📁 Project Structure

| File/Folder | Description |
|--------------|-------------|
| **workflow.json** | Single source of truth for workflow steps and configuration. |
| **langgraph_builder.py** | Reads, validates, builds, and executes LangGraph. |
| **agents/** | Modular sub-agents with structured input/output and logging. |

---

## 🔧 Extend or Modify

### ➕ Add a New Step
Add a new entry in **workflow.json** with:  
- `id`
- `agent`
- `inputs`
- `instructions`
- `tools`
- `output_schema`

### ⚙️ Add a New Agent
1. Implement a new class in `agents/`, deriving from `BaseAgent`.  
2. Register it in the `AGENT_REGISTRY` inside `agents/__init__.py`.

---

## 🧠 Notes
- **Mock Mode** → Returns deterministic demo data, skipping all external calls.  
- **Real Mode** → Requires valid API keys; may incur API costs.  

---

## 🌐 About
LangGraph is designed to **streamline prospect discovery and engagement** using AI-driven workflows.  
Built for **automation, scalability, and continuous learning**.

---

## 📘 Resources
- 🧾 [Readme](README.md)
- 🧩 [Workflow File](workflow.json)
- 🧠 [Agents Module](agents/)

---

## 🧑‍💻 Author
**Bala Sai M**  



---

## 📊 Languages
| Language | Usage |
|-----------|--------|
| 🐍 Python | 100% |

