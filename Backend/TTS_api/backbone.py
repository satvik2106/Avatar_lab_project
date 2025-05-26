# zonos/backbone.py

import torch
import torch.nn as nn
from models.fastspeech2 import FastSpeech2  # assumes you have FastSpeech2 model implemented
from utils.load_weights import load_pretrained_weights  # helper function

class ZonosBackbone(nn.Module):
    def _init_(self, config):
        super(ZonosBackbone, self)._init_()
        self.device = torch.device(config.get("device", "cuda" if torch.cuda.is_available() else "cpu"))
        self.precision = config.get("precision", "fp32")
        
        self.model = FastSpeech2(
            n_vocab=config["n_vocab"],
            n_mels=config["n_mels"],
            hidden_size=config["hidden_size"],
            num_encoder_layers=config["num_encoder_layers"],
            num_decoder_layers=config["num_decoder_layers"],
            ffn_kernel_size=config["ffn_kernel_size"],
            dropout=config["dropout"],
            use_speaker_embedding=config.get("use_speaker_embedding", False),
            use_pitch_predictor=config.get("use_pitch_predictor", True)
        ).to(self.device)

        if config.get("pretrained", False):
            self._load_weights(config["weights_path"])

        if self.precision == "fp16":
            self.model = self.model.half()

    def _load_weights(self, path):
        print(f"Loading pretrained weights from {path}")
        state_dict = torch.load(path, map_location=self.device)
        load_pretrained_weights(self.model, state_dict)

    def forward(self, inputs):
        """
        Args:
            inputs: dict with keys:
              - 'text': Tensor (B, T_text)
              - 'speaker_id': Tensor (B,) [optional]
              - 'pitch': Tensor (B, T_text) [optional]
        Returns:
            Mel-spectrogram predictions
        """
        return self.model(**inputs)