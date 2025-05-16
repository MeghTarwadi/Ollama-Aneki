#!/bin/bash

# Define the installation directory path
INSTALL_DIR="$HOME/.local/share/ollama-aneki"

# Function to handle Ctrl+C gracefully
function handle_interrupt() {
    echo -e "\nExiting Ollama-Aneki..."
    # Return to the directory where the command was executed
    cd "$ORIGINAL_DIR"
    exit 0
}

# Register the interrupt handler
trap handle_interrupt SIGINT

# Save the original directory
ORIGINAL_DIR="$(pwd)"

# Activate the virtual environment and run the application
cd "$INSTALL_DIR" || { echo "Installation directory not found. Please reinstall."; exit 1; }
source venv/bin/activate || { echo "Virtual environment not found. Please reinstall."; exit 1; }

# Run the application with all arguments passed to this script
python run.py "$@"

# Return to the original directory when the application exits
cd "$ORIGINAL_DIR"