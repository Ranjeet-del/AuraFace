# help_desk.py
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import webbrowser

class HelpDesk:
    def __init__(self, root):
        self.root = root
        self.root.title("Help Desk - Face Detection Student Management")
        self.root.geometry("900x550")
        self.root.configure(bg="#0f172a")

        # Main Frame
        main_frame = tk.Frame(self.root, bg="#0f172a")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Load Help Desk Image
        img_path = os.path.join("Dataset", "Help Desk.jpg")
        try:
            img = Image.open(img_path)
            img = img.resize((270, 270))
            self.photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(main_frame, image=self.photo, bg="#0f172a")
            img_label.grid(row=0, column=0, rowspan=4, padx=20, pady=10)
        except FileNotFoundError:
            tk.Label(main_frame, text="[Help Desk Image Missing]", fg="red", bg="#0f172a").grid(row=0, column=0)

        # Title
        title_label = tk.Label(
            main_frame,
            text="💡 Help Desk",
            font=("Arial", 28, "bold"),
            fg="#22c55e",
            bg="#0f172a"
        )
        title_label.grid(row=0, column=1, sticky="w", pady=(10, 15))

        # Contact Information Frame
        contact_frame = tk.LabelFrame(
            main_frame, text="📞 Contact Information",
            font=("Arial", 12, "bold"), fg="#f9fafb",
            bg="#1f2937", bd=2, relief="ridge", padx=10, pady=10
        )
        contact_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        contact_details = [
            "📧 Email: support@auraface.com",
            "📱 Phone: +91-7847982493",
            "⏰ Working Hours: Mon–Sat, 9 AM – 6 PM"
        ]
        for detail in contact_details:
            tk.Label(contact_frame, text=detail, bg="#1f2937", fg="white", font=("Arial", 11)).pack(anchor="w", pady=3)

        # FAQ Frame
        faq_frame = tk.LabelFrame(
            main_frame, text="❓ Frequently Asked Questions",
            font=("Arial", 12, "bold"), fg="#f9fafb",
            bg="#1f2937", bd=2, relief="ridge", padx=10, pady=10
        )
        faq_frame.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)

        faqs = [
            ("Q: What to do if my face is not detected?",
             "👉 Ensure good lighting and face is in front of camera."),
            ("Q: Attendance not marked?",
             "👉 Check internet connection or restart the software."),
            ("Q: Forgot password?",
             "👉 Click 'Forgot Password' on the login page.")
        ]

        for q, a in faqs:
            q_label = tk.Label(faq_frame, text=q, bg="#1f2937", fg="#60a5fa", font=("Arial", 11, "bold"))
            q_label.pack(anchor="w", pady=(5, 1))
            a_label = tk.Label(faq_frame, text=a, bg="#1f2937", fg="white", font=("Arial", 10))
            a_label.pack(anchor="w", padx=20, pady=(0, 5))

        # Developer Info Frame
        dev_frame = tk.LabelFrame(
            main_frame, text="👨‍💻 Developer Info",
            font=("Arial", 12, "bold"), fg="#f9fafb",
            bg="#1f2937", bd=2, relief="ridge", padx=10, pady=10
        )
        dev_frame.grid(row=3, column=1, sticky="nsew", padx=5, pady=5)

        dev_details = [
            "🔹 Project: AuraFace - Face Recognition Attendance System",
            "🔹 Developed By: Gayatri Dhal , Arun Kumar Bisoyi and Ranjeet Singh Baghel",
            "🔹 Version: 1.0 (2025)"
        ]
        for detail in dev_details:
            tk.Label(dev_frame, text=detail, bg="#1f2937", fg="white", font=("Arial", 11)).pack(anchor="w", pady=2)

        # Hover Effect Buttons
        button_frame = tk.Frame(main_frame, bg="#0f172a")
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)

        style = {"font": ("Arial", 12, "bold"), "width": 15, "height": 2, "bd": 0}

        btn1 = tk.Button(button_frame, text="📚 User Guide", bg="#22c55e", fg="white", **style, command=self.open_user_guide)
        btn2 = tk.Button(button_frame, text="🌐 Visit Website", bg="#3b82f6", fg="white", **style, command=self.open_website)
        btn3 = tk.Button(button_frame, text="❌ Exit", bg="#ef4444", fg="white", **style, command=self.root.quit)

        for btn in (btn1, btn2, btn3):
            btn.pack(side="left", padx=10)

            # Add Hover Effect
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#0ea5e9"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(
                bg="#22c55e" if "Guide" in b.cget("text")
                else "#3b82f6" if "Website" in b.cget("text")
                else "#ef4444"
            ))

    def open_user_guide(self):
        """Opens a local PDF guide if available."""
        pdf_path = os.path.join("Docs", "UserGuide.pdf")  # put our PDF here
        if os.path.exists(pdf_path):
            os.startfile(pdf_path)  # Windows
        else:
            tk.messagebox.showerror("Error", "User Guide not found!")

    def open_website(self):
        """Opens official website in browser."""
        webbrowser.open("https://AuraFace.com")  # Replace with our real website

if __name__ == "__main__":
    root = tk.Tk()
    app = HelpDesk(root)
    root.mainloop()
