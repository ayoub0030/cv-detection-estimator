from ultralytics import YOLO
import cv2

# Load trained model
model = YOLO("best.pt")

# Open webcam (0 = default camera)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO detection
    results = model(frame, conf=0.25)

    # Draw boxes
    annotated_frame = results[0].plot()

    # Show result
    cv2.imshow("YOLO Webcam Detection", annotated_frame)

    # Press ESC to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
