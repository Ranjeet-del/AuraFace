import cv2
import numpy as np
from PIL import Image
import os
from tkinter import messagebox, Tk
import time
import sys

# ==============================
# Paths
# ==============================
DATASET_PATH = "Dataset"   # folder where captured faces are stored
TRAINER_PATH = "trainer"   # folder to save trained model

# Create trainer folder if not exists
os.makedirs(TRAINER_PATH, exist_ok=True)

# Recognizer & detector
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


# ==============================
# Get Images & Labels Function
# ==============================
def getImagesAndLabels(path):
    faceSamples = []
    ids = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.lower().endswith(("jpg", "png", "jpeg")):
                imagePath = os.path.join(root, file)
                PIL_img = Image.open(imagePath).convert('L')  # grayscale
                img_numpy = np.array(PIL_img, 'uint8')

                # Folder format: user.<id>.<name>
                folder_name = os.path.basename(root)
                try:
                    id = int(folder_name.split(".")[1])  # Extract ID
                except:
                    print(f"⚠️ Skipping {imagePath}, invalid folder format")
                    continue

                faces = detector.detectMultiScale(img_numpy)
                for (x, y, w, h) in faces:
                    faceSamples.append(img_numpy[y:y+h, x:x+w])
                    ids.append(id)

    return faceSamples, ids


# ==============================
# Training Function
# ==============================
def train_classifier():
    print("\n📢 [INFO] Training faces. Please wait...")

    faces, ids = getImagesAndLabels(DATASET_PATH)

    if len(faces) == 0:
        print("❌ No faces found in dataset. Please capture images first!")
        # Show popup if run from GUI
        root = Tk()
        root.withdraw()
        messagebox.showerror("Training Failed", "No faces found in dataset.\nPlease capture student images first.")
        return

    # Progress Bar Simulation
    total = len(faces)
    for i, face in enumerate(faces):
        percent = int((i+1) / total * 100)
        sys.stdout.write(f"\r⏳ Training Progress: {percent}% completed")
        sys.stdout.flush()
        time.sleep(0.01)  # Just to simulate progress

    # Train recognizer
    recognizer.train(faces, np.array(ids))

    # Save trained model
    trainer_file = os.path.join(TRAINER_PATH, "trainer.yml")
    recognizer.save(trainer_file)

    print(f"\n\n✅ [SUCCESS] Training completed. {len(np.unique(ids))} unique IDs trained.")
    print(f"📂 Model saved at: {trainer_file}")

    # Popup Notification
    root = Tk()
    root.withdraw()
    messagebox.showinfo("Training Complete", f"Training Completed Successfully!\n\n{len(np.unique(ids))} students trained.")


# ==============================
# Run Training
# ==============================
if __name__ == "__main__":
    train_classifier()
