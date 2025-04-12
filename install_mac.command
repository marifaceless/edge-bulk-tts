#!/bin/bash

echo "==============================================="
echo "Edge Bulk TTS - Easy Installer"
echo "==============================================="

# Change to the directory where the script is located
cd "$(dirname "$0")"

echo "Checking for Python..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python is not installed"
    echo "Please install Python from https://www.python.org/downloads/"
    open https://www.python.org/downloads/
    echo "Press any key to exit..."
    read -n 1
    exit 1
fi
echo "[OK] Python is installed"

echo "Setting up virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to create virtual environment"
    echo "Press any key to exit..."
    read -n 1
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing required packages..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install requirements"
    echo "Press any key to exit..."
    read -n 1
    exit 1
fi
echo "[OK] All packages installed"

echo ""
echo "==============================================="
echo "Installation complete! Starting the app..."
echo "==============================================="
echo ""
echo "The app will open in your web browser shortly."
echo "If it doesn't open automatically, go to: http://localhost:8501"
echo ""

python3 -m streamlit run edge_bulk.py

echo ""
echo "Application has been closed."
echo "Press any key to exit..."
read -n 1 