# employee_page.py
import streamlit as st
from employee_login import show_employee_login
from employee_register import show_employee_register

def show_employee_page():
    # Maintain current tab state
    if "employee_tab" not in st.session_state:
        st.session_state.employee_tab = "login"

    tab = st.radio("Select Option", ["🔐 Employee Login", "📝 New Registration"], 
                   horizontal=True, key="employee_tab_selector")

    if tab == "🔐 Employee Login":
        if st.session_state.employee_tab != "login":
            # Just switched to Login tab — reset fields
            st.session_state.employee_tab = "login"
            for key in ["login_emp_id", "login_password"]:
                st.session_state.pop(key, None)

        show_employee_login()

    else:
        if st.session_state.employee_tab != "register":
            # Just switched to Register tab — reset state (if needed)
            st.session_state.employee_tab = "register"
        show_employee_register()
