@echo off
echo.
echo  ██████╗ ██████╗ ██████╗ ██╗   ██╗███████╗    ██████╗ ██████╗ ███████╗
echo  ██╔════╝██╔═══██╗██╔══██╗██║   ██║██╔════╝    ██╔══██╗██╔══██╗██╔════╝
echo  ██║     ██║   ██║██████╔╝██║   ██║███████╗    ██████╔╝██║  ██║█████╗
echo  ██║     ██║   ██║██╔══██╗╚██╗ ██╔╝╚════██║    ██╔═══╝ ██║  ██║██╔══╝
echo  ╚██████╗╚██████╔╝██║  ██║ ╚████╔╝ ███████║    ██║     ██████╔╝██║
echo   ╚═════╝ ╚═════╝ ╚═╝  ╚═╝  ╚═══╝  ╚══════╝    ╚═╝     ╚═════╝ ╚═╝
echo.
echo  [CORVUS LABS] Build Script — CorvusPDF v1.0
echo  ─────────────────────────────────────────────
echo.

cd /d "%~dp0"

echo  [1/3] Instalando dependencias...
pip install pypdf pyinstaller --quiet --upgrade
if %ERRORLEVEL% NEQ 0 (
    echo  ERRO: Falha ao instalar dependencias.
    pause
    exit /b 1
)

echo  [2/3] Empacotando com PyInstaller...
pyinstaller ^
    --onefile ^
    --noconsole ^
    --name CorvusPDF ^
    --clean ^
    corvus_pdf.py

if %ERRORLEVEL% NEQ 0 (
    echo  ERRO: Falha no PyInstaller.
    pause
    exit /b 1
)

echo.
echo  [3/3] Concluido!
echo  ─────────────────────────────────────────────
echo  Executavel em: %~dp0dist\CorvusPDF.exe
echo.

:: Abre a pasta dist automaticamente
explorer "%~dp0dist"

pause
