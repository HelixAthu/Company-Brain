import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.database import db_manager

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
