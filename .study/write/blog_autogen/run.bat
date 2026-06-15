@echo off
chcp 65001 > nul
setlocal
cd /d "%~dp0"

set "VENV_PY=c:\_proj\python_workspace\.venv\Scripts\python.exe"

if not exist "%VENV_PY%" (
    echo [ERROR] venv Python not found: %VENV_PY%
    pause
    exit /b 1
)

echo [1/2] Checking dependencies...
"%VENV_PY%" -m pip install -r "%~dp0requirements.txt"
if errorlevel 1 (
    echo [ERROR] pip install failed
    pause
    exit /b 1
)

echo.
echo [2/2] Starting GUI...
"%VENV_PY%" "%~dp0gui.py"

endlocal