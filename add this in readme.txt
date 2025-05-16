winget install Git.Git


close terminal than run this

cd C:\
mkdir Ollama-Aneki -ErrorAction SilentlyContinue

git clone https://github.com/MeghTarwadi/Ollama-Aneki C:\Ollama-Aneki
setx PATH "%PATH%;C:\Ollama-Aneki"

echo "Ollama-Aneki installed and environment variable set successfully!"

pip install -r requirements.txt
