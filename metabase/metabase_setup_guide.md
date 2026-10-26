# 📊 Metabase / Apache Superset Dashboard Integration Guide (Week 4)

**Project:** Customer Churn & Lifetime Value (LTV) Engine  
**Author:** Adarsh Kumar Pandey  
**Target BI Platforms:** Metabase / Apache Superset  
**Database Backend:** PostgreSQL (`customer_churn_db`)  

---

## 🚀 1. Connecting Metabase to PostgreSQL

When running via Docker Compose (`docker compose up`):
1. Navigate to `http://localhost:3000` in your browser.
2. Complete initial admin setup and choose **Add your data** > **PostgreSQL**.
3. Input connection settings:
   - **Host:** `postgres` (or `localhost` if running Metabase standalone)
   - **Port:** `5432`
   - **Database name:** `customer_churn_db`
   - **Username:** `postgres`
   - **Password:** `postgrespassword`
4. Click **Save** to sync database schema and views.

---

## 📈 2. Core Dashboard Cards & SQL Queries

### Card 1: Executive Churn & Revenue Health (Single Number / KPI)
```sql
SELECT 
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_count,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)::NUMERIC / COUNT(*) * 100, 2) AS churn_rate_pct,
    ROUND(SUM(MonthlyCharges)::NUMERIC, 2) AS total_mrr
FROM customers;
```

### Card 2: Risk Matrix by Contract & Tenure Cohort (Stacked Bar Chart)
```sql
SELECT 
    Contract,
    tenure_cohort,
    customer_count,
    cohort_churn_rate_pct
FROM vw_contract_tenure_risk_matrix
ORDER BY Contract, tenure_cohort;
```

### Card 3: High-Priority Retention Queue (Action Table)
```sql
SELECT 
    customerID,
    Contract,
    tenure,
    MonthlyCharges,
    annual_revenue,
    retention_action
FROM vw_high_risk_retention_queue
LIMIT 50;
```

### Card 4: Service Adoption Friction Matrix (Heatmap / Bar)
```sql
SELECT 
    InternetService,
    OnlineSecurity,
    TechSupport,
    total_subscribers,
    churn_rate_pct
FROM vw_service_adoption_vs_churn;
```

### Card 5: Segment Customer Lifetime Value (LTV) Distribution
```sql
SELECT 
    Contract,
    PaymentMethod,
    customer_count,
    avg_historical_charges,
    projected_ltv,
    total_segment_ltv
FROM vw_customer_ltv_aggregations;
```

---

## 🔄 3. Connecting to the FastAPI Prediction Endpoint

To score incoming or prospective customer leads directly from internal workflows:
- **API URL:** `http://localhost:8000/predict/single`
- **Method:** `POST`
- **Headers:** `Content-Type: application/json`
- **Payload:**
```json
{
  "customerID": "DEMO-101",
  "gender": "Female",
  "SeniorCitizen": 0,
  "Partner": "No",
  "Dependents": "No",
  "tenure": 4,
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
  "MonthlyCharges": 89.90,
  "TotalCharges": 359.60
}
```
- **Response:**
```json
{
  "customerID": "DEMO-101",
  "churn_probability": 0.8124,
  "churn_prediction": "Yes",
  "risk_tier": "High Risk",
  "predicted_ltv": 847.45,
  "annual_revenue_at_risk": 876.42,
  "recommended_retention_action": "Offer 1-Year Contract with 15% Discount Bundle"
}
```
