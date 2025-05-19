import streamlit as st
from app import logout



if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("You must log in to access this page.")
    st.stop()  # Stops execution if user is not authenticated

st.sidebar.button("Logout", on_click=logout)
st.title("Main Dashboard")
st.write("Welcome to the protected content!")

