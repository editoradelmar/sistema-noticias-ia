@echo off
cd /d D:\hromero\Desktop\projects\sistema-noticias-ia\backend
call venv\Scripts\activate.bat
echo =====================================
echo Iniciando Sistema de Noticias IA v2.4.0
echo =====================================
echo Directorio: %CD%
echo Entorno virtual: %VIRTUAL_ENV%
echo =====================================
uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause