import pandas as pd
import hashlib
import os

DATA_DIR = "SINIOR_MARKET_SAMPLE_v1"

try:
    csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
    if not csv_files:
        raise FileNotFoundError("No CSV files found in the dataset folder!")
    
    TARGET_FILE = os.path.join(DATA_DIR, csv_files[0])
    print(f"Found data file: {TARGET_FILE}")
except Exception as e:
    print(f"ERROR: {e}")
    exit()

print("Loading raw data into Pandas DataFrame...")
df = pd.read_csv(TARGET_FILE)
print(f"Dataset loaded successfully! Shape: {df.shape[0]} rows, {df.shape[1]} columns")

# Cybersecurity Algorithm (SHA-256)
def mask_sensitive_data(text):
    """Converts sensitive string data into an irreversible SHA-256 hash."""
    if pd.isna(text):
        return text
    encoded_text = str(text).encode('utf-8')
    return hashlib.sha256(encoded_text).hexdigest()

# Data Masking
print("Scanning for sensitive columns (GDPR/KVKK Compliance)...")

sensitive_keywords = ['id', 'card', 'account', 'ssn', 'record', 'phone', 'email']

masked_count = 0
for col in df.columns:
    if any(keyword in col.lower() for keyword in sensitive_keywords):
        print(f"Masking detected sensitive column: {col}...")
        df[col] = df[col].apply(mask_sensitive_data)
        masked_count += 1

if masked_count == 0:
    print("No highly sensitive columns detected based on keywords.")

#Praquet Export
output_filename = f"secured_{csv_files[0].replace('.csv', '.parquet')}"
print(f"Compressing and exporting to Big Data format...")

df.to_parquet(output_filename, engine='pyarrow', index=False)
print(f"Pipeline Complete! Secured file saved as: {output_filename}")
