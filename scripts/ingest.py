import os
import pandas as pd
from datetime import datetime

INCOMING_DIR = r"C:\Users\phiri\Documents\Projects_Mumu\Credit_Risk_Pipeline\data\incoming"

def get_latest_file(folder_path):
    """Return the path of the latest CSV file based on date in filename."""
    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    if not files:
        return None
    
    # Extract dates and sort
    dated_files = []
    for f in files:
        try:
            date_str = f.replace("credit_data_", "").replace(".csv", "")
            file_date = datetime.strptime(date_str, "%Y-%m-%d")
            dated_files.append((file_date, f))
        except ValueError:
            continue  # skip malformed filenames

    if not dated_files:
        return None

    latest_file = sorted(dated_files)[-1][1]
    return os.path.join(folder_path, latest_file)

def load_latest_data():
    file_path = get_latest_file(INCOMING_DIR)
    if file_path:
        print(f"Loading data from: {file_path}")
        df = pd.read_csv(file_path)
        print(f"Loaded {len(df)} records.")
        return df
    else:
        print("No CSV files found in the incoming folder.")
        return None

if __name__ == "__main__":
    load_latest_data()
