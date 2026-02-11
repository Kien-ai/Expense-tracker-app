import streamlit as st
from utils.auth import signup_user, login_user
from utils.data_manager import load_user_data, save_user_data

st.set_page_config("Expense Tracker", layout="wide")

# -----------------------------
# Session defaults
# -----------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# -----------------------------
# AUTH PAGE
# -----------------------------
if not st.session_state.authenticated:
    st.title("💰 Expense Tracker")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login_user(username, password):
                st.session_state.authenticated = True
                st.session_state.user = username
                st.session_state.df = load_user_data(username)
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid username or password")

    with tab2:
        st.subheader("Create Account")
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")
        if st.button("Sign Up"):
            if signup_user(new_user, new_pass):
                st.success("Account created. You can now log in.")
            else:
                st.error("Username already exists")

    st.stop()

# -----------------------------
# MAIN APP (AFTER LOGIN)
# -----------------------------
st.sidebar.success(f"Logged in as {st.session_state.user}")

page = st.sidebar.radio(
    "Navigation",
    ["Upload Data", "Add Expense", "Dashboard", "Insights", "Reports"]
)

if page == "Upload Data":
    import pages.upload_data
elif page == "Add Expense":
    import pages.add_expense
elif page == "Dashboard":
    import pages.dashboard
elif page == "Insights":
    import pages.insights
elif page == "Reports":
    import pages.reports

if st.sidebar.button("Save & Logout"):
    save_user_data(st.session_state.user, st.session_state.df)
    st.session_state.clear()
    st.rerun()
