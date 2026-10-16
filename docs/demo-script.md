# 🎬 DevTrace: 2-Minute Hackathon Demo Video Script

**Track:** Track 03 — Company Brain (Graph Hacks 2026 by WeMakeDevs & FalkorDB)  
**Target Duration:** 2 minutes (120 seconds)  
**URL:** [http://localhost:5173](http://localhost:5173)

---

## ⏱️ Video Timeline & Scene Breakdown

### Scene 1: The Hook & The Problem (0:00 - 0:25)
- **Visual:** Split screen showing fragmented Slack messages, unorganized Confluence pages, and terminal panic. Then transition into the glowing **DevTrace Console**.
- **Voiceover:**
  > *"When an incident strikes at 2 AM or a new engineer joins the team, organizational knowledge is scattered across Slack threads, outdated wikis, and tribal memory. Who owns this service? What breaks if this database fails? Why was this architecture chosen?  
  > Welcome to **DevTrace: The Enterprise Company Brain**, powered by **FalkorDB** and **Google Gemini**."*

---

### Scene 2: Live Query 1 — Service Ownership & On-Call (0:25 - 0:50)
- **Visual:** Click suggestion chip: *"Who owns the Payment Gateway?"*
- **Visual Action:** Watch the answer stream in instantaneously (3.4ms latency badge).
- **Voiceover:**
  > *"Let's ask DevTrace: 'Who owns the Payment Gateway?'  
  > In less than 4 milliseconds, FalkorDB traverses the graph from the Payment Gateway node to the Payments Team, returning Elena Rostova as Staff Architect and Bob Smith as the on-call engineer, complete with their direct Slack channels and disaster recovery runbooks."*

---

### Scene 3: Live Query 2 — Dependency Blast Radius (0:50 - 1:15)
- **Visual:** Click suggestion chip: *"What services break if the Billing DB fails?"*
- **Visual Action:** Camera highlights the visited entities and the relationship path `System → System → Document`.
- **Voiceover:**
  > *"Now imagine an outage on our primary database. 'What services break if the Billing DB fails?'  
  > Traditional vector search fails here, but FalkorDB executes a recursive topological graph traversal. It reveals a critical outage for Payment Gateway, degraded authentication, and stalled invoice webhooks—giving SREs instant blast radius intelligence before making changes."*

---

### Scene 4: Live Query 3 — Architecture Decision Records (1:15 - 1:40)
- **Visual:** Click suggestion chip: *"Why was the legacy cache migrated?"*
- **Visual Action:** Response displays ADR-012, author Alice Johnson, and date.
- **Voiceover:**
  > *"No more lost decisions. When asked 'Why was the legacy cache migrated?', DevTrace locates ADR-012, showing that Alice Johnson led the migration from legacy Redis to FalkorDB because FalkorDB delivers sub-millisecond multi-hop Cypher queries that slashed lookup latency by over 90%."*

---

### Scene 5: Live Cypher Transparency & Closing (1:40 - 2:00)
- **Visual:** Expand the **Graph Inspector Drawer** on the right side. Show syntax-colored Cypher, copy button, and visited node pills. Show the green *"FalkorDB Connected"* status dot.
- **Voiceover:**
  > *"What makes DevTrace unique is radical transparency. Every single answer is backed by the exact executed Cypher query in our live graph inspector—no black box hallucinations, only verified graph truth.  
  > DevTrace turns tribal silos into instant engineering intelligence. Thank you!"*

---

## 📋 Recording Checklist
- [ ] FalkorDB container running: `docker run -p 6379:6379 falkordb/falkordb:latest`
- [ ] Knowledge graph seeded: `python backend/seed.py`
- [ ] Backend running: `uvicorn backend.main:app --port 8000`
- [ ] Frontend running: `npm run dev` in browser at 1080p / 60fps
- [ ] Microphone test: crisp audio with no background noise
- [ ] Keep browser window zoomed at 110% for crisp code readability.
