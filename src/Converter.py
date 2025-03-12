import cv2

video_path = "Clear_Blue_Water.mov"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error opening video file")
    exit()

original_fps = cap.get(cv2.CAP_PROP_FPS)
desired_fps = 24
skip_frames = int(original_fps / desired_fps)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('test.mp4', fourcc, desired_fps, (width, height))

frame_number = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    if frame_number % skip_frames == 0:
        out.write(frame)

    frame_number += 1

cap.release()
out.release()
