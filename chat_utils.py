from firebase_config import db
import time


def save_chat_message(uid, user_msg, bot_msg):
    if not user_msg or not bot_msg:
        print("Skipping save due to missing message:", user_msg, bot_msg)
        return
    
    try:
        # Push the user and bot messages to the Firebase database
        ref = db.reference(f"chat_history/{uid}")
        ref.push({
            "user": user_msg,
            "bot": bot_msg,
            "timestamp": time.time()
        })
        print(f"Saved chat message to Firebase for user {uid}: {user_msg} -> {bot_msg}")
    except Exception as e:
        print(f"Error saving chat message to Firebase: {e}")


def get_chat_history(uid):
    try:
        ref = db.reference(f"chat_history/{uid}")
        data = ref.get()
        
        if not data:
            print(f"No chat history found for user {uid}")
            return []
        
        history = []
        for entry in data.values():
            user_msg = entry.get("user", "[Missing user message]")
            bot_msg = entry.get("bot", "[Missing bot reply]")
            history.append((user_msg, bot_msg))
        
        print(f"Retrieved chat history for user {uid}: {history}")
        return history
    
    except Exception as e:
        print(f"Error retrieving chat history from Firebase: {e}")
        return []
