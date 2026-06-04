import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from variance import calculate_variance
from ai_summary import generate_commentary
from ppt_generator import create_ppt

st.title("📊 BoardPack AI")

st.markdown(
    "### AI-Powered Executive Reporting & Board Pack Generation"
)

company_name = st.text_input(
    "Company Name",
    "ABC Corporation"
)

report_date = st.date_input(
    "Reporting Date"
)

uploaded_file = st.file_uploader(
    "Upload Finance Excel",
    type=["xlsx"]
)

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    df.columns = df.columns.str.strip()

    result = calculate_variance(df)

    # KPI Calculations
    total_budget = result["Budget"].sum()
    total_actual = result["Actual"].sum()
    total_variance = result["Variance"].sum()

    # EBITDA Calculation
    revenue = result[
        result["Account"].str.contains(
            "Revenue",
            case=False,
            na=False
        )
    ]["Actual"].sum()

    expenses = result[
        ~result["Account"].str.contains(
            "Revenue",
            case=False,
            na=False
        )
    ]["Actual"].sum()

    ebitda = revenue - expenses

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Budget", f"{total_budget:,.0f}")
    col2.metric("Actual", f"{total_actual:,.0f}")
    col3.metric("Variance", f"{total_variance:,.0f}")
    col4.metric("EBITDA", f"{ebitda:,.0f}")

    # Traffic Light Status
    if total_variance > 0:
        st.success(
            "🟢 Overall Performance Above Budget"
        )
    elif total_variance < 0:
        st.error(
            "🔴 Overall Performance Below Budget"
        )
    else:
        st.info(
            "🟡 Performance In Line With Budget"
        )

    # Executive Summary
    revenue_row = result[
        result["Account"] == "Revenue"
    ]

    if not revenue_row.empty:

        revenue_variance = revenue_row[
            "Variance %"
        ].iloc[0]

        st.success(
            f"""
📈 Revenue variance: {revenue_variance:.2f}%

⚠️ Review expense categories with high variance.

✅ Financial performance summary generated automatically.
"""
        )

    # Variance Table
    st.subheader("Variance Analysis")

    st.dataframe(
        result.style.highlight_max(
            subset=["Variance %"]
        )
    )

    # Chart
    st.subheader("Budget vs Actual")

    expense_chart = result[
        result["Account"] != "Revenue"
    ]

    chart_df = expense_chart.set_index(
        "Account"
    )[["Budget", "Actual"]]

    fig, ax = plt.subplots(
        figsize=(10, 5)
    )

    chart_df.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title(
        "Budget vs Actual Analysis",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Account")
    ax.set_ylabel("Amount")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        "budget_vs_actual.png"
    )

    st.pyplot(fig)

    # Variance % Chart
    st.subheader(
        "Variance % by Account"
    )

    variance_chart = result.set_index(
        "Account"
    )["Variance %"]

    st.bar_chart(
        variance_chart
    )

    # Top Variances
    st.subheader(
        "Top Variances"
    )

    top_var = result.sort_values(
        by="Variance %",
        ascending=False
    ).head(5)

    st.dataframe(top_var)

    # AI Commentary
    if st.button(
        "Generate AI Commentary"
    ):

        commentary = generate_commentary(
            result
        )

        st.subheader(
            "AI Board Commentary"
        )

        st.write(commentary)

        ppt_file = create_ppt(
            company_name,
            report_date,
            total_budget,
            total_actual,
            total_variance,
            ebitda,
            commentary
        )

        with open(
            ppt_file,
            "rb"
        ) as file:

            st.download_button(
                label="📥 Download Board Pack PPT",
                data=file,
                file_name="BoardPackAI.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )

    # CFO Copilot
    # CFO Copilot
st.subheader("💬 CFO Copilot")

question = st.selectbox(
    "Choose a finance question",
    [
        "",
        "What is revenue?",
        "What is EBITDA?",
        "What is the largest variance?",
        "What is the highest expense?",
        "Show top 3 variances",
        "What is the budget?",
        "What is the variance?"
    ]
)

if question:

    q = question.lower()

    if "revenue" in q:

        st.success(
            f"Revenue = {revenue:,.0f}"
        )

    elif "ebitda" in q:

        st.success(
            f"EBITDA = {ebitda:,.0f}"
        )

    elif "budget" in q:

        st.success(
            f"Total Budget = {total_budget:,.0f}"
        )

    elif "variance" in q and "largest" not in q:

        st.success(
            f"Total Variance = {total_variance:,.0f}"
        )

    elif "largest variance" in q:

        top_account = result.loc[
            result["Variance %"].abs().idxmax()
        ]

        st.success(
            f"Largest variance is "
            f"{top_account['Account']} "
            f"at {top_account['Variance %']:.2f}%"
        )

    elif "highest expense" in q:

        expense_rows = result[
            ~result["Account"].str.contains(
                "Revenue",
                case=False,
                na=False
            )
        ]

        top_expense = expense_rows.loc[
            expense_rows["Actual"].idxmax()
        ]

        st.success(
            f"Highest expense is "
            f"{top_expense['Account']} "
            f"at {top_expense['Actual']:,.0f}"
        )

    elif "top 3 variances" in q:

        top3 = result.sort_values(
            by="Variance %",
            ascending=False
        ).head(3)

        st.dataframe(top3)