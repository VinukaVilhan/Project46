@echo off
echo Building the executable with PyInstaller...
pyinstaller --noconfirm --onefile --windowed --clean --icon="path/to/icon.ico" app.py

if %errorlevel% neq 0 (
    echo PyInstaller build failed. Exiting...
    exit /b %errorlevel%
)

echo Signing the executable...
signtool sign /a /t http://timestamp.digicert.com /fd SHA256 /tr http://timestamp.digicert.com dist\app.exe

if %errorlevel% neq 0 (
    echo Code signing failed. Exiting...
    exit /b %errorlevel%
)

echo Build and signing completed successfully.
pause
