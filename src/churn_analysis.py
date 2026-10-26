import os
import pandas as pd

# Load dataset robustly whether executed from repo root or src directory
data_path = "data/WA_Fn-UseC_-Telco-Customer-Churn.csv"
if not os.path.exists(data_path):
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "WA_Fn-UseC_-Telco-Customer-Churn.csv")

df = pd.read_csv(data_path)

# Churn counts
churn_counts = df["Churn"].value_counts()

print("Churn Counts:")
print(churn_counts)

# Churn percentages
churn_percentages = df["Churn"].value_counts(normalize=True) * 100

print("\nChurn Percentages:")
print(churn_percentages)

# Churn summary
total_customers = len(df)

print("\nTotal Customers:", total_customers)
print("Churn Rate:", round(churn_percentages["Yes"], 2), "%")
print("Retention Rate:", round(churn_percentages["No"], 2), "%")

# Check missing values in Churn
print("\nMissing Churn Values:", df["Churn"].isnull().sum())