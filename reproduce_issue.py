import pandas as pd
from db_utils import get_supabase
import toml

# Mock st.secrets for local run if needed, but db_utils uses st.secrets.
# We might need to mock streamlit.secrets if we run this as a straight python script.
# Actually, db_utils imports streamlit. If we run as python script, st.secrets might be empty or fail.
# Let's patch db_utils.get_supabase or st.secrets.

import streamlit as st
# Load secrets manually for this script
try:
    secrets = toml.load(".streamlit/secrets.toml")
    st.secrets = secrets
except Exception as e:
    print(f"Could not load secrets: {e}")

def load_items_from_db():
    print("Loading items...")
    try:
        supabase = get_supabase()
        response = supabase.table("items").select("*").execute()
        df = pd.DataFrame(response.data)
        
        # Ensure correct types
        if not df.empty and 'item_number' in df.columns:
             df['item_number'] = pd.to_numeric(df['item_number'], errors='coerce').fillna(0).astype(int)

        # String cleanup (from found_lost.py)
        for col in df.select_dtypes(include=['object']).columns:
             df[col] = df[col].astype(str).str.strip()
        
        print(f"Loaded {len(df)} items.")
        return df
             
    except Exception as e:
        print(f"Failed to load database: {e}")
        return pd.DataFrame()

def save_to_db(df):
    print("Attempting to save ALL items (bulk upsert)...")
    try:
        supabase = get_supabase()
        # Convert NaN to None for SQL
        df_clean = df.where(pd.notnull(df), None)
        records = df_clean.to_dict(orient='records')
        
        print(f"Upserting {len(records)} records...")
        # Upsert
        response = supabase.table("items").upsert(records, on_conflict="item_number").execute()
        print("Save successful!")
        return True
    except Exception as e:
        print(f"Failed to save to database: {e}")
        return False

if __name__ == "__main__":
    df = load_items_from_db()
    if not df.empty:
        # Simulate adding a new item
        next_id = df['item_number'].max() + 1
        new_item = {
            'item_number': next_id,
            'item_name': f"Repro Item {next_id}",
            'item_description': "Reproduction Description",
            'item_image': "https://via.placeholder.com/150",
            'item_contact_type': "email",
            'item_contact': "repro@test.com",
            'item_location': "Repro Land",
            'item_date_start': "2026-01-01",
            'item_date_end': "2026-01-01",
            'item_status': "lost"
        }
        # Ensure new item has all columns in df
        for col in df.columns:
            if col not in new_item:
                new_item[col] = "" # or appropriate default
        
        new_row = pd.DataFrame([new_item])
        df = pd.concat([df, new_row], ignore_index=True)
        
        save_to_db(df)
    else:
        print("DataFrame empty, cannot test bulk upsert properly (or DB is empty).")
