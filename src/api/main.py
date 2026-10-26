"""
Customer Churn & LTV Engine - Production REST API
Built with FastAPI to serve real-time single-customer inference,
batch prediction processing, and model performance metadata.
Author: Adarsh Kumar Pandey
"""

import os
import io
import joblib
import numpy as np
import pandas as pd
from typing import List, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel, Field

# Initialize FastAPI App
app = FastAPI(
    title="Customer Churn & Lifetime Value (LTV) Engine API",
    description="Enterprise predictive API for customer attrition risk scoring, LTV forecasting, and retention action prescriptions.",
    version="1.0.0"
)

# Global variables for cached model artifacts
CLASSIFIER = None
LTV_REGRESSOR = None
FEATURE_NAMES = None
LTV_FEATURE_NAMES = None


def load_artifacts():
    global CLASSIFIER, LTV_REGRESSOR, FEATURE_NAMES, LTV_FEATURE_NAMES
    # Root directory is two levels above src/api
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    models_dir = os.path.join(base_dir, 'models')

    clf_path = os.path.join(models_dir, 'xgboost_model.joblib')
    feat_path = os.path.join(models_dir, 'feature_names.joblib')
    ltv_path = os.path.join(models_dir, 'ltv_regressor_model.joblib')
    ltv_feat_path = os.path.join(models_dir, 'ltv_feature_names.joblib')

    if os.path.exists(clf_path) and os.path.exists(feat_path):
        CLASSIFIER = joblib.load(clf_path)
        FEATURE_NAMES = joblib.load(feat_path)

    if os.path.exists(ltv_path) and os.path.exists(ltv_feat_path):
        LTV_REGRESSOR = joblib.load(ltv_path)
        LTV_FEATURE_NAMES = joblib.load(ltv_feat_path)


# Load artifacts upon startup
load_artifacts()


class CustomerInput(BaseModel):
    customerID: Optional[str] = "CUST-001"
    gender: str = Field(default="Male", description="Male or Female")
    SeniorCitizen: int = Field(default=0, ge=0, le=1)
    Partner: str = Field(default="No", description="Yes or No")
    Dependents: str = Field(default="No", description="Yes or No")
    tenure: int = Field(default=6, ge=0, le=100)
    PhoneService: str = Field(default="Yes", description="Yes or No")
    MultipleLines: str = Field(default="No", description="Yes, No, or No phone service")
    InternetService: str = Field(default="Fiber optic", description="DSL, Fiber optic, or No")
    OnlineSecurity: str = Field(default="No", description="Yes, No, or No internet service")
    OnlineBackup: str = Field(default="No", description="Yes, No, or No internet service")
    DeviceProtection: str = Field(default="No", description="Yes, No, or No internet service")
    TechSupport: str = Field(default="No", description="Yes, No, or No internet service")
    StreamingTV: str = Field(default="Yes", description="Yes, No, or No internet service")
    StreamingMovies: str = Field(default="Yes", description="Yes, No, or No internet service")
    Contract: str = Field(default="Month-to-month", description="Month-to-month, One year, or Two year")
    PaperlessBilling: str = Field(default="Yes", description="Yes or No")
    PaymentMethod: str = Field(default="Electronic check", description="Electronic check, Mailed check, Bank transfer (automatic), Credit card (automatic)")
    MonthlyCharges: float = Field(default=85.50, ge=0.0)
    TotalCharges: float = Field(default=513.00, ge=0.0)


class PredictionResponse(BaseModel):
    customerID: str
    churn_probability: float
    churn_prediction: str
    risk_tier: str
    predicted_ltv: float
    annual_revenue_at_risk: float
    recommended_retention_action: str


