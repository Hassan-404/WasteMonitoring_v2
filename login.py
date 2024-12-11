import streamlit as st

st.set_page_config(
    page_title="Waste Monitoring",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        # Simple hardcoded credentials for demo
        if username == "dylanharper" and password == "password123":
            st.session_state["logged_in"] = True
            st.rerun()
        else:
            st.error("Invalid credentials. Please try again.")

def ensure_login():
    """
    Check if user is logged in. If not, display login page and stop execution.
    """
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if not st.session_state["logged_in"]:
        login_page()
        st.stop()
