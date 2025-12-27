import streamlit as st
import pandas as pd
from datetime import datetime
import os
from datetime import timedelta
from PIL import Image
import io
import pyotp
import difflib
import json
import time

# Function to calculate relevance for fuzzy search
def calculate_relevance(row, query):
    if not query:
        return 0
    query = query.lower()
    score = 0
    
    # 1. Title Match
    title = str(row.get('item_name', '')).lower()
    if query in title:
        score += 100  # Exact substring match in title
    else:
        # Fuzzy word match in title
        for word in title.split():
            ratio = difflib.SequenceMatcher(None, query, word).ratio()
            if ratio > 0.6: 
                score += 50 * ratio 
                
    # 2. Description Match
    desc = str(row.get('item_description', '')).lower()
    if query in desc:
        score += 30   # Exact substring match in description
    else:
        # Fuzzy word match in description
        for word in desc.split():
            ratio = difflib.SequenceMatcher(None, query, word).ratio()
            if ratio > 0.6:
                score += 15 * ratio
                
    return score

import time

# Page configuration
st.set_page_config(page_title="Lost and Found", layout="wide", initial_sidebar_state="expanded")

# Initialize Session State for Balloons
if 'last_balloon_time' not in st.session_state:
    st.session_state.last_balloon_time = 0

# --- User Notification Section (Announcements & Balloons) ---
# Check for balloons
if os.path.exists("balloons.txt"):
    try:
        with open("balloons.txt", "r") as f:
            balloon_ts = float(f.read().strip())
            if balloon_ts > st.session_state.last_balloon_time:
                st.balloons()
                st.session_state.last_balloon_time = balloon_ts
    except Exception:
        pass # Ignore errors in reading balloon file


# Check for announcements
if os.path.exists("announcement.json"):
    try:
        with open("announcement.json", "r") as f:
            ann_data = json.load(f)
            
        show_announcement = False
        if ann_data.get('type') == 'perm':
            show_announcement = True
        elif ann_data.get('type') == 'shout':
            # Check if within 10 seconds of timestamp
            if time.time() - ann_data.get('timestamp', 0) < 10:
                show_announcement = True
                # Optional: Auto-refresh to clear it? No, rely on user action or next refresh.
                # But to make it "live" we might need st.empty but for now basic logic is fine.
        
        if show_announcement:
            msg = ann_data.get('text', '')
            if msg:
                st.markdown(f"<h2 style='color: #FF5722; text-align: center; border: 2px solid #FF5722; padding: 10px; border-radius: 10px; background-color: #FFF3E0;'>📢 {msg}</h2>", unsafe_allow_html=True)
                
    except Exception:
        pass


