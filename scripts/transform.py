import pandas as pd

def clean_data(df):
    # Standardise column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Convert numeric fields
    df['person_income'] = pd.to_numeric(df['person_income'], errors='coerce')
    df['person_emp_length'] = pd.to_numeric(df['person_emp_length'], errors='coerce')
    df['loan_amnt'] = pd.to_numeric(df['loan_amnt'], errors='coerce')
    df['loan_int_rate'] = pd.to_numeric(df['loan_int_rate'], errors='coerce')
    df['loan_percent_income'] = pd.to_numeric(df['loan_percent_income'], errors='coerce')
    df['cb_person_cred_hist_length'] = pd.to_numeric(df['cb_person_cred_hist_length'], errors='coerce')

    # Fill missing employment length with median
    df['person_emp_length'] = df['person_emp_length'].fillna(df['person_emp_length'].median())

    # Encode categorical fields with safe mapping
    df['person_home_ownership'] = df['person_home_ownership'].map({
        'RENT': 0, 'OWN': 1, 'MORTGAGE': 2, 'OTHER': 3
    }).fillna(-1)

    df['loan_intent'] = df['loan_intent'].astype('category').cat.codes
    df['loan_grade'] = df['loan_grade'].astype('category').cat.codes
    df['cb_person_default_on_file'] = df['cb_person_default_on_file'].map({'Y': 1, 'N': 0}).fillna(0)

    # Fill remaining missing values with 0
    df = df.fillna(0)

    return df

# Optional test run
if __name__ == "__main__":
    from ingest import load_latest_data
    df = load_latest_data()
    if df is not None:
        df_clean = clean_data(df)
        print(df_clean.head())


#df.to_csv(r"C:\Users\phiri\Documents\Projects_Mumu\Credit_Risk_Pipeline\savedtest_data.csv", index = False, sep = ",", decimal = ".")