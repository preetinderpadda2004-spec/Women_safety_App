import tkinter
from tkinter import *
import tkinter.messagebox as msg
import tkinter.ttk as ttk
from connection import *

class viewuser:
    def __init__(self):
        self.root = Tk()
        self.root.state('zoomed')
        self.root.title('Python MySQL Read Operation')
        self.primarycolor = "#E3D3E4"
        self.secondaycolor = "#946E83"
        self.txtcolor = 'black'
        self.root.configure(bg=self.secondaycolor)


        self.conn = get_connection()
        self.cur = self.conn.cursor()

        self.mainLabel = Label(self.root, text='View User',font=('Arial',28,'bold'),bg=self.secondaycolor,fg=self.txtcolor,width=10)
        self.mainLabel.pack(pady=20)

        self.searchFrame = Frame(self.root,bg=self.primarycolor,highlightthickness=2,highlightbackground="black")
        self.searchFrame.pack(pady=20)

        self.lbl = Label(self.searchFrame, text='Search', font=('Arial', 14),bg=self.primarycolor)
        self.lbl.grid(row=0, column=0, pady=10, padx=10)
        self.txt1 = Entry(self.searchFrame, font=('Arial', 14),relief="solid")
        self.txt1.grid(row=0, column=1, pady=10, padx=10)
        self.btn1 = Button(self.searchFrame, text='Search', font=('Arial', 14), command=self.searchUser,bg=self.primarycolor)
        self.btn1.grid(row=0, column=2, pady=10, padx=10)
        self.btn2 = Button(self.searchFrame, text='Refresh', font=('Arial', 14), command=self.resetUser,bg=self.primarycolor)
        self.btn2.grid(row=0, column=3, pady=10, padx=10)
        self.btn3 = Button(self.searchFrame, text='Delete', font=('Arial', 14), command=self.deleteUser,bg=self.primarycolor)
        self.btn3.grid(row=0, column=4, pady=10, padx=10)


        self.userTable = ttk.Treeview(self.root, columns=['id', 'name', 'email', 'mobile','role'])
        self.userTable.pack(expand=True, fill='both', padx=20, pady=20)
        self.userTable.heading('id', text="ID")
        self.userTable.heading('name', text="Name")
        self.userTable.heading('mobile', text="Mobile")
        self.userTable.heading('email', text="Email")

        self.userTable['show'] = 'headings'
        self.getValues()
        self.userTable.bind('<Double-1>',self.updateWindow)

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 14), rowheight=40)
        style.configure("Treeview.Heading", font=("Arial", 14))

        self.root.mainloop()

    def getValues(self):
        q = f"select id,name,mobile,email from user"
        self.cur.execute(q)
        result = self.cur.fetchall()
        for row in self.userTable.get_children():
            self.userTable.delete(row)

        index = 0
        for row in result:
            self.userTable.insert("", index=index, values=row)
            index += 1

    def resetUser(self):
        self.txt1.delete(0, 'end')
        self.getValues()

    def searchUser(self):
        text = self.txt1.get()
        q = f"select id,name,mobile,email from user where id like '%{text}%' or name like '%{text}%' or mobile like '%{text}%' or email like '%{text}%' "
        self.cur.execute(q)
        result = self.cur.fetchall()

        for row in self.userTable.get_children():
            self.userTable.delete(row)

        index = 0
        for row in result:
            self.userTable.insert("", index=index, values=row)
            index += 1

    def deleteUser(self):
        row = self.userTable.selection()
        if len(row) == 0:
            msg.showwarning("Warning", "No Data Found", parent=self.root)
        else:
            row_id = row[0]
            items = self.userTable.item(row_id)
            data = items["values"]
            confirm = msg.askyesno("Warning", "Do you want to delete?", parent=self.root)
            if confirm:
                q = f"delete from user where id ='{data[0]}'"
                self.cur.execute(q)
                self.conn.commit()
                self.resetUser()
                msg.showinfo("Delete", "Deletion Successful", parent=self.root)
            else:
                msg.showinfo("Delete", "Deletion Failed", parent=self.root)

    def updateWindow(self,e):
        row = self.userTable.selection()
        row_id = row[0]
        items = self.userTable.item(row_id)
        data = items["values"]
        self.root1 = tkinter.Tk()
        self.root1.geometry("650x650")
        self.root1.configure(bg=self.secondaycolor)
        self.root1.title("Admin")
        self.title = tkinter.Label(self.root1, text="Update Admin", font=("Arial", "18", "bold"),bg=self.secondaycolor,fg=self.txtcolor,width=14)
        self.title.pack(pady=10)

        self.formFont = ("Arial", 14)

        self.conn = get_connection()
        self.cur = self.conn.cursor()

        self.formFrame = tkinter.Frame(self.root1,bg=self.primarycolor,highlightthickness=2,highlightbackground="black")
        self.formFrame.pack()

        self.lb1 = tkinter.Label(self.formFrame, text="Enter ID", font=self.formFont,bg=self.primarycolor)
        self.lb1.grid(row=0, column=0, padx=10, pady=10)
        self.txt1 = tkinter.Entry(self.formFrame, font=self.formFont,relief="solid")
        self.txt1.grid(row=0, column=1, padx=10, pady=10)
        self.txt1.insert(0, data[0])
        self.txt1.configure(state="readonly")

        self.lb2 = tkinter.Label(self.formFrame, text="Enter Name", font=self.formFont,bg=self.primarycolor)
        self.lb2.grid(row=1, column=0, padx=10, pady=10)
        self.txt2 = tkinter.Entry(self.formFrame, font=self.formFont,relief="solid")
        self.txt2.grid(row=1, column=1, padx=10, pady=10)
        self.txt2.insert(0, data[1])

        self.lb3 = tkinter.Label(self.formFrame, text="Enter Mobile", font=self.formFont,bg=self.primarycolor)
        self.lb3.grid(row=2, column=0, padx=10, pady=10)
        self.txt3 = tkinter.Entry(self.formFrame, font=self.formFont,relief="solid")
        self.txt3.grid(row=2, column=1, padx=10, pady=10)
        self.txt3.insert(0, data[2])

        self.lb4 = tkinter.Label(self.formFrame, text="Enter Email", font=self.formFont,bg=self.primarycolor)
        self.lb4.grid(row=3, column=0, padx=10, pady=10)
        self.txt4 = tkinter.Entry(self.formFrame, font=self.formFont,relief="solid")
        self.txt4.grid(row=3, column=1, padx=10, pady=10)
        self.txt4.insert(0, data[3])




        self.buttonFrame = tkinter.Frame(self.root1,bg=self.secondaycolor)
        self.buttonFrame.pack()

        self.btn = tkinter.Button(self.buttonFrame, text="Update", font=self.formFont, command=self.getFormValues,bg=self.primarycolor)
        self.btn.grid(row=0, column=0, padx=10, pady=10)

        self.root1.mainloop()

    def getFormValues(self):
        self.id = self.txt1.get()
        self.name = self.txt2.get()
        self.mobile = self.txt3.get()
        self.email = self.txt4.get()


        if self.name == "" or self.mobile == "" or self.email == "":
            msg.showwarning("Warning", "Enter your Values", parent=self.root)
        else:
            q = f"update user set name='{self.name}' , mobile='{self.mobile}' , email='{self.email}'where id='{self.id}'"
            self.cur.execute(q)
            self.conn.commit()
            self.getValues()
            msg.showinfo("Success","Updation Successful",parent=self.root1)
            self.root1.destroy()


