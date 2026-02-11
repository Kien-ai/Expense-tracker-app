import streamlit as st
import pandas as pd
from datetime import date

st.header("✍️ Add Expense")

with st.form("add_expense"):
    d = st.date_input("Date", date.today())
    cat = st.text_input("Category")
    amt = st.number_input("Amount", min_value=0.0)
    desc = st.text_input("Description (optional)")
    submit = st.form_submit_button("Add")

if submit:
    new_row = {
        "Date": d,
        "Category": cat,
        "Amount": amt,
        "Description": desc
    }
    st.session_state["df"] = pd.concat(
        [st.session_state["df"], pd.DataFrame([new_row])],
        ignore_index=True
    )
    st.success("Expense added!")
