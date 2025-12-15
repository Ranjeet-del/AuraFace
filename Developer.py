# developer_options.py
import os
import sys
import json
import cv2
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
from datetime import datetime

class DeveloperOptions:
    def __init__(self, root):
        self.root = root
        self.root.title("Developer Options - AuraFace")
        self.root.geometry("960x600")
        self.root.configure(bg="#0f172a")

        # ======= Defaults (EDIT IF YOUR STRUCTURE IS DIFFERENT) =======
        self.var_dataset_dir   = tk.StringVar(value=os.path.abspath("Dataset"))
        self.var_trainer_py    = tk.StringVar(value=os.path.abspath(os.path.join("Modules", "trainer.py")) if os.path.exists("Modules") else os.path.abspath("trainer.py"))
        self.var_register_py   = tk.StringVar(value=os.path.abspath(os.path.join("Modules", "register_face.py")) if os.path.exists("Modules") else os.path.abspath("register_face.py"))
        self.var_trainer_yml   = tk.StringVar(value=os.path.abspath(os.path.join("trainer", "trainer.yml")) if os.path.exists("trainer") else os.path.abspath("trainer.yml"))
        self.var_cascade_path  = tk.StringVar(value=os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml"))
        self.var_logs_dir      = tk.StringVar(value=os.path.abspath("logs"))

        os.makedirs(self.var_logs_dir.get(), exist_ok=True)

        # ======= Title =======
        title = tk.Label(self.root, text="🛠️ Developer Options",
                         bg="#0f172a", fg="#22c55e",
                         font=("Segoe UI", 24, "bold"))
        title.pack(pady=10)

        # ======= Content Frame =======
        main = tk.Frame(self.root, bg="#0f172a")
        main.pack(fill="both", expand=True, padx=14, pady=8)
        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)

        # ======= Environment / Paths =========
        paths_frame = tk.LabelFrame(main, text="Environment & Paths",
                                    bg="#1f2937", fg="#f9fafb",
                                    font=("Segoe UI", 11, "bold"),
                                    bd=2, relief="ridge", padx=10, pady=10)
        paths_frame.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)

        self._add_path_row(paths_frame, "Dataset Dir:", self.var_dataset_dir, self.browse_dataset, 0)
        self._add_path_row(paths_frame, "trainer.py:", self.var_trainer_py, self.browse_trainer, 1)
        self._add_path_row(paths_frame, "register_face.py:", self.var_register_py, self.browse_register, 2)
        self._add_path_row(paths_frame, "trainer.yml:", self.var_trainer_yml, self.browse_trainer_yml, 3)
        self._add_path_row(paths_frame, "Haarcascade:", self.var_cascade_path, self.browse_cascade, 4)
        self._add_path_row(paths_frame, "Logs Folder:", self.var_logs_dir, self.browse_logs, 5)

        # Environment info + quick checks
        env_frame = tk.Frame(paths_frame, bg="#1f2937")
        env_frame.grid(row=6, column=0, columnspan=3, sticky="ew", pady=(8,0))
        tk.Button(env_frame, text="Check Environment", command=self.check_environment,
                  bg="#3b82f6", fg="white", bd=0, width=18, height=1, font=("Segoe UI", 10, "bold")).pack(side="left", padx=4)
        tk.Button(env_frame, text="Verify Files", command=self.verify_files,
                  bg="#22c55e", fg="white", bd=0, width=14, height=1, font=("Segoe UI", 10, "bold")).pack(side="left", padx=4)
        tk.Button(env_frame, text="Open Dataset", command=lambda: self.open_folder(self.var_dataset_dir.get()),
                  bg="#64748b", fg="white", bd=0, width=14, height=1, font=("Segoe UI", 10, "bold")).pack(side="left", padx=4)
        tk.Button(env_frame, text="Open Logs", command=lambda: self.open_folder(self.var_logs_dir.get()),
                  bg="#64748b", fg="white", bd=0, width=14, height=1, font=("Segoe UI", 10, "bold")).pack(side="left", padx=4)

        # ======= Dataset Tools =======
        ds_frame = tk.LabelFrame(main, text="Dataset Tools",
                                 bg="#1f2937", fg="#f9fafb",
                                 font=("Segoe UI", 11, "bold"),
                                 bd=2, relief="ridge", padx=10, pady=10)
        ds_frame.grid(row=0, column=1, sticky="nsew", padx=6, pady=6)

        tk.Button(ds_frame, text="Count Images", command=self.count_images,
                  bg="#3b82f6", fg="white", bd=0, width=16, height=2, font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=6, pady=6, sticky="ew")
        tk.Button(ds_frame, text="Build ID→Name Map", command=self.build_id_name_map,
                  bg="#22c55e", fg="white", bd=0, width=18, height=2, font=("Segoe UI", 10, "bold")).grid(row=0, column=1, padx=6, pady=6, sticky="ew")
        tk.Button(ds_frame, text="Open ID Map", command=self.open_id_map,
                  bg="#64748b", fg="white", bd=0, width=16, height=2, font=("Segoe UI", 10, "bold")).grid(row=1, column=0, padx=6, pady=6, sticky="ew")
        tk.Button(ds_frame, text="Validate Haarcascade", command=self.validate_cascade,
                  bg="#f59e0b", fg="white", bd=0, width=18, height=2, font=("Segoe UI", 10, "bold")).grid(row=1, column=1, padx=6, pady=6, sticky="ew")

        for i in range(2):
            ds_frame.grid_columnconfigure(i, weight=1)

        # ======= Actions =======
        actions = tk.LabelFrame(main, text="Actions",
                                bg="#1f2937", fg="#f9fafb",
                                font=("Segoe UI", 11, "bold"),
                                bd=2, relief="ridge", padx=10, pady=10)
        actions.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=6, pady=6)

        btn_style = {"bd": 0, "height": 2, "font": ("Segoe UI", 11, "bold")}
        tk.Button(actions, text="▶ Test Camera", command=self.test_camera,
                  bg="#3b82f6", fg="white", width=16, **btn_style).grid(row=0, column=0, padx=8, pady=8, sticky="ew")
        tk.Button(actions, text="🧠 Train Model (LBPH)", command=self.train_model,
                  bg="#22c55e", fg="white", width=20, **btn_style).grid(row=0, column=1, padx=8, pady=8, sticky="ew")
        tk.Button(actions, text="➕ Register New Face", command=self.launch_register_face,
                  bg="#10b981", fg="white", width=20, **btn_style).grid(row=0, column=2, padx=8, pady=8, sticky="ew")
        tk.Button(actions, text="📄 View Last Log", command=self.view_last_log,
                  bg="#64748b", fg="white", width=16, **btn_style).grid(row=0, column=3, padx=8, pady=8, sticky="ew")

        for i in range(4):
            actions.grid_columnconfigure(i, weight=1)

        # ======= Console Area =======
        console_frame = tk.LabelFrame(main, text="Console",
                                      bg="#1f2937", fg="#f9fafb",
                                      font=("Segoe UI", 11, "bold"),
                                      bd=2, relief="ridge", padx=8, pady=6)
        console_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=6, pady=6)
        self.console = tk.Text(console_frame, height=8, bg="#0b1220", fg="#e5e7eb",
                               insertbackground="#e5e7eb", font=("Consolas", 10))
        self.console.pack(fill="both", expand=True)
        self.log("Developer Options loaded.")

        # Hover style for Buttons (simple)
        self._attach_hover(self.root)

    # ---------- UI helpers ----------
    def _add_path_row(self, parent, label, var, browse_cmd, row):
        tk.Label(parent, text=label, bg="#1f2937", fg="#f9fafb",
                 font=("Segoe UI", 10, "bold")).grid(row=row, column=0, sticky="w", pady=3)
        entry = tk.Entry(parent, textvariable=var, bg="#111827", fg="#e5e7eb",
                         insertbackground="#e5e7eb", width=60, bd=1, relief="solid")
        entry.grid(row=row, column=1, padx=6, pady=3, sticky="ew")
        tk.Button(parent, text="Browse", command=browse_cmd,
                  bg="#334155", fg="white", bd=0, width=10, font=("Segoe UI", 10, "bold")).grid(row=row, column=2, padx=4, pady=3)

        parent.grid_columnconfigure(1, weight=1)

    def _attach_hover(self, widget):
        for child in widget.winfo_children():
            if isinstance(child, tk.Button):
                child.bind("<Enter>", lambda e, b=child: b.config(bg="#0ea5e9"))
                child.bind("<Leave>", lambda e, b=child: b.config(bg=b._orig_bg if hasattr(b, "_orig_bg") else b.cget("bg")))
                if not hasattr(child, "_orig_bg"):
                    child._orig_bg = child.cget("bg")
            self._attach_hover(child) if hasattr(child, "winfo_children") else None

    # ---------- Browsers ----------
    def browse_dataset(self):
        path = filedialog.askdirectory(title="Select Dataset Folder", initialdir=self.var_dataset_dir.get() or os.getcwd())
        if path:
            self.var_dataset_dir.set(path)

    def browse_trainer(self):
        path = filedialog.askopenfilename(title="Select trainer.py", filetypes=[("Python Files", "*.py")])
        if path:
            self.var_trainer_py.set(path)

    def browse_register(self):
        path = filedialog.askopenfilename(title="Select register_face.py", filetypes=[("Python Files", "*.py")])
        if path:
            self.var_register_py.set(path)

    def browse_trainer_yml(self):
        path = filedialog.askopenfilename(title="Select trainer.yml", filetypes=[("YAML", "*.yml *.yaml"), ("All Files", "*.*")])
        if path:
            self.var_trainer_yml.set(path)

    def browse_cascade(self):
        path = filedialog.askopenfilename(title="Select Haarcascade XML", initialdir=cv2.data.haarcascades,
                                          filetypes=[("XML", "*.xml"), ("All Files", "*.*")])
        if path:
            self.var_cascade_path.set(path)

    def browse_logs(self):
        path = filedialog.askdirectory(title="Select Logs Folder", initialdir=self.var_logs_dir.get() or os.getcwd())
        if path:
            self.var_logs_dir.set(path)

    # ---------- Utilities ----------
    def log(self, text):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.insert("end", f"[{timestamp}] {text}\n")
        self.console.see("end")

    def open_folder(self, path):
        try:
            os.makedirs(path, exist_ok=True)
            if sys.platform.startswith("win"):
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open folder:\n{e}")

    # ---------- Checks ----------
    def check_environment(self):
        try:
            info = [
                f"Python: {sys.version.split()[0]}",
                f"OpenCV: {cv2.__version__}",
                f"Haar Path: {self.var_cascade_path.get()}",
                f"Trainer YML: {self.var_trainer_yml.get()}"
            ]
            self.log("Environment OK:\n  " + "\n  ".join(info))
            messagebox.showinfo("Environment", "\n".join(info))
        except Exception as e:
            self.log(f"Environment check failed: {e}")
            messagebox.showerror("Error", f"Environment check failed:\n{e}")

    def validate_cascade(self):
        path = self.var_cascade_path.get()
        if not os.path.exists(path):
            self.log("Haarcascade file not found.")
            messagebox.showerror("Error", "Haarcascade file not found.")
            return
        try:
            detector = cv2.CascadeClassifier(path)
            if detector.empty():
                raise ValueError("Failed to load cascade (detector empty).")
            self.log("Haarcascade loaded successfully.")
            messagebox.showinfo("Success", "Haarcascade loaded successfully!")
        except Exception as e:
            self.log(f"Cascade validation failed: {e}")
            messagebox.showerror("Error", f"Cascade validation failed:\n{e}")

    def verify_files(self):
        msgs = []
        checks = [
            ("Dataset", os.path.isdir(self.var_dataset_dir.get())),
            ("trainer.py", os.path.isfile(self.var_trainer_py.get())),
            ("register_face.py", os.path.isfile(self.var_register_py.get())),
            ("trainer.yml (optional until trained)", os.path.isfile(self.var_trainer_yml.get())),
            ("Haarcascade", os.path.isfile(self.var_cascade_path.get())),
        ]
        for name, ok in checks:
            msgs.append(f"{'✅' if ok else '❌'} {name}")
        self.log("File verification:\n  " + "\n  ".join(msgs))
        messagebox.showinfo("Verify Files", "\n".join(msgs))

    # ---------- Dataset ops ----------
    def count_images(self):
        base = self.var_dataset_dir.get()
        if not os.path.isdir(base):
            messagebox.showerror("Error", "Dataset folder not found.")
            return
        total = 0
        per_user = {}
        for root, _, files in os.walk(base):
            for f in files:
                if f.lower().endswith((".jpg", ".jpeg", ".png")):
                    total += 1
                    parts = f.split(".")
                    # Accept both 'user.<id>.<name>.<count>.jpg' and '<name>.<count>.jpg'
                    key = None
                    if len(parts) >= 4 and parts[0].lower() == "user" and parts[1].isdigit():
                        key = f"{parts[0]}.{parts[1]}.{parts[2]}"
                    elif len(parts) >= 2:
                        key = parts[0]
                    per_user[key] = per_user.get(key, 0) + 1
        lines = [f"Total images: {total}"] + [f" - {k}: {v}" for k, v in sorted(per_user.items())]
        self.log("\n".join(lines))
        messagebox.showinfo("Dataset Count", "\n".join(lines))

    def build_id_name_map(self):
        """
        Scans dataset filenames like 'user.<id>.<name>.<count>.jpg' and creates id_name_map.json.
        """
        base = self.var_dataset_dir.get()
        if not os.path.isdir(base):
            messagebox.showerror("Error", "Dataset folder not found.")
            return
        id_to_name = {}
        for root, _, files in os.walk(base):
            for f in files:
                if not f.lower().endswith((".jpg", ".jpeg", ".png")):
                    continue
                parts = f.split(".")
                # Expect at least: user.<id>.<name>.<count>.jpg
                if len(parts) >= 4 and parts[0].lower() == "user":
                    _, sid, sname = parts[0], parts[1], parts[2]
                    if sid.isdigit():
                        clean_name = sname.replace("_", " ").strip()
                        id_to_name[int(sid)] = clean_name
        if not id_to_name:
            self.log("No valid 'user.<id>.<name>.*' files found.")
            messagebox.showwarning("ID→Name", "No valid filenames found with pattern 'user.<id>.<name>.<n>.jpg'.")
            return

        # Save
        out_path = os.path.abspath("id_name_map.json")
        try:
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump({str(k): v for k, v in sorted(id_to_name.items())}, f, indent=2, ensure_ascii=False)
            self.log(f"Saved ID→Name map to {out_path}")
            messagebox.showinfo("Success", f"ID→Name map saved:\n{out_path}")
        except Exception as e:
            self.log(f"Failed to write id_name_map.json: {e}")
            messagebox.showerror("Error", f"Failed to write id_name_map.json:\n{e}")

    def open_id_map(self):
        path = os.path.abspath("id_name_map.json")
        if not os.path.exists(path):
            messagebox.showwarning("Missing", "id_name_map.json not found. Build it first.")
            return
        self.open_folder(os.path.dirname(path))

    # ---------- Camera / Training / Launch ----------
    def test_camera(self):
        self.log("Opening camera… Press 'q' to close the preview window.")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            self.log("❌ Could not open camera.")
            messagebox.showerror("Camera", "Could not open camera (index 0).")
            return
        cv2.namedWindow("Camera Test - Press q to Quit", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Camera Test - Press q to Quit", 640, 480)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            cv2.imshow("Camera Test - Press q to Quit", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        self.log("Camera test closed.")

    def train_model(self):
        trainer = self.var_trainer_py.get()
        if not os.path.isfile(trainer):
            messagebox.showerror("Error", "trainer.py not found. Fix the path.")
            return
        self.log("Starting training… This will open a console process.")
        log_file = os.path.join(self.var_logs_dir.get(), f"train_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        try:
            with open(log_file, "w", encoding="utf-8") as lf:
                proc = subprocess.Popen([sys.executable, trainer],
                                        stdout=lf, stderr=lf, cwd=os.path.dirname(trainer) or None)
                proc.wait()
            self.log(f"Training finished. Log saved: {log_file}")
            messagebox.showinfo("Training", f"Training finished.\nLog:\n{log_file}")
        except Exception as e:
            self.log(f"Training failed: {e}")
            messagebox.showerror("Error", f"Training failed:\n{e}")

    def launch_register_face(self):
        register = self.var_register_py.get()
        if not os.path.isfile(register):
            messagebox.showerror("Error", "register_face.py not found. Fix the path.")
            return
        self.log("Launching register_face.py …")
        try:
            subprocess.Popen([sys.executable, register], cwd=os.path.dirname(register) or None)
            self.log("register_face.py launched.")
        except Exception as e:
            self.log(f"Failed to launch register_face.py: {e}")
            messagebox.showerror("Error", f"Failed to launch register_face.py:\n{e}")

    def view_last_log(self):
        folder = self.var_logs_dir.get()
        if not os.path.isdir(folder):
            messagebox.showwarning("Logs", "Logs folder not found.")
            return
        logs = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(".log")]
        if not logs:
            messagebox.showinfo("Logs", "No log files found yet.")
            return
        last = max(logs, key=os.path.getmtime)
        try:
            if sys.platform.startswith("win"):
                os.startfile(last)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", last])
            else:
                subprocess.Popen(["xdg-open", last])
            self.log(f"Opened log: {last}")
        except Exception as e:
            self.log(f"Failed to open log: {e}")
            messagebox.showerror("Error", f"Failed to open log:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DeveloperOptions(root)
    root.mainloop()
