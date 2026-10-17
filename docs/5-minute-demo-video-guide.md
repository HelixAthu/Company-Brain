# 🎬 DevTrace: 5-Minute Explainer & Demo Video Master Guide

**Event:** WeMakeDevs Graph Hacks 2026  
**Track:** Track 03 — Company Brain  
**Database:** FalkorDB  
**AI Agent:** Google Gemini Flash 2.5  
**Target Duration:** 5 Minutes (~650-750 words, comfortably paced)  

---

## 🧠 Part 1: Under the Hood Architecture & Technical Cheat Sheet

Use these points to explain the technical depths or answer judges' questions:

### 1. Why FalkorDB instead of Standard Vector RAG?
- **The Vector Limitation:** Vector search calculates cosine similarity between text chunks. For a query like *"What services break if the Billing DB fails?"*, semantic search only finds documents mentioning "Billing DB" and "failures". It **cannot compute multi-hop topological dependency chains**.
- **The FalkorDB Advantage:** FalkorDB models graphs as **sparse adjacency matrices** based on the GraphBLAS standard. Traversing relationships is represented as linear algebra matrix multiplications, completing deep multi-hop traversals in **sub-4 milliseconds**.

### 2. The 3-Stage AI Agent Pipeline
1. **Schema-Aware Text-to-Cypher:** Google Gemini Flash receives the question with the exact FalkorDB schema (`Person`, `Team`, `System`, `Document`, `Decision`). It generates valid, read-only Cypher queries.
2. **Automated Self-Correction Loop:** If FalkorDB raises a syntax or schema exception, the backend intercepts it and sends the database error + failed Cypher back to Gemini to auto-heal the query before re-executing.
3. **Graph Execution & Answer Synthesis:** FalkorDB executes the query. The raw result set is synthesized into an executive answer citing verified runbooks, Slack channels, and on-call engineers.

### 3. Radical Transparency Drawer
- Eliminates AI hallucinations: Every answer in the chat is paired with the exact executed Cypher query, execution latency, and clickable traversed graph entity badges in the right-side Graph Inspector.

---

## 🎥 Part 2: 5-Minute Video Recording Timeline & Script

### Pre-Flight Checklist Before Recording:
- [ ] FalkorDB container running: `docker ps` shows `devtrace-falkordb` on `0.0.0.0:6379`.
- [ ] Backend running: `http://localhost:8000/health` returns `"status": "healthy"`.
- [ ] Frontend running: `http://localhost:5173` open in browser.
- [ ] Browser zoom set to **110%** for clear text readability.
- [ ] Second tab open to Swagger docs: `http://localhost:8000/docs`.

---

### [0:00 – 0:45] Act 1: The Problem & The Vision

| Timestamp | Visual Action (What to show & where to click) | Spoken Script (Word-for-Word Voiceover) |
| :--- | :--- | :--- |
| **0:00 – 0:20** | Start on the DevTrace home page (`http://localhost:5173`).<br/>Move mouse over the title: *"Ask your company brain."*<br/>Point cursor at the green **"FalkorDB Connected"** badge in the top navbar. | *"Every engineering team has faced this at 2 AM: production is down, an unfamiliar service is throwing errors, and nobody knows who owns it, what on-call rotation to page, or what other systems will break if a database fails.  Organizational knowledge is fragmented across stale wikis, Slack channels, and tribal memory."* |
| **0:20 – 0:45** | Smoothly hover over the suggestion chips across the top of the chat panel. | *"Traditional vector search and AI chatbots fail here because company topology isn't a paragraph of text—it's a living, interconnected graph.  This is **DevTrace**, our submission for Track 03: Company Brain in the WeMakeDevs Graph Hacks Hackathon. DevTrace connects your teams, microservices, runbooks, and architectural decisions into an ultra-fast queryable graph powered by **FalkorDB** and **Google Gemini**."* |

---

### [0:45 – 1:30] Act 2: Architecture & Under the Hood

| Timestamp | Visual Action (What to show & where to click) | Spoken Script (Word-for-Word Voiceover) |
| :--- | :--- | :--- |
| **0:45 – 1:10** | Briefly switch tab to **`http://localhost:8000/docs`** to show the FastAPI endpoints (`GET /health`, `POST /api/ask`), then switch back to `http://localhost:5173`.<br/>Expand the right-side **Graph Inspector drawer**. | *"Let's talk about what's happening under the hood. Behind this interface runs an event-driven FastAPI backend connected directly to **FalkorDB** on port 6379.  We model the enterprise into five core node labels: `Person`, `Team`, `System`, `Document`, and `Decision`—linked by semantic relationships like `OWNS`, `DEPENDS_ON`, `MEMBER_OF`, and `AUTHORED`."* |
| **1:10 – 1:30** | Hover over the Graph Inspector where the Cypher query and visited entities are displayed. | *"When a developer asks a question in plain English, our AI agent doesn't guess. It translates the question into strict, read-only Cypher queries. FalkorDB executes the multi-hop traversal in under 5 milliseconds using GraphBLAS linear algebra, and our synthesis engine compiles an authoritative answer backed by exact citations."* |

---

### [1:30 – 2:30] Act 3: Demo 1 — Service Ownership & On-Call Routing

