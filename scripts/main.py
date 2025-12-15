# main.py

import os
import pandas as pd
import hashlib
import shutil
from datetime import datetime

from ingest import load_latest_data
from transform import clean_data
from score import score_data

# Paths
BASE_DIR = r"C:\Users\phiri\Documents\Projects_Mumu\Credit_Risk_Pipeline"
INCOMING_DIR = os.path.join(BASE_DIR, "data", "incoming")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
LATEST_PATH = os.path.join(BASE_DIR, "saved_data.csv")
HISTORY_PATH = os.path.join(BASE_DIR, "scored_history.csv")
HASH_LOG = os.path.join(BASE_DIR, "data", "hash_registry.txt")

# Ensure processed folder and hash registry exist
os.makedirs(PROCESSED_DIR, exist_ok=True)
if not os.path.exists(HASH_LOG):
    open(HASH_LOG, "w").close()


def compute_file_hash(file_path):
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def is_duplicate(file_path, hash_log_path=HASH_LOG):
    file_hash = compute_file_hash(file_path)
    with open(hash_log_path, "r") as f:
        if file_hash in f.read():
            return True
    return False


def log_file_hash(file_path, hash_log_path=HASH_LOG):
    file_hash = compute_file_hash(file_path)
    with open(hash_log_path, "a") as f:
        f.write(file_hash + "\n")


# Get list of new, unprocessed files
incoming_files = sorted(
    [f for f in os.listdir(INCOMING_DIR) if f.endswith(".csv")]
)

# Process only the first new file
for filename in incoming_files:
    full_path = os.path.join(INCOMING_DIR, filename)

    if is_duplicate(full_path):
        print(f"Skipping already processed file: {filename}")
        continue

    # Load and process this file
    df = pd.read_csv(full_path)
    if df.empty:
        print(f"File is empty: {filename}")
        continue

    print(f"New file detected: {filename} — processing...")

    # Clean and score
    df_clean = clean_data(df)
    df_scored = score_data(df_clean)
    df_scored['upload_date'] = datetime.today().strftime('%Y/%m/%d')

    # Save latest
    df_scored.to_csv(LATEST_PATH, index=False, sep=",", decimal=".")
    print(f"Saved latest scored data to: {LATEST_PATH}")

    # Append to history
    if os.path.exists(HISTORY_PATH):
        existing = pd.read_csv(HISTORY_PATH)
        combined = pd.concat([existing, df_scored], ignore_index=True)
        combined.to_csv(HISTORY_PATH, index=False, sep=",", decimal=".")
        print(f"Appended new data to: {HISTORY_PATH}")
    else:
        df_scored.to_csv(HISTORY_PATH, index=False, sep=",", decimal=".")
        print(f"Created history file: {HISTORY_PATH}")

    # Move the processed file to archive
    processed_path = os.path.join(PROCESSED_DIR, filename)
    shutil.move(full_path, processed_path)
    print(f"Moved file to: {processed_path}")

    # Log the file hash
    log_file_hash(processed_path)
    break  # Only process one file at a time

else:
    print(" No new data files to process.")
