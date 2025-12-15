# Face_Detect.py - corrected
import os
import cv2
import json

# Config - set to your model & mapping file names
MODEL_PATH = "trainer.yml"          # path to LBPH model file produced by your trainer
MAPPING_FILE = "id_to_name.json"    # JSON mapping: { "1": "Alice", "2": "Bob", ... }
CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

# Load face cascade
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

# Load recognizer - safe fallback if cv2.face is missing
try:
    recognizer = cv2.face.LBPHFaceRecognizer_create()
except AttributeError:
    raise RuntimeError("cv2.face LBPHFaceRecognizer not available. Install opencv-contrib-python.")

# load model if present, otherwise warn
if os.path.exists(MODEL_PATH):
    recognizer.read(MODEL_PATH)
else:
    print(f"[Warning] Model not found at {MODEL_PATH}. Please run trainer first.")

# load id->name mapping
if os.path.exists(MAPPING_FILE):
    with open(MAPPING_FILE, "r", encoding="utf-8") as f:
        id_to_name = json.load(f)
else:
    id_to_name = {}
    print(f"[Warning] Mapping file not found at {MAPPING_FILE}. Names will show as 'Unknown'.")

# Recommended ROI size: set to the same size your trainer uses.
# If your trainer used a particular face size, use that same size here.
ROI_SIZE = (200, 200)  # change if your training used different size

# Confidence threshold (lower = stricter)
CONF_THRESHOLD = 60  # tune between ~40..90 depending on training quality

cam = cv2.VideoCapture(0)
if not cam.isOpened():
    raise RuntimeError("Unable to open camera. Check device index or permissions.")

font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    ret, img = cam.read()
    if not ret or img is None:
        # skip frame instead of crashing
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))

    # iterate all detected faces (so multiple people are handled)
    for (x, y, w, h) in faces:
        # draw rectangle
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # extract ROI and resize to training size
        roi_gray = gray[y:y+h, x:x+w]
        try:
            roi_resized = cv2.resize(roi_gray, ROI_SIZE)
        except Exception:
            # if resize fails, use ROI as-is
            roi_resized = roi_gray

        # predict
        try:
            id_, conf = recognizer.predict(roi_resized)
        except Exception as e:
            # most likely model not loaded; mark unknown
            id_, conf = None, None

        if id_ is not None and conf is not None and conf < CONF_THRESHOLD:
            name = id_to_name.get(str(id_), id_to_name.get(int(id_), "Unknown"))
            label = f"{name} ({int(conf)})"
        else:
            label = "Unknown"

        # put label above rectangle
        cv2.putText(img, label, (x, y - 10), font, 0.8, (255, 255, 255), 2)

    cv2.imshow("Face Detect - Press q to quit", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()
