# # Copyright (c) 2024 Bytedance Ltd. and/or its affiliates
# #
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at
# #
# #     http://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.

# import argparse
# import os
# from omegaconf import OmegaConf
# import torch
# from diffusers import AutoencoderKL, DDIMScheduler
# from latentsync.models.unet import UNet3DConditionModel
# from latentsync.pipelines.lipsync_pipeline import LipsyncPipeline
# from accelerate.utils import set_seed
# from latentsync.whisper.audio2feature import Audio2Feature # Ensure this import is correct


# def main(config, args):
#     if not os.path.exists(args.video_path):
#         raise RuntimeError(f"Video path '{args.video_path}' not found")
#     if not os.path.exists(args.audio_path):
#         raise RuntimeError(f"Audio path '{args.audio_path}' not found")

#     is_fp16_supported = torch.cuda.is_available() and torch.cuda.get_device_capability()[0] >= 7
#     dtype = torch.float16 if is_fp16_supported else torch.float32

#     print(f"Using dtype: {dtype}")
#     print(f"Input video path: {args.video_path}")
#     print(f"Input audio path: {args.audio_path}")
#     print(f"Loaded checkpoint path: {args.inference_ckpt_path}")

#     scheduler_model_name_or_path = "runwayml/stable-diffusion-v1-5"
#     print(f"[INFO] Loading scheduler from: {scheduler_model_name_or_path}, subfolder='scheduler'")
#     try:
#         scheduler = DDIMScheduler.from_pretrained(
#             scheduler_model_name_or_path,
#             subfolder="scheduler",
#             torch_dtype=dtype
#         )
#     except TypeError:
#         print(f"[WARNING] Failed to load scheduler with torch_dtype. Attempting without torch_dtype.")
#         scheduler = DDIMScheduler.from_pretrained(
#             scheduler_model_name_or_path,
#             subfolder="scheduler"
#         )
#     except Exception as e:
#         print(f"[ERROR] Failed to load scheduler: {e}. Please check the scheduler name and internet connection.")
#         raise

#     # --- MODIFIED WHISPER MODEL PATH RESOLUTION ---
#     script_dir = os.path.dirname(os.path.abspath(__file__)) # .../backend/LatentSync/scripts
#     # Assuming "checkpoints" directory is at the same level as "scripts" and "api" directories,
#     # i.e., .../backend/LatentSync/checkpoints
#     checkpoints_dir = os.path.abspath(os.path.join(script_dir, '..', 'checkpoints'))

#     if config.model.cross_attention_dim == 768:
#         whisper_model_filename = "small.pt"
#     elif config.model.cross_attention_dim == 384:
#         whisper_model_filename = "tiny.pt" # This was selected based on your error
#     else:
#         raise NotImplementedError("cross_attention_dim must be 768 or 384")
    
#     # Construct the full expected path to the local .pt file
#     local_whisper_model_path = os.path.join(checkpoints_dir, "whisper", whisper_model_filename)
#     print(f"[INFO] Expected local Whisper model path: {local_whisper_model_path}")

#     model_to_load_for_whisper = ""
#     if os.path.exists(local_whisper_model_path):
#         # If the .pt file exists at the constructed path, use this absolute path
#         model_to_load_for_whisper = local_whisper_model_path
#         print(f"[INFO] Found local Whisper model at '{local_whisper_model_path}'. Using this path.")
#     else:
#         # If the local .pt file is NOT found, fall back to the model name (e.g., "tiny", "small")
#         # This will allow the Whisper library to attempt to download it if it's a recognized name.
#         model_name_only = whisper_model_filename.replace('.pt', '')
#         model_to_load_for_whisper = model_name_only
#         print(f"[WARNING] Local Whisper model file not found at '{local_whisper_model_path}'. "
#               f"Attempting to load/download Whisper by model name: '{model_to_load_for_whisper}'.")
        
