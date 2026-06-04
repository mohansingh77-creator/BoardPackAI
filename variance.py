import pandas as pd

def calculate_variance(df):

    df["Variance"] = df["Actual"] - df["Budget"]

    df["Variance %"] = (
        (df["Variance"] / df["Budget"]) * 100
    ).round(2)

    return df