@echo off
pip install -r requirements.txt -q
start python app.py
start python -m http.server 8000
timeout /t 2 >nul
start http://localhost:8000
