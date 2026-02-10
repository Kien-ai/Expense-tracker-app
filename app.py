# =============================
# IMPORTS
# =============================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
import io

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="💰 Expense Tracker",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Expense Tracker with Insights")
st.write("Upload a CSV or enter your expenses manually.")

# =============================
# SIDEBAR CONTROLS (ALWAYS DEFINED)
# =============================
st.sidebar.header("Settings")

n_clusters = st.sidebar.slider(
    "Number of spending clusters",
    min_value=2,
    max_value=6,
    value=3
)

show_budget = st.sidebar.checkbox(
    "Show next month budget prediction",
    value=True
)

input_mode = st.sidebar.radio(
    "Input method",
    ["Upload CSV", "Manual Input"]
)

# =============================
# SAMPLE DATA (FALLBACK)
# =============================
sample_data = """Date,Category,Amount
2026-01-01,Food,20
2026-01-02,Transport,15
2026-01-03,Entertainment,50
2026-02-01,Food,30
2026-02-05,Rent,400
2026-03-03,Utilities,80
"""

# =============================
# LOAD DATA
# =============================
df = None

if input_mode == "Upload CSV":
    file = st.file_uploader("Upload CSV file", type="csv")
    if file is None:
        st.info("Using sample data")
        df = pd.read_csv(io.StringIO(sample_data))
    else:
        df = pd.read_csv(file)

else:  # Manual Input
    st.subheader("Enter your expenses")
    editor_df = st.data_editor(
        pd.DataFrame(columns=["Date", "Category", "Amount"]),
        num_rows="dynamic"
    )
    if editor_df.empty:
        st.info("Using sample data")
        df = pd.read_csv(io.StringIO(sample_data))
    else:
        df = editor_df.copy()

# =============================
# DATA CLEANING
# =============================
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

df = df.dropna(subset=["Date", "Amount"])
df = df[df["Amount"] > 0]

df["Month"] = df["Date"].dt.to_period("M")

# =============================
# METRICS
# =============================
col1, col2, col3 = st.columns(3)

col1.metric("Total Spent", f"${df['Amount'].sum():,.2f}")
col2.metric("Average Expense", f"${df['Amount'].mean():,.2f}")
col3.metric("Categories", df["Category"].nunique())

st.divider()

# =============================
# SPENDING BY CATEGORY
# =============================
st.subheader("📊 Spending by Category")
category_sum = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)

fig1, ax1 = plt.subplots()
category_sum.plot(kind="bar", ax=ax1)
ax1.set_ylabel("Amount")
st.pyplot(fig1)

st.divider()

# =============================
# MONTHLY TREND
# =============================
st.subheader("📈 Monthly Spending Trend")
monthly_sum = df.groupby("Month")["Amount"].sum()

fig2, ax2 = plt.subplots()
monthly_sum.plot(marker="o", ax=ax2)
ax2.set_ylabel("Amount")
st.pyplot(fig2)

st.divider()

# =============================
# CLUSTERING (SAFE)
# =============================
st.subheader("🏷️ Spending Type by Month")

monthly_cat = (
    df.groupby(["Month", "Category"])["Amount"]
    .sum()
    .unstack()
    .fillna(0)
)

if len(monthly_cat) < 2:
    st.warning("Not enough data for clustering.")
else:
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(monthly_cat)

    actual_clusters = min(n_clusters, len(monthly_cat))

    if actual_clusters < n_clusters:
        st.info(f"Clusters reduced to {actual_clusters}")

    kmeans = KMeans(
        n_clusters=actual_clusters,
        random_state=42,
        n_init=10
    )

    monthly_cat["Cluster"] = kmeans.fit_predict(X_scaled)
    monthly_cat["Spending Type"] = (
        "Cluster " + (monthly_cat["Cluster"] + 1).astype(str)
    )

    st.dataframe(monthly_cat[["Spending Type"]])

st.divider()

# =============================
# BUDGET PREDICTION
# =============================
if show_budget:
    st.subheader("💵 Estimated Next Month Spending")

    monthly_total = df.groupby("Month")["Amount"].sum().reset_index()
    monthly_total["Month_Num"] = range(1, len(monthly_total) + 1)

    if len(monthly_total) > 1:
        X = monthly_total[["Month_Num"]]
        y = monthly_total["Amount"]

        model = LinearRegression()
        model.fit(X, y)

        next_month = pd.DataFrame(
            {"Month_Num": [monthly_total["Month_Num"].max() + 1]}
        )

        prediction = model.predict(next_month)[0]
        st.success(f"Estimated next month spend: ${prediction:,.2f}")
    else:
        st.info("Not enough data to predict budget")

st.divider()

# =============================
# TOP EXPENSES
# =============================
st.subheader("⚡ Top 5 Expenses")
st.table(
    df.sort_values("Amount", ascending=False)
      .head(5)[["Date", "Category", "Amount"]]
)

# =============================
# DOWNLOAD
# =============================
st.subheader("💾 Download Data")
st.download_button(
    "Download CSV",
    df.to_csv(index=False),
    "expenses_cleaned.csv",
    "text/csv"
)
