# from flask import Flask, request, jsonify, send_file
# from werkzeug.utils import secure_filename
# import os
# import uuid
# import sys
# from omegaconf import OmegaConf
# import cv2
# from flask_cors import CORS

# # Ensure the path to the 'scripts' and 'latentsync' directory is correct
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from scripts.inference import main as run_inference

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}})
# UPLOAD_FOLDER = 'temp'
# OUTPUT_FOLDER = 'outputs'

# # Path to the main configuration file
# CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'configs', 'unet', 'stage2.yaml'))

# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# @app.route("/")
# def index():
#     return "LatentSync API is up and running 🚀"

# @app.route('/api/lipsync', methods=['POST'])
# def lipsync():
#     if 'video' not in request.files:
#         return jsonify({'error': 'No video file provided'}), 400
#     if 'audio' not in request.files:
#         return jsonify({'error': 'No audio file provided'}), 400

#     video_file = request.files['video']
#     video_filename = secure_filename(video_file.filename)
#     unique_video_name = f"{uuid.uuid4()}_{video_filename}"
#     # video_path will be relative to app.py's location (e.g., 'temp/video.mp4')
#     video_path_relative = os.path.join(UPLOAD_FOLDER, unique_video_name)
#     video_file.save(video_path_relative)

#     if os.path.getsize(video_path_relative) == 0:
#         os.remove(video_path_relative)
#         return jsonify({'error': 'Uploaded video file is empty after saving'}), 400

#     # Perform initial checks with the relative path, as app.py knows its CWD
#     cap = cv2.VideoCapture(video_path_relative)
#     if not cap.isOpened():
#         cap.release()
#         os.remove(video_path_relative)
#         return jsonify({'error': 'Cannot open uploaded video file with OpenCV'}), 400
#     ret, frame = cap.read()
#     if not ret or frame is None:
#         cap.release()
#         os.remove(video_path_relative)
#         return jsonify({'error': 'Cannot read a frame from the uploaded video with OpenCV'}), 400
#     cap.release()

#     audio_file = request.files['audio']
#     audio_filename = secure_filename(audio_file.filename)
#     audio_unique_name = f"{uuid.uuid4()}_{audio_filename}"
#     # audio_path will be relative (e.g., 'temp/audio.wav')
#     audio_path_relative = os.path.join(UPLOAD_FOLDER, audio_unique_name)
#     audio_file.save(audio_path_relative)

#     if os.path.getsize(audio_path_relative) == 0:
#         os.remove(audio_path_relative)
#         return jsonify({'error': 'Uploaded audio file is empty after saving'}), 400

#     # Convert to absolute paths for the inference script
#     abs_video_path = os.path.abspath(video_path_relative)
#     abs_audio_path = os.path.abspath(audio_path_relative)
#     abs_output_folder = os.path.abspath(OUTPUT_FOLDER) # Ensure output folder path is absolute too

#     try:
#         print(f"[INFO] Loading base config from: {CONFIG_PATH}")
#         if not os.path.exists(CONFIG_PATH):
#             print(f"[ERROR] Base config file not found at: {CONFIG_PATH}")
#             return jsonify({'error': f'Server configuration error: Base config not found at {CONFIG_PATH}'}), 500
#         config = OmegaConf.load(CONFIG_PATH)

#         project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#         mask_image_path_from_config = config.data.get("mask_image_path", None)
#         resolved_mask_path = None

#         if mask_image_path_from_config:
#             if os.path.isabs(mask_image_path_from_config):
#                 resolved_mask_path = mask_image_path_from_config
#             else:
#                 resolved_mask_path = os.path.join(project_root, mask_image_path_from_config)
            
#             print(f"[DEBUG] Mask image path from config: {mask_image_path_from_config}")
#             print(f"[DEBUG] Attempting to use resolved absolute mask image path: {resolved_mask_path}")

#             if os.path.exists(resolved_mask_path):
#                 print(f"[DEBUG] Mask image file exists at: {resolved_mask_path}")
#                 config.data.mask_image_path = resolved_mask_path
#                 print(f"[INFO] Updated config.data.mask_image_path to absolute path: {resolved_mask_path}")
#             else:
#                 print(f"[DEBUG_ERROR] Mask image file DOES NOT EXIST at: {resolved_mask_path}. Setting to None.")
#                 config.data.mask_image_path = None
#         else:
#             print("[DEBUG] No 'mask_image_path' specified in config.data")
#             if "data" in config and hasattr(config.data, "mask_image_path"):
#                  config.data.mask_image_path = None
#             elif "data" in config:
#                 OmegaConf.update(config, "data.mask_image_path", None, merge=True)
#             else:
#                 OmegaConf.update(config, "data", {"mask_image_path": None}, merge=True)

#         # Output path for the final video - ensure it's absolute
#         abs_video_out_path = os.path.join(abs_output_folder, f"out_{unique_video_name}")

#         overrides = OmegaConf.create({
#             # These are now effectively placeholders in config if pipeline uses args directly
#             # 'input_video_path': abs_video_path, 
#             # 'output_path': abs_video_out_path,
#         })
#         # Merge, but args will provide the primary paths for video_path and video_out_path
#         config = OmegaConf.merge(config, overrides) 
#         # If the pipeline relies on config.output_path, ensure it's set correctly
#         config.output_path = abs_video_out_path


#         inference_ckpt_path = r"C:\Users\Satvik Vattipalli\OneDrive\Desktop\Avatar _lab_full\Backend\LatentSync\checkpoints\latentsync_unet.pt"
#         if not os.path.exists(inference_ckpt_path):
#             print(f"[ERROR] Inference checkpoint not found at: {inference_ckpt_path}")
#             return jsonify({'error': f'Server configuration error: Inference checkpoint not found at {inference_ckpt_path}'}), 500
#         print(f"[INFO] Using inference checkpoint: {inference_ckpt_path}")

