import tkinter as tk
from tkinter import messagebox as msg
from connection import *

class Emergency_contact:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x500")
        self.root.title("Insert Form")
        self.primarycolor = "#E3D3E4"
        self.secondaycolor = "#946E83"
        self.txtcolor = "black"
        self.title = tk.Label(self.root, text="Add Emergency Contact", font=("Arial", "20", "bold"), bg=self.secondaycolor,
                                   fg=self.txtcolor, width=20)
        self.title.pack(pady=20)

        self.formFont = ("Arial", 14)

        self.root.configure(bg=self.secondaycolor)

        self.conn = get_connection()
        self.cur = self.conn.cursor()

        self.formFrame = tk.Frame(self.root, bg=self.primarycolor, highlightthickness=2,
                                       highlightbackground="black")
        self.formFrame.pack()

        self.lb1 = tk.Label(self.formFrame, text="Enter User Id", font=self.formFont, bg=self.primarycolor)
        self.lb1.grid(row=0, column=0, padx=10, pady=10)
        self.txt1 = tk.Entry(self.formFrame, font=self.formFont, relief="raised")
        self.txt1.grid(row=0, column=1, padx=10, pady=10)

        self.lb2 = tk.Label(self.formFrame, text="Enter Name", font=self.formFont, bg=self.primarycolor)
        self.lb2.grid(row=1, column=0, padx=10, pady=10)
        self.txt2 = tk.Entry(self.formFrame, font=self.formFont, relief="raised")
        self.txt2.grid(row=1, column=1, padx=10, pady=10)

        self.lb3 = tk.Label(self.formFrame, text="Enter Phone", font=self.formFont, bg=self.primarycolor)
        self.lb3.grid(row=2, column=0, padx=10, pady=10)
        self.txt3 = tk.Entry(self.formFrame, font=self.formFont, relief="raised")
        self.txt3.grid(row=2, column=1, padx=10, pady=10)

        self.lb4 = tk.Label(self.formFrame, text="Enter Relation", font=self.formFont, bg=self.primarycolor)
        self.lb4.grid(row=3, column=0, padx=10, pady=10)
        self.txt4 = tk.Entry(self.formFrame, font=self.formFont, relief="raised")
        self.txt4.grid(row=3, column=1, padx=10, pady=10)

        self.buttonFrame = tk.Frame(self.root, bg=self.secondaycolor)
        self.buttonFrame.pack()

        self.btn1 = tk.Button(self.buttonFrame, text="Save Contact", font=self.formFont, command=self.save_contact,
                                   width=12, bg=self.primarycolor, fg=self.txtcolor, relief="raised")
        self.btn1.grid(row=0, column=0, padx=10, pady=30)

        self.root.mainloop()

    def save_contact(self):
        user_id = self.txt1.get()
        name = self.txt2.get()
        phone = self.txt3.get()
        relation = self.txt4.get()

        if user_id=='' or name == "" or phone == "" or relation == "":
            msg.showwarning("Warning", "All fields are required!", parent=self.root)
            return

        conn = get_connection()
        cur = conn.cursor()

        q = f"INSERT INTO emergency_contacts (user_id, name, phone, relation) VALUES ({user_id}, '{name}', '{phone}', '{relation}')"
        cur.execute(q)
        conn.commit()
        conn.close()

        msg.showinfo("Success", "Emergency contact saved!", parent=self.root)
        self.reset_form()

    def reset_form(self):

        self.txt1.delete(0, tk.END)
        self.txt2.delete(0, tk.END)
        self.txt3.delete(0, tk.END)
        self.txt4.delete(0, tk.END)




