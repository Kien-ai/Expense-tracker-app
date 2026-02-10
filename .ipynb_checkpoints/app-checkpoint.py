{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "da1d4baa-35ac-4012-ba16-f0b00e9ba127",
   "metadata": {},
   "outputs": [],
   "source": [
    "import streamlit as st\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "from sklearn.preprocessing import StandardScaler\n",
    "from sklearn.cluster import KMeans\n",
    "from sklearn.linear_model import LinearRegression\n",
    "from sklearn.decomposition import PCA"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "93012229-93c0-456a-b680-5527eb3c0c0b",
   "metadata": {},
   "outputs": [],
   "source": [
    "st.title(\"💰 Expense Tracker with Insights\")\n",
    "st.write(\"Upload your expense CSV and explore your spending patterns.\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "f2e2b846-9000-46d1-ad40-db75e1816a10",
   "metadata": {},
   "outputs": [],
   "source": [
    "file = st.file_uploader(\"Upload CSV\", type=\"csv\")\n",
    "\n",
    "if file is not None:\n",
    "    df = pd.read_csv(file)\n",
    "    \n",
    "    # Convert Date and clean\n",
    "    df['Date'] = pd.to_datetime(df['Date'])\n",
    "    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')\n",
    "    df = df.dropna(subset=['Amount'])\n",
    "    df = df[df['Amount'] > 0]\n",
    "    df['Month'] = df['Date'].dt.to_period('M')\n",
    "    \n",
    "    st.subheader(\"First 5 Rows of Your Data\")\n",
    "    st.write(df.head())\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "26c25120-ca3b-4546-830e-54528116aa0d",
   "metadata": {},
   "outputs": [],
   "source": [
    "    category_sum = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)\n",
    "    \n",
    "    st.subheader(\"Spending by Category\")\n",
    "    st.bar_chart(category_sum)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "71184ebe-4578-485e-b0c0-3c544eaa4188",
   "metadata": {},
   "outputs": [],
   "source": [
    "    monthly_sum = df.groupby('Month')['Amount'].sum()\n",
    "    \n",
    "    st.subheader(\"Monthly Spending Trend\")\n",
    "    st.line_chart(monthly_sum)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "880a1d18-4841-44ec-baed-0dcbce0774a8",
   "metadata": {},
   "outputs": [],
   "source": [
    "    # Prepare monthly category matrix\n",
    "    monthly_cat = df.groupby(['Month', 'Category'])['Amount'].sum().unstack().fillna(0)\n",
    "    \n",
    "    # Scale\n",
    "    scaler = StandardScaler()\n",
    "    X_scaled = scaler.fit_transform(monthly_cat)\n",
    "    \n",
    "    # KMeans\n",
    "    kmeans = KMeans(n_clusters=3, random_state=42)\n",
    "    clusters = kmeans.fit_predict(X_scaled)\n",
    "    monthly_cat['Cluster'] = clusters\n",
    "    \n",
    "    # Map cluster names\n",
    "    cluster_names = {0:\"Saver\", 1:\"Balanced\", 2:\"High Spender\"}\n",
    "    monthly_cat['Spending_Type'] = monthly_cat['Cluster'].map(cluster_names)\n",
    "    \n",
    "    st.subheader(\"Spending Type by Month\")\n",
    "    st.write(monthly_cat[['Spending_Type']])\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "7a229526-e65a-442d-bc55-4d174b94055f",
   "metadata": {},
   "outputs": [],
   "source": [
    "    monthly_total = df.groupby('Month')['Amount'].sum().reset_index()\n",
    "    monthly_total['Month_Num'] = range(1, len(monthly_total) + 1)\n",
    "    \n",
    "    X = monthly_total[['Month_Num']]\n",
    "    y = monthly_total['Amount']\n",
    "    \n",
    "    model = LinearRegression()\n",
    "    model.fit(X, y)\n",
    "    \n",
    "    next_month_df = pd.DataFrame({'Month_Num': [monthly_total['Month_Num'].max() + 1]})\n",
    "    predicted_budget = model.predict(next_month_df)\n",
    "    \n",
    "    st.subheader(\"Estimated Next Month Spending\")\n",
    "    st.write(f\"${predicted_budget[0]:.2f}\")\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.2"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
