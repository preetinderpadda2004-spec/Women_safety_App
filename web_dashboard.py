import streamlit as st
from user_login_sos_voice import *
from register import *
from view_users import *
from add_emergency_contact import *
from view_emergency_contact import *

st.set_page_config(page_title="Women Safety Dashboard", page_icon="🚨", layout="centered")

st.markdown("<h2 style='text-align:center; color:#946E83;'>WOMEN SAFETY DASHBOARD</h2>", unsafe_allow_html=True)

menu = ["Login", "Register", "View Users", "Add Emergency Contact", "View Emergency Contact"]
choice = st.selectbox("Select an Option", menu)

if choice == "Login":
    st.info("Voice detection will start automatically after login.")
    if st.button("Open Login"):
        Login()

elif choice == "Register":
    if st.button("Open Register Form"):
        Main()

elif choice == "View Users":
    if st.button("Show Users"):
        viewuser()

elif choice == "Add Emergency Contact":
    if st.button("Add Contact"):
        Emergency_contact()

elif choice == "View Emergency Contact":
    if st.button("View Contacts"):
        viewemergency()

st.markdown("<hr><p style='text-align:center;'>Women Safety System © 2025</p>", unsafe_allow_html=True)
