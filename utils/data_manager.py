import pandas as pd
import os

DATA_DIR = "data/users"

def user_file(username):
    os.makedirs(DATA_DIR, exist_ok=True)
    return f"{DATA_DIR}/{username}.csv"

def load_user_data(username):
    path = user_file(username)
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

def save_user_data(username, df):
    df.to_csv(user_file(username), index=False)
