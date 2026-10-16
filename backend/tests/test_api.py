import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_check_endpoint():
    """Verify health endpoint reports healthy service state."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "DevTrace Company Brain API"
    assert data["version"] == "1.0.0"
    assert "falkordb_connected" in data

def test_ask_service_ownership():
    """Verify natural language ownership query resolves with team and engineers."""
    payload = {
        "prompt": "Who owns the Payment Gateway?",
        "demo_mode": True
    }
    response = client.post("/api/ask", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "cypher_query" in data
    assert "MATCH" in data["cypher_query"]
    assert len(data["traversed_nodes"]) > 0
    node_names = [n["name"] for n in data["traversed_nodes"]]
    assert "Payment Gateway" in node_names
    assert "Payments Team" in node_names

def test_ask_dependency_blast_radius():
    """Verify downstream system impact analysis for critical database outage."""
    payload = {
        "prompt": "What services break if the Billing DB fails?",
        "demo_mode": True
    }
    response = client.post("/api/ask", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "Billing DB" in data["answer"]
    assert len(data["citations"]) > 0
    assert any("Billing DB Failover" in c["title"] for c in data["citations"])
    node_types = [n["type"] for n in data["traversed_nodes"]]
    assert "System" in node_types

def test_ask_adr_cache_migration():
    """Verify historical architecture decision record (ADR) provenance lookup."""
    payload = {
        "prompt": "Why was the legacy cache migrated to FalkorDB?",
        "demo_mode": True
    }
    response = client.post("/api/ask", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "ADR-012" in data["answer"]
    assert "FalkorDB" in data["answer"]
    assert len(data["traversed_nodes"]) >= 2
    assert any(n["type"] == "Decision" for n in data["traversed_nodes"])

def test_ask_validation_error_on_empty_body():
    """Verify Pydantic validation rejects requests missing required prompt."""
    response = client.post("/api/ask", json={})
    assert response.status_code == 422
