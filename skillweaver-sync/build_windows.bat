@echo off
REM Build WoW Suite Sync for Windows
REM Creates .exe and installer

echo Building WoW Suite Sync for Windows...

REM Install PyInstaller if needed
pip install pyinstaller pillow --upgrade

REM Clean previous builds
rmdir /s /q build dist

REM Build executable
pyinstaller build_windows.spec --clean

REM Create installer with Inno Setup (if installed)
where iscc >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    iscc installer_windows.iss
    echo Done! Installer created: Output\WoWSuiteSync-Setup.exe
) else (
    echo WARNING: Inno Setup not found. Install from https://jrsoftware.org/isdl.php
    echo Done! Executable created: dist\WoWSuiteSync.exe
)