| Timestamp | Visual Action (What to show & where to click) | Spoken Script (Word-for-Word Voiceover) |
| :--- | :--- | :--- |
| **1:30 – 1:45** | Click the first suggestion chip:<br/>**`"Who owns the Payment Gateway?"`**<br/>Wait 1 second as the response renders into the chat. | *"Let's see it in action. Suppose an incident strikes and we need immediate ownership. I'll click our first query: **'Who owns the Payment Gateway?'**  Instantly, DevTrace returns the exact squad: The Payments Team, with their direct `#team-payments` Slack channel, Staff Architect Elena Rostova, and on-call engineer Bob Smith."* |
| **1:45 – 2:10** | Hover cursor over the **`3.4ms · FalkorDB`** execution latency pill in the message header.<br/>Click/hover the **`Payment Gateway Incident Runbook`** citation badge. | *"Notice two critical details: First, look at the latency badge—resolved in just **3.4 milliseconds** directly from FalkorDB. Second, it attached the exact incident runbook citation directly from the graph via an `AUTHORED` and `DOCUMENTS` edge. No hallucinated links—only verified internal wiki URLs."* |
| **2:10 – 2:30** | Direct attention to the right-hand **Graph Inspector**.<br/>Scroll through the generated Cypher query and the 4 traversed entity pills (`Payment Gateway`, `Payments Team`, `Elena Rostova`, `Bob Smith`). | *"Look at the Graph Inspector drawer on the right. We provide complete query transparency. You can see the exact Cypher query executed: `MATCH (s:System {name: 'Payment Gateway'})<-[:OWNS]-(t:Team)...`. We can even click 'Copy' to paste this directly into a Cypher CLI or dashboard."* |

---

### [2:30 – 3:30] Act 4: Demo 2 — Dependency Blast Radius Analysis

| Timestamp | Visual Action (What to show & where to click) | Spoken Script (Word-for-Word Voiceover) |
| :--- | :--- | :--- |
| **2:30 – 2:50** | Click the second suggestion chip:<br/>**`"What services break if the Billing DB fails?"`**<br/>Watch the response render. | *"Now let's test a complex topological problem that standard search engines cannot solve: **'What services break if the Billing DB fails?'**  Here, DevTrace performs a recursive graph traversal across `DEPENDS_ON` edges."* |
| **2:50 – 3:15** | Point to the structured bullet points in the chat bubble showing `Payment Gateway` (Critical), `Auth Microservice` (Degraded), and `Notification Service` (Delayed). | *"Look at the blast radius breakdown: It identifies that the Payment Gateway suffers a critical failure because of its direct TCP link; the Auth Microservice falls into a degraded state; and downstream email notifications stall.  It also immediately surfaces the **Billing DB Failover Runbook**."* |
| **3:15 – 3:30** | Look at the Graph Inspector under **"Relationship Path"**.<br/>Highlight the breadcrumb: **`System → System → Document`**. | *"In the Inspector drawer, look at the relationship path: `System → System → Document`. FalkorDB traversed upstream and downstream dependencies simultaneously in 4.8 milliseconds. For SREs evaluating a maintenance window or diagnosing an outage, this replaces 30 minutes of cross-team Slack panic with a 4-millisecond query."* |

---

### [3:30 – 4:15] Act 5: Demo 3 — Architecture Decision Records (ADRs)

| Timestamp | Visual Action (What to show & where to click) | Spoken Script (Word-for-Word Voiceover) |
| :--- | :--- | :--- |
| **3:30 – 3:55** | Click the third suggestion chip:<br/>**`"Why was the legacy cache migrated?"`**<br/>Wait for the ADR-012 answer. | *"Next is a problem every tech lead deals with: forgotten architectural context. Why do we have this technology? Why was the old system replaced?  Let's ask: **'Why was the legacy cache migrated?'**  DevTrace navigates to **ADR-012**, recorded by Staff Engineer Alice Johnson on February 1st, 2026."* |
| **3:55 – 4:15** | Point out the details in the chat bubble: Status *Accepted*, legacy Redis vs. FalkorDB comparison, and latency drop from 120ms to 4.2ms. | *"It explains the exact rationale: legacy key-value Redis caching couldn't handle multi-hop joins without expensive application-level queries. By migrating to FalkorDB, dependency traversal latency plummeted from 120 milliseconds down to 4 milliseconds. The entire institutional memory of the engineering organization is preserved and queryable."* |

---

### [4:15 – 5:00] Act 6: Resilience, Self-Correction & Conclusion

| Timestamp | Visual Action (What to show & where to click) | Spoken Script (Word-for-Word Voiceover) |
| :--- | :--- | :--- |
| **4:15 – 4:35** | Click the **`Live Graph Mode / Demo Mode`** pill in the top header.<br/>Show it toggling to **"Demo Mode Active"** (amber pill), and then toggle it back to **"Live Graph Mode"**. | *"To guarantee production reliability, DevTrace features a dual-resilience layer: First, an automated **self-correction feedback loop** that re-prompts Gemini if a syntax error occurs. Second, a **Demo Mode toggle** in the header that can instantly switch to pre-computed graph traces if internet connectivity or third-party API quotas drop."* |
| **4:35 – 5:00** | Click **"+ New trace"** in the top right of the chat panel to show the clean state reset.<br/>Move cursor back to the brand mark: **DevTrace · Company Brain**. | *"To wrap up: DevTrace eliminates tribal knowledge silos by turning people, code, microservices, and decisions into a live graph powered by **FalkorDB**'s sub-millisecond query engine and **Google Gemini**'s reasoning.  Thank you for watching, and welcome to the future of organizational intelligence!"* |

---

## 🎯 Tips for Delivering an A+ Presentation
1. **Steady Cursor:** Keep mouse movements smooth. When mentioning a badge or query, hover deliberately over it so the judge's eyes track naturally.
2. **Confidence on FalkorDB:** Emphasize that FalkorDB delivers **sub-millisecond latency** and that queries are **pure Cypher graph traversals**, not black-box LLM hallucinations.
3. **Audio Quality:** Use a clean microphone without echo or background noise.
