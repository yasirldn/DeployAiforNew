import firebase_admin
from firebase_admin import credentials, auth, db, storage
import streamlit as st

# cred = credentials.Certificate("~/.firebase/serviceAccountKey.json")

# I'm now converting st.secrets["firebase"] to a normal dictionary

cred_dict = dict(st.secrets["firebase"])
cred = credentials.Certificate(cred_dict)

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ai-for-new-students-default-rtdb.europe-west1.firebasedatabase.app',  # This is my database URL
    'storageBucket': 'your-storage-bucket.appspot.com'          # This is my storage bucket URL
})


auth = auth
db = db
storage = storage
