import pandas as pd
from db_utils import get_supabase
import toml
import streamlit as st

# Load secrets manually for this script as it runs standalone
try:
    secrets = toml.load(".streamlit/secrets.toml")
    st.secrets = secrets
except Exception as e:
    print(f"Could not load secrets: {e}")

def verify_save_item_to_db():
    print("Testing save_item_to_db verify logic...")
    try:
        supabase = get_supabase()
        
        # Helper to get next ID (simplified)
        res = supabase.table("items").select("item_number").execute()
        existing_ids = [int(x['item_number']) for x in res.data if x.get('item_number')]
        next_id = max(existing_ids) + 1 if existing_ids else 1
        
        # Create an item with empty strings (which caused the error before)
        test_item = {
            'item_number': next_id,
            'item_name': f"Verify Fix Item {next_id}",
            'item_description': "This item has an empty date string to test the fix",
            'item_image': "", # Empty string
            'item_contact_type': "email",
            'item_contact': "verify@test.com",
            'item_location': "Verify Land",
            'item_date_start': "", # Empty string - THIS WAS THE KILLER
            'item_date_end': "", # Empty string
            'item_status': "lost"
        }
        
        print(f"Original Item: {test_item}")
        
        # APPLY THE FIX LOGIC
        clean_item = {k: (v if v != "" else None) for k, v in test_item.items()}
        print(f"Cleaned Item: {clean_item}")
        
        print("Upserting single clean item...")
        response = supabase.table("items").upsert([clean_item], on_conflict="item_number").execute()
        
        print("Success! Response:", response)
        return True
        
    except Exception as e:
        print(f"Failed to save item to database: {e}")
        return False

if __name__ == "__main__":
    verify_save_item_to_db()
