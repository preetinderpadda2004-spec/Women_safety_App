import tkinter
from tkinter import *
import tkinter.messagebox as msg
import tkinter.ttk as ttk
from connection import *

class viewemergency:
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

        self.mainLabel = Label(self.root, text='View Emergency Contact',font=('Arial',28,'bold'),bg=self.secondaycolor,fg=self.txtcolor,width=20)
        self.mainLabel.pack(pady=20)

        self.searchFrame = Frame(self.root,bg=self.primarycolor,highlightthickness=2,highlightbackground="black")
        self.searchFrame.pack(pady=20)

        self.lbl = Label(self.searchFrame, text='Search', font=('Arial', 14),bg=self.primarycolor)
        self.lbl.grid(row=0, column=0, pady=10, padx=10)
        self.txt1 = Entry(self.searchFrame, font=('Arial', 14),relief="solid")
        self.txt1.grid(row=0, column=1, pady=10, padx=10)
        self.btn1 = Button(self.searchFrame, text='Search', font=('Arial', 14), command=self.searchContact,bg=self.primarycolor)
        self.btn1.grid(row=0, column=2, pady=10, padx=10)
        self.btn2 = Button(self.searchFrame, text='Refresh', font=('Arial', 14), command=self.resetContact,bg=self.primarycolor)
        self.btn2.grid(row=0, column=3, pady=10, padx=10)
        self.btn3 = Button(self.searchFrame, text='Delete', font=('Arial', 14), command=self.deleteContact,bg=self.primarycolor)
        self.btn3.grid(row=0, column=4, pady=10, padx=10)


        self.emergency_contactsTable = ttk.Treeview(self.root, columns=['id', 'user_id', 'name', 'phone','relation'])
        self.emergency_contactsTable.pack(expand=True, fill='both', padx=20, pady=20)
        self.emergency_contactsTable.heading('id', text="ID")
        self.emergency_contactsTable.heading('user_id', text="USER_ID")
        self.emergency_contactsTable.heading('name', text="Name")
        self.emergency_contactsTable.heading('phone', text="Mobile")
        self.emergency_contactsTable.heading('relation', text="Relation")

        self.emergency_contactsTable['show'] = 'headings'
        self.getValues()
        self.emergency_contactsTable.bind('<Double-1>',self.updateWindow)

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 14), rowheight=40)
        style.configure("Treeview.Heading", font=("Arial", 14))

        self.root.mainloop()

    def getValues(self):
        q = f"select id,user_id,name,phone,relation from emergency_contacts"
        self.cur.execute(q)
        result = self.cur.fetchall()
        for row in self.emergency_contactsTable.get_children():
            self.emergency_contactsTable.delete(row)

        index = 0
        for row in result:
            self.emergency_contactsTable.insert("", index=index, values=row)
            index += 1

    def resetContact(self):
        self.txt1.delete(0, 'end')
        self.getValues()

    def searchContact(self):
        text = self.txt1.get()
        q = f"select id,user_id,name,phone,relation from emergency_contacts where id like '%{text}%' or user_id like '%{text}%' or name like '%{text}%' or phone like '%{text}%' or relation like '%{text}%' "
        self.cur.execute(q)
        result = self.cur.fetchall()

        for row in self.emergency_contactsTable.get_children():
            self.emergency_contactsTable.delete(row)

        index = 0
        for row in result:
            self.emergency_contactsTable.insert("", index=index, values=row)
            index += 1

    def deleteContact(self):
        row = self.emergency_contactsTable.selection()
        if len(row) == 0:
            msg.showwarning("Warning", "No Data Found", parent=self.root)
        else:
            row_id = row[0]
            items = self.emergency_contactsTable.item(row_id)
            data = items["values"]
            confirm = msg.askyesno("Warning", "Do you want to delete?", parent=self.root)
            if confirm:
                q = f"delete from user where id ='{data[0]}'"
                self.cur.execute(q)
                self.conn.commit()
                self.resetContact()
                msg.showinfo("Delete", "Deletion Successful", parent=self.root)
            else:
                msg.showinfo("Delete", "Deletion Failed", parent=self.root)

    def updateWindow(self,e):
        row = self.emergency_contactsTable.selection()
        row_id = row[0]
        items = self.emergency_contactsTable.item(row_id)
        data = items["values"]
        self.root1 = tkinter.Tk()
        self.root1.geometry("650x650")
        self.root1.configure(bg=self.secondaycolor)
        self.root1.title("Contact")
        self.title = tkinter.Label(self.root1, text="Update Contact", font=("Arial", "18", "bold"),bg=self.secondaycolor,fg=self.txtcolor,width=14)
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

        self.lb2 = tkinter.Label(self.formFrame, text="Enter User Id", font=self.formFont, bg=self.primarycolor)
        self.lb2.grid(row=1, column=0, padx=10, pady=10)
        self.txt2 = tkinter.Entry(self.formFrame, font=self.formFont, relief="solid")
        self.txt2.grid(row=1, column=1, padx=10, pady=10)
        self.txt2.insert(0, data[1])


        self.lb3 = tkinter.Label(self.formFrame, text="Enter Name", font=self.formFont,bg=self.primarycolor)
        self.lb3.grid(row=2, column=0, padx=10, pady=10)
        self.txt3 = tkinter.Entry(self.formFrame, font=self.formFont,relief="solid")
        self.txt3.grid(row=2, column=1, padx=10, pady=10)
        self.txt3.insert(0, data[2])

        self.lb4 = tkinter.Label(self.formFrame, text="Enter Mobile", font=self.formFont,bg=self.primarycolor)
        self.lb4.grid(row=3, column=0, padx=10, pady=10)
        self.txt4 = tkinter.Entry(self.formFrame, font=self.formFont,relief="solid")
        self.txt4.grid(row=3, column=1, padx=10, pady=10)
        self.txt4.insert(0, data[3])

        self.lb5 = tkinter.Label(self.formFrame, text="Enter Relation", font=self.formFont, bg=self.primarycolor)
        self.lb5.grid(row=4, column=0, padx=10, pady=10)
        self.txt5 = tkinter.Entry(self.formFrame, font=self.formFont, relief="solid")
        self.txt5.grid(row=4, column=1, padx=10, pady=10)
        self.txt5.insert(0, data[4])

        self.buttonFrame = tkinter.Frame(self.root1,bg=self.secondaycolor)
        self.buttonFrame.pack()

        self.btn = tkinter.Button(self.buttonFrame, text="Update", font=self.formFont, command=self.getFormValues,bg=self.primarycolor)
        self.btn.grid(row=0, column=0, padx=10, pady=10)

        self.root1.mainloop()

    def getFormValues(self):
        self.id = self.txt1.get()
        self.user_id = self.txt2.get()
        self.name = self.txt3.get()
        self.phone = self.txt4.get()
        self.relation = self.txt5.get()


        if self.user_id == "" or self.name == "" or self.phone == "" or self.relation == "":
            msg.showwarning("Warning", "Enter your Values", parent=self.root)
        else:
            q = f"update emergency_contacts set user_id='{self.user_id}', name='{self.name}' , phone='{self.phone}' , relation='{self.relation}'where id='{self.id}'"
            self.cur.execute(q)
            self.conn.commit()
            self.getValues()
            msg.showinfo("Success","Updation Successful",parent=self.root1)
            self.root1.destroy()


