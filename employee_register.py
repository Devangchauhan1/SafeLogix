import streamlit as st
import re
from encrypt_util import encrypt_data, load_key
from db_config import get_db
import random
import string

fernet = load_key()
db = get_db()
employee_users = db["employees"]

# Generate random unique 6-character alphanumeric employee ID
def generate_unique_employee_id():
    while True:
        emp_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not employee_users.find_one({"employee_id": emp_id}):
            return emp_id

# Password validation function
def is_valid_password(password):
    return (
        len(password) >= 8 and
        re.search(r'[A-Z]', password) and
        re.search(r'[a-z]', password) and
        re.search(r'\d', password) and
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    )

# Registration UI
def show_employee_register():
    st.subheader("📝 Register New Employee")

    name = st.text_input("Full Name", key="reg_name")
    contact = st.text_input("Contact Number", key="reg_contact")
    department = st.text_input("Department", key="reg_department")
    password = st.text_input("Password", type="password", key="reg_password")

    if st.button("Register"):
        if not name or not contact or not department or not password:
            st.warning("⚠️ Please fill in all the fields.")
        elif not contact.isdigit() or len(contact) != 10:
            st.warning("❌ Contact number must be exactly 10 digits and contain only numbers.")
        elif not is_valid_password(password):
            st.warning("❌ Password must be at least 8 characters and include:\n- One uppercase letter\n- One lowercase letter\n- One digit\n- One special character")
        else:
            emp_id = generate_unique_employee_id()
            encrypted_contact = encrypt_data(contact, fernet)
            encrypted_password = encrypt_data(password, fernet)

            employee_users.insert_one({
                "employee_id": emp_id,
                "name": name,
                "contact": encrypted_contact,
                "department": department,
                "password": encrypted_password
            })

            st.success(f"✅ Registration successful!")
            st.info(f"🆔 Your Employee ID is: `{emp_id}` — Please note it down.")
