import streamlit as st
st.title("Smart Restaurant System")
st.write("Welcome to the Smart Restaurant System")
name = st.text_input("Enter your name")
if name:
    st.write(f"Hello, {name}, your order is coming soon.")