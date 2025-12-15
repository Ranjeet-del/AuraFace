import sqlite3
import os
import time
from tkinter import *
from tkinter import ttk, messagebox, filedialog

DB_PATH = r"D:\5th Sem\Project AuraFAce\student.db"

class Student:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Details")
        self.root.geometry("1400x700+50+10")

        # DB change tracker
        self.last_modified = 0
        self.last_hash = None

        # Variables
        self.var_id = StringVar()
        self.var_name = StringVar()
        self.var_roll = StringVar()
        self.var_email = StringVar()
        self.var_gender = StringVar()
        self.var_phone = StringVar()
        self.var_guardian = StringVar()
        self.var_guardian_email = StringVar()
        self.var_address = StringVar()
        self.var_photo = StringVar()

        self.var_search_by = StringVar()
        self.var_search_txt = StringVar()

        # Title
        title = Label(self.root, text="Student Details",
                      font=("times new roman", 20, "bold"),
                      bg="navy", fg="white")
        title.pack(side=TOP, fill=X)

        # Manage Frame
        Manage_Frame = Frame(self.root, bd=4, relief=RIDGE, bg="lightblue")
        Manage_Frame.place(x=20, y=60, width=480, height=620)

        m_title = Label(Manage_Frame, text="Manage Students",
                        bg="lightblue", fg="black",
                        font=("times new roman", 20, "bold"))
        m_title.grid(row=0, columnspan=2, pady=10)

        # Labels and Entry fields
        labels = ["Student ID", "Name", "Roll No", "Email", "Gender",
                  "Phone", "Guardian Phone", "Guardian Email", "Address"]
        vars = [
            self.var_id, self.var_name, self.var_roll, self.var_email,
            self.var_gender, self.var_phone, self.var_guardian,
            self.var_guardian_email, self.var_address
        ]

        for i, (text, var) in enumerate(zip(labels, vars), start=1):
            Label(Manage_Frame, text=text, bg="lightblue",
                  font=("times new roman", 15, "bold")).grid(row=i, column=0,
                                                             pady=10, padx=20, sticky="w")
            Entry(Manage_Frame, textvariable=var,
                  font=("times new roman", 13, "bold"),
                  bd=5, relief=GROOVE).grid(row=i, column=1, pady=10, padx=20, sticky="w")

        # Gender ComboBox
        combo_gender = ttk.Combobox(Manage_Frame, textvariable=self.var_gender,
                                    font=("times new roman", 13, "bold"), state='readonly')
        combo_gender['values'] = ("Male", "Female", "Other")
        combo_gender.grid(row=5, column=1, pady=10, padx=20, sticky="w")

        # Photo
        Label(Manage_Frame, text="Photo", bg="lightblue",
              font=("times new roman", 15, "bold")).grid(row=10, column=0, pady=10, padx=20, sticky="w")
        txt_photo = Entry(Manage_Frame, textvariable=self.var_photo,
                          font=("times new roman", 13, "bold"), bd=5, relief=GROOVE,
                          state="readonly")
        txt_photo.grid(row=10, column=1, pady=10, padx=20, sticky="w")

        Button(Manage_Frame, text="Browse", command=self.browse_photo).grid(row=10, column=2, pady=10)

        # Button Frame
        btn_frame = Frame(Manage_Frame, bd=4, relief=RIDGE, bg="lightblue")
        btn_frame.place(x=10, y=560, width=450)

        Button(btn_frame, text="Save", width=10, command=self.add_students).grid(row=0, column=0, padx=10, pady=10)
        Button(btn_frame, text="Update", width=10, command=self.update_data).grid(row=0, column=1, padx=10, pady=10)
        Button(btn_frame, text="Delete", width=10, command=self.delete_data).grid(row=0, column=2, padx=10, pady=10)
        Button(btn_frame, text="Reset", width=10, command=self.clear).grid(row=0, column=3, padx=10, pady=10)

        # Detail Frame
        Detail_Frame = Frame(self.root, bd=4, relief=RIDGE, bg="lightblue")
        Detail_Frame.place(x=520, y=60, width=850, height=620)

        Label(Detail_Frame, text="Search By", bg="lightblue",
              font=("times new roman", 15, "bold")).grid(row=0, column=0, pady=10, padx=20, sticky="w")

        combo_search = ttk.Combobox(Detail_Frame, textvariable=self.var_search_by,
                                    width=12, font=("times new roman", 13, "bold"),
                                    state='readonly')
        combo_search['values'] = ("id", "name", "roll", "phone", "guardian_phone", "guardian_email")
        combo_search.grid(row=0, column=1, padx=20, pady=10)

        txt_search = Entry(Detail_Frame, textvariable=self.var_search_txt, width=15,
                           font=("times new roman", 13, "bold"), bd=5, relief=GROOVE)
        txt_search.grid(row=0, column=2, pady=10, padx=20, sticky="w")

        Button(Detail_Frame, text="Search", width=12,
               command=self.search_data).grid(row=0, column=3, padx=10, pady=10)
        Button(Detail_Frame, text="Show All", width=12,
               command=self.fetch_data).grid(row=0, column=4, padx=10, pady=10)

        # Table Frame
        Table_Frame = Frame(Detail_Frame, bd=4, relief=RIDGE, bg="lightblue")
        Table_Frame.place(x=10, y=70, width=830, height=530)

        scroll_x = Scrollbar(Table_Frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(Table_Frame, orient=VERTICAL)

        self.Student_table = ttk.Treeview(
            Table_Frame,
            columns=("id", "name", "roll", "email", "gender",
                     "phone", "guardian_phone", "guardian_email", "address", "photo"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.Student_table.xview)
        scroll_y.config(command=self.Student_table.yview)

        for col in ("id", "name", "roll", "email", "gender",
                    "phone", "guardian_phone", "guardian_email",
                    "address", "photo"):
            self.Student_table.heading(col, text=col.replace("_", " ").title())

        self.Student_table['show'] = 'headings'

        # Set column width
        column_sizes = {
            "id": 70, "name": 120, "roll": 100, "email": 150,
            "gender": 70, "phone": 110, "guardian_phone": 120,
            "guardian_email": 150, "address": 150, "photo": 150
        }

        for col, width in column_sizes.items():
            self.Student_table.column(col, width=width)

        self.Student_table.pack(fill=BOTH, expand=1)
        self.Student_table.bind("<ButtonRelease-1>", self.get_cursor)

        # Setup DB
        self.create_db()
        self.create_guardian_table()
        self.fetch_data()

        # Auto refresh
        self.root.after(1000, self.detect_db_change)

    # ---------------- PHOTO ----------------
    def browse_photo(self):
        file = filedialog.askopenfilename(
            title="Select Photo",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
        )
        if file:
            self.var_photo.set(file)

    # ---------------- DATABASE ----------------
    def create_db(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS student (
                id TEXT PRIMARY KEY,
                name TEXT,
                roll TEXT,
                email TEXT,
                gender TEXT,
                phone TEXT,
                guardian TEXT,
                guardian_email TEXT,
                address TEXT,
                photo TEXT
            )
        """)
        conn.commit()
        conn.close()

    def create_guardian_table(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS guardians (
                student_id TEXT PRIMARY KEY,
                student_name TEXT,
                guardian_phone TEXT,
                guardian_email TEXT
            )
        """)
        conn.commit()
        conn.close()

    # ---------------- AUTO REFRESH ----------------
    def get_table_hash(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT * FROM student")
        data1 = cur.fetchall()
        cur.execute("SELECT * FROM guardians")
        data2 = cur.fetchall()
        conn.close()
        return hash(str(data1) + str(data2))

    def detect_db_change(self):
        try:
            mod = os.path.getmtime(DB_PATH)
            if mod != self.last_modified:
                self.last_modified = mod
                new_hash = self.get_table_hash()

                if new_hash != self.last_hash:
                    self.last_hash = new_hash
                    self.fetch_data()

        except:
            pass

        self.root.after(1000, self.detect_db_change)

    # ---------------- CRUD ----------------
    def add_students(self):
        if self.var_id.get() == "" or self.var_name.get() == "":
            messagebox.showerror("Error", "All fields are required!")
            return

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        try:
            cur.execute("""
                INSERT INTO student VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.var_id.get(), self.var_name.get(), self.var_roll.get(),
                  self.var_email.get(), self.var_gender.get(), self.var_phone.get(),
                  self.var_guardian.get(), self.var_guardian_email.get(),
                  self.var_address.get(), self.var_photo.get()))

            cur.execute("""
                INSERT OR REPLACE INTO guardians(student_id, student_name, guardian_phone, guardian_email)
                VALUES (?, ?, ?, ?)
            """, (self.var_id.get(), self.var_name.get(),
                  self.var_guardian.get(), self.var_guardian_email.get()))

            conn.commit()
            self.fetch_data()
            self.clear()
            messagebox.showinfo("Success", "Record Added Successfully!")

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Student ID already exists!")

        conn.close()

    def fetch_data(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            SELECT s.id, s.name, s.roll, s.email, s.gender,
                   s.phone, COALESCE(g.guardian_phone, s.guardian),
                   COALESCE(g.guardian_email, s.guardian_email),
                   s.address, s.photo
            FROM student s
            LEFT JOIN guardians g ON s.id = g.student_id
        """)
        rows = cur.fetchall()
        conn.close()

        self.Student_table.delete(*self.Student_table.get_children())

        for row in rows:
            self.Student_table.insert("", END, values=row)

    def clear(self):
        self.var_id.set("")
        self.var_name.set("")
        self.var_roll.set("")
        self.var_email.set("")
        self.var_gender.set("")
        self.var_phone.set("")
        self.var_guardian.set("")
        self.var_guardian_email.set("")
        self.var_address.set("")
        self.var_photo.set("")

    def get_cursor(self, ev):
        row = self.Student_table.item(self.Student_table.focus())['values']
        if row:
            self.var_id.set(row[0])
            self.var_name.set(row[1])
            self.var_roll.set(row[2])
            self.var_email.set(row[3])
            self.var_gender.set(row[4])
            self.var_phone.set(row[5])
            self.var_guardian.set(row[6])
            self.var_guardian_email.set(row[7])
            self.var_address.set(row[8])
            self.var_photo.set(row[9])

    def update_data(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("""
            UPDATE student SET name=?, roll=?, email=?, gender=?, 
                               phone=?, guardian=?, guardian_email=?, 
                               address=?, photo=? WHERE id=?
        """, (self.var_name.get(), self.var_roll.get(), self.var_email.get(),
              self.var_gender.get(), self.var_phone.get(),
              self.var_guardian.get(), self.var_guardian_email.get(),
              self.var_address.get(), self.var_photo.get(),
              self.var_id.get()))

        cur.execute("""
            INSERT OR REPLACE INTO guardians(student_id, student_name, guardian_phone, guardian_email)
            VALUES (?, ?, ?, ?)
        """, (self.var_id.get(), self.var_name.get(),
              self.var_guardian.get(), self.var_guardian_email.get()))

        conn.commit()
        conn.close()

        self.fetch_data()
        self.clear()
        messagebox.showinfo("Success", "Record Updated Successfully!")

    def delete_data(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("DELETE FROM student WHERE id=?", (self.var_id.get(),))
        cur.execute("DELETE FROM guardians WHERE student_id=?", (self.var_id.get(),))

        conn.commit()
        conn.close()

        self.fetch_data()
        self.clear()
        messagebox.showinfo("Success", "Record Deleted Successfully!")

    def search_data(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        field = self.var_search_by.get()
        cur.execute(f"""
            SELECT s.id, s.name, s.roll, s.email, s.gender,
                   s.phone, COALESCE(g.guardian_phone, s.guardian),
                   COALESCE(g.guardian_email, s.guardian_email),
                   s.address, s.photo
            FROM student s
            LEFT JOIN guardians g ON s.id = g.student_id
            WHERE {field} LIKE ?
        """, ('%' + self.var_search_txt.get() + '%',))

        rows = cur.fetchall()
        conn.close()

        self.Student_table.delete(*self.Student_table.get_children())

        for row in rows:
            self.Student_table.insert("", END, values=row)


root = Tk()
ob = Student(root)
root.mainloop()