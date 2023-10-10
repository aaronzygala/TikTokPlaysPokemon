@echo off

REM Run Python script
start cmd /k python main.py

REM Open a new Command Prompt window, navigate to the tpp-dashboard directory, and run npm dev
start cmd /k cd tpp-dashboard && npm run dev
