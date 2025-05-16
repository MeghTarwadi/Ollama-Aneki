@"echo off
setlocal enabledelayedexpansion

echo Installing Ollama-Aneki...

:: Determine script and install directories
set "SCRIPT_DIR=%~dp0"
set "INSTALL_DIR=%USERPROFILE%\AppData\Local\ollama-aneki"

:: Check Python, pip, Ollama
python --version >nul 2>&1 || (echo Python required. Install and retry.& exit /b 1)
pip --version >nul 2>&1 || (echo pip required. Install and retry.& exit /b 1)
ollama --version >nul 2>&1 || echo Warning: Ollama missing; continue if intentional.

:: Prepare install dir
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
xcopy /E /I /Y "%SCRIPT_DIR%\*" "%INSTALL_DIR%\"

:: Setup venv and deps
python -m venv "%INSTALL_DIR%\venv"
call "%INSTALL_DIR%\venv\Scripts\activate.bat"
pip install -r "%INSTALL_DIR%\requirements.txt"
deactivate

:: Ensure data directories
for %%D in (custom\models custom\lowres custom\exp) do (
  if not exist "%INSTALL_DIR%\saves\%%D" mkdir "%INSTALL_DIR%\saves\%%D"
)

:: (Removed default config backup block)

:: Create launcher
(
  echo @echo off
  echo cd /d "%INSTALL_DIR%" || (echo Missing dir; reinstall.& exit /b 1)
  echo call venv\Scripts\activate.bat
  echo python run.py %%*
  echo deactivate
) > "%INSTALL_DIR%\aneki.bat"

:: Add install dir to user PATH
for /f "tokens=2*" %%A in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set "OLDPATH=%%B"
if defined OLDPATH (
  echo %OLDPATH% | find /I "%INSTALL_DIR%" >nul || (
    set "NEWPATH=%OLDPATH%;%INSTALL_DIR%"
    echo Adding to PATH... & setx PATH "%NEWPATH%"
  )
) else (
  echo Setting PATH for first time... & setx PATH "%INSTALL_DIR%"
)

echo Installation complete! Restart your shell to pick up PATH changes.
endlocal