#         from types import SimpleNamespace
#         inference_config = config.get("inference", {}) 

#         args = SimpleNamespace(
#             inference_ckpt_path=inference_ckpt_path,
#             video_path=abs_video_path, # Use absolute path
#             audio_path=abs_audio_path, # Use absolute path
#             video_out_path=abs_video_out_path, # Use absolute path
#             inference_steps=inference_config.get("inference_steps", 20),
#             guidance_scale=inference_config.get("guidance_scale", 1.0),
#             seed=inference_config.get("seed", 42)
#         )

#         print(f"[INFO] Running inference with absolute video_path: {args.video_path}")
#         print(f"[INFO] Running inference with absolute audio_path: {args.audio_path}")
#         print(f"[INFO] Output will be saved to (absolute): {args.video_out_path}")
#         print(f"[INFO] Inference args: {args}")
#         print(f"[INFO] Config being passed to run_inference (mask_image_path): {config.data.get('mask_image_path', 'Not set')}")
        
#         result = run_inference(config=config, args=args)
        
#         output_path_from_result = result.get('output_path') if isinstance(result, dict) else args.video_out_path

#         if not os.path.exists(output_path_from_result):
#             print(f"[ERROR] Output file was not created at: {output_path_from_result}")
#             raise FileNotFoundError(f"Output file not found after inference: {output_path_from_result}")

#         print(f"[INFO] Inference successful. Sending file: {output_path_from_result}")
#         return send_file(output_path_from_result, as_attachment=True)

#     except Exception as e:
#         import traceback
#         print("[ERROR] An exception occurred during lipsync processing:")
#         print(traceback.format_exc()) 
#         return jsonify({'error': str(e)}), 500

#     finally:
#         import threading
#         # Use the original relative paths for cleanup as they are simpler and defined in this scope
#         # These are captured by the closure for cleanup_files
#         final_video_path_relative = video_path_relative 
#         final_audio_path_relative = audio_path_relative
        
#         def cleanup_files():
#             try:
#                 # Check if variables are defined before using them for cleanup
#                 # (final_video_path_relative and final_audio_path_relative are from the outer scope)
#                 if os.path.exists(final_video_path_relative):
#                     print(f"[INFO] Cleaning up temporary video file: {final_video_path_relative}")
#                     os.remove(final_video_path_relative)
#                 else:
#                     print(f"[DEBUG] Temporary video file not found for cleanup (or already cleaned): {final_video_path_relative}")

#                 if os.path.exists(final_audio_path_relative):
#                     print(f"[INFO] Cleaning up temporary audio file: {final_audio_path_relative}")
#                     os.remove(final_audio_path_relative)
#                 else:
#                      print(f"[DEBUG] Temporary audio file not found for cleanup (or already cleaned): {final_audio_path_relative}")

#             except Exception as e_cleanup:
#                 print(f"[ERROR] Exception during file cleanup: {str(e_cleanup)}")

#         cleanup_thread = threading.Thread(target=cleanup_files)
#         cleanup_thread.start()

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=6900, debug=True)
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import uuid
import sys
from omegaconf import OmegaConf
import cv2
from flask_cors import CORS

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.inference import main as run_inference

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}})
UPLOAD_FOLDER = 'temp'
OUTPUT_FOLDER = 'outputs'
CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'configs', 'unet', 'stage2.yaml'))

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return "LatentSync API is up and running 🚀"

@app.route('/api/lipsync', methods=['POST'])
def lipsync():

    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    video = request.files['video']
    filename = secure_filename(video.filename)
    unique_name = f"{uuid.uuid4()}_{filename}"
    video_path = os.path.join(UPLOAD_FOLDER, unique_name)
    video.save(video_path)

    if os.path.getsize(video_path) == 0:
        os.remove(video_path)
        return jsonify({'error': 'Invalid or empty video file'}), 400

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        cap.release()
        os.remove(video_path)
        return jsonify({'error': 'Invalid or empty video file'}), 400
    cap.release()

    audio = request.files['audio']
    audio_filename = secure_filename(audio.filename)
    audio_unique_name = f"{uuid.uuid4()}_{audio_filename}"
    audio_path = os.path.join(UPLOAD_FOLDER, audio_unique_name)
    audio.save(audio_path)

    try:
        config = OmegaConf.load(CONFIG_PATH)

        overrides = OmegaConf.create({
            'input_video_path': video_path,
            'output_path': os.path.join(OUTPUT_FOLDER, f"out_{unique_name}"),
        })
        config = OmegaConf.merge(config, overrides)

        from types import SimpleNamespace
        args = SimpleNamespace(
            inference_ckpt_path=r"C:\Users\Satvik Vattipalli\OneDrive\Desktop\Avatar _lab_full\Backend\LatentSync\checkpoints\latentsync_unet.pt",
            video_path=video_path,
            audio_path=audio_path,
            video_out_path=config.output_path,
            inference_steps=20,
            guidance_scale=1.0,
            seed=42
        )

        print(f"[INFO] Running inference on {video_path}")
        result = run_inference(config=config, args=args)
        output_path = result.get('output_path') if isinstance(result, dict) else config.output_path

        if not os.path.exists(output_path):
            raise FileNotFoundError(f"Output file not found: {output_path}")

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return jsonify({'error': str(e)}), 500

    finally:
        import threading

        def cleanup_files():
            if os.path.exists(video_path):
                os.remove(video_path)
            if os.path.exists(audio_path):
                os.remove(audio_path)

        cleanup_thread = threading.Thread(target=cleanup_files)
        cleanup_thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6900, debug=True)
