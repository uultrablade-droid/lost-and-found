import toml
from supabase import create_client
import os

def test_connection():
    try:
        if not os.path.exists(".streamlit/secrets.toml"):
            print("Secrets file missing!")
            return

        secrets = toml.load(".streamlit/secrets.toml")
        url = secrets["supabase"]["url"]
        key = secrets["supabase"]["key"]
        
        print(f"Connecting to {url}...")
        supabase = create_client(url, key)
        
        print("Fetching items...")
        response = supabase.table("items").select("*").execute()
        
        data = response.data
        print(f"Found {len(data)} items.")
        if len(data) > 0:
            print("First item sample:", data[0])
        else:
            print("Table is empty.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_connection()
