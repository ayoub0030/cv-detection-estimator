from ultralytics import YOLO

# Load trained model
model = YOLO("best.pt")

# Run detection on image
results = model(
    source="z.png",   # image path
    conf=0.25,
    save=True,
    show=True
)

print("Detection done on image.")
