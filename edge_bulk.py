import streamlit as st
import asyncio
import edge_tts
import os
import time
import uuid
from typing import Dict, List

# Optional: Hide the small default spinner in the top-right corner
HIDE_DEFAULT_SPINNER = """
<style>
/* Hide the top-right status widget spinner */
.block-container div[data-testid="stStatusWidget"] {
    display: none !important;
}
</style>
"""
st.markdown(HIDE_DEFAULT_SPINNER, unsafe_allow_html=True)

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

st.title("Edge TTS Audio Generator")
st.write(
    "Enter your text below, choose a voice, and generate audio. "
    "You can add multiple entries and generate them all at once."
)

# Cache voices in session state so we don't fetch them repeatedly
if "voices" not in st.session_state:
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

# Initialize voice presets if not exists
if "voice_presets" not in st.session_state:
    st.session_state["voice_presets"] = {}

# Voice search and bulk change section
st.subheader("Voice Selection Tools")

# Voice preset system
preset_col1, preset_col2 = st.columns([2, 1])
with preset_col1:
    preset_name = st.text_input("Preset Name", key="preset_name")
    selected_preset = st.selectbox(
        "Select Preset",
        options=["None"] + list(st.session_state["voice_presets"].keys()),
        key="selected_preset"
    )

with preset_col2:
    if st.button("Save Current as Preset") and preset_name:
        current_voices = [entry["voice"] for entry in st.session_state["text_entries"]]
        if current_voices:
            st.session_state["voice_presets"][preset_name] = current_voices
            st.success(f"Saved preset '{preset_name}' with {len(current_voices)} voices")

    if st.button("Apply Selected Preset") and selected_preset != "None":
        preset_voices = st.session_state["voice_presets"][selected_preset]
        for i, entry in enumerate(st.session_state["text_entries"]):
            if i < len(preset_voices):
                entry["voice"] = preset_voices[i]
        st.success(f"Applied preset '{selected_preset}' to entries")

col1, col2 = st.columns([1, 1])

with col1:
    # Search/filter voices
    search_term = st.text_input("Search voices (name/language/gender)", "").lower()
    filtered_voices = [
        v["ShortName"] for v in all_voices 
        if (search_term in v["ShortName"].lower() or 
            search_term in v["Locale"].lower() or
            search_term in v["Gender"].lower())
    ]
    if search_term:
        st.write(f"Found {len(filtered_voices)} matching voices:")
        for voice in filtered_voices:
            st.write(f"- {voice}")

with col2:
    # Bulk voice change
    selected_locale = st.selectbox(
        "Change all voices to language",
        options=sorted(grouped_voices.keys()),
        format_func=lambda x: f"{x} ({len(grouped_voices[x])} voices)"
    )
    
    if selected_locale:
        locale_voices = grouped_voices[selected_locale]
        selected_voice = st.selectbox(
            "Select voice",
            options=[v["ShortName"] for v in locale_voices],
            format_func=lambda x: f"{x} ({next(v['Gender'] for v in locale_voices if v['ShortName'] == x)})"
        )
        
        if st.button("Apply to all entries"):
            for entry in st.session_state["text_entries"]:
                entry["voice"] = selected_voice
            st.success(f"Updated all entries to use {selected_voice}")

# Rate & Volume controls
rate = st.text_input("Rate (e.g. +0%)", "+0%")
volume = st.text_input("Volume (e.g. +0%)", "+0%")

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
            # Create a unique filename
            output_file = f"audio_{entry_id}_{uuid.uuid4().hex[:8]}.mp3"
            try:
                generate_audio(entry["text"], output_file, entry["voice"], rate, volume)
                # Read the generated file
                with open(output_file, "rb") as f:
                    audio_bytes = f.read()
                
                entry["generated"] = True
                entry["output_file"] = output_file
                entry["audio_bytes"] = audio_bytes
            except Exception as e:
                st.error(f"Error generating audio: {e}")
            break

# Add a new text entry button
if st.button("Add New Text Entry"):
    add_text_entry()

# If there are no entries yet, add one automatically
if not st.session_state["text_entries"]:
    add_text_entry()

# Display all text entries
for i, entry in enumerate(st.session_state["text_entries"]):
    with st.container():
        st.subheader(f"Text Entry #{i+1}")
        
        # Text area for input
        text_value = st.text_area(
            "Enter your text", 
            value=entry["text"],
            key=f"text_{entry['id']}",
            height=150
        )
        update_text(entry["id"], text_value)
        
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
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Generate", key=f"gen_{entry['id']}"):
                with st.spinner(f"Generating audio for entry #{i+1}..."):
                    generate_single_audio(entry["id"])
        
        with col2:
            if st.button("Remove this entry", key=f"remove_{entry['id']}"):
                remove_text_entry(entry["id"])
                st.rerun()
        
        # Display audio player if generated
        if entry["generated"] and entry["audio_bytes"]:
            st.audio(entry["audio_bytes"], format="audio/mp3")
            st.download_button(
                label="Download MP3",
                data=entry["audio_bytes"],
                file_name=entry["output_file"],
                mime="audio/mp3"
            )
        
        st.divider()

# Generate All button
if st.button("Generate All Pending"):
    pending_entries = [e for e in st.session_state["text_entries"] if not e["generated"]]
    total_pending = len(pending_entries)
    
    if total_pending > 0:
        st.subheader("Generating all pending entries...")
        progress_bar = st.progress(0)
        
        for i, entry in enumerate(pending_entries):
            with st.spinner(f"Generating entry #{st.session_state['text_entries'].index(entry)+1}..."):
                generate_single_audio(entry["id"])
                progress_bar.progress(int((i + 1) / total_pending * 100))
        
        st.success("All audio generated successfully!")
    else:
        st.info("No pending entries to generate.")