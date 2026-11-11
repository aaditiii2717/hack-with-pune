@echo off
cd /d "%~dp0"
set KC_DEMO_MODE=1
python -m uvicorn server:app --host 127.0.0.1 --port 8000
