import sys 
import os
import pandas as pd  #unused
import io #unused
import json
import time
import streamlit as st
import requests

 #To import files from outside the current dir and uses os and sys modules where os gets file paths dynamically (cross-platform compatible)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chat_utils import save_chat_message, get_chat_history      #where I defined functions like save_chat_message() and get_chat_history() to work with Firebase.

import streamlit as st
from firebase_config import auth, db        #Custom config file I wrote that connects to Firebase for authentication and database actions.
import streamlit.components.v1 as components        #It is Used to embed raw HTML/JavaScript into the Streamlit app
from streamlit_js_eval import streamlit_js_eval    #captures JS events

# using session state to track state using session variables

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_user_msg" not in st.session_state:
    st.session_state.last_user_msg = None

# To sign up with email and password and it creates account and stores in Firebase DB.

def signup():
    st.title("Sign Up")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    if st.button("Register"):
        try:            # Tries to create a new user in Firebase Authentication using the email and password.
            user = auth.create_user(email=email, password=password)         #on success, user session variable will contain the new Firebase user object.
            db.reference("users").child(user.uid).set({"email": email})    #now it stores the user's email in Firebase Realtime Database under /users/{uid}.
            st.success("Account created successfully! Please login.")
        except Exception as e:
            st.error(f"Error: {e}")

import requests

def login():
    st.title("Login")
        # email pass fields for user email and password with unique keys to maintain state

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

        # When the Login button is clicked it attempt to authenticate

    if st.button("Login"):
        try:
            # Now Using Firebase Auth REST API to sign in and get idToken
            # Function to load the API key from a local JSON file securely without pushing secret API

            # def load_api_key():
            #     path = os.path.expanduser(".firebase/apiKey.json")
            #     with open(path, "r") as f:
            #      data = json.load(f)
            #     return data["key"]
            # api_key = load_api_key()
            api_key = "AIzaSyDlqaigTbhCumGjM_V9e8CVK8clGpurO5U"  # from Firebase project settings and web app config
  # Firebase REST API endpoint for signing in with email/password
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
   # this is the payload to send to Firebase API including user credentials

            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
  # now making POST request to Firebase API with the credentials payload

            res = requests.post(url, json=payload)
            res.raise_for_status()  # to raise error if request fails
            data = res.json()   # Tp parse JSON response from Firebase


            # If successful, data will contain idToken, localId user uid, etc. store authentication status and user info in session state
            st.session_state.authenticated = True
            st.session_state.user = {"email": email, "uid": data["localId"]}
            # display the user login succeeded
            st.success("Logged in successfully!")
            # Wait 2 seconds before movin
            time.sleep(2)
            # Refresh the Streamlit app
            st.rerun()
        except requests.exceptions.HTTPError as e:
            st.error("Login failed: Incorrect email or password.")
        except Exception as e:
            st.error(f"Login failed: {e}")


def logout():

# to. rest authentication session state to log out the user when func is called
    st.session_state.authenticated = False
    st.session_state.user = None
    st.rerun()

# To check if user is not authenticated

if not st.session_state.authenticated:
    #  selectbox dropdown
    option = st.selectbox("Choose an option", ["Login", "Sign Up"])
    # Show appropriate page based on selection
    if option == "Login":
        login()
    else:
        signup()
else:
        # to show a Logout button on the sidebar when logged in

    st.sidebar.button("Logout", on_click=logout)
        # to dispaly a welcome message to the logged in user

    st.success(f"Welcome back, {st.session_state.user['email']}!")
    st.write("You are logged in!")
    # to get the current user ID from session state

    uid = st.session_state.user['uid']

    # this is for testing history If no chat history is loaded yet then it will try to load from storage

    if not st.session_state.chat_history:
        history = get_chat_history(uid)
        if history:
            st.session_state.chat_history = history
        else:
            st.info("No chat history found.")
        st.write(f"Loaded chat history: {st.session_state.chat_history}")

    # embedding wastsonx
    watson_script = """
<script>
    console.log("Injecting Watson Chat");

    window.streamlitReceiveMessage = null;

    window.addEventListener("message", (event) => {
        if (event.data && event.data.isWatsonMessage) {
            console.log("Received message from Watson → Streamlit:", event.data.data);
            window.streamlitReceiveMessage = event.data.data;
        }
    });

    async function onLoad(instance) {
        console.log("Watson Chat loaded");
        window.chatInstance = instance;

        instance.on({ type: 'send', handler: (event) => {
            const userMsg = event.data.message;
            console.log(" Watson SEND:", userMsg);
            postMessageToStreamlit("user", userMsg);
        }});

        instance.on({ type: 'receive', handler: (event) => {
            const botMsg = event.data.message;
            console.log(" Watson RECEIVE:", botMsg);
            postMessageToStreamlit("bot", botMsg);
        }});

        await instance.render();
    }

    function postMessageToStreamlit(sender, message) {
        const payload = { sender: sender, message: message };
        window.parent.postMessage({ isWatsonMessage: true, data: JSON.stringify(payload) }, "*");
    }

    window.watsonAssistantChatOptions = {
        integrationID: "b7b7c8ae-f11e-4bdd-a1b3-6bee7697de11",
        region: "eu-gb",
        serviceInstanceID: "1be8a1d9-b9c1-4017-ad84-d1858b6d1605",
        onLoad: onLoad,
    };

    setTimeout(() => {
        const t = document.createElement('script');
        t.src = "https://web-chat.global.assistant.watson.appdomain.cloud/versions/latest/WatsonAssistantChatEntry.js";
        document.head.appendChild(t);
    }, 0);
</script>
"""
    components.html(watson_script, height=700)

    # # try listening to javascript, streamlit_js_eval is to run a small JavaScript snippet inside the browser
    # event = streamlit_js_eval(
    #     js_expressions="""
    #     (() => {
    #         const msg = window.streamlitReceiveMessage;
    #         window.streamlitReceiveMessage = null;
    #         return msg;
    #     })()
    #     """,
    #     key="watson_listener"
    # )

    # if event:
    #     try:
    #         st.write(f"Raw message from Watson: `{event}`")
    #         data = json.loads(event)

    #         if data['sender'] == "user":
    #             st.session_state.last_user_msg = data['message']
    #             st.info(f"👤 User said: {data['message']}")

    #         elif data['sender'] == "bot" and st.session_state.last_user_msg:
    #             user_msg = st.session_state.last_user_msg
    #             bot_msg = data['message']

    #             st.write(f" Saving to Firebase: `{user_msg}` → `{bot_msg}`")
    #             save_chat_message(uid, user_msg, bot_msg)
    #             st.session_state.chat_history.append((user_msg, bot_msg))
    #             st.session_state.last_user_msg = None
    #             st.success(" Message saved.")
    #     except Exception as e:
    #         st.error(f" Error processing message: {e}")

    # to display history
    st.header("🧾 Chat History")
    if st.session_state.chat_history:
        for user_msg, bot_msg in st.session_state.chat_history:
            st.markdown(f"**You:** {user_msg}")
            st.markdown(f"**Bot:** {bot_msg}")
    else:
        st.info("No chat history yet.")
    st.markdown("---")

    # manually storing messages
    st.subheader("Save Important Messages Manually")
    with st.form("manual_save_form"):
        test_user_msg = st.text_input("User Message")
        test_bot_msg = st.text_input("Bot Reply")
        if st.form_submit_button("Save to Firebase"):
            save_chat_message(uid, test_user_msg, test_bot_msg)
            st.session_state.chat_history.append((test_user_msg, test_bot_msg))
            st.success("Manually saved to Firebase.")


    # Guidelines

    # stylising the page
