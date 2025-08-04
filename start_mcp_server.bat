@echo off
echo Starting MariaDB MCP Server...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found in PATH
    echo Please install Python or add it to your PATH
    pause
    exit /b 1
)

REM Install requirements if needed
echo Installing/updating requirements...
pip install -r requirements.txt --quiet

echo.
echo Starting MCP Server on http://localhost:9001
echo Press Ctrl+C to stop the server
echo.

REM Start the MCP server
python mcp_server.py

pause