@echo off
cd /d "%~dp0"
REM Start VS Code
start code .
REM Start the FastAPI server
start powershell -NoExit -Command "python server.py"
REM Start ngrok TCP tunnel on port 8000
start powershell -NoExit -Command "ngrok tcp 8000"