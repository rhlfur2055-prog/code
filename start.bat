@echo off
echo ========================================
echo CodeMaster Next.js Starter
echo ========================================

:: Check if node_modules exists
if not exist "node_modules" (
    echo [INFO] node_modules not found. Installing dependencies...
    call npm install
    if errorlevel 1 (
        echo [ERROR] npm install failed!
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed successfully!
) else (
    echo [OK] node_modules found.
)

:: Start dev server
echo.
echo [INFO] Starting development server...
echo [INFO] Open http://localhost:3000 in your browser
echo.
call npm run dev
