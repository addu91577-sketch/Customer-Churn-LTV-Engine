
import os
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load dataset
df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")

# Clean numerical data
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"], errors="coerce"
)
df["TotalCharges"] = df["TotalCharges"].fillna(0)

# Features used to group customers
features = ["tenure", "MonthlyCharges", "TotalCharges"]
X = df[features]

# Scale features before clustering
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Create 4 customer segments
kmeans = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)

df["Segment"] = kmeans.fit_predict(X_scaled) + 1

# Create segment summary
summary = df.groupby("Segment").agg(
    Customers=("customerID", "count"),
    AverageTenure=("tenure", "mean"),
    AverageMonthlyCharges=("MonthlyCharges", "mean"),
    AverageTotalCharges=("TotalCharges", "mean"),
    ChurnRate=("Churn", lambda x: (x == "Yes").mean() * 100)
).round(2)

print("\nCUSTOMER SEGMENTATION")
print("=" * 45)
print(summary)

# Save customer assignments and segment summary
os.makedirs("reports", exist_ok=True)

df[["customerID"] + features + ["Churn", "Segment"]].to_csv(
    "reports/customer_segments.csv", index=False
)

summary.to_csv("reports/segment_summary.csv")

print("\nCustomer assignments saved to reports/customer_segments.csv")
print("Segment summary saved to reports/segment_summary.csv")
print("\nCustomer segmentation completed successfully.")
