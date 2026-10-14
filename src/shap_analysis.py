
import os
import pandas as pd
import matplotlib.pyplot as plt
import shap

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

# Load dataset
df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"], errors="coerce"
)

# Separate features and target
X = df.drop(columns=["Churn", "customerID"])
y = df["Churn"].map({"No": 0, "Yes": 1})

# Identify numerical and categorical features
numeric_features = X.select_dtypes(
    include=["number"]
).columns.tolist()

categorical_features = X.select_dtypes(
    include=["object"]
).columns.tolist()

# Preprocessing
numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median"))
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("num", numeric_pipeline, numeric_features),
    ("cat", categorical_pipeline, categorical_features)
])

# Split data consistently
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Train XGBoost model
model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        random_state=42,
        eval_metric="logloss"
    ))
])

model.fit(X_train, y_train)

# Transform test data using the fitted preprocessor
fitted_preprocessor = model.named_steps["preprocessor"]
classifier = model.named_steps["classifier"]

X_test_transformed = fitted_preprocessor.transform(X_test)
feature_names = fitted_preprocessor.get_feature_names_out()

# SHAP explanations
# The transformed dataset is small enough to convert to dense format.
X_test_dense = (
    X_test_transformed.toarray()
    if hasattr(X_test_transformed, "toarray")
    else X_test_transformed
)

explainer = shap.TreeExplainer(classifier)
shap_values = explainer(X_test_dense)

# Output directory
os.makedirs("reports", exist_ok=True)

# Global feature importance
print("\nTOP FEATURES INFLUENCING CHURN")
print("=" * 45)

importance = pd.DataFrame({
    "Feature": feature_names,
    "MeanAbsoluteSHAP": abs(shap_values.values).mean(axis=0)
}).sort_values("MeanAbsoluteSHAP", ascending=False)

print(importance.head(15).round(4).to_string(index=False))

importance.to_csv(
    "reports/shap_feature_importance.csv", index=False
)

# SHAP summary plot
shap.summary_plot(
    shap_values,
    features=X_test_dense,
    feature_names=feature_names,
    max_display=15,
    show=False
)
plt.tight_layout()
plt.savefig("reports/shap_summary.png", dpi=150, bbox_inches="tight")
plt.close()

# SHAP importance bar plot
shap.summary_plot(
    shap_values,
    features=X_test_dense,
    feature_names=feature_names,
    plot_type="bar",
    max_display=15,
    show=False
)
plt.tight_layout()
plt.savefig("reports/shap_importance.png", dpi=150, bbox_inches="tight")
plt.close()

# Explain one individual customer prediction
# Select the first actual churned customer in the test set, if available.
churned_positions = [
    i for i, value in enumerate(y_test.to_numpy()) if value == 1
]

example_idx = churned_positions[0] if churned_positions else 0

customer = X_test.iloc[[example_idx]]
prediction = int(model.predict(customer)[0])
probability = float(model.predict_proba(customer)[0, 1])

print("\nINDIVIDUAL CUSTOMER EXPLANATION")
print("=" * 45)
print("Actual churn:", "Yes" if y_test.iloc[example_idx] == 1 else "No")
print("Predicted churn:", "Yes" if prediction == 1 else "No")
print("Predicted churn probability:", round(probability, 4))

# Save waterfall plot for the selected customer
shap.plots.waterfall(
    shap_values[example_idx],
    max_display=12,
    show=False
)
plt.tight_layout()
plt.savefig(
    "reports/shap_individual_customer.png",
    dpi=150,
    bbox_inches="tight"
)
plt.close()

# Save individual customer SHAP values
individual = pd.DataFrame({
    "Feature": feature_names,
    "SHAPValue": shap_values.values[example_idx]
})
individual["AbsoluteSHAP"] = individual["SHAPValue"].abs()
individual = individual.sort_values(
    "AbsoluteSHAP", ascending=False
)

individual.to_csv(
    "reports/shap_individual_customer.csv", index=False
)

print("\nSaved explainability outputs:")
print("- reports/shap_feature_importance.csv")
print("- reports/shap_summary.png")
print("- reports/shap_importance.png")
print("- reports/shap_individual_customer.png")
print("- reports/shap_individual_customer.csv")
print("\nSHAP analysis completed successfully.")
