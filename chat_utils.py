from firebase_config import db  # this Imports the firebase database reference from your config
import time     # Import time  to get timestamps


def save_chat_message(uid, user_msg, bot_msg):
            # condition to Skip saving if either user or bot message is missing/empty

    if not user_msg or not bot_msg:
        print("Skipping save due to missing message:", user_msg, bot_msg)
        return
    
    try:
        # Pushing both the the user and bot messages to the Firebase database
        # Getting a reference to the user's chat history node in Firebase Realtime Database

        ref = db.reference(f"chat_history/{uid}")
         # Pushing a new chat message entry with user message  bot reply  and current timestamp

        ref.push({
            "user": user_msg,
            "bot": bot_msg,
            "timestamp": time.time() # Unix timestamp for when the message was saved in epoch time from 1970
        })
        print(f"Saved chat message to Firebase for user {uid}: {user_msg} -> {bot_msg}")
    except Exception as e:
                # Catch any errors and print error message

        print(f"Error saving chat message to Firebase: {e}")


def get_chat_history(uid):
    try:
                # geeting a reference to user's chat history in Firebase

        ref = db.reference(f"chat_history/{uid}")
        # to get all chat history data as a dictionary
        data = ref.get()
        
        if not data:
            # returns empty
            print(f"No chat history found for the user {uid}")
            return []
        
        history = []
    
    # now loop through all saved chat entries

        for entry in data.values():
            user_msg = entry.get("user", "[Missing user message]")
            bot_msg = entry.get("bot", "[Missing bot reply]")
            # Append a tuple 
            history.append((user_msg, bot_msg))
        
        print(f"Retrieved chat history for the user {uid}: {history}")
        return history
         # Handle errors 
    except Exception as e:
        print(f"Error retrieving chat history from Firebase database: {e}")
        return []
