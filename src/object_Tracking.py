import cv2

# Open the video file
video_path = "test.mp4"  # Replace with your video file
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error opening video file")
    exit()

# Read the first frame
ret, frame = cap.read()
if not ret:
    print("Cannot read video file")
    exit()

# Let the user select a bounding box (ROI) around the object in the first frame
bbox = cv2.selectROI("Select Object", frame, False)
cv2.destroyWindow("Select Object")

# Create a tracker. Options include:
# - cv2.TrackerCSRT_create()
# - cv2.TrackerKCF_create()
# - cv2.TrackerMIL_create()
# - cv2.TrackerTLD_create() (if available in your OpenCV version)
tracker = cv2.TrackerCSRT.create()

# Initialize the tracker with the first frame and bounding box
tracker.init(frame, bbox)
fps = cap.get(cv2.CAP_PROP_FPS)

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

    # Display the frame
    cv2.imshow("Tracking", frame)

    # Exit if ESC pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