#         # Verify if the model name is a standard Whisper model name (optional check, good for clarity)
#         available_whisper_official_names = ['tiny.en', 'tiny', 'base.en', 'base', 'small.en', 'small', 'medium.en', 'medium', 'large', 'large-v1', 'large-v2', 'large-v3']
#         if model_to_load_for_whisper not in available_whisper_official_names:
#             # This should ideally not happen if your filenames are "tiny.pt" or "small.pt"
#             # but it's a safeguard.
#             raise FileNotFoundError(
#                 f"Local Whisper model '{local_whisper_model_path}' not found, "
#                 f"AND the derived model name '{model_to_load_for_whisper}' is not a recognized standard Whisper model. "
#                 f"Please ensure the .pt file exists or use a standard model name."
#             )
#     # --- END OF MODIFIED WHISPER MODEL PATH RESOLUTION ---

#     audio_encoder = Audio2Feature(
#         model_path=model_to_load_for_whisper, # Pass the resolved path or model name
#         device="cuda",
#         num_frames=config.data.num_frames,
#         audio_feat_length=config.data.audio_feat_length,
#     )

#     print(f"[INFO] Loading VAE from: stabilityai/sd-vae-ft-mse")
#     vae = AutoencoderKL.from_pretrained("stabilityai/sd-vae-ft-mse", torch_dtype=dtype)
#     if hasattr(vae.config, 'scaling_factor'):
#         vae.config.scaling_factor = 0.18215
#     if hasattr(vae.config, 'shift_factor'):
#         try:
#             vae.config.shift_factor = 0
#         except AttributeError:
#             print("[WARNING] Could not set 'shift_factor' on VAE config.")


#     print(f"[INFO] Loading UNet3DConditionModel from config and checkpoint: {args.inference_ckpt_path}")
#     denoising_unet, _ = UNet3DConditionModel.from_pretrained(
#         OmegaConf.to_container(config.model),
#         args.inference_ckpt_path,
#         device="cpu",
#     )
#     denoising_unet = denoising_unet.to(device="cuda", dtype=dtype)

#     pipeline = LipsyncPipeline(
#         vae=vae,
#         audio_encoder=audio_encoder,
#         denoising_unet=denoising_unet,
#         scheduler=scheduler,
#     ).to("cuda")

#     if args.seed != -1:
#         set_seed(args.seed)
#         print(f"Using fixed seed: {args.seed}")
#     else:
#         current_seed = torch.seed()
#         set_seed(current_seed)
#         print(f"Using random seed: {current_seed}")

#     print("[INFO] Starting LipsyncPipeline...")
#     pipeline_output = pipeline(
#         video_path=args.video_path,
#         audio_path=args.audio_path,
#         video_out_path=args.video_out_path,
#         video_mask_path=args.video_out_path.replace(".mp4", "_mask.mp4"),
#         num_frames=config.data.num_frames,
#         num_inference_steps=args.inference_steps,
#         guidance_scale=args.guidance_scale,
#         weight_dtype=dtype,
#         width=config.data.resolution,
#         height=config.data.resolution,
#         mask_image_path=config.data.get("mask_image_path", None),
#     )
#     print("[INFO] LipsyncPipeline completed.")
#     return {"output_path": args.video_out_path}


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--unet_config_path", type=str, default="configs/unet/stage2.yaml")
#     parser.add_argument("--inference_ckpt_path", type=str, required=True)
#     parser.add_argument("--video_path", type=str, required=True)
#     parser.add_argument("--audio_path", type=str, required=True)
#     parser.add_argument("--video_out_path", type=str, required=True)
#     parser.add_argument("--inference_steps", type=int, default=20)
#     parser.add_argument("--guidance_scale", type=float, default=1.0)
#     parser.add_argument("--seed", type=int, default=1247)
#     args_cli = parser.parse_args()

#     print(f"[INFO] Loading UNet config from: {args_cli.unet_config_path}")
#     if not os.path.exists(args_cli.unet_config_path):
#         raise FileNotFoundError(f"UNet config path '{args_cli.unet_config_path}' not found. Please check the path.")
    
#     config_loaded = OmegaConf.load(args_cli.unet_config_path)
#     main(config_loaded, args_cli)
# Copyright (c) 2024 Bytedance Ltd. and/or its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os
from omegaconf import OmegaConf
import torch
from diffusers.schedulers.scheduling_ddim import DDIMScheduler
import json

# --- Fix: resolve absolute path for scheduler config ---
current_dir = os.path.dirname(os.path.abspath(__file__))
scheduler_config_path =r"C:\Users\Satvik Vattipalli\OneDrive\Desktop\Avatar _lab_full\Backend\LatentSync\configs\scheduler_config.json"
scheduler_config_path = os.path.normpath(scheduler_config_path)

