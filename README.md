# 🧠 AI Orchestrator – ERP Natural Language Engine

Enterprise-grade AI layer for converting natural language into secure, structured ERP operations.

---

## 🚀 Overview

The AI Orchestrator is a standalone FastAPI microservice that enables users to interact with the ERP system using natural language.

### Example Queries

- “Show tasks below 30% completion”
- “Which projects are delayed more than 5 days?”
- “Create a high priority task for Rahul”
- “Give me engineers on leave today”

Instead of directly querying the database, the system:

1. Extracts intent and filters using an LLM
2. Validates the extracted structure
3. Applies permission rules (RBAC)
4. Builds safe database queries
5. Executes ERP backend APIs
6. Formats a human-readable response

---

# 🏗️ System Architecture

```
User → AI Orchestrator → ERP Backend → Database
```

The AI layer:

- ❌ Never accesses MongoDB directly
- ❌ Never executes raw LLM-generated queries
- ✅ Always validates and controls execution

---

# 📁 Project Structure

```
ai-orchestrator/
│
├── app/
│   ├── main.py
│   ├── config/
│   ├── core/
│   ├── agents/
│   ├── graph/
│   ├── schemas/
│   ├── services/
│   ├── memory/
│   ├── routes/
│   └── utils/
│
├── tests/
├── requirements.txt
├── Dockerfile
└── README.md
```

---

# 📦 Folder Breakdown

## 🔹 app/main.py
Application entry point.

- Initializes FastAPI
- Registers routes
- Connects LangGraph workflow
- Applies middleware

---

## 🔹 config/

- `settings.py` – Environment variables
- `llm_config.py` – LLM setup (model, temperature, tokens)

---

## 🔹 core/

- `security.py` – Authentication validation
- `logging.py` – Structured logging
- `dependencies.py` – FastAPI dependency injection

---

## 🔹 agents/

Handles all LLM-related logic.

- `erp_agent.py` – Wrapper around LLM
- `prompt_templates.py` – Strict JSON prompts
- `output_parsers.py` – Structured response validation

---

## 🔹 graph/

LangGraph deterministic workflow.

### Execution Flow

```
START
 ↓
INTENT EXTRACTION
 ↓
VALIDATION
 ↓
PERMISSION CHECK
 ↓
QUERY BUILDER
 ↓
ACTION EXECUTION
 ↓
RESPONSE FORMATTER
```

Each node is isolated and testable.

---

## 🔹 schemas/

Pydantic validation models:

- `intent_schema.py`
- `filter_schema.py`
- `action_schema.py`

Ensures strict structure enforcement.

---

## 🔹 services/

Business logic layer.

- `erp_api_client.py` – Calls ERP backend
- `permission_service.py` – Role-based filtering
- `query_builder.py` – Safe Mongo query generation
- `metadata_registry.py` – Allowed fields & types

---

## 🔹 memory/

Conversation context storage.

- `redis_memory.py`
- `session_memory.py`

Enables follow-up queries:

> “Now show only high priority ones”

---

## 🔹 routes/

Main endpoint:

```
POST /ai/chat
```

### Request

```json
{
  "message": "Show tasks below 30%"
}
```

### Response

```json
{
  "reply": "You have 4 tasks below 30% completion."
}
```

---

## 🔹 utils/

Helper utilities:

- `operator_mapper.py`
- `date_parser.py`
- `constants.py`

---

# 🔐 Security Principles

✔ No raw Mongo queries from LLM  
✔ Field-level validation  
✔ Intent registry enforcement  
✔ RBAC enforcement before execution  
✔ Safe operator mapping  

---

# 🧩 Supported Intents (Example)

- GET_TASKS
- CREATE_TASK
- UPDATE_TASK
- GET_PROJECTS
- GET_ENGINEERS
- GET_STATS

---

# 🧠 Example Query Flow

### User Input

> “Show high priority tasks under 30% completion”

### LLM Structured Output

```json
{
  "intent": "GET_TASKS",
  "filters": {
    "priority": { "operator": "eq", "value": "high" },
    "completionPercentage": { "operator": "lt", "value": 30 }
  }
}
```

### System Execution

1. Validate filters
2. Apply user permissions
3. Map operators safely
4. Build Mongo query
5. Call ERP backend
6. Format result

---

# 🛠️ Installation

## 1️⃣ Clone repository

```bash
git clone <repo-url>
cd ai-orchestrator
```

## 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

## 3️⃣ Run locally

```bash
uvicorn app.main:app --reload
```

Server runs at:

```
http://localhost:8000
```

---

# 🐳 Docker Setup

## Build image

```bash
docker build -t ai-orchestrator .
```

## Run container

```bash
docker run -p 8000:8000 ai-orchestrator
```

---

# 🧪 Testing

Run tests:

```bash
pytest
```

Test coverage includes:

- Intent extraction
- Query builder safety
- Graph flow validation

---

# 🎯 Design Principles

- LLM interprets language
- Backend validates structure
- Services execute logic
- Database remains protected

---

# 📈 Future Improvements

- Hybrid vector + structured search
- Multi-tenant isolation
- Audit logging for AI decisions
- Observability dashboard
- Automatic ERP schema sync

---

# 🏁 Final Philosophy

Natural language should enhance ERP productivity — not compromise system integrity.
