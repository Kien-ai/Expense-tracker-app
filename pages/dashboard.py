import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Expense Dashboard", layout="wide")
st.header("📊 Spending Dashboard")

# -----------------------------
# Check data availability
# -----------------------------
if 'df' not in st.session_state or st.session_state['df'].empty:
    st.warning("No data available. Please upload or add expenses first.")
    st.stop()

df = st.session_state['df'].copy()

# -----------------------------
# Data cleaning
# -----------------------------
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
df = df.dropna(subset=['Date', 'Amount'])
df['Month'] = df['Date'].dt.to_period('M')

# -----------------------------
# KPI Metrics
# -----------------------------
total_spend = df['Amount'].sum()
monthly_avg = df.groupby('Month')['Amount'].sum().mean()
largest_expense = df['Amount'].max()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Spending", f"${total_spend:,.2f}")
col2.metric("📅 Avg Monthly Spend", f"${monthly_avg:,.2f}")
col3.metric("🔥 Largest Expense", f"${largest_expense:,.2f}")

st.markdown("---")

# -----------------------------
# Spending by Category
# -----------------------------
st.subheader("📊 Spending by Category")
category_sum = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)

if not category_sum.empty:
    # Use Seaborn tab10 palette for better visuals
    palette = sns.color_palette("tab10", n_colors=len(category_sum))
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    category_sum.plot(kind='bar', color=palette, ax=ax1)
    ax1.set_ylabel("Amount ($)")
    ax1.set_xlabel("Category")
    ax1.set_title("Total Spending by Category")
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig1)

st.markdown("---")

# -----------------------------
# Monthly Spending Trend
# -----------------------------
st.subheader("📈 Monthly Spending Trend")
monthly_sum = df.groupby('Month')['Amount'].sum()

if not monthly_sum.empty:
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    sns.lineplot(x=monthly_sum.index.astype(str), y=monthly_sum.values, marker='o', color="#2ca02c", ax=ax2)
    ax2.set_ylabel("Amount ($)")
    ax2.set_xlabel("Month")
    ax2.set_title("Monthly Spending Over Time")
    plt.xticks(rotation=45)
    st.pyplot(fig2)

st.markdown("---")

# -----------------------------
# Top 5 Expenses
# -----------------------------
st.subheader("⚡ Top 5 Highest Expenses")
top_expenses = df.sort_values(by='Amount', ascending=False).head(5)
st.dataframe(top_expenses[['Date', 'Category', 'Amount']], use_container_width=True)

st.markdown("---")

# -----------------------------
# Download filtered data
# -----------------------------
st.subheader("💾 Download Your Data")
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", data=csv, file_name="filtered_expenses.csv", mime="text/csv")