with open(scheduler_config_path, "r") as f:
    scheduler_config = json.load(f)

scheduler = DDIMScheduler.from_config(scheduler_config)

from latentsync.models.unet import UNet3DConditionModel
from latentsync.pipelines.lipsync_pipeline import LipsyncPipeline
from accelerate.utils import set_seed
from latentsync.whisper.audio2feature import Audio2Feature
from diffusers.models import AutoencoderKL


def main(config, args):
    import latentsync.utils.util as util

    if not os.path.exists(args.video_path):
        raise RuntimeError(f"Video path '{args.video_path}' not found")
    if not os.path.exists(args.audio_path):
        raise RuntimeError(f"Audio path '{args.audio_path}' not found")

    is_fp16_supported = torch.cuda.is_available() and torch.cuda.get_device_capability()[0] > 7
    dtype = torch.float16 if is_fp16_supported else torch.float32

    print(f"Input video path: {args.video_path}")
    print(f"Input audio path: {args.audio_path}")
    print(f"Loaded checkpoint path: {args.inference_ckpt_path}")

    if config.model.cross_attention_dim == 768:
        whisper_model_path = "small"  # or "small.en" for English-only
    elif config.model.cross_attention_dim == 384:
        whisper_model_path = "tiny"   # or "tiny.en" for English-only
    else:
        raise NotImplementedError("cross_attention_dim must be 768 or 384")

    audio_encoder = Audio2Feature(
        model_path=whisper_model_path,
        device="cuda",
        num_frames=config.data.num_frames,
        audio_feat_length=config.data.audio_feat_length,
    )

    vae = AutoencoderKL.from_pretrained("stabilityai/sd-vae-ft-mse", torch_dtype=dtype)
    vae.config.scaling_factor = 0.18215
    vae.config.shift_factor = 0

    denoising_unet, _ = UNet3DConditionModel.from_pretrained(
        OmegaConf.to_container(config.model),
        args.inference_ckpt_path,
        device="cpu",
    )

    denoising_unet = denoising_unet.to(dtype=dtype)

    pipeline = LipsyncPipeline(
        vae=vae,
        audio_encoder=audio_encoder,
        denoising_unet=denoising_unet,
        scheduler=scheduler,
    ).to("cuda")

    if args.seed != -1:
        set_seed(args.seed)
    else:
        torch.seed()

    print(f"Initial seed: {torch.initial_seed()}")

    pipeline(
        video_path=args.video_path,
        audio_path=args.audio_path,
        video_out_path=args.video_out_path,
        video_mask_path=args.video_out_path.replace(".mp4", "_mask.mp4"),
        num_frames=config.data.num_frames,
        num_inference_steps=args.inference_steps,
        guidance_scale=args.guidance_scale,
        weight_dtype=dtype,
        width=config.data.resolution,
        height=config.data.resolution,
        mask_image_path=config.data.mask_image_path,
    )
    return {"output_path": args.video_out_path}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--unet_config_path", type=str, default="configs/unet.yaml")
    parser.add_argument("--inference_ckpt_path", type=str, required=True)
    parser.add_argument("--video_path", type=str, required=True)
    parser.add_argument("--audio_path", type=str, required=True)
    parser.add_argument("--video_out_path", type=str, required=True)
    parser.add_argument("--inference_steps", type=int, default=20)
    parser.add_argument("--guidance_scale", type=float, default=1.0)
    parser.add_argument("--seed", type=int, default=1247)
    args = parser.parse_args()

    from types import SimpleNamespace
    from omegaconf import OmegaConf

    def convert_namespace_to_omegaconf(obj):
        if isinstance(obj, SimpleNamespace):
            return OmegaConf.create({k: convert_namespace_to_omegaconf(v) for k, v in vars(obj).items()})
        elif isinstance(obj, dict):
            return {k: convert_namespace_to_omegaconf(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_namespace_to_omegaconf(item) for item in obj]
        else:
            return obj
    
    raw_config = OmegaConf.load(args.unet_config_path)
    config = convert_namespace_to_omegaconf(raw_config)

    # config = OmegaConf.load(args.unet_config_path)
    print("CONFIG TYPE DEBUG:", type(config), type(config.model))

    main(config, args)
