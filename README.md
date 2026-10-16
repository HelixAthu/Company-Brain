# 🧠 DevTrace: Enterprise Company Brain

[![Track](https://img.shields.io/badge/Graph_Hacks_2026-Track_03:_Company_Brain-purple.svg)](https://wemakedevs.org)
[![Database](https://img.shields.io/badge/Powered_by-FalkorDB-crimson.svg)](https://falkordb.com)
[![Backend](https://img.shields.io/badge/Backend-FastAPI_Python-blue.svg)](https://fastapi.tiangolo.com)
[![Frontend](https://img.shields.io/badge/Frontend-React_+_Vite-cyan.svg)](https://vitejs.dev)
[![AI](https://img.shields.io/badge/AI_Engine-Google_Gemini-orange.svg)](https://deepmind.google/technologies/gemini)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **DevTrace** is an enterprise-grade Knowledge Graph Intelligence Platform submitted to **Graph Hacks** by **WeMakeDevs** (Powered by **FalkorDB**).
> It turns dispersed organizational knowledge—teams, code repositories, microservices, architecture decision records (ADRs), runbooks, and incidents—into an ultra-fast queryable graph powered by FalkorDB and Google Gemini Text-to-Cypher reasoning.

---

## 📌 Submission Overview
- **Event:** WeMakeDevs Graph Hacks Hackathon
- **Track:** Track 03 — Company Brain
- **Engine:** FalkorDB Graph Database + Gemini Flash 2.5 AI
- **Repository:** HelixAthu/Company-Brain

---

## 🏗️ Architecture Overview

DevTrace eliminates tribal knowledge silos by structuring enterprise entities into an interconnected graph:

```
[ User Question ]
       │
       ▼
[ FastAPI Backend ] ──► [ Google Gemini AI ]
       │                         │
       │ (Generates Cypher)      │
       ▼                         │
[ FalkorDB Graph Engine ] ◄──────┘
       │
       ▼ (Sub-millisecond Graph Traversal)
[ Provenance & Path Synthesis ]
       │
       ▼
[ Interactive React UI + Graph Explorer ]
```

---

## ⚡ Tech Stack

| Component | Technology | Description |
|-----------|------------|-------------|
| **Graph Database** | FalkorDB (Redis Graph Engine) | Graph database engineered for millisecond latency Cypher queries |
| **Backend API** | FastAPI (Python 3.10+) | High-performance asynchronous REST endpoints |
| **LLM & Reasoning** | Google Gemini GenAI SDK | Text-to-Cypher translation with self-correcting validation |
| **Frontend Client** | React 18 + Vite | Modern reactive dashboard with dynamic graph inspector |
| **Styling** | TailwindCSS + Lucide Icons | Responsive enterprise dark/light developer UI |

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Docker & Docker Compose (for FalkorDB)
- Python 3.10+
- Node.js 18+

### 2. Launch FalkorDB
```bash
docker run -p 6379:6379 -it --rm falkordb/falkordb:latest
```

### 3. Backend Setup
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
python seed.py
uvicorn main:app --reload --port 8000
```

### 4. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 🎥 Demo Video & Visuals
- **Demo Video:** *Coming Soon (Submitted for Hackathon Evaluation)*
- **Live Demo:** `http://localhost:5173`

---

## 📄 License
This project is licensed under the MIT License.