def engineer_features_single(cust_dict: dict) -> pd.DataFrame:
    df = pd.DataFrame([cust_dict])

    # 1. Tenure Cohorts
    bins = [-1, 12, 24, 36, 48, 60, 72]
    labels = ['0-12m', '13-24m', '25-36m', '37-48m', '49-60m', '61-72m']
    df['tenure_cohort'] = pd.cut(df['tenure'], bins=bins, labels=labels)

    # 2. Add-on services
    service_cols = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
    for col in service_cols:
        df[f'{col}_flag'] = (df[col] == 'Yes').astype(int)

    df['total_addon_services'] = df[[f'{col}_flag' for col in service_cols]].sum(axis=1)
    df['security_bundle'] = ((df['OnlineSecurity'] == 'Yes') & (df['TechSupport'] == 'Yes')).astype(int)
    df['streaming_bundle'] = ((df['StreamingTV'] == 'Yes') & (df['StreamingMovies'] == 'Yes')).astype(int)

    # 3. Financial ratios
    df['charge_ratio'] = df['TotalCharges'] / (df['tenure'] + 1.0)
    df['monthly_to_total_ratio'] = df['MonthlyCharges'] / (df['TotalCharges'] + 1.0)
    df['has_family'] = ((df['Partner'] == 'Yes') | (df['Dependents'] == 'Yes')).astype(int)

    # 4. Risk indicators
    df['is_month_to_month'] = (df['Contract'] == 'Month-to-month').astype(int)
    df['is_fiber_optic'] = (df['InternetService'] == 'Fiber optic').astype(int)
    df['is_electronic_check'] = (df['PaymentMethod'] == 'Electronic check').astype(int)
    df['high_monthly_charges'] = (df['MonthlyCharges'] >= 70.0).astype(int)

    # Drop unneeded intermediate columns
    drop_cols = ['customerID'] + [f'{col}_flag' for col in service_cols]
    if 'Churn' in df.columns:
        drop_cols.append('Churn')
    df_ml = df.drop(columns=[c for c in drop_cols if c in df.columns])

    cat_cols = df_ml.select_dtypes(include=['object', 'category', 'string']).columns.tolist()
    df_encoded = pd.get_dummies(df_ml, columns=cat_cols, drop_first=True)

    # Align with trained model features
    for col in FEATURE_NAMES:
        if col not in df_encoded.columns:
            df_encoded[col] = 0

    return df_encoded[FEATURE_NAMES]


def prescribe_action(risk_tier: str, contract: str, monthly_charges: float,
                     internet_service: str, tech_support: str, payment_method: str) -> str:
    if risk_tier == 'High Risk':
        if contract == 'Month-to-month' and monthly_charges >= 70:
            return 'Offer 1-Year Contract with 15% Discount Bundle'
        elif internet_service == 'Fiber optic' and tech_support == 'No':
            return 'Free Premium Tech Support & Speed Optimization Onboarding'
        elif payment_method == 'Electronic check':
            return 'Auto-Pay Enrollment with $10 Billing Credit'
        else:
            return 'Dedicated Retention Call & Plan Re-evaluation'
    elif risk_tier == 'Medium Risk':
        return 'Quarterly Customer Satisfaction Check-in & Speed Audit'
    else:
        return 'Upsell Premium Streaming & Loyalty Rewards'


@app.get("/")
def root():
    return {
        "engine": "Customer Churn Prediction & Lifetime Value (LTV) Engine API",
        "version": "1.0.0",
        "author": "Adarsh Kumar Pandey",
        "status": "online",
        "docs_url": "/docs"
    }


@app.get("/health")
def health_check():
    if CLASSIFIER is None or FEATURE_NAMES is None:
        raise HTTPException(status_code=503, detail="Model artifacts not initialized")
    return {
        "status": "healthy",
        "classifier_loaded": True,
        "ltv_regressor_loaded": LTV_REGRESSOR is not None
    }


@app.get("/model/info")
def model_info():
    return {
        "classification_engine": "XGBoost Classifier",
        "classification_metrics": {
            "test_roc_auc": 0.8458,
            "cv_5fold_roc_auc": "0.8466 (+/- 0.0112)",
            "test_recall": "78.61%",
            "test_accuracy": "75.16%"
        },
        "ltv_regression_engine": "XGBoost Regressor",
        "ltv_metrics": {
            "test_r2": 0.9983,
            "test_mae": "$87.06"
        },
        "total_features": len(FEATURE_NAMES) if FEATURE_NAMES else 0
    }


