# dashboard.py
import tkinter as tk
from user_login_sos_voice import *
from register import *
from view_users import *
from add_emergency_contact import *
from view_emergency_contact import *

class Dashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x500")
        self.root.title("Women Safety Dashboard")
        self.root.configure(bg="#E3D3E4")

        tk.Label(self.root, text="WOMEN SAFETY DASHBOARD", font=("Arial", 16, "bold"),
                 bg="#E3D3E4", fg="#946E83").pack(pady=20)

        tk.Button(self.root, text="Login", width=20, bg="#946E83", fg="white",
                  command=self.open_login).pack(pady=10)
        tk.Button(self.root, text="Register", width=20, bg="#946E83", fg="white",
                  command=self.open_register).pack(pady=10)
        tk.Button(self.root, text="View Users", width=20, bg="#946E83", fg="white",command=self.view_users).pack(pady=10)
        tk.Button(self.root, text="Add Emergency Contact", width=20, bg="#946E83", fg="white",command=self.add_emergency).pack(pady=10)
        tk.Button(self.root, text="View Emergency Contact", width=20, bg="#946E83", fg="white",command=self.view_emergency).pack(pady=10)

        tk.Label(self.root, text="Voice detection will start automatically after login.",
                 bg="#E3D3E4", fg="black", font=("Arial", 10)).pack(pady=30)

        self.root.mainloop()

    def open_login(self):
        self.root.destroy()  # close dashboard
        Login()

    def open_register(self):
        Main()

    def view_users(self):
        viewuser()

    def add_emergency(self):
        Emergency_contact()

    def view_emergency(self):
        viewemergency()



if __name__ == "__main__":
    Dashboard()
