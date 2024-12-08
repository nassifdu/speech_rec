import os
import tempfile
import threading
import queue
import time
import sounddevice as sd
import numpy as np
import soundfile as sf
import keyboard
from pynput.keyboard import Controller
from groq import Groq
from pystray import Icon, MenuItem, Menu
from PIL import Image

# Initialize the Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

languages = {
    "en": "English",
    "zh": "Chinese",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "ja": "Japanese",
    "ru": "Russian",
    "pt": "Portuguese",
    "ar": "Arabic",
    "hi": "Hindi",
    "ko": "Korean",
    "it": "Italian",
    "tr": "Turkish",
    "vi": "Vietnamese",
    "pl": "Polish",
    "uk": "Ukrainian",
    "ms": "Malay",
    "th": "Thai",
    "nl": "Dutch",
    "id": "Indonesian"
}

current_code = "en"

# Initialize the keyboard controller
keyboard_controller = Controller()

# Queue to hold recorded audio data
audio_queue = queue.Queue()

# Global flags and variables
is_recording = False
temp_audio_file = None

# Function to load the tray icon
def load_custom_icon():
    # Load the icon.png from the current directory
    return Image.open(os.path.join(os.path.dirname(__file__), "icon.png"))

def load_recording_icon():
    # Load the rec_icon.png from the current directory
    return Image.open(os.path.join(os.path.dirname(__file__), "rec_icon.png"))

# Function to start recording audio
def start_recording(samplerate=16000, channels=1):
    global is_recording, temp_audio_file
    is_recording = True
    temp_audio_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    icon.icon = load_recording_icon()  # Update the icon to recording state
    try:
        def callback(indata, frames, time, status):
            if status:
                print(status)
            audio_queue.put(indata.copy())
        
        # Open file for writing
        with sf.SoundFile(temp_audio_file.name, mode='w', samplerate=samplerate, channels=channels) as file:
            with sd.InputStream(samplerate=samplerate, channels=channels, callback=callback):
                print("Recording started...")
                while is_recording:
                    file.write(audio_queue.get())
    except Exception as e:
        print(f"Error during recording: {e}")
    finally:
        print("Recording finished.")
        icon.icon = load_custom_icon()  # Revert to the default icon after recording

# Updated stop recording function to revert the icon
def stop_recording():
    global is_recording
    is_recording = False

# Function to transcribe audio using Groq's Whisper V3 Turbo model
def transcribe_audio(filename):
    try:
        with open(filename, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(filename, file.read()),
                model="whisper-large-v3",
                language=current_code  # Use the language code (e.g., "pt")
            )
        return transcription.text
    except Exception as e:
        print(f"Error during transcription: {e}")
        return ""

# Function to simulate typing the transcribed text
def type_text(text):
    for char in text:
        keyboard_controller.type(char)

def remove_leading_space(input_string):
    """Remove a leading space from the string if there is one."""
    return input_string[1:] if input_string.startswith(" ") else input_string

# Function to handle the hotkey event
def on_hotkey():
    global is_recording, temp_audio_file
    if not is_recording:
        threading.Thread(target=start_recording).start()
    else:
        stop_recording()
        time.sleep(1)  # Allow time for resources to release
        transcription = transcribe_audio(temp_audio_file.name)
        type_text(remove_leading_space(transcription))
        try:
            time.sleep(0.5)  # Brief delay before file deletion
            os.remove(temp_audio_file.name)
            print("Temporary file deleted.")
        except PermissionError:
            print(f"Failed to delete {temp_audio_file.name} due to a permission error.")
        except Exception as e:
            print(f"Error deleting file: {e}")

def change_language(code):
    global current_code
    current_code = code
    print(f"Language changed to: {languages[current_code]}")  # Use code to look up language
    refresh_menu()  # Refresh the menu to update checked states

# Function to quit the application
def quit_application(icon, item):
    print("Exiting...")
    icon.stop()

def create_language_action(code):
    def action(item):
        change_language(code)
    return action

def refresh_menu():
    global icon
    icon.menu = Menu(
        MenuItem("Quit", quit_application),
        MenuItem(
            "Languages",
            Menu(
                *[
                    MenuItem(
                        language,  # Display the language name
                        create_language_action(code),  # Use closure to bind the code
                        checked=lambda item, code=code: current_code == code  # Dynamically check the active language
                    ) for code, language in languages.items()
                ]
            )
        )
    )

icon = Icon(
    "Speech Recognition",
    load_custom_icon(),
    menu=Menu(
        MenuItem("Quit", quit_application),
        MenuItem(
            "Languages",
            Menu(
                *[
                    MenuItem(
                        language,  # Display the language name
                        create_language_action(code),  # Use the closure for proper binding
                        checked=lambda item, code=code: current_code == code  # Dynamically check active language
                    ) for code, language in languages.items()
                ]
            )
        )
    )
)

# Set up the hotkey listener in a thread
threading.Thread(target=lambda: keyboard.add_hotkey("win+enter", on_hotkey)).start()

# Run the tray icon in the main thread
icon.run()