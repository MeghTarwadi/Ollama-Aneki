@echo off

:: Change directory to C:\
cd C:\

:: Check if Ollama-Aneki folder exists, if not, clone it from GitHub
if not exist "C:\Ollama-Aneki" (
    echo Creating directory and cloning repository...
    mkdir C:\Ollama-Aneki
    git clone https://github.com/MeghTarwadi/Ollama-Aneki C:\Ollama-Aneki
    setx PATH "%PATH%;C:\Ollama-Aneki"
    echo "Ollama-Aneki installed and environment variable set successfully!"
    echo Installing dependencies...
    :: Install dependencies (requirements.txt)
    pip install -r requirements.txt
)

:: Change to the Ollama-Aneki directory
cd C:\Ollama-Aneki


:: Check the number of arguments passed
IF "%1"=="" (
    :: No arguments passed
    echo No arguments passed. Running run.py without arguments...
    python run.py
) ELSE IF "%2"=="" (
    :: One argument passed
    echo One argument passed: %1. Running run.py with argument...
    python run.py %1
) ELSE (
    :: Two or more arguments passed
    echo Two arguments passed: %1 %2. Running run.py with both arguments...
    python run.py %1 %2
)

pause