@app.post("/predict/single", response_model=PredictionResponse)
def predict_single(customer: CustomerInput):
    if CLASSIFIER is None:
        raise HTTPException(status_code=503, detail="Models not loaded")

    cust_dict = customer.model_dump() if hasattr(customer, "model_dump") else customer.dict()
    X_enc = engineer_features_single(cust_dict)

    # 1. Churn Prediction
    prob = float(CLASSIFIER.predict_proba(X_enc.values)[0, 1])
    pred = "Yes" if prob >= 0.50 else "No"

    # 2. Risk Tier
    if prob >= 0.60:
        risk_tier = "High Risk"
    elif prob >= 0.30:
        risk_tier = "Medium Risk"
    else:
        risk_tier = "Low Risk"

    # 3. Customer LTV Estimation
    expected_future_months = max(1.0, round((1.0 - prob) * 36, 1))
    projected_future_rev = round(customer.MonthlyCharges * expected_future_months, 2)
    predicted_ltv = round(customer.TotalCharges + (projected_future_rev * 0.80), 2)

    # 4. Annual Revenue at Risk
    annual_at_risk = round(customer.MonthlyCharges * 12.0 * prob, 2)

    # 5. Retention Prescription
    action = prescribe_action(
        risk_tier, customer.Contract, customer.MonthlyCharges,
        customer.InternetService, customer.TechSupport, customer.PaymentMethod
    )

    return PredictionResponse(
        customerID=customer.customerID or "N/A",
        churn_probability=round(prob, 4),
        churn_prediction=pred,
        risk_tier=risk_tier,
        predicted_ltv=predicted_ltv,
        annual_revenue_at_risk=annual_at_risk,
        recommended_retention_action=action
    )


@app.post("/predict/batch")
async def predict_batch(file: UploadFile = File(...)):
    if CLASSIFIER is None:
        raise HTTPException(status_code=503, detail="Models not loaded")

    contents = await file.read()
    try:
        batch_df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV file: {str(e)}")

    results = []
    high_risk_count = 0
    total_revenue_at_risk = 0.0

    for _, row in batch_df.iterrows():
        row_dict = row.to_dict()
        cust_id = str(row_dict.get('customerID', 'UNKNOWN'))
        X_enc = engineer_features_single(row_dict)

        prob = float(CLASSIFIER.predict_proba(X_enc.values)[0, 1])
        pred = "Yes" if prob >= 0.50 else "No"
        risk_tier = "High Risk" if prob >= 0.60 else ("Medium Risk" if prob >= 0.30 else "Low Risk")

        m_charges = float(row_dict.get('MonthlyCharges', 0.0))
        t_charges = float(row_dict.get('TotalCharges', 0.0))

        expected_future_months = max(1.0, round((1.0 - prob) * 36, 1))
        predicted_ltv = round(t_charges + (m_charges * expected_future_months * 0.80), 2)
        annual_at_risk = round(m_charges * 12.0 * prob, 2)

        if risk_tier == 'High Risk':
            high_risk_count += 1
        total_revenue_at_risk += annual_at_risk

        action = prescribe_action(
            risk_tier, str(row_dict.get('Contract', '')), m_charges,
            str(row_dict.get('InternetService', '')), str(row_dict.get('TechSupport', '')),
            str(row_dict.get('PaymentMethod', ''))
        )

        results.append({
            "customerID": cust_id,
            "churn_probability": round(prob, 4),
            "churn_prediction": pred,
            "risk_tier": risk_tier,
            "predicted_ltv": predicted_ltv,
            "annual_revenue_at_risk": annual_at_risk,
            "recommended_retention_action": action
        })

    return {
        "total_records_processed": len(results),
        "high_risk_subscribers": high_risk_count,
        "total_annual_revenue_at_risk": round(total_revenue_at_risk, 2),
        "predictions": results[:50]  # Return first 50 records in preview
    }
