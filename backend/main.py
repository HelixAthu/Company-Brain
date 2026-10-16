import logging
import time
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.database import db_manager
from backend.models import QueryRequest, QueryResponse, TraversedNode, Citation
from backend.ai_agent import gemini_agent

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("company_brain.api")

app = FastAPI(
    title="DevTrace: Company Brain API",
    description="Enterprise Knowledge Graph Intelligence Platform powered by FalkorDB and Google Gemini",
    version="1.0.0"
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    """Health check endpoint validating API and FalkorDB connectivity."""
    db_connected = db_manager.is_connected()
    return {
        "status": "healthy",
        "service": "DevTrace Company Brain API",
        "version": "1.0.0",
        "falkordb_connected": db_connected,
        "demo_mode": settings.DEMO_MODE
    }

@app.post("/api/ask", response_model=QueryResponse)
async def ask_company_brain(request: QueryRequest):
    """
    Main Question Answering pipeline:
    1. Natural Language -> FalkorDB Cypher generation via Gemini
    2. Dynamic Cypher execution with self-correcting error loop
    3. Natural language answer synthesis with citations and graph provenance
    """
    start_time = time.time()
    logger.info(f"Received query request: '{request.prompt}'")

    try:
        # Run Text-to-Cypher and Graph Traversal with self-correction
        graph_result = gemini_agent.execute_with_self_correction(request.prompt)

        # Synthesize human-readable answer and extract citations
        answer, citations = gemini_agent.synthesize_answer(
            prompt=request.prompt,
            cypher=graph_result.cypher,
            graph_rows=graph_result.data,
            traversed_nodes=graph_result.traversed_nodes
        )

        total_time_ms = round((time.time() - start_time) * 1000, 2)

        # Map traversed nodes to Pydantic models
        traversed_models = [
            TraversedNode(
                id=n.get("id", "entity"),
                name=n.get("name", "Unknown Entity"),
                type=n.get("type", "Node"),
                details=n.get("details", {})
            )
            for n in graph_result.traversed_nodes
        ]

        return QueryResponse(
            answer=answer,
            cypher_query=graph_result.cypher,
            traversed_nodes=traversed_models,
            citations=citations,
            execution_time_ms=total_time_ms,
            raw_results=graph_result.data
        )

    except Exception as e:
        logger.error(f"Error processing query request: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing company brain query: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
