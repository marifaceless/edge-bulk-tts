# Edge Bulk TTS

A powerful text-to-speech application using Microsoft Edge voices with a beautiful, easy-to-use interface.

## Quick Installation

### Windows Users
1. [Download the ZIP](https://github.com/marifaceless/edge-bulk-tts/archive/refs/heads/main.zip)
2. Extract the files to a folder
3. Double-click `install_windows.bat`
4. The app will install dependencies and start automatically

### Mac Users
1. [Download the ZIP](https://github.com/marifaceless/edge-bulk-tts/archive/refs/heads/main.zip)
2. Extract the files to a folder
3. Open Terminal and run:
   ```
   chmod +x /path/to/install_mac.command
   ```
   (Replace "/path/to/" with the actual path, or drag the file into Terminal after typing "chmod +x ")
4. Double-click `install_mac.command` to install and run

## Cloud Version

Don't want to install anything? Use our cloud version:
[Edge Bulk TTS Cloud](https://marifaceless-edge-bulk-tts-z44cejclbqsxsktptwjhrt.streamlit.app)

## Features

- Convert text to speech using 400+ Microsoft Edge voices
- Generate multiple audio files at once
- Adjust speech rate and volume
- Easy-to-use interface
- Download individual files or all as ZIP

## How to Use

1. Add text entries using the "Add New Text Entry" button
2. Enter your text in each text area
3. Select a voice for each entry 
4. Click "Generate" or "Generate All Pending"
5. Download individual files or all files as a ZIP

## Troubleshooting

### Windows Issues:
- **Python not found**: Install Python from [python.org](https://www.python.org/downloads/)
- **Installation errors**: Try running the script as administrator
- **App won't start**: Check that you have internet access for voice retrieval

### Mac Issues:
- **"Cannot be opened"**: Right-click the .command file → Open → Open
- **"Permission denied"**: Run `chmod +x install_mac.command` in Terminal
- **Python not found**: Install Python from [python.org](https://www.python.org/downloads/)

## System Requirements

- Python 3.6 or newer
- Internet connection (for accessing Edge TTS voices)
- Any modern web browser

## Credits

This application uses:
- Streamlit for the web interface
- edge-tts for text-to-speech functionality
- Microsoft Edge TTS voices 