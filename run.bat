@echo off
:: ══════════════════════════════════════════════════════════
::  TikFetch — Windows Launcher
:: ══════════════════════════════════════════════════════════
setlocal EnableDelayedExpansion

set "SCRIPT_DIR=%~dp0"
set "VENV_DIR=%SCRIPT_DIR%.venv"
set "MAIN_SCRIPT=%SCRIPT_DIR%tikfetch.py"
set "REQ_FILE=%SCRIPT_DIR%requirements.txt"

title TikFetch — TikTok Video Downloader

echo.
echo  =====================================================
echo   TikFetch  --  TikTok Video Downloader
echo  =====================================================
echo.

:: ── Find Python ───────────────────────────────────────────
set "PYTHON="
for %%P in (python python3) do (
    if "!PYTHON!"=="" (
        where %%P >nul 2>&1
        if !errorlevel! == 0 (
            set "PYTHON=%%P"
        )
    )
)

if "!PYTHON!"=="" (
    echo [ERROR] Python 3.8+ is required but was not found.
    echo         Please install it from: https://www.python.org/downloads/
    echo         Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%V in ('!PYTHON! --version 2^>^&1') do set "PY_VER=%%V"
echo [OK]   Found Python !PY_VER!

:: ── Create virtualenv ─────────────────────────────────────
if not exist "!VENV_DIR!\Scripts\python.exe" (
    echo [INFO] Creating virtual environment...
    !PYTHON! -m venv "!VENV_DIR!"
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [OK]   Virtual environment created.
)

set "PYTHON=!VENV_DIR!\Scripts\python.exe"

:: ── Install dependencies ──────────────────────────────────
echo [INFO] Checking dependencies...
"!PYTHON!" -m pip install --quiet --upgrade pip
if exist "!REQ_FILE!" (
    "!PYTHON!" -m pip install --quiet -r "!REQ_FILE!"
) else (
    "!PYTHON!" -m pip install --quiet --upgrade yt-dlp rich
)
echo [OK]   Dependencies ready.

:: ── Check ffmpeg ──────────────────────────────────────────
where ffmpeg >nul 2>&1
if !errorlevel! neq 0 (
    echo.
    echo [WARN] ffmpeg is not installed. Video merging may not work.
    echo        Download it from: https://ffmpeg.org/download.html
    echo        Or install via winget: winget install ffmpeg
    echo        Or via chocolatey:     choco install ffmpeg
    echo.
    echo  Press any key to continue anyway, or Ctrl+C to abort...
    pause >nul
)

:: ── Launch ────────────────────────────────────────────────
echo.
"!PYTHON!" "!MAIN_SCRIPT!" %*

:: Keep window open after script exits (so user can read output)
echo.
echo  =====================================================
echo   Program finished. Press any key to close this window.
echo  =====================================================
pause >nul
endlocal
