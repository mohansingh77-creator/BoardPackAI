def generate_commentary(df):

    revenue_row = df[df["Account"] == "Revenue"]

    if not revenue_row.empty:
        revenue_var = revenue_row["Variance %"].iloc[0]
    else:
        revenue_var = 0

    largest_var = df.iloc[
        df["Variance %"].abs().idxmax()
    ]

    return f"""
EXECUTIVE SUMMARY

The company delivered a solid financial performance during the reporting period.
Revenue variance against budget was {revenue_var:.2f}%.

KEY VARIANCES

• Revenue variance: {revenue_var:.2f}%
• Largest variance account: {largest_var['Account']}
• Variance percentage: {largest_var['Variance %']:.2f}%

RISKS

• Monitor operating expenses closely.
• Review accounts with significant unfavorable variances.
• Maintain budget discipline across business functions.

OPPORTUNITIES

• Leverage strong revenue performance.
• Improve operational efficiency.
• Continue investment in growth initiatives.

MANAGEMENT RECOMMENDATIONS

1. Investigate high-variance accounts.
2. Strengthen monthly variance reviews.
3. Focus on EBITDA improvement initiatives.
4. Continue revenue growth programs.
"""