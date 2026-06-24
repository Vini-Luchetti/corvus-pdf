@echo off
cd /d "%~dp0"
call "%~dp0env_pdf\Scripts\activate.bat"
python "%~dp0manipula_pdf.py" %*
pause