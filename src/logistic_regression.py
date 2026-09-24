import pandas as pd

from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from preprocessing_pipeline import preprocessor


# Load dataset
df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")


# Convert TotalCharges to numeric
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)


# Separate features and target
X = df.drop(columns=["Churn", "customerID"])
y = df["Churn"].map({"No": 0, "Yes": 1})


# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Day 12: Balanced Logistic Regression

balanced_model = Pipeline([
    ("preprocessor", preprocessor),
    ("model", LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    ))
])

# Train balanced Logistic Regression
balanced_model.fit(X_train, y_train)

print("\nBalanced Logistic Regression training completed successfully.")


# Make predictions
y_pred_balanced = balanced_model.predict(X_test)

print("\nBalanced Logistic Regression predictions completed successfully.")
print("Predicted churn distribution:")
print(pd.Series(y_pred_balanced).value_counts())


# Evaluate balanced model
balanced_accuracy = accuracy_score(y_test, y_pred_balanced)
balanced_precision = precision_score(
    y_test,
    y_pred_balanced,
    zero_division=0
)
balanced_recall = recall_score(
    y_test,
    y_pred_balanced,
    zero_division=0
)
balanced_f1 = f1_score(
    y_test,
    y_pred_balanced,
    zero_division=0
)

print("\nBalanced Logistic Regression Evaluation Metrics:")
print("Accuracy:", round(balanced_accuracy, 4))
print("Precision:", round(balanced_precision, 4))
print("Recall:", round(balanced_recall, 4))
print("F1 Score:", round(balanced_f1, 4))


# Confusion matrix for balanced model
balanced_cm = confusion_matrix(y_test, y_pred_balanced)

print("\nBalanced Logistic Regression Confusion Matrix:")
print(balanced_cm)

tn_b, fp_b, fn_b, tp_b = balanced_cm.ravel()

print("\nBalanced Confusion Matrix Details:")
print("True Negatives:", tn_b)
print("False Positives:", fp_b)
print("False Negatives:", fn_b)
print("True Positives:", tp_b)

# Normal Logistic Regression
logistic_model = Pipeline([
    ("preprocessor", preprocessor),
    ("model", LogisticRegression(max_iter=1000))
])

logistic_model.fit(X_train, y_train)

normal_pred = logistic_model.predict(X_test)

normal_f1 = f1_score(y_test, normal_pred)
balanced_f1 = f1_score(y_test, y_pred_balanced)

print("\nModel Comparison")
print("Normal LR F1:", round(normal_f1, 4))
print("Balanced LR F1:", round(balanced_f1, 4))

print("\nModel Comparison")
print("Normal LR F1:", round(f1_score(y_test, normal_pred), 4))
print("Balanced LR F1:", round(f1_score(y_test, y_pred_balanced), 4))