# ⚙️ DevTrace: Backend Engine (FastAPI & FalkorDB)

The **DevTrace Backend** serves as the intelligence and graph retrieval core for the Company Brain. It translates developer questions into executable FalkorDB Cypher queries using Google Gemini, performs sub-millisecond graph traversals, and synthesizes answers with provenance links and citations.

---

## 🛠️ Architecture Stack
- **API Framework:** [FastAPI](https://fastapi.tiangolo.com) (Python 3.10+)
- **Graph Database:** [FalkorDB](https://falkordb.com) (Redis-compatible Cypher Graph Engine)
- **AI / LLM:** Google Gemini Flash 2.5 (`google-genai` SDK)
- **Validation:** Pydantic v2
- **Testing:** Pytest & HTTPX TestClient

---

## 📋 Prerequisites
1. **Docker** installed and running (for FalkorDB)
2. **Python 3.10+** (Python 3.11 or 3.12 recommended)
3. Google Gemini API key (optional for offline demo mode)

---

## 🚀 Step-by-Step Setup

### 1. Launch FalkorDB via Docker
Ensure the FalkorDB graph engine is running on standard port `6379`:
```bash
# Windows / Linux / macOS
docker run -p 6379:6379 -it --rm falkordb/falkordb:latest
```
*Or execute the convenience script on Windows:*
```cmd
start_falkordb.bat
```

### 2. Configure Virtual Environment & Dependencies
```bash
# Navigate to the backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (cmd/PowerShell):
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

### 3. Setup Environment Variables
Copy `.env.example` to create your local `.env`:
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```ini
# Google Gemini API Key (leave default for mock/demo mode)
GEMINI_API_KEY=your_gemini_api_key_here

# FalkorDB Connection
FALKORDB_HOST=localhost
FALKORDB_PORT=6379
FALKORDB_GRAPH=company_brain

# Server Config
PORT=8000
HOST=0.0.0.0
DEMO_MODE=false
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

> **Note:** If `GEMINI_API_KEY` is not set or set to `your_gemini_api_key_here`, DevTrace seamlessly falls back to high-fidelity mock graph answers for core demo questions, ensuring zero demo failures.

### 4. Seed Knowledge Graph
Run the seed script to populate engineering teams, personnel, microservices, dependencies, runbooks, and ADRs:
```bash
python seed.py
```

Expected output:
```text
[INFO] Starting FalkorDB Company Brain seeding pipeline...
[INFO] Clearing existing nodes and relationships from graph...
[INFO] Seeding engineering teams and personnel...
[INFO] Seeding microservices systems and dependency tree...
[INFO] Seeding documentation and architectural decisions...
[INFO] Validating graph seeding counts and schema integrity...
[INFO] Seeding Validation: 15 nodes, 17 relationships created.
```

### 5. Launch FastAPI Application
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
*Or use the convenience startup script:*
```cmd
run.bat
```

The interactive OpenAPI docs will be accessible at:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## 📡 API Reference

### 1. Health Status
- **`GET /health`**
- Returns backend operational state and FalkorDB connection status:
```json
{
  "status": "healthy",
  "service": "DevTrace Company Brain API",
  "version": "1.0.0",
  "falkordb_connected": true,
  "demo_mode": false
}
```

### 2. Natural Language Graph Query
- **`POST /api/ask`**
- **Request Body:**
```json
{
  "prompt": "Who owns the Payment Gateway?",
  "demo_mode": false
}
```
- **Response Structure:**
```json
{
  "answer": "The Payments Team owns the Payment Gateway API...",
  "cypher_query": "MATCH (s:System {name: 'Payment Gateway'})<-[:OWNS]-(t:Team)...",
  "traversed_nodes": [
    {"id": "payment_gateway", "name": "Payment Gateway", "type": "System"},
    {"id": "payments_team", "name": "Payments Team", "type": "Team"}
  ],
  "citations": [
    {"title": "Payment Gateway Incident Runbook", "url": "https://wiki.company.internal/runbooks/payment-gateway", "type": "Runbook"}
  ],
  "execution_time_ms": 4.2
}
```

---

## 🧪 Running Unit Tests
Execute the pytest suite:
```bash
pytest tests/test_api.py -v
```
All endpoints and fallback trace handlers are validated.
