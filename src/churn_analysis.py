import pandas as pd

# Load dataset
df = pd.read_csv("../data/WA_Fn-UseC_-Telco-Customer-Churn.csv")

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

# Check TotalCharges data type
print("\nTotalCharges Data Type:")
print(df["TotalCharges"].dtype)

# Check blank values
print("\nBlank TotalCharges Values:")
print(df["TotalCharges"].astype(str).str.strip().eq("").sum())

# Convert TotalCharges to numeric
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

print("\nTotalCharges Data Type After Conversion:")
print(df["TotalCharges"].dtype)

print("\nMissing TotalCharges Values After Conversion:")
print(df["TotalCharges"].isnull().sum())

# Fill missing TotalCharges with 0
df["TotalCharges"] = df["TotalCharges"].fillna(0)

print("\nMissing TotalCharges Values After Filling:")
print(df["TotalCharges"].isnull().sum())

# Verify TotalCharges cleaning
print("\nTotalCharges Summary:")
print(df["TotalCharges"].describe())

# Verify zero TotalCharges customers
print("\nCustomers with Zero TotalCharges:")
print(df[df["TotalCharges"] == 0][["tenure", "TotalCharges"]])