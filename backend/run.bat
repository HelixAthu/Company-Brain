@echo off
echo ========================================================
echo   Starting DevTrace: Company Brain Backend Services
echo ========================================================

:: Check for virtual environment
if exist venv\Scripts\activate (
    echo Activating virtual environment...
    call venv\Scripts\activate
) else if exist ..\venv\Scripts\activate (
    echo Activating parent virtual environment...
    call ..\venv\Scripts\activate
) else (
    echo Warning: No venv detected, using global python environment.
)

:: Seed graph database with enterprise entities
echo.
echo [1/2] Seeding FalkorDB Knowledge Graph...
python seed.py

:: Start FastAPI server
echo.
echo [2/2] Launching DevTrace FastAPI Server on http://localhost:8000...
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
