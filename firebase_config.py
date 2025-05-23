import firebase_admin
from firebase_admin import credentials, auth, db, storage
import streamlit as st

# cred = credentials.Certificate("~/.firebase/serviceAccountKey.json")

# I'm now converting st.secrets["firebase"] to a normal dictionary

# cred_dict = dict(st.secrets["firebase"])
cred_dict = {
  "type": "service_account",
  "project_id": "ai-for-new-students",
  "private_key_id": "468d31ddf60f555c093205b72fafea3323a636b2",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDVfGvUkGnJdpJs\nJ3mBHhICCrzBuO+5w9kGYPV2U4/YCVZaiB/LmWW4KnPXkXQwNqcLyEcn4IrmlLhP\n5b8IBvlRpIITgOALvcJcDWF0DgdNNeOA1CFXLt/c+WVKM/yKds1qZuNtfWXK07FK\nX+qu1Wg9r0hfadmQqI0vSoQn9ClEz/RZbWpmTnqdGcAew634waAdsPpN/oNs2Lr3\n2NiWWtegSq8mLEjzx2tz6Yr4Kv41nyDWrFHYJBYJGg67hS+L2nYsLLMyjMYKsOZq\nT2kk9yDq2HJeeRax/nH3ubX1/ORi5XrZgEQzGmyIV5k4QTJQVooPWYNDRoFPYByd\nMgGSBzxPAgMBAAECggEAFBO1bbIpy2Ez9/6RC2GGlAaVJdV8m13Ib98idn75TM85\nUx5GJIxH5//7Zk8u5scyV9tSmx9021EqhukLrszpGZJ9C9SCPYMaX4nVRmgjVlGL\nvwvexCeLtL5c65OOsSmRu+tH1tOE2oRPbLfZ3ENZoE4ht5y+xz9IDSXW3o20a9zE\nDKIReKbWAY2NbMISfFf1Cy1NOJQO0TitYSlqqWWNjv5WGS07K5lwJZn+D2kdmI5t\n6i+g6TL9mHZo4hITjbd23ahAJQ9w9VWblaVYqgk67IOk5cPyRvm6E2Zq7QUZ/y/7\nS3XLpkddEKPveYX5GNqiCVuvO4K29WcsIdKgFuNuQQKBgQD2nd0efKT5DBpIU3cn\nTcdDxDWWGbsCqzKJFKxNXigtn55kU59g/GWrbnfPZ/ZgxQIJj+tJINr1L1q8R2GD\nNREqZ9gdbOs/dgzjsCMpAwYKR6Qs38W4alHDsJkI5ox85g2I2YQxcJwL6dpzovQK\nMzISlB1ZSDz7dC3IkhXLWdFO3wKBgQDdm9pdWwrk/MKzpf4qTWSUbm3x5vQjlGVf\nscS9KteT2uhHvchX8MQlPiYfomeifkOaVpyvoONVCt7OS0F745QiKBva6p17arGK\neFdaGrgIlM8kWJdJxz7CuNw9KHhkbgCTPPEd+Kt8K87bbCX58mY5Avxzcxskb4ep\nmAYsdwhwkQKBgQCVo9hF5W/cxiE0faCxMpqUXfv95gL5bZOuZeLe1yEd/dqIGc19\ndejjCpacPQLcWO4Ri0hDCTKSz3cJA28BxDN0Pap+wFZGHYVYqsnK2tDRcAMIT4eT\njL+sM/3Hzsy0BIt13DZAIYouGGm6/MeDYOkjKMheIl0OXsJhD3M1/nvolQKBgHKJ\nKsM1WtwfB0JyeHrEpUdSC+EKzQPWns5mwphCnEj+yy7JF9LbzYSyKmIPPiDtwWLz\ngOgE73n0tFNK8f1mEhnVQRBUUjCHZFt89yjKxnMo9iaC4y5unDFn+exiDldZw1JW\nHQiwjXEP80nVC4uzjMHKmU/SHiUmv6cXu5kfrG0BAoGAGHpUWr9rxDhe/u3mo+GO\nfLrYzXczIleHJVYRSQQzzxP6yxtVSHno8Tii1vJo9L5Pv/d9WiOMDgz0PCqG8fQr\nLzmSxn6fkTXD2ZAm9kpEqT0BLI73q7SoEhR254K0g2aIQU5ISjMXa3CQShBcDVUK\n76SvdobEGEeZ3Sf6d3e0fbQ=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@ai-for-new-students.iam.gserviceaccount.com",
  "client_id": "115622082007292513371",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40ai-for-new-students.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
cred = credentials.Certificate(cred_dict)

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ai-for-new-students-default-rtdb.europe-west1.firebasedatabase.app',  # This is my database URL
    'storageBucket': 'your-storage-bucket.appspot.com'          # This is my storage bucket URL
})


auth = auth
db = db
storage = storage
