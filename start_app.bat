@echo off
echo Starting OEE Analysis Application...

:: Start the backend server
start cmd /k "cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

:: Wait for a moment to ensure backend starts first
timeout /t 5

:: Start the frontend server
start cmd /k "cd frontend && npm start"

:: Open the application in default browser
timeout /t 5
start http://localhost:3001

echo Application is starting...
echo Backend server: http://localhost:8000
echo Frontend server: http://localhost:3001 