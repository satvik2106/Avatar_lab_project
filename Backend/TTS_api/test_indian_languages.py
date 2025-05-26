import os
import torchaudio
import uuid
from zonos.model import Zonos
from zonos.conditioning import make_cond_dict
from zonos.utils import DEFAULT_DEVICE as device

OUTPUT_FOLDER = 'outputs'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load the pretrained Zonos model
model = Zonos.from_pretrained("Zyphra/Zonos-v0.1-transformer", device=device)

def generate_speech(text: str, speaker_audio_path: str, language: str, output_folder: str = OUTPUT_FOLDER):
    try:
        print(f"[INFO] Loading speaker audio from: {speaker_audio_path}")
        wav, sampling_rate = torchaudio.load(speaker_audio_path)
        speaker = model.make_speaker_embedding(wav, sampling_rate)

        cond_dict = make_cond_dict(text=text, speaker=speaker, language=language)
        conditioning = model.prepare_conditioning(cond_dict)

        codes = model.generate(conditioning)
        wavs = model.autoencoder.decode(codes).cpu()

        output_path = os.path.join(output_folder, f"{uuid.uuid4()}_{language}.wav")
        torchaudio.save(output_path, wavs[0], model.autoencoder.sampling_rate)

        print(f"[INFO] Generated speech saved to: {output_path}")
        return output_path

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return None

if __name__ == "__main__":
    # Example speaker audio path - replace with your own speaker audio file path
    speaker_audio_path = r"C:\Users\Satvik Vattipalli\OneDrive\Desktop\Avatar _lab_full\Frontend\public\assets\demo1_audio.wav"

    # Example texts in various Indian languages
    test_cases = {
        "hi": "नमस्ते, यह एक परीक्षण है।",
        "ta": "வணக்கம், இது ஒரு சோதனை.",
        "te": "హలో, ఇది ఒక పరీక్ష.",
        "bn": "হ্যালো, এটি একটি পরীক্ষা।",
        "mr": "नमस्कार, हा एक चाचणी आहे.",
        "ml": "ഹലോ, ഇത് ഒരു പരീക്ഷയാണ്.",
        "pa": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ, ਇਹ ਇੱਕ ਟੈਸਟ ਹੈ।",
        "gu": "હેલો, આ એક પરીક્ષણ છે.",
        "kn": "ಹಲೋ, ಇದು ಒಂದು ಪರೀಕ್ಷೆ.",
        "or": "ନମସ୍କାର, ଏହା ଏକ ପରୀକ୍ଷା।"
    }

    for lang_code, text in test_cases.items():
        print(f"Generating speech for language: {lang_code}")
        output_file = generate_speech(text, speaker_audio_path, lang_code)
        if output_file:
            print(f"Output saved to: {output_file}")
        else:
            print(f"Failed to generate speech for language: {lang_code}")
