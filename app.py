import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression

st.title("💰 Expense Tracker with Insights")
st.write("Upload your expense CSV and explore your spending patterns.")

file = st.file_uploader("Upload CSV", type="csv")

if file is not None:
    df = pd.read_csv(file)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    df = df.dropna(subset=['Amount'])
    df = df[df['Amount'] > 0]
    df['Month'] = df['Date'].dt.to_period('M')

    st.subheader("First 5 Rows of Your Data")
    st.write(df.head())

    # Spending by Category
    category_sum = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
    st.subheader("Spending by Category")
    st.bar_chart(category_sum)

    # Monthly Spending Trend
    monthly_sum = df.groupby('Month')['Amount'].sum()
    st.subheader("Monthly Spending Trend")
    st.line_chart(monthly_sum)

    # Spending Type by Month using KMeans
    monthly_cat = df.groupby(['Month', 'Category'])['Amount'].sum().unstack().fillna(0)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(monthly_cat)
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)
    monthly_cat['Cluster'] = clusters
    cluster_names = {0: "Saver", 1: "Balanced", 2: "High Spender"}
    monthly_cat['Spending_Type'] = monthly_cat['Cluster'].map(cluster_names)
    st.subheader("Spending Type by Month")
    st.write(monthly_cat[['Spending_Type']])

    # Budget prediction
    monthly_total = df.groupby('Month')['Amount'].sum().reset_index()
    monthly_total['Month_Num'] = range(1, len(monthly_total) + 1)
    X = monthly_total[['Month_Num']]
    y = monthly_total['Amount']
    model = LinearRegression()
    model.fit(X, y)
    next_month_df = pd.DataFrame({'Month_Num': [monthly_total['Month_Num'].max() + 1]})
    predicted_budget = model.predict(next_month_df)
    st.subheader("Estimated Next Month Spending")
    st.write(f"${predicted_budget[0]:.2f}")
