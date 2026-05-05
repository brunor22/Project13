@echo off
echo Updating Stock Screener...
python "%~dp0stock_screener_app.py"
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Something went wrong. Make sure Python is installed.
    pause
    exit /b 1
)
echo.
echo Done! Opening stock_screener.html...
start "" "%~dp0stock_screener.html"
