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
set "ISCC="
where iscc >nul 2>nul
if not errorlevel 1 (
    set "ISCC=iscc"
) else if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    set "ISCC=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
) else if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    set "ISCC=C:\Program Files\Inno Setup 6\ISCC.exe"
)
if not defined ISCC (
    echo ERROR: Inno Setup compiler not found.
    echo        Install Inno Setup from https://jrsoftware.org/isdownload.php
    pause
    exit /b 1
)
"%ISCC%" installer.iss
echo.

if exist installer_output\FlashConvert_Setup.exe (
    echo === SUCCESS ===
    echo Installer: installer_output\FlashConvert_Setup.exe
) else (
    echo === FAILED ===
)
pause
