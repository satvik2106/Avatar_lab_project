import torch
import torchaudio
from zonos.model import Zonos
from zonos.conditioning import make_cond_dict
from zonos.utils import DEFAULT_DEVICE as device

torch._dynamo.config.suppress_errors = True
import torch._dynamo
torch._dynamo.config.suppress_errors = True


# model = Zonos.from_pretrained("Zyphra/Zonos-v0.1-hybrid", device=device)
model = Zonos.from_pretrained("Zyphra/Zonos-v0.1-transformer", device=device)

wav, sampling_rate = torchaudio.load(r"C:\Users\navee\Desktop\Avatar-Lab\Voice reference\Satvik.wav")
wav = wav.to(device)
speaker = model.make_speaker_embedding(wav, sampling_rate)

torch.manual_seed(421)

cond_dict = make_cond_dict(text="Zonos plays a crucial role in the Avatar Lab project by serving as the backbone of speech generation. Its high accuracy in converting text to realistic, phoneme-level speech ensures that the avatars not only look natural but also sound human-like. With support for multiple languages and expressive intonation, Zonos enables smooth and synchronized lip-syncing, making it an essential component for creating lifelike digital avatars in real-time applications.", speaker=speaker, language="en-us")
conditioning = model.prepare_conditioning(cond_dict)

codes = model.generate(conditioning)

wavs = model.autoencoder.decode(codes).cpu()
torchaudio.save("sample1.wav", wavs[0], model.autoencoder.sampling_rate)