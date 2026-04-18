import streamlit as st
from services.database_service import authenticate_user

st.set_page_config(page_title="Smart Restaurant System", page_icon="🍽️")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

st.title("Smart Restaurant System")
st.write("Welcome to the Smart Restaurant System.")
st.write("Customers can use the Customer page to place orders.")
st.write("Staff must log in below to access protected functions.")

st.subheader("Staff Login")

if not st.session_state.logged_in:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate_user(username, password)

        if user:
            st.session_state.logged_in = True
            st.session_state.username = user["username"]
            st.session_state.role = user["role"]

            st.success(f"Logged in successfully as {user['role']}")
            st.rerun()
        else:
            st.error("Invalid username or password.")

else:
    st.success(
        f"Logged in as {st.session_state.username} ({st.session_state.role})"
    )

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""

        st.success("Logged out successfully.")
        st.rerun()