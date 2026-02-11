import pandas as pd

def generate_insights(df):
    df["Month"] = pd.to_datetime(df["Date"]).dt.to_period("M")

    cur = df["Month"].max()
    prev = cur - 1

    insights = []

    cat_sum = df.groupby(["Month", "Category"])["Amount"].sum().unstack().fillna(0)

    if prev in cat_sum.index:
        change = ((cat_sum.loc[cur] - cat_sum.loc[prev]) / cat_sum.loc[prev]) * 100
        top = change.idxmax()
        insights.append(f"You spent {change[top]:.0f}% more on {top} this month.")

    biggest = df.groupby("Category")["Amount"].sum().idxmax()
    insights.append(f"{biggest} is your highest spending category overall.")

    return insights
