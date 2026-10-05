# Customer-Churn-LTV-Engine
A predictive analytics system using telco data to predict customer churn and lifetime value (LTV)
A machine learning project for analyzing customer churn and building predictive models using the Telco Customer Churn dataset.

The project covers data preprocessing, churn analysis, machine learning model development, evaluation, model comparison, cross-validation, hyperparameter tuning, feature importance, churn prediction, and model saving.

---

# Project Overview

Customer churn refers to customers discontinuing a service.

This project uses customer demographic, service, contract, and billing information to analyze customer churn and develop machine learning models to predict whether a customer is likely to churn.

The project uses the Telco Customer Churn dataset containing:

- 7,043 customer records
- 21 original attributes
- Customer demographic information
- Service information
- Contract information
- Payment information
- Monthly and total charges
- Churn status

The `customerID` column is removed before machine learning because it is an identifier and is not used as a predictive feature.

---

# Objectives

- Clean and preprocess customer data
- Analyze customer churn patterns
- Analyze numerical and categorical features
- Create a reusable preprocessing pipeline
- Build multiple machine learning models
- Handle class imbalance
- Generate churn predictions
- Evaluate model performance
- Compare machine learning models
- Perform cross-validation
- Tune Random Forest and XGBoost models
- Select a final model
- Analyze feature importance
- Create a reusable churn prediction function
- Save the trained model

---

# Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- Matplotlib
- Seaborn
- Joblib
- Git
- GitHub
- VS Code

---

# Dataset

## Telco Customer Churn Dataset

The dataset contains customer information related to:

### Customer Information

- Gender
- Senior Citizen
- Partner
- Dependents
- Tenure

### Service Information

- Phone Service
- Multiple Lines
- Internet Service
- Online Security
- Online Backup
- Device Protection
- Tech Support
- Streaming TV
- Streaming Movies

### Account Information

- Contract
- Paperless Billing
- Payment Method
- Monthly Charges
- Total Charges

### Target Variable

- Churn

### Dataset Statistics

- Total Customers: 7,043
- Churned Customers: 1,869
- Retained Customers: 5,174
- Churn Rate: 26.54%
- Retention Rate: 73.46%

---

# Project Architecture

```text
                    ┌─────────────────────────────┐
                    │       Telco Dataset        │
                    │     7,043 Customers        │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │     Data Preprocessing      │
                    │                             │
                    │ • Data cleaning             │
                    │ • TotalCharges conversion  │
                    │ • Missing value handling    │
                    │ • Remove customerID         │
                    │ • Feature identification    │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │       Churn Analysis        │
                    │                             │
                    │ • Churn distribution        │
                    │ • Numerical analysis        │
                    │ • Categorical analysis      │
                    │ • Customer profiles         │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │ Preprocessing Pipeline      │
                    │                             │
                    │ Numerical Features:         │
                    │ • Median Imputation         │
                    │ • Standard Scaling          │
                    │                             │
                    │ Categorical Features:       │
                    │ • Most Frequent Imputation │
                    │ • One-Hot Encoding          │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
        ┌────────────────────────────────────────────────────┐
        │              Machine Learning Models                │
        │                                                    │
        │  ┌──────────────────────────────────────────────┐  │
        │  │ Logistic Regression                          │  │
        │  └──────────────────────────────────────────────┘  │
        │                                                    │
        │  ┌──────────────────────────────────────────────┐  │
        │  │ Balanced Logistic Regression                 │  │
        │  └──────────────────────────────────────────────┘  │
        │                                                    │
        │  ┌──────────────────────────────────────────────┐  │
        │  │ Random Forest                                │  │
        │  └──────────────────────────────────────────────┘  │
        │                                                    │
        │  ┌──────────────────────────────────────────────┐  │
        │  │ XGBoost                                      │  │
        │  └──────────────────────────────────────────────┘  │
        └───────────────────────┬────────────────────────────┘
                                │
                                ▼
                    ┌─────────────────────────────┐
                    │     Model Evaluation        │
                    │                             │
                    │ • Accuracy                 │
                    │ • Precision                │
                    │ • Recall                   │
                    │ • F1 Score                 │
                    │ • Confusion Matrix         │
                    │ • Classification Report    │
                    │ • Threshold Analysis       │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │ Model Comparison             │
                    │                             │
                    │ • Model comparison          │
                    │ • 5-Fold Cross Validation   │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │ Hyperparameter Tuning        │
                    │                             │
                    │ • Random Forest             │
                    │ • XGBoost                   │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │    Final Model Selection    │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │       Final Model           │
                    │                             │
                    │ • Feature Importance        │
                    │ • Prediction Function       │
                    │ • Model Saving              │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │     final_model.pkl         │
                    │       Saved Model           │
                    └─────────────────────────────┘
