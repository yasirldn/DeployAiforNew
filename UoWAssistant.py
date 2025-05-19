import streamlit as st

# Configuring the Streamlit page title and Icon
st.set_page_config(page_title="Watson Assistant", page_icon="🤖", layout="wide")

# Then i will setup different pages links and their titles

Chatbot = st.Page (
    "pages/UoWAssistantChatbot.py",
    title="Welcome to UoW Assistant Chatbot",
    icon=":material/account_circle:",

)
Welcome = st.Page(
    "pages/Welcome.py",
    title="Welcome to UoW Assistant Web App",
    icon=":material/account_circle:",
)

about = st.Page(
    "pages/about.py",
    title="About the ChatBot",
    icon=":material/account_circle:",
    default=True,
)
exams = st.Page(
    "pages/exams.py",
    title="Exam FAQs",
    icon=":material/bar_chart:",
)
attendance = st.Page(
    "pages/attendance.py",
    title="Attendance FAQs",
    icon=":material/smart_toy:",
)

login = st.Page(
    "pages/app.py",
    title="Login Page",
    icon=":material/smart_toy:",
)


# Now setting up a side NavBar

nav = st.navigation(
    {
        "Chatbot": [Chatbot],
        "Info": [about],
        "Projects": [exams, attendance, login],

    }
)
nav.run()

st.sidebar.markdown("Made by Muhammad Yasir")

