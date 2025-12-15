import sqlite3
from tkinter import *
from tkinter import ttk, messagebox

DB_PATH = r"D:\5th Sem\Project AuraFAce\student.db"

class AttendanceReport:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Report")
        self.root.geometry("1000x650+200+50")
        self.root.config(bg="lightblue")

        # Variables
        self.var_search_by = StringVar()
        self.var_search_txt = StringVar()

        # Title
        title = Label(self.root, text="Attendance Report Dashboard",
                      font=("Arial", 25, "bold"), bg="navy", fg="white")
        title.pack(side=TOP, fill=X)

        # ---------------- SEARCH FRAME ----------------
        Search_Frame = Frame(self.root, bd=4, relief=RIDGE, bg="lightblue")
        Search_Frame.place(x=20, y=80, width=950, height=80)

        Label(Search_Frame, text="Search By", bg="lightblue",
              font=("Arial", 15, "bold")).grid(row=0, column=0, padx=20, pady=10)

        search_combo = ttk.Combobox(Search_Frame, textvariable=self.var_search_by,
                                    font=("Arial", 12), width=12, state="readonly")
        search_combo["values"] = ("name", "subject", "date")
        search_combo.grid(row=0, column=1, padx=10)

        Entry(Search_Frame, textvariable=self.var_search_txt,
              font=("Arial", 12), width=20).grid(row=0, column=2, padx=10)

        Button(Search_Frame, text="Search", width=12, command=self.search_data,
               bg="darkgreen", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=3, padx=10)

        Button(Search_Frame, text="Show All", width=12, command=self.fetch_data,
               bg="darkblue", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=4, padx=10)

        # ---------------- TABLE FRAME ----------------
        Table_Frame = Frame(self.root, bd=4, relief=RIDGE, bg="lightblue")
        Table_Frame.place(x=20, y=180, width=950, height=450)

        scroll_x = Scrollbar(Table_Frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(Table_Frame, orient=VERTICAL)

        self.att_table = ttk.Treeview(Table_Frame,
                                      columns=("id", "name", "subject", "timestamp"),
                                      xscrollcommand=scroll_x.set,
                                      yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.att_table.xview)
        scroll_y.config(command=self.att_table.yview)

        self.att_table.heading("id", text="Student ID")
        self.att_table.heading("name", text="Name")
        self.att_table.heading("subject", text="Subject")
        self.att_table.heading("timestamp", text="Date & Time")

        self.att_table["show"] = "headings"

        self.att_table.column("id", width=120)
        self.att_table.column("name", width=150)
        self.att_table.column("subject", width=150)
        self.att_table.column("timestamp", width=250)

        self.att_table.pack(fill=BOTH, expand=1)

        # Load data initially
        self.fetch_data()
        self.auto_refresh()   # <-- Auto refresh every 1 sec

    # ---------------- FETCH DATA ----------------
    def fetch_data(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT person_id, name, subject, timestamp FROM attendance ORDER BY timestamp DESC")
        rows = cursor.fetchall()

        self.att_table.delete(*self.att_table.get_children())

        for row in rows:
            self.att_table.insert("", END, values=row)

        conn.close()

    # ---------------- SEARCH ----------------
    def search_data(self):
        if self.var_search_by.get() == "":
            messagebox.showerror("Error", "Select search filter")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        if self.var_search_by.get() == "date":
            query = "timestamp LIKE ?"
        else:
            query = f"{self.var_search_by.get()} LIKE ?"

        cursor.execute(f"""
            SELECT person_id, name, subject, timestamp 
            FROM attendance WHERE {query}
        """, ('%' + self.var_search_txt.get() + '%',))

        rows = cursor.fetchall()
        self.att_table.delete(*self.att_table.get_children())

        for row in rows:
            self.att_table.insert("", END, values=row)

        conn.close()

    # ---------------- AUTO REFRESH ----------------
    def auto_refresh(self):
        self.fetch_data()
        self.root.after(1000, self.auto_refresh)  # refresh every 1 sec


# Run Window
root = Tk()
AttendanceReport(root)
root.mainloop()
