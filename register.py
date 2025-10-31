import tkinter
from tkinter import messagebox as msg
from connection import *
from tkinter import ttk
from tkinter import *

class Main:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry("500x500")
        self.root.title("Insert Form")
        self.primarycolor = "#E3D3E4"
        self.secondaycolor = "#946E83"
        self.txtcolor = "black"
        self.title = tkinter.Label(self.root, text="User Register", font=("Arial", "20", "bold"),bg=self.secondaycolor,fg=self.txtcolor,width=15)
        self.title.pack(pady=20)

        self.formFont = ("Arial", 14)


        self.root.configure(bg=self.secondaycolor)

        self.conn = get_connection()
        self.cur = self.conn.cursor()

        self.formFrame = tkinter.Frame(self.root,bg=self.primarycolor,highlightthickness=2,highlightbackground="black")
        self.formFrame.pack()

        self.lb1 = tkinter.Label(self.formFrame, text="Enter Name", font=self.formFont,bg=self.primarycolor)
        self.lb1.grid(row=0, column=0, padx=10, pady=10)
        self.txt1 = tkinter.Entry(self.formFrame, font=self.formFont,relief="raised")
        self.txt1.grid(row=0, column=1, padx=10, pady=10)

        self.lb2 = tkinter.Label(self.formFrame, text="Enter Mobile", font=self.formFont,bg=self.primarycolor)
        self.lb2.grid(row=1, column=0, padx=10, pady=10)
        self.txt2 = tkinter.Entry(self.formFrame, font=self.formFont,relief="raised")
        self.txt2.grid(row=1, column=1, padx=10, pady=10)

        self.lb3 = tkinter.Label(self.formFrame, text="Enter Email", font=self.formFont,bg=self.primarycolor)
        self.lb3.grid(row=2, column=0, padx=10, pady=10)
        self.txt3 = tkinter.Entry(self.formFrame, font=self.formFont,relief="raised")
        self.txt3.grid(row=2, column=1, padx=10, pady=10)

        self.lb4 = tkinter.Label(self.formFrame, text="Enter Password", font=self.formFont,bg=self.primarycolor)
        self.lb4.grid(row=3, column=0, padx=10, pady=10)
        self.txt4 = tkinter.Entry(self.formFrame, font=self.formFont, show="*",relief="raised")
        self.txt4.grid(row=3, column=1, padx=10, pady=10)



        self.buttonFrame=tkinter.Frame(self.root,bg=self.secondaycolor)
        self.buttonFrame.pack()

        self.btn1=tkinter.Button(self.buttonFrame,text="Register",font=self.formFont,command=self.getFormValues,width=12,bg=self.primarycolor,fg=self.txtcolor,relief="raised")
        self.btn1.grid(row=0, column=0, padx=10, pady=30)


        self.root.mainloop()

    def getFormValues(self):
        self.name=self.txt1.get()
        self.mobile=self.txt2.get()
        self.email=self.txt3.get()
        self.password = self.txt4.get()


        if self.name == "" or self.mobile == "" or self.email == "" or self.password == "" :
            msg.showwarning("Warning", "Enter your Values", parent=self.root)
        else:
            q4=f"select * from user where email='{self.email}'"
            self.cur.execute(q4)
            email=self.cur.fetchall()
            if len(email)==0:
                q5=f"select * from user where mobile='{self.mobile}'"
                self.cur.execute(q5)
                mobile=self.cur.fetchall()
                if len(mobile)==0:
                    if email_valid(self.email):
                        if mobile_valid(self.mobile):
                            q=f"insert into user values(null,'{self.name}', '{self.mobile}', '{self.email}','{self.password}')"
                            self.cur.execute(q)
                            self.conn.commit()
                            msg.showwarning("Success", "User has been added", parent=self.root)
                            self.resetForm()

                        else:
                            msg.showwarning("Warning","Enter valid mobile no", parent=self.root)

                    else:
                        msg.showwarning("Warning","Enter valid email address", parent=self.root)
                        parent = self.root
                else:
                    msg.showwarning("Warning","Mobile already exist", parent=self.root)
                    parent = self.root
            else:
                msg.showwarning("Warning","Email already exist", parent=self.root)
                parent = self.root

    def resetForm(self):
        self.txt1.delete(0, END)
        self.txt2.delete(0, END)
        self.txt3.delete(0, END)
        self.txt4.delete(0, END)



