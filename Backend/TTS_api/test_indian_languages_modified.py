import os
import torchaudio
import uuid
import torch._dynamo
from zonos.model import Zonos
from zonos.conditioning import make_cond_dict
from zonos.utils import DEFAULT_DEVICE as device

# Suppress TorchInductor errors and fallback to eager mode
torch._dynamo.config.suppress_errors = True

OUTPUT_FOLDER = 'outputs'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load the pretrained Zonos model
model = Zonos.from_pretrained("Zyphra/Zonos-v0.1-transformer", device=device)

def generate_speech(
    text: str,
    speaker_audio_path: str,
    language: str = "te",
    output_folder: str = OUTPUT_FOLDER,
    pitch_std: float = 25.0,
    speaking_rate: float = 12.0,
    emotion: list[float] = [0.5, 0.05, 0.05, 0.05, 0.05, 0.05, 0.4, 0.5],
):
    try:
        print(f"[INFO] Loading speaker audio from: {speaker_audio_path}")
        wav, sampling_rate = torchaudio.load(speaker_audio_path)
        speaker = model.make_speaker_embedding(wav, sampling_rate)

        cond_dict = make_cond_dict(
            text=text,
            speaker=speaker,
            language=language,
            pitch_std=pitch_std,
            speaking_rate=speaking_rate,
            emotion=emotion,
        )
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
    speaker_audio_path = r"C:\\Users\\navee\\Desktop\\Avatar-Lab\\TTS\\monisha.wav"

    # Telugu text crafted for native tone, emotion, and clarity
    telugu_text = (
        "హాయ్! నీకు గుర్తుందా, మన ఇద్దరం కలిసి పల్లెటూరి వీధుల్లో తిరిగిన రోజులు? "
        "ఆ జ్ఞాపకాలు నా మనసులో ఇప్పటికీ అల్లుకుంటూనే ఉంటాయి. ఎంత మధురంగా ఉన్నాయో!"
    )

    print("🎙️ Generating authentic Telugu speech...")

    output_file = generate_speech(
        text=telugu_text,
        speaker_audio_path=speaker_audio_path,
        language="te",
        pitch_std=25.0,
        speaking_rate=12.0,
        emotion=[0.5, 0.05, 0.05, 0.05, 0.05, 0.05, 0.4, 0.5]  # Balanced emotional tone with warmth
    )

    if output_file:
        print(f"✅ Telugu speech saved to: {output_file}")
    else:
        print("❌ Failed to generate Telugu speech.")
