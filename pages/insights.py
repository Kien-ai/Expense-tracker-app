import streamlit as st
import pandas as pd

st.header("💡 Insights & Recommendations")

# -----------------------------
# Check data
# -----------------------------
if 'df' not in st.session_state or st.session_state['df'].empty:
    st.warning("No data available. Please upload or add expenses first.")
    st.stop()

df = st.session_state['df'].copy()
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
df = df.dropna(subset=['Date', 'Amount'])
df['Month'] = df['Date'].dt.to_period('M')

# -----------------------------
# Insights calculations
# -----------------------------
total_spend = df['Amount'].sum()
category_totals = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)

insights = []

# Top category
if not category_totals.empty and total_spend > 0:
    top_category = category_totals.idxmax()
    top_amount = category_totals.max()
    top_pct = top_amount / total_spend * 100
    insights.append(f"💰 Top spending category: {top_category} (${top_amount:,.2f}, {top_pct:.1f}% of total)")

# Fastest-growing category (month-over-month)
monthly_category = df.groupby([df['Month'], 'Category'])['Amount'].sum().unstack(fill_value=0)
if monthly_category.shape[0] > 1:
    growth_pct = ((monthly_category.iloc[-1] - monthly_category.iloc[-2]) /
                  monthly_category.iloc[-2].replace(0, 1)) * 100
    fastest_growing = growth_pct.idxmax()
    fastest_pct = growth_pct.max()
    insights.append(f"📈 Fastest growing category this month: {fastest_growing} ({fastest_pct:.1f}% increase)")

# High spending alerts (>30% of total)
high_categories = category_totals[category_totals > total_spend * 0.3] if not category_totals.empty else pd.Series()
for cat, amt in high_categories.items():
    insights.append(f"🚨 High spending alert: {cat} - ${amt:,.2f}")

# -----------------------------
# Display insights
# -----------------------------
if insights:
    for item in insights:
        st.markdown(f"- {item}")
else:
    st.info("No insights available yet. Add more expenses to generate recommendations.")
