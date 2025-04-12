# Edge Bulk TTS Application

A simple application that uses Microsoft Edge's Text-to-Speech (TTS) service to generate audio from text with multiple voices.

## Features

- Convert text to speech using Microsoft Edge TTS voices
- Over 400 voices across multiple languages
- Bulk generation of multiple text entries
- Search for voices by name, language, or gender
- Create and save voice presets
- Adjust speech rate and volume
- Download generated audio files

## Installation and Usage

### Windows Users

1. Make sure you have Python installed (version 3.6 or newer)
   - Download from https://www.python.org/downloads/
   - **Important**: Check "Add Python to PATH" during installation

2. Download and extract the application files to a folder

3. Run the application by double-clicking the `run.bat` file
   - The script will automatically:
     - Create a virtual environment
     - Install required dependencies
     - Start the application

4. The application will open in your web browser (typically at http://localhost:8501)

### Mac/Linux Users

1. Make sure you have Python installed (version 3.6 or newer)

2. Open Terminal and navigate to the application folder:
   ```
   cd /path/to/extracted/folder
   ```

3. Run the application by executing:
   ```
   chmod +x "Run Edge Bulk.command"
   ./Run\ Edge\ Bulk.command
   ```

## Using the Application

1. **Add Text Entries**: Click "Add Text Entry" to create new text entries
2. **Enter Text**: Type or paste the text you want to convert to speech
3. **Select Voice**: Choose a voice for each text entry
4. **Generate Audio**: Click the "Generate" button for each entry or "Generate All" for bulk processing
5. **Download**: After generation, download buttons will appear for each audio file

## Voice Selection Tools

- **Search voices**: Filter by name, language, or gender
- **Bulk change**: Change all entries to use a specific language/voice
- **Voice presets**: Save and apply combinations of voices

## Troubleshooting

- **Python not found**: Ensure Python is installed and added to PATH
- **Installation errors**: Try running the script as administrator
- **Application crashes**: Check your internet connection (required for voice retrieval)

## Requirements

- Python 3.6 or newer
- Internet connection (for accessing Edge TTS voices)
- Modern web browser

## Credits

This application uses:
- Streamlit for the web interface
- edge-tts for text-to-speech functionality
- Microsoft Edge TTS voices 