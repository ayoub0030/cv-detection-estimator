import cv2
import math
from ultralytics import YOLO

# ================== CONFIG ==================
MODEL_PATH = "best.pt"
CAMERA_INDEX = 0
CONF_THRESHOLD = 0.5

REAL_OBJECT_HEIGHT_CM = 7.0
FOCAL_LENGTH_PIXELS = 1366.0
# ============================================

model = YOLO(MODEL_PATH)

cap = cv2.VideoCapture(CAMERA_INDEX)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

if not cap.isOpened():
    raise RuntimeError("❌ Could not open webcam")

print("✅ Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model.predict(
        source=frame,
        conf=CONF_THRESHOLD,
        verbose=False
    )

    for r in results:
        if r.boxes is None:
            continue

        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = float(box.conf[0])

            bbox_height_px = y2 - y1
            if bbox_height_px <= 0:
                continue

            # 🔹 ADD THIS PRINT HERE 🔹
            print(f"Bounding box height: {bbox_height_px:.1f} pixels")

            # Distance calculation
            distance_cm = (REAL_OBJECT_HEIGHT_CM * FOCAL_LENGTH_PIXELS) / bbox_height_px

            cv2.rectangle(
                frame,
                (int(x1), int(y1)),
                (int(x2), int(y2)),
                (0, 255, 0),
                2
            )

            label = f"toy_car {conf:.2f} | {distance_cm:.1f} cm"

            cv2.putText(
                frame,
                label,
                (int(x1), int(y1) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

    cv2.imshow("Toy Car Detection + Distance (C920)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()