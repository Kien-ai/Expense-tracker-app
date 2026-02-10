import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)

PRIMARY = "#4E79A7"
SUCCESS = "#59A14F"
WARNING = "#E15759"
ACCENT = "#EDC949"

# -----------------------------
# App title
# -----------------------------
st.title("💰 Smart Expense Tracker")
st.caption("Understand your spending • Spot trends • Plan better")

st.markdown("---")

# -----------------------------
# Sidebar – User-friendly
# -----------------------------
st.sidebar.header("⚙️ Controls")

input_mode = st.sidebar.radio(
    "How would you like to add data?",
    ["Upload CSV", "Manual Entry"]
)

show_insights = st.sidebar.checkbox("Show smart insights", value=True)
show_prediction = st.sidebar.checkbox("Estimate next month spending", value=True)

# -----------------------------
# Data input
# -----------------------------
df = None

if input_mode == "Upload CSV":
    file = st.file_uploader("📤 Upload your expense CSV", type="csv")
    if file:
        df = pd.read_csv(file)

else:
    st.subheader("✍️ Add an Expense")
    with st.form("manual_entry"):
        date = st.date_input("Date")
        category = st.text_input("Category")
        amount = st.number_input("Amount", min_value=0.0, step=1.0)
        submitted = st.form_submit_button("Add Expense")

        if submitted:
            df = pd.DataFrame([{
                "Date": date,
                "Category": category,
                "Amount": amount
            }])

# -----------------------------
# Stop if no data
# -----------------------------
if df is None or df.empty:
    st.info("👈 Upload a CSV or add expenses to get started")
    st.stop()

# -----------------------------
# Data cleaning
# -----------------------------
df["Date"] = pd.to_datetime(df["Date"])
df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
df = df.dropna()
df = df[df["Amount"] > 0]
df["Month"] = df["Date"].dt.to_period("M").astype(str)

# -----------------------------
# Filters
# -----------------------------
st.sidebar.subheader("📅 Filters")

months = sorted(df["Month"].unique())
categories = sorted(df["Category"].unique())

selected_months = st.sidebar.multiselect(
    "Select months",
    months,
    default=months
)

selected_categories = st.sidebar.multiselect(
    "Select categories",
    categories,
    default=categories
)

df = df[
    df["Month"].isin(selected_months)
    & df["Category"].isin(selected_categories)
]

# -----------------------------
# Overview metrics
# -----------------------------
st.subheader("📊 Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Total Spent", f"${df['Amount'].sum():,.2f}")
col2.metric("Average Expense", f"${df['Amount'].mean():,.2f}")
col3.metric("Number of Transactions", len(df))

st.markdown("---")

# -----------------------------
# Spending by Category
# -----------------------------
st.subheader("🗂️ Spending by Category")

category_sum = df.groupby("Category")["Amount"].sum().sort_values()

fig1, ax1 = plt.subplots()
category_sum.plot(kind="barh", ax=ax1, color=PRIMARY)
ax1.set_xlabel("Amount ($)")
ax1.set_ylabel("")
st.pyplot(fig1)

# -----------------------------
# Monthly Trend
# -----------------------------
st.subheader("📈 Monthly Spending Trend")

monthly_sum = df.groupby("Month")["Amount"].sum()

fig2, ax2 = plt.subplots()
monthly_sum.plot(marker="o", ax=ax2, color=SUCCESS)
ax2.set_xlabel("Month")
ax2.set_ylabel("Amount ($)")
st.pyplot(fig2)

st.markdown("---")

# -----------------------------
# Smart insights (plain English)
# -----------------------------
if show_insights:
    st.subheader("💡 Smart Insights")

    top_category = category_sum.idxmax()
    top_month = monthly_sum.idxmax()

    st.info(f"📌 You spent the most on **{top_category}**.")
    st.info(f"📅 Your highest spending month was **{top_month}**.")

    threshold = df["Amount"].mean() + 2 * df["Amount"].std()
    outliers = df[df["Amount"] > threshold]

    if not outliers.empty:
        st.warning("🚨 Some expenses are unusually high:")
        st.dataframe(outliers[["Date", "Category", "Amount"]])

st.markdown("---")

# -----------------------------
# Budget prediction
# -----------------------------
if show_prediction and len(monthly_sum) > 1:
    st.subheader("🔮 Estimated Next Month Spending")

    monthly_df = monthly_sum.reset_index()
    monthly_df["Month_Num"] = range(1, len(monthly_df) + 1)

    X = monthly_df[["Month_Num"]]
    y = monthly_df["Amount"]

    model = LinearRegression()
    model.fit(X, y)

    next_month = pd.DataFrame(
        {"Month_Num": [monthly_df["Month_Num"].max() + 1]}
    )
    prediction = model.predict(next_month)

    st.success(f"💰 Estimated spending next month: **${prediction[0]:,.2f}**")

# -----------------------------
# Download data
# -----------------------------
st.markdown("---")
st.subheader("💾 Download")

csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download filtered data",
    csv,
    "filtered_expenses.csv",
    "text/csv"
)
