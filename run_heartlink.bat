@echo off
cd %~dp0
call conda activate heartlink
streamlit run app.py
pause
