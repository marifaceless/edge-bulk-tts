#!/bin/bash

echo "==============================================="
echo "Edge Bulk TTS - Easy Installer"
echo "==============================================="

# Change to the directory where the script is located
cd "$(dirname "$0")"

# Check if we're on a Mac
if [ "$(uname)" != "Darwin" ]; then
    echo "[ERROR] This script is for Mac OS only."
    echo "Please use install_windows.bat on Windows."
    echo "Press any key to exit..."
    read -n 1
    exit 1
fi

# Check for Python installation
echo "Checking for Python..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python is not installed on your Mac"
    echo "Would you like to open the Python download page? (y/n)"
    read -n 1 answer
    if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
        open https://www.python.org/downloads/
        echo "Please install Python and run this script again."
    else
        echo "You'll need to install Python before continuing."
        echo "Download Python from: https://www.python.org/downloads/"
    fi
    echo "Press any key to exit..."
    read -n 1
    exit 1
fi

# Get Python version
python_version=$(python3 --version)
echo "[OK] Found $python_version"

# Create output directory if needed
if [ ! -d "output" ]; then
    mkdir output
fi

# Check if we have write permissions
if ! touch .write_test &> /dev/null; then
    echo "[ERROR] No write permission in this folder"
    echo "Please extract the zip file to a location where you have write access,"
    echo "such as your Documents or Desktop folder."
    echo "Press any key to exit..."
    read -n 1
    exit 1
else
    rm .write_test
fi

# Create requirements.txt if it doesn't exist or is empty
if [ ! -f "requirements.txt" ] || [ ! -s "requirements.txt" ]; then
    echo "Creating requirements.txt..."
    echo "streamlit==1.43.2" > requirements.txt
    echo "edge-tts==6.1.9" >> requirements.txt
    echo "[OK] Created requirements.txt"
fi

echo "Setting up virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to create virtual environment"
    echo "This might be due to Python version or permissions issues."
    echo "Try installing Python 3.9 or newer if you haven't already."
    echo "Press any key to exit..."
    read -n 1
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate virtual environment"
    echo "Press any key to exit..."
    read -n 1
    exit 1
fi
echo "[OK] Virtual environment activated"

echo "Installing required packages..."
echo "This may take a minute or two..."

# Install specific packages with explicit versions
echo "Installing Streamlit..."
pip install streamlit==1.43.2
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install Streamlit"
    echo "This might be due to internet connection issues."
    echo "Press any key to exit..."
    read -n 1
    exit 1
fi

echo "Installing edge-tts..."
pip install edge-tts==6.1.9
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install edge-tts"
    echo "This might be due to internet connection issues."
    echo "Press any key to exit..."
    read -n 1
    exit 1
fi

# Also install from requirements.txt as a backup
pip install -r requirements.txt
echo "[OK] All packages installed"

# Verify that edge-tts is installed
if ! python3 -c "import edge_tts" &> /dev/null; then
    echo "[WARNING] edge-tts package doesn't seem to be installed correctly."
    echo "Installing edge-tts again with pip directly..."
    pip install edge-tts==6.1.9
    
    # Check again
    if ! python3 -c "import edge_tts" &> /dev/null; then
        echo "[ERROR] Still cannot import edge-tts. Please try manually:"
        echo "1. In Terminal: source venv/bin/activate"
        echo "2. Then run: pip install edge-tts==6.1.9"
        echo "Press any key to exit..."
        read -n 1
        exit 1
    fi
fi

echo ""
echo "==============================================="
echo "Installation complete! Starting the app..."
echo "==============================================="
echo ""
echo "The app will open in your web browser shortly."
echo "If it doesn't open automatically, go to: http://localhost:8501"
echo ""
echo "You can close this window at any time to stop the app."
echo ""

# Run Streamlit with more explicit options
python3 -m streamlit run edge_bulk.py --server.headless=false --browser.serverAddress=localhost

# If we get here, either the app was closed or there was an error
echo ""
if [ $? -ne 0 ]; then
    echo "[ERROR] The application has exited with an error."
else
    echo "The application has been closed."
fi

echo "Press any key to exit..."
read -n 1 
