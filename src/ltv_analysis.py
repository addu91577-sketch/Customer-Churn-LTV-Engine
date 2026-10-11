
import pandas as pd

# Load dataset
df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")

# Convert TotalCharges to numeric
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"], errors="coerce"
)

# Handle missing values
df["TotalCharges"] = df["TotalCharges"].fillna(0)

# Calculate annualized revenue estimate
df["EstimatedAnnualValue"] = df["MonthlyCharges"] * 12

print("CUSTOMER LTV ANALYSIS")
print("-" * 40)

print("\nTotal Customers:", len(df))

print("\nOverall Customer Value Summary:")
print(
    df[["MonthlyCharges", "TotalCharges", "EstimatedAnnualValue"]]
    .describe()
    .round(2)
)

# Compare customer value by churn status
print("\nCustomer Value by Churn Status:")
print(
    df.groupby("Churn")[
        ["MonthlyCharges", "TotalCharges", "EstimatedAnnualValue"]
    ]
    .mean()
    .round(2)
)

# Compare value by contract type
print("\nCustomer Value by Contract Type:")
print(
    df.groupby("Contract")[
        ["MonthlyCharges", "TotalCharges", "EstimatedAnnualValue"]
    ]
    .mean()
    .round(2)
)

# Identify high-value customers
high_value = df[
    df["EstimatedAnnualValue"] >= df["EstimatedAnnualValue"].quantile(0.75)
]

print("\nHigh-Value Customer Analysis:")
print("Number of high-value customers:", len(high_value))
print("Churned high-value customers:", (high_value["Churn"] == "Yes").sum())
print(
    "High-value customer churn rate:",
    round((high_value["Churn"] == "Yes").mean() * 100, 2),
    "%"
)

print("\nLTV analysis completed successfully.")
