@echo off
setlocal enabledelayedexpansion

echo Installing Ollama-Aneki...

:: Determine script directory and installation directory
set "SCRIPT_DIR=%~dp0"
set "INSTALL_DIR=%USERPROFILE%\AppData\Local\ollama-aneki"

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is required but not installed. Please install Python and try again.
    exit /b 1
)

:: Check if pip is installed
pip --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo pip is required but not installed. Please install pip and try again.
    exit /b 1
)

:: Check if Ollama is installed
ollama --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Warning: Ollama is not installed or not in PATH. This script will continue, but make sure to install Ollama for full functionality.
)

:: Create installation directory
echo Creating installation directory...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

:: Copy necessary files to the installation directory
echo Copying files to installation directory...
xcopy /E /I /Y "%SCRIPT_DIR%\*" "%INSTALL_DIR%\"

:: Create virtual environment
echo Creating virtual environment...
python -m venv "%INSTALL_DIR%\venv"

:: Activate virtual environment and install dependencies
echo Installing dependencies...
call "%INSTALL_DIR%\venv\Scripts\activate.bat"
pip install -r "%INSTALL_DIR%\requirements.txt"
deactivate

:: Create necessary directories for saving data
echo Creating data directories...
if not exist "%INSTALL_DIR%\saves\custom\models" mkdir "%INSTALL_DIR%\saves\custom\models"
if not exist "%INSTALL_DIR%\saves\custom\lowres" mkdir "%INSTALL_DIR%\saves\custom\lowres"
if not exist "%INSTALL_DIR%\saves\custom\exp" mkdir "%INSTALL_DIR%\saves\custom\exp"

:: Copy default config if it doesn't exist
if not exist "%INSTALL_DIR%\saves\default\config.conf" (
    echo Creating default configuration...
    if not exist "%INSTALL_DIR%\saves\default" mkdir "%INSTALL_DIR%\saves\default"
    
    (
        echo alert = [red]
        echo asciiart = [yellow]
        echo asciiart_index = -1
        echo ascii2_path = saves/default/ascii2.txt
        echo asciis1_path = saves/default/ascii1.txt
        echo ask_for_Topic = 1
        echo auto_clear = 1
        echo box_borders = DOUBLE
        echo box_width = 0
        echo custom_path = saves/custom
        echo emotion_generation = 1
        echo exit_code = die
        echo highlight = [blue]
        echo max_respose_size = 500
        echo memory_length = 10
        echo normal = [white]
        echo pngfolder = Aneki
        echo reprint_everytime = 0
        echo user_conversation = ^^>^^>
        echo width = 40
        echo height = 30
    ) > "%INSTALL_DIR%\saves\default\config.conf"
)

:: Create the aneki.bat script
echo Creating aneki command script...
(
    echo @echo off
    echo setlocal
    echo.
    echo :: Save the original directory
    echo set "ORIGINAL_DIR=%%CD%%"
    echo.
    echo :: Change to the installation directory and activate the virtual environment
    echo cd /d "%INSTALL_DIR%" ^|^| ^(echo Installation directory not found. Please reinstall. ^& exit /b 1^)
    echo call venv\Scripts\activate.bat ^|^| ^(echo Virtual environment not found. Please reinstall. ^& exit /b 1^)
    echo.
    echo :: Run the application with all arguments passed to this script
    echo python run.py %%*
    echo.
    echo :: Return to the original directory and deactivate the virtual environment
    echo cd /d "%%ORIGINAL_DIR%%"
    echo call venv\Scripts\deactivate.bat
    echo.
    echo endlocal
) > "%INSTALL_DIR%\aneki.bat"

:: Add the installation directory to PATH
echo Adding installation directory to PATH...
setx PATH "%PATH%;%INSTALL_DIR%"

:: Create a shortcut in the Start Menu
echo Creating Start Menu shortcut...
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\Ollama-Aneki.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\aneki.bat'; $Shortcut.Save()"

echo Installation complete!
echo You can now run 'aneki' from anywhere in your terminal.
echo Please restart your command prompt for the PATH changes to take effect.

endlocal