import streamlit as st
import pandas as pd

st.header("📤 Upload Expense CSV")

uploaded = st.file_uploader("Upload CSV", type="csv")

if uploaded:
    new_df = pd.read_csv(uploaded)
    required = {"Date", "Category", "Amount"}

    if not required.issubset(new_df.columns):
        st.error("CSV must contain Date, Category, Amount")
    else:
        new_df["Date"] = pd.to_datetime(new_df["Date"])
        new_df["Amount"] = pd.to_numeric(new_df["Amount"])

        st.session_state["df"] = pd.concat(
            [st.session_state["df"], new_df],
            ignore_index=True
        )

        st.success("Data uploaded and merged successfully!")
