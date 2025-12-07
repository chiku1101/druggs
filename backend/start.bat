@echo off
REM Start the FastAPI backend server for Windows

echo Starting Drug Repurposing Platform Backend...
echo Server will run on http://localhost:8000
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies if needed
if not exist "venv\.installed" (
    echo Installing dependencies...
    pip install -r requirements.txt
    type nul > venv\.installed
)

REM Run the server
echo Starting FastAPI server...
python main.py

pause

