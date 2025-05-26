import cv2

# Ensure this is the path to the video that causes issues in app.py
# (e.g., copy it from your 'temp' folder after an upload attempt)
video_path = r"C:\Users\Satvik Vattipalli\OneDrive\Desktop\Avatar _lab_full\Backend\LatentSync\assets\demo1_video.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"Error: Could not open video {video_path}")
else:
    frame_count = 0
    max_frames_to_test = 10 # Test the first 10 frames
    while frame_count < max_frames_to_test:
        ret, frame = cap.read()
        if ret:
            print(f"Successfully read frame {frame_count}. Shape: {frame.shape}")
            # You could try cvtColor here if you know the expected conversion
            # try:
            #     gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #     print(f"Frame {frame_count} converted to gray successfully.")
            # except cv2.error as e:
            #     print(f"Error converting frame {frame_count}: {e}")
            #     break
            frame_count += 1
        else:
            print(f"Error: Could not read frame {frame_count} (or video ended).")
            break
    cap.release()
    print(f"Tested {frame_count} frames.")