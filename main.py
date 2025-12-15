import sqlite3
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import ttk, Toplevel, messagebox

class AuraFace:
    def open_student_details(self):
        import subprocess
        subprocess.Popen(["python", "Modules/Student.py"])

    def open_face_detection(self):
        import subprocess
        import sys
        subprocess.Popen([sys.executable, "Modules/Face_Detect.py"])

    def open_attendance(self):
        import subprocess, sys
        from tkinter import simpledialog, messagebox

        # Ask for subject before running Attendance
        subject = simpledialog.askstring("Attendance", "Enter Subject Name:")
        if not subject:
            messagebox.showwarning("Warning", "Subject name is required!")
            return

        # Pass subject name to Attendance.py
        subprocess.Popen([sys.executable, "Modules/Attendance.py", subject])
        
    def open_help_desk(self):
        import subprocess
        subprocess.Popen(["python", "Modules/Help.py"])
        

    def open_photos(self):
        import os
        os.startfile(r"D:\5th Sem\Project AuraFAce\Dataset")  # Opens folder

    def open_developer(self):
        import subprocess
        subprocess.Popen(["python", "Modules/Developer.py"])

    def open_train_data(self):
        import subprocess, sys
        subprocess.Popen([sys.executable, "Modules/trainer.py"])
    
    def open_view_attendance(self):
        """Open a new window to show attendance database"""
        try:
            # Connect to SQLite database
            conn = sqlite3.connect(r"D:\5th Sem\Project AuraFAce\student.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM attendance")  # table name must be 'attendance'
            rows = cursor.fetchall()

            if not rows:
                messagebox.showinfo("No Data", "No attendance records found.")
                return

            # Create new window
            top = Toplevel(self.root)
            top.title("Attendance Records")
            top.geometry("800x500")

            # Table
            cols = [description[0] for description in cursor.description]
            tree = ttk.Treeview(top, columns=cols, show="headings")
            tree.pack(fill="both", expand=True)

            # Add headings
            for col in cols:
                tree.heading(col, text=col)
                tree.column(col, width=150)

            # Insert rows
            for row in rows:
                tree.insert("", "end", values=row)

            conn.close()

        except Exception as e:
            messagebox.showerror("Error", f"Unable to open database.\n{e}")      

    def exit_app(self):
        self.root.destroy()
 
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("AuraFace")
        
        # FIRST IMAGE
        img=Image.open(r"D:\5th Sem\Project AuraFAce\Dataset\giet.jpg")
        img=img.resize((300,125),Image.LANCZOS)
        self.photoimg=ImageTk.PhotoImage(img)

        f_lbl=Label(self.root,image=self.photoimg)
        f_lbl.place(x=350,y=0,width=300,height=130)


        # FIRST IMAGE
        img13=Image.open(r"D:\5th Sem\Project AuraFAce\Dataset\Label Image 1.jpg")
        img13=img13.resize((350,125),Image.LANCZOS)
        self.photoimg13=ImageTk.PhotoImage(img13)

        f_lbl=Label(self.root,image=self.photoimg13)
        f_lbl.place(x=0,y=0,width=350,height=130)


        # Second Image
        img1=Image.open(r"D:\5th Sem\Project AuraFAce\Dataset\Logo.png")
        img1=img1.resize((450,400),Image.LANCZOS)
        self.photoimg1=ImageTk.PhotoImage(img1)

        f_lbl=Label(self.root,image=self.photoimg1)
        f_lbl.place(x=650,y=0,width=450,height=130)

        
        # Third Image
        img2=Image.open(r"D:\5th Sem\Project AuraFAce\Dataset\third image.avif")
        img2=img2.resize((500,150),Image.LANCZOS)
        self.photoimg2=ImageTk.PhotoImage(img2)

        f_lbl=Label(self.root,image=self.photoimg2)
        f_lbl.place(x=1100,y=0,width=500,height=130)

        # Background Image
        img3=Image.open(r"D:\5th Sem\Project AuraFAce\Dataset\background image1.jpg")
        img3=img3.resize((1530,710),Image.LANCZOS)
        self.photoimg3=ImageTk.PhotoImage(img3)

        bg_img=Label(self.root,image=self.photoimg3)
        bg_img.place(x=0,y=130,width=1530,height=710)

        # Title
        title_lbl=Label(bg_img,text="",font=("times new roman",35,"bold"),bg="white",fg="red")
        title_lbl.place(x=0,y=0,width=1530,height=30)


        # Student Button (Student Details)
        img4=Image.open(r"D:\5th Sem\Project AuraFAce\Dataset\Student detail button.webp")
        img4=img4.resize((350,350),Image.LANCZOS)
        self.photoimg4=ImageTk.PhotoImage(img4)

        b1=Button(bg_img,image=self.photoimg4,cursor="hand2",command=self.open_student_details)
        b1.place(x=200,y=100,width=220,height=220)
        
        b1_1=Button(bg_img,text="Student Details",cursor="hand2",font=("times new roman",20,"bold"),bg="darkblue",fg="white")
        b1_1.place(x=200,y=300,width=220,height=40)

        # Student Button (Face Detection)
        img5=Image.open(r"D:\5th Sem\Project AuraFAce\Dataset\face_detect Button.jpg")
        img5=img5.resize((440,320),Image.LANCZOS)
        self.photoimg5=ImageTk.PhotoImage(img5)

        b1=Button(bg_img,image=self.photoimg5,cursor="hand2", command=self.open_face_detection)
        b1.place(x=500,y=100,width=220,height=220)
        
        b1_1=Button(bg_img,text="Face Detection ",cursor="hand2",font=("times new roman",20,"bold"),bg="darkblue",fg="white")
        b1_1.place(x=500,y=300,width=220,height=40)

        # Student Button (Attendance)
        img6=Image.open(r"D:\5th Sem\Project AuraFAce\Dataset\attendance button.jpg")
        img6=img6.resize((250,220),Image.LANCZOS)
        self.photoimg6=ImageTk.PhotoImage(img6)

        b1=Button(bg_img,image=self.photoimg6,cursor="hand2", command=self.open_attendance)
        b1.place(x=800,y=100,width=220,height=220)
        
        b1_1=Button(bg_img,text="Attendance ",cursor="hand2",font=("times new roman",20,"bold"),bg="darkblue",fg="white")
        b1_1.place(x=800,y=300,width=220,height=40)

        # Student Button (Help Desk)
        img7=Image.open(r"D:\5th Sem\Project AuraFAce\Dataset\Help Desk.jpg")
        img7=img7.resize((180,180),Image.LANCZOS)
        self.photoimg7=ImageTk.PhotoImage(img7)

        b1=Button(bg_img,image=self.photoimg7,cursor="hand2", command=self.open_help_desk)
        b1.place(x=1100,y=380,width=220,height=220)
        
        b1_1=Button(bg_img,text="Help Desk ",cursor="hand2",font=("times new roman",20,"bold"),bg="darkblue",fg="white")
        b1_1.place(x=1100,y=580,width=220,height=40)

        # Student Button (Train Data )
        img8=Image.open(r"D:\5th Sem\Project AuraFAce\Dataset\Train Data.jpg")
        img8=img8.resize((220,220),Image.LANCZOS)
        self.photoimg8=ImageTk.PhotoImage(img8)

        b1=Button(bg_img,image=self.photoimg8,cursor="hand2", command=self.open_train_data)
        b1.place(x=200,y=380,width=220,height=220)
        
        b1_1=Button(bg_img,text="Train Data ",cursor="hand2",font=("times new roman",20,"bold"),bg="darkblue",fg="white")
        b1_1.place(x=200,y=580,width=220,height=40)

        # Student Button (Photos )
        img9=Image.open(r"D:\5th Sem\Project AuraFAce\Dataset\photo gallery button.webp")
        img9=img9.resize((350,220),Image.LANCZOS)
        self.photoimg9=ImageTk.PhotoImage(img9)

        b1=Button(bg_img,image=self.photoimg9,cursor="hand2", command=self.open_photos)
        b1.place(x=500,y=380,width=220,height=220)
        
        b1_1=Button(bg_img,text="Photos ",cursor="hand2",font=("times new roman",20,"bold"),bg="darkblue",fg="white")
        b1_1.place(x=500,y=580,width=220,height=40)

        # Student Button (Developer )
        img10=Image.open(r"D:\5th Sem\Project AuraFAce\Dataset\Developer.jpg")
        img10=img10.resize((220,220),Image.LANCZOS)
        self.photoimg10=ImageTk.PhotoImage(img10)

        b1=Button(bg_img,image=self.photoimg10,cursor="hand2", command=self.open_developer)
        b1.place(x=800,y=380,width=220,height=220)
        
        b1_1=Button(bg_img,text="Developer ",cursor="hand2",font=("times new roman",20,"bold"),bg="darkblue",fg="white")
        b1_1.place(x=800,y=580,width=220,height=40)

        # Student Button (Exit )
        img11=Image.open(r"D:\5th Sem\Project AuraFAce\Dataset\Exit.jpg")
        img11=img11.resize((100,100),Image.LANCZOS)
        self.photoimg11=ImageTk.PhotoImage(img11)

        b1=Button(bg_img,image=self.photoimg11,cursor="hand2", command=self.exit_app)
        b1.place(x=1420,y=40,width=100,height=100)
        
        # Student Button (View Attendance)
        img12=Image.open(r"D:\5th Sem\Project AuraFAce\Dataset\View_attendance.png")
        img12=img12.resize((250,220),Image.LANCZOS)
        self.photoimg12=ImageTk.PhotoImage(img12)

        b1=Button(bg_img,image=self.photoimg12,cursor="hand2", command=self.open_view_attendance)
        b1.place(x=1100,y=100,width=220,height=220)
        
        b1_1=Button(bg_img,text="View Attendance ",cursor="hand2",font=("times new roman",20,"bold"),bg="darkblue",fg="white")
        b1_1.place(x=1100,y=300,width=220,height=40)

if __name__== "__main__":
    root=Tk()
    obj=AuraFace(root)
    root.mainloop()