# Custom CSS for styling
st.markdown("""
    <style>
    .item-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
        background-color: #f9f9f9;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .status-box {
        background-color: #e3f2fd;
        padding: 12px;
        border-radius: 5px;
        margin: 5px 0;
        font-size: 14px;
    }
    .description-box {
        background-color: #fff;
        padding: 20px;
        border-radius: 5px;
        border: 1px solid #ddd;
        min-height: 150px;
        font-size: 15px;
        line-height: 1.6;
        color: #333;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .description-box:hover {
        background-color: #f5f5f5;
    }
    .image-container {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .title-text {
        font-size: 24px;
        font-weight: bold;
        margin-top: 10px;
        color: #333;
    }
    /* Hidden admin button styling (blend with background) */
    .admin-btn button {
        color: #f0f2f6 !important;
        background: #f0f2f6 !important;
        border: none !important;
        padding: 2px 8px !important;
        height: 28px !important;
        box-shadow: none !important;
    }
    .admin-btn button:hover {
        background: #f0f2f6 !important;
        color: #f0f2f6 !important;
    }
    @media (max-width: 768px) {
        .description-box {
            min-height: 100px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'items_df' not in st.session_state:
    if os.path.exists("database.csv"):
        # Read CSV and strip whitespace from column names
        st.session_state.items_df = pd.read_csv("database.csv")
        st.session_state.items_df.columns = st.session_state.items_df.columns.str.strip()
        # Also strip whitespace from string values
        for col in st.session_state.items_df.select_dtypes(include=['object']).columns:
            st.session_state.items_df[col] = st.session_state.items_df[col].astype(str).str.strip()
        
        # Handle backward compatibility - migrate old format to new format
        if 'item_date' in st.session_state.items_df.columns:
            if 'item_date_start' not in st.session_state.items_df.columns:
                st.session_state.items_df['item_date_start'] = st.session_state.items_df['item_date']
            if 'item_date_end' not in st.session_state.items_df.columns:
                st.session_state.items_df['item_date_end'] = st.session_state.items_df['item_date']
        
        if 'item_contact_type' not in st.session_state.items_df.columns:
            st.session_state.items_df['item_contact_type'] = ''
        
        # Ensure all required columns exist
        required_columns = ['item_number', 'item_name', 'item_description', 'item_image', 
                           'item_contact_type', 'item_contact', 'item_location', 
                           'item_date_start', 'item_date_end', 'item_status']
        for col in required_columns:
            if col not in st.session_state.items_df.columns:
                st.session_state.items_df[col] = ''
    else:
        st.session_state.items_df = pd.DataFrame(columns=[
            'item_number', 'item_name', 'item_description', 'item_image', 
            'item_contact_type', 'item_contact', 'item_location', 'item_date_start', 'item_date_end', 'item_status'
        ])

if 'show_form' not in st.session_state:
    st.session_state.show_form = False

if 'uploaded_images' not in st.session_state:
    st.session_state.uploaded_images = {}

# Admin controls
if 'show_admin_auth' not in st.session_state:
    st.session_state.show_admin_auth = False
if 'admin_unlocked' not in st.session_state:
    st.session_state.admin_unlocked = False
if 'admin_lock_until' not in st.session_state:
    st.session_state.admin_lock_until = None
if 'admin_taunt_idx' not in st.session_state:
    st.session_state.admin_taunt_idx = 0
if 'admin_auth_stage' not in st.session_state:
    st.session_state.admin_auth_stage = 0

if 'expanded_items' not in st.session_state:
    st.session_state.expanded_items = set()

# Function to save data to CSV
def save_to_csv(df):
    df.to_csv("database.csv", index=False)

# Function to get next item number
def get_next_item_number(df):
    if len(df) == 0:
        return 1
    return df['item_number'].max() + 1

# Helper function to safely get value from Series
def get_value(series, key, default=''):
    """Safely get value from pandas Series, handling missing values and NaN"""
    if key in series.index:
        val = series[key]
        if pd.isna(val) or str(val).strip().lower() == 'nan':
            return default
        return str(val).strip()
    return default

# Function to display item card
def display_item_card(item, item_idx=None, tab_name=""):
    # Create a container for the card
    with st.container():
        col1, col2, col3 = st.columns([2.5, 1.8, 4])
        
        with col1:
            # Image and Title section (left column)
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            # Get image from Series
            image_val = get_value(item, 'item_image', '')
            if image_val and image_val != '':
                image_path = image_val
                # Check for URL
                if image_path.startswith('http://') or image_path.startswith('https://'):
                    st.image(image_path, use_container_width=True)
                # Check directly on disk (relative path)
                elif os.path.exists(image_path):
                    st.image(image_path, use_container_width=True)
                # Fallback check for filename in images dir if path is just filename
                elif os.path.exists(os.path.join("images", os.path.basename(image_path))):
                     st.image(os.path.join("images", os.path.basename(image_path)), use_container_width=True)
                else:
                    st.image("https://via.placeholder.com/200x150?text=No+Image", use_container_width=True)
            else:
                st.image("https://via.placeholder.com/200x150?text=No+Image", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Get title from Series
            title = get_value(item, 'item_name', 'Untitled')
            if not title or title == '':
                title = 'Untitled'
            st.markdown(f'<div class="title-text">{title}</div>', unsafe_allow_html=True)
        
        with col2:
            # Status and location/time section (middle small box)
            # Get status from Series
            status = get_value(item, 'item_status', 'unknown').lower()
            if not status or status == '':
                status = 'unknown'
            if status == "lost":
                status_color = "#ff9800"
            elif status == "archive":
                status_color = "#9e9e9e"
            else:
                status_color = "#4caf50"
            
            # Get location from Series
            location = get_value(item, 'item_location', 'N/A')
            if not location or location == '':
                location = 'N/A'
            
            # Get date from Series - handle both single date and date range
            date_start = get_value(item, 'item_date_start', '')
            date_end = get_value(item, 'item_date_end', '')
            # Fallback to old item_date field for backward compatibility
            if not date_start or date_start == '':
                date_start = get_value(item, 'item_date', '')
            
            if date_start and date_end and date_start != date_end:
                date_display = f"{date_start} to {date_end}"
            elif date_start:
                date_display = date_start
            else:
                date_display = 'N/A'
            
            st.markdown(f"""
                <div class="status-box" style="background-color: {status_color}15; border-left: 4px solid {status_color};">
                    <strong>Status:</strong><br>{status.upper()}<br><br>
                    <strong>Where:</strong><br>{location}<br><br>
                    <strong>When:</strong><br>{date_display}
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            # Description section (right large box)
            # Get description from Series
            description = get_value(item, 'item_description', 'No description available.')
            if not description or description == '':
                description = 'No description available.'
            
            # Get contact information
            contact_type = get_value(item, 'item_contact_type', '')
            contact_val = get_value(item, 'item_contact', '')
            contact_display = ''
            if contact_type == 'email':
                contact_display = f"📧 Email: {contact_val}"
            elif contact_type == 'phone':
                contact_display = f"📞 Phone: {contact_val}"
            elif contact_type == 'office':
                office_name = contact_val if contact_val else 'Office'
                contact_display = f"🏢 Contact: {office_name}"
            
            # Get all item details for expanded view
            item_number = get_value(item, 'item_number', '')
            title = get_value(item, 'item_name', 'Untitled')
            location = get_value(item, 'item_location', 'N/A')
            date_start = get_value(item, 'item_date_start', '')
            date_end = get_value(item, 'item_date_end', '')
            status = get_value(item, 'item_status', 'unknown').upper()
            
            # Create unique key for this item (include tab name to avoid duplicates across tabs)
            item_key = f"{tab_name}_item_{item_number}_{item_idx if item_idx is not None else item_number}"
            is_expanded = item_key in st.session_state.expanded_items
            
            # Create expandable description box
            if is_expanded:
                # Show full details
                full_details = f"""
                    <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; border: 2px solid #4CAF50; margin-bottom: 10px;">
                        <strong style="color: #333;">Full Details:</strong><br><br>
                        <strong style="color: #333;">Item Number:</strong> <span style="color: #333;">{item_number}</span><br>
                        <strong style="color: #333;">Title:</strong> <span style="color: #333;">{title}</span><br>
                        <strong style="color: #333;">Status:</strong> <span style="color: #333;">{status}</span><br>
                        <strong style="color: #333;">Location:</strong> <span style="color: #333;">{location}</span><br>
                        <strong style="color: #333;">Date Range:</strong> <span style="color: #333;">{date_start} to {date_end}</span><br>
                        <strong style="color: #333;">Description:</strong><br><span style="color: #333;">{description}</span><br>
                        {f'<br><strong style="color: #333;">Contact:</strong><br><span style="color: #333;">{contact_display}</span>' if contact_display else ''}
                    </div>
                """
                st.markdown(full_details, unsafe_allow_html=True)
                col_btn1, col_btn2, col_btn3 = st.columns([2, 3, 2])
                with col_btn2:
                    if st.button("✖️ Collapse", key=f"hide_{item_key}", use_container_width=True, type="secondary"):
                        st.session_state.expanded_items.discard(item_key)
                        st.rerun()
            else:
                # Show preview with clickable area
                preview_text = description[:200] + "..." if len(description) > 200 else description
                show_full_button = len(description) > 200 or contact_display
                
                st.markdown(f"""
                    <div class="description-box">
                        <strong style="color: #333;">Description:</strong><br><br>
                        <span style="color: #333;">{preview_text}</span>
                        {f'<br><br><strong style="color: #333;">Contact:</strong><br><span style="color: #333;">{contact_display}</span>' if contact_display else ''}
                    </div>
                """, unsafe_allow_html=True)
                
                if show_full_button:
                    col_btn1, col_btn2, col_btn3 = st.columns([2, 3, 2])
                    with col_btn2:
                        if st.button("📋 View Full Details", key=f"click_{item_key}", use_container_width=True):
                            st.session_state.expanded_items.add(item_key)
                            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)

