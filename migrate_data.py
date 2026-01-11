import pandas as pd
import toml
from supabase import create_client
import os

def migrate_csv_to_supabase():
    print("Starting migration...")
    
    # 1. Load Secrets
    try:
        if not os.path.exists(".streamlit/secrets.toml"):
            print("Secrets file not found.")
            return
        
        secrets = toml.load(".streamlit/secrets.toml")
        url = secrets["supabase"]["url"]
        key = secrets["supabase"]["key"]
        print("Secrets loaded.")
    except Exception as e:
        print(f"Error loading secrets: {e}")
        return

    # 2. Initialize Supabase
    try:
        supabase = create_client(url, key)
        print("Supabase client initialized.")
    except Exception as e:
        print(f"Error initializing Supabase: {e}")
        return

    # 3. Read CSV
    csv_path = "database.csv"
    if not os.path.exists(csv_path):
        print("database.csv not found.")
        return

    try:
        df = pd.read_csv(csv_path)
        # Strip whitespace from columns
        df.columns = df.columns.str.strip()
        print(f"Loaded {len(df)} rows from CSV.")
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # 4. Prepare data for insertion
    # Replace NaN with None (NULL in SQL)
    df = df.where(pd.notnull(df), None)
    
    # Clean column names in DF to match SQL if needed (they seem to match: item_number, etc.)
    records = df.to_dict(orient='records')

    # 5. Insert into Supabase
    try:
        print(f"Attempting to upsert {len(records)} records...")
        
        # Upsert with on_conflict item_number to avoid duplicates if re-run
        response = supabase.table("items").upsert(records, on_conflict="item_number").execute()
        
        print("Migration successful!")
        # print(response) # Response might be large/complex
        
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate_csv_to_supabase()
