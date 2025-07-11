import streamlit as st
from datetime import datetime
from encrypt_util import encrypt_data, decrypt_data, load_key
from db_config import get_db
import pytz

# Load encryption key and DB
fernet = load_key()
db = get_db()
collection = db["entries"]

# Get or create today's guest document
def get_today_guest_doc():
    today = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d")
    guest_doc = collection.find_one({"date": today, "type": "guest"})
    if not guest_doc:
        new_doc = {"date": today, "type": "guest", "entries": []}
        collection.insert_one(new_doc)
        return new_doc
    return guest_doc

# Generate access code
def generate_access_code():
    from random import choices
    import string
    return ''.join(choices(string.ascii_uppercase + string.digits, k=6))

# UI Logic
def show_guest_entry():
    st.header("👋 Guest Entry / Exit")

    tab = st.radio("Select Option", ["Check-In", "Check-Out"], horizontal=True)

    if tab == "Check-In":
        st.subheader("Guest Check-In")

        # Default values on first run
        if "guest_submitted" not in st.session_state:
            st.session_state.guest_submitted = False

        name = st.text_input("Full Name")
        contact = st.text_input("Contact Number")
        id_proof = st.text_input("ID Proof Number")
        purpose = st.text_area("Purpose of Visit")

        if st.button("Submit Check-In"):
            if not name.strip() or not contact.strip() or not id_proof.strip() or not purpose.strip():
                st.warning("Please fill all fields.")
            elif not contact.isdigit():
                st.warning("❌ Contact number must contain only digits.")
            elif len(contact) > 10:
                st.warning("❌ Contact number cannot be more than 10 digits.")
            else:
                guest_doc = get_today_guest_doc()
                encrypted_contact = encrypt_data(contact, fernet)
                encrypted_id = encrypt_data(id_proof, fernet)

                already_checked_in = False
                for entry in guest_doc['entries']:
                    try:
                        decrypted_id = decrypt_data(entry["id_proof"], fernet)
                        if decrypted_id == id_proof and entry["status"] == "IN":
                            already_checked_in = True
                            st.warning(f"⚠️ Already checked in today. Access Code: {entry['access_code']}")
                            break
                    except Exception:
                        continue

                if not already_checked_in:
                    checkin_time = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%H:%M:%S")
                    access_code = generate_access_code()
                    entry = {
                        "name": name,
                        "contact": encrypted_contact,
                        "id_proof": encrypted_id,
                        "purpose": purpose,
                        "checkin_time": checkin_time,
                        "status": "IN",
                        "access_code": access_code
                    }
                    collection.update_one(
                        {"date": guest_doc['date'], "type": "guest"},
                        {"$push": {"entries": entry}}
                    )
                    st.success(f"✅ Check-in successful! Your access code: {access_code}")
                    st.session_state.guest_submitted = True
                    st.rerun()

        # Auto clear form after rerun
        if st.session_state.get("guest_submitted"):
            st.session_state.guest_submitted = False  # reset flag

    elif tab == "Check-Out":
        st.subheader("Guest Check-Out")
        name_out = st.text_input("Name (Check-Out)", key="out_name")
        access_code_out = st.text_input("Access Code", key="out_code")

        if st.button("Submit Check-Out"):
            if not name_out or not access_code_out:
                st.warning("Please provide both name and access code.")
            else:
                guest_doc = get_today_guest_doc()
                updated = False
                for idx, entry in enumerate(guest_doc["entries"]):
                    if entry["name"] == name_out and entry["access_code"] == access_code_out and entry["status"] == "IN":
                        checkout_time = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%H:%M:%S")
                        collection.update_one(
                            {"date": guest_doc["date"], "type": "guest"},
                            {"$set": {
                                f"entries.{idx}.status": "OUT",
                                f"entries.{idx}.checkout_time": checkout_time
                            }}
                        )
                        st.success("🟢 Successfully Checked Out!")
                        updated = True
                        break
                if not updated:
                    st.error("❌ No matching check-in found for the provided name and access code.")
