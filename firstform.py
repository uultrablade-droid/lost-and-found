import streamlit as st
import pandas as pd

# Page config must be the first Streamlit command
st.set_page_config(layout="wide", page_title="Clinic Ya")

# --- CSS Styling ---
# We keep the detailed card styles and add styles for the simple home list
st.markdown("""
<style>
    /* Global */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }

    /* --- Inventory View Styles --- */
    .medicine-card {
        border: 2px solid #5a5a5a;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        background-color: #262730;
    }
    .medicine-name {
        border: 1px solid #777;
        border-radius: 5px;
        padding: 8px;
        text-align: center;
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 15px;
        background-color: #1e1e1e;
        color: #fff;
    }
    .info-box {
        border: 1px solid #555;
        border-radius: 5px;
        padding: 5px;
        text-align: center;
        margin-bottom: 5px;
        background-color: #31333f;
    }
    .info-label {
        font-size: 0.8rem;
        color: #aaa;
        display: block;
        margin-bottom: 2px;
    }
    .info-value {
        font-size: 1rem;
        font-weight: bold;
        color: #fff;
    }
    img.med-image {
        width: 100%;
        height: 150px;
        object-fit: cover;
        border-radius: 5px;
    }

    /* --- Home View Styles --- */
    .home-title {
        font-size: 4rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 3rem;
        color: #333; /* Dark gray for light mode, white for dark? Let's use standard text color */
    }
    .med-list-item {
        border: 2px solid #666;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: white; /* Adapting to light/dark might require more css, assuming dark theme from previous view context but let's stick to simple */
        color: black;
    }
    @media (prefers-color-scheme: dark) {
        .med-list-item {
            background-color: #262730;
            color: white;
            border-color: #555;
        }
        .home-title {
            color: white;
        }
    }
    
    .med-list-name {
        font-size: 1.2rem;
        font-weight: 500;
    }
    .med-list-amount {
        font-size: 1rem;
        color: #888;
        display: flex;
        flex-direction: column;
        align-items: flex-end;
    }
    
    /* Footer Buttons in Home */
    .home-footer {
        margin-top: 50px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* Simulate button styling if needed, but st.button is fine */
</style>
""", unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("medicines.csv")
        return df
    except FileNotFoundError:
        return pd.DataFrame()

df = load_data()

# --- State Management ---
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'
if 'selected_medicine' not in st.session_state:
    st.session_state['selected_medicine'] = None

def go_to_inventory(item_name=None):
    st.session_state['page'] = 'inventory'
    st.session_state['selected_medicine'] = item_name

def go_to_home():
    st.session_state['page'] = 'home'
    st.session_state['selected_medicine'] = None


# --- Views ---

def save_data(dataframe):
    dataframe.to_csv("medicines.csv", index=False)
    st.cache_data.clear()

def render_home():
    # Title
    st.markdown('<div class="home-title">clinic ya</div>', unsafe_allow_html=True)
    
    # Medicine List
    with st.container():
        if not df.empty:
            for index, row in df.iterrows():
                # We make the Name a button to trigger the view
                # To align nicely, we use columns. 
                # Note: st.button returns True if clicked. We use a key based on index/name.
                
                with st.container():
                    c_name, c_space, c_amt = st.columns([2, 1, 1])
                    with c_name:
                         # Use a button that looks like the name, or just a button "View details"
                         # User said "press each of the medicine". 
                         # A full width button is hard, so we make the Name the trigger.
                         if st.button(row['name'], key=f"home_btn_{index}", use_container_width=True):
                             go_to_inventory(item_name=row['name'])
                             st.rerun()
                             
                    with c_amt:
                        st.markdown(f"<div style='text-align: right; color: #888;'>Amount Left:<br><span style='font-size: 1.2rem; color: #fff;'>{row['left']}</span></div>", unsafe_allow_html=True)
                    
                    st.divider()
                
        else:
            st.info("No medicines found.")

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Footer Buttons
    c_back, c_space, c_admin = st.columns([1, 4, 1])
    with c_back:
        if st.button("go back to home", use_container_width=True):
            go_to_home() # Just refreshes/stays here
    
    with c_admin:
        if st.button("admin", use_container_width=True):
            go_to_inventory(item_name=None) # Full inventory
            st.rerun()

def render_inventory():
    # -- CSS for Sticky Header --
    st.markdown("""
    <style>
        .sticky-div {
            position: sticky;
            top: 0;
            z-index: 999;
            background-color: #0e1117;
            padding-top: 10px;
            padding-bottom: 20px;
            border-bottom: 1px solid #333;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- Header (Sticky) ---
    sticky_container = st.container()
    with sticky_container:
        st.markdown('<div class="sticky-div">', unsafe_allow_html=True)
        col_nav, col_cat_add, col_search = st.columns([1, 4, 3])
        
        with col_nav:
            if st.button("← Back"):
                go_to_home()
                st.rerun()

        # If a specific medicine is selected, we might hide the search/category bar 
        # OR we keep it to allow moving away from that single view?
        # User said "only one and its that one".
        # Let's keep the search bar but maybe default filtering overrides it.
        # Actually, if looking at one item, search doesn't make sense unless it clears the single selection.
        
        is_single_view = st.session_state['selected_medicine'] is not None
        
        if not is_single_view:
            with col_search:
                search_query = st.text_input("Search", placeholder="search bar")
            
            # --- Categories ---
            if not df.empty:
                all_categories = ["All"] + list(df['category'].unique())
                try:
                    selected_category = st.radio("Categories", all_categories, horizontal=True)
                except:
                    selected_category = "All"
        else:
            # In single view, just show title of what we are looking at or nothing extra
            with col_search:
                st.markdown(f"### Viewing: {st.session_state['selected_medicine']}")

        st.markdown('</div>', unsafe_allow_html=True)

    # --- Logic ---
    if not df.empty:
        # Filter Data
        filtered_df = df.copy()
        
        if is_single_view:
            # Exact match filter
            filtered_df = filtered_df[filtered_df['name'] == st.session_state['selected_medicine']]
        else:
            # Normal filters
            if selected_category != "All":
                filtered_df = filtered_df[filtered_df['category'] == selected_category]
                
            if search_query:
                filtered_df = filtered_df[filtered_df['name'].str.contains(search_query, case=False, na=False)]

        # --- Edit Mode Handling ---
        if 'edit_item_name' in st.session_state:
            item_name = st.session_state['edit_item_name']
            # Ensure item still exists
            if not df[df['name'] == item_name].empty:
                item_row = df[df['name'] == item_name].iloc[0]
                
                with st.form("edit_form"):
                    st.subheader(f"Editing {item_name}")
                    c1, c2 = st.columns(2)
                    with c1:
                        new_cat = st.text_input("Category", value=item_row['category'])
                        new_mg = st.text_input("Milligrams", value=item_row['milligrams'])
                        new_lots = st.number_input("Lots", value=int(item_row['lots']))
                        new_sold = st.number_input("Sold", value=int(item_row['sold']))
                    with c2:
                        new_left = st.number_input("Left", value=int(item_row['left']))
                        new_price = st.number_input("Price", value=float(item_row['price']))
                        new_desc = st.text_area("Description", value=item_row['description'])
                        new_expiry = st.text_input("Expiry Date", value=item_row['expiry_date'])
                    
                    if st.form_submit_button("Save Changes"):
                        # Update DataFrame
                        idx = df.index[df['name'] == item_name][0]
                        df.at[idx, 'category'] = new_cat
                        df.at[idx, 'milligrams'] = new_mg
                        df.at[idx, 'lots'] = new_lots
                        df.at[idx, 'sold'] = new_sold
                        df.at[idx, 'left'] = new_left
                        df.at[idx, 'price'] = new_price
                        df.at[idx, 'description'] = new_desc
                        df.at[idx, 'expiry_date'] = new_expiry
                        
                        save_data(df)
                        st.success("Updated successfully!")
                        del st.session_state['edit_item_name']
                        st.rerun()
                
                if st.button("Cancel Edit"):
                    del st.session_state['edit_item_name']
                    st.rerun()
                st.divider()

        # --- Display Grid ---
        # If single view, maybe center it? Or just standard grid with 1 item.
        cols = st.columns(2)
        
        for index, row in filtered_df.iterrows():
            col_idx = index % 2
            with cols[col_idx]:
                # Construct Card HTML
                card_html = f"""
<div class="medicine-card">
    <div class="medicine-name">{row['name']}</div>
    
    <!-- Row 1: Lots & Cat/Mg -->
    <div style="display: flex; gap: 10px; margin-bottom: 10px;">
        <div class="info-box" style="flex: 1; display: flex; flex-direction: column; justify-content: center;">
            <span class="info-label">Lots</span>
            <span class="info-value">{row['lots']}</span>
        </div>
        <div style="flex: 1; display: flex; flex-direction: column; gap: 5px;">
            <div class="info-box"><span class="info-value">{row['category']}</span></div>
            <div class="info-box"><span class="info-value">{row['milligrams']}</span></div>
        </div>
    </div>

    <!-- Row 2: Sold & Left -->
    <div style="display: flex; gap: 10px; margin-bottom: 10px;">
        <div class="info-box" style="flex: 1;">
            <span class="info-label">Sold</span>
            <span class="info-value">{row['sold']}</span>
        </div>
        <div class="info-box" style="flex: 1;">
            <span class="info-label">Left</span>
            <span class="info-value">{row['left']}</span>
        </div>
    </div>

    <!-- Row 3: Description -->
    <div class="info-box" style="margin-bottom: 10px; text-align: left;">
            <span class="info-label">Description</span>
            <div style="font-size: 0.9rem;">{row['description']}</div>
    </div>

    <!-- Row 4: Price & Lot# -->
    <div style="display: flex; gap: 10px; margin-bottom: 10px;">
            <div class="info-box" style="flex: 1;">
            <span class="info-label">Value (THB)</span>
            <span class="info-value">{row['price']}</span>
        </div>
        <div class="info-box" style="flex: 1;">
            <span class="info-label">Lot Number</span>
            <span class="info-value">{row['lot_number']}</span>
        </div>
    </div>
    
    <!-- Row 5: Image & Expiry -->
    <div style="display: flex; gap: 10px;">
        <div style="flex: 1;">
            <img src="{row['image_url']}" class="med-image" alt="Medicine Image">
        </div>
        <div class="info-box" style="flex: 1; display: flex; flex-direction: column; justify-content: center;">
            <span class="info-label">Expiry Date</span>
            <span class="info-value">{row['expiry_date']}</span>
        </div>
    </div>

</div>
"""
                st.markdown(card_html, unsafe_allow_html=True)
                
                # Edit Button (Only show if we are in admin mode or single view? User said 'admin will just be there to inventory' implying admin button goes to inventory logic. 
                # Let's keep Edit button available in both single and full view for simplicity, as user requested "admin be aple to edit" previously).
                if st.button(f"Edit {row['name']}", key=f"btn_edit_{row['name']}"):
                    st.session_state['edit_item_name'] = row['name']
                    st.rerun()

    else:
        st.info("No medicine data available.")
        
    # --- Add Category Expander ---
    # Only show this if NOT in single view? Or always?
    # Usually "Add" is an admin function. If user just clicked 'Paracetamol', they probably just want to see details.
    # But adhering to 'admin will just be there to inventory', maybe the full inventory view IS the admin view.
    # So if single_view, hide 'add'?
    
    if not is_single_view:
        with st.expander("Add New Category / Medicine"):
            with st.form("new_med_form"):
                c1, c2 = st.columns(2)
                with c1:
                    new_name = st.text_input("Medicine Name")
                    new_cat = st.text_input("Category")
                    new_mg = st.text_input("Milligrams")
                    new_lots = st.number_input("Lots", min_value=0)
                with c2:
                    new_price = st.number_input("Price", min_value=0.0)
                    new_desc = st.text_area("Description")
                    new_expiry = st.text_input("Expiry Date (YYYY-MM-DD)")
                    new_img = st.text_input("Image URL", value="https://placehold.co/400")
                
                submitted = st.form_submit_button("Add Item")
                if submitted:
                     # Create new row
                    new_data = {
                        'name': new_name, 'category': new_cat, 'milligrams': new_mg,
                        'lots': new_lots, 'sold': 0, 'left': new_lots * 100, # Dummy logic
                        'description': new_desc, 'price': new_price, 
                        'lot_number': 'NEW', 'expiry_date': new_expiry, 'image_url': new_img
                    }
                    # Append
                    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
                    save_data(df)
                    st.success(f"Added {new_name}")
                    st.rerun()

# --- Main Routing ---
if st.session_state['page'] == 'home':
    render_home()
elif st.session_state['page'] == 'inventory':
    render_inventory()
