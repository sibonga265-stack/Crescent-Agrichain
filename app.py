# pip install streamlit web3 streamlit-js-eval

# ==========================================
# app.py
# ==========================================
import streamlit as st
import os
import json
import html
import base64
from datetime import datetime
from web3 import Web3
from streamlit_js_eval import streamlit_js_eval

# Import all configuration variables from our config file
from config import (
    APP_NAME, APP_TAGLINE, APP_DESCRIPTION, LOGO_PATH,
    SEPOLIA_RPC_URL, CONTRACT_ADDRESS, CONTRACT_ABI, ORDER_STATUS_LABELS
)

# Image shown on the login page only.
LOGIN_BANNER_PATH = "loginLogo.jpeg"
# Company details image shown on the homepage.
HOME_BANNER_PATH = r"C:\Users\User\.cursor\projects\c-Users-User-OneDrive-Desktop-CrescentAgriChain\assets\c__Users_User_AppData_Roaming_Cursor_User_workspaceStorage_980a708d9402a2090f2537220cef1f35_images_WhatsApp_Image_2026-04-28_at_14.03.42-5e875ebc-19be-4f7a-9c24-7cf139f274c3.png"

# --- SETUP & INITIALIZATION ---
# Connect to the Sepolia blockchain in read-only mode for querying data
w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC_URL))
# Load the smart contract object so we can interact with it
contract = w3.eth.contract(address=w3.to_checksum_address(CONTRACT_ADDRESS), abi=CONTRACT_ABI)
LISTING_LOCATION_FILE = "listing_locations.json"
DELISTED_LISTINGS_FILE = "farmer_delisted_listings.json"
ORDER_TRACKING_FILE = "order_tracking_details.json"

# Set up page configuration for Streamlit
st.set_page_config(page_title=APP_NAME, layout="wide", initial_sidebar_state="expanded")

