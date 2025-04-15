import cv2
from ultralytics import YOLO

# Load YOLO model (explicitly setting task)
model = YOLO("yolov8_trained_model_25epoch.pt", task="detect")

# Initialize webcam
cap = cv2.VideoCapture(0)  

if not cap.isOpened():
    print("❌ ERROR: Camera not detected!")
    exit()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run inference
    results = model(frame)

    # Extract detected class names
    detected_classes = [model.names[int(d.cls.item())] for d in results[0].boxes]

    # Check if SafetyVest or HardHat is missing
    missing_items = []
    if "SafetyVest" not in detected_classes:
        missing_items.append("Safety Vest")
    if "HardHat" not in detected_classes:
        missing_items.append("Hard Hat")

    # Annotate the frame
    annotated_frame = results[0].plot()

    # Display warning message if needed
    if missing_items:
        alert_text = f"⚠️ MISSING: {', '.join(missing_items)}"
        cv2.putText(
            annotated_frame, alert_text, (50, 50), 
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3
        )

    # Show the annotated video feed
    cv2.imshow("YOLOv8 Safety Detection", annotated_frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()