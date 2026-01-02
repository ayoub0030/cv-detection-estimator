from ultralytics import YOLO
import cv2

# -----------------------------
# PARAMETERS
# -----------------------------
KNOWN_WIDTH = 25.0      # cm
FOCAL_LENGTH = 700

# Load model
model = YOLO("best.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, conf=0.5)

    for box in results[0].boxes:
        cls = int(box.cls[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        box_width = x2 - x1
        if box_width == 0:
            continue

        distance = (KNOWN_WIDTH * FOCAL_LENGTH) / box_width

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"{distance:.1f} cm",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    cv2.imshow("Helmet Distance Estimation", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
