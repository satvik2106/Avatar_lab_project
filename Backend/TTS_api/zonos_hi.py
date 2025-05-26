# zonos_hindi_tts.py

from TTS.api import TTS

# Load the Zonos TTS model (replace with correct model path or ID if needed)
model = TTS(model_name="Zyphra/Zonos", progress_bar=True)

# List available speakers and languages
print("Available speakers:\n", model.speakers)
print("Available languages:\n", model.languages)

# Your Hindi text input
hindi_text = "नमस्ते, आप कैसे हैं?"

# Inference
model.tts_to_file(
    text=hindi_text,
    speaker="hin_speaker",  # Replace with actual Hindi speaker name from model.speakers
    language="hin",         # Replace with actual code if needed
    file_path="output_hindi.wav"
)