# Main title with white color
st.markdown("""
    <style>
    h1 {
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)
st.title("Lost and Found")

# --- Admin access (moved to top) ---
admin_top_col = st.columns([0.08, 0.92])[0]
with admin_top_col:
    admin_click = st.button("Admin", key="admin_hidden_top")
    st.markdown("""
        <style>
        div[data-testid="column"]:first-child div[data-testid="stButton"] > button {
            color: #f0f2f6 !important;
            background: #f0f2f6 !important;
            border: none !important;
            padding: 2px 8px !important;
            height: 28px !important;
            box-shadow: none !important;
        }
        div[data-testid="column"]:first-child div[data-testid="stButton"] > button:hover {
            background: #f0f2f6 !important;
            color: #f0f2f6 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    if admin_click:
        st.session_state.show_admin_auth = True

# Search Functionality
search_query = st.text_input("🔍 Search Items", placeholder="Type to search (e.g. 'phone' matches 'phonie')...", label_visibility="visible")

# Tab navigation (including Archive)
tab1, tab2, tab3, tab4 = st.tabs(["Lost", "All", "Found", "Archive"])

# Filter items based on selected tab
# Reload from CSV to ensure we have latest data
if os.path.exists("database.csv"):
    df = pd.read_csv("database.csv")
    df.columns = df.columns.str.strip()
    # Strip whitespace from string values
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()
    
    # Handle backward compatibility - migrate old format to new format
    if 'item_date' in df.columns:
        if 'item_date_start' not in df.columns:
            df['item_date_start'] = df['item_date']
        if 'item_date_end' not in df.columns:
            df['item_date_end'] = df['item_date']
    
    if 'item_contact_type' not in df.columns:
        df['item_contact_type'] = ''
    
    # Ensure all required columns exist
    required_columns = ['item_number', 'item_name', 'item_description', 'item_image', 
                       'item_contact_type', 'item_contact', 'item_location', 
                       'item_date_start', 'item_date_end', 'item_status']
    for col in required_columns:
        if col not in df.columns:
            df[col] = ''
    
    # Update session state
    st.session_state.items_df = df.copy()
else:
    df = st.session_state.items_df.copy()

# Admin authentication UI (top)
if st.session_state.show_admin_auth and not st.session_state.admin_unlocked:
    with st.expander("Admin Login", expanded=True):
        stage = st.session_state.admin_auth_stage
        
        # Determine current prompt based on stage
        if stage == 0:
            prompt_label = "Enter 1st Admin Password"
        elif stage == 1:
            prompt_label = "Enter 2nd Admin Password"
        else:
            prompt_label = "Enter 3rd Admin Password"
            
        # Use a unique key per stage so the input clears/updates
        admin_pwd = st.text_input(prompt_label, type="password", key=f"admin_pwd_{stage}")
        
        now_ts = datetime.now().timestamp()
        locked = st.session_state.admin_lock_until and now_ts < st.session_state.admin_lock_until

        if locked:
            wait_sec = int(st.session_state.admin_lock_until - now_ts)
            st.warning(f"Locked. Please wait {wait_sec} seconds before trying again.")
        else:
            if st.button("Unlock / Next Step", key=f"unlock_admin_{stage}"):
                # Password logic
                correct = False
                if stage == 0 and admin_pwd == "Arm081750#":
                    correct = True
                elif stage == 1 and admin_pwd == "FFsQu5H6#":
                    correct = True
                elif stage == 2 and admin_pwd == "Armisawesome1!":
                    correct = True
                
                if correct:
                    if stage < 2:
                        st.session_state.admin_auth_stage += 1
                        st.success(f"Password {stage+1} correct. Proceeding to next step.")
                        st.rerun()
                    else:
                        # Final stage correct
                        st.session_state.admin_unlocked = True
                        st.session_state.admin_auth_stage = 0 # Reset for next time
                        st.success("Admin unlocked")
                        st.rerun()
                else:
                    # Wrong password
                    taunts = ["try again", "that's... not it.", "what are you trying to do?"]
                    st.session_state.admin_taunt_idx = (st.session_state.admin_taunt_idx + 1) % len(taunts)
                    st.session_state.admin_lock_until = now_ts + 5 # Short lock
                    # Optional: Reset to stage 0 on failure? User didn't specify, but for security resetting is often better.
                    # However, to be less annoying, we'll keep them on the current stage but lock them briefly.
                    st.error(taunts[st.session_state.admin_taunt_idx])


# Admin interface for archiving (claiming) items
if st.session_state.admin_unlocked:
    # --- Announcements & Fun ---
    with st.expander("Admin: Announcements & Fun 🎈", expanded=False):
        st.subheader("Broadcast Announcement")
        st.subheader("Broadcast Announcement")
        new_announcement = st.text_area("Announcement Message", placeholder="Enter message for all users...")
        ann_type = st.radio("Announcement Type", ["Permanent Shout", "10s Shout"], horizontal=True)
        
        col_ann_1, col_ann_2 = st.columns(2)
        with col_ann_1:
            if st.button("📢 Post Announcement", use_container_width=True):
                ann_data = {
                    "text": new_announcement,
                    "type": "shout" if ann_type == "10s Shout" else "perm",
                    "timestamp": time.time()
                }
                with open("announcement.json", "w") as f:
                    json.dump(ann_data, f)
                st.success("Announcement posted!")
        with col_ann_2:
            if st.button("🗑️ Clear Announcement", use_container_width=True):
                if os.path.exists("announcement.json"):
                    os.remove("announcement.json")
                st.success("Announcement cleared!")
        
        st.divider()
        st.subheader("Fun Triggers")
        if st.button("🎈 Send Balloons to Everyone", use_container_width=True):
            with open("balloons.txt", "w") as f:
                f.write(str(time.time()))
            st.success("Balloons sent!")
            
    with st.expander("Admin: mark items as claimed (archive)", expanded=False):
        if st.button("Exit admin", key="exit_admin"):
            st.session_state.admin_unlocked = False
            st.session_state.show_admin_auth = False
            st.session_state.admin_lock_until = None
            st.success("Admin exited")
            st.rerun()
        state_df = st.session_state.items_df
        if len(state_df) == 0:
            st.info("No items available to archive.")
        else:
            has_active = False
            for idx, row in state_df.iterrows():
                status_val = str(row.get('item_status', '')).lower().strip() if pd.notna(row.get('item_status', '')) else ''
                if status_val == 'archive':
                    continue
                has_active = True
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.markdown(f"**#{row.get('item_number', '?')} - {row.get('item_name', 'Untitled')}**")
                    st.markdown(f"Status: {row.get('item_status', 'unknown')}")
                    st.markdown(f"Location: {row.get('item_location', 'N/A')}")
                    st.markdown(f"Date: {row.get('item_date_start', 'N/A')} to {row.get('item_date_end', 'N/A')}")
                with col_b:
                    if st.button("Mark as archived", key=f"archive_{row.get('item_number', idx)}"):
                        st.session_state.items_df.loc[row.name, 'item_status'] = 'archive'
                        save_to_csv(st.session_state.items_df)
                        st.success("Item archived")
                        st.rerun()
            if not has_active:
                st.info("All items are already archived.")

# Apply Search Filter to global df if query exists
if search_query:
    # Calculate scores for all items
    scores = []
    for idx, row in df.iterrows():
        score = calculate_relevance(row, search_query)
        scores.append(score)
    
    df['relevance_score'] = scores
    # Filter out zero relevance
    df = df[df['relevance_score'] > 0]
    # Sort by score descending
    df = df.sort_values(by='relevance_score', ascending=False)
    
    if len(df) == 0:
        st.info(f"No items found matching '{search_query}'.")

with tab1:
    if len(df) > 0 and 'item_status' in df.columns:
        filtered_df = df[df['item_status'].str.lower().str.strip() == 'lost']
    else:
        filtered_df = pd.DataFrame()
    st.subheader("Lost Items")
    
    if len(filtered_df) == 0:
        st.info("No lost items found.")
    else:
        for idx, row in filtered_df.iterrows():
            display_item_card(row, idx, "lost")

with tab2:
    st.subheader("All Items")
    
    if len(df) == 0:
        st.info("No items found. Submit an item to get started!")
    else:
        for idx, row in df.iterrows():
            display_item_card(row, idx, "all")

with tab3:
    if len(df) > 0 and 'item_status' in df.columns:
        filtered_df = df[df['item_status'].str.lower().str.strip() == 'found']
    else:
        filtered_df = pd.DataFrame()
    st.subheader("Found Items")
    
    if len(filtered_df) == 0:
        st.info("No found items found.")
    else:
        for idx, row in filtered_df.iterrows():
            display_item_card(row, idx, "found")

with tab4:
    if len(df) > 0 and 'item_status' in df.columns:
        filtered_df = df[df['item_status'].str.lower().str.strip() == 'archive']
    else:
        filtered_df = pd.DataFrame()
    st.subheader("Archived (Claimed) Items")
    
    if len(filtered_df) == 0:
        st.info("No archived items.")
    else:
        for idx, row in filtered_df.iterrows():
            display_item_card(row, idx, "archive")

# Submit form (using sidebar or expander)
st.sidebar.title("Submit New Item")

with st.sidebar:
    with st.form("submit_item_form", clear_on_submit=True):
        st.subheader("Item Details")
        
        uploaded_file = st.file_uploader("Upload Image *", type=['png', 'jpg', 'jpeg'], help="Image is required")
        
        item_name = st.text_input("Title *", placeholder="Enter item name")
        
        item_status = st.selectbox("Status *", ["lost", "found"], index=0)
        
        item_location = st.text_input("Where *", placeholder="Enter location")
        
        # Date selection - single date or date range
        date_option = st.radio("Date Type *", ["Single Date", "Date Range"], horizontal=True)
        
        today = datetime.now().date()
        max_date = today  # Cannot select future dates
        
        if date_option == "Single Date":
            item_date_start = st.date_input("When *", value=today, max_value=max_date, key="date_start")
            item_date_end = item_date_start  # Same date for single date
        else:
            col_date1, col_date2 = st.columns(2)
            with col_date1:
                item_date_start = st.date_input("From Date *", value=today, max_value=max_date, key="date_start_range")
            with col_date2:
                item_date_end = st.date_input("To Date *", value=today, max_value=max_date, key="date_end_range")
        
        item_description = st.text_area("Description *", placeholder="Enter detailed description", height=150)
        
        # Contact options - None is not allowed, user must select a contact type
        contact_type = st.selectbox("Contact Type *", ["Email", "Phone", "Contact Office"], index=0)
        
        item_contact = ''
        item_contact_type = ''
        
        if contact_type == "Email":
            item_contact = st.text_input("Email Address *", placeholder="example@email.com")
            item_contact_type = 'email'
        elif contact_type == "Phone":
            item_contact = st.text_input("Phone Number *", placeholder="0812345678")
            item_contact_type = 'phone'
        elif contact_type == "Contact Office":
            office_selection = st.selectbox("Select Office *", ["A Building Office", "H Building Office"], key="office_select")
            item_contact = office_selection
            item_contact_type = 'office'
        
        submitted = st.form_submit_button("Submit Item", type="primary", use_container_width=True)
        
        if submitted:
            # Validation
            validation_errors = []
            if not item_name:
                validation_errors.append("Title is required")
            
            # Location validation - prevent generic/vague locations
            blocked_locations = [
                'earth', 'the world', 'this planet', 'somewhere on earth',
                'here', 'there', 'over there', 'around here', 'nearby', 'far away',
                'in the area', 'somewhere else', 'out there',
                'asia', 'europe', 'africa', 'north america', 'south america',
                'australia', 'antarctica', 'the middle east', 'southeast asia',
                'the pacific', 'the northern hemisphere', 'the southern hemisphere',
                'the tropics', 'thailand', 'japan', 'brazil', 'canada', 'india',
                'france', 'mexico', 'kenya',
                'in the city', 'in the countryside', 'in town', 'out of town',
                'downtown', 'uptown', 'suburbs', 'rural area', 'on the outskirts',
                'the neighborhood', 'indoors', 'outdoors',
                'near the water', 'by the river', 'near the ocean', 'on the coast',
                'in the mountains', 'in the forest', 'in the desert', 'at the park',
                'near the road', 'somewhere mysterious', 'the unknown', 'the beyond',
                'not sure', 'i forgot', 'lost in time and space',
                'in a parallel universe', 'over the horizon', 'the middle of nowhere',
                'somewhere kinda far', 'at home', 'solar system', 'at work', 'at the store',
                'at the station', 'on the street', 'at the mall', 'at the restaurant',
                'near my house', 'by the bus stop', 'at the corner', 'at the market'
            ]
            
            if not item_location:
                validation_errors.append("Location is required")
            elif item_location.lower().strip() in blocked_locations:
                validation_errors.append("Please provide a specific, detailed location. Generic locations like 'here', 'there', country names, or vague descriptions are not allowed.")
            
            if not item_description:
                validation_errors.append("Description is required")
            
            # Date validation
            if item_date_start > max_date or item_date_end > max_date:
                validation_errors.append("Cannot select dates in the future")
            elif date_option == "Date Range":
                if item_date_start > item_date_end:
                    validation_errors.append("Start date must be before or equal to end date")
                elif item_date_start == item_date_end:
                    validation_errors.append("For date range, start date and end date must be different. Use 'Single Date' if you want one date.")
            
            # Image validation - image is required
            if uploaded_file is None:
                validation_errors.append("Image upload is required")
            
            # Contact validation - contact type is required (None is not an option)
            if not item_contact:
                validation_errors.append(f"{contact_type} contact information is required")
            elif contact_type == "Email":
                # Email validation - must contain @ symbol
                if '@' not in item_contact:
                    validation_errors.append("Email address must contain '@' symbol")
            
            if not validation_errors:
                # Handle image upload
                image_path = ""
                if uploaded_file is not None:
                    # Save to images/ folder
                    file_ext = uploaded_file.name.split('.')[-1]
                    filename = f"img_{get_next_item_number(st.session_state.items_df)}_{int(datetime.now().timestamp())}.{file_ext}"
                    save_path = os.path.join("images", filename)
                    
                    # Create dir if not exists (safety check)
                    if not os.path.exists("images"):
                        os.makedirs("images")
                        
                    with open(save_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    image_path = save_path
                
                # Create new item
                new_item = {
                    'item_number': get_next_item_number(st.session_state.items_df),
                    'item_name': item_name,
                    'item_description': item_description,
                    'item_image': image_path,
                    'item_contact_type': item_contact_type,
                    'item_contact': item_contact if item_contact else '',
                    'item_location': item_location,
                    'item_date_start': str(item_date_start),
                    'item_date_end': str(item_date_end),
                    'item_status': item_status.lower()
                }
                
                # Add to dataframe
                new_row = pd.DataFrame([new_item])
                st.session_state.items_df = pd.concat([st.session_state.items_df, new_row], ignore_index=True)
                
                # Save to CSV
                save_to_csv(st.session_state.items_df)
                
                st.success("Item submitted successfully!")
                st.rerun()
            else:
                for error in validation_errors:
                    st.error(error)
                
