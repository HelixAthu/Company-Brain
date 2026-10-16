from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    """Schema for natural language user query sent to the Company Brain."""
    prompt: str = Field(..., description="Natural language query from developer or on-call engineer")
    user_context: Optional[Dict[str, Any]] = Field(default=None, description="Optional caller context, e.g. role, team")
    demo_mode: Optional[bool] = Field(default=False, description="Explicitly trigger offline demo response mode")

class Citation(BaseModel):
    """Schema for documentation or architectural citations returned with answer."""
    title: str = Field(..., description="Document or ADR title")
    url: Optional[str] = Field(default=None, description="Internal link or wiki URL")
    type: Optional[str] = Field(default="Runbook", description="Citation type (Runbook, ADR, Spec)")

class TraversedNode(BaseModel):
    """Graph entity traversed during Cypher execution."""
    id: str = Field(..., description="Node ID or slug")
    name: str = Field(..., description="Human readable entity name")
    type: str = Field(..., description="Entity type: Person, Team, System, Document, Decision")
    details: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Metadata key-value pairs")

class QueryResponse(BaseModel):
    """Full trace response payload returning answer, Cypher query, and graph provenance."""
    answer: str = Field(..., description="Synthesized natural language answer with citations")
    cypher_query: str = Field(..., description="Generated Cypher query executed against FalkorDB")
    traversed_nodes: List[TraversedNode] = Field(default_factory=list, description="List of graph nodes visited")
    citations: List[Citation] = Field(default_factory=list, description="Referenced documents and runbooks")
    execution_time_ms: Optional[float] = Field(default=None, description="Total execution time in milliseconds")
    raw_results: Optional[List[Dict[str, Any]]] = Field(default=None, description="Raw rows returned from graph")
