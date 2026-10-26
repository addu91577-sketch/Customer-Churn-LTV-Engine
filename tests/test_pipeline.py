"""
Customer Churn & LTV Engine - Automated Verification & Test Suite
Ensures dataset integrity, model artifact availability, inference correctness,
Power BI data enrichment consistency, LTV regression, and FastAPI endpoints.
"""

import os
import joblib
import numpy as np
import pandas as pd
import pytest
from starlette.testclient import TestClient

from src.api.main import app


def test_raw_dataset_integrity():
    raw_path = 'data/WA_Fn-UseC_-Telco-Customer-Churn.csv'
    assert os.path.exists(raw_path), f"Missing raw dataset at {raw_path}"
    df = pd.read_csv(raw_path)
    assert df.shape == (7043, 21), f"Expected (7043, 21), got {df.shape}"
    assert 'customerID' in df.columns
    assert 'Churn' in df.columns


def test_cleaned_dataset_integrity():
    clean_path = 'data/telco_customer_churn_clean.csv'
    assert os.path.exists(clean_path), f"Missing cleaned dataset at {clean_path}"
    df = pd.read_csv(clean_path)
    assert df.shape == (7043, 21), f"Expected (7043, 21), got {df.shape}"
    assert df['TotalCharges'].isnull().sum() == 0, "Cleaned TotalCharges has nulls"
    assert pd.api.types.is_numeric_dtype(df['TotalCharges']), "TotalCharges is not numeric"
    assert df['customerID'].duplicated().sum() == 0, "Duplicate customer IDs found"


def test_model_artifacts_and_inference():
    required_artifacts = [
        'models/logistic_regression_model.joblib',
        'models/random_forest_model.joblib',
        'models/xgboost_model.joblib',
        'models/scaler.joblib',
        'models/feature_names.joblib',
    ]
    for art in required_artifacts:
        assert os.path.exists(art), f"Missing artifact: {art}"

    # Load artifacts
    xgb = joblib.load('models/xgboost_model.joblib')
    scaler = joblib.load('models/scaler.joblib')
    feature_names = joblib.load('models/feature_names.joblib')

    assert len(feature_names) > 0, "Feature names list is empty"

    # Dummy test sample matching feature dimension
    sample = np.zeros((1, len(feature_names)))
    prob = xgb.predict_proba(sample)[0, 1]
    assert 0.0 <= prob <= 1.0, f"XGBoost probability out of range: {prob}"


def test_ltv_regression_artifacts():
    ltv_model_path = 'models/ltv_regressor_model.joblib'
    ltv_feat_path = 'models/ltv_feature_names.joblib'
    assert os.path.exists(ltv_model_path), "Missing LTV regression model"
    assert os.path.exists(ltv_feat_path), "Missing LTV feature names"

    ltv_model = joblib.load(ltv_model_path)
    ltv_features = joblib.load(ltv_feat_path)
    assert len(ltv_features) > 0

    dummy_sample = np.zeros((1, len(ltv_features)))
    pred_ltv = ltv_model.predict(dummy_sample)[0]
    assert isinstance(pred_ltv, (float, np.floating))


def test_powerbi_enriched_dataset():
    pbi_path = 'data/telco_churn_powerbi_dataset.csv'
    assert os.path.exists(pbi_path), f"Missing Power BI dataset at {pbi_path}"
    df = pd.read_csv(pbi_path)
    assert len(df) == 7043, f"Expected 7043 rows, got {len(df)}"

    required_cols = [
        'Churn_Probability', 'Predicted_Churn', 'Risk_Tier',
        'Tenure_Cohort', 'Customer_LTV', 'Annual_Revenue_At_Risk',
        'Recommended_Retention_Action'
    ]
    for col in required_cols:
        assert col in df.columns, f"Missing required Power BI column: {col}"

    assert df['Churn_Probability'].between(0.0, 1.0).all(), "Churn probability out of range [0, 1]"
    assert set(df['Risk_Tier'].unique()).issubset({'Low Risk', 'Medium Risk', 'High Risk'})
    assert (df['Customer_LTV'] >= 0).all(), "Negative customer LTV found"


def test_visual_and_report_artifacts():
    visuals = [
        'visuals/churn_distribution.png',
        'visuals/churn_by_contract.png',
        'visuals/tenure_churn_distribution.png',
        'visuals/monthly_charges_by_churn.png',
        'visuals/churn_by_internet.png',
        'visuals/model_comparison_metrics.png',
        'visuals/roc_curves_comparison.png',
        'visuals/confusion_matrices.png',
        'visuals/shap_summary_plot.png',
        'visuals/shap_feature_importance.png',
        'visuals/powerbi_dashboard_page1_executive.png',
        'visuals/powerbi_dashboard_page2_diagnostics.png',
        'visuals/powerbi_dashboard_page3_ltv_engine.png',
    ]
    for v in visuals:
        assert os.path.exists(v), f"Missing visual asset: {v}"

    reports = [
        'notebooks/reports/business_insights.md',
        'notebooks/reports/excel_data_exploration.md',
        'notebooks/reports/model_evaluation_report.md',
        'notebooks/reports/ltv_regression_report.md',
    ]
    for r in reports:
        assert os.path.exists(r), f"Missing report: {r}"


def test_sql_and_docker_files_exist():
    required_files = [
        'sql/01_create_database.sql',
        'sql/02_create_table.sql',
        'sql/03_basic_analysis.sql',
        'sql/04_churn_and_ltv_views.sql',
        'Dockerfile',
        'docker-compose.yml',
        'metabase/metabase_setup_guide.md',
    ]
    for f in required_files:
        assert os.path.exists(f), f"Missing required project file: {f}"


def test_fastapi_endpoints():
    client = TestClient(app)

    # 1. Root
    resp = client.get("/")
    assert resp.status_code == 200
    assert "version" in resp.json()

    # 2. Health
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"

    # 3. Model Info
    resp = client.get("/model/info")
    assert resp.status_code == 200
    assert "classification_engine" in resp.json()

    # 4. Single-customer prediction
    sample_payload = {
        "customerID": "TEST-999",
        "gender": "Female",
        "SeniorCitizen": 0,
        "Partner": "No",
        "Dependents": "No",
        "tenure": 3,
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "Fiber optic",
        "OnlineSecurity": "No",
        "OnlineBackup": "No",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "Yes",
        "StreamingMovies": "Yes",
        "Contract": "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": 92.40,
        "TotalCharges": 277.20
    }
    resp = client.post("/predict/single", json=sample_payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["customerID"] == "TEST-999"
    assert 0.0 <= data["churn_probability"] <= 1.0
    assert data["risk_tier"] in ["High Risk", "Medium Risk", "Low Risk"]
    assert data["predicted_ltv"] > 0
    assert len(data["recommended_retention_action"]) > 0
