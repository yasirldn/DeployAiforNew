import firebase_admin
from firebase_admin import credentials, auth, db, storage
import streamlit as st

cred = credentials.Certificate("~/.firebase/serviceAccountKey.json")
# cred = credentials.Certificate(st.secrets["firebase"])

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ai-for-new-students-default-rtdb.europe-west1.firebasedatabase.app',  # This is my database URL
    'storageBucket': 'your-storage-bucket.appspot.com'          # This is my storage bucket URL
})


auth = auth
db = db
storage = storage
