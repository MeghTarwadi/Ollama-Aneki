@echo off
setlocal

:: Save the original directory
set "ORIGINAL_DIR=%CD%"

:: Installation directory
set "INSTALL_DIR=%USERPROFILE%\AppData\Local\ollama-aneki"

:: Handle Ctrl+C and errors gracefully
:: The following provides a cleaner exit mechanism
if not exist "%INSTALL_DIR%" (
    echo Installation directory not found. Please run setup.bat first.
    exit /b 1
)

:: Change to the installation directory and activate the virtual environment
cd /d "%INSTALL_DIR%" || (echo Installation directory not found. Please reinstall. & exit /b 1)
call venv\Scripts\activate.bat || (echo Virtual environment not found. Please reinstall. & exit /b 1)

:: Run the application with all arguments passed to this script
python run.py %*

:: Return to the original directory and deactivate the virtual environment
cd /d "%ORIGINAL_DIR%"
call venv\Scripts\deactivate.bat

endlocal