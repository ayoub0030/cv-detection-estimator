from ultralytics import YOLO
import cv2

# -----------------------------
# PARAMETERS
# -----------------------------
KNOWN_WIDTH = 4.0       # The real width of your object in cm
KNOWN_HEIGHT = 12.0     # The real height of your object in cm
FOCAL_LENGTH = 700      # STARTING POINT: Calibrate this using Step 1 above!

# Load your trained model
model = YOLO("best.pt")

# Open laptop camera
cap = cv2.VideoCapture(0)

# To make the distance display smoother
smooth_distance = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO11 inference
    results = model(frame, conf=0.5)

    for box in results[0].boxes:
        # Get coordinates
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = box.conf[0]
        
        # Calculate width in pixels
        pixel_width = x2 - x1
        
        if pixel_width > 0:
            # DISTANCE FORMULA: (Real Width * Focal Length) / Pixel Width
            distance = (KNOWN_WIDTH * FOCAL_LENGTH) / pixel_width
            
            # Simple smoothing filter (keeps the number from flickering)
            if smooth_distance == 0:
                smooth_distance = distance
            else:
                smooth_distance = (smooth_distance * 0.9) + (distance * 0.1)

            # Draw the box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Display Distance and Object info
            label = f"Dist: {smooth_distance:.1f} cm"
            cv2.putText(
                frame, label, (x1, y1 - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
            )

    # Display the frame
    cv2.imshow("HP Camera - Distance Detector", frame)

    # Press 'ESC' to quit
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()