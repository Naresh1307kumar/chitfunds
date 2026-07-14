@echo off
echo ===================================================
echo Starting Secure Chit Fund Management System...
echo ===================================================

echo Starting Backend API (FastAPI)...
cd backend
start cmd /k ".\venv\Scripts\activate & python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo Starting Frontend (React/Vite)...
cd ../frontend
start cmd /k "npm run dev"

echo Both servers are starting up!
echo Backend API will be at: http://localhost:8000
echo Frontend will be at: http://localhost:5174
echo.
echo You can close this window now. The servers are running in the other windows.
pause
