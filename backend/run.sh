#!/usr/bin/env bash
set -e

echo "========================================================"
echo "  Starting DevTrace: Company Brain Backend Services"
echo "========================================================"

if [ -f "venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

echo ""
echo "[1/2] Seeding FalkorDB Knowledge Graph..."
python seed.py

echo ""
echo "[2/2] Launching DevTrace FastAPI Server on http://localhost:8000..."
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
