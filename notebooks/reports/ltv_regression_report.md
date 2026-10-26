# 💰 Customer Lifetime Value (LTV) Regression Modeling Report

**Project:** Customer Churn & Lifetime Value (LTV) Engine  
**Author:** Adarsh Kumar Pandey  
**Week 3: Days 1–3 Deliverable**  

---

## 1. Regression Model Benchmark

| Model Architecture | Mean Absolute Error (MAE) | Root Mean Squared Error (RMSE) | R² Score |
| :--- | :---: | :---: | :---: |
| **Ridge Regression** | $678.92 | $848.71 | 0.9160 |
| **Random Forest Regressor** | $90.99 | $131.53 | 0.9980 |
| **XGBoost Regressor** | $87.06 | $121.15 | 0.9983 |

**Production Model Selected:** `XGBoost Regressor` with **R² = 0.9983** and **MAE = $87.06**.

---

## 2. Business Value
- Enables dynamic forecasting of expected customer gross contribution over the lifetime.
- Feeds directly into retention budget allocation, ensuring spend does not exceed expected remaining customer lifetime value.
