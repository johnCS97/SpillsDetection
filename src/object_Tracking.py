import cv2

# Open the video file
video_path = "Clear_Water.mp4" # Replace with your video file
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error opening video file")
    exit()

# Get video properties
fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter object
output_path = "Oil_Spill_Tracking.mp4"
fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec for .mp4 files
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# Read the first frame
ret, frame = cap.read()
if not ret:
    print("Cannot read video file")
    exit()

# Let the user select a bounding box (ROI) around the object in the first frame
bbox = cv2.selectROI("Select Object", frame, False)
cv2.destroyWindow("Select Object")

# Create a tracker
tracker = cv2.legacy.TrackerTLD_create()

# Initialize the tracker with the first frame and bounding box
tracker.init(frame, bbox)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Update the tracker and get the updated position
    success, bbox = tracker.update(frame)

    if success:
        # Draw the bounding box on the frame
        x, y, w, h = [int(v) for v in bbox]
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    else:
        cv2.putText(frame, "Tracking failure detected", (100, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    # Write the frame to the output video
    out.write(frame)

    # Display the frame
    cv2.imshow("Tracking", frame)

    # Exit if ESC is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"Tracking video saved as {output_path}")
