# 📡 DevTrace API Reference & Specification

This specification documents the REST API provided by the **DevTrace Company Brain** backend running on FastAPI.

- **Base URL (Local):** `http://localhost:8000`
- **Swagger Documentation:** `http://localhost:8000/docs`
- **ReDoc Documentation:** `http://localhost:8000/redoc`

---

## 1. Health Status Check

Check backend service liveness and active FalkorDB connectivity.

- **Endpoint:** `GET /health`
- **Headers:** `Accept: application/json`

### Example cURL:
```bash
curl -X GET "http://localhost:8000/health" \
     -H "Accept: application/json"
```

### Successful Response (200 OK):
```json
{
  "status": "healthy",
  "service": "DevTrace Company Brain API",
  "version": "1.0.0",
  "falkordb_connected": true,
  "demo_mode": false
}
```

---

## 2. Natural Language Graph Query

Translates natural language questions into FalkorDB Cypher, executes the graph traversal, and returns synthesized answers with citations and visited nodes.

- **Endpoint:** `POST /api/ask`
- **Headers:**
  - `Content-Type: application/json`
  - `Accept: application/json`

### Request Body Schema:
| Field | Type | Required | Description |
|---|---|---|---|
| `prompt` | String | Yes | Developer query in natural language |
| `demo_mode` | Boolean | No | Force pre-calculated mock response mode (default: `false`) |
| `user_context` | Object | No | Caller metadata (role, team, permissions) |

### Example cURL (Service Ownership):
```bash
curl -X POST "http://localhost:8000/api/ask" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "Who owns the Payment Gateway?",
       "demo_mode": false
     }'
```

### Example cURL (Blast Radius Analysis):
```bash
curl -X POST "http://localhost:8000/api/ask" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "What services break if the Billing DB fails?",
       "demo_mode": false
     }'
```

### Example cURL (Architecture Decision Record Lineage):
```bash
curl -X POST "http://localhost:8000/api/ask" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "Why was the legacy cache migrated?",
       "demo_mode": false
     }'
```

### Successful Response (200 OK):
```json
{
  "answer": "### Payment Gateway Ownership\n\n**The Payments Team** owns the **Payment Gateway API** (Tier-1 critical service)...\n",
  "cypher_query": "MATCH (s:System {name: 'Payment Gateway'})<-[:OWNS]-(t:Team)<-[:MEMBER_OF]-(p:Person) RETURN s, t, collect(p) AS engineers",
  "traversed_nodes": [
    {
      "id": "payment_gateway",
      "name": "Payment Gateway",
      "type": "System",
      "details": {
        "tier": "Tier-1",
        "status": "production"
      }
    },
    {
      "id": "payments_team",
      "name": "Payments Team",
      "type": "Team",
      "details": {
        "slack": "#team-payments",
        "domain": "FinTech"
      }
    }
  ],
  "citations": [
    {
      "title": "Payment Gateway Incident Runbook & Disaster Recovery",
      "url": "https://wiki.company.internal/runbooks/payment-gateway",
      "type": "Runbook"
    }
  ],
  "execution_time_ms": 3.8
}
```

---

## 3. Error Handling

### 422 Unprocessable Entity
Occurs when the request body is missing the required `prompt` field:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "prompt"],
      "msg": "Field required"
    }
  ]
}
```

### 500 Internal Server Error
Returned if an unrecoverable database or synthesis error occurs:
```json
{
  "detail": "Error executing company brain query: <error message>"
}
```
*(Note: DevTrace features built-in fallback handlers to minimize 500 errors in live presentations).*