# --- GLOBAL STYLES ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #c7d3c0;
    }
    .hero-title {
        text-align: center;
        color: #1f5e3b;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
        text-shadow: 0 2px 6px rgba(0, 0, 0, 0.5);
    }
    .hero-subtitle {
        text-align: center;
        color: #1f5e3b;
        font-size: 1.05rem;
        margin-bottom: 1.2rem;
        text-shadow: 0 2px 5px rgba(0, 0, 0, 0.5);
    }
    .info-card {
        background: #f6fbf7;
        border: 1px solid #d5eadb;
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 10px;
    }
    .focus-card {
        background: #ffffff;
        border: 1px solid #dceee3;
        border-left: 4px solid #2f8f53;
        border-radius: 10px;
        padding: 12px;
        min-height: 128px;
    }
    .focus-card h4 {
        color: #155c3b;
        margin: 0 0 6px 0;
        font-size: 1rem;
    }
    .focus-card p {
        margin: 0;
        color: #3d4a42;
        font-size: 0.92rem;
    }
    .login-title {
        text-align: center;
        color: #1f5e3b;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
        text-shadow: 0 2px 6px rgba(0, 0, 0, 0.5);
    }
    .login-subtitle {
        text-align: center;
        color: #1f5e3b;
        margin-bottom: 1rem;
        text-shadow: 0 2px 5px rgba(0, 0, 0, 0.5);
    }
    .login-card {
        background: #ffffff;
        border: 1px solid #dceee3;
        border-radius: 14px;
        padding: 12px 16px;
        box-shadow: 0 2px 8px rgba(10, 92, 54, 0.06);
    }
    section[data-testid="stSidebar"] {
        width: 320px !important;
        min-width: 320px !important;
        max-width: 320px !important;
        margin-left: -306px !important;
        transition: margin-left 0.25s ease;
        z-index: 1000;
    }
    section[data-testid="stSidebar"]:hover {
        margin-left: 0 !important;
    }
    [data-testid="stSidebar"]:has(:hover) {
        margin-left: 0 !important;
    }
    section[data-testid="stSidebar"] .stRadio > label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #2f5f46;
        letter-spacing: 0.02em;
        text-transform: uppercase;
    }
    section[data-testid="stSidebar"] [data-baseweb="radio"] {
        background: #f6fbf7;
        border: 1px solid #d5eadb;
        border-radius: 10px;
        margin-bottom: 6px;
        padding: 8px 10px;
    }
    section[data-testid="stSidebar"] * {
        color: #1f5e3b !important;
        text-shadow: none !important;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] h5,
    section[data-testid="stSidebar"] h6,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: #1f5e3b !important;
    }
    .market-card {
        background: #ffffff;
        border: 1px solid #dceee3;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 10px;
        min-height: 220px;
        box-shadow: 0 2px 8px rgba(10, 92, 54, 0.05);
    }
    .market-card h4 {
        margin: 0 0 8px 0;
        color: #155c3b;
        font-size: 1rem;
    }
    .market-card p {
        margin: 0 0 6px 0;
        color: #30433a;
        font-size: 0.9rem;
    }
    .product-box {
        background: #ffffff;
        border: 1px solid #dceee3;
        border-left: 4px solid #2f8f53;
        border-radius: 10px;
        padding: 10px 12px;
        margin-bottom: 10px;
        min-height: 170px;
        box-shadow: 0 2px 8px rgba(10, 92, 54, 0.05);
    }
    .product-box h4 {
        margin: 0 0 8px 0;
        color: #155c3b;
        font-size: 0.98rem;
    }
    .product-box p {
        margin: 0 0 6px 0;
        color: #30433a;
        font-size: 0.86rem;
    }
    .product-box-photo-wrap {
        background: #f0f4f1;
        border-radius: 8px;
        margin-bottom: 8px;
        overflow: hidden;
        min-height: 100px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .product-box-photo {
        width: 100%;
        max-height: 160px;
        object-fit: cover;
        display: block;
        vertical-align: middle;
    }
    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3,
    [data-testid="stAppViewContainer"] h4,
    [data-testid="stAppViewContainer"] h5,
    [data-testid="stAppViewContainer"] h6,
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] li,
    [data-testid="stAppViewContainer"] label,
    [data-testid="stAppViewContainer"] span,
    [data-testid="stAppViewContainer"] a {
        color: #1f5e3b;
    }
    [data-testid="stAppViewContainer"] a:hover,
    [data-testid="stAppViewContainer"] a:visited {
        color: #1f5e3b;
    }
    .stTextInput > label,
    .stNumberInput > label,
    .stSelectbox > label,
    .stRadio > label {
        color: #1f5e3b !important;
        font-weight: 700;
    }
    .stTextInput input,
    .stNumberInput input,
    .stSelectbox div[data-baseweb="select"] {
        background: rgba(255, 255, 255, 0.97) !important;
        color: #183c2a !important;
    }
    .info-card, .info-card *,
    .focus-card, .focus-card *,
    .login-card, .login-card *,
    .market-card, .market-card *,
    .product-box, .product-box *,
    [data-testid="stExpander"], [data-testid="stExpander"] *,
    [data-testid="stAlert"], [data-testid="stAlert"] *,
    [data-testid="metric-container"], [data-testid="metric-container"] *,
    [data-testid="stForm"], [data-testid="stForm"] * {
        color: #1f3f2e !important;
        text-shadow: none !important;
    }
    .info-card a, .info-card a:visited, .info-card a:hover,
    .focus-card a, .focus-card a:visited, .focus-card a:hover,
    .login-card a, .login-card a:visited, .login-card a:hover,
    .market-card a, .market-card a:visited, .market-card a:hover,
    .product-box a, .product-box a:visited, .product-box a:hover,
    [data-testid="stExpander"] a, [data-testid="stExpander"] a:visited, [data-testid="stExpander"] a:hover,
    [data-testid="stAlert"] a, [data-testid="stAlert"] a:visited, [data-testid="stAlert"] a:hover,
    [data-testid="metric-container"] a, [data-testid="metric-container"] a:visited, [data-testid="metric-container"] a:hover,
    [data-testid="stForm"] a, [data-testid="stForm"] a:visited, [data-testid="stForm"] a:hover {
        color: #1f3f2e !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- UI HEADER ---
def render_top_center_logo(width=260):
    """Renders logo in the visual center of the page."""
    if not os.path.exists(LOGO_PATH):
        return False
    left, center, right = st.columns([1, 2.6, 1])
    with center:
        st.image(LOGO_PATH, width=width)
    return True

def render_header(show_logo=True):
    """Renders the top header area of the application safely."""
    logo_rendered = False
    try:
        if show_logo and not render_top_center_logo(width=280):
            # Fallback to text title if the image is missing
            st.markdown(
                f"<h1 style='text-align: center; color: #000000; text-shadow: none;'>{APP_NAME}</h1>",
                unsafe_allow_html=True
            )
        elif show_logo:
            logo_rendered = True
    except Exception:
        # Silent fallback if anything goes wrong loading the image
        st.markdown(
            f"<h1 style='text-align: center; color: #000000; text-shadow: none;'>{APP_NAME}</h1>",
            unsafe_allow_html=True
        )

    # Keep tagline directly under logo with tight spacing.
    tagline_margin_top = "-8px" if logo_rendered else "0px"
    st.markdown(
        f"<p style='text-align: center; margin-top: {tagline_margin_top}; margin-bottom: 8px; font-weight: 600; color: #000000; text-shadow: none;'>{APP_TAGLINE}</p>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<p style='text-align: center; color: #000000; text-shadow: none;'>{APP_DESCRIPTION}</p>",
        unsafe_allow_html=True
    )
    st.divider()

def render_login_page():
    """Renders the login gateway page before loading the app."""
    render_top_center_logo(width=250)

    st.markdown("<div class='login-title'>Sign in to Crescent AgriChain</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='login-subtitle'>Secure access for partners, farmers, and retailers.</div>",
        unsafe_allow_html=True
    )

    banner_col, form_col = st.columns([1.3, 1])
    with banner_col:
        if os.path.exists(LOGIN_BANNER_PATH):
            _, login_logo_center, _ = st.columns([0.3, 5, 0.3])
            with login_logo_center:
                st.image(LOGIN_BANNER_PATH, use_container_width=True)
    with form_col:
        st.markdown("<div class='login-card'>", unsafe_allow_html=True)
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        remember_me = st.checkbox("Remember me on this device")
        login_clicked = st.button("Login", use_container_width=True, type="primary")

        st.caption("By logging in, you agree to Crescent AgriChain security and data policies.")
        st.markdown("</div>", unsafe_allow_html=True)

        if login_clicked:
            if not username.strip() or not password.strip():
                st.error("Please enter both username and password.")
            else:
                st.session_state.is_authenticated = True
                st.session_state.logged_in_user = username.strip()
                st.session_state.remember_me = remember_me
                st.success("Login successful. Redirecting to homepage...")
                st.rerun()

if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False

if not st.session_state.is_authenticated:
    render_login_page()
    st.stop()

render_header(show_logo=True)

# --- METAMASK WALLET CONNECTION ---
# We use session_state to remember if the user connected their wallet
if "wallet_address" not in st.session_state:
    st.session_state.wallet_address = None
if "wallet_error" not in st.session_state:
    st.session_state.wallet_error = None


def _set_wallet_from_response(account_value):
    """Validates and stores a wallet address returned from JS."""
    if not account_value:
        return False
    if isinstance(account_value, str) and account_value.startswith("ERROR:"):
        st.session_state.wallet_error = account_value.replace("ERROR:", "").strip()
        return False
    if account_value == "NO_METAMASK":
        st.session_state.wallet_error = "MetaMask is not detected in this browser."
        return False
    try:
        st.session_state.wallet_address = w3.to_checksum_address(account_value)
        st.session_state.wallet_error = None
        return True
    except Exception:
        st.session_state.wallet_error = "Invalid wallet address received from MetaMask."
        return False

# Passive background check to see if MetaMask is already connected
passive_check_js = (
    "window.ethereum "
    "? window.ethereum.request({method: 'eth_accounts'}).then(res => res[0]).catch(err => 'ERROR: ' + err.message) "
    ": 'NO_METAMASK'"
)
connected_account = streamlit_js_eval(js_expressions=passive_check_js, key="passive_wallet_check")

# Update session state based on the background check
if connected_account:
    _set_wallet_from_response(connected_account)

st.sidebar.header("Wallet Connection")
if st.session_state.wallet_address:
    st.sidebar.success(f"Connected: {st.session_state.wallet_address[:6]}...{st.session_state.wallet_address[-4:]}")
    if st.sidebar.button("Disconnect Wallet"):
        st.session_state.wallet_address = None
        st.session_state.wallet_error = None
        st.rerun()
else:
    st.sidebar.warning("Not Connected. Connect MetaMask to interact.")
    if st.session_state.wallet_error:
        st.sidebar.error(st.session_state.wallet_error)
    # Button to trigger the MetaMask popup if not passively connected
    if st.sidebar.button("Connect Wallet"):
        active_request_js = (
            "window.ethereum "
            "? window.ethereum.request({method: 'eth_requestAccounts'}).then(res => res[0]).catch(err => 'ERROR: ' + err.message) "
            ": 'NO_METAMASK'"
        )
        active_account = streamlit_js_eval(
            js_expressions=active_request_js,
            key=f"active_wallet_request_{os.urandom(4).hex()}"
        )
        if _set_wallet_from_response(active_account):
            st.sidebar.success("Wallet connected successfully.")
            st.rerun()
        elif not st.session_state.wallet_error:
            st.sidebar.info("Please approve the wallet connection in MetaMask and try again.")

# --- HELPER FUNCTIONS ---
def send_browser_transaction(func_name, args, value_wei=0):
    """Builds a transaction in Python and asks MetaMask (browser) to sign and send it."""
    if not st.session_state.wallet_address:
        st.error("Please connect your wallet first.")
        return

    try:
        # Prepare the data payload for the smart contract function
        try:
            # web3.py newer versions use snake_case ABI encoding.
            tx_data = contract.encode_abi(func_name, args=args)
        except Exception:
            # Fallback path for compatibility across web3.py versions.
            contract_function = getattr(contract.functions, func_name)(*args)
            tx_data = contract_function._encode_transaction_data()
        
        # Structure the transaction for MetaMask
        tx_params = {
            "to": CONTRACT_ADDRESS,
            "from": st.session_state.wallet_address,
            "data": tx_data,
            "value": hex(value_wei) # Value must be sent as a hex string to MetaMask
        }
        
        # Create a JavaScript snippet to send the transaction request to MetaMask
        js_code = f"""
        window.ethereum.request({{
            method: 'eth_sendTransaction',
            params: [{json.dumps(tx_params)}]
        }}).then(hash => hash).catch(err => 'ERROR: ' + err.message)
        """
        
        # Execute the JS in the browser
        tx_hash = streamlit_js_eval(js_expressions=js_code, key=f"tx_{func_name}_{os.urandom(4).hex()}")
        
        if tx_hash:
            if tx_hash.startswith("ERROR:"):
                st.error(f"Transaction failed or was cancelled: {tx_hash.replace('ERROR: ', '')}")
            else:
                st.success("Transaction submitted successfully!")
                st.markdown(f"[View on Sepolia Etherscan](https://sepolia.etherscan.io/tx/{tx_hash})")
                
    except Exception as e:
        st.error(f"An error occurred preparing the transaction: {str(e)}")

def get_produce_details(item_id):
    """Fetches a single item from the blockchain."""
    try:
        # Calls the 'listings' mapping on the contract
        data = contract.functions.listings(item_id).call()
        item = {
            "id": data[0],
            "farmer": data[1],
            "retailer": data[2],
            "item_type": data[3],
            "quantity": data[4],
            "price_wei": data[5],
            "delivery_date": data[6],
            "status": ORDER_STATUS_LABELS.get(data[7], "Unknown Status")
        }
        location_info = get_location_for_listing(item)
        item["province"] = location_info.get("province", "Not provided")
        item["address"] = location_info.get("address", "Not provided")
        item["image_b64"] = location_info.get("image_b64")
        item["image_mime"] = location_info.get("image_mime")
        item["image_name"] = location_info.get("image_name")
        return item
    except Exception:
        return None

def _load_listing_locations():
    """Loads off-chain listing location metadata from a local JSON file."""
    if not os.path.exists(LISTING_LOCATION_FILE):
        return []
    try:
        with open(LISTING_LOCATION_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
    except Exception:
        pass
    return []

def _save_listing_locations(records):
    """Persists off-chain listing location metadata to a local JSON file."""
    try:
        with open(LISTING_LOCATION_FILE, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)
    except Exception:
        # Non-blocking: app should keep working even if file writing fails.
        pass

def _encode_uploaded_image(uploaded_file):
    """Converts an uploaded image into JSON-safe metadata for local persistence."""
    if uploaded_file is None:
        return {"image_b64": None, "image_mime": None, "image_name": None}
    try:
        raw_bytes = uploaded_file.getvalue()
        if not raw_bytes:
            return {"image_b64": None, "image_mime": None, "image_name": None}
        return {
            "image_b64": base64.b64encode(raw_bytes).decode("ascii"),
            "image_mime": uploaded_file.type or "image/jpeg",
            "image_name": uploaded_file.name or "product-image",
        }
    except Exception:
        return {"image_b64": None, "image_mime": None, "image_name": None}

def save_pending_listing_location(farmer, item_type, quantity, price_wei, delivery_date, province, address, image_payload):
    """Stores location details for a listing submitted by the farmer."""
    records = _load_listing_locations()
    records.append({
        "listing_id": None,
        "farmer": farmer,
        "item_type": item_type,
        "quantity": int(quantity),
        "price_wei": str(price_wei),
        "delivery_date": int(delivery_date),
        "province": province.strip(),
        "address": address.strip(),
        "image_b64": image_payload.get("image_b64"),
        "image_mime": image_payload.get("image_mime"),
        "image_name": image_payload.get("image_name"),
        "created_at": datetime.utcnow().isoformat()
    })
    _save_listing_locations(records)

def get_location_for_listing(item):
    """Returns province/address for a listing by matching and then pinning listing_id."""
    records = _load_listing_locations()
    matched_record = None

    # First try direct lookup by listing_id.
    for record in records:
        if record.get("listing_id") == item["id"]:
            matched_record = record
            break

    # If not linked yet, match by listing details and link to listing_id.
    if not matched_record:
        for record in records:
            if (
                record.get("listing_id") is None
                and record.get("farmer") == item["farmer"]
                and record.get("item_type") == item["item_type"]
                and int(record.get("quantity", 0)) == int(item["quantity"])
                and int(record.get("delivery_date", 0)) == int(item["delivery_date"])
                and int(record.get("price_wei", 0)) == int(item["price_wei"])
            ):
                record["listing_id"] = item["id"]
                matched_record = record
                _save_listing_locations(records)
                break

    if matched_record:
        return {
            "province": matched_record.get("province", "Not provided"),
            "address": matched_record.get("address", "Not provided"),
            "image_b64": matched_record.get("image_b64"),
            "image_mime": matched_record.get("image_mime"),
            "image_name": matched_record.get("image_name"),
        }
    return {
        "province": "Not provided",
        "address": "Not provided",
        "image_b64": None,
        "image_mime": None,
        "image_name": None,
    }

def _load_delisted_records():
    """Farmer-initiated removals from this app's marketplace (pair listing_id + farmer)."""
    if not os.path.exists(DELISTED_LISTINGS_FILE):
        return []
    try:
        with open(DELISTED_LISTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
    except Exception:
        pass
    return []

def _save_delisted_records(records):
    try:
        with open(DELISTED_LISTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)
    except Exception:
        pass

def _delisted_listing_ids_validated():
    """IDs hidden from the marketplace: file entry must match on-chain farmer for that id."""
    validated = set()
    for rec in _load_delisted_records():
        lid = rec.get("listing_id")
        farmer = rec.get("farmer")
        if lid is None or not farmer:
            continue
        try:
            data = contract.functions.listings(int(lid)).call()
            chain_farmer = w3.to_checksum_address(data[1])
            if chain_farmer == w3.to_checksum_address(farmer):
                validated.add(int(lid))
        except Exception:
            continue
    return validated

def _purge_listing_location_for_id(listing_id):
    records = _load_listing_locations()
    new_recs = [r for r in records if r.get("listing_id") != int(listing_id)]
    if len(new_recs) != len(records):
        _save_listing_locations(new_recs)

def _delete_pending_listing_record(created_at, farmer_wallet):
    if not created_at or not farmer_wallet:
        return False
    fw = w3.to_checksum_address(farmer_wallet)
    records = _load_listing_locations()
    new_recs = []
    removed = False
    for r in records:
        if (
            r.get("created_at") == created_at
            and r.get("listing_id") is None
            and w3.to_checksum_address(r.get("farmer")) == fw
        ):
            removed = True
            continue
        new_recs.append(r)
    if removed:
        _save_listing_locations(new_recs)
    return removed

def register_farmer_delist(farmer_wallet, listing_id):
    """
    Removes local listing metadata and hides the listing from this app's marketplace.
    The on-chain record is unchanged (no cancel function on the deployed contract).
    """
    if not farmer_wallet:
        return False, "Connect your wallet first."
    try:
        data = contract.functions.listings(int(listing_id)).call()
    except Exception as e:
        return False, f"Could not read listing: {e}"
    chain_farmer = w3.to_checksum_address(data[1])
    wallet = w3.to_checksum_address(farmer_wallet)
    if chain_farmer != wallet:
        return False, "You can only delete your own listings."
    status = ORDER_STATUS_LABELS.get(data[7], "")
    if status != "Listed for Sale":
        return False, "Only listings that are still for sale can be removed here."
    records = _load_delisted_records()
    for r in records:
        try:
            if int(r.get("listing_id")) == int(listing_id) and w3.to_checksum_address(
                r.get("farmer")
            ) == wallet:
                _purge_listing_location_for_id(listing_id)
                return True, "Listing is already removed from the marketplace."
        except Exception:
            continue
    records.append(
        {
            "listing_id": int(listing_id),
            "farmer": wallet,
            "removed_at": datetime.utcnow().isoformat(),
        }
    )
    _save_delisted_records(records)
    _purge_listing_location_for_id(listing_id)
    return True, "Listing removed from the marketplace and local product details deleted."

def _load_order_tracking_records():
    """Buyer-side order metadata such as delivery address and ETA."""
    if not os.path.exists(ORDER_TRACKING_FILE):
        return []
    try:
        with open(ORDER_TRACKING_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
    except Exception:
        pass
    return []

def _save_order_tracking_records(records):
    try:
        with open(ORDER_TRACKING_FILE, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)
    except Exception:
        pass

def save_order_tracking_details(
    retailer_wallet,
    listing_id,
    customer_address,
    eta_date,
    item_type,
    bank_name=None,
    account_holder=None,
    account_number_last4=None,
):
    """Upserts order tracking details keyed by (listing_id, retailer)."""
    if not retailer_wallet:
        return
    try:
        retailer_chk = w3.to_checksum_address(retailer_wallet)
    except Exception:
        return

    records = _load_order_tracking_records()
    updated = False
    now_iso = datetime.utcnow().isoformat()
    for rec in records:
        try:
            same_pair = (
                int(rec.get("listing_id")) == int(listing_id)
                and w3.to_checksum_address(rec.get("retailer")) == retailer_chk
            )
        except Exception:
            same_pair = False
        if same_pair:
            rec["customer_address"] = (customer_address or "").strip()
            rec["eta_date"] = int(eta_date) if eta_date else None
            rec["item_type"] = item_type
            rec["bank_name"] = (bank_name or "").strip()
            rec["account_holder"] = (account_holder or "").strip()
            rec["account_number_last4"] = (account_number_last4 or "").strip()
            rec["updated_at"] = now_iso
            updated = True
            break
    if not updated:
        records.append(
            {
                "listing_id": int(listing_id),
                "retailer": retailer_chk,
                "customer_address": (customer_address or "").strip(),
                "eta_date": int(eta_date) if eta_date else None,
                "item_type": item_type,
                "bank_name": (bank_name or "").strip(),
                "account_holder": (account_holder or "").strip(),
                "account_number_last4": (account_number_last4 or "").strip(),
                "created_at": now_iso,
                "updated_at": now_iso,
            }
        )
    _save_order_tracking_records(records)

def get_order_tracking_details(retailer_wallet, listing_id):
    """Returns local buyer tracking details for a listing and wallet."""
    if not retailer_wallet:
        return {}
    try:
        retailer_chk = w3.to_checksum_address(retailer_wallet)
    except Exception:
        return {}
    for rec in _load_order_tracking_records():
        try:
            if (
                int(rec.get("listing_id")) == int(listing_id)
                and w3.to_checksum_address(rec.get("retailer")) == retailer_chk
            ):
                return rec
        except Exception:
            continue
    return {}

def _format_yyyymmdd(date_val):
    """Formats 20260503 into a readable date; returns fallback for invalid values."""
    try:
        raw = str(int(date_val))
        if len(raw) != 8:
            return "Not available"
        return datetime.strptime(raw, "%Y%m%d").strftime("%d %b %Y")
    except Exception:
        return "Not available"

# --- SIDEBAR NAVIGATION ---
st.sidebar.divider()
pages = [
    "📊 Dashboard Overview",
    "🌾 Farmer Portal",
    "🛒 Marketplace",
    "📦 Track Your Order",
    "🚚 Logistics Manager",
    "⚖️ Dispute Resolution",
    "⚙️ Settings"
]
selected_page = st.sidebar.radio("Navigation", pages)

# ==========================================
# PAGE: OVERVIEW & DASHBOARD
# ==========================================
if selected_page == "📊 Dashboard Overview":
    st.markdown("<div class='hero-title'>Welcome to Crescent AgriChain</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='hero-subtitle'>Building a sustainable, transparent, and farmer-first agriculture ecosystem.</div>",
        unsafe_allow_html=True
    )
    if os.path.exists(HOME_BANNER_PATH):
        _, home_logo_center, _ = st.columns([0.3, 5, 0.3])
        with home_logo_center:
            st.image(HOME_BANNER_PATH, use_container_width=True)
    else:
        st.warning("Company profile image not found. Please check the image path.")

    st.markdown(
        """
        <div class='info-card'>
        <strong>About Crescent AgriChain</strong><br>
        Crescent AgriChain is an agri-focused company committed to empowering farmers, strengthening rural trade,
        and delivering sustainable agricultural solutions through trusted partnerships and blockchain transparency.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### What We Focus On")
    fc1, fc2 = st.columns(2)
    with fc1:
        st.markdown(
            """
            <div class='focus-card'>
            <h4>Quality Agricultural Inputs</h4>
            <p>Supporting productivity with reliable seeds, fertilizers, and modern farming practices.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            """
            <div class='focus-card'>
            <h4>Farmer Empowerment</h4>
            <p>Helping farmers grow with market access, practical guidance, and fair opportunities.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with fc2:
        st.markdown(
            """
            <div class='focus-card'>
            <h4>Trade & Market Linkage</h4>
            <p>Connecting producers and retailers through transparent transactions and efficient coordination.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            """
            <div class='focus-card'>
            <h4>Sustainability at Heart</h4>
            <p>Promoting responsible agriculture that protects land, livelihoods, and long-term food security.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class='info-card'>
        <strong>Our Mission</strong><br>
        To empower farmers, support communities, and deliver sustainable agri-solutions for a better tomorrow.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()
    st.subheader("Platform Dashboard")
    st.info("Live marketplace snapshot from the blockchain.")
    
    with st.spinner("Fetching blockchain data..."):
        try:
            # Read operations to get high-level statistics
            total_items = contract.functions.produceCount().call()
            admin_address = contract.functions.admin().call()
            
            col1, col2 = st.columns(2)
            col1.metric("Total Produce Listed", total_items)
            col2.metric("Platform Administrator", f"{admin_address[:6]}...{admin_address[-4:]}")
            
            st.divider()
            st.write("### Recent Listings")
            if total_items == 0:
                st.write("No items have been listed on the platform yet.")
            else:
                delisted_ids = _delisted_listing_ids_validated()
                # Loop backwards to show the most recent items first (up to 5)
                for i in range(total_items, max(0, total_items - 5), -1):
                    if i in delisted_ids:
                        continue
                    item = get_produce_details(i)
                    if item:
                        with st.expander(f"Item #{item['id']}: {item['item_type']} - {item['status']}"):
                            st.write(f"**Farmer:** {item['farmer']}")
                            st.write(f"**Province:** {item['province']}")
                            st.write(f"**Address:** {item['address']}")
                            st.write(f"**Quantity:** {item['quantity']} units")
                            # Convert Wei (smallest Ethereum unit) back to Ether for readability
                            eth_price = w3.from_wei(item['price_wei'], 'ether')
                            st.write(f"**Price:** {eth_price} ETH")
                            
        except Exception as e:
            st.error(f"Failed to load dashboard data. Ensure the contract is deployed. Error: {str(e)}")

# ==========================================
# PAGE: FARMER PORTAL
# ==========================================
elif selected_page == "🌾 Farmer Portal":
    st.subheader("List New Produce")
    st.write("Farmers: Use this form to list your harvest on the blockchain.")
    
    with st.form("list_produce_form"):
        item_type = st.text_input("Produce Type", placeholder="e.g., Organic Apples")
        st.caption("Describe the agricultural product you are selling.")

        province = st.text_input("Province", placeholder="e.g., Eastern Cape")
        st.caption("Province where this produce is available.")

        address = st.text_input("Address", placeholder="e.g., 12 Farm Road, Mthatha")
        st.caption("Pick-up or farm address for this listing.")
        
        quantity = st.number_input("Quantity Available (units/kg)", min_value=1, step=1)
        st.caption("Total amount of produce ready for sale.")
        
        price_eth = st.number_input("Price for entire batch (in ETH)", min_value=0.0001, format="%.4f")
        st.caption("The total cost the retailer must pay into escrow.")
        
        delivery_date = st.number_input("Expected Delivery Date (YYYYMMDD)", min_value=20240101, step=1)
        st.caption("Estimated date when the goods will be ready for the retailer.")

        product_image = st.file_uploader(
            "Product Image (optional)",
            type=["png", "jpg", "jpeg", "webp"],
            help="Upload a clear picture so retailers can view your produce in the marketplace.",
        )
        st.caption("Accepted formats: PNG, JPG, JPEG, WEBP.")
        
        submit = st.form_submit_button("Publish Listing to Blockchain")
        
        if submit:
            if not st.session_state.wallet_address:
                st.error("Please connect your wallet first before publishing a listing.")
            else:
                # Convert the user-friendly ETH price into Wei for the smart contract
                price_wei = w3.to_wei(price_eth, 'ether')
                image_payload = _encode_uploaded_image(product_image)
                save_pending_listing_location(
                    st.session_state.wallet_address,
                    item_type,
                    quantity,
                    price_wei,
                    delivery_date,
                    province,
                    address,
                    image_payload,
                )
                # Pass arguments in the exact order the Solidity function expects
                send_browser_transaction("listProduce", [item_type, int(quantity), price_wei, int(delivery_date)])

    st.divider()
    st.subheader("Your listings")
    st.caption(
        "Remove a listing from this marketplace and delete saved photos and address data. "
        "The on-chain listing remains; retailers using other tools could still interact with it until the contract supports cancel."
    )
    _portal_flash = st.session_state.pop("_farmer_portal_flash", None)
    if _portal_flash:
        if _portal_flash[0] == "ok":
            st.success(_portal_flash[1])
        else:
            st.error(_portal_flash[1])

    if not st.session_state.wallet_address:
        st.info("Connect your wallet to manage your produce.")
    else:
        wallet_chk = w3.to_checksum_address(st.session_state.wallet_address)
        pending_records = [
            r
            for r in _load_listing_locations()
            if r.get("listing_id") is None
            and r.get("farmer")
            and w3.to_checksum_address(r.get("farmer")) == wallet_chk
        ]
        if pending_records:
            st.markdown("**Draft listings** (saved locally before the chain transaction confirms)")
            for pend_idx, pr in enumerate(pending_records):
                ct = pr.get("created_at") or ""
                with st.container():
                    c1, c2 = st.columns([4, 1])
                    with c1:
                        st.write(
                            f"**{html.escape(str(pr.get('item_type') or ''))}** — "
                            f"{pr.get('quantity')} units, delivery {pr.get('delivery_date')}"
                        )
                    with c2:
                        if st.button("Remove draft", key=f"pending_del_{pend_idx}_{ct}"):
                            if _delete_pending_listing_record(ct, st.session_state.wallet_address):
                                st.session_state["_farmer_portal_flash"] = ("ok", "Draft removed.")
                            else:
                                st.session_state["_farmer_portal_flash"] = (
                                    "err",
                                    "Could not remove that draft.",
                                )
                            st.rerun()
            st.divider()

        try:
            delisted_ids = _delisted_listing_ids_validated()
            total_on_chain = contract.functions.produceCount().call()
            my_active = []
            for i in range(1, int(total_on_chain) + 1):
                if i in delisted_ids:
                    continue
                data = contract.functions.listings(i).call()
                if w3.to_checksum_address(data[1]) != wallet_chk:
                    continue
                if ORDER_STATUS_LABELS.get(data[7]) != "Listed for Sale":
                    continue
                my_active.append(get_produce_details(i))
            my_active = [x for x in my_active if x]
            if not my_active:
                st.info("You have no active listings on the marketplace.")
            else:
                for item in my_active:
                    with st.container():
                        row_a, row_b = st.columns([4, 1])
                        with row_a:
                            st.markdown(
                                f"**#{item['id']} — {html.escape(str(item.get('item_type') or ''))}**  \n"
                                f"{item.get('quantity')} units · "
                                f"{w3.from_wei(item['price_wei'], 'ether')} ETH · "
                                f"{html.escape(str(item.get('province') or ''))}"
                            )
                        with row_b:
                            if st.button("Delete", key=f"farmer_delist_{item['id']}"):
                                ok, msg = register_farmer_delist(
                                    st.session_state.wallet_address, item["id"]
                                )
                                st.session_state["_farmer_portal_flash"] = (
                                    "ok" if ok else "err",
                                    msg,
                                )
                                st.rerun()
        except Exception as e:
            st.error(f"Could not load your listings: {e}")

# ==========================================
# PAGE: MARKETPLACE
# ==========================================
elif selected_page == "🛒 Marketplace":
    st.subheader("Retailer Marketplace")
    st.write("Retailers: Browse available produce and secure them in escrow.")

    st.write("### Available Produce")
    product_cards = []
    try:
        with st.spinner("Loading available listings..."):
            total_items = contract.functions.produceCount().call()
            if total_items == 0:
                st.info("No produce is currently listed.")
            else:
                delisted_ids = _delisted_listing_ids_validated()
                for i in range(1, total_items + 1):
                    if i in delisted_ids:
                        continue
                    item = get_produce_details(i)
                    if item and item["status"] == "Listed for Sale":
                        product_cards.append(item)
                if not product_cards:
                    st.info("No currently available produce found.")
    except Exception as e:
        st.error(f"Could not load marketplace listings. Error: {str(e)}")

    if product_cards:
        if "pending_checkout_listing_id" not in st.session_state:
            st.session_state.pending_checkout_listing_id = None

        pending_checkout_listing = None
        pending_checkout_id = st.session_state.pending_checkout_listing_id
        if pending_checkout_id is not None:
            for card in product_cards:
                if int(card["id"]) == int(pending_checkout_id):
                    pending_checkout_listing = card
                    break

        if pending_checkout_id is not None and pending_checkout_listing is None:
            st.session_state.pending_checkout_listing_id = None

        if pending_checkout_listing:
            st.markdown("### Secure Checkout Portal")
            st.info(
                "Complete your bank and delivery details below, then lock this order in escrow."
            )
            with st.container():
                st.markdown(
                    f"""
                    <div class='market-card'>
                    <h4>Selected Product: #{pending_checkout_listing['id']} - {html.escape(str(pending_checkout_listing.get('item_type') or ''))}</h4>
                    <p><strong>Quantity:</strong> {pending_checkout_listing.get('quantity')} units</p>
                    <p><strong>Province:</strong> {html.escape(str(pending_checkout_listing.get('province') or ''))}</p>
                    <p><strong>Address:</strong> {html.escape(str(pending_checkout_listing.get('address') or ''))}</p>
                    <p><strong>Escrow Amount:</strong> {w3.from_wei(pending_checkout_listing['price_wei'], 'ether')} ETH</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with st.form(f"checkout_portal_form_{pending_checkout_listing['id']}"):
                st.markdown("#### Bank Details")
                bank_name = st.text_input("Bank name", placeholder="e.g., Crescent National Bank")
                account_holder = st.text_input(
                    "Account holder full name", placeholder="e.g., Jane Doe"
                )
                account_number = st.text_input(
                    "Bank account number", placeholder="e.g., 0123456789"
                )
                st.markdown("#### Home Address")
                home_address = st.text_area(
                    "Delivery home address",
                    placeholder="e.g., 45 Rosebank Ave, Johannesburg",
                )
                place_order = st.form_submit_button(
                    "Confirm secure order & lock escrow", type="primary"
                )

                if place_order:
                    if not st.session_state.wallet_address:
                        st.error("Please connect your wallet first.")
                    elif (
                        not bank_name.strip()
                        or not account_holder.strip()
                        or not account_number.strip()
                        or not home_address.strip()
                    ):
                        st.error("Please complete all bank details and your home address.")
                    else:
                        account_digits = "".join(ch for ch in account_number if ch.isdigit())
                        if len(account_digits) < 4:
                            st.error("Please enter a valid bank account number.")
                        else:
                            save_order_tracking_details(
                                st.session_state.wallet_address,
                                pending_checkout_listing["id"],
                                home_address,
                                pending_checkout_listing.get("delivery_date"),
                                pending_checkout_listing.get("item_type"),
                                bank_name=bank_name,
                                account_holder=account_holder,
                                account_number_last4=account_digits[-4:],
                            )
                            send_browser_transaction(
                                "placeOrder",
                                [pending_checkout_listing["id"]],
                                value_wei=pending_checkout_listing["price_wei"],
                            )
                            st.session_state.pending_checkout_listing_id = None
                            st.success(
                                "Order submitted. Your home address was saved and will be used in Track Your Order."
                            )
                            st.rerun()

            if st.button("Cancel checkout", key=f"cancel_checkout_{pending_checkout_listing['id']}"):
                st.session_state.pending_checkout_listing_id = None
                st.rerun()

            st.divider()

        st.markdown(
            "<div style='font-weight: 800; font-size: 1.05rem; margin-bottom: 0.2rem;'>Search produce</div>",
            unsafe_allow_html=True,
        )
        search_q = st.text_input(
            "Search produce",
            placeholder="Filter by name, province, address, farmer, or listing ID…",
            key="marketplace_search",
            label_visibility="collapsed",
        ).strip().lower()

        if search_q:
            def _listing_matches_search(p):
                blob = " ".join(
                    [
                        str(p["id"]),
                        str(p.get("item_type") or ""),
                        str(p.get("province") or ""),
                        str(p.get("address") or ""),
                        str(p.get("farmer") or ""),
                    ]
                ).lower()
                return search_q in blob

            filtered_cards = [p for p in product_cards if _listing_matches_search(p)]
        else:
            filtered_cards = product_cards

        if not filtered_cards:
            st.warning("No listings match your search.")
        else:
            for start in range(0, len(filtered_cards), 3):
                row_items = filtered_cards[start : start + 3]
                cols = st.columns(3)
                for idx, product in enumerate(row_items):
                    with cols[idx]:
                        price_eth = w3.from_wei(product["price_wei"], "ether")
                        title = html.escape(f"#{product['id']} - {product['item_type']}")
                        province = html.escape(str(product.get("province") or ""))
                        status = html.escape(str(product.get("status") or ""))
                        image_b64 = product.get("image_b64")
                        image_mime = (product.get("image_mime") or "image/jpeg").strip() or "image/jpeg"
                        if image_b64:
                            try:
                                base64.b64decode(image_b64, validate=True)
                                safe_mime = html.escape(image_mime, quote=True)
                                data_src = f"data:{safe_mime};base64,{image_b64}"
                                image_html = (
                                    f"<div class='product-box-photo-wrap'>"
                                    f"<img class='product-box-photo' src='{data_src}' alt='' />"
                                    f"</div>"
                                )
                            except Exception:
                                image_html = (
                                    "<div class='product-box-photo-wrap'>"
                                    "<p style='margin:0;font-size:0.85rem;color:#6b7a72;'>Photo unavailable</p>"
                                    "</div>"
                                )
                        else:
                            image_html = (
                                "<div class='product-box-photo-wrap' style='min-height:72px;'>"
                                "<p style='margin:0;font-size:0.85rem;color:#6b7a72;'>No photo</p>"
                                "</div>"
                            )
                        st.markdown(
                            f"""
                            <div class='product-box'>
                            {image_html}
                            <h4>{title}</h4>
                            <p><strong>Qty:</strong> {product['quantity']} units</p>
                            <p><strong>Province:</strong> {province}</p>
                            <p><strong>Price:</strong> {price_eth} ETH</p>
                            <p><strong>Status:</strong> {status}</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        if st.button(
                            "Secure order & lock escrow",
                            key=f"marketplace_buy_{product['id']}",
                            use_container_width=True,
                        ):
                            if not st.session_state.wallet_address:
                                st.error("Please connect your wallet first.")
                                continue
                            st.session_state.pending_checkout_listing_id = product["id"]
                            st.rerun()

# ==========================================
# PAGE: TRACK YOUR ORDER
# ==========================================
elif selected_page == "📦 Track Your Order":
    st.subheader("Track Your Order")
    st.write("Customers: View your purchased orders, expected arrival date, and delivery address.")

    if not st.session_state.wallet_address:
        st.info("Please connect your wallet to view your orders.")
    else:
        wallet_chk = w3.to_checksum_address(st.session_state.wallet_address)
        order_rows = []
        try:
            with st.spinner("Loading your orders..."):
                total_items = contract.functions.produceCount().call()
                for i in range(1, int(total_items) + 1):
                    item = get_produce_details(i)
                    if not item:
                        continue
                    try:
                        retailer_chk = w3.to_checksum_address(item.get("retailer"))
                    except Exception:
                        continue
                    if retailer_chk != wallet_chk:
                        continue
                    if item.get("status") == "Listed for Sale":
                        continue
                    local = get_order_tracking_details(st.session_state.wallet_address, item["id"])
                    eta_raw = local.get("eta_date") or item.get("delivery_date")
                    eta_display = _format_yyyymmdd(eta_raw)
                    customer_address = local.get("customer_address") or "Not provided"
                    order_rows.append(
                        {
                            "id": item["id"],
                            "item_type": item.get("item_type"),
                            "quantity": item.get("quantity"),
                            "price_eth": w3.from_wei(item["price_wei"], "ether"),
                            "status": item.get("status"),
                            "eta_display": eta_display,
                            "customer_address": customer_address,
                        }
                    )
        except Exception as e:
            st.error(f"Could not load your orders: {e}")
            order_rows = []

        if not order_rows:
            st.info("No purchased orders found for this wallet yet.")
        else:
            for row in order_rows:
                st.markdown(
                    f"""
                    <div class='market-card'>
                    <h4>Order #{row['id']} - {html.escape(str(row.get('item_type') or ''))}</h4>
                    <p><strong>Quantity:</strong> {row.get('quantity')} units</p>
                    <p><strong>Price Paid:</strong> {row.get('price_eth')} ETH</p>
                    <p><strong>Status:</strong> {html.escape(str(row.get('status') or ''))}</p>
                    <p><strong>Estimated Arrival:</strong> {html.escape(str(row.get('eta_display') or 'Not available'))}</p>
                    <p><strong>Customer Address:</strong> {html.escape(str(row.get('customer_address') or 'Not provided'))}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

# ==========================================
# PAGE: LOGISTICS MANAGER
# ==========================================
elif selected_page == "🚚 Logistics Manager":
    st.subheader("Logistics & Delivery Tracking")
    st.write("Crescent Movers & Retailers: Update the physical location of goods.")
    
    action = st.radio("Select Action", ["Mark as 'In Transit'", "Confirm Final Delivery"])
    
    item_id = st.number_input("Produce ID", min_value=1, step=1)
    st.caption("Enter the ID of the order you are updating.")
    
    if action == "Mark as 'In Transit'":
        st.write("*(Admin Only)* Collect goods from farmer and begin transport.")
        if st.button("Update Status to In Transit"):
            send_browser_transaction("startTransport", [item_id])
            
    elif action == "Confirm Final Delivery":
        st.write("*(Admin or Retailer)* Goods have arrived safely. **This will auto-release payment to the farmer.**")
        if st.button("Confirm Delivery & Release Escrow"):
            send_browser_transaction("confirmDelivery", [item_id])

# ==========================================
# PAGE: DISPUTE RESOLUTION
# ==========================================
elif selected_page == "⚖️ Dispute Resolution":
    st.subheader("Dispute Management")
    st.write("Manage issues regarding quality, missing deliveries, or payment conflicts.")
    
    st.write("### 1. Raise a Dispute")
    st.write("Freeze an order's status if a problem occurs.")
    dispute_id = st.number_input("Produce ID to Dispute", min_value=1, step=1, key="raise_disp")
    if st.button("Halt Order & Raise Dispute"):
        send_browser_transaction("raiseDispute", [dispute_id])
        
    st.divider()
    
    st.write("### 2. Resolve a Dispute (Admin Only)")
    st.write("Decide where the escrowed funds should go after an investigation.")
    resolve_id = st.number_input("Disputed Produce ID", min_value=1, step=1, key="res_disp")
    resolution_choice = st.selectbox("Resolution Outcome", ["Refund the Retailer", "Pay the Farmer"])
    
    if st.button("Execute Resolution & Close Dispute"):
        # Convert English dropdown choice to the boolean expected by the smart contract
        refund_retailer = True if resolution_choice == "Refund the Retailer" else False
        send_browser_transaction("resolveDispute", [resolve_id, refund_retailer])

# ==========================================
# PAGE: SETTINGS
# ==========================================
elif selected_page == "⚙️ Settings":
    st.subheader("Platform Settings")
    st.write("Manage basic application preferences and account session controls.")

    st.write("### Profile")
    st.text_input("Display Name", value=st.session_state.get("logged_in_user", "User"))
    st.text_input("Email Address", placeholder="name@company.com")

    st.write("### Preferences")
    st.toggle("Enable notifications", value=True)
    st.toggle("Compact dashboard view", value=False)
    st.selectbox("Default landing section", ["Dashboard Overview", "Marketplace", "Farmer Portal"])

    st.write("### Security")
    st.caption("These controls are UI placeholders for now and can be connected later.")
    st.button("Change Password")
    if st.button("Log Out"):
        st.session_state.is_authenticated = False
        st.session_state.wallet_address = None
        st.rerun()