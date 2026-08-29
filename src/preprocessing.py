import cv2
import os
from mtcnn import MTCNN
def extract_faces_from_video(video_path, output_folder, target_size=(224, 224)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # Face Detector
    detector = MTCNN()
    video_capture = cv2.VideoCapture(video_path)
    frame_count = 0
    saved_count = 0
    print(style_text("[DeepGuard Core] Processing video stream...", "blue"))
    while video_capture.isOpened():
        ret, frame = video_capture.read()
        if not ret:
            break
        if frame_count % 5 == 0:
            results = detector.detect_faces(frame)
            for result in results:
                x, y, w, h = result['box']
                x, y = max(0, x), max(0, y)
                face_crop = frame[y:y+h, x:x+w]                
                if face_crop.size > 0:                
                    face_resized = cv2.resize(face_crop, target_size)                    
                    output_path = os.path.join(output_folder, f"face_frame_{saved_count}.jpg")
                    cv2.imwrite(output_path, face_resized)
                    saved_count += 1                    
        frame_count += 1
    video_capture.release()
    print(f"[DeepGuard Core] Complete! Extracted {saved_count} structured facial frames.")
def style_text(text, color):
    colors = {"blue": "\033[94m", "end": "\033[0m"}
    return f"{colors.get(color, '')}{text}{colors['end']}"
if __name__ == "__main__":
    # extract_faces_from_video('sample_onboarding.mp4', 'data/extracted_faces')
    pass
