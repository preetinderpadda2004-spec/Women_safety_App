import tkinter as tk
from tkinter import messagebox as msg
from connection import *
import cv2
import threading
import time
import speech_recognition as sr
import smtplib
from email.mime.text import MIMEText
from playsound import playsound


class Login:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x500")
        self.root.title("User Login")

        self.primarycolor = "#E3D3E4"
        self.secondaycolor = "#946E83"
        self.txtcolor = "black"

        self.root.configure(bg=self.secondaycolor)
        self.conn = get_connection()
        self.cur = self.conn.cursor()

        # ---------- UI Design ----------
        self.title = tk.Label(
            self.root,
            text="User Login",
            font=("Arial", 20, "bold"),
            bg=self.secondaycolor,
            fg=self.txtcolor,
            width=10
        )
        self.title.pack(pady=20)

        self.formFont = ("Arial", 14)
        self.formFrame = tk.Frame(
            self.root,
            bg=self.primarycolor,
            highlightthickness=2,
            highlightbackground="black"
        )
        self.formFrame.pack()

        tk.Label(
            self.formFrame, text="Enter Email",
            font=self.formFont, bg=self.primarycolor
        ).grid(row=0, column=0, padx=10, pady=10)

        self.txt1 = tk.Entry(self.formFrame, font=self.formFont, relief="solid")
        self.txt1.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(
            self.formFrame, text="Enter Password",
            font=self.formFont, bg=self.primarycolor
        ).grid(row=1, column=0, padx=10, pady=10)

        self.txt2 = tk.Entry(self.formFrame, font=self.formFont, relief="solid", show="*")
        self.txt2.grid(row=1, column=1, padx=10, pady=10)

        self.buttonFrame = tk.Frame(self.root, bg=self.secondaycolor)
        self.buttonFrame.pack()

        self.btn1 = tk.Button(
            self.buttonFrame, text="Login",
            font=self.formFont, command=self.userLogin,
            width=12, bg=self.primarycolor,
            fg=self.txtcolor, relief="raised"
        )
        self.btn1.grid(row=0, column=0, padx=10, pady=30)

        self.root.mainloop()

    # ---------------- Login ----------------
    def userLogin(self):
        email = self.txt1.get()
        password = self.txt2.get()
        q = f"SELECT * FROM user WHERE email='{email}' AND password='{password}'"
        self.cur.execute(q)
        res = self.cur.fetchall()

        if len(res) == 0:
            msg.showwarning("Warning", "Invalid Email/Password", parent=self.root)
        else:
            msg.showinfo("Success", "Login Successful", parent=self.root)
            self.root.destroy()

            # Start the voice listener window or infinite loop
            listener_window = tk.Tk()
            listener_window.title("Safety Monitoring Active")
            listener_window.geometry("300x200")
            tk.Label(listener_window, text="🔊 Voice monitoring is ON",
                     font=("Arial", 12, "bold"), fg="green").pack(pady=30)
            tk.Label(listener_window, text="Say 'help' or scream to trigger SOS.",
                     font=("Arial", 10)).pack()

            # Start background listening thread
            threading.Thread(target=self.voiceDetection, args=(email,), daemon=True).start()

            listener_window.mainloop()

    # ---------------- After Login Start Voice Detection ----------------
    def startListening(self, user_email):
        print("Starting background voice listener...")
        threading.Thread(target=self.voiceDetection, args=(user_email,), daemon=True).start()

    # ---------------- Voice/Scream Detection ----------------
    def voiceDetection(self, user_email):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        print("Listening for 'help' or loud sounds...")
        while True:
            try:
                with mic as source:
                    recognizer.adjust_for_ambient_noise(source)
                    print("Listening...")
                    audio = recognizer.listen(source, phrase_time_limit=4)

                try:
                    text = recognizer.recognize_google(audio).lower()
                    print("Heard:", text)
                    if "help" in text or "bachao" in text or "save me" in text:
                        print("Help word detected! Triggering SOS...")
                        self.triggerSOS(user_email)
                        time.sleep(10)
                except sr.UnknownValueError:
                    # If no words recognized, check loudness for scream
                    energy = audio.get_raw_data()
                    if len(energy) > 50000:  # Rough scream detection threshold
                        print("Loud scream detected!")
                        self.triggerSOS(user_email)
                        time.sleep(10)
            except Exception as e:
                print("Error in voice detection:", e)

    # ---------------- Trigger SOS ----------------
    def triggerSOS(self, user_email):
        # Run sound, alert, and recording simultaneously
        threading.Thread(target=self.playAlertSound, daemon=True).start()
        threading.Thread(target=self.sendSOSAlert, args=(user_email,), daemon=True).start()
        threading.Thread(target=self.startVideoRecording, daemon=True).start()

    # ---------------- Alert Sound ----------------
    def playAlertSound(self):
        try:
            for _ in range(3):
                playsound("alert.mp3")  # keep an alert.mp3 in folder
                time.sleep(1)
        except Exception as e:
            print("Alert sound error:", e)

    # ---------------- Send SOS Email ----------------
    def sendSOSAlert(self, user_id):
        q = f"SELECT phone FROM emergency_contacts WHERE user_id='{user_id}'"
        self.cur.execute(q)
        contacts = self.cur.fetchall()

        sender_email = "your_email@gmail.com"
        sender_pass = "your_app_password"
        subject = "🚨 SOS ALERT 🚨"
        body = "This is an emergency! The user may be in danger. Please check immediately."

        try:
            for contact in contacts:
                receiver = contact[0]
                msg_text = MIMEText(body)
                msg_text['Subject'] = subject
                msg_text['From'] = sender_email
                msg_text['To'] = receiver

                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(sender_email, sender_pass)
                    server.sendmail(sender_email, receiver, msg_text.as_string())
            print("SOS Alert Sent Successfully!")
        except Exception as e:
            print("Error sending SOS alert:", e)

    # ---------------- Video Recording ----------------
    import time

    is_recording = False

    def startVideoRecording(self):
        global is_recording
        if self.is_recording:
            print("Recording already in progress...")
            return
        self.is_recording = True
        print("Recording started...")

        cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter("recorded_video.avi", fourcc, 20.0, (640, 480))

        start_time = time.time()
        while int(time.time() - start_time) < 10:  # Record for 10 seconds
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)

        cap.release()
        out.release()
        cv2.destroyAllWindows()
        print("Recording stopped & saved.")
        is_recording = False


if __name__ == "__main__":
    Login()
