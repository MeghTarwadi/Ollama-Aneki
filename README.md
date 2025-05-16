
# Ollama-Aneki

<p align="center">
  <img src="https://github.com/user-attachments/assets/e855a33f-0d49-41de-991b-affb7ed9333e" alt="Ollama-Aneki Logo" width="600">
</p>
<p align="center">
  <b>A beautiful terminal UI for Ollama with emotion visualization and custom model management</b><br>
  <i>Transform your CLI into a visually appealing, feature-rich tool for interacting with Ollama models</i>
</p>
<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#configuration">Configuration</a> •
  <a href="#customization">Customization</a> •
  <a href="#contributing">Contributing</a>
</p>
## Features

### 🔄 Enhanced Chat Management

* **History View:** Easily browse through past conversations and pick up where you left off
* **Continue Chats:** Seamlessly continue conversations without losing context
* **Automatic Saving:** Conversations are stored in JSON format for easy recall

https://github.com/user-attachments/assets/b1120195-777a-45ba-9373-2b0a213c64cb

### 😊 Emotion Generation Mode

* **Visual Emotions:** Analyzes the emotional tone of responses and displays corresponding high-resolution PNGs
* **Rich Expression Library:** Choose from 38 predefined emotion expressions:
  * afraid, anger, annoyed, blush, catty, coffee, confused, crying, curious, default, demon, disapproval, disgust, dizzy, embarrassed, evil, excited, happy, heart, joy, laughing, love, music, naughty, pain, peaceful, pleased, proud, sad, scared, shocked, shy, sleepy, smug, surprised, sweat, thinking, wink
* **Rich Terminal Display:** PNGs render beautifully in supported terminals

https://github.com/user-attachments/assets/4a601fdd-a863-4bb1-9298-485fce102e4b

### 🤖 Custom Model Building

* **Create Personal Models:** Build custom models based on existing ones
* **Personalized Behavior:** Define unique system prompts for your models
* **Memory Management:** Add personalized information to your model's memory
* **No Duplication:** Uses the base model efficiently without duplicating storage

https://github.com/user-attachments/assets/23e13371-f03b-4eee-bce9-bb9c4db6298d

### ⚙️ Fully Configurable

* **Rich Terminal UI:** Beautiful tables, colors, and borders that work in most modern terminals
* **ASCII Art:** Custom banners and art with random or fixed display options
* **Appearance Settings:** Customize colors, borders, and layout to your preferences
* **Behavior Control:** Fine-tune how conversations are handled and saved

## Installation

### Prerequisites

* **Python:** Python 3.6 or higher
* **Ollama:** Must be installed and configured on your system

### Linux Installation

```bash
# Clone the repository
git clone https://github.com/MeghTarwadi/ollama-aneki.git

# Navigate to the directory
cd ollama-aneki

# Run the setup script
chmod +x setup.sh
./setup.sh
```

The setup script will:

1. Create a virtual environment for dependencies
2. Install required Python packages
3. Set up necessary directories and configuration files
4. Create a system-wide executable command (`aneki`)

After installation, you can run the `aneki` command from anywhere in your terminal!

### Windows Installation

```powershell
# Install Git if not already installed (using winget)
winget install Git.Git

# Close and reopen terminal, then run:
git clone https://github.com/MeghTarwadi/ollama-aneki.git C:\temp\ollama-aneki

# Navigate to the directory
cd C:\temp\ollama-aneki

# Run the setup script
.\setup.bat
```

After installation:

1. Restart your terminal/command prompt
2. You can run `aneki` from anywhere in your command prompt or PowerShell

## Usage

### Basic Commands

* `aneki` - Launch the main interface
* `aneki run [model_name]` - Run a specific model
* `aneki new` - Create a new custom model
* `aneki history` - View past model configurations
* `aneki help` - Display help information
* `aneki asciiart` - Merge ASCII arts for custom display
* `aneki pixelize` - Change emotional model files

### Creating a Custom Model

1. Run `aneki new`
2. Enter base model name (e.g., `phi3.5`)
3. Choose a name for your custom model
4. Set behavior instructions for your model
5. Optionally add information to your model's memory

### Chat Management

* Inside a conversation, type your exit code (default: `die`) to quit
* Use `aneki run read` to view past conversations
* Use `aneki run cont` to continue a previous conversation

### Quitting Properly

* To exit a conversation: type your exit code (default: `die`)
* To interrupt the program: press `Ctrl+C` - this will safely exit and return you to your original directory

## Configuration

The configuration file is located at `saves/default/config.conf`. Here are some key settings:

```ini
# Appearance settings
alert = [red]                # Color for alerts
asciiart = [yellow]          # Color for ASCII art  
normal = [white]             # Default text color
highlight = [blue]           # Color for highlighted text
box_borders = DOUBLE         # Box style: DOUBLE, HEAVY, SIMPLE, ROUNDED, SQUARE
box_width = 0                # Terminal width (0 = auto)

# Behavior settings
auto_clear = 1               # Clear terminal automatically (1 = yes, 0 = no)
emotion_generation = 1       # Enable emotion visualization (1 = yes, 0 = no)
exit_code = die              # Command to exit conversation
memory_length = 10           # Number of messages to keep in memory

# Content settings
pngfolder = Aneki            # Emotion style ("Aneki", "Makima", "Makima white background")
custom_path = saves/custom   # Custom data storage location
width = 40                   # Width for pixel art emotions
height = 30                  # Height for pixel art emotions
```

## Customization

### Adding Custom Emotions

Place your PNG files in the `saves/custom/exp/` directory with the emotion name as filename (e.g., `happy.png`).

### Creating Custom ASCII Art

1. Edit the ASCII art files in `saves/default/ascii1.txt` or `saves/default/ascii2.txt`
2. Run `aneki asciiart` to merge the arts
3. Your custom art will appear in the banner

## Uninstallation

### Linux Uninstallation

```bash
# Remove the executable
sudo rm /usr/local/bin/aneki

# Remove the installation directory
rm -rf ~/.local/share/ollama-aneki
```

### Windows Uninstallation

```powershell
# Remove the installation directory
Remove-Item -Recurse -Force "$env:USERPROFILE\AppData\Local\ollama-aneki"

# Remove Start Menu shortcut
Remove-Item "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Ollama-Aneki.lnk"

# You may need to manually remove the directory from PATH
```

## Contributing

We welcome contributions to improve Ollama-Aneki! Feel free to:

* Report issues
* Suggest new features
* Create pull requests
* Share your custom configurations and ASCII art

## License

This project is licensed under the MIT License.

---

**Experience the beauty of simplicity with Ollama-Aneki. Elevate your CLI game today!**
