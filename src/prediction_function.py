import pandas as pd


def predict_churn(model, customer_data):
   
    customer_df = pd.DataFrame([customer_data])

    prediction = model.predict(customer_df)[0]

    probability = model.predict_proba(customer_df)[0][1]

    if prediction == 1:
        result = "Yes"
    else:
        result = "No"

    return {
        "Churn Prediction": result,
        "Churn Probability": round(float(probability), 4)
    }