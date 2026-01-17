import toml
from supabase import create_client
import os
import pandas as pd
from datetime import datetime

# Mimic the app's environment
def get_supabase():
    secrets = toml.load(".streamlit/secrets.toml")
    url = secrets["supabase"]["url"]
    key = secrets["supabase"]["key"]
    return create_client(url, key)

def get_next_item_number_db():
    print("Getting next ID...")
    try:
        supabase = get_supabase()
        response = supabase.table("items").select("item_number").execute()
        data = response.data
        print(f"Current IDs in DB: {[r.get('item_number') for r in data]}")
        
        if not data:
            return 1
        
        numbers = []
        for row in data:
            try:
                numbers.append(int(row['item_number']))
            except:
                pass
        
        if not numbers:
            return 1
            
        next_id = max(numbers) + 1
        print(f"Calculated Next ID: {next_id}")
        return next_id
    except Exception as e:
        print(f"Error getting next ID: {e}")
        return 1

def debug_upsert():
    try:
        print("Initializing Supabase...")
        supabase = get_supabase()
        
        next_id = get_next_item_number_db()
        
        print(f"Preparing to insert item #{next_id}...")
        
        # Mimic the DataFrame structure used in the app
        new_item = {
            'item_number': next_id, # Sending as INT
            'item_name': f"Debug Submission {next_id}",
            'item_description': "Debug Description",
            'item_image': "https://via.placeholder.com/150",
            'item_contact_type': "email",
            'item_contact': "debug@test.com",
            'item_location': "Debug Land",
            'item_date_start': "2026-01-01",
            'item_date_end': "2026-01-01",
            'item_status': "lost"
        }
        
        # The app puts it in a DF first, then converts to dict records
        df = pd.DataFrame([new_item])
        
        # Mimic save_to_csv logic exactly
        print("Converting DF to records...")
        df_clean = df.where(pd.notnull(df), None)
        records = df_clean.to_dict(orient='records')
        print(f"Payload: {records}")
        
        print("Executing Upsert...")
        response = supabase.table("items").upsert(records, on_conflict="item_number").execute()
        
        print("Upsert Response:", response)
        print("Check Supabase dashboard now!")
        
    except Exception as e:
        print(f"CRITICAL FAILURE: {e}")

if __name__ == "__main__":
    debug_upsert()
