import cv2
import os
import json
import sys

MAPPING_FILE = "id_to_name.json"  # store mapping here

def load_mapping():
    """Load ID-to-Name mapping from file"""
    if os.path.exists(MAPPING_FILE):
        with open(MAPPING_FILE, "r") as f:
            return json.load(f)
    return {}

def save_mapping(mapping):
    """Save mapping back to file"""
    with open(MAPPING_FILE, "w") as f:
        json.dump(mapping, f, indent=4)

def capture_faces(student_id, student_name, save_dir='Dataset'):
    # Format name
    student_name = student_name.strip().replace(" ", "_")
    save_path = os.path.join(save_dir, f"user.{student_id}.{student_name}")
    os.makedirs(save_path, exist_ok=True)

    # Start webcam
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)

    # Load face detector
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    count = 0
    print("📸 Capturing face samples. Look at the camera. Press 'q' to quit.")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("❌ Failed to capture frame.")
            break

        frame = cv2.flip(frame, 1)  # Mirror the image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4, minSize=(80, 80))

        for (x, y, w, h) in faces:
            count += 1
            filename = f"{student_name}.{str(count).zfill(2)}.jpg"
            filepath = os.path.join(save_path, filename)
            cv2.imwrite(filepath, gray[y:y+h, x:x+w])

            # Draw bounding box
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"Sample {count}/50", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("Register Face - Press 'q' to Quit", frame)

        # Exit on key press or enough samples
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif count >= 50:
            print("✅ 50 face samples collected.")
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    if len(sys.argv) >= 3:
        # Case 1: run from Tkinter popup (ID & Name passed as arguments)
        student_id = sys.argv[1]
        student_name = sys.argv[2]
    else:
        # Case 2: run manually in terminal
        print("🔐 Face Registration")

        # Load existing mapping
        id_to_name = load_mapping()

        # Auto-generate next ID
        if id_to_name:
            next_id = str(int(max(id_to_name.keys(), key=int)) + 1)
        else:
            next_id = "1"

        student_id = input(f"Enter Student ID (or press Enter for auto {next_id}, or 'q' to quit): ").strip()
        if student_id.lower() == "q":
            print("❌ Registration cancelled.")
            sys.exit(0)

        if not student_id:
            student_id = next_id

        while not student_id.isdigit():
            student_id = input("❌ ID must be numeric. Try again (or 'q' to quit): ").strip()
            if student_id.lower() == "q":
                print("❌ Registration cancelled.")
                sys.exit(0)

        student_name = input("Enter full name (or 'q' to quit): ").strip()
        if student_name.lower() == "q":
            print("❌ Registration cancelled.")
            sys.exit(0)

    # Save to dictionary & file
    id_to_name = load_mapping()
    id_to_name[student_id] = student_name
    save_mapping(id_to_name)

    # Start face capture
    capture_faces(student_id, student_name)
    print(f"✅ Mapping updated: {student_id} → {student_name}")
