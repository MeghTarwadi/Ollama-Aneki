# Installation Guide for Ollama-Aneki

This guide will help you install Ollama-Aneki on your system.

## Prerequisites

Before installing Ollama-Aneki, make sure you have:

1. **Python 3.6 or higher** installed on your system
2. **Ollama** installed and configured (https://ollama.com)
3. **Git** for cloning the repository

## Choose your operating system

### For Linux

1. Open your terminal and run:
   ```bash
   # Clone the repository
   git clone https://github.com/MeghTarwadi/ollama-aneki.git

   # Navigate to the directory
   cd ollama-aneki

   # Run the setup script
   chmod +x setup.sh
   ./setup.sh
   ```
2. The installation will create an `aneki` command available system-wide.
3. Test it by running:
   ```bash
   aneki help
   ```

### For Windows

1. Open PowerShell or Command Prompt (Administrator recommended) and run:
   ```powershell
   # Install Git if not already installed
   winget install Git.Git

   # Close and reopen your terminal after installing Git

   # Clone the repository
   git clone https://github.com/MeghTarwadi/ollama-aneki.git C:\temp\ollama-aneki

   # Navigate to the directory
   cd C:\temp\ollama-aneki

   # Run the setup script
   .\setup.bat
   ```
2. Restart your terminal or command prompt.
3. Test it by running:
   ```powershell
   aneki help
   ```

## Troubleshooting

If you encounter issues:

1. **Command not found** : Make sure the installation completed successfully. For Windows, you may need to restart your terminal.
2. **Dependencies missing** : Try reinstalling with:

```bash
   # For Linux
   pip install -r requirements.txt

   # For Windows
   pip install -r requirements.txt
```

1. **Permission issues** : On Linux, you might need to run the setup script with sudo:

```bash
   sudo ./setup.sh
```

## Next Steps

Now that you've installed Ollama-Aneki, try creating your first custom model:

```bash
aneki new
```

Follow the prompts to configure your model, then run it with:

```bash
aneki run [your-model-name]
```

Enjoy your enhanced Ollama experience!
