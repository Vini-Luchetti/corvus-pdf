@echo off
chcp 65001 > nul
echo.
echo  CORVUS LABS — Corvus PDF 1.0.0
echo  ────────────────────────────────────────
echo.

cd /d "%~dp0"
echo  [1/3] Verificando dependencias...
pip install -r requirements.txt --quiet
if %ERRORLEVEL% NEQ 0 (
    echo  ERRO: Falha ao instalar dependencias.
    pause & exit /b 1
)

echo  [2/3] Empacotando com PyInstaller...
pyinstaller CorvusPDF.spec --clean --noconfirm
if %ERRORLEVEL% NEQ 0 (
    echo  ERRO: Falha no PyInstaller.
    pause & exit /b 1
)

echo.
echo  [3/3] Concluido.
echo  ────────────────────────────────────────
echo  Executavel: %~dp0dist\CorvusPDF.exe
echo.

explorer "%~dp0dist"
pause