st.markdown(
    """
    <style>
        .section-title {
            font-size: 1.5rem;
            font-weight: bold;
            margin-top: 2rem;
        }
        .example-questions {
            margin-top: 1rem;
            font-style: italic;
            color: #555;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# defining the header
st.title("Welcome to the Student Chatbot")
st.write("This chatbot is here to help you with all your university-related queries.")

# layout for guide
with st.container():
    st.markdown("<div class='section-title'>How to Use the Chatbot</div>", unsafe_allow_html=True)
    st.write(
        "To get the best responses from the chatbot, try to ask clear and concise questions. Here are some tips:"
    )
    st.write("- Be specific about your topic. For example, instead of saying 'Help me,' try 'How do I get my student ID card?'")
    st.write("- Use keywords related to your question. For example, 'library hours,' 'career advice,' or 'mental health support.'")
    st.write("- If you're unsure, just start typing! The chatbot is designed to guide you.")

# discussed topics
def render_section(title, topics):
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
    for topic, examples in topics.items():
        st.subheader(f"- {topic}")
        st.markdown(
            f"<div class='example-questions'>Example questions: {', '.join(examples)}</div>",
            unsafe_allow_html=True
        )

render_section(
    "New Student Checklist",
    {
        "Student ID Card": ["Where do I collect my student ID?", "How do I get my ID badge?"],
        "Course Induction": ["What happens during the course induction?", "Where can I meet my tutors?"],
        "WiFi Access": ["How do I connect to campus WiFi?", "What is the university's WiFi password?"],
    },
)

render_section(
    "Academic-related Information",
    {
        "Course Modules": ["What modules are available in my course?", "Can I change my course module?"],
        "Class Timetable": ["Where can I view my timetable?", "How do I find my lecture schedule?"],
        "Attendance Policy": ["What is the attendance policy?", "Is attendance mandatory for lectures?"],
    },
)

render_section(
    "Campus Facilities",
    {
        "Library Information": ["What are the library hours?", "Can I reserve a book in the library?"],
        "IT Support": ["How do I reset my university email password?", "Who can help me with my laptop issues?"],
        "Student Centre": ["What services are available at the Student Centre?", "Where is the Student Centre located?"],
    },
)

render_section(
    "Employability and Career Advice",
    {
        "Career Services": ["How do I book an appointment with career services?", "What career workshops are available?"],
        "Internships": ["Where can I find internship opportunities?", "Can the university help me get an internship?"],
    },
)

render_section(
    "Social and Extracurricular Activities",
    {
        "Clubs and Societies": ["What clubs are available?", "How do I join a club?"],
        "Event Schedule": ["What events are happening this month?", "Where can I find the events calendar?"],
        "Sports Information": ["What sports facilities are on campus?", "How do I join the football team?"],
    },
)

render_section(
    "Well-being and Mental Health Support",
    {
        "Well-being Support": ["Where can I get well-being support?", "What mental health services are available?"],
        "Contact Mental Health Services": ["How do I contact the counseling center?", "Is there a crisis hotline available?"],
    },
)

render_section(
    "Visa and Fees Information",
    {
        "Visa Information": ["What documents do I need for my student visa?", "How do I renew my visa?"],
        "Fees and Payment": ["Where can I pay my tuition fees?", "What payment methods are accepted?"],
    },
)

render_section(
    "Housing and Accommodation",
    {
        "Accommodation Info": ["What housing options are available?", "How do I report a housing issue?"],
        "Move-in Process": ["What do I need for move-in day?", "Can I check-in early?"]
    },
)
