import streamlit as st
import sys
import os

# Database operations access kosam path setting
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend_api')))
from database.operations import get_admin, create_admin

def check_password():
    # Database lo admin unnadho ledo check chesthunnam
    admin_account = get_admin()

    # Case 1: First time run (Setup mode)
    if not admin_account:
        st.header("🛠️ Initial MIDS System Setup")
        st.info("No Admin account found. Please set your master password to initialize the dashboard.")
        
        new_pass = st.text_input("Set Master Admin Password", type="password")
        conf_pass = st.text_input("Confirm Password", type="password")
        
        if st.button("Set Password & Start System"):
            if new_pass == conf_pass and len(new_pass) > 0:
                if create_admin(new_pass):
                    st.success("✅ Password set successfully! Refreshing for Login...")
                    st.rerun()
                else:
                    st.error("Failed to save password to database.")
            else:
                st.error("Passwords do not match or are empty.")
        return False

    # Case 2: Standard Login
    def password_entered():
        if st.session_state["user_input"] == "admin" and st.session_state["pass_input"] == admin_account.password:
            st.session_state["password_correct"] = True
            del st.session_state["pass_input"] 
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.header("🔒 MIDS Secure Admin Login")
        st.text_input("Username", key="user_input")
        st.text_input("Password", type="password", key="pass_input")
        st.button("Login", on_click=password_entered)
        return False
        
    elif not st.session_state["password_correct"]:
        st.header("🔒 MIDS Secure Admin Login")
        st.text_input("Username", key="user_input")
        st.text_input("Password", type="password", key="pass_input")
        st.button("Login", on_click=password_entered)
        st.error("😕 Invalid username or password. Please try again.")
        return False
    
    return True