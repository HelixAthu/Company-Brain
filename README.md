# 🧠 DevTrace: Enterprise Company Brain

[![Track](https://img.shields.io/badge/Graph_Hacks_2026-Track_03:_Company_Brain-8A2BE2.svg?style=for-the-badge)](https://wemakedevs.org)
[![Database](https://img.shields.io/badge/Graph_Database-FalkorDB_v1.0-FF0040.svg?style=for-the-badge)](https://falkordb.com)
[![AI Engine](https://img.shields.io/badge/AI_Agent-Google_Gemini_Flash-FFA500.svg?style=for-the-badge)](https://deepmind.google/technologies/gemini)
[![Backend](https://img.shields.io/badge/Backend-FastAPI_Python-009688.svg?style=for-the-badge)](https://fastapi.tiangolo.com)
[![Frontend](https://img.shields.io/badge/Frontend-React_18_+_Vite-00BFFF.svg?style=for-the-badge)](https://vitejs.dev)
[![License](https://img.shields.io/badge/License-MIT-32CD32.svg?style=for-the-badge)](LICENSE)

> **DevTrace** is an enterprise-grade Knowledge Graph Intelligence Platform submitted to **Graph Hacks** by **WeMakeDevs** (Powered by **FalkorDB**).
> It turns dispersed organizational knowledge—teams, code repositories, microservices, architecture decision records (ADRs), runbooks, and incidents—into an ultra-fast queryable graph powered by FalkorDB and Google Gemini Text-to-Cypher reasoning.

---

## 📌 Submission Overview
- **Event:** WeMakeDevs Graph Hacks Hackathon 2026
- **Track:** Track 03 — Company Brain
- **Core Database:** **FalkorDB** (Low-Latency Graph Database)
- **AI / LLM:** Google Gemini Flash 2.5 (`google-genai` SDK) with Self-Correcting Cypher Loop
- **Repository:** `HelixAthu/Company-Brain`

---

## ⚡ The Problem: Organizational Blindness

Modern engineering organizations suffer from severe knowledge fragmentation:
1. **Tribal Knowledge & Silos:** Who actually owns the Payment Gateway? Who is on-call tonight?
2. **Blast Radius Blindness:** If the Billing DB fails, which customer-facing microservices crash?
3. **Lost Architectural Decisions:** Why was the legacy cache migrated? Who signed off on the change and where is the ADR?

Traditional search and vector RAG fail here because **relational topology and multi-hop dependency chains cannot be computed with simple vector similarity**.

---

## 💡 The Solution: DevTrace

DevTrace indexes the entire enterprise topology inside **FalkorDB**. When an engineer asks a question:
1. **Google Gemini Flash** converts natural language into strict, read-only Cypher queries.
2. **Self-Correction Engine** detects any schema or syntax errors and retries automatically.
3. **FalkorDB Engine** executes the query in **sub-millisecond latency** using sparse matrix linear algebra.
4. **Synthesis Engine** compiles a human-readable answer citing author engineers, teams, runbooks, and ADRs.
5. **Live Cypher Transparency Drawer** shows the exact executed Cypher query and traversed entities in real time.

---

## 🏗️ Architecture & Pipeline Flow

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Developer / SRE
    participant UI as DevTrace React Console
    participant API as FastAPI Backend
    participant Gemini as Google Gemini AI
    participant Falkor as FalkorDB Graph Engine

    Dev->>UI: "Who owns the Payment Gateway?"
    UI->>API: POST /api/ask { prompt }
    API->>Gemini: Text-to-Cypher with Graph Schema
    Gemini-->>API: MATCH (s:System)<-[:OWNS]-(t:Team)...
    API->>Falkor: Execute Cypher Query
    alt Syntax Error
        Falkor-->>API: Cypher Syntax Exception
        API->>Gemini: Self-Correction Loop with DB Error
        Gemini-->>API: Corrected Cypher Query
        API->>Falkor: Execute Corrected Cypher
    end
    Falkor-->>API: Traversed Nodes & Relationships (Sub-millisecond)
    API->>Gemini: Synthesize Answer with Provenance & Citations
    Gemini-->>API: Synthesized Response + Citations
    API-->>UI: Answer, Cypher Query, Traversed Nodes, Citations
    UI-->>Dev: Render Answer & Update Live Graph Inspector
```

---

## 🧩 FalkorDB Knowledge Graph Schema

DevTrace models enterprise entities into a rich semantic graph:

```mermaid
graph TD
    Person["Person<br/>(name, role, email, slack)"] -->|MEMBER_OF| Team["Team<br/>(name, domain, slack_channel)"]
    Team -->|OWNS| System["System / Service<br/>(name, tier, repo_url, status)"]
    Person -->|AUTHORED| Document["Document / Runbook<br/>(title, type, url)"]
    Person -->|RECORDED| Decision["Decision / ADR<br/>(title, status, rationale, date)"]
    Document -->|DOCUMENTS| System
    Decision -->|DOCUMENTS| System
    System -->|DEPENDS_ON| System
```

### Core Entity Types:
- **`Person`**: Software engineers, architects, and SRE on-call leads.
- **`Team`**: Functional squads (Payments Team, Core Infra, Identity Team).
- **`System`**: Microservices and databases (Payment Gateway, Billing DB, Auth Microservice, FalkorDB Graph Engine).
- **`Document`**: Incident runbooks, disaster recovery procedures, architecture specs.
- **`Decision`**: Architectural Decision Records (ADRs) with rationale and date provenance.

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- **Docker** (to run FalkorDB)
- **Python 3.10+** (Python 3.11 recommended)
- **Node.js 18+**

### 2. One-Command Docker Compose (Recommended)
```bash
docker compose up -d
```
This automatically launches:
- FalkorDB on port `6379`
- DevTrace FastAPI Backend on port `8000`

### 3. Manual Local Setup

#### Step A: Launch FalkorDB
```bash
docker run -p 6379:6379 -it --rm falkordb/falkordb:latest
```

#### Step B: Backend Setup
```bash
cd backend
python -m venv venv

# Activate venv:
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env

# Seed the knowledge graph
python seed.py

# Launch FastAPI server
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

#### Step C: Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 🧪 Automated Testing Suite

DevTrace includes comprehensive automated tests for endpoints and graph traversals:
```bash
pytest backend/tests/test_api.py -v
```

---

## 🌟 Key Features

| Feature | Description |
|---|---|
| **Sub-Millisecond Graph Traversal** | Powered by FalkorDB's linear algebra engine running RedisGraph protocol. |
| **Self-Correcting Text-to-Cypher** | Translates natural language into Cypher and corrects syntax errors on the fly. |
| **Live Cypher Transparency Drawer** | Inspect executed queries, syntax coloring, and traversed node graphs in real time. |
| **Blast Radius Dependency Tracing** | Determine immediate and transitive downstream service outages. |
| **Architectural Provenance (ADRs)** | Trace *why* technical decisions were made with author and runbook attribution. |
| **Bulletproof Offline Demo Mode** | Zero-failure presentation mode with instant high-fidelity answers. |

---

## 📄 License
This project is licensed under the MIT License. Submitted for **Graph Hacks Track 03 (Company Brain)**.
