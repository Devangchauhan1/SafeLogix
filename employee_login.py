import streamlit as st
from encrypt_util import encrypt_data, decrypt_data, load_key
from db_config import get_db
from datetime import datetime
import pytz

# Setup
fernet = load_key()
db = get_db()
collection = db["entries"]
employee_users = db["employees"]

# Ensure daily employee document
def get_today_employee_doc():
    today = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d")
    doc = collection.find_one({"date": today, "type": "employee"})
    if not doc:
        new_doc = {"date": today, "type": "employee", "entries": []}
        collection.insert_one(new_doc)
        return new_doc
    return doc

def show_employee_login():
    if "employee_logged_in" not in st.session_state:
        st.session_state.employee_logged_in = False
        st.session_state.employee_id = None
        st.session_state.employee_name = None

    # ================= LOGIN FORM ==================
    if not st.session_state.employee_logged_in:
        emp_id = st.text_input("Employee ID", key="login_emp_id")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", key="login_button"):
            if not emp_id or not password:
                st.warning("Please enter both Employee ID and Password.")
            else:
                user = employee_users.find_one({"employee_id": emp_id})
                if not user:
                    st.error("❌ No such employee registered.")
                else:
                    try:
                        stored_password = decrypt_data(user["password"], fernet)
                        if stored_password != str(password):
                            st.error("❌ Incorrect password.")
                        else:
                            st.session_state.employee_logged_in = True
                            st.session_state.employee_id = emp_id
                            st.session_state.employee_name = user["name"]
                            st.success(f"✅ Welcome, {user['name']}!")
                            st.rerun()
                    except Exception:
                        st.error("❌ Decryption error. Please contact admin.")
    else:
        # ================= LOGGED-IN VIEW ==================
        st.success(f"🟢 Logged in as {st.session_state.employee_name} ({st.session_state.employee_id})")
        today_doc = get_today_employee_doc()
        entries = today_doc["entries"]

        checked_in = False
        entry_index = None
        for i, entry in enumerate(entries):
            if entry["employee_id"] == st.session_state.employee_id and entry["status"] == "IN":
                checked_in = True
                entry_index = i
                break

        if checked_in:
            st.info("You are currently checked IN.")
            if st.button("🔁 Check-Out"):
                checkout_time = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%H:%M:%S")
                entries[entry_index]["status"] = "OUT"
                entries[entry_index]["checkout_time"] = checkout_time
                collection.update_one(
                    {"_id": today_doc["_id"]},
                    {"$set": {"entries": entries}}
                )
                st.success("✅ Successfully Checked Out!")
        else:
            checkin_time = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%H:%M:%S")
            entry = {
                "employee_id": st.session_state.employee_id,
                "name": st.session_state.employee_name,
                "department": employee_users.find_one(
                    {"employee_id": st.session_state.employee_id}
                )["department"],
                "checkin_time": checkin_time,
                "status": "IN"
            }
            collection.update_one(
                {"_id": today_doc["_id"]},
                {"$push": {"entries": entry}}
            )
            st.success("🟢 Check-in recorded!")

        # ================= LOGOUT ==================
        if st.button("🔓 Logout"):
            st.session_state.employee_logged_in = False
            st.session_state.employee_id = None
            st.session_state.employee_name = None
            st.rerun()
