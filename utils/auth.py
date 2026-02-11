import pandas as pd
import hashlib
import os

USERS_FILE = "data/users/users.csv"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(USERS_FILE):
        return pd.DataFrame(columns=["username", "password_hash"])
    return pd.read_csv(USERS_FILE)

def save_users(df):
    os.makedirs("data/users", exist_ok=True)
    df.to_csv(USERS_FILE, index=False)

def signup_user(username, password):
    users = load_users()
    if username in users["username"].values:
        return False
    users = pd.concat(
        [users, pd.DataFrame([{
            "username": username,
            "password_hash": hash_password(password)
        }])],
        ignore_index=True
    )
    save_users(users)
    return True

def login_user(username, password):
    users = load_users()
    hashed = hash_password(password)
    match = users[
        (users["username"] == username) &
        (users["password_hash"] == hashed)
    ]
    return not match.empty
