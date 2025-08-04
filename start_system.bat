@echo off
echo ========================================
echo   MariaDB User Management System
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found in PATH
    echo Please install Python or add it to your PATH
    pause
    exit /b 1
)

echo Starting MariaDB MCP Server (Port 9001)...
start "MCP Server" cmd /k "python mcp_server.py"

echo Starting API Server (Port 9002)...
start "API Server" cmd /k "python api_server.py"

echo Waiting for servers to start...
timeout /t 5 /nobreak >nul

echo Starting Web UI Server (Port 8080)...
start "Web UI" cmd /k "python web_server.py"

echo.
echo ========================================
echo   System Started Successfully!
echo ========================================
echo.
echo MCP Server: http://localhost:9001
echo API Server: http://localhost:9002  
echo Web UI:     http://localhost:8080
echo.
echo Both servers are running in separate windows.
echo Close those windows to stop the servers.
echo.

pause