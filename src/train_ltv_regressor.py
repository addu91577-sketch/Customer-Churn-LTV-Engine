"""
Customer Churn & LTV Engine - LTV Regression Modeling (Week 3: Days 1–3)
Develops regression models (Ridge, Random Forest Regressor, XGBoost Regressor)
to forecast the expected lifetime revenue / Customer Lifetime Value (LTV) of subscribers.
Author: Adarsh Kumar Pandey
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def train_ltv_regression():
    print("Loading enriched dataset for LTV regression modeling...")
    data_path = 'data/telco_churn_powerbi_dataset.csv'
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Missing enriched dataset at {data_path}")

    df = pd.read_csv(data_path)

    # Features for LTV regression
    # Drop identifiers, raw leakages, and target
    feature_cols = [
        'tenure', 'MonthlyCharges', 'SeniorCitizen',
        'gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
        'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
        'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract',
        'PaperlessBilling', 'PaymentMethod', 'Churn_Probability'
    ]

    X_raw = df[feature_cols].copy()
    y = df['Customer_LTV'].values

    # Encode categorical features
    cat_cols = X_raw.select_dtypes(include=['object', 'category', 'string']).columns.tolist()
    X = pd.get_dummies(X_raw, columns=cat_cols, drop_first=True)
    ltv_feature_names = X.columns.tolist()

    # Train/Test Split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    print(f"Train samples: {X_train.shape[0]} | Test samples: {X_test.shape[0]}")

    models = {
        'Ridge Regression': Ridge(alpha=10.0),
        'Random Forest Regressor': RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42, n_jobs=-1),
        'XGBoost Regressor': XGBRegressor(n_estimators=250, max_depth=4, learning_rate=0.04, subsample=0.8, random_state=42, n_jobs=-1)
    }

    results = {}
    fitted_models = {}

    print("\nEvaluating LTV Regression Models...")
    for name, reg in models.items():
        reg.fit(X_train, y_train)
        y_pred = reg.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)

        results[name] = {'MAE': mae, 'RMSE': rmse, 'R2': r2}
        fitted_models[name] = reg
        print(f"[{name}] MAE: ${mae:,.2f} | RMSE: ${rmse:,.2f} | R²: {r2:.4f}")

    # Best model selection by R²
    best_name = max(results, key=lambda k: results[k]['R2'])
    best_model = fitted_models[best_name]
    print(f"\n[BEST MODEL] {best_name} (R² = {results[best_name]['R2']:.4f})")

    # Serialize artifacts
    os.makedirs('models', exist_ok=True)
    joblib.dump(best_model, 'models/ltv_regressor_model.joblib')
    joblib.dump(ltv_feature_names, 'models/ltv_feature_names.joblib')
    print("Saved models/ltv_regressor_model.joblib and models/ltv_feature_names.joblib")

    # Generate Markdown Report
    os.makedirs('notebooks/reports', exist_ok=True)
    report_path = 'notebooks/reports/ltv_regression_report.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# 💰 Customer Lifetime Value (LTV) Regression Modeling Report\n\n")
        f.write("**Project:** Customer Churn & Lifetime Value (LTV) Engine  \n")
        f.write("**Author:** Adarsh Kumar Pandey  \n")
        f.write("**Week 3: Days 1–3 Deliverable**  \n\n")
        f.write("---\n\n")
        f.write("## 1. Regression Model Benchmark\n\n")
        f.write("| Model Architecture | Mean Absolute Error (MAE) | Root Mean Squared Error (RMSE) | R² Score |\n")
        f.write("| :--- | :---: | :---: | :---: |\n")
        for m_name, m_metrics in results.items():
            f.write(f"| **{m_name}** | ${m_metrics['MAE']:,.2f} | ${m_metrics['RMSE']:,.2f} | {m_metrics['R2']:.4f} |\n")
        f.write(f"\n**Production Model Selected:** `{best_name}` with **R² = {results[best_name]['R2']:.4f}** and **MAE = ${results[best_name]['MAE']:,.2f}**.\n\n")
        f.write("---\n\n")
        f.write("## 2. Business Value\n")
        f.write("- Enables dynamic forecasting of expected customer gross contribution over the lifetime.\n")
        f.write("- Feeds directly into retention budget allocation, ensuring spend does not exceed expected remaining customer lifetime value.\n")

    print(f"Report successfully saved to {report_path}")
    return results


if __name__ == '__main__':
    train_ltv_regression()
