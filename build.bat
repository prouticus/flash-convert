@echo off
echo Building Flash Convert...
pyinstaller --onefile --noconsole flash_convert.py
echo.
if exist dist\flash_convert.exe (
    echo Build successful: dist\flash_convert.exe
) else (
    echo Build failed!
)
pause
