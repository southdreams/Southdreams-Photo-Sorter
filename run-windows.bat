@echo off
:: ====================================================
::   SOUTHDREAMS PHOTO SORTER v2.0 — Windows Launcher
::   by SouthDreams | Dirty Road Creations
::   Double-click this file to run.
:: ====================================================

title SouthDreams Photo Sorter v2.0

cls
echo.
echo ====================================================
echo   SOUTHDREAMS PHOTO SORTER v2.0
echo   by SouthDreams ^| Dirty Road Creations
echo ====================================================
echo.

:: ── CHECK: Python installed? ────────────────────────
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   Python is NOT installed.
    echo.
    echo   To install Python for free:
    echo   1. Go to: https://www.python.org/downloads/
    echo   2. Click the big Download button
    echo   3. Run the installer
    echo   4. IMPORTANT: Check "Add Python to PATH"
    echo   5. Double-click this file again
    echo.
    pause
    exit /b 1
)

:: ── CHECK: Pillow installed? ─────────────────────────
python -c "from PIL import Image" >nul 2>&1
if %errorlevel% neq 0 (
    echo   Installing Pillow (needed to read photo dates)...
    pip install Pillow --quiet
    echo   Pillow installed.
    echo.
)

:: ── ASK: Source folder ───────────────────────────────
echo   Where are your UNSORTED photos?
echo.
echo   Examples:
echo     C:\Users\YourName\Pictures
echo     C:\Users\YourName\Downloads
echo     D:\PhoneBackup
echo.
set /p SOURCE="  Type or paste the folder path: "

if not exist "%SOURCE%" (
    echo.
    echo   [ERROR] Folder not found: %SOURCE%
    pause
    exit /b 1
)

:: ── ASK: Destination folder ──────────────────────────
echo.
echo   Where do you want the SORTED photos to go?
echo.
echo   Example: C:\Users\YourName\Sorted_Photos
echo.
set /p DEST="  Type or paste the destination path: "

echo.

:: ── ASK: Mode ────────────────────────────────────────
echo   What do you want to do?
echo.
echo   1 = PREVIEW  - Show what will happen (safe, nothing moves)
echo   2 = SORT     - Actually sort and move the files
echo.
set /p CHOICE="  Type 1 or 2: "

echo.

set SCRIPT_DIR=%~dp0

if "%CHOICE%"=="2" (
    echo   Running in SORT mode...
    python "%SCRIPT_DIR%src\photo_sorter.py" "%SOURCE%" "%DEST%" --confirm
) else (
    echo   Running in PREVIEW mode (safe)...
    python "%SCRIPT_DIR%src\photo_sorter.py" "%SOURCE%" "%DEST%"
)

echo.
pause
