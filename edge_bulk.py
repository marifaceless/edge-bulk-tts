import streamlit as st
import asyncio
import edge_tts
import os
import time
import uuid
import io
import zipfile
from typing import Dict, List

# Set page config for better appearance
st.set_page_config(
    page_title="Edge TTS Audio Generator",
    page_icon="🔊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better UI
CUSTOM_CSS = """
<style>
/* Improve overall appearance */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Improve button appearance */
.stButton button {
    width: 100%;
    border-radius: 5px;
    height: 2.5rem;
}

/* Add some color to the headers */
h1, h2, h3 {
    color: #1E88E5;
}

/* Hide the top-right status widget spinner */
.block-container div[data-testid="stStatusWidget"] {
    display: none !important;
}

/* Improve spacing */
.stTextArea textarea {
    font-size: 1rem;
}

/* Style dividers */
hr {
    margin-top: 2rem;
    margin-bottom: 2rem;
}

/* Style download buttons */
.stDownloadButton button {
    background-color: #4CAF50;
    color: white;
}

/* Add some margin to audio players */
.stAudio audio {
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
    width: 100%;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Output directory configuration
OUTPUTS_DIR = "outputs"

# Ensure outputs directory exists
os.makedirs(OUTPUTS_DIR, exist_ok=True)

def generate_audio(text, output_file, voice, rate="+0%", volume="+0%"):
    """Generate TTS audio (synchronous call)."""
    async def _generate():
        communicate = edge_tts.Communicate(text, voice=voice, rate=rate, volume=volume)
        await communicate.save(output_file)
    asyncio.run(_generate())

async def get_voices():
    """Fetch and return all available voices."""
    voices_manager = await edge_tts.VoicesManager.create()
    return voices_manager.voices

def group_voices_by_locale(voices: List[Dict]) -> Dict[str, List[Dict]]:
    """Group voices by locale/language."""
    grouped: Dict[str, List[Dict]] = {}
    for voice in voices:
        locale = voice["Locale"]
        if locale not in grouped:
            grouped[locale] = []
        grouped[locale].append(voice)
    return grouped

def create_zip_file(files_data):
    """Create a zip file in memory containing all audio files."""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for filename, data in files_data.items():
            zip_file.writestr(filename, data)
    return zip_buffer.getvalue()

# App header with logo
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/7/7e/Microsoft_Edge_logo_%282019%29.png", width=80)
with col2:
    st.title("Edge TTS Audio Generator")
    st.write(
        "Enter your text below, choose a voice, and generate audio. "
        "You can add multiple entries and generate them all at once."
    )

# Display a nice info box with instructions
with st.expander("ℹ️ How to use this app", expanded=False):
    st.markdown("""
    ### Quick Start Guide
    1. **Add text entries** using the "Add New Text Entry" button
    2. **Enter your text** in each text area
    3. **Select a voice** for each entry
    4. **Generate audio** by clicking "Generate" or "Generate All Pending"
    5. **Download** individual files or all files as a ZIP
    
    ### Tips
    - Adjust rate and volume for all entries using the controls below
    - You can preview audio directly in the browser before downloading
    - All generated files are saved automatically to the `/outputs` directory
    """)

# Cache voices in session state so we don't fetch them repeatedly
if "voices" not in st.session_state:
    with st.spinner("Loading voices... Please wait."):
        st.session_state["voices"] = asyncio.run(get_voices())
all_voices = st.session_state["voices"]
voice_names = [v["ShortName"] for v in all_voices]

# Group voices by locale
grouped_voices = group_voices_by_locale(all_voices)

# Initialize session state for text entries if not exists
if "text_entries" not in st.session_state:
    st.session_state["text_entries"] = []
    
# Add an entry ID counter to ensure unique keys
if "entry_counter" not in st.session_state:
    st.session_state["entry_counter"] = 0

# Simplified Voice Selection Tools - just a single dropdown to change all voices
st.header("Voice Selection")

# Simplified voice selection with a single dropdown for all voices
selected_voice = st.selectbox(
    "🔊 Select voice for all entries",
    options=voice_names,
    format_func=lambda x: f"{x} ({next((v['Locale'] + ', ' + v['Gender']) for v in all_voices if v['ShortName'] == x)})"
)

if st.button("Apply to all entries", type="primary"):
    for entry in st.session_state["text_entries"]:
        entry["voice"] = selected_voice
    st.success(f"Updated all entries to use {selected_voice}")

# Rate & Volume controls
st.subheader("Speech Settings")
col1, col2 = st.columns(2)
with col1:
    rate = st.text_input("🏃‍♂️ Speech Rate (e.g. +0%, +10%, -10%)", "+0%")
with col2:
    volume = st.text_input("🔉 Volume (e.g. +0%, +10%, -10%)", "+0%")

# Function to add a new text entry
def add_text_entry():
    entry_id = st.session_state["entry_counter"]
    st.session_state["entry_counter"] += 1
    
    # Default voice
    default_voice = "en-US-SteffanNeural"
    if default_voice in voice_names:
        default_index = voice_names.index(default_voice)
    else:
        default_index = 0
        
    st.session_state["text_entries"].append({
        "id": entry_id,
        "text": "",
        "voice": voice_names[default_index],
        "generated": False,
        "output_file": None,
        "audio_bytes": None
    })

# Function to remove a text entry
def remove_text_entry(entry_id):
    st.session_state["text_entries"] = [
        entry for entry in st.session_state["text_entries"] 
        if entry["id"] != entry_id
    ]

# Function to update text for an entry
def update_text(entry_id, text):
    for entry in st.session_state["text_entries"]:
        if entry["id"] == entry_id:
            entry["text"] = text
            # Reset generated flag when text changes
            entry["generated"] = False
            entry["output_file"] = None
            entry["audio_bytes"] = None
            break

# Function to update voice for an entry
def update_voice(entry_id, voice):
    for entry in st.session_state["text_entries"]:
        if entry["id"] == entry_id:
            entry["voice"] = voice
            # Reset generated flag when voice changes
            entry["generated"] = False
            entry["output_file"] = None
            entry["audio_bytes"] = None
            break

# Function to generate audio for a single entry
def generate_single_audio(entry_id):
    for entry in st.session_state["text_entries"]:
        if entry["id"] == entry_id and not entry["generated"]:
            # Get filename-safe text (first 20 chars)
            safe_text = "".join([c if c.isalnum() else "_" for c in entry["text"][:20]])
            
            # Create a unique filename
            filename = f"{safe_text}_{entry_id}_{uuid.uuid4().hex[:8]}.mp3"
            output_file = os.path.join(OUTPUTS_DIR, filename)
            
            try:
                # Generate the audio
                generate_audio(entry["text"], output_file, entry["voice"], rate, volume)
                
                # Read the generated file for in-browser playback
                with open(output_file, "rb") as f:
                    audio_bytes = f.read()
                
                entry["generated"] = True
                entry["output_file"] = filename
                entry["audio_bytes"] = audio_bytes
                
                st.success(f"Audio saved to {output_file}")
            except Exception as e:
                st.error(f"Error generating audio: {e}")
            break

# Function to generate all pending audio files and update UI
def generate_all_pending():
    pending_entries = [e for e in st.session_state["text_entries"] if not e["generated"]]
    total_pending = len(pending_entries)
    
    if total_pending == 0:
        st.info("No pending entries to generate.")
        return
    
    # Create a placeholder for the progress bar
    st.subheader("Generating all pending entries...")
    progress_bar = st.progress(0)
    
    generated_files = []
    
    # Bulk generation process
    for i, entry in enumerate(pending_entries):
        # Display current progress
        progress_text = st.empty()
        progress_text.text(f"Generating entry #{st.session_state['text_entries'].index(entry)+1}...")
        
        # Get filename-safe text (first 20 chars)
        safe_text = "".join([c if c.isalnum() else "_" for c in entry["text"][:20]])
        
        # Create a unique filename
        filename = f"{safe_text}_{entry['id']}_{uuid.uuid4().hex[:8]}.mp3"
        output_file = os.path.join(OUTPUTS_DIR, filename)
        
        try:
            # Generate the audio
            generate_audio(entry["text"], output_file, entry["voice"], rate, volume)
            
            # Read the generated file for in-browser playback
            with open(output_file, "rb") as f:
                audio_bytes = f.read()
            
            entry["generated"] = True
            entry["output_file"] = filename
            entry["audio_bytes"] = audio_bytes
            
            generated_files.append(output_file)
            
            # Update progress bar
            progress_bar.progress((i + 1) / total_pending)
            
        except Exception as e:
            st.error(f"Error generating audio for entry #{st.session_state['text_entries'].index(entry)+1}: {e}")
    
    st.success(f"All audio generated successfully! Files saved to {OUTPUTS_DIR}/")
    
    # Display the list of generated files
    if generated_files:
        with st.expander("Generated Files"):
            for file in generated_files:
                st.text(file)
    
    # Show a message to indicate generation has completed
    st.subheader("⬇️ All files generated - scroll down to download ⬇️")
    
    # Display the download section immediately
    display_download_section()

# Function to display the download section
def display_download_section():
    generated_entries = [e for e in st.session_state["text_entries"] if e["generated"] and e["audio_bytes"]]
    
    if not generated_entries:
        return
    
    st.header("Download All Generated Audio")
    
    # Create a dictionary of filenames and audio data
    audio_files = {e["output_file"]: e["audio_bytes"] for e in generated_entries}
    
    # Create a zip file
    zip_data = create_zip_file(audio_files)
    
    # Display download button for the zip
    st.download_button(
        label=f"📦 Download All ({len(generated_entries)}) Audio Files as ZIP",
        data=zip_data,
        file_name=f"edge_tts_audio_{time.strftime('%Y%m%d_%H%M%S')}.zip",
        mime="application/zip",
        use_container_width=True
    )
    
    # Show a summary of what's in the zip
    with st.expander("Details of included files"):
        for i, entry in enumerate(generated_entries):
            voice_info = next((v for v in all_voices if v["ShortName"] == entry["voice"]), None)
            locale = voice_info["Locale"] if voice_info else "Unknown"
            gender = voice_info["Gender"] if voice_info else "Unknown"
            
            st.markdown(f"**File {i+1}**: {entry['output_file']}")
            st.markdown(f"- **Voice**: {entry['voice']} ({locale}, {gender})")
            st.markdown(f"- **Text**: {entry['text'][:100]}..." if len(entry['text']) > 100 else f"- **Text**: {entry['text']}")
            st.markdown(f"- **Saved to**: `{os.path.join(OUTPUTS_DIR, entry['output_file'])}`")
            st.markdown("---")

# Control buttons
st.header("Text Entries")
col1, col2 = st.columns([1, 3])
with col1:
    if st.button("➕ Add New Text Entry", use_container_width=True):
        add_text_entry()

with col2:
    if st.button("🔄 Generate All Pending", type="primary", use_container_width=True):
        generate_all_pending()
            
# If there are no entries yet, add one automatically
if not st.session_state["text_entries"]:
    add_text_entry()

# Display all text entries
for i, entry in enumerate(st.session_state["text_entries"]):
    with st.container():
        st.subheader(f"Text Entry #{i+1}")
        
        # Text area for input with better layout
        text_col, voice_col = st.columns([3, 1])
        
        with text_col:
            text_value = st.text_area(
                "Enter your text", 
                value=entry["text"],
                key=f"text_{entry['id']}",
                height=150
            )
            update_text(entry["id"], text_value)
        
        with voice_col:
            # Voice selection
            default_voice = "en-US-SteffanNeural"
            if default_voice in voice_names:
                default_index = voice_names.index(default_voice)
            else:
                default_index = 0
                
            selected_voice_index = voice_names.index(entry["voice"]) if entry["voice"] in voice_names else default_index
            
            selected_voice = st.selectbox(
                "Select voice",
                voice_names,
                index=selected_voice_index,
                key=f"voice_{entry['id']}"
            )
            update_voice(entry["id"], selected_voice)
            
            # Generate button for this entry
            button_col1, button_col2 = st.columns([1, 1])
            with button_col1:
                if st.button("🔊 Generate", key=f"gen_{entry['id']}", use_container_width=True):
                    with st.spinner("Generating..."):
                        generate_single_audio(entry["id"])
            
            with button_col2:
                if st.button("🗑️ Remove", key=f"remove_{entry['id']}", use_container_width=True):
                    remove_text_entry(entry["id"])
                    st.rerun()
        
        # Display audio player if generated
        if entry["generated"] and entry["audio_bytes"]:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.audio(entry["audio_bytes"], format="audio/mp3")
            with col2:
                st.download_button(
                    label="💾 Download MP3",
                    data=entry["audio_bytes"],
                    file_name=entry["output_file"],
                    mime="audio/mp3",
                    use_container_width=True
                )
                st.markdown(f"📁 Saved to: `{os.path.join(OUTPUTS_DIR, entry['output_file'])}`")
        
        st.divider()

# Display download section at the bottom of the page
display_download_section()

# Footer
st.markdown("---")
st.markdown("Powered by Microsoft Edge TTS and Streamlit. Created with ❤️")
