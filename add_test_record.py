import toml
from supabase import create_client
import os
import time

def add_record():
    try:
        if not os.path.exists(".streamlit/secrets.toml"):
            print("Secrets file missing!")
            return

        secrets = toml.load(".streamlit/secrets.toml")
        url = secrets["supabase"]["url"]
        key = secrets["supabase"]["key"]
        
        print(f"Connecting to {url}...")
        supabase = create_client(url, key)
        
        # Create a test item
        test_item = {
            "item_number": "9999", # Distinct number
            "item_name": "TEST RECORD FROM AI",
            "item_description": "This is a test record added directly to verify database write access. You can delete this.",
            "item_image": "https://placehold.co/400x300?text=Test+Item",
            "item_contact_type": "email",
            "item_contact": "test@ai.bot",
            "item_location": "The Cloud",
            "item_date_start": "2026-01-01",
            "item_date_end": "2026-01-01",
            "item_status": "lost"
        }
        
        print("Inserting test record...")
        response = supabase.table("items").upsert([test_item]).execute()
        
        print("Success! Record added.")
        print(response.data)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    add_record()
