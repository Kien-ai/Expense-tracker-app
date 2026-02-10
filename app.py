import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
import io

# -----------------------------
# App Configuration
# -----------------------------
st.set_page_config(page_title="💰 Expense Tracker", page_icon="💰", layout="wide")
st.title("💰 Expense Tracker with Insights")
st.write("Upload your expenses CSV and explore your spending patterns interactively.")

# -----------------------------
# Sample CSV (Fallback)
# -----------------------------
sample_data = """Date,Category,Amount
2026-01-01,Food,20
2026-01-02,Transport,15
2026-01-03,Entertainment,50
2026-01-04,Food,30
2026-01-05,Bills,60
2026-01-06,Shopping,45
"""

# -----------------------------
# Sidebar: Upload & Filters
# -----------------------------
st.sidebar.title("Upload & Settings")
file = st.sidebar.file_uploader("Upload CSV", type="csv")
show_budget = st.sidebar.checkbox("Show next month budget", True)
n_clusters = st.sidebar.slider("Select number of clusters", 2, 6, 3)

# -----------------------------
# Load Data
# -----------------------------
if file is None:
    st.warning("No file uploaded. Using sample data for demonstration.")
    file = io.StringIO(sample_data)

try:
    df = pd.read_csv(file)
except Exception as e:
    st.error(f"Error reading CSV: {e}")
    st.stop()

# -----------------------------
# Preprocess Data
# -----------------------------
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
df = df.dropna(subset=['Date', 'Amount'])
df = df[df['Amount'] > 0]
df['Month'] = df['Date'].dt.to_period('M')

# -----------------------------
# Sidebar: Category Filter
# -----------------------------
categories = df['Category'].unique().tolist()
selected_categories = st.sidebar.multiselect(
    "Select Categories to include", options=categories, default=categories
)
if selected_categories:
    df = df[df['Category'].isin(selected_categories)]

# -----------------------------
# Quick Metrics
# -----------------------------
total_spent = df['Amount'].sum()
average_daily = df['Amount'].mean()
num_categories = len(df['Category'].unique())
col1, col2, col3 = st.columns(3)
col1.metric("Total Spent", f"${total_spent:,.2f}")
col2.metric("Average Daily Spend", f"${average_daily:,.2f}")
col3.metric("Number of Categories", num_categories)

st.markdown("---")

# -----------------------------
# Spending by Category (Bar Chart)
# -----------------------------
category_sum = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
st.markdown("## 📊 Spending by Category")
fig1, ax1 = plt.subplots()
colors = ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F", "#EDC949", "#AF7AA1"]
category_sum.plot(kind='bar', color=colors[:len(category_sum)], ax=ax1)
ax1.set_ylabel("Amount ($)")
ax1.set_xlabel("Category")
ax1.set_title("Total Spending by Category")
st.pyplot(fig1)

st.markdown("---")

# -----------------------------
# Monthly Spending Trend (Line Chart)
# -----------------------------
monthly_sum = df.groupby('Month')['Amount'].sum()
st.markdown("## 📈 Monthly Spending Trend")
fig2, ax2 = plt.subplots()
monthly_sum.plot(kind='line', marker='o', color='#59A14F', ax=ax2)
ax2.set_ylabel("Amount ($)")
ax2.set_xlabel("Month")
ax2.set_title("Monthly Spending Trend")
st.pyplot(fig2)

st.markdown("---")

# -----------------------------
# Spending Distribution (Pie Chart)
# -----------------------------
st.markdown("## 🥧 Spending Distribution by Category")
fig3, ax3 = plt.subplots()
category_sum.plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax3, legend=False, colors=colors[:len(category_sum)])
ax3.set_ylabel("")
st.pyplot(fig3)

st.markdown("---")

# -----------------------------
# Spending Type Clustering
# -----------------------------
monthly_cat = df.groupby(['Month', 'Category'])['Amount'].sum().unstack().fillna(0)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(monthly_cat)

kmeans = KMeans(n_clusters=n_clusters, random_state=42)
clusters = kmeans.fit_predict(X_scaled)
monthly_cat['Cluster'] = clusters
cluster_names = {i: f"Type {i+1}" for i in range(n_clusters)}
monthly_cat['Spending_Type'] = monthly_cat['Cluster'].map(cluster_names)

st.markdown("## 🏷️ Spending Type by Month")
st.dataframe(monthly_cat[['Spending_Type']])

st.markdown("---")

# -----------------------------
# Budget Prediction
# -----------------------------
if show_budget:
    monthly_total = df.groupby('Month')['Amount'].sum().reset_index()
    monthly_total['Month_Num'] = range(1, len(monthly_total) + 1)

    X = monthly_total[['Month_Num']]
    y = monthly_total['Amount']

    model = LinearRegression()
    model.fit(X, y)
    next_month_df = pd.DataFrame({'Month_Num': [monthly_total['Month_Num'].max() + 1]})
    predicted_budget = model.predict(next_month_df)

    st.markdown("## 💵 Estimated Next Month Spending")
    st.write(f"${predicted_budget[0]:,.2f}")

st.markdown("---")

# -----------------------------
# Top 5 Expenses
# -----------------------------
st.markdown("## ⚡ Top 5 Expenses")
top_expenses = df.sort_values(by='Amount', ascending=False).head(5)
st.table(top_expenses[['Date', 'Category', 'Amount']])

st.markdown("---")

# -----------------------------
# Download Filtered Data
# -----------------------------
st.markdown("## 💾 Download Your Data")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download CSV",
    data=csv,
    file_name='filtered_expenses.csv',
    mime='text/csv'
)

st.markdown("---")

# -----------------------------
# Highlight High Spending Outliers
# -----------------------------
threshold = df['Amount'].mean() + 2 * df['Amount'].std()
outliers = df[df['Amount'] > threshold]

if not outliers.empty:
    st.markdown("## 🚨 High Spending Alerts")
    st.dataframe(outliers[['Date', 'Category', 'Amount']].style.apply(
        lambda x: ['background-color: #FFDDDD' if v > threshold else '' for v in x['Amount']], axis=1
    ))
