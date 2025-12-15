# scripts/split_dataset.py
import pandas as pd
import os
from datetime import datetime, timedelta

# Load the full dataset
df = pd.read_csv(r"C:\Users\phiri\Documents\Projects_Mumu\Credit_Risk_Pipeline\data\credit_risk_dataset.csv")

# Simulate splitting into 10 daily chunks
num_days = 10
rows_per_day = len(df) // num_days
start_date = datetime(2025, 5, 13)

# Create incoming folder if it doesn't exist
incoming_dir = r"C:\Users\phiri\Documents\Projects_Mumu\Credit_Risk_Pipeline\data\incoming"
os.makedirs(incoming_dir, exist_ok=True)

# Generate daily files
for i in range(num_days):
    start = i * rows_per_day
    end = (i + 1) * rows_per_day if i < num_days - 1 else len(df)
    chunk = df.iloc[start:end]

    date_str = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
    filename = f"{incoming_dir}/credit_data_{date_str}.csv"
    chunk.to_csv(filename, index=False)

print("Dataset Split")
