import sys
import os

# I Start by adding root directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from firebase_config import auth, db
import time
import streamlit.components.v1 as components
from chat_utils import save_chat_message             #, get_chat_history
from streamlit_js_eval import streamlit_js_eval
import json

# # Start retrieving relevant secrets from secrets.toml

# integration_id = st.secrets["watson"]["integration_id"]
# region = st.secrets["watson"]["region"]
# service_instance_id = st.secrets["watson"]["service_instance_id"]


# I start by Initialising the session state variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# I create a function to be used for registering new users on firebase
def signup():
    st.title("Sign Up")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")

    if st.button("Register"):
        try:
            user = auth.create_user(email=email, password=password)
            db.reference("users").child(user.uid).set({"email": email})
            st.success("Your account created successfully! Please login using the same details.")
        except Exception as e:
            st.error(f"Error: {e}")

# I create a function to be used for loging in an existing user
def login():
    st.title("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        try:
            user = auth.get_user_by_email(email)
            st.session_state.authenticated = True
            st.session_state.user = {'email': email, 'uid': user.uid}
            st.success("Logged in successfully!")
            time.sleep(2)
            st.rerun()
        except Exception as e:
            st.error(f"Login failed: {e}")

# I then create a function to  logout
def logout():
    st.session_state.authenticated = False
    st.session_state.user = None
    st.rerun()

# Authentication Flow
if not st.session_state.authenticated:
    option = st.selectbox("Choose an option", ["Login", "Sign Up"])
    if option == "Login":
        login()
    else:
        signup()
else:
    st.sidebar.button("Logout", on_click=logout)
    st.success(f"Welcome back, {st.session_state.user['email']}!")
    st.write("You are logged in!")

    # Watson Assistant embed script
    watson_script = """
    <script>
    window.watsonAssistantChatOptions = {
        integrationID: "b7b7c8ae-f11e-4bdd-a1b3-6bee7697de11",
        region: "eu-gb",
        serviceInstanceID: "1be8a1d9-b9c1-4017-ad84-d1858b6d1605",
        onLoad: async (instance) => {
            window.chatInstance = instance;
            instance.on({
                type: "send",
                handler: async (event) => {
                    window.lastUserMessage = event.data.message;
                    sendToStreamlit("user", event.data.message);
                }
            });
            instance.on({
                type: "receive",
                handler: async (event) => {
                    sendToStreamlit("bot", event.data.message);
                }
            });
            await instance.render();
        }
    };
    function sendToStreamlit(sender, message) {
        const payload = {
            sender: sender,
            message: message,
        };
        const json = JSON.stringify(payload);
        window.parent.postMessage({ isWatsonMessage: true, data: json }, "*");
    }
    setTimeout(function(){
        const t=document.createElement('script');
        t.src="https://web-chat.global.assistant.watson.appdomain.cloud/versions/latest/WatsonAssistantChatEntry.js";
        document.head.appendChild(t);
    });
    </script>
    """

    components.html(watson_script, height=700)

    # Listen for chat messages
    event = streamlit_js_eval(js_expressions="""
    (() => {
        return new Promise((resolve) => {
            window.addEventListener("message", (e) => {
                if (e.data?.isWatsonMessage) {
                    resolve(JSON.stringify(e.data.data));
                }
            });
        });
    })()
    """, key="watson_listener")

    # Save chat to Firebase
    if event:
        try:
            data = json.loads(event)
            if data['sender'] == "user":
                st.session_state.last_user_msg = data['message']
                st.write("Streamlit JS event:", event)
                st.write("Incoming event data:", data)
                st.write("Session last_user_msg (before):", st.session_state.get("last_user_msg"))
                
            elif data['sender'] == "bot":
                # Save the chat message to Firebase
                uid = st.session_state.user['uid']
                save_chat_message(uid, st.session_state.last_user_msg, data['message'])
                
                # Update the session state for chat history
                st.session_state.chat_history.append((st.session_state.last_user_msg, data['message']))
                st.session_state.last_user_msg = None
                st.rerun()
        except Exception as e:
            st.error(f"Error processing message: {e}")

    # Display Chat History
    st.header("Chat History")
    for user_msg, bot_msg in st.session_state.chat_history:
        st.markdown(f"**You:** {user_msg}")
        st.markdown(f"**Bot:** {bot_msg}")

    st.markdown("---")
