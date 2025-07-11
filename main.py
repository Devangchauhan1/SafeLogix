# main.py
import streamlit as st
import streamlit.components.v1 as components
from employee_page import show_employee_page
from guest_page import show_guest_page

# Page config
st.set_page_config(page_title="Secure Entry System", layout="centered")

# Inject CSS + JS for particles + visual style
def inject_custom_styles():
    st.markdown("""
    <style>
    html, body, .stApp {
        height: 100%;
        margin: 0;
        padding: 0;
        background: linear-gradient(270deg, #0f2027, #2c5364, #11998e, #38ef7d, #0f2027);
        background-size: 400% 400%;
        animation: gradientMove 30s ease infinite;
        overflow-x: hidden;
        color: #ffffff !important;
    }

    @keyframes gradientMove {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    header, footer, .css-18ni7ap.e8zbici2 {
        display: none !important;
    }

    .main-container {
        position: relative;
        z-index: 2;
        padding-top: 5vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        color: #ffffff;
    }

    .main-container h1 {
        font-size: 2.7rem;
        font-weight: 800;
        color: #ffffff !important;
        text-shadow: 0 3px 14px #000000;
        margin-bottom: 0.5rem;
    }

    .main-container p {
        color: #eeeeee;
        margin-bottom: 2rem;
        font-weight: 500;
        font-size: 1.05rem;
        text-shadow: 0 1px 4px rgba(0,0,0,0.6);
    }

    .choice-container {
        display: flex;
        gap: 3rem;
        margin-top: 1rem;
    }

    .emoji {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }

    .stButton>button {
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        color: #ffffff !important;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
        transition: all 0.3s ease;
        text-shadow: 0 1px 4px rgba(0,0,0,0.6);
    }

    .stButton>button:hover {
        background: linear-gradient(90deg, #38ef7d 0%, #11998e 100%);
        transform: scale(1.05);
    }

    h1, h2, h3, h4, h5, p, span, div, label, .stTabs [role="tab"] {
        color: #ffffff !important;
    }

    #particles-js {
        position: fixed;
        width: 100vw;
        height: 100vh;
        z-index: 0;
        top: 0;
        left: 0;
        pointer-events: none;
    }
    </style>
    """, unsafe_allow_html=True)

    components.html('''
    <div id="particles-js"></div>
    <script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>
    <script>
    particlesJS("particles-js", {
      "particles": {
        "number": {"value": 75, "density": {"enable": true, "value_area": 800}},
        "color": {"value": "#ffffff"},
        "shape": {"type": "circle"},
        "opacity": {"value": 0.4},
        "size": {"value": 3, "random": true},
        "line_linked": {"enable": true, "distance": 150, "color": "#ffffff", "opacity": 0.4, "width": 1},
        "move": {"enable": true, "speed": 2}
      },
      "interactivity": {
        "events": {
          "onhover": {"enable": true, "mode": "repulse"},
          "onclick": {"enable": true, "mode": "push"}
        },
        "modes": {
          "repulse": {"distance": 100},
          "push": {"particles_nb": 4}
        }
      },
      "retina_detect": true
    });
    </script>
    ''', height=0, width=0)

# Inject styles
inject_custom_styles()

# Routing
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

def go_home():
    st.session_state.current_page = "home"

# Home Page
if st.session_state.current_page == "home":
    with st.container():
        st.markdown("<div class='main-container'>", unsafe_allow_html=True)
        st.markdown("""
            <h1>🔐 Secure Entry Authorization & Monitoring System</h1>
            <p>Welcome to the Smart Entry Portal for Employees & Guests</p>
        """, unsafe_allow_html=True)

        st.markdown("<div class='choice-container'>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='emoji'>🙋</div>", unsafe_allow_html=True)
            if st.button("Guest Entry / Exit", use_container_width=True):
                st.session_state.current_page = "guest"
                st.rerun()

        with col2:
            st.markdown("<div class='emoji'>👨‍💼</div>", unsafe_allow_html=True)
            if st.button("Employee Login / Register", use_container_width=True):
                st.session_state.current_page = "employee"
                st.rerun()

        st.markdown("</div></div>", unsafe_allow_html=True)

# Guest Page
elif st.session_state.current_page == "guest":
    st.title("🙋 Guest Entry / Exit")
    if st.button("← Back to Home", key="guest_back"):
        go_home()
        st.rerun()
    st.markdown("---")
    show_guest_page()

# Employee Page
elif st.session_state.current_page == "employee":
    st.title("👨‍💼 Employee Portal")
    if st.button("← Back to Home", key="employee_back"):
        go_home()
        st.rerun()
    st.markdown("---")
    show_employee_page()
