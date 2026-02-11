@echo off
echo === Flash Convert - Full Build ===
echo.

echo [1/2] Building flash_convert.exe with PyInstaller...
pyinstaller --onefile --noconsole flash_convert.py
if not exist dist\flash_convert.exe (
    echo FAILED: PyInstaller build did not produce dist\flash_convert.exe
    pause
    exit /b 1
)
echo       Done.
echo.

echo [2/2] Building installer with Inno Setup...
where iscc >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Inno Setup compiler (iscc) not found on PATH.
    echo        Install Inno Setup from https://jrsoftware.org/isdownload.php
    echo        then add its directory to your PATH, or run:
    echo        "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
    pause
    exit /b 1
)
iscc installer.iss
echo.

if exist installer_output\FlashConvert_Setup.exe (
    echo === SUCCESS ===
    echo Installer: installer_output\FlashConvert_Setup.exe
) else (
    echo === FAILED ===
)
pause
