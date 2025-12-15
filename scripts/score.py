import pandas as pd
import joblib
from ingest import load_latest_data

def score_data(df):
    model = joblib.load(r"C:\Users\phiri\Documents\Projects_Mumu\Credit_Risk_Pipeline\models\credit_model.pkl")

    # Create a copy to use for prediction
    X = df.copy()

    # Drop target column only from model input
    if 'loan_status' in X.columns:
        X = X.drop(columns=['loan_status'])

    # Predict
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)[:, 1]

    # Add predictions back to original df (with loan_status still there)
    df['predicted_default'] = predictions
    df['default_probability'] = probabilities

    return df

# Optional test block
if __name__ == "__main__":
    from transform import clean_data
    df = load_latest_data()
    if df is not None:
        df_clean = clean_data(df)
        df_scored = score_data(df_clean)
        print(df_scored[['loan_status', 'predicted_default', 'default_probability']].head())
