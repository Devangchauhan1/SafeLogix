# guest_page.py
import streamlit as st
from guest_entry import show_guest_entry

def show_guest_page():
    with st.tabs(["🙋 Guest Entry / Exit"])[0]:
        show_guest_entry()
