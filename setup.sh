#!/bin/bash

# Colors for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Installing Ollama-Aneki...${NC}"

# Determine the installation directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
INSTALL_DIR="$HOME/.local/share/ollama-aneki"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is required but not installed. Please install Python 3 and try again.${NC}"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}pip3 is required but not installed. Please install pip3 and try again.${NC}"
    exit 1
fi

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo -e "${YELLOW}Warning: Ollama is not installed or not in PATH. This script will continue, but make sure to install Ollama for full functionality.${NC}"
fi

# Create installation directory
echo -e "${GREEN}Creating installation directory...${NC}"
mkdir -p "$INSTALL_DIR"

# Copy necessary files to the installation directory
echo -e "${GREEN}Copying files to installation directory...${NC}"
cp -r "$SCRIPT_DIR"/* "$INSTALL_DIR"

# Create virtual environment
echo -e "${GREEN}Creating virtual environment...${NC}"
python3 -m venv "$INSTALL_DIR/venv"

# Activate virtual environment and install dependencies
echo -e "${GREEN}Installing dependencies...${NC}"
source "$INSTALL_DIR/venv/bin/activate"
pip install -r "$INSTALL_DIR/requirements.txt"
deactivate

# Create necessary directories for saving data
echo -e "${GREEN}Creating data directories...${NC}"
mkdir -p "$INSTALL_DIR/saves/custom/models"
mkdir -p "$INSTALL_DIR/saves/custom/lowres"
mkdir -p "$INSTALL_DIR/saves/custom/exp"

# Copy default config if it doesn't exist
if [ ! -f "$INSTALL_DIR/saves/default/config.conf" ]; then
    echo -e "${GREEN}Creating default configuration...${NC}"
    mkdir -p "$INSTALL_DIR/saves/default"
    # This is a minimal config, you might want to create a more detailed one
    cat > "$INSTALL_DIR/saves/default/config.conf" << EOF
alert = [red]
asciiart = [yellow]
asciiart_index = -1
ascii2_path = saves/default/ascii2.txt
asciis1_path = saves/default/ascii1.txt
ask_for_Topic = 1
auto_clear = 1
box_borders = DOUBLE
box_width = 0
custom_path = saves/custom
emotion_generation = 1
exit_code = die
highlight = [blue]
max_respose_size = 500
memory_length = 10
normal = [white]
pngfolder = Aneki
reprint_everytime = 0
user_conversation = >>
width = 40
height = 30
EOF
fi

# Create the aneki.sh script
echo -e "${GREEN}Creating aneki command script...${NC}"
cat > "$INSTALL_DIR/aneki.sh" << EOF
#!/bin/bash

# Define the installation directory path
INSTALL_DIR="$INSTALL_DIR"

# Function to handle Ctrl+C gracefully
function handle_interrupt() {
    echo -e "\nExiting Ollama-Aneki..."
    # Return to the directory where the command was executed
    cd "\$ORIGINAL_DIR"
    exit 0
}

# Register the interrupt handler
trap handle_interrupt SIGINT

# Save the original directory
ORIGINAL_DIR="\$(pwd)"

# Activate the virtual environment and run the application
cd "\$INSTALL_DIR" || { echo "Installation directory not found. Please reinstall."; exit 1; }
source venv/bin/activate || { echo "Virtual environment not found. Please reinstall."; exit 1; }

# Run the application with all arguments passed to this script
python run.py "\$@"

# Return to the original directory when the application exits
cd "\$ORIGINAL_DIR"
EOF

chmod +x "$INSTALL_DIR/aneki.sh"

# Create global executable
echo -e "${GREEN}Creating global executable...${NC}"
sudo mkdir -p /usr/local/bin
sudo ln -sf "$INSTALL_DIR/aneki.sh" /usr/local/bin/aneki
sudo chmod +x /usr/local/bin/aneki

echo -e "${GREEN}Installation complete!${NC}"
echo -e "${YELLOW}You can now run 'aneki' from anywhere in your terminal.${NC}"