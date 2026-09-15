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

# Average tenure by churn status
print("\nAverage Tenure by Churn Status:")
print(df.groupby("Churn")["tenure"].mean())

# Churn count by contract type
print("\nChurn Count by Contract Type:")
print(pd.crosstab(df["Contract"], df["Churn"]))

# Churn rate by contract type
print("\nChurn Rate by Contract Type:")
contract_churn_rate = pd.crosstab(
    df["Contract"],
    df["Churn"],
    normalize="index"
) * 100

print(contract_churn_rate["Yes"].round(2))

# Average monthly charges by churn status
print("\nAverage Monthly Charges by Churn Status:")
print(df.groupby("Churn")["MonthlyCharges"].mean().round(2))

# Churn count by internet service
print("\nChurn Count by Internet Service:")
print(pd.crosstab(df["InternetService"], df["Churn"]))

# Churn rate by Internet Service
print("\nChurn Rate by Internet Service:")
internet_churn_rate = pd.crosstab(
    df["InternetService"],
    df["Churn"],
    normalize="index"
) * 100

print(internet_churn_rate.round(2))

# Churn count by payment method
print("\nChurn Count by Payment Method:")
payment_churn = pd.crosstab(
    df["PaymentMethod"],
    df["Churn"]
)

print(payment_churn)

# Churn rate by payment method
print("\nChurn Rate by Payment Method:")
payment_churn_rate = pd.crosstab(
    df["PaymentMethod"],
    df["Churn"],
    normalize="index"
) * 100

print(payment_churn_rate.round(2))

# Average tenure by contract type
print("\nAverage Tenure by Contract Type:")
contract_tenure = df.groupby("Contract")["tenure"].mean()

print(contract_tenure.round(2))

# Churn count by senior citizen status
print("\nChurn Count by Senior Citizen Status:")
print(pd.crosstab(df["SeniorCitizen"], df["Churn"]))

# Churn rate by senior citizen status
print("\nChurn Rate by Senior Citizen Status:")
senior_churn_rate = pd.crosstab(
    df["SeniorCitizen"],
    df["Churn"],
    normalize="index"
) * 100

print(senior_churn_rate["Yes"].round(2))

# Churn count by partner status
print("\nChurn Count by Partner Status:")
print(pd.crosstab(df["Partner"], df["Churn"]))

# Churn rate by partner status
print("\nChurn Rate by Partner Status:")
partner_churn_rate = pd.crosstab(
    df["Partner"],
    df["Churn"],
    normalize="index"
) * 100

print(partner_churn_rate["Yes"].round(2))

# Average tenure and monthly charges by churn status
print("\nCustomer Profile by Churn Status:")
profile = df.groupby("Churn")[["tenure", "MonthlyCharges"]].mean().round(2)

print(profile)

# Numerical feature summary by churn status
print("\nNumerical Feature Summary by Churn Status:")
print(
    df.groupby("Churn")[["tenure", "MonthlyCharges", "TotalCharges"]]
    .mean()
    .round(2)
)