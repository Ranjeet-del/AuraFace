import cv2
import sqlite3
import os
import json
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import simpledialog, messagebox

# ---------------- Paths ----------------
MODEL_PATH = "trainer.yml"
MAPPING_FILE = "id_to_name.json"
DB_PATH = r"D:\5th Sem\Project AuraFAce\student.db"
CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

# ---------------- Subject Input ----------------
if len(sys.argv) > 1:
    SUBJECT_NAME = sys.argv[1]
else:
    root = tk.Tk()
    root.withdraw()
    SUBJECT_NAME = simpledialog.askstring("Subject Input", "Enter Subject Name:")

if not SUBJECT_NAME:
    messagebox.showerror("Error", "⚠ Subject name cannot be empty. Exiting...")
    exit()

# ---------------- Recognizer ----------------
try:
    recognizer = cv2.face.LBPHFaceRecognizer_create()
except AttributeError:
    raise RuntimeError("Install opencv-contrib-python to use LBPH recognizer.")

if os.path.exists(MODEL_PATH):
    recognizer.read(MODEL_PATH)
else:
    messagebox.showwarning("Warning", "Trainer model not found. Train first.")

# ---------------- Load ID → Name Mapping ----------------
id_to_name = {}
if os.path.exists(MAPPING_FILE):
    with open(MAPPING_FILE, "r") as f:
        id_to_name = json.load(f)

# ---------------- Database Setup ----------------
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id TEXT,
    name TEXT,
    subject TEXT,
    timestamp TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS guardians (
    student_id TEXT PRIMARY KEY,
    student_name TEXT,
    guardian_email TEXT
)
""")

conn.commit()

# ---------------- Fetch Guardian Email ----------------
def get_guardian_email(student_id):
    cursor.execute("SELECT guardian_email FROM guardians WHERE student_id = ?", (str(student_id),))
    result = cursor.fetchone()
    if result:
        return result[0]
    return None

# ---------------- EMAIL FUNCTION ----------------
def send_email_alert(student_name, subject, guardian_email):
    sender_email = "ranjeetsingh79386@gmail.com"                 # <-- CHANGE THIS
    app_password = "szrolhuutwlnlide"           # <-- CHANGE THIS

    subject_line = f"Attendance Alert: {student_name}"
    body = f"""
    Dear Guardian,

    This is to inform you that **{student_name}** has been marked present for the subject **{subject}** 
    at {datetime.now().strftime('%H:%M:%S')}.

    Regards,
    AuraFace Attendance System
    """

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = guardian_email
    msg["Subject"] = subject_line
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()

        print(f"📧 Email sent to {guardian_email} for {student_name}")

    except Exception as e:
        print("❌ Email sending failed:", e)

# ---------------- Attendance Logic ----------------
def can_mark_attendance(person_id, subject):
    cursor.execute("""
        SELECT timestamp FROM attendance
        WHERE person_id = ? AND subject = ?
        ORDER BY timestamp DESC LIMIT 1
    """, (str(person_id), subject))
    
    last = cursor.fetchone()

    if not last:
        return True

    last_time = datetime.strptime(last[0], "%Y-%m-%d %H:%M:%S")
    return datetime.now() - last_time >= timedelta(minutes=10)

def mark_attendance(person_id, name, subject):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "INSERT INTO attendance (person_id, name, subject, timestamp) VALUES (?, ?, ?, ?)",
        (str(person_id), name, subject, timestamp)
    )
    conn.commit()

    # Fetch guardian email
    guardian_email = get_guardian_email(person_id)
    if guardian_email:
        send_email_alert(name, subject, guardian_email)
    else:
        print(f"⚠ No guardian email registered for {name}")

    messagebox.showinfo("Attendance Marked", f"✅ {name} marked present for {subject}")

# ---------------- Camera ----------------
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
cam = cv2.VideoCapture(0)

if not cam.isOpened():
    raise RuntimeError("Cannot open camera.")

ROI_SIZE = (200, 200)
CONF_THRESHOLD = 60
font = cv2.FONT_HERSHEY_SIMPLEX

# ---------------- Main Loop ----------------
while True:
    ret, img = cam.read()
    if not ret:
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        face_roi = gray[y:y + h, x:x + w]
        try:
            resized = cv2.resize(face_roi, ROI_SIZE)
        except:
            resized = face_roi

        try:
            id_, conf = recognizer.predict(resized)
        except:
            id_, conf = None, None

        if id_ is not None and conf < CONF_THRESHOLD:
            name = id_to_name.get(str(id_), "Unknown")

            if can_mark_attendance(id_, SUBJECT_NAME):
                mark_attendance(id_, name, SUBJECT_NAME)
                print(f"✅ Attendance marked for {name}")
            else:
                print(f"⏳ {name} already marked recently")

            label = f"{name} ({int(conf)})"
        else:
            label = "Unknown"

        cv2.putText(img, label, (x + 5, y - 10), font, 0.8, (255, 255, 255), 2)

    cv2.imshow(f"Attendance - {SUBJECT_NAME}", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# ---------------- Cleanup ----------------
cam.release()
conn.close()
cv2.destroyAllWindows()
