# Edge Bulk TTS

A powerful text-to-speech application using Microsoft Edge voices with a beautiful, easy-to-use interface.

## 📥 Download & Installation

### Option 1: Use Online (No Installation)
👉 **[CLICK HERE TO USE THE APP ONLINE](https://marifaceless-edge-bulk-tts-z44cejclbqsxsktptwjhrt.streamlit.app)** - No installation required!

### Option 2: Install on Your Computer

#### Step 1: Download the Files
👉 **[CLICK HERE TO DOWNLOAD ZIP](https://github.com/marifaceless/edge-bulk-tts/archive/refs/heads/main.zip)**

#### Step 2: Install & Run

**Windows Users:**
1. Extract the downloaded ZIP file
2. Double-click `install_windows.bat`
3. The app will install and start automatically

**Mac Users (Detailed Instructions):**

> **First Time Setup** (Only needed once)

1. **Download & Extract**
   - After downloading, find the ZIP file in your Downloads folder
   - Double-click to extract it
   - Open the extracted folder

2. **Make the installer executable** (this is required for security reasons)
   - Press Command+Space to open Spotlight
   - Type "Terminal" and press Enter
   - When Terminal opens, type exactly: `chmod +x ` (including the space at the end)
   - Find the extracted folder in Finder
   - Drag the file named `install_mac.command` from Finder into the Terminal window
   - Your Terminal should now show something like: `chmod +x /Users/yourname/Downloads/edge-bulk-tts-main/install_mac.command`
   - Press Enter

3. **Allow the app in Security Settings** (required on macOS)
   - Try to double-click the `install_mac.command` file - you'll likely get a security warning
   - Go to Apple menu (top left) → System Settings/Preferences → Security & Privacy → General
   - Look for a message about "install_mac.command" being blocked
   - Click "Open Anyway" or "Allow" (you may need to click the lock icon and enter your password first)
   - Go back to Finder and double-click the file again
   - If prompted again, click "Open"

4. **If you still get an error about edge_tts**
   - Open Terminal
   - Navigate to the folder: `cd /path/to/edge-bulk-tts-main` (or drag the folder into Terminal)
   - Run: `source venv/bin/activate`
   - Run: `pip install edge-tts==6.1.9`
   - Then run: `streamlit run edge_bulk.py`

> **Future Use** (After first-time setup)
>
> Just double-click the `install_mac.command` file whenever you want to use the app again!

## ✨ Features

- Convert text to speech using 400+ Microsoft Edge voices
- Generate multiple audio files at once
- Adjust speech rate and volume
- Easy-to-use interface
- Download individual files or all as ZIP

## 🎮 How to Use

1. Add text entries using the "Add New Text Entry" button
2. Enter your text in each text area
3. Select a voice for each entry 
4. Click "Generate" or "Generate All Pending"
5. Download individual files or all files as a ZIP

## ❓ Troubleshooting

### Windows Issues:
- **Python not found**: Install Python from [python.org](https://www.python.org/downloads/) (check "Add to PATH")
- **Installation errors**: Try running the script as administrator
- **App won't start**: Check that you have internet access for voice retrieval

### Mac Issues:
- **"Cannot be opened"**: Follow step 3 in the Mac installation instructions to allow it in Security settings
- **"Permission denied"**: Follow the detailed steps above for making the file executable
- **"No module named edge_tts"**: Follow step 4 in Mac installation instructions to install it manually
- **Python not found**: Install Python from [python.org](https://www.python.org/downloads/)
- **Terminal says "Operation not permitted"**: Go to System Preferences → Security & Privacy → Privacy → Full Disk Access → add Terminal

## 💻 System Requirements

- Python 3.6 or newer
- Internet connection (for accessing Edge TTS voices)
- Any modern web browser

## 🙏 Credits

This application uses:
- Streamlit for the web interface
- edge-tts for text-to-speech functionality
- Microsoft Edge TTS voices 
