# ✅ employee_checkout.py
import streamlit as st
from encrypt_util import load_key, decrypt_data
from db_config import get_db
from datetime import datetime
import pytz

fernet = load_key()
db = get_db()
collection = db["entries"]
employee_users = db["employees"]

def get_today_employee_doc():
    today = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d")
    doc = collection.find_one({"date": today, "type": "employee"})
    return doc

st.markdown("<div style='height:1px; color:transparent;'>.</div>", unsafe_allow_html=True)

st.set_page_config(page_title="Employee Check-Out", layout="centered")
st.title("🔁 Employee Check-Out")

emp_id = st.text_input("Employee ID")
password = st.text_input("Password", type="password")

if st.button("Check-Out"):
    if not emp_id or not password:
        st.warning("Please fill both fields.")
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
                    today_doc = get_today_employee_doc()
                    if not today_doc:
                        st.error("❌ No employee entries found for today.")
                        st.stop()

                    entries = today_doc["entries"]
                    found = False
                    for i, entry in enumerate(entries):
                        if entry["employee_id"] == emp_id:
                            if entry["status"] == "OUT":
                                st.info("ℹ️ You have already checked out today.")
                            else:
                                entries[i]["status"] = "OUT"
                                entries[i]["checkout_time"] = datetime.now(
                                    pytz.timezone('Asia/Kolkata')).strftime("%H:%M:%S")
                                collection.update_one(
                                    {"_id": today_doc["_id"]},
                                    {"$set": {"entries": entries}}
                                )
                                st.success("✅ Successfully Checked Out!")
                            found = True
                            break

                    if not found:
                        st.warning("You haven't checked in yet today.")

            except Exception as e:
                st.error("Encryption error or data issue. Please contact admin.")
